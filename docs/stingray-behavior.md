# Stingray behavior: foundations and connected choices

September 7, 2026. **First analysis slice, not a complete Stingray model or a schema proposal.**

Every model will use the same analysis structure: foundations; connected choices
and charges; guide → workbook → observed behavior; unresolved differences; remaining
coverage. Each model's explanation is self-contained. Similarity to another model
does not supply a missing fact or authorize shared ownership. Future implementation
must express model differences through a consistent structure, not six independently
invented architectures. This analysis does not choose that structure yet.

This slice follows Stingray's six body/trim configurations, seat/paint foundations,
and connected roof, accent, engine-appearance and spoiler decisions. It establishes
specific behavior and limitations below. It does not claim that every option,
interior, accessory or combination has been understood or tested.

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
They corroborate this slice rather than creating extra options. This does not
assert that every row of those two sheets is redundant.

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
this slice did not select every seat/interior combination.

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
3LT. These are counts of expanded workbook memberships, not 130 independent raw
color codes. Their full cell-by-cell expansion and all interior component/seat-belt/
stitching interactions are **not yet reconciled in this slice**. The previously
verified [R6X additive-price requirement and frozen defect](model-rule-review.md#executed-r6x-review)
remain relevant; those 180 cross-model cases were not rerun here.

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

## 7. Coverage, unresolved facts and next boundary

**Completed in this slice:** all six starting configurations; selected body/trim
status reconciliation; ten paint identities/amounts read; seat/interior foundation
and source-footnote distinctions; 17 frozen-runtime scenarios / 57 recorded states
covering the sequences above. Source and frozen browser hashes were checked.
All 39 selected duplicate occurrences matched description text and availability.
No workbook, raw guide, schema, importer, consumer or deployment was modified.
No database table design follows from this analysis yet.

The 33 primary source rows checked across six configurations were UQT, AQ9, AH2,
AE4, AUP, BAZ, FA5, ZF1, CM9, D84, D86, EFR, EFY, EDU, E60, 5ZU, 5ZZ, 5ZW,
ZYC, CF7, CC3, C2Z, CF8, TVS, B6P, ZZ3, BC7, BC4, BCP, BCS, D3V, SL9 and Z51.
Matrix agreement covers 198 pairs. It does not validate all clauses or all 242
Stingray workbook options. Original S/■ and superscript distinctions remain evidence.

**Open within the inspected area:**

- Exact contextual physical content of accents/ZYC beyond text and simple option
  inclusion; painted spoiler treatment depends on Z51/TVS as well as ZYC.
- ZF1/wing and TVS/Z51 source-versus-output distinctions above.
- CF8 is inactive. Its raw disclosure (`Exterior 1!C75`) lists 14 stripe codes,
  including DTC; the workbook group at `rule_group_members!A76:D88` lists 13,
  omitting DTC. No conclusion about adding a Stingray DTC offering or activating
  CF8 is justified by that difference alone.
- Full mapping of the 130 interior memberships, including R6X, stitches, N26, TU7,
  mixed seats, included belts, recommendations and hard prohibitions. The color
  tables' footnotes do not reduce to one generic interior requirement.
- Source option prices remain ambiguous by column heading; baseline workbook
  amounts are reported explicitly, not represented as accepted manufacturer prices.

**Still unreviewed as complete connected families:** wheel/tire and brake choices,
remaining suspension/package paths, full stripes/graphics/accessory interactions,
exhaust, delivery/order restrictions, remaining standard equipment and all
cross-family transitions. Other models have not been started.

The local read-only investigation is retained in `.local/stingray-foundations/`:
source-comparison.json (full selected disclosures/cell runs and matrix comparison),
probe.mjs, observed.json and observed.txt. `node .local/stingray-foundations/probe.mjs`
repeats the frozen-runtime observations using the pinned reference harness. These
are local analysis aids, not a new production importer or validation framework.
The source originals remain Git-ignored. Future work should extend this same
Stingray walkthrough with the next connected family, using the same sections and
source/behavior distinctions for every model.
