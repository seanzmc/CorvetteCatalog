"""Full-lane behavior checks against retained source and accepted target traces.

Expected amounts and code sets below are independent of translation recipes.
Release completeness and whole-revision overlap are deliberately separate.
"""
import json
from unittest.mock import patch
import unittest

from catalog import foundation as f
from catalog.behavior_sources import import_behavior, FAMILIES, BehaviorLane
from catalog.evaluator import Evaluator, Session, EvaluationError


class BehaviorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = f.connect(':memory:')
        f.create_schema(cls.db)
        import_behavior(cls.db)
        cls.evaluators = {model: Evaluator(cls.db, revision) for model, revision in cls.db.execute(
            'SELECT model_key, revision_id FROM catalog_revision JOIN model_year USING(model_year_id) JOIN model USING(model_id)')}

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    def ev(self, model):
        return self.evaluators[model]

    def oid(self, ev, code):
        matches = [r['id'] for r in ev.options.values() if r['rpo'] == code and r['lifecycle'] != 'retired']
        self.assertEqual(len(matches), 1, code)
        return matches[0]

    def codes(self, ev, state, field='resolved'):
        return {ev.options[o]['rpo'] for o in getattr(state, field)}

    def select(self, ev, state, *codes):
        for code in codes:
            state = ev.transition(state, 'select', self.oid(ev, code))
        return state

    def test_every_source_behavior_row_has_one_reasoned_disposition(self):
        for lane in f.LANES:
            data = json.loads((f.ROOT / 'docs' / (lane + '-structured-records.json')).read_text())
            ev = self.ev(data['model_key'])
            expected = {(data['sheet_roles'][role], row['_row']) for role in FAMILIES
                        for row in data['baseline_rows'][data['sheet_roles'][role]]}
            expected |= {('default_selection_rules', row['_row']) for row in data['baseline_rows']['default_selection_rules']}
            dispositions = list(self.db.execute('''SELECT a.locator, d.disposition, d.reason FROM source_disposition d
                JOIN source_anchor a USING(anchor_id) WHERE revision_id=? AND d.fragment_key='behavior' ''', (ev.revision_id,)))
            actual = {(loc.split('/')[1], int(loc.split('=')[-1])) for loc, _, _ in dispositions}
            self.assertEqual(actual, expected)
            self.assertEqual(len(dispositions), len(expected))
            self.assertTrue(all(reason for _, _, reason in dispositions))
            self.assertTrue(all(status in ('translated', 'superseded', 'inactive') for _, status, _ in dispositions))

    def test_all_32_initial_states_keep_exact_lane_base_and_tax(self):
        for model, ev in self.evaluators.items():
            for config, row in ev.configs.items():
                with self.subTest(model=model, config=config):
                    state = ev.state(config)
                    tax = {'z06': 2600, 'zr1': 3000, 'zr1x': 2600}.get(model, 0)
                    self.assertEqual(state.total_minor, row['starting_amount_minor'] + tax * 100)
                    self.assertIn('partial_catalog_not_submission_ready', state.issues)
                    self.assertIn('missing_required_interior', state.issues)
                    self.assertNotIn('GBA', self.codes(ev, state))
                    self.assertEqual(state.intent, ())

    def test_translated_direct_endpoints_reconcile_with_original_source(self):
        for lane in f.LANES:
            data = json.loads((f.ROOT / 'docs' / (lane + '-structured-records.json')).read_text())
            ev = self.ev(data['model_key'])
            sheet = data['sheet_roles']['rule_mapping']
            for row in data['baseline_rows'][sheet]:
                locator = f'baseline_rows/{sheet}/_row={row["_row"]}'
                anchor, status = self.db.execute('''SELECT d.anchor_id, d.disposition FROM source_disposition d
                    JOIN source_anchor a USING(anchor_id) WHERE d.revision_id=? AND a.locator=? AND d.fragment_key='behavior' ''',
                    (ev.revision_id, locator)).fetchone()
                if status != 'translated':
                    continue
                source, target = row['source_id'], row['target_id']
                if lane == 'grand-sport':
                    source = 'opt_t0e_001' if source == 'opt_t0e_002' else source
                    target = 'opt_t0e_001' if target == 'opt_t0e_002' else target
                with self.subTest(lane=lane, rule=row['rule_id']):
                    if row['rule_type'] == 'includes':
                        rows = list(self.db.execute('''SELECT a.* FROM acquisition a JOIN acquisition_translation t
                            ON t.revision_id=a.revision_id AND t.acquisition_id=a.id WHERE a.revision_id=? AND t.anchor_id=?''',
                            (ev.revision_id, anchor)))
                        self.assertTrue(any(r['target_option_id'] == target and any(
                            (m['option_id'] or m['interior_id']) == source for m in ev.rows['condition_member'] if m['condition_id'] == r['condition_id']) for r in rows))
                    elif row['rule_type'] == 'requires':
                        rows = [r for r in ev.rows['requirement'] if r['id'] == row['rule_id']]
                        self.assertEqual(len(rows), 1)
                        self.assertEqual(rows[0]['source_option_id'] or rows[0]['source_interior_id'], source)
                        self.assertTrue(any((m['option_id'] or m['interior_id']) == target for m in ev.rows['condition_member']
                                            if m['condition_id'] == rows[0]['satisfaction_condition_id']))
                    else:
                        ids = {r[0] for r in self.db.execute('''SELECT conflict_id FROM conflict_translation
                            WHERE revision_id=? AND anchor_id=?''', (ev.revision_id, anchor))}
                        self.assertTrue(any(r['id'] in ids and (r['source_option_id'] or r['source_interior_id']) == source for r in ev.rows['conflict']))
                        self.assertTrue(any(r['conflict_id'] in ids and (r['option_id'] or r['interior_id']) == target for r in ev.rows['conflict_member']))

    def test_source_direct_requires_remain_requirements_not_acquisitions(self):
        ev = self.ev('stingray')
        with self.assertRaisesRegex(EvaluationError, 'prerequisites'):
            self.select(ev, ev.state('2lt_c07'), 'FE4')
        state = self.select(ev, ev.state('2lt_c07'), 'Z51', 'FE4')
        self.assertEqual(state.total_minor, 8788500)
        self.assertNotIn('FE3', self.codes(ev, state, 'installed'))
        removed = ev.transition(state, 'remove', self.oid(ev, 'Z51'))
        self.assertNotIn('FE4', self.codes(ev, removed))
        self.assertEqual(removed.total_minor, 8059500)

    def test_stingray_aero_accepted_corrections(self):
        ev = self.ev('stingray')
        state = self.select(ev, ev.state('2lt_c07'), 'G8G', 'Z51', '5ZU')
        self.assertNotIn('ZF1', self.codes(ev, state))
        self.assertNotIn('T0A', self.codes(ev, state, 'installed'))
        state = self.select(ev, ev.state('2lt_c07'), 'Z51', 'TVS', 'RNX')
        self.assertTrue({'Z51', 'TVS', 'ZF1', 'RNX'}.issubset(self.codes(ev, state)))
        self.assertNotIn('T0A', self.codes(ev, state, 'installed'))
        # Paint loss clears the invalid wing; it does not invent replacement paint.
        state = self.select(ev, self.select(ev, ev.state('2lt_c07'), 'G8G', '5ZU'), 'G26')
        self.assertNotIn('5ZU', self.codes(ev, state))
        self.assertIn('G26', self.codes(ev, state))

    def test_stingray_packages_and_replaceable_caps(self):
        ev = self.ev('stingray')
        state = self.select(ev, ev.state('2lt_c07'), 'PDV', '5ZD')
        self.assertIn('PDV', self.codes(ev, state))
        self.assertNotIn('VWD', self.codes(ev, state))
        self.assertEqual(state.total_minor, 8159500)
        state = ev.transition(state, 'remove', self.oid(ev, 'PDV'))
        self.assertIn('5ZD', self.codes(ev, state))
        self.assertNotIn('SB7', self.codes(ev, state))
        state = self.select(ev, ev.state('2lt_c07'), 'PCX', '5DO')
        self.assertNotIn('PCX', self.codes(ev, state))
        self.assertEqual(state.total_minor, 8499000)

    def test_gs_brake_prerequisites_restoration_and_independent_paid_caliper(self):
        ev = self.ev('grand_sport')
        state = ev.state('2lt_e07')
        self.assertNotIn('B4Z', self.codes(ev, state, 'standard'))
        for code, total in [('FEB', 99095), ('J57', 105095), ('T0F', 114090)]:
            state = self.select(ev, state, code)
            self.assertEqual(state.total_minor, total * 100)
        state = ev.transition(state, 'remove', self.oid(ev, 'FEB'))
        self.assertTrue({'J57', 'T0F', 'CFZ', 'B4Z'}.isdisjoint(self.codes(ev, state)))
        self.assertTrue({'JX6', 'J6A', 'T0E', 'SWM'}.issubset(self.codes(ev, state)))
        state = self.select(ev, ev.state('2lt_e07'), 'J6A', 'FEB', 'J57')
        self.assertNotIn('J6A', self.codes(ev, state))
        self.assertIn('J6D', self.codes(ev, state))
        state = self.select(ev, state, 'J6F')
        state = ev.transition(state, 'remove', self.oid(ev, 'FEB'))
        self.assertIn('J6F', self.codes(ev, state))

    def test_all_gs_gsx_conditional_roof_pairs_and_direct_removal(self):
        pairs = {'DMX': ('G26', 'G4Z', 'GBK', 'GKZ', 'GPH'), 'DMV': ('G26', 'G4Z', 'GBK', 'GKZ', 'GPH'),
                 'DMY': ('G26', 'G4Z', 'GBK', 'GTR'), 'DMW': ('G26', 'G4Z', 'GBK')}
        for model in ('grand_sport', 'grand_sport_x'):
            ev = self.ev(model)
            for config, cfg in ev.configs.items():
                for stripe, paints in pairs.items():
                    for paint in paints:
                        with self.subTest(model=model, config=config, stripe=stripe, paint=paint):
                            state = self.select(ev, ev.state(config), paint, '97A', stripe)
                            self.assertEqual('D84' in self.codes(ev, state), cfg['body'] == 'convertible')
                            if cfg['body'] == 'convertible':
                                after = ev.transition(state, 'remove', self.oid(ev, 'D84'))
                                self.assertNotIn(stripe, self.codes(ev, after))
                                self.assertIn(paint, self.codes(ev, after))
                                self.assertIn('97A', self.codes(ev, after))
            config = '2lt_e67' if model == 'grand_sport' else '2lt_g67'
            state = self.select(ev, ev.state(config), 'G26', '97A', 'DMX')
            self.assertEqual(state.total_minor, (107175 if model == 'grand_sport' else 129275) * 100)

    def test_gsx_ls6_retirement_and_independent_equipment(self):
        ev = self.ev('grand_sport_x')
        state = ev.state('2lt_g67')
        self.assertTrue({'LS6', 'J57', 'B4Z', 'FE5'}.issubset(self.codes(ev, state)))
        self.assertNotIn('D3V', self.codes(ev, state))
        state = self.select(ev, state, 'ZZ3', 'FED')
        self.assertNotIn('D3V', self.codes(ev, state))
        self.assertTrue({'BC7', 'SL9', 'XFR'}.issubset(self.codes(ev, state)))
        self.assertNotIn('XFT', self.codes(ev, state, 'installed'))

    def test_z06_all_54_package_wheel_totals_and_caliper_upgrades(self):
        ev = self.ev('z06')
        totals = {'PDB': [16000, 17000, 17500], 'PDD': [25495, 26495, 26995], 'PDF': [26495, 27495, 27995]}
        for config, cfg in ev.configs.items():
            for package, amounts in totals.items():
                for wheel, amount in zip(('ROY', 'ROZ', 'STZ'), amounts):
                    with self.subTest(config=config, package=package, wheel=wheel):
                        state = self.select(ev, ev.state(config), package, wheel)
                        self.assertEqual(state.total_minor, cfg['starting_amount_minor'] + (amount + (2600 if package == 'PDB' else 3000)) * 100)
                        self.assertIn('J6D', self.codes(ev, state))
                        state = self.select(ev, state, 'J6F')
                        self.assertIn(package, self.codes(ev, state))
                        self.assertIn('J6F', self.codes(ev, state))

    def test_z06_pcz_charge_child_ownership_and_lpo_factory_wheel_separation(self):
        ev = self.ev('z06')
        state = self.select(ev, ev.state('2lz_h07'), 'PCZ')
        self.assertEqual(state.total_minor, 13819000)
        self.assertTrue({'PCZ', '5DK', 'SFZ', 'SHT', 'VPO', 'SOE'}.issubset(self.codes(ev, state)))
        for code in ('5DK', 'SFZ', 'SHT', 'VPO'):
            line, = [c for c in state.charges if c.owner_id == self.oid(ev, code)]
            self.assertEqual(line.amount_minor, 0)
        for wheel in ('5DH', '5DK'):
            state = self.select(ev, ev.state('2lz_h07'), wheel)
            self.assertIn('SOE', self.codes(ev, state))
            for conflict in ('R8C', 'SPY', 'S47'):
                replaced = self.select(ev, state, conflict)
                self.assertNotIn(wheel, self.codes(ev, replaced))
        state = self.select(ev, ev.state('2lz_h07'), 'SHT', 'PCZ')
        state = ev.transition(state, 'remove', self.oid(ev, 'PCZ'))
        self.assertIn('SHT', self.codes(ev, state))
        self.assertNotIn('5DK', self.codes(ev, state))

    def test_exclusive_default_restoration_is_not_whole_section_vacancy(self):
        ev = self.ev('z06')
        state = self.select(ev, ev.state('2lz_h07'), 'CBF')
        self.assertIn('EFR', self.codes(ev, state))
        state = self.select(ev, state, 'EDU')
        self.assertTrue({'CBF', 'EDU'}.issubset(self.codes(ev, state)))
        self.assertNotIn('EFR', self.codes(ev, state))
        state = ev.transition(state, 'remove', self.oid(ev, 'EDU'))
        self.assertTrue({'CBF', 'EFR'}.issubset(self.codes(ev, state)))

    def test_z06_stripe_paint_both_directions_with_negative_controls(self):
        ev = self.ev('z06')
        pairs = [(stripe, paint) for stripes, paints in [('DUE DPB', 'GTR'), ('DUK DPL DSZ DZX', 'GKZ GPH'),
                 ('DPC DT0 DZU', 'GBK'), ('DPG DSY', 'G26')] for stripe in stripes.split() for paint in paints.split()]
        self.assertEqual(len(pairs), 15)
        for config in ev.configs:
            for stripe, paint in pairs:
                for first, second in ((stripe, paint), (paint, stripe)):
                    with self.subTest(config=config, first=first, second=second):
                        state = self.select(ev, ev.state(config), first, second)
                        self.assertIn(second, self.codes(ev, state))
                        self.assertNotIn(first, self.codes(ev, state))
            for stripe in ('DPT', 'DTH', 'DUB', 'DZV'):
                state = self.select(ev, ev.state(config), 'GTR', stripe)
                self.assertTrue({'GTR', stripe}.issubset(self.codes(ev, state)))

    def test_z06_cbf_removes_complete_package_roots_and_cancel_revert(self):
        ev = self.ev('z06')
        for codes in [('PDD',), ('PDF',), ('Z07', 'T0F'), ('Z07', 'T0G'), ('T0F',), ('T0G',), ('T0F', 'PDD')]:
            for config in ev.configs:
                with self.subTest(config=config, codes=codes):
                    session = Session(ev, config)
                    for code in codes:
                        session.confirm(session.preview('select', self.oid(ev, code)))
                    before = session.state
                    preview = session.preview('select', self.oid(ev, 'CBF'))
                    self.assertTrue({'PDD', 'PDF', 'Z07', 'T0F', 'T0G', 'CFZ', 'CFV'}.isdisjoint(self.codes(ev, preview.candidate)))
                    self.assertIn('CBF', self.codes(ev, preview.candidate))
                    session.cancel()
                    self.assertEqual(session.state, before)
                    session.confirm(session.preview('select', self.oid(ev, 'CBF')))
                    self.assertEqual(session.revert(), before)

    def test_every_lane_sbt_independent_pouch_and_source_only_removal(self):
        for model, ev in self.evaluators.items():
            for config, cfg in ev.configs.items():
                if cfg['body'] != 'coupe':
                    continue
                for prior in (False, True):
                    with self.subTest(model=model, config=config, prior=prior):
                        state = ev.state(config)
                        base = state.total_minor
                        if prior:
                            state = self.select(ev, state, 'SC7')
                        state = self.select(ev, state, 'SBT')
                        self.assertEqual(state.total_minor - base, 252500)
                        state = ev.transition(state, 'remove', self.oid(ev, 'SBT'))
                        self.assertEqual('SC7' in self.codes(ev, state), prior)
                        self.assertEqual(state.total_minor - base, 19500 if prior else 0)

    def test_all_lanes_dtc_and_sai_conflicts_keep_retired_duw_absent(self):
        for model, ev in self.evaluators.items():
            for config in ev.configs:
                state = self.select(ev, ev.state(config), 'GTR', 'DTC')
                self.assertNotIn('GTR', self.codes(ev, state))
                self.assertIn('DTC', self.codes(ev, state))
                self.assertNotIn('DUW', self.codes(ev, state))
                self.assertTrue(any(r['source_option_id'] == self.oid(ev, 'SAI') for r in ev.rows['conflict']))
                self.assertTrue(all(o['lifecycle'] == 'retired' for o in ev.options.values() if o['rpo'] == 'DUW'))

    def test_zr_lane_prices_equipment_and_displaced_cover_intent(self):
        for model, delta, suspension, track, brake in [('zr1', 18990, 'FE8', 'FEJ', 'J58'), ('zr1x', 14495, 'FEH', 'FEZ', 'J59')]:
            ev = self.ev(model)
            for config in ev.configs:
                before = ev.state(config)
                state = self.select(ev, before, 'TOM', 'ZTK')
                self.assertEqual(state.total_minor - before.total_minor, delta * 100)
                self.assertTrue({track, 'XFS', 'TOM', 'J59'}.issubset(self.codes(ev, state, 'installed')))
                self.assertNotIn(suspension, self.codes(ev, state, 'installed'))
                state = ev.transition(state, 'remove', self.oid(ev, 'ZTK'))
                self.assertIn('TOM', self.codes(ev, state))
                self.assertIn(brake, self.codes(ev, state))
                state = self.select(ev, before, 'WKR', 'ZTK')
                state = ev.transition(state, 'remove', self.oid(ev, 'ZTK'))
                self.assertNotIn('WKR', self.codes(ev, state))
                self.assertNotIn('TOM', self.codes(ev, state))

    def test_all_704_interiors_acquire_once_without_conflicting_defaults(self):
        count = 0
        for model, ev in self.evaluators.items():
            count += len(ev.interiors)
            for interior, config in ev.interior_scopes:
                with self.subTest(model=model, config=config, interior=interior):
                    state = ev.transition(ev.state(config), 'interior', interior)
                    self.assertEqual(state.interior_id, interior)
                    self.assertIn(ev.interiors[interior]['seat_option_id'], state.resolved)
                    owners = [(c.owner_kind, c.owner_id) for c in state.charges]
                    self.assertEqual(len(owners), len(set(owners)))
                    self.assertNotIn('missing_required_interior', state.issues)
        self.assertEqual(count, 704)

    def test_content_is_supplied_without_new_purchases(self):
        for model, codes, expected in [
                ('z06', ('5DK',), 'Tech Bronze center caps supplied with second wheel set'),
                ('grand_sport', ('G26', '97A', 'DMX'), 'center stripe omitted from roof'),
                ('stingray', ('G8G', '5ZU', 'WKR'), 'high-wing version')]:
            ev = self.ev(model)
            config = next(c for c, row in ev.configs.items() if row['body'] == 'convertible' and row['trim'].startswith('2'))
            state = self.select(ev, ev.state(config), *codes)
            self.assertIn(expected, [r.value for r in state.content])
            if model == 'z06':
                self.assertTrue({'SPY', 'SPZ'}.isdisjoint(self.codes(ev, state)))
        for model in ('zr1', 'zr1x'):
            ev = self.ev(model)
            config = next(c for c, row in ev.configs.items() if row['body'] == 'convertible')
            state = ev.state(config)
            self.assertIn('Carbon Flash nacelles, A-pillars and header', [r.value for r in state.content])
            state = self.select(ev, state, 'GBA')
            self.assertIn('body-color nacelles, A-pillars and header with black exterior paint', [r.value for r in state.content])
            self.assertNotIn('Carbon Flash nacelles, A-pillars and header', [r.value for r in state.content])

    def test_color_override_retains_every_cause_but_one_charge(self):
        ev = self.ev('stingray')
        state = ev.transition(ev.state('1lt_c07'), 'interior', '1LT_AQ9_HUQ')
        state = self.select(ev, state, 'G26', '379')
        oid = self.oid(ev, 'D30')
        self.assertEqual(len([c for c in state.causes if c.option_id == oid]), 2)
        self.assertEqual([c.amount_minor for c in state.charges if c.owner_id == oid], [149500])
        state = self.select(ev, state, 'GBA')
        self.assertIn(oid, state.resolved)
        state = ev.transition(state, 'remove', self.oid(ev, '379'))
        self.assertNotIn(oid, state.resolved)
        self.assertEqual(state.interior_id, '1LT_AQ9_HUQ')

    def test_source_accounting_does_not_hide_changed_or_mixed_projection(self):
        from catalog.evaluator_sources import import_cases
        db = f.connect(':memory:')
        self.addCleanup(db.close)
        f.create_schema(db)
        import_cases(db)
        count = db.execute('SELECT COUNT(*) FROM option').fetchone()[0]
        with self.assertRaisesRegex(ValueError, 'Different projection'):
            import_behavior(db)
        self.assertEqual(db.execute('SELECT COUNT(*) FROM option').fetchone()[0], count)

    def test_distinct_price_outcomes_do_not_depend_on_source_row_order(self):
        # Current rates use one option/interior condition each. Different
        # amounts have disjoint configurations or mutually exclusive wheels;
        # equal amounts need no invented business winner.
        for model, ev in self.evaluators.items():
            for config in ev.configs:
                rates = ev.scoped('option_rate', config)
                for i, left in enumerate(rates):
                    for right in rates[i + 1:]:
                        if left['target_option_id'] != right['target_option_id'] or left['amount_minor'] == right['amount_minor']:
                            continue
                        endpoints = []
                        for row in (left, right):
                            members = [m for m in ev.rows['condition_member'] if m['condition_id'] == row['condition_id']]
                            self.assertEqual(len(members), 1)
                            endpoints.append(members[0]['option_id'])
                        self.assertTrue(any(set(endpoints).issubset(ev.members[g['id']]) for g in ev.scoped('choice_group', config)),
                                        (model, config, left['id'], right['id']))

    def test_reimport_reuses_every_row_and_failed_translation_rolls_back(self):
        def snapshot(db):
            return {r[0]: sorted(tuple(x) for x in db.execute('SELECT * FROM "' + r[0] + '"'))
                    for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        before = snapshot(self.db)
        import_behavior(self.db)
        self.assertEqual(snapshot(self.db), before)
        empty = f.connect(':memory:')
        self.addCleanup(empty.close)
        f.create_schema(empty)
        original = BehaviorLane.translate
        def fail_late(lane):
            original(lane)
            if lane.lane == 'zr1x':
                raise ValueError('synthetic final-lane failure')
        with patch.object(BehaviorLane, 'translate', fail_late):
            with self.assertRaisesRegex(ValueError, 'synthetic final-lane'):
                import_behavior(empty)
        self.assertTrue(all(not rows for rows in snapshot(empty).values()))


if __name__ == '__main__':
    unittest.main()
