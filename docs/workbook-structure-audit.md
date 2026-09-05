> Historical reference: read-only audit of the existing 27vette workbook. Its recommendations to retain Excel authority are superseded for this proposed new project by `migration-plan.md`. No existing-project authority has changed.

# Canonical workbook structure audit and relational plan

Audit date: September 4, 2026. Scope: read-only structural analysis of `/Users/seandm/Projects/27vette/stingray_master.xlsx` and its current consumers. No workbook, application, generated artifact, or repository file was changed.

## Recommendation

Organize canonical data by entity and relationship, with one schema per family across all models. Keep model-oriented screens and comparison grids as views over those tables. Preserve the workbook as the canonical store during this refactor; making a database canonical is a separate architectural decision.

The workbook is already partly relational. The highest-value improvement is to separate shared definitions from model applicability and presentation. Simply stacking all model sheets into larger sheets would improve consistency but would not, by itself, establish third normal form (3NF).

A practical 3NF design gives each table a declared row meaning and candidate keys, removes repeating values that represent relationships, and places attributes with the key that determines them. Microsoft provides a useful description of these principles in [Database design basics](https://support.microsoft.com/en-us/access/database-design-basics). Repeated labels are evidence to investigate, not automatic proof that two business entities are identical. A snapshot can demonstrate current agreement; business ownership must establish whether that agreement is an invariant.

## What the workbook actually contains

The audit inspected every populated sheet, its headers, values, tables, validation objects, freeze panes, formulas, and model-source mapping.

| Model | Variants | Options | Availability rows | Direct rules | Rule groups | Price rules |
|---|---:|---:|---:|---:|---:|---:|
| Stingray | 6 | 242 | 1,452 | 178 | 27 | 52 |
| Grand Sport | 6 | 241 | 1,446 | 157 | 49 | 55 |
| Grand Sport X | 6 | 239 | 1,434 | 144 | 43 | 51 |
| Z06 | 6 | 244 | 1,464 | 110 | 35 | 72 |
| ZR1 | 4 | 207 | 828 | 98 | 5 | 34 |
| ZR1X | 4 | 206 | 824 | 96 | 4 | 33 |
| **Total** | **32** | **1,379** | **7,448** | **783** | **163** | **297** |

There are **77 sheets and 15,134 populated data rows**, excluding headers and empty rows. The workbook contains no Excel formulas and no merged ranges. Its complexity comes from stored data and the relationships interpreted by code.

All **11 registered source roles have identical ordered headers across their six model assignments**. This includes options, availability, direct rules, price rules, group headers/members, exclusivity, variant overrides, color overrides, and interiors. Some assignments intentionally share a physical sheet. Nine families occupy six separate model-specific tables each: **54 physical sheets** before shared metadata and interiors are counted.

All availability tables exactly match their model's option × variant combinations: no missing pairs, extra pairs, or duplicate pair keys. Their 7,448 rows are legitimate relationship records. They should be easier to edit through a matrix, but should not be removed merely to lower row counts.

The 32 variant IDs each belong to one model in this snapshot. Each `(model_key, interior_id)` is also unique in the 704-row interior-scope table, although the registered key additionally includes trim.

## Findings and implications

### 1. Physical distribution is inconsistent; family-level column parity is already good

Stingray's direct rules are in `rule_mapping`; Grand Sport uses `grandSport_rule_mapping`; Grand Sport X uses `grand_sport_x_rule_mapping`. Group-member naming similarly differs: `rule_group_members`, `grandSport_rule_group_members`, and `grand_sport_x_rule_members`.

The `model_workbook_sources` table correctly records 66 model/role assignments, so consumers do not need to guess names. Preserve this explicit mapping during migration. Long term, replace repeated per-model tables with shared family tables and explicit model ownership. Do not make cosmetic sheet renaming the first migration.

### 2. Option identity, business terms, and presentation share the same row

Each option row currently combines its ID/RPO, name, description, original detail, price, section, selection behavior, order, and activation. Shared identity and copy are repeated with model-specific placement and behavior.

Across 1,379 rows, there are 434 distinct existing option IDs, 319 nonblank RPOs, and 155 rows without an RPO. There are 410 distinct `(rpo, option_name, description)` tuples, leaving 969 repetitions of that tuple. These are reuse candidates, **not 969 deletable options**. Different applicability, price, order, lifecycle, and business meaning must survive.

Do not use RPO as the primary key. `grandSport_options` rows 74 and 126 both contain T0E, but one is inactive/nonselectable and the other is active/default-selected with different placement. Existing IDs are also reused across models, so migration joins must initially use `(model_key, legacy_option_id)`.

Do not assume a shared price or identical behavior from an identical ID. R6X is `auto_only` across all six models, but its stored `selectable` value differs. That is a review candidate, not evidence authorizing correction.

### 3. Interiors offer the clearest normalization opportunity

`lt_interiors` and `LZ_Interiors` hold 262 combinations in matching 16-column schemas. `model_interior_scope` adds 704 model/interior associations in 18 columns, mixing eligibility with labels, ordering, hierarchy, and provenance. `interior_components` adds 1,044 rows with model, component identity, repeated labels, pricing references, order, and notes.

Ignoring model and notes and treating equivalent text/native scalar values consistently, the 1,044 component rows collapse to **395 distinct records**. More specifically, for the observed `(interior_id, rpo, component_type)` groups, label, price-reference type/code/trim, display order, and activation do not conflict between models. This is strong evidence for separating shared component definitions from applicability. The number of applicability relationships need not fall when descriptive duplication is removed.

Likewise, interior trim, seat label, color family, material family, and leaf label currently agree across models for each interior ID. These are candidate shared attributes; group order and other presentation decisions still need their own dependency review.

There are **704 JSON hierarchy arrays** in `model_interior_scope.interior_hierarchy_levels`. For an explicitly relational authoring structure, store hierarchy nodes and ordered membership, then generate display paths. Do not make people edit JSON alongside the labels that it repeats.

The interior source sheets also contain 70 comma-separated `Color Overrides` cells, while executable color relationships are separately represented by 831 rows across two `color_overrides` sheets. The text is emitted as raw metadata; it must not be mistaken for the sole executable rule source. Establish one canonical relationship and derive any display list only after consumer parity is demonstrated.

### 4. Rule representation is structured but fragmented

Business behavior is distributed across direct rules, rule groups and members, exclusive groups and members, price rules, default-selection rules, variant overrides, color overrides, and interior requirements. These represent genuinely different operations; combining them into one sparse table with generic text conditions would make entry harder.

Several specific readability problems can be improved:

- `disabled_reason` means the explanation shown when a choice is unavailable; it does not deactivate the rule. Group rows can have both `active=True` and a populated `disabled_reason`.
- `color_overrides.adds_rpo` actually contains option IDs such as `opt_d30_001`, not literal RPO codes. A future schema should call this `added_option_id`; the current editor can immediately explain it more clearly.
- All 783 direct-rule body-style scopes are blank. Group scopes use both blanks and `*`; pricing scopes also mix uppercase and lowercase trim values. Empty columns are not automatically obsolete capabilities.
- `original_detail_raw` is populated on 611 direct-rule rows but contains only 137 distinct texts. Evidence statements can be stored once and linked to the rules they support, retaining source location and revision.
- Source row order can matter: `form-app/app.js` returns the first matching price override. Sorting during migration can silently change prices unless order or precedence is represented and tested.

Provide one joined rule-review view with **model, condition, effect, target(s), scope, order/priority, customer explanation, evidence, and authored/derived status**. Keep separate typed editing forms behind that view. For example, the Stingray group at `rule_groups!A2:J2` can read: “When 5V7 is selected, require at least one of 5ZU or 5ZZ.” The member relationships remain structured rows; the sentence is generated.

Preserve ALL versus ANY, required versus included, ordinary exclusion versus replacement, and exactly-one versus at-most-one. Flattening these distinctions would change the form.

### 5. Pricing needs an ownership map before decomposition

Prices are authored in variant base prices, model option prices, conditional price rules, interior source totals, and `PriceRef` component rates. These are different price grains, not automatically conflicting copies.

`pricing.py` computes an interior's generated price from its stored price plus an R6X seat delta. `interiors.py` separately resolves component prices through `PriceRef`. The browser then subtracts the selected seat's resolved price from the interior price. A component sum must not replace the current total without reconciling that full path and preserving rounding, zero, missing-value, and inclusion behavior.

`PriceRef.Trim` being blank is a deliberate universal fallback. `price_ref_component_price()` checks a trim-specific price first, then the blank-trim fallback, then returns zero. Define these semantics explicitly in the target model and flag unresolved prices separately from an intentional zero, without changing current customer totals during migration.

### 6. Some business behavior still depends on code conventions

The workbook is the declared authority, but a complete ownership audit must include existing exceptions:

- `rule_derivation.py` has five approved Z06 replacement pairs in `EMISSION_ALLOWLIST`. The general graph calculation can remain code; these model-specific emission permissions are candidates for workbook-authored policy in a separately approved slice. Do not enable all derived candidates while normalizing.
- `interiors.py` derives R6X behavior from trim/ID strings and derives a seat code from the first token of a label. `pricing.py` also interprets R6X in identifiers. Future facts should be explicit relational values, with the same emitted behavior verified before removing these conventions.

`rule_phrase_map` has six preserved rows and `runtime_rule_exceptions` is empty; neither currently has an active generation path. Label these as historical/preserved surfaces. Do not resurrect them as a new rule system or delete them without a retention decision.

### 7. Excel entry controls are uneven, with a confirmed misplaced dropdown

Only **11 sheets have Excel Tables**, and only **six sheets have any data-validation objects**. One of those objects has no validation type. Seventeen sheets have no frozen panes. `PriceRef` is hidden.

Confirmed examples:

- `section_master!G2:G48` has the list `locked_included,replaceable_default`, but G is `step_key`; the matching semantic field is F, `standard_behavior`. The sheet's last data row is 49, outside that validation range. This is a metadata/entry-control defect even though schema validation passes.
- `stingray_ovs` freezes at `A1605` although its last populated row is 1453. Other examples are `grandSport_options!A208`, `z06_options!A107`, and `grand_sport_x_options!A44`. These settings freeze far more than a header.
- Grand Sport's price-rule reference validation covers only rows 3–26 of a sheet with data through row 56. Its options section-reference validation skips row 173 and extends beyond populated data.
- `model_interior_scope.active` contains 392 text values and 312 native Booleans. `interior_components.display_order` contains 592 strings and 452 integers; its activation values have the same text/Boolean split. The consumers currently normalize these successfully.

These are useful improvements independent of a relational redesign. This audit inspected stored Excel metadata; it did not operate Excel or visually test the resulting viewport.

## Proposed relational organization

Names below describe a target, not approved new workbook sheets or a finalized migration contract. One table should represent one entity or relationship. Keep model/year identity explicit: the current workbook contains MY2027 only, so a multi-year catalog should be added only if required.

| Domain | Proposed tables and row meaning | Current sources |
|---|---|---|
| Models | `models`: one model/year record; `model_copy`: model-specific presentation; `model_facts`: one ordered card fact; `publication`: one model's publishing configuration | `model_master`, `model_registry_promotion` |
| Variants | `variants`: one model/trim/body configuration and its base price; trim/body reference tables; separate ordered membership only if a variant can genuinely belong to multiple models | `variant_master`, `model_variants` |
| Option definitions | `option_definitions`: one approved shared identity and intrinsic attributes; keep RPO nullable/nonunique | Six options sheets |
| Model offerings | `model_options`: one option offered by one model, preserving its legacy runtime ID, model-specific price, lifecycle, and selection behavior; `option_presentation`: contextual placement/order/copy where these depend on presentation context | Six options sheets and variant overrides |
| Availability | `option_variant_status`: one model offering and one compatible variant, with exactly one status; variant-specific overrides keyed by that same relationship | Six OVS sheets, six override sheets |
| Interiors | `interior_definitions`: one explicit combination; `model_interiors`: applicability; `interior_component_members`: combination-to-component relationship; component definitions and rates stored at their own actual grain | LT/LZ interiors, scope, components, `PriceRef` |
| Interior display | Shared hierarchy/group definitions, model-specific group placement, and ordered interior membership; generate hierarchy arrays/paths | Presentation columns in `model_interior_scope` |
| Rules | Shared rule metadata plus typed direct, group, exclusivity, pricing, default, and color-rule relations; explicit members and scope relationships | Existing rule families |
| Form layout | Section and step definitions, model layout assignments, context sections, summary sections and mappings; overrides only where independently authored | `section_master`, runtime/context/presentation/summary sheets |
| Assets | Asset identity/URL, with model/target/role assignments and contextual alt text/crop settings | `asset_map` |
| Evidence | Source statements and precise origin/revision, linked to facts/rules; preserved historical metadata isolated from executable facts | Detail, notes, grouping provenance, preserved sheets |

A concrete core could use these keys:

```text
models(model_id PK, model_key, model_year, UNIQUE(model_key, model_year))
variants(variant_id PK, model_id FK, trim_id FK, body_style_id FK,
         base_price, UNIQUE(model_id, trim_id, body_style_id))
option_definitions(option_definition_id PK, rpo, intrinsic_name, ...)
model_options(model_option_id PK, model_id FK, option_definition_id FK,
              legacy_option_id, model_price, ...,
              UNIQUE(model_id, legacy_option_id))
option_variant_status(model_option_id FK, variant_id FK, status,
                      PK(model_option_id, variant_id))
```

Require the offering and variant to belong to the same model. An Excel-backed implementation needs a cross-table validator for this constraint; individual foreign-key existence checks are insufficient. Additional trim/edition distinctions must be incorporated before adopting the proposed variant uniqueness constraint if the domain later needs them.

For each proposed relation, the design specification must list all candidate keys and functional dependencies, not merely introduce a surrogate ID. Check that every nontrivial dependency meets 3NF, that splitting the table can be joined back without lost or multiplied facts, and that necessary constraints remain enforceable.

Examples to resolve explicitly:

- If option copy is intrinsic to a definition, store it there. If it differs legitimately by model, put the contextual copy in the model presentation relation; do not overwrite the common definition.
- If `variant_id` uniquely owns its model, do not copy model name/year into every availability row.
- If component labels/rates depend on component and pricing context, store them at that grain rather than on every model/interior membership.
- If section labels are contextual editorial choices, equal current text does not make them one global fact.
- A generic `target_type + target_id` column does not provide a real foreign key by itself. Choose typed references or a validated entity supertype for rule and asset targets; preserve option-versus-interior identity. That design decision belongs in the specification.
- Represent multi-value rule scope as member rows. Distinguish “all present and future variants” from an explicit frozen variant set. Preserve current wildcard expansion semantics and require an impact preview when adding a model or variant.

Avoid replacing model duplication with an inheritance chain such as Stingray → Grand Sport → Grand Sport X. It would make exceptions harder to locate. Shared definitions plus explicit applications and shallow, documented contextual overrides are easier to audit.

## Human entry should remain model-oriented

The canonical tables can be normalized without making users manually traverse every join. Use the existing Workbook Manager as the primary editing surface and provide:

- A model workspace showing effective options, placement, availability, price, and rules together.
- A shared-definition editor with a preview of every affected model before saving a shared change.
- An availability matrix for entry, persisted as ordinary relationship rows.
- A rule builder for each supported effect, with searchable named targets and a generated sentence.
- An interior editor separating the combination, eligible models, component pricing, and display grouping.
- Cross-model comparison showing inherited/shared values, explicit contextual values, and differences needing review.

Joined views must be read-only unless every editable field maps unambiguously to one canonical row. All writes continue through the existing draft, reviewed ChangeSet, safe-save, and Apply/Rebuild path. Do not allow independently writable model views and canonical tables to become competing authorities.

For direct Excel use, put an index/data dictionary first, group tabs by domain, apply uniform table styles and bounded reference validation, freeze headers/identifiers consistently, and distinguish inputs from generated review columns. Familiar display labels can differ from stable machine column names without renaming the contract.

## Staged plan

### Stage 1 — Approve the data model on evidence

Produce a field-by-field source-to-target mapping, entity/relationship diagram, candidate-key and dependency inventory, null/wildcard dictionary, and ownership map for every price and rule mechanism. Classify each repeated value as shared fact, legitimate contextual override, independent copy, derived output, or historical evidence. Record unresolved business decisions instead of inferring them.

Acceptance: every current field has a destination or explicit retention decision; every rule type and price path has a preserved interpretation; no identifier merges rely only on RPO or matching text. This is the recommended next bounded task.

### Stage 2 — Improve entry safety independently

In a separate approved change, repair the misplaced/partial validation ranges and freeze panes, expose useful registry-owned field descriptions, and standardize typed values using the existing write contract. Add a report for cross-model parity and suspicious differences, with intentional differences recorded explicitly. Preserve field names and runtime meanings.

Acceptance: saved-workbook package/schema checks pass, targeted Excel metadata checks prove correct headers/ranges, and affected generated outputs remain unchanged where the edits are representational only. Excel usability still needs visual verification.

### Stage 3 — Prove one normalization slice on a disposable copy

Pilot shared interior-component definitions and model applicability. The observed 1,044-to-395 descriptive repetition makes this a useful bounded experiment. Preserve exact applicability and all pricing inputs; do not redesign price arithmetic in this slice.

Create a temporary relational projection and a reversible mapping to existing identifiers. Use it to reconstruct the current family input through an isolated adapter and prove semantic readback and generated parity. This is an experiment, not permission to feed a disposable export into production generation.

Acceptance: no lost/extra memberships, identical component labels/order/prices, exact legacy-ID mapping, and unchanged generated contracts across all six models. Stop at this checkpoint before migrating another domain.

### Stage 4 — Consolidate offerings and availability

After approving the schema and shared-identity map, introduce common family tables, migrate explicit model ownership, and separate option definitions from model offerings. Retain the complete availability relationship and update the registry, schema validator, editor ownership/reference rules, Manager projection, and generator together.

Acceptance: exact option/variant coverage, preserved inactive history, contextual pricing and selection behavior, and cross-model references rejected. Do not cut over simply because row counts reconcile.

### Stage 5 — Normalize rules, pricing, and presentation by family

Move evidence out of repeated rule text; make scope, precedence, lifecycle, and typed targets explicit. Normalize interior grouping and reference prices only after their dependencies and current calculations are reconciled. Handle the five Python-owned replacement permissions as their own approved source-ownership change.

Acceptance: identical AND/OR behavior, inclusion/exclusion/replacement transitions, default restoration, exclusivity, conditional prices, interior/seat totals, summary labels, images, and model-specific presentation. Each independently useful family ends at a reviewable checkpoint.

### Stage 6 — Cut over once, with one source of truth

Select a single canonical authoring layout and remove dual-write paths. Any legacy model sheets retained for familiarity become generated/read-only views. Update the family registry and shared safe writer before enabling Manager edits to the new structure. Keep a verified workbook/artifact rollback set and document the inverse mapping until parity is established.

Acceptance: the catalog-selected workbook/Manager/generator gates pass; a complete six-model candidate and published-registry comparison pass; affected browser flows cover model switching, rules, totals, summaries and downloads; dealer modal/payload behavior is preserved without live submission. No deployment is implied by normalization.

## Useful changes even if the refactor stops here

Priority order:

1. Fix `section_master`'s misplaced dropdown and the extreme freeze-pane settings.
2. Add a compact data dictionary explaining row grain, keys, reference targets, blank/zero/`*`, lifecycle, and source ownership. Surface it in the existing editor.
3. Generate a cross-model difference report. Flag mismatched prices/copy/behavior for review; never auto-align legitimate differences.
4. Generate a joined rule explanation and trace from authored row through grouped/derived rules to runtime behavior.
5. Add typed-value and validation-coverage diagnostics. The current schema gate does not catch the misplaced Excel dropdown.
6. Reconcile interior total, selected-seat deduction, component rates, and conditional pricing in a read-only price trace.
7. Identify shared-change impact before editing shared interiors, colors, assets, or price references.
8. Label preserved non-executable sheets clearly and document the remaining Python-owned model permissions.

## Validation and limitations

Executed successfully:

- `.venv/bin/python scripts/validate_workbook_schema.py stingray_master.xlsx`: valid, 0 errors, 0 warnings.
- `.venv/bin/python scripts/validate_workbook_package.py stingray_master.xlsx`: valid, 0 issues.
- Read-only profiling of all 77 sheets, ordered header parity for all 11 registered roles, exact availability-pair coverage, relevant key uniqueness, candidate dependency comparisons, stored data types, Excel tables/validation/panes, and repeated content.
- Traced source mapping, rule assembly, interior/component pricing, runtime pricing and color behavior, and Manager source-of-truth boundaries.

No data changes were requested. Regeneration, broad test suites, browser checks, Excel visual inspection, live submissions, publication, and deployment were not performed. Existing validators passing does not prove the workbook is in 3NF or confirm the correctness of every authored business fact. Full rule contradiction/cycle analysis and exhaustive price reconciliation remain specification/prototype acceptance work.

Snapshot: repository `f80d599ce8b83bb1b70e5937ce9200dba6ecce89`; workbook SHA-256 `3127e663b1531e366ce86b989b6190914108d40dfd15a33a258307a05d608e3c`. The audit report is outside the repository; this analysis requires no branch, commit, or PR.

Final readback confirmed the same workbook hash and a clean `git diff --check`. Unrelated concurrent activity changed the checkout branch to `codex/pr-coder-astra-low` and modified `docs/pr-coder-runbook.md`; this audit did not modify or revert that work.

## Code evidence

- [Source surface ownership](/Users/seandm/Projects/27vette/README.md:58)
- [Registered roles and family keys](/Users/seandm/Projects/27vette/scripts/corvette_form_generator/workbook_domain/registry.py:15)
- [Price reference blank-key semantics](/Users/seandm/Projects/27vette/scripts/corvette_form_generator/workbook_domain/registry.py:277)
- [Rule assembly, grouping, and redundant-rule handling](/Users/seandm/Projects/27vette/scripts/corvette_form_generator/rules.py:143)
- [Interior scope uniqueness](/Users/seandm/Projects/27vette/scripts/corvette_form_generator/runtime_metadata.py:553)
- [Interior grouping JSON and derived fields](/Users/seandm/Projects/27vette/scripts/corvette_form_generator/interiors.py:65)
- [Interior source assembly](/Users/seandm/Projects/27vette/scripts/corvette_form_generator/interiors.py:142)
- [Price reference fallback and R6X arithmetic](/Users/seandm/Projects/27vette/scripts/corvette_form_generator/pricing.py:47)
- [Selected-seat deduction](/Users/seandm/Projects/27vette/form-app/app.js:795)
- [First matching option price override](/Users/seandm/Projects/27vette/form-app/app.js:1191)
- [Five approved Z06 derived replacements](/Users/seandm/Projects/27vette/scripts/corvette_form_generator/rule_derivation.py:34)
- [Disposable projection and guarded editing](/Users/seandm/Projects/27vette/workbook-manager/README.md:8)
