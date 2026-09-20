"""Complete editor transactions, acceptance replay and authored release artifacts."""
from contextlib import closing
import hashlib
import json
import os
import shutil
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import test_authoring as base
from catalog import authoring as a, authoring_records as r, authoring_acceptance as ac
from catalog.authoring_server import Application
from catalog.consumers import ConsumerCatalog, encode, digest
from catalog.releases import database_hash, ReleaseStore


class ReleaseJobTests(unittest.TestCase):
    def test_release_process_reports_failure_without_blocking_editor_reads(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'draft.sqlite'
            with closing(base.f.connect(path)) as db:
                a.prepare(db, 'test-baseline')
            app = Application(path)
            try:
                self.assertNotEqual(app.release_worker.submit(os.getpid).result(timeout=15), os.getpid())
                job = app.dispatch('/api/release/create', {'etag': '0' * 64})['job']
                self.assertTrue(app.read('/api/editors')['editors'])
                with self.assertRaisesRegex(ValueError, 'Stale draft snapshot'):
                    app.release_jobs[job].result(timeout=15)
                result = app.read('/api/release/status?job=' + job)
                self.assertEqual(result['state'], 'failed')
                self.assertIn('Stale draft snapshot', result['error'])
                self.assertFalse(list((Path(directory) / 'releases/frozen').iterdir()))
            finally:
                app.release_worker.shutdown()


class OperationsTests(unittest.TestCase):
    setUpClass=classmethod(base.AuthoringTests.setUpClass.__func__)
    tearDownClass=classmethod(base.AuthoringTests.tearDownClass.__func__)
    # Reuse only fixture construction, not the pilot's seven test methods.
    def setUp(self):
        base.AuthoringTests.setUp(self)
        self.app=Application(self.path)

    def request(self,table,key,values,action='update',**extra):
        return dict(table=table,key=dict(revision_id=self.rev,**key),values=values,action=action,**extra)

    def edit(self,requests,**extra):
        change=r.preview(self.db,self.rev,database_hash(self.db),requests,'Synthetic regression evidence',**extra)
        r.save(self.db,change)
        return change

    def test_typed_editors_all_lanes_and_exact_money(self):
        for revision in self.revisions.values():
            self.rev=revision
            option=dict(self.db.execute("SELECT * FROM option WHERE revision_id=? AND rpo='RYT'",(revision,)).fetchone())
            old=option['purchase_amount_minor']
            change=self.edit([self.request('option',dict(id=option['id']),dict(purchase_amount_minor=old+125,name=option['name']+' reviewed'))])
            self.assertEqual(ConsumerCatalog(self.db,revision).option(option['id'])['label'],option['name']+' reviewed')
            self.assertTrue(change['connected_after'])
        self.assertEqual(self.db.execute('SELECT count(*) FROM authoring_record_change').fetchone()[0],6)

    def test_coupled_endpoint_and_prerequisite_edit(self):
        rid='rule_opt_pdy_001_includes_opt_ryt_001'
        # Move the inclusion to a different independently purchasable accessory,
        # and update its matched continuing requirement in one transaction.
        target=self.db.execute("SELECT id FROM option WHERE revision_id=? AND rpo='SFE'",(self.rev,)).fetchone()[0]
        requirement=dict(self.db.execute("SELECT r.* FROM requirement r JOIN condition_member m ON m.revision_id=r.revision_id AND m.condition_id=r.satisfaction_condition_id WHERE r.revision_id=? AND r.source_option_id='opt_pdy_001' AND m.option_id='opt_ryt_001'",(self.rev,)).fetchone())
        member=dict(self.db.execute('SELECT * FROM condition_member WHERE revision_id=? AND condition_id=?',(self.rev,requirement['satisfaction_condition_id'])).fetchone())
        requests=[self.request('acquisition',dict(id=rid),dict(target_option_id=target)),
                  self.request('condition_member',{k:member[k] for k in ('condition_id','clause_id','member_id')},dict(option_id=target))]
        invalid=json.loads(encode(requests));invalid[0]['values']['target_option_id']='opt_v8x_001';invalid[1]['values']['option_id']='opt_v8x_001'
        with self.assertRaisesRegex(ValueError,'Cannot verify affected|Previously active'):
            self.edit(invalid)
        change=self.edit(requests,scenarios=[dict(configuration_id='1lt_c07',actions=[dict(action='select',target='opt_pdy_001'),dict(action='remove',target='opt_pdy_001')])])
        self.assertTrue(change['connected_after'])
        ev=ConsumerCatalog(self.db,self.rev).ev
        state=ev.transition(ev.state('1lt_c07'),'select','opt_pdy_001')
        self.assertIn(target,state.resolved)
        self.assertNotIn('opt_ryt_001',state.resolved)

    def test_broader_editor_rejects_overlapping_ownership(self):
        self.rev=self.revisions['grand_sport_x']
        before=database_hash(self.db)
        with self.assertRaisesRegex(ValueError,'Cannot verify affected|conflicting overlaps'):
            self.edit([self.request('acquisition',dict(id='grand_sport_x_rule_bc4_includes_d3v_519876ef19b6'),dict(intent_policy='absorb_prior'))])
        self.assertEqual(database_hash(self.db),before)

    def test_create_owned_option_and_remove_membership_preserve_evidence(self):
        old_count=self.db.execute('SELECT count(*) FROM source_anchor').fetchone()[0]
        change=self.edit([self.request('option',dict(id=self.oid),dict(name='Synthetic new accessory',rpo='TST'),action='clone')])
        created=next(op['after'] for op in change['operations'] if op['table']=='option')
        self.assertNotEqual(created['id'],self.oid)
        self.assertEqual(ConsumerCatalog(self.db,self.rev).option(created['id'])['label'],'Synthetic new accessory')
        self.assertEqual(self.db.execute('SELECT count(*) FROM option_configuration WHERE revision_id=? AND option_id=?',(self.rev,created['id'])).fetchone()[0],6)
        self.assertEqual(old_count,self.db.execute('SELECT count(*) FROM source_anchor').fetchone()[0])
        with self.assertRaisesRegex(ValueError,'Retire'):
            self.edit([self.request('option',dict(id=self.oid),{},action='delete')])

    def test_cancel_stale_tokens_validation_and_raw_change_guards(self):
        request=self.request('option',dict(id=self.oid),dict(purchase_amount_minor=6125))
        body=dict(revision_id=self.rev,etag=database_hash(self.db),requests=[request],reason='Token exercise')
        before=database_hash(self.db)
        first=self.app.dispatch('/api/records/preview',body)
        self.app.dispatch('/api/cancel',dict(token=first['token']))
        self.assertEqual(database_hash(self.db),before)
        with self.assertRaisesRegex(ValueError,'expired'): self.app.dispatch('/api/records/save',dict(token=first['token']))
        pending=self.app.dispatch('/api/records/preview',body)
        with self.db: self.db.execute("UPDATE component SET code=code||'X' WHERE revision_id=? AND id=(SELECT id FROM component WHERE revision_id=? LIMIT 1)",(self.rev,self.rev))
        with self.assertRaisesRegex(ValueError,'Stale'): self.app.dispatch('/api/records/save',dict(token=pending['token']))
        with self.assertRaisesRegex(ValueError,'Unrecorded'): ac.replay(self.db,False)
        before=database_hash(self.db)
        with self.assertRaises(Exception): self.edit([self.request('option',dict(id=self.oid),dict(purchase_amount_minor=-1))])
        self.assertEqual(database_hash(self.db),before)
        with self.assertRaisesRegex(ValueError,'read-only'): self.edit([self.request('option',dict(id=self.oid),dict(evidence_set_id='fake'))])
        with self.assertRaisesRegex(ValueError,'policies must be explicit'):
            self.edit([self.request('acquisition',dict(id='rule_opt_pdy_001_includes_opt_ryt_001'),dict(intent_policy=None))])

    def test_new_replacement_plan_with_actions_and_scope(self):
        condition=self.db.execute("SELECT id FROM condition WHERE revision_id=? AND mode='always' LIMIT 1",(self.rev,)).fetchone()[0]
        plan=r.new_record(self.db,self.rev,'replacement_plan')
        requests=[self.request('replacement_plan',dict(id=plan['id']),dict(condition_id=condition,requested_option_id=self.oid),action='create'),
            self.request('replacement_plan_configuration',dict(plan_id=plan['id'],configuration_id='1lt_c07'),{},action='create'),
            self.request('replacement_action',dict(plan_id=plan['id'],position=1),dict(option_id='opt_sfe_001',action='remove',intent_effect=None),action='create'),
            self.request('replacement_action',dict(plan_id=plan['id'],position=2),dict(option_id=self.oid,action='add',intent_effect='commit_purchase'),action='create')]
        change=self.edit(requests,scenarios=[dict(configuration_id='1lt_c07',actions=[dict(action='select',target=self.oid)])])
        ev=ConsumerCatalog(self.db,self.rev).ev
        state=ev.transition(ev.transition(ev.state('1lt_c07'),'select','opt_sfe_001'),'select',self.oid)
        self.assertIn(self.oid,state.resolved)
        self.assertNotIn('opt_sfe_001',state.resolved)
        self.assertTrue(change['connected_after'])
        self.assertEqual(ac.replay(self.db,False)['product_sha256'],ac.product_hash(self.db))

    def test_configuration_interior_copy_and_emission_reach_consumers(self):
        cat=ConsumerCatalog(self.db,self.rev)
        interior=next(i for i,c in cat.ev.interior_scopes if c=='1lt_c07')
        self.edit([self.request('configuration',dict(id='1lt_c67'),dict(enabled=0)),
                   self.request('interior',dict(id=interior),dict(enabled=0)),
                   self.request('configuration',dict(id='1lt_c07'),dict(starting_amount_minor=7349512))])
        cat=ConsumerCatalog(self.db,self.rev)
        self.assertFalse(cat.maps['configuration']['1lt_c67']['active'])
        self.assertEqual(cat.maps['configuration']['1lt_c07']['base_price'],73495.12)
        self.assertNotIn(interior,[i['interior_id'] for i in cat.cards(cat.ev.state('1lt_c07'))['interiors']])
        from catalog.semantic_validation import Audit
        audit=Audit(self.db,self.rev)
        self.assertNotIn('1lt_c67',audit.ev.configs)
        self.assertFalse(any(i==interior for i,c in audit.ev.interior_scopes))
        audit._disjoint.cache_clear()
        mapping=dict(self.db.execute('SELECT * FROM consumer_option WHERE revision_id=? AND option_id=?',(self.rev,self.oid)).fetchone())
        payload=json.loads(mapping['presentation']);payload['emit_code']=False
        self.edit([self.request('consumer_option',dict(option_id=self.oid),dict(presentation=encode(payload)))])
        cat=ConsumerCatalog(self.db,self.rev);state=cat.ev.transition(cat.ev.state('1lt_c07'),'select',self.oid)
        self.assertNotIn(self.oid,[o['option_id'] for o in cat.project(state,'test')['order_codes']])
        self.assertIn(self.oid,state.resolved)
        payload['name']='Wrong owner'
        with self.assertRaisesRegex(ValueError,'owning product'):
            self.edit([self.request('consumer_option',dict(option_id=self.oid),dict(presentation=encode(payload)))])

    def test_contextual_prices_and_owned_membership_replay(self):
        for revision in self.revisions.values():
            self.rev=revision
            rate=dict(self.db.execute('SELECT * FROM option_rate WHERE revision_id=? AND amount_minor IS NOT NULL LIMIT 1',(revision,)).fetchone())
            change=self.edit([self.request('option_rate',dict(id=rate['id']),dict(amount_minor=rate['amount_minor']+125))])
            self.assertTrue(change['connected_after'])
            self.assertEqual(self.db.execute('SELECT amount_minor FROM option_rate WHERE revision_id=? AND id=?',(revision,rate['id'])).fetchone()[0],rate['amount_minor']+125)
        self.rev=self.revisions['stingray']
        scope=dict(self.db.execute('SELECT * FROM interior_configuration WHERE revision_id=? LIMIT 1',(self.rev,)).fetchone())
        anchors=self.db.execute('SELECT count(*) FROM source_anchor').fetchone()[0]
        removed=self.edit([self.request('interior_configuration',dict(interior_id=scope['interior_id'],configuration_id=scope['configuration_id']),{},action='delete')])
        self.assertTrue(any(o['table']=='interior_configuration_translation' for o in removed['operations']))
        self.assertEqual(self.db.execute('SELECT count(*) FROM source_anchor').fetchone()[0],anchors)
        # Exact replay includes restored/deleted translation links, not only values.
        self.assertEqual(ac.replay(self.db,False)['product_sha256'],ac.product_hash(self.db))

    def test_source_plus_approved_history_release_and_recovery(self):
        self.edit([self.request('option',dict(id=self.oid),dict(purchase_amount_minor=6125,name='Accepted test first aid kit'))])
        with self.assertRaisesRegex(ValueError,'Unaccepted'): ac.replay(self.db)
        source=Path('docs/stingray-structured-records.json')
        payload=dict(source_path=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),locator='baseline_rows/stingray_options',
                     assertion='Synthetic test interpretation',scope='Stingray',comparison='changed',ambiguity='Synthetic evidence; no business correction',coverage='partial')
        iid=ac.stage(self.db,payload)['intake_id']
        self.assertEqual(ac.stage(self.db,payload)['intake_id'],iid)
        history=ac.events(self.db)
        acceptance=ac.preview(self.db,database_hash(self.db),'Test reviewer','Synthetic release qualification',
                              [dict(intake_id=iid,resolution='Test-only recorded interpretation',change_ids=[history[0]['change_ref']])])
        ac.accept(self.db,acceptance)
        report=ac.replay(self.db)
        self.assertEqual(report['acceptance']['reviewer'],'Test reviewer')
        self.assertEqual(report['intake'][0]['disposition'],'accepted')
        store=ReleaseStore(Path(self.tmp.name)/'releases')
        with patch('catalog.releases.validate_semantics',return_value={'test':'mocked, real milestone separate'}):
            frozen=store.freeze(self.db,database_hash(self.db))
        release=store.complete(frozen)
        self.assertEqual(store.complete(frozen),release)
        manifest=store.verify(release)
        self.assertIn('reviewed-edits.json',manifest['artifacts'])
        self.assertEqual(json.loads((store.completed/release/'reviewed-edits.json').read_text()),report)
        store.publish(release,0)
        backup=Path(self.tmp.name)/'backup';store.backup(release,backup)
        restored=ReleaseStore(Path(self.tmp.name)/'restored');self.assertEqual(restored.restore(backup),release)
        restored.verify(release)
        resumed=Path(self.tmp.name)/'resumed.sqlite'
        a.initialize(backup/'catalog.sqlite',resumed)
        with closing(a.open_workspace(resumed)) as resumed_db:
            self.assertEqual(ac.events(resumed_db),ac.events(self.db))
            self.assertEqual(ac.product_hash(resumed_db),ac.product_hash(self.db))
        forged=Path(self.tmp.name)/'forged';shutil.copytree(backup,forged)
        changed=json.loads((forged/'manifest.json').read_text())
        del changed['freeze']['reviewed_edits_sha256']
        changed['frozen_id']=digest(changed['freeze'])
        del changed['artifacts']['reviewed-edits.json']
        (forged/'reviewed-edits.json').unlink()
        (forged/'manifest.json').write_text(encode(changed))
        with self.assertRaisesRegex(ValueError,'require reviewed edit evidence'):
            restored._verify_path(forged,digest(changed))
        # New unaccepted edits and unrecorded changes cannot inherit approval.
        self.edit([self.request('option',dict(id=self.oid),dict(purchase_amount_minor=6250))])
        with self.assertRaisesRegex(ValueError,'Unaccepted'): ac.replay(self.db)
        self.assertEqual(store.pointer()['release_id'],release)
        with self.db: self.db.execute("UPDATE authoring_intake SET reason='tampered'")
        with self.assertRaisesRegex(ValueError,'Unaccepted'): ac.replay(self.db)

    def test_intake_deferral_removal_coverage_and_schema_guards(self):
        self.edit([self.request('option',dict(id=self.oid),dict(purchase_amount_minor=6125))])
        source=Path('docs/stingray-structured-records.json')
        payload=dict(source_path=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),locator='test',assertion='Test removal',scope='Stingray',comparison='removed',ambiguity='unknown',coverage='partial')
        iid=ac.stage(self.db,payload)['intake_id']
        ac.disposition(self.db,iid,'deferred','Test','Need complete source coverage')
        with self.assertRaisesRegex(ValueError,'complete relevant source coverage'):
            ac.preview(self.db,database_hash(self.db),'Test','Cannot accept partial removal',[dict(intake_id=iid,resolution='Not enough evidence',change_ids=[ac.events(self.db)[0]['change_ref']])])
        with self.db: self.db.execute('CREATE INDEX extra_authoring_index ON authoring_record_change(reason)')
        with self.assertRaisesRegex(ValueError,'authoring schema'): ac.replay(self.db,False)
