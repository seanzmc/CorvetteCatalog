# Z06 behavior: foundations and connected choices

September 10, 2026. **Complete family relationship analysis; all twelve owner decisions accepted.**
Z06 is model four of six. Stingray, Grand Sport and Grand Sport X have behavior
analyses and structured handoffs; GSX's final decision PR #24 is merged. ZR1 and
ZR1X remain. This pass follows the same structure: model/body/trim, connected
choices and charges, guide → workbook → runtime, discrepancies and coverage.
The original behavior pass did not implement corrections or build the structured
handoff. The subsequent [structured handoff](z06-structured.md) and
[record file](z06-structured-records.json) now preserve this full analysis and all
twelve accepted decisions; frozen evidence and implementation boundaries remain unchanged.

Z06 starts with J56 iron brakes, FE6 suspension and XFR tires. J57, Z07 and
PDB/PDD/PDF are different acquisition paths; they cannot inherit GSX's standard
carbon-ceramic brake behavior. Its LZ interiors use N2Z at 3LZ, and LT6 engine
intake/cover choices differ from the earlier LS6 lanes. Numerical package-price
agreement does not establish correct included equipment or permitted builds.

## 1. Sources, authority and observation method

- **Guide:** unchanged `2027 Chevrolet Car Corvette Export (6).xlsx`, SHA-256
  `d3ca7d3a09c9fb89210b4ce584493b3ad8fb65ca35087c49d816d1cbf1a333d1`.
  Z06 has its own Interior 4, Exterior 4, Mechanical 4, Standard Equipment 4 and
  Equipment Groups 4. D–F are coupe 1LZ/2LZ/3LZ; G–I convertible 1LZ/2LZ/3LZ.
  Shared Color and Trim charts are narrowed to LZ applicability, excluding EL9.
  See [source provenance](../sources/README.md).
- **Workbook:** [September 6 frozen baseline](../baselines/2026-09-06/README.md),
  SHA-256 `3127e663b1531e366ce86b989b6190914108d40dfd15a33a258307a05d608e3c`.
  `model_workbook_sources!35:45` routes Z06 to `z06_*`, `LZ_Interiors` and
  `color_overrides`; interior membership and components are model-qualified.
- **Runtime:** unchanged frozen `form-app/app.js`, registry `data.js` and
  `z06-runtime-contract.json` from `4fe92a4f078370c478f18484cad31bdafe58ad43`.
  Each extracted member's hash was checked against the manifest. Probes call
  the actual selection, pricing, reconciliation and order functions through the
  established DOM-stub harness, asserting registry key `z06` and source sheet
  `z06_options`. These are local functional observations, not browser visual QA,
  live ordering or corrected-runtime proof. All runs made zero requests.

Amounts below retain the frozen numeric basis, compared with guide option
Price Schedule column E and its column D qualifiers. Base prices use F + J.
The guide's option header alignment ambiguity remains documented in source
provenance. Earlier model USD/price-basis decisions are precedent for review;
this pass does not silently accept a new Z06 tariff or extend GSX-only approvals.
The canonical workbook, baseline, application, schema and reference project stay
unchanged. Frozen findings below remain historical evidence; the September 10 owner decision
overlay in §9 records accepted targets, not implemented corrections.

## 2. Model, body and trim establish the starting configuration

`model_variants!20:25` joins `variant_master!20:25`; trim labels are not model
identities. Destination 2,495 is already included in the base. R8E is separate.

| Body | Trim | Base including destination | Initial R8E | Initial runtime total |
|---|---|---:|---:|---:|
| Coupe | 1LZ | 121,395 | 2,600 | 123,995 |
| Coupe | 2LZ | 130,295 | 2,600 | 132,895 |
| Coupe | 3LZ | 134,945 | 2,600 | 137,545 |
| Convertible | 1LZ | 128,395 | 2,600 | 130,995 |
| Convertible | 2LZ | 137,295 | 2,600 | 139,895 |
| Convertible | 3LZ | 141,945 | 2,600 | 144,545 |

All six bases reconcile to Price Schedule rows 25/30/31 and 28/32/33. R8E is
mandatory at `Mechanical 4!35` and numeric rates are in Price Schedule 199–200.
`default_selection_rules!20` selects the charge. `z06_price_rules!50:51` raises
it to 3,000 when T0F or T0G is present, including through packages. The trigger
is the aero, not simply Z07 or carbon wheels. Coupe 3LZ T0G → T0E gives
148,940 → 137,545, removing both 10,995 aero and the 400 tax increment.
This is order-guide/workbook behavior, not independent tax-law verification.

All initial builds select EYT, J6A, T0E, J56, SOE, NGA, EFR, R8E and black 719.
Paint and Interior Color remain required and unset. Coupe has CF7; convertible
CM9. AQ9 starts at 1LZ/2LZ and AH2 at 3LZ. Body/trim changes reset purchases
and interior: 3LZ coupe with PDF and HTE → 1LZ convertible returns to 130,995.

UQT is a 1,495 purchase at 1LZ, included/display-only at 2LZ/3LZ. Its workbook
option base is zero; price row 46 and four variant overrides implement the
exception. E60 and BAZ/FA5 begin at 2LZ; DY0/FA6/5JR begin at 3LZ. W2D is a
1LZ accessory while AP9 is supplied at 2LZ/3LZ. UV6 and DRZ are standard even
at 1LZ. Audio UQS→UQH, charging K7A→K7B, mirrors DWK→DYX and UVB→UVA camera
changes are independent trim equipment facts, reconciled across all six contexts.
Sources: Interior 4 rows 8–12, 18, 23, 29, 43–44, 54, 57–58, 66–92, 104–105;
Exterior 4 rows 22, 45, 68–73. LT6/M1M/B4Z are standard (Mechanical 4 24/42/48).

## 3. Brakes, Z07, aero and carbon-wheel packages

### Acquisition, charge ownership and required content

Sources: Exterior 4 rows 4–9, 24–26, 77, 94–107; Mechanical 4 rows 6–17,
45–49; `z06_rule_mapping!17:21,!34:46,!50:53`; price rules 4–34, 50–51;
rule groups 2–5 and 11–16. Standard suspension/tires are FE6/XFR.

| Path | Frozen acquisition / charge | Consequences |
|---|---|---|
| J57 alone | 9,000; no Z07 prerequisite | Replaces J56 and black J6A; permits carbon wheels and orange J6L |
| Z07 | 9,500 plus T0F 8,995 by default | J57, FE7, XFS and CFZ included; aero raises R8E by 400 |
| Z07 with T0G | 9,500 + 10,995 | CFV replaces CFZ; explicit T0G survives removing Z07 |
| PDB | Wheel-qualified package rate below | J57, J6D and default ROY; no Z07, FE7 or XFS |
| PDD | Wheel-qualified package rate below | Z07, T0F/CFZ, J57, FE7, XFS, default ROY |
| PDF | Wheel-qualified package rate below | Z07, T0G/CFV, J57, FE7, XFS, default ROY |

| Package | ROY | ROZ | STZ |
|---|---:|---:|---:|
| PDB | 16,000 | 17,000 | 17,500 |
| PDD | 25,495 | 26,495 | 26,995 |
| PDF | 26,495 | 27,495 | 27,995 |

All nine combinations were checked in all six configurations: **54 package
states**. Package-plus-wheel charges match Price Schedule 52–60; PDB retains
2,600 R8E, PDD/PDF use 3,000. The browser's `packageComponentBasePrice()` and
`packageComponentDelta()` display the minimum package amount plus a 1,000 ROZ
or 1,500 STZ increment. Workbook wheel→package overrides therefore must not be
added again to the wheel delta. Standalone ROY/ROZ/STZ are 11,995/13,995/15,500
and require J57; these are not the package deltas or GSX's discounted rates.

**Missing included calipers:** Mechanical 4 row 7 says J57 includes J6D; row 49
also specifies J6D with Z07. The workbook has J6D→J57 prerequisite and a
J57→J6A replacement, but no J57→J6D inclusion. Only PDB directly includes J6D.
Consequently J57 and Z07 leave Caliper Color empty in all six configurations;
36 PDD/PDF matrix states do too. PDB's 18 states correctly have J6D. Manually
selecting J6D resolves the missing requirement at zero cost. This blocks
submission until addressed; it is not a silent numerical undercharge.

Paid compatible calipers remain independent: J6F 795 survives a J57→J56
change or PDB removal. J6L and J6D require J57. In coupe 3LZ, J57 → J6L → ROY
→ J56 ends at 137,545 with J6A/SOE restored and the now-invalid orange calipers
and carbon wheels removed. Clicking an already selected required brake does
not clear it; use J56 to downgrade. Probes distinguish toggles from replacements.

### Package switching, removal and overlapping causes

PDB/PDD/PDF replace each other. Carbon-wheel alternatives remain available,
while aluminum wheels and J56 are blocked until the package is removed. PDD
locks T0F; PDF locks T0G. Standalone Z07 permits either aero, while blocking
T0E/5ZV and J56 even after switching to T0G.

Coupe 2LZ PDB → ROZ → PDD → STZ → PDF → remove PDF totals
148,895 → 149,895 → 159,790 → 160,290 → 161,290 → 132,895.
The PDB→PDD switch also loses J6D, demonstrating the missing inclusion above.
Package removal restores J56/J6A/SOE/T0E when nothing independently supports
an alternative. Previously bought J57/ROZ/T0G are absorbed by PDF; removing PDF
does not restore those purchases. This purchase-intent loss needs an explicit
target policy rather than assuming the original paid state survives.

PDB and standalone Z07 can coexist in either order. Coupe 2LZ totals 167,790
with ROY, T0F and 3,000 R8E, versus 158,790 for PDD's equivalent listed content:
**9,000 more**. The guide does not explicitly prohibit stacking or require
automatic package substitution. Preserve this as a price-path decision, not an
invented exclusion or an automatically accepted repricing. Removing either
cause preserves the other's valid content; removing PDB can again expose the
missing-J6D state while Z07 remains.

## 4. Aero, accents, roofs and physical content

T0F supplies CFZ; T0G supplies CFV, each at zero additional charge. Standalone
CFZ/CFV cost 3,495/4,495. Acquiring aero replaces incompatible standalone ground
effects. Once included by aero, the alternate ground effects/CFL are blocked.
CFL is 995 and exchanges with standalone CFV. SIG costs 425 and requires the
standard T0E spoiler: selecting 5ZV removes SIG, while returning to T0E allows
it again. Do not copy GSX's different SIG prerequisite. WKR's high-wing version
is contextual supplied content when the guide's listed high wings/aero are
present; it is not a second car-cover purchase (Exterior 4 37, 51–53).

EFR, EDU and EFY describe finish coverage. CBF costs 495 and conflicts with
GBA, EFY and CFV/CFZ. EDU+CBF is allowed. Selecting GBA after EDU+CBF removes
both and restores EFR; attempting CBF under EFY is refused. T0F acquired after
CBF removes CBF, whereas direct CFV attempted after CBF is refused. The five
extra runtime replacement edges derive T0F/T0G/Z07/PDD/PDF→CBF from inclusion
closures. There are 110 workbook direct rules and **115 emitted direct rules**;
these five code-derived effects need an explicit future owner. Do not infer
that every exclusion has the same direction or interaction.

Guide Exterior 4 18–21 retains physical distinctions: CFV changes the EFR
rocker/splitter finish; CFV/CFZ changes EDU's splitter and EFY's rocker finish;
convertible tonneau grille wording differs. These are contextual descriptions,
not additional option identities. Some workbook relation disclosures still
mention LS6 covers or Z51/TVS (`z06_rule_mapping!3,!9`); their actual endpoints
are D3V/DRG, so preserve the old wording as provenance rather than treating it
as a new Z06 acquisition rule.

Coupe CF7/CC3/C2Z and convertible CM9/D84/D86 are separate availability paths.
D84/D86 cost 1,295; ZYC 295 includes DRG. In convertible 2LZ, G8G → D84 → ZYC
→ GBA totals 139,895 → 141,190 → 141,485 → 139,895: the new black paint removes
the incompatible top finish and mirrors and restores CM9. This is different
from GSX's observed paint refusal. 5JR and ZYC can both support DRG; removing
one retains DRG until its last cause disappears (3LZ four-state reversal).

**Dual-roof overcharge:** Exterior 4 47/Interior 4 40 specify SBT includes SC7;
Price Schedule 131 gives 2,525. `z06_rule_mapping!14` acquires SC7, but the 72
price rules omit SBT→SC7 zero pricing. SBT alone therefore charges **2,720** in
all three coupe trims. The 2LZ total is 135,615 rather than guide-derived
135,420. An already purchased pouch is also charged under SBT, then removed
with the package. CC3 and SBT block each other in both tested directions;
the extra transparent panel is physical package content, not a second CC3 charge.

## 5. LT6 engine intake, appearance and exhaust

Sources: Mechanical 4 24–40; Price Schedule 51, 121, 173, 180–181, 186;
`z06_rule_mapping!3:5,!47,!49,!54`; price rules 2–3, 35–37 and 47.

| Context | Frozen behavior |
|---|---|
| Coupe BCW alone | 995, includes D3V at zero; does not require B6P |
| Coupe BCW with B6P | B6P 1,895 + BCW 895; D3V/SL9 zero |
| Convertible BCW | Requires ZZ3 1,195, then BCW 895; SL9 included, no D3V |
| PBC engine build | 9,995; coupe independent, convertible requires ZZ3 |

Coupe 2LZ BCW → B6P → remove B6P → remove BCW totals
133,890 → 135,685 → 133,890 → 132,895. D3V survives package loss while BCW
still supports it. An independent D3V purchase absorbed by B6P does not return
when B6P is removed. Convertible 2LZ ZZ3 → BCW → PBC → remove ZZ3 totals
141,090 → 141,985 → 151,980 → 139,895, clearing both invalid dependents and SL9.
The emitted BCW/PBC prerequisites explicitly scope convertible. No GSX
ZZ3→LS6 engine mapping is present in this lane.

**Cover/brace exclusion missing:** Mechanical 4 37 and `z06_options!49` say
SLN is unavailable with RXI. No direct/grouped/exclusive relationship enforces
that disclosure. RXI 2,495 and SLN 2,895 coexist in both directions in all three
coupe trims, with no missing requirement and enabled submission. Coupe 2LZ
charges 138,285 for the conflicting combination. Unlike GSX, this Z06 SLN
source does not say unavailable at this time; do not copy that lifecycle status.

WUB quad-center exhaust is standard here (Mechanical 4 31), not a 1,995
prerequisite purchase. NWI adds 395 and replaces NGA; removing NWI restores NGA.
E60 at 2LZ/3LZ adds 2,995 and TR7; removal clears TR7 and its content once.

## 6. LPO wheels, Tech Bronze and graphics

### PCZ's description is not an executed package

Exterior 4 32 explicitly includes 5DK, SFZ, SHT and VPO in PCZ for 5,295.
Workbook option row 75 repeats that content, but the direct rules, group rules
and price rules have no PCZ inclusion/zero-price implementation. Across all six
configurations PCZ alone emits none of those four codes. Each can be purchased
again: 4,450 + 250 + 495 + 575 = **5,770 additional**, while PCZ remains charged.
Coupe 2LZ totals 138,190 for PCZ alone and 143,960 after adding its four stated
contents. Both states pass missing-required checks; compact output confirms the
missing or separately charged content. Removing PCZ leaves the separate purchases.

PCZ also permits R8C, PDA, DPB and PDB/carbon wheels despite its guide exclusions.
These are missing relationships, not an architecture proposal or a reason to
reuse Grand Sport's different PCX package. The full guide exclusion set includes
R8C, SPZ/SFE/SPY/S47, ROY/ROZ/STZ, EYK, PDA/SNE/VPW and all 16 listed racing/
stinger stripes. Current PCZ wording also omits VPW from its exclusion list.
A corrected target must preserve package content, child pricing, conflicts and
removal behavior together; just adding four codes would leave invalid builds.

### Second wheel sets are not factory-wheel replacements

Exterior 4 64–65 describe 5DH and 5DK as accessory second sets, each 4,450.
Both include black lug nuts/locks as physical content; 5DK also supplies bronze
caps. Factory SOE stays selected in the baseline. Their guide excludes R8C,
SPZ/SFE/SPY/S47 and ROY/ROZ/STZ, but those constraints are not implemented.
Both R8C→5DK and 5DH→R8C succeed across all six configurations; 5DK→PDB and
5DH→SPY do too. Every tested resulting build is submission-ready. Do not emit
an additional charged SPY/SPZ purchase merely to represent the supplied hardware.

Standalone hardware does have rules: SPZ requires SPY; losing SPY removes SPZ.
S47/SFE conflict with carbon wheels and SPY. These relationships do not establish
coverage for the missing LPO-wheel constraints. R8C includes CFX and blocks BV4
in the tested path; it costs 1,695. Guide Exterior 4 15 also requires SOLD status,
Ship To BAC 184590 and acknowledgement, none of which is a locally verified
external ordering action.

### Stripe/paint and rear-hash conflicts are incomplete

The following complete source-listed prohibition pairs were tested on both
bodies in both selection directions at 2LZ:

| Stripe | Forbidden paint(s) |
|---|---|
| DUE, DPB | GTR |
| DUK, DPL, DSZ, DZX | GKZ, GPH |
| DPC, DT0, DZU | GBK |
| DPG, DSY | G26 |

**All 60 attempts retain both choices with no missing requirement.** Source:
Exterior 4 78–93; the workbook has disclosures but lacks these direct paint
exclusions. Example: GTR + DUE is 134,690 in coupe 2LZ, in either direction.
DPT/DTH/DUB/DZV have no corresponding source paint prohibition; they are not
classified as missing restrictions. DTC is absent, discussed in §9.

VPW/VPO groups 19–20 only cover other Jake graphics. They omit the full stripe
exclusions at Exterior 4 54–55. VPW+DPB in both directions and VPO+DPB remain
submission-ready in all six configurations; VPO+EYK is also allowed despite its
explicit chrome-badge exclusion. The 2LZ rear-hash/DPB total is 134,765.
PDA correctly includes SNE/VPW for 950 with zero child charges, replaces an
independently purchased SNE, and removes children on package loss. Its included
hood graphic and group prevent the tested DZX conflict. SHT/SNE and full-length/
stinger stripe groups are present; they do not rescue standalone rear-hash gaps.

SFZ acquired after DPB removes DPB; DPB attempted after SFZ is refused. R88 has
badge/stripe groups but remains purchasable despite its lifecycle disclosure.
No Z15, heritage hashes, EL9 or Z25 choice belongs to this Z06 lane; the GS/GSX
conditional center-stripe/D84 relationship is not imported here.

## 7. Complete LZ interiors, component prices, paint and belts

Color and Trim 1 rows 5–12 and Color and Trim 2 rows 5–8 yield **78** base
trim/seat/code combinations, expanding exactly to **130** workbook leaves:
four 1LZ, 40 2LZ, 71 ordinary 3LZ and 15 custom R6X 3LZ. No missing or extra
expanded leaves. `model_interior_scope!134:263` selects them; all 197 model-owned
component memberships (`interior_components!396:592`) were reconciled against
PriceRef with its type normalization, including `two_tone`→`TwoTone`.

N26 costs 695 on the specified 1LZ/2LZ suede paths; 3LZ suede uses N2Z 895.
AH2's HU7/HUA/HXO paths require TU7, and optional two-tone remains confined to
the chart codes and AH2. HU0/HXO require 38S. Optional 36S/37S/38S uses the listed
black interiors and costs 495. TU7 is 595. EL9 is not applicable: the separate
Color and Trim 1 row 13 is 3LT only. Sources: Interior 4 66–87 and both charts'
footnotes. Do not reuse LT N26 prices for these 3LZ leaves.

Seat rates reconcile to Price Schedule 238–242: AE4 1,095/2,095/595 by trim,
AH2 1,695 at 2LZ and standard at 3LZ, AUP 350 at 3LZ. The price schedule's
AUP qualifier names HVZ only, while Interior 4 69 and Color and Trim 1 12
explicitly permit both HVZ and HAG. Preserve that internal guide inconsistency;
the workbook and runtime permit both at 350. Bare 2LZ AE4 initially
shows its option-base price 1,095; completed ordinary interiors include the
2,095 component amount. This transition is not proof of a final undercharge;
Interior Color is mandatory and an incompatible seat change clears it. The
missing-interior submit handler was exercised and made no request.

### Four R6X/AE4 leaves lose the seat increment

| Workbook leaf / LZ_Interiors row | Component-derived charge | Frozen resolved charge |
|---|---:|---:|
| `3LZ_R6X_AE4_HUU` / 121 | 1,590 | 995 |
| `3LZ_R6X_AE4_HU0_38S` / 124 | 2,085 | 1,490 |
| `3LZ_R6X_AE4_HZP_N2Z` / 129 | 2,485 | 1,890 |
| `3LZ_R6X_AE4_HXO_N2Z_38S` / 131 | 2,980 | 2,385 |

Each is short 595. HXO should comprise AE4 595 + R6X 995 + N2Z 895 + stitching
495. The observed 3LZ coupe total is 139,930 versus component-derived 140,525.
The LZ sheet's stored Price is extras-only; legacy contract assembly adds the
R6X increment after subtracting the ordinary seat rate, and browser interior
itemization suppresses the separate seat when components contain R6X. The
frozen component list for these leaves lacks the AE4 component, leaving its
595 unpaid. This is the independently demonstrated LZ path, not a copied LT
stored-composite explanation. `catalog/contracts.py:interiors()` preserves the
legacy assembly; frozen `adjustedInteriorPrice()`/`lineItemsFromInterior()` are
the observed consumer. No baseline value was changed to manufacture parity.
The other 126 resolved interior charges match their applicable components.

### Recommendations, inclusions and prohibitions stay separate

All 260 body/interior contexts selected their expected leaf and component rates.
The chart yields exactly 137 paint/interior D30 conditions, matching the workbook.
All 1,300 coupe paint/interior states agree. These are surcharge recommendations,
not hard color prohibitions. D30 costs 1,495 once regardless of multiple causes. A 1LZ coupe HUQ
sequence G26 → orange belt → G8G → red belt totals 126,485 → 127,080 →
126,085 → 124,590: losing the paint cause retains D30 until the belt cause
is also removed, with never more than one D30 line.

Interior 4 60–65 yields exactly 132 belt surcharge pairs, matching this model's
color-override rows. All 780 belt attempts reproduce them; all 30 forbidden
HAG/HVZ alternatives are refused and each result has one belt line. HAG permits
blue 3A9 only, HVZ red 3F9 only. H8T/HAG include blue; HNK/HVZ red; HUW/HUX
orange; HZN/HUF/EJH/EPX natural. Other permitted paid alternatives may replace
an included belt. H8T → orange yields 595 belt + 1,495 D30; switching to HTE
retains orange but removes D30. AUP HAG→HVZ switches the zero-cost belt while
retaining its 350 seat charge. There is no EL9/belt exception in this model.

BAZ 695 can coexist with FA5 1,795; FA6 5,295 replaces FA5 at 3LZ. DY0 795
is independent. Removing FA6 does not restore previously selected FA5.
IWE and the custom leather-wrapped package are trim content. HUB/HUC changes
the stated instrument-panel/door/console finish to suede (Interior 4 89–92).
N3W is standard in the guide at 3LZ but inactive in the workbook: it is absent
from runtime standard equipment, unlike NK4 at lower trims. Its future content
representation must be resolved separately from selectable N2Z and lifecycle
unavailable accessories; the guide does not mark N3W unavailable.

## 8. Remaining accessories, availability and order consumers

PCQ 1,675 includes VWE/VWT at zero; PEF 475 includes CAV/RIA; PDY 195 includes
RYT/S08. Tested independent-child→package→removal sequences return to base and
lose the absorbed purchase. These families have zero-price overrides, unlike
SBT and the absent PCZ inclusions. Source: Exterior 4 33, 43–44; Interior 4
27–33, 38. Indoor covers, center caps, rear-script colors and suede compartment
liners each exchange within their own group. Outdoor RWJ is separately scoped.
5ZC/5ZD cost 250; SXB/SXR 2,095, SXT 2,695; RIK/RIN/SL8 are 395/440/495.
ERI, VUP, SLK, RWU and S2L were also exercised as independent accessories.

Guide lifecycle limits remain distinct from status markers. RYQ/V8X/5V5/CF8
are inactive and absent from active choices. R88 remains active and purchasable
for 695 despite Exterior 4 41's unavailable-at-this-time disclosure. The source
limits are at Exterior 4 39/41/51/73 and Interior 4 42. Retaining dormant
compatibility evidence does not certify those items for release. Z06 SLN has
no equivalent lifecycle prohibition in the supplied guide.

The 12 dealer/service/emissions codes omitted from customer options are:
Interior 4 R6P (11), R9Y/R9V/R9W (45–47), R9L/PRB (52–53); Mechanical 4
FE9/YF5/NE1/NB8/NB9/NC7 (18–23). These comprise six interior/service and six emissions codes. Their ordering context remains guide evidence, not a
missing option-card implementation request. D30/R6X/BV4/PIN and R8C retain
SOLD-order or approval disclosures; VK3 is selected locally, without verifying
ship-to-state enforcement. PBC program acceptance is also external to these probes.

`standardEquipmentRows()` is based on model/body/trim, not the resolved purchases:
its 2LZ output is identical before/after Z07 and still lists FE6/XFR. The compact
configured item list records FE7/XFS and the purchased/package choices; static
equipment must not be presented as a complete installed-build inventory. N3W's
inactive omission is separate from that static-versus-configured distinction.

Of 99 completed defect-context checks, 87 have no missing requirement and enabled
submission, including PCZ missing/double-priced content, incompatible LPO wheels,
rear hashes, SBT pouch charges and cover/brace combinations. The 12 J57/Z07
caliper-gap contexts correctly block submission. Package-matrix PDD/PDF caliper
gaps were recorded separately. No valid submit handler was invoked. Only the
incomplete-interior rejection was tested; no customer data or order was sent.

## 9. Complete source disposition and review decisions

All **244 workbook offerings** have a disposition: 207 primary-guide coded
matches, 26 uncoded equipment matches, ten chart paints and legacy DUW. No
within-model duplicate RPO exists, including inactive rows. The 1,242 coded and
156 uncoded statuses all match: **1,398 primary status comparisons**. The full
availability table has 1,464 rows; the remaining 66 cover paints and DUW.
All 233 repeated coded occurrences in Standard Equipment 4/Equipment Groups 4
agree with their primary text/status. Status agreement includes inactive N3W
and therefore is not equivalent to correct runtime emission.

Uncoded mappings, workbook option row → guide row:

- Interior 4: 25→89, 160→6, 161→16, 162→17, 163→19, 164→20, 165→22,
  166→24, 167→26, 168→59, 169→84, 170→94, 171→98, 172→101, 173→102, 217→51.
- Exterior 4: 174→7, 175→17, 176→23, 177→108.
- Mechanical 4: 139→4, 140→10, 178→34, 179→41, 180→44, 181→47.

All 155 numeric option amounts were compared with Price Schedule: 137 match
at least one same-code column-E amount, UQT reconciles through its trim-specific
price/availability, and 17 standard/default/paint zero rows have no schedule
amount. The remaining 89 option prices are null evidence. Qualified rates were
also checked: nine carbon-wheel package totals, standalone wheel/J57/Z07 rates,
BCW body/package pricing, R8E aero conditions, seats and interior components.
This does not turn same-code numeric agreement into blanket acceptance: SBT,
PCZ and R6X show different ways an apparently correct price can resolve wrongly.

DTC is a new primary offering at Exterior 4 80, 1,295 at Price Schedule 257,
with GTR exclusion; DUW (workbook 208) lacks a primary offering in this guide.
The guide still mentions DUW in some conflict disclosures, so preserve that
source inconsistency. DUE's guide name is Royal Blue, not the workbook's
Santorini Blue. SAI is absent from workbook customer offerings but offered in
all six guide contexts at Interior 4 41 and Price Schedule 128 (295), with V8X
conflict at 3LZ. TU7/N26/N2Z/36S/37S/38S are represented through interior
components, not classified as missing customer cards.

### Owner decisions accepted September 10, 2026

The owner approved all twelve review items in this conversation, with the
specific interaction policies below. These accepted targets supersede the earlier
proposals and unresolved-choice wording; frozen observations and raw contradictions
remain unchanged. This is the decision log for the subsequent structured handoff,
not the complete structured record file or corrected-runtime verification.

| Review ID | Status | Accepted target |
|---|---|---|
| Z06-D01 | Accepted | Add J57→J6D default inclusion, allowing compatible paid caliper upgrades. Confirm J57/Z07/PDD/PDF acquisition and default restoration across all configurations. J6D is gray; the conversational review list incorrectly called it red. The approved code is unchanged. |
| Z06-D02 | Accepted | Implement PCZ's four contents (5DK, SFZ, SHT, VPO) once at its 5,295 charge, with zero additional child charges, full guide conflicts and explicit child/removal ownership under the accepted independent-purchase policy. |
| Z06-D03 | Accepted | Implement 5DH/5DK second-set exclusions. Retain factory wheels; represent included black lug nuts/locks and 5DK bronze caps as supplied content without duplicate accessory charges. |
| Z06-D04 | Accepted | Apply all 15 inspected stripe/paint prohibition pairs in both directions; retain non-prohibited combinations. |
| Z06-D05 | Accepted | Complete VPW/VPO stripe and package/badge conflicts. Explicitly refuse conflicting stripes in both directions. Use a replacement notice for conflicting badges, following the accepted replacement-offer policy rather than silent replacement. |
| Z06-D06 | Accepted | Price SC7 at zero under SBT so the package costs 2,525, not 2,720. Preserve independent-purchase intent according to the accepted application policy, including a pouch purchased before SBT and subsequent package removal. |
| Z06-D07 | Accepted | Enforce RXI/SLN conflict in both directions using the accepted general conflict policy. Keep Z06 SLN available otherwise; do not classify it as lifecycle-unavailable. |
| Z06-D08 | Accepted | Restore each of the four missing AE4 595 charges listed in §7, retaining N2Z 895 and all other model-qualified components. |
| Z06-D09 | Accepted | Replace legacy DUW with DTC at 1,295 and all its relationships, including the GTR prohibition. Rename DUE to Royal Blue. Add SAI at 295 across all six configurations with its 3LZ V8X exclusion. Preserve raw source contradictions. |
| Z06-D10 | Accepted | Display unavailable R88/RYQ/V8X/5V5/CF8 accessories as disabled, with unavailable-at-this-time presentation. Restore N3W as 3LZ standard equipment, separate from N2Z; selecting N2Z removes N3W from the configured equipment. |
| Z06-D11 | Accepted | Do not permit PDB and standalone Z07 to coexist. Make Z07 nonselectable with PDB, or require a switch to PDD with notice before accepting Z07. The owner authorized either interaction; the combined 9,000-premium path is rejected. Do not silently substitute a package or infer approval for a PDF substitution. |
| Z06-D12 | Accepted | Use USD and raw Price Schedule column E for option amounts. Destination is included once in base; R8E is separate at 2,600, rising to 3,000 with T0F/T0G. Permit AUP HAG and HVZ at 350 while preserving the guide qualifier inconsistency. Keep customer-form ordering scope and external approval/delivery disclosures without claiming external enforcement. Distinguish baseline informational equipment from the configured installed build, reflecting replacements such as FE6/XFR→FE7/XFS. |

Previously accepted application-level dependency cleanup with alert/revert,
independent-purchase preservation and explained conflict replacement offers remain
design guidance. Explicit refusal exceptions, including D05's stripes, take
precedence; D05's badge conflicts use replacement notice. D11 records the owner's
permitted interaction alternatives without inventing a single chosen UI treatment.
No business-decision item remains unaccepted. Implementation, final UI treatment
within those alternatives and corrected-output validation are later work.

## 10. Implications, validation and handoff

The paused Stingray proposal must accommodate model-owned acquisition paths,
multiple inclusion causes, replaceable defaults versus locked package content,
package base-plus-component price display, extras-only LZ interior prices,
mandatory conditionally priced charges and independent accessory-set content.
A disclosure is not an executed constraint; a status row is not active emission;
a price match is not correct total ownership. The five derived CBF replacement
edges and static equipment consumer also require explicit translation ownership.
Revisit one coherent design after the remaining model lanes, without implementing
an independent Z06 schema or importing GSX's standard-brake assumptions.

Validation performed against the frozen sources:

- All 244 offering dispositions, 1,398 primary status pairs, 233 repeated guide
  occurrences, 155 numeric option amounts and six base prices reconciled.
- 78 source interior combinations → 130 exact leaves; 197 component memberships,
  260 body/interior contexts, 1,300 paint states and 780 belt attempts checked.
- 61 connected sequences / 274 states plus eight focused sequences / 26 states
  and a four-state D30 multiple-cause check.
- 54 package/trim/body/wheel states; 99 completed defect contexts; 60 prohibited
  stripe/paint attempts; static-equipment comparison and submit-handler rejection.
- Source/manifest checks and documentation consistency/diff review. No requests,
  source mutation, generation into 27vette, runtime repair or schema changes.

Local reproducible extraction/probes and observations are in `.local/z06/`:
`extract.py`, `coverage.py`, `audit.py`, `interior-check.py`, `verify-source.py`,
`full-probe.mjs`, `combinations.mjs`, `focused.mjs`, `d30.mjs` and their JSON results.
Exact source rows and material outcomes are retained above for durable review.
“Complete” is family/source coverage, not all-build combinatorial acceptance,
visual browser QA, production validation or verification of proposed corrections.
Owner decision review and the subsequent Z06 structured handoff are complete.
ZR1/ZR1X remain the next model lanes; they and schema consolidation do not start
in this pass. Implementation and corrected-output verification remain later work.
