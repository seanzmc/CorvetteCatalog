# Disposable relational baseline

## Disposable master-schema foundation

The September 15 foundation implements the bounded structural slice in
[proposal §9](../docs/master-schema-proposal.md#9-review-outcome-and-next-bounded-work),
using the [O1–O4/O6–O7 resolutions](../docs/master-schema-worked-examples.md#open).
It is independent of the historical importer below. Run from the repository root
with Python's standard library; no new dependencies:

```sh
python3 -m catalog.foundation
python3 -m unittest discover -s tests -p test_foundation.py -v
```

The command creates or reuses `.local/foundation/catalog.sqlite`. Every foundation
connection goes through `catalog.foundation.connect`, which enables and verifies
`PRAGMA foreign_keys=ON`. Tests exercise initial and reopened file connections.
The historical `catalog.schema` path is unchanged.

**Implemented structure:** model/year and draft-only revisions; all 18 separate
typed identity/version pairs; structural endpoints and ordinary uniqueness;
eight rule/content scope junctions plus direct option/interior applicability;
condition clauses/members and explicit choice-group membership; documents,
anchors, evidence, decision-version membership and dispositions. Every version
references both its complete revision/model-year owner and its complete typed
model-year/identity key. RPO is not unique.

**Sample:** each of the six `docs/*-structured-records.json` files contributes its
own `opt_uvb_001` (UVB, HD Rear Vision Camera), all its actual `variant_master`
configurations and every UVB availability row: 6/6/6/6/4/4 for
ST/GS/GSX/Z06/ZR1/ZR1X. UVB is standard in each lane's base trim and unavailable
in the higher trims. Six model-owned options and 32 configuration/status pairs
retain their IDs and values. Matching source IDs do not create global sharing.
No source price is copied, and unavailable rows are retained.

The UVB command populates three revision-owned translation families:
`configuration_translation`, `option_translation` and
`option_configuration_translation`. The last retains **both** target IDs; each
link references the full revision/anchor/fragment disposition key. The documents
are tracked handoff JSON files hashed from their actual bytes; locators preserve
`baseline_rows/<sheet>/_row=<Excel row>`. These are not raw-workbook hashes.
Global UUIDs are allocated once and retrieved by declared natural keys; source
IDs remain in identity/version/translation rows. Re-import checks existing facts
and reuses immutable evidence membership. Changed source hashes are rejected,
not refreshed. The entire six-lane import is atomic.

**Enforcement:** `foundation_schema.statements()` emits standard `CREATE TABLE`,
explicit non-null primary keys, composite FKs, `UNIQUE` and `CHECK`. No rowid-based
keys, triggers, generated IDs or engine-specific DDL clauses. Only SQLite has
been executed; PRAGMAs and initial database detection are SQLite adapter code.
`foundation.validate` checks FK integrity, nonempty evidence/decision containers,
parent revision order, all 18 families' same-model/earlier-year predecessors and
group-scope containment for every implemented condition consumer (both requirement
conditions and every clause/group). Empty scope means nowhere. Cross-row rules
run before import commits and must run inside future write transactions; raw SQL
can bypass Python validation. No authoring/write service is supplied here.

**Boundary:** this command remains a structural UVB sample. The shared DDL now
also supports the bounded source slice below. Draft payload columns can remain
null in structural fixtures; `evaluator_sources.validate_sources` requires the
populated slice's prices and policies. Presentation, visual bindings, consumer
exports, general editing, freeze and release operations remain unimplemented.

Sixteen foundation tests reconcile sample fields/locators and check typed keys,
FK enforcement, predecessor rules, provenance, group scopes and atomic re-import.
These are structural checks, not corrected-runtime or release proof.

## Evaluator case source population — step 3

The September 16 source slice populates the inputs for
[E01–E08](../docs/master-schema-worked-examples.md#first-evaluator-slice--evidence-derived-acceptance-targets).
Run from the repository root using the standard library:

```sh
python3 -m catalog.evaluator_sources
python3 -m unittest discover -s tests -p test_evaluator_sources.py -v
```

This creates/reuses **`.local/foundation/evaluator-sources.sqlite`** through the
same FK-enforcing connection factory. It leaves the earlier foundation file and
historical baseline candidate untouched. There is no automatic schema migration:
use a fresh disposable file when changing DDL or pinned inputs. Changed input
hashes or recorded facts are rejected rather than silently refreshed. The complete
import, including the underlying foundation and new allocations, is one transaction.

### Translated coverage and source reconciliation

| Cases | Populated facts and accepted interpretations |
|---|---|
| E01–E02 / ST | UQT standard roots in the four source override configurations and context-reset policy; PCX's four retained inclusion IDs and zero rates, absorbing ownership, PCX/5DO conflict and purchase-transfer actions. Independent QE6 keeps its own 1,095 amount. |
| E03–E04 / GS | DMX AND ANY of five exact paints, convertible-only D84 acquisition and continuing requirement; 97A/Z15 and DMX/Z15 validity; both EL9 leaves with typed seat ownership, 3LT eligibility, Z25/3F9 acquisition and requirements. GS-D05 assigns source leaf 1,995 to Z25 instead of its frozen zero; AE4 uses its 595 3LT source rate; 3F9's Z25 rate is zero. No residual/component charge. |
| E05 / GSX | FED/XFR source inclusion, explicit no-separate-charge XFR, XFT substitution and standard J57/B4Z/FE5/LS6/XFT roots. |
| E06 / Z06 | PDB/PDD/Z07/T0F inclusions, carbon-wheel source groups including STZ, explicit wheel membership and requirements, J57/J6D corrected default, PDB/Z07 conflict and PDD purchase transfer, contextual package/wheel/R8E rates, standard roots and equipment substitutions. The J6D soft default excludes PDB's locked acquisition scope; the Z07/T0F soft default excludes PDD's locked cause. |
| E07–E08 / ZR1 and ZR1X | Each lane's ZTK children and TOM requirement, preserve-prior intent, separate R8E defaults, standard roots and equipment substitutions. Restored FE8/FEH lifecycle is decision-linked; TOM stays 12,995, with distinct retained IDs. Local ZTK prices remain 5,995 versus 1,500. |

The projection contains 32 configurations, 72 options (including the six original
UVB samples), two interiors, 55 acquisitions, 11 requirements and 29 rates.
These counts describe scope, not proof of parity. The recipes explicitly select
source rows; they do not import every rule attached to every referenced option.
Supplemental PDB wheel membership, STZ rates, Z07→T0F and T0F→CFZ preserve the
selected groups and reverse/request-transfer context without requiring the full
catalog. Covers, alternative aero/package families, CBF expansion, other interiors
and full 54-state Z06 coverage remain outside this projection.

**Money:** `starting_amount_minor`, `purchase_amount_minor` and `amount_minor`
are exact nonnegative integer cents, with a `basis_id` FK. The two immutable USD
bases distinguish vehicle price including destination once from option purchase
price. Null and zero differ. `charge_mode=no_separate_charge` is a finite,
evidenced equipment/hash classification; an unexpected null purchase rate fails.
Acquisition does not imply a zero charge. No floating-point price calculation is
used. SQL checks reject fractional/negative amounts and unmatched amount/basis
pairs; Python validation also checks the basis meaning for each owner.

**Rules and ownership:** typed clauses/members preserve AND, ANY and absence
conditions. Coexisting CFZ and belt acquisition causes have distinct priorities;
both remain supported causes. Acquisitions carry origin, peer policy, intent policy and priority;
requirements carry source state and loss policy. Replacement actions distinguish
remove from add/`commit_purchase`, including Z07 request → PDD purchase transfer.
The revision interaction policy encodes the approved notice/confirm/cancel,
direct dependency removal and whole-state revert semantics. Configurations carry
reset and required-interior policies. These are inputs, not executed transitions.

**Provenance:** all newly populated revision-owned families, including singleton
policies and composite scope/member/action rows, have concrete translation tables
with complete target FKs. Source IDs remain unchanged. New typed identities use
UUIDs allocated once via source-fragment translation links; `ex:` aliases are not
stored as identities. Hashed source documents include the six handoffs, accepted
lane overlays, common policy and worked design. Evidence sets are immutable;
decision sets link accepted lane decisions and both shared-policy decisions at
explicit version 1. Original frozen observations and source documents are unchanged.

**Validation:** source tests independently compare IDs, applicability, exact
amounts, price owners, conditions/scopes, ownership, request transfer and equipment
substitution. They exercise reopened-file re-import equality, late-failure rollback,
typed composite FK rejection, missing prices, money constraints, decision evidence
and the real Z06 group-scope subset. The foundation tests retain cross-model/year
and predecessor checks. All use fresh disposable databases.

**Not implemented:** the evaluator, transition/cancel/revert execution, charge
resolution, convergence and semantic overlap validation, UI, exports, publication
or canonical cutover. The UVB-only structural rows remain unpriced and unused by
the cases. This subset is not a selectable full catalog or a release candidate;
passing source tests does not prove E01–E08's runtime totals or behavior.

## Historical baseline implementation

**Historical implementation reference.** Current work is
the separate foundation above, not extending this candidate or cutting over from
the workbook. Preserve this implementation as evidence.

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
Options are owned by their model; matching labels or RPOs do not merge identities.

- UUID identities derive from the legacy namespace and natural identity, never
  sheet positions, source hashes, or RPO alone. `legacy_mapping` keeps consumer
  identifiers. Every entity has a checked typed subtype. Typed foreign keys and
  composite model keys constrain relationships and prevent cross-model joins.
- One `option` row owns identity, RPO, name/description, base price, placement and
  selection flags. Availability and variant overrides remain separate relations.
  All option/variant pairs survive, including unavailable ones.
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
source rows, model counts, dispositions and code/source provenance. All 23,588
typed rows and 189,371 stored fields were compared with the values prepared from
the workbook. Independent tests additionally compare all six models' options,
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

Twelve importer tests pass, including corrupt identities, missing availability,
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
local candidate, not a deployment or a release-management API. Current schema
version 3 requires a fresh database path; version 1/2 candidates are refused,
not migrated in place. The schema-3 example below uses a separate path.

The original schema-2 refinement retained contract-facing notes on interiors, direct/group/
price/default rules and summary sections, runtime-step source text and model
source labels. `scope_axis.all_token` preserves authored blank versus `*`, while
`scope_member.position` preserves token order. These are source-preserving
columns, not business corrections. At that checkpoint, all 77 sheets, 15,134 source rows, 30,328 typed
rows and 218,779 stored fields reconciled. No source row or product identity was
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
or changed output facts. Eleven generator tests additionally deny evidence-table
reads, mutate typed values, check model isolation, reject missing availability
and stale or unsupported derivation permissions, and verify deterministic/failed
publication including refusal of dangling symlinks at both output checks.

The runtime test reads the frozen browser files and obtains only the DOM/fetch
stub harness from the pinned reference Git revision (optional third argument:
reference repository path). It runs baseline and candidate registries through
the same consumer and compares defaults, prices, disabled reasons, standard
summary, selections, interior components, reset, model switching, Markdown
content and dealer payloads. Submission time is fixed for that comparison;
network sends are never invoked. It is a differential parity test, not proof
that the original business policies are correct or exhaustive configuration
coverage. The initial implementation (`3a42fe9`) passed 32 variant baseline states, 126
option transitions and 32 interior transitions in about 18 seconds, plus all 29
Python tests in 33 seconds. After the review fixes, all 11 contract tests pass
in 5.3 seconds, including exact six-model/registry parity and the new permission
and symlink regressions. The unchanged importer/intake, runtime and browser
checks were not repeated; the report retains their original commit attribution.
The local Chromium check covered setup, coupe-to-convertible, 1LT-to-3LT,
standard-equipment counts and a priced paint selection. Missing logo/vehicle
artwork in the frozen archive produced four 404s; full artwork fidelity and live
dealer submission are outside this check. Details are in the parity report.

## Option consolidation (schema 3)

The implemented [blueprint option slice](../docs/workbook-translation-blueprint.md)
replaces six tables with `option`, unique on `(model_id, legacy_id)`. The former
8,119 option-related rows become 1,379 rows; the candidate now has 43 tables.
`rpo` remains nullable/nonunique. `base_price` is exact decimal text, with null
distinct from zero; `price_basis`, unknown `currency` and `rpo_role` preserve
the old price/code semantics. Nullable display fields retain their original values.

All typed option references now target `option` with composite model constraints;
reference columns formerly named `offering_id` are named `option_id`, including
the corresponding interior/default-rule columns. Rule endpoint guards accept
`option` or `model_interior`. The rule inventory emits an `option` family with
the full row instead of `offering_policy`. Consumer-facing workbook IDs remain
unchanged; internal UUIDs and legacy-mapping kinds change from `offering` to
`option`. Rebuild disposable databases and inventories; no compatibility views
or in-place migration are provided.

```sh
python -m catalog.importer --output .local/options-v3/catalog.sqlite
python -m catalog.contracts --database .local/options-v3/catalog.sqlite --output .local/options-v3/generated
python -m catalog.parity --database .local/options-v3/catalog.sqlite
node tests/runtime_parity.mjs .local/options-v3/generated/form-app/data.js
```

Validation: all 1,379 options reconciled field by field with the previous six-table
representation, including identical definition/presentation copy. Every other
table reconciled after translating internal option references and consolidating
duplicate evidence links. All 15,134 original source rows, 7,448 availability
pairs, 16 variant overrides, rule memberships, price amounts/bases, nulls, order,
assets, source dispositions and code provenance remain intact. There are no added,
changed or removed business facts; currency remains unresolved.

All 41 Python tests pass, including source reconciliation, identity/reference
constraints, direct six-model contract/registry parity, inventory names and
schema-derived diagram comparison. Runtime parity passes all 32 variants,
126 option transitions and 32 interior transitions against the frozen browser.
This preserves the known R6X/AE4 undercharge; structural parity does not repair
or approve that pricing behavior. The earlier visual-browser check was not rerun:
the browser code and generated business content are unchanged. No production
system or reference-project files were modified.
