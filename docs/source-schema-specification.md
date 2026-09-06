# Source and schema specification

Checkpoint A, September 5, 2026. This is a logical design and source mapping for a fresh implementation. It authorizes no DDL, parser, import, application, canonical-data change, or cutover. The roadmap remains [migration-plan.md](migration-plan.md). Extend this specification when domain ambiguity warrants it; do not make a new specification for each task.

## 1. Scope and completion

Define the source roles, entity grains, fields and owners, identities, intake/reconciliation contract, and requirements shared by the future form and visualizer. Inspect one actual guide format and a bounded family. Completion means these contracts are explicit and remaining decisions have named consequences, not that all guide facts have been reconciled or a technology stack chosen.

The user confirmed the roles of both root Excel files: the manufacturer export is the **raw format in which the order guide arrives**, before processing and transformation into the `stingray_master.xlsx` format; `stingray_master.xlsx` is the **canonical source of truth for the existing form**. The source lineage is raw manufacturer guide → processing/transformation → canonical workbook → generated form data. This is context for the new intake requirements, not a direction to reuse the old transformation architecture.

Workbook parity and manufacturer corrections are separate outcomes. In CorvetteCatalog the canonical workbook is the migration baseline; only later reviewed acceptance creates catalog facts, and only Checkpoint G changes operational authority. Preserve existing transformation decisions, overrides and behavior until classified. No Excel synchronization, Manager projection, or retired ingest architecture is carried forward.

## 2. Inspected sources

All paths in this section are read-only references under `/Users/seandm/Projects/27vette`. Hashes identify the bytes inspected, not an immutable implementation baseline. Freeze matched workbook/runtime snapshots in Checkpoint B before depending on them.

| Source | Identity and observed scope | Role and limitations |
|---|---|---|
| `stingray_master.xlsx` | 581,513 bytes; SHA-256 `3127e663b1531e366ce86b989b6190914108d40dfd15a33a258307a05d608e3c`; 77 sheets, 15,134 populated data rows | Primary migration/business-behavior baseline, including editorial choices and overrides; not proof every fact agrees with the manufacturer |
| `2027 Chevrolet Car Corvette Export (4) (1).xlsx` | 1,619,319 bytes; SHA-256 `6ac9538d5bb8a823ade9afea70b2654057b793e1cf27c081c088545aa3add8a1`; 28 sheets; MY2027 in `Price Schedule!A1:A3` | Raw manufacturer order-guide input, confirmed by the user as the format processed into the canonical workbook format. Original download URL, acquisition date, and whole-document revision are unknown; exact historical transformation coverage has not been reconstructed |
| Guide price schedule revision | `Price Schedule!A297`: revision text contains May 26, 2026, concatenated with the next title | Record the exact text and parsed date with **price-schedule** scope. Do not assert this dates every sheet; `A3` describes start-of-model-year effectivity without a calendar date |
| Reference code | Git HEAD `4fe92a4f078370c478f18484cad31bdafe58ad43`, clean at initial inspection | Behavior evidence, not code selected for reuse. Runtime outputs were not frozen or proven to match this workbook during A |
| `dist_updates/*.pdf` | Three local update PDFs discovered | Not inspected or included in this intake pilot. Filenames alone establish neither revision precedence nor completeness |

The guide package has no `docProps/core.xml`; file timestamps must not fill missing publication/acquisition metadata. Source origin is recorded as the supplied local path, with manufacturer attribution from document content and acquisition history unknown. This is not a claim that it is the latest guide.

### Guide inventory and format

Counts below are populated rows including headings and notes. Last-row coordinates can exceed those counts. The numbered matrix sheets map 1=Stingray, 2=Grand Sport, 3=Grand Sport X, 4=Z06, 5=ZR1 **and** ZR1X, verified from sheet content. Never infer model solely from the suffix.

| Sheets | Populated rows, in suffix order | Structure and intake concerns |
|---|---|---|
| Price Schedule | 295, last row 300 | Base prices: header row 5, records 6–37. Options: header row 39, subsequent section headings/records through 287. Notes 288–300. Columns change meaning between base and option blocks |
| Standard Equipment 1–5 | 82, 86, 83, 86, 88 | Model/title row 1, legend row 2, variant headers row 3, equipment and notes below |
| Equipment Groups 1–5 | 175, 181, 178, 181, 145 | Matrix family with equipment-group membership and upgradeability; retain symbols, headings, and footnotes |
| Interior 1–5 | 100, 100, 100, 104, 104 | Model/variant matrices with component and package relationships |
| Exterior 1–5 | 105, 111, 108, 108, 75 | Model/variant matrices, including appearance and paint applicability |
| Mechanical 1–5 | 53, 51, 47, 49, 50 | Model/variant matrices; Mechanical 1 supplies the pilot below |
| Color and Trim 1, 2 | 26, 21; last rows 27, 22 | Multiple blocks; row 4 contains trim/seat/color headers, later blocks describe exterior/interior combinations. Slash/comma combinations and superscript footnotes cannot be treated as flat identifiers |

The matrix sheets contain padded cells through column Z; use actual cell content, headers, merged ranges, and worksheet XML relationships rather than trusting dimensions or hardcoding XML sheet numbers. Preserve rich text: `Mechanical 1!D7` is `A` plus superscript `1`; `C7` contains its numbered restriction. Flattening both into strings loses the distinction between a code digit and a footnote. The legend in `C2` distinguishes standard, available, unavailable, ADI available, included, upgradeable included, and cross-model markers. These are source symbols; only reviewed interpretation maps them to catalog availability and selection policy.

### Bounded pilot definition and examples

Proposed Checkpoint C family: **Stingray JL9/J55 brakes and their Z51 inclusion relationship**, all six Stingray variants. Primary coverage: `Mechanical 1!A1:I3`, `A6:I7`; supporting evidence: `A53:I53`, `Price Schedule!B221:J221`, base header/first price row `B5:J6`, option header `B39:J39`, notes `A288:A300`. Other Z51 package members in row 53 are retained as context and unresolved external references, not silently declared fully processed.

| Evidence | Workbook counterpart | Interpretation for review |
|---|---|---|
| `Mechanical 1!B6:I6`: JL9, six S cells | `stingray_options!A168:K168`; `stingray_ovs!A596:C601` | Standard brakes; reference-only code is distinct from orderable code. Customer label/section need not equal guide prose |
| `Mechanical 1!B7:I7`: J55, six A-with-footnote-1 cells; C7 restriction | `stingray_options!A62:K62`; `stingray_ovs!A560:C565` | Availability plus package restriction, not freely selectable J55. Workbook separately stores `selectable=false` |
| `Mechanical 1!C53` includes J55 | `rule_mapping!A109:H109` | Z51 includes J55. “Only available with” in C7 also proposes a prerequisite; whether it is already enforced by nonselectability/inclusion requires behavior comparison, not an automatic extra rule |
| `Price Schedule!B221:G221`: Z51 MSRP 5,395 | `stingray_options!C128` = 5,395 | Matching sampled amount; not proof all pricing contexts agree. No standalone J55 amount is established by this row |
| `Price Schedule!F6` = 71,000; J6 destination = 2,495; A294 excludes destination from MSRP | `variant_master!F2` = 73,495 | Arithmetic agrees after adding destination. Preserve the existing total; classifying 2,495 as a manufacturer correction from raw inequality would be wrong |

These are inspected examples, not imported candidates or accepted reconciliation decisions. The pilot has no removal authority outside its precise coverage, and a full package interpretation must expand coverage deliberately.

## 3. Ownership and value semantics

Owners below mean responsibility for acceptance/editing, not an automatic source winner:

- **Product steward (P):** reviewed product meaning, identities, applicability, equipment, prices, restrictions. Starts from workbook parity; guide evidence may propose changes.
- **Dealer editor (E):** customer copy, placement, defaults chosen for the form, explanation text, summary layout. A guide cannot silently replace these. A default or selectable flag that also expresses a product restriction needs P review.
- **Intake system/reviewer (I):** immutable originals, locations, extracted assertions, coverage, parser identity, mapping decisions and discrepancy resolutions. Extraction has no acceptance authority.
- **Release system (R):** derived output, immutable catalog revision/release identity, resolved builds, manifests and artifacts. No separately authored business values.
- **Art editor (A):** imagery, scenes, composition, display bindings, rights/source notes and coverage. Cannot alter product eligibility or price.

All accepted rows use typed fields. Empty, false, zero, missing, unknown, and unrestricted are different states. Preserve the source representation in evidence before normalizing it.

| Value/domain | Required meaning |
|---|---|
| IDs and codes | Opaque case-preserving text. New stable IDs are independent of worksheet rows, labels, RPOs, years, and filenames. Legacy values remain exact in mappings |
| Null | Unknown/not supplied only where the field permits it. A missing override means inherit; an explicit false/zero override must survive. Clearing a nullable field is a distinct proposed operation from leaving it unchanged |
| Money | Exact decimal amount with currency and basis (`msrp_ex_destination`, `destination`, `baseline_total`, `option`, `component`, `conditional_total`, `adjustment`, or preserved source-only basis). No floating-point canonical money. Negative adjustments are allowed. Unconfirmed currency stays unresolved; this inspection does not independently establish currency from an explicit currency label |
| Baseline price fallback | Retain authored blank separately from the current runtime's zero fallback. Record missing-rate diagnostics without inventing a priced fact or changing parity totals. Do not replace total price with component sum |
| Boolean/lifecycle | Explicit true/false; inactive history retained. Row activation, customer visibility, selectable behavior, and availability are separate fields. Inactive override means ignore that override, not deactivate the offering |
| Availability | `standard`, `available`, `unavailable` for accepted baseline relations. Unknown guide interpretation remains staging; do not map unknown to unavailable |
| Scope | Explicit `all` or `members` for each applicable axis (model, variant, trim, body). `all` has no members; `members` is nonempty. Multiple axes intersect. Adding a variant to a dynamic all-scope requires impact preview. A frozen variant set does not expand automatically |
| Source blank / `*` scope | Preserve exact token and consumer interpretation. Only normalize to all after confirming the relevant field's behavior; no blanket blank-is-all rule across the workbook |
| Ordering | Explicit integer sequence/priority at its owning context, preserving current order and tie behavior. Source row ordinal is evidence and supplies migration ordering when current code depends on it |
| Missing guide row | Not proof of removal. Blank cells, unprocessed sections, hidden content, unsupported symbols and unparsed notes are coverage gaps |
| Text/raw hierarchy | Original prose/runs remain evidence. Accepted relationships use typed members, not CSV, JSON hierarchy strings, or free-form executable expressions |

## 4. Logical relational model

This describes business relations before DDL. Types, indexes, database engine, web framework and hosting are deferred. Names are logical destinations, not a commitment to one physical table for every line. There is no model inheritance chain.

Common conventions: each independently addressable row has `id` (stable identity, I/system assigned). `active` means retained but enabled/disabled at that relation's grain; `sequence` means order among siblings; `notes` are non-executable editorial evidence. Unless stated otherwise, fields are required. Fields marked `?` may be unknown. Owners apply to every listed domain field; IDs/references are system maintained after reviewed identity mapping. Every candidate key below determines all other fields on its relation. Repeated relationships are member rows, never arrays in canonical authoring.

### Product identity and applicability

| Relation / owner | Grain and candidate keys | Fields and meaning / constraints |
|---|---|---|
| Model / P | One model identity; `id`, `model_key` | `model_key` stable internal name; `name` intrinsic name. No year-specific values here |
| ModelYear / P | One model in a year; `id`, `(model_id, year)` | `model_id` FK; `year` integer MY; `active` lifecycle |
| Trim, BodyStyle / P | One defined trim or body kind; each `id`, `code` | `code` stable domain token, `label` display name. LT/LZ remain distinct |
| Variant / P | One offered model/year/trim/body; `id`, `(model_year_id, trim_id, body_style_id)` for current domain | Three FKs, `active`. Additional editions may invalidate that natural key: stop and extend identity before importing such a case, never squeeze it into a label |
| VariantPresentation / E | One variant; `variant_id` | `display_name`, `sequence`. Year/model labels derive through Variant |
| OptionDefinition / P | One reviewed product meaning; `id` only | `intrinsic_name`, `description?`. Equal labels/RPOs do not establish uniqueness. Initial definitions stay separate where shared identity is unproven |
| Offering / P | One model/year application of a definition; `id` only | `model_year_id`, `definition_id`, `active`. Several offerings may share a definition in a model/year for legitimate distinct roles; no premature unique pair constraint |
| OfferingCode / P | A code assignment; `id`, `(offering_id, code, role)` | `code` text; `role` orderable/reference/legacy-unspecified. Multiple offerings can use one RPO; old workbook RPO does not establish guide orderability |
| OfferingPolicy / P+E | One offering's base interaction policy; `offering_id` | `selectable` whether user may select; `display_behavior?` explicit display_only/auto_only/default_selected/hidden or inherited convention. Preserve workbook blanks until equivalence established |
| Availability / P | One offering/variant pair; `(offering_id, variant_id)` | `status` three-valued accepted availability. Both parents must belong to the same ModelYear. Complete baseline option × variant pairs survive |
| VariantPresentationOverride / E (P for restriction changes) | One offering/variant override; `(offering_id, variant_id)` | `selectable?`, `display_behavior?`, `section_id?`, `active`. Null means inherit the matching base field; cannot erase base values implicitly |
| LegacyMapping / I | One legacy identity in source namespace; `(namespace, model_year_id, entity_kind, legacy_id)` | `entity_id` typed FK through the entity registry below. `namespace` identifies legacy system/version contract, not source file hash. Mapping many legacy aliases to one reviewed identity is permitted; one legacy key cannot map to two identities |

Manufacturer variant mapping uses document identity + year + model designation + manufacturer model code + trim + body. `1YC07` alone is not a variant key: it repeats for 1LT, 2LT, 3LT. Source-specific mappings point to Variant after review. `model_key=grand_sport` and legacy registry key `grandSport` remain distinct namespaces, not silent spelling corrections.

### Interiors and pricing

| Relation / owner | Grain and candidate keys | Fields and meaning / constraints |
|---|---|---|
| InteriorDefinition / P | One approved combination; `id` only | `name`, `material?`, `seat_component_id?`, `interior_code?`, `suede_component_id?`, `stitch_component_id?`, `two_tone_component_id?`, `requires_r6x` explicit fact. Null component means unspecified, not absent by assumption |
| ModelInterior / P | One interior application to model/year/trim; `id`, `(model_year_id, interior_id, trim_id)` | FKs, `active`, `required_offering_id?`, `included_offering_id?`, `section_id`. Do not globalize model-specific prerequisites; linked offerings must share model/year |
| ComponentDefinition / P | One reviewed component meaning; `id` only | `component_type`, `code?`, `label`. Shared labels do not prove shared component identity |
| InteriorComponent / P | One component role in a model interior; `id`, `(model_interior_id, component_id, role)` | `role` seat/color/suede/stitch/two-tone or explicitly reviewed source type; `sequence`, `active`, `rate_context_id?`. No duplicate membership. Shared memberships can be consolidated only after dependency review |
| PriceContext / P | One explicit basis/currency/trim context; `id`, `(basis, currency, trim_scope)` once resolved | `basis` meaning from §3; `currency` required before new price acceptance; `trim_scope` explicit any or a Trim FK, never SQL-null wildcard. Source-only unresolved prices remain candidates |
| Price / P | One amount for typed subject and context in the catalog revision; `(subject_id, context_id)` | `amount` exact decimal, `value_state` priced/unpriced. Amount is present only for priced. Subject is Variant, Offering, ModelInterior or ComponentDefinition; no context-free overwrite |
| ComponentRateReference / P | One source rate key; `(component_type, code, trim_scope, currency)` | Resolved `component_id`, `price_context_id`. Preserves PriceRef type normalization, code and universal-trim fallback without conflating a rate code with an offering ID |
| InteriorPricePolicy / P | One model interior's composition policy; `model_interior_id` | `stored_price_context_id`, `base_seat_rate_id?`, `r6x_seat_rate_id?`, `seat_deduction_mode`. Explicit R6X delta and selected-seat deduction replace ID-string inference only after parity |
| PackagePricePolicy / P | One package pricing interpretation per scope; `(package_offering_id, scope_id)` | `mode` direct/conditional-component; `base_selection` current minimum-positive-component-total rule where applicable; ordered component-price memberships link the conditional price rules. Preserve inferred current behavior as reviewed migration policy, not new automatic heuristics |

No cross-model sharing of interior fields is forced by present equality. Candidate shared definitions are reviewed; model ordering, copy and applicability remain contextual. PriceRef blank-trim fallback is explicit. The current generator adds `max(0, R6X seat rate - base seat rate)` to stored interior price, and the browser subtracts the selected seat's resolved price with a zero floor. Preserve each input and operation; a component sum is a different business proposal.

### Typed rules and references

Use a closed **CatalogEntity** identity registry for referenceable rows (model/year, variant, offering, model interior, component, section/context choice, rule, presentation, price and visual rows). `entity_id` is a real FK; each entry has exactly one matching typed subtype, enforced on writes. Relation-specific references also enforce permitted subtype and model/year ownership. A loose `target_type + target_id` string pair is insufficient. The registry is identity plumbing, not a generic property/value catalog.

| Relation / owner | Grain/key | Fields and constraints |
|---|---|---|
| Rule / P; explanation E | One authored rule; `id` | `model_year_id`, `kind`, `scope_id`, `sequence`, `active`, `explanation?`. Kind has exactly one typed rule subtype. Raw source text belongs in Evidence; it is not executable |
| Scope / P | One applicability set; `id` | For each axis: `axis`, `mode=all/members` and typed member FKs in ScopeMember, key `(scope_id, axis, member_id)`. Membership/axis compatibility and nonempty explicit sets enforced |
| DirectRule / P | One Rule; `rule_id` | `source_entity_id`, `target_entity_id`, `effect=requires/includes/excludes`, `runtime_action?=replace`. Preserve directed edges. Exclusion does not imply replacement |
| GroupRule / P; label E | One Rule; `rule_id` | `display_label?` authored group name; `source_entity_id`, `effect=requires/excludes/includes`, `member_logic=any/all`. Baseline types observed are requires_any/excludes_any; do not enable other semantics without supporting facts |
| RuleMember / P | One group target; `(rule_id, target_entity_id)` | `sequence`, `active`; member target subtype and scope must be valid |
| ExclusiveGroup / P; label E | One group in model/year; `id` | `model_year_id`, `display_label?`, `selection_mode=at_most_one/exactly_one`, `active`; ExclusiveMember key `(group_id, offering_id)`, fields `sequence`, `active` |
| ConditionalPriceRule / P | One Rule; `rule_id` | `condition_entity_id` constrained to Offering or ModelInterior, `target_offering_id`, `price_context_id`, `amount`, `effect=override`. Explicit sequence retains first matching rule precedence. B confirmed interior-triggered seatbelt prices in the frozen workbook and `inspection.py:build_draft_price_rules`; the earlier offering-only condition was too narrow |
| DefaultRule / E+P | One Rule; `rule_id` | `target_offering_id`, `condition_kind`, typed condition relation, `display_behavior?`, `priority`. Kinds: always, unless selected code, unless selected section, when selected offering unless user choice in target section. Code predicate retains code-matching behavior; never selects an arbitrary offering for a nonunique RPO |
| Default condition subtypes / E+P | Exactly the matching subtype for each default rule | Always has no operand; code has `code`; section has `section_id`; when-selected has `condition_offering_id`, `target_section_id`. Resolve current target section behavior per variant before replacing runtime derivation |
| ColorRule / P | One Rule; `rule_id` | `model_interior_id`, `condition_offering_id`, `added_offering_id`, `effect=requires`. Source `adds_rpo` actually names an option ID. Keep a distinct interior + option condition |
| DerivationPermission / P | One allowed derived replacement; `(model_year_id, source_offering_id, target_offering_id, method)` | `method` identified derivation algorithm; supporting primitive rule evidence. Only the five observed approved Z06 pairs initially qualify; derived candidates are not automatically authorized |

Rule explanation view: model/year, condition, effect, targets, scope, order, customer explanation, evidence, authored/derived origin. Editing uses typed fields with names, not manually authored prose or expressions. Independent requirements compose with ALL; requires-any members retain ANY; includes means automatic inclusion. Preserve default restoration, automatic inclusions, exclusive-peer suppression and replacement transitions, not just final valid/invalid states. Cycle/contradiction behavior needs executable characterization in D; this specification is not proof those cases are correct today.

### Presentation, evidence and release

| Relation / owner | Grain/key | Fields and meaning |
|---|---|---|
| ModelPresentation / E | One ModelYear; `model_year_id` | `model_label`, `dataset_name`, `export_slug`, `setup_card_subtitle`, `setup_eyebrow`, `setup_title`, `setup_description`; ModelFact `(model_year_id, sequence)` carries `text` for ordered setup facts |
| PublicationSelection / E, artifacts R | One ModelYear in a release selection; `(release_id, model_year_id)` | `registry_key`, `promoted`, `default_model`, `active`, `sequence`, `legacy_alias?`. Exactly one default among enabled promoted models. Artifact locations are generated release outputs, not product facts |
| Section / E+P | One section definition; `id`, `section_key` | `name`, `selection_mode`, `required`, `standard_behavior`, `sequence`, `step_key`. Group/selection semantics require P review; editorial labels E |
| SectionPresentation / E | One model/year/section placement; `(model_year_id, section_id)` | `display_label`, `step_key`, `display_behavior?`, `sequence`, `standard_equipment_bucket?`, `standard_equipment_group_type?`, `auto_added_bucket?`, `active` |
| OfferingPresentation / E | One offering's base placement/copy; `offering_id` | `section_id`, `label`, `description?`, `sequence`. Keep contextual copy even when currently equal to shared definition text |
| RuntimeStep / E | One step per model/year; `(model_year_id, step_key)` | `label`, `sequence`, `active`; source marker retained in evidence |
| ContextSection / E+P | One model/year/context type; `(model_year_id, context_type)` | `section_id`, `name`, `selection_mode`, `choice_mode`, `required`, `standard_behavior`, `sequence`, `step_key`, `step_label`, `active` |
| ContextChoice / E+P | One setup value/body context; `id`, `(model_year_id, context_type, value, body_scope)` | `value` typed trim/body token; `body_scope` explicit any or BodyStyle; `info_tooltip?`, `active`. Consumer identity retained for asset assignments |
| SummarySection, StepSummary / E | `(model_year_id, section_key)` and `(model_year_id, step_key)` | First: `label`, `sequence`, `active`; second: `section_key` FK, `active`. Each step maps to at most one summary section |
| InteriorPresentation / E | One ModelInterior; `model_interior_id` | `seat_label`, `color_family`, `material_family`, `variant_label`, `group_sequence`, `material_sequence`, `choice_sequence`, `parent_group_label?`, `leaf_label`, `reference_order?` |
| HierarchyNode, InteriorHierarchyMember / E | One contextual hierarchy node; `id`; membership `(model_interior_id, position)` | Node: `model_year_id`, `parent_node_id?`, `label`, `sequence`; membership: `node_id`, `position`. No cycles; membership path must follow parent links. Generate hierarchy arrays for output |
| SourceDocument / I | One immutable byte object; `id`, `sha256` | `original_name`, `media_type`, `byte_length`, `original_location`, `attributed_publisher?`, `model_year?`, `acquired_at?`, `observed_at`, `publication_date?`, `revision_label?`, `supersedes_document_id?`. Unknown dates stay null; supersession requires evidence and scope |
| Evidence / I | One located statement; `id`, `(document_id, locator, fragment_key)` | `locator` sheet/cell/range or PDF page/table/bounds; `raw_text`, `raw_runs?`, `source_headers`, `source_ordinal`, `revision_scope?`, `effective_text?`. Fragment key separates multiple assertions/notes in a cell; source bytes remain the authority for exact representation |
| FactEvidence / I + accepting owner | One evidence link; `(entity_id, field_name, evidence_id, role)` | `field_name` must exist on that entity subtype; `role=supports/contradicts/derivation_input`, `decision_id?`. Field links distinguish price from copy ownership; relationship facts use their own entity identity |
| IntakeRun, Coverage, Candidate, Decision / I | Specified in §6 | Review workflow records, separate from accepted catalog; never used as a fallback business database |
| CatalogRevision / R | One accepted atomic change; `id` | `parent_revision_id?`, `accepted_at`, `actor`, `decision_ids`, `change_summary`. Typed row history/diffs must reconstruct immutable revisions; physical version-storage design deferred |
| Release / R | One immutable generated candidate; `id` | `catalog_revision_id`, `contract_version`, `generator_version`, `artifact_hashes`, `created_at`, `status=candidate/failed/published/retired`. Published release pointer changes atomically only after candidate succeeds; previous release remains reproducible |

Relations represented by ordered memberships in the logical model remain relational even when a release exports arrays. Evidence metadata and immutable review payloads may preserve original structured content; they are not an alternative place to author product rules.

### Dependencies and lossless migration

Natural keys above and surrogate IDs determine only attributes at that row grain. In particular, ModelYear determines year/model, Offering determines model/year and definition, and Variant determines trim/body/model/year; Availability stores none of their repeated names or prices. Component identity does not determine price without its price context. A source hash/location determines evidence, not product identity.

Preserve the link when splitting a row: legacy option → Offering → OfferingPolicy/Presentation/Price/Availability. Rejoining at the declared keys must yield one original offering row and the original availability memberships, without multiplication. Interior memberships must retain model and trim while shared definition candidates are reviewed. Merging repeated descriptions is optional; losing applicability to reduce row count is unacceptable.

The current registered interior key includes trim even though `(model_key, interior_id)` is unique in this snapshot. Keep the wider business key. Proposed natural keys are domain contracts to validate in B, not proof from one snapshot of all future dependencies. Do not claim formal 3NF for unreviewed shared fields or unresolved future edition semantics.

## 5. Workbook field destinations

All 77 sheets fall into the families below; repeated model-specific families use `model_workbook_sources` assignments, never guessed prefixes. The baseline has identical ordered headers across all 11 registered roles. Model ownership comes from the registry when absent in the row. This mapping covers every observed header, including empty and preserved families.

Common mapping rules: IDs/FKs go to typed identity/membership or LegacyMapping; `active` goes to that row's lifecycle, never an unrelated parent; `display_order` and named orders go to explicit contextual sequence. `notes`, `note`, source markers and original wording become non-executable Evidence linked to the affected row. Their ownership is I for originals, E for newly authored notes. No field is silently discarded because it is blank today.

| Source family | Exact fields → destination / meaning |
|---|---|
| model_master | `model_key`, `model_year` → Model/ModelYear; `registry_key` → PublicationSelection + legacy namespace; `model_label`, `dataset_name`, `export_slug`, `setup_card_subtitle`, `setup_eyebrow`, `setup_title`, `setup_description` → ModelPresentation; `setup_fact_1`, `setup_fact_2`, `setup_fact_3` → ordered ModelFact; `expected_variant_count` → retained baseline expectation, derive future count; `default_model` → PublicationSelection; `active` → ModelYear; `notes` → Evidence |
| model_registry_promotion | `model_key`, `registry_key`, `promoted_to_runtime`, `default_model`, `legacy_alias`, `active`, `display_order` → PublicationSelection; `artifact_path`, `artifact_type` → retained legacy release mapping, future Release artifacts; `notes` → Evidence. Conflicting default flags require review, no last-row winner |
| model_workbook_sources | `model_key`, `source_role`, `sheet_name`, `active`, `notes` → baseline source assignments/evidence retained for import trace. No workbook-sheet routing in the future catalog runtime |
| model_variants | `model_key`, `variant_id` → Variant ownership + legacy mapping; `display_order` → contextual VariantPresentation order; `active` → variant membership evidence/lifecycle; `notes` → Evidence |
| variant_master | `variant_id`, `model_year`, `trim_level`, `body_style` → Variant and references; `display_name`, `display_order` → VariantPresentation; `base_price` → Price with baseline_total basis; `active` → Variant. Preserve both membership/master activation and ordering if unequal; effective behavior requires consumer characterization |
| six options sheets | `option_id` → legacy Offering mapping; `rpo` → OfferingCode (legacy-unspecified); `price` → offering Price; `option_name`, `description` → OfferingPresentation and proposed shared-definition evidence; `detail_raw` → Evidence; `section_id`, `display_order` → OfferingPresentation; `selectable`, `display_behavior` → OfferingPolicy; `active` → Offering |
| six OVS sheets | `option_id`, `variant_id`, `status` → Availability and exact legacy references |
| six variant overrides | `option_id`, `variant_id`, `selectable`, `display_behavior`, `section_id`, `active` → VariantPresentationOverride; `note` → Evidence |
| six direct-rule sheets | `rule_id` → Rule + legacy mapping; `source_id`, `rule_type`, `target_id`, `runtime_action` → DirectRule; `body_style_scope` → Scope; `disabled_reason` → Rule.explanation (does not disable); `original_detail_raw` → Evidence; current row order → sequence. No authored active column: retain source-family behavior rather than invent deactivation |
| six group headers | `group_id` → Rule identity; `display_label` → contextual group label; `group_type`, `source_id` → GroupRule; `body_style_scope`, `trim_level_scope`, `variant_scope` → Scope; `disabled_reason` → explanation; `active` → Rule; `notes` → Evidence |
| six group-member sheets | `group_id`, `target_id`, `display_order`, `active` → RuleMember |
| six exclusive headers/members | Header `group_id`, `display_label`, `selection_mode`, `active` → ExclusiveGroup; `notes` → Evidence. Member `group_id`, `option_id`, `display_order`, `active` → ExclusiveMember |
| six price-rule sheets | `price_rule_id`, `condition_option_id`, `price_rule_type`, `target_option_id`, `price_value` → ConditionalPriceRule; `body_style_scope`, `trim_level_scope` → Scope; `notes` → Evidence; original order → sequence |
| default_selection_rules | `model_key`, `rule_id`, `target_option_id`, `condition_type`, `condition_id`, `priority`, `display_behavior`, `active` → DefaultRule and matching typed condition; `body_style_scope`, `trim_level_scope`, `variant_scope` → Scope; `notes` → Evidence |
| lt_interiors, LZ_Interiors | `interior_id` → legacy interior identity; `Interior Name`, `Material`, `Seat`, `Interior Code`, `Suede`, `Stitch`, `Two Tone`, `requires_r6x` → InteriorDefinition/component facts after explicit decomposition; `Price` → model-interior stored Price; `Trim` → ModelInterior/price context (including explicit R6X context); `section_id`, `included_option_id` → ModelInterior; `active_for_stingray` → retained legacy eligibility evidence, reconcile with ModelInterior scope; `Detail from Disclosure`, `Color Overrides` → raw evidence. Color Overrides text is not a replacement for executable color rows |
| model_interior_scope | `model_key`, `interior_id`, `trim_level`, `active`, `requires_option_id` → ModelInterior; `interior_seat_label`, `interior_color_family`, `interior_material_family`, `interior_variant_label`, `interior_group_display_order`, `interior_material_display_order`, `interior_choice_display_order`, `interior_parent_group_label`, `interior_leaf_label`, `interior_reference_order` → InteriorPresentation; `interior_hierarchy_levels` → HierarchyNode/ordered membership plus original evidence; `notes`, `grouping_source` → Evidence |
| interior_components | `model_key`, `interior_id` → ModelInterior; `rpo`, `component_type`, `label` → proposed ComponentDefinition; `price_ref_type`, `price_ref_code`, `price_trim_scope` → ComponentRateReference; `display_order`, `active` → InteriorComponent; `notes` → Evidence. Confirm trim scope when resolving model-interior membership |
| PriceRef | `OptionType`, `Trim`, `Code` → ComponentRateReference/context; `Price` → component Price. Preserve raw type/key plus observed normalizer and blank-trim fallback |
| color_overrides, grand_sport_x_color_overrides | `interior_id`, `option_id`, `rule_type`, `adds_rpo` → ColorRule. Expand only explicitly registered model assignments, preserving shared source evidence |
| section_master | `section_id`, `section_name`, `selection_mode`, `is_required`, `display_order`, `standard_behavior`, `step_key` → Section |
| context_section_master | `model_key`, `context_type`, `section_id`, `section_name`, `selection_mode`, `choice_mode`, `is_required`, `standard_behavior`, `section_display_order`, `step_key`, `step_label`, `active` → ContextSection; `notes` → Evidence |
| section_presentation | `model_key`, `section_id`, `display_label`, `step_key`, `display_behavior`, `section_display_order`, `standard_equipment_bucket`, `standard_equipment_group_type`, `auto_added_bucket`, `active` → SectionPresentation; `notes` → Evidence |
| runtime_steps | `model_key`, `step_key`, `step_label`, `runtime_order`, `active` → RuntimeStep; `source`, `notes` → Evidence |
| context_choice_copy | `model_key`, `context_type`, `value`, `body_style`, `info_tooltip`, `active` → ContextChoice; `notes` → Evidence |
| order_summary_sections | `model_key`, `section_key`, `section_label`, `display_order`, `active` → SummarySection; `notes` → Evidence |
| step_order_summary_map | `model_key`, `step_key`, `section_key`, `active` → StepSummary; `notes` → Evidence |
| asset_map | `model_key`, `target_type`, `target_id` → typed AssetAssignment; `image_url`, `hover_image_url` → Asset/Rendition references; `image_alt`, `image_fit`, `image_position`, `hover_image_alt`, `hover_image_position` → role-specific assignment display fields; `active` → assignment; `notes` → Evidence. Existing cards are not proven visualizer layers |
| rule_phrase_map (6 rows) | `phrase`, `rule_type`, `direction`, `stop_phrases`, `review_flag_default`, `active`, `notes` → historical evidence only. No active parser/generator inferred from this preserved sheet |
| runtime_rule_exceptions (0 rows) | `model_key`, `exception_id`, `source_option_id`, `target_option_id`, `exception_type`, `body_style_scope`, `trim_level_scope`, `variant_scope`, `disabled_reason`, `active`, `notes` → retained empty-schema evidence, no new executable rule family. Future populated input needs explicit classification |

Compatibility facts found in code also need provenance: the five Z06 derived replacement permissions in `rule_derivation.py`, R6X/seat-code inference in `pricing.py` and `interiors.py`, and package-component pricing in `form-app/app.js`. Record their revision/symbol locations and classification as baseline behavior; do not attribute them to the manufacturer or quietly omit them because they are outside the workbook.

September 6 B implementation: the [disposable candidate mapping](../catalog/README.md)
preserves those policies with pinned code evidence. It also distinguishes the
code-owned, nonnavigable `standard_equipment` bucket from authored runtime steps,
and retains wildcard asset scope separately from model overrides. The candidate
is a single frozen model-year import, not the final authoring/release schema.
See its report for complete row accounting; full runtime equivalence remains D.

## 6. Intake, discrepancy and acceptance contract

### Staging records

These are logical records, not parser code or an implemented API.

| Record / key | Fields, meanings and owner |
|---|---|
| IntakeRun / `id`; unique `(document_hash, parser_version, extraction_config_hash)` | I: `document_id`, `parser_version` exact extractor identity, `extraction_config_hash` including selected ranges/family and normalization rules, `started_at`, `status`, `coverage_scope`. Repeating the same run reuses candidates; a new parser/config creates a separate auditable run |
| Coverage / `(run_id, locator)` | I: `expected_region`, `status=processed/partial/unparsed/out_of_scope`, `record_count`, `unresolved_reference_count`, `reason?`. Include headings, footnotes, nonblank cells and relevant hidden/merged content, not just successfully parsed rows |
| Candidate / `(run_id, evidence_id, assertion_kind, assertion_ordinal)` | I: `assertion_kind` closed typed domain operation; `raw_value`, `typed_value?`, `units?`, `applicability`, `source_code_role?`, `target_mapping_id?`, `confidence?`, `parse_issues`, `comparison_class`, `base_revision_id?`. Ordinal separates multiple assertions from one location; target mapping is optional until reviewed, never guessed from RPO |
| SourceIdentityMapping / `(document_id, source_identity_key, target_kind)` | I with P review: `target_entity_id`, `mapping_status=proposed/confirmed/ambiguous`, `reason`, supporting `evidence_ids`. Source identity key retains model/year/code/trim/body and local disambiguators. Across revisions, review the link to stable entity; a shifted row does not create a new product |
| Discrepancy / `id` | I: `candidate_ids`, `current_entity_id?`, `field_name`, `baseline_value`, `proposed_value`, `comparison_basis`, `class`, `cause?`, `evidence_ids`, `status`. A discrepancy may relate several candidate assertions to one fact |
| Decision / `id` | Accepting owner: `discrepancy_ids`, `outcome`, `reason`, `actor`, `decided_at`, `base_revision_id`, `accepted_operations`, `evidence_ids`. Outcome accept guide correction / retain intentional dealer value / reject extraction / defer unresolved / accept nonbehavioral migration representation |

Arrays listed on review records express attached immutable review content or links; referenced evidence/candidates/decisions are addressable relationships. Accepted operations specify entity, field or relationship, previous value, new value and expected revision. They cannot contain arbitrary executable code.

### Processing and conflict rules

1. Register source identity and preserve original bytes in future intake storage. No source copies are made in A. Store acquisition truthfully and label unknowns. Never overwrite an earlier document with a newly downloaded file of the same name.
2. Extract exact cells/text/runs and context into staging. Preserve orderable versus reference-only RPO columns, multi-line variant headings, footnotes, unit/basis distinctions and unparsed text. Price Schedule base MSRP is column F; option MSRP is G. Option column D contains contextual restrictions even though its header is blank. Do not use a global column mapping.
3. Parse typed candidate facts for the selected family. An unrecognized token, unresolved footnote, ambiguous RPO/variant, unknown currency or unclear prerequisite stays unresolved. Parser confidence can prioritize review; it cannot approve a change.
4. Compare at the same identity, field, scope and price basis against the frozen workbook/candidate revision. Classes: unchanged, added, changed, removed, ambiguous, conflicting. Distinguish editorial differences from manufacturer facts. A matching amount at a different basis is not equality.
5. Diagnose differences as manufacturer correction, intentional dealer choice, extraction error, representational difference, or unresolved conflict. The latest date alone does not resolve conflicting facts, and accepting one field does not overwrite all fields on the source row.
6. Removal requires complete relevant source coverage, explicit evidence for the proposed absence/removal, and review. Partial pilot extraction cannot retire outside-family offerings or package members. Retain superseded facts/evidence for prior releases.
7. Preview affected models/variants, prices, rules, customer copy and releases. Accept only a coherent dependency-complete set in one transaction with expected-revision comparison. Stale review requires recomparison; no last-write-wins acceptance. Rejected/deferred candidates remain visible and cannot leak into releases.
8. Same reviewed input/decision cannot apply twice. Acceptance binds candidate identities, operations and base revision. Reprocessing a document after catalog edits requires a fresh comparison, even when extraction was reused.

The current code has first-match pricing and additional package-component price handling **before** ordinary overrides. Preserve that precedence, ordered conditions, inclusion/replacement totals, interior deductions and missing-rate fallbacks in D. Merely preserving the final `price_rules` rows is insufficient.

## 7. Future visualizer and form contracts

Both consumers use one Release and its resolved configuration. No visualizer-owned eligibility, pricing or package resolver. The current `visualizer/visualizer.js` reads `state.selected` and optional `layer_src`/`layer_z`; that is useful reference behavior, not the new contract. `visualizer/export-layers.jsx` demonstrates aligned transparent layers, but no complete scene asset set was established by this inspection.

| Relation / owner | Grain/key | Fields and meaning |
|---|---|---|
| Asset / A | One source artwork identity; `id` | `source_uri`, `content_hash?`, `media_type`, `rights_note?`, `evidence_id?`. Missing hash means unverified remote bytes; publishing visual layers needs fixed content identity |
| Rendition / A | One asset rendition; `id`, `(asset_id, rendition_key)` | `uri`, `content_hash`, `width`, `height`, `format`, `role` preview/export. Dimensions positive; transparent-layer registration explicit |
| AssetAssignment / A+E | One target/role/scope assignment; `(target_entity_id, role, scope_id)` | `rendition_id`, `alt_text`, `fit`, `position`, `active`; roles primary/hover. Targets typed model-year/offering/context choice. Scope explicitly identifies model/body context; overlapping assignments for the same role require an unambiguous resolution before release, not an RPO URL convention |
| Scene / A | One model/year/view/body composition; `id`, `(model_year_id, body_style_id, view_key)` | `view_key` exterior/interior camera identity, `canvas_width`, `canvas_height`, `registration_key`, `active`. Artwork dictates pilot dimensions, not the legacy hardcoded canvas |
| LayerSlot / A | One compositing slot; `id`, `(scene_id, slot_key)` | `slot_key`, `z_order`, `required_for_complete_scene`, `composition_mode=single/stack`. Explicit secondary sequence resolves stacking order; single slots may not have overlapping winning bindings |
| VisualBinding / A | One scoped asset contribution; `id` | `scene_id`, `slot_id`, `rendition_id`, `predicate_id`, `priority`, `sequence`, `active`. One offering may drive several bindings/slots; one rendition may serve many bindings |
| VisualPredicate / A | One structured condition; `id` | `match=all/any`, ordered typed terms for variant/body, resolved offering, interior or component, each with `present/absent`. No free-form script; no price or eligibility effects. Conditions use resolved IDs, not label substrings |
| VisualCoverage / A, evaluation R | One required scene/scope/slot expectation; `(scene_id, scope_id, slot_id)` | `status=verified/missing/unsupported/not_applicable`, `reason?`, `checked_asset_revision?`. Missing artwork is not an unavailable product choice |

Resolved-build output fields and owners: `release_id`, `catalog_revision_id`, `contract_version` (R identity); `model_year_id`, `variant_id`, `interior_id?` (resolved typed identities); `user_selected_ids`, `default_ids`, `included_ids`, `effective_ids`, `removed_or_replaced_ids` (R results with explanation/rule traces); resolved component IDs, line prices and total with basis/currency (R); `scene_id`, ordered layer contributions, coverage gaps (R visual output). These are generated collections, not extra canonical authoring tables.

Before drawing, manifest and form release IDs must match. An option removed by replacement must leave all its layers; defaults and auto-included equipment must appear even when absent from user selections. No suitable scene yields an honest unavailable-preview state with the valid form still usable. Missing/unsupported art never removes a product option or changes total/submission. A partial image export is labeled incomplete rather than silently presented as complete. Asset loading/rights/CORS, alignment, alternative text and reduced-motion behavior are implementation checks for H.

First form parity covers all six legacy model contracts: exact identifiers and meaningful order; body/trim and defaults; available/standard/unavailable status; includes/requires/excludes/replacement and groups; contextual and interior prices; labels, sections, summary, downloads and dealer payload model scoping. Preserve output namespaces through explicit release mappings. Generate directly from catalog facts without reconstructing Excel. No form, viewer, API or renderer is built in A.

## 8. Decisions and implementation boundaries

Owner clarifications received September 5, 2026 (business direction, not a new source inspection or implementation authorization):

- **Authoring:** local, single-user; Sean is the sole developer. Hosted multi-user editing is not a current requirement. Technology choices remain open.
- **Workbook behavior:** existing pricing, availability-condition and rule conflicts are intentional and should be traceable through `stingray_master.xlsx`. Preserve them rather than normalizing away differences. The owner expects the raw export to express the same rules, often through inference and inconsistent or abstract language, and is confident the workbook represents them. This is owner direction, not completed rule-coverage proof.
- **Coverage concern:** specifically reconcile non-LPO options and the listing/display of standard features and trim-level equipment consistently across all six models. Distinguish legitimate model differences from omissions or presentation gaps; present concrete ambiguities after tracing the workbook format and consumers.
- **Policy ownership:** some business policies may still reside in 27vette runtime code. Trace those during B/D so they can become explicit data-owned rules in the future catalog. The stated goal of complete workbook ownership does not authorize modifying the reference workbook or runtime here, or change the planned relational-catalog destination. Preserve current behavior and surface any policy that cannot be traced to workbook data.
- **Manufacturer refresh:** Sean plans to supply an updated raw export with the July 26 price schedule and the order guide for the week of September 7, 2026. These are forthcoming source editions, not files inspected by this specification; retain the existing evidence and hashes. Verify exact document date labels, acquisition metadata and currency on receipt.
- **Stingray brakes:** owner confirms JL9 is standard; J55 is included with and only available with Z51, and replaces JL9. Use this interpretation in the proposed bounded intake pilot, with source citations and workbook/runtime tracing still required.
- **Visualizer:** the owner reports unprocessed `.psb` files in a local folder. Asset inspection and processing will be part of a later task; the files have not been inspected in this clarification task.

| Remaining decision or evidence | Consequence / when required |
|---|---|
| Updated guide delivery, exact revision labels, acquisition history and price currency | Verify in C before monetary acceptance or revision-precedence decisions; the promised update does not overwrite inspected source evidence |
| Authorization for the proposed Stingray brake-family intake pilot | Brake semantics are clarified; C still requires its own authorized task and bounded coverage |
| Shared option/interior/component identity and any unresolved copy/default/pricing interpretation | B keeps conservative identities and intentional behavior. Trace workbook sheets before presenting specific ambiguities; merges or behavior changes require P/E decisions. No majority-value normalization |
| Previously unrepresented edition/variant dimensions, unknown price bases or unresolved source restrictions | Investigate the format and related sheets first; stop only the affected mapping and present evidence if ambiguity remains |
| Code-owned policies and exact field override precedence | Trace 27vette read-only and confirm current behavior with targeted fixtures in B/D; identify data-ownership gaps without silently changing business behavior |
| Available art, rights and first exterior/interior scene | Unprocessed local `.psb` files reported; inspection, processing, rights and scene selection remain for a later task in H. No assumption that existing images provide compositing coverage |

These decisions do not prevent completing the specification. They prevent particular acceptance/implementation choices, as stated. No new approval mechanism, enforcement script, standalone progress PR or application framework is proposed.

## 9. Evidence and validation

Performed read-only for A:

- Read README, roadmap and historical audit; inspected all workbook headers and guide sheet/cell structure with bundled Python, plus guide rich-text XML for the pilot. Source counts and hashes above come from current reads, not historical claims.
- Rechecked all 66 source-role assignments: identical ordered headers within all 11 roles; the sum of each model's offering × variant combinations yields 7,448 explicit availability pairs from 1,379 offerings and 32 variants, with zero missing, extra or duplicate pairs across six models.
- Traced the shared assembly and runtime boundary in `scripts/corvette_form_generator/source_assembly.py`; component/seat pricing in `pricing.py`; approved derivation permissions in `rule_derivation.py`; and first-match/package-component/default logic in `form-app/app.js`. Inspected visualizer selection and layer-export assumptions.
- Inspected guide pilot cells and their workbook counterparts, source legend and price headers/notes. Verified that 71,000 + 2,495 = 73,495 and Z51's sampled 5,395 amount matches. Neither observation accepts a guide correction.
- Final readback confirmed both Excel hashes unchanged and the reference checkout clean at the same HEAD. No 27vette file was modified. Confirmed `.local/STATUS.md` is ignored by Git in CorvetteCatalog.

Not performed: application/database/schema creation, parser pilot execution, canonical import, full guide semantic reconciliation, frozen six-model runtime parity, exhaustive key/FD/cycle/price validation, browser/Excel visual testing, remote art inspection, publication or deployment. A broad 27vette test/generator run would not validate these documentation changes and could rewrite unrelated artifacts; it was intentionally not run.

Implementation validation belongs with affected behavior: B accounts for every baseline row and mapping and proves constrained joins; C checks exact extraction/footnote coverage and idempotent comparisons on the chosen family; D proves rule/price/ordering and submission parity with representative transition cases; H checks resolved-build layers against matching releases. No extra documentation-only gate is required.
