"""Static bundle for running the customer form in the browser."""
from contextlib import closing
import gzip
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from catalog import foundation as f, static_bundle as sb
from catalog.behavior_sources import import_behavior
from catalog.consumers import ConsumerCatalog, ConsumerSession, encode, import_mappings
from catalog.releases import ReleaseStore, database_hash

ROOT = Path(__file__).resolve().parents[1]


class StaticBundleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = tempfile.TemporaryDirectory()
        with closing(f.connect(':memory:')) as db:
            f.create_schema(db); import_behavior(db); import_mappings(db)
            cls.store = ReleaseStore(Path(cls.root.name) / 'releases')
            # Bundling is under test; the six-model audit is covered by the release tests.
            with patch('catalog.releases.validate_semantics', return_value={'test_fixture': True}):
                cls.release = cls.store.complete(cls.store.freeze(db, database_hash(db)))
        cls.bundle = sb.build(cls.store, cls.release, Path(cls.root.name) / 'bundle')
        cls.description = sb.verify(cls.bundle)

    @classmethod
    def tearDownClass(cls):
        cls.root.cleanup()

    def test_bundle_holds_each_model_small_and_the_release_identity(self):
        d = self.description
        self.assertEqual((d['release_id'], d['pyodide']), (self.release, sb.PYODIDE_VERSION))
        self.assertEqual([m['model_key'] for m in d['models']],
                         ['stingray', 'grand_sport', 'grand_sport_x', 'z06', 'zr1', 'zr1x'])
        for model in d['models']:
            size = (self.bundle / model['catalog']).stat().st_size
            self.assertLess(size, 1_000_000, model['model_key'])
        # No provenance tables travel to the browser.
        tables = {t for m in d['models'] for t in m['tables']}
        self.assertFalse({t for t in tables if 'translation' in t or 'evidence' in t or 'source_' in t})
        self.assertTrue(all((self.bundle / p).exists() for p in d['engine']))
        self.assertTrue(any(p.startswith('artwork/') and p.endswith('.webp') for p in d['files']))

    def test_trimmed_model_plays_a_build_exactly_like_the_release(self):
        model = next(m for m in self.description['models'] if m['model_key'] == 'z06')
        manifest = json.loads((self.bundle / self.description['artwork_manifest']).read_text())
        small = sqlite3.connect(':memory:'); small.row_factory = sqlite3.Row
        raw = gzip.decompress((self.bundle / model['catalog']).read_bytes())
        with tempfile.NamedTemporaryFile(suffix='.sqlite') as file:
            file.write(raw); file.flush()
            with closing(sqlite3.connect(file.name)) as disk:
                disk.backup(small)
        full_db = f.connect(':memory:')
        with closing(sqlite3.connect((self.store.completed / self.release / 'catalog.sqlite').as_uri() + '?mode=ro', uri=True)) as source:
            source.backup(full_db)
        full = ConsumerCatalog(full_db, model['revision_id'], artwork_manifest=manifest)
        trimmed = ConsumerCatalog(small, model['revision_id'], artwork_manifest=manifest)
        def play(catalog):
            session, out = ConsumerSession(catalog, '3lz_h07', 'r'), []
            for oid in sorted(o for o, v in catalog.ev.options.items() if v['lifecycle'] == 'active')[:25]:
                action = 'remove' if oid in session._session.state.resolved else 'select'
                try:
                    p = session.preview(action, oid, session.version)
                except ValueError as error:
                    out.append(str(error)); continue
                session.confirm(p['token'], p['warning_sha256'], session.version)
                out.append(encode(dict(p['warning'], cards=catalog.cards(session._session.state))))
            return out
        self.assertEqual(play(trimmed), play(full))

    def test_rebuild_is_identical_and_tampering_is_caught(self):
        again = sb.build(self.store, self.release, Path(self.root.name) / 'again')
        self.assertEqual(sb.verify(again)['files'], self.description['files'])
        # Only the root bundle.json is exempt from the file list.
        (again / 'artwork/bundle.json').write_text('{}')
        with self.assertRaisesRegex(ValueError, 'altered or unexpected'):
            sb.verify(again)
        (again / 'artwork/bundle.json').unlink()
        (again / 'engine/link.py').symlink_to(again / 'engine/catalog/evaluator.py')
        with self.assertRaisesRegex(ValueError, 'symbolic links'):
            sb.verify(again)
        (again / 'engine/link.py').unlink()
        self.assertEqual(sb.verify(again)['files'], self.description['files'])
        (again / 'engine/catalog/evaluator.py').write_text('# altered\n')
        with self.assertRaisesRegex(ValueError, 'altered or unexpected'):
            sb.verify(again)
        with self.assertRaisesRegex(ValueError, 'already exists'):
            sb.build(self.store, self.release, again)

    def test_engine_list_is_the_import_closure_of_the_form_engine(self):
        code = "import sys; import catalog.consumers; print(sorted(m.split('.', 1)[1] if '.' in m else '__init__' for m in sys.modules if m == 'catalog' or m.startswith('catalog.')))"
        out = subprocess.run([sys.executable, '-c', code], cwd=ROOT, capture_output=True, text=True, check=True).stdout
        self.assertEqual(json.loads(out.replace("'", '"')), sorted(sb.ENGINE))


if __name__ == '__main__':
    unittest.main()
