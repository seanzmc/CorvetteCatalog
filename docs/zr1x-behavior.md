# ZR1X model discovery

Frozen source and browser evidence at reference `4fe92a4f078370c478f18484cad31bdafe58ad43`.
This is discovery of the archived form, not verification of the current app.
All ZR1X owner decisions below are open. No correction has been accepted or implemented.

## 1. Sources, identities and completeness

Use [structured records](zr1x-structured-records.json),
[accounting](discovery/zr1x-accounting.json), and
[runtime observations](discovery/zr1x-runtime.json) together.
The workbook hash is `3127e663b1531e366ce86b989b6190914108d40dfd15a33a258307a05d608e3c`;
the guide hash is `d3ca7d3a09c9fb89210b4ce584493b3ad8fb65ca35087c49d816d1cbf1a333d1`.
Original worksheet headers, nulls, IDs, inactive rows and `_row` locators remain intact.
Shared guide sheets 5 use **H:K for ZR1X**; D:G are ZR1 context only.
In particular, numbered J59/ZTK footnote 1 belongs to ZR1's columns, while
ZR1X has standard J59 and ZTK footnote 2. Do not infer applicability from the
shared disclosure text alone.

The extractor reconciles 206 offerings: 170 coded matches, 26 explicitly mapped
uncoded equipment rows and ten paints. All 824 availability rows are retained;
680 primary coded comparisons and 194 repeated coded occurrences match the guide.
All 90 interior leaves, 127 component memberships and 214 color-override rows
reconcile with the LZ color/trim source. No duplicate RPOs were found within ZR1X.
All 96 direct rule rows are emitted; no additional direct endpoint triples are
derived by the archived runtime. Four grouped rules/43 members, eight exclusive
groups/22 members, 33 conditional-price rows and six default rules remain separate
source structures, not unexamined substitutes for the direct-rule count.

The 19 guide-only records comprise SAI, six interior component codes, and twelve
service/emissions/order-type offerings outside the baseline customer-selection
scope. This is an explicit scope disposition for owner review, not evidence that
the manufacturer removed those offerings. SAI is an omitted customer accessory;
TU7/N26/N2Z/36S/37S/38S are represented through interior components.

## 2. Model, body, trim and price foundations

| Configuration | Workbook base including 2,495 destination | Frozen starting total including 2,600 R8E | Guide base anchor |
|---|---:|---:|---|
| `1lz_s07` coupe | 227,395 | 229,995 | Price Schedule!F38:J38 |
| `3lz_s07` coupe | 238,395 | 240,995 | Price Schedule!F40:J40 |
| `1lz_s67` convertible | 237,395 | 239,995 | Price Schedule!F39:J39 |
| `3lz_s67` convertible | 248,395 | 250,995 | Price Schedule!F41:J41 |

Foundations still require paint/interior. Connected cases supply valid G8G and an
ordinary trim-qualified interior before exercising options. AQ9 is the 1LZ seat;
AH2 is the 3LZ seat. Defaults include EYT, J6D, T0E, 719, J59, SOJ, NGA, EFR and R8E.
Source standard equipment includes LT7, HP1, MLP and XFR. HP1's workbook copy already
says 186 front-axle hp and 1,250 combined with LT7; the unrelated GSX/LS6 correction
must not be imported. J58, FE8, FEJ, M1K and SIG are not ZR1X offerings.

Every option amount is classified: 118 numeric and 88 null; 65 direct rate matches,
28 matches retaining qualifiers, 16 zeros without schedule rates, and nine
standard-equipment amounts that are not another model's purchase price. Null is
not inferred zero. The accounting retains all same-code schedule candidates and
their column-D qualifiers, even when another model has a different rate.
Column E is the observed option-price basis. USD remains proposed for this lane,
not separately confirmed by the owner (D08).

Source distinctions include 3LZ-only E60 at 2,995 (Price Schedule row 50), standard
UQT with no selectable purchase, ZR1X R8E at 2,600 (row 199), TOM at 12,995
(row 193), and ZR1X ZTK at 1,500 (row 231). ZR1's 5,995 ZTK and 3,000 tax do not apply.
PriceRef and the 33 conditional rules govern seat/component and included-child
charges; rate agreement alone does not establish correct build arithmetic.

## 3. Performance, aero, wheels and physical equipment

`zr1x-C295`/C308/C321/C334 exercise ZTK, attempted T0E, J59 and removal in all
four configurations. ZTK adds FEZ, XFS and TOM for **14,495**, blocks T0E, and leaves
standard J59 independently selected. Removal restores T0E and removes package
content/charges without losing J59 or the interior. A paid caliper survives the
round trip. The default suspension FEH is source-standard but globally inactive;
it is absent from starting choices and informational equipment (D01).

`zr1x-C296` and the corresponding other variants show a different ownership issue:
TOM selected first costs 12,995; adding ZTK costs 14,495 in total; removing ZTK
loses that independently selected TOM and returns to T0E. The future ownership
proposal is D06, not an inherited accepted ZR1 decision.

Both bodies exercise all five wheel choices, black/chrome lug nuts and locks,
carbon wheels first, and exclusive center caps. SPZ requires SPY; S47 and SFE
conflict with SU1, and S47 conflicts with SPY. Selected replacement wheels own
their rate; standard SOJ restores zero. E60 is hidden/unavailable at 1LZ, available
at 3LZ, includes TR7 and removes it with the lift. ETV is coupe-only; UQT and
body-qualified B6P/ZZ3 are display-only. Engine appearance and SL9 are standard
physical content rather than new paid purchases. NWI replaces NGA for 395;
removal restores NGA.

CFC is standard on convertibles and visible in static equipment. Its emitted
`CFC includes GBA` rule (mapping row 5) contradicts the guide's conditional trim
description: Exterior 5!A9:K9 does not require black exterior paint. The archived
display-only CFC is not acquired by the probe; correcting this latent relationship
before promoting standard content is an open target, not a demonstrated forced
paint change. DY0 and CFV already appear in ZR1X static equipment; do not inherit
ZR1's missing-visibility finding for those codes.

## 4. Paint, graphics, badges, mirrors and covers

The probe exercises all 56 listed stripe/paint prohibition directions across both
bodies, and 180 graphic/stripe-or-badge interactions. All listed paint conflicts
refuse the second choice in the frozen form. That observation remains separate
from the already accepted common notice/confirm/cancel interaction policy.

DTC is absent from all three grouped graphic exclusion memberships even though
the guide names it. SFZ+DTC coexist for 1,545 (`zr1x-C075/C076`), and R88+DTC coexist
for 1,990 (C105/C106), in both acquisition orders and both bodies. SB9 and DTC
replace each other via their section (C045/C046); this does not prove the missing
group relationship exists. D05 proposes complete membership with the common UI
policy. DUW and DTC both exist in the source. Removing DUW from ZR1 is not authority
to remove it here. DUE's workbook Santorini Blue name differs from the guide's
Royal Blue wording (Exterior 5 row 54); D07 keeps that discrepancy explicit.

Both mirror cause-removal orders retain DRG until the last of 5JR/ZYC is removed.
GBA conflicts are tested in both directions. Independent badges, covers, compartment
liners and wheel caps exercise their exclusive groups. FA5/FA6 share their own
exclusive group; FA6 is unavailable at 1LZ and replaces FA5 at 3LZ.

RWJ/WKR versus TOM/ZTK are tested in both acquisition orders and bodies.
TOM is refused after a conflicting cover, and a cover is refused after TOM.
ZTK after a cover removes the cover; removing ZTK does not restore it or its charge
(C125–C132 and convertible counterparts). Clicking selected TOM itself does not
deselect that radio-like aero choice; T0E provides the ordinary replacement path.
D06 proposes explicit purchase ownership and no automatic displaced-cover restoration.

## 5. Interiors, belts and price consequences

All 90 leaves are executed in both bodies (180 complete-context snapshots), with
900 paint cases and 540 belt cases. ZR1X records these under the common
`connected_sequences` shape rather than adding ZR1's six camelCase exception keys.
Each case retains order sections, item prices/types/routing, compact recap,
configured selections and static informational IDs.

Color-source expansion and all 214 incompatible interior/paint pairs reconcile;
the 900 runtime paint states agree with the source D30 applicability. Belt cases
exercise ordinary paid alternatives, zero-price included belts and hard-exclusive
asymmetrical interiors. All 30 refusals match direct workbook exclusions; all 510
allowed cases have the expected belt charge from option/conditional-price rows.
For example, HVZ rejects 379 and retains free 3F9
(C1066/C1069). HUQ+379 adds both 595 belt and 1,495 D30, while HUQ+3F9 does not add
D30 (C400/C403). Two independent paint/belt cause-removal orders show D30 survives
one remaining cause and disappears after the last cause is removed.

The 90 interior charge comparisons agree except four 3LZ R6X/AE4 leaves:

| Runtime case | Interior | Source-qualified expected | Observed | Difference |
|---|---|---:|---:|---:|
| C1773 | `3LZ_R6X_AE4_HUU` | 1,590 | 995 | −595 |
| C1827 | `3LZ_R6X_AE4_HU0_38S` | 2,085 | 1,490 | −595 |
| C1917 | `3LZ_R6X_AE4_HZP_N2Z` | 2,485 | 1,890 | −595 |
| C1953 | `3LZ_R6X_AE4_HXO_N2Z_38S` | 2,980 | 2,385 | −595 |

Expected values use PriceRef rows 12/14/18/20/22 and the retained component links;
Price Schedule!B238:E239 distinguishes 3LZ and 1LZ AE4 rates. The component paths
omit the separate 595 seat charge (D04). Other leaves must not receive a duplicate
seat charge. Inactive N3W is missing from 3LZ static equipment despite its standard
guide status; N2Z's configured replacement requires owner review in D01.

## 6. Packages, accessories, delivery and lifecycle

Both acquisition orders and removal run for PCQ/VWE, PEF/CAV and PDY/RYT in each
body. Included children have zero charges; the package owns its amount. However,
adding a package absorbs an independently purchased child; removing the package
loses that child (C119–C124). Both coupe trims also exercise SC7 before/after SBT:
SBT adds 2,720 instead of its 2,525 rate because included SC7 still charges 195
(C347–C350). D03 fixes the duplicate-charge proposal; D06 separately addresses
independent purchase retention.

Factory-unavailable disclosures exist for PCQ, VWT, R88, SLN and V8X. The first
four are nevertheless selectable in applicable frozen contexts; V8X is globally
inactive although its availability is 3LZ-only. D02 proposes consistent disabled
presentation for applicable unavailable offerings; unavailable lifecycle must not
be confused with selectable compatibility conflicts.

R8C supplies CFX and conflicts with BV4 in both directions; PBC is a separate
9,995 purchase with a complete round trip. Free-floating accessories are covered
by the full active-offering sweep, with grouped liner/badge/cap cases for shared
selection behavior. Dealer, subscription, emissions and region/order-type
conditions remain source disclosures and explicitly excluded baseline purchase
scope, pending D08; the probe does not execute those external workflows.

## 7. Build output and limits

All 1,973 connected case starts are complete. The run retains 2,259 action states,
812 observations covering every active offering in all four variants, four seat
transitions, four missing-interior rejection cases, and a coupe 3LZ → convertible
1LZ reset. There are zero live requests. No exhaustive whole-build claim is made:
each family uses its own conditions, complete source accounting and stated
representative acquisition/removal cases.

Static standard-equipment lists still describe the trim while a ZTK build carries
XFS/FEZ/TOM. They must not be mistaken for installed content (D09). Workbook
presentation rows, 14 runtime steps, 12 order sections and all routing metadata
remain in the source file; the snapshots show their actual pricing/recap consumers.
The current form, corrected targets, production submission and visual rendering
have not been verified by this pass.

## 8. Open owner decisions and expected targets

The [owner overlay](zr1x-owner-decisions.json) is the decision authority record.
Every decision is **open**; proposed additions and non-default targets have no
effect until the owner accepts them. The common compatibility UI policy is already
accepted across models, but it does not accept these ZR1X facts or corrections.

| Decision | Proposal or unresolved choice | Evidence |
|---|---|---|
| ZR1X-D01 | Restore source-standard FEH/N3W in the correct configured scope; resolve CFC→GBA before promoting standard content | Mechanical 5!A45:K45; Interior 5!A80:K80; Exterior 5!A9:K9; options rows 64/165/188; mapping row 5; foundations |
| ZR1X-D02 | Apply factory-unavailable presentation to PCQ/VWT/R88/SLN and applicable V8X | Exterior 5 rows 22/28/31; Mechanical 5 row 36; Interior 5 row 42; starting-choice observations |
| ZR1X-D03 | SBT costs 2,525 with included SC7 at zero | Exterior 5!A34:K34; C347–C350 |
| ZR1X-D04 | Restore missing 595 AE4 charge on four R6X leaves | PriceRef rows 12/14/18/20/22; C1773/C1827/C1917/C1953 |
| ZR1X-D05 | Complete DTC graphic exclusions under the common compatibility UI policy | Exterior 5 rows 26–28; group memberships; C045/C046/C075/C076/C105/C106 |
| ZR1X-D06 | Preserve independently purchased TOM/children through packages; do not restore displaced covers automatically | C119–C132, C296/C309/C322/C335, C347–C350 |
| ZR1X-D07 | Add SAI at 295 with V8X exclusion; rename DUE Royal Blue; decide DUW independently, retaining it provisionally | Interior 5 row 41; Price Schedule row 128; Exterior 5 rows 54/56/62 |
| ZR1X-D08 | Confirm currency, model-qualified prices, HP1/LT7 copy and customer-selection boundary | Price Schedule rows 38–41/50/193/199/231/238–239; Mechanical 5 row 25; guide-only dispositions |
| ZR1X-D09 | Distinguish static trim information from resolved configured equipment | Foundations and ZTK states C295/C308/C321/C334 |

No master-schema design, migration, DDL, canonical change, deployment or cutover
is authorized by this handoff. Source-derived requirements are inputs to a later
six-model review after these open owner decisions are considered.
