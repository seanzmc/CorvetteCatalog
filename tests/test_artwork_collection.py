"""Native ownership and exact model/body/paint selection across scene packages."""
import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest

import test_consumers as base
from catalog import artwork
from catalog.consumers import ConsumerSession
from catalog.releases import write_json


class CollectionTests(unittest.TestCase):
    setUpClass = classmethod(base.ConsumerTests.setUpClass.__func__)
    tearDownClass = classmethod(base.ConsumerTests.tearDownClass.__func__)
    commit = base.ConsumerTests.commit

    def test_every_native_combination_keeps_its_model_and_body_planes(self):
        count = 0
        for scene in artwork.load_collection():
            folder = scene.get('asset_prefix', '')
            proof = json.loads((artwork.ROOT / folder / 'source-proof.json').read_text())
            cat = self.catalogs[proof['catalogModelKey']]
            cfg, = [key for key, row in cat.ev.configs.items() if (row['body'], row['trim']) == (proof['body'], proof['trim'])]
            for paint in proof['paints']:
                choices = paint.get('choices', proof.get('choices', []))
                for choice in choices:
                    with self.subTest(model=cat.model_key, cfg=cfg, paint=paint['rpo'], spoiler=choice['rpo']):
                        session = ConsumerSession(cat, cfg, 'multi-model-test')
                        self.commit(session, 'select', paint['optionId'])
                        if cat.model_key == 'grand_sport' and choice['rpo'] == 'T0F':
                            for oid in ('opt_feb_001', 'opt_j57_001'): self.commit(session, 'select', oid)
                        self.commit(session, 'select', choice['optionId'])
                        view = session.current()['build']['visualizer']
                        self.assertEqual(view['scene_id'], proof['id'])
                        self.assertEqual(view['paint_rpo'], paint['rpo'])
                        self.assertEqual(view['option_id'], choice['optionId'])
                        native = [paint['back'], choice['webAsset'], paint['foreground']]
                        self.assertEqual([a['url'] for a in view['assets']],
                            ['/artwork/'+folder+Path(a['path']).name for a in native])
                        self.assertEqual([a['sha256'] for a in view['assets']], [a['sha256'] for a in native])
                        count += 1
        self.assertEqual(count, 96)

    def test_paint_specific_wing_changes_all_three_planes_after_confirmation(self):
        session = ConsumerSession(self.catalogs['stingray'], '3lt_c07', 'multi-model-test')
        for oid in ('opt_gba_001', 'opt_5zu_001'): self.commit(session, 'select', oid)
        before = session.current()['build']['visualizer']
        pending = session.preview('select', 'opt_g8g_001', session.version)
        self.assertEqual(session.current()['build']['visualizer'], before)
        session.cancel(session.version)
        self.assertEqual(session.current()['build']['visualizer'], before)
        self.commit(session, 'select', 'opt_g8g_001')
        after = session.current()['build']['visualizer']
        self.assertTrue(all(a['sha256'] != b['sha256'] for a, b in zip(before['assets'], after['assets'])))
        self.assertEqual(after['rpo'], '5ZU')
        self.commit(session, 'revert')
        self.assertEqual(session.current()['build']['visualizer'], before)

    def test_collection_rejects_paths_duplicates_overlap_and_false_paint_binding(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'artwork'; shutil.copytree(artwork.ROOT, root)
            original = json.loads((root / 'index.json').read_text())
            for folders in (['', '../outside'], ['', ''], ['', 'missing']):
                write_json(root / 'index.json', dict(original, scenes=folders))
                with self.subTest(folders=folders), self.assertRaises(ValueError): artwork.load_collection(root)
            shutil.copytree(root / 'stingray-coupe', root / 'duplicate')
            write_json(root / 'index.json', dict(original, scenes=original['scenes']+['duplicate']))
            with self.assertRaisesRegex(ValueError, 'Overlapping'): artwork.load_collection(root)
            write_json(root / 'index.json', original)
            manifest = root / 'stingray-coupe/manifest.json'; altered = json.loads(manifest.read_text())
            altered['choices'][0]['paint_rpo'] = 'G8G'; write_json(manifest, altered)
            with self.assertRaisesRegex(ValueError, 'binding mismatch'): artwork.load_collection(root)

    def test_one_stale_body_binding_does_not_borrow_or_hide_another_body(self):
        scenes = copy.deepcopy(artwork.load_collection())
        convertible = next(s for s in scenes if s['model_key']=='grand_sport' and s['body']=='convertible')
        convertible['choices'][0]['rpo'] = 'UNREVIEWED'
        cat = self.catalogs['grand_sport']; before = cat.artwork
        try:
            cat.artwork = artwork.catalog_contract(cat, scenes)
            for cfg, expected in [('3lt_e07', 'component_preview'), ('3lt_e67', 'art_not_available')]:
                session = ConsumerSession(cat, cfg, 'multi-model-test')
                for oid in ('opt_gba_001','opt_5zv_001'): self.commit(session, 'select', oid)
                self.assertEqual(session.current()['build']['visualizer']['coverage'], expected)
        finally:
            cat.artwork = before


if __name__ == '__main__': unittest.main()
