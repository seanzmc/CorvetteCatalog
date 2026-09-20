# Catalog editing, acceptance and local releases

The local authoring application now covers the existing catalog's product,
availability, interior, pricing, relationship and presentation fields. These are
management screens; the customer form and dealer integration keep their separate
migration scope. Workbook authority and the frozen migration baseline are unchanged.

## Edit a coherent change

Start the application using the setup in [the authoring pilot](authoring-pilot.md).
Open **All catalog editors** (`/records`). Choose a model, editor and record. The
editors cover:

- Body/trim labels, enabled state, ordering and exact starting prices.
- Option codes, names, selectability, lifecycle and explicit charge semantics;
  configuration availability and selection overrides.
- Interior choices, seat ownership, component membership, applicability and rates.
- Conditions, positive/negative clauses and option/interior/group members.
- Inclusions/defaults, continuing prerequisites, conflicts, choice groups,
  replacements and their actions, contextual prices, equipment substitutions,
  conditional equipment descriptions and each rule's configuration scope.
- Customer descriptions, interior hierarchy labels, steps/sections, summaries,
  display ordering and explicit order-code emission roles.

Prices are entered as decimal currency amounts and stored as integer minor units.
Zero is a priced amount; null/no-separate-charge remains a separate meaning with
its own basis constraints. Model-owned references cannot cross model revisions.
Duplicate consumer names/codes and configuration amounts follow their typed owner;
copy screens cannot overwrite those facts independently. Selected-interior output
also exposes its actual configured code, seat and component owners, separately
from retained descriptive source fields.

Queue related changes across editors, then review and save the complete set in
one transaction. For example, changing an inclusion target also requires reviewing
its continuing prerequisites and applicable configurations. References to queued
new rules are available when adding their members/actions/scopes. A new rule can
be created even when that model has no existing record of its type. Copying an
option or interior creates a new identity and its owned consumer/availability
context. Copying a rule retains its members and scope; its other endpoints stay
explicit and model-owned. New records inherit baseline source context, which is
not evidence that the manufacturer asserted the new fact.

Retire or disable product identities; do not delete their history. Removing a
relationship or membership archives its exact row and affected typed translation
links in the change history. Original source documents, anchors and dispositions
remain intact. New model/year foundations and additional customer-layout record
structures are outside this editor surface; existing presentation structures can
be edited without replacing their retained identifiers.

Review shows every row change, all initial configurations, affected condition
witnesses, referencing interiors, charges, independent purchases, installed
state, order codes and supplying owners. Additional selection/removal sequences
can be included. Missing witnesses are explicit; newly impossible previously
active relationships and contradictory affected overlaps are refused. The review
is bounded behavior evidence, not a claim to enumerate every possible build.
The complete six-lane audit still runs at release freeze.

Save revalidates the same server-held candidate under a write lock, checks typed
constraints/consumer mappings, increments the revision, and writes before/after
history together. Another edit or raw database change invalidates the review.
Cancel retains the unsaved queue. Save/reload preserves accepted values. Restoring
an earlier value uses a new reviewed edit, preserving the earlier history.

## Review intake and accept a draft

Open **Acceptance and releases** (`/acceptance`). Saving a draft and accepting it
are separate actions. Review the saved history, enter a reviewer and reason, and
confirm the exact acceptance preview. The application checks the recorded edits
against the source baseline before presenting that preview, then checks again
under the write lock before recording the decision. New edits need new acceptance.
This remains a local, single-user decision record, not an authentication system.

Manufacturer intake stages one explicitly interpreted assertion at a time. Supply
its preserved repository source path, verified SHA-256, exact locator, model/scope,
comparison classification, coverage and known ambiguity. Repeating identical input
reuses its content identity. Pending, deferred and rejected assertions remain
visible and do not change product facts. To accept an assertion, link it to exact
saved edit references and record the evidence/ambiguity resolution. A removal
assertion requires complete relevant coverage. Acceptance never automatically
copies an entire guide row over dealer-authored facts.

This provides the review/acceptance boundary for interpreted intake. It does not
claim a new whole-guide parser, resolve the historical brake assertions by default,
or modify C's immutable staging files or `accepted_operations` evidence. Those
facts require their own explicit, evidence-backed decisions through this workflow.

## Reproduce and recover an authored release

**Create release from accepted draft** runs the existing release builder in the
background. It verifies the exact accepted draft, audits all active scopes in all
six models, generates the consumer artifacts, and verifies the completed bundle.
Disabled configurations/interiors remain recorded but cannot be selected as active
builds. The page reports failure or the completed release identity and store.
It does not publish a channel or deploy anything.

The CLI supports the same boundary:

```sh
python3 -m catalog.releases digest .local/authoring/draft.sqlite
python3 -m catalog.releases freeze .local/authoring/draft.sqlite --expected-digest DRAFT_SHA256
python3 -m catalog.releases complete FROZEN_ID
```

The UI uses a `releases` directory next to its draft database. The CLI defaults to
`.local/releases`; use `--store` to select the same store when mixing interfaces.
Existing verify, publish, rollback, backup and restore commands remain documented
in [consumer releases](consumer-releases.md).

The authored release validator:

1. Checks the recognized authoring schema, complete ordered edit history and
   exact current acceptance.
2. Reverses every recorded edit in a separate copy and requires the original
   workspace baseline digest.
3. Runs the unchanged pinned source-translation validation on that baseline.
4. Replays the recorded operations in order, verifies their before values and
   requires exact equality with the edited catalog and consumer mappings.
5. Runs the real semantic audit on the captured snapshot; concurrent draft or
   runtime changes refuse the release.

It does not strip history to make a draft appear source-derived. Every authored
bundle contains the database's complete history and a hashed `reviewed-edits.json`
artifact with the source baseline, exact edits, evidence, intake dispositions and
acceptance decision. Frozen/completed identities bind that artifact along with the
catalog, runtime, validation and all consumer outputs. Unrecorded edits, altered
history/evidence, stale acceptance and missing artifacts fail verification.

A restored completed bundle can initialize a new authoring workspace using its
`catalog.sqlite` with `--initialize-from`. Accepted replay is verified first; the
baseline and history continue in the new copy. The immutable bundle is unchanged.
Backup/restore never publishes the recovered release automatically.

## Validation

Focused regression coverage lives in `tests/test_authoring_operations.py`, alongside
the existing pilot, consumer and release tests. The acceptance/recovery cases run
real source replay; lifecycle fault tests may replace only the expensive semantic
audit, clearly marking that substitute. A separate real six-lane freeze qualifies
the evaluation/release path and actual authored snapshot. The task PR records exact results,
browser flows and any remaining limitations.
