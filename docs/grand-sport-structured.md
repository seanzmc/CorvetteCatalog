# Grand Sport structured model handoff

**September 10 discovery catch-up:** the [current completion review](model-discovery.md#grand-sport) supplements this historical analysis with retained source/price accounting, full starting-choice observations and additional connected behavior/output evidence. Read it before interpreting older statements about unfinished coverage. Original facts, observations and accepted decisions below remain unchanged.

September 9, 2026. Model: **Grand Sport, 2027**. Status: **structured review input**.

This document organizes the [behavior analysis](grand-sport-behavior.md) into
facts, conditions, actions, charges, evidence and decisions. Its companion
[record file](grand-sport-structured-records.json) preserves complete model-scoped
baseline lists, all 44 recorded sequences and the supplemental observations.
It follows the [Stingray handoff](stingray-structured.md)'s categories for comparison,
while retaining Grand Sport's own identities, rules and owner decisions.
Neither file is a new canonical dataset, executable ruleset or database schema.
The [Stingray schema proposal](stingray-schema-plan.md) is a design reference,
not a required storage format for these review records.


**September 9 owner review:** the decisions in §8 supersede earlier unresolved
or proposed target language in this handoff and the linked behavior/schema analyses.
Frozen workbook rows, source disclosures and observed sequences remain historical
evidence, including their old labels, prices and conflict actions. Accepted target
changes are not implementation or runtime verification.

## 1. Record conventions and evidence

Use the same categories for each model: configurations, offerings, applicability,
interiors/parts, relationships, prices, selection behavior, presentation/content,
evidence/decisions and expected sequences. Matching RPOs do not establish shared
identity or authorize copying another model's decisions.

| Convention | Meaning |
|---|---|
| `GS-C`, `GS-R`, `GS-P`, `GS-S`, `GS-V`, `GS-D`, `GS-T` | Local configuration, relationship, price, selection, presentation, decision and target-check IDs. Review references, not database keys. |
| `GS-O01`–`GS-O44` | Original sequences, with every captured state and original field layout retained. Supplemental sweeps are separate records, not additional sequences. |
| Identity | Existing offerings use `grand_sport:<legacy option_id>`; additions use provisional `grand_sport:proposed:<RPO>`. Browser registry key is `grandSport`, workbook key is `grand_sport`. |
| Baseline versus target | Frozen evidence remains unchanged, including defects. Only explicit accepted corrections establish target changes. Proposed presentation and unresolved facts remain labeled. |
| Evidence versus review state | Coded/uncoded matches, missing offerings, duplicate identities and conflicting facts are evidence classifications; accepted, proposed and unresolved are decision states. |
| Scope | `All` means the six GS-C configurations, intersected with effective option/interior applicability. Unknown scope is unresolved. |
| Conditions | Keep eligibility, auto-add, price override, refusal/replacement and removal separate. `AND` requires every condition; `ANY(...)` requires at least one. |
| Prices | Preserve the frozen numeric basis. Zero is known zero; null is unknown. Destination is already in base amounts. Guide OPTIONS use Price Schedule column E; all prices are USD, confirmed by the owner after PR #20. |
| Completeness | Complete baseline lists do not mean all target decisions or interaction directions are resolved. Neither file is release acceptance. |

| Evidence ID | Identity / locator | Use |
|---|---|---|
| E-W | [Frozen workbook](../baselines/2026-09-06/README.md), SHA-256 `3127e663b1531e366ce86b989b6190914108d40dfd15a33a258307a05d608e3c` | `baseline_rows.<sheet>` preserves original headers, nulls, ordering and `_row` Excel row numbers. |
| E-G | [Manufacturer guide](../sources/README.md), `2027 Chevrolet Car Corvette Export (6).xlsx`, SHA-256 `d3ca7d3a09c9fb89210b4ce584493b3ad8fb65ca35087c49d816d1cbf1a333d1` | Interior/Exterior/Mechanical 2, associated equipment sheets and model-qualified Color and Trim tables. |
| E-O | Frozen browser commit `4fe92a4f078370c478f18484cad31bdafe58ad43` | Existing DOM-stub observations: 44 sequences / 199 states. No new runtime execution, visual QA or live submission in this handoff. |
| E-B | [Grand Sport analysis](grand-sport-behavior.md), §§1–12 | Connected interpretation, source traces, coverage and limits. |
| E-A | [Owner decisions](grand-sport-behavior.md#owner-review-decisions--september-8-2026), September 8 | Earlier Grand Sport decisions; September 9 updates in §8 supersede the Z15 card proposal. |
| E-S | [Stingray schema proposal](stingray-schema-plan.md), compared in E-B §12 | Design reasoning only; conditional stripe/paint prerequisite ownership is still a cross-model design obligation. |

Original Grand Sport observation JSON does not embed source hashes. The record
file identifies that limitation, retains current hashes of the original outputs
and probe sources, and records the current comparison of local browser bytes with
the frozen archive. E-B §1 and the probe's explicit `grandSport` activation identify
the recorded context. This does not retroactively make the outputs self-attesting.

## 2. Complete record sets and how to use them

Read the JSON with this document: `baseline_rows` is evidence, while offering
and GS-D decisions describe departures. **Do not import the baseline as the
accepted target**, flatten all source rule types, or silently discard dormant rows.

| Category | Record-file location | Scope / disposition |
|---|---|---|
| Configurations | `baseline_rows.variant_master`, `model_variants` | Six configurations and six model memberships. |
| Offerings | `grandSport_options`, `offering_dispositions` | All 241: 204 coded guide matches, 25 uncoded equipment mappings, 10 paints, dormant T0E duplicate, legacy DUW. |
| Additions / omissions | `accepted_additions`, `guide_only_dispositions` | DTC/SAI additions with guide disclosures and related mentions; components, services, emissions, VK3 and uncoded OnStar Basics remain separately classified. |
| Applicability / overrides | `grandSport_ovs`, `grandSport_variant_overrides` | All 1,446 status rows and four UQT contextual overrides. Active state and relationships also affect selection. |
| Interior choices | `lt_interiors`, `model_interior_scope`, `interior_source_links` | All 132 leaves, including two EL9 choices; exact guide cells, workbook rows and component references. |
| Interior parts / rates | `interior_components`, `PriceRef` | 198 memberships and 21 legacy source rates. Retain old EL9 residual pricing and four R6X shortfalls as evidence. |
| Direct relationships | `grandSport_rule_mapping` | All 157 rows, original scopes and text. |
| Grouped relationships | `grandSport_rule_groups`, `grandSport_rule_group_members` | All 49 groups / 324 members. Separate alternative prerequisite sets remain separate. |
| Exclusive groups | `grandSport_exclusive_groups`, `grandSport_exclusive_members` | All 12 groups / 37 members, including inactive WUB membership. Section-level choice modes are additional evidence. |
| Conditional prices | `grandSport_price_rules` | All 55 rows. No invented package minimum/delta schedule. |
| Combination additions | `color_overrides` | All 281 exact pairs: 145 paint and 136 belt conditions adding D30. Guide's two extra EL9/orange conditions are historical gaps, superseded by target belt locking. |
| Defaults | `default_selection_rules` | Four explicit rules: J6D with J57, NGA, coupe BC7, T0E. Initial section/standard defaults are additional evidence. |
| Presentation | `section_master`, `section_presentation`, `runtime_steps`, `context_section_master`, `context_choice_copy`, `order_summary_sections`, `step_order_summary_map`, `asset_map` | Scoped presentation plus all referenced section definitions and applicable wildcard rows. Shared storage does not approve shared ownership. |
| Routing / intake | `model_master`, `model_registry_promotion`, `model_workbook_sources`, `rule_phrase_map`, `runtime_rule_exceptions` | Model metadata, 11 source routes, six phrase rows, empty exception list. Historical source routing is not a future authoring contract. |
| Observed sequences | `observed_sequences` | Original names, selections, auto-additions, line items, totals and missing requirements for 44 sequences / 199 states. |
| Supplemental observations | `supplemental_observations` | 264 interior/body contexts; 132 price comparisons; 1,320 paint states; 792 belt attempts; 100 stripe/body/paint states; six completed-context package-removal guard checks. |
| Source comparison | `source_reconciliation` | 204 primary coded comparisons, 233 repeated equipment-sheet occurrences, interior/component and recommended-paint reconciliation. Uncoded source anchors are in offering dispositions. |
| Duplicate audit | `duplicate_rpos_within_model` | T0E: dormant `opt_t0e_002` and active `opt_t0e_001`. Neither automatically becomes a second target product. |

Workbook sheet locations in the table are under `baseline_rows`; other locations
are top-level JSON keys. For example, find `opt_t0f_001` in `grandSport_options`,
its six status rows and direct/grouped/price relationships, then read GS-R08/09
and GS-D06 for baseline versus target removal. For EL9, join its exact leaf IDs
to scope, components, combination rows and source links; GS-P02 resolves target
charge ownership without rewriting the legacy rows.

Supplemental `priceResults.expected` means the earlier component-sum comparison,
**not an accepted target total**. In particular, EL9's 0/595 component expectations
omit its Launch Edition content; use GS-P02 and GS-D05 for the reviewed target.

## 3. Configurations and offering scope

| ID | Legacy configuration | Body | Trim | Base | Starting roof | Starting seat |
|---|---|---|---|---:|---|---|
| GS-C01 | `1lt_e07` | Coupe | 1LT | 88,495 | CF7 | AQ9 |
| GS-C02 | `2lt_e07` | Coupe | 2LT | 95,595 | CF7 | AQ9 |
| GS-C03 | `3lt_e07` | Coupe | 3LT | 100,245 | CF7 | AH2 |
| GS-C04 | `1lt_e67` | Convertible | 1LT | 95,495 | CM9 | AQ9 |
| GS-C05 | `2lt_e67` | Convertible | 2LT | 102,595 | CM9 | AQ9 |
| GS-C06 | `3lt_e67` | Convertible | 3LT | 107,245 | CM9 | AH2 |

E-W `variant_master!A8:H13`, `model_variants!A2:E7`; E-G Price Schedule rows
15/18/19/17/20/21, columns F + J; E-O GS-O31–36. No second destination charge.
Coupe starts with BC7; convertible has no selected engine cover. Baseline touring
equipment includes FEA/JX6/XFT, LS6/M1N and cooling; FEB/FEY are not initial purchases.
B4Z's baseline standard status is an accepted scope correction, GS-D08.

UQT is a 1,495 purchase at 1LT and included display-only at 2LT/3LT. E60 is
unavailable at 1LT; BAZ/FA5 begin at 2LT; 5JR at 3LT. B6P is coupe-only, ZZ3
convertible-only; D84/D86 are convertible treatments, while C2Z/CC3/CF8/SBT belong
to coupe. Preserve applicability separately from lifecycle warnings (GS-D11).
Interior eligibility is 4 leaves at 1LT, 40 at 2LT, 73 ordinary 3LT and 15 custom
R6X 3LT, totaling 132; EL9 contributes two of the ordinary 3LT leaves. E-B §§2–3.

## 4. Price ownership and interpretation

| ID | Condition / owner | Baseline and target meaning | Evidence |
|---|---|---|---|
| GS-P01 | Base / option rates | Preserve six bases and exact legacy option/conditional rates. Missing rates do not mean free. UQT's trim override does not create another product. | E-W; E-B §§1–2 |
| GS-P02 | EL9 → Z25 | Baseline AH2/EL9 and AE4/EL9 both add 1,995: AE4 itemizes 595 seat + 1,400 interior; Z25 is zero. Accepted target: Z25 owns 1,995 content once, AH2 adds zero, AE4 adds another 595. Coupe 3LT totals 102,240 / 102,835. Disclose Z25 cost on EL9 selection. | E-W options row 167, interiors rows 47/80, component row 847; E-G Price Schedule row 228; E-A; GS-O40/41 |
| GS-P03 | Ordinary interiors / components | Preserve exact seat/N26/TU7/stitch/R6X memberships and rates. Four R6X/AE4 leaves omit 595; the additional 595 is accepted for all four Grand Sport combinations on September 9. | E-B §7; GS-D09; supplemental price comparisons |
| GS-P04 | FEB / J57 / T0F / FEY | FEB 3,500; J57 with FEB +6,000; T0F +8,995; FEY 20,695 includes J57/T0F/WUB/CFZ at zero incremental charge. Absorbed purchases do not return on removal. | E-B §8; GS-O01–03/12 |
| GS-P05 | Heritage | Selected hash acquires Z15 995; center stripe adds 1,295; required/selected D84 adds 1,295. Hash source null prices becoming runtime zero is baseline behavior, not a universal null-price policy. | E-B §§4/6; GS-O15/38; GS-D03/04 |
| GS-P06 | Engine covers | BC4/BCP/BCS 695 normally, 595 with applicable B6P 1,895 or ZZ3 1,195. Do not charge supplied lighting twice. | E-B §5; GS-O13/14/37 |
| GS-P07 | D30 / belts | D30 1,495 once for a surviving nonrecommended combination. Hard belt prohibitions are not bypassed by payment. Target EL9 always supplies 3F9 at zero with no alternative. | E-B §§3/7; GS-D05; combination rows and sweeps |

The four GS-P03 leaves have component-sum versus frozen additions of
2,085 vs 1,490 (`3LT_R6X_AE4_HU0_38S`), 1,590 vs 995 (`..._HUU`),
2,780 vs 2,185 (`..._HXO_N26_38S`), and 2,285 vs 1,690 (`..._HZP_N26`).
These component sums are accepted Grand Sport target additions as of September 9;
the lower frozen amounts remain defect evidence.

## 5. Connected relationship records

The baseline relationship descriptions below retain observed behavior. Apply the
September 9 decisions in §8 for target changes, including conflict handling and
dependency cleanup; an old observation does not override an accepted decision.

| ID | Trigger / eligibility | Connected action and removal | Charge / evidence |
|---|---|---|---|
| GS-R01 | Trim/context change | Reset selections and interior; restore new context defaults. UQT becomes included display-only at 2LT/3LT. | E-B §2; GS-O31–36/44 |
| GS-R02 | Nonrecommended paint/interior | Allow with D30; prohibited stripe/paint instead refuses the attempted paint. All 145 paint conditions retained, including EL9. | D30 1,495; E-B §§3–4; paint sweep |
| GS-R03 | Convertible D84/D86, EDU, ZYC | Each excludes GBA; ZYC includes DRG. D84 versus D86 surfaces remain distinct from accent EFR/EDU. | 1,295 / 1,295 / 995 / 295; E-B §4; GS-O39 |
| GS-R04 | Convertible center stripe + listed paint | Accepted target auto-adds D84 with disclosure. DMX/DMV require it for ANY(G26,G4Z,GBK,GKZ,GPH); DMY for ANY(G26,G4Z,GBK,GTR); DMW for ANY(G26,G4Z,GBK); DMU has no listed set. Prohibitions: DMX/GTR, DMV/GKA, DMY/GKZ or GPH, DMW/G8G. | E-G Exterior 2 rows 70–74; baseline omits all 17 required-roof cases; GS-D04 |
| GS-R05 | BC4/BCP/BCS | Coupe replaces BC7 and supplies D3V; B6P adds SL9 and discounts cover. Removing B6P retains cover/D3V at 695. Convertible requires ZZ3; removing ZZ3 removes cover/SL9; no D3V. | GS-P06; E-B §5; GS-O13/14/37. Stale BCP/BCS prose is not an extra coupe gate. |
| GS-R06 | Heritage hash / center | Hash auto-adds Z15; center requires selected hash through package path. Removing hash removes dependent center and Z15 charge. Avoid a circular entry gate. | E-A; E-B §6; GS-O15; GS-D03 |
| GS-R07 | Heritage versus graphics / CF8 | Racing/Jake/stinger conflicts retain Grand Sport member sets. DPB after heritage and hash after DPB refuse. CF8 after hash/center removes center but retains hash/Z15; reverse center attempt refuses. | E-B §6; GS-O16–22; no universal symmetric action |
| GS-R08 | J57 / T0F | J57 requires ANY(FEB,FEY); T0F requires J57 AND ANY(FEB,FEY). FEB supplies J56/XFR; J57 replaces J56; T0F replaces T0E and adds CFZ. Target removes unsupported J57/T0F when package support is lost. | E-B §8; GS-O01; GS-D06 |
| GS-R09 | FEY | Replaces FEB, supplies J57/XFS/WUB/T0F/CFZ, absorbs J57/T0F/WUB/CFZ purchases. Switching back to FEB restores J56/XFR/T0E, not absorbed purchases. CFV becomes unavailable: removal is conflict cleanup, not absorption. | E-A; E-B §§8–10; GS-O02/03/07/12 |
| GS-R10 | J57 changes calipers | Target add: J6A → J6D, even explicit J6A. Target removal: J6D/J6L → J6A. Other paid calipers survive; restore standard available choice if section becomes empty. | E-A; baseline soft default insufficient; GS-O04–06; GS-D07 |
| GS-R11 | Factory wheels / J57 | Eleven factory choices; SWM starts at zero. ROY/ROZ/STZ require J57; losing it removes dependent wheels. Target restores standard available wheel. S47/SFE exclude carbon wheels; SPZ requires SPY, which conflicts with S47. | E-G Exterior 2 rows 54–57/100–110; GS-O09–11; GS-D07 |
| GS-R12 | WUB → NWI | WUB 1,995 permits NWI 395, replacing NGA. FEY includes WUB; removing it after absorption removes WUB/NWI and restores NGA. Inactive WUB exhaust-peer membership remains inactive. | E-B §8; GS-O12 |
| GS-R13 | 5ZV / SIG / T0E | 5ZV replaces T0E, removes dependent SIG; FEY attempt with 5ZV refuses. T0E restoration rule remains separate from duplicate identity disposition. | 2,075 / 425; E-B §9; GS-O08; GS-D10 |
| GS-R14 | EL9 | Interior-first entry acquires Z25/3F9; do not convert `requires_z25` metadata into an impossible entry gate. Target locks zero 3F9; ordinary interior change removes Z25. | GS-P02; E-A; GS-O40/41 |
| GS-R15 | Other interiors / belts | HAG requires blue, HVZ red; AUP/HAG→AUP/HVZ exchanges automatic belts. Permitted explicit alternatives can replace included belts in observed non-EL9 contexts. Target EL9 is the explicit exception. | E-B §7; GS-O43; 792 belt attempts |
| GS-R16 | PDA / VPW / VPO | PDA includes SNE/VPW; absorbs prior SNE, which does not return. Baseline permits VPW+DPB contrary to guide; VPO also lacks full exclusion set. | PDA 950; E-G Exterior 2 rows 47–48; GS-O23/24; GS-D12 |
| GS-R17 | PCQ / PEF / PDY | Include VWE/VWT, RIA/CAV, RYT/S08 respectively. Absorb prior VWE/CAV/RYT without resurrection on package removal. | 1,675 / 475 / 195; E-B §10; GS-O25–27 |
| GS-R18 | Coupe SBT | Adds second transparent roof plus SC7; blocks CC3; absorbs prior SC7. Does not replace the factory roof. | 2,525; E-G Exterior 2 row 41; GS-O28 |
| GS-R19 | Caps / covers / badges / liners / ground effects | Preserve each family separately: 5ZD→5ZB, RWH→WKR, RIK→SL8, SXB→SXR; CFL/CFZ/CFV exclusive. Independent accessories retain their own identity and charge. | E-B §10; GS-O29 |
| GS-R20 | R8C / BV4 / PIN | R8C supplies CFX, conflicts with BV4; wheel change SWN→ROU retains delivery. Preserve SOLD/BAC/approval disclosures separately from observed selection. | E-B §§9/11; GS-O11; GS-V04 |
| GS-R21 | DTC/SAI addition, DUW removal | Retire DUW active offering/relationships. DTC requires exact guide GTR and package/graphic/badge/roof exclusions; SAI excludes V8X. Do not mechanically rename DUW edges. | E-A; `accepted_additions` retains source disclosure and all related guide mentions; GS-D01/02 |
| GS-R22 | B4Z | Target included and only available with FEB or FEY in all six configurations; baseline is standard without either. | E-G Mechanical 2 row 44; E-A; GS-D08 |

September 9 settles D84 cause loss: remove dependency-added D84 and its charge
when no longer required, retain independently selected D84, and notify the customer.
The universal dependency-removal interaction includes an option to revert the
triggering selection. Verify both purchase-intent paths and reversal directions.

## 6. Selection and reconciliation policies

| ID | Event / condition | Required or proposed result | Authority / limit |
|---|---|---|---|
| GS-S01 | Body/trim change | Reset purchases and interior, then establish new defaults. | GS-O44; baseline observed |
| GS-S02 | Choice attempt | Intersect model/body/trim/lifecycle and prerequisites. General conflicts explain and offer replacement; VPW/VPO guide conflicts refuse. | September 9 GS-D12/16; test both interaction directions. |
| GS-S03 | Last package prerequisite lost | Remove unsupported J57/T0F and reconcile equipment/charges. Retain FEY-supported inclusions. Alert and offer revert of the trigger. | GS-D06/16; old retained-invalid state is historical. |
| GS-S04 | Wheel/caliper availability lost | Restore standard available choice; wheels/calipers must not remain empty. Apply exact J57 caliper swap policy. | E-A; GS-D07; other untested section fallback not inferred |
| GS-S05 | Absorbed purchase / incompatible option | Consumed purchase does not return on package removal. Keep CFV incompatibility distinct from FEY absorption. | E-A; GS-O03/07/12/23/25–28 |
| GS-S06 | Multiple inclusion causes | Retain one resolved item/charge while supported; preserve cause distinctions. Shared references do not imply extra purchase quantities. | E-B §§5/7–8; complete multi-cause reversal coverage remains unverified |
| GS-S07 | Interior / belts | Preserve exact eligible leaves, clear incompatible interior on context change; missing interior blocks completion. EL9's included 3F9 is locked at zero; HAG/HVZ restrictions remain hard. | E-A; GS-O40–44; detailed zero/one/many reconciliation still needs Grand Sport target verification |
| GS-S08 | Defaults / restoration | Keep four authored rules and section defaults separate. New wheel/caliper restoration is a target correction, not proof the old defaults worked. | E-W; GS-D07 |
| GS-S09 | Heritage acquisition / removal | Hash adds Z15; center needs hash; last supporting hash removal removes center and Z15 charge. Hash-first with the explicit $995 disclosure in GS-D03 is accepted. | E-A; GS-D03 |
| GS-S10 | Totals / recap / order | Corrected resolved equipment and single charge ownership must reach all consumers. Old submit guards prove rejection of invalid state, not correctness of retained charges. | E-B §§8/11; target output validation pending |

## 7. Presentation, physical content and operational boundaries

| ID | Subject / condition | Content or presentation consequence | Evidence / state |
|---|---|---|---|
| GS-V01 | Any center stripe with D84 | Required disclosure: “When (D84) Carbon Flash painted nacelles and roof is ordered (required or selected) roof will not include the stripe.” Conditional addition also alerts the customer. | E-A; physical roof content separate from stripe eligibility |
| GS-V02 | Z15 / EL9 | Hash-first selection and the exact $995 Z15 disclosure in GS-D03 are accepted. EL9-triggered Z25 charge must remain visible; accepted content 1,995 plus separate seat charge. | E-A; GS-D03/05 |
| GS-V03 | Z25 / accents / cover / second roof | Retain Launch Edition quilting, mats, embossed headrests and plaque; EFR/EDU surface changes with CFV/CFZ; WKR version depends on 5ZV/T0F; SBT supplies an additional roof. No extra purchasable identities inferred. | E-G Exterior 2 rows 4/16–17/31/41; E-B §§7/9–10 |
| GS-V04 | R8C/BV4/PIN/VK3/D30/R6X and services | Retain source restrictions as evidence. Customer configuration scope omits dealer/service/emissions options and does not implement full dealer-order validation. | September 9 GS-D15; historical omissions remain documented. |
| GS-V05 | Standard versus installed equipment | Equipment within selected-options sections reflects configured replacements; informational standard-equipment lists stay model/body/trim based. Preserve actual brake/tire/suspension and B4Z consequences. | September 9 GS-D15; implementation/consumer verification pending. |
| GS-V06 | Sections / navigation / assets | Preserve scoped steps, required/single/multiple/display-only modes, contextual copy and summary routing. Shared `standard_equipment` section metadata is retained even though it is not an interactive runtime-step row. Assets are references, not validated visualizer bindings. | Complete scoped rows; no visual QA or asset rendering in this task |

## 8. Decision overlay: source, baseline and target remain separate

| ID | Source / baseline difference | Target or pending decision | State |
|---|---|---|---|
| GS-D01 | DTC missing; DUW retained in baseline | Retire DUW active offering/relationships; add DTC across six configurations at 1,295 with exact GTR and guide package/graphic/badge/roof exclusions. Preserve raw DUW mentions as history. | Accepted September 8; price accepted September 9, Price Schedule!E257. |
| GS-D02 | SAI missing | Add across six configurations at 295 with guide V8X conflict; V8X remains inactive. | Accepted September 8; price accepted September 9, Price Schedule!E128. |
| GS-D03 | Heritage acquisition presentation | Use hash-first selection with disclosure: “Selecting this hash mark adds the Grand Sport Heritage Package (Z15) for $995.” Hash→Z15 and center dependency/removal remain accepted. This supersedes the earlier priced Z15 entry-card proposal. | Accepted by explicit owner confirmation after PR #20; hash-first flow and exact disclosure wording finalized. |
| GS-D04 | Conditional D84 absent; later cause loss unspecified | Auto-add D84 for the exact accepted convertible stripe/paint conditions with disclosure. When no longer required, remove D84 and its 1,295 charge only if it was dependency-added; retain independently chosen D84. Notify through toast/alert; universal dependency cleanup offers revert of the triggering selection. | Accepted September 8 and September 9 answers 3/15; target unexecuted. |
| GS-D05 | EL9 bundles seat in 1,995 and permits other belts | Z25 content 1,995 once; AH2 zero, AE4 another 595; visible EL9-triggered charge. Lock included 3F9 at zero. Historical orange-belt D30 gap is not a target pairing to enable. | Accepted September 8; target arithmetic, not runtime proof. |
| GS-D06 | FEB removal leaves charged J57/T0F invalid | Remove unsupported dependencies, reconcile equipment/charges; retain FEY-supported inclusions. Universal dependency-loss cleanup alerts customer and offers revert of triggering selection. | Accepted September 8; universal interaction accepted September 9 answer 3. |
| GS-D07 | Caliper swaps and wheel loss leave empty/incorrect defaults | Add J57: J6A→J6D, including explicit J6A. Remove J57: J6D/J6L→J6A; retain other paid calipers. Restore standard available wheels/calipers after loss. | Accepted September 8; target reversal checks pending. |
| GS-D08 | B4Z standard without package support | Included and only available with FEB or FEY in all six configurations; reconcile availability and acquisition. | Accepted September 8; baseline conflicts retained. |
| GS-D09 | Four R6X/AE4 component sums exceed frozen totals by 595 | Add missing 595 once in all four affected combinations. Required additions: HU0/38S 2,085; HUU 1,590; HXO/N26/38S 2,780; HZP/N26 2,285. | Accepted September 9, answer 10; original price observations unchanged. |
| GS-D10 | Two T0E identities | Retain active opt_t0e_001 as the single target T0E option; retire dormant opt_t0e_002 and reconcile affected references. Keep both raw records as historical evidence. | Accepted September 9, answer 11; target identity resolved. |
| GS-D11 | SLN/R88 unavailable; CF8 unavailable at production start | Show SLN/R88/CF8/RZ9/V8X cards in applicable model/body/trim contexts but disable selection with reason “Unavailable at this time”. Apply this policy to every option unavailable under a guide lifecycle notice, including already-inactive options; release is required before selection becomes available. Preserve compatibility rules and historical evidence. | Accepted September 9, answer 16 and PR #20 owner clarification; visibility does not imply availability. |
| GS-D12 | VPW/VPO incomplete graphic exclusions | Apply full guide exclusions to both graphics and refuse conflicting selections. This explicit refusal policy overrides the general explain-and-offer-replacement interaction for these conflicts. | Accepted September 9, answer 12; both directions require verification. |
| GS-D13 | DUE Santorini Blue workbook name versus Royal Blue guide name | Use Royal Blue for DUE target customer-facing naming; retire old DUE naming throughout target references. Preserve original workbook/observation labels as historical evidence; do not rename unrelated legitimately Santorini Blue items. | Accepted September 9, answer 13. |
| GS-D14 | Option-price basis and addition rates previously unresolved | Use raw Price Schedule column E for OPTIONS. DTC 1,295 at E257; SAI 295 at E128. Preserve base/destination interpretation and frozen numeric evidence. All prices are USD, confirmed by the owner after PR #20; numeric amounts are unchanged. | Accepted September 9, answer 17; code/value cells verified; no wholesale repricing. |
| GS-D15 | Dealer-order scope and equipment display meaning incomplete | Customer configuration form: omitted dealer/service/emissions options stay outside customer selection. Selected-options equipment reflects configured replacements; informational standard equipment uses model/body/trim. Physical content/assets still need implementation verification. | Accepted September 9, answers 18–19. |
| GS-D16 | General conflict and dependency-loss interaction; stale prose | General conflicts explain and offer replacement before changing selections. Remove dependency-invalid selections with an alert and option to revert the trigger; keep independent purchase intent distinct. Explicit VPW/VPO refusal overrides the general policy. Retire stale target cover prerequisites in favor of accepted current behavior. Hash-first disclosure makes the 995 charge visible; no universal null-as-zero rule inferred. | Accepted September 9, answers 3/6/9, plus confirmed hash-first flow; untested directions remain verification work. |

## 9. Worked sequences and expected outcomes

These are review checks, not newly executed tests. `B` is configuration base;
amounts are partial-build totals. Accepted corrections have separate target
expectations; unresolved decisions retain baseline expectations only.

| ID | Context and actions | Expected outcome / authority | Evidence |
|---|---|---|---|
| GS-T01 | Each configuration → initial | Bases/roof/seat/defaults in §3; no FEB/FEY purchase; required paint/interior remain unset. | GS-O31–36 |
| GS-T02 | Coupe 3LT FEY/EL9 → convertible 1LT | Reset purchases/interior; total 95,495, default CM9; no retained FEY/EL9. | GS-O44 |
| GS-T03 | Coupe 2LT BC4 → B6P → remove B6P → remove BC4 | 96,290 → 98,085 → 96,290 → 95,595; D3V retained with cover, SL9 removed with package, BC7 restored at end. | GS-O13 |
| GS-T04 | Convertible 2LT BC4 attempt → ZZ3 → BC4 → remove ZZ3 | First refused; 103,790 → 104,385 → 102,595; no D3V or dependent cover remains. | GS-O37 |
| GS-T05 | Coupe 2LT 97A → DMU → remove 97A | 96,590 → 97,885 → 95,595; center and Z15 removed with hash. | GS-O15 |
| GS-T06 | Convertible 2LT G26/97A → DMX | Baseline 105,880 without D84; target D84 addition brings 107,175 and disclosure. Target auto-add not executed. | GS-O38; 17 focused roof gaps; GS-D04 |
| GS-T07 | Heritage→DPB; DPB→hash; heritage/center→CF8; CF8→center | Historical baseline: first two refuse; CF8 removes center and keeps hash/Z15; reverse center refuses. Accepted target: CF8 remains visible but disabled with “Unavailable at this time”, so its selection is refused before these historical replacement paths can run (GS-D11). | GS-O16/17/19/20 |
| GS-T08 | G8G/20A/DMX → attempt GTR; D84/ZYC → attempt GBA | Preserve selected valid paint and purchases; prohibited paint refused. | GS-O18/39 |
| GS-T09 | Coupe 3LT AH2/EL9 versus AE4/EL9 | Baseline both 102,240. Target 102,240 / 102,835; Z25 charged once and 3F9 locked zero. No orange/alternative belt path in target. | GS-O40/41; GS-D05 |
| GS-T10 | Each four R6X/AE4 discrepancy leaves | Retain exact component sums and observed additions in §4; +595 once is now the accepted correction for each affected leaf. | GS-O42 plus complete price sweep; GS-D09 |
| GS-T11 | HAG → attempt red; AUP/HAG → AUP/HVZ | Red refused under HAG; automatic blue changes to red under HVZ; D30 does not bypass prohibition. | GS-O43; belt sweep |
| GS-T12 | Coupe 2LT FEB → J57 → T0F → FEY → FEB | 99,095 → 105,095 → 114,090 → 116,290 → 99,095; absorbed purchases do not return, J56/XFR/T0E restored. | GS-O03 |
| GS-T13 | Completed configuration FEB/J57/T0F → remove FEB | Baseline retains invalid components/charges and blocks button/modal/submit; coupe 2LT 110,590. Target removes unsupported J57/T0F/dependents and reconciles charges/defaults. | GS-O01; six focused checks; GS-D06/07 |
| GS-T14 | J6A (including explicit) → J57 → remove J57; paid J6F with J57 | Target J6A→J6D→J6A; paid J6F retained. J6L falls back to J6A after J57 loss. No empty caliper. | GS-O04–06 baseline; GS-D07 target not executed |
| GS-T15 | FEB/J57 → ROY → remove J57 | Baseline coupe 2LT 116,090 before loss, then missing wheel. Target removes invalid ROY and restores standard available wheel. | GS-O09; GS-D07 |
| GS-T16 | S47 → ROZ attempt; SWN/R8C → ROU | Chrome/carbon conflict refuses; factory wheel replacement preserves delivery. | GS-O10/11 |
| GS-T17 | WUB → NWI → FEY → remove FEY | WUB/NWI supported during package; absorbed WUB and dependent NWI removed at end, NGA restored. | GS-O12 |
| GS-T18 | CFV → FEY → remove FEY; SIG → 5ZV → FEY attempt | CFV removed as incompatible and does not return; 5ZV removes SIG and blocks FEY. | GS-O07/08 |
| GS-T19 | SNE→PDA / VWE→PCQ / CAV→PEF / RYT→PDY / SC7→SBT; remove package | Prior absorbed item does not reappear as a paid purchase. SBT retains factory roof and blocks CC3 while selected. | GS-O23/25–28 |
| GS-T20 | VPW → DPB | Baseline permits both despite guide exclusion; target applies full guide exclusions and refuses the conflict. | GS-O24; GS-D12 |
| GS-T21 | Peer accessory changes; attempt SLN/R88/CF8/RZ9/V8X | Preserve peer replacement examples; target shows SLN/R88/CF8/RZ9/V8X disabled with “Unavailable at this time”. | GS-O29/30; GS-D11 |
| GS-T22 | Add DTC / attempt GTR; add SAI with V8X; inspect active DUW/T0E | Accepted additions use guide conflicts and all-six scope, DTC 1,295 / SAI 295; DUW retired. Retain active T0E, retire dormant duplicate. | GS-D01/02/10; new behavior unexecuted |
| GS-T23 | Any of six configurations without / with FEB or FEY | Target B4Z absent without support, included with either; verify availability, selection and installed-equipment outputs together. | Six source status differences; GS-D08; target unexecuted |

## 10. Coverage and handoff boundary

This populated handoff retains every Grand Sport baseline offering, availability
row, interior leaf/component, direct/grouped/exclusive relationship, conditional
price, combination row and recorded sequence, plus scoped presentation and source
reconciliation. The readable tables distinguish accepted changes from unresolved
facts. No original observations have been refreshed to make a target appear to
have been the old behavior.

Validation for this handoff: verified workbook/guide hashes and local browser
bytes against the frozen archive; compared the complete local workbook extraction
with freshly read frozen rows; checked exact extracted content, model scoping,
identity references, guide code/disclosure anchors, offering dispositions,
interior links, duplicate RPOs and observation preservation; reviewed narrative
against E-B/E-A, local links and the diff. No runtime probes were rerun and no
corrected target was executed.

The earlier analysis compared 1,374 status pairs (1,368 matches, six B4Z conflicts)
and 233 repeated coded equipment-sheet occurrences. The full 1,446-row baseline
includes additional paint/legacy/dormant evidence; those counts are not interchangeable.
Supplemental sweeps retain their original scope and comparisons, including EL9
component-only price expectations and the historical orange-belt gap. They do not
prove complete interaction/direction coverage, full option-price reconciliation,
visual QA, installed-equipment accuracy or dealer-order acceptance.

Implement and validate the accepted GS-D decisions before a priced release or
implementation acceptance. The owner confirmed the hash-first flow, exact GS-D03 disclosure wording and USD for all Grand Sport prices after PR #20. These close the remaining model-review decision details; UI implementation and verification remain separate work. Continue separately with **Grand Sport X,
Z06, ZR1, ZR1X**, using the same handoff categories, before consolidating one
comprehensive schema. This task stops at the Grand Sport structured handoff:
no schema, evaluator, canonical workbook, reference repository, production output
or deployment changes.
