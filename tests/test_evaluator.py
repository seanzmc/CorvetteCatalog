"""Independent E01–E08 targets from worked examples and accepted lane decisions.

Literal source IDs and dollar checkpoints are authored from the retained docs,
not generated from the imported database or evaluator. Synthetic guards below
are explicitly separate from the evidence-derived acceptance cases.
"""
import random
import unittest

from catalog import foundation as f
from catalog.evaluator_sources import import_cases
from catalog.evaluator import Evaluator, Session, EvaluationError


class EvaluatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sample = f.connect(':memory:')
        f.create_schema(cls.sample)
        import_cases(cls.sample)

    @classmethod
    def tearDownClass(cls):
        cls.sample.close()

    def setUp(self):
        self.db = f.connect(':memory:')
        self.sample.backup(self.db)
        self.addCleanup(self.db.close)

    def evaluator(self, model):
        revision, = self.db.execute('''SELECT revision_id FROM catalog_revision
            JOIN model_year USING (model_year_id) JOIN model USING (model_id)
            WHERE model_key = ?''', (model,)).fetchone()
        return Evaluator(self.db, revision)

    def session(self, model, config):
        return Session(self.evaluator(model), config)

    def act(self, session, action, target=None):
        previous = session.state
        preview = session.preview(action, target)
        self.assertIs(session.state, previous)
        # Pure preview is repeatable, including intent order and all cause roots.
        again = session.preview(action, target)
        self.assertEqual(preview, again)
        return session.confirm(again)

    def buy(self, session, *ids):
        for oid in ids:
            self.act(session, 'select', oid)
        return session.state

    def charges(self, state, base, **options):
        expected = {('configuration', state.configuration_id): base * 100}
        expected.update({('option', oid): amount * 100 for oid, amount in options.items()})
        actual = {(c.owner_kind, c.owner_id): c.amount_minor for c in state.charges}
        self.assertEqual(len(actual), len(state.charges), 'No duplicate charge owner')
        self.assertEqual(actual, expected)
        self.assertEqual(state.total_minor, sum(expected.values()))
        self.assertIn('partial_catalog_not_submission_ready', state.issues)

    def total(self, state, dollars):
        self.assertEqual(state.total_minor, dollars * 100)

    def cancel_remove_revert(self, session, action, target, expected):
        original = session.state
        preview = session.preview(action, target)
        self.total(preview.candidate, expected)
        self.assertIs(session.cancel(), original)
        self.assertEqual(session.state, original)
        with self.assertRaises(EvaluationError):
            session.confirm(preview)
        result = self.act(session, action, target)
        self.total(result, expected)
        self.assertEqual(session.revert(), original)
        return result

    def test_e01_uqt_context_reset(self):
        # ST-T02/O07; option row69 and variant override rows2–5.
        s = self.session('stingray', '1lt_c07')
        self.buy(s, 'opt_uqt_002')
        self.charges(s.state, 73495, opt_uqt_002=1495)
        self.total(s.state, 74990)
        self.act(s, 'configure', '2lt_c07')
        self.charges(s.state, 80595)
        self.assertEqual(s.state.intent, ())
        self.assertIn('opt_uqt_002', s.state.resolved)
        self.assertEqual({c.origin for c in s.state.causes if c.option_id == 'opt_uqt_002'}, {'standard'})
        with self.assertRaises(EvaluationError):
            s.preview('select', 'opt_uqt_002')
        self.act(s, 'configure', '1lt_c07')
        self.charges(s.state, 73495)
        self.assertNotIn('opt_uqt_002', s.state.resolved)

    def test_current_configuration_preserves_whole_state_and_undo(self):
        # Reuse the E04 interior and independent-belt ownership case.
        s = self.session('grand_sport', '3lt_e07')
        self.buy(s, 'opt_3f9_001', 'opt_g26_001')
        prior = s.state
        self.act(s, 'interior', '3LT_AE4_EL9')
        original = s.state
        self.assertEqual(original.intent, ('opt_3f9_001', 'opt_g26_001'))
        self.assertEqual(original.interior_id, '3LT_AE4_EL9')

        self.assertIs(s.evaluator.transition(original, 'configure', '3lt_e07'), original)
        for _ in range(2):  # A redundant event and its retry are both inert.
            preview = s.preview('configure', '3lt_e07')
            self.assertIs(s.state, original)
            self.assertEqual(preview.candidate, original)
            self.assertEqual(preview.added, frozenset())
            self.assertEqual(preview.removed, frozenset())
            self.assertEqual(preview.removed_intent, frozenset())
            self.assertFalse(preview.interior_changed)
            self.assertIs(s.cancel(), original)
            self.assertIs(self.act(s, 'configure', '3lt_e07'), original)
        self.assertEqual(s.revert(), prior)

        # An actual context change still clears both intent and interior.
        self.act(s, 'interior', '3LT_AE4_EL9')
        self.assertEqual(self.act(s, 'configure', '2lt_e07'),
                         s.evaluator.state('2lt_e07'))
        self.assertEqual(s.state.intent, ())
        self.assertIsNone(s.state.interior_id)
        self.assertEqual(s.revert(), original)

    def test_e02_pcx_replacement_and_absorption(self):
        # ST-O26/D06 and common policy: frozen coexistence 90,680 is rejected.
        s = self.session('stingray', '2lt_c07')
        self.buy(s, 'opt_qe6_001', 'opt_pcx_001')
        original = s.state
        self.charges(original, 80595, opt_qe6_001=1095, opt_pcx_001=4595,
                     opt_5dg_001=0, opt_sfz_001=0, opt_sht_001=0, opt_sng_001=0)
        self.total(original, 86285)
        candidate = s.preview('select', 'opt_5do_001').candidate
        self.charges(candidate, 80595, opt_qe6_001=1095, opt_5do_001=4395)
        self.total(candidate, 86085)
        self.assertEqual(candidate.intent, ('opt_qe6_001', 'opt_5do_001'))
        self.assertTrue({'opt_pcx_001', 'opt_5dg_001', 'opt_sfz_001', 'opt_sht_001', 'opt_sng_001'}.isdisjoint(candidate.resolved))
        self.assertEqual(s.cancel(), original)
        self.act(s, 'select', 'opt_5do_001')
        self.assertEqual(s.revert(), original)
        removed = self.cancel_remove_revert(s, 'remove', 'opt_pcx_001', 81690)
        self.charges(removed, 80595, opt_qe6_001=1095)
        # Prior child purchases are absorbed by this lane's package policy.
        t = self.session('stingray', '2lt_c07')
        self.buy(t, 'opt_sfz_001', 'opt_pcx_001')
        self.assertEqual(t.state.intent, ('opt_pcx_001',))
        self.act(t, 'remove', 'opt_pcx_001')
        self.assertNotIn('opt_sfz_001', t.state.resolved)

    def test_e02_reverse_conflict_order(self):
        s = self.session('stingray', '2lt_c07')
        self.buy(s, 'opt_5do_001')
        before = s.state
        preview = s.preview('select', 'opt_pcx_001')
        self.assertEqual(preview.candidate.intent, ('opt_pcx_001',))
        self.charges(preview.candidate, 80595, opt_pcx_001=4595, opt_5dg_001=0,
                     opt_sfz_001=0, opt_sht_001=0, opt_sng_001=0)
        self.assertEqual(s.cancel(), before)
        self.act(s, 'select', 'opt_pcx_001')
        self.assertNotIn('opt_5do_001', s.state.resolved)

    def gs_roof(self, independent=False):
        s = self.session('grand_sport', '2lt_e67')
        self.buy(s, 'opt_g26_001', 'opt_97a_001')
        self.charges(s.state, 102595, opt_g26_001=995, opt_z15_001=995)
        self.total(s.state, 104585)
        if independent:
            self.buy(s, 'opt_d84_001')
        self.buy(s, 'opt_dmx_001')
        self.charges(s.state, 102595, opt_g26_001=995, opt_z15_001=995,
                     opt_dmx_001=1295, opt_d84_001=1295)
        self.total(s.state, 107175)
        return s

    def test_e03_dependency_and_independent_removal(self):
        for independent in (False, True):
            with self.subTest(independent=independent):
                s = self.gs_roof(independent)
                causes = [c for c in s.state.causes if c.option_id == 'opt_d84_001']
                self.assertEqual({c.origin for c in causes}, {'dependency', 'independent'} if independent else {'dependency'})
                self.assertTrue(all(c.roots for c in causes))
                removed = self.cancel_remove_revert(s, 'remove', 'opt_dmx_001', 105880 if independent else 104585)
                self.assertEqual('opt_d84_001' in removed.resolved, independent)
                self.assertEqual('opt_d84_001' in removed.intent, independent)
                self.assertNotIn('opt_dmx_001', removed.resolved)
                # Accepted Sept15 direct removal removes stripe, preserves paint/hash.
                direct = self.cancel_remove_revert(s, 'remove', 'opt_d84_001', 104585)
                self.assertEqual(direct.intent, ('opt_g26_001', 'opt_97a_001'))
                self.assertEqual(direct.resolved, {'opt_g26_001', 'opt_97a_001', 'opt_z15_001'})

    def test_e03_condition_truth_and_body_scope(self):
        e = self.evaluator('grand_sport')
        for config in ('2lt_e67', '2lt_e07'):
            for paint in ('opt_g26_001', 'opt_g4z_001', 'opt_gbk_001', 'opt_gkz_001', 'opt_gph_001', None):
                for stripe in (True, False):
                    with self.subTest(config=config, paint=paint, stripe=stripe):
                        intent = ['opt_97a_001'] + ([paint] if paint else []) + (['opt_dmx_001'] if stripe else [])
                        # Predicate/acquisition control, not an invented full-build total.
                        causes, _ = e.closure(config, intent, None)
                        self.assertEqual(any(c.option_id == 'opt_d84_001' for c in causes),
                                         config == '2lt_e67' and bool(paint) and stripe)

    def test_e04_interior_owns_seat_once_and_two_belt_causes(self):
        s = self.session('grand_sport', '3lt_e07')
        self.act(s, 'interior', '3LT_AE4_EL9')
        self.charges(s.state, 100245, opt_ae4_002=595, opt_z25_001=1995, opt_3f9_001=0)
        self.total(s.state, 102835)
        self.assertEqual(s.state.resolved, {'opt_ae4_002', 'opt_z25_001', 'opt_3f9_001'})
        self.assertEqual(s.state.installed, s.state.resolved)
        self.assertEqual(s.state.intent, ())
        belt = [c for c in s.state.causes if c.option_id == 'opt_3f9_001']
        self.assertEqual(len(belt), 2)
        self.assertEqual({r for c in belt for r in c.roots}, {'interior:3LT_AE4_EL9'})
        cleared = self.cancel_remove_revert(s, 'interior', None, 100245)
        self.assertEqual(cleared.resolved, frozenset())
        self.assertIn('missing_required_interior', cleared.issues)
        t = self.session('grand_sport', '3lt_e07')
        self.act(t, 'interior', '3LT_AH2_EL9')
        self.charges(t.state, 100245, opt_ah2_001=0, opt_z25_001=1995, opt_3f9_001=0)
        self.total(t.state, 102240)
        with self.assertRaises(EvaluationError):
            self.session('grand_sport', '2lt_e07').preview('interior', '3LT_AE4_EL9')

    def test_e05_fed_equipment_round_trip(self):
        s = self.session('grand_sport_x', '1lt_g07')
        baseline = s.state
        equipment = {'opt_j57_001', 'opt_b4z_001', 'opt_fe5_001', 'opt_ls6_001', 'opt_xft_001'}
        self.assertEqual(baseline.installed, equipment)
        self.charges(baseline, 112195)
        self.buy(s, 'opt_fed_001')
        self.charges(s.state, 112195, opt_fed_001=500)
        self.assertEqual(s.state.installed, equipment - {'opt_xft_001'} | {'opt_fed_001', 'opt_xfr_001'})
        self.assertIn('opt_xft_001', s.state.standard)
        removed = self.cancel_remove_revert(s, 'remove', 'opt_fed_001', 112195)
        self.assertEqual(removed, baseline)

    def test_e06_request_transfer_rates_equipment_and_revert(self):
        s = self.session('z06', '2lz_h07')
        baseline = s.state
        self.charges(baseline, 130295, opt_r8e_002=2600)
        self.buy(s, 'opt_pdb_001')
        pdb = s.state
        self.charges(pdb, 130295, opt_r8e_002=2600, opt_pdb_001=16000,
                     opt_j57_001=0, opt_j6d_001=0, opt_roy_001=0)
        self.total(pdb, 148895)
        preview = s.preview('select', 'opt_z07_001')
        self.total(preview.candidate, 158790)
        self.assertEqual(s.cancel(), pdb)
        self.act(s, 'select', 'opt_z07_001')
        pdd = s.state
        self.assertEqual(pdd.intent, ('opt_pdd_001',))
        self.charges(pdd, 130295, opt_r8e_002=3000, opt_pdd_001=25495,
                     opt_z07_001=0, opt_t0f_001=0, opt_cfz_001=0, opt_j57_001=0,
                     opt_j6d_001=0, opt_roy_001=0)
        suppressed = {'opt_j56_001', 'opt_j6a_001', 'opt_soe_002', 'opt_t0e_001', 'opt_fe6_002', 'opt_xfr_001'}
        self.assertTrue(suppressed.isdisjoint(pdd.installed))
        self.assertEqual(pdd.installed, {'opt_pdd_001', 'opt_z07_001', 'opt_t0f_001', 'opt_cfz_001', 'opt_j57_001', 'opt_j6d_001', 'opt_fe7_001', 'opt_xfs_001', 'opt_roy_001', 'opt_r8e_002'})
        self.assertEqual(len([c for c in pdd.causes if c.option_id == 'opt_cfz_001']), 2)
        self.buy(s, 'opt_roz_001')
        self.charges(s.state, 130295, opt_r8e_002=3000, opt_pdd_001=26495,
                     opt_z07_001=0, opt_t0f_001=0, opt_cfz_001=0, opt_j57_001=0,
                     opt_j6d_001=0, opt_roz_001=0)
        self.total(s.state, 159790)
        self.assertNotIn('opt_roy_001', s.state.resolved)
        self.assertEqual(s.revert(), pdd)
        removed = self.cancel_remove_revert(s, 'remove', 'opt_pdd_001', 132895)
        self.assertEqual(removed, baseline)

    def test_e06_reverse_conflict_and_explicit_wheel_before_default(self):
        s = self.session('z06', '2lz_h07')
        self.buy(s, 'opt_z07_001')
        before = s.state
        preview = s.preview('select', 'opt_pdb_001')
        self.assertEqual(preview.candidate.intent, ('opt_pdb_001',))
        self.charges(preview.candidate, 130295, opt_r8e_002=2600, opt_pdb_001=16000,
                     opt_j57_001=0, opt_j6d_001=0, opt_roy_001=0)
        self.assertEqual(s.cancel(), before)
        self.act(s, 'select', 'opt_pdb_001')
        self.assertNotIn('opt_z07_001', s.state.resolved)
        # Explicit peer first must suppress, not race, an eligible package default.
        t = self.session('z06', '2lz_h07')
        self.buy(t, 'opt_roz_001', 'opt_pdd_001')
        self.total(t.state, 159790)
        self.assertNotIn('opt_roy_001', t.state.resolved)
        self.assertEqual(t.state.intent, ('opt_roz_001', 'opt_pdd_001'))

    def test_e07_e08_local_tom_ownership_and_paid_acquisition(self):
        # ZR1-D06/08 and ZR1X-D06/08/09; distinct IDs and local price bases.
        for model, config, tom, base, gas, package, suspension, track, start, paid, both in (
            ('zr1', '1lz_r07', 'opt_tom_001', 197195, 3000, 5995, 'opt_fe8_002', 'opt_fej_001', 200195, 213190, 219185),
            ('zr1x', '1lz_s07', 'opt_tom_002', 227395, 2600, 1500, 'opt_feh_002', 'opt_fez_001', 229995, 242990, 244490),
        ):
            for independent in (False, True):
                with self.subTest(model=model, independent=independent):
                    s = self.session(model, config)
                    baseline = s.state
                    self.charges(baseline, base, opt_r8e_002=gas)
                    self.total(baseline, start)
                    if independent:
                        self.buy(s, tom)
                        self.total(s.state, paid)
                    self.buy(s, 'opt_ztk_001')
                    before = s.state
                    self.total(before, both)
                    expected = {tom: 12995, 'opt_r8e_002': gas, 'opt_ztk_001': package, track: 0}
                    if model == 'zr1':
                        expected['opt_j59_002'] = 0
                    self.charges(before, base, **expected)
                    self.assertTrue({suspension, 'opt_xfr_001', 'opt_t0e_001'}.isdisjoint(before.installed))
                    self.assertTrue({track, 'opt_xfs_001', 'opt_j59_002', tom}.issubset(before.installed))
                    self.buy(s, tom)  # locked click cannot create independent intent
                    self.assertEqual(s.state, before)
                    self.assertEqual(tom in before.intent, independent)
                    removed = self.cancel_remove_revert(s, 'remove', 'opt_ztk_001', paid if independent else start)
                    self.assertEqual(tom in removed.resolved, independent)
                    if not independent:
                        self.assertEqual(removed, baseline)
                    direct = self.cancel_remove_revert(s, 'remove', tom, start)
                    self.assertEqual(direct, baseline)

    def test_scope_missing_price_and_factory_rejections_are_atomic(self):
        s = self.session('zr1x', '1lz_s07')
        original = s.state
        for action, target in [('select', 'opt_tom_001'), ('configure', '1lz_r07'), ('select', 'opt_feh_002'), ('remove', 'opt_j59_002')]:
            with self.assertRaises(EvaluationError):
                s.preview(action, target)
            self.assertIs(s.state, original)
        # Synthetic missing-rate/lifecycle defects, not accepted catalog facts.
        s.evaluator.options['opt_tom_002']['purchase_amount_minor'] = None
        with self.assertRaisesRegex(EvaluationError, 'price'):
            s.preview('select', 'opt_tom_002')
        self.assertIs(s.state, original)
        s.evaluator.options['opt_tom_002']['lifecycle'] = 'factory_unavailable'
        with self.assertRaises(EvaluationError):
            s.preview('select', 'opt_tom_002')
        self.assertIs(s.state, original)

    def test_stale_and_foreign_previews_rejected(self):
        s = self.session('stingray', '1lt_c07')
        p = s.preview('select', 'opt_uqt_002')
        q = s.preview('select', 'opt_qe6_001')
        with self.assertRaises(EvaluationError):
            s.confirm(p)
        s.confirm(q)
        with self.assertRaises(EvaluationError):
            s.confirm(q)
        other = self.session('stingray', '1lt_c07')
        with self.assertRaises(EvaluationError):
            other.confirm(q)

    def test_independent_belt_survives_interior_cause_loss(self):
        # GS-D05/preserve-prior: three causes, one zero line while EL9 is chosen;
        # clearing the leaf restores the independent belt's source price of 595.
        s = self.session('grand_sport', '3lt_e07')
        self.buy(s, 'opt_3f9_001')
        self.act(s, 'interior', '3LT_AE4_EL9')
        self.assertEqual(len([c for c in s.state.causes if c.option_id == 'opt_3f9_001']), 3)
        self.charges(s.state, 100245, opt_ae4_002=595, opt_z25_001=1995, opt_3f9_001=0)
        self.act(s, 'interior', None)
        self.assertEqual(s.state.intent, ('opt_3f9_001',))
        self.charges(s.state, 100245, opt_3f9_001=595)
        self.assertEqual({c.origin for c in s.state.causes}, {'independent'})

    def test_evaluation_ignores_sql_row_order_and_does_not_write(self):
        e = self.evaluator('z06')
        expected = e.state('2lz_h07', ('opt_pdd_001', 'opt_roz_001'))
        changes = self.db.total_changes
        rng = random.Random(42)
        for rows in e.rows.values():
            rng.shuffle(rows)
        self.assertEqual(e.state('2lz_h07', ('opt_pdd_001', 'opt_roz_001')), expected)
        self.assertEqual(self.evaluator('z06').state('2lz_h07', ('opt_pdd_001', 'opt_roz_001')), expected)
        self.assertEqual(self.db.total_changes, changes)

    def test_invalid_independent_state_and_revision_boundaries(self):
        e = self.evaluator('stingray')
        with self.assertRaises(EvaluationError):
            e.state('1lt_c07', ('opt_uqt_002', 'opt_uqt_002'))
        with self.assertRaises(EvaluationError):
            e.state('2lt_c07', ('opt_uqt_002',))
        with self.assertRaises(EvaluationError):
            e.transition(self.session('zr1', '1lz_r07').state, 'select', 'opt_uqt_002')
        s = Session(e, '1lt_c07')
        before = s.state
        e.statuses['opt_uqt_002', '1lt_c07'] = 'unavailable'
        with self.assertRaises(EvaluationError):
            s.preview('select', 'opt_uqt_002')
        self.assertIs(s.state, before)

    def test_synthetic_ambiguous_replacement_fails_without_commit(self):
        s = self.session('stingray', '2lt_c07')
        self.buy(s, 'opt_pcx_001')
        before = s.state
        row = dict(s.evaluator.rows['replacement_plan'][0], id='synthetic-plan')
        s.evaluator.rows['replacement_plan'].append(row)
        s.evaluator.scopes['replacement_plan'].add((row['id'], '2lt_c07'))
        with self.assertRaisesRegex(EvaluationError, 'Ambiguous applicable replacements'):
            s.preview('select', 'opt_5do_001')
        self.assertIs(s.state, before)

    def test_synthetic_absence_oscillation_and_rootless_cycle(self):
        s = self.session('stingray', '1lt_c07')
        e = s.evaluator
        # Synthetic UQT iff absent: no stable solution; do not commit a partial state.
        cid = 'synthetic-absence'
        e.conditions[cid] = {'mode': 'conjunction'}
        e.rows['condition_clause'].append(dict(condition_id=cid, clause_id='1', mode='none_present'))
        e.rows['condition_member'].append(dict(condition_id=cid, clause_id='1', option_id='opt_uqt_002', interior_id=None, group_id=None, state='resolved_selection'))
        row = dict(e.rows['acquisition'][0], id='synthetic-oscillation', condition_id=cid, target_option_id='opt_uqt_002', origin_kind='default')
        e.rows['acquisition'].append(row)
        e.scopes['acquisition'].add((row['id'], '1lt_c07'))
        original = s.state
        with self.assertRaisesRegex(EvaluationError, 'nonconvergence'):
            s.preview('select', 'opt_qe6_001')
        self.assertIs(s.state, original)
        # Synthetic positive A <-> B cycle has no life without a root.
        e.rows['acquisition'].remove(row)
        for a, b in [('opt_uqt_002', 'opt_qe6_001'), ('opt_qe6_001', 'opt_uqt_002')]:
            cid = 'synthetic-' + a
            e.conditions[cid] = {'mode': 'conjunction'}
            e.rows['condition_clause'].append(dict(condition_id=cid, clause_id='1', mode='any_present'))
            e.rows['condition_member'].append(dict(condition_id=cid, clause_id='1', option_id=a, interior_id=None, group_id=None, state='resolved_selection'))
            row = dict(row, id=cid, condition_id=cid, target_option_id=b, origin_kind='included')
            e.rows['acquisition'].append(row)
            e.scopes['acquisition'].add((cid, '1lt_c07'))
        self.assertEqual(e.state('1lt_c07').resolved, frozenset())
        rooted = e.state('1lt_c07', ('opt_uqt_002',))
        self.assertEqual(rooted.resolved, {'opt_uqt_002', 'opt_qe6_001'})
        self.assertTrue(all(c.roots == {'opt_uqt_002'} for c in rooted.causes))
        self.assertEqual(e.state('1lt_c07').resolved, frozenset())

    def test_synthetic_ambiguous_group_defaults_and_scope(self):
        s = self.session('z06', '2lz_h07')
        e = s.evaluator
        original = s.state
        row = next(r for r in e.rows['acquisition'] if r['target_option_id'] == 'opt_roy_001')
        competing = dict(row, id='synthetic-peer', target_option_id='opt_roz_001')
        e.rows['acquisition'].append(competing)
        e.scopes['acquisition'].add((competing['id'], '2lz_h07'))
        with self.assertRaisesRegex(EvaluationError, 'Ambiguous competing defaults'):
            s.preview('select', 'opt_pdb_001')
        self.assertIs(s.state, original)
        e.rows['acquisition'].remove(competing)
        e.scopes['choice_group'].remove(('z06_group_pdb_requires_carbon_wheel', '2lz_h07'))
        with self.assertRaisesRegex(EvaluationError, 'out-of-scope group'):
            s.preview('select', 'opt_pdb_001')
        self.assertIs(s.state, original)


if __name__ == '__main__':
    unittest.main()
