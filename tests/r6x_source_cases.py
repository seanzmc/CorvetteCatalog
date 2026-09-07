"""Independent frozen-workbook expectations for the bounded R6X review.

Run with Python/openpyxl, redirect stdout to a temporary JSON file, then pass
that file and a generated candidate data.js to r6x_review.mjs.
"""
import hashlib
import io
import json
from pathlib import Path
import tarfile

from openpyxl import load_workbook

baseline = Path(__file__).resolve().parents[1] / 'baselines/2026-09-06'
manifest = json.loads((baseline / 'manifest.json').read_text())
with tarfile.open(baseline / manifest['archive']['path']) as archive:
    raw = archive.extractfile('stingray_master.xlsx').read()
assert hashlib.sha256(raw).hexdigest() == next(
    f['sha256'] for f in manifest['files'] if f['path'] == 'stingray_master.xlsx')
workbook = load_workbook(io.BytesIO(raw), data_only=True)


def rows(sheet):
    values = list(workbook[sheet].values)
    return [dict(zip(values[0], row), source=f'{sheet}!{n}')
            for n, row in enumerate(values[1:], 2) if any(v is not None for v in row)]


def active(row):
    return row['active'] in (True, 'True')


def scope(value, actual):
    return value in (None, '', '*') or actual in str(value).split('|')


roles = {(r['model_key'], r['source_role']): r['sheet_name']
         for r in rows('model_workbook_sources') if active(r)}
registry_keys = {r['model_key']: r['registry_key'] for r in rows('model_registry_promotion') if active(r)}
variants = {r['variant_id']: r for r in rows('variant_master')}
memberships = rows('model_variants')
rates = rows('PriceRef')
r6x_rate = [r for r in rates if r['OptionType'] == 'R6X' and r['Code'] == 'R6X']
assert len(r6x_rate) == 1 and r6x_rate[0]['Price'] == 995
components = rows('interior_components')
cases = []
for membership in rows('model_interior_scope'):
    if not active(membership):
        continue
    model, key = membership['model_key'], membership['interior_id']
    source = {r['interior_id']: r for r in rows(roles[model, 'interior_source_sheet'])}[key]
    if source['requires_r6x'] not in (True, 'True'):
        continue
    owned_components = [r for r in components if r['model_key'] == model
                        and r['interior_id'] == key and active(r)]
    assert sum(r['rpo'] == 'R6X' for r in owned_components) == 1
    assert not any(r['component_type'] == 'seat' for r in owned_components)
    extras = []
    for component in owned_components:
        rate = [r for r in rates if str(r['OptionType']).lower() == component['price_ref_type'].replace('_', '')
                and r['Code'] == component['price_ref_code'] and r['Trim'] is None]
        assert len(rate) == 1, component
        extras.append(dict(rpo=component['rpo'], price=rate[0]['Price'],
                           source=[component['source'], rate[0]['source']]))
    assert source['Price'] == sum(r['price'] for r in extras if r['rpo'] != 'R6X')
    options = rows(roles[model, 'source_option_sheet'])
    seat = [r for r in options if r['rpo'] == source['Seat']]
    assert len(seat) == 1
    seat = seat[0]
    r6x = [r for r in options if r['rpo'] == 'R6X']
    assert len(r6x) == 1 and r6x[0]['price'] == r6x_rate[0]['Price']
    prices = rows(roles[model, 'price_rules_sheet'])
    for member in memberships:
        if member['model_key'] != model or not active(member):
            continue
        variant = variants[member['variant_id']]
        trim = str(variant['trim_level']).upper()
        if trim != membership['trim_level']:
            continue
        overrides = [r for r in prices if r['target_option_id'] == seat['option_id']
                     and r['condition_option_id'] == seat['option_id']
                     and r['price_rule_type'] == 'override'
                     and scope(r.get('body_style_scope'), variant['body_style'])
                     and scope(r.get('trim_level_scope'), trim)
                     and scope(r.get('variant_scope'), variant['variant_id'])]
        assert len(overrides) <= 1
        amount = overrides[0]['price_value'] if overrides else seat['price']
        cases.append(dict(model=model, interior_id=key, seat=source['Seat'],
                          seat_option_id=seat['option_id'], seat_price=amount,
                          variant_id=variant['variant_id'], trim=trim,
                          body=variant['body_style'], base_price=variant['base_price'],
                          expected_interior_components=extras,
                          expected_seat_and_interior=amount + source['Price'] + r6x_rate[0]['Price'],
                          source=[source['source'], membership['source'], seat['source'],
                                  r6x[0]['source'], member['source'], variant['source']]
                                 + [r['source'] for r in overrides]))
assert len(cases) == 180
assert len({(c['model'], c['interior_id']) for c in cases}) == 90
print(json.dumps(dict(workbook_sha256=hashlib.sha256(raw).hexdigest(), registry_keys=registry_keys, cases=cases), indent=2))
