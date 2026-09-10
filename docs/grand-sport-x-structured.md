# Grand Sport X structured model handoff

September 10, 2026. Model: **Grand Sport X, 2027**. Status: **structured review input**.

This handoff organizes the [complete behavior analysis](grand-sport-x-behavior.md)
using the [Grand Sport handoff](grand-sport-structured.md)'s categories. Its
[record file](grand-sport-x-structured-records.json) retains the complete scoped
workbook baseline, source reconciliation, recorded observations and owner decisions.
These are review inputs, not canonical data, an executable ruleset or a schema.

The owner applied the accepted Grand Sport decisions to overlapping issues on
September 10 and separately corrected HP1 copy. Section 8 records that authority
against actual Grand Sport X identities. **All 14 decision entries are now accepted**, including the subsequent explicit
owner instruction to remove both LS6 rules from `grand_sport_x_rule_mapping`.
Earlier unresolved language in the behavior analysis describes historical review
state; the accepted overlay controls target interpretation without rewriting evidence.

## 1. Record conventions and evidence

| Convention | Meaning |
|---|---|
| IDs | GSX-C, GSX-R, GSX-P, GSX-S, GSX-V, GSX-D and GSX-T identify local configuration, relationship, price, selection, presentation, decision and expected-check records; not database keys. |
| Observation IDs | GSX-O01–49 preserve original sequences; GSX-E01–05 preserve supplemental reversal sequences. Sweeps remain separate. |
| Identity | `grand_sport_x:<legacy option_id>`; proposed SAI uses `grand_sport_x:proposed:SAI`. Both workbook and browser registry keys are `grand_sport_x`. |
| Scope | All means the six configurations, intersected with effective availability, lifecycle and prerequisites. Matching LT labels or RPOs do not establish shared model ownership. |
| Conditions | Preserve AND versus alternative prerequisites, acquisition versus eligibility, price overrides, conflict actions and cause-loss cleanup separately. Blank source scope is not proof of all-body behavior. |
| Prices | USD is accepted. Column E supplies guide OPTIONS prices; preserve model qualifiers and discounts. Destination is included in base. Null is unknown evidence, not universally zero. |
| Evidence / target | Original source fields and defective observations stay intact. Accepted corrections establish target requirements; expected checks are not executed target proof. |

| Evidence | Identity / locator |
|---|---|
| E-W | [Frozen workbook](../baselines/2026-09-06/README.md), SHA-256 `3127e663b1531e366ce86b989b6190914108d40dfd15a33a258307a05d608e3c`; `baseline_rows` preserves sheet names, headers, nulls and Excel `_row` numbers. |
| E-G | [Guide provenance](../sources/README.md), `2027 Chevrolet Car Corvette Export (6).xlsx`, SHA-256 `d3ca7d3a09c9fb89210b4ce584493b3ad8fb65ca35087c49d816d1cbf1a333d1`. Interior/Exterior/Mechanical 3, Standard Equipment 3, Equipment Groups 3 and model-qualified Color and Trim/Price Schedule. |
| E-O | Frozen browser revision `4fe92a4f078370c478f18484cad31bdafe58ad43`; previously captured DOM-stub observations, zero requests. No new runtime execution in this handoff. |
| E-B | [Behavior analysis](grand-sport-x-behavior.md), §§1–12, source locators and connected interpretation. |
| E-A | Owner review September 10, preserved in E-B §12 and §8 below. Overlapping Grand Sport targets plus explicit HP1 copy correction. |

Original observation outputs do not embed source hashes. The JSON records current
artifact hashes and verifies local browser bytes against the frozen archive;
this does not retroactively make the observations self-attesting. The earlier
[foundation JSON](grand-sport-x-foundations-records.json) remains unchanged evidence
for its six FED round trips, rather than being relabeled as a complete handoff.

## 2. Complete record sets and how to use them

Baseline sheet names below are under `baseline_rows`. Other paths are top-level
JSON categories. Join identities and configuration membership before applying
rules. Read the decision overlay before treating any baseline row as a target.

| Category | Record-file location / scope |
|---|---|
| Configurations | `variant_master`, `model_variants`: six configurations and memberships. |
| Offerings | `grand_sport_x_options`, `offering_dispositions`: all 239; 202 coded guide matches, 26 uncoded matches, ten paints and price-only 5ZB. |
| Additions / omissions | `accepted_additions`: SAI at 295 across six contexts, 3LT V8X conflict. `guide_only_dispositions`: source disclosures and component/customer-scope classification. |
| Applicability | `grand_sport_x_ovs`: 1,434 rows; `grand_sport_x_variant_overrides`: four UQT overrides. Lifecycle and rules additionally constrain selection. |
| Interiors | `lt_interiors`, `model_interior_scope`, `interior_source_links`: all 132 leaves, exact guide/workbook links. |
| Parts / source rates | `interior_components`: 198 memberships; `PriceRef`: 21 legacy rates, retained as lookup evidence. |
| Direct relationships | `grand_sport_x_rule_mapping`: 144 rows with original scopes and text. |
| Grouped relationships | `grand_sport_x_rule_groups`, `grand_sport_x_rule_members`: 43 groups / 268 members; alternative prerequisite sets remain distinct. |
| Exclusivity | `grand_sport_x_exclusive_groups`, `grand_sport_x_exclusive_members`: nine groups / 28 members. Section choice modes also constrain selection. |
| Conditional prices | `grand_sport_x_price_rules`: 51 rows for seats, covers, inclusions and belts. |
| Combination additions | `grand_sport_x_color_overrides`: 281 exact pairs, 145 paint and 136 belt. This model uses its own sheet, not `color_overrides`. |
| Defaults | `default_selection_rules`: three authored rules; section/standard defaults are additional behavior. |
| Presentation | `section_master`, `section_presentation`, `runtime_steps`, `context_section_master`, `context_choice_copy`, `order_summary_sections`, `step_order_summary_map`, `asset_map`: model-scoped and applicable wildcard rows, plus referenced section definitions. |
| Routing / intake | `model_master`, `model_registry_promotion`, `model_workbook_sources`: model metadata and 11 routes; `rule_phrase_map`, `runtime_rule_exceptions`: six phrase rows, no exceptions. |
| Observations | `observed_sequences`: 49 sequences / 213 states; `supplemental_observations.edges`: five sequences / 20 states. |
| Sweeps | `supplemental_observations`: 264 interior/body contexts, 1,320 paint states, 792 belt attempts, 132 price comparisons, 100 roof cases, 16 completed defect cases, two equipment comparisons and six seat/cause states. |
| Source reconciliation | `source_reconciliation`: 202 primary coded comparisons, 226 repeated occurrences, exact interior/component/paint reconciliation and 148 numeric price comparisons. Uncoded disclosures are in offering dispositions. |
| Decisions | `owner_review.records`: 14 accepted entries, including exact sheet/row/rule IDs for both LS6 removals; exact HP1 target and GSX-specific preservation requirements. |
| Duplicate audit | `duplicate_rpos_within_model` is empty, including inactive offerings. DTC exists; DUW does not. |

For example, follow the existing DTC offering through its six availability rows,
section, direct/grouped conflicts and GSX-O11/12, then apply GSX-D01. Do not add
a duplicate DTC or import Grand Sport's DUW retirement. For EL9, join exact leaf
IDs to scope, components, color conditions and GSX-D02 before assigning charges.
The price sweep's `expected` is an earlier component-sum comparison; EL9's
component-only 0/595 expectations omit Launch Edition content and are not targets.

## 3. Configurations and offering scope

| ID | Legacy configuration | Body | Trim | Base USD | Roof | Seat |
|---|---|---|---|---:|---|---|
| GSX-C01 | 1lt_g07 | Coupe | 1LT | 112,195 | CF7 | AQ9 |
| GSX-C02 | 2lt_g07 | Coupe | 2LT | 117,695 | CF7 | AQ9 |
| GSX-C03 | 3lt_g07 | Coupe | 3LT | 122,845 | CF7 | AH2 |
| GSX-C04 | 1lt_g67 | Convertible | 1LT | 119,195 | CM9 | AQ9 |
| GSX-C05 | 2lt_g67 | Convertible | 2LT | 124,695 | CM9 | AQ9 |
| GSX-C06 | 3lt_g67 | Convertible | 3LT | 129,845 | CM9 | AH2 |

E-W `variant_master!A14:H19`, `model_variants` rows 8–13; E-G Price Schedule
rows 22/23/26/24/27/29, F + J. Destination 2,495 is already included. GSX-O36–41
retain starting states with paint/interior unset. Coupe starts with BC7; convertible
has no cover. SWM, J57/J6D, B4Z, FE5, LS6, HP1 and MLG are standard across all six.
FED is not an initial purchase. No FEB, FEY or T0F offering belongs to this lane.

B6P/roof panels/SBT are coupe-only; ZZ3/D84/D86 convertible-only. UQT costs 1,495
at 1LT and is included/display-only at 2LT/3LT. E60/BAZ/FA5 begin at 2LT; 5JR
at 3LT. UV6 and DRZ are standard even at 1LT. W2D is a 1LT accessory; AP9 is
supplied at 2LT/3LT. Interior eligibility is four 1LT, 40 2LT, 73 ordinary 3LT
and 15 R6X 3LT leaves, including two EL9 leaves within the ordinary count.

## 4. Price ownership and interpretation

| ID | Owner / condition | Baseline and accepted target | Evidence |
|---|---|---|---|
| GSX-P01 | Base / ordinary options | Preserve six bases and contextual rates; USD, guide OPTIONS column E with qualifiers. No second destination or blanket repricing. | E-B §§2/12; GSX-D10 |
| GSX-P02 | EL9 / Z25 / seat | Baseline both seats add 1,995: AH2 interior 1,995; AE4 seat 595 + residual 1,400; Z25 absent from output. Target Z25 owns 1,995 once, AH2 zero, AE4 another 595. Coupe 3LT totals 124,840 / 125,435. | E-B §7; GSX-D02 |
| GSX-P03 | Four R6X/AE4 leaves | Correct each by +595 once: HU0/38S 2,085 versus frozen 1,490; HUU 1,590 versus 995; HXO/N26/38S 2,780 versus 2,185; HZP/N26 2,285 versus 1,690. | Exact `3LT_R6X_AE4_*` leaves; E-B §7; GSX-D03 |
| GSX-P04 | D30 | One 1,495 charge for surviving nonrecommended paint/belt causes, not per trigger. Hard belt prohibitions stay hard. EL9 target has no alternative-belt path. | E-B §§3/7; GSX-D05 |
| GSX-P05 | Hash / Z15 / center / D84 | Hash acquires Z15 995; center 1,295; required or independent D84 1,295. Hash source null-to-runtime-zero is historical behavior only. | E-B §§4/6; GSX-D01/04 |
| GSX-P06 | Covers / appearance | BC4/BCP/BCS 695 alone on coupe; 595 with applicable B6P 1,895 or ZZ3 1,195. Included D3V/SL9 do not charge again. | Mechanical 3 rows 24–30/38; Price Schedule 173–179 |
| GSX-P07 | FED / exhaust | FED 500 supplies XFR; standard J57/B4Z/FE5 remain. WUB 1,995 permits NWI 395. | E-B §8 |
| GSX-P08 | Carbon wheels | ROY 11,995−1,000=10,995; ROZ 13,995−2,000=11,995; STZ 15,500−3,005=12,495. Preserve model-qualified discounts. | Price Schedule rows 278–281/291–292, D/E; E-B §9 |
| GSX-P09 | Ordinary seats / components | Preserve trim/seat/interior applicability, N26/TU7/stitch/R6X owners. AE4 1,095/2,095/595 by trim; AH2 1,695 at 2LT and standard 3LT. Avoid duplicate component and option charges. | Price Schedule 238–241; interior links and 198 memberships |

## 5. Connected relationship records

Historical conflict actions below are evidence. Apply GSX-D12's replacement offer
and dependency cleanup policy, with explicit refusal exceptions, to target behavior.

| ID | Trigger / eligibility | Connected effect and removal | Evidence |
|---|---|---|---|
| GSX-R01 | Body/trim change | Reset purchases/interior and restore new defaults. UQT presentation follows trim. | GSX-O34/36–41/49; E-B §2 |
| GSX-R02 | Nonrecommended paint or belt | Add D30 once; retain it until last cause disappears. Prohibited combinations cannot buy an override. | GSX-O48; focused seat/cause records; E-B §§3/7 |
| GSX-R03 | Seat/interior changes | Clear invalid leaf and require another interior. HAG requires blue, HVZ red; automatic belt exchanges with leaf. N26/TU7/stitch scope follows source links. | GSX-O48; 264-context and 792-belt sweeps |
| GSX-R04 | EL9 | Target interior-first acquisition adds Z25/locked zero 3F9 and visible content charge; ordinary interior change removes unsupported Z25. `requires_z25` metadata alone is not a working acquisition rule. | GSX-O45/46; four completed cases; GSX-D02/05 |
| GSX-R05 | Convertible stripe + paint | Target D84 required for DMX/DMV with G26/G4Z/GBK/GKZ/GPH, DMY with G26/G4Z/GBK/GTR, DMW with G26/G4Z/GBK. DMU has no set. | Exterior 3!C67:I71; GSX-D04 |
| GSX-R06 | Roof / paint | DMX excludes GTR; DMV GKA; DMY GKZ/GPH; DMW G8G. D84/D86/EDU/ZYC exclude GBA. D84 physically removes roof stripe regardless of acquisition cause. | GSX-O13/43/44; E-B §4 |
| GSX-R07 | Coupe colored cover / B6P | Cover replaces BC7 and supplies D3V. B6P adds SL9 and discounts cover. Remove B6P: retain cover/D3V at 695; remove cover: restore BC7. Absorbed independent D3V does not return if no cause survives. | GSX-O07–09; E-B §5 |
| GSX-R08 | Convertible cover / ZZ3 | Cover requires ZZ3; package supplies BC7/SL9, cover replaces BC7. Remove ZZ3: remove unsupported cover/content. D3V unavailable. Keep effective body scope despite blank raw prerequisite scope. | GSX-O42; E-B §5; GSX-D14 accepted rule removals |
| GSX-R09 | Hash / center | Hash-first acquires Z15; center requires hash. Removing last hash removes dependent center/Z15 charge. Exact 995 disclosure required. | GSX-O10; GSX-D01 |
| GSX-R10 | DTC / Heritage | Baseline DTC suppresses Z15 in its single-choice section but leaves hash. Target complete guide conflicts on existing DTC prevent unsupported coexistence and lost package charge. | GSX-O11/12; 12 completed cases; GSX-D01 |
| GSX-R11 | FED | Adds XFR; removal removes that inclusion while standard J57/B4Z/FE5 and independent wheel/caliper choices survive. Target configured tires reflect XFT/XFR replacement; frozen static equipment retains XFT. | GSX-O01/02; foundation records; E-B §8 |
| GSX-R12 | Factory wheels / hardware | Eleven factory peers; carbon wheels need no new brake package. Chrome S47/SFE conflict with carbon wheels; SPZ requires SPY; remove SPY removes SPZ. SPY conflicts with S47/SFE. | GSX-O03–05; supplemental edges; E-B §9 |
| GSX-R13 | WUB / NWI | WUB permits NWI, replacing NGA; remove WUB removes NWI and restores NGA. | GSX-O06; E-B §8 |
| GSX-R14 | 5ZV / SIG / T0E | 5ZV replaces default T0E and removes dependent SIG. Required aero section cannot be emptied by toggling 5ZV; choose T0E. SIG does not return. WKR changes delivered cover version without another charge. | GSX-O30; E-B §9 |
| GSX-R15 | Ground effects / accents / DRG | CFL/CFZ/CFV exclusive; EDU remains but surface content changes. FED independent. 5JR and ZYC each support DRG; remove last cause to remove DRG. | GSX-O31; supplemental edges; E-B §9 |
| GSX-R16 | PDA / SNE / VPW | PDA includes SNE/VPW; absorbs SNE purchase, which does not return. Historical PDA-after-hash replaces hash; reverse refused. Preserve complete stripe/stinger scopes. | GSX-O16–18/22; E-B §10 |
| GSX-R17 | VPW / VPO | Baseline permits VPW+DPB and VPO+DTC. Target applies complete guide stripe exclusions and refuses both directions, overriding general replacement offers. | Exterior 3!C45:C46; GSX-O19–21; GSX-D06 |
| GSX-R18 | SFZ / CF8 | Historical addition removes center, preserves hash/Z15; reverse center refused. Target CF8 is lifecycle-disabled before that old path can run. SFZ retains full badge/stripe conflicts. | GSX-O14/15/23/24; GSX-D09 |
| GSX-R19 | PCQ / PEF / PDY | Include VWE/VWT, CAV/RIA, RYT/S08 respectively. Absorb prior purchases; package removal does not resurrect them. | GSX-O25–27; E-B §10 |
| GSX-R20 | SBT | Supplies additional transparent roof and SC7, retains factory roof; CC3 conflict refuses both observed directions. Absorbed SC7 does not return after removal. | GSX-O28/29; E-B §10 |
| GSX-R21 | Accessories / delivery | Caps, indoor covers, badges and suede liners retain separate peer groups. Independent ERI/VUP/SLK/RWU/S2L stay independent. R8C persists across wheel changes; retain delivery restrictions as source evidence. | GSX-O05/32/35; E-B §§9–11 |
| GSX-R22 | SAI / DUE / HP1 | Add SAI with 3LT V8X conflict; correct DUE to Royal Blue; remove HP1 combined-power and LT7 copy while retaining axle specs. No DTC addition, DUW retirement or duplicate T0E cleanup. | GSX-D07/13 |

## 6. Selection and reconciliation policies

| ID | Event | Target requirement / limit |
|---|---|---|
| GSX-S01 | Context change | Reset purchases/interior, then establish model/body/trim defaults; do not carry unsupported choices. |
| GSX-S02 | General conflict | Explain conflict and offer replacement before changing selection. Explicit refusal rules, including VPW/VPO, take precedence. Verify both directions. |
| GSX-S03 | Dependency loss | Remove invalid dependents and their charges; alert and offer revert of triggering choice. Preserve independent intent, especially independently selected D84. |
| GSX-S04 | Multiple inclusion causes | Keep equipment while any valid cause survives; charge once. Distinguish surviving cause from an absorbed purchase that does not return. |
| GSX-S05 | Lifecycle unavailable | Show applicable SLN/R88/CF8/RZ9/V8X disabled with “Unavailable at this time”; releasing availability requires separate validation. |
| GSX-S06 | Interior / belt | Require a valid leaf after seat change; preserve hard HAG/HVZ restrictions. EL9 acquires Z25 and locks zero 3F9, without an impossible circular entry gate. |
| GSX-S07 | Required sections / defaults | Retain required aero/wheel choices and scoped defaults. Do not import Grand Sport's package-dependent brake/caliper restoration requirements. |
| GSX-S08 | Resolved output | Corrected choices, inclusions and single charge ownership must reach recap and order, including Z25; an enabled button alone does not prove valid output. |

## 7. Presentation, physical content and operational boundaries

| ID | Subject | Target / evidence |
|---|---|---|
| GSX-V01 | Hash-first Heritage | Exact disclosure: “Selecting this hash mark adds the Grand Sport Heritage Package (Z15) for $995.” |
| GSX-V02 | Center stripe / D84 | Disclose: “When (D84) Carbon Flash painted nacelles and roof is ordered (required or selected) roof will not include the stripe.” Show conditional acquisition and removal/revert effects. |
| GSX-V03 | EL9 | Visible Z25 1,995 content charge plus separate seat charge; preserve quilting, mats, embossed headrests and plaque. Included red belt locked at zero. |
| GSX-V04 | Physical content | EFR/EDU surfaces depend on CFV/CFZ; WKR version depends on 5ZV; SBT adds a second roof. These do not imply extra purchasable identities. |
| GSX-V05 | HP1 / DUE | HP1 title “Electrified Front Axle”; description “Electrified front axle: 186 hp (138.7 kW), 145 lb-ft of front torque (196.6 N-m).” No replacement combined-power claim. DUE target naming Royal Blue. |
| GSX-V06 | Equipment displays | Selected-options equipment reflects configured replacements; informational standard equipment stays model/body/trim based. Static baseline lists do not prove installed equipment. |
| GSX-V07 | Customer scope | Dealer/service/emissions offerings remain outside customer selection. Preserve source SOLD/BAC/approval/VK3 and service disclosures without claiming full dealer-order validation. |
| GSX-V08 | Navigation / assets / messages | Preserve scoped section modes, steps, copy and summary routing as evidence. Asset references are not visualizer proof. Fix misleading conflict reasons such as “Blocked by S47” naming the attempted candidate when explaining the actual conflict. |

## 8. Decision overlay: source, baseline and target remain separate

The following records reproduce the current behavior-analysis owner overlay.
All 14 entries are accepted. None is implementation proof.

| ID | Source / baseline issue | Target / clarification | State |
|---|---|---|---|
| GSX-D01 | DTC/hash coexistence loses Z15 and its charge | Apply complete guide conflicts to the existing DTC identity. Keep hash-first acquisition and the exact disclosure: “Selecting this hash mark adds the Grand Sport Heritage Package (Z15) for $995.” Preserve hash→Z15 and center dependency/removal; no universal null-as-zero rule. GS-D01/03/16. | Accepted September 10 |
| GSX-D02 | EL9 lacks Z25; AH2/AE4 share 1,995 total | EL9 acquires Z25 with a visible 1,995 content charge once; AH2 zero, AE4 another 595. Lock included 3F9 at zero. Emit Z25 in configured output. GS-D05. | Accepted September 10 |
| GSX-D03 | Four R6X/AE4 shortfalls | Add the missing 595 once in each affected leaf, using the component subtotals in §7. GS-D09. | Accepted September 10 |
| GSX-D04 | Conditional D84 absent | Auto-add D84 for the exact convertible stripe/paint contexts with disclosure. On cause loss remove dependency-added D84 and its charge, retain independently selected D84; alert and offer revert. Retain the center-stripe roof disclosure. GS-D04/16. | Accepted September 10 |
| GSX-D05 | EL9/orange D30 gap | Red-belt locking supersedes this historical alternative-belt defect; do not enable the orange pairing. GS-D05. | Accepted September 10 |
| GSX-D06 | VPW/VPO incomplete stripe exclusions | Apply full guide exclusions and refuse conflicting selections in both directions; this explicit blocking policy overrides general replacement offers. GS-D12. | Accepted September 10 |
| GSX-D07 | SAI missing; DUE naming differs | Add SAI across six configurations at 295 with the 3LT V8X conflict; use Royal Blue for DUE. DTC already exists, DUW does not, and no T0E duplicate needs retirement. GS-D01/02/13 applied to actual GSX identities. | Accepted September 10 |
| GSX-D08 | 5ZB has price-only guide support | Preserve the existing workbook choice, consistent with retained Grand Sport cap behavior. Price-only guide evidence remains a provenance limitation, not a renewed owner decision. | Accepted September 10 |
| GSX-D09 | SLN/CF8 and inactive lifecycle options | Show applicable SLN/R88/CF8/RZ9/V8X cards disabled with “Unavailable at this time”, including already-inactive options. Preserve compatibility rules; verify them before release. GS-D11. | Accepted September 10 |
| GSX-D10 | Currency and price basis | USD; raw Price Schedule column E for OPTIONS, preserving base/destination semantics and model-qualified wheel discounts. No wholesale baseline repricing. GS-D14. | Accepted September 10 |
| GSX-D11 | Output/content and ordering scope | Customer configuration form; omitted dealer/service/emissions options remain out of customer selection. Configured equipment reflects replacements; informational equipment remains model/body/trim based. GS-D15. | Accepted September 10 |
| GSX-D12 | General conflicts and dependency loss | Explain and offer replacement before changing selections, except explicit refusal rules. Remove invalid dependents with alert/revert and preserve independent purchase intent. GS-D16. | Accepted September 10 |
| GSX-D13 | HP1 copy | Remove the combined 1,250-hp / 932.1-kW statement and LT7 engine reference. Retain the supported front-axle rating; no replacement combined-power claim. Explicit owner correction September 10. | Accepted September 10 |
| GSX-D14 | ZZ3→LS6→D3V | Remove both LS6-related rules from the accepted target: grand_sport_x_rule_mapping row 51 (grand_sport_x_rule_ls6_includes_d3v_c7bc4b3df65b) and row 82 (grand_sport_x_rule_zz3_includes_ls6_b15b51ebf396). Retain standard LS6 independently, ZZ3→BC7/SL9 and valid coupe cover/package→D3V relationships. These are rule-mapping errors, not errors in the options-sheet disclosure. Frozen rows remain historical evidence. | Accepted September 10, explicit owner instruction |

## 9. Worked sequences and expected outcomes

These are review checks, not newly executed tests. Baseline outcomes preserve
actual observations; accepted target expectations are explicitly distinguished.
Amounts are USD partial-build totals unless the context is described as completed.

| ID | Context / actions | Expected outcome / authority |
|---|---|---|
| GSX-T01 | All six initial contexts | Bases/roof/seat from §3; paint/interior unset; J57/B4Z/FE5 standard, no FED purchase. GSX-O36–41. |
| GSX-T02 | 3LT coupe FED/EL9 → 1LT convertible | Purchases/interior reset; 119,195, CM9. GSX-O49. |
| GSX-T03 | FED with paid caliper/wheel → remove FED | Baseline removes XFR inclusion; retain standard J57/B4Z/FE5 and independent purchases. Target configured tire display returns to XFT; baseline static list is separate. GSX-O01/02, foundation records. |
| GSX-T04 | Coupe 2LT BC4 → B6P → remove B6P → remove BC4 | 118,390 → 120,185 → 118,390 → 117,695; D3V retained by cover until removal, SL9 lost with package, BC7 restored. GSX-O07. |
| GSX-T05 | Convertible 2LT BC4 attempt → ZZ3 → BC4 → remove ZZ3 | First refused; 125,890 → 126,485 → 124,695; unsupported cover/content removed, no D3V. GSX-O42. Accepted GSX-D14 removes the erroneous engine edges; the original sequence is baseline evidence. |
| GSX-T06 | D3V → B6P → remove B6P, no colored cover | Absorbed D3V does not return. Contrast GSX-T04's surviving cover cause. GSX-O09. |
| GSX-T07 | Coupe 2LT 97A → DMU → remove 97A | 118,690 → 119,985 → 117,695; dependent center and Z15 removed. Target adds exact hash-first disclosure. GSX-O10, GSX-D01. |
| GSX-T08 | Completed DTC→hash and hash/center→DTC across six contexts | Baseline permits DTC/hash without Z15, button enabled. Target applies complete DTC conflicts and preserves valid package/output/charge after the accepted interaction. Verify both directions. GSX-O11/12, focused cases, GSX-D01/12. |
| GSX-T09 | Convertible 2LT G26/97A → DMX | Baseline 127,980 without D84; target 129,275 with required D84/disclosure. Test all 17 required cases and nonrequired controls. E-B §4, roof sweep, GSX-D04. |
| GSX-T10 | Required D84 cause lost; repeat with independent D84 | Target removes dependency-added roof/1,295 only, retains independent purchase, alerts/offers revert. Selecting CM9 must not silently leave a stripe/paint state that still requires D84. Supplemental edges; GSX-D04/12. |
| GSX-T11 | Coupe 3LT AH2/EL9 versus AE4/EL9 | Baseline both 124,840, no Z25 code. Target 124,840 / 125,435, Z25 emitted/charged once, zero locked 3F9. Repeat both bodies and remove EL9. GSX-O45/46; GSX-D02. |
| GSX-T12 | Four R6X/AE4 leaves | Target additions 2,085 / 1,590 / 2,780 / 2,285, each +595 once over frozen result. Other leaves retain correct owners. Price sweep, GSX-D03. |
| GSX-T13 | HAG → red attempt; HAG → HVZ; EL9 → orange attempt | Preserve hard HAG refusal and automatic belt exchange; target EL9 refuses alternative belt and supplies 3F9 zero. GSX-O48, belt sweep, GSX-D05. |
| GSX-T14 | 1LT coupe HUQ/G26/orange → G8G → 3F9 | Baseline 115,280 → 114,285 → 112,790; D30 remains for surviving belt cause then disappears. Focused seat/cause records, E-B §3. |
| GSX-T15 | 2LT AH2/HU7/N26/TU7 → AE4 → valid AE4/HU7/N26 | Old interior cleared; missing-interior guard refuses submission until new leaf; valid total 120,485 versus original 120,680, no TU7. Focused records; E-B §3. |
| GSX-T16 | Carbon wheel ↔ chrome; SPY/SPZ → remove SPY; SWN/R8C → ROU | Preserve compatibility sets, remove dependent SPZ, retain delivery. Apply accepted interaction and accurate reason text; no added J57 charge. GSX-O03–05 and edges. |
| GSX-T17 | WUB → NWI → remove WUB | NWI removed, NGA restored, no remaining unsupported charge. GSX-O06. |
| GSX-T18 | Coupe 2LT WKR → SIG → 5ZV → T0E | 118,970 → 119,395 → 121,045 → 118,970; SIG removed and does not return; WKR retains one charge with contextual content. GSX-O30. |
| GSX-T19 | 5JR + ZYC → remove either → remove last | DRG survives first removal only; each selected paid source retains own charge. Supplemental edges; E-B §9. |
| GSX-T20 | SNE/PDA, VWE/PCQ, CAV/PEF, RYT/PDY, SC7/SBT → remove package | Absorbed purchase does not return. SBT retains factory roof and observed CC3 conflicts; target interaction follows applicable policy. GSX-O18/25–29. |
| GSX-T21 | VPW↔DPB and VPO↔DTC | Baseline permits both; target refuses conflicts in both directions using full guide sets. GSX-O19–21, GSX-D06. |
| GSX-T22 | Attempt SLN/R88/CF8/RZ9/V8X in applicable contexts | Target cards visible but disabled with exact unavailability text. Historical CF8 replacement behavior is not target selection permission. GSX-O33, GSX-D09. |
| GSX-T23 | SAI / DUE / HP1; inspect DTC and T0E identities | SAI 295 across six contexts with 3LT V8X conflict; DUE Royal Blue; exact axle-only HP1 copy. DTC/T0E remain single identities; no DUW. GSX-D07/13. |
| GSX-T24 | FED and EL9 in recap/order versus informational equipment | Configured equipment shows XFR/Z25 with correct charges; informational standard list remains context-based. Two static-equipment comparisons are baseline evidence only. GSX-D11. |
| GSX-T25 | ZZ3 engine ownership | Accepted target removes both LS6 rules identified in GSX-D14; LS6 remains standard without ZZ3, and valid cover/package lighting remains. Check the resolved rule set has no source or target opt_ls6_001 in this model mapping; corrected runtime verification is still future work. |

## 10. Coverage and handoff boundary

The record file preserves complete model-scoped baseline lists and all recorded
full-analysis observations. Source comparisons cover 1,368 primary equipment
statuses: 1,212 coded plus 156 uncoded, all matching. The remaining 66 availability
rows concern ten paints and price-only 5ZB; they are not primary-equipment matches.
All 226 repeated coded guide occurrences agree. All 132 interior leaves and 198
component memberships retain their source links; 145 paint surcharge pairs match.
The 136 versus 138 belt-pair discrepancy is preserved, while accepted EL9 red locking
supersedes its two historical orange alternatives.

All 148 numeric option rates retain comparisons: 126 same-code E matches, three
qualified wheel discounts, standard J57, residual-priced Z25 and 17 zero rows
without same-code schedule amounts. Another 91 option prices remain null. Rate
matching alone does not resolve component ownership or certify build totals.

Validation for this handoff verifies frozen workbook/guide identities, exact
fresh workbook extraction versus saved rows, local app/registry bytes against the
archive, model scoping and identity references, source anchors/disclosures,
dispositions, retained observation equality, decision consistency and local links.
No runtime probes were rerun; no corrected target, visual UI, live submission or
production output was tested. Existing observations are not exhaustive interaction
or reversal coverage. Original outputs lack embedded source hashes as disclosed
in §1. The price-only 5ZB provenance limit remains explicit despite accepted retention.

The structured handoff and all business decisions are complete, matching the
Stingray and Grand Sport review stage. Merge of this final decision update remains;
implementation/target verification is later work for all three models. This task stops
here: no Z06 analysis, schema consolidation, canonical workbook change, runtime
implementation, merge or deployment is included.
