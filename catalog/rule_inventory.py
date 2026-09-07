"""Export model-specific candidate behavior records for review, not test coverage.

Read-only input. Keeps inactive and generator-suppressed records, ordered members,
scope tokens, source locations and resolved reference names. No rule deduplication.
"""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import sqlite3

from catalog.schema import GLOBAL, TABLES


CHILDREN = {
    'group_rule': ('group_member', 'group_id'),
    'exclusive_group': ('exclusive_member', 'group_id'),
}
NESTED = {'variant', 'scope_axis', 'scope_member',
          *(table for table, _ in CHILDREN.values())}
FAMILIES = tuple(t for t in TABLES if t not in GLOBAL | NESTED)
RULE_FAMILIES = ('direct_rule', 'group_rule', 'exclusive_group', 'price_rule',
                 'default_rule', 'color_rule', 'derivation_permission')


def cross_model_matches(models):
    """Conservative comparison candidates, never shared business identities.

    Ignore workbook rule IDs, prose and physical row positions. Compare all
    other fields, endpoint kind/local key/RPO, explicit scopes and ordered
    members. Different member orders deliberately remain different patterns.
    """
    ignored = {'id', 'model_id', 'sequence', 'legacy_id', 'source_note', 'notes',
               'explanation', 'display_label', 'owner_id', 'scope_id', 'group_id'}

    def signature(record):
        fields = {k:v for k,v in record['fields'].items() if k not in ignored}
        for field, ref in record['references'].items():
            if field in fields:
                fields[field] = {k:ref[k] for k in ('kind', 'key', 'rpo')}
        return dict(fields=fields,
                    scopes=[signature(r) for r in sorted(record.get('scopes', []),
                                                        key=lambda r:r['fields']['axis'])],
                    members=[signature(r) for r in record.get('members', [])])

    groups = defaultdict(list)
    for model, data in models.items():
        for family in RULE_FAMILIES:
            for record in data['families'][family]:
                key = family, json.dumps(signature(record), sort_keys=True)
                groups[key].append(dict(model=model, id=record['fields']['id'],
                                        rule_id=record['fields'].get('legacy_id'),
                                        sequence=record['fields']['sequence'],
                                        source_rows=record['source_rows']))
    return [dict(family=family, pattern=json.loads(pattern), occurrences=occurrences)
            for (family, pattern), occurrences in sorted(groups.items())
            if len({r['model'] for r in occurrences}) > 1]


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
        sources = [dict(r) for r in db.execute('SELECT * FROM source_sheet ORDER BY ordinal')]
        dispositions = [dict(r) for r in db.execute('SELECT * FROM source_disposition ORDER BY source_id,model_key,disposition')]
    by_id = {r['id']: (t, r) for t, rows in tables.items() for r in rows}
    models = {r['id']: r['model_key'] for r in tables['model']}
    names = {r['id']: r['name'] for r in tables['option']}
    names.update({r['id']: r['name'] for r in tables['interior_definition']})

    def identity(value):
        kind, row = by_id[value]
        return dict(kind=kind, model=models.get(row['model_id'], 'shared'),
                    key=row.get('legacy_id', row.get('section_key', value)),
                    name=names.get(value, names.get(row.get('definition_id'),
                         row.get('display_label', row.get('name', row.get('label'))))),
                    id=value, rpo=row.get('rpo'))

    def record(kind, row):
        refs = {field: identity(row[field]) for item in TABLES[kind][0].split()
                for field, typ in [item.split(':')]
                if typ.startswith('@') and row[field] is not None}
        return dict(fields=row, references=refs, source_rows=evidence[row['id']])

    result = dict(status='Inventory only: behavioral scenarios not yet verified',
                  metadata=metadata, models={}, shared_sections=[], code_evidence=code,
                  source_sheets=sources, source_dispositions=dispositions,
                  record_counts={t:len(rows) for t, rows in tables.items()})
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
    for rows in children.values():
        rows.sort(key=lambda r: (r['fields']['display_order'] or 0,
                                 r['fields']['sequence'], r['fields']['id']))
    for mid, model in models.items():
        result['models'][model] = dict(model=record('model', by_id[mid][1]),
                                      variants=[record('variant', r) for r in tables['variant']
                                               if r['model_id'] == mid], families={})
        for family in FAMILIES:
            rows = result['models'][model]['families'][family] = []
            for row in tables[family]:
                if row['model_id'] == mid:
                    rows.append(dict(**record(family, row), scopes=scopes[row['id']],
                                     members=children[row['id']]))
    result['shared_sections'] = [record('section', r) for r in tables['section']]
    result['shared_component_rates'] = [record('component_rate', r)
                                        for r in tables['component_rate']]
    result['shared_interior_definitions'] = [record('interior_definition', r)
                                            for r in tables['interior_definition']]
    result['cross_model_matches'] = cross_model_matches(result['models'])
    result['cross_model_match_meaning'] = (
        'Comparison candidates only. Local endpoint keys are not proof of shared identity. '
        'Prose and sequence are omitted from matching but retained on source records. '
        'Availability, other interacting rules, price precedence and shared edit ownership '
        'must be reviewed before sharing a rule. Nonmatches may still have common parts.')
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
