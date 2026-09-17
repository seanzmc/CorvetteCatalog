# Semantic overlap and cross-lane validation

This pass validates the translated draft's model-owned relationships and the
accepted common interaction policy. The workbook remains canonical. It does not
implement the form, visualizer, release creation, publication or migration-plan
§5 release contracts.

## Scope and evidence

The [complete inventory and execution results](validation/semantic-overlap.json)
cover all six model revisions and every declared configuration. The inventory
includes direct/grouped exclusions, choice-group members, replacement plans and
actions, continuing requirements, package/default/conditional acquisitions,
interior-owned seats and parts, contextual rates, equipment substitutions and
supplied-content effects. Each rule retains its source path and locator.

Conditions are normalized under each lane's `conditions` map. Each inventory
entry's `checks` contains indices into that lane's `checks` array. A check records
its configuration, interaction, input intent/interior, disposition, and, for
transactions, added/removed selections, removed intent and before/after totals.
The imported revision IDs identify this run; newly imported disposable databases
allocate their own opaque IDs. The report includes the implementation hashes and
the accepted policy used by the run.
`witness_failures` records discarded search branches for diagnosis; only the
top-level `findings` list identifies failed or unresolved coverage.

The report also retains each of the 3,770 behavior source dispositions, including
inactive and superseded rows. The source-accounting regression independently
reconciles them against the retained handoffs.
Inventory coverage alone is not proof of the correctness of the original facts:
source-endpoint, accepted-price and lane-specific acceptance tests remain separate.
No raw guide, frozen handoff evidence, baseline workbook or 27vette file changes.

## Final results — September 17

The full matrix completed in **644.06 seconds**, with **zero failed or unresolved
findings**. All 32 configurations are covered. The saved report declares
`complete: true` and `release_ready: false`; its implementation hashes and every
inventory/check/condition reference were verified after lossless formatting.
The final regression suite passed **115 tests in 98.225 seconds**.

| Model lane | Inventory entries | Scoped check outcomes | Live same-target overlaps |
| --- | ---: | ---: | ---: |
| Grand Sport | 1,297 | 15,553 | 558 |
| Grand Sport X | 1,291 | 14,357 | 558 |
| Stingray | 1,257 | 12,240 | 538 |
| Z06 | 1,319 | 15,630 | 574 |
| ZR1 | 878 | 6,028 | 342 |
| ZR1X | 879 | 5,988 | 346 |
| **Total** | **6,921** | **69,796** | **2,916** |

The inventory contains 602 exclusions, 485 choice groups, 305 continuing
requirements, 4,460 acquisitions, two replacement plans, 704 interior ownership
records, 304 contextual rates, 25 equipment substitutions and 34 content effects.

Scoped outcomes comprise 49,412 passed checks, 7,530 active-condition/acquisition
checks, 6,920 inactive-condition checks, 3,721 expected refusals and 2,213 proved
inapplicable cases. These are per-rule references, not distinct builds: shared
outcomes normalize to 52,597 check records. The overlap analysis separately proves
272,609 scoped pairs disjoint and retains all 2,916 live overlaps for inspection.
The 44,908 unique transactions reported by the lane matrix exclude any additional
transactions first encountered during overlap analysis and the focused regressions.

The longer runtime is specific to this explicitly requested full milestone:
each eligible interaction executes a preview, canceled-preview rejection, a
second preview with reversed rules, confirmation and full-state restoration.
Routine focused regression execution remains under two minutes. No browser or
release-operation check ran because those consumers are not implemented here.

## What the pass checks

- Every scoped exclusion member and every pair of choice-group members in both
  request directions, including inapplicable and nonselectable endpoints.
- Every requirement alternative and removal of its live prerequisite, plus
  true/false conditions. No implicit waiver or invented prerequisite purchase.
- Acquisition causes, source-only removal, prior independent ownership, source
  before child clicks, direct child removal, and simultaneous compatible causes.
- Every interior's seat/option ownership through select, clear and direct removal
  of customer-removable children. Missing interiors stay incomplete.
- Each replacement action set and every alternative trigger, preserving the
  specifically authorized replacement product and its purchase ownership.
- Pairwise overlapping acquisition, price, replacement and content conditions
  within their actual configuration scopes. Proven disjoint combinations are
  counted separately; unresolved searches are failures, not evidence of disjointness.
- Preview does not commit; cancel invalidates the pending offer and preserves the
  full state; confirmation commits the disclosed candidate; revert restores the
  entire previous state, including causes, intent, interior, content and charges.
  The repeated preview reverses rule/price/plan row order to detect accidental
  dependence on storage order. Charge owners remain unique and removed options
  cannot retain charges.

The matrix constructs witnesses from typed predicates and checks their declared
constraints. Independently authored regressions retain the accepted dollar and
ownership expectations. This is finite relationship/condition coverage, not an
exhaustive enumeration of every possible multi-option build or UI validation.

## Policy precedence and legitimate refusal

The [September 11 common policy](compatibility-notice-policy.json) follows the
model owner decisions for interaction treatment. It supersedes earlier stripe
refusal instructions while retaining the model-specific prohibited combinations.
The September 15 direct-removal extension includes every supporting owner and
invalidated dependent in the same preview/confirm/cancel/revert transaction.

An unavailable or inapplicable endpoint stays unavailable. Informational or
standard-only equipment does not become independently purchasable/removable.
Unmet prerequisites can still require refusal; a resolver cannot invent a product
or silently select a different interior. An unconditional configuration/default
cause cannot be removed by inventing an unrequested replacement peer. Expected
refusals are recorded with their actual reason and unchanged committed state.

Similar package names do not imply shared ownership: Stingray PCX absorbs prior
child purchases; Z06 PCZ preserves them. The six lanes keep their own identities,
prices, equipment, scopes and replacement products. Z06's PDB/Z07 notice offers
the accepted PDD switch, not PDF.

## Repairs

Directly removing an interior-owned seat previously returned an unchanged build.
The transition temporarily blocked the seat, but its supporting interior survived;
final evaluation then reacquired the seat. The resolver now clears that interior
owner before reconciliation, preserves independent choices, and refuses to commit
any requested removal that would be reacquired. Cancel and revert preserve the
complete former interior and its charges.

A second defect discarded the customer owner of a package-supplied choice merely
because that choice could yield to a different peer. In Z06, removing Z07 from
PDD/PDF could loop when ROY's unmet J57 requirement was processed first. Cleanup
now retains customer/package roots during prerequisite-loss cleanup, while ignoring
soft configuration roots. Ordinary peer conflicts still preserve compatible
packages whose supplied choice can yield. The PDD/PDF regressions cover all Z06
configurations and restore the exact pre-package state and charges; Stingray
Z51/T0A→TVS separately verifies compatible package retention.

Replacement cleanup now prefers the plan's accepted purchase roots. The PDB→PDD
switch had incorrectly preferred the consumed Z07 request, refusing valid notices
when existing CBF, 5ZV or other accessories conflicted with PDD. A regression
exercises every selectable extra offering that can coexist with PDB in each Z06
configuration and checks the authorized PDD candidate and full transaction.

Removing an already absent option is now inert. Previously, removing absent ROY
after selecting ROZ could remove PDD and ROZ because the dormant ROY inclusion
still pointed at PDD. The no-op preserves both the build and the prior undo state.

Missing-group diagnostics now have stable ordering, so reversing rule storage
order does not change an otherwise identical preview.

The overlap review also clarified the acquisition-priority wording in the
[worked examples](master-schema-worked-examples.md#open). Compatible causes of the
same target are retained even at equal priority: ZR1X 5JR and ZYC both supply DRG.
Removing either source retains the other cause and one charge. This does not allow
contradictory ownership policies, ambiguous competing defaults, price precedence
or multiple replacement plans.

## Reproduction

Use Python's standard library from the repository root:

```sh
python3 -m catalog.semantic_validation --output .local/semantic-overlap.json
python3 -m unittest tests.test_semantic_validation tests.test_behavior_sources tests.test_evaluator tests.test_catalog_offerings tests.test_evaluator_sources tests.test_foundation
```

The full matrix is an explicit milestone check, not a new hook or per-edit gate.
The CLI exits unsuccessfully for failed or unresolved findings and still writes
its report for diagnosis. `--models` and `--tables` restrict a diagnostic run;
these runs never claim complete coverage. Every result retains
`partial_catalog_not_submission_ready`. Release contracts, consumer rendering and
publication/rollback proof remain subsequent work.
