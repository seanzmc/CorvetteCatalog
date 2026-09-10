# Model discovery for the master schema

The purpose is to understand each model's complete data and connected behavior so
one master schema can be designed from demonstrated requirements. This is not a
database implementation, a corrected runtime, or permission to cut over from the
workbook. Model-specific packages and rules require different cases, not different
definitions of completion.

## Completion questions

For every applicable family, the model handoff must answer:

1. **What exists?** Account for model/body/trim configurations, every offering,
   interior leaf/component, standard equipment and guide-only omission. Preserve
   identities, duplicates, inactive records, raw facts and exact source locations.
2. **When does it apply?** Explain body/trim, lifecycle, paint/interior and option
   conditions, prerequisites, required selections, defaults and effective scope.
   Do not equate a workbook status with actual runtime availability.
3. **What does selection do?** Trace additions, exclusions, replacements, physical
   content, and each charge owner through guide, workbook and observed baseline.
   Account for every numeric option rate and its model-qualified source; classify
   null/zero amounts and qualified discounts without inventing missing prices.
4. **What does change/removal do?** Exercise relevant acquisition orders, loss of
   prerequisites, defaults/restoration and multiple causes. Distinguish a direct
   purchase from package-supplied content. Explain when a representative case
   covers a family and when a distinct condition needs its own case.
5. **What reaches the build?** Observe equipment, line items, totals and recap/order
   output in valid product contexts, plus relevant required-selection rejection.
   Separate informational equipment from configured content. No live order is needed.
6. **What is established?** Keep source facts, frozen observations, accepted target
   corrections, inferred equivalence and unresolved business decisions separate.
   Record expected target outcomes without claiming an unimplemented target ran.

The completion review checks those answers and their evidence, not just row counts,
headings or a passing helper. A known baseline defect can be fully discovered when
its trigger, consequences, evidence and intended disposition are explicit. Missing
investigation must remain incomplete; a business decision must remain open until
the owner resolves it. Neither is silently renamed implementation work.

## Evidence and repeatability

Use each existing behavior report, structured handoff and companion JSON together.
Retain original evidence unchanged. Add new observations separately with source
hashes, model/context, actions and outcomes. Supporting facts needed by the schema
handoff belong in tracked files; raw originals remain ignored. Local scratch files
are useful for investigation, but must not be the only copy of required results.

Apply new checks to earlier models only where the behavior exists. Record why a
check is not applicable rather than creating identical tests or copying another
model's business rules. Equal model counts and exhaustive build combinations are
not required. All source relationships still need an explained disposition.

## Current model handoffs

| Model | Behavior | Structured facts and decisions | Catch-up status |
|---|---|---|---|
| Stingray | [Analysis](stingray-behavior.md) | [Handoff](stingray-structured.md), [records](stingray-structured-records.json) | Catch-up verified; see model review below |
| Grand Sport | [Analysis](grand-sport-behavior.md) | [Handoff](grand-sport-structured.md), [records](grand-sport-structured-records.json) | Catch-up verified; see model review below |
| Grand Sport X | [Analysis](grand-sport-x-behavior.md) | [Handoff](grand-sport-x-structured.md), [records](grand-sport-x-structured-records.json) | Catch-up verified; see model review below |
| Z06 | [Analysis](z06-behavior.md) | [Handoff](z06-structured.md), [records](z06-structured-records.json) | Catch-up verified; see model review below |
| ZR1 | Not started | Not started | After the four-model catch-up |
| ZR1X | Not started | Not started | After ZR1 |

The older schema proposals, disposable catalog and migration-parity milestones
remain historical reference. Finish the model handoffs, then separately review
one coherent master-schema proposal. Do not build separate model schemas or resume
the earlier database plan while discovery is active.

## Catch-up completion review

The four existing lanes now retain the same categories of source accounting and
behavior evidence. This review uses their full original family analyses plus the
new cases, not the new cases alone. Baseline defects retain their accepted decision
IDs. All 54 accepted decisions (12/16/14/12) remain unchanged. No corrected runtime,
new business decision, schema or production release is claimed.

| Completion question | Evidence checked across all four |
|---|---|
| Existence and provenance | Complete baseline lists/dispositions, exact frozen workbook rows, raw guide identities, six configurations, interior membership and explicitly classified omissions. Existing model-specific lifecycle/standard-equipment decisions remain authoritative. |
| Effective availability | New full active-offering × six-configuration browser sweep, including hidden, unavailable, display-only and enabled states. Inactive source offerings remain in the original handoff rather than being counted as executed choices. |
| Selection and charge ownership | Existing direct/group/exclusive/conditional-price records and family traces, plus every option's numeric/null/zero classification, full same-code schedule candidates including column-D qualifiers, and qualified discounts. Matching a rate is not acceptance of a build total. |
| Reversal and independent causes | New source-linked cases for applicable package/child acquisition orders, mirror causes in both removal orders, paint/stripe directions, cover variants, roof/accent paths and model-specific performance packages; earlier unique-model cases remain retained. |
| Build consumers | Each new connected case starts with valid paint/interior and captures actual item/routing/price projections, order sections, compact recap, informational equipment IDs, missing requirements and button state after each action. Missing-interior rejection is executed in all six configurations. |
| Disposition and target | Original accepted overlays and expected sequences remain separate from observed defects. New results below identify the observed behavior and the existing governing target. Not-applicable probes are recorded explicitly, not counted as successful behavior tests. |

Representative selection: ordinary 2LT/2LZ interiors isolate exterior/accessory
relationships without introducing unrelated interior charges. Both bodies are used
for paint/graphics/accessory paths; coupe/convertible covers have separate cases;
3LT/3LZ exercises mirrors; performance packages, defaults, seat reconciliation and
rejection run across six configurations. Earlier complete interior/paint/belt
sweeps supply the interior coverage. This is not an assertion that every possible
combination or every dormant option has been executed.

### Stingray

[Supplemental accounting](discovery/stingray-accounting.json) ·
[Supplemental runtime evidence](discovery/stingray-runtime.json)

- All 242 option amounts are accounted for: 150 numeric and 92 null. All 178
  direct relationships are traced to emitted runtime rows or inactive-endpoint
  filtering. This preserves dormant compatibility facts without treating them as
  active selections. All same-code schedule candidates retain their qualifiers;
  BCP/BC4/BCS body/package and AE4/AH2 trim prices remain distinct.
- The original local evidence is now retained in `retained_original_supplemental`:
  260 interior contexts, 1,416 option observations, 130 interior-price comparisons,
  1,300 paint states, 780 belt attempts, primary/repeated source comparisons and
  interior reconciliation. Those results are preserved, not relabeled as new runs.
- New run: 1,416 starting-choice observations / 742 enabled actions, 109 connected
  cases and six rejection checks. All 60 listed stripe/paint attempts refuse the
  second conflicting choice. All three colored covers now have both coupe package
  acquisition orders and convertible prerequisite-loss examples. Coupe cover cost
  moves 695 → 595 with B6P; removal restores 695 while the independent cover stays.
- D84/D86 and EFY refuse GBA conflicts in both tested directions. **EDU differs:**
  GBA after EDU removes the accents/charge; EDU after GBA is refused. The older
  unverified-EDU wording must not imply the same action as EFY. Accepted ST-D06/07
  interaction policy still controls the future target.
- Both mirror-removal orders retain DRG until the last cause disappears. Z51/FE4
  acquisition/removal now has six complete-context output traces. PCU (not PCQ),
  PEF, PDY, SBT, PCX and PDV are independently traced; PCX's paid wheel replacement
  remains frozen behavior rejected by ST-D06, not a newly approved alternative.

### Grand Sport

[Supplemental accounting](discovery/grand-sport-accounting.json) ·
[Supplemental runtime evidence](discovery/grand-sport-runtime.json)

- All 241 option amounts are accounted for: 152 numeric and 89 null, including
  ROY 11995−1000=10995, ROZ 13995−2000=11995 and STZ 15500−3005=12495. AH2's
  3LT standard amount and Z25's accepted content-charge correction are explicitly
  classified. All 157 direct relationships have emitted runtime endpoints.
- New run: 1,428 starting-choice observations / 744 enabled actions, 121 connected
  cases and six rejection checks. All 60 stripe/paint attempts refuse the second
  choice. VPW/DPB and VPO/DPB coexist in both orders and both bodies; this extends
  the original single counterexample and remains governed by GS-D12's refusal.
- All three cover variants, D84/D86, EDU and both mirror-cause removal orders are
  observed. EDU→GBA removes EDU; the reverse is refused. EFY is not a Grand Sport
  offering and is explicitly not applicable rather than inherited from Stingray.
- FEY removal leaves a missing caliper in all six tested contexts; FEB loss leaves
  J57/T0F with missing performance prerequisites. These are the already accepted
  GS-D06/07 cleanup/restoration corrections. Full output traces now accompany the
  earlier selection and rejection evidence. Package/child order tests preserve
  historical absorbed-purchase loss separately from the accepted intent policy.

### Grand Sport X

[Supplemental accounting](discovery/grand-sport-x-accounting.json) ·
[Supplemental runtime evidence](discovery/grand-sport-x-runtime.json)

- All 239 amounts are accounted for: 148 numeric and 91 null. The earlier rate
  comparisons now have explicit schedule qualifiers, null classifications and
  direct-rule translation accounting: 141 emitted, three filtered because R88 is
  inactive. Standard J57 is not assigned another model's paid brake price.
- New run: 1,416 starting-choice observations / 756 enabled actions, 119 connected
  cases and six rejection checks. All 60 existing stripe/paint pairs are blocked;
  the existing DTC/GTR pair also has both-body/both-order coverage. VPW/VPO gaps
  remain accepted GSX-D06 corrections.
- Cover variants, D84/D86, package/child order and mirror support now have the same
  questions answered independently. **EDU/GBA refuses both directions here**, in
  contrast to Grand Sport; do not consolidate their frozen conflict actions.
- FED retains its 500 tire-package charge and complete six-context round trips;
  no FEB/FEY requirements are imported. Original EL9/Z25, heritage/D84, HP1 and LS6
  findings/accepted targets remain preserved, including the exact two LS6 rule
  removals. New accounting does not restore those rejected target rules.

### Z06

[Supplemental accounting](discovery/z06-accounting.json) ·
[Supplemental runtime evidence](discovery/z06-runtime.json)

- All 244 amounts are accounted for: 155 numeric and 89 null. Schedule qualifiers
  retain the nine package/wheel rates, BCW body/package pricing, R8E aero amounts,
  seat rates and other-model discount exclusions. WUB is a standard, nonselectable
  Z06 item with null workbook price; a same-code paid exhaust rate does not turn it
  into a Z06 purchase. The original 54-state package matrix remains retained.
- New run: 1,434 starting-choice observations / 807 enabled actions, 112 connected
  cases and six rejection checks. All 60 prohibited stripe/paint combinations
  still coexist in the frozen baseline, independently reproducing Z06-D04.
- Roof/accent→GBA removes incompatible content; reverse acquisition is refused.
  Package/child order, mirror causes, PCZ content and convertible engine prerequisites
  have full output traces. Z07 first leaves the known caliper requirement; manual
  J6D fills it and package removal restores the baseline. Z06-D01 remains the
  accepted default-inclusion correction.
- All 110 workbook direct relationships are emitted. Five additional CBF edges
  remain in the original `runtime_derived_relationships`; the other three models
  have no additional endpoint triples in the frozen contracts. This is a legitimate
  model difference, not a missing section to fabricate elsewhere.

### Cross-model findings and preserved boundaries

All four models auto-select HTJ/N26 after the tested 1LT/1LZ AQ9→AE4 transition
because one interior remains eligible. The tested higher-trim changes leave the
interior unset. Six fresh incomplete-interior builds per model reject submission
with zero requests. The known zero/one/many selection policy is therefore not
replaced by a blanket assumption that any seat change must empty the interior.

Source status, browser registry and standalone contract flags are not interchangeable:
charge-only R6X, GS/GSX package records and Z06 FE7 can appear in the browser's
active-choice universe while marked inactive in standalone contract choices.
The full sweep is checked against active workbook identities in six contexts,
using the hash-verified frozen browser registry. No data is changed to force parity
between different representations.

These records catch up the identified uneven discovery categories. The remaining
work for these four models is implementation and verification of the already
accepted corrections after all six lanes and master-schema design, not a claim
that the existing form is correct. ZR1 and ZR1X remain unfinished model discoveries.

## Reproduce and verify this evidence

Run from the repository root using the existing Node and openpyxl environments:

```sh
node scripts/discovery_catchup.mjs /tmp/catalog-discovery-new-run
PYTHONDONTWRITEBYTECODE=1 /Users/seandm/Projects/27vette/.venv/bin/python scripts/verify_discovery_catchup.py
```

The probe refuses to overwrite output, reads the immutable archive and pinned
reference harness, and uses stubbed network/DOM functions. It does not write into
27vette. The verifier checks frozen source rows, complete option accounting and
qualifiers, direct-rule translations, full choice universes, known stripe outcomes,
context completeness, provenance and rejection evidence. It does not turn row
preservation or arithmetic equality into manufacturer acceptance. Expected target
corrections remain in the model handoffs and have not been executed here.
