# ZR1X structured discovery handoff

## 1. Record conventions and evidence

Read [behavior](zr1x-behavior.md), [source records](zr1x-structured-records.json),
[accounting](discovery/zr1x-accounting.json), [runtime](discovery/zr1x-runtime.json)
and [owner decisions](zr1x-owner-decisions.json) together. `_row` is the original
workbook row; `sheet_roles` addresses model-owned worksheets without renaming them.
Source hashes and reference `4fe92a4f078370c478f18484cad31bdafe58ad43` remain pinned.
H:K are ZR1X guide columns; the raw shared D:G facts are context only.
`guide_rows` retains both models' existing symbol fields; `applicable_to_zr1`
describes D:G only. ZR1X accounting independently selects H:K.

## 2. Complete record sets and how to use them

Records retain 206 options, 824 availability rows, 90 interior leaves, 127 component
memberships, 214 color overrides, 96 direct rules, four rule groups/43 members,
eight exclusive groups/22 members, 33 price rules and six defaults. Generic roles
resolve to original `zr1x_*` sheets and shared LZ tables. All active, inactive,
display-only and source-only records remain distinguishable. The 19 guide-only
dispositions separate SAI, six components and twelve external-scope offerings.
Accounting covers each option price and all 96 emitted direct rules; derived
direct relationships are explicitly empty. Raw originals remain Git-ignored.

## 3. Configurations and offering scope

`1lz_s07`, `3lz_s07`, `1lz_s67`, `3lz_s67` are the two trims in both bodies.
680 coded status pairs, 26 uncoded correspondences and 194 repeated occurrences
reconcile. The 812 starting observations cover all 203 active options × four
variants, including hidden body/trim-unavailable states. N3W, FEH and V8X remain
globally inactive source records and are accounted for separately. E60 is 3LZ-only;
UQT is standard/display-only; J59 is standard and selected in every foundation.
J58/FE8/FEJ/M1K/SIG are outside ZR1X, not missing runtime tests.

## 4. Price ownership and interpretation

Base includes destination once; R8E adds 2,600. The four starting totals are
229,995/240,995/239,995/250,995. Option accounting retains column-E rates and D
qualifiers: 118 numeric amounts and 88 nulls. ZTK 1,500 plus TOM 12,995 produces
14,495; J59 is not an extra package charge. Component PriceRef rows and conditional
rules remain separate from option base rates. Four R6X/AE4 paths omit 595, while
SBT incorrectly charges included SC7 another 195. D03/D04 propose corrections;
D08 leaves currency and the full pricing/scope basis open for owner confirmation.

## 5. Connected relationship records

`connected_sequences` carries 1,973 cases/2,259 actions with source anchors,
complete initial state and actual order/compact projections. Cases cover
stripe/paint directions, graphic memberships, both child/package orders, cover
replacement, mirror and D30 multiple causes, performance round trips, wheel
hardware, interior contexts/paint/belts, delivery, and body/trim reset. Common
runtime keys suffice; the ZR1-only camelCase exception is not extended to ZR1X.
See behavior §§3–6 for case IDs and the relationship/price consequences.

## 6. Selection and reconciliation policies

Frozen selection behavior is evidence, not the target policy. ZTK removal loses
an independently selected TOM; packages absorb and later lose independently
purchased children. D06 proposes preserving purchase intent and leaving displaced
covers deselected. DTC's absent group memberships permit prohibited coexistence;
D05 proposes completing them. The accepted common notice/confirm/cancel UI applies
only with this lane's own compatibility facts. Factory unavailability remains a
different state; the relevant lifecycle corrections are still open in D02.

## 7. Presentation, physical content and operational boundaries

Preserve original 14 runtime steps, 12 order sections, context copy, assets and
step/section mappings. Snapshots expose selected/automatic items, charge ownership,
order sections, compact recap and informational equipment. CFC/DY0/CFV/HP1 are
already represented as static content; FEH and 3LZ N3W are missing due to inactive
flags. A CFC→GBA source rule is latent while CFC remains display-only. Static trim
information is not the installed ZTK build; D01/D09 record the proposed treatment.
External order types, services and dealer processes were not exercised.

## 8. Decision overlay: source, baseline and target remain separate

The owner overlay uses the common contract, with one offering target per source
offering. Retention is the default; every proposed non-default target or addition
links an **open** decision. The nine decisions are listed in behavior §8. No ZR1X
decision has been accepted on the owner's behalf, and no source fact is silently
changed to match an earlier model's accepted target. DUW remains provisionally
retained; ZR1's removal decision does not transfer automatically.

## 9. Worked sequences and expected outcomes

| Sequence | Frozen result | Proposed target or preserved source constraint |
|---|---|---|
| ZTK → attempted T0E → J59 → remove ZTK, all variants | Adds FEZ/XFS/TOM at 14,495; rejects T0E; J59 persists; restores T0E | Preserve model-specific equipment/rates, subject to D08/D09 |
| TOM → ZTK → remove ZTK | Independently selected TOM is lost | D06: retain TOM at 12,995 when independently purchased |
| RWJ/WKR → ZTK → remove ZTK | Cover removed; never automatically restored | D06: explicit replacement notice and retained deselection |
| VWE → PCQ → remove PCQ | VWE purchase absorbed and lost | D06: preserve independent child ownership |
| SBT with/without earlier SC7, both coupe trims | 2,720 package delta | D03: 2,525, included SC7 zero; ownership handled separately |
| SFZ/R88 ↔ DTC | Both remain with both charges | D05: enforce disclosed model-specific replacement |
| Four R6X/AE4 leaves | Each undercharges 595 | D04: 1,590/2,085/2,485/2,980 without duplicate charges elsewhere |
| HUQ with independent paint/belt D30 causes | D30 persists until last cause disappears | Preserve observed cause accounting |

## 10. Coverage and handoff boundary

All six completion questions are answered in [the discovery index](model-discovery.md#zr1x-completion-review).
The source accounting, 180 interior/body contexts, 900 paint cases, 540 belt cases,
all active choices and four missing-interior rejections retain comparable evidence.
All connected initial contexts are complete and live requests equal zero.
These are representative family flows plus full source inventories, not exhaustive
build enumeration or current-app/visual verification. Nine owner decisions remain
open; corrected behavior and the later six-model schema review have not run.

```sh
/Users/seandm/Projects/27vette/.venv/bin/python scripts/model_discovery.py zr1x .local/zr1x-source-new
node scripts/model_discovery.mjs zr1x .local/zr1x-runtime-new
python3 scripts/validate_handoffs.py
/Users/seandm/Projects/27vette/.venv/bin/python -m unittest discover -s tests
```

The extractor and runtime probe refuse existing output files. Reproduction tests
compare extractor bytes exactly and runtime bytes with only compact submission
timestamps normalized. Do not hand-edit generated runtime evidence.
