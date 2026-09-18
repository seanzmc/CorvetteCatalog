# Disposable relational baseline

The current executable draft is [full behavior translation](#full-behavior-translation).
The foundation, eight-case and offering-only importers remain separate regression
projections; the historical baseline importer remains unchanged.

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
python3 -m catalog.evaluator_sources --cases
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

**Boundary:** source checks alone do not prove runtime behavior. The evaluator
below executes the selected targets. The UVB-only structural rows remain unpriced
and unused by the cases. This subset is not a selectable full catalog or a release
candidate; full semantic overlap/release validation remains deferred.

## Bounded evaluator — step 4

`catalog.evaluator` reads one revision from the step 3 SQLite database into a
snapshot. It executes the independently authored E01–E08 targets in
`tests/test_evaluator.py`; it never imports product rules from Python lane recipes
or writes to the catalog. No new schema or dependencies are required.

```sh
python3 -m unittest discover -s tests -p test_evaluator.py -v
```

Example using the existing disposable source database:

```python
from contextlib import closing
from catalog.foundation import connect
from catalog.evaluator import Evaluator, Session

with closing(connect('.local/foundation/evaluator-sources.sqlite')) as db:
    revision = db.execute("""SELECT revision_id FROM catalog_revision
        JOIN model_year USING (model_year_id) JOIN model USING (model_id)
        WHERE model_key = 'stingray' AND revision_number = 1""").fetchone()[0]
    session = Session(Evaluator(db, revision), '2lt_c07')

session.confirm(session.preview('select', 'opt_pcx_001'))
preview = session.preview('select', 'opt_5do_001')
# preview.before and session.state are unchanged until confirmation.
# preview.candidate contains exact charges, retained intent and all live causes.
session.cancel()                    # discard the preview
session.confirm(session.preview('select', 'opt_5do_001'))
session.revert()                    # restore the whole PCX state
```

**State and transactions:** frozen states expose the revision/configuration,
ordered independent purchase intent, chosen interior, rooted causes, resolved
selections, static standard equipment, installed equipment, exact charge lines
and completeness issues. Removing intent preserves the acquisition order of
survivors. Causes name the source acquisition/part and supporting live roots.
Preview reports additions, removals, removed intent and interior changes alongside
both complete states. Confirm accepts only that session's current preview; cancel,
failed requests and stale previews cannot change committed state. Revert restores
the immediately preceding committed state once, including ownership and charges.

Actions are `select`/`remove` with retained option IDs, `interior` with an eligible
leaf ID (or `None` to clear), and `configure` with a same-revision configuration
ID. Configuration changes clear intent/interior according to the stored policy.
A different model/revision requires a fresh evaluator/session; no intent crosses
that boundary. Clicking a locked supplied child adds no independent purchase.
Customer-removable dependencies follow the accepted whole-removal policy, while
standard-only and mandatory configuration equipment remain protected.

**Evaluation:** rooted acquisition closure evaluates typed AND/ANY/absence
conditions and scoped groups. Explicit group peers suppress soft defaults;
competing defaults need distinct priorities, and multiple compatible causes for
one target remain visible. Requirements and bidirectional conflicts are reconciled
before pricing. Named replacement actions transfer Z07's request to independent
PDD; direct D84 removal removes DMX without changing paint. Absorbing ST package
intent is applied on transitions; preserved TOM intent survives ZTK-only removal.
Repeated states, iteration exhaustion, conflicting ownership policies, ambiguous
defaults/replacements and missing rates fail with `EvaluationError`.

**Pricing and projections:** charge owners are configuration or option IDs with
basis and selected rate IDs. Amounts are exact integer USD cents. First applicable
rate priority wins, with the option amount as fallback. Standard-only causes do
not charge; known zero creates a zero line; explicit `no_separate_charge` creates
no line. TOM remains paid when acquired, and the EL9 seat charges once. Equipment
substitutions suppress installed equipment without altering static trim facts or
creating purchases. The evaluator consumes the existing typed provenance links;
it does not emit presentation, order codes or visualizer manifests.

**Validation:** 18 evaluator tests cover all eight sequences with literal source
IDs, independent charge-owner/amount expectations, ownership/cause assertions,
installed output, scoped conditions, reverse conflict order and cancel/revert.
Source parity remains the separate 13-test source reconciliation suite. Synthetic
invalid-input tests prove ambiguity, nonconvergence, rootless-cycle, missing-price,
scope and stale-preview guards; they are not accepted business fixtures. Row-order
and repeated-evaluation checks prove deterministic results and no catalog writes.

**Limits:** every state carries `partial_catalog_not_submission_ready`; missing
required interior is reported separately. These are context totals, not complete
quotes. Paint/completeness rules and option relationships outside this selected
closure are not translated. No full-catalog validity, generic authoring/release
validator, UI, export, deployment or canonical-data change is implemented.

## Complete offering population

`import_catalog` in `catalog/evaluator_sources.py` expands the offering data
across all six lanes. `import_cases` preserves the original E01–E08 fixture.

```sh
python3 -m catalog.evaluator_sources
python3 -m catalog.evaluator_sources --database .local/foundation/fresh-offerings.sqlite
python3 -m unittest tests.test_catalog_offerings tests.test_evaluator_sources tests.test_evaluator tests.test_foundation
```

The default destination is **`.local/foundation/catalog-offerings.sqlite`**.
Use a fresh file for changed schema or translation recipes; existing matching
imports can be reopened. There is no in-place migration of earlier drafts.

| Lane | Source options | Accepted additions | Interior leaves | Applicability pairs | Source contextual rates |
|---|---:|---:|---:|---:|---:|
| Stingray | 242 | 2 | 130 | 1,464 | 52 |
| Grand Sport | 241 | 2 | 132 | 1,458 | 55 |
| Grand Sport X | 239 | 1 | 132 | 1,440 | 51 |
| Z06 | 244 | 2 | 130 | 1,476 | 72 |
| ZR1 | 207 | 1 | 90 | 832 | 34 |
| ZR1X | 206 | 1 | 90 | 828 | 33 |
| Total | 1,379 | 9 | 704 | 7,498 | 297 |

**Source and accepted target:** every source option identity survives, including
uncoded equipment, retired DUW and the retired GS T0E duplicate. Nine additions
use persisted UUIDs linked to accepted-addition records: DTC in ST/GS/Z06 and SAI
in every lane. GSX/ZR1/ZR1X retain their existing DTC identities. Applicable
factory-unavailable offerings cannot acquire or charge; missing disabled prices
remain unknown, never zero. Accepted standard-equipment restorations retain their
original applicability matrices. DUE uses Royal Blue in the five lanes with that
accepted correction. GS/GSX Z25 carries the accepted 1,995 content price.

Null-price equipment and GS/GSX hash marks have explicit no-separate-charge
classifications; an unexpected active purchase-price omission fails the import.
All 297 source rates retain their IDs, targets, amounts, typed option/interior
conditions and body/trim scopes. Existing case precedence comes first, followed
by remaining workbook row order. This draft ordering does **not** establish
general overlap correctness; that remains a semantic validation boundary.
Three decision-linked rates add the accepted SC7-at-zero-with-SBT correction in
Z06/ZR1/ZR1X, bringing the populated rate total to 300. The other three lanes
already have that source rate. All six preserve the standalone pouch charge.

**Interior ownership:** typed `interior_part` and `component_rate` relations add
700 non-seat parts, 33 model-owned components and 112 configuration-qualified
component rates. Every leaf owns its seat through one FK, even where the source
component list omitted AE4. R6X is an option-backed part; suede, stitching and
two-tone extras have independent exact rates. Source interior inclusion rows
supply belts and GS launch-edition content; GSX-D02 supplies the missing GSX Z25
acquisition. No stored interior total, residual, combined seat/R6X rate, or duplicate
seat line is executed. The four defective AE4/R6X paths now contribute 1,590,
2,085, 2,780 and 2,285 in LT lanes; LZ equivalents are 1,590, 2,085, 2,980 and
2,485. Frozen defect evidence is unchanged.

The evaluator reads these part/rate relations and source configuration-specific
selectability overrides. E01–E08 still execute with their original expected
charge lines in both the case fixture and the complete offering population.

**Validation and boundary:** independent tests reconcile all option IDs, names,
lifecycle, default amounts and matrices; all contextual rate endpoints, amounts
and scopes; and all interior seats, parts and extra rates. Every interior is
priced in each permitted configuration, with explicit corrected-charge tests
across six lanes. Reopened-file re-import preserves every allocation and row;
changed pinned input is rejected and a late failure rolls back the entire import.
Typed FK/monetary checks and full provenance validation remain in force.

This completes **offering data**, not all catalog behavior. General acquisitions,
requirements, defaults, choice groups, conflicts, substitutions and replacement
policies still use the bounded case recipes; other accepted behavior corrections
(including new-offering conflicts, lifecycle-dependent package behavior, and
full GS/GSX hash/roof rules) remain to be translated and tested. Presentation,
disclosures, navigation, visual bindings and exports are not populated consumers.
Every evaluator state retains `partial_catalog_not_submission_ready`. Complete
offering counts and interior pricing are not complete quote, semantic-overlap,
release, UI or cutover proof. No frozen evidence or canonical workbook changed.

## Full behavior translation

`catalog.behavior_sources` builds a fresh, separate behavior projection from the
six retained handoffs and accepted decision overlays. It uses the same typed
schema and evaluator, without invoking 27vette or reconstructing a workbook.

```sh
python3 -m catalog.behavior_sources
python3 -m unittest tests.test_behavior_sources tests.test_evaluator tests.test_catalog_offerings tests.test_evaluator_sources tests.test_foundation
```

The destination is `.local/foundation/catalog-behavior.sqlite`. Use a fresh path
when changing schema or translation recipes. Matching imports reuse all rows and
IDs; a case/offering database cannot be extended into this projection. Import
and allocation are one transaction, including the last model lane.

**Translated behavior:** all 3,770 direct/group/member/exclusive/default/color
source rows receive an individual, reasoned disposition: 3,716 translated,
10 superseded and 44 inactive/retired. Typed translation links retain original
anchors. Requires-any groups supersede redundant direct requirements; ordinary
requires never automatically purchases the prerequisite. Configuration-qualified
section choices become explicit group/member data. Evaluation does not read
section IDs. Defaults yield to explicit, interior and supplied choices, and
conflicting purchases reach one preview before confirmation. Unsupported requests
fail without committing a state.

| Lane | Accepted behavior implemented beyond the offering projection |
|---|---|
| Stingray | Full Z51/FE4 equipment and prerequisite cleanup; 5ZU/5ZZ suppress T0A without adding ZF1; TVS+Z51 acquires ZF1; RNX exception; body-qualified covers; PCX ownership, replaceable PDV caps; DTC and SAI conflicts |
| Grand Sport | FEB/FEY/J57 AND/OR prerequisites; conditional B4Z applicability/acquisition; gray-caliper acquisition and restoration; six hash acquisitions and all 17 conditional roof pairs; EL9 locking; full graphics conflicts |
| Grand Sport X | Its own standard J57/B4Z/FE5 and FED tire substitution; retire the two LS6 edges; retain ZZ3 and coupe-lighting paths; EL9/Z25, hash/roof and graphics corrections using GSX identities |
| Z06 | All nine package/wheel prices in six configurations; compatible caliper upgrades; complete PCZ child ownership/zero rates; 5DH/5DK exclusions; all 15 stripe/paint pairs; RXI/SLN; five pinned CBF fragments; PDB/Z07 request transfer to PDD |
| ZR1 | Model-specific ZTK/TOM ownership and equipment; corrected CFC paint direction and EFR content scope; standard restorations; complete DTC graphic conflicts; retained 3,000 R8E |
| ZR1X | Its own J59/FEH/FEZ, 2,600 R8E and 14,495 ZTK+TOM; CFC/DTC/DUW corrections; independent children and displaced-cover ownership, without importing ZR1 prices |

Every lane retains complete interior parts/prices, conditional D30 causes with
one charge owner, SBT's zero-priced included pouch, factory-unavailable states,
and notice/confirm/cancel/whole-state revert. GS B4Z changes from unconditional
standard to available with an explicit FEB/FEY requirement under GS-D08; the
offering-only importer and frozen matrix keep the original observation.

Source includes share one priority tier. Supplied choices precede configuration
defaults; conditional soft defaults retain their authored priorities. Complete
behavior rates use stable identity ordering, not workbook row order as business
precedence: differing amounts have disjoint configurations or mutually exclusive
wheel conditions; equal amounts do not create a second charge. Tests check this
specific rate property; it does not replace whole-revision overlap validation.

Z06 CBF uses one plan covering all live incompatible package/aero/ground-effect
causes. Absent removal endpoints are inert. The preview discloses the actual
complete removal set, including independently retained roots, and adds CBF once.
This prevents three competing plans for one PDD→Z07→T0F chain. Each of the five
frozen fragments and the pinned runtime revision retains provenance.

`State.content` contains typed supplied-content effects alongside `installed`:
roof-stripe omission, applicable WKR high-wing version, accent/ground-effect
finish changes, second-wheel-set hardware/caps, SBT's extra panel and ZR roof trim.
These are not new purchases or visual assets. Z06's WKR text mentions 5ZW without
a corresponding model offering; the original text remains evidence and no
phantom option is created. New schema payloads are content names, effect kind,
value and precedence, plus a reason on source dispositions; no dependencies added.

**Validation:** the focused suite exercises all 32 initial configurations and
704 interiors in each applicable body, 54 Z06 package/wheel states, all GS/GSX
conditional roof pairs, stripe conflicts in both directions, CBF complete-root
replacement/cancel/revert, six-lane package ownership, exact independent totals,
rate-order independence, repeat import and last-lane rollback. The preserved
eight-case, offering, source and foundation suites run alongside it.

**Remaining boundary:** this is full translation of retained behavior families
and the identified accepted behavior corrections, not exhaustive combination
proof. Whole-revision semantic overlap remains next. Presentation/navigation,
disclosure rendering, code-emission mappings and generated consumer artifacts
are still absent, as are freeze/completion/publication operations and §5 release
proof. Every state retains `partial_catalog_not_submission_ready`. No browser,
deployment, canonical authority or frozen evidence changed.

## Semantic overlap and cross-lane validation

The [semantic validation report](../docs/semantic-overlap-validation.md) and
[complete inventory](../docs/validation/semantic-overlap.json) extend the behavior
pass to every scoped exclusion/peer pair, requirement, replacement, acquisition
and interior ownership path. The audit records source dispositions and separates
proved inapplicability from failed or unresolved checks.

```sh
python3 -m catalog.semantic_validation --output .local/semantic-overlap.json
python3 -m unittest tests.test_semantic_validation
```

This explicit milestone command checks preview/confirm/cancel/revert, both request
directions, independent and concurrent ownership, true/false conditions and
conflicting precedence. Repeated previews reverse rule storage order. It is not
an import hook, authoring service or release gate. Expected values in the focused
lane cases come from accepted policy and retained evidence; the larger matrix
checks the translated constraints rather than inventing a new source of truth.

The pass repairs direct removal of interior-owned seats, which previously were
silently reacquired during final evaluation. The interior owner is now cleared,
unrelated purchases remain, and the entire prior state can be canceled/reverted.
Prerequisite cleanup retains package owners even when their supplied choice
allows an alternative peer. Replacement cleanup honors the accepted purchase,
and redundant removal of an absent choice preserves the build and undo state.
Missing-group diagnostics have stable order. No schema or business-data
changes, dependencies, consumer rendering or release operations are introduced.
Every state remains `partial_catalog_not_submission_ready`.

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

## Consumer mappings and local release operations

See [consumer and release implementation](../docs/consumer-releases.md) for the
complete six-lane mapping, confirmation-gated local form and freeze/completion/
publication/rollback/backup/restore commands. These consumers use the typed
evaluator directly, with server-held candidates and complete warnings. They do
not replace the historical parity generator or deploy to the existing form.
