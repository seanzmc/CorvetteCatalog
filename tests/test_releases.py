"""Release state transitions, source completeness, corruption and recovery."""
from contextlib import closing
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from catalog import foundation as f
from catalog.behavior_sources import import_behavior
from catalog.consumers import import_mappings, ConsumerCatalog
from catalog.releases import ReleaseStore, database_hash, membership, validate_translation, digest, write_json
from catalog.consumer_server import Application


class ReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db=f.connect(':memory:');f.create_schema(cls.db);import_behavior(cls.db);import_mappings(cls.db)
        cls.hash=database_hash(cls.db)

    @classmethod
    def tearDownClass(cls):cls.db.close()

    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.store=ReleaseStore(Path(self.tmp.name)/'releases')

    def freeze(self):
        # Lifecycle fault tests isolate the expensive audit. The real audit is
        # exercised separately through the freeze CLI on the final revision.
        with patch('catalog.releases.validate_semantics',return_value={'test_fixture':True}):
            return self.store.freeze(self.db,self.hash)

    def test_source_replay_and_all_lane_membership(self):
        validate_translation(self.db)
        members=membership(self.db)
        self.assertEqual(len(members),6);self.assertEqual(sum(m['is_default'] for m in members),1)
        self.assertEqual(sum(len(ConsumerCatalog(self.db,m['revision_id']).ev.configs) for m in members),32)

    def test_source_tampering_is_not_blessed_by_freeze(self):
        with closing(f.connect(':memory:')) as bad:
            self.db.backup(bad)
            bad.execute("UPDATE consumer_option SET presentation='{}' WHERE rowid=(SELECT min(rowid) FROM consumer_option)");bad.commit()
            with self.assertRaisesRegex(ValueError,'differs from complete'):
                validate_translation(bad)

    def test_extra_source_rows_do_not_pass_idempotent_replay(self):
        with closing(f.connect(':memory:')) as extra:
            self.db.backup(extra)
            extra.execute("INSERT INTO source_document VALUES ('unexpected','aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','unexpected','test')")
            extra.commit()
            with self.assertRaisesRegex(ValueError,'Unexpected source translation rows'):
                validate_translation(extra)

    def test_unpinned_schema_objects_are_rejected(self):
        changes = {
            'table': 'CREATE TABLE unexpected (payload TEXT)',
            'view': 'CREATE VIEW unexpected AS SELECT * FROM model',
            'index': 'CREATE INDEX unexpected ON model(model_key)',
            'trigger': '''CREATE TRIGGER unexpected AFTER DELETE ON model
                          BEGIN SELECT 1; END''',
            'column': 'ALTER TABLE model ADD COLUMN unexpected TEXT',
        }
        for kind, sql in changes.items():
            with self.subTest(kind=kind), closing(f.connect(':memory:')) as draft:
                self.db.backup(draft)
                draft.execute(sql)
                if kind == 'table':
                    draft.execute("INSERT INTO unexpected VALUES ('unpinned data')")
                draft.commit()
                with patch('catalog.releases.validate_semantics') as audit:
                    with self.assertRaisesRegex(ValueError, 'Unexpected source translation schema'):
                        self.store.freeze(draft, database_hash(draft))
                    audit.assert_not_called()
                self.assertEqual(list(self.store.frozen.iterdir()), [])

    def test_repeated_freeze_validates_existing_artifacts(self):
        frozen = self.freeze()
        self.assertEqual(self.freeze(), frozen)
        for name in ('catalog.sqlite', 'validation.json'):
            with self.subTest(artifact=name):
                artifact = self.store.frozen / frozen / name
                original = artifact.read_bytes()
                artifact.write_bytes(original + b'corrupt')
                try:
                    with self.assertRaisesRegex(ValueError, 'Frozen snapshot or validation was altered'):
                        self.freeze()
                    self.assertEqual(artifact.read_bytes(), original + b'corrupt')
                    self.assertEqual([p.name for p in self.store.frozen.iterdir()], [frozen])
                    self.assertEqual(self.store.pointer(), {'release_id': None, 'version': 0})
                finally:
                    artifact.write_bytes(original)
        self.store.frozen_record(frozen)

    def test_freeze_rejects_stale_snapshot_and_semantic_failure(self):
        with self.assertRaisesRegex(ValueError,'Stale draft'):
            self.store.freeze(self.db,'0'*64)
        with patch('catalog.releases.validate_semantics',side_effect=ValueError('bad semantic relationship')):
            with self.assertRaisesRegex(ValueError,'bad semantic'):
                self.store.freeze(self.db,self.hash)
        self.assertEqual(list(self.store.frozen.iterdir()),[])
        self.assertEqual(self.store.pointer(),{'release_id':None,'version':0})

    def test_edit_during_freeze_invalidates_snapshot_even_without_edit_version(self):
        with closing(f.connect(':memory:')) as draft:
            self.db.backup(draft)
            def edit(_):
                draft.execute('UPDATE configuration SET chooser_order=chooser_order+1');draft.commit()
                return {}
            with patch('catalog.releases.validate_semantics',side_effect=edit):
                with self.assertRaisesRegex(ValueError,'Draft changed'):
                    self.store.freeze(draft,self.hash)
        self.assertEqual(list(self.store.frozen.iterdir()),[])

    def test_deterministic_artifacts_publication_cas_and_rollback(self):
        frozen=self.freeze();release=self.store.complete(frozen)
        self.assertEqual(self.store.complete(frozen),release)
        manifest=self.store.verify(release)
        self.assertEqual(len([p for p in manifest['artifacts'] if p.endswith('/form.json')]),6)
        self.assertEqual(len([p for p in manifest['artifacts'] if p.endswith('/order.json')]),6)
        self.assertEqual(len([p for p in manifest['artifacts'] if p.endswith('/visualizer.json')]),6)
        self.assertEqual(self.store.publish(release,0),{'release_id':release,'version':1})
        with self.assertRaisesRegex(ValueError,'Stale publication'):
            self.store.publish(release,0)
        # A second independent identity uses a new draft edit version. All facts
        # and semantic behavior are unchanged, but membership identifies it.
        with closing(f.connect(':memory:')) as db:
            self.db.backup(db);db.execute('UPDATE catalog_revision SET edit_version=edit_version+1');db.commit()
            with patch('catalog.releases.validate_semantics',return_value={'test_fixture':True}):
                frozen2=self.store.freeze(db,database_hash(db))
        release2=self.store.complete(frozen2)
        self.assertNotEqual(release,release2)
        self.assertEqual(self.store.publish(release2,1)['release_id'],release2)
        self.assertEqual(self.store.rollback(2),{'release_id':release,'version':3})
        with self.assertRaisesRegex(ValueError,'Stale publication'):
            self.store.rollback(2)

    def test_failed_completion_and_corrupt_release_preserve_last_good_pointer(self):
        frozen=self.freeze();release=self.store.complete(frozen);self.store.publish(release,0)
        with patch('catalog.releases.write_json',side_effect=OSError('disk full')):
            with self.assertRaises(OSError):self.store.complete(frozen)
        self.assertEqual(self.store.pointer(),{'release_id':release,'version':1})
        self.assertFalse(any(p.name.startswith('.building') for p in self.store.completed.iterdir()))
        artifact=self.store.completed/release/'stingray/form.json';old=artifact.read_bytes();artifact.write_bytes(b'{}')
        with self.assertRaisesRegex(ValueError,'altered'):
            self.store.publish(release,1)
        self.assertEqual(self.store.pointer()['version'],1)
        artifact.write_bytes(old);self.store.verify(release)
        frozen_db=self.store.frozen/frozen/'catalog.sqlite'
        with frozen_db.open('ab') as stream:stream.write(b'corrupt')
        with self.assertRaisesRegex(ValueError,'altered'):
            self.store.complete(frozen)

    def test_backup_restore_in_fresh_store_and_corrupt_backup_refusal(self):
        release=self.store.complete(self.freeze())
        backup=Path(self.tmp.name)/'backup'
        self.assertEqual(self.store.backup(release,backup),release)
        recovered=ReleaseStore(Path(self.tmp.name)/'recovered')
        self.assertEqual(recovered.restore(backup),release)
        self.assertEqual(recovered.publish(release,0)['release_id'],release)
        (backup/'z06/order.json').write_text('{}')
        with self.assertRaisesRegex(ValueError,'altered'):
            recovered.restore(backup)
        self.assertEqual(recovered.pointer()['version'],1)

    def test_rehashed_manifest_cannot_omit_required_consumers(self):
        release=self.store.complete(self.freeze())
        folder=self.store.completed/release
        manifest=json.loads((folder/'manifest.json').read_text())
        (folder/'z06/form.json').unlink()
        del manifest['artifacts']['z06/form.json']
        replacement=digest(manifest)
        write_json(folder/'manifest.json',manifest)
        folder.rename(self.store.completed/replacement)
        with self.assertRaisesRegex(ValueError,'Missing required consumer artifact'):
            self.store.publish(replacement,0)
        self.assertEqual(self.store.pointer()['version'],0)

    def test_frozen_or_partial_release_cannot_publish(self):
        frozen=self.freeze()
        with self.assertRaises(FileNotFoundError):self.store.publish(frozen,0)
        self.assertEqual(self.store.pointer()['version'],0)
        with self.assertRaisesRegex(ValueError,'Invalid content'):
            self.store.verify('../anything')

    def test_http_application_uses_exact_pending_warning_and_signed_build_state(self):
        release=self.store.complete(self.freeze());app=Application(self.store,release)
        c=app.catalogs['z06'];cfg='1lz_h67'
        codes={r['rpo']:r['id'] for r in c.ev.options.values() if r['lifecycle']=='active'}
        call=lambda path,state,**body:app.dispatch(path,dict(body,build_token=state['build_token']))
        state=app.dispatch('/api/session',{'model':'z06','configuration_id':cfg})
        for code in ('GBA','DPB'):
            p=call('/api/preview',state,action='select',target=codes[code],version=state['version'])
            state=call('/api/confirm',state,**p,total_minor=0)
        before=state['build']
        p=call('/api/preview',state,action='select',target=codes['VPW'],version=state['version'])
        # A preview changes nothing: the same token still rebuilds the same build.
        self.assertEqual(before,call('/api/restore',state)['build'])
        self.assertTrue(any('DPB' in line and line.startswith('Remove:') for line in p['warning']['lines']))
        with self.assertRaises(ValueError):call('/api/confirm',state,version=state['version'],token='fake',warning_sha256=p['warning_sha256'])
        with self.assertRaises(ValueError):call('/api/confirm',state,**dict(p,warning_sha256='0'*64))
        # A pending token belongs to exactly the build it was previewed on.
        other=app.dispatch('/api/session',{'model':'z06','configuration_id':cfg})
        with self.assertRaises(ValueError):call('/api/confirm',other,**dict(p,version=other['version']))
        # Client-supplied candidates or totals are ignored.
        confirmed=call('/api/confirm',state,**p,candidate=before,total_minor=0)
        self.assertEqual(confirmed['build'],p['warning']['candidate'])
        self.assertNotEqual(confirmed['build'],before)
        # The confirmed build survives a new server process with the same key.
        key=b'k'*32;keyed=Application(self.store,release,token_key=key)
        s1=keyed.dispatch('/api/session',{'model':'z06','configuration_id':cfg})
        p1=keyed.dispatch('/api/preview',dict(build_token=s1['build_token'],action='select',target=codes['GBA'],version=0))
        s1=keyed.dispatch('/api/confirm',dict(p1,build_token=s1['build_token']))
        restored=Application(self.store,release,token_key=key).dispatch('/api/restore',{'build_token':s1['build_token']})
        self.assertEqual(restored['build'],s1['build']);self.assertTrue(restored['revertible'])
        with self.assertRaisesRegex(ValueError,'foreign build'):
            Application(self.store,release,token_key=b'x'*32).dispatch('/api/restore',{'build_token':s1['build_token']})
        # An expired review cannot be applied.
        p2=keyed.dispatch('/api/preview',dict(build_token=s1['build_token'],action='select',target=codes['DPB'],version=1))
        with patch('catalog.consumer_server.time.time',return_value=10**12):
            with self.assertRaises(ValueError):keyed.dispatch('/api/confirm',dict(p2,build_token=s1['build_token']))
        # Undo is a replayed action, not server memory.
        p3=keyed.dispatch('/api/preview',dict(build_token=s1['build_token'],action='revert',version=1))
        undone=keyed.dispatch('/api/confirm',dict(p3,build_token=s1['build_token']))
        self.assertFalse(undone['revertible'])
        self.assertEqual(keyed.dispatch('/api/restore',{'build_token':undone['build_token']})['build'],undone['build'])


if __name__=='__main__':unittest.main()
