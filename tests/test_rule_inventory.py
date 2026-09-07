"""Review exports retain authored member order and component pricing evidence."""
import hashlib
from pathlib import Path
import sqlite3
import tempfile
import unittest

from catalog.importer import build
from catalog.rule_inventory import CHILDREN, inventory
from catalog.schema import TABLES


class RuleInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.database = Path(cls.temp.name) / 'catalog.sqlite'
        build(cls.database)
        cls.before = hashlib.sha256(cls.database.read_bytes()).hexdigest()
        cls.result = inventory(cls.database)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_group_members_follow_display_order_and_keep_all_fields(self):
        with sqlite3.connect(self.database) as db:
            db.row_factory = sqlite3.Row
            for model in self.result['models'].values():
                for family, (table, foreign_key) in CHILDREN.items():
                    for group in model['families'][family]:
                        expected = [dict(r) for r in db.execute(
                            f'SELECT * FROM {table} WHERE {foreign_key}=? '
                            'ORDER BY COALESCE(display_order,0),sequence,id',
                            (group['fields']['id'],))]
                        self.assertEqual([m['fields'] for m in group['members']], expected)
                        if group['fields']['legacy_id'] == 'gs_excl_performance_brakes':
                            self.assertEqual([m['fields']['display_order']
                                              for m in group['members']], [5, 10, 20])

    def test_shared_rates_preserve_fields_evidence_and_all_r6x_memberships(self):
        rates = {r['fields']['id']: r for r in self.result['shared_component_rates']}
        with sqlite3.connect(self.database) as db:
            db.row_factory = sqlite3.Row
            expected = {r['id']: dict(r) for r in db.execute('SELECT * FROM component_rate')}
            self.assertEqual({key: r['fields'] for key, r in rates.items()}, expected)
            for key, rate in rates.items():
                self.assertEqual(rate['source_rows'], [r[0] for r in db.execute(
                    'SELECT source_id FROM evidence_link WHERE entity_id=? ORDER BY source_id',
                    (key,))])
        for model in self.result['models'].values():
            components = model['families']['interior_component']
            r6x = [c for c in components if c['fields']['component_type'] == 'r6x']
            self.assertEqual(len(r6x), 15)
            for component in components:
                rate_id = component['fields']['rate_id']
                if rate_id is not None:
                    self.assertIn(rate_id, rates)
            for component in r6x:
                rate = rates[component['fields']['rate_id']]
                self.assertEqual(rate['fields']['amount'], '995')
                self.assertEqual(rate['fields']['code'], 'R6X')
                self.assertEqual(rate['fields']['basis'], 'component')
                self.assertEqual(rate['source_rows'], ['PriceRef!22'])

    def test_repeatable_and_database_unchanged(self):
        self.assertEqual(self.result, inventory(self.database))
        self.assertEqual(self.before, hashlib.sha256(self.database.read_bytes()).hexdigest())

    def test_option_rows_supply_inventory_names_and_policy(self):
        for model in self.result['models'].values():
            options={r['fields']['id']:r for r in model['families']['option']}
            for row in model['families']['variant_override']:
                target=options[row['fields']['option_id']]
                self.assertEqual(row['references']['option_id']['name'],target['fields']['name'])
                self.assertEqual(row['references']['option_id']['kind'],'option')
            self.assertTrue(all('selectable' in r['fields'] and r['source_rows'] for r in options.values()))

    def test_every_typed_record_and_relationship_is_present_once(self):
        records = {}

        def visit(value):
            if isinstance(value, dict):
                if 'fields' in value and 'id' in value['fields']:
                    key = value['fields']['id']
                    self.assertNotIn(key, records)
                    records[key] = value
                for child in value.values():
                    visit(child)
            elif isinstance(value, list):
                for child in value:
                    visit(child)

        visit(self.result)
        with sqlite3.connect(self.database) as db:
            db.row_factory = sqlite3.Row
            expected = {r['id']:dict(r) for table in TABLES
                        for r in db.execute(f'SELECT * FROM {table}')}
            self.assertEqual({key:r['fields'] for key,r in records.items()}, expected)
            for table, (spec, _) in TABLES.items():
                for row in db.execute(f'SELECT * FROM {table}'):
                    record = records[row['id']]
                    self.assertEqual(record['source_rows'], [r[0] for r in db.execute(
                        'SELECT source_id FROM evidence_link WHERE entity_id=? ORDER BY source_id',
                        (row['id'],))])
                    for item in spec.split():
                        field, typ = item.split(':')
                        if typ.startswith('@') and row[field] is not None:
                            self.assertEqual(record['references'][field]['id'], row[field])
                            self.assertIn(row[field], records)
            self.assertEqual(len(self.result['source_dispositions']),
                             db.execute('SELECT count(*) FROM source_disposition').fetchone()[0])
            self.assertEqual(sum(r['row_count'] for r in self.result['source_sheets']),
                             db.execute('SELECT count(*) FROM source_row').fetchone()[0])

    def test_shared_wheel_lock_prerequisite_does_not_merge_model_exclusions(self):
        matches = self.result['cross_model_matches']
        prerequisite = [r for r in matches if r['family'] == 'direct_rule'
                        and r['pattern']['fields']['source_id']['key'] == 'opt_spz_001'
                        and r['pattern']['fields']['target_id']['key'] == 'opt_spy_001'
                        and r['pattern']['fields']['effect'] == 'requires']
        self.assertEqual(len(prerequisite), 1)
        self.assertEqual({r['model'] for r in prerequisite[0]['occurrences']},
                         set(self.result['models']))
        # SU1 is a ZR1/ZR1X exclusion, not a shared requirement for every model.
        su1 = [r for r in matches if r['family'] == 'direct_rule'
               and r['pattern']['fields']['source_id']['key'] == 'opt_sfe_001'
               and r['pattern']['fields']['target_id']['key'] == 'opt_su1_001']
        self.assertEqual(len(su1), 1)
        self.assertEqual({r['model'] for r in su1[0]['occurrences']}, {'zr1', 'zr1x'})


if __name__ == '__main__':
    unittest.main()
