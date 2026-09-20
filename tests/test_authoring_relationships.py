"""Direct inclusion authoring: source-derived behavior and transactional guards."""
from contextlib import closing
import unittest
from unittest.mock import patch

import test_authoring as base
from catalog import authoring as a, authoring_relationships as r
from catalog.authoring_server import Application
from catalog.evaluator import Evaluator
from catalog.releases import database_hash, validate_translation


class RelationshipTests(unittest.TestCase):
    setUpClass = classmethod(base.AuthoringTests.setUpClass.__func__)
    tearDownClass = classmethod(base.AuthoringTests.tearDownClass.__func__)

    def setUp(self):
        base.AuthoringTests.setUp(self)
        r.prepare(self.db)
        self.rid = 'rule_opt_pdy_001_includes_opt_ryt_001'
        self.target = 'opt_ryt_001'

    def change(self, **kwargs):
        detail = r.detail(self.db, self.rev, self.rid)
        return r.preview(self.db, self.rev, self.rid, **(dict(etag=detail['etag'],intent_policy='absorb_prior',reason='Synthetic local inclusion review') | kwargs))

    def test_connected_save_restore_and_model_isolation(self):
        # Frozen Stingray PDY includes RYT + S08 and preserves a prior RYT purchase.
        # Synthetic edit absorbs the prior purchase;
        # no accepted source/business correction is asserted by this exercise.
        before = r.detail(self.db, self.rev, self.rid)
        self.assertEqual(before['relationship']['target_rpo'], 'RYT')
        others = [tuple(x) for x in self.db.execute('SELECT * FROM acquisition WHERE revision_id<>?', (self.rev,))]
        change = self.change()
        for b, c in zip(change['before_outcomes'], change['after_outcomes']):
            self.assertIn('opt_ryt_001', {o['option_id'] for o in b['selected']['resolved']})
            ids = {o['option_id'] for o in c['selected']['resolved']}
            self.assertIn('opt_ryt_001', ids)
            self.assertIn(self.target, b['removed']['intent'])
            self.assertNotIn(self.target, c['removed']['intent'])
            self.assertTrue({'opt_pdy_001','opt_s08_001',self.target} <= ids)
            self.assertEqual(b['selected']['total_minor'], c['selected']['total_minor'])
            self.assertNotIn(self.target, {o['option_id'] for o in c['removed']['resolved']})
        saved = r.save(self.db, change)
        self.assertEqual(saved['edit_version'], before['edit_version'] + 1)
        self.assertEqual(saved['history'][0]['before'], change['before'])
        self.assertEqual(saved['evidence'], before['evidence'])
        self.assertEqual(saved['configurations'], before['configurations'])
        self.assertEqual(saved['relationship']['target_option_id'], self.target)
        self.assertEqual(others, [tuple(x) for x in self.db.execute('SELECT * FROM acquisition WHERE revision_id<>?', (self.rev,))])
        with closing(a.open_workspace(self.path)) as reopened:
            self.assertEqual(r.detail(reopened, self.rev, self.rid)['history'], saved['history'])
            ev = Evaluator(reopened, self.rev)
            state = ev.transition(ev.state('1lt_c07'), 'select', 'opt_pdy_001')
            self.assertIn(self.target, state.resolved)
        restored = r.save(self.db, self.change(intent_policy='preserve_prior'))
        self.assertEqual(restored['relationship'], before['relationship'])
        self.assertEqual(len(restored['history']), 2)
        with self.assertRaisesRegex(ValueError, 'Unexpected source translation schema'):
            validate_translation(self.db)
        with closing(a.open_workspace(self.template)) as source:
            self.assertEqual(source.execute('SELECT baseline_sha256 FROM authoring_workspace').fetchone()[0], self.source_digest)

    def test_preview_cancel_replay_and_client_substitution(self):
        app = Application(self.path)
        current = r.detail(self.db, self.rev, self.rid)
        body = dict(revision_id=self.rev,acquisition_id=self.rid,etag=current['etag'],intent_policy='absorb_prior',reason='Browser exercise')
        before = database_hash(self.db)
        first = app.dispatch('/api/relationship/preview', body)
        self.assertEqual(database_hash(self.db), before)
        app.dispatch('/api/cancel', {'token': first['token']})
        with self.assertRaisesRegex(ValueError, 'Preview expired'):
            app.dispatch('/api/relationship/save', {'token': first['token']})
        second = app.dispatch('/api/relationship/preview', body)
        saved = app.dispatch('/api/relationship/save', {'token': second['token'], 'intent_policy': 'preserve_prior'})
        self.assertEqual(saved['relationship']['intent_policy'], 'absorb_prior')
        with self.assertRaisesRegex(ValueError, 'Preview expired'):
            app.dispatch('/api/relationship/save', {'token': second['token']})

    def test_stale_dependency_changes_and_write_failure_rollback(self):
        change = self.change()
        with closing(a.open_workspace(self.path)) as other:
            with other:
                other.execute('UPDATE option SET purchase_amount_minor=purchase_amount_minor+1 WHERE revision_id=? AND id=?', (self.rev,self.target))
        with self.assertRaisesRegex(ValueError, 'Stale edit'):
            r.save(self.db, change)
        change = self.change()
        before = database_hash(self.db)
        with patch('catalog.authoring_relationships.validate_mappings', side_effect=ValueError('injected validation failure')):
            with self.assertRaisesRegex(ValueError, 'injected'):
                r.save(self.db, change)
        self.assertEqual(database_hash(self.db), before)
        self.assertFalse(self.db.in_transaction)
        with patch('catalog.authoring_relationships.outcomes', side_effect=[change['before_outcomes'], ValueError('candidate failure')]):
            with self.assertRaisesRegex(ValueError, 'candidate failure'):
                self.change()
        self.assertEqual(database_hash(self.db), before)
        self.assertFalse(self.db.in_transaction)

    def test_refuse_invalid_policies_and_unverifiable_candidates(self):
        for target in ('unknown','', 'preserve_prior'):
            with self.subTest(target=target), self.assertRaises(ValueError):
                self.change(intent_policy=target)
        with self.assertRaisesRegex(ValueError, 'reason'):
            self.change(reason=' ')
        with self.assertRaisesRegex(ValueError, 'direct option inclusion'):
            r.detail(self.db, self.rev, 'not-a-relationship')
        before = database_hash(self.db)
        # Target with an unmet continuing requirement cannot be demonstrated.
        with self.assertRaises(ValueError):
            row = r.detail(self.db, self.rev, 'rule_opt_z51_001_includes_opt_j55_001')
            r.preview(self.db,self.rev,row['relationship']['id'],row['etag'],'absorb_prior','Unverifiable purchase')
        self.assertEqual(database_hash(self.db), before)

    def test_each_lane_lists_only_owned_direct_relationships(self):
        for revision in self.revisions.values():
            rows = r.relationships(self.db, revision)
            self.assertTrue(rows)
            self.assertEqual({row['revision_id'] for row in rows}, {revision})
            detail = r.detail(self.db, revision, rows[0]['id'])
            self.assertEqual({c['revision_id'] for c in detail['configurations']}, {revision})


if __name__ == '__main__':
    unittest.main()
