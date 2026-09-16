"""Independent source reconciliation for E01–E08 inputs, not evaluator tests."""
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import tempfile
import unittest
from uuid import UUID

from catalog import foundation as f
from catalog import evaluator_sources as s


class EvaluatorSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sample = f.connect(':memory:')
        f.create_schema(cls.sample)
        s.import_cases(cls.sample)

    @classmethod
    def tearDownClass(cls):
        cls.sample.close()

    def setUp(self):
        self.db = f.connect(':memory:')
        self.sample.backup(self.db)
        self.addCleanup(self.db.close)

    def revision(self, model):
        return self.db.execute('''SELECT revision_id FROM catalog_revision
            JOIN model_year USING (model_year_id) JOIN model USING (model_id)
            WHERE model_key = ?''', (model,)).fetchone()[0]

    def option(self, model, code):
        row, = self.db.execute('SELECT * FROM option WHERE revision_id = ? AND rpo = ?', (self.revision(model), code)).fetchall()
        return dict(row)

    def snapshot(self, db=None):
        db = db or self.db
        return {t[0]: sorted(tuple(r) for r in db.execute(f'SELECT * FROM "{t[0]}"'))
                for t in db.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}

    def test_bounded_options_amounts_statuses_and_source_ids_in_all_six_lanes(self):
        # Independently enumerated reviewed closure, not importer-generated output.
        expected = {
            'stingray': 'UQT PCX 5DO 5DG SFZ SHT SNG QE6',
            'grand-sport': 'DMX D84 G26 G4Z GBK GKZ GPH 97A Z15 AE4 AH2 Z25 3F9',
            'grand-sport-x': 'FED XFR XFT J57 B4Z FE5 LS6',
            'z06': 'PDB PDD Z07 T0F CFZ J57 J6D ROY ROZ STZ J56 J6A SOE T0E FE6 FE7 XFR XFS R8E',
            'zr1': 'ZTK TOM J58 J59 FE8 FEJ XFR XFS T0E R8E',
            'zr1x': 'ZTK TOM J59 FEH FEZ XFR XFS T0E R8E',
        }
        for lane, codes in expected.items():
            source = json.loads((f.ROOT / 'docs' / (lane + '-structured-records.json')).read_bytes())
            rows, roles = source['baseline_rows'], source['sheet_roles']
            revision = self.revision(source['model_key'])
            actual_codes = {r[0] for r in self.db.execute('SELECT rpo FROM option WHERE revision_id = ?', (revision,))}
            self.assertEqual(actual_codes, set(codes.split()) | {'UVB'})
            for source_option in rows[roles['options']]:
                code = source_option['rpo']
                if code not in codes.split():
                    continue
                actual = self.option(source['model_key'], code)
                self.assertEqual(actual['id'], source_option['option_id'])
                self.assertEqual(actual['name'], source_option['option_name'])
                self.assertEqual(actual['customer_selectable'], int(source_option['selectable']))
                self.assertEqual(actual['lifecycle'], 'active')
                price = source_option['price']
                if lane == 'grand-sport' and code == 'Z25':
                    self.assertEqual(price, 0)  # intentional accepted correction
                    price = 1995
                self.assertEqual(actual['purchase_amount_minor'], None if price is None else price * 100)
                self.assertEqual(actual['charge_mode'], 'no_separate_charge' if price is None else 'priced')
                matrix = {(r['variant_id'], r['status']) for r in rows[roles['availability']] if r['option_id'] == actual['id']}
                actual_matrix = {tuple(r) for r in self.db.execute('SELECT configuration_id, status FROM option_configuration WHERE revision_id = ? AND option_id = ?', (revision, actual['id']))}
                self.assertEqual(actual_matrix, matrix)
            for config in rows['variant_master']:
                amount, meaning, currency = self.db.execute('''SELECT starting_amount_minor, amount_meaning, currency
                    FROM configuration JOIN price_basis USING (basis_id) WHERE revision_id = ? AND id = ?''', (revision, config['variant_id'])).fetchone()
                self.assertEqual((amount, meaning, currency), (config['base_price'] * 100, 'vehicle_destination_included', 'USD'))

    def test_rates_retain_exact_source_targets_scopes_and_amounts(self):
        for lane in ('stingray', 'grand-sport', 'z06'):
            data = json.loads((f.ROOT / 'docs' / (lane + '-structured-records.json')).read_bytes())
            source_rates = {r['price_rule_id']: r for r in data['baseline_rows'][data['sheet_roles']['price_rules']]}
            revision = self.revision(data['model_key'])
            for rate in self.db.execute('SELECT * FROM option_rate WHERE revision_id = ?', (revision,)):
                source = source_rates[rate['id']]
                self.assertEqual((rate['target_option_id'], rate['amount_minor']), (source['target_option_id'], source['price_value'] * 100))
                condition, = self.db.execute('SELECT option_id, state FROM condition_member WHERE revision_id = ? AND condition_id = ?', (revision, rate['condition_id'])).fetchall()
                self.assertEqual(tuple(condition), (source['condition_option_id'], 'resolved_selection'))
                scopes = {r[0] for r in self.db.execute('SELECT configuration_id FROM option_rate_configuration WHERE revision_id = ? AND rate_id = ?', (revision, rate['id']))}
                expected = {c['variant_id'] for c in data['baseline_rows']['variant_master']
                            if source['trim_level_scope'] in (None, '*') or c['trim_level'].upper() == source['trim_level_scope'].upper()}
                self.assertEqual(scopes, expected)
        # Independent evidence anchors from E06, including owner, not only total.
        rate = self.db.execute("SELECT target_option_id, amount_minor FROM option_rate WHERE id = 'z06_pr_roz_pdd_26495'").fetchone()
        self.assertEqual(tuple(rate), ('opt_pdd_001', 2649500))
        self.assertEqual(self.db.execute("SELECT amount_minor FROM option_rate WHERE id = 'z06_pr_pdd_roz_zero'").fetchone()[0], 0)
        self.assertEqual(self.option('zr1', 'ZTK')['purchase_amount_minor'], 599500)
        self.assertEqual(self.option('zr1x', 'ZTK')['purchase_amount_minor'], 150000)
        self.assertEqual(self.option('zr1', 'TOM')['id'], 'opt_tom_001')
        self.assertEqual(self.option('zr1x', 'TOM')['id'], 'opt_tom_002')
        for model in ('zr1', 'zr1x'):
            self.assertEqual(self.option(model, 'TOM')['purchase_amount_minor'], 1299500)
            self.assertFalse(self.db.execute('SELECT 1 FROM option_rate WHERE revision_id = ?', (self.revision(model),)).fetchone())

    def test_dmx_and_any_paints_and_convertible_scope_are_literal(self):
        revision = self.revision('grand_sport')
        row, = self.db.execute("SELECT * FROM acquisition WHERE revision_id = ? AND target_option_id = 'opt_d84_001'", (revision,)).fetchall()
        clauses = self.db.execute('SELECT clause_id, mode FROM condition_clause WHERE revision_id = ? AND condition_id = ? ORDER BY clause_id', (revision, row['condition_id'])).fetchall()
        self.assertEqual([tuple(r) for r in clauses], [('1', 'any_present'), ('2', 'any_present')])
        expected = {'1': {'opt_dmx_001'}, '2': {'opt_g26_001', 'opt_g4z_001', 'opt_gbk_001', 'opt_gkz_001', 'opt_gph_001'}}
        for clause, ids in expected.items():
            actual = {r[0] for r in self.db.execute('SELECT option_id FROM condition_member WHERE revision_id = ? AND condition_id = ? AND clause_id = ?', (revision, row['condition_id'], clause))}
            self.assertEqual(actual, ids)
        scopes = {r[0] for r in self.db.execute('SELECT configuration_id FROM acquisition_configuration WHERE revision_id = ? AND acquisition_id = ?', (revision, row['id']))}
        self.assertEqual(scopes, {'1lt_e67', '2lt_e67', '3lt_e67'})
        self.assertEqual((row['origin_kind'], row['intent_policy']), ('dependency', 'preserve_prior'))
        req, = self.db.execute("SELECT * FROM requirement WHERE revision_id = ? AND activation_condition_id = ?", (revision, row['condition_id'])).fetchall()
        self.assertEqual((req['source_option_id'], req['loss_policy']), ('opt_dmx_001', 'remove_source_with_notice_revert'))
        self.assertEqual(self.db.execute('SELECT direct_removal_action FROM interaction_policy WHERE revision_id = ?', (revision,)).fetchone()[0], 'remove_requested_and_supporting_sources')

    def test_interiors_have_one_seat_owner_and_no_residual_charge(self):
        revision = self.revision('grand_sport')
        leaves = {tuple(r) for r in self.db.execute('SELECT id, seat_option_id FROM interior WHERE revision_id = ?', (revision,))}
        self.assertEqual(leaves, {('3LT_AE4_EL9', 'opt_ae4_002'), ('3LT_AH2_EL9', 'opt_ah2_001')})
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM component').fetchone()[0], 0)
        for identifier, seat in leaves:
            self.assertEqual({r[0] for r in self.db.execute('SELECT configuration_id FROM interior_configuration WHERE revision_id = ? AND interior_id = ?', (revision, identifier))}, {'3lt_e07', '3lt_e67'})
        self.assertEqual(self.option('grand_sport', 'Z25')['purchase_amount_minor'], 199500)
        self.assertEqual(self.db.execute("SELECT amount_minor FROM option_rate WHERE id = 'gs_pr_3lt_ae4_seat_001'").fetchone()[0], 59500)
        self.assertEqual(self.db.execute("SELECT amount_minor FROM option_rate WHERE id = 'gs_sb_zero_z25_3f9'").fetchone()[0], 0)

    def test_source_inclusions_ownership_and_purchase_transfer(self):
        for model, expected in [('stingray', 'absorb_prior'), ('zr1', 'preserve_prior'), ('zr1x', 'preserve_prior')]:
            policies = {r[0] for r in self.db.execute("SELECT intent_policy FROM acquisition WHERE revision_id = ? AND origin_kind = 'included'", (self.revision(model),))}
            self.assertEqual(policies, {expected})
        for lane in f.LANES:
            data = json.loads((f.ROOT / 'docs' / (lane + '-structured-records.json')).read_bytes())
            rules = {r['rule_id']: r for r in data['baseline_rows'][data['sheet_roles']['rule_mapping']]}
            revision = self.revision(data['model_key'])
            for row in self.db.execute('SELECT * FROM acquisition WHERE revision_id = ?', (revision,)):
                if row['id'] not in rules:
                    UUID(row['id'])
                    continue
                source = rules[row['id']]
                self.assertEqual(row['target_option_id'], source['target_id'])
                endpoints = self.db.execute('SELECT option_id, interior_id FROM condition_member WHERE revision_id = ? AND condition_id = ?', (revision, row['condition_id'])).fetchall()
                self.assertIn(source['source_id'], {v for r in endpoints for v in r})
        for model, request, add, remove in [('stingray', 'opt_5do_001', 'opt_5do_001', 'opt_pcx_001'), ('z06', 'opt_z07_001', 'opt_pdd_001', 'opt_pdb_001')]:
            plan, = self.db.execute('SELECT * FROM replacement_plan WHERE revision_id = ?', (self.revision(model),)).fetchall()
            self.assertEqual(plan['requested_option_id'], request)
            actions = [tuple(r) for r in self.db.execute('SELECT action, option_id, intent_effect FROM replacement_action WHERE revision_id = ? AND plan_id = ? ORDER BY position', (plan['revision_id'], plan['id']))]
            self.assertEqual(actions, [('remove', remove, None), ('add', add, 'commit_purchase')])

    def test_locked_package_and_soft_default_policies_do_not_compete(self):
        # Source Z07->T0F is a soft default; PDD includes locked T0F.
        revision = self.revision('z06')
        acquisition = self.db.execute("SELECT * FROM acquisition WHERE revision_id = ? AND id = 'z06_rule_opt_z07_001_includes_opt_t0f_001'", (revision,)).fetchone()
        self.assertEqual(acquisition['peer_policy'], 'yield_to_explicit')
        predicates = {tuple(r) for r in self.db.execute("""SELECT c.mode, m.option_id
            FROM condition_clause c JOIN condition_member m USING (revision_id, condition_id, clause_id)
            WHERE c.revision_id = ? AND c.condition_id = ?""", (revision, acquisition['condition_id']))}
        self.assertEqual(predicates, {('any_present', 'opt_z07_001'), ('none_present', 'opt_pdd_001')})
        # These two live roots retain two causes, with explicit distinct priority.
        priorities = {tuple(r) for r in self.db.execute("SELECT id, priority FROM acquisition WHERE revision_id = ? AND target_option_id = 'opt_cfz_001'", (revision,))}
        self.assertEqual(priorities, {('z06_rule_opt_pdd_001_includes_opt_cfz_001', 1), ('z06_rule_opt_t0f_001_includes_opt_cfz_001', 2)})

    def test_substitutions_keep_lane_equipment_distinct(self):
        for model, expected in {
            'grand_sport_x': {('opt_xft_001', 'opt_xfr_001')},
            'zr1': {('opt_fe8_002', 'opt_fej_001'), ('opt_xfr_001', 'opt_xfs_001'), ('opt_j58_002', 'opt_j59_002'), ('opt_t0e_001', 'opt_tom_001')},
            'zr1x': {('opt_feh_002', 'opt_fez_001'), ('opt_xfr_001', 'opt_xfs_001'), ('opt_t0e_001', 'opt_tom_002')},
        }.items():
            actual = {tuple(r) for r in self.db.execute('SELECT removed_option_id, replacement_option_id FROM equipment_substitution WHERE revision_id = ?', (self.revision(model),))}
            self.assertEqual(actual, expected)

    def test_reimport_reopen_reuses_every_row_and_allocation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'sample.sqlite'
            db = f.connect(path)
            self.db.backup(db)
            before = self.snapshot(db)
            db.close()
            db = f.connect(path)
            try:
                s.import_cases(db)
                self.assertEqual(self.snapshot(db), before)
                self.assertEqual(db.execute('PRAGMA foreign_keys').fetchone()[0], 1)
            finally:
                db.close()

    def test_all_provenance_links_and_decision_versions_resolve(self):
        s.validate_sources(self.db)
        for doc in self.db.execute('SELECT * FROM source_document'):
            self.assertEqual(doc['content_sha256'], hashlib.sha256((f.ROOT / doc['source_path']).read_bytes()).hexdigest())
        for revision in self.db.execute('SELECT revision_id FROM catalog_revision'):
            decisions = {r[0] for r in self.db.execute('''SELECT decision_id FROM interaction_policy p
                JOIN decision_member d ON p.decision_set_id = d.set_id WHERE revision_id = ?''', (revision[0],))}
            self.assertTrue({'compatibility-notices', 'COMMON-DIRECT-REMOVAL-2026-09-15'} <= decisions)
        # A composite child translation cannot point at a nonexistent clause.
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("UPDATE condition_member_translation SET clause_id = 'absent'")
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("UPDATE replacement_action_translation SET position = 99")
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("UPDATE review_decision SET evidence_set_id = 'missing'")

    def test_invalid_money_and_purchase_action_are_rejected(self):
        for amount in (-1, 1.5):
            with self.assertRaises(sqlite3.IntegrityError):
                self.db.execute('UPDATE option_rate SET amount_minor = ?', (amount,))
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute('UPDATE option_rate SET basis_id = NULL')
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("UPDATE option SET charge_mode = 'no_separate_charge' WHERE rpo = 'TOM'")
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("UPDATE replacement_action SET intent_effect = NULL WHERE action = 'add'")
        with self.assertRaises(ValueError):
            s.cents('0.001')
        # Unknown draft price stays unknown and fails slice validation, never zero.
        self.db.execute("UPDATE option SET purchase_amount_minor = NULL, basis_id = NULL WHERE rpo = 'TOM'")
        with self.assertRaisesRegex(ValueError, 'Missing classified purchase price'):
            s.validate_sources(self.db)

    def test_price_basis_meaning_and_nonempty_conditions(self):
        vehicle_basis = self.db.execute("SELECT basis_id FROM price_basis WHERE amount_meaning = 'vehicle_destination_included'").fetchone()[0]
        self.db.execute('UPDATE option_rate SET basis_id = ?', (vehicle_basis,))
        with self.assertRaisesRegex(ValueError, 'Wrong price basis'):
            s.validate_sources(self.db)
        self.db.rollback()
        self.db.execute("UPDATE condition SET mode = 'always' WHERE mode = 'conjunction'")
        with self.assertRaisesRegex(ValueError, 'Condition mode/clauses disagree'):
            s.validate_sources(self.db)

    def test_real_group_scope_subset_and_cross_revision_rejections(self):
        revision = self.revision('z06')
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute('UPDATE replacement_action SET revision_id = ?', (self.revision('stingray'),))
        self.db.execute("DELETE FROM choice_group_configuration_translation WHERE revision_id = ? AND group_id = 'z06_group_pdd_requires_carbon_wheel' AND configuration_id = '2lz_h67'", (revision,))
        self.db.execute("DELETE FROM choice_group_configuration WHERE revision_id = ? AND group_id = 'z06_group_pdd_requires_carbon_wheel' AND configuration_id = '2lz_h67'", (revision,))
        with self.assertRaisesRegex(ValueError, 'not a subset'):
            s.validate_sources(self.db)

    def test_changed_pinned_input_and_late_failure_are_atomic(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            for name in [f'{lane}-{suffix}.json' for lane in f.LANES for suffix in ('structured-records', 'owner-decisions')] + [s.DESIGN, s.POLICY]:
                shutil.copyfile(f.ROOT / 'docs' / name, path / name)
            target = path / 'zr1x-structured-records.json'
            data = json.loads(target.read_bytes())
            for option in data['baseline_rows']['zr1x_options']:
                if option['option_id'] == 'opt_tom_002':
                    option['price'] = None
            target.write_text(json.dumps(data))
            before = self.snapshot()
            with self.assertRaisesRegex(ValueError, 'source changed'):
                s.import_cases(self.db, path)
            self.assertEqual(before, self.snapshot())
            empty = f.connect(':memory:')
            self.addCleanup(empty.close)
            f.create_schema(empty)
            with self.assertRaisesRegex(ValueError, 'Missing purchase price'):
                s.import_cases(empty, path)
            self.assertTrue(all(not rows for rows in self.snapshot(empty).values()))


if __name__ == '__main__':
    unittest.main()
