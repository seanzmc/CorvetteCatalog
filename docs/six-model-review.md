# Consolidated six-model discovery review

September 13, 2026. Reviewed repository baseline: `4e23ce35ffb8495fa552eebb18ca9c9443ff0e72`.

**Outcome: the six model lanes provide sufficient discovery evidence to proceed to
one master-schema design.** No additional model-wide discovery pass or repeated
approval of the 72 recorded decisions is needed. The existing disposable schema
and the historical Stingray proposal are not ready to adopt unchanged. The design
must address the ownership and translation requirements below before implementation.
This review does not implement corrections or approve DDL, an application or cutover.

## Evidence and authority

Each lane was reviewed using its behavior report, structured handoff, source records,
price/rule accounting, frozen runtime observations and owner overlay. The
[discovery index](model-discovery.md#current-model-handoffs) links all six-file sets.
The six completion questions govern this review; inventory totals alone do not
establish completion. Original family analyses and supplemental observations remain
part of the evidence, including cases not represented in the common runtime layout.

Apply the evidence in this order:

1. Frozen guide/workbook rows and runtime observations establish what was supplied
   and what the baseline did. They retain defects, dormant records and contradictions.
2. Each model's accepted owner overlay establishes its target departures. A default
   `retain_subject_to_decision_overlay` offering target is not an assertion that all
   of that offering's relationships or charges remain unchanged.
3. The [shared compatibility policy](compatibility-notice-policy.json) applies last
   to interaction behavior. It does not share products, prices or exclusion sets.

All six overlays have USD, option schedule column E, accepted decision records and
empty `unresolved_decisions` lists. This establishes the recorded decision status,
not an executed target dataset. Historical paragraphs saying that later lanes are
unfinished, currency is unknown or Z06 still has two UI alternatives are superseded
by those overlays and the September 13 roadmap entry.

## Six-lane accounting and completion

Numbers below were checked against the JSON records, accounting and runtime files.
Interiors are model-scoped leaves; summing them does not establish global uniqueness.

| Lane | Configurations | Offerings / availability pairs | Interior leaves | Numeric / null option amounts | Workbook direct rules → emitted source rules (+ derived) | Accepted decisions |
|---|---:|---:|---:|---:|---:|---:|
| Stingray | 6 | 242 / 1,452 | 130 | 150 / 92 | 178 → 147 (+0) | 12 |
| Grand Sport | 6 | 241 / 1,446 | 132 | 152 / 89 | 157 → 157 (+0) | 16 |
| Grand Sport X | 6 | 239 / 1,434 | 132 | 148 / 91 | 144 → 141 (+0) | 14 |
| Z06 | 6 | 244 / 1,464 | 130 | 155 / 89 | 110 → 110 (+5) | 12 |
| ZR1 | 4 | 207 / 828 | 90 | 121 / 86 | 98 → 97 (+0) | 9 |
| ZR1X | 4 | 206 / 824 | 90 | 118 / 88 | 96 → 96 (+0) | 9 |

The 1,379 offerings, 7,448 availability pairs and 704 model-interior leaves agree
with the disposable import inventory. The 783 direct source rules have accounted
translations: 35 are filtered for inactive endpoints, 748 emitted, and Z06 adds
five code-derived edges. Filtering does not authorize deletion of source facts or
permanent omission from a corrected target. Each option amount has a classification;
qualified rates, standard equipment, zero and null remain distinct.

| Completion question | Cross-model finding | Evidence and consequence |
|---|---|---|
| What exists? | All six inventories retain offerings, interiors/components, standard equipment, duplicates and classified guide-only omissions. | `baseline_rows`, `offering_dispositions`, `guide_only_dispositions`, `interior_source_links`. GS's dormant T0E is explicitly retired in its target; GSX's price-only 5ZB is explicitly retained. Neither is an unaccounted row. |
| When does it apply? | All configurations have foundations and complete starting-choice sweeps for the documented active universe, with inactive/hidden records separately accounted. | Runtime starting observations: ST 1,416; GS 1,428; GSX 1,416; Z06 1,434; ZR1 800; ZR1X 812. Standard status, selection eligibility, lifecycle and display flags cannot be collapsed into one availability field. |
| What does selection do? | Each lane traces packages, interiors, graphics, equipment and price owners through source and observed consequences. | Structured handoff §§4–5 and every option's accounting. Inclusion is not a zero-price rule: the LZ SBT/SC7 double charge demonstrates the distinction. |
| What does change/removal do? | Package/child order, surviving causes, dependency loss and context reset are represented, with model-specific performance and restoration cases. | Common runtime connected cases: ST 109; GS 121; GSX 119; Z06 112; ZR1 354; ZR1X 1,973, plus retained original evidence. Counts differ because ZR1X includes interior/paint/belt sweeps in that array. They are not comparable coverage scores. |
| What reaches the build? | Complete-context observations retain itemization, equipment, totals, order sections and compact recap. Every configuration has a required-interior rejection. | 32 rejection checks in the common runtime files; zero live requests. Enabled submission and correct arithmetic alone do not prove a valid build. |
| What is established? | Known defects have recorded dispositions and accepted targets; no missing whole family was identified in this consolidation. | 72 accepted records plus the shared policy. Corrected outcomes, current-app visuals, successful external order handling and exhaustive build enumeration remain unverified. |

## Family review in each model's lane

These are connected review conclusions, not proposed shared product definitions.
The cited handoffs retain the exact source cells, endpoint sets and observation IDs.

| Lane | Foundations and interiors | Performance, wheels and engine content | Graphics, body/accessories and output | Disposition |
|---|---|---|---|---|
| [Stingray](stingray-structured.md) | Six LT configurations; UQT paid at 1LT and supplied higher; 130 exact leaves, no EL9. R6X seat correction is separate from component charges. | Z51/FE4 and WUB/NWI dependency loss; factory wheels versus second sets; PCX locked wheel content versus PDV paid-cap substitution. | Colored covers have body-specific prerequisites and shared lighting causes; wing/Z51/ZF1 order codes, RNX exception, D30/DRG causes and configured equipment are traced. | Complete with ST-D01–12 targets. Do not import GS brake restoration, Heritage or ZR1 package prices. |
| [Grand Sport](grand-sport-structured.md) | Six LT configurations and 132 leaves; EL9 must acquire Z25 at 1,995 plus an independent AE4 595, with red belt locked. | FEB/FEY, J57 and T0F require AND/ANY conditions; caliper/wheel restoration and B4Z scope are explicit corrections. | Hash-first Z15 acquisition, conditional stripe/paint→D84, colored-cover removal, rear-graphic exclusions and T0E duplicate resolution are traced. | Complete with GS-D01–16 targets. Preserve qualified carbon-wheel discounts and accepted identities. |
| [Grand Sport X](grand-sport-x-structured.md) | Six LT configurations and 132 leaves; EL9 currently omits the Z25 output code, beyond the charge-owner issue. | J57/B4Z/FE5 are standard; FED changes tires. GS package-dependent brake rules do not apply. Remove exactly the two accepted LS6 mapping edges; retain standard LS6. | Independently evidenced DTC/Heritage and D84 gaps; existing DTC, no DUW or duplicate T0E. HP1 gets the accepted axle-only copy. | Complete with GSX-D01–14 targets. Price-only 5ZB remains an accepted provenance limitation. |
| [Z06](z06-structured.md) | Six LZ configurations, 130 extras-priced leaves; four missing AE4 components require their own LZ amounts. | J57/Z07 and PDB/PDD/PDF have wheel-qualified prices and caliper defaults. R8E changes with aero. Five derived CBF edges are translation obligations. | PCZ contents and second-set hardware need full exclusions without replacing factory wheels; SBT/SC7, stripe/paint, N3W/N2Z and equipment output have explicit corrections. | Complete with Z06-D01–12 and the final noticed-PDD policy. No PDF substitution is authorized. |
| [ZR1](zr1-structured.md) | Four configurations, 1LZ/3LZ; 90 leaves; UQT and engine packages standard. Guide columns D:G. | ZTK 5,995 + TOM 12,995 = 18,990; J58/FE8/XFR yield to J59/FEJ/XFS. Independent TOM survives only when acquired before ZTK. | Cover displacement is not child absorption; SBT/SC7, DTC groups, dormant CFC→GBA, EFR scope, lifecycle and static-equipment gaps are accounted. | Complete with ZR1-D01–09. DUW retirement is an owner departure from a guide containing both DUW and DTC. |
| [ZR1X](zr1x-structured.md) | Four configurations, 90 leaves; guide columns H:K independently reconciled; E60 3LZ-only. | J59 remains standard; ZTK 1,500 + TOM 12,995 = 14,495, with FEZ/XFS. FEH restoration is this lane's target. | DTC, SBT, purchase intent and covers have their own observations. CFC→GBA is emitted but latent; DY0/CFV are already in static equipment. | Complete with reconciled ZR1X-D01–09. Do not copy ZR1 missing-equipment findings or its rates. |

## Findings that control the consolidated design

### R1. Resolve policy precedence before translating expected behavior

Historical ST-T14, GS/GSX rear-graphic checks and Z06-T06/T12 still describe refusal
or alternative UI choices. The shared policy supersedes those interactions:
conflicting choices remain clickable; the notice discloses changes; confirm applies
a compatible replacement; cancel preserves selections and charges. Z06 PDB/Z07
requires a noticed PDD switch, with PDF expressly unauthorized. PCX still cannot
keep incompatible paid accessory wheels in place of its included wheels.

**Disposition:** resolved by existing authority, not a new owner decision. Future
acceptance cases must compose the lane target with the final policy instead of
copying historical expected-sequence prose. Preserve the original observations.

### R2. Purchase intent, inclusion causes and displacement are different state

The baseline loses independently purchased children after package removal. Compare
`stingray-C031/C032`, `grand-sport-C031/C032`, `grand-sport-x-C033/C034`
and `z06-C031/C032` in their runtime files, plus `zr1x-C296` and its other variants.
These case pairs exercise VWE with ST PCU or GS/GSX/Z06 PCQ; the handoffs retain
the other package families.
Surviving D30/DRG causes are separately observed; they do not prove that absorbed
purchase intent was retained.

GS-D04 and GSX-D04 explicitly retain independently selected D84. GS-D16 keeps
independent purchase intent distinct; GSX-D12 and Z06-D06 require preservation,
and ZR1/ZR1X-D06 specify the TOM and accessory-child cases. Older GSX-T20 and
absorbed-child descriptions cannot override those accepted targets. A displaced
ZR1/ZR1X cover stays deselected and uncharged; it is not a package child to restore.

Stingray's ST-S05/ST-T16 retain absorption behavior, and its owner overlay does not
contain a blanket independent-child preservation correction. Its paid PDV cap
exception is separately accepted under ST-D06. **Do not silently extend the later
lanes' package policy to every Stingray relationship.**

**Disposition:** the design must represent explicit purchase intent, automatic
causes, defaults and incompatible-choice displacement separately, with scoped
acquisition/removal policies. This review does not create a universal restoration
rule or reopen recorded decisions. Any proposal to standardize the remaining
Stingray absorption behavior would be an additional business-policy change.

### R3. Conditional acquisition needs more than a direct prerequisite

GS/GSX convertible stripe + one of the exact paint sets must acquire D84 and disclose
its price and roof-stripe consequence. Hash selection acquires Z15, and EL9 selection
acquires Z25. A prerequisite-only translation would create a circular entry gate;
`requires_z25` alone already fails to emit Z25 in GSX. See GS-R04/06/14,
GSX-R04/05/09 and their source disclosures.

**Disposition:** one design must express typed conjunctions, alternative sets,
acquisition, continuing validity and loss behavior. Keep paint conditions separate
from body/trim configurations. Do not use the interior-only D30 combination table
as a universal conditional-rule table. This extends the historical Stingray proposal
at the demonstrated requirement, without inventing a general scripting language.

### R4. One charge owner does not mean one global price

The six lanes all have four observed R6X/AE4 shortfalls of 595, but LT and LZ source
representations and extras differ. LT target subtotals include 2,780/2,285 where LZ
paths include 2,980/2,485. Exact leaf memberships, seat ownership and PriceRef
qualifiers control the translation; code equality does not justify sharing rates.

Other necessary distinctions are GS/GSX Z25 1,995 plus AE4 595; Z06's 54-state
package/wheel matrix and conditional R8E; ZR1 versus ZR1X ZTK amounts; standard UQT
versus its paid LT use; and SBT supplying SC7 without an additional 195 charge.
See each handoff §4 and `accounting.option_prices` for model-qualified sources.

**Disposition:** use exact amounts, explicit charge owners and context-qualified
rates. Null is unknown evidence, zero an explicit amount, and standard/supplied
content is not automatically a purchase. Preserve destination once. Frozen stored
interior sums remain comparison evidence, not additional editable charge owners.

### R5. Availability and static equipment cannot decide installed content

GS B4Z is package-dependent in the target; GSX B4Z/J57/FE5 are standard. Z06 and
ZR1/ZR1X require N3W restoration with N2Z replacement. ZR1's CFC→GBA rule is filtered;
ZR1X's corresponding rule is emitted but unacquired. Blindly making standard rows
active could promote a latent wrong paint implication. These are accounted defects,
not missing model families. ZR1X-D01 identifies the exact rule removal.

**Disposition:** model/body/trim applicability, lifecycle, display role, acquisition
and installed content need distinct ownership. Correct the accepted latent
relationships before enabling affected standard content. Static trim information,
configured equipment, purchases, line items and physical content are separate
projections; a second roof, accessory wheel hardware or contextual cover version
does not require a new purchasable option identity.

### R6. Preserve source identity and translate complete relationship sets

Accepted additions are DTC in ST/GS/Z06 and SAI in all six lanes. GSX/ZR1/ZR1X
already have DTC. Retire DUW in ST/GS/Z06/ZR1/ZR1X, but retain its guide/workbook
history; retire only GS's dormant `opt_t0e_002`, retaining `opt_t0e_001`. Rename
DUE only in the lanes with accepted naming corrections; preserve GSX's exact HP1
copy target. These operations are not an RPO rename/import-deduplication shortcut.

Complete graphic group memberships and scoped lifecycle targets live in the lane
decisions, not merely the offering-level disposition. Preserve all five Z06 derived
CBF edges with their code provenance; an empty derived list in the other lanes is
an accounted difference. GSX-D14 removes exactly two LS6 edges without removing
standard LS6 or valid cover lighting. See the overlays' `target_rule_removals` and
source `runtime_derived_relationships`.

**Disposition:** stable model/year/revision identities and explicit legacy mappings
must survive additions, retirements and revision changes. Source anchors are
provenance, not keys. The target translator must consume the complete overlay;
a `retain` offering row alone cannot approve its old rules, label or prices.

### R7. One navigation defect was repaired without changing a decision

The ZR1 review pointer and nine decision records pointed to the former `8-open-owner-decisions...` heading;
the behavior report now says `8-accepted-owner-decisions...`. The overlay links are
corrected to the existing heading. Decision text, IDs, states, prices, authority,
source anchors and frozen evidence remain unchanged.

## Applicability of later checks to earlier lanes

| Later finding/check | Disposition across earlier lanes |
|---|---|
| ZR1X puts interior/body, paint and belt sweeps in connected sequences | Earlier lanes retain equivalent categories in original supplemental data or ZR1's frozen extra keys. No representation change or extra equal-count gate is needed. |
| ZTK/TOM/cover order and independent intent | The exact ZTK/TOM experiment applies to ZR1 and ZR1X. Earlier lanes have their own package/child and cover/engine/aero cases; R2 preserves their policy scope instead of transferring the product relationship. |
| Standard equipment hidden by inactive flags and latent implications | Applicable across all lanes through starting-choice accounting and configured/static comparisons. R5 records the differing B4Z, N3W, FE8/FEH and CFC outcomes. |
| Missing derived direct edges | All lanes contain explicit derived accounting. Only Z06 has five additional endpoint triples; no additional edges are inferred elsewhere. |
| Different trim counts and adjacent guide columns | Four-context ZR1/ZR1X checks cover their complete configuration sets. Earlier six-context lanes stay six. D:G and H:K must never be merged merely because the guide sheet is shared. |
| Graphics or packages absent from an earlier model | Common runtime `not_applicable` records explicitly exclude ST's PDA/VPW/VPO probes and GS/GSX's absent EFY. This is scoped absence, not failed coverage. |

## Database design handoff and existing-code disposition

The review supports one common structural vocabulary with model-owned facts. It
does not yet fix final table names, keys or an approved schema. The next design
must specify row grain, keys/foreign keys, effective scope, null/zero semantics,
price precedence, acquisition/removal semantics and source/decision/release lineage
for each family below, then walk the six lanes through it.

| Existing material | Disposition for the next design | Reason |
|---|---|---|
| Frozen archive, six handoffs, owner overlays, discovery probes | Retain as evidence and acceptance inputs | They distinguish preserved baseline from accepted departures. The probes execute a pinned baseline, not the future evaluator. |
| `catalog/schema.py`: model-owned option/availability and typed reference approach | Reuse the design principles; review exact storage | The current `model` is one frozen year and the schema lacks the planned revision/release lifecycle. Matching RPOs are not shared identities. |
| `catalog/schema.py`: global interior definitions/component rates, stored interior price, source scope tokens | Redesign ownership/translation for the target | LT/LZ component meaning and model-qualified rates cannot inherit global ownership solely from workbook layout. Raw scope syntax is source evidence. |
| `catalog/schema.py`: direct/group/default/price families | Retain useful separation; revise expressiveness | R2–R4 require conditional acquisition, scoped purchase intent, replaceable defaults and single charge ownership. Legacy direct `requires/includes/excludes` is insufficient by itself. |
| `catalog/contracts.py`: R6X adjustment and `requires_z25` emission | Preserve for baseline comparison; replace those target semantics | These intentionally reproduce old pricing/output and do not implement accepted corrections. Reusing them unchanged would carry defects forward. |
| `catalog/contracts.py` and `catalog/parity.py`: direct typed-data generation, deterministic output, isolation and baseline comparison | Reuse where compatible after design | No Excel intermediate is needed. Exact old hashes remain the parity oracle, not the expected hashes of a corrected release. |
| Historical `stingray-schema-plan.md` and cross-model database proposal | Revise into one coherent proposal | Useful model ownership/content/provenance concepts remain; conditional acquisition, absorption-only policy, old conflict UI and pricing assumptions require R1–R6 changes. |
| Source intake and future authoring/release/visualizer work | Keep their existing boundaries | Manufacturer discrepancies remain reviewed changes. Authoring UI, asset preparation and canonical cutover are later tasks. |

A bounded next task is to produce that logical master-schema proposal with connected
walkthroughs for ST Z51/PCX, GS EL9/D84/FEB, GSX FED/DTC/LS6, Z06 package wheels/PCZ,
ZR1 ZTK/TOM and ZR1X ZTK/standard J59. Include the source-to-target translation for
accepted additions/removals, one charge per owner, independent causes and both
confirmation/cancellation paths. Review it before DDL or importer replacement.
Then implement separately authorized slices with two comparisons: unchanged
behavior against the frozen baseline, and intentional differences against the
accepted targets. Corrected-output verification precedes authoring/release/cutover.

## Validation and limits

- Six-lane handoff contract validation and all nine handoff-contract tests passed;
  they cover file shape, identities, references,
  accounting links and decision coverage; it does not judge business correctness.
- All three existing discovery reproduction tests passed in 87.6 seconds: all six frozen runtime outputs,
  ZR1/ZR1X extractor bytes and their option-price workbook anchors. Runtime comparison
  permits only compact submission timestamps and the explicitly verified historical
  versus current probe hash; no snapshot refresh is part of this review.
- Review inventory, decision counts, source-rule dispositions and the listed model
  differences were checked against retained JSON and the connected handoffs.
- Link/diff checks and a semantic comparison of the ZR1 overlay confirm that only
  its ten obsolete decision-heading links changed. All source/accounting/runtime
  evidence remains byte-for-byte unchanged from the reviewed baseline.

These results and the final diff checks are also recorded in the PR. No corrected evaluator,
current-app visual test, real order submission, manufacturer-order acceptance,
new schema, deployment or cutover was performed. Source discrepancies with accepted
targets remain visible; price-only evidence and historical probe provenance limits
are not converted into stronger claims by this review.
