"""One-command preview selection and fresh-build orchestration."""
from contextlib import closing
from pathlib import Path
import json
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from scripts import preview


class PreviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.local = self.root / '.local'
        self.bundle = self.local / 'existing/completed' / ('a' * 64)
        self.bundle.mkdir(parents=True)
        self.source = self.root / 'source.json'
        self.source.write_text('{"price":60}')
        self.runtime = {'catalog/evaluator.py': 'current-code'}
        self.manifest = {'runtime': self.runtime, 'freeze': {}}
        (self.bundle / 'manifest.json').write_text(json.dumps(self.manifest))
        self.validation = {
            'translation': 'complete_pinned_replay',
            'semantic': {key: {'findings': []} for key in preview.MODEL_KEYS},
        }
        self.write_validation()
        with closing(sqlite3.connect(self.bundle / 'catalog.sqlite')) as db, db:
            db.execute('CREATE TABLE source_document(source_path,content_sha256)')
            db.execute('INSERT INTO source_document VALUES (?,?)', ('source.json', preview.file_hash(self.source)))
        self.root_patch = patch.object(preview, 'ROOT', self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)

    def write_validation(self):
        (self.bundle / 'validation.json').write_text(json.dumps(self.validation))

    def matches(self):
        return preview.matches_checkout(self.bundle, self.manifest, self.runtime)

    def test_source_and_runtime_changes_invalidate_reuse(self):
        self.assertTrue(self.matches())
        self.source.write_text('{"price":61}')
        self.assertFalse(self.matches())
        self.source.write_text('{"price":60}')
        self.assertFalse(preview.matches_checkout(self.bundle, self.manifest, {'catalog/evaluator.py': 'new-code'}))
        self.source.unlink()
        self.assertFalse(self.matches())

    def test_authored_release_is_not_the_checked_in_catalog(self):
        self.manifest['freeze']['reviewed_edits_sha256'] = 'authored'
        self.assertFalse(self.matches())

    def test_mocked_or_incomplete_audit_is_not_reused(self):
        for semantic in ({'test_fixture': True}, {}, {key: {'findings': ['failure']} for key in preview.MODEL_KEYS}):
            with self.subTest(semantic=semantic):
                self.validation['semantic'] = semantic
                self.write_validation()
                self.assertFalse(self.matches())

    def test_existing_candidate_must_pass_bundle_verification(self):
        with patch.object(preview, 'pins', return_value=self.runtime), patch.object(preview, 'ReleaseStore') as factory:
            store = factory.return_value
            self.assertEqual(preview.find_release(self.local), (store, self.bundle.name))
            store.verify.assert_called_once_with(self.bundle.name)
            store.verify.side_effect = ValueError('Corrupt image')
            self.assertIsNone(preview.find_release(self.local))

    def test_fresh_build_uses_release_pipeline_and_cleans_temporary_draft(self):
        # Exercise orchestration only; the unchanged full audit is not mocked as
        # passing qualification or made available for reuse by this test.
        with patch.object(preview, 'ReleaseStore') as factory, \
                patch.object(preview.f, 'create_schema'), \
                patch.object(preview, 'import_behavior'), \
                patch.object(preview, 'import_mappings'), \
                patch.object(preview, 'database_hash', return_value='exact-draft-digest'):
            store = factory.return_value
            store.root = self.local / 'preview/releases'
            store.root.mkdir(parents=True)
            store.freeze.return_value = 'frozen-id'
            store.complete.return_value = 'release-id'
            self.assertEqual(preview.build_release(self.local), (store, 'release-id'))
            self.assertEqual(store.freeze.call_args.args[1], 'exact-draft-digest')
            store.complete.assert_called_once_with('frozen-id')
            self.assertEqual(list(store.root.iterdir()), [])
            store.complete.reset_mock()
            store.freeze.side_effect = ValueError('Audit failed')
            with self.assertRaisesRegex(ValueError, 'Audit failed'):
                preview.build_release(self.local)
            store.complete.assert_not_called()
            self.assertEqual(list(store.root.iterdir()), [])

    def test_occupied_port_exits_before_preparing_any_catalog(self):
        with patch('sys.argv', ['preview.py', '--no-browser']), \
                patch.object(preview, 'HTTPServer', side_effect=OSError('Address in use')), \
                patch.object(preview, 'find_release') as find, \
                patch.object(preview, 'build_release') as build:
            with self.assertRaises(SystemExit) as result:
                preview.main()
            self.assertEqual(result.exception.code, 1)
            find.assert_not_called()
            build.assert_not_called()


if __name__ == '__main__':
    unittest.main()
