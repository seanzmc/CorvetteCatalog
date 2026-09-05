# CorvetteCatalog working principles

## Scope and authority
- Build a fresh implementation here. Treat `/Users/seandm/Projects/27vette`
  as read-only reference material; do not inherit its architecture wholesale.
- Read `README.md` and `docs/migration-plan.md` before roadmap work.
- Work on one bounded task at a time. Finish the authorized task and stop;
  do not automatically begin the next checkpoint.
- Preserve source provenance and original evidence. Never silently resolve
  disagreements between manufacturer guides and the workbook baseline.
- In 27vette, the root manufacturer export is raw order-guide input processed
  into `stingray_master.xlsx`, the canonical source of truth for the existing form.
- Planning does not authorize application implementation, canonical-data
  changes, or production cutover.

## Execution
- Inspect relevant files, data, configuration, and execution paths before asking.
- Preserve unrelated work and make the smallest complete change.
- Proceed with requested, reversible work when the intended outcome is clear.
  Ask only for unresolved business decisions, consequential architectural
  choices, destructive actions, or scope expansion that evidence cannot settle.
- Use validation proportional to affected behavior. Explain what was checked
  and any material gaps. Do not add duplicate gates, ceremonial receipts,
  documentation-only checks, or enforcement scripts without demonstrated need.

## Commits and pull requests
- Use one task branch and one PR per independently useful, reviewable outcome.
  A large roadmap checkpoint may span several separately authorized tasks.
- Start task branches from current `origin/main`. Keep implementation, relevant
  tests, and necessary documentation together; keep unrelated cleanup and
  intentional business-data corrections separate from migration-parity work.
- Commit only reviewed task files. Review-fix commits may stay on the PR branch;
  squash merge so `main` has one revertible commit per PR. Use concise commit
  titles describing the resulting change; no mandatory naming taxonomy.
- Deliver requested changes through a PR to `main`; opening it needs no second
  approval. Merging requires an explicit user request. Do not push changes
  directly to `main` after the initial repository bootstrap.
- Analysis-only discussions with no tracked changes need no commit or PR.
  If no remote is configured, leave a verified local commit and report that
  limitation rather than inventing a remote or claiming PR delivery.

## Verification and review
- Before editing, state the intended outcome, affected paths, preserved
  behavior, and smallest checks that can establish success. A brief progress
  update is sufficient; do not create a specification just for this purpose.
- Select checks by actual impact, including callers and consumers, not merely
  changed filenames. Documentation needs diff and consistency review; localized
  code needs focused regression checks; UI behavior needs an affected-flow
  browser check when practical. Shared schema, pricing, or rule changes need
  coverage across affected models and consumers.
- For drift, compare affected behavior/output with an identified baseline and
  explain meaningful differences. For data accuracy, reconcile identities,
  values, applicability, relationships, price semantics, and omissions against
  source evidence. Report added, changed, removed, and unresolved facts with
  source references. Row counts alone are not proof of parity.
- Expected values must come from inspected evidence. Do not automatically
  refresh snapshots to bless changed output; preserve the distinction between
  migration parity and intentional manufacturer corrections.
- Review the diff for unnecessary files, dependencies, abstractions, duplicated
  ownership, and unrelated changes. Passing tests does not prove simplicity
  or factual accuracy.
- Target routine automated checks under two minutes. Investigate runs exceeding
  five minutes and explain broader coverage when impact requires it; these are
  budgeting targets, not permission to skip necessary checks or call a timeout
  a pass. Reserve full parity/recovery checks for relevant milestones and
  releases, unless the current change directly affects those guarantees.
- Default to one worker inline, one focused review and one fix round. Concrete
  unresolved defects block merge; report them at a clean checkpoint rather
  than starting an unbounded review loop. Re-run affected checks after fixes;
  repeat broader checks only when changed assumptions or failures justify it.
- Add executable checks as implementation risks appear. Each new check must
  catch a specific failure existing checks miss. Do not add validation
  frameworks, mandatory slow hooks, receipt collections, or duplicate gates.
- Report checks actually run, results, and material gaps in the PR. Checks must
  cover the final relevant revision; do not claim stale results cover later
  behavioral changes. Merge and deployment remain separate actions.

## Documentation and handoffs
- Keep durable instructions here and the overall roadmap in
  `docs/migration-plan.md`. Do not create a specification for every task.
  Small tasks can use their PR description; complex work gets a specification
  only when it resolves meaningful ambiguity.
- Keep Git-ignored `.local/STATUS.md` concise and current. Include the current
  task and branch, completed work, validation results, blockers or decisions,
  and next action. Replace stale status at meaningful handoffs, not every command.
- Record milestone completion in the roadmap as part of the related change;
  do not create a separate commit or PR merely to update progress.
- Focus PR descriptions on the problem, resulting behavior, relevant validation,
  and remaining limitations.
- These are working principles, not a workflow framework to implement.
