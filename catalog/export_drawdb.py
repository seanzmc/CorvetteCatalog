"""Generate a disposable diagram from the implemented schema (stdlib only)."""
import argparse
from graphlib import TopologicalSorter
from pathlib import Path
import re

from catalog.schema import connect, create


def split_definitions(sql):
    """Split CREATE TABLE's body without splitting expressions or quoted text."""
    body = sql[sql.index("(") + 1:sql.rindex(")")]
    start = depth = 0
    for token in re.finditer(r"'(?:''|[^'])*'|\"(?:\"\"|[^\"])*\"|[(),]", body):
        value = token.group()
        if value == "(":
            depth += 1
        elif value == ")":
            depth -= 1
        elif value == "," and depth == 0:
            yield body[start:token.start()].strip()
            start = token.end()
    yield body[start:].strip()


def comment(sql):
    return "\n".join("-- " + line for line in sql.splitlines())


def export_sql():
    db = connect(":memory:")
    try:
        create(db)
        tables = dict(db.execute(
            "SELECT name, sql FROM sqlite_schema WHERE type='table' ORDER BY rowid"
        ).fetchall())
        dependencies = {
            name: sorted({row["table"] for row in db.execute(
                f'PRAGMA foreign_key_list("{name}")'
            ) if row["table"] != name})
            for name in tables
        }
        # drawDB resolves references as it reads tables. Fail on cross-table
        # cycles rather than silently exporting a diagram with missing edges.
        order = tuple(TopologicalSorter(dependencies).static_order())
        output = [
            "-- CorvetteCatalog: CURRENT DISPOSABLE CANDIDATE",
            "-- Not the final authoring/release design; visualization only.",
            "-- Generated from catalog.schema.create; do not edit or apply as a migration.",
            "-- Refresh: python3 -m catalog.export_drawdb",
            "-- Import into a new SQLite diagram in drawDB. See docs/drawdb.md.",
            "-- CHECK constraints and triggers are comments because drawDB cannot model them.",
            "-- Deferred FK timing is omitted; STRICT remains SQL-only diagram metadata.",
        ]
        for name in order:
            definitions = []
            omitted = []
            required_columns = {row["name"] for row in db.execute(
                f'PRAGMA table_info("{name}")'
            ) if row["notnull"]}
            for definition in split_definitions(tables[name]):
                if definition.upper().startswith("CHECK "):
                    omitted.append(comment(definition))
                    continue
                if " DEFERRABLE INITIALLY DEFERRED" in definition:
                    omitted.append(comment("Deferred in source: " + definition))
                    definition = definition.replace(" DEFERRABLE INITIALLY DEFERRED", "")
                # STRICT primary keys are implicitly NOT NULL in SQLite.
                # Spell this out so the diagram preserves actual nullability.
                if definition.split()[0] in required_columns and "NOT NULL" not in definition:
                    definition += " NOT NULL"
                definitions.append(definition)
            # Preserve the actual suffix, including SQLite STRICT.
            prefix = tables[name][:tables[name].index("(")]
            suffix = tables[name][tables[name].rindex(")") + 1:]
            output.append("\n" + prefix + "(\n  " + ",\n  ".join(definitions) + "\n)" + suffix + ";")
            output.extend(omitted)
        output.append("\n-- Trigger DDL retained as reference comments only; not imported by drawDB.")
        output.extend(comment(row[0] + ";") for row in db.execute(
            "SELECT sql FROM sqlite_schema WHERE type='trigger' ORDER BY name"
        ))
        return "\n".join(output) + "\n"
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1]
                        / "docs" / "schema-candidate.drawdb.sql")
    args = parser.parse_args()
    sql = export_sql()
    args.output.write_text(sql, encoding="utf-8")
    print(f"Wrote disposable candidate diagram SQL: {args.output}")


if __name__ == "__main__":
    main()
