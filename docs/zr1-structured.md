# ZR1 structured handoff

**September 11 shared policy:** the [owner overlay](zr1-owner-decisions.json)
references the [common structured compatibility policy](compatibility-notice-policy.json)
at `owner_review.compatibility_notice_policy.$ref` (relative to the overlay).
Read that policy after each model's historical decisions; it governs compatibility
UI only, preserving model-specific constraints and frozen evidence.

September 10, 2026 discovery; all nine ZR1-D targets accepted September 11, 2026,
including explicit TOM ownership and DUW removal corrections. Read the
[behavior analysis](zr1-behavior.md) with the [source records](zr1-structured-records.json),
[price and rule accounting](discovery/zr1-accounting.json),
[executed observations](discovery/zr1-runtime.json) and the
[structured owner overlay](zr1-owner-decisions.json). This is a model discovery
handoff in the [common handoff contract](model-discovery.md#handoff-contract);
it is not an implemented dataset, database schema or corrected runtime.

## 1. Record conventions and evidence

| Convention | Meaning |
|---|---|
| Identity | `zr1:<option_id>` is the model-qualified offering identity; the addition uses `zr1:proposed:SAI`. Workbook and browser key are both `zr1`. |
| Rows | `_row` retains the original Excel row; each `baseline_rows` key is the owning worksheet and `sheet_roles` names the generic role of each model sheet. |
| Guide scope | Anchors retain sheet/row/column scope. ZR1 reads columns D:G; H:K are retained in `guide_rows` as ZR1X context, not ZR1 facts. |
| Prices | USD by the shared Price Schedule; column E with D qualifiers, accepted as the numeric basis in ZR1-D08. Null is unknown evidence, not a universal zero. |
| Evidence and target | Source rows, accounting and observations are frozen. Accepted targets live only in the owner overlay; expected sequences there are not executed correction tests. |

| Evidence | Identity / locator |
|---|---|
| E-W | [Frozen workbook](../baselines/2026-09-06/README.md), SHA-256 `3127e663b1531e366ce86b989b6190914108d40dfd15a33a258307a05d608e3c`. |
| E-G | [Guide provenance](../sources/README.md), SHA-256 `d3ca7d3a09c9fb89210b4ce584493b3ad8fb65ca35087c49d816d1cbf1a333d1`; Interior/Exterior/Mechanical 5, Standard Equipment/Equipment Groups 5, qualified Color and Trim and Price Schedule. |
| E-O | Frozen browser revision `4fe92a4f078370c478f18484cad31bdafe58ad43`, exercised with DOM/network stubs; zero requests. Probe and harness hashes are embedded in the runtime evidence. |
| E-B | [Full behavior analysis](zr1-behavior.md), §§1–9. |
| E-A | September 11 owner approvals, recorded in E-B §8 and in the overlay's `owner_review.records`. |

There are no duplicate nonempty RPOs within the 207 ZR1 offering records.

## 2. Complete record sets and how to use them

| Category | Retained record location / scope |
|---|---|
| Foundations | `variant_master`, `model_variants`: four each; base reconciliation in `source_reconciliation.base_prices` |
| Offerings | `zr1_options`, `offering_dispositions`: 207 each, including six inactive records and hidden EFR |
| Availability | `zr1_ovs`: 828 option/configuration pairs; no variant overrides |
| Guide correspondence | 171 coded matches / 684 status pairs; 26 uncoded equipment mappings; ten paints; 195 applicable repeated coded rows |
| Guide disclosures | `guide_rows`: original wording and both model column scopes across the five family sheets, including ZR1X-only rows marked inapplicable |
| Guide-only facts | `guide_only_dispositions`: 19; one omitted offering (SAI, accepted under D07), six interior components, twelve service/emissions/territory codes outside customer scope |
| Interiors | `LZ_Interiors`, `model_interior_scope`, `interior_source_links`: 90 each; 127 component memberships; 58 raw chart combinations expand to exactly these 90 leaves |
| Direct relationships | `zr1_rule_mapping`: 98; accounting `direct_rule_translation`: 97 emitted, dormant CFC→GBA filtered; `runtime_derived_relationships` is empty |
| Grouped constraints | Five groups / 44 member rows; nine exclusive groups / 24 members; missing DTC membership remains explicit |
| Price ownership | 34 price rules, 214 model-qualified color overrides, 21 retained shared PriceRef lookup rows; accounting `option_prices`: 121 numeric / 86 null offering rates with schedule qualifiers |
| Defaults | Six authored default-selection rows plus section/standard behavior |
| Presentation | 33 referenced sections, eight section-presentation rows, 14 runtime steps, two context sections, three scoped/wildcard context-copy rows, 12 summary sections, 14 step mappings and 69 asset rows |
| Source routing | One model, one promotion, 11 workbook source routes; six phrase mappings and no runtime exceptions |
| Runtime universe | 800 observations = 200 eligible browser rows × four configurations; 396 enabled attempts. Six inactive records and one explicitly hidden EFR account for the other seven offerings |
| Connected output | 354 sequences / 826 action states, each beginning with valid paint/interior and carrying order/recap/equipment projections |
| Interior output | 180 body/leaf states, 90 price comparisons, 900 paint states, 540 belt attempts, two D30 multiple-cause sequences |
| Required input | Four seat transitions, four missing-interior rejection attempts, one body/trim reset; zero requests |
| Decisions | Overlay `owner_review.records`: nine accepted; `offering_targets`: one per offering; `accepted_additions`: SAI; `model_policies.displaced_cover_policy` |

Amounts and record counts describe frozen evidence. They do not prove source
acceptance or future resolved-build correctness.

## 3. Configurations and offering scope

ZR1 has four configurations, not six: coupe and convertible at 1LZ and 3LZ
(`variant_master!26:29`). Bases including destination are 197,195 / 208,195 /
207,195 / 218,195, reconciled to Price Schedule 34/36/35/37 (F + J); R8E is a
separate 3,000 default line. J58, J6D, SOJ, T0E, EYT, NGA and black 719 begin
selected; AQ9 starts at 1LZ and AH2 at 3LZ; paint and interior start unset.
Body/trim change resets the build (E-B §2).

All 207 offerings have a source disposition: 171 coded guide matches, 26 uncoded
standard-equipment matches and ten paints. Six records are inactive and EFR is
active but hidden, so the browser universe is 200 rows in each of the four
contexts. HP1, FEH/FEZ and MLP appear on the shared sheets but are ZR1X-only;
their presence creates no ZR1 offering (E-B §1). Lifecycle facts are separate:
PCQ/VWT/R88/SLN are selectable in the baseline despite guide "unavailable at this
time" notices, and inactive V8X has applicable 3LZ cells (E-B §7, ZR1-D02).

## 4. Price ownership and interpretation

Every offering amount is classified in `discovery/zr1-accounting.json`: 121 numeric
and 86 null. Same-code schedule rows keep their qualifiers; nine standard items
(B6P, ZZ3, D3V, SL9, DY0, CFV, C2Z, CFC, AH2) are classified as standard equipment,
not purchases at another model's paid rate. UQT is standard at both trims; the
dormant 1LZ 1,495 rule (`zr1_price_rules!12`) is not a ZR1 recorder charge. The
guide's 1,500 ZTK rate is ZR1X-only; ZR1 ZTK costs 5,995 and requires TOM 12,995,
so ZTK from the starting configuration adds 18,990 (E-B §§2–3, ZR1-D08).

Package and component ownership: PCQ 1,675, PEF 475 and PDY 195 supply their
children at zero; R8C supplies CFX at 1,695 once; E60 supplies TR7 at zero. SBT
includes SC7 without a zero override, charging 2,720 instead of 2,525 (ZR1-D03).
Seat charges are AE4 1,095 at 1LZ / 595 at 3LZ, AH2 standard at 3LZ, AUP 350;
N26 695, N2Z 895, TU7 595, optional stitch 495, R6X 995. Four R6X/AE4 leaves omit
the 595 seat charge (`LZ_Interiors!121,124,129,131`; ZR1-D04). D30 is a single
1,495 charge until both paint and belt causes disappear (E-B §6).

## 5. Connected relationship records

| Family | Workbook ownership | Source / executed evidence |
|---|---|---|
| ZTK and aero/brakes | Direct rows 39–41,45; groups 5–6; brake/aero exclusive groups | Mechanical 5!6:7,43:50; each configuration has ZTK→T0E/J58 refusal→removal and TOM→ZTK→removal |
| Covers and aero | Direct rows 28,38,46–47; indoor cover group | Exterior 5!24:25; both covers, both bodies, both acquisition orders with TOM and ZTK |
| Wheels/hardware/calipers | Direct rows 29–30,32–33,36–37; wheel/caliper sections | Exterior 5!39:44,70:74; four wheel round trips and both hardware acquisition orders; J6O survives ZTK |
| Graphics and paint | Direct rows 6–19,34; groups 2–4; stripe/badge sections | Exterior 5!26:28,54:67; all 14 stripe/paint prohibited pairs and all 14 full-length stripe identities against SB9/SFZ/R88 |
| Mirrors | Direct rows 2,42–43 | Exterior 5!32,45:46; both cause-removal orders and both GBA conflict orders |
| Roof package | Direct row 31; missing SC7 price override | Exterior 5!34, Interior 5!40; both coupe trims and package/child orders |
| Engine/body equipment | Direct rows 3,5,44; price rows 3–4; option activity/presentation | Mechanical 5!24:38, Exterior 5!9,14,49; body-qualified output, PBC, ETV, NWI and dormant CFC finding |
| Lift and interior trim | Direct row 20; trim section/exclusive group | Exterior 5!15,18, Interior 5!88:92; all four contexts, FA5/FA6 and BAZ coexistence |
| Accessory packages | Direct rows 21–26; price rows 6–11 | Interior 5!27:38, Exterior 5!22,30:31; both package/child orders, both bodies |
| Delivery/plaque | Direct rows 4,27 | Exterior 5!10:11, Interior 5!55:56; refusal, supplier and charge output |
| Interiors/belts | Direct rows 48–99; price rows 14–35; exact scoped leaves/components/color overrides | Interior 5!60:87 and Color and Trim charts; complete leaf/body, paint and belt observations |
| Equipment/lifecycle/defaults | Option active/display behavior, availability, default rules, standardEquipment output | Full starting-choice observations, foundations, inactive source accounting and accepted ZR1-D01/02/09 |
| Remaining independent accessories | Offering scope and four accessory exclusive groups | Complete active-choice sweep; covers, cap, script and suede-liner replacement sequence |

The detailed source IDs, target IDs and rule IDs are retained on each row.
Rule-group membership is independent from section exclusivity: SB9/DTC's observed
replacement does not repair its missing member row. Direct inclusion is independent
from zero pricing: SBT includes SC7 but still double-charges it. Static equipment
is independent from configured line items: ZTK demonstrates why those consumers
cannot share an unqualified "installed equipment" meaning. The dormant
`zr1_rule_mapping!5` CFC→GBA row is the only direct row filtered from the emitted
contract; there are no derived endpoint triples.

## 6. Selection and reconciliation policies

Observed baseline policies, retained as evidence (E-B §§3–7):

- Package acquisition supplies children at zero; a child bought first is absorbed
  and package removal drops it. TOM→ZTK→remove ZTK loses the original TOM purchase.
  ZR1-D06 accepts the future policy: independently acquired children and
  TOM-before-ZTK survive removal; package-supplied TOM is removed with ZTK.
- Stripe/paint pairs refuse the second conflicting choice in both orders and bodies
  (56 attempts). Graphic-first refuses a stripe; stripe-first silently replaces it.
  SFZ+DTC and R88+DTC coexist because DTC is missing from the three graphic groups
  (ZR1-D05). The common compatibility-notice policy supersedes the refusal UI.
- Covers: TOM refuses WKR/RWJ in both orders; ZTK after a cover removes it, covers
  after ZTK are refused, and ZTK removal does not restore the displaced cover. The
  overlay's `displaced_cover_policy` accepts no automatic restoration.
- Multiple causes: DRG (5JR/ZYC) and D30 (paint/belt) persist until the last cause
  disappears, in either removal order.
- Seat transitions: AQ9→AE4 at 1LZ auto-selects the sole HTJ/N26 leaf; AH2→AE4 at
  3LZ leaves the interior unset and submission disabled. Four missing-interior
  submissions reject with zero requests. The one-valid-leaf case is not a blanket
  "clear interior on seat change" rule.
- Defaults: six authored default rows; R8E is a default line; NWI removal restores
  NGA; E60 loss removes supplied TR7; ZTK removal restores J58/T0E.

## 7. Presentation, physical content and operational boundaries

The informational equipment function filters by variant only. Inactive rows
suppress DY0, CFV, FE8, 3LZ N3W and convertible CFC (`zr1_options!65,113,189,64,116`)
although they are not lifecycle-unavailable; EFR is active but hidden
(`zr1_options!52`). Under ZTK the static list still shows XFR/J58 while configured
lines carry XFS/J59 (ZR1-D01, ZR1-D09). B6P/D3V (coupe), ZZ3 (convertible) and
SL9 appear as informational equipment, not purchases. Presentation rows: 33
referenced sections, eight section-presentation rows, 14 runtime steps, 12 summary
sections, 14 step mappings, three context-copy rows and 69 asset rows.

Order restrictions remain disclosures, not executed constraints: SOLD-only, VIN
approval, museum acknowledgement/BAC, shipping-state VK3 and service/emissions
conditions. No external approval, dealer-order-system constraint, live submission
or visual browser QA was executed.

## 8. Decision overlay: source, baseline and target remain separate

The source records, accounting and runtime files are unchanged discovery
snapshots. The [owner overlay](zr1-owner-decisions.json) retains all nine accepted
ZR1-D01–09 records with authority, evidence and expected sequences, one
`offering_targets` entry per offering, the SAI `accepted_additions` record, the
displaced-cover policy and the common compatibility-card policy reference. The
[behavior decision table](zr1-behavior.md#8-open-owner-decisions-and-expected-targets)
carries the same targets. No decision details remain open.

Overlay dispositions derived from the accepted decisions: DUW `retire` and DUE
`rename` to Royal Blue (D07); PCQ/VWT/R88/SLN/V8X `visible_unavailable` (D02);
every other offering `retain_subject_to_decision_overlay`, linked to each decision
whose target names its code. The guide still lists both DUW and DTC (Exterior
5!56,62); DUW removal is an owner correction, not a source fact. No accepted
target was run against a modified form; source/probe verification is not
corrected-runtime verification.

## 9. Worked sequences and expected outcomes

Executed baseline sequences are in `discovery/zr1-runtime.json` (`connected_sequences`,
354 cases / 826 action states, each starting from valid paint/interior with
order, recap and equipment projections). Representative frozen outcomes:

| Sequence | Observed baseline | Governing target |
|---|---|---|
| ZTK from start, any configuration | +18,990 (TOM 12,995 + ZTK 5,995); J59/FEJ/XFS at zero; removal restores J58/T0E and the starting total | D08, D09 |
| TOM → ZTK → remove ZTK | Returns to baseline; original TOM purchase lost | D06: TOM retained at its standalone charge |
| SBT at either coupe trim, either order with SC7 | 2,720 | D03: 2,525 with SC7 zero |
| R6X/AE4 leaves HUU, HU0/38S, HZP/N2Z, HXO/N2Z/38S | 995 / 1,490 / 1,890 / 2,385 | D04: 1,590 / 2,085 / 2,485 / 2,980 |
| SFZ+DTC, R88+DTC | Coexist at 1,545 / 1,990 | D05: exclusion with compatibility notice |
| WKR or RWJ, then ZTK, then remove ZTK | Cover displaced, not restored | D06 and `displaced_cover_policy`: stays deselected |
| PCQ/VWT/R88/SLN selection | Selectable and charged | D02: fully inactive with factory disclosure |
| 1LZ HUQ paint/belt D30, either removal order | Single 1,495 until both causes gone | Retained |
| AH2→AE4 at 3LZ, then submit | Interior unset; rejected, zero requests | Retained |

Expected target outcomes are stated, not executed.

## 10. Coverage and handoff boundary

All six completion questions have model-specific evidence (E-B §9): existence and
provenance, effective availability, selection and charge ownership, reversal and
independent causes, build consumers, and source versus target. Cross-model checks
applied here: four configurations, standard J58/FE8, ZTK J59/FEJ, model-specific
TOM, standard engine packages and explicit DUW+DTC source coexistence are ZR1
evidence; earlier lanes must not inherit them, and their existing decisions are
not reopened. ZR1X still needs its own discovery.

Reproduce from the repository root, using Python with openpyxl and Node:

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/seandm/Projects/27vette/.venv/bin/python scripts/model_discovery.py zr1 .local/zr1-source-new
node scripts/model_discovery.mjs zr1 .local/zr1-runtime-new
python3 scripts/validate_handoffs.py --lane zr1
```

Both discovery commands refuse to overwrite their primary result. The Python
extractor reads the immutable workbook and locally retained raw guide, checks
manifest member hashes, model-specific status/text correspondence, uncoded
availability, interior expansion, price accounting, base rates and direct rule
emission, and writes `zr1-structured-records.json` plus `zr1-accounting.json` in
the contract shape. The Node probe extracts the frozen app/registry and reads the
harness from the pinned reference commit; it writes `zr1-runtime.json` with source
and probe hashes and zero-request evidence. The validator checks all lane files
against the [handoff contract](discovery/handoff-schema.json). Fresh source
records reproduced the tracked JSON exactly at the September 10 extraction; fresh
runtime results reproduced every retained value except `compact.submitted_at`.
