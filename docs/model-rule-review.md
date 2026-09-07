# Model-specific rule review and R6X correction

September 7, 2026. R6X source and runtime review completed; no schema or pricing changes applied.

**A passing Stingray example does not verify Grand Sport, Grand Sport X, Z06, ZR1 or ZR1X.** Even within one model, two `includes` rows can behave differently because of scope, prerequisites, replacements, exclusivity, defaults and conditional prices. Rule-type names are an inventory dimension, not a sufficient test plan.

## R6X: requirement versus implementation

The owner's requirement is: **selecting certain interior codes adds R6X; R6X never offsets another price.** This replaces the blueprint's earlier characterization of seat-offset arithmetic as the intended R6X rule.

The inspected candidate contains:

- `opt_r6x_001`, Custom Interior Trim and Seat Combination, priced at **995** in each model.
- **15 R6X interior-component memberships per model**, 90 total, each linked to a 995 rate. `PriceRef!22` is the dedicated R6X rate.
- For example, Stingray interior `3LT_R6X_AH2_HUU` has interior code HUU and seat AH2; `3LT_R6X_AE4_HUU` has the same interior code with seat AE4. Both carry an R6X component. Keep complete model/interior/seat eligibility when reviewing the qualifying set; do not assume code text alone proves applicability.
- `PriceRef!6–7` and `!13–14` also encode R6X seat totals (995 for AH2, 1590 for AE4). These are separate from the dedicated R6X rate.

The implementation is more complicated than that requirement:

1. [`catalog.contracts.Catalog.interiors`](../catalog/contracts.py) starts with stored interior price and adds a nonnegative R6X-seat-rate minus ordinary-seat-rate difference when trim/ID contains R6X. It also emits an R6X component and infers `requires_r6x` from trim/ID.
2. The frozen browser does not use `requires_r6x` as a selection trigger. It renders the interior's component list. Its `selectedInteriorReplacesSeat` explicitly treats **either `seat` or `r6x` component type** as grounds to omit the selected seat line.
3. `adjustedInteriorPrice` subtracts the selected-seat resolved price, while `lineItemsFromInterior` adds a replacement-seat amount back before subtracting component totals. The net result must be traced; subtraction in one helper alone does not prove the final order is undercharged.

Source: [frozen browser pricing/itemization](https://github.com/seanzmc/27vette/blob/4fe92a4f078370c478f18484cad31bdafe58ad43/form-app/app.js#L1286), plus the candidate generator above. The executed review below now establishes the exact defect: **AE4's 595 seat charge is omitted when a qualifying R6X interior is selected.** Existing-output parity reproduces this defect.

### Executed R6X review

All 90 model/interior memberships were selected in both applicable body variants: **180 cases**. Expectations were extracted independently from the frozen workbook, using explicit model/sheet routing, active interior/model membership, component-rate rows, model-owned seat options and scoped seat-price rules. Every R6X interior's stored price equals its non-R6X extras; no seat component is present in these memberships. Each model's applicable AE4 self-price rule specifies 595, while AH2 resolves to zero. Every component amount and the exact qualifying set were checked against generated output.

| Model | AH2 cases matching expected subtotal | AE4 cases missing 595 | Removal/reset checks passed |
|---|---:|---:|---:|
| Stingray | 22 | 8 | 16 |
| Grand Sport | 22 | 8 | 16 |
| Grand Sport X | 22 | 8 | 16 |
| Z06 | 22 | 8 | 16 |
| ZR1 | 22 | 8 | 16 |
| ZR1X | 22 | 8 | 16 |

Every case contains exactly one R6X component at 995 and the correct extras. All **48 AE4 cases fail additive pricing**; the 132 AH2 cases match because the suppressed seat costs zero. The frozen and candidate lanes produce identical orders, compact exports and dealer payloads in all 180 cases. No live submission was made.

Concrete Stingray coupe example: `3LT_R6X_AE4_HUU`, from `lt_interiors!120`, has stored extras of zero. `model_interior_scope!560` establishes membership; `interior_components!170` references R6X at `PriceRef!22` (995). `stingray_options!157` identifies AE4 and `price_rules!30` sets its 3LT charge to 595. The expected seat/interior subtotal is **595 + 995 = 1590**. The observed lines contain HUU at zero and R6X at 995, with no AE4 line. With the tested defaults and `variant_master!4` base of 85245, observed MSRP is **86240**, versus **86835** with the missing seat restored. Other selected/default amounts are held constant; this is not an independent oracle for unrelated vehicle pricing.

Root cause: the generator emits 995 plus extras after subtracting the ordinary seat rate from the combined R6X seat rate. The browser's `selectedInteriorReplacesSeat` then treats the R6X component as replacing the seat. Its itemization arithmetic restores the interior components but never the separate 595 seat charge. This is a consumer/accounting defect; the inspected R6X source amounts reconcile. Fixing only the seat-line suppression is insufficient unless the associated interior residual arithmetic is also checked, especially when extras exceed the seat amount.

The 96 transition checks cover both seat types in each model: nonqualifying interior, qualifying reapplication, incompatible seat change, body change, trim change, reset, model change, and return/reapplication. They verify R6X removal or one charge as appropriate. Body/trim changes use the browser's actual `setBodyAndTrim` reset path. These transitions test R6X lifecycle, not independent pricing of every nonqualifying interior or every possible option interaction.

### Settled translation requirement

For these memberships, total the independently resolved **seat + R6X + other interior components**, each once. R6X is an additive component linked to qualifying model/interior memberships, never a seat-replacement instruction or a price adjustment inferred from an ID substring. Preserve the authored evidence for `requires_r6x`, `included_option_id`, component membership and model scope; their current runtime interpretations differ, and source evidence is not another editable owner.

The eventual authoring design must give each charge one price owner and link applicability to it. The current R6X option amount, dedicated component rate and combined seat-rate rows agree, but must not become three independently editable ways of pricing the same R6X charge. This does not choose a final interior DDL or require a special R6X table. It settles the business rule needed for that design.

This bounded review is complete. The existing parity implementation remains unchanged; implementing additive itemization in the new consumer is a known correction, separate from reproducing the frozen baseline. No additional R6X research is needed to proceed with foundation design. Broader model-rule obligations below remain separate.

Reproduce using the existing Python/openpyxl environment and Node, from the repository root:

```sh
mkdir -p .local/r6x-review
python -m catalog.importer --output .local/r6x-review/catalog.sqlite
python -m catalog.contracts --database .local/r6x-review/catalog.sqlite --output .local/r6x-review/contracts
python tests/r6x_source_cases.py > .local/r6x-review/cases.json
node tests/r6x_review.mjs .local/r6x-review/cases.json .local/r6x-review/contracts/form-app/data.js > .local/r6x-review/results.json
```

Importer/generator destinations must be new; reuse their existing output for repeat diagnostics. The source extractor checks the frozen workbook hash. The runtime diagnostic checks frozen app/data hashes and loads the harness from the pinned reference commit. Its JSON records every source reference, expected/actual subtotal, affected line item and transition. It deliberately **exits 1** while the 48 pricing discrepancies remain (`summary.passed: false`); that is not a successful acceptance result. The command accepts an optional reference-repository path. Eleven existing contract tests also passed, including complete six-model serialization parity. This is an in-process browser-code review with DOM stubs, not visual or production verification.

## Observed differences by model

These counts describe imported records, including records later suppressed by generation. They are not assertions that every record is runtime-active or tested.

| Mechanism | Stingray | Grand Sport | Grand Sport X | Z06 | ZR1 | ZR1X |
|---|---:|---:|---:|---:|---:|---:|
| Direct requires | 17 | 18 | 12 | 9 | 2 | 1 |
| Direct includes | 59 | 61 | 55 | 56 | 40 | 39 |
| Ordinary direct excludes | 98 | 73 | 77 | 44 | 54 | 54 |
| Authored replace actions | 4 | 5 | 0 | 1 | 2 | 2 |
| Requires-any groups | 2 | 2 | 0 | 4 | 0 | 0 |
| Excludes-any groups | 25 | 47 | 43 | 31 | 5 | 4 |
| At-most-one groups | 8 | 8 | 7 | 11 | 8 | 8 |
| Exactly-one groups | 2 | 4 | 2 | 2 | 1 | 0 |
| Option-conditioned price rules | 30 | 31 | 27 | 50 | 12 | 11 |
| Interior-conditioned price rules | 22 | 24 | 24 | 22 | 22 | 22 |
| Unless-section defaults | 2 | 1 | 0 | 3 | 4 | 4 |
| When-selected/unless-section defaults | 0 | 1 | 1 | 0 | 0 | 0 |
| Code-authorized derived replacements | 0 | 0 | 0 | 5 | 0 | 0 |
| Variant overrides | 4 | 4 | 4 | 4 | 0 | 0 |
| Model-qualified color rules | 269 | 281 | 281 | 269 | 214 | 214 |

Every model additionally has one `always` default and one `unless_selected_rpo` default. Identical counts do not imply identical targets or behavior.

Concrete review anchors, **not the full scenario list**:

| Model | Actual records and distinct obligation |
|---|---|
| Stingray | `rule_groups!2–3`: Black Ground Effects requires one of two spoilers; Body-Color High Wing requires an allowed paint. Exercise each allowed member, no member, a disallowed choice, and reverse selection order. Z51 includes brakes and zeroes TVS through different rule families. |
| Grand Sport | `grandSport_rule_groups!3` and `!28`: aero/brake prerequisite groups. `default_selection_rules` rule `gs_default_j6d_with_j57`: J57 triggers Dark Gray Metallic-Painted Calipers only when the user has not chosen a competing caliper in the resolved target section. Test explicit color before and after J57 and removal of J57. |
| Grand Sport X | Has the corresponding J57/J6D conditional default but **no requires-any groups and no authored replace actions**. Do not copy Grand Sport's prerequisite/replacement expectations just because option codes overlap. Preserve its own 43 excludes-any groups and 51 price rules. |
| Z06 | `z06_rule_groups!2–5`: Z07 aero requirement and PDB/PDD/PDF carbon-wheel requirements. Five code-authorized CBF replacements interact with inclusion closure. Package component pricing and zero-price brake rules must be evaluated with each qualifying wheel/aero choice and selection order. |
| ZR1 | One exactly-one group and four unless-section defaults; interior-conditioned belt prices such as `zr1_price_rules!14–17`. Exercise its required group and each default independently, then select/change the corresponding dipped interiors and verify belt pricing/restoration. |
| ZR1X | **No exactly-one groups**, despite ZR1 having one; four unless-section defaults still exist. Its own dipped-interior belt rows are `zr1x_price_rules!13–16`. Verify its required sections/defaults from its records rather than inheriting ZR1 expectations. |

## What the current tests actually establish

`catalog.parity` compares all six generated contracts and the registry with the frozen baseline, excluding only generation timestamp. This covers serialized values and ordering across every model; it does not independently prove that baseline logic is correct.

[`tests/runtime_parity.mjs`](../tests/runtime_parity.mjs) runs default/reset comparisons on all 32 variants. **Only on each model's first variant**, it reserves each section's first candidate that passes the static selectable/active/status filters. It then checks dynamic disable reasons and skips a disabled candidate without trying a later choice in that section, so some sections receive no option transition. It also selects one viable interior per variant. Its 126 option transitions and 32 interior transitions are samples. It does not identify coverage by source-rule ID, establish both outcomes of each condition, or calculate intended prices independently of the same browser implementation.

Consequently, the existing parity sample does not establish complete R6X, package/wheel-price, grouped prerequisite, replacement, default-restoration, or model-specific interaction coverage. The dedicated R6X review above now covers its specified source memberships and transitions and identifies the AE4 defect; the other families remain open acceptance work. Do not relabel the original sample as complete because all six model names appear in its output.

## How to make coverage explicit

For each model, track **source rule ID(s) → applicable variants → starting selections → action → independently expected result → executed result**. The expected result includes selected and automatically included items, disabled reason, required-choice state, itemized amounts, total and submission payload where affected.

Review every record, including filtered/inactive records with an explicit reason, before choosing representative scenarios. A shared test implementation can execute many cases; it cannot replace model-specific inputs and expected outcomes.

- Direct rules: condition absent/present/removed; both selection orders; includes closure and conflicting peers; author-replace versus ordinary exclusion.
- Groups: every member alternative, no qualifying member, inactive members, scope boundaries and interaction with direct-rule suppression.
- Prices: every condition/target pair, multiple applicable overrides in original order, zero versus missing amount, package base/delta paths, interior/seat/belt/component combinations and restoration after removal.
- Defaults and exclusivity: each condition kind and priority, user-selected alternatives, resolved section changes, exactly-one versus at-most-one, reset and model switching.
- Availability, display and scopes: applicable and inapplicable body/trim/variant states, all override fields, standard/available/unavailable and auto-only/hidden/display-only behavior.
- Color/interior eligibility: each model's own memberships, required options, seat/trim compatibility, added codes and removal transitions; retain explicit R6X scenarios above.

Overlapping rules require interaction cases: sharing a source, target, exclusive group, section, or price target is a reason to inspect the combination. One successful example per effect name is insufficient. There is no claim here of exhaustive combination coverage.

## Refreshable record inventory

Run from the repository root:

```sh
python3 -m catalog.rule_inventory \
  --database .local/checkpoint-d/final.sqlite \
  --output DrawDB/model-rule-inventory.json
```

The input is opened read-only. The output is a visible local review artifact, not drawDB import SQL or an application dependency. It lists each model separately with variants and every stored direct/group/exclusive/price/default/color/derived rule, variant override, option policy, interior membership/component and section presentation. Group members are sorted by display order (missing order means zero), then database sequence and ID for deterministic ties. Scopes, exact fields, database sequence, resolved reference names and workbook row references are retained; code evidence is included separately. The shared component-rate collection preserves rate identity fields, amounts, price basis, currency and source rows; match a component's `rate_id` to a rate's `fields.id` to inspect its pricing evidence. It retains inactive/suppressed records rather than silently excluding them.

This is a record-review aid, not a scenario runner or a replacement for the database. In candidate schema 3, the inventory's `option` family replaces `offering_policy` and includes option identity, base price, copy and policy from their single owner; resolved rule-reference names come from that owner. Availability records remain outside this inventory, in the catalog and complete generated-contract comparison. Its `status` explicitly says behavioral scenarios are not verified. Rebuild older disposable databases and regenerate after candidate changes; do not maintain a handwritten rule duplicate.

Validation for the original inventory review: all 12 model-owned inventory families reconciled to the read-only database; ordered group/scope members and source references checked; deterministic export and unchanged input checked. The matrix and named examples were queried from the candidate imported from workbook SHA-256 `3127e663b1531e366ce86b989b6190914108d40dfd15a33a258307a05d608e3c`. The subsequent R6X execution and its known pricing failures are reported above. Broader per-model scenario work and implementation of the confirmed additive-pricing correction remain separate tasks.
