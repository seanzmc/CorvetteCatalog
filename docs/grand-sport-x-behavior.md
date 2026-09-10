# Grand Sport X behavior: foundations and connected choices

September 9, 2026. First bounded analysis slice: model/body/trim foundations and
FED acquisition/removal. This uses the Stingray and Grand Sport lane structure;
it is not a complete model review or schema authorization. The accompanying
[foundation records](grand-sport-x-foundations-records.json) retain model routing,
variant/default rows and all 18 observed states. Full structured handoff follows
completion of the remaining families.

## 1. Sources and authority

PR #21 is merged. All 12 ST-D and 16 GS-D review records are accepted. Remaining
Stingray/Grand Sport implementation, output verification and source reconciliation
are not unanswered business decisions. Historical unresolved statements remain
historical evidence, superseded by each handoff's owner-review overlay.

Use the unchanged export `2027 Chevrolet Car Corvette Export (6).xlsx`, SHA-256
`d3ca7d3a09c9fb89210b4ce584493b3ad8fb65ca35087c49d816d1cbf1a333d1`.
Grand Sport X is explicitly named in `Interior 3`, `Exterior 3`, `Mechanical 3`,
`Standard Equipment 3` and `Equipment Groups 3`. D–F are coupe 1LT/2LT/3LT;
G–I are convertible 1LT/2LT/3LT. Shared Color and Trim sheets still need their
own model-specific eligibility reconciliation. See [source provenance](../sources/README.md).

The [frozen workbook](../baselines/2026-09-06/README.md) hash is
`3127e663b1531e366ce86b989b6190914108d40dfd15a33a258307a05d608e3c`.
Workbook `model_workbook_sources` rows 13–23 route this model to
`grand_sport_x_*` sheets and `lt_interiors`. The runtime registry key is
`grand_sport_x`, not Grand Sport's `grandSport`. Shared storage and matching
codes do not transfer Grand Sport corrections into this model.

Observed states execute the frozen `form-app/app.js` and `data.js` from
`4fe92a4f078370c478f18484cad31bdafe58ad43`, using the existing DOM-stub harness
with read access to selection and itemization functions. Model identity was
asserted before observations. No network requests or live submissions occurred.
Amounts below are frozen numeric evidence; PR #21's explicit currency confirmation
was scoped to Stingray and Grand Sport. No Grand Sport X currency or option-price
policy is inferred from that confirmation.

## 2. Model, body and trim foundations

`model_variants` rows 8–13 join `variant_master` rows 14–19. Model membership must
precede trim matching; LT names alone cannot identify this lane.

| Body | 1LT | 2LT | 3LT |
|---|---:|---:|---:|
| Coupe (`*_g07`) | 112,195 | 117,695 | 122,845 |
| Convertible (`*_g67`) | 119,195 | 124,695 | 129,845 |

Guide `Price Schedule` rows 22/23/26 and 24/27/29 respectively give these same
amounts as F + J, including 2,495 destination exactly once. All six runtime
starting totals match. Paint and Interior Color remain missing in each state.

Observed coupe defaults include CF7 roof and BC7 cover; convertible uses CM9
without BC7. AQ9 is selected at 1LT/2LT, AH2 at 3LT. J57 brakes, J6D calipers,
SWM wheels and T0E are selected in all six initial states. Exact selected IDs
are retained in the companion records; this is observation, not an assertion
that every default has already passed manufacturer reconciliation.

`Mechanical 3` independently establishes standard J57/J6D (rows 6/10), LS6/HP1
(rows 22/23), B4Z (41), FE5 (44), and MLG (47). In particular, B4Z and J57 are
standard here. Grand Sport's FEB/FEY dependency decisions cannot be copied here.
`grand_sport_x_options` rows 125/159/165/171 retain J57/FE5/HP1/LS6 respectively.

## 3. Connected performance choice: FED and tire content

Guide `Mechanical 3!C45:I45` makes FED available in all six configurations and
includes XFR performance tires. `Exterior 3!C95:I95` says XFR is included and
only available with FED. Workbook `grand_sport_x_options` row 129 prices FED
at 500; row 73 retains XFR as nonselectable content with a null standalone price.
`grand_sport_x_rule_mapping` row 49 links FED to XFR through `includes`.
Null is retained as null; the evidence does not establish a separately purchasable
zero-price tire option.

For each of six configurations, the executed sequence is initial → FED → remove
FED. Adding FED increases the total by exactly 500 and auto-adds XFR. Removing
FED removes that automatic XFR and restores the starting total. J57 and J6D stay
selected throughout. All 18 states still require paint/interior; these are partial
builds, not order-ready configurations. For example, coupe 2LT totals are
117,695 → 118,195 → 117,695.

This proves acquisition, charge and automatic tire removal for this sequence.
It does not yet prove that every configured-equipment consumer suppresses the
standard XFT tire description when FED is installed. That comparison remains
part of the equipment/output analysis.

## 4. Source differences and unresolved work

- **Powertrain copy requires reconciliation:** `Mechanical 3!C23` attributes
  1,250 combined hp to LS6 (Grand Sport X) or LT7 (ZR1X); workbook option row 165
  repeats that text. Preserve both verbatim as evidence. Their agreement is not
  independent verification of the horsepower claim; no corrected number is
  proposed in this slice.
- **Prices:** base-plus-destination reconciliation is complete for six variants.
  Option-price basis, full numeric reconciliation and explicit currency scope
  still require Grand Sport X review; 500 above is the workbook charge observed.
- **Families still unanalyzed:** full interior/seat/belt and R6X/EL9/Z25 pricing;
  heritage hash/center/roof dependencies; engine covers; wheels/calipers and
  paid alternatives; accessories; lifecycle notices; duplicate identities;
  complete source offering/status reconciliation; equipment and submission
  outputs; body/trim transitions with existing purchases.

These are Grand Sport X evidence/coverage gaps. They do not reopen accepted
Stingray or Grand Sport decisions. Business questions should be narrowed using
this model's evidence before requesting owner answers.

## 5. Coverage and next checkpoint

Verified workbook, guide, frozen app, registry and Grand Sport X contract bytes
against recorded hashes. Inspected the model-specific mechanical disclosures,
variant routing, FED option/include records, and six base-price rows. Executed
six FED round trips / 18 states with zero requests; assertions check the 500
increment, restored total, XFR acquisition/removal and retained J57/J6D.
Reviewed the document and record file against those results.

No full family reconciliation, visual browser QA, corrected evaluator test or
release acceptance is claimed. Next: analyze the connected interior and heritage
families, populate the same structured categories used for the prior models,
then assess model-specific implications for the paused schema proposal. No DDL,
canonical workbook, reference-project or production changes were made.
