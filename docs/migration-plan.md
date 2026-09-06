# CorvetteCatalog migration and manufacturer-intake plan

Status: Checkpoint A specification completed September 5, 2026. The owner authorized starting the next checkpoint on September 5. Checkpoint B is in progress: its first bounded slice freezes the workbook and matching runtime baseline. Relational import remains unfinished; Checkpoints C–H remain unauthorized. See [source and schema specification](source-schema-specification.md) for inspected evidence, logical field mappings and unresolved decisions.

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

Define model years/models, variants, option definitions, model offerings, availability, interiors/components, typed rules, price contexts, presentation, assets, and source evidence as explicit entities and relationships. Specify row grain, candidate keys, functional dependencies, null/zero/all-scope semantics, and reference constraints before DDL.

Preserve existing runtime IDs through explicit mappings; do not merge on RPO or matching labels alone. Shared definitions must represent shared meaning. Model-specific price, applicability, copy, and lifecycle differences remain explicit where legitimate.

Source-document identity and page/row locations are provenance, not product primary keys. Revisions must link to stable product identities without erasing the evidence behind earlier accepted releases.

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
| B — Disposable baseline import — in progress | [Workbook/runtime baseline frozen](../baselines/2026-09-06/README.md); next import frozen workbook facts into a new relational candidate | Six contracts match regeneration except generation timestamps; browser registry matches byte for byte. Relational row accounting, constraints and identity reconciliation remain pending |
| C — Manufacturer intake pilot | Extract one bounded guide family into review staging | Precise citations, coverage accounting, idempotent import, explained differences; no automatic canonical updates |
| D — Form parity | Generate all six model contracts directly from the candidate catalog | Exact business behavior and meaningful output ordering preserved |
| E — Authoring pilot | Edit an offering, shared definition, and relationship through the new UI | Transactional changes, persistence, shared impact, stale-edit refusal, readable history |
| F — Complete operations | Remaining editors, reviewed intake acceptance, release creation, export, backup/restore | No Excel write dependency; repeatable recovery and release rollback |
| G — Canonical cutover | Final source freeze/reconciliation and explicit authority switch | No lost edits, unresolved drafts, or unclassified behavior changes |
| H — Visualizer delivery | Art-supported exterior/interior pilot, then expanded coverage | Correct resolved-build images and release identity; unchanged pricing/submission |

Checkpoint A is complete as a specification. Checkpoint B has started with the frozen baseline prerequisite; no importer, database, parser or application has been implemented. The inspected raw export defines the first candidate format, with Stingray JL9/J55 brakes and their Z51 relationship proposed as the bounded intake pilot. The existing workbook remains canonical for the form. Stop at the completed baseline slice; the next bounded B task is the disposable relational importer. Checkpoint C requires its own intake authorization. Do not migrate production or automatically continue across checkpoints.

## 8. Owner clarifications and remaining decisions

September 5, 2026: authoring is local and single-user, with Sean as sole developer. Existing workbook pricing, availability-condition and rule conflicts are intentional; trace them through the sheets and preserve their behavior. The owner expects the workbook to capture the raw guide's rules despite inconsistent and abstract manufacturer wording. Verify that expectation rather than treating it as completed parity evidence.

Pay particular attention in B/D to non-LPO options, standard-feature listings and trim-equipment display across all six models. Trace any code-owned business policies in 27vette so the future catalog can own them explicitly as data. Present concrete ambiguities after inspecting the workbook format and runtime consumers; do not normalize intentional differences or modify the reference project.

Sean will supply refreshed manufacturer input: the July 26 price schedule and order guide for the week of September 7, 2026. Verify exact edition labels, acquisition history and currency when received; the existing inspected source remains historical evidence. For the proposed C pilot, JL9 is standard on Stingray; J55 is included with and only available with Z51, replacing JL9. Intake implementation still requires separate authorization.

Visualizer assets are unprocessed `.psb` files in a local folder, as reported by the owner. Inspection and processing will be part of a later task; inventory, rights and the first scene remain to be established in H. UI interactions to retain or redesign remain a decision for authoring UI work.

The owner clarifications above did not authorize source corrections or change canonical authority. The subsequent request to start the next checkpoint authorized beginning B; its workbook/runtime baseline is now frozen as described above.
