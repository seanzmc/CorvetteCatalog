# ZR1 behavior: foundations and connected choices

September 10, 2026. ZR1 discovery is ready for owner review. Source facts and
frozen behavior are retained in the [structured handoff](zr1-structured.md),
[records](zr1-structured-records.json) and [runtime observations](discovery/zr1-runtime.json).
The open decisions below are proposals, not accepted corrections. No canonical
workbook, application, database, production form or ZR1X lane was changed.

## 1. Evidence and model scope

The unchanged guide `2027 Chevrolet Car Corvette Export (6).xlsx` has SHA-256
`d3ca7d3a09c9fb89210b4ce584493b3ad8fb65ca35087c49d816d1cbf1a333d1`.
Interior/Exterior/Mechanical 5 and Standard Equipment/Equipment Groups 5 combine
ZR1 and ZR1X. **D:G belongs to ZR1**, in coupe 1LZ/3LZ, convertible 1LZ/3LZ
order. H:K belongs to ZR1X. TOM has separate rows for the two models. HP1,
FEH/FEZ and MLP are not ZR1 equipment. Their shared-sheet presence does not
create ZR1 offerings. Full wording and both scopes are retained as source evidence.

The [frozen September 6 workbook](../baselines/2026-09-06/README.md) has SHA-256
`3127e663b1531e366ce86b989b6190914108d40dfd15a33a258307a05d608e3c`.
`model_workbook_sources!46:56` routes this model to `zr1_*`, LZ interiors and
color overrides. Workbook and browser key are both `zr1`. Original workbook,
app, registry and contract bytes are checked against the frozen manifest.
The runtime revision is `4fe92a4f078370c478f18484cad31bdafe58ad43`.

Observations execute the actual frozen selection, reconciliation, pricing and
order functions with the established DOM/network stubs. They preserve actions,
disable reasons, selected and automatic IDs, prices, totals, missing requirements,
order sections, compact recap and informational equipment. No visual browser QA,
live submission or corrected-runtime test is claimed; there were zero requests.

All 207 offerings have a disposition: 171 coded guide matches, 26 uncoded
standard-equipment matches and ten paints. All 684 coded status pairs agree;
the 26 uncoded mappings also agree in all four contexts. All 195 applicable
repeated coded occurrences agree in wording and status. ZR1X's second TOM row
is explicitly excluded from that comparison. Counts support this review; they
do not establish connected behavior or acceptance by themselves.

## 2. Four starting configurations

| Body / trim | Base including destination | R8E | Starting total |
|---|---:|---:|---:|
| Coupe 1LZ | 197,195 | 3,000 | 200,195 |
| Coupe 3LZ | 208,195 | 3,000 | 211,195 |
| Convertible 1LZ | 207,195 | 3,000 | 210,195 |
| Convertible 3LZ | 218,195 | 3,000 | 221,195 |

`variant_master!26:29` and `model_variants!26:29` reconcile to Price Schedule
34/36/35/37, F + J. Destination 2,495 is already included. R8E is a separate
3,000 line from `zr1_options!54`, selected by `default_selection_rules!22`.
TOM/ZTK do not change that rate. Qualified option amounts are read from guide
column E with D qualifiers; the header alignment/currency history remains in
[source provenance](../sources/README.md). These are source schedule comparisons,
not tax-law verification or a newly accepted price basis.

J58, J6D, SOJ, T0E, EYT, NGA and black 719 begin selected. AQ9 starts at 1LZ;
AH2 starts at 3LZ. Paint and interior remain unset. Body/trim change resets the
build; a 3LZ coupe ZTK build returns to the 1LZ convertible foundation.

ZR1's guide-standard LT7/M1K/G0K, UQT, DY0 and CFV differ from Z06's lane.
UQT is standard at **both** trims and is display-only at zero incremental cost;
the inherited 1LZ 1,495 price rule (`zr1_price_rules!12`) is dormant in the
observed path. It must not be interpreted as an actual ZR1 recorder charge.
E60 is available only at 3LZ. FA5 is available at both trims; FA6 and BAZ only
at 3LZ. The two carbon trim alternatives replace each other; BAZ can coexist.

3LZ upgrades include UQH audio, UVA cameras, K7B charging, DYX mirrors, memory,
heated/vented seats and theft sensors. 1LZ retains UQS/UVB/K7A/DWK. UV6 and
DRZ are standard even at 1LZ. W2D is an optional 1LZ net set; AP9 is supplied
at 3LZ. These facts retain their exact source rows and four availability cells.

## 3. ZTK, brakes, aero, wheels and calipers

Mechanical 5!6:7,43:50 and Exterior 5!5,53,68:74 establish the lane:
J58/FE8/XFR are standard; ZTK includes J59/FEJ/XFS and requires TOM.
TOM is 12,995; ZTK is 5,995, so acquiring ZTK from the starting configuration
adds **18,990**. J59/FEJ/XFS appear at zero; TOM remains a separate 12,995 charge.
The guide's 1,500 ZTK rate is explicitly ZR1X-only (Price Schedule 231–232).

`zr1_rule_mapping!39:41,45` supplies these components. The `ztk_excludes_j58_brakes`
and `ztk_excludes_non_ztk_aero` groups (`zr1_rule_groups!5:6`) block restoring
J58/T0E while ZTK survives. In all four contexts, ZTK acquisition leaves no
missing requirement; removal restores J58/T0E and the original total. J59 is
not directly purchasable despite its `available` workbook cells. The required
brake group prevents empty brakes. J6D is already standard, unlike Z06's missing
caliper inclusion. A purchased J6O survives ZTK acquisition and removal at 795.

TOM → ZTK → remove ZTK loses the original TOM purchase and returns to baseline.
This is observed purchase-intent loss, not a manufacturer requirement. Clicking
selected TOM does not remove the radio-like aero choice; selecting T0E does.
SIG requires T0E; acquiring TOM removes SIG, and returning to T0E makes SIG
available again. All four contexts were exercised.

SOJ is standard. SOF/SOG/SOH/SU1 replace the factory wheel at
1,495/1,995/1,995/15,995 (Price Schedule 283–285,293). SU1 is available with
standard J58; there is no imported Z06 J57 prerequisite or carbon-wheel package.
S47 and SFE refuse SU1 in both acquisition directions. SPY costs 320; SPZ
costs 105 and requires SPY. Removing SPY removes SPZ and both charges.
Factory carbon wheels are not dealer second wheel sets; the guide R8C/LPO-wheel
restriction does not prohibit SU1. No Z06 5DH/5DK/PCZ package belongs here.

## 4. Body, roofs, engine and physical equipment

C2Z is the standard coupe removable panel. CFC is the standard convertible
visible-carbon hardtop; neither is a paid Z06-style roof upgrade. ETV is a
995 coupe-only split-window finish. There are no ZR1 D84/D86, EDU/EFY/CBF,
BCW, RXI, Z07 or PDB/PDD/PDF offerings to inherit from the prior lane.

SBT adds another transparent panel and includes SC7 (Exterior 5!34;
Interior 5!40). The workbook includes SC7 through `zr1_rule_mapping!31`, rule
`zr1_rule_sbt_includes_sc7_a92404645c0c`, but has no SC7 zero-price override.
Both coupe trims therefore charge **2,720 instead of 2,525**. SC7 bought first
is absorbed; SBT removal drops it rather than restoring the independent purchase.
The extra physical panel is not an invented CC3 purchase.

B6P and D3V are standard on the coupe; ZZ3 is standard on the convertible;
SL9 is standard with either body package. They appear as informational equipment,
not additional purchases. `zr1_rule_mapping!3,44` and price rules 3–4 preserve
SL9/D3V relationships. PBC is available in both bodies at 9,995, without the
optional-ZZ3 prerequisite of Z06 because ZZ3 is already standard here.
NPP/WUB/NGA are standard; NWI costs 395 and removal restores NGA. E60 at
3LZ supplies TR7 at zero and removes it on loss of the lift option.

**Missing standard information:** inactive rows suppress DY0, CFV, FE8,
3LZ N3W and convertible CFC from the informational equipment list. They are
not lifecycle-unavailable items. Exact workbook rows are 65,113,189,64,116.
EFR is an active but explicitly hidden row (`zr1_options!52`) excluded from
the 200-choice browser universe. Its copied description also mentions rockers
and splitters beyond ZR1's Exterior 5!13 wording.

Do not simply reactivate CFC: dormant `zr1_rule_mapping!5`, rule
`zr1_rule_cfc_includes_gba_dd934a80de02`, maps `opt_cfc_002` → `opt_gba_001`.
Exterior 5!9 says the trim finish changes **when black paint is selected**;
it does not say a standard convertible roof forces black paint. That rule is
the only one of 98 authored direct rows filtered from the emitted 97 rows.
There are no additional derived endpoint triples in this model.

The equipment function filters only by variant. Under ZTK it continues listing
baseline XFR/J58 while configured lines carry XFS/J59. FE8 is absent entirely.
A static trim-information list is not a resolved installed-equipment inventory.

## 5. Paint, stripes, decals, badges and covers

All 14 applicable stripe/paint pairs refuse the second conflicting selection in
both orders and bodies: DUE/DUW/DTC/DPB with GTR; DPC/DT0 with GBK;
DPG/DSY with G26; DPL/DSZ/DUK with GKZ/GPH. This is 56 observed attempts.
There are no ZR1 DZU/DZX stingers. The guide explicitly lists **both DUW and DTC**
(Exterior 5!56,62); keep both pending review rather than extending other models'
DUW retirement. DUE's workbook name says Santorini Blue while its source says
Royal Blue (Exterior 5!54; `zr1_options!186`).

SB9, SFZ and R88 have complete full-length stripe conflict disclosures in
Exterior 5!26:28. Their workbook groups omit `opt_dtc_001`: groups
`zr1_group_sb9_excludes_full_length_stripe_choices`,
`zr1_group_sfz_excludes_badge_and_stripe_choices`, and
`zr1_group_r88_excludes_badge_and_stripe_choices`, rows 4/3/2.

All 14 stripe identities were exercised against these three sources in both
orders and bodies. **SFZ+DTC costs 1,545 and R88+DTC costs 1,990**: both coexist.
SB9 and DTC instead replace each other through section selection, so the missing
explicit group member has a different observed consequence. For existing group
members, graphic-first refuses the stripe; stripe-first silently replaces it
with the graphic. The selection interaction needs owner review separately from
which combinations are permitted. SFZ/SB9 and R88/SFZ were also checked both ways.
EYK is refused after SFZ/R88; the reverse replaces EYK. SB9/EYK coexist.

WKR and RWJ are prohibited with TOM, rather than receiving a Z06-style alternate
high-wing cover. Direct TOM/cover attempts refuse the conflicting second choice
in both orders. ZTK after either cover removes the cover because rows 46–47
explicitly mark replacement; covers after ZTK are refused. Removing ZTK does
not restore the displaced cover. RWH/WKR are exclusive indoor covers; RWJ is
a separate outdoor offering and can coexist with an indoor cover.

ZYC/GBA refuses both orders. 5JR and ZYC each support DRG. Both removal orders
retain DRG until the last cause disappears; charge ownership remains with 5JR
and ZYC, not an extra DRG purchase. Rear script badges, center caps and suede
liners each replace within their own exclusive group.

## 6. Interiors, components, belts and color overrides

The shared LZ charts narrow to **58 trim/seat/color combinations, expanded to 90
leaves**: four 1LZ, 71 ordinary 3LZ and 15 R6X 3LZ. No 2LZ or EL9 is allowed.
All memberships, suede, mandatory/optional stitching and AH2 two-tone expansions
reconcile to inspected chart cells. The model has 127 component memberships and
214 color overrides: 113 paint and 101 belt pairs. All 180 leaf/body contexts
were executed; 900 paint states match the source-derived D30 expectations.

Seat charges are AE4 1,095 at 1LZ and 595 at 3LZ; AH2 is standard at 3LZ;
AUP costs 350 for HAG/HVZ. N26 costs 695 at 1LZ, N2Z 895 at 3LZ, TU7 595,
optional stitch 495 and R6X 995. Same-code prices retain all guide qualifiers.

Four R6X/AE4 leaves omit the 595 seat charge: HUU, HU0/38S, HZP/N2Z and
HXO/N2Z/38S. Source-derived totals are 1,590/2,085/2,485/2,980; observed totals
are 995/1,490/1,890/2,385. `LZ_Interiors!121,124,129,131` and model-qualified
component rows retain the original facts; `zr1_price_rules!5` contains the
ordinary AE4 595 override but does not fix these component-owned paths.

540 interior-first belt attempts retain hard incompatibility reasons, included
belt defaults, paid alternatives and D30 charges. HAG requires blue; HVZ requires
red. Recommended mismatches can incur D30 rather than becoming hard prohibitions.
Two cause-loss sequences using 1LZ HUQ demonstrate a single 1,495 D30 charge
until both paint and belt causes disappear, in either removal order.

AQ9→AE4 at 1LZ selects the sole HTJ/N26 leaf automatically. AH2→AE4 at 3LZ
leaves interior unset and submission disabled. Four missing-interior submission
attempts reject with zero requests. The one-valid-leaf case must not be replaced
with a blanket rule that every seat change clears the interior.

## 7. Accessories, lifecycle and order restrictions

PCQ supplies VWE/VWT at a single 1,675 package charge; PEF supplies CAV/RIA
at 475; PDY supplies RYT/S08 at 195. Each has child-before-package and
package-before-child removal traces in both bodies. Zero-price child ownership
works, but prior independent purchases disappear on removal.

PCQ, VWT, R88 and SLN remain selectable although Exterior 5!22,31,28 and
Mechanical 5!36 say unavailable at this time. V8X is inactive; applicable 3LZ
availability cells alone do not expose it. This needs an explicit lifecycle
policy, separately from standard equipment hidden by inactive flags.

SAI is a guide-only 295 accessory (Interior 5!41; Price Schedule!128), with
V8X conflict on applicable 3LZ cells. The other 18 guide-only codes are six
interior components and twelve service/emissions/territory-order items. They
remain retained with exact disclosures as outside the present customer-selection
scope for review, rather than silently becoming new configurator choices.

R8C/BV4 refuse coexistence; R8C supplies CFX and costs 1,695 once. PBC costs
9,995; PIN costs 5,495. SOLD-only, VIN approval, museum acknowledgement/BAC,
shipping-state VK3 and service/emissions conditions remain disclosures. No
external approval, dealer-order-system constraint or real order acceptance was
executed. All 121 numeric and 86 null offering amounts are classified; a null
source price is not a universal inferred zero. Standard amounts with same-code
paid rates in other models are explicitly distinguished.

## 8. Open owner decisions and expected targets

None of these proposals has been accepted by the discovery request. Each would
require implementation and corrected-runtime verification later.

| ID | Proposed target / decision | Evidence and expected sequence |
|---|---|---|
| ZR1-D01 | Represent all guide-standard equipment; correct dormant CFC→GBA and EFR scope before restoring visibility. | §4; convertible roof must allow all otherwise permitted paints; DY0/CFV/FE8 and 3LZ N3W must appear in appropriate equipment. N2Z replaces N3W in configured content. |
| ZR1-D02 | Apply unavailable lifecycle disclosures to PCQ/VWT/R88/SLN and present applicable V8X disabled. | §7; no acquisition/charge while unavailable, independently of baseline standard-equipment flags. |
| ZR1-D03 | Charge SBT 2,525 with SC7 zero while included. | §4; both coupe trims, either acquisition order, no 195 duplicate charge. |
| ZR1-D04 | Add the missing 595 AE4 charge to four R6X component paths. | §6; expected totals 1,590/2,085/2,485/2,980; no duplicate seat charge on other leaves. |
| ZR1-D05 | Complete DTC membership in all three graphic exclusion groups; choose refusal versus noticed replacement interaction. | §5; SFZ/R88+DTC must not coexist; SB9 must have an explicit rule rather than accidental section replacement. |
| ZR1-D06 | Preserve independent purchase intent through packages and make replacement/removal effects explicit. | TOM→ZTK→remove ZTK retains purchased TOM; SC7/PEF/PDY/PCQ analogues retain independently acquired children. Displaced conflicting covers require a separately explicit restoration policy. |
| ZR1-D07 | Add SAI with its V8X scope; rename DUE to Royal Blue; retain both source-listed DUW and DTC pending explicit owner disposition. | Interior 5!41 and Exterior 5!54,56,62; no imported DUW retirement. |
| ZR1-D08 | Preserve ZR1-qualified base/options, R8E 3,000, ZTK+TOM 18,990 and standard UQT; confirm price basis and operational scope. | §§2–3,7; do not apply ZR1X ZTK rate, Z06 recorder charge or other-model paid standard equipment. |
| ZR1-D09 | Separate static trim information from resolved installed equipment. | ZTK build shows J59/FEJ/XFS instead of J58/FE8/XFR in configured equipment; static information must be labeled and not mistaken for the build. |

## 9. Completion review and cross-model applicability

Existence, applicability, selection/charges, reversal, build consumers and source
versus target are covered together above. Full source rows and numeric qualifiers
are retained; all direct and grouped relationships have family dispositions.
Known baseline defects are investigated findings with open targets, not corrected
behavior. This review does not claim exhaustive possible builds or approval of
business corrections. Owner review remains open.

New model differences were checked against earlier lanes: four configurations,
standard J58/FE8, ZTK J59/FEJ, model-specific TOM, standard engine packages and
explicit DUW+DTC coexistence in the source are ZR1 requirements. Earlier lanes
must not inherit them. Earlier standard-equipment, lifecycle, price ownership,
independent-purchase and DTC concerns already have their own recorded decisions;
this run supplies ZR1 evidence without reopening or changing those decisions.
ZR1's single-column-family scope and repeated TOM identity reinforce the existing
model-qualified provenance rule. ZR1X still needs its own discovery.
