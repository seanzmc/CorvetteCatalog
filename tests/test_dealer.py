"""Dealer wire compatibility and confirmed-state accounting, without delivery."""
from contextlib import closing
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import test_consumers as base
from catalog import dealer, foundation as f
from catalog.consumers import ConsumerCatalog, ConsumerSession
from catalog.consumer_server import Application
from catalog.evaluator import EvaluationError
from catalog.releases import ReleaseStore, database_hash


class DealerTests(unittest.TestCase):
    setUpClass = classmethod(base.ConsumerTests.setUpClass.__func__)
    tearDownClass = classmethod(base.ConsumerTests.tearDownClass.__func__)
    oid = base.ConsumerTests.oid
    commit = base.ConsumerTests.commit

    def complete(self, key='stingray', cfg='1lt_c07', iid='1LT_AQ9_HTA', catalog=None):
        c = catalog or self.catalogs[key]
        s = ConsumerSession(c, cfg, 'test-release')
        self.commit(s, 'select', self.oid(c, 'GBA'))
        self.commit(s, 'interior', iid)
        return s

    def body(self, session):
        return dict(version=session.version, customer=dict(name='Ada Buyer', email='ada@example.com'),
                    turnstile_token='test-token')

    @staticmethod
    def items(order):
        return [item for section in order['sections'] for item in section['items']]

    def test_six_model_contract_against_captured_existing_form(self):
        # Frozen output from the read-only 27vette runtime; fixture records exact
        # source hashes. Compare section order and item content, not the old
        # insertion-dependent order inside a section.
        evidence = json.loads((Path(__file__).parent / 'fixtures/dealer-baseline.json').read_text())
        for expected in evidence['cases']:
            key = {'grandSport': 'grand_sport'}.get(expected['model'], expected['model'])
            with self.subTest(model=key):
                s = self.complete(key, expected['configuration_id'], expected['interior_id'])
                actual = dealer.prepare(s, self.body(s))['payload']
                self.assertEqual(set(actual), {'model','customer','vehicle','sections','msrp','plain_text_summary','turnstile_token'})
                for field in ('model', 'vehicle', 'msrp'):
                    self.assertEqual(actual[field], expected[field])
                self.assertEqual([s['section'] for s in actual['sections']], [s['section'] for s in expected['sections']])
                for got, want in zip(actual['sections'], expected['sections']):
                    self.assertCountEqual(got['items'], want['items'])
                self.assertEqual(actual['customer']['address'], '')
                self.assertNotIn('comments', actual['customer'])

    def test_all_32_body_trim_configurations_account_for_actual_charges(self):
        count = 0
        for key, c in self.catalogs.items():
            for cfg in c.ev.configs:
                choices = [i for i in c.ev.interiors if (i, cfg) in c.ev.interior_scopes]
                iid = next((i for i in choices if 'HTA' in i), choices[0])
                with self.subTest(model=key, cfg=cfg):
                    s = self.complete(key, cfg, iid)
                    order = dealer.review(s, s.version)
                    self.assertEqual(round(100 * (order['vehicle']['base_price'] + sum(i['price'] for i in self.items(order)))),
                                     s.order()['total_minor'])
                    self.assertEqual(order['vehicle']['trim_level'], c.ev.configs[cfg]['trim'].upper())
                    count += 1
        self.assertEqual(count, 32)

    def test_paid_interiors_emit_each_actual_owner_once(self):
        s = self.complete('z06', '3lz_h07', '3LZ_AE4_EPX_N2Z')
        order = dealer.review(s, s.version)
        items = self.items(order)
        # Inspected source: 3LZ coupe AE4 $595, N2Z $895, identity $0.
        for code, price in (('AE4', 595), ('N2Z', 895), ('EPX', 0)):
            self.assertEqual([i['price'] for i in items if i['rpo'] == code], [price])
        s = self.complete('z06', '3lz_h07', '3LZ_R6X_AE4_HU0_38S')
        items = self.items(dealer.review(s, s.version))
        # The current evaluator retains the purchased seat owner alongside R6X.
        # Do not silently lose its charge because legacy component copy lacks it.
        for code, price in (('AE4', 595), ('R6X', 995), ('38S', 495)):
            self.assertEqual([i['price'] for i in items if i['rpo'] == code], [price])

    def test_package_children_and_reference_only_codes_keep_price_semantics(self):
        s = self.complete()
        self.commit(s, 'select', self.oid(s.catalog, 'Z51'))
        codes = [i['rpo'] for i in self.items(dealer.review(s, s.version))]
        self.assertIn('Z51', codes)
        self.assertNotIn('JL9', codes)
        self.commit(s, 'select', self.oid(s.catalog, 'R8C'))
        items = self.items(dealer.review(s, s.version))
        self.assertNotIn('CFX', [i['rpo'] for i in items])
        self.assertEqual([i['price'] for i in items if i['rpo'] == 'R8C'], [1695])
        self.assertIn('CFX', [i['rpo'] for i in s.order()['resolved']])

    def test_edited_prices_and_copy_use_current_catalog_not_source_metadata(self):
        with closing(f.connect(':memory:')) as db:
            self.db.backup(db)
            c = self.catalogs['stingray']; oid = self.oid(c, 'RYT')
            # This isolates the consumer boundary. Reviewed acceptance/replay is
            # covered in test_authoring_operations, not bypassed in a release.
            db.execute('UPDATE option SET purchase_amount_minor=6125 WHERE revision_id=? AND id=?', (c.revision, oid))
            saved = json.loads(db.execute('SELECT presentation FROM consumer_option WHERE revision_id=? AND option_id=?', (c.revision, oid)).fetchone()[0])
            saved['name'] = 'Reviewed <lamp> & accessory'; saved['emit_code'] = False
            db.execute('UPDATE consumer_option SET presentation=? WHERE revision_id=? AND option_id=?', (json.dumps(saved), c.revision, oid))
            c = ConsumerCatalog(db, c.revision); s = self.complete(catalog=c)
            self.commit(s, 'select', oid)
            payload = dealer.prepare(s, self.body(s))['payload']
            self.assertEqual(payload['msrp'], '$73,556.25')
            item, = [i for i in self.items(payload) if i['label'] == saved['name']]
            self.assertEqual(item, dict(rpo='', label=saved['name'], price=61.25))
            self.assertIn('Reviewed &lt;lamp&gt; &amp; accessory: $61.25', payload['plain_text_summary'])

    def test_contact_validation_escaping_and_no_client_order_overrides(self):
        s = self.complete(); body = self.body(s)
        body['customer'].update(name=' <Ada> & Buyer ', comments='<script>bad()</script>', phone=' 555-0100 ')
        payload = dealer.prepare(s, body)['payload']
        self.assertIn('&lt;Ada&gt; &amp; Buyer', payload['plain_text_summary'])
        self.assertNotIn('<script>', payload['plain_text_summary'])
        self.assertEqual(payload['customer']['phone'], '555-0100')
        self.assertNotIn('option_id', payload['plain_text_summary'])
        for customer in ({}, {'name':'Ada','email':'bad'}, {'name':'Ada','email':'a@b.c','comments':'x'*4001},
                         {'name':'Ada','email':'a@b.c','total_minor':0}):
            with self.subTest(customer=list(customer)), self.assertRaises(ValueError):
                dealer.prepare(s, {**body, 'customer':customer})
        for forged in ({'msrp':0}, {'sections':[]}, {'model':'zr1x'}):
            with self.assertRaises(ValueError): dealer.prepare(s, body | forged)
        with self.assertRaisesRegex(ValueError, 'Security check'):
            dealer.prepare(s, {**body, 'turnstile_token':''})
        self.assertEqual(dealer.prepare(s, {**body, 'turnstile_token':''}, require_turnstile=False)['payload']['turnstile_token'], '')

    def test_pending_incomplete_stale_and_foreign_session_are_rejected(self):
        c = self.catalogs['stingray']; incomplete = ConsumerSession(c, '1lt_c07', 'test-release')
        with self.assertRaisesRegex(EvaluationError, 'Complete required'):
            dealer.prepare(incomplete, self.body(incomplete))
        s = self.complete(); body = self.body(s)
        p = s.preview('select', self.oid(c, 'RYT'), s.version)
        with self.assertRaises(EvaluationError): dealer.prepare(s, body)
        s.confirm(p['token'], p['warning_sha256'], p['version'])
        with self.assertRaises(EvaluationError): dealer.prepare(s, body)
        with self.assertRaises(EvaluationError): dealer.review(s, True)
        self.assertEqual(dealer.prepare(s, self.body(s))['version'], s.version)

    def test_completed_release_serves_preview_and_explicit_live_configuration(self):
        with tempfile.TemporaryDirectory() as directory:
            store = ReleaseStore(directory)
            # Isolate the release packaging/HTTP contract; the real semantic
            # audit is separately run on the final runtime before delivery.
            with patch('catalog.releases.validate_semantics', return_value={'test_fixture':True}):
                frozen = store.freeze(self.db, database_hash(self.db))
            release = store.complete(frozen)
            for enabled in (False, True):
                app = Application(store, release, dealer_submissions=enabled)
                config = app.catalog()['dealer']
                self.assertEqual(config['enabled'], enabled)
                self.assertEqual(config['endpoint'], dealer.ENDPOINT if enabled else None)
                state = app.dispatch('/api/session', {'model':'stingray', 'configuration_id':'1lt_c07'})
                for action, target in (('select', self.oid(app.catalogs['stingray'], 'GBA')), ('interior', '1LT_AQ9_HTA')):
                    p = app.dispatch('/api/preview', dict(build_token=state['build_token'], action=action, target=target, version=state['version']))
                    state = app.dispatch('/api/confirm', dict(p, build_token=state['build_token']))
                body = dict(version=state['version'], customer=dict(name='Ada Buyer', email='ada@example.com'),
                            turnstile_token='', build_token=state['build_token'])
                if enabled:
                    with self.assertRaisesRegex(ValueError, 'Security check'): app.dispatch('/api/dealer/prepare', body)
                else:
                    self.assertEqual(app.dispatch('/api/dealer/prepare', body)['release_id'], release)
                with self.assertRaisesRegex(ValueError, 'foreign build'):
                    app.dispatch('/api/dealer/prepare', dict(body, build_token='foreign'))
            manifest = store.verify(release)
            self.assertIn('runtime/catalog/dealer.py', manifest['artifacts'])
            self.assertIn('runtime/catalog/web/dealer.js', manifest['artifacts'])


if __name__ == '__main__':
    unittest.main()
