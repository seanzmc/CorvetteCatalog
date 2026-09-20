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

## Completion boundary

This implements option editing and bounded direct-inclusion ownership editing.
A genuinely shared record selected after ownership review remains the other E
pilot. Other relationship families and linked endpoint editing remain later work. It does not create a generic table editor
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

## Direct inclusion relationship editor

Open **Edit option relationships** from the option editor, or `/relationships`.
Choose a model and direct option inclusion, then change whether a prior independent
purchase is preserved or absorbed by its source package. The source/target options,
condition, scope, peer policy, prices and provenance remain unchanged. This pilot
changes ownership policy, not inclusion endpoints or linked prerequisite groups.

Review executes the real evaluator in every recorded configuration: independently
purchase the included option, select its source package, then remove the package.
It shows before/after resolved options, independent intent, charges and totals.
Relationships that cannot demonstrate this sequence are refused with a configuration-
specific error. These bounded sequences are not exhaustive build acceptance.
Cancel rolls back the candidate and retains unsaved fields. Save rechecks executable
dependencies and the exact reviewed results under a write lock, validates structural
and consumer mappings, and commits policy/version/history together. Changing the
policy back uses the same reviewed path and keeps both history entries.

Server startup adds `authoring_relationship_change` to an existing authoring workspace;
no source reimport or destructive migration is required. Existing option edits remain
available. Authored drafts remain excluded from source-only release freeze.

Focused checks: `python3 -m unittest discover -s tests -p test_authoring_relationships.py -v`.
The evidence-backed exercise is Stingray PDY → RYT: the existing $60 independent RYT
purchase survives PDY removal under `preserve_prior`; a synthetic local edit to
`absorb_prior` removes that purchase with PDY in all six configurations. The demo is
restored after browser validation; it does not accept a business correction.
