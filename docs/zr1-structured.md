# ZR1 structured discovery handoff

September 10, 2026. Read the [behavior analysis](zr1-behavior.md) with the
[source records](zr1-structured-records.json) and
[executed observations](discovery/zr1-runtime.json). This is a model discovery
handoff with all nine ZR1-D targets accepted September 11, 2026, including explicit
TOM ownership and DUW removal corrections. It is not an implemented dataset or
database schema. Two interaction details remain unresolved in the decision table.

## Record identity and scope

`zr1:<option_id>` is the model-qualified offering identity. `_row` retains the
original Excel row, and each `baseline_rows` key is the owning worksheet.
Guide anchors retain sheet/row/column scope; ZR1 reads D:G and ZR1X H:K.
The frozen workbook, guide and runtime hashes are embedded in the evidence.
There are no duplicate nonempty RPOs within the 207 ZR1 offering records.

| Category | Retained record location / scope |
|---|---|
| Foundations | `variant_master`, `model_variants`: four each; base reconciliation in `source_reconciliation.base_prices` |
| Offerings | `zr1_options`, `offering_dispositions`: 207 each, including six inactive records and hidden EFR |
| Availability | `zr1_ovs`: 828 option/configuration pairs; no variant overrides |
| Guide correspondence | 171 coded matches / 684 status pairs; 26 uncoded equipment mappings; ten paints; 195 applicable repeated coded rows |
| Guide disclosures | `guide_rows`: original wording and both model column scopes across the five family sheets, including ZR1X-only rows marked inapplicable |
| Guide-only facts | `guide_only_dispositions`: 19; SAI addition accepted under D07 (frozen disposition remains `open_addition`), six interior components, twelve service/emissions/territory codes outside customer scope for review |
| Interiors | `LZ_Interiors`, `model_interior_scope`, `interior_source_links`: 90 each; 127 component memberships; 58 raw chart combinations expand to exactly these 90 leaves |
| Direct relationships | `zr1_rule_mapping`: 98; `direct_rule_translation`: 97 emitted, dormant CFC→GBA filtered; no extra derived triples |
| Grouped constraints | Five groups / 44 member rows; nine exclusive groups / 24 members; missing DTC membership remains explicit |
| Price ownership | 34 price rules, 214 model-qualified color overrides, 21 retained shared PriceRef lookup rows; 121 numeric / 86 null offering rates with schedule qualifiers |
| Defaults | Six authored default-selection rows plus section/standard behavior |
| Presentation | 33 referenced sections, eight section-presentation rows, 14 runtime steps, two context sections, three scoped/wildcard context-copy rows, 12 summary sections, 14 step mappings and 69 asset rows |
| Source routing | One model, one promotion, 11 workbook source routes; six phrase mappings and no runtime exceptions |
| Runtime universe | 800 observations = 200 eligible browser rows × four configurations; 396 enabled attempts. Six inactive records and one explicitly hidden EFR account for the other seven offerings |
| Connected output | 354 sequences / 826 action states, each beginning with valid paint/interior and carrying order/recap/equipment projections |
| Interior output | 180 body/leaf states, 90 price comparisons, 900 paint states, 540 belt attempts, two D30 multiple-cause sequences |
| Required input | Four seat transitions, four missing-interior rejection attempts, one body/trim reset; zero requests |

Amounts and record counts describe frozen evidence. They do not prove source
acceptance or future resolved-build correctness. Standard/null/zero and matching
same-code prices retain separate classifications. The guide price header ambiguity
is preserved; the working numeric interpretation remains column E plus qualifiers.

## Relationship families and evidence routes

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
cannot share an unqualified “installed equipment” meaning.

## Accepted targets

[ZR1-D01–09](zr1-behavior.md#8-open-owner-decisions-and-expected-targets) preserve
source facts, observed defects, accepted targets and expected future sequences.
The behavior document is the current owner-decision record. The source JSON is
an unchanged discovery snapshot: its empty `owner_review` and original role and
disposition wording describe the September 10 extraction, not current approval.
It must be read with the September 11 decisions, including DUW removal despite
the retained source listing. D05 interaction and D06 displaced-cover restoration
remain unresolved as specified there. No accepted target was run against a
modified form; source/probe verification is not corrected-runtime verification.

## Reproduce

From the repository root, using Python with openpyxl and Node:

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/seandm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/zr1_discovery.py .local/zr1-source-new
node scripts/zr1_discovery.mjs .local/zr1-runtime-new
```

Both commands refuse to overwrite their primary result. The Python extractor
reads the immutable workbook and locally retained raw guide, checks manifest
member hashes, model-specific status/text correspondence, uncoded availability,
interior expansion, price accounting, base rates and direct rule emission. Its
primary result is `zr1-structured-records.json`. The Node probe extracts the
frozen app/registry and reads the harness from the pinned reference commit;
it does not use the current working copy's runtime. It writes `zr1-runtime.json`,
with source and probe hashes and zero-request evidence. Embedded assertions
cover source-backed prices/availability plus explicitly known baseline defects.
A known-defect assertion preserves the observed baseline, not a target approval.

Fresh source records reproduced the tracked JSON exactly. Fresh runtime results
reproduced every retained value except `compact.submitted_at`, the deliberately
variable recap timestamp. List order and all other fields remain significant.
No unrelated model evidence was regenerated. Visual browser layout, real customer
submission and corrected-runtime behavior were not tested because this task
changes discovery evidence only.
