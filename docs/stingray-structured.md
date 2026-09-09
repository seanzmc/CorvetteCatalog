# Stingray structured model handoff

September 9, 2026. Model: **Stingray, 2027**. Status: **structured review input**.

This document organizes the [behavior analysis](stingray-behavior.md) into explicit
facts, conditions, actions, charges, evidence and decisions. Its companion
[record file](stingray-structured-records.json) preserves the complete model-scoped
source lists and all 48 recorded behavior sequences. Together they are the
Stingray handoff for comparing model requirements before designing the comprehensive
catalog. They are not another database schema, an executable ruleset, or a new
canonical dataset. The [logical schema proposal](stingray-schema-plan.md) remains
a design reference; its proposed tables are not imposed on this intermediate format.

## 1. Record conventions and evidence

Use these same categories for subsequent models: configurations, offerings,
applicability, interiors/parts, relationships, prices, selection behavior,
presentation/content, evidence/decisions and expected sequences. Each model owns
its records. Matching an RPO in another model does not establish shared identity.

| Convention | Meaning |
|---|---|
| `ST-C`, `ST-R`, `ST-P`, `ST-S`, `ST-V`, `ST-D`, `ST-T` | Local configuration, relationship, price, selection, presentation, decision and target-check IDs in this document. They are review references, not database keys. |
| `ST-O01`–`ST-O48` | Original observed sequences in the record file, including every captured state. State layouts retain original `automatic` versus `auto` fields; these are evidence, not a normalized runtime contract. |
| Option identity | Record file uses `stingray:<legacy option_id>` for existing offerings. RPO is a readable reference only. New DTC/SAI use provisional `stingray:proposed:<RPO>` identities, not aliases of existing items. |
| Baseline | Frozen workbook values and old-form behavior. Preserve even when incorrect. A source status match does not prove all rules/prices correct. |
| Target | Baseline interpretation plus an explicitly identified accepted correction. A proposed behavior or unresolved decision must not be silently treated as approved. |
| Evidence class / review state | Keep added, removed, conflicting, ambiguous and component-accounted facts distinct from accepted, proposed or unresolved decisions. |
| Scope | `All` below means exactly the six ST-C configurations. Otherwise intersect the stated body/trim with option and interior applicability. Unknown scope is unresolved, not all. |
| Conditions | `AND` requires every condition; `ANY(...)` requires at least one. Separate eligibility, auto-add, price override, conflict action and removal action. |
| Prices | Numeric frozen-workbook basis; currency and guide price-column interpretation unresolved. Zero is known zero; null is unknown. No second destination charge. |
| Completeness | Full baseline lists are preserved in the record file. This document resolves known connected semantics by family; unexecuted interaction directions remain unverified. Neither artifact is a fully resolved target dataset. |

| Evidence ID | Immutable identity / locator | Use |
|---|---|---|
| E-W | [Frozen workbook](../baselines/2026-09-06/README.md), SHA-256 `3127e663b1531e366ce86b989b6190914108d40dfd15a33a258307a05d608e3c` | Record-file `baseline_rows.<sheet>` entries preserve original headers, nulls, ordering and `_row` Excel row numbers. |
| E-G | [Manufacturer source](../sources/README.md), `2027 Chevrolet Car Corvette Export (6).xlsx`, SHA-256 `d3ca7d3a09c9fb89210b4ce584493b3ad8fb65ca35087c49d816d1cbf1a333d1` | Stingray `Interior 1`, `Exterior 1`, `Mechanical 1`, associated equipment sheets, model-qualified color tables. |
| E-O | Frozen browser commit `4fe92a4f078370c478f18484cad31bdafe58ad43` | DOM-stub selection functions; 48 sequences / 237 states retained. No live requests or visual/dealer-order acceptance. |
| E-B | [Behavior analysis](stingray-behavior.md), §§2–12 | Connected explanations, broader sweeps, source interpretation and limits. References such as E-B §7 below refer here. |
| E-A | [Accepted owner corrections](stingray-behavior.md#owner-decisions-accepted-for-the-schema-plan--september-7-2026) | September 7 DTC/DUW and SAI decisions; other open questions remain open. |
| E-S | [Schema proposal](stingray-schema-plan.md), §§2–9 | Proposed ownership and required-interior policy. Design reasoning is separate from executed evidence. |

## 2. Complete record sets and how to use them

The companion JSON contains the following exact lists. Read it with this document:
`baseline_rows` is evidence; `offering_dispositions`, `accepted_additions` and
ST-D decisions describe departures. **Do not import `baseline_rows` as the accepted
target**, and do not flatten the source rule sheets into one universal behavior.

| Category | Record-file location | Scope / disposition |
|---|---|---|
| Configurations | `baseline_rows.variant_master`, `model_variants` | Six Stingray configurations and six membership rows. |
| Offerings | `baseline_rows.stingray_options`, `offering_dispositions` | All 242 source offerings, each classified and source-linked: 205 coded guide matches, 26 uncoded equipment, 10 paints, legacy DUW. |
| Additions / omissions | `accepted_additions`, `guide_only_dispositions` | DTC and SAI additions with full guide disclosures; component-accounted and service/emissions omissions remain distinct. |
| Applicability / overrides | `baseline_rows.stingray_ovs`, `stingray_variant_overrides` | All 1,452 option/configuration statuses, including paint and DUW, plus four UQT display overrides. Effective selection also depends on lifecycle and relationships. |
| Interior choices | `baseline_rows.lt_interiors`, `model_interior_scope`, `interior_source_links` | Exactly 130 complete leaves; source guide cells and workbook rows; full navigation and eligibility metadata. No EL9. |
| Interior parts / rates | `baseline_rows.interior_components`, `PriceRef` | All 197 memberships and 21 source rates. These retain duplicated legacy charge evidence; ST-P02 defines target ownership. |
| Direct relationships | `baseline_rows.rule_mapping` | All 178 source rows, including original text and raw scopes. See ST-R/ST-S for effective behavior and remaining questions. |
| Grouped relationships | `baseline_rows.rule_groups`, `rule_group_members` | All 27 groups / 155 members. Member sets stay separate even where similar. |
| Exclusive groups | `baseline_rows.exclusive_groups`, `exclusive_group_members` | All 10 groups / 36 members; section-level selection modes are additional evidence. |
| Conditional prices | `baseline_rows.price_rules` | All 52 rows. No inferred positive package-minimum/delta schedule. |
| Combination additions | `baseline_rows.color_overrides` | All 269 exact interior/selected-option pairs: 137 paint and 132 belt conditions, all adding D30. |
| Defaults | `baseline_rows.default_selection_rules` | Four explicit restoration/default rows: FE1, NGA, 719, coupe BC7. Initial defaults also come from sections and standard status. |
| Presentation | `baseline_rows.section_master`, `section_presentation`, `runtime_steps`, `context_section_master`, `context_choice_copy`, `order_summary_sections`, `step_order_summary_map`, `asset_map` | Relevant sections, model-scoped rows and applicable wildcard copy/assets retained. Wildcard evidence is not approval of shared ownership. |
| Routing / intake evidence | `baseline_rows.model_master`, `model_registry_promotion`, `model_workbook_sources`, `rule_phrase_map`, `runtime_rule_exceptions` | Model metadata, 11 source routes, six phrase rows, empty exception list. Historical routes are not future authoring tables. |
| Observations | `observed_sequences` | 48 original sequences, 237 captured states; names, selected/automatic equipment, line items, totals and missing requirements retained as recorded. Sweeps remain documented in E-B, not relabeled as new executions. |
| Duplicate RPO audit | `duplicate_rpos_within_model` | No duplicate nonblank RPO among the 242 baseline option rows, including inactive offerings. Blank equipment codes are not one product. Repeated guide occurrences are references, not duplicate options. |

**Lookup example:** find `opt_bcp_001` in `stingray_options`, its six `stingray_ovs`
rows and related direct/price rows; then ST-R04 and ST-T04 explain the body's
selection/removal behavior. The offering disposition supplies its guide anchor.
For an interior, use its exact leaf ID across `lt_interiors`, `model_interior_scope`,
`interior_components`, `color_overrides` and `interior_source_links`. Raw blank
body scope on BCP→ZZ3 is not proof of a coupe prerequisite.

## 3. Configurations and offering scope

| ID | Legacy configuration | Body | Trim | Base | Starting roof | Starting seat |
|---|---|---|---|---:|---|---|
| ST-C01 | `1lt_c07` | Coupe | 1LT | 73,495 | CF7 | AQ9 |
| ST-C02 | `2lt_c07` | Coupe | 2LT | 80,595 | CF7 | AQ9 |
| ST-C03 | `3lt_c07` | Coupe | 3LT | 85,245 | CF7 | AH2 |
| ST-C04 | `1lt_c67` | Convertible | 1LT | 80,495 | CM9 | AQ9 |
| ST-C05 | `2lt_c67` | Convertible | 2LT | 87,595 | CM9 | AQ9 |
| ST-C06 | `3lt_c67` | Convertible | 3LT | 92,245 | CM9 | AH2 |

Evidence: E-W `variant_master!A2:H7`, `model_variants!A14:E19`; ST-O01–06.
Paint and interior begin unset. Other observed initial selections include EYT,
J6A, 719, QEB, EFR, FE1 and NGA; coupe includes BC7. See exact per-body states.

| Offering family | Scope and role | Evidence / decision |
|---|---|---|
| UQT | Purchasable 1LT, 1,495; supplied/display-only 2LT/3LT with no purchase line. Stored base price remains 1,495. | E-B §2; four source overrides; ST-P03. |
| BAZ / FA5 / E60 | 2LT/3LT only, both bodies; 695 / 1,795 / 2,995. | E-G Interior 1 rows 85/88, Exterior 1 rows 17–19; E-B §2. |
| Roofs | Coupe CF7/CC3/C2Z; CF8 only 2LT/3LT but inactive. Convertible CM9/D84/D86. | E-B §§2/4; ST-D05. |
| Engine appearance | B6P coupe; ZZ3 convertible. BC4/BCP/BCS body-qualified requirements/content/prices. | E-B §5; ST-R04. |
| Paint | G8G/GBA/GKA/GEC/GKZ = 0; GTR/G4Z = 500; GBK/GPH/G26 = 995. | E-W `stingray_options!A116:K125`; E-G color tables; ST-D12 price basis. |
| Factory wheels | Exactly one QEB/QE6/Q99/Q9A/Q9I/Q9O in required factory-wheel section. | E-G Exterior 1 rows 99–104; E-B §9. |
| Accessory wheels | Optional separate second set 5DO/5DG; coexist with factory wheels. | E-G Exterior 1 rows 66–67; ST-R12. |
| Trim/body equipment | AP9 at 2LT/3LT versus W2D purchase at 1LT; SLK/SLN/VUP coupe; 5JR 3LT. | E-B §§10–11; lifecycle issue ST-D05. |
| Historical/added options | Retire DUW; add DTC and SAI across all six configurations. Do not map DTC as a DUW alias. | ST-D01/02; additions retain unknown prices. |
| Duplicate control | Flag duplicate option RPOs within each model for resolution; preserve raw evidence separately. | Owner's September 8 review instruction; baseline audit is empty. |

## 4. Interior records and price ownership

Exact eligibility is the 130 leaf IDs in the record file: 4 at 1LT, 40 at 2LT,
86 at 3LT (71 ordinary and 15 R6X). The guide's 78 seat/trim/code combinations
expand through disclosed extras. **Do not generate a free cross-product.**

| Record | Condition / members | Target meaning | Evidence |
|---|---|---|---|
| ST-R01 | Selected trim + seat + exact interior leaf | One eligible interior; changing seat clears an incompatible leaf. EL9/Z25 is outside Stingray. | E-B §§3/7; ST-S02. |
| ST-R02 | Performance Textile at 1LT; specified suede interiors | N26 carried by the leaf; no separate N26 purchase card. | Color and Trim 1 A27 footnotes 5/7; Color and Trim 2 A22 footnote 2; Interior 1 row 79. |
| ST-R03 | 36S/37S/38S leaves; HU0/HXO require 38S; AH2-specific TU7 leaves | Optional extras distinguish leaves; mandatory extras have no omission path. HU7/HUA/HXO with AH2 require TU7; AE4 does not inherit TU7. | Interior 1 rows 69, 82–84; color-table footnotes; 197 exact memberships. |
| ST-P01 | Selected seat | Seat option owns amount: AQ9 standard 0; AH2 2LT 1,695 / 3LT 0; AE4 1LT 1,095 / 2LT 2,095 / 3LT 595; AUP 3LT 350 for HAG/HVZ only. | E-B §§2/7; unavailable seat contexts remain unavailable. |
| ST-P02 | R6X leaf + exact extras | Seat + R6X 995 + N26 695 + each selected stitch 495 + TU7 595, once each. Seat/R6X option charges; other extras component charges. Stored interior total and combined source rates are comparison evidence, not additional editable prices. | E-B §7; E-S §2; ST-D03. |
| ST-P03 | Supplied/display-only versus purchased | Supplied equipment does not create a purchase simply because its stored amount is positive. UQT 2LT/3LT is the concrete case. | E-B §2; ST-O07. |
| ST-P04 | Multiple valid causes add D30 or DRG/D3V | Resolve one target/charge. Remove only when no applicable cause or valid selection remains; distinguish suppression and absorbed intent. | E-B §§5/7/10; ST-S04/05. |
| ST-P05 | Contextual price | Use exact applicable option/body/trim/interior rule; retain raw ordering for review. Blank is not zero. Do not borrow rates from another year/model. | 52 price rows, 21 PriceRef rows; E-S §4; ST-D12. |

| Known correction leaf | Frozen subtotal | Required subtotal | Difference / authority |
|---|---:|---:|---|
| `3LT_R6X_AE4_HU0_38S` | 1,490 | 2,085 | +595 seat; ST-D03 |
| `3LT_R6X_AE4_HUU` | 995 | 1,590 | +595 seat; ST-D03 |
| `3LT_R6X_AE4_HXO_N26_38S` | 2,185 | 2,780 | +595 seat; ST-D03 |
| `3LT_R6X_AE4_HZP_N26` | 1,690 | 2,285 | +595 seat; ST-D03 |

These are interior/seat subtotals, not complete vehicle totals. The other 126
leaves matched the additive coupe check. No corrected evaluator was executed.

## 5. Relationships: conditions, consequences and removal

Each row below describes a connected business relationship. Its complete endpoint
sets remain in the record file where too large to repeat. E-B section references
supply guide and workbook locations. Scope is effective availability plus any
explicit condition below; source text and old raw scope are not silently rewritten.

| ID | Trigger / prerequisites | Addition, exclusion or replacement | Price and loss behavior | Evidence / target state |
|---|---|---|---|---|
| ST-R04 | Coupe colored cover BC4/BCP/BCS; convertible requires ZZ3 | Cover replaces BC7. Coupe adds D3V; B6P adds D3V/SL9. Convertible ZZ3 adds BC7/SL9, paid cover suppresses BC7; no D3V. | Cover 695 normally, 595 with applicable B6P/ZZ3. Coupe B6P removal retains cover/D3V, removes SL9. Convertible ZZ3 removal removes cover/SL9. | E-B §5; ST-O10/11 exercise BCP; BC4/BCS direction coverage not claimed. |
| ST-R05 | Convertible D84/D86; EFY/EDU with permitted paint | GBA incompatible; roof/accent peers replaced as applicable. | D84/D86 1,295; EFY/EDU 995. Tested D84/EFY↔GBA attempts refused, not automatic deletions. | E-B §4; ST-O08/09. Full D86/EDU directions unverified. |
| ST-R06 | Exact interior + selected paint/belt in 269-row combination list | Auto-add D30; recommended combinations differ from hard prohibitions. | 1,495 once even with two causes; remove after final cause disappears. | E-B §§3/7; ST-O17/45/47. |
| ST-R07 | Eligible HZN/HUF/EJH/EPX interiors | Include 3N9. | Included belt zero; permitted paid alternative can replace it. | E-B §7; 22 interior inclusion / belt-zero pairs. |
| ST-R08 | Eligible H8T/HAG; HNK/HVZ; HUW/HUX | Include 3A9; 3F9; 379 respectively. HAG permits only 3A9; HVZ only 3F9. | H8T can yield to a paid alternative plus D30 where required; hard HAG/HVZ prohibitions cannot be bought out. | E-B §7; ST-O43/44; full belt pair list retained. |
| ST-R09 | Z51 | Includes J55/FE3/G0K/G96/M1N/QTU/T0A/V08; replaces FE1/FE2; installed-equipment substitutions are separately described. | Package 5,395; included members zero. Removal drops unsupported inclusions; FE1 returns, old FE2 purchase does not. | E-B §8; ST-O18/19; output boundary ST-V01. |
| ST-R10 | FE4 requires Z51 | Replaces included FE3, adds B4Z. | Additional 1,895; FE4 removal with Z51 restores FE3. Z51 loss removes FE4/B4Z. Paid caliper retained. | E-B §8; ST-O18/19. Do not import Grand Sport caliper policies. |
| ST-R11 | NWI requires WUB; E60 permitted only 2LT/3LT | NWI replaces NGA tips; WUB and NGA may coexist. E60 includes TR7. | WUB 1,995; NWI 395; removing WUB drops NWI/restores NGA. E60 2,995; TR7 zero and follows E60 removal. | E-B §8; ST-O22/39. |
| ST-R12 | 5DO/5DG accessory wheels | Additional to factory selection; exclude R8C/S47/SFE/SPY/SPZ. Included hardware is content, not those excluded option purchases. | 4,395 each in observed/source baseline; removing accessory set retains factory wheel. | E-B §9; ST-O20; exact source amounts in option rows. |
| ST-R13 | SPZ requires SPY; SPY conflicts with S47/SFE | Locks are not auto-included with nuts. | SPY 320 + SPZ 105; loss of SPY removes SPZ. | E-B §9; ST-O21. |
| ST-R14 | PCX | Includes 5DG/SFZ/SHT/SNG; full model-local exclusion group retained. Paid 5DO/SHW suppress included peers. | PCX stays 4,595 without credit; paid peers add their full prices. Removal drops remaining inclusions and retains paid alternatives. | E-B §9; ST-O26. |
| ST-R15 | PDV | Includes SB7/VWD; paid cap peer overrides VWD, including already-selected 5ZD then RXH. | PDV 750 retained; RXH remains after package removal. | E-B §9; ST-O27. |
| ST-R16 | 5ZU requires ANY(G8G,GBA,GKZ); incompatible with 5ZW/5ZZ/TVS | With Z51, baseline auto-adds ZF1, suppressing T0A. Without Z51, no ZF1. | Wing 1,395; removing Z51 retains wing, removes ZF1. Incompatible later paint retains charged invalid wing in baseline. | E-B §6; ST-O12–14/48; unresolved ST-D04/07. |
| ST-R17 | TVS + Z51, either tested order | T0A suppressed; frozen output omits guide-required ZF1. | TVS resolves to 0; coupe 2LT total 85,990. | E-B §6; ST-O15/16; ST-D04. |
| ST-R18 | Stripe + forbidden paint | DPB/DUE/DTC vs GTR; DPC/DT0/DZU vs GBK; DPG/DSY vs G26; DPL/DSZ/DUK/DZX vs GKZ/GPH. DPT/DTH/DUB/DZV have no listed paint restriction. | Stripe peer changes replace price; tested DPB↔GTR refused. DTC is accepted addition, not executed legacy behavior. | E-G Exterior 1 rows 81–96; E-B §10; ST-D01. |
| ST-R19 | Graphics/package/badge group conflicts | Preserve each of 25 exclusion member sets. DPB→PDV removes DPB; PDV→PCX replaces PDV; PCX→DPB refused. EYK→SFZ removes EYK; SHT→SB7 refused. | No universal symmetric conflict action. Hash section remains separate from stripe section. | E-B §10; ST-O28–31; ST-D06. |
| ST-R20 | 5V7 requires permitted high wing | Baseline ANY(5ZU,5ZZ); conflicts with Z51/TVS/STI and specified ground effects. Guide also mentions inactive 5ZW. | 650; alone refused; 5ZU→5V7 succeeds; removing 5V7 retains wing. | E-B §10; ST-O32/48; ST-D08. |
| ST-R21 | PCU / PEF / PDY | PCU includes STI/VQK/VWE; PEF includes CAV/RIA; PDY includes RYT/S08. | 1,575 / 475 / 195; prior standalone STI/CAV/RYT absorbed at zero, not restored when package removed. | E-B §10; ST-O23–25. |
| ST-R22 | Coupe SBT | Adds second transparent roof and SC7; conflicts with CC3; does not replace factory roof. | 2,525; absorbs SC7; removing SBT drops SC7 and permits CC3 purchase at 995. | E-B §10; ST-O35. |
| ST-R23 | Cover compatibility | WKQ excludes high wings; RWJ excludes Z51; RNX baseline excludes Z51 despite guide's ZF1 conditional path. | Keep indoor RWH/SL1/WKR/WKQ separate from outdoor RNX/RWJ exclusive group. | E-B §10; ST-O33/34; ST-D09. |
| ST-R24 | SXB/SXR/SXT; RIK/RIN/SL8 | Replace within liner-color and script groups respectively; independent accessories unaffected. | Removing RWU removes only its 175; other purchases remain. | E-B §10; ST-O36/37. |
| ST-R25 | 5JR at 3LT; ZYC; RYQ/RZ9 vs EFY | 5JR/ZYC both supply DRG; preserve EFY conflicts and lifecycle. | 5JR 1,395 + ZYC 295; DRG once; aero deletion removes T0A without removing unrelated DRG/ZYC. | E-B §10; ST-O46; physical surfaces ST-V02. |
| ST-R26 | R8C / BV4 | R8C includes CFX; BV4/R8C excluded in baseline; accessory-wheel conflicts also apply. | R8C 1,695; BV4 395; removing R8C removes CFX. | E-B §11; ST-O38; operational limits ST-V04/ST-D08. |
| ST-R27 | DTC/SAI accepted additions, DUW retirement | DTC conflicts with GTR and guide-listed PDV/PCX/SFZ/R88/SHT/SB7/CF8; SAI conflicts with V8X in 3LT. Remove DUW from selectable list and active relationships. | DTC/SAI price unresolved; retain DUW only as historical evidence. | E-A; full new-option guide text in `accepted_additions`; ST-D01/02. |

## 6. Selection and reconciliation policies

These records prevent a relationship inventory from losing behavior. They describe
reviewed baseline or expressly proposed target policy; they do not prescribe an
implementation algorithm or database cascade.

| ID | Event / condition | Required or proposed result | Evidence / qualification |
|---|---|---|---|
| ST-S01 | Body/trim change | Reset selections and interior; apply new context defaults. Do not restore old purchases when returning to previous trim. | E-B §§2/4/11; ST-O07/08. |
| ST-S02 | Interior absent or incompatible after context/seat change | Exactly one eligible interior required. Clear invalid selection; auto-select sole eligible choice; multiple choices remain unset; zero choices remain blocked. Report `Interior Color`, step `base_interior`. | E-S §2 records reviewed frozen `reconcileInteriorSelection()` / `missingRequirementDetails()`; no new zero/one/many execution here. |
| ST-S03 | Choice attempted | Check effective applicability, prerequisites and direction-specific conflicts. Preserve tested refusal/replacement direction; untested directions require verification. | ST-R04/05/16/19; E-S §3. |
| ST-S04 | More than one inclusion/addition cause | Emit target once, charge once; retain while another cause remains. Do not infer multiple purchases from repeated relationships. | D30, D3V, DRG; ST-O10/46/47. |
| ST-S05 | Package absorbs prior standalone purchase | Consume prior purchase intent; package removal does not resurrect it. | PCU/STI, PEF/CAV, PDY/RYT, SBT/SC7; ST-O23–25/35. |
| ST-S06 | Included peer yields to explicit choice | Keep paid alternative, suppress included peer, retain full package charge; remove package without removing independently valid paid peer. | PCX/PDV; ST-O26/27; ST-D06 target-policy confirmation remains explicit. |
| ST-S07 | Direct prerequisite lost | Remove FE4 after Z51, BCP after convertible ZZ3, NWI after WUB, SPZ after SPY. | ST-O11/18/21/22. This is not universal evidence for every requirement family. |
| ST-S08 | 5ZU paint prerequisite lost after selection | Baseline retains wing and charge but marks build invalid and blocks submission. Immediate deletion/refusal is an unresolved target choice. | E-B §6; ST-D07. |
| ST-S09 | Default/restoration conditions | FE1 when suspension empty; NGA absent NWI; 719 when belt group empty; BC7 coupe unless cover peer prevents re-add. FE3 supplied by surviving Z51 after FE4 removal. | Four default rows plus group/inclusion behavior; E-B §§5/7/8. |
| ST-S10 | Required choice groups | Required factory wheel/roof/paint/seat/belt/caliper and badge behavior follows effective sections; interior cardinality is separately ST-S02. Initial defaults and fallback are distinct. | All relevant section/group rows retained. Grand Sport's newly stated wheel/caliper fallback policy is not proof of Stingray's untested removal paths. |
| ST-S11 | Pricing/output | One resolved set of explicit/default/automatic/retained-invalid selections, with suppression and causes distinguished, supplies totals/recap/order inputs. | E-S §4 recommendation; E-B §11 legacy `currentOrder()` / `compactOrder()` evidence; installed-equipment limits below. |

## 7. Presentation, physical content and operational boundaries

| ID | Condition / subject | Content or presentation consequence | Evidence / state |
|---|---|---|---|
| ST-V01 | Z51/FE4 installed equipment | Describe replacements of JL9/G0J/M1L/XFN/FE1 with applicable performance equipment. Keep the static standard-equipment view distinct from installed equipment. | E-B §8; legacy `standardEquipmentRows()` is configuration-only; target installed view proposed, ST-D10. |
| ST-V02 | Convertible EFR/EFY/EDU; D84 versus D86; WKR + high wing; HUB/HUC interiors | Preserve tonneau/accent/roof surfaces, contextual high-wing cover version and suede-trim content. Do not invent separate purchasable RPOs or visual assets. | E-B §§2/4/10/11; ST-D10. |
| ST-V03 | SBT; 5DO/5DG | Additional roof or second wheel set is physical content, not a replacement of factory choice. Included wheel hardware is not separately selected incompatible accessories. | E-G Exterior 1 rows 44, 66–67; ST-R12/22. |
| ST-V04 | R8C/BV4/PIN/VK3/D30/R6X | Preserve sold-order, ship-to BAC, state, acknowledgement and approval disclosures. Frozen selection does not enforce those external contexts. | E-B §11; ST-D11. No customer/approval data added. |
| ST-V05 | Sections, steps, interior navigation and summaries | Preserve required/single/multiple/display-only meaning, placement/order, body/trim copy and recap routing. Raw `is_required=false` on interior sections does not override ST-S02. | Complete scoped presentation rows in record file; E-B §11. |
| ST-V06 | Option/interior/model artwork and future visualizer | Retain existing asset references/roles as evidence. Missing artwork does not alter availability. `.psb` scenes/layers and bindings remain unprocessed. | E-S §6; no new asset inspection or rendering claim. |
| ST-V07 | Refused option explanation | D84 attempted after GBA currently says “Blocked by D84” although D84 is candidate. Keep this known copy issue visible. | E-B §4; no accepted replacement wording or UI implementation. |

## 8. Decision overlay: source, baseline and target remain separate

| ID | Source / baseline difference | Target or pending decision | State |
|---|---|---|---|
| ST-D01 | Guide has DTC, workbook has legacy DUW | Remove DUW offering/active references; add DTC across six configurations with GTR and full guide accessory/package/roof exclusions. Do not mechanically rename DUW edges. DTC appears in exclusions authored by PDV/PCX/SFZ/R88/SHT/SB7/CF8 at Exterior 1 rows 24/25/33/34/55/56/75; preserve those exact endpoints, applicability and lifecycle. New interaction directions still need validation. Raw guide mentions of DUW remain evidence. | Accepted correction, September 7; price unresolved. E-G Exterior 1 row 83; E-A. |
| ST-D02 | SAI absent from workbook | Add all six configurations; retain 3LT V8X conflict while V8X remains inactive. | Accepted correction, September 7; price unresolved. E-G Interior 1 row 40; E-A. |
| ST-D03 | Four R6X/AE4 leaves omit 595 | Add seat charge once under established additive requirement; preserve old totals as defect evidence. | Established requirement; consumer correction not implemented. E-B §7; [R6X review](model-rule-review.md#r6x-requirement-versus-implementation). |
| ST-D04 | 5ZU/Z51 emits guide-conflicting ZF1; TVS/Z51 omits guide-required ZF1 | Decide emitted order-code requirements separately from net T0A suppression. E-S proposes compatibility until resolved. | Conflicting, unresolved. E-G Exterior 1 rows 4/49/80; E-B §6. |
| ST-D05 | 5ZZ/R88/SLN active despite guide unavailable; other six options already inactive | Choose lifecycle for a future release. Preserve baseline and footnotes independently; do not activate CF8/5ZW/5VM/5W8/RYQ/V8X. | Conflicting, unresolved. E-B §12. |
| ST-D06 | Package paid alternatives and asymmetric conflict actions | E-S recommends preserving reviewed behavior. Confirm target treatment and inspect unexecuted overlap/direction cases. No inferred package credit. | Baseline observed; target policy proposed. E-B §§9/10. |
| ST-D07 | Wing remains charged after incompatible paint change | Decide retain-invalid versus immediate reconciliation. Grand Sport prerequisite corrections do not silently resolve this Stingray decision. | Target behavior unresolved. E-B §6. |
| ST-D08 | 5V7 guide includes inactive 5ZW; BV4/R8C exclusion stronger than guide; BCP prose suggests extra coupe prerequisite | Retain effective baseline for review, preserve exact source alternatives, do not promote prose into executable requirements. | Unresolved interpretation/behavior where noted. E-B §§5/10/11. |
| ST-D09 | RNX guide permits Z51 with ZF1; workbook excludes Z51 | Decide conditional guide path versus outright conflict; tested Z51→ZF1→RNX remains refused. | Conflicting, unresolved. E-G Exterior 1 row 31; E-B §10. |
| ST-D10 | Static equipment card and descriptive surfaces do not prove installed-equipment/visual output | Define target output meaning and physical-content vocabulary; retain source facts without claiming executed substitutions/assets. | Proposed design, incomplete output validation. E-B §§8/10/11. |
| ST-D11 | Six service codes and six emissions codes absent from offerings; order approvals not enforced | Keep R6P/R9Y/R9V/R9W/R9L/PRB and FE9/YF5/NE1/NB8/NB9/NC7 as source candidates. Decide ordering-service scope before adding enforcement. | Explicit scope gap. E-G Interior 1 rows 11/44–46/51–52, Mechanical 1 rows 19–24. |
| ST-D12 | Guide option-price headings/currency ambiguous; new-option amounts not accepted | Preserve legacy numeric basis; resolve DTC/SAI rates and release price basis before priced release. Missing does not mean free. | Ambiguous, unresolved. E-B §§1/12. |

## 9. Worked sequences and expected outcomes

These are review checks, not newly executed tests. Each points to retained observed
sequences where available. `B` means configuration base; amounts are partial builds.
Unresolved behavior has a baseline expectation only; accepted corrections have
separate target expectations. Existing observations must never be refreshed to
make a corrected target appear to have been the old behavior.

| ID | Starting context and actions | Expected outcome / authority | Evidence |
|---|---|---|---|
| ST-T01 | Any ST-C configuration → initial state | Correct base, roof/seat/defaults; paint and interior missing. | ST-O01–06 |
| ST-T02 | Coupe 1LT → UQT → 2LT → 1LT | 74,990 → 80,595 → 73,495; included UQT at 2LT, prior purchase not restored. | ST-O07 |
| ST-T03 | Convertible 2LT G8G → D84 → EFY → attempt GBA | 89,885 retained; GBA refused. Body change to coupe resets to 80,595/CF7. | ST-O08/09 |
| ST-T04 | Coupe 2LT BCP → B6P → remove B6P | 81,290 → 83,085 → 81,290; D3V remains through BCP, SL9 removed. | ST-O10 |
| ST-T05 | Convertible 2LT BCP attempt → ZZ3 → BCP → remove ZZ3 | First refused; 88,790 → 89,385 → 87,595; no D3V and no dependent cover left. | ST-O11 |
| ST-T06 | Coupe 1LT HUQ + G26 + Orange belt → White → Torch Red belt | 76,580 initially; D30 retained after paint cause removed, removed after belt cause removed. One D30 throughout. | ST-O17/45/47 |
| ST-T07 | Coupe 2LT AH2/HU7/N26/TU7 → AE4/HU7/N26 | 83,580 → 83,385; seat change clears invalid interior before new leaf selection; AE4 has no TU7. | ST-O40 |
| ST-T08 | Each of four ST-D03 leaves at coupe 3LT | Target = 85,245 + required subtotal in §4, exactly +595 over frozen total; ordinary/AH2 paths unchanged. | ST-O42 plus E-B §7 additive sweep; corrected result is not executed. |
| ST-T09 | Coupe 3LT H8T → paid 3F9 → HTE | 87,335 then 85,840; paid red retained, D30 removed. AUP/HAG instead refuses red; AUP/HVZ supplies red zero. | ST-O43/44 |
| ST-T10 | Coupe 2LT FE2 → Z51 → FE4 → J6F → remove Z51 | 82,490 → 85,990 → 87,885 → 88,680 → 81,390. FE1 restored; red caliper retained; no old FE2 restoration. | ST-O18/19 |
| ST-T11 | Coupe 2LT WUB → NWI → remove WUB | 82,590 → 82,985 → 80,595; NWI removed, NGA restored. | ST-O22 |
| ST-T12 | Coupe 2LT QE6 → 5DG → remove 5DG → R8C | Factory QE6 retained throughout; 86,085 with wheel set, 83,385 with delivery/CFX after removal. | ST-O20 |
| ST-T13 | SPY → SPZ → attempt S47 → remove SPY | S47 refused; dependent SPZ removed with SPY. | ST-O21 |
| ST-T14 | Coupe 2LT QE6 → PCX → 5DO → SHW → remove PCX | 86,285 → 90,680 → 90,975 → 86,380; paid peers survive; full package price before removal. | ST-O26; target confirmation ST-D06 |
| ST-T15 | Coupe 2LT 5ZD → PDV → RXH → remove PDV | RXH replaces caps, remains after package; 81,595 with package/RXH, 80,845 after removal. | ST-O27; ST-D06 |
| ST-T16 | STI→PCU / CAV→PEF / RYT→PDY / SC7→SBT; remove package | Absorbed standalone choice does not return. SBT removal permits CC3; factory roof not replaced by second-roof content. | ST-O23–25/35 |
| ST-T17 | GBA→5ZU→Z51, reverse order, remove Z51 | 87,385 with package/wing at coupe 2LT; ZF1 automatic/T0A absent in baseline; removal leaves wing. | ST-O12/14; ST-D04 |
| ST-T18 | Existing 5ZU/Z51 → G26; TVS+Z51 in both orders | Wing retained invalid at 88,380; TVS/Z51 baseline 85,990 with no ZF1. Do not call either order-code policy resolved. | ST-O12/15/16; ST-D04/07 |
| ST-T19 | DPB→PDV→PCX; PCX→attempt DPB; GTR→attempt DPB | Preserve recorded replacement versus refusal; no universal symmetric action. | ST-O28–31; ST-D06 |
| ST-T20 | 5V7 alone; G8G→5ZU→5V7; attempt Z51/PCU | Alone refused, valid wing route succeeds for 1,395 + 650, conflicting packages refused. | ST-O32/48; inactive 5ZW not exercised |
| ST-T21 | Z51→ZF1→RNX; WKQ→attempt 5ZU | RNX still refused in baseline; cover blocks wing. Conditional RNX target remains unresolved. | ST-O33/34; ST-D09 |
| ST-T22 | 5JR + ZYC + Z51 → aero deletion | DRG once; both paid source charges retained; T0A removal does not drop unrelated mirror content. | ST-O46 |
| ST-T23 | Add DTC in permitted context / attempt GTR; SAI at 3LT with V8X | Target enforces exact guide conflicts and all-six offering scope; DUW absent from active offerings/edges. No total until new rates resolved; V8X currently inactive. | E-A; ST-D01/02; target not executed |
| ST-T24 | Interior eligibility yields zero / one / several leaves; incompatible seat change | Zero blocked; one auto-selected; several await user choice; invalid old selection cleared; unset interior always blocks submission. | E-S §2 reviewed policy; targeted new evaluator check pending |
| ST-T25 | SXB→SXR; RIK→RIN; independent accessory removal; E60 removal; R8C removal | Only respective peers/dependents change. E60 loses TR7; R8C loses CFX; removing RWU does not remove independent accessories. | ST-O36–39 |

## 10. Coverage and handoff boundary

This handoff contains every baseline offering, status, interior leaf/component,
direct/grouped/exclusive relationship, conditional price, combination row and
recorded sequence from the reviewed Stingray analysis, plus the scoped presentation
records and accepted correction overlay. It is a populated model handoff, not an
empty template. Exact rows remain accessible without relying on ignored local notes.

Validation performed for this document: re-read the workbook from its frozen
archive; verified workbook and guide hashes; compared the entire local workbook
extraction to those immutable workbook rows; checked model scoping and referenced
option/interior/configuration identities; reconciled offering classifications and
interior source links; preserved all 48 sequence / 237 state records; checked
within-model RPO duplicates; reviewed the tables against E-B/E-S and checked links
and the diff. No old runtime probes were rerun and no corrected target was executed.

Remaining work is explicit: resolve ST-D open decisions, classify unexecuted
conflict directions/effective scopes during detailed translation, finalize target
price basis/new-option amounts, and validate corrected and installed-equipment
outputs. The 1,386 previously matched status pairs and broader sweeps are evidence
of their stated scope, not full manufacturer-order or release acceptance.

Apply this category structure to Grand Sport next in a separately authorized task,
including its own accepted decisions. Continue the remaining model analyses and
structured handoffs before consolidating the comprehensive schema. No SQL, evaluator,
canonical workbook, reference repository, production output or deployment changes
are part of this task.
