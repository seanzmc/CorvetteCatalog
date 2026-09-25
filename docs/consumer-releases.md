# Consumer mappings and local release operations

This implementation adds a local form, order export and visualizer state contract
on top of the six-lane evaluator. It does not switch canonical authority from the
workbook or deploy to the existing form. Dealer submission and artwork processing
remain separate work.

## Consumer boundary

`catalog/consumers.py` imports all 1,388 option mappings, 704 interior mappings,
32 configuration mappings and 7,498 option/configuration presentation mappings
from the pinned structured handoffs and accepted owner overlays. Typed foreign
keys keep every mapping in its own revision. Existing option, configuration and
interior consumer keys are retained. Accepted additions use the overlay's existing
`record_id` as their new lane-local consumer key; runtime UUIDs are pinned by the
release snapshot, rather than regenerated at request time.

Source steps, sections, section overrides, summary routes, setup copy, contextual
copy, interior hierarchy and component copy are retained in the mapped contract.
The DTC addition uses that lane's retained stripe section; SAI uses its retained
interior-accessory section. Their ordering uses an explicit zero followed by the
stable consumer key. GSX HP1 uses the accepted front-axle-only copy. Inactive and
factory-unavailable identities remain accounted for. Source-hidden and auto-only
cards stay hidden; factory-unavailable cards remain visible and nonselectable.

Equipment code mappings use installed state for standard equipment and explicit
substitution endpoints; other purchase/order choices use resolved selection.
Reference-only CFX does not emit a code. Each emitted code retains its contributing
option identity: duplicate codes never select an arbitrary product owner. The
order includes the selected interior's retained codes/components, independently
owned choices, configured equipment, informational standard equipment, supplied
content and the evaluator's exact integer-cent charges. Configuration and component
charges are labeled independently; a null/no-separate-charge item does not acquire
a fabricated zero-price purchase.

Form, order and visualizer artifacts share one snapshot and revision membership.
The visualizer contract consumes installed equipment and supplied content. Its
asset list is explicitly empty with `art_not_bound` coverage. No unverified remote
images or unprocessed PSB files are included as release assets. Missing artwork
has no effect on product eligibility or price. Card photos are different: the
model presentation carries the source `asset_map` rows as links to images hosted
by the dealership, as the existing form does; they are not release assets.

The new interface is server-evaluated. It does not export executable rules to the
old JavaScript engine, and it does not claim wire compatibility with that engine
or the dealer submission API. Historical `catalog/contracts.py` and its frozen
migration-parity outputs remain intact as the comparison baseline. Accepted
corrections remain separate from unchanged migration facts.

## Warning and confirmation

`ConsumerSession.preview` returns a single-use opaque token, build version and
hash of the complete warning. The server holds the candidate. Confirmation must
match all three; client-supplied candidates, totals and removals are never used.
A later preview, cancellation, failed replacement preview or successful confirmation
invalidates the prior token. Foreign-session and replayed confirmations fail.

Warnings contain every resolved addition/removal, independent ownership change,
interior change, installed-equipment change, supplying cause, charge change,
content change, final total and missing required choice. Ownership and charge
changes remain visible even when the net total is unchanged. The local form
renders every warning line before enabling confirmation. Pending candidates are
never rendered as the committed build. Escape and Cancel leave the whole committed
state unchanged. Revert also previews the complete restored state and requires
confirmation. There is no direct apply/revert endpoint.

`catalog/consumer_server.py` serves only a verified completed release on loopback.
It binds each session to a model, configuration and release. Starting a build
establishes its configuration; options and interiors then use the confirmation
boundary. Sessions are local, in memory and do not store customer records.
Order export refuses pending changes or missing required selections and derives
the total from server state. Export is not dealer submission. The pure evaluator
continues to report its partial-consumer sentinel; the verified local release
consumer checks actual missing requirements separately.

## Authored draft acceptance

Source-only drafts retain the exact pinned importer comparison below. Authoring
workspaces instead require [explicit acceptance and source-plus-edit replay](authoring-operations.md).
The original baseline must still pass source validation; every logged change is
then replayed exactly. Authored bundles additionally pin `reviewed-edits.json` and
retain their evidence/history through completion and backup/restore. The semantic
audit, publication comparison, immutable artifacts and recovery checks still apply.

## Release lifecycle

`catalog/releases.py` stores immutable content-addressed snapshots and completed
bundles separately from the editable draft database. The source database retains
its draft state; the frozen snapshot's external manifest owns its frozen state.
This avoids making the original editable rows masquerade as frozen facts.

1. **Prepare** imports behavior and consumer mappings into a fresh draft database.
2. **Freeze** compares an expected digest of all schema, facts, mappings and edit
   versions with a captured SQLite snapshot. It validates foreign keys and mappings,
   replays the pinned importers into a separate copy, and requires exact equality.
   Fresh-import table counts also reject unexpected extra rows; counts are used
   together with value/replay checks, never as a parity substitute.
   It then runs the complete semantic inventory/overlap audit on that actual
   snapshot. A final locked comparison rejects concurrent draft changes, even if
   the edit version was not incremented. The frozen manifest pins source hashes,
   compatibility policy, all six model/year/revision memberships, runtime hashes
   and validation output. Failure leaves no frozen candidate.
3. **Complete** generates all six form, order and visualizer contracts from that
   snapshot, copies the pinned runtime, and checks deterministic artifacts and
   membership. All files receive content hashes. The completed manifest includes the frozen
   record and requires every model consumer artifact. A directory rename makes the
   complete bundle visible only after generation succeeds.
4. **Publish** verifies the entire completed bundle and changes a local channel's
   pointer using compare-and-swap in one SQLite transaction. The expected pointer
   version is mandatory. The history records the prior completed release.
5. **Rollback** revalidates the prior release and changes the pointer with the same
   compare-and-swap check. Frozen facts and completed artifacts are never edited.
6. **Backup/restore** copies an entire completed bundle, validates all hashes before
   installation, and restores it to a fresh store. Restore does not publish it.

Completeness requires exactly one revision per lane, the same year, a default
member and unambiguous model aliases. The manifest pins every runtime file and
artifact; missing, modified, unexpected or symlinked files fail verification.
The included runtime permits an old bundle to run independently of later source
changes. Failed builds, stale publication and failed restore leave the prior
publication pointer unchanged. `.building-*` directories are never published.
These are local filesystem operations, not a hosting/deployment system.

## Commands

Run from the repository root. Keep generated databases and bundles under `.local`.

```sh
python3 -m catalog.releases prepare .local/consumer-release/draft.sqlite
# Use the exact digest printed by prepare:
python3 -m catalog.releases freeze .local/consumer-release/draft.sqlite --expected-digest DRAFT_SHA256
python3 -m catalog.releases complete FROZEN_ID
python3 -m catalog.releases verify RELEASE_ID
python3 -m catalog.consumer_server --store .local/releases --release RELEASE_ID
# Open http://127.0.0.1:8765
python3 -m catalog.releases publish RELEASE_ID --expected-version 0
python3 -m catalog.releases pointer
python3 -m catalog.releases rollback --expected-version CURRENT_VERSION
python3 -m catalog.releases backup RELEASE_ID .local/release-backup
python3 -m catalog.releases --store .local/recovered-releases restore .local/release-backup
```

Publication here changes only a local store. For an older release whose runtime
no longer matches the checkout, run its bundled runtime without generating cache
files in the immutable bundle:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.local/releases/completed/RELEASE_ID/runtime \
  python3 -P -m catalog.consumer_server --store .local/releases --release RELEASE_ID
```

## Verification

`tests/test_consumers.py` covers mappings against retained sources, both stripe
interaction directions, full warning/cancel/confirm/revert behavior, all-lane
roof ownership and charges, interior clearing, equipment substitutions, disabled
cards and token tampering/staleness/replay. `tests/test_releases.py` covers exact
source replay, stale/concurrent edits, failed freeze/completion, corrupt artifacts,
deterministic generation, publication CAS, rollback and backup/recovery. The small
lifecycle fault tests mock only the expensive semantic audit; they do not establish
semantic release qualification. The real freeze command runs that audit separately
against the release snapshot.

Focused execution results on September 17:

- Ten consumer tests passed in 14.464 seconds.
- Ten release lifecycle tests passed in 203.093 seconds.
- The added source-completeness check and source replay regression passed in
  51.470 seconds after the final source-validation refinement (two tests, one
  overlapping the lifecycle suite; 21 distinct tests across the runs).
- Python syntax, JavaScript syntax and diff whitespace checks passed.

The lifecycle suite exceeds the routine two-minute target because it repeatedly
replays all six source imports and creates/verifies complete SQLite/runtime bundles
for failure, race and recovery cases. The full semantic qualification is a separate
release-milestone check; it is not installed as a routine commit hook.


The actual freeze then completed the full six-lane matrix: **6,921 inventory
entries, 69,796 scoped outcomes and 2,916 live overlaps**, with **zero failed or
unresolved findings**. This is relationship/condition coverage, not exhaustive
Cartesian build-history enumeration.

- Frozen snapshot: `b51549dc707bef92646da7d61ed96c780389c72ae326393d86866a2cc94a2055`.
- Completed release: `fb1215257ae52e70dd91d818e6921832337168e4fe536cbca4a820585d3032c6`.
- All **39 artifacts** verified; local publication advanced from version 0 to 1.
- Backup restored into a fresh store, all hashes reverified, and its bundled
  runtime started successfully without using the checkout's runtime modules.
- Browser verification against the restored release, Z06 `1lz_h67`: GBA then DPB;
  VPW preview disclosed DPB removal, both charge lines, ownership changes and
  `$132,290 → $131,570`. Preview/cancel retained `$132,290`; confirm committed
  `$131,570`; confirmed revert restored DPB and `$132,290`. Required interior
  confirmation then enabled export. No browser console errors were observed.

The local artifacts are under `.local/consumer-release/`; they are generated
review output and are not committed as a second product-data authority. Commands
above reproduce qualification and generation from the pinned source inputs.
