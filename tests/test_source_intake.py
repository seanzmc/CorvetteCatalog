"""Whole-source intake: price schedules read whole, three-way comparison, keep or take."""
from contextlib import closing
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import test_authoring as base
from catalog import authoring_records as r, foundation as f, source_intake as si
from catalog.releases import database_hash

HEADER = '''2027 CHEVROLET CORVETTE,,,,,,,,,
2027 MODEL YEAR VEHICLE PRICE SCHEDULE,,,,,,,,,
"{effective}",,,,,,,,,
Base Model Prices,,,,,,,,,
,Model,Model Description,"List
Price","Factory
D/H(b)",MSRP(c),"Dealer
Invoice
Price(a)&(c)","Dealer
Price(c)","Employee
Price(c)",DFC
'''
OPTIONS = '''Additional Options,,,,,,,,,
,Option Code,Description,,"List
Price","Factory
D/H(b)",MSRP(c),"Dealer
Invoice
Price(a)","Dealer
Price(c)","Employee
Price(c)"
,Dealer Installed:,,,,,,,,
'''


def schedule(path, coupe, convertible, first_aid, spoiler=None, effective='EFFECTIVE TEST', revised='July 06'):
    rows = [f',1YC07,Corvette Stingray Coupe 1LT,"${coupe:,}.00",$0.00,"${coupe:,}.00",$1.00,$1.00,$0.00,"$2,495.00"',
            f',1YC67,Corvette Stingray Convertible 1LT,"${convertible:,}.00",$0.00,"${convertible:,}.00",$1.00,$1.00,$0.00,"$2,495.00"']
    options = [f',RYT,First Aid Kit,,${first_aid}.00,$0.00,${first_aid}.00,$1.00,$1.00,$0.00',
               ',PCQ,Grille Screen Protection Package,Stingray,"$1,375.00",$0.00,"$1,375.00",$1.00,$1.00,$0.00',
               ',PCQ,Grille Screen Protection Package,,"$1,675.00",$0.00,"$1,675.00",$1.00,$1.00,$0.00',
               ',ROY,Carbon Fiber Wheel Discount,Grand Sport and Grand Sport X Only,"-$1,000.00",$0.00,"-$1,000.00",$1.00,$1.00,$0.00',
               ',ROY,Carbon Flash - Painted Carbon Fiber Wheels,,"$11,995.00",$0.00,"$11,995.00",$1.00,$1.00,$0.00']
    if spoiler:
        options.append(f',5WN,ZR1 and ZR1X aero enhancement kit,,"${spoiler:,}.00",$0.00,"${spoiler:,}.00",$1.00,$1.00,$0.00')
    text = (HEADER.format(effective=effective) + '\n'.join(rows) + '\n' + OPTIONS + '\n'.join(options) +
            f'\n"¨Revised {revised}, 20262027 CHEVROLET CORVETTE",,,,,,,,,\n')
    Path(path).write_text(text)
    return Path(path)


class ScheduleTests(unittest.TestCase):
    def test_reads_rows_locations_and_footer_date(self):
        with tempfile.TemporaryDirectory() as directory:
            result = si.read_price_schedule(schedule(Path(directory) / 's.csv', 71300, 78300, 60, 1500))
        self.assertEqual(result['revised'], 'Revised July 06, 2026')
        coupe = result['entries'][0]
        self.assertEqual((coupe['configuration_id'], coupe['amount_minor'], coupe['destination_minor'], coupe['locator']),
                         ('1lt_c07', 7130000, 249500, 'line 12'))
        discount = next(e for e in result['entries'] if e['code'] == 'ROY' and e['amount_minor'] < 0)
        self.assertEqual(discount['amount_minor'], -100000)
        self.assertTrue(all(e['consistent'] for e in result['entries']))

    def test_duplicate_code_and_qualifier_is_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            path = schedule(Path(directory) / 's.csv', 71300, 78300, 60)
            path.write_text(path.read_text().replace(',PCQ,Grille Screen Protection Package,,', ',PCQ,Grille Screen Protection Package,Stingray,'))
            with self.assertRaisesRegex(ValueError, 'share a code and qualifier: option:PCQ:Stingray'):
                si.read_price_schedule(path)

    def test_qualifiers_that_only_name_models(self):
        self.assertEqual(si.qualifier_models('Z06, Grand Sport, & Grand Sport X'), {'z06', 'grand_sport', 'grand_sport_x'})
        self.assertEqual(si.qualifier_models('ZR1/ZR1X Only'), {'zr1', 'zr1x'})
        self.assertIsNone(si.qualifier_models('Z06 with ROY Carbon Fiber Wheel'))
        self.assertIsNone(si.qualifier_models('2LT/LZ or 3LT/LZ'))


class IntakeTests(unittest.TestCase):
    setUpClass = classmethod(base.AuthoringTests.setUpClass.__func__)
    tearDownClass = classmethod(base.AuthoringTests.tearDownClass.__func__)

    def setUp(self):
        base.AuthoringTests.setUp(self)
        self.db.close()
        self.db = si.open_draft(self.path)
        self.addCleanup(self.db.close)
        root = tempfile.TemporaryDirectory()
        self.addCleanup(root.cleanup)
        self.root = Path(root.name).resolve()
        (self.root / 'sources').mkdir()
        rooted = patch.object(f, 'ROOT', self.root)
        rooted.start()
        self.addCleanup(rooted.stop)
        # The catalog's September 6 values: base 71,000/78,000 plus 2,495; RYT 60.
        self.old = schedule(self.root / 'sources/old.csv', 71000, 78000, 60)

    def config(self, cid):
        return r.lookup(self.db, 'configuration', dict(revision_id=self.rev, id=cid))['starting_amount_minor']

    def manual(self, cid, amount):
        request = dict(table='configuration', key=dict(revision_id=self.rev, id=cid), values=dict(starting_amount_minor=amount))
        r.save(self.db, r.preview(self.db, self.rev, database_hash(self.db), [request], 'Owner promotion price'))

    def test_three_way_comparison_keep_take_apply_and_accept(self):
        new = schedule(self.root / 'sources/new.csv', 71300, 78300, 60, spoiler=1500, revised='September 09')
        self.manual('1lt_c67', 8000000)        # a manual edit, then a manufacturer change: conflict
        review = si.compare_prices(self.db, new, self.old)
        by_config = {i['key']['id']: i for i in review['items']}
        self.assertEqual(set(by_config), {'1lt_c07', '1lt_c67'})  # RYT unchanged: nothing to do anywhere
        self.assertEqual((by_config['1lt_c07']['status'], by_config['1lt_c07']['new']), ('update', 7379500))
        conflict = by_config['1lt_c67']
        self.assertEqual((conflict['status'], conflict['last'], conflict['current'], conflict['new']),
                         ('conflict', 8049500, 8000000, 8079500))
        self.assertEqual(conflict['manual_edits'][0]['reason'], 'Owner promotion price')
        self.assertIn('not_in_catalog', {n['kind'] for n in review['notes']})
        with self.assertRaisesRegex(ValueError, 'Choose keep or take for every conflict'):
            si.apply(self.db, review)

        result = si.apply(self.db, review, keep=[conflict['id']])
        self.assertEqual((result['applied'], self.config('1lt_c07'), self.config('1lt_c67')), (1, 7379500, 8000000))
        intake = json.loads(self.db.execute('SELECT payload_json FROM authoring_intake').fetchone()[0])
        self.assertEqual((intake['locator'], intake['source_path'], intake['coverage']), ('line 12', 'sources/new.csv', 'complete'))
        # The intake's own edit is not a manual edit; the owner's kept value still is.
        edits = si.manual_edits(self.db)
        self.assertNotIn(('configuration', si.encode(dict(revision_id=self.rev, id='1lt_c07'))), edits)
        self.assertIn(('configuration', si.encode(dict(revision_id=self.rev, id='1lt_c67'))), edits)
        with self.assertRaisesRegex(ValueError, 'changed since this review'):
            si.apply(self.db, review, keep=[conflict['id']])

        again = si.compare_prices(self.db, new, self.old)
        self.assertEqual({i['status'] for i in again['items']}, {'already_current', 'conflict'})
        accepted = si.accept(self.db, 'Owner', 'September 28 price schedule')
        self.assertTrue(accepted['accepted'])
        row = self.db.execute('SELECT disposition, accepted_change_ids_json FROM authoring_intake').fetchone()
        self.assertEqual(row['disposition'], 'accepted')
        self.assertEqual(len(json.loads(row['accepted_change_ids_json'])), 1)

    def test_proposals_flag_manual_edits_and_skip_applied_steps(self):
        option = dict(self.db.execute("SELECT * FROM option WHERE revision_id=? AND rpo='RYT'", (self.rev,)).fetchone())
        source = self.root / 'sources/notes.pdf'
        source.write_bytes(b'distribution update')
        proposals = self.root / 'proposals.json'
        proposals.write_text(json.dumps(dict(format='source-proposals-v1', source=si._source(source), notes=[], proposals=[dict(
            id='rename-ryt', model_key='stingray', locator='page 1, line 2', quote='(RYT) renamed', summary='RYT renamed',
            steps=[[dict(table='option', key=dict(id=option['id']), values=dict(name='First Aid Kit, renamed'))]],
            expected=[dict(table='option', key=dict(id=option['id']), values=dict(name=option['name']))])])))
        review = si.compare_proposals(self.db, proposals)
        self.assertEqual(review['items'][0]['status'], 'update')
        request = dict(table='option', key=dict(revision_id=self.rev, id=option['id']), values=dict(name='First Aid Kit (owner)'))
        r.save(self.db, r.preview(self.db, self.rev, database_hash(self.db), [request], 'Owner wording'))
        review = si.compare_proposals(self.db, proposals)
        item = review['items'][0]
        self.assertEqual(item['status'], 'conflict')
        self.assertEqual(item['differs'][0]['current'], dict(name='First Aid Kit (owner)'))
        self.assertEqual(si.apply(self.db, review, keep=['rename-ryt'])['applied'], 0)
        changed = dict(review, source=dict(review['source'], sha256='0' * 64))
        with self.assertRaisesRegex(ValueError, 'no longer matches its hash'):
            si.apply(self.db, changed, take=['rename-ryt'])
        si.apply(self.db, si.compare_proposals(self.db, proposals), take=['rename-ryt'])
        self.assertEqual(si.compare_proposals(self.db, proposals)['items'][0]['status'], 'already_current')
        reason = self.db.execute('SELECT reason FROM authoring_record_change ORDER BY edit_version DESC').fetchone()[0]
        # Text keys stay text, so the recorded history replays exactly.
        conflict = self.db.execute('SELECT id FROM conflict WHERE revision_id=? LIMIT 1', (self.rev,)).fetchone()[0]
        member = dict(table='conflict_member', key=dict(revision_id=self.rev, conflict_id=conflict, member_id=99),
                      action='create', values=dict(option_id=option['id']))
        with self.assertRaisesRegex(ValueError, 'member_id requires text'):
            r.operations(self.db, self.rev, [member])
        self.assertTrue(reason.startswith(si.INTAKE_REASON))
        self.assertIn('page 1, line 2', reason)


    def test_proposals_name_imported_identities_by_meaning(self):
        # Condition and rule IDs are generated at import; a proposal must work in any draft.
        source = self.root / 'sources/notes.pdf'
        source.write_bytes(b'distribution update')
        pdb = self.db.execute("SELECT id FROM option WHERE revision_id=? AND rpo='PDY'", (self.rev,)).fetchone()[0]
        rule = dict(self.db.execute("SELECT * FROM acquisition WHERE revision_id=? AND id='rule_opt_pdy_001_includes_opt_ryt_001'",
                                    (self.rev,)).fetchone())
        proposals = self.root / 'proposals.json'
        proposals.write_text(json.dumps(dict(format='source-proposals-v1', source=si._source(source), notes=[], proposals=[dict(
            id='refs', model_key='stingray', locator='page 1, line 3', quote='quoted', summary='references',
            steps=[[dict(table='conflict', key=dict(id='conflict_new'), action='create',
                         values=dict(source_option_id=pdb, activation_condition_id={'always': True})),
                    dict(table='acquisition', action='delete', key={},
                         match=dict(target_option_id=rule['target_option_id'], condition_options=[pdb]))]])])))
        steps = si.compare_proposals(self.db, proposals)['items'][0]['steps'][0]
        always = steps[0]['values']['activation_condition_id']
        self.assertEqual(self.db.execute('SELECT mode FROM condition WHERE revision_id=? AND id=?', (self.rev, always)).fetchone()[0], 'always')
        deleted = [s for s in steps[1:] if s['table'] == 'acquisition']
        self.assertEqual([d['key']['id'] for d in deleted], [rule['id']])
        self.assertTrue(all(s['action'] == 'delete' for s in steps[1:]))
        self.assertIn('acquisition_configuration', {s['table'] for s in steps[1:]})


    def test_withdrawing_an_option_needs_its_dependents_withdrawn_too(self):
        # NWI requires WUB. A manufacturer "not available at this time" for WUB alone
        # would leave NWI unbuildable; withdrawing both proves the rule inapplicable.
        def withdraw(*codes):
            requests = [dict(table='option', key=dict(revision_id=self.rev, id=self.db.execute(
                'SELECT id FROM option WHERE revision_id=? AND rpo=?', (self.rev, code)).fetchone()[0]),
                values=dict(lifecycle='factory_unavailable')) for code in codes]
            return r.preview(self.db, self.rev, database_hash(self.db), requests, 'Manufacturer constraint')
        with self.assertRaisesRegex(ValueError, 'Cannot verify affected requirement rule_opt_nwi_001_requires_opt_wub_001'):
            withdraw('WUB')
        change = withdraw('WUB', 'NWI')
        self.assertIn('Inapplicable: this edit makes an option it needs unavailable',
                      {item.get('coverage') for item in change['connected_after']})


if __name__ == '__main__':
    unittest.main()
