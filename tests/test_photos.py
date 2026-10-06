"""Option photos found by the existing form's file-name rules."""
import json
import unittest

from catalog import foundation as f
from catalog.photos import INDEX, LANES, PATH_FILTER, Media, targets

SITE = 'https://stingraychevroletcorvette.com' + PATH_FILTER


class PhotoRuleTests(unittest.TestCase):
    def test_rules_follow_the_existing_sync_order(self):
        media = Media([SITE + p for p in (
            'lpo/h-vk3.png', 'ext/r-s-etv.jpg', 'ext/e-g-h-r-s-etv.jpg', 'ext/e-cfl.png', 'ext/cf8.png',
            'imgi_4_c-abc-2.png', 'x/c-dup.png', 'y/c-dup.jpg', 'z/r-s-tie.png', 'z/h-r-tie.png')])
        def url(model, rpo):
            found, rule, _ = media.resolve(model, rpo)
            return found and found.removeprefix(SITE), rule
        self.assertEqual(url('z06', 'VK3'), ('lpo/h-vk3.png', 'own'))
        self.assertEqual(url('zr1', 'VK3'), ('lpo/h-vk3.png', 'fallback:z06'))
        self.assertEqual(url('stingray', 'VK3'), (None, None))  # Stingray does not fall back to Z06
        self.assertEqual(url('zr1x', 'ETV'), ('ext/r-s-etv.jpg', 'shared'))  # the smallest group wins
        self.assertEqual(url('z06', 'ETV'), ('ext/e-g-h-r-s-etv.jpg', 'shared'))
        self.assertEqual(url('grand_sport_x', 'CFL'), ('ext/e-cfl.png', 'fallback:grand_sport'))
        self.assertEqual(url('z06', 'CFL'), (None, None))
        self.assertEqual(url('zr1x', 'CF8'), ('ext/cf8.png', 'bare'))
        self.assertEqual(url('stingray', 'ABC'), ('imgi_4_c-abc-2.png', 'own'))
        self.assertEqual(url('stingray', 'DUP'), (None, 'own'))  # two files at one rule: neither
        self.assertEqual(url('zr1', 'TIE'), (None, 'shared'))

    def test_index_only_adds_photos_where_the_baseline_has_none(self):
        index = json.loads(INDEX.read_text())
        wanted = targets()
        self.assertEqual(set(index['models']) - set(LANES), set())
        for model, photos in index['models'].items():
            for rpo, photo in photos.items():
                self.assertIn(rpo, wanted[model], (model, rpo))
                self.assertTrue(photo['image_url'].startswith(SITE), (model, rpo))
        # Every baseline-photographed RPO is excluded, whichever row carries the photo.
        rows = json.loads((f.ROOT / 'docs/z06-structured-records.json').read_text())['baseline_rows']
        options = {r['option_id']: r['rpo'] for r in rows['z06_options']}
        photographed = {options[r['target_id']] for r in rows['asset_map']
                        if r['target_type'] == 'option' and r.get('image_url') and r['target_id'] in options}
        self.assertFalse(photographed & set(wanted['z06']))


if __name__ == '__main__':
    unittest.main()
