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

## Checkpoint C work in progress

`scripts/intake_brakes.py` is an unfinished extractor for the exact source hash
above and the frozen B workbook/runtime archive. It is intended to preserve cells
and rich text, stage typed assertions, and reuse immutable comparison results.
None of those end-to-end results has yet passed verification. No staging JSON
has been published and no canonical operation has been performed.

Two execution attempts failed at variant identity mapping. The first compared
guide trim `1LT` with workbook `1lt`. Correcting casing then found three records:
`variant_master!A2:H2` (Stingray), `A8:H8` (Grand Sport), and `A14:H14`
(Grand Sport X). The missing model-membership join is explicitly available in
`model_variants!A14:E19`. The next bounded fix must restrict candidates through
active `model_key=stingray` membership before matching trim/body/year. Do not
choose the first match or infer identity from labels.

Work stopped at the repository's two-failure limit. The extractor remains draft
code, not a completed Checkpoint C deliverable. After the mapping fix, exercise
the actual source, unknown/flattened footnotes, missing/duplicate identities,
price ambiguity, source preservation and repeated-run idempotence. Review the
remaining extraction/comparison paths before treating their results as evidence.

To resume with Python and `openpyxl==3.1.5` (available in the bundled workspace
runtime):

```sh
python3 scripts/intake_brakes.py
```

The current command fails at the known mapping defect. It writes only review
staging after a successful build; it has no canonical acceptance path.
