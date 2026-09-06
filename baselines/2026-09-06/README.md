# Frozen workbook and runtime baseline

First bounded slice of Checkpoint B, captured September 6, 2026 UTC
(September 5 in America/New_York). This baseline preserves the existing form's
inputs and outputs for the disposable relational import. It does not establish
manufacturer accuracy or complete Checkpoint B.

`workbook-runtime.tar.gz` contains unchanged bytes from the clean 27vette commit
`4fe92a4f078370c478f18484cad31bdafe58ad43`: the canonical workbook, six runtime
contracts, four browser files, and the generator requirements. `manifest.json`
identifies every member by size and SHA-256, records regeneration results, and
hashes the archive itself. Keep this baseline immutable; a later source freeze
belongs in a new directory.

The workbook hash matches Checkpoint A. The original workbook package is retained
without opening/saving it, preserving cell types, formulas, formatting and source
locations. The compressed browser files are comparison evidence, not a deployed
application. Remote images, Turnstile and the dealer submission service are not
captured. Do not submit orders from an extracted reference form.

## Matching evidence

The reference generator was run from an isolated export of the pinned commit,
using Python 3.14.7 and its existing environment (requirements preserved in the
archive). All six generations reported zero validation errors and warnings.
Recursive comparisons checked every JSON value, type and list position. The only
changed field in each contract was `/dataset/generated_at`; original timestamps
and exact bytes remain in the archive. The manifest's business-content hashes
use UTF-8 JSON after removing only that field, with sorted object keys,
`ensure_ascii=False` and separators `(',', ':')`.

The registry generator, reading the captured contracts and workbook, reproduced
`form-app/data.js` byte for byte, including model order, aliases and defaults.
Archive members were read back and checked against their hashes. After generation,
all captured files still matched the reference checkout, which remained clean.

This is reproducibility evidence, not browser transition testing, production
verification, a row-by-row relational reconciliation, or proof that all business
policies live in the workbook. Those remain B/D work. No manufacturer input is
included and no source disagreements have been resolved.

## Reproduce the comparison

From this repository root, use an empty scratch directory. The pinned reference
commit must be available in the read-only 27vette repository. Use Python with the
versions in the archived requirements; do not install into or generate inside
27vette. The commands below use its already provisioned interpreter.

```sh
BASELINE="$PWD/baselines/2026-09-06"
SCRATCH=$(mktemp -d)
PYTHON=/Users/seandm/Projects/27vette/.venv/bin/python
export PYTHONDONTWRITEBYTECODE=1
git -C /Users/seandm/Projects/27vette archive \
  4fe92a4f078370c478f18484cad31bdafe58ad43 scripts | tar -x -C "$SCRATCH"
tar -xzf "$BASELINE/workbook-runtime.tar.gz" -C "$SCRATCH"
for model in stingray grand_sport grand_sport_x z06 zr1 zr1x; do
  "$PYTHON" "$SCRATCH/scripts/generate_form.py" --model "$model" \
    --workbook "$SCRATCH/stingray_master.xlsx" --output-root "$SCRATCH/regenerated"
done
"$PYTHON" "$SCRATCH/scripts/generate_registry.py" \
  --workbook "$SCRATCH/stingray_master.xlsx" --root "$SCRATCH" \
  --output "$SCRATCH/rebuilt-data.js"
cmp "$SCRATCH/form-app/data.js" "$SCRATCH/rebuilt-data.js"
"$PYTHON" - "$SCRATCH" "$BASELINE" <<'PY'
import hashlib, json, sys
from pathlib import Path
root, baseline = map(Path, sys.argv[1:])
manifest = json.loads((baseline / 'manifest.json').read_text())
digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
assert digest(baseline / manifest['archive']['path']) == manifest['archive']['sha256']
for member in manifest['files']:
    assert digest(root / member['path']) == member['sha256'], member['path']
for result in manifest['verification']['contracts']:
    name = result['model'].replace('_', '-') + '-runtime-contract.json'
    original = json.loads((root / 'form-output/runtime' / name).read_text())
    generated = json.loads((root / 'regenerated/form-output/runtime' / name).read_text())
    del original['dataset']['generated_at']
    del generated['dataset']['generated_at']
    canonical = lambda value: json.dumps(value, sort_keys=True, ensure_ascii=False,
                                        separators=(',', ':')).encode()
    assert canonical(original) == canonical(generated), name
    assert hashlib.sha256(canonical(original)).hexdigest() == result['business_content_sha256']
print('Archive, members, and all six contract comparisons passed.')
PY
```

## Next bounded task

Implement the disposable relational baseline importer against this frozen
workbook. Reconcile all source rows, conservative legacy identities and constrained
relationships against the Checkpoint A mapping, preserving intentional values and
source evidence. Physical schema choices and concrete mapping ambiguities must be
resolved from the specification and consumers before implementation. Full form
parity remains D; manufacturer intake remains separately authorized C work.
