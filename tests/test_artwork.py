"""Confirmed-state artwork ownership, complete release packaging and recovery."""
import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import test_consumers as base
from catalog import artwork
from catalog.consumers import ConsumerCatalog, ConsumerSession, digest
from catalog.consumer_server import Application, handler
from catalog.releases import ReleaseStore, database_hash, write_json


class ArtworkTests(unittest.TestCase):
    setUpClass = classmethod(base.ConsumerTests.setUpClass.__func__)
    tearDownClass = classmethod(base.ConsumerTests.tearDownClass.__func__)
    commit = base.ConsumerTests.commit

    def session(self, cfg='3lt_e07', paint='opt_gba_001', key='grand_sport'):
        s = ConsumerSession(self.catalogs[key], cfg, 'test-release')
        self.commit(s, 'select', paint)
        return s

    def test_exact_native_asset_hashes_and_evidence_are_required(self):
        manifest = artwork.load()
        self.assertEqual(len(manifest['assets']), 22)
        for asset in manifest['assets']:
            self.assertEqual((asset['width'], asset['height']), (1500, 844))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'artwork'; shutil.copytree(artwork.ROOT, root)
            for name in ('proof-base.webp', 'source-proof.json'):
                path = root / name; before = path.read_bytes(); path.write_bytes(before+b'altered')
                with self.assertRaisesRegex(ValueError, 'altered'): artwork.load(root)
                path.write_bytes(before)
            for mutation in ('scope', 'trim', 'binding', 'paint', 'order', 'path'):
                changed = copy.deepcopy(manifest)
                if mutation == 'scope': changed['model_key'] = 'z06'
                elif mutation == 'trim': changed['trim'] = '1lt'
                elif mutation == 'binding': changed['choices'][0]['option_id'] = 'opt_5zv_001'
                elif mutation == 'paint': changed['paints'][1]['base_asset_id'] = changed['paints'][0]['base_asset_id']
                elif mutation == 'order': changed['assets'][0]['stack_order'] = 40
                else: changed['assets'][0]['file'] = '../proof-base.webp'
                write_json(root / 'manifest.json', changed)
                with self.subTest(mutation=mutation), self.assertRaises(ValueError): artwork.load(root)

    def test_foreign_model_body_trim_and_missing_choice_have_no_art(self):
        cases = [('grand_sport','3lt_e67','opt_gba_001'), ('grand_sport','1lt_e07','opt_gba_001'),
                 ('stingray','3lt_c07','opt_gba_001'),
                 ('grand_sport_x','3lt_g07','opt_gba_001'), ('z06','3lz_h07','opt_gba_001')]
        for key, cfg, paint in cases:
            with self.subTest(model=key, cfg=cfg, paint=paint):
                s = self.session(cfg, paint, key)
                # This option is unavailable on Stingray; GSX and Z06 are the
                # positive same-ID/RPO cases that must not borrow Grand Sport art.
                if key != 'stingray': self.commit(s, 'select', 'opt_5zv_001')
                self.assertEqual(s.current()['build']['visualizer']['assets'], [])
        self.assertEqual(self.session().current()['build']['visualizer']['assets'], [])

    def test_all_twenty_native_paint_and_spoiler_combinations(self):
        manifest = artwork.load()
        for choice in manifest['choices']:
            s = self.session()
            if choice['rpo'] == 'T0F':
                for oid in ('opt_feb_001', 'opt_j57_001'): self.commit(s, 'select', oid)
            self.commit(s, 'select', choice['option_id'])
            for paint in manifest['paints']:
                with self.subTest(paint=paint['rpo'], spoiler=choice['rpo']):
                    self.commit(s, 'select', paint['option_id'])
                    view = s.current()['build']['visualizer']
                    self.assertEqual(view['paint_rpo'], paint['rpo'])
                    self.assertEqual(view['rpo'], choice['rpo'])
                    self.assertEqual([a['id'] for a in view['assets']],
                        [paint['base_asset_id'], choice['asset_id'], paint['foreground_asset_id']])

    def test_cancel_confirm_and_revert_preserve_the_confirmed_spoiler(self):
        s = self.session()
        self.commit(s, 'interior', '3LT_AH2_EJH')
        for oid in ('opt_feb_001', 'opt_j57_001', 'opt_t0f_001'): self.commit(s, 'select', oid)
        before = s.current()['build']['visualizer']
        self.assertEqual(before['rpo'], 'T0F')
        self.assertEqual([a['stack_order'] for a in before['assets']], [0, 20, 30])
        self.assertEqual(before['release_id'], 'test-release')
        p = s.preview('select', 'opt_5zv_001', s.version)
        self.assertEqual(p['warning']['candidate']['visualizer']['rpo'], '5ZV')
        self.assertEqual(s.current()['build']['visualizer'], before)
        s.cancel(s.version)
        self.assertEqual(s.current()['build']['visualizer'], before)
        self.commit(s, 'select', 'opt_5zv_001')
        after = s.current()['build']['visualizer']
        self.assertEqual(after['rpo'], '5ZV')
        self.assertEqual(after['assets'][0], before['assets'][0])
        self.assertEqual(after['assets'][2], before['assets'][2])
        self.assertNotEqual(after['assets'][1], before['assets'][1])
        self.commit(s, 'revert')
        self.assertEqual(s.current()['build']['visualizer'], before)
        self.commit(s, 'select', 'opt_g8g_001')
        white = s.current()['build']['visualizer']
        self.assertEqual(white['paint_rpo'], 'G8G')
        self.assertNotEqual(white['assets'][0], before['assets'][0])
        self.assertEqual(white['assets'][1], before['assets'][1])
        self.assertNotEqual(white['assets'][2], before['assets'][2])

    def test_edited_catalog_identity_cannot_reuse_stale_art(self):
        c = self.catalogs['grand_sport']; original = c.ev.options['opt_t0f_001']
        try:
            c.ev.options['opt_t0f_001'] = dict(original, rpo='CHANGED')
            result = artwork.catalog_contract(c, artwork.load())
            self.assertEqual(result['coverage'], 'art_not_available')
            self.assertEqual(result['assets'], [])
        finally:
            c.ev.options['opt_t0f_001'] = original

    def test_release_restores_art_and_rejects_rehashed_binding_declarations(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); store = ReleaseStore(root / 'store')
            with patch('catalog.releases.validate_semantics', return_value={'test_fixture':True}):
                frozen = store.freeze(self.db, database_hash(self.db))
            release = store.complete(frozen); manifest = store.verify(release)
            self.assertEqual(len(manifest['media']['assets']), 22)
            self.assertIn('runtime/catalog/web/artwork/source-proof.json', manifest['artifacts'])
            self.assertEqual(store.complete(frozen), release)
            backup = root / 'backup'; store.backup(release, backup)
            recovered = ReleaseStore(root / 'recovered'); self.assertEqual(recovered.restore(backup), release)
            self.assertEqual(recovered.verify(release), manifest)
            # A running release must not pick up a later checkout's artwork.
            app = Application(recovered, release)
            relative = Path(manifest['media']['assets'][0]['path']).relative_to('runtime/catalog/web/artwork')
            expected = (recovered.completed / release / manifest['media']['assets'][0]['path']).read_bytes()
            checkout = root / 'changed-checkout'
            (checkout / relative).parent.mkdir(parents=True)
            (checkout / relative).write_bytes(b'later checkout artwork')
            request = object.__new__(handler(app)); request.allowed = lambda: True
            sent = []; request.send = lambda *args: sent.append(args)
            request.path = '/artwork/' + relative.as_posix()
            with patch.object(artwork, 'ROOT', checkout):
                request.do_GET()
            self.assertEqual(sent, [(200, expected, 'image/webp')])
            package = store.completed / release
            changed = copy.deepcopy(manifest); changed['media']['assets'] = []
            changed_id = digest(changed); package.rename(store.completed / changed_id)
            write_json(store.completed / changed_id / 'manifest.json', changed)
            with self.assertRaisesRegex(ValueError, 'artwork declaration'): store.verify(changed_id)
            # A fresh recovery remains usable after the corrupt declaration.
            self.assertEqual(recovered.verify(release), manifest)
            asset = backup / manifest['media']['assets'][0]['path']; asset.write_bytes(b'corrupt')
            with self.assertRaisesRegex(ValueError, 'altered'): recovered.restore(backup)


if __name__ == '__main__':
    unittest.main()
