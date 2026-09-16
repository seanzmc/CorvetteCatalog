"""Full offering reconciliation plus the unchanged E01–E08 acceptance tests.

These checks compare identities, scopes, amounts and ownership with retained
handoff rows. Full relationship translation and release validity are not asserted.
"""
import json
from pathlib import Path
import shutil
import sqlite3
import tempfile
from uuid import UUID

from catalog import foundation as f
from catalog import evaluator_sources as s
from catalog.evaluator import EvaluationError
from tests import test_evaluator


class CatalogOfferingTests(test_evaluator.EvaluatorTests):
    @classmethod
    def setUpClass(cls):
        cls.sample = f.connect(':memory:')
        f.create_schema(cls.sample)
        s.import_catalog(cls.sample)

    def source(self, lane):
        return json.loads((f.ROOT / 'docs' / (lane + '-structured-records.json')).read_bytes())

    def review(self, lane):
        return json.loads((f.ROOT / 'docs' / (lane + '-owner-decisions.json')).read_bytes())['owner_review']

    def test_complete_identity_value_and_matrix_reconciliation(self):
        total = 0
        for lane in f.LANES:
            data, review = self.source(lane), self.review(lane)
            rows, roles = data['baseline_rows'], data['sheet_roles']
            ev = self.evaluator(data['model_key'])
            source = {r['option_id']: r for r in rows[roles['options']]}
            additions = {r['rpo']: r for r in review['accepted_additions']}
            targets = {r['record_id'].split(':', 1)[1]: r for r in review['offering_targets']}
            self.assertEqual(len(ev.options), len(source) + len(additions))
            total += len(ev.options)
            for oid, row in source.items():
                with self.subTest(lane=lane, option=oid):
                    actual = ev.options[oid]
                    self.assertEqual(actual['rpo'], row['rpo'])
                    self.assertEqual(actual['customer_selectable'], row['selectable'])
                    disposition = targets[oid]['target_disposition']
                    expected_lifecycle = ('retired' if disposition in ('retire', 'retire_duplicate') else
                                          'factory_unavailable' if disposition == 'visible_unavailable' else 'active')
                    self.assertEqual(actual['lifecycle'], expected_lifecycle)
                    name = row['option_name']
                    if targets[oid].get('target_name') and targets[oid]['target_name'] != 'Royal Blue':
                        name = targets[oid]['target_name']
                    elif row['rpo'] == 'DUE' and lane != 'stingray':
                        name = name.replace('Santorini Blue', 'Royal Blue')
                    self.assertEqual(actual['name'], name)
                    price = 1995 if row['rpo'] == 'Z25' and lane in ('grand-sport', 'grand-sport-x') else row['price']
                    self.assertEqual(actual['purchase_amount_minor'], None if price is None else price * 100)
                    expected = {(r['variant_id'], r['status']) for r in rows[roles['availability']] if r['option_id'] == oid}
                    self.assertEqual({(c, v) for (o, c), v in ev.statuses.items() if o == oid}, expected)
                    if expected_lifecycle != 'active':
                        self.assertTrue(all(not ev.eligible(oid, c) for c in ev.configs))
            for code, addition in additions.items():
                option, = [r for r in ev.options.values() if r['rpo'] == code]
                UUID(option['id'])
                self.assertNotIn(option['id'], source)
                self.assertEqual(option['purchase_amount_minor'], addition['price'] * 100)
                self.assertEqual({c for (o, c), status in ev.statuses.items() if o == option['id'] and status == 'available'}, set(addition['configuration_ids']))
        self.assertEqual(total, 1388)  # 1,379 historical identities + nine additions.

    def test_all_contextual_rates_keep_source_endpoint_type_amount_and_scope(self):
        total = 0
        for lane in f.LANES:
            data = self.source(lane)
            rows, roles = data['baseline_rows'], data['sheet_roles']
            ev = self.evaluator(data['model_key'])
            source = {r['price_rule_id']: r for r in rows[roles['price_rules']]}
            actual = {r['id']: r for r in ev.rows['option_rate'] if r['id'] in source}
            self.assertEqual(set(actual), set(source))
            corrections = [r for r in ev.rows['option_rate'] if r['id'] not in source]
            self.assertEqual(len(corrections), 1 if lane in ('z06', 'zr1', 'zr1x') else 0)
            for rate in corrections:
                self.assertEqual((rate['target_option_id'], rate['amount_minor']), ('opt_sc7_001', 0))
                member, = [r for r in ev.rows['condition_member'] if r['condition_id'] == rate['condition_id']]
                self.assertEqual((member['option_id'], member['state']), ('opt_sbt_001', 'resolved_selection'))
                self.assertEqual({c for r, c in ev.scopes['option_rate'] if r == rate['id']}, {c['id'] for c in ev.configs.values() if c['body'] == 'coupe'})
            total += len(actual)
            for identifier, row in source.items():
                rate = actual[identifier]
                self.assertEqual((rate['target_option_id'], rate['amount_minor']), (row['target_option_id'], row['price_value'] * 100))
                expected_scope = {c['variant_id'] for c in rows['variant_master']
                                  if (row['body_style_scope'] in (None, '*') or row['body_style_scope'].lower() == c['body_style'].lower())
                                  and (row['trim_level_scope'] in (None, '*') or row['trim_level_scope'].lower() == c['trim_level'].lower())}
                self.assertEqual({c for r, c in ev.scopes['option_rate'] if r == identifier}, expected_scope)
                member, = [r for r in ev.rows['condition_member'] if r['condition_id'] == rate['condition_id']]
                if row['condition_option_id'] in ev.interiors:
                    self.assertEqual((member['interior_id'], member['state']), (row['condition_option_id'], 'chosen'))
                else:
                    self.assertEqual((member['option_id'], member['state']), (row['condition_option_id'], 'resolved_selection'))
        self.assertEqual(total, 297)

    def test_roof_pouch_zero_rates_and_standalone_prices_in_every_lane(self):
        for model, config in [('stingray', '3lt_c07'), ('grand_sport', '3lt_e07'), ('grand_sport_x', '3lt_g07'),
                              ('z06', '3lz_h07'), ('zr1', '3lz_r07'), ('zr1x', '3lz_s07')]:
            ev = self.evaluator(model)
            baseline = ev.state(config).total_minor
            for intent in [('opt_sc7_001', 'opt_sbt_001'), ('opt_sbt_001', 'opt_sc7_001')]:
                state = ev.state(config, intent)
                self.assertEqual(state.total_minor - baseline, 252500)
                self.assertEqual(next(c.amount_minor for c in state.charges if c.owner_id == 'opt_sc7_001'), 0)
            self.assertEqual(ev.state(config, ('opt_sc7_001',)).total_minor - baseline, 19500)

    def test_all_interiors_and_parts_reconcile_without_duplicate_seat_or_residual(self):
        total = 0
        for lane in f.LANES:
            data = self.source(lane)
            rows, roles = data['baseline_rows'], data['sheet_roles']
            ev = self.evaluator(data['model_key'])
            source = {r['interior_id']: r for r in rows[roles['interiors']]}
            self.assertEqual(set(ev.interiors), set(source))
            total += len(source)
            components = {r['id']: dict(r) for r in self.db.execute('SELECT * FROM component WHERE revision_id = ?', (ev.revision_id,))}
            scope_rows = {r['interior_id']: r for r in rows['model_interior_scope']}
            for identifier, leaf in source.items():
                actual = ev.interiors[identifier]
                self.assertEqual(ev.options[actual['seat_option_id']]['rpo'], leaf['Seat'])
                expected = {c['variant_id'] for c in rows['variant_master'] if c['trim_level'].lower() == scope_rows[identifier]['trim_level'].lower()}
                self.assertEqual({c for i, c in ev.interior_scopes if i == identifier}, expected)
                source_parts = {r['rpo'] for r in rows['interior_components'] if r['interior_id'] == identifier and str(r['active']).lower() == 'true' and r['component_type'] != 'seat'}
                parts = [r for r in ev.rows['interior_part'] if r['interior_id'] == identifier]
                self.assertEqual({r['part_key'] for r in parts}, source_parts)
                self.assertTrue(all(r['option_id'] != actual['seat_option_id'] for r in parts))
                for part in parts:
                    if part['option_id']:
                        self.assertEqual(ev.options[part['option_id']]['rpo'], part['part_key'])
                    else:
                        component = components[part['component_id']]
                        self.assertEqual(component['code'], part['part_key'])
                        price, = {r['Price'] for r in rows['PriceRef'] if r['Code'] == component['code']}
                        for config in expected:
                            rate, = [r for r in ev.rows['component_rate'] if r['component_id'] == component['id'] and r['configuration_id'] == config]
                            self.assertEqual(rate['amount_minor'], price * 100)
        self.assertEqual(total, 704)

    def test_interior_corrected_charge_owners_across_all_six_lanes(self):
        for model, config, trim, suede, high, low in [
            ('stingray', '3lt_c07', '3LT', 'N26', 2780, 2285),
            ('grand_sport', '3lt_e07', '3LT', 'N26', 2780, 2285),
            ('grand_sport_x', '3lt_g07', '3LT', 'N26', 2780, 2285),
            ('z06', '3lz_h07', '3LZ', 'N2Z', 2980, 2485),
            ('zr1', '3lz_r07', '3LZ', 'N2Z', 2980, 2485),
            ('zr1x', '3lz_s07', '3LZ', 'N2Z', 2980, 2485),
        ]:
            ev = self.evaluator(model)
            for suffix, expected in [('HUU', 1590), ('HU0_38S', 2085), (f'HXO_{suede}_38S', high), (f'HZP_{suede}', low)]:
                with self.subTest(model=model, leaf=suffix):
                    state = ev.state(config, interior=f'{trim}_R6X_AE4_{suffix}')
                    baseline = ev.state(config)
                    self.assertEqual(state.total_minor - baseline.total_minor, expected * 100)
                    seat_id = 'opt_ae4_001' if model == 'grand_sport_x' else 'opt_ae4_002'
                    charges = [c for c in state.charges if c.owner_kind == 'option' and c.owner_id in (seat_id, 'opt_r6x_001')]
                    self.assertEqual({c.owner_id: c.amount_minor for c in charges}, {seat_id: 59500, 'opt_r6x_001': 99500})
                    self.assertEqual(len(charges), 2)

    def test_every_interior_prices_in_its_own_configurations(self):
        for lane in f.LANES:
            ev = self.evaluator(self.source(lane)['model_key'])
            for identifier, config in ev.interior_scopes:
                with self.subTest(lane=lane, interior=identifier, config=config):
                    state = ev.state(config, interior=identifier)
                    owners = [(c.owner_kind, c.owner_id) for c in state.charges]
                    self.assertEqual(len(owners), len(set(owners)))
                    self.assertNotIn('missing_required_interior', state.issues)
                    self.assertIn('partial_catalog_not_submission_ready', state.issues)
        for model, config in [('grand_sport', '3lt_e07'), ('grand_sport_x', '3lt_g07')]:
            ev = self.evaluator(model)
            for seat, contribution in [('AE4', 2590), ('AH2', 1995)]:
                state = ev.state(config, interior=f'3LT_{seat}_EL9')
                self.assertEqual(state.total_minor - ev.state(config).total_minor, contribution * 100)
                self.assertIn('opt_z25_001', state.resolved)

    def test_no_charge_source_price_changes_fail_in_fresh_imports(self):
        # Synthetic prices only modify temporary copies, never source evidence.
        for lane, code, importers in [
            ('grand-sport-x', 'XFR', (s.import_cases, s.import_catalog)),
            ('stingray', 'UVB', (s.import_catalog,)),
        ]:
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory)
                for name in [f'{l}-{suffix}.json' for l in f.LANES for suffix in ('structured-records', 'owner-decisions')] + [s.DESIGN, s.POLICY]:
                    shutil.copyfile(f.ROOT / 'docs' / name, path / name)
                target = path / f'{lane}-structured-records.json'
                data = json.loads(target.read_bytes())
                row, = [r for r in data['baseline_rows'][data['sheet_roles']['options']] if r['rpo'] == code]
                self.assertIsNone(row['price'])
                for amount in (0, 100):
                    row['price'] = amount
                    target.write_text(json.dumps(data))
                    for importer in importers:
                        with self.subTest(lane=lane, code=code, amount=amount, importer=importer.__name__):
                            db = f.connect(':memory:')
                            try:
                                f.create_schema(db)
                                with self.assertRaisesRegex(ValueError, f'No-charge classification source changed: {lane}/{code}'):
                                    importer(db, path)
                                for table, in db.execute("SELECT name FROM sqlite_master WHERE type = 'table'"):
                                    self.assertEqual(db.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0], 0, table)
                            finally:
                                db.close()

    def test_late_full_import_failure_rolls_back_and_pins_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            for name in [f'{lane}-{suffix}.json' for lane in f.LANES for suffix in ('structured-records', 'owner-decisions')] + [s.DESIGN, s.POLICY]:
                shutil.copyfile(f.ROOT / 'docs' / name, path / name)
            target = path / 'zr1x-structured-records.json'
            data = json.loads(target.read_bytes())
            for row in data['baseline_rows']['zr1x_options']:
                if row['option_id'] == 'opt_tom_002':
                    row['price'] = None
            target.write_text(json.dumps(data))
            before = list(self.db.iterdump())
            with self.assertRaisesRegex(ValueError, 'source changed'):
                s.import_catalog(self.db, path)
            self.assertEqual(list(self.db.iterdump()), before)
            db = f.connect(':memory:')
            self.addCleanup(db.close)
            f.create_schema(db)
            with self.assertRaisesRegex(ValueError, 'Missing purchase price'):
                s.import_catalog(db, path)
            for table, in db.execute("SELECT name FROM sqlite_master WHERE type = 'table'"):
                self.assertEqual(db.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0], 0, table)

    def test_selectability_unknown_disabled_prices_and_component_guards(self):
        ev = self.evaluator('grand_sport_x')
        with self.assertRaisesRegex(EvaluationError, 'nonselectable'):
            ev.state('2lt_g07', ('opt_uqt_001',))
        for model in ('stingray', 'grand_sport', 'z06', 'zr1', 'zr1x'):
            ev = self.evaluator(model)
            option = ev.options['opt_v8x_001']
            if option['purchase_amount_minor'] is None:
                self.assertIsNone(option['charge_mode'])  # Unknown is not free.
        ev = self.evaluator('stingray')
        self.db.execute('DELETE FROM component_rate_translation WHERE revision_id = ?', (ev.revision_id,))
        self.db.execute('DELETE FROM component_rate WHERE revision_id = ?', (ev.revision_id,))
        with self.assertRaisesRegex(EvaluationError, 'component rate'):
            self.evaluator('stingray').state('3lt_c07', interior='3LT_R6X_AE4_HXO_N26_38S')
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute('UPDATE interior_part SET option_id = NULL, component_id = NULL')

    def test_full_reimport_reopen_preserves_allocations_and_provenance(self):
        def snapshot(db):
            return {r[0]: [tuple(x) for x in db.execute(f'SELECT * FROM "{r[0]}" ORDER BY rowid')]
                    for r in db.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'catalog.sqlite'
            before = snapshot(self.db)
            with f.connect(path) as db:
                self.db.backup(db)
            db.close()
            db = f.connect(path)
            try:
                s.import_catalog(db)
                self.assertEqual(snapshot(db), before)
                s.validate_sources(db)
            finally:
                db.close()
