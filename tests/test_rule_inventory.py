"""Review exports retain authored member order and component pricing evidence."""
import hashlib
from pathlib import Path
import sqlite3
import tempfile
import unittest

from catalog.importer import build
from catalog.rule_inventory import CHILDREN, inventory


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


if __name__ == '__main__':
    unittest.main()
