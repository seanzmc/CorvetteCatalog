"""Full frozen parity plus mutations proving typed facts drive the live surface."""
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from catalog.contracts import Catalog, generate, generate_bundle, write_bundle
from catalog.importer import build
from catalog.parity import compare, differences
from catalog.schema import connect


class ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        cls.database=Path(cls.temp.name)/'catalog.sqlite'
        build(cls.database)
        cls.contracts=generate(cls.database,'fixed-test-time')

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_all_six_contracts_and_registry_equal_frozen_baseline(self):
        report=compare(self.database)
        self.assertTrue(report['passed'],json.dumps(report,indent=2))
        self.assertEqual(len(report['models']),6)
        manifest=json.loads((Path(__file__).resolve().parents[1]/'baselines/2026-09-06/manifest.json').read_text())
        for row in manifest['verification']['contracts']:
            self.assertEqual(report['models'][row['model']]['business_content_sha256'],row['business_content_sha256'])

    def test_generation_does_not_read_source_evidence_or_reference_files(self):
        db=connect(self.database)
        forbidden={'source_row','source_sheet','evidence_link','source_disposition','code_evidence'}
        def authorize(action,table,*_):
            return sqlite3.SQLITE_DENY if action==sqlite3.SQLITE_READ and table in forbidden else sqlite3.SQLITE_OK
        db.set_authorizer(authorize)
        try:
            # Deny all filesystem reads during the in-memory typed generation.
            with patch('builtins.open',side_effect=AssertionError('Unexpected file read')):
                catalog=Catalog(db)
                actual={m['model_key']:catalog.generate(m,'fixed-test-time') for m in catalog.tables['model'] if m['active']}
            self.assertEqual(actual,self.contracts)
        finally:
            db.close()

    def test_typed_price_label_availability_and_scope_mutations_reach_output(self):
        db=connect(self.database)
        try:
            db.execute('BEGIN')
            mid=db.execute("SELECT id FROM model WHERE model_key='stingray'").fetchone()[0]
            oid=db.execute("SELECT id FROM offering WHERE model_id=? AND legacy_id='opt_z51_001'",(mid,)).fetchone()[0]
            db.execute("UPDATE offering_price SET amount='9999' WHERE offering_id=?",(oid,))
            db.execute("UPDATE offering_presentation SET label='Test package' WHERE offering_id=?",(oid,))
            db.execute("UPDATE availability SET status='standard' WHERE offering_id=?",(oid,))
            db.execute("UPDATE scope_axis SET all_token=NULL WHERE owner_id IN (SELECT id FROM default_rule WHERE model_id=?)",(mid,))
            catalog=Catalog(db)
            actual=catalog.generate(catalog.by_id[mid],'fixed-test-time')
            package=[c for c in actual['choices'] if c['option_id']=='opt_z51_001']
            self.assertEqual(len(package),6)
            self.assertTrue(all(c['base_price']==9999 and c['label']=='Test package' and c['status']=='standard' for c in package))
            expected_scopes={r['rule_id']:('' if r['body_style_scope']=='*' else r['body_style_scope']) for r in self.contracts['stingray']['defaultSelectionRules']}
            self.assertEqual({r['rule_id']:r['body_style_scope'] for r in actual['defaultSelectionRules']},expected_scopes)
            for key,contract in self.contracts.items():
                if key!='stingray':
                    m=next(m for m in catalog.tables['model'] if m['model_key']==key)
                    self.assertEqual(catalog.generate(m,'fixed-test-time'),contract)
        finally:
            db.rollback();db.close()

    def test_component_rates_and_derivation_permissions_are_data_driven(self):
        db=connect(self.database)
        try:
            db.execute('BEGIN')
            mid=db.execute("SELECT id FROM model WHERE model_key='z06'").fetchone()[0]
            db.execute('DELETE FROM derivation_permission WHERE model_id=?',(mid,))
            catalog=Catalog(db)
            actual=catalog.generate(catalog.by_id[mid],'fixed-test-time')
            self.assertEqual(len(self.contracts['z06']['rules'])-len(actual['rules']),5)
            self.assertFalse(any(r['rule_id'].startswith('derived_') for r in actual['rules']))
            db.execute("UPDATE component_rate SET amount='1234' WHERE component_type='suede' AND code='N26'")
            catalog=Catalog(db)
            actual=catalog.generate(catalog.by_id[mid],'fixed-test-time')
            changed=[c for i in actual['interiors'] for c in i['interior_components'] if c['rpo']=='N26']
            self.assertTrue(changed)
            self.assertTrue(all(c['price']==1234 for c in changed))
        finally:
            db.rollback();db.close()

    def test_missing_availability_and_stale_permissions_fail(self):
        db=connect(self.database)
        try:
            db.execute('BEGIN')
            db.execute("DELETE FROM availability WHERE id=(SELECT id FROM availability LIMIT 1)")
            with self.assertRaises(KeyError):
                catalog=Catalog(db)
                for m in catalog.tables['model']:catalog.generate(m,'test')
            db.rollback()
            db.execute('BEGIN')
            db.execute("UPDATE direct_rule SET effect='requires' WHERE effect='includes'")
            with self.assertRaisesRegex(ValueError,'Stale derivation permission'):
                catalog=Catalog(db)
                for m in catalog.tables['model']:catalog.generate(m,'test')
        finally:
            db.rollback();db.close()

    def test_reproducible_output_read_only_database_and_existing_directory_refusal(self):
        before=self.database.read_bytes()
        one,two=Path(self.temp.name)/'one',Path(self.temp.name)/'two'
        for path in (one,two):write_bundle(self.database,path,'fixed-test-time')
        for path in one.rglob('*'):
            if path.is_file():self.assertEqual(path.read_bytes(),(two/path.relative_to(one)).read_bytes())
        with self.assertRaises(FileExistsError):write_bundle(self.database,one)
        self.assertEqual(self.database.read_bytes(),before)

    def test_failed_generation_leaves_no_output(self):
        target=Path(self.temp.name)/'failed'
        with patch('catalog.contracts.registry_script',side_effect=ValueError('forced failure')):
            with self.assertRaisesRegex(ValueError,'forced failure'):write_bundle(self.database,target)
        self.assertFalse(target.exists())
        self.assertFalse(list(target.parent.glob('.contracts-*')))

    def test_comparison_rejects_type_order_and_missing_value_drift(self):
        self.assertEqual(list(differences({'v':[0,1]},{'v':[False,1]})),['/v/0'])
        self.assertEqual(list(differences({'v':[0,1]},{'v':[1,0]})),['/v/0','/v/1'])
        self.assertEqual(list(differences({'v':None},{})),['/v'])


if __name__=='__main__':unittest.main()
