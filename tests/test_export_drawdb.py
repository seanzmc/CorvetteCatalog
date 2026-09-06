"""Verify diagram structure against SQLite's implemented schema, not snapshots."""
from pathlib import Path
import unittest

from catalog.export_drawdb import export_sql, split_definitions
from catalog.schema import connect, create


class DrawDBExportTests(unittest.TestCase):
    def test_structure_and_order_preserve_every_key_and_reference(self):
        source, diagram = connect(":memory:"), connect(":memory:")
        self.addCleanup(source.close)
        self.addCleanup(diagram.close)
        create(source)
        sql = export_sql()
        diagram.executescript(sql)
        tables = lambda db: [r[0] for r in db.execute(
            "SELECT name FROM sqlite_schema WHERE type='table' ORDER BY rowid")]
        self.assertEqual(set(tables(source)), set(tables(diagram)))
        seen = set()
        for table in tables(diagram):
            for pragma in ("table_info", "foreign_key_list"):
                read = lambda db: [tuple(r) for r in db.execute(f'PRAGMA {pragma}("{table}")')]
                self.assertEqual(read(source), read(diagram), (table, pragma))
            def unique_keys(db):
                return sorted(tuple(r["name"] for r in db.execute(
                    f'PRAGMA index_info("{index["name"]}")'))
                    for index in db.execute(f'PRAGMA index_list("{table}")') if index["unique"])
            self.assertEqual(unique_keys(source), unique_keys(diagram), table)
            seen.add(table)
            for fk in diagram.execute(f'PRAGMA foreign_key_list("{table}")'):
                self.assertIn(fk["table"], seen, (table, tuple(fk)))

        self.assertFalse(diagram.execute("SELECT 1 FROM sqlite_schema WHERE type='trigger'").fetchall())
        for row in source.execute("SELECT sql FROM sqlite_schema WHERE type='trigger'"):
            self.assertIn("\n".join("-- " + line for line in (row[0] + ";").splitlines()), sql)
        for row in source.execute("SELECT sql FROM sqlite_schema WHERE type='table'"):
            for definition in split_definitions(row[0]):
                if definition.startswith("CHECK "):
                    self.assertIn("\n".join("-- " + line for line in definition.splitlines()), sql)

    def test_repeatable_and_committed_export_is_current(self):
        sql = export_sql()
        self.assertEqual(sql, export_sql())
        path = Path(__file__).resolve().parents[1] / "docs/schema-candidate.drawdb.sql"
        self.assertEqual(sql, path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
