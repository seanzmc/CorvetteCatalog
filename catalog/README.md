# Disposable relational baseline

Checkpoint B imports the frozen canonical workbook directly into a SQLite
candidate. It does not read runtime JSON, invoke 27vette code, generate Excel,
accept manufacturer changes, or change canonical authority. The workbook archive
and reference project remain unchanged.

Run from the repository root with Python 3.11+ (SQLite 3.37+ for STRICT tables)
and the existing `requirements.txt` environment:

```sh
python -m catalog.importer --output .local/checkpoint-b/catalog.sqlite
python -m unittest discover -s tests -v
```

The CLI verifies the archive and pinned workbook hashes, builds and validates a
temporary database, then publishes the completed file atomically. Repeating the
same import reuses an identical destination. A differing existing file is never
overwritten; choose a new disposable path for a changed importer/schema. Failed
imports leave no published database or temporary file. No dependencies beyond
the existing openpyxl and Python standard library were added.

## Candidate contract

The ordinary typed tables are declared in [schema.py](schema.py). Their scope is
one frozen baseline, not the future authoring/revision/release schema. `model`
has model/year grain in this candidate, and deliberately rejects another year
under the same model key; this importer accepts only the inspected workbook hash.
Global interior definitions preserve the source combination and stored price;
model applicability, prerequisites, presentation and components are separate.
No cross-model offering definitions are merged on matching labels or RPOs.

- UUID identities derive from the legacy namespace and natural identity, never
  sheet positions, source hashes, or RPO alone. `legacy_mapping` keeps consumer
  identifiers. Every entity has a checked typed subtype. Typed foreign keys and
  composite model keys constrain relationships and prevent cross-model joins.
- Offering definitions, codes, policy, presentation, price and availability are
  separate tables. All option/variant pairs survive, including unavailable ones.
  `sequence` preserves source order; authored display orders remain separate.
  Variant membership and master lifecycle/order are both retained.
- Prices are exact decimal TEXT, with null for unpriced and `"0"` for authored
  zero. Offering, conditional and component prices retain their bases and unknown
  currency. Variant `base_price` means baseline total; interior `stored_price`
  means the authored interior amount before R6X adjustments. Neither amount is
  recalculated during import.
- Direct rules, groups/members, exclusivity, conditional prices, defaults and
  color relationships have separate typed tables. Scope axes/members preserve
  exact tokens, including case. Blank/star normalization follows the inspected
  family; direct rules do not silently interpret `*` as unrestricted. Hierarchy
  arrays become nodes and ordered interior memberships.
- Source sheet headers and every nonempty row's cell value, Excel type and number
  format are evidence, linked to typed rows. The frozen workbook retains original
  package bytes. Runtime-facing notes and source labels also have typed columns.
  Historical phrase rules and the empty exception schema remain evidence, not executable
  fallback data.
  Consumers can read all product relations without opening source evidence JSON.
- `code_evidence` identifies pinned compatibility policies for D. The five Z06
  replacement permissions are typed rows. The remaining generator compatibility
  algorithms are now executed by `contracts.py`; browser algorithms stay in the
  pinned comparison consumer. Identity/subtype, scope and coverage validation
  runs before publishing; this module is not an authoring API for arbitrary writes.

## Reconciliation and inspected differences

The [import report](baseline-import-report.json) records all 77 sheets, 15,134
source rows, model counts, dispositions and code/source provenance. All 30,328
typed rows and 218,779 stored fields were compared with the values prepared from
the workbook. Independent tests additionally rejoin all six models' options,
prices, presentation, availability and direct/price-rule endpoints to the frozen
source, and compare source cells and interior hierarchy paths. SQLite integrity
and foreign-key checks pass; the full offering × variant relation has no gaps.

| Model | Variants | Offerings | Availability pairs | Model interiors |
|---|---:|---:|---:|---:|
| Stingray | 6 | 242 | 1,452 | 130 |
| Grand Sport | 6 | 241 | 1,446 | 132 |
| Grand Sport X | 6 | 239 | 1,434 | 132 |
| Z06 | 6 | 244 | 1,464 | 130 |
| ZR1 | 4 | 207 | 828 | 90 |
| ZR1X | 4 | 206 | 824 | 90 |

Three concrete mappings refine Checkpoint A without changing business values:

1. Conditional prices may use an interior as their condition, not just an
   offering. For example `price_rules!A32:H32` identifies an interior-triggered
   seatbelt price. The pinned generator's `inspection.py:build_draft_price_rules`
   explicitly accepts both endpoint types; targets remain offerings.
2. Z06/ZR1/ZR1X summary mappings refer to `standard_equipment`, which is absent
   from navigable `runtime_steps`. The pinned `runtime_metadata.py` identifies
   this as a bucket and supplies its label. Three nonnavigable rows retain those
   relationships without inventing new wizard steps.
3. Shared option assets expand only to models containing the target, retaining
   shared versus model-specific scope for the documented override precedence.
   Grand Sport X lacks one shared target. Shared color rows similarly expand
   only through registered model/interior membership; per-model exclusions are
   recorded as not applicable, never manufacturer removals.

The two Grand Sport offerings carrying `T0E` remain distinct. All 1,044 interior
component rate references resolve, including explicit universal-trim fallback.
No business corrections, removals or manufacturer acceptances were made.

Ten importer tests pass, including corrupt identities, missing availability,
wrong endpoint types, cross-model references, unmapped columns, repeat imports
and failed-import cleanup. The existing eleven brake-intake tests also pass.
Currency remains unconfirmed. Checkpoint D evidence follows below.

## Checkpoint D: direct form generation

`contracts.py` reads a single SQLite transaction and generates all six contracts
and their browser registry from typed relations. It does not open the workbook,
read source-evidence JSON, import the reference generator, or read saved contracts.
`parity.py` separately reads the frozen archive as the expected comparison.

```sh
python -m catalog.importer --output .local/checkpoint-d/catalog.sqlite
python -m catalog.contracts --database .local/checkpoint-d/catalog.sqlite \
  --output .local/checkpoint-d/generated
python -m catalog.parity --database .local/checkpoint-d/catalog.sqlite
python -m unittest discover -s tests -v
node tests/runtime_parity.mjs .local/checkpoint-d/generated/form-app/data.js
```

Use a new output directory for each generation; completed directories are never
intentionally overwritten. `--generated-at` optionally fixes the timestamp for
repeatable output. Generation opens the database read-only. The output is a
local candidate, not a deployment or a release-management API. Schema version 2
requires rebuilding B's disposable database at a new path; existing version 1
candidates are refused, not migrated in place.

The schema refinement retains contract-facing notes on interiors, direct/group/
price/default rules and summary sections, runtime-step source text and model
source labels. `scope_axis.all_token` preserves authored blank versus `*`, while
`scope_member.position` preserves token order. These are source-preserving
columns, not business corrections. All 77 sheets, 15,134 source rows, 30,328 typed
rows and 218,779 stored fields reconcile. No source row or product identity was
added, removed, merged or accepted from the manufacturer pilot.

The independently implemented algorithms were traced to reference commit
`4fe92a4f078370c478f18484cad31bdafe58ad43`:

- `inspection.py`: source-order choices, first-visible-variant fallback for
  unavailable variants, display behavior and standard-equipment projection.
- `runtime_metadata.py` and `contract.py`: steps/sections, explicit default
  display rules, context copy, model-specific asset precedence and summaries.
- `interiors.py` and `pricing.py`: definition ordering, model membership,
  component filtering, R6X seat-price delta, grouping and whole-dollar conversion.
- `rules.py` and `rule_derivation.py`: grouped-requirement suppression,
  same-section exclusion deactivation, includes closure and authored precedence.
  Only the five typed Z06 derivation permissions authorize derived replacements.
- `registry_promotion.py`: promoted model order, aliases, default and setup copy.

Generic legacy UI vocabulary (body display order, selection-mode labels and
nonnavigable bucket label) remains compatibility code. Legacy R6X/`requires_z25`
output flags remain compatible with the pinned consumer; this is not a redesign
of pricing policies or the future authoring schema.

The [parity report](form-parity-report.json) compares every business value, type
and array position. All six baseline business hashes match; the only excluded
contract path is `/dataset/generated_at`. The registry comparison also checks
model order, aliases and every setup/asset field. There are zero added, removed
or changed output facts. Eight generator tests additionally deny evidence-table
reads, mutate typed values, check model isolation, reject missing availability
and stale derivation permissions, and verify deterministic/failed publication.

The runtime test reads the frozen browser files and obtains only the DOM/fetch
stub harness from the pinned reference Git revision (optional third argument:
reference repository path). It runs baseline and candidate registries through
the same consumer and compares defaults, prices, disabled reasons, standard
summary, selections, interior components, reset, model switching, Markdown
content and dealer payloads. Submission time is fixed for that comparison;
network sends are never invoked. It is a differential parity test, not proof
that the original business policies are correct or exhaustive configuration
coverage. The final run passed 32 variant baseline states, 126 option transitions and 32
interior transitions in about 18 seconds. All 29 Python tests passed in 33 seconds.
The local Chromium check covered setup, coupe-to-convertible, 1LT-to-3LT,
standard-equipment counts and a priced paint selection. Missing logo/vehicle
artwork in the frozen archive produced four 404s; full artwork fidelity and live
dealer submission are outside this check. Details are in the parity report.
