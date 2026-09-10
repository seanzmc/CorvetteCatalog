# Grand Sport X behavior: foundations and connected choices

September 10, 2026. **Complete family relationship analysis for review.** This
extends the initial PR #22 foundation slice through interiors, graphics, roofs,
performance, wheels, accessories, equipment and order output. It follows the
same lane structure as [Stingray](stingray-behavior.md) and
[Grand Sport](grand-sport-behavior.md): foundations, connected choices and charges,
guide → workbook → observed behavior, source differences and coverage.
“Complete” means every family and workbook offering has been analyzed; it does
not mean every possible configuration is tested or every discrepancy accepted.
The full structured handoff is deliberately deferred to the next pass.

Grand Sport X is not Grand Sport with a price change. J57 carbon-ceramic brakes
and B4Z are standard; FED supplies performance tires rather than the FEB/FEY
brake/aero chain. DTC is already present and DUW absent, but DTC has a heritage
relationship gap. EL9 is selectable without emitting Z25. Those differences
must survive review instead of being overwritten by the other model's analysis.

## 1. Sources and how to read this analysis

**Guide:** unchanged `2027 Chevrolet Car Corvette Export (6).xlsx`, SHA-256
`d3ca7d3a09c9fb89210b4ce584493b3ad8fb65ca35087c49d816d1cbf1a333d1`.
Grand Sport X is explicitly named in `Interior 3`, `Exterior 3`, `Mechanical 3`,
`Standard Equipment 3` and `Equipment Groups 3`. D–F are coupe 1LT/2LT/3LT;
G–I are convertible 1LT/2LT/3LT. Shared Color and Trim charts are narrowed using
this model's LT seat/component eligibility. See [source provenance](../sources/README.md).

**Workbook:** [frozen baseline](../baselines/2026-09-06/README.md), SHA-256
`3127e663b1531e366ce86b989b6190914108d40dfd15a33a258307a05d608e3c`.
`model_workbook_sources` rows 13–23 route this model to `grand_sport_x_*` sheets
and `lt_interiors`. Its color conditions are in `grand_sport_x_color_overrides`,
not the other models' color-override sheet. Model-owned interior components and
membership are selected by `model_key=grand_sport_x`.

**Observed:** actual frozen `form-app/app.js` and `data.js` selection functions
from `4fe92a4f078370c478f18484cad31bdafe58ad43`, exercised with a DOM-stub harness.
The asserted registry key is `grand_sport_x`, not `grandSport`. These are local
runtime observations, not a new evaluator, visual browser QA or live orders.
All probes made zero requests. The [initial foundation records](grand-sport-x-foundations-records.json)
remain unchanged historical evidence for that earlier slice; they are not the
complete structured handoff or the complete evidence for this expanded analysis.

PR #21 closed the 12 Stingray and 16 Grand Sport decision records. Their accepted
corrections are not automatically Grand Sport X data corrections. Previously
accepted universal application policies, such as dependency cleanup with an
alert/revert opportunity, remain design guidance; the model-specific facts below
still require review. No schema, canonical-data or runtime changes are made here.

Amounts below use the frozen workbook's numeric basis. Guide column E option
amounts are compared as evidence, with their column D qualifiers; they are not
silently adopted as a new tariff. PR #21 explicitly confirmed USD for Stingray
and Grand Sport, not this lane. Currency and final price-basis acceptance for
Grand Sport X remain separate from numeric agreement.

## 2. Model, body and trim establish the starting configuration

`model_variants` rows 8–13 join `variant_master` rows 14–19. Model membership must
precede trim matching: LT labels alone identify neither a model nor a price.

| Body | 1LT | 2LT | 3LT |
|---|---:|---:|---:|
| Coupe, `*_g07` | 112,195 | 117,695 | 122,845 |
| Convertible, `*_g67` | 119,195 | 124,695 | 129,845 |

Guide `Price Schedule` rows 22/23/26 and 24/27/29 respectively have F + J equal
to these amounts. Destination is 2,495 and already counted once. All six frozen
runtime starting totals agree. Initial Paint and Interior Color are unset.

**Body:** coupe starts with CF7 roof and BC7 engine cover; convertible starts
with CM9 and no selected cover. B6P, roof panels and SBT are coupe-only; ZZ3,
D84 and D86 are convertible-only. Changing a 3LT coupe with FED and EL9 to a
1LT convertible resets those purchases and the interior, returning to 119,195.
Sources: guide `Exterior 3` rows 9–11, 39, 59–62; `Mechanical 3` rows 24–30;
workbook default rows 24–26 and configuration-scoped availability.

**Trim:** AQ9 starts at 1LT/2LT; AH2 at 3LT. UQT is a 1,495 purchase at 1LT
but included/display-only at 2LT/3LT. Both-body probes confirmed that distinction;
`grand_sport_x_variant_overrides` rows 2–5 own its presentation change. E60,
BAZ and FA5 begin at 2LT; 5JR begins at 3LT. W2D is a 1LT accessory while AP9
is supplied at 2LT/3LT. Sources: `Interior 3` rows 12, 28, 53, 65–68, 85, 88;
`Exterior 3` rows 17, 37.

Do not inherit Grand Sport's trim equipment assumptions: UV6 head-up display and
DRZ rear camera mirror are standard even at Grand Sport X 1LT (`Interior 3`
rows 22/43). UQS versus UQH, K7A versus K7B, and DWK versus DYX still change
with trim. All their six-context statuses were reconciled independently.

## 3. Interior and paint choices begin here, but add further conditions

The guide's 80 trim/seat/interior-code combinations expand to exactly 132
workbook leaves: four 1LT, 40 2LT, 73 ordinary 3LT and 15 custom R6X 3LT.
This includes the two EL9 leaves; it is not copied eligibility from another model.
All 198 model-owned component memberships were checked against the runtime's
component rates in 264 body/interior contexts.

Sources: `Color and Trim 1!A5:Q13` and A27 footnotes; `Color and Trim 2!A5:H8`
and A22 footnotes; `Interior 3` rows 65–69, 79, 82–84. N26 follows the suede
requirements. TU7 is restricted to AH2 and mandatory for its HU7/HUA/HXO paths.
HU0/HXO require 38S. Optional 36S/37S/38S stitching stays within the chart's
listed black-interior codes. AUP remains confined to HAG/HVZ at 3LT.

The 145 guide-derived paint/interior surcharge pairs exactly match this model's
color-override rows. All 1,320 paint/interior states reproduce that D30 behavior.
A recommended-chart `--` is interpreted with its D30 disclosure, not as an
unconditional prohibition. Hard HAG/HVZ belt exclusions remain separate (§7).

D30 is one 1,495 charge even with multiple causes. In a 1LT coupe with HUQ,
G26 and orange belt produce 115,280. Changing to G8G leaves the belt cause and
114,285; changing the belt to 3F9 removes D30 and leaves 112,790. The paint and
belt prices themselves remain separate. Do not duplicate D30 by trigger count.

Seat changes clear invalid interiors. Coupe 2LT AH2/HU7/N26/TU7 totals 120,680.
Changing to AE4 clears that leaf and flags Interior Color; choosing AE4/HU7/N26
gives 120,485, with no TU7. Missing-interior submission was independently
rejected by the button and handler, with zero requests. Shared leaf labels do
not make the two component memberships interchangeable.

## 4. Roof, paint and exterior surfaces have connected consequences

D84 and D86 each cost 1,295 and conflict with GBA; EDU costs 995 and also
conflicts with GBA. ZYC costs 295 and has its own GBA conflict. A convertible
G8G → D84 → ZYC → attempted GBA sequence keeps the valid prior paint and total
126,285. The refusal is not automatic paint replacement or a D30 override.
Sources: `Exterior 3` rows 10–11, 16, 55; direct rules 17–18, 48, 79–80.

The guide requires D84 for certain convertible center-stripe/paint pairs:

| Center stripe | Paints requiring D84 on convertible | Additional paint exclusions |
|---|---|---|
| DMX Admiral Blue | G26, G4Z, GBK, GKZ, GPH | GTR |
| DMV Blade Silver | G26, G4Z, GBK, GKZ, GPH | GKA |
| DMY Red Mist | G26, G4Z, GBK, GTR | GKZ, GPH |
| DMW Arctic White | G26, G4Z, GBK | G8G |
| DMU Carbon Flash | None stated | None stated |

Sources: `Exterior 3!C67:I71`. Across 100 body/stripe/paint states, all 17
convertible cases requiring D84 allow the stripe without D84 and report no
missing roof. The workbook has paint exclusions and Z15 prerequisites, but no
stripe-plus-paint D84 prerequisite. Convertible 2LT G26 + 97A + DMX totals
127,980; manually adding D84 gives 129,275. Selecting CM9 afterward removes
D84 and its charge but retains DMX, returning to the same guide-invalid state.

All five center stripes disclose that D84 means the roof will not carry the
stripe, whether D84 was required or selected. That physical-content rule is
separate from eligibility and acquisition. Grand Sport X needs its own accepted
D84 target, preserving explicit versus dependency-added ownership and the
already reviewed application-level cleanup/revert interaction.

CF8 is a 3,500 coupe 2LT/3LT roof, but the guide says unavailable at production
start. The frozen form permits it (§11). CF8 after 97A/DMU removes DMU and
retains the hash/Z15; DMU after CF8 is refused. The complete full-length and
center-stripe set is present in `grand_sport_x_rule_groups` row 44 and its
members, including DTC and no nonexistent DUW identity. There is no justified
blanket rule that every conflict direction behaves identically.

EFR supplies Carbon Flash accents; EDU changes side vents/front splitter to
body color. CFV/CFZ change which splitter/rocker surfaces retain those finishes.
Convertible tonneau-grille wording is body-specific. Sources: `Exterior 3`
rows 15–16, 19–21. These are contextual content effects, not extra purchasable
RPOs. Artwork/visualizer binding remains outside this behavior analysis.

## 5. Engine covers and appearance packages have multiple charge causes

Sources: `Mechanical 3` rows 24–30, 38; options 40–47; direct rules 8–15,
51, 81–83, 90; price rules 4–11 and 23–26.

| Context | Acquisition and charge | Included content / removal |
|---|---|---|
| Coupe BC4/BCP/BCS alone | 695; no B6P prerequisite | D3V included at zero; replaces BC7 |
| Coupe B6P with colored cover | B6P 1,895 + cover 595 | D3V and SL9 at zero; cover's standalone price reduced by 100 |
| Convertible colored cover | Requires ZZ3 1,195; cover 595 | ZZ3 supplies BC7 and SL9; colored cover replaces BC7; D3V unavailable |

Guide `Price Schedule` rows 173–179 explicitly distinguish 595 with B6P/ZZ3
from 695 for a coupe without B6P. Coupe 2LT BC4 → B6P → remove B6P gives
118,390 → 120,185 → 118,390. D3V remains supported by BC4 after B6P loss;
SL9 disappears. Removing BC4 restores BC7 and the 117,695 base. Switching
BCP→BCS exchanges covers rather than stacking their prices.

A separate D3V purchase at 195 is absorbed when B6P is acquired. Removing B6P
then removes D3V; the old purchase does not return. This differs from the
previous sequence, where a still-selected colored cover remains a valid cause.

Convertible 2LT BC4 alone is refused. ZZ3 → BC4 → remove ZZ3 gives
125,890 → 126,485 → 124,695; the unsupported cover, BC7 and SL9 disappear.
No D3V is emitted in this body. The unqualified workbook cover→ZZ3 rules are
not coupe requirements at runtime: `ruleAppliesToCurrentVariant()` suppresses
them when the prerequisite option is unavailable in the current body.
An explicit future scope must preserve the effective behavior, not copy blanks
as all-body requirements.

There is also a misleading equipment edge: ZZ3→LS6 (row 82) and LS6→D3V
(row 51). The guide describes an LS6 **cover**, not package acquisition of the
standard engine. Runtime emits LS6 under ZZ3, but availability filtering prevents
D3V on convertible; the engine is standard even without ZZ3. Reconcile that
relationship as source-data debt, not a new engine price or blanket inclusion.

## 6. Heritage graphics connect hashes, center stripes and exclusions

The frozen acquisition path is hash-first: one of 17A/20A/55A/75A/97A/DX4
adds Z15 at 995, and a center stripe adds 1,295. Z15 is an auto-only identity
in the ordinary Stripes section, while hash and center choices occupy separate
sections. Hash rows have null workbook prices, converted to zero in the frozen
contract; that conversion is evidence, not a general null-means-free policy.
Sources: `Exterior 3` rows 5, 67–77; options 57–67/198; direct rules 19–28,
84–89; `section_master` rows 5–7.

Coupe 2LT 97A → DMU → remove 97A gives 118,690 → 119,985 → 117,695.
Removing the hash removes Z15, then the unsupported center stripe. DMU alone
is refused. The guide describes Z15 as requiring a hash; translating that as
an entry gate on both sides would make the hash-first path unusable.

**DTC has an independently reproduced gap.** It already exists at option row
197 with a GTR exclusion (direct rule 38); DUW is absent. But DTC lacks the
hash/Z15 exclusion group carried by the other racing stripes. The Z15 source
itself has no complete exclusion group. The runtime suppresses an automatically
included option when another explicit choice occupies its single-choice section
(`shouldSuppressIncludedDefault()`). DTC therefore suppresses Z15 without
removing the selected hash.

| Coupe 2LT sequence | Frozen result |
|---|---|
| 97A → DMU → DTC | 97A and DTC remain; Z15 and DMU disappear; total 118,990 |
| DTC → 97A | DTC and 97A remain; Z15 never appears; total stays 118,990 |
| Remove DTC from that state | Hash reacquires Z15 and 995; total 118,690; DMU can be selected again |

Both defective directions were reproduced after filling paint/interior across
all six configurations: 12 completed builds, no missing-required message and
an enabled submit button. The local compact order omits Z15. This is a real
invalid selection/output defect, not a missing-card cosmetic issue. No valid
submission handler was invoked and no order was sent.

Other groups are directional too. PDA selected after a hash replaces it and
supplies SNE/VPW; a hash attempted after PDA is refused. CF8 and SFZ can remove
an existing center stripe while preserving the hash/Z15; reverse center-stripe
attempts are refused. Paint conflicts refuse the new paint. The accepted global
conflict-offer policy should govern a future implementation; these observations
must remain labeled as the old behavior, not approved target interactions.

## 7. Complete interior choices, component charges and belts

### Launch Edition loses an order code, not just a price component

Guide `Exterior 3!C4:I4` and `Color and Trim 1!Q13`/A27 footnote 8 connect
Z25, EL9, 3F9, special quilting, mats, headrests and the Launch Edition plaque.
The price schedule identifies Grand Sport/Grand Sport X 3LT Z25 at 1,995
(row 228). Workbook Z25 row 156 is nonselectable, auto-only and priced zero.
Both EL9 leaves store 1,995 in `lt_interiors` rows 47/80.

Unlike Grand Sport, Grand Sport X has **no EL9→Z25 inclusion** among its 144
direct relationships. `model_interior_scope` rows 619/652 carry the Z25
requirement metadata, but the frozen browser does not evaluate `requires_z25`
as an interior prerequisite. It sees only the direct interior→3F9 belt edges.

Both AH2 and AE4 EL9 paths produce a coupe 3LT total of 124,840:

| Selected interior | Frozen itemization | Z25 output |
|---|---|---|
| AH2 + EL9 | EL9 residual 1,995; seat zero; 3F9 zero | Absent |
| AE4 + EL9 | EL9 residual 1,400; AE4 595; 3F9 zero | Absent |

Four completed EL9 builds (two seats × two bodies) have no missing requirement,
an enabled submit button and no Z25 in compact output. The numerical charge
does not prove correct package acquisition. If the 1,995 content plus separate
AE4 595 interpretation is accepted for this lane, the AE4 coupe total would
be 125,435, but that is a proposed correction, not an observed result or an
already accepted Grand Sport X tariff. One visible package-charge owner is needed;
do not erase the residual 1,400/1,995 evidence or charge the package twice.

Changing EL9 to an ordinary interior removes its residual content charge and
included belt cause. Explicit alternatives can survive. EL9 permits orange or
blue belts in this baseline; it does not implement Grand Sport's accepted red-belt
lock. This lane's package acquisition, seat increment and belt policy need review
together, rather than a one-line Z25 flag fix.

### Four R6X/AE4 leaves undercharge against their own components

All 130 non-EL9 leaves were compared against the model's seat and non-seat
components. Four have a 595 shortfall; the remaining 126 match.

| 3LT AE4 custom leaf | Component subtotal | Frozen subtotal |
|---|---:|---:|
| `3LT_R6X_AE4_HU0_38S` | 2,085 | 1,490 |
| `3LT_R6X_AE4_HUU` | 1,590 | 995 |
| `3LT_R6X_AE4_HXO_N26_38S` | 2,780 | 2,185 |
| `3LT_R6X_AE4_HZP_N26` | 2,285 | 1,690 |

For HXO, 595 seat + 995 R6X + 695 N26 + 495 stitching = 2,780. The frozen
coupe 3LT total is 125,030 rather than the component-derived 125,625.
`adjustedInteriorPrice()` and the interior/seat itemization path retain the stored
composite-price problem. This is independently verified Grand Sport X evidence;
no prices were changed to match another lane's accepted correction.

### Belt inclusions, hard exclusions and D30 must stay separate

`Interior 3!C59:C64` specifies the included colors, recommendations and hard
HAG/HVZ exclusions. The guide yields 138 belt surcharge pairs, but the workbook
has 136: both EL9/orange combinations omit D30. The 792 attempted belt choices
reproduce the workbook conditions; 30 HAG/HVZ attempts are refused and every
result has exactly one belt line. All other expected surcharge pairs agree.

An included belt normally yields to a permitted paid alternative. EL9 blue costs
595; orange also costs 595 but incorrectly omits the extra 1,495 described by
the guide recommendation. HAG only accepts blue and HVZ only red; D30 cannot
bypass those hard conflicts. AUP/HAG→AUP/HVZ replaces automatic blue with red
while retaining the 350 seat charge. Included-belt zero rates are explicit
interior-context overrides (price rows 28–51), with a separate Z25→3F9 zero
rate at row 52; that latter rate does not itself acquire Z25.

BAZ and FA5 remain independent optional interior trim at 2LT/3LT, 695 and 1,795.
Both can coexist; removing BAZ retains FA5. HUB/HUC change leather-wrapped
surface descriptions to suede (`Interior 3!C86`); IWE is standard 3LT upper
trim. These physical surfaces are distinct from the N26/stitch/TU7 components.

## 8. Performance connects standard brakes, tires, calipers and exhaust

Guide `Mechanical 3` establishes J57/J6D at rows 6/10, LS6/HP1 at 22/23,
B4Z at 41, FE5 at 44 and MLG at 47 as standard across all six configurations.
FED at row 45 is available and includes XFR; `Exterior 3!C95:I95` says XFR
is included and only available with FED. There is no FEB/FEY or T0F offering.
Grand Sport's package-only B4Z correction would be wrong here.

FED costs 500 (`grand_sport_x_options` row 129); its row-49 inclusion supplies
XFR, a nonselectable row with null standalone price. All six initial → FED →
remove FED sequences restore the starting total, remove automatic XFR and retain
J57/J6D. A separate coupe 2LT sequence FED → paid J6F → ROY → remove FED gives
118,195 → 118,990 → 129,985 → 129,485. Paid calipers and wheels remain, as
neither depends on the tire package.

J57 is the required standard brake choice. Clicking it does not remove the
vehicle's brakes. J6D is supplied at zero; a permitted J6F/J6L alternative costs
795 and suppresses J6D. Choosing J6D again returns to zero. No Grand Sport
J6A/J56/JX6 fallback should be invented for this lane. The direct J57→J6D
inclusion and default row 25 coexist; actual itemization contains one caliper.

NWI (395) requires WUB (1,995). Coupe 2LT NWI alone is refused; WUB→NWI gives
119,690→120,085, replacing NGA. Removing WUB removes NWI and restores NGA,
returning to 117,695. Required exhaust-tip membership contains NGA/NWI, not WUB
(`grand_sport_x_exclusive_members` rows 25–26). Package acquisition, section
occupancy and default restoration are different facts.

**Powertrain wording remains unresolved evidence:** `Mechanical 3!C23` attributes
1,250 combined hp to LS6 (Grand Sport X) or LT7 (ZR1X); option row 165 repeats
it. The agreement is not independent confirmation of that horsepower claim.
The guide and workbook originals stay intact; a corrected model-specific number
requires corroboration rather than inference from another model's copy.

## 9. Wheels, aero, ground effects and contextual content

All eleven wheel choices in `Exterior 3` rows 96–106 are factory choices;
workbook options 230–240 keep them in one required section. SWM starts at zero.
SWN/SWO/SWP and ROU/SON/SOM/ROX are alternatives. ROY/ROZ/STZ are available
without an additional brake-package purchase because J57 is already standard.
R8C remains selected when SWN changes to ROU; do not import Stingray's accessory
wheel ownership or a Grand Sport FEB requirement.

The three carbon prices reconcile with explicit model discounts in the guide:

| Wheel | Guide Price Schedule column E calculation | Frozen price |
|---|---|---:|
| ROY | row 279: 11,995 + row 278: −1,000 | 10,995 |
| ROZ | row 281: 13,995 + row 280: −2,000 | 11,995 |
| STZ | row 292: 15,500 + row 291: −3,005 | 12,495 |

Column D limits those discounts to Grand Sport and Grand Sport X. Comparing
only the positive rate would falsely report a pricing defect. Preserve the
price basis and discount provenance; this does not authorize a new pricing engine.

Chrome S47/SFE conflict with carbon wheels; both tested order directions refuse
the conflicting addition. SPZ requires SPY, and removing SPY removes SPZ.
SPY conflicts with S47 and SFE. Sources: `Exterior 3` rows 51–54; direct rules
65–68, 71–74, 76–77. A refusal can misleadingly name the candidate itself
(“Blocked by S47” when attempting S47 after ROY); retain that copy defect as
an implementation issue, not an unexplained business rule.

5ZV costs 2,075 and replaces default T0E in the required Aero Packages section.
SIG (425) requires T0E and disappears when 5ZV replaces it. Clicking 5ZV again
does not empty this required section; selecting T0E restores the standard spoiler
without reviving SIG. With WKR selected, the observed coupe 2LT sequence
WKR→SIG→5ZV→T0E totals 118,970→119,395→121,045→118,970.
Sources: `Exterior 3` rows 29, 43–44, 66; direct rule 75; `section_master` row 33.

WKR's guide disclosure supplies the high-wing cover version with 5ZV. It remains
one 1,275 choice, not a second SKU/charge; the relationship describes delivered
content. CFL/CFZ/CFV are mutually exclusive ground-effects choices at
995/3,495/4,495. Their changes preserve EDU but alter physical splitter finishes
(§4); FED is independent. 5JR and ZYC can both supply DRG: removing either alone
retains DRG, removing the last cause removes it, while both paid source charges
are retained when selected together.

## 10. Graphics and remaining accessory families

PDA at 950 supplies SNE/VPW at zero. SNE purchased first is absorbed by PDA;
removing PDA removes the included graphics and does not restore the purchase.
Groups 40–43 contain the PDA/SNE/SHT stripe constraints, including DTC and the
stinger codes. PDA→DZX was refused. This lane has explicit additional group
coverage absent from some earlier model evidence.

**Rear-graphic exclusions remain incomplete.** VPW→DPB and DPB→VPW both leave
the 575 rear graphic and 1,295 racing stripe selected, total 119,565 on coupe
2LT. VPO→DTC likewise permits both. `Exterior 3!C45:C46` expressly excludes
those stripe families; workbook groups 35–38 omit their complete stripe sets.
SNE/PDA restrictions do not make a standalone VPW safe by transitivity.

SFZ at 250 has the full active badge/full-length/center-stripe set in group 39.
It refuses a center stripe when already selected; acquired afterward, it removes
the center but retains the hash/Z15. DUE's name still says Santorini Blue/Carbon
Flash in option row 210; guide `Exterior 3!C78` says Royal Blue/Carbon Flash.
That naming difference is distinct from DTC identity and from the stale DUW
mentions retained in guide disclosures.

| Family | Charge and connected behavior | Guide / workbook anchor |
|---|---|---|
| PCQ grille screens | 1,675; VWE/VWT included zero; absorbs purchased VWE; neither returns after removal | Exterior 3 rows 27, 35–36; direct 53–54; price 14–15 |
| PEF liners | 475; CAV/RIA included zero; absorbed CAV does not return | Interior 3 rows 26, 30–31; direct 59–60; price 20–21 |
| PDY roadside safety | 195; RYT/S08 included zero; absorbed RYT does not return | Interior 3 rows 27, 32, 37; direct 57–58; price 18–19 |
| SBT second roof | 2,525; extra transparent roof and SC7 pouch; retains factory roof; CC3 conflict refuses both tested orders | Exterior 3 row 39; Interior 3 row 39; direct 69–70; price 22 |
| Wheel caps | 5ZD/5ZC/5ZB each 250; one optional peer, not an added wheel | Exterior 3 rows 49–50; Price Schedule row 96 for 5ZB; exclusive members 27–29 |
| Indoor covers | RWH 495 versus WKR 1,275; optional peers; RWJ outdoor cover has its own row | Exterior 3 rows 28–30; exclusive members 9–10 |
| Script badges | RIK/RIN/SL8 are peers at 395/440/495 | Exterior 3 rows 40–42; exclusive members 14–16 |
| Suede luggage-area liners | SXB/SXR/SXT are peers at 2,095/2,095/2,695 | Interior 3 rows 34–36; exclusive members 6–8 |
| Independent accessories | ERI, VUP, SLK, RWU, S2L retain separate charges; removing ERI preserves the others | Mechanical 3 rows 5, 37, 39; Interior 3 rows 29, 38 |

VYW mats, SDA recovery hook, VTB protector, W2D nets and PIN remain individual
context-qualified offerings with no additional workbook relationship chain.
Their primary-guide status pairs and numeric source amounts are accounted for;
no undocumented package membership is inferred. Included equipment like AP9
must not become a second purchased W2D merely because both descriptions say nets.

## 11. Lifecycle, ordering scope and equipment/output boundaries

**Lifecycle:** SLN is unavailable according to `Mechanical 3!C36` but is active
and purchasable at 2,895 in the frozen form. CF8 is likewise purchasable despite
its production-start notice (`Exterior 3!C62`). R88, RZ9 and V8X are already
inactive and absent from active choices, consistent with their notices at
`Exterior 3!C32/C34` and `Interior 3!C41`. A future visible-unavailable-card
policy must preserve those eligibility restrictions. R88's dormant edges do
not encode its full stripe disclosure; a future release needs that reconciliation
before activation. Inactive is not proof of permanently removed equipment.

**Order context:** R8C supplies CFX, conflicts with BV4, and carries SOLD-order,
acknowledgement and ship-to-BAC disclosures. PIN requires approval; D30/R6X have
SOLD-only disclosures. Sources: `Exterior 3` rows 12–13; `Interior 3` rows 13–14,
54–55. VK3 is present here at 40 (`grand_sport_x_options` row 78), but the
ship-to-state forcing disclosure at `Exterior 3!C25` is not enforced by the
body/trim controls. These are product-selection probes, not dealer-order validation.

U2K, UE1, VV4, U5G and uncoded OnStar Basics are retained equipment in this lane.
R6P, R9Y/R9V/R9W, R9L, PRB and the six emissions/override codes
FE9/YF5/NE1/NB8/NB9/NC7 have no option identity. Sources: `Interior 3` rows 11,
44–52 and `Mechanical 3` rows 16–21. Those are explicit scope omissions, not
manufacturer removals. Territorial/Fleet/service conditions remain source
content rather than executable customer-form context.

**Equipment consumers:** `standardEquipmentRows()` filters by variant only.
In completed 2LT coupe and convertible builds, its 86/85 rows are unchanged
after FED acquisition; XFT remains in standard equipment while XFR appears in
the selected-build output. Thus static standard equipment cannot be presented
as an installed-equipment list. The same distinction matters for paid calipers,
seats, roofs, covers and ground effects. `currentOrder()` builds charges and
sections from `lineItems()` and also attaches a static equipment summary;
`compactOrder()` retains section items and only the standard-equipment count.

An enabled submit button proves neither manufacturer validity nor package-output
completeness: the 12 DTC/heritage and four EL9 cases pass its product-completeness
guards despite the demonstrated errors. Invalid interior completeness does block
the handler. No customer information was supplied, no valid submission was invoked,
and no external order service was exercised.

## 12. Coverage, decisions and implications for the schema proposal

### Source dispositions and price reconciliation

All **239 workbook offerings** have a disposition: 202 primary-guide coded
matches, 26 uncoded equipment matches, ten chart paints, and 5ZB supported by
`Price Schedule!B96:E96` but absent from the primary equipment offering sheets.
That price-only evidence does not establish the guide's six-context 5ZB
availability; the workbook's offering is preserved pending applicability review.
No duplicate RPO exists within this model, including inactive rows. No DUW
identity exists; DTC exists. SAI is the missing customer-accessory identity at
`Interior 3!C40:I40`; the guide allows all six contexts with V8X conflict at 3LT,
and `Price Schedule!E128` gives 295. Addition remains a proposed model correction.
TU7/N26/36S/37S/38S are accounted for as interior components, not missing cards.

The 1,212 coded and 156 uncoded status pairs all match: **1,368 comparisons**.
The full availability table has 1,434 rows; the remaining 66 pairs belong to
ten paints plus 5ZB and are not counted as primary-equipment status comparisons.
All 226 repeated coded occurrences in Standard Equipment 3/Equipment Groups 3
agree in text/status with their primary occurrence. Repetition is corroboration,
not an independent approval of business rules or prices.

The 26 uncoded mappings, workbook option row → guide row, are:

- Interior 3: 25→86, 157→16, 161→21, 162→25, 163→58, 179→97, 182→98,
  183→17, 185→19, 187→18, 188→90, 189→94, 190→81, 192→6, 194→23, 216→50.
- Exterior 3: 158→6, 164→107, 184→14, 191→18.
- Mechanical 3: 166→4, 180→9, 181→35, 186→46, 193→40, 195→43.

All 148 numeric option amounts were compared with the price schedule: 126 match
at least one same-code column-E amount; three carbon-wheel prices reconcile
through explicit model discounts (§9); J57 is standard here rather than either
other-model paid brake rate; Z25 has the documented residual-charge problem;
17 zero rows have no same-code schedule amount. Those 17 include standard/default
choices, no-cost paints and inactive V8X; absence from the price schedule is not
an inferred missing paid option. The other 91 option prices remain null evidence.

Qualifiers matter: BC4/BCP/BCS use the inspected body/package rates (§5); AE4
uses 1,095/2,095/595 by trim (schedule 239/240/238); AH2 is 1,695 at 2LT and
standard at 3LT (241); PCQ/VWE have separate Stingray rates and this lane's
1,675/950 branch (103–104/161–162). The 51 conditional-price rows cover seats,
covers, package inclusions and belts. Matching a base rate does not certify
all resolved totals: EL9/R6X examples demonstrate why component ownership and
selection/output still need independent checks.

### Remaining model-specific review items

These are review findings, not applied corrections or a new structured overlay.
Universal interaction decisions already made are not being reopened.

| Finding | Proposed disposition / decision still needed |
|---|---|
| DTC/hash coexistence loses Z15 and its charge | Reconcile DTC's complete heritage conflicts and preserve a usable hash-first acquisition path; verify both directions and order output. Confirm this lane's package disclosure and null-hash-price interpretation. |
| EL9 lacks Z25; AH2/AE4 share 1,995 total | Restore correct package acquisition/output; review content versus separate AE4 charge and EL9 belt locking for this model. |
| Four R6X/AE4 shortfalls | Review adding the missing 595 once, based on this lane's components, preserving old observations. |
| Conditional D84 absent | Add exact convertible stripe/paint requirements and disclosure, with explicit/dependency ownership and existing cleanup/revert policy. |
| EL9/orange D30 gap | Resolve alongside EL9 belt policy; if alternatives are prohibited, do not implement a new invalid pairing just to add its surcharge. |
| VPW/VPO incomplete stripe exclusions | Reconcile complete guide sets, including standalone rear graphics, in both directions. |
| SAI missing; DUE naming differs | Review adding SAI at the evidenced scope/rate and correcting DUE naming; no DUW replacement or T0E deduplication is needed here. |
| 5ZB has price-only guide support | Retain the observed workbook choice while confirming Grand Sport X applicability; a matching price is not an availability assertion. |
| SLN/CF8 selectable during lifecycle restriction | Review disabled-selection treatment and applicability; retain inactive R88/RZ9/V8X and verify full rules before future release. |
| ZZ3→LS6→D3V and HP1 copy | Remove misleading package-engine ownership from the target after review; corroborate model-specific horsepower rather than silently edit evidence. |
| Currency and price basis | Confirm Grand Sport X scope; preserve qualified discounts and zero/null distinctions. |
| Output/content and ordering scope | Carry configured versus informational equipment semantics into future consumers; retain disclosures without assuming full dealer-order enforcement. |

### Implications for the paused Stingray proposal

Model-owned identities, explicit configuration membership, inclusion/requirement
families, separate price owners and contextual content remain useful. This lane
also demonstrates several translation obligations:

- A metadata flag is not an executed prerequisite: EL9's `requires_z25` cannot
  stand in for a working acquisition relationship or correct order code.
- Single-section suppression is not a substitute for compatibility: DTC can
  hide the package charge while leaving its hash selected.
- Availability-dependent prerequisite scope must be resolved explicitly:
  cover→ZZ3 is effectively convertible-only despite blank workbook rule scope.
- Stripe-plus-paint D84 requires the same missing conditional-prerequisite
  capability identified in Grand Sport, independently evidenced here.
- Price provenance can comprise a model-qualified base plus discount; matching
  one RPO is insufficient. Null equipment/hash amounts need explicit treatment.
- Standard J57/B4Z/FE5 and FED's tire-only content must not inherit FEB/FEY
  requirements or the other model's brake/default restoration rules.
- Static equipment, installed content, selected purchases and order codes are
  separate consumers of the resolved build, each requiring acceptance checks.

No DDL or independent model schema is proposed here. Revisit one coherent design
after the remaining lanes, rather than patching the current candidate schema.

### Validation performed and handoff

Reverified the guide, frozen workbook, app, registry and model contract hashes.
Reviewed all model-owned direct/grouped/exclusive relationships, price families,
source disclosures and effective scopes. Executed:

- 49 connected sequences / 213 captured states, plus five focused reversal/cause
  sequences / 20 states, in addition to the retained initial six FED round trips.
- 264 body/interior contexts, 1,320 paint/interior states and 792 belt attempts.
- 100 body/stripe/paint cases, including all 17 guide-required D84 contexts.
- Four completed EL9 and 12 completed DTC/heritage defect cases, two static
  equipment comparisons, six seat/charge-cause states and missing-interior
  submission rejection. All probes made zero requests.

Local extraction, observations and verification scripts are retained under
`.local/grand-sport-x/`; exact source locations and material observed outcomes
are recorded above so the findings do not depend on row counts or local logs.
No new permanent test framework is introduced for this documentation task.
This is full family coverage, not exhaustive combination/direction acceptance,
visual QA, corrected runtime proof or production validation. The frozen evidence,
existing foundation JSON, canonical workbook and reference project are unchanged.

This task ends at the complete Grand Sport X **behavior analysis**. The next pass
is its structured handoff and owner review of the model-specific findings.
Do not start Z06 or schema consolidation as part of this task.
