"""Option authoring persistence, transactional safety and consumer effects."""
from contextlib import closing
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from catalog import authoring as a, foundation as f
from catalog.behavior_sources import import_behavior
from catalog.consumers import ConsumerCatalog, import_mappings
from catalog.authoring_server import Application
from catalog.releases import database_hash, validate_translation


class AuthoringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = tempfile.TemporaryDirectory()
        cls.source = Path(cls.root.name) / 'source.sqlite'
        cls.template = Path(cls.root.name) / 'authoring.sqlite'
        with closing(f.connect(cls.source)) as db:
            f.create_schema(db)
            import_behavior(db)
            import_mappings(db)
            cls.source_digest = database_hash(db)
        a.initialize(cls.source, cls.template)

    @classmethod
    def tearDownClass(cls):
        cls.root.cleanup()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'draft.sqlite'
        self.db = f.connect(self.path)
        self.addCleanup(self.db.close)
        with closing(a.open_workspace(self.template)) as src:
            src.backup(self.db)
        self.revisions = {r['model_key']: r['revision_id'] for r in a.catalog(self.db)}
        self.rev = self.revisions['stingray']
        self.oid, = self.db.execute("SELECT id FROM option WHERE revision_id=? AND rpo='RYT'", (self.rev,)).fetchone()

    def change(self, revision=None, option=None, **values):
        revision, option = revision or self.rev, option or self.oid
        current = a.detail(self.db, revision, option)
        row = current['option']
        amount = row['purchase_amount_minor']
        values = dict(name=row['name'] + ' reviewed', price=None if amount is None else f'{amount // 100}.{amount % 100:02d}',
                      reason='Local authoring test', etag=current['etag']) | values
        return a.preview(self.db, revision, option, **values)

    def test_source_copy_and_release_boundary(self):
        with closing(f.connect(self.source)) as source:
            self.assertEqual(database_hash(source), self.source_digest)
        self.assertEqual(self.db.execute('SELECT baseline_sha256 FROM authoring_workspace').fetchone()[0], self.source_digest)
        with self.assertRaisesRegex(ValueError, 'Unexpected source translation schema'):
            validate_translation(self.db)
        existing = self.path.read_bytes()
        with self.assertRaises(FileExistsError):
            a.initialize(self.source, self.path)
        self.assertEqual(self.path.read_bytes(), existing)
        with self.assertRaises(Exception):
            a.open_workspace(self.source)

    def test_preview_cancel_and_server_token_replay(self):
        app = Application(self.path)
        data = a.detail(self.db, self.rev, self.oid)
        before = database_hash(self.db)
        body = dict(revision_id=self.rev, option_id=self.oid, etag=data['etag'], name='Reviewed first aid kit',
                    price='1234.56', reason='Review UI exercise')
        first = app.dispatch('/api/preview', body)
        self.assertEqual(database_hash(self.db), before)
        second = app.dispatch('/api/preview', body | {'previous_token': first['token']})
        with self.assertRaisesRegex(ValueError, 'Preview expired'):
            app.dispatch('/api/save', {'token': first['token']})
        app.dispatch('/api/cancel', {'token': second['token']})
        with self.assertRaisesRegex(ValueError, 'Preview expired'):
            app.dispatch('/api/save', {'token': second['token']})
        self.assertEqual(database_hash(self.db), before)
        third = app.dispatch('/api/preview', body)
        app.dispatch('/api/save', {'token': third['token'], 'name': 'Unreviewed client substitution'})
        self.assertEqual(a.detail(self.db, self.rev, self.oid)['option']['name'], body['name'])
        with self.assertRaisesRegex(ValueError, 'Preview expired'):
            app.dispatch('/api/save', {'token': third['token']})

    def test_saved_name_price_history_persist_and_affect_only_owned_option(self):
        before = a.detail(self.db, self.rev, self.oid)
        other = [tuple(r) for r in self.db.execute('SELECT * FROM option WHERE revision_id<>?', (self.rev,))]
        old_cat = ConsumerCatalog(self.db, self.rev)
        change = self.change(name='First aid kit — authoring check', price='1234.56', reason='Evidence-backed local review')
        saved = a.save(self.db, change)
        self.assertEqual(saved['edit_version'], before['edit_version'] + 1)
        self.assertEqual(saved['history'][0]['after'], change['after'])
        self.assertEqual(saved['history'][0]['before'], change['before'])
        self.assertEqual(saved['evidence'], before['evidence'])
        self.assertEqual(saved['contextual_rates'], before['contextual_rates'])
        self.assertEqual([tuple(r) for r in self.db.execute('SELECT * FROM option WHERE revision_id<>?', (self.rev,))], other)
        with closing(a.open_workspace(self.path)) as reopened:
            self.assertEqual(a.detail(reopened, self.rev, self.oid)['history'], saved['history'])
            new_cat = ConsumerCatalog(reopened, self.rev)
        self.assertEqual(new_cat.option(self.oid)['label'], change['after']['name'])
        self.assertEqual(new_cat.contract()['options'][self.oid]['name'], change['after']['name'])
        for scope in saved['configurations']:
            cfg = scope['id']
            old = old_cat.ev.transition(old_cat.ev.state(cfg), 'select', self.oid)
            new = new_cat.ev.transition(new_cat.ev.state(cfg), 'select', self.oid)
            self.assertEqual(old.resolved, new.resolved)
            self.assertEqual(old.installed, new.installed)
            self.assertEqual(new.total_minor - old.total_minor,
                             change['after']['purchase_amount_minor'] - change['before']['purchase_amount_minor'])
            charge, = [c for c in new_cat.project(new, 'local-authoring')['charges'] if c['owner_id'] == self.oid]
            self.assertEqual(charge['label'], change['after']['name'])
            self.assertEqual(charge['amount_minor'], 123456)

    def test_stale_same_row_other_row_and_raw_mapping_change_refused(self):
        pending = self.change(price='1000.00')
        with closing(a.open_workspace(self.path)) as other:
            a.save(other, self.change(name='First editor saves'))
        with self.assertRaisesRegex(ValueError, 'Stale edit'):
            a.save(self.db, pending)
        # A different option in the same revision still invalidates the reviewed version.
        pending = self.change()
        oid, = self.db.execute('SELECT id FROM option WHERE revision_id=? AND id<>? LIMIT 1', (self.rev,self.oid)).fetchone()
        a.save(self.db, self.change(option=oid))
        with self.assertRaisesRegex(ValueError, 'Stale edit'):
            a.save(self.db, pending)
        pending = self.change()
        self.db.execute("UPDATE consumer_option SET source_locator=source_locator || '/changed' WHERE revision_id=? AND option_id=?", (self.rev,self.oid))
        self.db.commit()
        with self.assertRaisesRegex(ValueError, 'Stale edit'):
            a.save(self.db, pending)

    def test_validation_failure_rolls_back_option_mapping_version_and_history(self):
        before = database_hash(self.db)
        change = self.change()
        with patch('catalog.authoring.validate_mappings', side_effect=ValueError('failed validation')):
            with self.assertRaisesRegex(ValueError, 'failed validation'):
                a.save(self.db, change)
        self.assertEqual(database_hash(self.db), before)

    def test_money_and_no_separate_charge_semantics(self):
        for bad in ('1.001', '-1', 'NaN', '1e3', '', '1,000', '1000000000', 1, None):
            with self.subTest(price=bad), self.assertRaises(ValueError):
                self.change(price=bad)
        for bad in ('', ' ', None, 'x' * 2049):
            with self.subTest(name=bad), self.assertRaises(ValueError):
                self.change(name=bad)
        with self.assertRaisesRegex(ValueError, 'reason'):
            self.change(reason=' ')
        nocharge, = self.db.execute("SELECT id FROM option WHERE revision_id=? AND charge_mode='no_separate_charge' LIMIT 1", (self.rev,)).fetchone()
        with self.assertRaisesRegex(ValueError, 'no editable base'):
            self.change(option=nocharge, price='0')
        saved = a.save(self.db, self.change(option=nocharge))
        self.assertIsNone(saved['option']['purchase_amount_minor'])
        self.assertIsNone(saved['option']['basis_id'])
        saved = a.save(self.db, self.change(price='0'))
        self.assertEqual(saved['option']['purchase_amount_minor'], 0)
        self.assertEqual(saved['option']['charge_mode'], 'priced')
        self.assertIsNotNone(saved['option']['basis_id'])

    def test_all_models_keep_scoped_identity_and_mapping(self):
        for revision in self.revisions.values():
            oid, = self.db.execute("SELECT id FROM option WHERE revision_id=? AND rpo='UVB'", (revision,)).fetchone()
            saved = a.save(self.db, self.change(revision=revision, option=oid))
            self.assertEqual(saved['option']['revision_id'], revision)
            self.assertEqual(ConsumerCatalog(self.db, revision).option(oid)['label'], saved['option']['name'])
        self.assertEqual(self.db.execute('SELECT count(*) FROM authoring_change').fetchone()[0], 6)


if __name__ == '__main__':
    unittest.main()
