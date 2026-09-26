"""Cross-lane consumer transactions and source-owned output expectations."""
import json
import tarfile
import unittest
from unittest.mock import patch

from catalog import foundation as f
from catalog.behavior_sources import import_behavior
from catalog.consumers import ConsumerCatalog, ConsumerSession, import_mappings, validate_mappings
from catalog.evaluator import EvaluationError


class ConsumerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = f.connect(':memory:')
        f.create_schema(cls.db)
        import_behavior(cls.db)
        import_mappings(cls.db)
        cls.catalogs = {key: ConsumerCatalog(cls.db, rev) for key,rev in cls.db.execute('''
            SELECT model_key,revision_id FROM catalog_revision JOIN model_year USING(model_year_id) JOIN model USING(model_id)''')}

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    def oid(self, cat, code):
        row, = [r for r in cat.ev.options.values() if r['rpo'] == code and r['lifecycle'] == 'active']
        return row['id']

    def commit(self, session, action, target=None):
        p = session.preview(action, target, session.version)
        return session.confirm(p['token'], p['warning_sha256'], p['version'])

    def test_complete_mappings_and_source_routes(self):
        validate_mappings(self.db)
        counts = {kind: self.db.execute('SELECT count(*) FROM consumer_' + kind).fetchone()[0]
                  for kind in ('option','configuration','interior','option_context')}
        self.assertEqual(counts, dict(option=1388, configuration=32, interior=704, option_context=7498))
        for key,cat in self.catalogs.items():
            data = json.loads((f.ROOT / 'docs' / (key.replace('_','-') + '-structured-records.json')).read_text())
            rows=data['baseline_rows']
            self.assertEqual(cat.model['presentation']['runtime_steps'], rows['runtime_steps'])
            self.assertEqual(cat.model['presentation']['order_summary_sections'], rows['order_summary_sections'])
            for row in rows[data['sheet_roles']['options']]:
                self.assertEqual(cat.maps['option'][row['option_id']]['key'], row['option_id'])
            for cfg in cat.ev.configs:
                for row in rows[data['sheet_roles']['options']]:
                    oid=row['option_id']
                    override=next((o for o in rows[data['sheet_roles']['variant_overrides']] if o['option_id']==oid and o['variant_id']==cfg and str(o['active']).lower()=='true'),{})
                    self.assertEqual(cat.contexts[oid,cfg]['section_id'], override.get('section_id') or row['section_id'])

    def test_card_photos_match_the_existing_runtime(self):
        fields = ('image_url', 'image_alt', 'image_fit', 'image_position')
        with tarfile.open(f.ROOT / 'baselines/2026-09-06/workbook-runtime.tar.gz') as baseline:
            registry = baseline.extractfile('form-app/data.js').read().decode()
            for key, cat in self.catalogs.items():
                with self.subTest(model=key):
                    runtime = json.load(baseline.extractfile(f'form-output/runtime/{key.replace("_", "-")}-runtime-contract.json'))
                    assets = cat.model['presentation']['asset_map']
                    # Every option photo the existing form shows, for options this catalog offers.
                    expected = {c['option_id']: {k: c[k] for k in fields} for c in runtime['choices']
                                if c.get('image_url') and c['option_id'] in cat.ev.options}
                    actual = {r['target_id']: {k: r[k] for k in fields} for r in assets
                              if r['target_type'] == 'option' and r['target_id'] in cat.ev.options}
                    # Two photos belong to options the existing runtime never lists:
                    # ZR1 EFR is hidden everywhere, and GSX R88 is factory-unavailable,
                    # which this form shows as a visible, unselectable card.
                    extra = actual.keys() - expected.keys()
                    self.assertEqual({cat.ev.options[k]['rpo'] for k in extra},
                                     {'grand_sport_x': {'R88'}, 'zr1': {'EFR'}}.get(key, set()))
                    self.assertEqual({k: v for k, v in actual.items() if k not in extra}, expected)
                    body = {c['context_choice_id']: (c['image_url'], c.get('hover_image_url')) for c in runtime['contextChoices'] if c.get('image_url')}
                    self.assertEqual({r['target_id']: (r['image_url'], r['hover_image_url']) for r in assets
                                      if r['target_type'] == 'context_choice'}, body)
                    photo, = [r['image_url'] for r in assets if r['target_type'] == 'model']
                    self.assertIn(json.dumps(photo), registry)

    def test_card_price_change_matches_confirmed_preview(self):
        # The UI quotes the complete transition, including package consequences,
        # rather than treating an option's list price as the build price delta.
        for key, cat in self.catalogs.items():
            with self.subTest(model=key):
                cfg = next(iter(cat.ev.configs))
                session = ConsumerSession(cat, cfg, 'local-test')
                cards = cat.cards(session._session.state)['options']
                for card in cards:
                    if not card['selectable']:
                        self.assertIsNone(card['delta_minor'])
                choice = next(c for c in cards if c['selectable'] and not c['selected'] and c['delta_minor'])
                preview = session.preview('select', choice['option_id'], session.version)
                self.assertEqual(choice['delta_minor'], preview['warning']['changes']['delta_minor'])
                before = session.current()['build']['total_minor']
                after = session.confirm(preview['token'], preview['warning_sha256'], preview['version'])
                self.assertEqual(after['build']['total_minor'] - before, choice['delta_minor'])
                selected = next(c for c in cat.cards(session._session.state)['options']
                                if c['option_id'] == choice['option_id'])
                removal = session.preview('remove', choice['option_id'], session.version)
                self.assertEqual(selected['delta_minor'], removal['warning']['changes']['delta_minor'])

    def test_missing_mapping_fails(self):
        self.db.execute('SAVEPOINT missing')
        try:
            self.db.execute('DELETE FROM consumer_option_context WHERE rowid=(SELECT min(rowid) FROM consumer_option_context)')
            with self.assertRaisesRegex(ValueError,'Missing option context'):
                validate_mappings(self.db)
        finally:
            self.db.execute('ROLLBACK TO missing');self.db.execute('RELEASE missing')

    def test_model_contract_retains_source_display_order(self):
        contracts = {key: cat.contract() for key, cat in self.catalogs.items()}
        # HTTP encoding sorts object keys; consumers must use the source order.
        decoded = json.loads(json.dumps(contracts, sort_keys=True))
        self.assertEqual(sorted(decoded, key=lambda key: decoded[key]['display_order']),
                         ['stingray', 'grand_sport', 'grand_sport_x', 'z06', 'zr1', 'zr1x'])
        for key, contract in decoded.items():
            rows = json.loads((f.ROOT / 'docs' / (key.replace('_', '-') + '-structured-records.json')).read_text())['baseline_rows']
            self.assertEqual(contract['display_order'], rows['model_registry_promotion'][0]['display_order'])

    def test_interior_labels_are_readable_without_changing_scoped_identities(self):
        seen = set()
        for key, cat in self.catalogs.items():
            for cfg in cat.ev.configs:
                cards = cat.cards(cat.ev.state(cfg))['interiors']
                self.assertEqual({card['interior_id'] for card in cards},
                                 {iid for iid, cid in cat.ev.interior_scopes if cid == cfg})
                for card in cards:
                    iid = card['interior_id']
                    seen.add((key, iid))
                    self.assertNotIn('[', card['label'])
                    self.assertNotIn('"', card['label'])
                    levels = json.loads(cat.maps['interior'][iid]['hierarchy']['interior_hierarchy_levels'])
                    self.assertEqual(card['label'].split(' › '), levels)
        self.assertEqual(len(seen), 704)
        for key, cfg, iid, expected in (
            ('stingray', '1lt_c07', '1LT_AQ9_HTA', '1LT › AQ9 GT1 Bucket Seats › HTA Jet Black'),
            ('z06', '1lz_h67', '1LZ_AQ9_HTA', '1LZ › AQ9 Seats › Jet Black › Mulan leather seating surfaces with perforated inserts › Jet Black'),
        ):
            cat = self.catalogs[key]
            labels = {c['interior_id']: c['label'] for c in cat.cards(cat.ev.state(cfg))['interiors']}
            self.assertEqual(labels[iid], expected)

    def test_both_stripe_directions_all_gsx_z06_configurations(self):
        for key in ('grand_sport_x','z06'):
            c=self.catalogs[key]
            for cfg in c.ev.configs:
                for badge in ('VPW','VPO'):
                    for first,second in (('DPB',badge),(badge,'DPB')):
                        with self.subTest(key=key,cfg=cfg,first=first,second=second):
                            s=ConsumerSession(c,cfg,'release')
                            self.commit(s,'select',self.oid(c,'GBA'))
                            self.commit(s,'select',self.oid(c,first))
                            before=s.current()
                            p=s.preview('select',self.oid(c,second),s.version)
                            w=p['warning'];removed={i['rpo'] for i in w['changes']['removed']}
                            self.assertIn(first,removed)
                            self.assertEqual(before['build'],s.current()['build'])
                            self.assertTrue(any('Remove: '+first in line for line in w['lines']))
                            with self.assertRaises(EvaluationError):s.order()
                            s.cancel(s.version)
                            self.assertEqual(before,s.current())
                            with self.assertRaises(EvaluationError):s.confirm(p['token'],p['warning_sha256'],p['version'])
                            p=s.preview('select',self.oid(c,second),s.version)
                            result=s.confirm(p['token'],p['warning_sha256'],p['version'])
                            self.assertEqual(result['build'],p['warning']['candidate'])
                            self.assertNotIn(self.oid(c,first),[i['option_id'] for i in result['build']['resolved']])
                            undo=s.preview('revert',None,s.version)
                            self.assertEqual(result['build'],s.current()['build'])
                            self.assertTrue(before['revertible'])
                            s.confirm(undo['token'],undo['warning_sha256'],undo['version'])
                            self.assertEqual(before['build'],s.current()['build'])
                            self.assertFalse(s.current()['revertible'])
                            with self.assertRaises(EvaluationError):s.preview('revert',None,s.version)

    def test_every_lane_roof_dependency_warning_and_charge_restoration(self):
        for c in self.catalogs.values():
            for cfg,config in c.ev.configs.items():
                if config['body']!='coupe':continue
                s=ConsumerSession(c,cfg,'release')
                for code in ('GBA','SC7','SBT'):self.commit(s,'select',self.oid(c,code))
                before=s.current()['build']
                p=s.preview('remove',self.oid(c,'SC7'),s.version)
                self.assertTrue({'SBT','SC7'} <= {i['rpo'] for i in p['warning']['changes']['removed']})
                self.assertEqual(p['warning']['changes']['delta_minor'],-252500)
                self.assertTrue(p['warning']['changes']['causes_removed'])
                self.assertTrue(p['warning']['changes']['charge_changes'])
                s.confirm(p['token'],p['warning_sha256'],p['version'])
                self.commit(s,'revert')
                self.assertEqual(before,s.current()['build'])

    def test_hash_first_uses_exact_accepted_disclosure(self):
        for key in ('grand_sport','grand_sport_x'):
            c=self.catalogs[key];cfg=next(iter(c.ev.configs));s=ConsumerSession(c,cfg,'release')
            p=s.preview('select',self.oid(c,'97A'),0)
            self.assertIn('Selecting this hash mark adds the Grand Sport Heritage Package (Z15) for $995.',p['warning']['lines'])
            self.assertIn('Z15',{i['rpo'] for i in p['warning']['changes']['added']})

    def test_confirmation_tokens_cannot_commit_foreign_stale_tampered_or_replayed_changes(self):
        c=self.catalogs['stingray'];cfg=next(iter(c.ev.configs));a=ConsumerSession(c,cfg,'r');b=ConsumerSession(c,cfg,'r')
        p=a.preview('select',self.oid(c,'GBA'),0)
        before=a.current()['build']
        for session,token,hash_,version in ((a,None,p['warning_sha256'],0),(b,p['token'],p['warning_sha256'],0),
                                            (a,p['token'],'tampered',0),(a,p['token'],p['warning_sha256'],1)):
            with self.assertRaises(EvaluationError):session.confirm(token,hash_,version)
        self.assertEqual(before,a.current()['build'])
        p2=a.preview('select',self.oid(c,'G8G'),0)
        with self.assertRaises(EvaluationError):a.confirm(p['token'],p['warning_sha256'],0)
        a.confirm(p2['token'],p2['warning_sha256'],0)
        with self.assertRaises(EvaluationError):a.confirm(p2['token'],p2['warning_sha256'],0)
        p=a.preview('select',self.oid(c,'GBA'),1)
        with self.assertRaises(EvaluationError):a.preview('select','not-an-option',1)
        with self.assertRaises(EvaluationError):a.confirm(p['token'],p['warning_sha256'],1)

    def test_interior_clear_warning_all_lanes(self):
        for c in self.catalogs.values():
            cfg=next(iter(c.ev.configs));s=ConsumerSession(c,cfg,'release')
            # Plain source leaf without paint prerequisites.
            iid=next(i for i,row in c.ev.interiors.items() if (i,cfg) in c.ev.interior_scopes and 'AE4_HTJ_N26' in i)
            self.commit(s,'select',self.oid(c,'GBA'));self.commit(s,'interior',iid)
            p=s.preview('remove',c.ev.interiors[iid]['seat_option_id'],s.version)
            self.assertEqual(p['warning']['changes']['interior'],{'before':iid,'after':None})
            self.assertTrue(any(line.startswith('Interior:') and iid in line for line in p['warning']['lines']))
            s.confirm(p['token'],p['warning_sha256'],p['version'])
            with self.assertRaisesRegex(EvaluationError,'Complete required'):s.order()

    def test_equipment_code_projection_honors_substitution(self):
        c=self.catalogs['stingray'];s=ConsumerSession(c,'2lt_c07','release')
        self.commit(s,'select',self.oid(c,'GBA'))
        self.commit(s,'select',self.oid(c,'Z51'))
        b=s.current()['build']
        codes={i['rpo'] for i in b['order_codes']}
        self.assertIn('J55',codes);self.assertNotIn('JL9',codes)
        self.assertIn('JL9',{i['rpo'] for i in b['informational_standard_equipment']})
        self.assertEqual(b['visualizer']['installed_option_ids'],sorted(i['option_id'] for i in b['installed_equipment']))
        self.assertEqual(b['visualizer']['release_id'],b['release_id'])

    def test_step_pricing_matches_full_pricing(self):
        for key, c in self.catalogs.items():
            for cfg in sorted(c.ev.configs)[:2]:
                with self.subTest(model=key, configuration=cfg):
                    state = c.ev.state(cfg); full = c.cards(state)['options']
                    shown = [x for x in full if c.ev.options[x['option_id']]['customer_selectable']]
                    expected = list({x['step_key']: x['section_label'] for x in reversed(shown)}.items())[::-1]
                    steps = c.card_steps(cfg)
                    self.assertEqual(sorted((s['step_key'], s['section_label']) for s in steps), sorted(expected))
                    self.assertEqual([s['step_key'] for s in steps], list(dict.fromkeys(x['step_key'] for x in shown)))
                    for step in {x['step_key'] for x in full}:
                        self.assertEqual(c.cards(state, [step])['options'], [x for x in full if x['step_key'] == step])
                    self.assertEqual(c.cards(state, [])['options'], [])

    def test_corrected_copy_and_disabled_unavailable_cards(self):
        c=self.catalogs['grand_sport_x'];hp=self.oid(c,'HP1')
        self.assertEqual(c.maps['option'][hp]['description'],'Electrified front axle: 186 hp (138.7 kW), 145 lb-ft of front torque (196.6 N-m).')
        for c in self.catalogs.values():
            cfg=next(iter(c.ev.configs));cards=c.cards(c.ev.state(cfg))['options']
            for card in cards:
                if c.ev.options[card['option_id']]['lifecycle']=='factory_unavailable':
                    self.assertFalse(card['selectable']);self.assertEqual(card['reason'],'Unavailable at this time')

    def test_confirmed_complete_build_exports_server_price(self):
        for c in self.catalogs.values():
            cfg=next(iter(c.ev.configs));s=ConsumerSession(c,cfg,'release')
            self.commit(s,'select',self.oid(c,'GBA'))
            iid=next(i for i in c.ev.interiors if (i,cfg) in c.ev.interior_scopes and 'HTA' in i)
            self.commit(s,'interior',iid)
            order=s.order()
            self.assertEqual(order['total_minor'],sum(c['amount_minor'] for c in order['charges']))
            self.assertEqual(order['release_id'],'release')


if __name__=='__main__':unittest.main()
