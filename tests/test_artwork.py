"""Confirmed-state artwork ownership, complete release packaging and recovery."""
import copy
from contextlib import contextmanager
from dataclasses import replace
import hashlib
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


@contextmanager
def no_spoiler_fixture(catalog):
    """Synthetic opt-in proof only; never qualify or edit the bundled artwork."""
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        scene_root = root / 'stingray-coupe'
        shutil.copytree(artwork.ROOT / 'stingray-coupe', scene_root)
        write_json(root / 'index.json', dict(format='catalog-artwork-collection-v1', scenes=['stingray-coupe']))
        manifest = artwork.load(scene_root)
        # The imported test baseline and pinned R3 have different retained IDs.
        # Resolve the actual fixture catalog's rear group, never borrow R3's ID.
        group, = [g for g in catalog.ev.rows['choice_group']
                  if {'opt_5zu_001', 'opt_t0a_001', 'opt_tvs_001'} <= catalog.ev.members[g['id']]]
        manifest['no_spoiler'] = dict(group_id=group['id'], excluded_option_ids=['opt_z51_001'])
        evidence_path = scene_root / manifest['evidence']['file']
        evidence = json.loads(evidence_path.read_text())
        evidence['no_spoiler'] = manifest['no_spoiler']
        write_json(evidence_path, evidence)
        manifest['evidence']['sha256'] = hashlib.sha256(evidence_path.read_bytes()).hexdigest()
        write_json(scene_root / 'manifest.json', manifest)
        yield root, artwork.load_collection(root)[0]


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
        cases = [('grand_sport','1lt_e67','opt_gba_001'), ('grand_sport','1lt_e07','opt_gba_001'),
                 ('stingray','1lt_c07','opt_gba_001'),
                 ('grand_sport_x','3lt_g07','opt_gba_001'), ('z06','1lz_h07','opt_gba_001')]
        for key, cfg, paint in cases:
            with self.subTest(model=key, cfg=cfg, paint=paint):
                s = self.session(cfg, paint, key)
                # GSX has the same ID/RPO but no source family. Lower trims must
                # not borrow the top-trim scene from their own model either.
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

    def test_declared_no_spoiler_uses_resolved_members_and_fixed_plane_exclusions(self):
        cat = copy.copy(self.catalogs['stingray'])
        with no_spoiler_fixture(cat) as (root, scene):
            cat.artwork = artwork.catalog_contract(cat, scene)
            session = ConsumerSession(cat, '3lt_c07', 'no-spoiler-test')
            self.commit(session, 'select', 'opt_gba_001')
            state = session._session.state
            view = session.current()['build']['visualizer']
            paint = next(p for p in scene['paints'] if p['rpo'] == 'GBA')
            self.assertEqual(view['coverage'], 'component_preview')
            self.assertEqual(view['label'], 'No rear spoiler')
            self.assertIsNone(view['option_id'])
            self.assertIsNone(view['rpo'])
            self.assertEqual([a['id'] for a in view['assets']], [paint['base_asset_id'], paint['foreground_asset_id']])
            self.assertEqual([a['stack_order'] for a in view['assets']], [0, 30])
            self.assertEqual([a['url'] for a in view['assets']],
                             ['/artwork/stingray-coupe/'+a['file'] for a in view['assets']])
            for asset in view['assets']:
                self.assertEqual(artwork.asset_path(asset['url'], root), root / 'stingray-coupe' / asset['file'])
            self.commit(session, 'select', 'opt_5zu_001')
            bound = artwork.project(cat, session._session.state)
            legacy = dict(scene); del legacy['no_spoiler']
            cat.artwork = artwork.catalog_contract(cat, legacy)
            self.assertEqual(bound, artwork.project(cat, session._session.state))
            self.assertEqual([a['stack_order'] for a in bound['assets']], [0, 20, 30])
            cat.artwork = artwork.catalog_contract(cat, scene)
            # Every rear group member counts, including unbound/paint-unmatched
            # choices; an invalid mixed state must not select just its bound wing.
            for extras in ({'opt_tvs_001'}, {'opt_z51_001'}, {'opt_5zu_001', 'opt_tvs_001'},
                           {'opt_5zu_001', 'opt_z51_001'}):
                with self.subTest(extras=extras):
                    result = artwork.project(cat, replace(state, installed=state.installed | extras))
                    self.assertEqual(result['coverage'], 'art_not_available')
                    self.assertEqual(result['assets'], [])
            for installed in (frozenset(), state.installed | {'opt_g8g_001'},
                              state.installed - {'opt_gba_001'} | {'opt_gph_001', 'opt_5zu_001'}):
                with self.subTest(installed=installed):
                    self.assertEqual(artwork.project(cat, replace(state, installed=installed))['coverage'], 'art_not_available')
            # Exercise actual catalog resolution, including ZF1 with replacement TVS.
            session = ConsumerSession(cat, '3lt_c07', 'no-spoiler-test')
            for oid in ('opt_gba_001', 'opt_z51_001', 'opt_zf1_001'):
                self.commit(session, 'select', oid)
            self.assertNotIn('opt_t0a_001', session._session.state.installed)
            self.assertEqual(session.current()['build']['visualizer']['coverage'], 'art_not_available')
            self.commit(session, 'select', 'opt_tvs_001')
            self.assertIn('opt_tvs_001', session._session.state.installed)
            self.assertEqual(session.current()['build']['visualizer']['coverage'], 'art_not_available')

    def test_no_spoiler_declaration_must_match_hash_pinned_evidence(self):
        with no_spoiler_fixture(self.catalogs['stingray']) as (root, scene):
            path = root / 'stingray-coupe' / 'manifest.json'
            for mutation in ('missing', 'group', 'exclusions', 'evidence_missing'):
                changed = copy.deepcopy(scene)
                if mutation == 'missing': del changed['no_spoiler']
                elif mutation == 'group': changed['no_spoiler']['group_id'] = 'different-group'
                elif mutation == 'exclusions': changed['no_spoiler']['excluded_option_ids'] = []
                else:
                    evidence_path = path.parent / scene['evidence']['file']
                    evidence = json.loads(evidence_path.read_text())
                    del evidence['no_spoiler']
                    write_json(evidence_path, evidence)
                    changed['evidence']['sha256'] = hashlib.sha256(evidence_path.read_bytes()).hexdigest()
                write_json(path, changed)
                with self.subTest(mutation=mutation), self.assertRaisesRegex(ValueError, 'no-spoiler binding mismatch'):
                    artwork.load(path.parent)

    def test_no_spoiler_contract_requires_model_owned_optional_scoped_group(self):
        cat = copy.copy(self.catalogs['stingray'])
        with no_spoiler_fixture(cat) as (_, scene):
            gid = scene['no_spoiler']['group_id']
            foreign = self.catalogs['grand_sport']
            foreign_gid = next(g['id'] for g in foreign.ev.rows['choice_group'] if g['id'] not in cat.ev.members)
            foreign_oid = next(oid for oid in foreign.ev.options if oid not in cat.ev.options)
            for mutation in ('minimum', 'maximum_zero', 'maximum_two', 'foreign_group',
                             'outside_group', 'scope', 'unknown_option', 'foreign_option'):
                cat.ev = copy.deepcopy(self.catalogs['stingray'].ev)
                changed = copy.deepcopy(scene)
                if mutation == 'minimum':
                    next(g for g in cat.ev.rows['choice_group'] if g['id'] == gid)['minimum'] = 1
                elif mutation in ('maximum_zero', 'maximum_two'):
                    next(g for g in cat.ev.rows['choice_group'] if g['id'] == gid)['maximum'] = (
                        0 if mutation == 'maximum_zero' else 2)
                elif mutation == 'foreign_group': changed['no_spoiler']['group_id'] = foreign_gid
                elif mutation == 'outside_group': cat.ev.members[gid].remove('opt_5zu_001')
                elif mutation == 'scope': cat.ev.scopes['choice_group'].remove((gid, '3lt_c07'))
                else: changed['no_spoiler']['excluded_option_ids'] = [foreign_oid if mutation == 'foreign_option' else 'missing']
                with self.subTest(mutation=mutation):
                    self.assertEqual(artwork.catalog_contract(cat, changed), dict(assets=[], coverage='art_not_available',
                                     reason='Artwork bindings need review for this catalog.'))

    def test_no_spoiler_declaration_requires_ids_even_when_both_documents_agree(self):
        with no_spoiler_fixture(self.catalogs['stingray']) as (root, scene):
            scene_root = root / 'stingray-coupe'
            evidence_path = scene_root / scene['evidence']['file']
            evidence = json.loads(evidence_path.read_text())
            for declaration in (None, {}, dict(group_id='', excluded_option_ids=[]),
                                dict(group_id='group', excluded_option_ids='opt_z51_001'),
                                dict(group_id='group', excluded_option_ids=[None])):
                changed = copy.deepcopy(scene)
                changed['no_spoiler'] = evidence['no_spoiler'] = declaration
                write_json(evidence_path, evidence)
                changed['evidence']['sha256'] = hashlib.sha256(evidence_path.read_bytes()).hexdigest()
                write_json(scene_root / 'manifest.json', changed)
                with self.subTest(declaration=declaration), self.assertRaisesRegex(ValueError, 'Invalid no-spoiler declaration'):
                    artwork.load(scene_root)

    def test_release_restores_art_and_rejects_rehashed_binding_declarations(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); store = ReleaseStore(root / 'store')
            with patch('catalog.releases.validate_semantics', return_value={'test_fixture':True}):
                frozen = store.freeze(self.db, database_hash(self.db))
            release = store.complete(frozen); manifest = store.verify(release)
            self.assertEqual(len(manifest['media']['assets']), 192)
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
