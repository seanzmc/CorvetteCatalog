# Z06 structured handoff

September 10, 2026. Complete model review handoff following the established
Stingray, Grand Sport and Grand Sport X structure. The [record file](z06-structured-records.json)
preserves frozen source rows, observed behavior and the twelve accepted owner
decisions from the [behavior analysis](z06-behavior.md). These are review inputs,
not canonical data, an executable ruleset or a new schema.

All twelve decisions are accepted. The owner permits either blocking Z07 while
PDB is selected or requiring a noticed switch to PDD; the precise UI alternative
is not selected. No PDB+Z07 coexistence or silent PDF substitution is authorized.
This handoff does not implement corrections or establish corrected-runtime proof.

## 1. Record conventions and evidence

| Convention | Meaning |
|---|---|
| IDs | Z06-C/R/P/S/V/D/T identify configuration, relationship, price, selection, presentation, decision and expected-check records. They are local review IDs, not database keys. |
| Observations | Z06-O01–61 retain the original sequences and states. Supplemental paths preserve sweeps, eight reversal sequences and the four-state D30 check. |
| Identity | `z06:<legacy option_id>`; additions use `z06:proposed:DTC` and `z06:proposed:SAI`. Both workbook and browser registry keys are `z06`. |
| Scope | Six body/trim configurations intersected with availability, lifecycle and prerequisites. LZ interiors and LT6 paths remain model-owned. |
| Prices | USD; guide OPTIONS column E with qualifiers. Base includes destination; R8E is separate. Null is unknown evidence, not a universal zero. |
| Relationships | Inclusion, prerequisites, alternative prerequisite sets, conflicts, defaults, pricing and cause-loss cleanup remain distinct. Source disclosure alone is not an executed constraint. |
| Evidence and target | Original defective rows and observations remain unchanged. Accepted targets are an overlay; expected checks below are not executed correction tests. |

| Evidence | Identity / locator |
|---|---|
| E-W | [Frozen workbook](../baselines/2026-09-06/README.md), SHA-256 `3127e663b1531e366ce86b989b6190914108d40dfd15a33a258307a05d608e3c`. `baseline_rows` retains source sheet names, original headers/nulls and Excel `_row`. |
| E-G | [Guide provenance](../sources/README.md), unchanged `2027 Chevrolet Car Corvette Export (6).xlsx`, SHA-256 `d3ca7d3a09c9fb89210b4ce584493b3ad8fb65ca35087c49d816d1cbf1a333d1`. Interior/Exterior/Mechanical 4, Standard Equipment 4, Equipment Groups 4 and qualified Color and Trim/Price Schedule. |
| E-O | Frozen browser revision `4fe92a4f078370c478f18484cad31bdafe58ad43`. Previously captured actual browser functions under DOM stubs; zero requests. |
| E-B | [Full behavior analysis](z06-behavior.md), §§1–10. Source anchors and interpretation remain durable review context. |
| E-A | September 10 owner approvals in E-B §9, merged in PR #25. Reproduced exactly in §8 and JSON `owner_review.records`. |

Workbook, app, registry and Z06 contract hashes were checked against the manifest;
local extraction and browser files match the frozen archive. Original observation
outputs do not embed source hashes. Recording their present hashes preserves
artifact identity; it does not retroactively make observations self-attesting.
No new runtime execution, visual browser QA, live submission or external order
validation occurred in this handoff pass.

## 2. Complete record sets and how to use them

Join scoped identities and configurations before interpreting relationships.
Read the accepted overlay before treating a baseline row as a target.

| Category | JSON location / scope |
|---|---|
| Configurations | `baseline_rows.variant_master` and `model_variants`: six each. |
| Offerings | `z06_options` and `offering_dispositions`: all 244; 207 primary coded matches, 26 uncoded equipment matches, ten paints and legacy DUW. |
| Additions / omissions | `accepted_additions`: DTC/SAI with source disclosures and related guide mentions; `guide_only_dispositions`: 20 records, comprising two additions, six interior-component codes and 12 outside customer scope. |
| Applicability | `z06_ovs`: 1,464 exact option/configuration pairs; `z06_variant_overrides`: four UQT overrides. Lifecycle and constraints are additional. |
| Interiors | `LZ_Interiors`, `model_interior_scope`, `interior_source_links`: 130 leaves each; 197 model-qualified `interior_components` memberships; all 21 `PriceRef` rows retained as lookup evidence. |
| Relationships | `z06_rule_mapping`: 110 direct rows; `z06_rule_groups` / `z06_rule_group_members`: 35 / 178; `z06_exclusive_groups` / `z06_exclusive_members`: 13 / 48. |
| Prices and combinations | `z06_price_rules`: 72; model-qualified `color_overrides`: 269 pairs, comprising 137 paint and 132 belt surcharge conditions. |
| Defaults | `default_selection_rules`: five authored rows; standard and section defaults also participate. |
| Presentation | 37 referenced `section_master` rows, eight `section_presentation`, 14 `runtime_steps`, two `context_section_master`, six applicable wildcard `context_choice_copy`, 12 `order_summary_sections`, 14 `step_order_summary_map` and 93 applicable `asset_map` rows. Referenced section definitions include presentation-only references. |
| Routing / intake | One `model_master`, one `model_registry_promotion`, 11 `model_workbook_sources`; six shared `rule_phrase_map` rows and no `runtime_rule_exceptions`. |
| Observations | `observed_sequences`: 61 / 274 states. `supplemental_observations.interior_body_contexts`: 260. |
| Supplemental evidence | `focused`: 54 package states, 99 defect contexts, 60 stripe/paint attempts, eight sequences / 26 states, two equipment records and incomplete-interior submit rejection. `combinations`: 130 price comparisons, 1,300 paint states, 780 belt attempts. `d30_multiple_causes`: four states. |
| Reconciliation | `source_reconciliation`: 207 primary comparisons, 233 repeated coded occurrences, exact interior/paint reconciliation and 155 numeric-price records. Uncoded guide disclosures and anchors reside in offering dispositions. |
| Derived runtime edges | `runtime_derived_relationships`: five exact emitted CBF replacements beyond the 110 direct workbook rows; preserved separately from authored rows. |
| Decisions | `owner_review.records`: all twelve accepted; `pdb_z07_interaction` preserves the authorized alternatives without choosing one. |
| Duplicate audit | `duplicate_rpos_within_model` is empty, including inactive offerings. DUW exists in the baseline; DTC does not. |

For J57, follow its offering through all six availability rows, direct/grouped
relationships, price rules and Z06-O01/O03/O04, then apply Z06-D01. For an R6X
leaf, join exact LZ identity, components and the price sweep before applying
Z06-D08. The four baseline shortfalls stay in the evidence. Do not rewrite
baseline rows or substitute LT pricing to make a comparison pass.

## 3. Configurations and offering scope

| ID | Legacy configuration | Body | Trim | Base USD | Initial R8E | Initial total | Roof / seat |
|---|---|---|---|---:|---:|---:|---|
| Z06-C01 | 1lz_h07 | Coupe | 1LZ | 121,395 | 2,600 | 123,995 | CF7 / AQ9 |
| Z06-C02 | 2lz_h07 | Coupe | 2LZ | 130,295 | 2,600 | 132,895 | CF7 / AQ9 |
| Z06-C03 | 3lz_h07 | Coupe | 3LZ | 134,945 | 2,600 | 137,545 | CF7 / AH2 |
| Z06-C04 | 1lz_h67 | Convertible | 1LZ | 128,395 | 2,600 | 130,995 | CM9 / AQ9 |
| Z06-C05 | 2lz_h67 | Convertible | 2LZ | 137,295 | 2,600 | 139,895 | CM9 / AQ9 |
| Z06-C06 | 3lz_h67 | Convertible | 3LZ | 141,945 | 2,600 | 144,545 | CM9 / AH2 |

E-W `model_variants!20:25`, `variant_master!20:25`; E-G Price Schedule
25/30/31/28/32/33, F + J. Destination 2,495 is already included. Z06-O47–52
capture starting states and UQT behavior. Initial paint/interior remain unset.
J56, FE6, XFR, LT6, M1M, B4Z and WUB are standard. J57 is a purchase or inclusion,
not a standard GSX-like brake. EYT/J6A/T0E/SOE/NGA/EFR/R8E and black 719 start
selected along with the roof and seat above.

UQT is 1,495 at 1LZ and included/display-only at 2LZ/3LZ. E60/BAZ/FA5 begin
at 2LZ; DY0/FA6/5JR at 3LZ. W2D is a 1LZ accessory, AP9 supplied at higher
trims; UV6/DRZ are standard even at 1LZ. Preserve the audio, charging, mirror
and camera trim changes recorded in E-B §2. Coupe roofs, B6P and RXI/SLN differ
from convertible ZZ3/D84/D86 paths. Interior leaves comprise four 1LZ, 40 2LZ,
71 ordinary 3LZ and 15 R6X 3LZ. EL9 is not applicable.

## 4. Price ownership and interpretation

| ID | Owner / condition | Baseline and accepted target | Evidence |
|---|---|---|---|
| Z06-P01 | Base / R8E | Preserve §3 bases. R8E 2,600 becomes 3,000 with T0F/T0G, including package acquisition; not every carbon wheel or Z07 label independently. | E-B §2; Z06-D12; price rows 50–51 |
| Z06-P02 | J57 / Z07 | J57 9,000 alone. Z07 9,500 plus default T0F 8,995 or T0G 10,995; included J57/FE7/XFS/ground effects do not charge again. | E-B §3; Z06-D01 |
| Z06-P03 | Carbon packages | PDB ROY/ROZ/STZ: 16,000/17,000/17,500. PDD: 25,495/26,495/26,995. PDF: 26,495/27,495/27,995. Minimum package plus wheel delta is one amount; do not add override and delta twice. | Price Schedule 52–60; 54-state matrix |
| Z06-P04 | Standalone carbon wheels | ROY/ROZ/STZ 11,995/13,995/15,500, requiring J57. These are not package deltas or GSX discounted rates. | E-B §3 |
| Z06-P05 | PCZ | 5,295 includes 5DK/SFZ/SHT/VPO once. Baseline separately charges their 5,770 total. Target removes duplicate child charges and applies full constraints. | E-B §6; Z06-D02 |
| Z06-P06 | SBT / SC7 | Target 2,525 total, SC7 zero; baseline 2,720. Preserve independent pouch intent through package removal. | Exterior 4 47; Interior 4 40; Price Schedule 131; Z06-D06 |
| Z06-P07 | Four R6X/AE4 leaves | Target HUU 1,590; HU0/38S 2,085; HZP/N2Z 2,485; HXO/N2Z/38S 2,980. Each baseline is 595 lower. Retain R6X 995, N2Z 895 and stitching 495. | `LZ_Interiors` rows 121/124/129/131; Z06-D08 |
| Z06-P08 | Ordinary interiors | AE4 1,095/2,095/595 by trim; AH2 1,695 at 2LZ, standard at 3LZ; AUP 350 for HAG and HVZ. N26 695 at applicable 1LZ/2LZ paths; N2Z 895 at 3LZ; TU7 595, optional stitch 495. | E-B §7; component links; Z06-D12 |
| Z06-P09 | D30 | One 1,495 charge while any paint or belt cause survives. Recommendations do not become hard color prohibitions. Hard HAG/HVZ belt restrictions cannot be purchased away. | 269 combination rows; four-state cause check |
| Z06-P10 | BCW / appearance | Coupe BCW 995 alone, 895 with B6P 1,895; D3V zero. Convertible BCW 895 requires ZZ3 1,195; SL9 supplied, no D3V. PBC 9,995, convertible requires ZZ3. | Mechanical 4 24–40; Z06-O25/O53/O54 |
| Z06-P11 | Other package / accessory rates | PCQ 1,675, PEF 475, PDY 195 and PDA 950 have zero-priced children. E60 2,995 supplies TR7; NWI 395 uses standard WUB. Preserve all other qualified baseline amounts. | E-B §§5/6/8; 72 price rules |
| Z06-P12 | Accepted offerings | DTC 1,295 replaces DUW; SAI 295; DUE naming becomes Royal Blue. Preserve raw contradictory DUW disclosures and AUP qualifier. | Z06-D09/D12; Price Schedule 257/128 |

The LZ stored Price is extras-only. Legacy assembly subtracts the ordinary seat
rate before adding R6X; browser itemization suppresses a separate seat when R6X
is present. The missing AE4 component creates the four 595 shortfalls; this is
not the LT stored-composite explanation. Bare 2LZ AE4 shows 1,095 until a valid
ordinary interior resolves 2,095. An incomplete interior cannot be submitted;
do not misclassify that transient display as a completed undercharge.

## 5. Connected relationship records

Frozen interaction directions below are observations. Accepted selection policies
in §6 control future behavior where they differ.

| ID | Trigger / eligibility | Consequences, removal and ownership | Evidence |
|---|---|---|---|
| Z06-R01 | Body/trim change | Reset purchases/interior and restore context defaults, including roof, seat and R8E. | Z06-O61; E-B §2 |
| Z06-R02 | J57 / calipers / wheels | Replace J56/J6A; target includes default gray J6D. Permit compatible paid alternatives. J6L/J6D and carbon wheels require J57; downgrade removes invalid dependents, restores defaults, retains valid independent J6F. | Z06-O01–03; focused edges; Z06-D01 |
| Z06-R03 | Z07 / aero | Includes J57/FE7/XFS/CFZ and default T0F; T0G substitutes CFV. Block J56/T0E/5ZV while Z07 remains. Independently supported aero may survive Z07 removal. | Z06-O04/05; E-B §3 |
| Z06-R04 | PDB/PDD/PDF | Mutually replace; default ROY, permitted carbon wheel alternatives. PDB includes J57/J6D; PDD includes Z07/T0F; PDF Z07/T0G. PDD/PDF lock their aero. Package loss restores J56/J6A/SOE/T0E absent another valid cause. | Z06-O06–10; matrix; Z06-D01 |
| Z06-R05 | PDB + standalone Z07 | Frozen coexistence in either order preserves remaining cause on removal and costs 9,000 more than PDD. Target disallows coexistence; block or require noticed PDD switch. | Z06-O11/12; Z06-D11 |
| Z06-R06 | Aero / ground effects / CBF | T0F→CFZ and T0G→CFV at zero; alternate ground effects/CFL blocked while included. Five emitted T0F/T0G/Z07/PDD/PDF→CBF replacement edges arise from inclusion closure, beyond 110 workbook rules. Preserve explicit translation ownership. | Z06-O13/14; focused CBF edge; E-B §4 |
| Z06-R07 | Accents / physical finish | CBF conflicts with GBA/EFY/CFV/CFZ; EDU+CBF allowed. GBA after EDU+CBF removes both and restores EFR. CFV/CFZ alter supplied surfaces, not option identities. Retain differing interaction directions as baseline evidence. | Z06-O16–18; Exterior 4 18–21 |
| Z06-R08 | Spoiler / cover | SIG requires T0E; 5ZV removes SIG, returning to T0E permits it again. WKR high-wing version is contextual content, not another cover purchase. | Z06-O15; Exterior 4 37/51–53 |
| Z06-R09 | Convertible roofs / mirrors | D84/D86 incompatible with GBA; ZYC includes DRG. Frozen GBA transition removes finish/mirrors and restores CM9. 5JR/ZYC independently support DRG until last cause disappears. | Z06-O55; focused mirror causes |
| Z06-R10 | Coupe BCW/B6P/D3V | BCW supplies D3V; B6P discounts BCW and supplies D3V/SL9. Removing B6P retains D3V while BCW supports it. Frozen absorbed independent D3V does not return without another cause; target preserves independent intent. | Z06-O25/26; E-B §5 |
| Z06-R11 | Convertible ZZ3/BCW/PBC | BCW/PBC prerequisites explicitly convertible-scoped. Removing ZZ3 invalidates both and removes unsupported SL9. No GSX ZZ3→LS6 relationship belongs here. | Z06-O53/54 |
| Z06-R12 | RXI / SLN | Frozen permits both in both directions; target enforces conflict. SLN stays available otherwise. | Z06-O27/28; Z06-D07 |
| Z06-R13 | Exhaust / lift | Standard WUB; NWI replaces NGA and removal restores it. E60 includes TR7, removed with last cause. | Z06-O29/30 |
| Z06-R14 | PCZ | Target includes 5DK/SFZ/SHT/VPO and complete exclusions: R8C, listed hardware/carbon wheels, EYK, PDA/SNE/VPW and all 16 listed stripes. Preserve child price and independent-removal ownership together. | Exterior 4 32; Z06-O22–24; Z06-D02 |
| Z06-R15 | 5DH/5DK second sets | Keep factory wheels. Apply R8C, SPZ/SFE/SPY/S47 and ROY/ROZ/STZ restrictions; include hardware physically without extra purchases. | Exterior 4 64–65; Z06-O20/21; Z06-D03 |
| Z06-R16 | Standalone hardware / delivery | SPZ requires SPY; loss removes SPZ. S47/SFE conflict with carbon wheels/SPY. R8C includes CFX and blocks BV4; external SOLD/BAC/acknowledgement remains a disclosure. | Z06-O19–21; E-B §6 |
| Z06-R17 | Stripe / paint | Enforce exactly 15 source pairs in both directions: DUE/DPB vs GTR; DUK/DPL/DSZ/DZX vs GKZ/GPH; DPC/DT0/DZU vs GBK; DPG/DSY vs G26. DTC adds its GTR restriction under D09. | Z06-O43/44; 60-attempt sweep; Z06-D04/D09 |
| Z06-R18 | Rear hashes / badges / Jake | Complete VPW/VPO conflicts; explicitly refuse conflicting stripes, give badge replacement notice. VPO excludes EYK. PDA includes SNE/VPW at zero; preserve hood and stripe conflicts. | Z06-O36–40; Z06-D05 |
| Z06-R19 | SFZ / stripes | Frozen SFZ after DPB removes DPB; reverse refused. Retain full source conflict sets; apply general replacement policy where no explicit refusal exception controls. | Z06-O41/42 |
| Z06-R20 | SBT and accessory packages | SBT includes SC7 and a second transparent panel, conflicts with CC3. PCQ includes VWE/VWT; PEF CAV/RIA; PDY RYT/S08. Frozen removal loses absorbed independent purchases; accepted target preserves intent. | Z06-O31–35; Z06-D06 |
| Z06-R21 | Interiors / belts / D30 | Valid leaf required after seat change; TU7/N2Z/stitch follow exact chart paths. HAG blue-only, HVZ red-only; other compatible paid belts can replace included defaults. D30 retains all surviving causes once. | Z06-O58–60; interior/paint/belt sweeps |
| Z06-R22 | Trim / equipment / lifecycle | BAZ and FA5 coexist; FA6 replaces FA5 at 3LZ, DY0 independent. Target N3W standard at 3LZ, removed by N2Z. Unavailable accessories displayed disabled, separate from standard equipment. | Z06-O56/57; Z06-D10 |
| Z06-R23 | Remaining accessories | Keep caps, indoor covers, badges and suede liners in their own groups; outdoor RWJ separately scoped. ERI/VUP/SLK/RWU/S2L remain independent. | Z06-O45/46; E-B §8 |

Full guide conflict wording is retained in offering dispositions and addition
mentions, not reduced to the example pairs above. Z06 has no Z15, Z25, heritage
hash or EL9 choice; do not import earlier-model relationships. Old LS6/Z51/TVS
workbook wording remains provenance while actual Z06 endpoints remain D3V/DRG.

## 6. Selection and reconciliation policies

| ID | Event | Accepted target / preservation |
|---|---|---|
| Z06-S01 | Context reset | Establish body/trim defaults after clearing prior purchases/interior. |
| Z06-S02 | General conflict | Explain and offer replacement before changing selections; explicit refusal exceptions take precedence. |
| Z06-S03 | Rear hash conflicts | Refuse conflicting stripes in both directions; use replacement notice for badges. Do not flatten these into a single conflict action. |
| Z06-S04 | Dependency loss | Remove invalid dependents and charges with alert/revert; preserve independent purchase intent. Frozen absorbed-purchase loss remains historical evidence. |
| Z06-S05 | Multiple causes | Retain content while any valid cause survives; charge once. Distinguish acquired defaults, locked package content and independent choices. |
| Z06-S06 | Lifecycle | Display applicable unavailable R88/RYQ/V8X/5V5/CF8 disabled with unavailable wording. N3W is standard, not lifecycle-unavailable; N2Z replaces it in the configured build. |
| Z06-S07 | PDB/Z07 | Prevent coexistence, in either acquisition order. Preserve the owner's two allowed UI alternatives without choosing a silent substitution. |
| Z06-S08 | Required selections | Enforce paint/interior and required section choices. J57 inclusion must fill caliper default while allowing compatible upgrades. Included equipment and pricing must agree in recap/order. |

## 7. Presentation, physical content and operational boundaries

| ID | Subject | Target / evidence |
|---|---|---|
| Z06-V01 | Package prices | Show package base plus wheel increment once; included children zero. Explain PDD switch before accepting Z07 with PDB. |
| Z06-V02 | Equipment views | Informational baseline remains model/body/trim based. Configured equipment reflects FE6/XFR→FE7/XFS and N3W→N2Z replacements. Never label static equipment as a complete installed inventory. |
| Z06-V03 | Physical content | Preserve finish coverage, convertible tonneau distinctions, WKR version, second wheel-set hardware and SBT's extra panel without invented purchase identities. |
| Z06-V04 | Availability and copy | Unavailable cards remain visible disabled; DUE becomes Royal Blue. Preserve DUW contradictions and AUP source qualifier alongside accepted target. |
| Z06-V05 | Customer scope | Six service/interior and six emissions codes remain outside customer selection. SOLD/BAC/approval/PBC/VK3 requirements remain disclosures; no external enforcement or order acceptance is certified. |
| Z06-V06 | Routing / assets | Preserve scoped section modes, step order, summary routing, copy and asset references. Asset mapping is not visualizer or browser-layout proof. |

## 8. Decision overlay: source, baseline and target remain separate

All twelve entries below reproduce the accepted behavior-document targets.
Frozen findings in E-B §§2–9 and JSON are not overwritten by these decisions.

| ID | Accepted target | State |
|---|---|---|
| Z06-D01 | Add J57→J6D default inclusion, allowing compatible paid caliper upgrades. Confirm J57/Z07/PDD/PDF acquisition and default restoration across all configurations. J6D is gray; the conversational review list incorrectly called it red. The approved code is unchanged. | Accepted September 10 |
| Z06-D02 | Implement PCZ's four contents (5DK, SFZ, SHT, VPO) once at its 5,295 charge, with zero additional child charges, full guide conflicts and explicit child/removal ownership under the accepted independent-purchase policy. | Accepted September 10 |
| Z06-D03 | Implement 5DH/5DK second-set exclusions. Retain factory wheels; represent included black lug nuts/locks and 5DK bronze caps as supplied content without duplicate accessory charges. | Accepted September 10 |
| Z06-D04 | Apply all 15 inspected stripe/paint prohibition pairs in both directions; retain non-prohibited combinations. | Accepted September 10 |
| Z06-D05 | Complete VPW/VPO stripe and package/badge conflicts. Explicitly refuse conflicting stripes in both directions. Use a replacement notice for conflicting badges, following the accepted replacement-offer policy rather than silent replacement. | Accepted September 10 |
| Z06-D06 | Price SC7 at zero under SBT so the package costs 2,525, not 2,720. Preserve independent-purchase intent according to the accepted application policy, including a pouch purchased before SBT and subsequent package removal. | Accepted September 10 |
| Z06-D07 | Enforce RXI/SLN conflict in both directions using the accepted general conflict policy. Keep Z06 SLN available otherwise; do not classify it as lifecycle-unavailable. | Accepted September 10 |
| Z06-D08 | Restore each of the four missing AE4 595 charges listed in §7, retaining N2Z 895 and all other model-qualified components. | Accepted September 10 |
| Z06-D09 | Replace legacy DUW with DTC at 1,295 and all its relationships, including the GTR prohibition. Rename DUE to Royal Blue. Add SAI at 295 across all six configurations with its 3LZ V8X exclusion. Preserve raw source contradictions. | Accepted September 10 |
| Z06-D10 | Display unavailable R88/RYQ/V8X/5V5/CF8 accessories as disabled, with unavailable-at-this-time presentation. Restore N3W as 3LZ standard equipment, separate from N2Z; selecting N2Z removes N3W from the configured equipment. | Accepted September 10 |
| Z06-D11 | Do not permit PDB and standalone Z07 to coexist. Make Z07 nonselectable with PDB, or require a switch to PDD with notice before accepting Z07. The owner authorized either interaction; the combined 9,000-premium path is rejected. Do not silently substitute a package or infer approval for a PDF substitution. | Accepted September 10 |
| Z06-D12 | Use USD and raw Price Schedule column E for option amounts. Destination is included once in base; R8E is separate at 2,600, rising to 3,000 with T0F/T0G. Permit AUP HAG and HVZ at 350 while preserving the guide qualifier inconsistency. Keep customer-form ordering scope and external approval/delivery disclosures without claiming external enforcement. Distinguish baseline informational equipment from the configured installed build, reflecting replacements such as FE6/XFR→FE7/XFS. | Accepted September 10 |

## 9. Worked sequences and expected outcomes

These are review checks for later implementation. Baseline figures are observed;
accepted target expectations are not newly executed tests. Totals are partial
builds unless described as completed, with no paint/interior cost unless specified.

| ID | Context / actions | Expected outcome / authority |
|---|---|---|
| Z06-T01 | All six initial configurations | §3 bases plus R8E, standard J56/FE6/XFR and context defaults; paint/interior unset. Z06-O47–52. |
| Z06-T02 | 3LZ coupe PDF/interior → 1LZ convertible | Reset to 130,995 with CM9/AQ9 and no previous package/interior. Z06-O61. |
| Z06-T03 | Each context J57, Z07, PDD or PDF | Target default J6D, no caliper requirement gap, single content charge. Repeat paid caliper upgrades and downgrade/removal; valid independent J6F survives. Z06-D01; matrix and focused defects. |
| Z06-T04 | Coupe 2LZ PDB → ROZ → PDD → STZ → PDF → remove PDF | Observed totals 148,895 → 149,895 → 159,790 → 160,290 → 161,290 → 132,895. Target repairs missing J6D without changing valid package totals. Z06-O06. |
| Z06-T05 | All 54 package/wheel/body/trim states | Match nine §4 package rates; PDB R8E 2,600, PDD/PDF 3,000. No duplicate wheel delta; required caliper filled in target. |
| Z06-T06 | PDB → Z07 and reverse | Frozen coexistence 167,790 with ROY/T0F versus PDD 158,790 in coupe 2LZ. Target prevents coexistence; block or require noticed PDD switch. Verify decline leaves a valid prior state. Z06-D11. |
| Z06-T07 | Coupe 3LZ J57 → J6L → ROY → J56 | Remove unsupported caliper/wheel; restore J6A/SOE and 137,545. Independent J6F variant retains its charge. Focused brake edges. |
| Z06-T08 | Coupe 3LZ T0G → T0E | 148,940 → 137,545: lose aero and 400 R8E increment. CBF→T0F must apply the derived replacement. Focused tax/CBF edges. |
| Z06-T09 | Coupe 2LZ PCZ, then its four contents | Target 138,190 with all four codes and no additional 5,770; baseline 143,960 after separate purchases. Exercise each complete guide conflict, child ownership and package removal. Z06-D02. |
| Z06-T10 | 5DH/5DK versus R8C, hardware and carbon wheels | Target prevents every source-listed conflict in both directions; retains factory wheels and supplied hardware without new charges. Baseline completed invalid cases remain recorded. Z06-D03. |
| Z06-T11 | All 15 stripe/paint pairs, both bodies and directions | Baseline all 60 attempts retain both. Target enforces prohibitions; non-prohibited DPT/DTH/DUB/DZV controls remain available. New DTC/GTR has separate coverage. Z06-D04/D09. |
| Z06-T12 | VPW/VPO + conflicting stripe; VPO + EYK | Target stripe refused in either direction; badge replacement notice before change. Test PDA/PCZ interactions against full retained disclosures. Z06-D05. |
| Z06-T13 | Coupe 2LZ SBT; repeat after SC7 purchase | Target 135,420 while SBT selected versus frozen 135,615. Removal preserves independent pouch intent; CC3 conflict remains. Z06-D06. |
| Z06-T14 | Each coupe trim RXI→SLN and reverse | Target prevents coexistence with conflict interaction; SLN independently remains available. Frozen coupe 2LZ invalid total 138,285 is not a target. Z06-D07. |
| Z06-T15 | Four exact R6X/AE4 leaves, both bodies | Add 595 once; preserve N2Z/stitch/R6X rates. HXO/N2Z/38S coupe 3LZ target 140,525 versus frozen 139,930. Other 126 leaves retain applicable component totals. Z06-D08. |
| Z06-T16 | DTC / DUW / DUE / SAI | Target DTC once at 1,295 with all relationships; DUW retired, DUE Royal Blue, SAI 295 in six contexts with 3LZ V8X restriction retained even though V8X disabled. Z06-D09. |
| Z06-T17 | Lifecycle cards and 3LZ steering equipment | Unavailable accessories visible disabled; N3W present as standard, removed by N2Z in configured output. Verify N3W default restored when its replacement no longer applies. Z06-D10. |
| Z06-T18 | Coupe 2LZ BCW → B6P → remove B6P → remove BCW | Observed 133,890 → 135,685 → 133,890 → 132,895; D3V survives while BCW remains, SL9 loses last cause. Independently purchased D3V additionally follows target intent policy. Z06-O25/26. |
| Z06-T19 | Convertible 2LZ ZZ3 → BCW → PBC → remove ZZ3 | 141,090 → 141,985 → 151,980 → 139,895; clear invalid BCW/PBC and SL9 with target alert/revert. Attempts before prerequisite are refused. Z06-O53. |
| Z06-T20 | Convertible 2LZ G8G → D84 → ZYC → GBA | Frozen 139,895 → 141,190 → 141,485 → 139,895. Target explains conflict replacement/dependency loss. Repeat 5JR+ZYC: DRG survives until both causes disappear. Z06-O55 and focused mirror edge. |
| Z06-T21 | 1LZ coupe HUQ, G26 → orange belt → G8G → red belt | 126,485 → 127,080 → 126,085 → 124,590; D30 survives one cause, disappears with last, never duplicates. Four-state D30 record. |
| Z06-T22 | All 130 leaves / both bodies, paint and belt sweeps | Preserve 260 valid contexts, 137 paint and 132 belt conditions, 1,300 paint states and 780 belt attempts. HAG blue-only/HVZ red-only, other permitted paid belt upgrades and AUP 350 preserved. |
| Z06-T23 | PCQ/PEF/PDY/PDA independent child → package → removal | Included children zero while package selected. Preserve independent intent in target versus frozen absorption loss. Verify last-cause removal and no duplicate line. Z06-O31–33/O36. |
| Z06-T24 | Valid configuration → incompatible seat, no replacement interior | Incomplete-interior submit rejected, no request. Bare AE4 price is not a completed build. Recap/order must reflect accepted equipment replacements; valid external submission remains untested. Focused rejection/equipment evidence. |
| Z06-T25 | 5ZV/SIG, NWI, E60, accents, peer/independent accessories | Preserve connected behavior and scoped rates from Z06-O13–19/O29–30/O45–46; apply accepted conflict/cleanup notices where required. No invented prerequisite WUB purchase. |

## 10. Verification, limitations and next boundary

Handoff checks verify frozen hashes and exact extraction; every retained workbook
row and its source locator; complete model scope and offering dispositions;
unique nonblank RPOs; option/configuration, relationship/group, price, interior,
section and decision references; guide status/base-price reconciliation; exact
observation preservation; numeric source anchors; accepted overlay equality; and
Markdown links. The companion JSON retains all original sequence states and
supplemental outcomes, including invalid completed builds and blocked attempts.

The baseline analysis observed 87 of 99 completed defect contexts with enabled
submission and no missing requirement; 12 J57/Z07 caliper cases correctly blocked.
PDD/PDF gaps also appear in the separate package matrix. Only incomplete-interior
submit rejection was executed. No valid submit handler, customer order, visual
browser check or corrected runtime was exercised. These are coverage limits,
not successful verification of the accepted corrections.

This completes Z06's structured review handoff and accepted decision stage.
Implementation, correction tests and final UI choice within D11's alternatives
remain later work. ZR1 and ZR1X are subsequent model lanes; schema consolidation,
canonical workbook changes, deployment and cutover remain outside this pass.
