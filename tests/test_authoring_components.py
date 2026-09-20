"""Shared component ownership, exact affected consumers and atomic authoring."""
from contextlib import closing
import unittest
from unittest.mock import patch

import test_authoring as base
from catalog import authoring as a, authoring_components as c
from catalog.authoring_server import Application
from catalog.consumers import ConsumerCatalog
from catalog.releases import database_hash, validate_translation


class ComponentTests(unittest.TestCase):
    setUpClass = classmethod(base.AuthoringTests.setUpClass.__func__)
    tearDownClass = classmethod(base.AuthoringTests.tearDownClass.__func__)

    def setUp(self):
        base.AuthoringTests.setUp(self)
        c.prepare(self.db)
        self.rev = self.revisions['z06']
        self.component, = self.db.execute("SELECT id FROM component WHERE revision_id=? AND kind='suede' AND code='N2Z'", (self.rev,)).fetchone()
        self.config = '3lz_h07'

    def change(self, **kwargs):
        data = c.detail(self.db,self.rev,self.component,self.config)
        return c.preview(self.db,self.rev,self.component,self.config,**(dict(etag=data['etag'],price='900.25',reason='Synthetic shared price test') | kwargs))

    def test_all_37_consumers_receive_one_exact_charge_and_other_rates_stay_fixed(self):
        # Accepted Z06 N2Z rate is $895; 37 exact 3LZ coupe leaves reference it.
        detail = c.detail(self.db,self.rev,self.component,self.config)
        self.assertEqual(detail['rate']['amount_minor'],89500)
        self.assertEqual(len(detail['members']),37)
        unaffected = [tuple(r) for r in self.db.execute('''SELECT * FROM component_rate
            WHERE NOT (revision_id=? AND component_id=? AND configuration_id=?)''', (self.rev,self.component,self.config))]
        old_catalog = ConsumerCatalog(self.db,self.rev)
        change = self.change()
        self.assertEqual(len(change['after_outcomes']),37)
        for old,new in zip(change['before_outcomes'],change['after_outcomes']):
            self.assertEqual(new['total_minor']-old['total_minor'],525)
            self.assertEqual((old['amount_minor'],new['amount_minor']),(89500,90025))
            self.assertEqual(old['resolved'],new['resolved'])
            self.assertEqual(old['installed'],new['installed'])
        saved = c.save(self.db,change)
        self.assertEqual(saved['history'][0]['after'],change['after'])
        self.assertEqual(saved['evidence'],detail['evidence'])
        self.assertEqual(saved['members'],detail['members'])
        self.assertEqual(saved['edit_version'],detail['edit_version']+1)
        self.assertEqual(unaffected,[tuple(r) for r in self.db.execute('''SELECT * FROM component_rate
            WHERE NOT (revision_id=? AND component_id=? AND configuration_id=?)''',(self.rev,self.component,self.config))])
        with closing(a.open_workspace(self.path)) as reopened:
            self.assertEqual(c.detail(reopened,self.rev,self.component,self.config)['history'],saved['history'])
            catalog = ConsumerCatalog(reopened,self.rev)
            for member in saved['members']:
                iid=member['interior_id']
                state=catalog.ev.transition(catalog.ev.state(self.config),'interior',iid)
                output=catalog.project(state,'local-authoring')
                charges=[r for r in output['charges'] if r['owner_kind']=='component' and r['owner_id']==self.component]
                self.assertEqual(len(charges),1)
                self.assertEqual(charges[0]['amount_minor'],90025)
            # This model's convertible uses a different rate record for the same component.
            iid=saved['members'][0]['interior_id']
            old=old_catalog.ev.transition(old_catalog.ev.state('3lz_h67'),'interior',iid)
            new=catalog.ev.transition(catalog.ev.state('3lz_h67'),'interior',iid)
            self.assertEqual(old,new)
        restored=c.save(self.db,self.change(price='895'))
        self.assertEqual(restored['rate'],detail['rate'])
        with self.assertRaisesRegex(ValueError,'Unexpected source translation schema'):
            validate_translation(self.db)
        with closing(base.f.connect(self.source)) as source:
            self.assertEqual(database_hash(source),self.source_digest)

    def test_all_six_model_owned_shared_rates(self):
        for model,revision in self.revisions.items():
            row=next(r for r in c.rates(self.db,revision) if r['kind']=='suede' and r['trim'].startswith('3'))
            detail=c.detail(self.db,revision,row['component_id'],row['configuration_id'])
            self.assertGreater(len(detail['members']),1)
            amount=row['amount_minor']+100
            change=c.preview(self.db,revision,row['component_id'],row['configuration_id'],detail['etag'],str(amount//100),'One dollar synthetic lane check')
            saved=c.save(self.db,change)
            self.assertEqual(saved['rate']['revision_id'],revision,model)
            for old,new in zip(change['before_outcomes'],change['after_outcomes']):
                self.assertEqual(new['total_minor']-old['total_minor'],100,model)
        self.assertEqual(self.db.execute('SELECT count(*) FROM authoring_component_change').fetchone()[0],6)

    def test_cancel_single_use_server_review_and_substitution(self):
        app=Application(self.path)
        d=c.detail(self.db,self.rev,self.component,self.config)
        body=dict(revision_id=self.rev,component_id=self.component,configuration_id=self.config,etag=d['etag'],price='900.25',reason='Server exercise')
        before=database_hash(self.db)
        first=app.dispatch('/api/component-rate/preview',body)
        second=app.dispatch('/api/component-rate/preview',body | {'previous_token':first['token']})
        with self.assertRaisesRegex(ValueError,'Preview expired'):
            app.dispatch('/api/component-rate/save',{'token':first['token']})
        app.dispatch('/api/cancel',{'token':second['token']})
        with self.assertRaisesRegex(ValueError,'Preview expired'):
            app.dispatch('/api/component-rate/save',{'token':second['token']})
        self.assertEqual(database_hash(self.db),before)
        third=app.dispatch('/api/component-rate/preview',body)
        saved=app.dispatch('/api/component-rate/save',{'token':third['token'],'price':'1.00'})
        self.assertEqual(saved['rate']['amount_minor'],90025)
        with self.assertRaisesRegex(ValueError,'Preview expired'):
            app.dispatch('/api/component-rate/save',{'token':third['token']})

    def test_stale_membership_and_independent_connection_edits(self):
        change=self.change()
        with closing(a.open_workspace(self.path)) as other:
            c.save(other,self.change(price='899'))
        with self.assertRaisesRegex(ValueError,'Stale edit'):
            c.save(self.db,change)
        change=self.change()
        iid=c.detail(self.db,self.rev,self.component,self.config)['members'][0]['interior_id']
        with self.db:
            self.db.execute('UPDATE interior_part SET role=? WHERE revision_id=? AND interior_id=? AND component_id=?',('changed role',self.rev,iid,self.component))
        with self.assertRaisesRegex(ValueError,'Stale edit'):
            c.save(self.db,change)

    def test_failed_candidate_and_failed_save_leave_no_partial_writes(self):
        change=self.change()
        before=database_hash(self.db)
        with patch('catalog.authoring_components.outcomes',side_effect=[change['before_outcomes'],ValueError('candidate failure')]):
            with self.assertRaisesRegex(ValueError,'candidate failure'):
                self.change()
        self.assertEqual(database_hash(self.db),before)
        with patch('catalog.authoring_components.validate_mappings',side_effect=ValueError('validation failure')):
            with self.assertRaisesRegex(ValueError,'validation failure'):
                c.save(self.db,change)
        self.assertEqual(database_hash(self.db),before)
        self.assertFalse(self.db.in_transaction)

    def test_money_identity_and_reason_guards(self):
        for price in ('-1','1.001','1e3','NaN','',None,895):
            with self.subTest(price=price),self.assertRaises(ValueError):
                self.change(price=price)
        with self.assertRaisesRegex(ValueError,'reason'):
            self.change(reason=' ')
        with self.assertRaisesRegex(ValueError,'No changes'):
            self.change(price='895.00')
        with self.assertRaisesRegex(ValueError,'shared by at least two'):
            c.detail(self.db,self.revisions['stingray'],self.component,self.config)
        saved=c.save(self.db,self.change(price='0'))
        self.assertEqual(saved['rate']['amount_minor'],0)
        self.assertIsNotNone(saved['rate']['basis_id'])


if __name__ == '__main__':
    unittest.main()
