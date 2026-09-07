"""Export model-specific candidate behavior records for review, not test coverage.

Read-only input. Keeps inactive and generator-suppressed records, ordered members,
scope tokens, source locations and resolved reference names. No rule deduplication.
"""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import sqlite3

from catalog.schema import TABLES


FAMILIES = (
    'direct_rule', 'group_rule', 'exclusive_group', 'price_rule', 'default_rule',
    'color_rule', 'derivation_permission', 'variant_override', 'offering_policy',
    'model_interior', 'interior_component', 'section', 'section_presentation',
)
CHILDREN = {
    'group_rule': ('group_member', 'group_id'),
    'exclusive_group': ('exclusive_member', 'group_id'),
}


def inventory(database):
    uri = Path(database).resolve().as_uri() + '?mode=ro'
    with sqlite3.connect(uri, uri=True) as db:
        db.row_factory = sqlite3.Row
        db.execute('BEGIN')
        tables = {t: [dict(r) for r in db.execute(f'SELECT * FROM {t} ORDER BY sequence,id')]
                  for t in TABLES}
        metadata = dict(db.execute('SELECT key,value FROM import_metadata'))
        evidence = defaultdict(list)
        for row in db.execute('SELECT entity_id,source_id FROM evidence_link ORDER BY source_id'):
            evidence[row['entity_id']].append(row['source_id'])
        code = [dict(r) for r in db.execute('SELECT * FROM code_evidence ORDER BY path,symbol')]
    by_id = {r['id']: (t, r) for t, rows in tables.items() for r in rows}
    models = {r['id']: r['model_key'] for r in tables['model']}
    names = {r['offering_id']: r['label'] for r in tables['offering_presentation']}
    names.update({r['id']: r['name'] for r in tables['interior_definition']})

    def identity(value):
        kind, row = by_id[value]
        return dict(kind=kind, model=models.get(row['model_id'], 'shared'),
                    key=row.get('legacy_id', row.get('section_key', value)),
                    name=names.get(value, names.get(row.get('definition_id'),
                         row.get('display_label', row.get('name')))))

    def record(kind, row):
        refs = {field: identity(row[field]) for item in TABLES[kind][0].split()
                for field, typ in [item.split(':')]
                if typ.startswith('@') and row[field] is not None}
        return dict(fields=row, references=refs, source_rows=evidence[row['id']])

    result = dict(status='Inventory only: behavioral scenarios not yet verified',
                  metadata=metadata, models={}, shared_sections=[], code_evidence=code)
    scopes = defaultdict(list)
    members = defaultdict(list)
    for r in tables['scope_member']:
        members[r['scope_id']].append(record('scope_member', r))
    for r in tables['scope_axis']:
        scopes[r['owner_id']].append(dict(**record('scope_axis', r), members=members[r['id']]))
    children = defaultdict(list)
    for _, (table, foreign_key) in CHILDREN.items():
        for r in tables[table]:
            children[r[foreign_key]].append(record(table, r))
    for mid, model in models.items():
        result['models'][model] = dict(variants=[record('variant', r) for r in tables['variant']
                                               if r['model_id'] == mid], families={})
        for family in FAMILIES:
            if family == 'section':
                continue
            rows = result['models'][model]['families'][family] = []
            for row in tables[family]:
                if row['model_id'] == mid:
                    rows.append(dict(**record(family, row), scopes=scopes[row['id']],
                                     members=children[row['id']]))
    result['shared_sections'] = [record('section', r) for r in tables['section']]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    if args.output.resolve() == args.database.resolve():
        parser.error('Output must not overwrite the source database')
    data = inventory(args.database)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main()
