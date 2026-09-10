# Stingray behavior: foundations and connected choices

**September 10 discovery catch-up:** the [current completion review](model-discovery.md#stingray) supplements this historical analysis with retained source/price accounting, full starting-choice observations and additional connected behavior/output evidence. Read it before interpreting older statements about unfinished coverage. Original facts, observations and accepted decisions below remain unchanged.

**September 9 review update:** [Accepted owner decisions](stingray-structured.md#8-decision-overlay-source-baseline-and-target-remain-separate) supersede earlier unresolved/proposed target statements below. This analysis preserves the original guide, workbook and observed behavior; it is not a statement that corrected targets have been implemented.

September 7, 2026. **Stingray relationship analysis for schema planning.** All
remaining families are now covered below, with source differences and behavioral
limits explicit. This is not schema approval, implementation or canonical acceptance.

Every model will use the same analysis structure: foundations; connected choices
and charges; guide → workbook → observed behavior; unresolved differences; remaining
coverage. Each model's explanation is self-contained. Similarity to another model
does not supply a missing fact or authorize shared ownership. Future implementation
must express model differences through a consistent structure, not six independently
invented architectures. This analysis does not choose that structure yet.

Sections 2–6 retain the reviewed foundations and roof, accent, engine-appearance
and spoiler paths. Sections 7–12 complete the family analysis: interior expansion,
belts, performance, wheels, accessories, order restrictions and equipment/output.
The completion boundary is coverage of the model's relationships and explicit
disposition of source gaps, not exhaustive acceptance of every possible build.

## 1. Sources and how to read this analysis

**Guide** means the unchanged export documented in [source provenance](../sources/README.md):
`2027 Chevrolet Car Corvette Export (6).xlsx`, SHA-256
`d3ca7d3a09c9fb89210b4ce584493b3ad8fb65ca35087c49d816d1cbf1a333d1`.
The main Stingray option sheets are `Interior 1`, `Exterior 1`, `Mechanical 1`;
each explicitly names Stingray in A1 and its six configurations in D3:I3.
`Color and Trim 1` and `Color and Trim 2` supply paint/interior combinations and
footnotes; their shared content must be narrowed to Stingray before use.

**Workbook** means the [frozen form baseline](../baselines/2026-09-06/README.md),
SHA-256 `3127e663b1531e366ce86b989b6190914108d40dfd15a33a258307a05d608e3c`.
`model_workbook_sources!A24:E34` supplies the Stingray sheet assignments. Paint
becoming selectable option rows is a workbook transformation, not a reason to
retain the guide's sheet layout in a database. Workbook values remain the existing
form baseline; a guide disagreement is not permission to change them.

**Observed** means execution of frozen browser revision
`4fe92a4f078370c478f18484cad31bdafe58ad43` using its existing DOM-stub harness.
Actual selection and context-change functions ran; no live submission or visual
browser test ran. Example totals are the current calculated totals of partial
builds, often still missing paint or interior. They are not completed-order quotes.
Amounts below use the workbook's numeric price basis; currency and the raw option
price-column ambiguity remain unresolved as documented in source provenance.

For 33 named primary-sheet rows, all **198 body/trim status pairs** agree with
workbook availability after interpreting S/■ as standard, A or A/D as available and
-- as unavailable. The original distinction between S and equipment-group inclusion
is retained in the explanation. All markers encountered were recognized; rich-text
superscripts were separated from availability symbols. This is status agreement,
not proof of complete disclosure interpretation.

For those selected rows, **39 matching occurrences** in `Standard Equipment 1` and
`Equipment Groups 1` have the same full description text and six status symbols.
They corroborate the original slice rather than creating extra options. Section 12
extends this comparison to all matched coded occurrences and uncoded equipment.

## 2. Model, body and trim establish the starting configuration

| Stingray configuration | Workbook base amount | Default roof | Default seat |
|---|---:|---|---|
| Coupe 1LT | 73,495 | CF7 body-color removable | AQ9 GT1 |
| Coupe 2LT | 80,595 | CF7 body-color removable | AQ9 GT1 |
| Coupe 3LT | 85,245 | CF7 body-color removable | AH2 GT2 |
| Convertible 1LT | 80,495 | CM9 body-color hardtop | AQ9 GT1 |
| Convertible 2LT | 87,595 | CM9 body-color hardtop | AQ9 GT1 |
| Convertible 3LT | 92,245 | CM9 body-color hardtop | AH2 GT2 |

Guide configuration identity: `Interior 1!D3:I3`; workbook membership:
`model_variants!A14:E19`, vehicle rows `variant_master!A2:H7`.
All six default states were observed. Paint and interior are still unchosen in
these states. Standard equipment and selectable defaults are not identical sets.

### Body determines which physical features are relevant

- **Coupe:** CF7, CC3 transparent roof and C2Z visible-carbon roof belong to the
  removable-panel family. CF8 additionally needs 2LT/3LT, but its source says not
  available at start of production and the workbook marks it inactive. It does
  not appear as a current selectable choice. See `Exterior 1!A72:I75` and
  `stingray_options!A129:K132`.
- **Convertible:** CM9 is the starting roof. D84 changes nacelles and roof to
  Carbon Flash; D86 changes nacelles while retaining a body-color roof. Both have
  a GBA restriction at every trim. See `Exterior 1!A8:I10`.
- **Engine appearance:** B6P belongs to coupe; ZZ3 belongs to convertible. The same
  colored engine-cover codes have different prerequisite/equipment consequences
  in those bodies, traced in section 5. See `Mechanical 1!A26:I32`.
- **Accents:** EFR/EFY/EDU also describe the convertible tonneau grille. Body can
  change what a package physically finishes, not merely whether it is selectable.
  See `Exterior 1!B14:I16`. This slice has not established a separate executable
  representation of every finished surface; text preservation alone is not proof.

### Trim determines optional purchase versus supplied equipment

| Feature | 1LT | 2LT | 3LT |
|---|---|---|---|
| UQT recorder | Optional, 1,495 | Included equipment; no separate purchase | Included equipment; no separate purchase |
| BAZ Stealth Interior | Unavailable | Optional, 695 | Optional, 695 |
| FA5 carbon-fiber interior trim | Unavailable | Optional, 1,795 | Optional, 1,795 |
| E60 front lift | Unavailable | Optional, 2,995 | Optional, 2,995 |
| AQ9 GT1 | Standard | Standard | Unavailable |
| AH2 GT2 | Unavailable | Optional, 1,695 | Standard, zero seat charge |
| AE4 Competition | Optional, 1,095 | Optional, 2,095 | Optional, 595 |
| AUP mixed seats | Unavailable | Unavailable | Optional, 350; restricted to HVZ/HAG interiors |

These statuses apply to both bodies, before additional conditions. Sources:
`Interior 1!A53:I53`, `A65:I69`, `A85:I88`, `Exterior 1!A17:I19`;
`stingray_options!A69:K71`, `A127:K127`, `A155:K158`;
`price_rules!A29:H31`. The seat-price display was observed in each of six contexts;
the original slice did not select every seat/interior combination; section 7 now
covers the full interior expansion.

**UQT transformation and transition:** the workbook retains one 1,495 option,
marks it standard in 2LT/3LT (`stingray_ovs!A1112:C1117`), and makes it display-only
in the included-equipment section (`stingray_variant_overrides!A2:H5`). On coupe
1LT, selecting it produces 74,990 = 73,495 + 1,495. Changing to 2LT resets choices
and produces 80,595 with no separate UQT charge. Returning to 1LT produces 73,495;
the former UQT purchase is not restored. The internal option-price lookup still
returns 1,495 on 2LT: the observed absence of a charge comes from its equipment/
selection role, not a universal rule that standard status sets stored price to zero.

## 3. Interior and paint choices begin here, but add further conditions

The ten paint choices are not listed as ordinary options in the guide's main
option sheets. They come from `Color and Trim 1!A16:D25` and `Color and Trim 2!A11:D20`.
The workbook makes them selectable in `stingray_options!A116:K125`:

| Paint | Workbook amount |
|---|---:|
| G8G Arctic White; GBA Black; GKA Blade Silver; GEC Pitch Gray; GKZ Torch Red | 0 each |
| GTR Admiral Blue; G4Z Roswell Green | 500 each |
| GBK Competition Yellow; GPH Red Mist; G26 Sebring Orange | 995 each |

Guide premium-color footnotes corroborate categories, not independently verified
option price-column values. Paint affects both component compatibility and interior
combinations; neither can be inferred from paint price or color name.

The starting interior paths in `Color and Trim 1!A5:Q13` are:

- **1LT/AQ9:** HTA Jet Black, HUP Sky Cool Gray, HUQ Adrenaline Red.
- **1LT/AE4:** HTJ Jet Black Performance Textile; footnote 5 requires N26.
- **2LT/AQ9:** H1Y, HUN, HUR, HUV. Moving to AH2/AE4 changes the code/material
  families to the rows at A8:Q9; seat choice also affects two-tone conditions.
- **3LT/AH2 or AE4:** rows A10:Q11; AUP is the mixed-seat route to HVZ/HAG.
  The shared sheet's EL9 row requires Z25 Grand Sport Launch Edition and must not
  become a Stingray offering simply because the row says 3LT.
- **Custom 3LT combinations:** `Color and Trim 2!A5:H8` and A22 establish R6X,
  with additional 38S, N26 and AH2/TU7 conditions for particular cells. A code alone
  is insufficient to establish the seat/material/prerequisite context.

The workbook has 130 Stingray interior memberships: 4 at 1LT, 40 at 2LT and 86 at
3LT. These are expanded workbook memberships, not 130 independent raw color codes.
Section 7 now reconciles the complete expansion and follows components, charges,
belts and changes of seat. The previously verified
[R6X additive-price requirement and frozen defect](model-rule-review.md#executed-r6x-review)
remain relevant; this extension rechecks Stingray, not the other models.

### A recommended combination differs from a prohibited option combination

Guide `Color and Trim 1!G16` marks G26 with Adrenaline Red as --, but A27 explicitly
allows deviations from the recommended matrix with paid D30. Contrast that with
D84's explicit “not available with GBA” disclosure. The same printed -- cannot be
interpreted without its surrounding table meaning.

Workbook `color_overrides!A2:D2` connects `1LT_AQ9_HUQ`, G26 and `opt_d30_001`;
`stingray_options!A34:K34` prices D30 at 1,495. In the observed coupe 1LT sequence:

| Change | Selected/automatic consequence | Calculated total |
|---|---|---:|
| Select G26 | Paint charge 995 | 74,490 |
| Select HUQ interior with AQ9 | HUQ accepted; D30 auto-added for 1,495 | 75,985 |
| Change paint to G8G | Interior retained; G26 and D30 charges removed | 73,495 |
| Return to G26 | D30 restored once | 75,985 |
| Change interior to HTA | G26 retained; D30 removed | 74,490 |

This demonstrates the two-input condition, automatic charge and both removal paths.
It does not prove every recommended-combination cell or any seat-belt warning has
identical semantics. No D30 equivalence for `Color and Trim 2` is assumed here.

## 4. Convertible roof and accents under a paint restriction

**Guide meaning:** D84 and D86 apply only to convertible and exclude GBA.
EFY and EDU also exclude GBA; EFR is the standard Carbon Flash accent choice.
The convertible's tonneau grille is included in those accent descriptions.

**Workbook representation:** body/trim availability for D84/D86; direct GBA
exclusions in `rule_mapping!A46:H47` and EFY in row 65; grouped GBA→EDU in
`rule_groups!A27:J27` plus `rule_group_members!A155:D155`. The required accent
set is `exclusive_groups!A8:E8`, members `exclusive_group_members!A24:D26`.
Option amounts are D84/D86 1,295; EFY/EDU 995; EFR zero. There are several stored
mechanisms behind one connected business decision, which is why a rule-type
inventory did not explain it.

**Observed 2LT convertible paths:**

| Selection sequence | Result |
|---|---|
| G8G → D84 | CM9 replaced; total rises from 87,595 to 88,890 |
| Then EFY | EFR replaced; total becomes 89,885 |
| Then attempt GBA | Refused; G8G/D84/EFY remain, total stays 89,885 |
| Fresh start → GBA → attempt D84 | D84 refused; CM9 remains; total stays 87,595 |
| Change GBA to G8G → D84 | D84 now permitted, total becomes 88,890 |
| Then change body to coupe | Full context reset; CF7 restored, paint/roof purchase cleared, total 80,595 |

The source establishes incompatibility. The current interaction chooses refusal,
not automatic deletion, when the conflicting paint or roof is clicked. In the
paint-first path the reason says “Blocked by D84 Carbon Flash Convertible Top”
even though D84 is the attempted choice. That is an observed explanation problem;
no copy or behavior was fixed. D86/EDU/EFY's full transition permutations remain
unexercised; their source/availability records were inspected.

## 5. Engine appearance: body, selected cover and price act together

Guide `Mechanical 1!A26:I32,A40:I40` provides the complete local chain:

- B6P coupe package includes D3V lighting and SL9 plaque, plus described carbon trim.
- ZZ3 convertible package includes the viewing window, BC7 cover and SL9 plaque.
- BCP/BC4/BCS on coupe include D3V; on convertible they require ZZ3.
- D3V is unavailable on convertible, so the coupe inclusion must not leak into it.

Workbook `rule_mapping!A37:H44,A119:H122` holds inclusion/prerequisite rows.
`price_rules!A3:H7,A22:H28` zeroes included lighting/plaque and changes colored
cover totals to 595 in the relevant selected-package/body context.

**Observed BCP sequences, 2LT:**

| Context and change | Equipment and charge consequence | Calculated total |
|---|---|---:|
| Coupe: select BCP alone | BC7 replaced; BCP 695, included D3V 0 | 81,290 |
| Add B6P | B6P 1,895; BCP becomes 595; D3V and SL9 0 | 83,085 |
| Remove B6P | BCP returns to 695; D3V stays through BCP; SL9 disappears | 81,290 |
| Convertible: attempt BCP without ZZ3 | Refused; ZZ3 required | 87,595 |
| Select ZZ3 | ZZ3 1,195; BC7 and SL9 auto-added at 0 | 88,790 |
| Select BCP | BCP 595; BC7 inclusion suppressed; SL9 remains; no D3V | 89,385 |
| Remove ZZ3 | BCP and dependent automatic equipment removed | 87,595 |

The coupe ZZ3-prerequisite rows have blank body scope, yet do not block BCP on
coupe: the frozen `ruleAppliesToCurrentVariant` discards a relationship whose
referenced target is unavailable in the current configuration. Availability is
therefore also controlling rule applicability. Copying that prerequisite row
alone would misdescribe behavior. The stored prose also mentions B6P as a coupe
requirement in places, while the guide and observed form allow BCP alone. That
prose/executable distinction remains visible; it has not been normalized away.

This tests one colored cover through both bodies. BC4/BCS have corresponding source
and price rows but have not been separately exercised here.

## 6. Paint, wing, Z51 equipment and deletion interact

Guide `Exterior 1!A49:I49` says 5ZU requires G8G/GBA/GKZ, conflicts with
5ZW/5ZZ/TVS, and deletes T0A when ordered with Z51. `Mechanical 1!A53:I53`
describes Z51's larger equipment set. A selected wing therefore affects paint
eligibility, peer choices and package-supplied equipment at the same time.

Workbook paint group: `rule_groups!A3:J3`, `rule_group_members!A4:D6`.
Spoiler peers: `exclusive_groups!A3:E3`, `exclusive_group_members!A6:D9`.
Z51 inclusions: `rule_mapping!A106:H113`. The 5ZU→ZF1 inclusion at row 124,
ZF1→Z51 prerequisite at row 117 and ZF1→T0A replacement at row 116 jointly
implement a conditional deletion: ZF1 can be included only when its Z51
prerequisite is met. It is not an unconditional 5ZU package member.

**Observed coupe 2LT sequences:**

| Change | Result |
|---|---|
| GBA → 5ZU | Wing permitted at 1,395; no ZF1 without Z51; total 81,990 |
| Add Z51 | Z51 5,395; ZF1 auto-added at 0; T0A absent; FE3/G0K/G96/J55/M1N/QTU/V08 included; total 87,385 |
| Reverse order: GBA → Z51 → 5ZU | Same selected equipment/charges; wing replaces package T0A through the deletion chain |
| Remove Z51 | Its automatic equipment and ZF1 disappear; FE1 default returns; wing remains at 1,395 |
| Fresh start: G26 → attempt 5ZU | Wing refused; requires G8G/GBA/GKZ |
| Existing GBA/5ZU/Z51 build → G26 | Paint changes; wing remains selected and charged; missing-requirement validation flags its paint prerequisite; total 88,380 |

The last state is **incomplete**, not demonstrated as an accepted valid order.
The form checks prerequisites differently when adding an option versus validating
an already-selected option. It neither refuses the paint change nor automatically
removes 5ZU. This is a behavior to preserve or explicitly reconsider later, not a
reason to invent a database deletion cascade.

### Two source/translation differences this chain exposes

1. **ZF1/wing:** guide `Exterior 1!A4:I4` says ZF1 is not available with 5ZU;
   the workbook deliberately uses automatic ZF1 with 5ZU/Z51. The guide separately
   says the wing deletes T0A. The net spoiler result matches that latter clause,
   but the form's intermediate order-code representation differs. Owner intent
   for that representation must remain explicit; no automatic correction.
2. **TVS/Z51:** guide `Exterior 1!A80:I80` explicitly requires ZF1 when TVS is ordered
   with Z51. The workbook option disclosure
   (`stingray_options!A160:K160`) says TVS requires ZF1 if Z51 is ordered. In both
   tested orders, TVS and Z51 coexist, TVS resolves to zero through `price_rules!A2:H2`,
   T0A is absent, and **ZF1 is absent**. The current total is 85,990 on coupe 2LT.
   Whether that net equipment result sufficiently represents the aero-delete
   requirement is unresolved; an isolated “Z51 makes TVS zero” example concealed it.

## 7. Complete interior choices, components and belts

### Trim and seat determine the allowed expansion

`Color and Trim 1!E5:P12` and `Color and Trim 2!E5:H8` contain **78 distinct
trim/seat/interior-code combinations** after expanding AH2/AE4 cells into their
separate seat contexts. EL9 is excluded by its Z25-only footnote. Applying the
stitch, N26 and TU7 disclosures produces exactly **130 Stingray choices**:
4 at 1LT, 40 at 2LT, and 86 at 3LT (71 ordinary, 15 R6X). There are no missing
or extra combinations in this expansion against `lt_interiors` and Stingray's
`model_interior_scope!A444:R573`. Identity includes the selected seat and extras;
an interior code alone cannot distinguish these leaves.

| Relationship | Source and complete scope | Workbook/form consequence |
|---|---|---|
| N26 is required for particular materials | `Color and Trim 1!A27` footnotes 5/7 and `Color and Trim 2!A22` footnote 2; `Interior 1!A79:I79` | Performance Textile at 1LT and the applicable suede-insert interiors contain an N26 component. It is carried by the interior choice, not purchased from a separate Stingray option card. |
| Stitching can be optional or mandatory | `Interior 1!A82:I84`: 36S/37S/38S on H1Y/HTM/HTP at 2LT and HTE/HTT/HUB/HUC at 3LT. `Color and Trim 2!A22`: HU0/HXO require 38S | Optional stitch choices become separate leaves. HU0/HXO have no stitch-free leaf. Each selected stitch contributes 495 from `PriceRef!A16:D18`. |
| Two-tone depends on seat and interior | `Interior 1!A69:I69`; both color-table footnotes | Only AH2 has TU7 leaves. HU7, HUA and HXO with AH2 require TU7; the other disclosed AH2 combinations offer it optionally. AE4 does not inherit AH2's TU7 requirement. TU7 contributes 595 from `PriceRef!A21:D21`. |
| Custom interior/seat combinations add R6X | `Interior 1!A14:I14`, `Color and Trim 2!A5:H8`, A22 | The 15 expanded custom choices each contain R6X at 995, plus their applicable extras. Eight raw custom codes yield 12 seat/code combinations, then 15 leaves. |
| Mixed seats restrict the interior set | `Interior 1!A68:I68`, `Color and Trim 1!O12:P12` | AUP at 3LT permits HAG/HVZ only, at a 350 seat charge. These interiors are also available in the ordinary AH2/AE4 contexts; AUP is not an interior-wide requirement. |

The **197 workbook component memberships** are at
`interior_components!A2:K198`; rates are at `PriceRef!A2:D22`. Zero-cost identity
and paid components have different purposes. The workbook's hierarchy labels
organize choices by seat, color, material and leaf; they do not establish new
equipment or price ownership merely because a label repeats.

**Observed coupe 2LT:** AH2 adds 1,695. Selecting `2LT_AH2_HU7_N26_TU7`
produces 83,580 = 80,595 + 1,695 + 695 + 595. Changing to AE4 clears that
interior. Selecting `2LT_AE4_HU7_N26` produces 83,385 = 80,595 + 2,095 + 695,
with no TU7. Returning to AQ9 clears the incompatible interior and its extras.
Separately, `2LT_AQ9_H1Y_38S` adds 495; switching to the plain H1Y leaf removes it.
All 130 leaves were selected in both bodies, checking actual eligibility and
itemization, not merely enumerating their IDs.

### Each charge must survive itemization exactly once

The additive relationship is seat + R6X when applicable + N26/stitch/TU7 extras.
The frozen output matches that subtotal for 126 of 130 choices in the coupe
price check. The four R6X/AE4 leaves each omit the 595 seat charge:

| Interior leaf | Additive seat/interior subtotal | Frozen subtotal |
|---|---:|---:|
| `3LT_R6X_AE4_HU0_38S` | 2,085 | 1,490 |
| `3LT_R6X_AE4_HUU` | 1,590 | 995 |
| `3LT_R6X_AE4_HXO_N26_38S` | 2,780 | 2,185 |
| `3LT_R6X_AE4_HZP_N26` | 2,285 | 1,690 |

This reproduces the [established R6X defect](model-rule-review.md#r6x-requirement-versus-implementation).
For example, the AH2 HXO/N26/38S/TU7 choice totals 88,025 on coupe 3LT:
85,245 + 995 + 695 + 495 + 595. The AE4 HXO/N26/38S choice totals 87,430,
but should contain another 595 under the already established additive requirement.
The frozen browser treats an R6X component as replacing the selected seat line.
An R6X flag, the stored interior total, the combined seat rate and the actual
component list therefore cannot become competing editable charge owners.
No price correction was applied during this analysis.

### Included belts, paid alternatives and hard prohibitions differ

Guide `Interior 1!A59:I64` supplies the belt relationship in each interior context:

| Interior codes, in their permitted seat contexts | Included belt |
|---|---|
| HZN/HUF Natural Dipped; EJH/EPX Very Dark Atmosphere | 3N9 Natural |
| H8T Santorini Blue; HAG Asymmetrical Santorini Blue/Jet Black | 3A9 Santorini Blue |
| HNK Adrenaline Red Dipped; HVZ Asymmetrical Adrenaline Red/Jet Black | 3F9 Torch Red |
| HUW/HUX Habanero | 379 Orange |
| Other interiors, absent a paid alternative | 719 Black default |

Workbook `rule_mapping!A128:H179` holds the 22 interior inclusions and the hard
HAG/HVZ prohibitions; `price_rules!A32:H53` makes the included belt zero in its
qualifying context. `exclusive_group_members!A27:D32` allows one belt at a time.
The default at `default_selection_rules!A4:K4` restores 719 when the section is
empty. Inclusion, price and default restoration are separate relationships.

HAG permits only 3A9; HVZ permits only 3F9. The six HAG/HVZ seat/interior leaves
produce **30 blocked belt attempts** across the six belt choices. In contrast,
H8T's included 3A9 can be replaced by paid 3F9: observed coupe 3LT goes from
85,245 to **87,335 = 85,245 + 595 + 1,495 D30**. Changing that interior to HTE
retains the chosen 3F9 but removes D30, producing 85,840. With AUP/HAG, the same
3F9 attempt is refused; changing to AUP/HVZ exchanges the automatic belt without
adding a belt charge. A recommendation override does not defeat a prohibition.

The 269 Stingray `color_overrides` relationships comprise **137 paint/interior
conditions and 132 belt/interior conditions**. The guide-derived paint matrix
matches all 137 workbook conditions exactly; all 1,300 interior × paint executions
produce D30 in exactly those cases. All 780 interior × belt attempts were also
executed, with all 132 guide-derived belt conditions matching the workbook and
observed D30 outcomes. Belt recommendation sets follow the specific disclosures: Orange,
Blue, Red and Yellow list discouraged colors; Natural lists recommended colors
and the workbook charges D30 for its complementary eligible set. This translation
is distinct from the hard HAG/HVZ exclusions. The coupe 1LT HUQ → Orange example
adds both 595 belt and 1,495 D30; changing paint to White does not remove this
belt-triggered D30, while changing the belt to Torch Red does.

With **both** G26 and Orange belts on HUQ, D30 appears once: coupe 1LT totals
76,580 = 73,495 + 995 paint + 595 belt + 1,495 D30. Changing paint to White
leaves the belt condition and D30 in place; changing to Torch Red belts then
removes D30. Multiple qualifying relationships do not mean multiple charges.

## 8. Performance connects suspension, brakes, tires and exhaust

### Z51 changes several equipment families together

`Mechanical 1!A53:I53` defines Z51's bundle; rows 7, 16, 18, 44, 48 and 52 plus
`Exterior 1!A79:I79` and A98:I98 disclose its members individually. Workbook
`rule_mapping!A106:H113` includes J55, FE3, G0K, G96, M1N, QTU, T0A and V08.
The front splitter is disclosed content, not a separate selectable RPO here.
The current Z51 charge is 5,395 (`stingray_options!A128:K128`).

The starting equipment is JL9 brakes, G0J mechanical differential, M1L
transmission, XFN all-season tires, FE1 suspension and NPP performance exhaust.
Z51 supplies J55 brakes, G96 electronic differential, M1N transmission, QTU
performance tires, G0K axle ratio and V08 cooling. Brake size, tire specification,
transmission and differential relationships cannot be reduced to a single generic
"performance" flag. Caliper color is independently selectable across all six
configurations (`Mechanical 1!A11:I15`).

| Observed coupe 2LT transition | Equipment/price consequence |
|---|---|
| Select FE2 | Non-Z51 magnetic suspension; total 82,490 (1,895 extra) |
| Add Z51 | Explicit replacement removes FE2; FE3 and seven other Z51 members become automatic; total 85,990 |
| Select FE4 | FE4 replaces included FE3 and adds B4Z traction management; total 87,885 |
| Select J6F | Red calipers add 795; Z51 brake equipment is unchanged; total 88,680 |
| Remove Z51 | FE4 loses its prerequisite and disappears, along with package equipment/B4Z; FE1 returns; J6F remains; total 81,390 |
| Select FE2 again | Retains the chosen caliper color; total 83,285 |

FE4's requirement and B4Z inclusion are separate rows at `rule_mapping!A66:H67`;
Z51's FE1/FE2 replacements are rows 126–127. FE4 costs 1,895 in addition to Z51.
Attempting FE4 first is refused. Removing FE4 while retaining Z51 restores
included FE3 at zero. The single suspension section and its default explain that
restoration; deleting the package does not restore an earlier user FE2 purchase.

**Equipment-output boundary:** `standardEquipmentRows()` in the frozen browser
filters by configuration only. It does not subtract replaced equipment according
to the selected build. The static standard-equipment catalog and the resolved
Z51 automatic lines are different views. Future planning must describe the
installed-equipment substitution explicitly; current summary counts do not prove
that JL9/G0J/M1L/XFN have been removed from a resolved equipment list.

### Exhaust layout and tip finish are separate choices

NPP is standard on all six configurations (`Mechanical 1!B33:I33`), independent
of Z51. WUB adds the quad center exit for 1,995; NWI adds bright tips for 395 and
requires WUB (rows 34–36; `rule_mapping!A68:H68`). The NGA/NWI required group
and NGA default are at `exclusive_groups!A11:E11`, members 36–37 and
`default_selection_rules!A3:K3`.

Observed coupe 2LT: NWI first is refused; WUB gives 82,590 with NGA retained;
NWI gives 82,985 and replaces NGA. Removing WUB removes dependent NWI and restores
NGA, returning to 80,595. The required group is tip finish, not WUB versus NGA:
WUB and NGA can coexist. E60 similarly adds TR7 at zero and removes it when E60
is removed, but is limited to 2LT/3LT (`Exterior 1!A17:I19`).

## 9. Factory wheels, accessory wheels and package alternatives

`Exterior 1!B99:I104` defines the factory wheel family: QEB standard, with
QE6/Q99/Q9A/Q9I/Q9O alternatives. The required factory-wheel section chooses one.
The guide separately calls 5DO/5DG **a second set of wheels**, including their
own hardware (`Exterior 1!A66:I67`). The workbook's optional LPO-wheel section
therefore coexists with the factory-wheel selection; both can carry charges.

Observed coupe 2LT: QE6 costs 1,095, then 5DG adds 4,395, yielding 86,085.
QE6 remains selected. R8C and SPZ attempts are blocked by 5DG. Removing 5DG keeps
QE6, and R8C can then be selected, adding CFX and giving 83,385.
`rule_mapping!A2:H11` preserves both accessory wheels' exclusions of
R8C/S47/SFE/SPY/SPZ. Their included hardware is descriptive content, not those
excluded accessory option purchases.

SPZ requires SPY; SFE conflicts with SPY, and SPY/S47 conflict with each other
(`Exterior 1!A62:I65`; `rule_mapping!A93:H99`). Selecting SPY then SPZ adds
320 + 105. S47 is refused. Removing SPY removes its now-invalid SPZ dependent.
This is a prerequisite plus a conflict, not automatic inclusion of locks with nuts.

### A package's included component can yield to a paid alternative

PCX includes 5DG, SFZ, SHT and SNG at a package charge of 4,595
(`Exterior 1!A25:I25`; `rule_mapping!A75:H78`; `price_rules!A11:H14`). Its
exclusion group spans delivery, hardware, badges and graphics.

Observed with QE6 already selected: PCX gives 86,285 and includes its four
components at zero. Selecting **5DO instead suppresses included 5DG**, retains
PCX at 4,595, and adds 5DO at 4,395: total 90,680. Selecting SHW then suppresses
included SNG and adds 295, producing 90,975. Removing PCX removes its remaining
automatic SFZ/SHT but retains paid QE6, 5DO and SHW, producing 86,380.

PDV shows the same distinction with a different membership mechanism. It includes
SB7/VWD for 750 (`Exterior 1!A24:I24`; `rule_mapping!A79:H80`,
`price_rules!A15:H16`). If 5ZD was explicitly chosen first, PDV preserves those
paid caps and suppresses VWD. Changing to RXH replaces 5ZD; removing PDV removes
SB7 but retains RXH. The total is 81,595 with PDV and 80,845 after its removal.

These are observed workbook/consumer policies, not guide-authorized package
credits. `shouldSuppressIncludedDefault()` and `userSelectedExclusiveGroupPeer()`
give explicit user choices precedence in these cases. The package price does not
fall when a member is suppressed. A future plan must represent that policy
explicitly or list an intentional change; a plain package-membership edge is
insufficient. Stingray has no varying positive package-price schedule requiring
the browser's inferred package-base/component-delta calculation: its 52 price
rules are zero inclusions, scoped cover/seat prices and interior-conditioned belts.

## 10. Stripes, ground effects and remaining accessories

### Paint conflicts and directional group behavior

`Exterior 1!A81:I96` ties stripes to paint: DPB/DUE/DTC conflict with GTR;
DPC/DT0/DZU with GBK; DPG/DSY with G26; DPL/DSZ/DUK/DZX with GKZ/GPH.
DPT/DTH/DUB/DZV have no paint restriction in these rows. The workbook instead
has DUW and no DTC. The owner resolved this on September 7, 2026: remove DUW
and include DTC in stripes using the newer export (section 12). The observations
below still describe the unchanged frozen workbook.
`rule_mapping!A48:H63` contains the workbook paint exclusions.

Observed: GTR blocks DPB; changing to G8G permits DPB at 1,295. With DPB already
selected, attempting GTR is refused, leaving G8G and its total unchanged.
DPT → DZV replaces the stripe through the single stripe section, changing the
charge from 1,295 to 595. DZV blocks SB7; removing DZV permits SB7 at 595.
The hash-mark section is independent of that stripe section.

The 25 exclusion groups (`rule_groups!A4:J28`) cover PCX/PDV, R88/SFZ/CF8,
SB7/SHT, the individual stripe sources, and GBA's EDU/ZYC restrictions. Their
full member lists are at `rule_group_members!A7:D156`. They are not interchangeable:
badge/roof groups concern full-length stripes, while other groups also contain
stingers and package endpoints. The raw SHT/SB7 lists even differ from PCX/PDV
on DUW; absence and repetition are evidence, not permission to unify the lists.

**Selection order matters:** DPB → PDV removes DPB and selects PDV with SB7/VWD;
PDV → PCX removes PDV and selects PCX with its four members. But PCX → DPB is
refused. Similarly EYK → SFZ removes EYK, whereas SHT → SB7 is refused.
The frozen `excludesAnyReason()` checks selected sources against the candidate;
reconciliation can remove a previous choice after a new group source is selected.
These are not all authored `runtime_action=replace` rows. A schema plan must
separate conflict membership from the interaction policy used to resolve it.

### Ground effects and covers depend on installed aero

5V7 requires a permitted high wing and conflicts with Z51, TVS, STI and relevant
ground effects (`Exterior 1!A38:I41`). The workbook requires-any group currently
contains 5ZU/5ZZ, whereas the guide also names 5ZW; 5ZW is inactive. 5VM/5W8
are also inactive, retain their prerequisite/exclusion evidence, and cannot be
used as proof of selectable paths. The original four direct requires rows for
each remain evidence; they do not make an inactive offering usable.

Observed: 5V7 alone is refused. G8G → 5ZU → 5V7 succeeds for 1,395 + 650;
Z51 and PCU are then refused. Removing 5V7 retains the wing. PCU supplies
STI/VQK/VWE for 1,575, with zero component prices (`rule_mapping!A69:H74`,
`price_rules!A8:H10`). Selecting STI first, then PCU, absorbs STI into automatic
equipment. Removing PCU does **not** restore the earlier standalone STI purchase.

| Cover relationship | Guide and observed/workbook disposition |
|---|---|
| WKQ excludes high wings | `Exterior 1!A27:I27`; WKQ first blocks 5ZU, then removing WKQ permits the wing. |
| RWJ excludes Z51 | `Exterior 1!A30:I30`; the Z51 build refuses it. |
| RNX with Z51 requires ZF1 | `Exterior 1!A31:I31`; workbook `rule_mapping!A89:H89` instead excludes Z51 outright. Z51 → ZF1 → RNX is still refused. This is a concrete source/behavior difference. |
| WKR supplies a high-wing cover when appropriate | `Exterior 1!A29:I29`; one workbook WKR offering carries the disclosure. The form does not emit a distinct cover-version selection. Physical fulfillment is contextual content, not demonstrated as a separate executable relationship. |
| Cover peers | Indoor RWH/SL1/WKR/WKQ and outdoor RNX/RWJ are separate exclusive groups. Indoor and outdoor covers are not one combined group. |

### Packages and standalone accessories retain distinct lifecycle behavior

PEF includes CAV/RIA for 475; PDY includes RYT/S08 for 195
(`Interior 1!A26:I37`; `rule_mapping!A81:H84`; `price_rules!A17:H20`). Observed
CAV → PEF removes the separate 230 purchase and adds zero-price CAV/RIA.
RYT → PDY similarly absorbs the 60 first-aid kit. Removing either package removes
its inclusions without restoring the former standalone selection.

SBT adds a second transparent roof and SC7 for 2,525, requires coupe applicability,
and conflicts with CC3 (`Exterior 1!A44:I44`, `Interior 1!A39:I39`). Observed SC7
first costs 195; SBT absorbs it at zero; CC3 is blocked. Removing SBT drops SC7,
after which CC3 replaces CF7 for 995. The additional roof is not an instruction
to replace the factory roof with CC3.

Other relationship families are covered as follows:

- SXB/SXR/SXT are mutually exclusive liner colors, and RIK/RIN/SL8 are mutually
  exclusive rear scripts. Actual SXB → SXR and RIK → RIN transitions replace
  only their respective peer, retaining an independently chosen indoor cover.
- RWU organizer, VYW mats, S2L bags, VTB protector, SDA hook and ERI battery
  protection are independent purchases within their configured sections;
  they have no additional source prerequisite in the inspected rows. The
  RWU/ERI/SDA/VYW sequence accumulates their charges; removing RWU removes only 175.
- W2D cargo nets are offered at 1LT; AP9 supplies cargo nets in 2LT/3LT
  (`Interior 1!B12:I12`, A28:I28). Shared purpose does not make them one
  simultaneously purchasable item.
- SLK, SLN and VUP are coupe-only engine-bay accessories
  (`Mechanical 1!A38:I41`). SLN's current active state disagrees with the guide's
  unavailable-at-this-time disclosure; see section 12.
- RYQ/RZ9 conflict with EFY (`Exterior 1!A32:I36`); RYQ is inactive. 5JR is
  3LT-only and includes DRG. Observed 5JR + ZYC contains DRG once, while both
  paid sources remain charged (1,395 + 295). ZYC with Z51 adds no separate
  painted-spoiler charge; deleting aero removes T0A but retains DRG and ZYC.
  EFY/EDU's body-specific surfaces and WKR's cover version remain descriptive
  physical consequences for the schema plan, not extra invented RPOs.

## 11. Order restrictions, standard equipment and consumer boundaries

R8C includes CFX for 1,695 and conflicts with accessory wheels; BV4 is a separate
395 plaque. `Exterior 1!A11:I12` and `Interior 1!A54:I55` disclose sold-order,
ship-to BAC, acknowledgement and approval requirements. The workbook adds an
explicit BV4/R8C exclusion (`rule_mapping!A45:H45`), where the guide says the
museum plaque is already included rather than expressly prohibiting BV4.

Observed BV4 → R8C is refused. Removing BV4 permits R8C and automatic CFX;
removing R8C removes CFX. PIN can be selected at 5,495 and VK3 at 40 without
supplying a VIN reservation approval or a ship-to state. The frozen form has no
modeled sold/stock-order, BFU, BAC or emissions jurisdiction selector enforcing
these disclosures. VK3's forced-by-state policy (`Exterior 1!A22:I22`) is text,
not a verified state-dependent default. Likewise D30/R6X sold-order restrictions
are not enforced by choosing an interior. These are catalog/ordering boundaries
to decide in the whole schema plan, not missing UI fields added by this task.

The guide also has service/order-type and emissions relationships absent from
the workbook offering set, listed in section 12. Their omission is explicit;
matching the existing form does not establish manufacturer-order completeness.

### Standard equipment is a configuration view, not the selected-option list

All 26 uncoded workbook equipment records have corresponding primary-guide
descriptions and matching body/trim status, including coupe hatch versus
convertible trunk release, 3LT leather-wrapped interior and universal safety/
convenience features. Codes are not mandatory equipment identities. The 205
matched coded records include the trim changes from UVB/UQS/K7A/DWK at 1LT to
UVA/UQH/K7B/DYX at 2LT/3LT, with the extra comfort/security equipment supplied by
those trims. No duplicate purchase should arise from a second guide occurrence.

Custom leather wrapped trim's HUB/HUC suede substitution is disclosed at
`Interior 1!C86`, preserved in `stingray_options!A25:K25`, and reflected in the
interior definition. The static equipment card itself does not change its name
when that interior is selected. Similar physical-content dependencies must not
be mistaken for independently resolved assets or surfaces.

The remaining consumer relationships are workbook-authored:
sections define required/single/multiple/display-only behavior; section presentation
and runtime steps place choices; summary sections route line items; context copy
describes body/trim; assets attach images without changing availability.
`model_workbook_sources!A24:E34` fixes Stingray's source routes. These presentation
relationships and the model's six configuration memberships are part of the model
plan, even though they are not manufacturer equipment relationships.

The frozen `currentOrder()` computes base + line items, separating selected
options, automatic options, interior identity and interior components.
`compactOrder()` derives its recap from those same sections. Standard equipment
is a separate configuration-based summary. The observed totals above are partial
builds, not submitted orders. Body/trim changes reset selections; changing a seat
clears an incompatible interior. No dealer submission, live request or production
verification was performed.

## 12. Coverage, unresolved facts and next boundary

### Complete family accounting

| Evidence set | Result and practical limit |
|---|---|
| All 242 workbook offerings | 205 match coded primary-guide rows; 26 match uncoded equipment descriptions; 10 paints originate in the color tables; DUW has no matching primary-guide offering in this revision. Every offering has a disposition. |
| Body/trim statuses | All 1,230 coded and 156 uncoded matched pairs agree: 1,386 comparisons. The 60 paint pairs and six DUW pairs remain workbook facts, not an equivalent primary-guide option matrix. |
| Repeated guide occurrences | All 223 coded occurrences in Standard Equipment 1 / Equipment Groups 1 match their primary-sheet disclosure and six status symbols. Uncoded records were mapped by meaning separately, not merged using blank codes. |
| Interior structure | 78 guide trim/seat/code combinations expand to exactly 130 workbook choices; complete extra-component membership comparison has no missing/extra leaves. All 130 selected in both bodies, 260 contexts. |
| Interior prices | 126 of 130 coupe subtotals match additive seat/components; the four R6X/AE4 defects above remain. Both-body interior execution is retained; the independently calculated price sweep used coupe. |
| Paint/interior and belt/interior | 137 guide-derived paint conditions match workbook; 1,300 paint states match D30 expectations. All 780 belt attempts recorded, including 30 hard refusals. The 132 belt conditions and 22 zero-price inclusions are distinct from paint conditions. |
| Runtime choice inventory | 236 active offerings × six configurations = 1,416 status/visibility/disable-reason observations, including unavailable contexts; 742 independently enabled choice actions. Six inactive offerings retained as evidence. This is baseline-state coverage, not all combinations. |
| Connected transitions | Original 17 scenarios / 57 states rerun; 31 additional sequences / 180 states cover the paths above: **48 sequences / 237 states**. Sweeps are counted separately. |
| Rules and consumers | All 178 direct rows, 27 groups/155 members, 10 exclusive groups/36 members, 52 prices, four defaults and 269 color relationships inspected by family and connected consumer path. This is not an assertion that every rule branch in every state was executed. |

### Owner decisions accepted for the schema plan — September 7, 2026

The owner reviewed the analysis and confirmed that everything else reviewed looks
correct. The following two source corrections are accepted requirements for the
whole Stingray schema plan. This accepts the analysis as a planning foundation;
it does not resolve every remaining business decision or authorize implementation.

- **Remove DUW and add DTC to stripes.** Use the newer export for this specific
  area. DTC is Royal Blue Full Length Dual Racing Stripes, available across all
  six body/trim configurations and unavailable with GTR Admiral Blue Metallic
  (`Exterior 1!A83:I83`). Carry DTC's guide-listed accessory/package/roof
  exclusions into the plan. DUW must no longer be a selectable offering or an
  active relationship target; retain its historical workbook identity and raw
  guide mentions as evidence. This is an intentional source correction, not a
  claim that the frozen workbook already contains DTC or that the two codes are
  interchangeable aliases.
- **Add SAI sill plates.** The new LPO stainless steel dark sill plates are
  offered across all six configurations (`Interior 1!A40:I40`). Preserve the
  guide's 3LT footnote excluding V8X visible Carbon Fiber sill plates. The
  existing inactive V8X evidence remains separate; SAI's omission is resolved
  in favor of inclusion in the plan.

These decisions do not establish an option price or resolve the source's price
column/currency ambiguity. Frozen coverage counts and runtime observations remain
unchanged; future validation must distinguish these accepted changes from parity.

### Differences and dispositions that must remain visible in the schema plan

| Fact or behavior | Exact evidence and disposition |
|---|---|
| R6X seat undercharge | Four Stingray AE4 leaves omit 595. Additive requirement already established; consumer correction remains separate from parity. |
| Wing/ZF1 and TVS/Z51 | Section 6: guide and current emitted order-code relationships differ even when spoiler suppression looks correct. Keep these as explicit decisions. |
| RNX with Z51/ZF1 | Guide permits the conditional aero-delete path; workbook excludes Z51 outright. Reproduced refusal; no repair made. |
| DTC versus DUW | Guide `Exterior 1!A83:I83` has DTC; workbook has no DTC offering. Workbook `stingray_options!A202:K202` has DUW, absent as a primary offering in this guide, although some guide exclusion lists mention it. Owner decision: remove DUW and include DTC in stripes using this export. Carry the corrected active stripe membership into the plan, including CF8's exclusions; retain the original 14-code raw list and 13-member workbook list as historical evidence. |
| Lifecycle disagreements | Guide marks 5ZZ (`Exterior 1!C50`), R88 (C34) and SLN (`Mechanical 1!C38`) unavailable at this time; all three are active workbook choices. Workbook-inactive RYQ/5VM/5W8/V8X/CF8/5ZW are preserved separately. Matrix availability does not supersede a lifecycle footnote. |
| SAI omission | `Interior 1!A40:I40` offers stainless dark sill plates with a 3LT V8X conflict. No Stingray SAI workbook offering exists. Owner decision: add the new SAI offering using the export, retaining its scoped V8X conflict. V8X remains inactive in the frozen baseline. |
| Service and order-type scope omitted | R6P, R9Y, R9V, R9W, R9L and PRB at `Interior 1!A11:I11`, A44:I46, A51:I52 have no matching workbook offerings. They depend on service prerequisites, BFU, order type and/or destination; no automatic inheritance into the schema baseline. |
| Emissions scope omitted | FE9/YF5/NE1/NB8/NB9/NC7 at `Mechanical 1!A19:I24` are absent from the offering set. NB8 requires FE9; NB9/NC7 require YF5 or NE1, with dealer/registration/shipping conditions. These relationships are recorded as outside the current form, not silently discarded. |
| Package alternatives and charge retention | PCX/PDV examples suppress an included member while retaining the package charge and adding a paid alternative. Current behavior is clear; guide text alone does not establish that authoring policy. |
| Descriptive physical and operational consequences | WKR cover version, accessory-wheel hardware, accent/roof surfaces, HUB/HUC trim material, sold-order/ship-to/approval conditions are not all executable facts in the current form. Preserve their disclosure and name the future ownership decision. |
| Source prices/currency | Raw option-price headings and currency remain unresolved. All quoted amounts use the frozen workbook basis; no manufacturer-price acceptance was inferred. |

The five guide codes TU7/N26/36S/37S/38S absent from `stingray_options` are
**accounted for as interior components**, unlike the 14 unmatched guide offerings
above (DTC, SAI, six service codes and six emissions codes). No source fact or
relationship was added to, changed in, or removed from canonical data. The added
facts here are analysis findings and explicit dispositions; DTC/DUW and SAI are
now owner-accepted planning corrections, pending implementation.

### Schema plan drafted; review before implementation

This completes the remaining family analysis at the stated planning boundary.
The [whole Stingray schema plan](stingray-schema-plan.md) is now drafted for review:
ownership, identities, relationship grains, scopes, prices and consumer/presentation
boundaries, with accepted corrections and remaining decisions attached to their
owners. Its connected walkthrough is design reasoning, not a new runtime test.
Do not implement a small database pilot or cut over before the model plan is
reviewed. The previous cross-model ownership proposal remains unvalidated; other model lanes have not
been completed by this work.

Source/workbook/browser hashes were checked, and the frozen source remains unchanged.
The local read-only investigation is in `.local/stingray-foundations/`: original
`source-comparison.json`, `probe.mjs`, `observed.json`; added `remaining-source.py`,
`coverage.py`, `interior-check.py`, `remaining-probe.mjs`, `combinations.mjs`,
`verify-remaining.py` and their
JSON/text outputs. These are local investigation aids, not application code or a
new mandatory validation framework. The source originals stay Git-ignored.

The Python reads use the bundled Python/openpyxl environment. Run the original
`probe.mjs` first to refresh the hash-checked frozen app/data and pinned harness,
then the added source/coverage/interior checks and the two added Node probes.
All runtime runs use the pinned DOM-stub harness with zero live requests. There
was no visual browser test and no exhaustive cross-product or production acceptance
claim. No schema, importer, consumer, workbook, raw guide or deployment was changed.
