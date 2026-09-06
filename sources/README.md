# Manufacturer source originals

Original Excel exports live under Git-ignored `sources/raw/<sha256>/`, retaining
their supplied filenames and exact bytes. Provenance stays tracked here; originals
remain in the local checkout. A fresh clone needs the matching original supplied
separately. Do not overwrite a different revision under an existing hash directory.

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

Local implementation and validation are complete. Public push/PR delivery is
pending explicit approval: automatic approval review previously rejected publishing
source-derived details even with the raw workbook ignored. Nothing has been
merged, deployed or accepted into canonical data. Do not start another checkpoint
or resolve the seven ambiguous assertions automatically.
