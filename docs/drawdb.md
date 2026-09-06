# Current disposable candidate in drawDB

[schema-candidate.drawdb.sql](schema-candidate.drawdb.sql) visualizes the
**current disposable candidate**, not the final authoring/release design.
[catalog/schema.py](../catalog/schema.py) remains authoritative for the implemented
SQLite schema. The workbook remains canonical for the existing form. Diagram
edits and SQL exported back from drawDB must not be applied to the application.

## Open and refresh

1. Open the [drawDB editor](https://www.drawdb.app/editor) and choose **SQLite**
   for a new diagram.
2. Use **File → Import from SQL → Upload file**, choose
   `schema-candidate.drawdb.sql` from this directory, and import. Name it
   **CorvetteCatalog — current disposable candidate**.
3. Arrange tables as useful. Save a drawDB project locally if you want to retain
   that layout; it is a disposable viewing artifact.

After changing the implemented schema, run from the repository root:

```sh
python3 -m catalog.export_drawdb
python3 -m unittest discover -s tests -p test_export_drawdb.py -v
```

Review and commit the regenerated SQL alongside the schema change, then import
it into a **new** SQLite diagram. Refresh replaces your viewing copy; it does not
merge diagram edits or preserve its layout automatically. An optional
`--output /path/to/export.sql` writes elsewhere instead.

The exporter uses Python's standard library and SQLite 3.37+ (for STRICT), calls
the real schema creation function in memory, and reads `sqlite_schema` and
foreign-key metadata. No workbook, candidate database, product rows, application
dependency, hosting, account, or automatic synchronization is required.

## Compatibility and limits

Checked 2026-09-06 against drawDB
[revision 95cc92e](https://github.com/drawdb-io/drawdb/blob/95cc92ec0f35d30ad2d18eb8480b7ae6df780df8/src/utils/importSQL/sqlite.js)
and its locked `node-sql-parser` 5.4.0. The actual parser/importer reproduced all
48 tables, 390 columns and 126 foreign keys (165 ordered column pairs), including
composite model keys and the hierarchy self-reference. Column types, nullability,
primary-key membership and unique-column tuples were also compared with SQLite.

| Feature | Export and diagram behavior |
|---|---|
| Table order | Referenced tables precede dependents because drawDB resolves references in one pass. A future cross-table cycle stops generation instead of silently losing relationships. Self-references work. |
| Primary, unique and foreign keys | Preserved, including composite grouping. drawDB's inferred cardinality uses the first field's unique flag, so its one/many labels may misdescribe keys; inspect key tuples rather than treating labels as authoritative. |
| 45 table CHECK constraints | Retained verbatim as SQL comments, not diagram constraints. The importer ignores table CHECKs, and its parser rejects decimal `GLOB` expressions. These include boolean domains, exact-decimal text syntax, availability/effect/selection/scope domains, and default-rule condition shape. |
| 81 deferred foreign keys | Foreign-key endpoints remain; `DEFERRABLE INITIALLY DEFERRED` is removed from executable export SQL because the parser rejects it. The original declarations remain in comments. The diagram cannot express transaction-end validation timing. |
| STRICT | Retained in SQL and accepted by the parser, but not modeled in the diagram. Implicit primary-key NOT NULL is made explicit from SQLite metadata so diagram nullability is accurate. |
| 89 triggers | Full DDL retained as reference comments only. The 80 subtype INSERT/UPDATE guards enforce matching entity kind/model; 8 rule-endpoint guards restrict direct/group/member/price ends to offerings or model interiors; `entity_identity_immutable` rejects entity updates. None are represented by diagram edges. |

Importer/contract validation also enforces rules beyond DDL, such as source
coverage, complete availability and supported derivation permissions. A diagram
does not represent those algorithms or establish business-data correctness.
The generated SQL is deliberately unsuitable as a replacement schema or migration.

These checks cover the pinned upstream importer; the hosted editor may run a
different revision. Hosted menu controls were checked, but the browser file chooser
timed out, so hosted import/rendering remains unverified.
See the [drawDB guide](https://drawdb-io.github.io/docs/create-diagram)
for editor controls.
