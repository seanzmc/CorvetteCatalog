"""Verify retained discovery against immutable sources, not a corrected runtime.

Run with the existing openpyxl environment from the repository root.
This focused verifier protects the supplemental evidence and accounting added by
the catch-up; it does not certify exhaustive builds or replace human source review.
"""
import hashlib
import io
import json
from pathlib import Path
import tarfile

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((ROOT / path).read_text())
def digest(content):
    return hashlib.sha256(content).hexdigest()

manifest = read('baselines/2026-09-06/manifest.json')
archive_path = ROOT / 'baselines/2026-09-06' / manifest['archive']['path']
assert digest(archive_path.read_bytes()) == manifest['archive']['sha256']
with tarfile.open(archive_path) as archive:
    workbook_bytes = archive.extractfile('stingray_master.xlsx').read()
    frozen = load_workbook(io.BytesIO(workbook_bytes), data_only=True)
    guide_hash = read('docs/stingray-structured-records.json')['sources']['guide_sha256']
    raw = next((ROOT / 'sources/raw' / guide_hash).glob('*.xlsx'))
    assert digest(raw.read_bytes()) == guide_hash
    guide = load_workbook(raw, data_only=True)
    for model, option_sheet, rule_sheet in [
        ('stingray', 'stingray_options', 'rule_mapping'),
        ('grand-sport', 'grandSport_options', 'grandSport_rule_mapping'),
        ('grand-sport-x', 'grand_sport_x_options', 'grand_sport_x_rule_mapping'),
        ('z06', 'z06_options', 'z06_rule_mapping'),
    ]:
        handoff = read(f'docs/{model}-structured-records.json')
        accounting = read(f'docs/discovery/{model}-accounting.json')
        runtime = read(f'docs/discovery/{model}-runtime.json')
        baseline = handoff['baseline_rows']
        options = {r['option_id']: r for r in baseline[option_sheet]}
        assert accounting['guide_sha256'] == runtime['provenance']['guide_sha256'] == guide_hash
        assert digest(workbook_bytes) == runtime['provenance']['workbook_sha256'] == handoff['sources']['workbook_sha256']
        assert runtime['provenance']['probe_sha256'] == digest((ROOT / 'scripts/discovery_catchup.mjs').read_bytes())
        assert runtime['provenance']['reference_commit'] == manifest['reference_commit']
        for member in ('form-app/app.js', 'form-app/data.js'):
            assert runtime['provenance'][member] == digest(archive.extractfile(member).read())
        # No mutation or loss of the retained source row's types, nulls or columns.
        for sheet, rows in baseline.items():
            headers = [c.value for c in frozen[sheet][1]]
            for r in rows:
                values = [c.value for c in frozen[sheet][r['_row']]]
                expected = dict(_row=r['_row'], **{str(k): v for k, v in zip(headers, values) if k is not None})
                assert r == expected, (model, sheet, r['_row'])
        prices = accounting['option_prices']
        assert len(prices) == len(options)
        assert {r['option_id'] for r in prices} == set(options)
        for r in prices:
            o = options[r['option_id']]
            assert r['baseline_amount'] == o['price'] and r['rpo'] == o['rpo']
            candidates = []
            if o['rpo']:
                for row in guide['Price Schedule'].iter_rows(min_row=48):
                    if str(row[1].value).strip() == o['rpo']:
                        candidates.append({'anchor': f'Price Schedule!B{row[0].row}:E{row[0].row}', 'row': row[0].row,
                                           'description': row[2].value, 'qualifier': row[3].value, 'amount': row[4].value})
            assert r['source_rates'] == candidates, (model, o['rpo'])
            if r['classification'] == 'qualified_base_plus_discount':
                assert sum(x['amount'] for x in candidates) == o['price']
        translations = accounting['direct_rule_translation']
        assert len(translations) == len(baseline[rule_sheet])
        contract = json.load(archive.extractfile(f'form-output/runtime/{model}-runtime-contract.json'))
        for r, source in zip(translations, baseline[rule_sheet]):
            assert r['source_row'] == source['_row'] and r['rule_id'] == source['rule_id']
            assert r['runtime_rows'] == [x for x in contract['rules'] if all(x[k] == source[k] for k in ('source_id','rule_type','target_id'))]
            if not r['runtime_rows']:
                assert r['inactive_endpoints'] and all(not options[x]['active'] for x in r['inactive_endpoints'])
        # Exact active choice universe, including unavailable/display-only rows.
        # The frozen browser registry retains charge-only choices that the standalone
        # contract marks inactive (e.g. R6X). Check the complete active workbook
        # offering universe against the actual registry consumer, not that flag.
        expected_pairs = {(o['option_id'], v['variant_id']) for o in options.values() if o['active']
                          for v in baseline['variant_master']}
        observed = runtime['starting_choice_observations']
        assert {(r['id'], r['variant_id']) for r in observed} == expected_pairs
        assert len(observed) == len(expected_pairs)
        assert runtime['live_requests'] == 0
        assert len(runtime['foundations']) == len(runtime['seat_transitions']) == len(runtime['required_interior_rejection']) == 6
        assert all(r['requests'] == 0 and 'Interior Color' in r['missing'] for r in runtime['required_interior_rejection'])
        stripe_cases = [s for s in runtime['connected_sequences'] if s['name'] == 'stripe/paint prohibition']
        assert len(stripe_cases) == 60
        for case in stripe_cases:
            assert all(a['action']['outcome'] == 'attempted' for a in case['states']) if model == 'z06' else case['states'][1]['action']['outcome'] == 'not_selectable'
        for case in runtime['connected_sequences']:
            assert not case['initial']['missing'], (model, case['id'])
            assert case['source_anchors'], (model, case['id'])
            for step in case['states']:
                s = step['state']
                assert s['total'] == s['order']['pricing']['total_msrp']
                assert step['action']['outcome'] != 'absent_from_active_model'
        if model == 'stingray':
            retained = accounting['retained_original_supplemental']
            assert len(retained['interior_body_contexts']) == 260
            assert len(retained['starting_option_observations']) == 1416
            assert [len(retained['combinations'][k]) for k in ('priceResults','paintResults','beltResults')] == [130,1300,780]
        print(f'{model}: frozen rows, all option rates/qualifiers, direct translations, {len(observed)} runtime choices, {len(runtime["connected_sequences"])} connected cases and rejection evidence verified')
