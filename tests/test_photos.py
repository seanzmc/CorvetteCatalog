"""Option photos found by the existing form's file-name rules."""
import json
import unittest

from catalog import foundation as f
from catalog.photos import INDEX, LANES, PATH_FILTER, Media, list_sftp, targets

SITE = 'https://stingraychevroletcorvette.com' + PATH_FILTER


class PhotoRuleTests(unittest.TestCase):
    def test_reported_beta_images_are_bundled_for_each_applicable_model(self):
        web = f.ROOT / 'catalog/web'
        corrections = json.loads((web / 'photos/corrections.json').read_text())['models']
        common = set('379 3A9 3F9 3M9 3N9 719 5JS DPB DPC DPG DPL DPT DTC DUE DUK NWI R88 V8X WKR ZZ3'.split())
        self.assertEqual(set(corrections), set(LANES))
        files = set()
        for model, photos in corrections.items():
            self.assertTrue(common <= photos.keys(), model)
            for code, photo in photos.items():
                path = web / photo['image_url']
                self.assertTrue(path.resolve().is_relative_to((web / 'photos/cards').resolve()))
                raw = path.read_bytes()
                self.assertTrue(raw.startswith((b'\xff\xd8\xff', b'\x89PNG\r\n\x1a\n')), (model, code))
                self.assertEqual(photo['image_fit'], 'contain')  # keep the full stripe/roof illustration visible
                files.add(path)
        self.assertEqual(files, set((web / 'photos/cards').iterdir()), 'no unused bundled images')
        for model in ('zr1', 'zr1x'):
            self.assertIn('PBC', corrections[model])
            self.assertIn('VWT', corrections[model])
        for model in ('grand_sport', 'grand_sport_x', 'z06'):
            self.assertIn('EDU', corrections[model])
            self.assertIn('CM9', corrections[model])
        self.assertIn('SL9', corrections['grand_sport_x'])
        self.assertFalse(any('SL9' in photos for model, photos in corrections.items() if model != 'grand_sport_x'))

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

    def test_sftp_listing_keeps_original_images_only(self):
        tree = {
            'wp-content/uploads/pictures': [('d', 'wp-content/uploads/pictures/27vette'), ('-', 'wp-content/uploads/pictures/x.jpg')],
            'wp-content/uploads/pictures/27vette': [
                ('d', 'wp-content/uploads/pictures/27vette/stripes'), ('-', 'wp-content/uploads/pictures/27vette/.'),
                ('-', 'wp-content/uploads/pictures/27vette/h-vk3.png'),
                ('-', 'wp-content/uploads/pictures/27vette/h-vk3-300x200.png'),
                ('-', 'wp-content/uploads/pictures/27vette/big-scaled.jpg'),
                ('-', 'wp-content/uploads/pictures/27vette/.rpmcreated')],
            'wp-content/uploads/pictures/27vette/stripes': [('-', 'wp-content/uploads/pictures/27vette/stripes/dsy.jpg')],
        }
        def run(target, commands):
            out = []
            for command in commands:
                folder = command.split('"')[1]
                out.append(f'sftp> {command}')
                out += [f'{kind}rwxr-xr-x 1 u g 10 Oct 6 12:00 {name}' for kind, name in tree[folder]]
            return '\n'.join(out)
        self.assertEqual(list_sftp('login', run), [
            'https://stingraychevroletcorvette.com/wp-content/uploads/pictures/27vette/h-vk3.png',
            'https://stingraychevroletcorvette.com/wp-content/uploads/pictures/27vette/stripes/dsy.jpg',
            'https://stingraychevroletcorvette.com/wp-content/uploads/pictures/x.jpg'])

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
