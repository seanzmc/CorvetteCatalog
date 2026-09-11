# CorvetteCatalog migration and manufacturer-intake plan

## Current direction — September 10 discovery catch-up

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
removed from the future offering set. D05 conflict interaction and D06
displaced-cover restoration remain unresolved details in the accepted decision record.
ZR1X is not started; schema and correction implementation remain paused.

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
