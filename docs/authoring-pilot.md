# Local option authoring pilot

This first E slice edits an existing model-owned option's name and base purchase
price through a local UI. It copies a source-verified draft into a separate
authoring database. The original source database, workbook, frozen evidence,
accepted overlays and existing release bundles remain unchanged.

Choose a model and search by RPO or name. The editor shows configuration
availability, existing contextual prices, source references and saved history.
Review the proposed name/price and affected configurations, supply a reason, then
save. Cancel makes no database change and retains the unsaved fields. Reload
restores saved values; navigating away from unsaved fields asks before discarding.

The base price is not a calculated build total. Contextual rates and package
ownership can override or suppress it. The pilot preserves those relationships,
applicability, lifecycle, identifiers, RPOs, price basis and charge mode. A priced
zero remains distinct from a null/no-separate-charge item. The latter's price is
read-only. Existing conditional rates are displayed but are not editable here.

## Run locally

Use Python with the repository's existing requirements installed. Create a fresh
source draft if one is not already available:

```sh
python3 -m catalog.releases prepare .local/authoring/source.sqlite
python3 -m catalog.authoring_server \
  --database .local/authoring/draft.sqlite \
  --initialize-from .local/authoring/source.sqlite
python3 -m catalog.authoring_server --database .local/authoring/draft.sqlite
```

Open `http://127.0.0.1:8766`. Initialization validates a captured source snapshot,
opens the source read-only and refuses to overwrite an existing destination.
Normal startup requires an initialized workspace and never creates a database
for a mistyped path. The server binds to loopback and rejects foreign Host/Origin
values and non-JSON writes. This remains a local, single-user management tool.

## Write boundary

`catalog/authoring.py` holds the bounded write operation. The server retains the
reviewed candidate behind a single-use token. Saving rechecks the option,
consumer mapping, revision version and scope under a SQLite write lock. A stale
review is refused; reload and review again. Client-supplied replacement values
are not used by the save endpoint.

The option, matching consumer name, revision version and timestamped before/after
history commit in one transaction, after structural/mapping validation. A failure
rolls back all four. Source provenance is retained as baseline evidence; the
separate history records the authored departure and its reason, not a newly
accepted manufacturer fact. Other model lanes retain their independent records.

## Shared component-price editor and ownership review

Open **Edit shared component prices** from the option editor, or `/components`.
This pilot edits an existing non-option component rate referenced by at least two
interior leaves in the same model revision and configuration. The shared record
is `(revision_id, component_id, configuration_id)` in `component_rate`; actual
`interior_part` and `interior_configuration` references establish its consumers.
Identical RPOs, labels or source PriceRef codes in other models do not share ownership.
This follows the reviewed [component ownership](master-schema-proposal.md#3-interiors-and-charge-components).

For example, Z06 suede N2Z has one $895 rate for `3lz_h07`, referenced by 37 exact
interior leaves. Evidence includes `z06-structured-records.json` PriceRef row 20
and the 37 component memberships retained in the rate's evidence set (starting
at interior_components row 501). The convertible's rate and other models' N2Z
records are distinct. Seat and R6X option charges retain their existing owners.

The editor lists every referencing leaf before review. It evaluates selecting
each interior from that configuration's initial state and shows before/after
totals, requiring exactly one component charge and an exact total-price delta
with unchanged resolved/installed equipment and issues. Other optional builds
are outside this preview. Price input uses integer minor units; a priced zero
retains its basis and does not become a null/no-separate-charge item.

Cancel leaves no persisted change. Save rechecks rate, membership, revision and
executable dependencies under a write lock, then commits the amount, revision
and history atomically after structural/consumer validation. A stale review or
failed validation leaves no partial write. Reload restores saved values. Changing
back uses the same reviewed path and keeps history. Source evidence remains the
baseline evidence, not evidence for accepting a new manufacturer price.

Startup adds one `authoring_component_change` history table to existing local
workspaces. Source import, schema ownership, workbook authority and source-only
release refusal remain unchanged. Focused checks:
`python3 -m unittest discover -s tests -p test_authoring_components.py -v`.

## Completion boundary

This branch implements the option and shared-component-price slices of E.
The direct-inclusion ownership editor is delivered separately in PR #52.
Together these cover the three bounded E pilot operations, subject to PR review
and integration. General relationship/remaining field editors are later F work.
It does not create a generic table editor
or infer shared ownership from repeated names or codes.

The existing release freeze deliberately rejects this authoring schema and
authored source differences. Reviewed-edit acceptance/replay and release
integration belong to the remaining F work; do not strip the history tables or
weaken source checks to publish an edited draft. No live customer form, dealer
submission, artwork processing, deployment or canonical cutover is included.

## Validation

Run the focused regression checks with:

```sh
python3 -m unittest discover -s tests -p test_authoring.py -v
```

They cover source isolation and release refusal, token cancellation/replay,
persistence and consumer names/prices, exact-cent and null/zero semantics,
cross-connection stale edits, rollback of every write, and independent model
ownership across all six lanes. Browser validation exercises the actual local
editor; its final results are recorded in the task PR.
