"""Deploy packages, one-step publish, channel serving and draft previews."""
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch
from urllib.request import urlopen

from catalog import deploy, foundation as f
from catalog.behavior_sources import import_behavior
from catalog.consumers import import_mappings
from catalog.releases import ReleaseStore, database_hash

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import preview  # noqa: E402


class DeployTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = tempfile.TemporaryDirectory()
        cls.db = f.connect(':memory:')
        f.create_schema(cls.db); import_behavior(cls.db); import_mappings(cls.db)
        cls.digest = database_hash(cls.db)
        cls.store = ReleaseStore(Path(cls.root.name) / 'releases')
        # Packaging is under test; the six-model audit is covered by the release tests.
        with patch('catalog.releases.validate_semantics', return_value={'test_fixture': True}):
            cls.release = cls.store.complete(cls.store.freeze(cls.db, cls.digest))

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        cls.root.cleanup()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.deploy = Path(self.tmp.name) / 'deploy'

    def test_package_is_verified_reused_and_runs_on_its_pinned_code(self):
        folder = deploy.package(self.store, self.release, self.deploy / self.release)
        self.assertIn(f'--release {self.release}', (folder / 'start.sh').read_text())
        self.assertIn('FROM python:3.12-slim', (folder / 'Dockerfile').read_text())
        self.assertEqual(deploy.package(self.store, self.release, folder), folder)
        # The packaged store alone serves the release on the code pinned in it.
        with socket.socket() as probe:
            probe.bind(('127.0.0.1', 0)); port = probe.getsockname()[1]
        runtime = (folder / 'store/completed' / self.release / 'runtime').resolve()
        env = dict(os.environ, PYTHONPATH=str(runtime), PYTHONDONTWRITEBYTECODE='1')
        server = subprocess.Popen([sys.executable, '-P', '-m', 'catalog.consumer_server', '--store', str(folder / 'store'),
                                   '--release', self.release, '--port', str(port)],
                                  cwd=self.tmp.name, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        self.addCleanup(server.wait)
        self.addCleanup(server.terminate)
        for _ in range(120):
            try:
                with urlopen(f'http://127.0.0.1:{port}/healthz', timeout=2) as response:
                    self.assertEqual(json.loads(response.read())['release_id'], self.release)
                    break
            except OSError:
                if server.poll() is not None:
                    self.fail(server.stderr.read().decode())
                time.sleep(0.5)
        else:
            self.fail('Packaged server did not start')
        # Tampering with a reused package is refused, not overwritten.
        (folder / 'start.sh').write_text('#!/bin/sh\nexec true\n')
        with self.assertRaisesRegex(ValueError, 'start.sh differs'):
            deploy.package(self.store, self.release, folder)

    def test_start_script_requires_the_public_origin(self):
        folder = deploy.package(self.store, self.release, self.deploy / self.release)
        env = {k: v for k, v in os.environ.items() if k != 'CATALOG_ORIGIN'}
        result = subprocess.run(['sh', str(folder / 'start.sh')], env=env, capture_output=True, text=True, timeout=30)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Set CATALOG_ORIGIN', result.stderr)

    def test_publish_packages_first_and_uses_compare_and_swap(self):
        version = self.store.pointer(deploy.CHANNEL)['version']
        with self.assertRaisesRegex(ValueError, 'Stale publication pointer'):
            deploy.publish(self.store, self.release, version + 5, self.deploy)
        self.assertEqual(self.store.pointer(deploy.CHANNEL)['version'], version)
        result = deploy.publish(self.store, self.release, version, self.deploy)
        self.assertEqual(result['pointer'], dict(release_id=self.release, version=version + 1))
        self.assertTrue((Path(result['package']) / 'Dockerfile').exists())
        # A package failure leaves production where it was.
        with patch.object(deploy, 'package', side_effect=OSError('disk full')):
            with self.assertRaises(OSError):
                deploy.publish(self.store, self.release, version + 1, self.deploy)
        self.assertEqual(self.store.pointer(deploy.CHANNEL)['version'], version + 1)

    def test_ship_releases_publishes_and_packages_an_accepted_draft(self):
        database = Path(self.tmp.name) / 'draft.sqlite'
        built = dict(release_id=self.release, store=str(self.store.root))
        with patch('catalog.deploy.authoring.open_workspace', return_value=self.db_copy()), \
                patch('catalog.authoring_server.build_release', return_value=built) as build:
            result = deploy.ship(database, 'backups')
        build.assert_called_once_with(database, self.digest, 'backups')
        self.assertEqual(result['pointer']['release_id'], self.release)
        self.assertEqual(Path(result['package']), Path(self.tmp.name).resolve() / 'deploy' / self.release)

    def test_channel_serving_needs_a_published_release(self):
        empty = Path(self.tmp.name) / 'empty-store'
        result = subprocess.run([sys.executable, '-m', 'catalog.consumer_server', '--store', str(empty), '--channel', 'production'],
                                cwd=ROOT, capture_output=True, text=True, timeout=60)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Nothing is published to the production channel', result.stderr)

    def test_draft_preview_reuses_the_release_of_that_exact_draft(self):
        with patch('preview.authoring.open_workspace', side_effect=lambda path: self.db_copy()), \
                patch('preview.ReleaseStore', return_value=self.store):
            self.assertEqual(preview.draft_release(Path(self.tmp.name) / 'draft.sqlite'), (self.store, self.release))

    def db_copy(self):
        copy = f.connect(':memory:')
        self.db.backup(copy)
        return copy


if __name__ == '__main__':
    unittest.main()
