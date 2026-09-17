"""Evidence-authored lane cases and guards for the whole-revision audit.

The larger relational matrix is run explicitly with catalog.semantic_validation;
these checks catch audit blind spots and policy regressions without duplicating it.
"""
import json
import unittest
from unittest.mock import patch

from catalog import foundation as f
from catalog.behavior_sources import import_behavior
from catalog.evaluator import EvaluationError, Session
from catalog.semantic_validation import Audit, findings
from catalog.foundation_schema import SCOPES


class SemanticValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = f.connect(':memory:')
        f.create_schema(cls.db)
        import_behavior(cls.db)
        cls.audits = {model: Audit(cls.db, rev) for model, rev in cls.db.execute('''SELECT model_key,revision_id
            FROM catalog_revision JOIN model_year USING(model_year_id) JOIN model USING(model_id)''')}

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    def oid(self, e, code):
        row, = [r for r in e.options.values() if r['rpo'] == code and r['lifecycle'] == 'active']
        return row['id']

    def test_shared_policy_precedence_and_lane_boundaries(self):
        policy = json.loads((f.ROOT / 'docs/compatibility-notice-policy.json').read_text())
        self.assertEqual(policy['review_state'], 'accepted')
        self.assertEqual(policy['direct_dependency_removal']['review_state'], 'accepted')
        self.assertEqual(set(policy['model_overrides']), set(self.audits))
        for lane, audit in self.audits.items():
            e = audit.ev
            with self.subTest(lane=lane):
                row, = e.rows['interaction_policy']
                self.assertEqual({k: row[k] for k in ('conflict_action', 'direct_removal_action', 'cancel_action', 'revert_action')},
                                 dict(conflict_action='notice_confirm_cancel', direct_removal_action='remove_requested_and_supporting_sources',
                                      cancel_action='preserve_whole_state', revert_action='restore_whole_state'))
                self.assertTrue(self.db.execute('''SELECT 1 FROM evidence_member m JOIN source_anchor a USING(anchor_id)
                    JOIN source_document d USING(document_id) WHERE m.set_id=? AND d.source_path=?''',
                    (row['evidence_set_id'], 'docs/compatibility-notice-policy.json')).fetchone())
                inventory = audit.inventory()
                for table in SCOPES:
                    self.assertEqual({r['id'] for r in e.rows[table]}, {r['id'] for r in inventory if r['table'] == table})
                self.assertTrue(all(r['evidence'] for r in inventory))
        for lane, old in [('grand_sport','GS-D12'), ('grand_sport_x','GSX-D06'), ('z06','Z06-D05')]:
            self.assertIn(old, policy['model_overrides'][lane]['superseded_ui_decision_ids'])
        z06 = policy['model_overrides']['z06']['pdb_z07_interaction']
        self.assertFalse(z06['coexistence_allowed'])
        self.assertFalse(z06['pdf_substitution_authorized'])

    def test_all_lane_independent_roof_pouch_transactions_and_exact_charges(self):
        # Each lane owner policy preserves independently purchased SC7 after
        # SBT removal; source SBT=2525 and standalone SC7=195, no extra package fee.
        for lane, audit in self.audits.items():
            e = audit.ev
            for config, cfg in e.configs.items():
                if cfg['body'] != 'coupe':
                    continue
                pouch, roof, paint = (self.oid(e, c) for c in ('SC7', 'SBT', 'GBA'))
                for prior in (False, True):
                    with self.subTest(lane=lane, config=config, prior=prior):
                        s = Session(e, config)
                        s.confirm(s.preview('select', paint))
                        base = s.state.total_minor
                        if prior:
                            s.confirm(s.preview('select', pouch))
                        s.confirm(s.preview('select', roof))
                        before = s.state
                        self.assertEqual(before.total_minor - base, 252500)
                        result = audit.probe(before, 'remove', roof, retained=[paint])
                        self.assertEqual(result['status'], 'passed', result)
                        after = audit.transaction(before, 'remove', roof)[2]
                        self.assertEqual(pouch in after.intent, prior)
                        self.assertEqual(pouch in after.resolved, prior)
                        self.assertEqual(after.total_minor - base, 19500 if prior else 0)
                        result = audit.probe(before, 'remove', pouch, absent=[pouch, roof], retained=[paint])
                        self.assertEqual(result['status'], 'passed', result)
                        self.assertEqual(audit.transaction(before, 'remove', pouch)[2].total_minor, base)

    def test_package_ownership_exceptions_use_actual_transition_history(self):
        # ST-D06 absorbs prior SFZ; Z06-D02 preserves prior SHT. Similar-looking
        # packages must never acquire one another's ownership policy.
        for lane, config, package, child, retain in [('stingray','2lt_c07','PCX','SFZ',False),
                                                    ('z06','2lz_h07','PCZ','SHT',True)]:
            a = self.audits[lane]
            e = a.ev
            package, child, paint = (self.oid(e, x) for x in (package, child, 'GBA'))
            s = Session(e, config)
            for target in (paint, child, package):
                s.confirm(s.preview('select', target))
            before = s.state
            self.assertEqual(child in before.intent, retain)
            self.assertEqual(a.probe(before, 'remove', package, retained=[paint])['status'], 'passed')
            after = a.transaction(before, 'remove', package)[2]
            self.assertEqual(child in after.resolved, retain)
            self.assertEqual(child in after.intent, retain)
            self.assertEqual(a.probe(before, 'remove', child, absent=[child, package], retained=[paint])['status'], 'passed')

    def test_removing_interior_owned_seat_clears_leaf_and_restores_everything_on_revert(self):
        # Common September 15 policy: an interior is a supporting owner too.
        # Direct seat removal clears its leaf; independently owned belt and paint
        # survive. No replacement leaf may be invented.
        for lane, a in self.audits.items():
            e = a.ev
            for config, cfg in e.configs.items():
                if not cfg['trim'].startswith('3'):
                    continue
                leaf = '3LT_AE4_EL9' if lane in ('grand_sport','grand_sport_x') else (
                    '3LT_AE4_HVZ' if lane == 'stingray' else '3LZ_AE4_HVZ')
                seat = e.interiors[leaf]['seat_option_id']
                belt, paint = (self.oid(e,x) for x in ('3F9','GBA'))
                s = Session(e, config)
                for target in (belt,paint):
                    s.confirm(s.preview('select',target))
                prior = s.state
                s.confirm(s.preview('interior',leaf))
                before = s.state
                preview = s.preview('remove',seat)
                self.assertIn(seat,preview.removed)
                self.assertTrue(preview.interior_changed)
                self.assertIsNone(preview.candidate.interior_id)
                self.assertEqual(set(preview.candidate.intent),set(prior.intent))
                self.assertTrue({belt,paint}.issubset(preview.candidate.resolved))
                self.assertIn('missing_required_interior',preview.candidate.issues)
                self.assertEqual(preview.candidate,prior)
                self.assertIs(s.cancel(),before)
                s.confirm(s.preview('remove',seat))
                self.assertEqual(s.revert(),before)

    def test_yielding_package_child_keeps_its_owner_during_dependency_cleanup(self):
        # Z06 PDF/PDD supply ROY, which permits a different factory wheel.
        # ROY still depends on J57. Removing included Z07 loses J57 and must
        # remove the supplying package, regardless of which requirement is read
        # first; yielding does not make the package's ownership disappear.
        a = self.audits['z06']
        e = a.ev
        z07, paint = (self.oid(e,c) for c in ('Z07','GBA'))
        for config in e.configs:
            for code in ('PDD','PDF'):
                with self.subTest(config=config,package=code):
                    s = Session(e,config)
                    s.confirm(s.preview('select',paint))
                    original = s.state
                    package = self.oid(e,code)
                    s.confirm(s.preview('select',package))
                    before = s.state
                    result = a.probe(before,'remove',z07,absent=[package,z07],retained=[paint])
                    self.assertEqual(result['status'],'passed',result)
                    self.assertEqual(a.transaction(before,'remove',z07)[2],original)

    def test_conflicting_independent_peer_yields_without_removing_compatible_package(self):
        a = self.audits['stingray']
        e = a.ev
        z51,t0a,tvs = (self.oid(e,c) for c in ('Z51','T0A','TVS'))
        for config in e.configs:
            s = Session(e,config)
            for target in (z51,t0a):
                s.confirm(s.preview('select',target))
            result = a.probe(s.state,'select',tvs,absent=[t0a],retained=[z51,tvs])
            self.assertEqual(result['status'],'passed',result)

    def test_conditional_default_absence_uses_its_disabling_selection(self):
        a = self.audits['zr1']
        e = a.ev
        efr,zyc = (self.oid(e,c) for c in ('EFR','ZYC'))
        for config in e.configs:
            state = a.witness(config,absent=[efr])
            self.assertIsNotNone(state)
            self.assertIn(zyc,state.intent)
            self.assertNotIn(efr,state.resolved)

    def test_replacement_purchase_wins_conflicts_after_consuming_the_request(self):
        # Common Z06 override: requesting Z07 with PDB commits PDD. PDD is the
        # accepted purchase root; the consumed Z07 request must not cause a
        # refusal when an existing choice (e.g. CBF or 5ZV) conflicts with PDD.
        a = self.audits['z06']
        e = a.ev
        pdb,pdd,z07 = (self.oid(e,c) for c in ('PDB','PDD','Z07'))
        for config in e.configs:
            base = e.transition(e.state(config),'select',pdb)
            for oid in e.options:
                if not a.selectable(config,oid):
                    continue
                try:
                    before = e.transition(base,'select',oid)
                except EvaluationError:
                    continue  # Extra choice needs an unselected prerequisite.
                if pdb not in before.resolved:
                    continue  # This is not a PDB -> PDD replacement context.
                with self.subTest(config=config,extra=oid):
                    result = a.probe(before,'select',z07,absent=[pdb],retained=[pdd,z07])
                    self.assertEqual(result['status'],'passed',result)
                    after = a.transaction(before,'select',z07)[2]
                    self.assertIn(pdd,after.intent)
                    self.assertNotIn(z07,after.intent)

    def test_replacement_without_requested_option_is_refused_without_losing_undo(self):
        e = self.audits['z06'].ev
        pdb, z07, paint = (self.oid(e, c) for c in ('PDB', 'Z07', 'GBA'))
        plan, = [r for r in e.rows['replacement_plan'] if r['requested_option_id'] == z07]
        # Synthetic mistranslation: a valid but unrelated purchase replaces PDB.
        actions = [dict(r, option_id=paint) if r['plan_id'] == plan['id'] and r['action'] == 'add'
                   else r for r in e.rows['replacement_action']]
        for config in e.configs:
            with self.subTest(config=config):
                s = Session(e, config)
                original = s.state
                s.confirm(s.preview('select', pdb))
                before = s.state
                with patch.dict(e.rows, replacement_action=actions):
                    with self.assertRaisesRegex(EvaluationError, 'Requested option cannot satisfy its prerequisites'):
                        s.preview('select', z07)
                self.assertIs(s.state, before)
                self.assertIs(s.cancel(), before)
                self.assertEqual(s.revert(), original)

    def test_replacement_without_witness_records_unresolved_or_proved_inapplicable(self):
        a = self.audits['z06']
        for proof, status in ((None, 'unresolved'), ('Synthetic disjoint condition', 'inapplicable')):
            with self.subTest(status=status), patch.object(a, 'witness', return_value=None), \
                    patch.object(a, 'disjoint', return_value=proof):
                entries = a.run(tables=['replacement_plan'])
            plans = [entry for entry in entries if entry['table'] == 'replacement_plan']
            self.assertTrue(plans)
            for entry in plans:
                checks = [c for c in entry['checks'] if c['kind'] == 'replacement']
                self.assertEqual({c['configuration'] for c in checks}, set(entry['configurations']))
                self.assertEqual(len(checks), len(entry['configurations']))
                self.assertTrue(all(c['status'] == status for c in checks))
            problems = findings({'lanes': {'z06': {'inventory': entries}}})
            self.assertEqual(bool(problems), status == 'unresolved')
            if problems:
                self.assertTrue(any(p['kind'] == 'replacement' for p in problems))

    def test_removing_absent_supplied_peer_preserves_build_and_undo(self):
        # After choosing ROZ instead of PDD's default ROY, ROY is absent.
        # A redundant removal must not destroy PDD and the selected ROZ wheel.
        e = self.audits['z06'].ev
        pdd,roy,roz = (self.oid(e,c) for c in ('PDD','ROY','ROZ'))
        for config in e.configs:
            s = Session(e,config)
            s.confirm(s.preview('select',pdd))
            previous = s.state
            s.confirm(s.preview('select',roz))
            before = s.state
            self.assertNotIn(roy,before.resolved)
            preview = s.preview('remove',roy)
            self.assertIs(preview.candidate,before)
            self.assertEqual(preview.removed,frozenset())
            self.assertIs(s.cancel(),before)
            self.assertIs(s.confirm(s.preview('remove',roy)),before)
            self.assertEqual(s.revert(),previous)

    def test_equal_rank_compatible_causes_are_retained_in_both_orders(self):
        # ZR1X source inclusions: 5JR and ZYC independently supply DRG. Their
        # equal priority does not select a winner or eliminate either owner.
        a = self.audits['zr1x']
        e = a.ev
        child, left, right = (self.oid(e, x) for x in ('DRG','5JR','ZYC'))
        for config in e.configs:
            for first, second in ((left,right),(right,left)):
                s = Session(e,config)
                for target in (first,second):
                    s.confirm(s.preview('select',target))
                before = s.state
                self.assertEqual(len([c for c in before.causes if c.option_id == child]), 2)
                result = a.probe(before,'remove',first,retained=[second,child])
                self.assertEqual(result['status'],'passed',result)
                after = a.transaction(before,'remove',first)[2]
                self.assertEqual(len([c for c in after.causes if c.option_id == child]), 1)
                result = a.probe(after,'remove',second,absent=[child,first,second])
                self.assertEqual(result['status'],'passed',result)

    def test_audit_detects_silent_noop_instead_of_accepting_transaction_symmetry(self):
        a = self.audits['grand_sport_x']
        e = a.ev
        first, second = (self.oid(e, x) for x in ('DPB','VPW'))
        before = e.transition(e.state('1lt_g67'), 'select', first)
        # A resolver that does nothing passes preview/cancel/revert symmetry.
        # The independent exclusion postcondition must still reject it.
        a.transactions.clear()
        with patch.object(e, 'transition', return_value=before):
            self.assertEqual(a.probe(before, 'select', second, absent=[first])['status'], 'failed')
        a.transactions.clear()
        self.assertEqual(a.probe(before, 'select', second, absent=[first])['status'], 'passed')

    def test_condition_witnesses_respect_interior_ownership_and_implicit_children(self):
        a = self.audits['zr1x']
        e = a.ev
        state = a.witness('3lz_s07', [self.oid(e,'ZTK'), self.oid(e,'FEZ')])
        self.assertIsNotNone(state)
        self.assertIn(self.oid(e,'FEZ'), state.resolved)
        # EJH supplies its own belt; competing paid belts cannot coexist just
        # because the color-override table retains that historical condition.
        self.assertIsNotNone(a.disjoint('3lz_s07', {'interior:3LZ_AE4_EJH',self.oid(e,'3A9')}, set()))
        self.assertIsNone(a.witness('3lz_s07', {'interior:3LZ_AE4_EJH',self.oid(e,'3A9')}))
        gs = self.audits['grand_sport']
        self.assertIsNotNone(gs.disjoint('3lt_e07', {'opt_z25_001', 'interior:3LT_AE4_HVZ'}, set()))
        self.assertIsNone(gs.disjoint('3lt_e07', {'opt_z25_001', 'interior:3LT_AE4_EL9'}, set()))


if __name__ == '__main__':
    unittest.main()
