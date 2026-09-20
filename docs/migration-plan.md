# CorvetteCatalog migration and manufacturer-intake plan

## Current direction — September 19 authoring and delivery scope

The customer experience remains a close port of the current live form and dealer
submission workflow, with reviewed order-guide detail and accepted behavior
corrections. Steps and sections may be reordered or regrouped to support a coherent
visualizer flow; this is not authorization for an unrelated customer-form redesign.
Dealer integration must trace and preserve the existing operational contract.
The local consumer review form is integration groundwork, not the final customer
design. Catalog authoring is a separate local management interface.

Sean is preparing visualizer assets separately. Asset inventory and processing
are not part of the current catalog task. Later visualizer integration will bind
that artwork to the resolved build and adapt the form flow around the stage.

Continue authoring and reviewed intake acceptance first, then dealer integration
and visualizer integration, production delivery, and final reconciliation and
explicit canonical cutover last. The workbook remains canonical. Existing local
release operations are retained; authored-edit acceptance still needs to extend
their source-only validation contract before edited drafts can be released.

The first bounded E implementation is the [option authoring pilot](authoring-pilot.md):
model-owned name/base-price editing, scope review, atomic persistence, stale-edit
refusal and readable history in a separate local draft. E is not complete:
relationship editing and the ownership-reviewed shared-record pilot remain next,
followed by the remaining F editors and reviewed acceptance. Equal RPOs or labels
do not justify cross-model sharing.

## Prior direction — September 17 consumer mappings and release operations

The separately authorized [consumer and release implementation](consumer-releases.md)
adds all six lanes' presentation/identifier/output mappings and a local form whose
complete warnings must be confirmed before the server commits a candidate. Cancel
preserves the whole build; revert previews restoration and also requires confirmation.
Order exports and visualizer state use the same frozen catalog as the form.

Local operations now prepare a draft, freeze an exactly validated snapshot, build
all consumer artifacts, complete an immutable release, and publish or roll back a
channel using compare-and-swap. Backup and restore validate the complete bundle.
Freeze replays pinned source translation and runs the semantic audit on the actual
snapshot. Failed generation and stale publication preserve the last good pointer.

Validation passed 21 distinct regression tests and a fresh 6,921-entry semantic
audit with zero failed/unresolved findings. All 39 release artifacts verified,
backup/restore ran in a fresh store, and the restored runtime passed the affected
Z06 browser preview/cancel/confirm/revert flow.

This implements the local §5 generation/publication boundary. The workbook remains
canonical; dealer submission, visual artwork, production deployment and canonical
cutover remain separate. The historical parity generator and frozen evidence are
preserved. See the implementation note for commands, verification and limitations.

## Prior direction — September 17 semantic overlap and cross-lane validation

The [semantic-overlap pass](semantic-overlap-validation.md) inventories every
scoped exclusion, replacement, continuing dependency, acquisition, choice group,
interior ownership path, contextual rate, equipment substitution and content
effect across all six lanes. The complete evidence report retains the 3,770 source
behavior dispositions and tests both exclusion directions, ownership histories,
policy precedence and whole-state preview/confirm/cancel/revert. Reversed rule
storage challenges accidental ordering dependencies.

The pass fixes interior-owned seats being silently reacquired after removal,
order-dependent cleanup of yielding package children with unmet prerequisites,
replacement conflicts preferring a consumed request over the accepted purchase,
and absent-option removal destroying its former supplying package. Compatible
package peer yielding and prior undo state are preserved. Equal-rank compatible
acquisition causes remain distinct owners of one charged item.

The final implementation passes **115 regression tests in 98.225 seconds**.
The full matrix completed in 644.06 seconds with 6,921 inventory entries,
69,796 scoped outcomes and zero failed or unresolved findings. Detailed coverage
and dispositions are recorded in the linked report.
No source facts, accepted business decisions, schema, dependencies or canonical
workbook changed. The draft remains `partial_catalog_not_submission_ready`.

Consumer presentation/emission mappings, artifact generation and
freeze/completion/publication operations remain subsequent work. They require
separate authorization; §5 release contracts cannot establish readiness until
those paths exist. No merge, deployment or cutover is included in this pass.

## Prior direction — September 16 full behavior translation

The authorized [full behavior pass](../catalog/README.md#full-behavior-translation)
implements `catalog/behavior_sources.py` across all six lanes. It translates
direct/grouped requirements and conflicts, explicit choices, defaults, interior
and color conditions, accepted corrections, equipment substitutions and supplied
content, while preserving the eight-case and offering-only regression projections.
All 3,770 source behavior rows have individual dispositions and typed provenance;
five Z06 code-derived CBF fragments retain the pinned runtime source identity.

Accepted corrections include GS/GSX hash/roof and graphics behavior, GS brake
restoration and conditional B4Z, Z06 PCZ/second-wheel-set/stripe relationships,
DTC/SAI conflicts, GSX LS6-rule retirements, CFC paint direction, and full
independent-purchase retention. Whole-state previews preserve cancel/revert;
the CBF transaction accounts for all incompatible live package/aero roots.
Exact rates, all 32 initial states, all 704 interiors, the 54 Z06 package/wheel
states, source accounting, repeat import and atomic failure are covered by the
focused behavior/source/evaluator/foundation checks: **100 tests passed in
63.701 seconds** on the final implementation. Fresh and reopened CLI imports,
all six handoff contracts and diff checks pass. A separate 4,032-request smoke
pass found only 254 missing-prerequisite refusals and no unexpected errors.

The next pass is whole-revision **semantic overlap and cross-lane consistency**.
Release contracts in §5 remain the target: consumer presentation/emission mappings,
artifact generation and freeze/completion/publication operations still need
implementation before release validation can establish readiness. The draft
continues to report `partial_catalog_not_submission_ready`; no canonical change,
merge, deployment or cutover is part of this pass.

## Prior direction — September 16 complete offering population

The authorized population expansion is implemented in
[`catalog/evaluator_sources.py`](../catalog/evaluator_sources.py). The
[complete offering importer](../catalog/README.md#complete-offering-population)
retains all 1,379 source option identities, adds nine accepted DTC/SAI identities,
and populates 704 interiors, 7,498 applicability pairs and all 297 source
contextual rates plus three accepted SC7/SBT rate corrections. Retirements,
unavailable states, accepted naming/restoration decisions, GS/GSX Z25 pricing,
and model-qualified interior charge owners remain
separate from frozen baseline facts. The original eight-case fixture remains
available for independent regression checks.

Typed interior parts/component rates and contextual selectability overrides
extend the disposable schema and evaluator only as needed to consume these
offerings. The four known AE4/R6X defects are corrected by one seat owner, with
no stored total or balancing residual. Every scoped interior is exercised;
all six lanes reconcile against retained handoffs rather than counts alone.
Validation: the broader suite passed 135 tests in 182 seconds before the final
ZR1X name and three SC7 rate refinements; all 76 affected source/evaluator/
foundation tests passed on the final implementation in 16 seconds. Fresh and
reopened CLI imports, six-lane handoff validation and diff checks pass. Existing
`rule_inventory.py` ResourceWarnings remain without test failures.

This checkpoint completes offering population, while general behavior beyond
E01–E08 and interior price ownership remains bounded. Full option-rule/default/
conflict translation, remaining accepted behavior corrections, semantic overlap,
release operations and consumers remain subsequent work. The database remains
draft and every result is `partial_catalog_not_submission_ready`; the workbook
and frozen sources are unchanged. No merge, deployment or cutover is authorized.

## Prior direction — September 16 bounded evaluator

Following merged PR #39, the owner authorized SQLite and the bounded foundation
in [proposal §9](master-schema-proposal.md#9-review-outcome-and-next-bounded-work).
The [implemented foundation](../catalog/README.md#disposable-master-schema-foundation)
creates model/year/revisions, all 18 typed identity/version pairs, structural
endpoints, applicability scopes and evidence. Its six-lane UVB sample retains
source option/configuration IDs: six model-owned options, 32 configurations and
all 32 status rows, including unavailable pairs. Only the three populated
revision-owned relations receive typed translation tables.

Fifteen focused tests pass: per-connection FK enforcement, composite and
model/year rejection, same-model earlier-year predecessors, persisted UUID
reuse on re-import, atomic failure, source reconciliation, provenance and group
scope containment. DDL uses standard table/key/check constructs; SQLite is the
only engine executed. Cross-row predecessor and scope rules use Python validation.
The disposable file is `.local/foundation/catalog.sqlite`; the older baseline
candidate and frozen source evidence are unchanged.

The original foundation was a structural projection. Step 3 below extends the
same DDL with the selected cases' price and policy payloads; presentation,
visual bindings, full catalog population, consumers and releases remain later work.
PR #40 is merged. The owner reports the environment baseline restored in the
review worktree: Python 3.14 virtual environment, existing pinned requirements,
and access to the ignored raw guide; 76 tests passed in approximately 160 seconds.
That full-suite result was not rerun for this documentation-only target selection.

Step 2 now selects [eight evidence-derived evaluator cases across all six lanes](master-schema-worked-examples.md#first-evaluator-slice--evidence-derived-acceptance-targets),
including exact charge checkpoints, ownership, cancellation/revert, scope and
negative controls. Baseline observations remain separate from accepted corrections.
E03 specifies both trigger removal and the September 15 accepted direct D84
removal: disclose D84+DMX removal, preserve paint, confirm/cancel/revert atomically.
The shared machine-readable compatibility policy records this resolution and
applies the same interaction to analogous dependent-option conflicts across all
six lanes. The worked examples document that coverage and the unchanged factory,
mandatory-equipment and model-specific replacement limits.
PR #41 merged with these targets and the direct-removal clarification.
Step 3 now implements their [bounded source population](../catalog/README.md#evaluator-case-source-population--step-3)
in `catalog/evaluator_sources.py`, using a separate ignored
`.local/foundation/evaluator-sources.sqlite` file. Prices use exact integer USD
cents and evidenced bases. The slice adds typed conditions, ownership policies,
requirements, carbon-wheel groups, purchase-transfer actions, substitutions and
complete typed translation provenance, preserving source IDs and accepted decisions.
It includes 32 configurations, 72 options including the original UVB samples,
two GS EL9 leaves, 55 acquisitions, 11 requirements and 29 contextual rates.
Source tests reconcile values/scopes/relationships rather than relying on counts;
re-import preserves allocations and a failed import rolls back the whole slice.
Frozen sources, original observations and the canonical workbook are unchanged.
Validation on the final implementation: 89 full-suite tests passed in 155 seconds
using the established Python 3.14/openpyxl environment, including 16 foundation
and 13 source tests. Fresh/reopened CLI re-import, six-lane handoff validation
and diff checks also pass.

**Step 4 — conditional-rule, intent-transition and pricing evaluator — implemented.**
PR #42 merged the source inputs. `catalog/evaluator.py` now reads that revision
snapshot and executes the independently authored E01–E08 targets, including
rooted causes, exact charge owners, installed-equipment substitutions, ordered
independent intent, scoped conditions, confirm/cancel/revert and direct D84
removal. E02/E06 reverse-order conflicts and E07/E08 independent-first versus
package-only ownership are covered. Synthetic guards reject ambiguous defaults
or replacements, nonconvergence, missing prices and invalid scope without
modifying committed state. The [evaluator API and boundaries](../catalog/README.md#bounded-evaluator--step-4)
document the implementation; no evaluator rule is hard-coded by model or RPO.

Validation: all 107 tests passed in 158 seconds in the established Python 3.14/
openpyxl environment, including the 18 evaluator tests; diff checks pass. The
existing `rule_inventory.py` unclosed-database ResourceWarnings remain.
Every result remains explicitly incomplete for submission because the catalog
is partial; required-interior state is reported independently. Passing these
selected runtime targets does not establish complete catalog parity or release
readiness. Full-catalog translation, semantic overlap/release validation, UI,
canonical-data change, deployment and cutover remain outside this slice. No
subsequent checkpoint has been started.

## Prior direction — September 13 master-schema proposal

The owner authorized the [master-schema proposal](master-schema-proposal.md)
after the merged six-model review. The logical proposal is now drafted for review:
model/year/revision ownership, typed keys and applicability, conditional acquisition
and continuing validity, model-scoped purchase intent, single charge ownership,
equipment/presentation separation, provenance and release boundaries. Six connected
walkthroughs and a 72-decision coverage index retain the accepted lane differences.
No DDL, target-data translation, evaluator or canonical change is implemented.
Review corrections now make choice-group membership explicit and independent of
presentation, type conflict members, define interior conflicts through dependency
loss/revert, correct UQT charge wording and constrain release membership by model
and year. The [relationship diagram slice](master-schema-diagram.md) now covers
every named relation, per-relation keys/FKs and all nine scope junctions, settles
which relations carry continuing identities and the freeze-time group scope
constraint, and links the subsequent column naming and allocation resolutions.
The [populated-tables and traces slice](master-schema-worked-examples.md) now
illustrates paired identities/versions, scoped conditions, purchase ownership,
pricing, cancellation/revert and static/installed/order outputs across all six
lanes. Source IDs and accepted totals are retained; exact GSX LS6 and ZR1X CFC
relationship retirements remain evidence-linked dispositions. The examples expose
key/allocation needs in their Open section, including replacement purchase
ownership and the limits of a representative output subset. September 14: that
section now gives explicit design resolutions for O1–O8 and N1–N3, with concrete
keys, typed request transfer, evidence/translation linkage and release validation
responsibilities. The five omitted Z06 CBF fragments are individually identified.
These are design dispositions for review; full target population, consumer mapping
and executed output/constraint checks remain outstanding. Review the resolutions
before separately authorizing a disposable relational foundation.
Authoring, deployment and cutover remain later work.

## Prior discovery direction and completion

The owner directed a consistent completion review and catch-up of Stingray,
Grand Sport, Grand Sport X and Z06 before continuing ZR1/ZR1X. The authoritative
current scope and model status are in the [discovery index](model-discovery.md).
Earlier dated completion entries mean completion of the work described at that
time; they do not override the current coverage review. Keep their source evidence
and accepted decisions intact. Complete all six independent model discoveries
before proposing one master schema. No DDL, canonical corrections, application
implementation, deployment or cutover is authorized by this work.

ZR1 discovery was subsequently authorized and executed: [behavior](zr1-behavior.md)
and [structured handoff](zr1-structured.md) retain all four configurations, source
accounting and connected runtime evidence. All nine owner targets were accepted
September 11, 2026, with TOM retained only when selected before ZTK and DUW
removed from the future offering set. The subsequent owner clarification closes D05 with clickable compatibility styling
and replacement notices, reserving fully inactive cards for factory unavailability;
D06 keeps displaced covers deselected. All nine decisions are retained in the
[structured owner overlay](zr1-owner-decisions.json). The [common interaction policy](model-discovery.md#common-compatibility-notice-policy--september-11-owner-decision)
supersedes earlier differing compatibility UI treatments while retaining model rules.
ZR1 discovery and decision capture are complete; corrections are not implemented.
September 12: [ZR1X discovery](zr1x-behavior.md) and its [six-file handoff](zr1x-structured.md) now retain source accounting and frozen runtime evidence. The initial handoff marked nine ZR1X decisions open; the September 13 reconciliation below supersedes that decision status. The runtime probe and ZR1/ZR1X extractor are unified, with parsed-value preservation and byte-reproduction gates.

September 13: the owner clarified that these decisions had already been made and
requested reconciliation with prior approvals. All nine [ZR1X decisions](zr1x-behavior.md#8-reconciled-owner-decisions-and-expected-targets)
now cite the earlier approvals and retain independent ZR1X source applicability.
DUW retirement is recorded as an owner-directed target departure, SAI is an accepted
addition, and currency/pricing/scope policies are carried forward without importing
another model's amounts or equipment. No new owner choice remains among these nine
items. All six model discovery handoffs and decision records are complete; one
coherent six-model review remains the next separately authorized task. Corrected
runtime verification, master-schema implementation and cutover have not occurred.

September 13: the [consolidated six-model review](six-model-review.md) is complete.
The 72 accepted decisions and all six family handoffs support proceeding to one
logical master-schema proposal. The review resolves historical compatibility-policy
precedence, preserves model-specific purchase ownership and rates, and identifies
conditional acquisition, charge ownership, equipment projections and source-to-target
translation requirements. The next task is the coherent schema proposal and its
six-lane walkthroughs, not DDL or application implementation. Frozen evidence and
accepted business decisions remain unchanged; a stale ZR1 decision-heading link
was repaired in the review pointer and nine records. Corrected-output verification
and cutover remain later work.

## Historical roadmap and decisions

Status: Checkpoint A specification completed September 5, 2026. Checkpoint B's disposable relational import is implemented and verified locally September 6, 2026. The owner separately authorized C after supplying a new export; its bounded brake intake is also verified locally. D's direct catalog generation and six-model form parity are implemented and verified locally September 6, 2026. E–H remain unauthorized. See [relational import evidence](../catalog/README.md), [source and schema specification](source-schema-specification.md) and [source intake results](../sources/README.md).

## 1. Clean project boundary

Implement the new domain model, application operations, and import contracts here. Study the existing Manager's useful interactions and the form's observable behavior without inheriting its Excel synchronization architecture. Reuse individual components or algorithms only after evaluating their dependencies and fit; React, FastAPI, and SQLite remain candidate choices rather than scaffolded commitments.

The existing project continues operating independently. Nothing in this repository writes its workbook, generated artifacts, runtime, or deployment. Later cutover requires an explicit decision after comparison and recovery proof.

## 2. Two source roles, one accepted catalog

`/Users/seandm/Projects/27vette/stingray_master.xlsx` is the canonical source of truth for the existing form and the primary migration and behavior baseline here. The other root Excel file, `2027 Chevrolet Car Corvette Export (4) (1).xlsx`, is the raw manufacturer order-guide format that is processed and transformed into the `stingray_master.xlsx` format. This source lineage does not make the raw guide a direct form input or authorize overwriting the canonical workbook.

Manufacturer order guides are first-class intake evidence, particularly for future model years and revisions. Preserve source documents unchanged, with source identity, hash, model year, publication/revision date when known, and acquisition date. Do not invent dates when absent.

Capture exact page/table/cell locations as the format permits. Extracted records retain original wording alongside parsed values. Document structure, footnotes, model/trim/body applicability, price units, included equipment, and package relationships all matter. Preserve unresolved text rather than guessing its interpretation.

The accepted catalog distinguishes manufacturer facts, dealer-authored presentation or operational choices, and derived runtime output. Provenance links facts to their evidence and records reviewed departures from the guide. A newer document does not automatically override every field from an older source or a dealer-authored choice.

## 3. Intake workflow

Original guide → extraction staging → typed candidate facts → workbook/catalog comparison → discrepancy review → accepted catalog transaction.

Classify candidates as unchanged, added, changed, removed, ambiguous, or conflicting. Absence from an extraction is not proof of manufacturer removal. A removal needs complete relevant coverage and affirmative review.

Track source coverage: tables/pages processed, unexplained omissions, unparsed notes, unresolved references, and duplicate identities. Parser confidence alone cannot authorize a business change. Keep repeated imports idempotent through stable source/candidate identities, and preview their actual effects.

Initially support one real supplied guide format and one bounded family, chosen after inspecting the document. Do not build a universal PDF/Excel parser in advance. Do not revive the retired 27vette raw-ingest pipeline: its artifacts may explain prior failure modes but are not trusted extracted data or an implementation template.

## 4. Relational design

September 7 behavior-analysis reset: the relationship inventory did not demonstrate
comprehension of complete model behavior. The subsequent [ownership proposal](proposed-database-design.md)
(PR #12) is unvalidated and is not a basis for implementation. Schema
implementation remains paused. Analyze each model in its own lane with the same structure, following
model/body/trim foundations through connected selections, equipment and prices.
Use full raw-guide disclosures with the workbook and inspect runtime behavior
where needed; do not inherit the old architecture or consolidate models from
matching codes/signatures.

The [Stingray relationship analysis](stingray-behavior.md) now covers every family,
including interiors/belts, performance, wheels, accessories, order restrictions
and equipment/output. All 242 workbook offerings have a source disposition;
1,386 matched status pairs and 223 coded duplicate occurrences agree. The guide's
78 trim/seat/interior combinations expand exactly to 130 workbook choices. The
review includes 260 interior/body contexts, 1,300 paint/interior states, 780 belt
attempts and 48 connected sequences / 237 states. Four known R6X/AE4 undercharges
and source/behavior differences remain explicit; this is family-analysis completion,
not exhaustive build acceptance or blanket manufacturer reconciliation approval.
The owner subsequently accepted the DTC/DUW and SAI corrections for planning
(section 8).
The owner wants one whole Stingray schema plan before implementation or cutover.
The owner authorized that planning task. The [whole Stingray schema plan](stingray-schema-plan.md)
is now drafted for review: model-owned identities, explicit configuration scopes,
typed relationships, one owner per charge, equipment/content, presentation,
provenance and release boundaries. Connected walkthroughs cover the analyzed
families and distinguish accepted corrections from unresolved decisions.
This is a logical proposal, not executed DDL or new runtime parity. Review the
plan and its decision table before scoping implementation; no database pilot is
started here.
Other models remain unfinished.
The [earlier relationship map](form-relationship-map.md) remains inventory evidence,
not completed behavioral analysis or schema approval.

The earlier cross-model proposal remains reference material. For Stingray, the
new plan proposes direct model-owned relationship families without an unproven
shared-definition/application layer. Seat and R6X charges have option owners;
non-option interior extras have component rates. Detailed row translation and
consumer equivalence remain implementation obligations after plan review.
No DDL or authoring implementation is authorized by either proposal.

September 8: before implementing the proposed schema, the owner directed the
remaining model analyses in this order: Grand Sport, Grand Sport X, Z06, ZR1,
ZR1X. Use the same lane structure and test each against the Stingray proposal;
revise one coherent proposal after the model-specific challenges are understood.
The [Grand Sport analysis](grand-sport-behavior.md) is documented for review,
including connected package/graphics/interior behavior and source discrepancies.
It identifies a missing option-plus-paint condition on prerequisites and
distinctions between initial defaults and restoration. Owner review resolves
Launch Edition pricing and records the other intended Grand Sport corrections.
No new tables or source corrections were applied.

September 9: the owner directed structured handoffs as each model is completed,
starting by backfilling Stingray. The [Stingray structured handoff](stingray-structured.md)
and its [record file](stingray-structured-records.json) now organize complete
baseline lists, connected behavior, accepted corrections, unresolved decisions
and expected sequences. These are review inputs, not a finalized target dataset
or implementation. Grand Sport's structured handoff is next; remaining behavior
lanes retain their order: Grand Sport X, Z06, ZR1, ZR1X. Consolidate the schema
after the model handoffs. This task stops at structured Stingray.

September 9: the separately authorized [Grand Sport structured handoff](grand-sport-structured.md)
and [record file](grand-sport-structured-records.json) now retain the complete
model-scoped baseline, recorded observations and September 8 owner decisions.
Baseline defects remain distinct from accepted target corrections and unresolved
facts, including the T0E duplicate and R6X charge discrepancy. Grand Sport X is
next in the established model order; schema consolidation remains paused. This
task stops at structured Grand Sport, without implementation or canonical-data changes.

September 9 owner review resolves the model decision lists in the
[Stingray handoff](stingray-structured.md#8-decision-overlay-source-baseline-and-target-remain-separate)
and [Grand Sport handoff](grand-sport-structured.md#8-decision-overlay-source-baseline-and-target-remain-separate).
Accepted targets include dependency-loss removal with alert/revert, general
conflict replacement offers with explicit blocking exceptions, aero/cover rules,
Grand Sport R6X/T0E/graphics/naming corrections, visible unavailable cards,
column-E option pricing (DTC 1,295; SAI 295), customer-form scope and separate
configured/informational equipment displays. After PR #20, the owner confirmed hash-first Z15 selection with the exact disclosure
“Selecting this hash mark adds the Grand Sport Heritage Package (Z15) for $995.”
and USD for all Stingray and Grand Sport prices. These confirmations close the
remaining decision details for both model handoffs; numeric prices are unchanged.
Earlier currency-unknown statements below describe preserved historical evidence,
not the accepted currency for these two models.
Frozen evidence is unchanged. Implementation, corrected-output verification and
schema consolidation remain separate work after model analysis.

September 9: PR #21 is merged and the 12 Stingray / 16 Grand Sport decision
records are accepted. [Grand Sport X analysis](grand-sport-x-behavior.md) has
begun with model/body/trim foundations and FED tire-package round trips across
six configurations (18 observed states). The [foundation records](grand-sport-x-foundations-records.json)
preserve this partial evidence. Remaining families and the complete structured
handoff are unfinished; schema consolidation remains paused.

September 10: the owner authorized completion of the Grand Sport X behavior
analysis, with its structured handoff explicitly deferred to the next pass.
The [complete family analysis](grand-sport-x-behavior.md) now accounts for all
239 workbook offerings, reconciles 1,368 primary-equipment status pairs, and
traces interiors, graphics/roof dependencies, performance, accessories and order
output. Independently observed issues include missing Z25 output, DTC/hash
coexistence without Z15, conditional D84 gaps, R6X/AE4 undercharges and incomplete
rear-graphic exclusions. These are review findings, not accepted corrections.
September 10 owner review subsequently applies the accepted Grand Sport decisions
to overlapping Grand Sport X findings and directs removing the HP1 combined
1,250-hp claim and LT7 reference. The behavior document records these accepted
targets; the separate ZZ3/LS6 relationship correction remains a clarification.
The earlier foundation JSON remains unchanged. Next is the Grand Sport X
structured handoff and model-specific review; no Z06 or schema work starts here.

September 10: the owner separately authorized the [Grand Sport X structured
handoff](grand-sport-x-structured.md) and [record file](grand-sport-x-structured-records.json).
They now preserve all 239 offerings, 1,434 availability rows, 132 interiors,
198 components, model-scoped relationships/prices/presentation and all full-analysis
observations. Thirteen owner-overlay entries are accepted; the ZZ3→LS6→D3V
relationship correction remains proposed. HP1 target copy retains only the
front-axle rating and torque. Frozen source/behavior evidence remains distinct
from accepted targets. Structured review input is complete; implementation and
corrected-output verification remain separate. No Z06 or schema work starts here.

September 10 final Grand Sport X decision: the owner explicitly approved removal
of both LS6 rules in `grand_sport_x_rule_mapping`: row 51
`grand_sport_x_rule_ls6_includes_d3v_c7bc4b3df65b` and row 82
`grand_sport_x_rule_zz3_includes_ls6_b15b51ebf396`. The handoff now records exact
removal operations while retaining frozen evidence. All 14 Grand Sport X decision
entries are accepted, matching Stingray and Grand Sport's completed behavior,
structured handoff and business-decision stage. This supersedes the preceding
pending-ZZ3 status. Only review/merge of this decision update remains for that
stage; implementation and corrected-output verification are later work.

The [workbook translation blueprint](workbook-translation-blueprint.md) maps the current source families and behavior. Its first structural slice is implemented in candidate schema 3: one model-owned `option` table replaces six option tables, with relationships retargeted and six-model parity preserved. The candidate now has 43 tables and 23,588 typed rows; all source facts and 7,448 availability pairs remain intact. Workbook meaning and intended behavior are the migration requirements; remaining table boundaries remain revisable. Passing import and output parity does not approve the final authoring schema or the known R6X pricing defect.

Define model years/models, variants, model-owned options, availability, interiors/components, typed rules, price contexts, contextual presentation, assets, and source evidence as explicit entities and relationships. Specify row grain, candidate keys, functional dependencies, null/zero/all-scope semantics, and reference constraints before DDL.

Preserve existing runtime IDs through explicit mappings; do not merge on RPO or matching labels alone. Shared definitions must represent shared meaning. Model-specific price, applicability, copy, and lifecycle differences remain explicit where legitimate.

Source-document identity and page/row locations are provenance, not product primary keys. Revisions must link to stable product identities without erasing the evidence behind earlier accepted releases.

September 10: live repository/PR verification confirms Stingray, Grand Sport and
Grand Sport X behavior analyses and structured handoffs are delivered, including
merged GSX decision PR #24. The [Z06 behavior pass](z06-behavior.md), model four
of six, now covers all 244 offerings, complete LZ interior expansion, connected
package/price/removal behavior and guide/workbook/runtime discrepancies. Its
54 package states match wheel-qualified charges, while missing caliper content,
PCZ relationships, LPO/graphics restrictions, SBT and R6X charges remain explicit
review findings. The owner subsequently accepted all twelve Z06 decisions, including
explicit stripe refusal versus badge replacement notice, disabled unavailable
accessories, N3W standard at 3LZ and removed by N2Z, and no PDB+Z07 coexistence
(block Z07 or require a noticed switch to PDD). The behavior report logs the full
accepted overlay. Z06 structured handoff remains next, followed by ZR1 and ZR1X. No Z06 corrections,
schema consolidation, canonical-data changes or cutover are implemented.

September 10: PR #25 is merged. The separately authorized [Z06 structured
handoff](z06-structured.md) and [record file](z06-structured-records.json) now
preserve all 244 offerings, 1,464 availability rows, 130 LZ interiors, 197
component memberships, model-scoped relationships/prices/presentation and all
captured full-analysis observations. All twelve owner decisions are accepted;
D11 retains the authorized block-or-noticed-PDD-switch alternatives without
choosing a final UI treatment. Five code-derived CBF replacement edges remain
explicit translation obligations. Z06 behavior, structured review input and
business-decision capture are complete. Implementation and corrected-output
verification remain separate; ZR1/ZR1X and schema work do not start in this pass.

## 5. Comparison and release contracts

Maintain two separate comparisons:

1. **Migration parity:** accepted workbook baseline versus new-catalog output, preserving existing six-model rules, prices, ordering, identifiers, defaults, and submission behavior.
2. **Manufacturer reconciliation:** guide candidates versus accepted facts, producing explained proposed changes rather than requiring automatic equality.

Freeze a workbook snapshot and matching runtime outputs when the implementation baseline is established. Current reference paths are live, not immutable snapshots. Hash and label captured baselines before relying on them.

Generate the customer form and visualizer manifest from one consistent catalog revision. Review catalog edits, apply related changes atomically, and build a candidate release separately. Failed builds leave the last good customer release untouched. Excel export is a convenience; database generation must not reconstruct Excel as an intermediate step.

## 6. Visualizer preparation

Reserve scenes, layer slots, assets/renditions, configuration bindings, and coverage status in the domain design. Bind visuals to the resolved build, including defaults and automatically included equipment. Keep visual conditions separate from product eligibility and prices.

One option may affect multiple layers; an asset may serve several configurations; model/body/paint combinations may require distinct artwork. Missing images do not make product choices unavailable. Choose the first exterior/interior pilot only after inspecting available art. Full visualizer delivery is independent of database migration completion.

## 7. Bounded checkpoints

| Checkpoint | Deliverable | Required evidence |
|---|---|---|
| A — Source and schema specification — completed 2026-09-05 | [Specification](source-schema-specification.md): 28-sheet raw guide inventory, canonical workbook field mapping, logical entities/keys/ownership, intake/discrepancy contract and future visualizer requirements | Read-only hashes, all 77 workbook sheets mapped by family, 11-role header parity, complete 7,448 availability pairs, precise brake-family/price/footnote examples; remaining source and implementation decisions explicit |
| B — Disposable baseline import — verified locally 2026-09-06 | [Frozen baseline](../baselines/2026-09-06/README.md) imported into a [disposable SQLite candidate](../catalog/README.md) | All 77 sheets / 15,134 source rows accounted for; 30,328 typed rows reconciled; all 7,448 availability pairs and model-qualified identities preserved. Ten importer tests pass, including independent source comparisons, constraints, repeat import and atomic failure checks |
| C — Manufacturer intake pilot — verified locally 2026-09-06 | Unchanged new export, model-qualified six-variant mapping, immutable Stingray JL9/J55/Z51 review staging | 18 availability comparisons and one inclusion unchanged; seven assertions ambiguous. Exact selected cells/runs, 28-sheet inventory, partial coverage and external references retained. Eleven tests pass; repeat CLI reuses identical output. No accepted operations |
| D — Form parity — verified locally 2026-09-06 | [Six contracts and browser registry generated directly from typed candidate tables](../catalog/README.md#checkpoint-d-direct-form-generation) | All six frozen business hashes match; registry metadata/order/aliases match; runtime differential and local browser checks preserve pricing, defaults, equipment and submission output |
| E — Authoring pilot | Edit a model-owned option, a genuinely shared record, and a relationship through the new UI; choose the shared record after its ownership review | Transactional changes, persistence, shared impact, stale-edit refusal, readable history |
| F — Complete operations | Remaining editors, reviewed intake acceptance, release creation, export, backup/restore | No Excel write dependency; repeatable recovery and release rollback |
| G — Canonical cutover | Final source freeze/reconciliation and explicit authority switch | No lost edits, unresolved drafts, or unclassified behavior changes |
| H — Visualizer delivery | Art-supported exterior/interior pilot, then expanded coverage | Correct resolved-build images and release identity; unchanged pricing/submission |

Checkpoint A is complete as a specification. B's frozen baseline now has a verified disposable relational import; currency remains unknown. D generates all six contracts and the registry directly from the candidate, with exact frozen output parity and runtime transition checks. The owner authorized C independently against that baseline: Stingray JL9/J55 brakes and their Z51 relationship remain the bounded pilot. C's [results and remaining ambiguities](../sources/README.md#checkpoint-c-local-completion) remain preserved for review. No manufacturer discrepancy is accepted; D establishes migration parity against the workbook baseline, not guide accuracy. The existing workbook remains canonical. This bounded task stops at D. E–H and manufacturer corrections require separate authorization.

## 8. Owner clarifications and remaining decisions

September 5, 2026: authoring is local and single-user, with Sean as sole developer. Existing workbook pricing, availability-condition and rule conflicts are intentional; trace them through the sheets and preserve their behavior. The owner expects the workbook to capture the raw guide's rules despite inconsistent and abstract manufacturer wording. Verify that expectation rather than treating it as completed parity evidence.

Pay particular attention in B/D to non-LPO options, standard-feature listings and trim-equipment display across all six models. Trace any code-owned business policies in 27vette so the future catalog can own them explicitly as data. Present concrete ambiguities after inspecting the workbook format and runtime consumers; do not normalize intentional differences or modify the reference project.

Sean supplied a refreshed export and authorized C. The new file's price schedule actually reads July 06, 2026; a July 26 revision or September 7 whole-guide edition has not been established. Its option-price headers appear shifted relative to data, and currency remains unknown. Preserve those ambiguities and the earlier source evidence. Owner-confirmed brake interpretation remains: JL9 is standard; J55 is included with and only available with Z51, replacing JL9. No source correction or acceptance is authorized by intake execution.

Visualizer assets are unprocessed `.psb` files in a local folder, as reported by the owner. Inspection and processing will be part of a later task; inventory, rights and the first scene remain to be established in H. UI interactions to retain or redesign remain a decision for authoring UI work.

The owner clarifications above did not authorize source corrections or change canonical authority. The subsequent request to start the next checkpoint authorized beginning B; its workbook/runtime baseline is now frozen as described above.

September 7, 2026, after reviewing the complete Stingray relationship analysis:
the owner accepted two specific corrections for the whole-model schema plan.
Remove DUW and include DTC Royal Blue Full Length Dual Racing Stripes; add SAI
stainless steel dark sill plates. Use the newer export for these items, including
DTC's GTR paint restriction and SAI's 3LT V8X exclusion. See the
[accepted decisions and source locations](stingray-behavior.md#owner-decisions-accepted-for-the-schema-plan--september-7-2026).
The owner confirmed the rest of the reviewed analysis looks correct. These are
accepted planning requirements; the frozen workbook/runtime evidence remains
unchanged, other explicit decisions remain visible, and no implementation or
canonical cutover is performed by this clarification.
