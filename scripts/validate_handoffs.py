"""Validate every model lane's handoff files against docs/discovery/handoff-schema.json.

Usage: python scripts/validate_handoffs.py [--lane zr1 ...]

Checks each lane's records, owner-decisions, accounting and runtime JSON against the
schema, then the cross-file facts a schema cannot express: sheet roles resolve, one
offering target per disposition record, decision links resolve, hashes agree, and
the structured handoff carries the fixed section headings. Read-only; exits non-zero
with every violation listed. It does not judge business facts or reproduce probes.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / 'docs/discovery/handoff-schema.json'
TYPES = {'object': dict, 'array': list, 'string': str, 'integer': int, 'number': (int, float), 'boolean': bool, 'null': type(None)}


def check(schema, value, path, root, errors):
    """Minimal JSON Schema subset: type, const, enum, pattern, required, properties,
    additionalProperties, items, $ref (local). Enough for this contract; keep the
    schema inside this subset so external validators agree."""
    if '$ref' in schema:
        target = root
        for part in schema['$ref'].lstrip('#/').split('/'):
            target = target[part]
        return check(target, value, path, root, errors)
    if 'type' in schema:
        allowed = schema['type'] if isinstance(schema['type'], list) else [schema['type']]
        ok = any(isinstance(value, TYPES[t]) and not (t in ('integer', 'number') and isinstance(value, bool)) for t in allowed)
        if not ok:
            errors.append(f'{path}: expected {allowed}, got {type(value).__name__}')
            return
    if 'const' in schema and value != schema['const']:
        errors.append(f'{path}: expected {schema["const"]!r}, got {value!r}')
    if 'enum' in schema and value not in schema['enum']:
        errors.append(f'{path}: {value!r} not in {schema["enum"]}')
    if 'pattern' in schema and isinstance(value, str) and not re.search(schema['pattern'], value):
        errors.append(f'{path}: {value!r} does not match {schema["pattern"]}')
    if isinstance(value, dict):
        for key in schema.get('required', []):
            if key not in value:
                errors.append(f'{path}: missing required key {key!r}')
        props = schema.get('properties', {})
        extra = schema.get('additionalProperties', True)
        for key, item in value.items():
            if key in props:
                check(props[key], item, f'{path}.{key}', root, errors)
            elif extra is False:
                errors.append(f'{path}: unexpected key {key!r}')
            elif isinstance(extra, dict):
                check(extra, item, f'{path}.{key}', root, errors)
    if isinstance(value, list) and 'items' in schema:
        for index, item in enumerate(value):
            check(schema['items'], item, f'{path}[{index}]', root, errors)


def load(path):
    return json.loads((ROOT / path).read_text())


def validate_lane(lane, schema, errors):
    files = {kind: pattern.format(lane=lane) for kind, pattern in schema['lanes']['files'].items()}
    missing = [p for p in files.values() if not (ROOT / p).exists()]
    if missing:
        errors.extend(f'{lane}: missing {p}' for p in missing)
        return
    data = {kind: load(files[kind]) for kind in ('records', 'decisions', 'accounting', 'runtime')}
    exceptions = schema['lanes']['frozen_exceptions'].get(files['runtime'], {}).get('extra_top_level_keys', [])
    runtime = data['runtime']
    if isinstance(runtime, dict):
        runtime = {k: v for k, v in runtime.items() if k not in exceptions}
    structurally_valid = True
    for kind, value in (('records', data['records']), ('decisions', data['decisions']), ('accounting', data['accounting']), ('runtime', runtime)):
        local = []
        check(schema['$defs'][kind], value, files[kind], schema, local)
        errors.extend(local)
        if local:
            structurally_valid = False
    # Required-field accesses below depend on all four schema checks succeeding.
    # Return only from this lane so main still reports violations in later lanes.
    if not structurally_valid:
        return
    records, decisions, accounting, runtime = data['records'], data['decisions'], data['accounting'], data['runtime']
    review = decisions['owner_review']
    if not all(d['model_key'] == records['model_key'] for d in (decisions, accounting, runtime)):
        errors.append(f'{lane}: model_key differs across files')
    for role, sheet in records.get('sheet_roles', {}).items():
        if sheet not in records['baseline_rows']:
            errors.append(f'{files["records"]}: sheet_roles.{role} -> {sheet!r} is not a baseline_rows key')
    if decisions['source_records'] != Path(files['records']).name or decisions['runtime_evidence'] != files['runtime'].removeprefix('docs/') \
            or decisions['accounting_evidence'] != files['accounting'].removeprefix('docs/'):
        errors.append(f'{files["decisions"]}: evidence pointers do not name this lane\'s files')
    if not (records['sources']['guide_sha256'] == accounting['guide_sha256'] == runtime['provenance']['guide_sha256']):
        errors.append(f'{lane}: guide_sha256 differs across files')
    if records['sources']['workbook_sha256'] != runtime['provenance']['workbook_sha256']:
        errors.append(f'{lane}: workbook_sha256 differs between records and runtime')
    option_sheet = records['sheet_roles'].get('options')
    options = records['baseline_rows'].get(option_sheet, [])
    option_ids = {o['option_id'] for o in options}
    disposition_ids = [r['record_id'] for r in records['offering_dispositions']]
    if len(disposition_ids) != len(options):
        errors.append(f'{files["records"]}: {len(disposition_ids)} offering_dispositions for {len(options)} options')
    target_ids = [t['record_id'] for t in review['offering_targets']]
    if sorted(target_ids) != sorted(disposition_ids):
        errors.append(f'{files["decisions"]}: offering_targets must match offering_dispositions one-to-one')
    if len(set(target_ids)) != len(target_ids):
        errors.append(f'{files["decisions"]}: duplicate offering_targets record_id')
    decision_ids = [r['decision_id'] for r in review['records']]
    if len(set(decision_ids)) != len(decision_ids):
        errors.append(f'{files["decisions"]}: duplicate decision_id')
    for t in review['offering_targets']:
        for d in t['decision_ids']:
            if d not in decision_ids:
                errors.append(f'{files["decisions"]}: {t["record_id"]} links unknown decision {d}')
        if t['target_disposition'] != 'retain_subject_to_decision_overlay' and not t['decision_ids']:
            errors.append(f'{files["decisions"]}: {t["record_id"]} has a non-default target without a decision')
        if t['target_disposition'] == 'rename' and not t['target_name']:
            errors.append(f'{files["decisions"]}: {t["record_id"]} rename needs target_name')
    variant_ids = {v['variant_id'] for v in records['baseline_rows']['variant_master']}
    for a in review['accepted_additions']:
        if a['decision_id'] not in decision_ids:
            errors.append(f'{files["decisions"]}: addition {a["rpo"]} links unknown decision {a["decision_id"]}')
        if not set(a['configuration_ids']) <= variant_ids:
            errors.append(f'{files["decisions"]}: addition {a["rpo"]} names unknown configurations')
        if a['rpo'] not in {g['rpo'] for g in records['guide_only_dispositions'] if g['source_classification'] == 'omitted_offering'}:
            errors.append(f'{files["decisions"]}: addition {a["rpo"]} is not an omitted_offering in guide_only_dispositions')
    if {p['option_id'] for p in accounting['option_prices']} != option_ids:
        errors.append(f'{files["accounting"]}: option_prices do not cover exactly the option sheet')
    rule_sheet = records['sheet_roles'].get('rule_mapping')
    rule_rows = records['baseline_rows'].get(rule_sheet, [])
    translations = accounting['direct_rule_translation']
    if len(translations) != len(rule_rows):
        errors.append(f'{files["accounting"]}: direct_rule_translation count differs from {rule_sheet}')
    # Both lists retain workbook order, including filtered direct rules. Compare
    # provenance and endpoints, not runtime-derived or accepted target relations.
    fields = {'source_row': '_row', 'rule_id': 'rule_id', 'source_id': 'source_id',
              'rule_type': 'rule_type', 'target_id': 'target_id'}
    for index, (translation, source) in enumerate(zip(translations, rule_rows)):
        for field, source_field in fields.items():
            if source_field not in source or translation[field] != source[source_field]:
                errors.append(f'{files["accounting"]}: direct_rule_translation[{index}].{field} '
                              f'differs from {rule_sheet}[{index}].{source_field}')
    derived = records['runtime_derived_relationships']
    emitted = sum(1 for r in accounting['direct_rule_translation'] if r['runtime_disposition'] == 'emitted')
    if derived['workbook_direct_count'] != len(accounting['direct_rule_translation']) or derived['emitted_direct_count'] != emitted + len(derived['records']):
        errors.append(f'{files["records"]}: runtime_derived_relationships counts disagree with accounting')
    for name in ('foundations', 'seat_transitions', 'required_interior_rejection'):
        if len(runtime[name]) != len(variant_ids):
            errors.append(f'{files["runtime"]}: {name} has {len(runtime[name])} entries for {len(variant_ids)} configurations')
    active_pairs = {(o['option_id'], v) for o in options if o['active'] for v in variant_ids}
    observed = {(r['id'], r['variant_id']) for r in runtime['starting_choice_observations']}
    if lane != 'zr1' and observed != active_pairs:
        errors.append(f'{files["runtime"]}: starting_choice_observations differ from active option × configuration universe')
    if lane == 'zr1' and not observed <= active_pairs:
        # ZR1's probe observes the browser registry's eligible rows (inactive and hidden rows excluded); see zr1-structured.md.
        errors.append(f'{files["runtime"]}: starting_choice_observations outside the active universe')
    if lane == 'zr1' and observed != active_pairs:
        hidden = {(o['option_id'], v) for o in options if o['active'] and o.get('display_behavior') == 'hidden' for v in variant_ids}
        if observed != active_pairs - hidden:
            errors.append(f'{files["runtime"]}: starting_choice_observations differ from active, non-hidden option × configuration universe')
    policy = load('docs/compatibility-notice-policy.json')
    if records['model_key'] not in policy['model_overrides']:
        errors.append(f'{lane}: compatibility-notice-policy.json has no model_overrides entry for {records["model_key"]}')
    text = (ROOT / files['structured']).read_text()
    headings = [line[3:].strip() for line in text.splitlines() if line.startswith('## ')]
    if headings != schema['lanes']['structured_sections']:
        errors.append(f'{files["structured"]}: "## " headings must be exactly the ten contract sections; got {headings}')
    if not (ROOT / files['behavior']).read_text().startswith('# '):
        errors.append(f'{files["behavior"]}: missing title')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--lane', action='append', help='validate only this lane (repeatable)')
    args = parser.parse_args(argv)
    schema = json.loads(SCHEMA_PATH.read_text())
    lanes = args.lane or schema['lanes']['models']
    errors = []
    for lane in lanes:
        if lane not in schema['lanes']['models']:
            errors.append(f'{lane}: not listed in handoff-schema.json lanes.models')
            continue
        validate_lane(lane, schema, errors)
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        print(f'{len(errors)} handoff contract violation(s)', file=sys.stderr)
        return 1
    print(f'{len(lanes)} lane(s) conform to the handoff contract: {", ".join(lanes)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
