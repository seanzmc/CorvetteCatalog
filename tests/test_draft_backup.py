"""Draft backups: consistent compressed copies, retention, restore and editor hooks."""
from contextlib import closing, redirect_stderr
from datetime import datetime, timedelta, timezone
import gzip
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import test_authoring as base
from catalog import authoring as a, draft_backup as b
from catalog.authoring_server import Application, build_release
from catalog.releases import database_hash


class RetentionTests(unittest.TestCase):
    def test_keeps_recent_and_one_per_day(self):
        now = datetime(2026, 9, 24, 12, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as directory:
            names = []
            # 25 saves today, then three saves on each of the previous 40 days.
            stamps = [now - timedelta(minutes=m) for m in range(25)]
            stamps += [now - timedelta(days=d, hours=h) for d in range(1, 41) for h in (1, 2, 3)]
            for stamp in stamps:
                name = f'{b.PREFIX}{stamp.strftime("%Y%m%dT%H%M%S%fZ")}-{"0" * 16}{b.SUFFIX}'
                (Path(directory) / name).touch()
                names.append(name)
            b.prune(directory, now)
            kept = [p.name for p in b.backups(directory)]
        self.assertEqual(kept[:20], names[:20])
        # Today already has 20; days 1-29 keep their newest backup; older days go.
        self.assertEqual(kept[20:], [names[25 + 3 * (d - 1)] for d in range(1, 30)])


class DraftBackupTests(unittest.TestCase):
    setUpClass = classmethod(base.AuthoringTests.setUpClass.__func__)
    tearDownClass = classmethod(base.AuthoringTests.tearDownClass.__func__)

    def setUp(self):
        base.AuthoringTests.setUp(self)
        self.backups = Path(self.tmp.name) / 'backups'

    def save_name(self, app, name):
        data = a.detail(self.db, self.rev, self.oid)
        preview = app.dispatch('/api/preview', dict(revision_id=self.rev, option_id=self.oid, etag=data['etag'],
                                                     name=name, price='1234.56', reason='Backup test'))
        return app.dispatch('/api/save', {'token': preview['token']})

    def test_editor_backs_up_at_start_and_after_saves_then_restores(self):
        app = Application(self.path, self.backups)
        self.addCleanup(app.release_worker.shutdown)
        self.assertEqual(len(b.backups(self.backups)), 1)
        # Nothing changed, so a repeat snapshot is skipped.
        self.assertIsNone(b.snapshot(self.path, self.backups))
        saved = self.save_name(app, 'Backed up kit')
        self.assertTrue(saved['backup']['saved'])
        latest = b.backups(self.backups)[0]
        self.assertEqual(str(latest), saved['backup']['path'])
        self.assertEqual(len(b.backups(self.backups)), 2)

        restored = Path(self.tmp.name) / 'restored.sqlite'
        b.restore(latest, restored)
        with closing(a.open_workspace(restored)) as db:
            self.assertEqual(database_hash(db), database_hash(self.db))
            self.assertEqual(a.detail(db, self.rev, self.oid)['option']['name'], 'Backed up kit')
        with self.assertRaisesRegex(ValueError, 'already exists'):
            b.restore(latest, restored)

    def test_backup_failure_is_reported_without_undoing_the_save(self):
        app = Application(self.path, self.backups)
        self.addCleanup(app.release_worker.shutdown)
        blocked = Path(self.tmp.name) / 'not-a-directory'
        blocked.write_text('')
        app.backup_dir = blocked
        with redirect_stderr(io.StringIO()) as log:
            saved = self.save_name(app, 'Saved without backup')
        self.assertFalse(saved['backup']['saved'])
        self.assertIn('Draft backup failed', log.getvalue())
        self.assertEqual(a.detail(self.db, self.rev, self.oid)['option']['name'], 'Saved without backup')

    def test_unusable_backup_location_fails_at_startup(self):
        blocked = Path(self.tmp.name) / 'not-a-directory'
        blocked.write_text('')
        with self.assertRaises(OSError):
            Application(self.path, blocked)

    def test_corrupt_backup_is_refused(self):
        self.backups.mkdir()
        broken = self.backups / f'{b.PREFIX}20260924T120000000000Z-{"0" * 16}{b.SUFFIX}'
        with gzip.open(broken, 'wb') as out:
            out.write(b'not a sqlite database' * 100)
        destination = Path(self.tmp.name) / 'restored.sqlite'
        with self.assertRaises(Exception):
            b.restore(broken, destination)
        self.assertFalse(destination.exists())


class ReleaseBackupTests(unittest.TestCase):
    def test_created_release_is_copied_once_and_failures_are_reported(self):
        # The real freeze/complete path is covered by the release tests.
        with tempfile.TemporaryDirectory() as directory, \
                patch('catalog.authoring_server.authoring.open_workspace'), \
                patch('catalog.releases.ReleaseStore.freeze', return_value='frozen-id'), \
                patch('catalog.releases.ReleaseStore.complete', return_value='release-id'), \
                patch('catalog.releases.ReleaseStore.verify', return_value={'artifacts': {}}), \
                patch('catalog.releases.ReleaseStore.backup') as backup, \
                patch('catalog.releases.ReleaseStore._verify_path') as verify:
            database, backups = Path(directory) / 'draft.sqlite', Path(directory) / 'backups'
            destination = backups / 'releases' / 'release-id'
            backup.side_effect = lambda release, path: Path(path).mkdir(parents=True)
            self.assertEqual(build_release(database, 'etag', backups)['backup'], str(destination))
            verify.assert_not_called()
            # A rebuild verifies the existing copy instead of trusting or replacing it.
            self.assertEqual(build_release(database, 'etag', backups)['backup'], str(destination))
            backup.assert_called_once_with('release-id', destination)
            verify.assert_called_once_with(destination, 'release-id')
            verify.side_effect = ValueError('Missing, altered or unexpected release artifacts')
            damaged = build_release(database, 'etag', backups)
            self.assertNotIn('backup', damaged)
            self.assertIn('failed verification', damaged['backup_error'])
            backup.assert_called_once()
            self.assertNotIn('backup', build_release(database, 'etag'))
            backup.side_effect = OSError('disk full')
            result = build_release(database, 'etag', Path(directory) / 'other')
            self.assertEqual(result['backup_error'], 'disk full')
            self.assertEqual(result['release_id'], 'release-id')

    def test_empty_existing_release_copy_is_reported_not_trusted(self):
        with tempfile.TemporaryDirectory() as directory, \
                patch('catalog.authoring_server.authoring.open_workspace'), \
                patch('catalog.releases.ReleaseStore.freeze', return_value='frozen-id'), \
                patch('catalog.releases.ReleaseStore.complete', return_value='release-id'), \
                patch('catalog.releases.ReleaseStore.verify', return_value={'artifacts': {}}):
            backups = Path(directory) / 'backups'
            (backups / 'releases' / 'release-id').mkdir(parents=True)
            result = build_release(Path(directory) / 'draft.sqlite', 'etag', backups)
            self.assertIn('failed verification', result['backup_error'])
            self.assertEqual(list((backups / 'releases' / 'release-id').iterdir()), [])


if __name__ == '__main__':
    unittest.main()
