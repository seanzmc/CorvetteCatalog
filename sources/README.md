# Manufacturer source originals

Original Excel exports live under Git-ignored `sources/raw/<sha256>/`, retaining
their supplied filenames and exact bytes. Provenance stays tracked here; originals
remain in the local checkout. A fresh clone needs the matching original supplied
separately. Do not overwrite a different revision under an existing hash directory.

**Current review:** the [September 18 reconciliation](#september-18-intake-reconciliation)
below applies later owner decisions and current implementation evidence to C's
seven original ambiguities. The receipt and staging descriptions below retain
their September 6 findings, including then-unconfirmed currency and price basis;
they are not the current owner-decision status.

## Export received September 6, 2026 UTC

- Original placement: `docs/2027 Chevrolet Car Corvette Export (6).xlsx`.
- Current placement: `sources/raw/d3ca7d3a09c9fb89210b4ce584493b3ad8fb65ca35087c49d816d1cbf1a333d1/2027 Chevrolet Car Corvette Export (6).xlsx`.
- Size: 195,524 bytes.
- SHA-256: `d3ca7d3a09c9fb89210b4ce584493b3ad8fb65ca35087c49d816d1cbf1a333d1`.
- Received from Sean in this checkout; original download URL and earlier
  acquisition history are unknown. Receipt date is not publication date.
- 28 sheets. `Price Schedule!A2:A4` identifies MY2027 and start-of-production
  effectivity. `Price Schedule!A308` reads
  `¨Revised July 06, 20262027 CHEVROLET CORVETTE`.
  The parsed July 6 date applies only to the price schedule. A July 26 revision
  and a whole-guide September 7 edition were not established by this inspection.
- `Mechanical 1!D7:I7` retains separate `A` and superscript `1` runs. Its footnote
  at `C7` says J55 is included and only available with Z51.
- Price layout ambiguity: `Price Schedule!F44` says MSRP and `G44` says Dealer,
  while Z51 has `F229=0` and `G229=5395`. The apparent one-column shift in option
  rows must remain unresolved; do not adopt either value as verified MSRP.
- Base-price context: `F10=71000` and `J10=2495` total 73495, matching frozen
  `variant_master!F2`; currency remains unconfirmed.

The move was byte-preserving and the hash was rechecked afterward. The original
is not included in Git or the PR. This placement follows the owner's explicit
permission to keep the raw export Git-ignored.

## Checkpoint C local completion

[`scripts/intake_brakes.py`](../scripts/intake_brakes.py) extracts only this exact
source revision against the frozen B workbook/runtime archive. The owner resumed
the stopped task, and the mapping now joins active `model_key=stingray` membership
in `model_variants!A14:E19` to active `variant_master` identities before matching
year, trim and body. This excludes the Grand Sport and Grand Sport X rows that
caused the earlier ambiguous matches. Missing, duplicate, dangling and inactive
identities fail before staging. Each proposed variant mapping retains its cells.

The [immutable comparison](../intake/stingray-brakes/6d649f46323c0be53dd49be125c49c4073eb872397c41ff3ed4da3a82e440364.json)
contains 26 pending-review assertions, with no accepted operations:

| Result | Evidence and limits |
|---|---|
| 18 unchanged availability pairs | `Mechanical 1!D6:I7` and `D53:I53`: JL9 standard, J55 available with footnote 1, Z51 available across six Stingray variants; exact workbook pair locations retained |
| 1 unchanged inclusion | `Mechanical 1!C7/C53` and `rule_mapping!A109:H109`: Z51 includes J55. Frozen runtime rule evidence also records active auto-add into a display-only section |
| 2 ambiguous relationships | J55 requires Z51 has no direct prerequisite row; J55 is nonselectable and included. Owner-confirmed replacement of JL9 is not explicit removal wording in these guide cells. Behavioral equivalence is not established |
| 3 ambiguous code roles | JL9/J55 are reference-only; Z51 is orderable. The baseline's RPO field does not represent that distinction |
| 2 ambiguous price assertions | Z51 option headers/amounts remain unresolved; sampled base MSRP plus destination equals 73495 but currency is unknown. Base-price scope is only `1lt_c07`, not all six variants |

There are no asserted additions, changes, removals or conflicts. Ambiguous facts
remain unresolved rather than being counted as accepted differences. Exact
selected cells, rich-text runs, fonts, formats and headings are retained. The
28-sheet inventory marks two sheets partial and 26 out of scope. Selected ranges
are explicitly partial because descriptions and unrelated notes are not fully
interpreted. Z51 members FE3, G0K, G96, M1N, QTU, T0A and V08 remain external
references. This is brake-family coverage, not whole-guide or full-package parity.

Eleven focused tests passed on September 6, 2026 UTC in 9.6 seconds. They cover the
18 exact availability pairs, six model-qualified mappings, selected-cell coverage,
rich footnotes, unresolved/flattened markers, missing notes, invalid identities,
price scope/ambiguity, source/archive integrity, stable candidate identities across
new comparisons, identical repeated builds, reuse and refusal to overwrite
conflicting staging. An initial test-fixture failure was corrected by reloading
original bytes instead of deep-copying openpyxl's custom-format tables. Two actual
CLI runs returned `created` then `reused` for the same comparison. Source/archive
bytes are unchanged; 27vette remains clean. No browser behavior or acceptance
transaction was implemented or tested.

To reproduce with Python and `openpyxl==3.1.5` (available in the bundled workspace
runtime; supply the matching ignored original first):

```sh
python3 scripts/intake_brakes.py
python3 -m unittest discover -s tests -v
```

Repeat the extractor command to verify `reused`. Missing source evidence fails
the tests rather than silently skipping them. Parser/config changes create a new
run; workbook/runtime baseline changes create a new comparison. Existing staged
files are never replaced.

Local implementation and validation are complete. The owner authorized public
publication of the source-derived code and review evidence, with raw originals
remaining Git-ignored. Routine catalog pricing and intake evidence follow the
repository commit/PR authorization in `AGENTS.md`. Publishing these pending-review
assertions does not accept them into canonical data. Do not start another
checkpoint or resolve the seven ambiguous assertions automatically.

## September 18 intake reconciliation

The owner authorized this follow-up as the first task in the
[agreed remaining sequence](../docs/migration-plan.md#current-direction--september-18-agreed-remaining-sequence).
It reconciles existing evidence and decisions; it does not accept staged facts
into canonical data or implement the F acceptance transaction.

The exact source hash, frozen workbook hash and comparison remain those above.
The extractor returned `reused` for comparison
`6d649f46323c0be53dd49be125c49c4073eb872397c41ff3ed4da3a82e440364`:
19 unchanged and seven ambiguous original assertions, `accepted_operations: []`.
Neither those classifications nor the raw source have been rewritten. There are
no newly asserted additions, removals or canonical corrections in this review.

### Disposition of all seven assertions

IDs below are unique 12-character prefixes of `candidates[].id` in the
[immutable comparison](../intake/stingray-brakes/6d649f46323c0be53dd49be125c49c4073eb872397c41ff3ed4da3a82e440364.json).
All apply to the six mapped Stingray configurations except the explicitly scoped
base-price assertion. “Reconciled” is this review's disposition, not an acceptance
operation or a retroactive claim about the old runtime.

| Assertion ID / subject | Later evidence and current disposition | Remaining boundary |
|---|---|---|
| `0c7d74d9318b` — J55 requires Z51 | **Reconciled behavior.** `Mechanical 1!C7` says included and only available with Z51. The [existing brake interpretation](../docs/source-schema-specification.md#8-decisions-and-implementation-boundaries) confirms it. Frozen `rule_mapping!A109:H109` supplies J55 and `stingray_options!A62:K62` makes it nonselectable. Current six-configuration checks refuse direct J55 selection, supply it with Z51, and remove it when Z51 is removed. | No new prerequisite rule is inferred merely to match the guide's wording. F must retain the dependency semantics and their provenance when accepting/editing the relationship. |
| `d6ae2734ce11` — Z51 replaces JL9 with J55 | **Reconciled accepted interpretation and implementation.** The same owner clarification establishes replacement; ST-D10 in the [owner overlay](../docs/stingray-owner-decisions.json) distinguishes installed from informational equipment. `catalog/behavior_sources.py` implements the scoped Z51/JL9/J55 substitution. All six checked configurations install J55 instead of JL9 with Z51, restore JL9 afterward, and retain JL9 in informational standard equipment throughout. | The selected guide cells still do not explicitly say “remove JL9.” Attribute this interpretation to the owner rather than rewriting manufacturer wording. |
| `ab375900a23e` — JL9 reference role | **Source role established; representation remains open.** `Mechanical 1!B6` under `B3` identifies a reference-only code. The current option is nonselectable standard equipment. | Neither the baseline RPO field nor current consumer `emit_code` records the manufacturer role explicitly. Preserve this role in F acceptance and map it deliberately in the dealer contract. |
| `5deced7708bf` — J55 reference role | **Source role established; representation remains open.** `Mechanical 1!B7` under `B3` identifies a reference-only code. Current J55 is package-supplied and nonselectable. | The local `order_codes` projection includes installed J55; that is not proof it belongs in a dealer's selectable/orderable-code payload. Explicit role representation and dealer mapping remain work. |
| `afeed1d3bca9` — Z51 orderable role | **Source role established; representation remains open.** `Mechanical 1!A53` under `A3` identifies an orderable code. Current Z51 is selectable and emitted in local output. | Selectability is not a substitute for retaining the manufacturer's role. F acceptance and dealer integration must preserve the distinction from JL9/J55. |
| `33b13de68221` — Z51 option price | **Reconciled by ST-D12.** The owner accepted Price Schedule column E for OPTIONS and USD. Fresh read of the same hashed source confirms `B229=Z51`, `D229=Stingray`, `E229=5395`; [Stingray price accounting](../docs/discovery/stingray-accounting.json) independently retains `B229:E229` and the matching workbook amount. Current Z51 charge is 539,500 cents in all six configurations. | Preserve the shifted headers (`F44=MSRP(c)`, `F229=0`, `G229=5395`) as source evidence. Column E is the accepted interpretation, not a repaired header or a license to reprice other rows. |
| `e27a65c16d9b` — sampled base price | **Reconciled by the USD decision in ST-D12.** Fresh source read confirms `F10=71000` plus `J10=2495`, matching frozen `variant_master!F2=73495`; current `1lt_c07` initial total is 7,349,500 cents. ST-D12 explicitly preserves the separate base/destination calculation. | Scope remains `1lt_c07` only. This assertion does not establish base-price reconciliation for the other five configurations, nor authorize a second destination charge. |

The two price decisions are already machine-readable in
`stingray-owner-decisions.json` (`owner_review.option_price_column`,
`currency_code`, and record `ST-D12`); this review introduces no new business
decision or duplicate overlay. Four historical assertions now have a reconciled
interpretation/behavior; three retain an explicit representation requirement.
They are not seven unanswered owner questions.

### Source identity and acceptance limits

- **Known:** supplied filename, receipt date, source SHA-256 and MY2027 identity;
  `Price Schedule!A308` establishes a July 6, 2026 price-schedule revision.
- **Still unknown:** whole-guide edition and original acquisition history. Neither
  the promised July 26 revision nor a September 7 whole-guide edition is proven
  by this file. Do not invent revision precedence; any acceptance that depends
  on a newer edition needs that edition's evidence.
- **Coverage remains bounded:** C extracted selected brake/price cells only.
  FE3/G0K/G96/M1N/QTU/T0A/V08 remain external references in that comparison.
  Later full behavior work does not retroactively turn C into whole-guide intake.
- **Next:** the E authoring pilot can proceed without inventing missing metadata.
  F must carry original assertions, later decisions, source roles and unresolved
  metadata into reviewed acceptance. Actual acceptance/persistence remains
  unimplemented; dealer submission and canonical cutover remain separate tasks.

### Verification on September 18

At implementation baseline `79c941f3f22484e622a6f31fe95b26b52e879383`:

- All 11 `tests.test_intake_brakes` checks passed in 9.922 seconds with the bundled
  Python runtime and openpyxl. The system `python3` could not import openpyxl;
  the bundled runtime resolved that environment issue without dependency changes.
- The unchanged extractor returned `reused`; the raw SHA-256 and price/date cells
  above were independently read and checked.
- A focused in-memory probe imported current behavior and consumer mappings and
  used `ConsumerSession.preview/confirm/cancel` for each configuration below.
  Initial JL9/no-J55, direct JL9/J55 refusal, unchanged state after preview/cancel,
  Z51-supplied J55/JL9 substitution, informational JL9 retention, package removal
  and total restoration all passed. Each Z51 line charged 539,500 cents; neither
  brake received a separate charge. Local code output included J55 and excluded
  JL9 while Z51 was selected. Draft qualification remained unchanged.

| Configuration | Initial and restored total (USD) | Brake transition checks |
|---|---:|---|
| `1lt_c07` | 73,495 | Passed |
| `2lt_c07` | 80,595 | Passed |
| `3lt_c07` | 85,245 | Passed |
| `1lt_c67` | 80,495 | Passed |
| `2lt_c67` | 87,595 | Passed |
| `3lt_c67` | 92,245 | Passed |

These are local evaluator/consumer checks, not browser or dealer integration
checks. Full parity, semantic-audit and release-recovery suites were not rerun:
this task changes review documentation only, preserving code, frozen evidence,
owner overlays and release artifacts.
