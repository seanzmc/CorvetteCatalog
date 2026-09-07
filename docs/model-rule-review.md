# Model-specific rule review and R6X correction

September 6, 2026. Candidate design review; no schema or pricing changes applied.

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

Source: [frozen browser pricing/itemization](https://github.com/seanzmc/27vette/blob/4fe92a4f078370c478f18484cad31bdafe58ad43/form-app/app.js#L1286), plus the candidate generator above. This establishes an implementation discrepancy to reconcile, **not a verified dollar error in every R6X order**. Existing-output parity can reproduce an existing mistake and cannot settle the owner's intended behavior.

Required R6X scenarios: in every model, select each of its 15 qualifying interior records, confirm one R6X charge at its source amount, and verify that R6X itself discounts no seat or other item. Switch to a nonqualifying interior, switch seats, change trim/body, reset and switch models; verify correct removal/reapplication and no duplicate charge. Expected line items and totals must be calculated from independently inspected source amounts and the owner's additive rule. These scenarios are **not yet executed**. The complete membership set is in the generated inventory described below.

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

[`tests/runtime_parity.mjs`](../tests/runtime_parity.mjs) runs default/reset comparisons on all 32 variants. It chooses the first viable selectable option per section **only on each model's first variant**, skips disabled choices, and selects one viable interior per variant. Its 126 option transitions and 32 interior transitions are samples. It does not identify coverage by source-rule ID, establish both outcomes of each condition, or calculate intended prices independently of the same browser implementation.

Consequently, the existing test does not establish complete R6X, package/wheel-price, grouped prerequisite, replacement, default-restoration, or model-specific interaction coverage. These remain open acceptance work. Do not relabel that sample as complete because all six model names appear in its output.

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

The input is opened read-only. The output is a visible local review artifact, not drawDB import SQL or an application dependency. It lists each model separately with variants and every stored direct/group/exclusive/price/default/color/derived rule, variant override, option policy, interior membership/component and section presentation. Group members, scopes, exact fields, database sequence, resolved reference names and workbook row references are retained; code evidence is included separately. It retains inactive/suppressed records rather than silently excluding them.

This is a record-review aid, not a scenario runner or a replacement for the database. It does not contain every availability/base-price record or prove generator/runtime coverage. Those remain in the catalog and complete generated-contract comparison. Its `status` explicitly says behavioral scenarios are not verified. Regenerate after candidate changes; do not maintain a handwritten rule duplicate.

Validation for this review: all 12 model-owned inventory families reconciled to the read-only database; ordered group/scope members and source references checked; deterministic export and unchanged input checked. The matrix and named examples were queried from the candidate imported from workbook SHA-256 `3127e663b1531e366ce86b989b6190914108d40dfd15a33a258307a05d608e3c`. No new behavioral scenario passes are claimed. Completing the per-model scenario ledger and correcting any confirmed R6X implementation mismatch remain subsequent implementation work.
