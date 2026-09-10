# Grand Sport behavior: foundations and connected choices

**September 9 review update:** [Accepted owner decisions](grand-sport-structured.md#8-decision-overlay-source-baseline-and-target-remain-separate) supersede earlier unresolved/proposed target statements below. This analysis preserves the original guide, workbook and observed behavior; it is not a statement that corrected targets have been implemented.

September 8, 2026. **Grand Sport relationship analysis for schema planning.**
This follows the same lane structure as [Stingray](stingray-behavior.md):
foundations, connected choices and charges, guide → workbook → observed behavior,
unresolved differences, and coverage. Section 12 tests those findings against the
[Stingray schema proposal](stingray-schema-plan.md). No schema, workbook, runtime,
business-data correction or cutover is implemented here. The owner decisions
below establish intended Grand Sport behavior; they do not authorize schema
implementation or cutover. Frozen observations remain evidence of the old form.

Grand Sport adds two important design challenges: a stripe can require a roof
only with specified paints, and a special interior currently carries a package's
charge while automatically acquiring that package. Performance packages also
demonstrate why initial defaults, restoration, explicit purchases and locked
included equipment need separate behavior.

## 1. Sources and how to read this analysis

**Guide:** the unchanged `2027 Chevrolet Car Corvette Export (6).xlsx`, hash
`d3ca7d3a09c9fb89210b4ce584493b3ad8fb65ca35087c49d816d1cbf1a333d1`.
Grand Sport is explicitly named in `Interior 2`, `Exterior 2`, `Mechanical 2`,
`Standard Equipment 2` and `Equipment Groups 2`. In the primary sheets, D–F are
coupe 1LT/2LT/3LT and G–I are convertible 1LT/2LT/3LT. The shared `Color and Trim`
sheets are narrowed to this model, including EL9. See [source provenance](../sources/README.md).

**Workbook:** the [frozen baseline](../baselines/2026-09-06/README.md), hash
`3127e663b1531e366ce86b989b6190914108d40dfd15a33a258307a05d608e3c`.
`model_workbook_sources!A2:E12` routes Grand Sport to the `grandSport_*` option,
availability, relationship, price and override sheets, plus `lt_interiors` and
`color_overrides`. Shared storage does not establish shared product ownership.

**Observed:** execution of the frozen `form-app/app.js` and `data.js` from
`4fe92a4f078370c478f18484cad31bdafe58ad43`, using its DOM-stub harness with additional
read access to selection/itemization functions. The browser registry key is
`grandSport`; the workbook model key is `grand_sport`. Source hashes and the
active model were checked. These are real frozen selection functions, not a new
evaluator, visual browser QA, or a live submission. All probes made zero requests.

Amounts below use the workbook's numeric basis. Six base amounts reconcile with
guide base MSRP plus destination; the option-price column ambiguity and currency
remain unresolved. Example totals are partial builds unless stated otherwise.
Agreement with a price-schedule number alone does not resolve its price basis.

### Owner review decisions — September 8, 2026

These decisions supersede unresolved behavior questions below, while retaining
frozen observations and source references for comparison. They apply to Grand
Sport; duplicate-RPO review is scoped strictly within each individual model.

| Area | Intended behavior / disposition |
|---|---|
| Heritage dependency (§6) | Any heritage hash mark automatically adds Z15 at $995. Center heritage stripes are available only with a selected hash mark. Removing the hash removes its dependent center stripe and the Z15 charge. |
| Z15 presentation (§6) | Proposed UI: a $995 Z15 option card prompts the customer to choose a hash mark, avoiding apparently free hashes. This is a presentation proposal, not a finalized interaction design; preserve a usable entry path and require a hash for the completed package selection. |
| Conditional D84 (§4) | On convertible, selecting a center stripe with a paint in its listed requirement set automatically adds D84 with disclosure. Example: G26, no optional roof treatment, then 20A adds Z15; selecting DMX adds D84 Carbon Flash painted roof and nacelles and alerts the customer. This is a new dataset rule absent from the old form. |
| Center-stripe disclosure (§4) | All center stripes must carry: “When (D84) Carbon Flash painted nacelles and roof is ordered (required or selected) roof will not include the stripe.” |
| EL9 / Z25 pricing (§7) | The $1,995 applies to EL9's Launch Edition content through Z25; seats are separate and additional. AH2 + EL9 costs $1,995 above base; AE4 + EL9 costs $1,995 + $595 = $2,590 above base. Charge once. The old EL9 placement deliberately exposed the cost; an EL9 selection alert explaining that Z25 adds $1,995 can preserve that visibility with Z25 as charge owner. |
| EL9 belt (§7) | EL9 always includes 3F9 at $0 with no belt override. The old alternative-belt behavior is not the target, so the EL9/orange-belt D30 gap is historical evidence rather than a request to enable that pairing. |
| Prerequisite loss (§8) | The retained J57/T0F state after FEB removal is a real bug. Remove them when their required package support is lost; FEY still supplies them when selected. Reconcile dependent equipment and charges as part of the removal. |
| B4Z (§8) | Correct to the guide: included and only available with FEB or FEY, not standard without either package, in all six body/trim contexts. |
| Caliper swaps (§8) | Removing J57 replaces J6D or J6L with J6A. Adding J57 replaces selected J6A with J6D, including explicitly selected J6A. Retain other paid caliper selections when brakes change. |
| Required selections (§§8–9) | Wheels and calipers must never remain empty. If a selected choice becomes unavailable, restore the standard available choice for the resulting configuration. |
| FEY absorption (§§8–10) | FEY absorbs J57, T0F, WUB and CFZ. CFV is an adjacent option that becomes unavailable with FEY; its removal is incompatibility cleanup, not absorption into FEY. |
| Offering corrections (§12) | Remove DUW from Grand Sport; add missing DTC and SAI sill plates. The inspected baseline lacks both identities. Reconcile affected relationships when implementing these corrections. |
| Duplicate RPOs (§12) | Flag every duplicate RPO in a single model's option list for resolution, including dormant entries. The known active/dormant T0E duplication is unresolved. Preserve raw source identities as evidence; they do not justify duplicate catalog options. This is not cross-model deduplication, and repeated guide references are not duplicate option identities. |

## 2. Model, body and trim establish the starting configuration

`model_variants!A2:E7` selects six Grand Sport identities in
`variant_master!A8:H13`; LT labels alone cannot select a model.

| Body | 1LT | 2LT | 3LT |
|---|---:|---:|---:|
| Coupe, `*_e07` | 88,495 | 95,595 | 100,245 |
| Convertible, `*_e67` | 95,495 | 102,595 | 107,245 |

Guide `Price Schedule` rows 15, 18, 19, 17, 20 and 21 respectively have F + J
equal to these amounts. Destination is already represented; adding it again
would double-charge it. All six runtime starting totals equal the workbook.

The baseline supplies FEA touring Magnetic Ride, JX6 low-dust touring brakes,
XFT all-season tires, LS6, M1N and heavy-duty cooling. It does not begin with
FEB or FEY. Sources: `Mechanical 2!C6:I6`, `C19:I19`, `C26:I26`, `C47:I51`,
`Exterior 2!C97:I97`; workbook options rows 129, 172, 177–181 and 202.

**Body:** coupe starts with CF7 roof and BC7 engine cover; convertible starts
with CM9 roof and no selected engine cover. B6P is coupe-only, ZZ3 is
convertible-only. D84/D86 belong to convertible; C2Z/CC3/CF8/SBT to coupe.
Changing body/trim resets selected options and interior: a 3LT coupe with FEY
and EL9 becomes a default 1LT convertible at 95,495, without those purchases.

**Trim:** AQ9 is standard at 1LT/2LT; AH2 at 3LT. UQT costs 1,495 at 1LT but
becomes included display-only equipment at 2LT/3LT. E60 is unavailable at 1LT;
BAZ/FA5 begin at 2LT; 5JR begins at 3LT. The UQT change is an explicit contextual
override, not a second product or a zero base price. Sources: `Interior 2`
rows 53, 65–68, 85, 88; `Exterior 2` rows 18, 39;
`grandSport_variant_overrides!A2:H5`. Both-body UQT attempts confirmed the distinction.

## 3. Interior and paint choices begin here, but add further conditions

The guide has 80 Grand Sport trim/seat/interior-code combinations. Applying its
N26, stitching, TU7 and R6X disclosures produces exactly 132 workbook leaves:
4 at 1LT, 40 at 2LT, 73 ordinary 3LT and 15 custom R6X 3LT choices.
`model_interior_scope` rows 2–133 own this lane's eligibility. EL9 contributes
two of these leaves; it is not inherited from Stingray.

Sources: `Color and Trim 1!A5:Q13` and its A27 footnotes;
`Color and Trim 2!A5:H8` and A22 footnotes; `Interior 2` rows 65–69, 79, 82–84.
The 198 Grand Sport component memberships in `interior_components` were compared
against `PriceRef` and runtime output in both bodies. No leaf or component
membership discrepancy was found. Price interpretation is a separate check (§7).

**Recommended paint combinations are not hard prohibitions.** All 145
guide-derived nonrecommended paint/interior pairs match this lane's
`color_overrides` rows. Across 1,320 runtime paint/interior states, each acquires
D30 exactly where expected. For EL9, G26/G4Z/GBK/GPH trigger the 1,495 charge;
other paints do not. The source is `Color and Trim 1!Q16:Q25`, A27;
workbook `color_overrides` rows 32–35 and 76–79. A selected incompatible stripe,
by contrast, can refuse a paint change (§4), rather than allowing it for D30.

## 4. Convertible roof and accents under paint restrictions

D84 and D86 each cost 1,295 and exclude GBA Black. EDU costs 995 and also
excludes GBA; ZYC costs 295, includes DRG, and excludes GBA. A build with D84
and ZYC refuses a subsequent GBA attempt. EFR/EDU select the accent treatment;
ZYC is a separate mirror/spoiler choice. Sources: `Exterior 2` rows 11–12,
16–17, 58–59; `grandSport_rule_mapping` rows 21, 41–43;
`grandSport_rule_groups` row 29.

### Center stripes introduce an additional conditional roof requirement

Every DM* center stripe requires Z15. On convertible, these additional
paint-dependent D84 requirements appear in `Exterior 2!C70:C74`:

| Center stripe | Paints requiring D84 on convertible | Paints prohibited outright |
|---|---|---|
| DMX Admiral Blue | G26, G4Z, GBK, GKZ, GPH | GTR |
| DMV Blade Silver | G26, G4Z, GBK, GKZ, GPH | GKA |
| DMY Red Mist | G26, G4Z, GBK, GTR | GKZ, GPH |
| DMW Arctic White | G26, G4Z, GBK | G8G |
| DMU Carbon Flash | None specified | None specified |

With D84, the roof does **not** receive the center stripe, whether D84 was required
or voluntarily selected. This is a physical-content consequence, separate from
eligibility and price.

The workbook's direct rules (rows 29–33 and 72–76) implement prohibited paints
and Z15 prerequisites but no paint-conditioned D84 prerequisite. Of 100
body/stripe/paint runtime states examined, all 17 convertible combinations for
which the guide requires D84 accept the stripe without it. For example,
2LT convertible + G26 + 97A + DMX totals 105,880 with CM9 still selected.
Adding D84 raises it to 107,175. The first state reports only missing interior,
not missing roof. This is a guide-to-runtime conflict. Owner review now requires
D84 auto-add with disclosure for these cases; it has not been implemented.

## 5. Engine appearance: body, selected cover and price act together

BC4, BCP and BCS are three distinct LS6 cover choices, each 695 normally and
595 with the applicable B6P/ZZ3 package. They share an exclusive group with BC7.
Sources: `Mechanical 2!C27:I33`; workbook options rows 41–48,
direct rules 3–12 and 93, price rules 10–18 and 21–23,
exclusive members 2–5. `Price Schedule` rows 174–175 separately illustrate
BC4's with/without-package price contexts, subject to the recorded price-basis ambiguity.

**Coupe:** BC4 removes default BC7 and supplies D3V. On 2LT, 95,595 becomes
96,290. Adding B6P (1,895) reduces BC4 to 595, adds SL9 and retains one D3V,
giving 98,085. Removing B6P retains BC4/D3V, removes SL9 and restores BC4 to
695. Removing BC4 restores BC7 and removes D3V. BCP→BCS exchanges covers
without duplicating the lighting charge.

**Convertible:** BC4 is refused until ZZ3 (1,195) is present. ZZ3 supplies
BC7 and SL9. BC4 then replaces the included BC7 for 595, producing 104,385
on 2LT. Removing ZZ3 removes BC4 and SL9. D3V is not supplied on convertible;
its guide/workbook availability is coupe-only. Blank scope on an authored
requirement cannot be interpreted independently of effective availability.

The old BCP/BCS rule descriptions mention a coupe B6P requirement, but the
current guide permits the covers without B6P and the observed coupe behavior
does too. Preserve original text without converting that stale description into
an extra prerequisite. Source text, executable relationships and observed scope
must remain distinguishable.

## 6. Heritage graphics connect hash marks, center stripes and exclusions

The customer selects one of six hash marks, not a standalone Z15 card.
That choice acquires Z15 at 995; the hash row's missing price becomes zero in
the frozen contract. A center stripe is an additional 1,295 purchase requiring
Z15. Thus 2LT coupe + 97A + DMU totals 97,885. Removing 97A removes Z15 and
then DMU, returning to 95,595.

Sources: `Exterior 2` rows 5, 70–80; `grandSport_options` rows 58–68 and 203;
direct rules 72–82; `section_master` rows 5–7. The guide describes Z15 as
including one required hash. The workbook reverses the acquisition path to make
the hash the customer-facing choice. The target must retain a usable acquisition
path without a circular entry gate.
Owner review proposes a priced Z15 card prompting hash selection; the dependency
and removal rules above remain required regardless of presentation.

Z15 permits the DM* center stripes, but excludes the racing/stinger/Jake families.
The workbook contains both the Z15-side group (row 2) and explicit reverse
hash/Z15 exclusions (rows 30–50). Runtime attempts confirmed that DPB after
97A/DMU is refused, and 97A after DPB is refused. The same refusal was observed
between heritage and PDA/SNE/VPO. These member sets belong to Grand Sport.

CF8 illustrates directional behavior: selecting it after 97A/DMU removes DMU
but retains 97A/Z15; selecting DMU after CF8 is refused. This is not a symmetric
pair that always refuses. Source: `Exterior 2!C65`, workbook group row 6.
Selecting GTR after G8G/20A/DMX is refused rather than silently replacing the
paint and removing the graphics.

## 7. Complete interior choices, components and belts

### Launch Edition has a distinct acquisition and charge problem

The guide says Z25 includes EL9, red belts, special quilting, unique floor mats,
embossed headrests and a Launch Edition waterfall plaque; EL9 is only available
with Z25. Sources: `Exterior 2!C4:I4`, `Color and Trim 1!Q13`, A27 footnote 8.

The workbook instead makes Z25 an auto-only option with price zero
(`grandSport_options!A167:L167`). Selecting either `3LT_AH2_EL9` or
`3LT_AE4_EL9` acquires Z25 and 3F9 through direct rules 97–98, 105, 126 and 158.
Both interior records cost 1,995 (`lt_interiors` rows 47 and 80). Their
`model_interior_scope.requires_option_id` becomes `requires_z25=True` in the
contract, but the frozen browser does not read that flag as a selection gate.
The executable interior→Z25 inclusion is what makes the workflow work.

Both seat paths produce a 102,240 3LT coupe total. Itemization differs:

| Selected interior | Frozen interior/seat lines | Z25 line |
|---|---|---:|
| AH2 + EL9 | EL9 1,995; AH2 0 | 0 |
| AE4 + EL9 | EL9 1,400; AE4 595 | 0 |

`interior_components!A847:K847` supplies AE4's 595 component. The browser's
`adjustedInteriorPrice` and `lineItemsFromInterior` subtract the seat from the
stored interior total. A new schema with no editable interior total cannot
simply discard these residual charges. Owner review resolves the seat question:
Z25/EL9 content costs 1,995 and AE4
is an additional 595. With Z25 owning the charge, disclose it when EL9 is
selected. Corrected partial 3LT coupe totals would be 102,240 with AH2 and
102,835 with AE4; these are target calculations, not executed runtime results.
Guide `Price Schedule` row 228 shows 1,995 for Z25; the broader source
option-price column ambiguity remains separate from this owner decision.

Selecting a different ordinary interior removes Z25. An explicitly purchased
alternative belt can remain. Package content such as quilting and mats currently
lives in description text; it is not a separate charge or selectable option.

### Other interior charges and belt relationships

All 130 non-EL9 leaves were checked against seat plus non-seat component amounts.
Four R6X/AE4 cases have the same 595 shortfall observed in Stingray, now verified
independently for Grand Sport: `3LT_R6X_AE4_HU0_38S`, `..._HUU`,
`..._HXO_N26_38S`, and `..._HZP_N26`. For HXO, 595 seat + 995 R6X + 695 N26
+ 495 stitching is 2,780; frozen itemization is 2,185. This is a retained
discrepancy, not a new accepted Grand Sport correction. No package-minimum/delta
pricing mechanism is needed to describe the observed FEB/FEY prices.

In the frozen form, included belts yield to permitted explicit alternatives.
EL9 supplies 3F9 at
zero; 3A9 costs 595 when chosen instead. HAG/HVZ enforce hard exclusions:
the AUP/HAG→AUP/HVZ change swaps automatic blue for red, and red is refused
while HAG is selected. D30 does not bypass those exclusions. Sources:
`Interior 2!C59:C64`, direct rules 104–158, price rules 32–56.

The guide-derived belt recommendation matrix contains 138 charge-triggering
combinations, but the workbook contains 136. **Both EL9 + 379 orange belt cases
are missing D30**, contrary to `Interior 2!C60` footnote 2. Runtime confirms
the 595 belt charge without the additional 1,495. The two EL9 yellow and two
natural combinations do acquire D30 (`color_overrides` rows 439, 442, 500, 509).
All 792 belt attempts reproduce the workbook matrix; 30 prohibited attempts
are refused and every resulting state has exactly one belt line. This verifies
the discrepancy rather than treating workbook parity as manufacturer accuracy.
Owner review supersedes the EL9 alternative-belt path: 3F9 is included at zero
and cannot be overridden. Other interior belt findings remain unchanged.

## 8. Performance connects suspension, brakes, tires and exhaust

Sources: `Mechanical 2` rows 6–8, 12–18, 34–37, 44, 47–49;
`Exterior 2` rows 7, 20–22, 45–46, 97–99. Workbook direct rules 14, 18–20,
60–66 and 94–101; groups 3 and 28; price rules 2–5 and 20.

| Choice | Acquisition and charge | Consequences |
|---|---|---|
| FEB Sport | 3,500 purchase | Supplies J56 and XFR; excludes default JX6 |
| J57 with FEB | Additional 6,000 | Replaces J56; removes J6A; permits carbon wheels and orange calipers |
| T0F with FEB + J57 | Additional 8,995 | Replaces T0E; supplies CFZ at zero |
| FEY Track | 20,695 purchase; replaces FEB | Supplies J57, XFS, WUB, T0F and CFZ; component price overrides prevent duplicate charges |

J57 requires FEB **or** FEY. T0F requires J57 **and** the FEB/FEY alternative.
These are independent ANDed requirements, not one flat ANY list. FEY's included
J57 satisfies T0F's brake requirement through resolved state.

On 2LT coupe: base 95,595 → FEB 99,095 → J57 105,095 → T0F 114,090.
Switching to FEY gives 116,290 and absorbs the earlier J57/T0F purchases.
Switching back to FEB gives 99,095 with J56/XFR and T0E; the absorbed purchases
do not return. An explicit CFV selection is likewise removed by FEY's CFZ
inclusion; CFV/CFL attempts are then refused. Removing FEY does not restore CFV.

**Prerequisite loss is inconsistent by rule family.** Removing FEB while its
separately purchased J57/T0F remain leaves both selected and charged at 110,590,
with CFZ still included. The runtime reports two missing Performance Packages
requirements. This was reproduced in all six configurations after completing
paint/interior; the submit button is disabled, the modal does not open, and
the submit handler makes no request. Direct prerequisites behave differently:
removing J57 removes J6L and carbon wheels that require it (§9).

**Calipers are a soft default, not locked package equipment.**
`default_selection_rules!A6:L6` adds J6D when J57 is present and no competing
customer-selected caliper occupies the section. J6F selected before J57 survives;
J6F chosen after FEY replaces J6D and adds 795. Removing FEY retains paid J6F.
Removing J57/J6D without an alternative can leave Caliper Color missing rather
than restoring J6A. The initial standard default and restoration are distinct.

**B4Z conflicts with the guide.** `Mechanical 2!C44:I44` makes Performance
Traction Management included and only available with FEB/FEY. The workbook
stores B4Z as standard in all six contexts (`grandSport_ovs!A176:C181`), with
no FEB/FEY inclusion edge. It therefore appears in the baseline standard-equipment
view even without either package. Owner review accepts correcting all six
contexts to that guide scope; the frozen differences remain evidence until implementation is verified.

**Exhaust layout and tips:** NWI (395) requires WUB (1,995). NGA is the default
tip; NWI replaces NGA but retains WUB. The WUB row in
`grandSport_exclusive_members!A28:E28` is inactive; only NGA/NWI are active peers.
FEY supplies WUB at zero. If FEY absorbs a purchased WUB, removing FEY removes
WUB and dependent NWI and restores NGA. Inactive membership cannot be silently
reactivated by a schema translation.

## 9. Wheels, aero and package alternatives

All eleven listed Grand Sport wheels are factory choices in one required section:
SWM is the zero starting wheel; SWN/SWO/SWP and ROU/SON/SOM/ROX are alternatives;
ROY/ROZ/STZ require J57. Sources: `Exterior 2!C100:I110`, workbook options
232–242 and direct rules 67–69. Do not import Stingray's LPO wheel purchase path.
Observed R8C remains selected when SWN changes to ROU.

ROY costs 10,995; FEB + J57 + ROY on 2LT totals 116,090. Removing J57 removes
ROY and leaves Wheels missing, rather than restoring SWM. S47/SFE chrome
hardware excludes carbon wheels; an S47→ROZ attempt is refused. SPZ requires
SPY; SPY and S47 conflict. Sources: `Exterior 2` rows 54–57; direct rules 83–92.
These are compatibility facts about complete wheel/hardware choices, not prices
to fold into a shared wheel record.

5ZV (2,075) replaces T0E and causes dependent SIG (425) to disappear. With 5ZV
selected, FEY is refused. FEY/T0F supply a different high-wing system with CFZ;
5ZV is not an equivalent package member. The three aero choices are a required
exclusive group, with T0E's explicit restoration rule. WKR's physical cover
version depends on 5ZV or T0F (`Exterior 2!C31`); the form sells one WKR choice.

## 10. Stripes, ground effects and remaining accessories

PDA costs 950 and supplies SNE/VPW at zero. Purchasing SNE first, then PDA,
then removing PDA removes both graphics; SNE does not reappear as a purchase.
However, standalone VPW followed by DPB is permitted and both remain charged.
The guide explicitly prohibits that pairing (`Exterior 2!C47`), whereas workbook
group row 11 lists only SHT/VPO for VPW. VPO likewise lacks the guide's complete
racing/stinger exclusions (guide C48, workbook group row 10). The VPO row-set
gap is source inspection; the executed counterexample is VPW + DPB.

| Accessory path | Workbook charge and observed ownership | Sources |
|---|---|---|
| PCQ grille screens | 1,675; supplies VWE/VWT at zero; absorbs a prior VWE purchase | `Exterior 2` rows 28, 37–38; direct rules 22–23; prices 6–7 |
| PEF liners | 475; supplies RIA/CAV; prior CAV does not return after package removal | `Interior 2` rows 26, 30–31; direct rules 27–28; prices 8–9 |
| PDY safety | 195; supplies RYT/S08; absorbs prior RYT | `Interior 2` rows 27, 32, 37; direct rules 24–25; prices 28–29 |
| SBT second roof | 2,525; supplies SC7 and describes an additional transparent roof; blocks CC3 | `Exterior 2` row 41; direct rules 26, 70; price 19 |
| Caps, indoor covers, script badges, suede liners | Each family selects a peer; the observed 5ZD→5ZB, RWH→WKR, RIK→SL8 and SXB→SXR transitions exchange products/prices | `grandSport_exclusive_groups` rows 3–6 and members 6–16 |

EFR/EDU physical surfaces change with CFV/CFZ; EDU's front splitter is no longer
body-color with either ground-effects package. These guide disclosures
(`Exterior 2!C16:C17`) need contextual content rather than extra price records.
CFL/CFZ/CFV are exclusive choices (`grandSport_exclusive_members` rows 17–19).
Independent accessories such as ERI, VUP, SLK and luggage retain their own rows;
matching another model's name does not establish a common owner.

## 11. Order restrictions, standard equipment and consumer boundaries

R8C supplies CFX, excludes BV4 and carries SOLD-order, acknowledgement and
ship-to-BAC requirements (`Exterior 2!C13`, `Interior 2!C54:C55`). PIN has its
own approval/SOLD restrictions. D30 and R6X also have SOLD-only disclosures.
The probes cover product selection, not dealer eligibility or fulfillment approval.

The guide's VK3 forced ship-to-state bracket (`Exterior 2!C26`) has no Grand Sport
option row. Nor do emissions codes FE9/YF5/NE1/NB8/NB9/NC7 in `Mechanical 2`
rows 20–25. OnStar/service/SiriusXM codes U2K, R6P, R9Y/R9V/R9W, UE1, VV4,
U5G, R9L and PRB are also absent as option identities (`Interior 2` rows 10–11,
44–52). The uncoded OnStar Basics row 50 has no mapped equipment record either.
These are scope/coverage omissions, not evidence of manufacturer removal.
The form does not enforce those ordering contexts through its body/trim controls.

`standardEquipmentRows()` filters a static configuration view. It does not
reconcile installed equipment after package selection. JX6/J56/J57, XFT/XFR/XFS,
FEA/FEB/FEY and B4Z therefore need an explicit installed-equipment interpretation
before a new consumer claims to describe the finished vehicle.

The guide currently says SLN and R88 are unavailable, and CF8 is unavailable
at start of production. The workbook keeps them active; the 2LT coupe probe
could purchase all three. RZ9 and V8X are inactive. Preserve these lifecycle
differences for review (`Mechanical 2!C39`, `Exterior 2!C34:C36`, C65,
`Interior 2!C41`). An availability marker alone does not override the footnote.

## 12. Coverage, unresolved facts and implications for the schema proposal

### Coverage and source dispositions

All 241 workbook offerings were accounted for: 204 matched primary-guide coded
offerings, 25 mapped uncoded equipment rows, 10 paint rows from the color charts,
one dormant duplicate T0E identity and legacy DUW. The 1,374 compared status
pairs contain 1,368 matches and the six B4Z differences. All 233 repeated coded
guide occurrences in the two equipment sheets agree with their primary-guide
text/status; this does not independently approve workbook rules or prices.

The 25 uncoded mappings, expressed as workbook option row → guide sheet/row,
are: Interior 2: 26→86, 153→90, 182→6, 183→16, 184→17, 185→18, 186→19,
187→21, 188→23, 189→25, 190→58, 191→81, 192→94, 193→97, 194→98;
Mechanical 2: 154→4, 155→11, 156→50, 197→38, 198→43, 199→46;
Exterior 2: 195→15, 196→19, 200→111, 224→6.

TU7, N26 and 36S/37S/38S are accounted for as interior components, not missing
option cards. SAI (`Interior 2!C40:I40`) and DTC (`Exterior 2!C83:I83`) have no
workbook option identity. DUW remains in workbook row 207 and rule sets; the
guide has no primary DUW offering but still mentions it in some exclusions.
DUE's workbook name says Santorini Blue; the current guide calls it Royal Blue
(`Exterior 2!C81`). Owner review now independently directs removing DUW and adding
DTC/SAI in Grand Sport. This is model-specific authority, not inheritance from Stingray.
The dormant T0E duplicate is flagged for resolution under the within-model
duplicate-RPO rule; source identity preservation does not permit duplicate
options in the corrected catalog.

Validation executed: 44 connected sequences / 199 captured states; 264
interior/body contexts; 1,320 paint/interior states; 792 belt attempts; 100
stripe/body/paint states; and six completed-context package-removal checks of
button, modal and submit-handler guards. The frozen workbook, guide, browser
bytes and reference repository were not modified. The report has family coverage,
not exhaustive combination/direction acceptance, visual QA, full option-price
reconciliation, or dealer-order validation. Unexecuted reverse interactions and
the detailed release/visualizer contract remain implementation obligations.

### What fits, what is missing, and what needs a decision

| Grand Sport requirement | Assessment of the Stingray proposal | Next design/review obligation |
|---|---|---|
| Model/body/trim identity; active and dormant T0E records | Fits model-owned options, explicit configuration membership and lifecycle | Preserve both raw source identities as evidence; flag and resolve the duplicate T0E catalog option within Grand Sport |
| T0F requires J57 AND (FEB OR FEY) | Fits multiple `requirement` rows with ANY members | Remove unsupported J57/T0F after package loss; retain FEY-supplied inclusions through resolved-state evaluation |
| Stripe + paint requires D84 on convertible | **Missing explicit condition ownership** in the proposed requirement family | Add a bounded typed option-condition capability after cross-model review; enumerate the exact paint sets. Do not misuse interior-only `combination_addition` or duplicate configurations by paint |
| D84 removes the stripe from the physical roof | Fits configuration-qualified `content_effect` with an option guard | Preserve the difference between what is purchasable and which surfaces receive it |
| Hash acquires Z15; center stripe requires Z15 | Fits option inclusion, requirement, choice-group and separate price owner | Decide explicit zero/included semantics for blank hash prices; avoid circular entry requirements |
| EL9 acquires Z25 and shares an included belt cause | Fits interior-source inclusion; owner resolves 1,995 content plus separate 595 AE4 | Use one charge owner with visible EL9-triggered Z25 disclosure; preserve the old 1,400/595 split as discrepancy evidence, not target pricing; lock included 3F9 at zero |
| Z25-only interior metadata | Requires a precise translation, not a blind flag-to-requirement mapping | Preserve EL9-first entry with automatic Z25 acquisition and disclosed charge |
| J6D trigger default honors explicit alternatives | Proposed default kind is relevant, but “section occupied” is insufficiently precise | Replace J6A with J6D when adding J57; replace J6D/J6L with J6A when removing J57; retain other paid choices |
| Wheels/calipers can remain empty after dependency loss | Initial default versus restoration needs an explicit contract | Restore the standard available wheel/caliper after availability loss; empty sections are not the accepted target |
| FEB/FEY locked inclusions and absorbed purchases | Fits inclusion acquisition and peer policies | Verify FEY absorbs J57/T0F/WUB/CFZ; CFV becomes unavailable and is removed as a conflict, not absorbed |
| B4Z, orange/EL9 D30, VPW/VPO stripe gaps | Structures can represent these facts; data differs | Correct B4Z to guide scope; EL9 belt locking supersedes orange-belt repair; VPW/VPO remain unresolved. Keep corrections distinct from parity |
| Static versus installed equipment | Fits proposed equipment substitutions/content, after facts are resolved | Define brake/tire/suspension replacements and implement the reviewed B4Z package scope before claiming a finished-build view |
| Ship-to/order/dealer/lifecycle restrictions | Current body/trim scope is insufficient for full dealer-order validation | Decide consumer scope before adding ordering-context fields; retain disclosures and omissions meanwhile |

These findings justify keeping DDL paused. They do not authorize a new rule
language, six independent schemas, or cross-model consolidation. Review this
Grand Sport lane, then continue in the owner's order: **Grand Sport X, Z06,
ZR1, ZR1X**. Revise one coherent proposal after the remaining model challenges
are laid out. This task stops at Grand Sport.
