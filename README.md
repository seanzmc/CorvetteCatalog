# CorvetteCatalog

A fresh project for relational Corvette product data, manufacturer order-guide intake, and configuration data for an order form and visualizer.

## Direction

Build a clean application and schema in this repository. The existing 27vette project is a reference implementation and behavioral comparison baseline, not a codebase to clone wholesale.

- **Current workbook:** `27vette/stingray_master.xlsx` is the canonical source of truth for the existing form and the primary migration baseline for model data, intentional overrides, customer copy, and form behavior.
- **Manufacturer order guides:** the manufacturer Excel export in the root of 27vette is the raw order-guide format, processed and transformed into the `stingray_master.xlsx` format. Preserve raw guides with their model year, revision, and precise source locations.
- **Future relational catalog:** reviewed, accepted business facts with explicit provenance and applicability.
- **Form and visualizer:** consumers of versioned releases from the same catalog.

When a guide and workbook disagree, record the discrepancy and its evidence. Neither silently overwrites the other. Accepting a manufacturer correction may intentionally change current behavior; classify and review that separately from migration parity.

## Start here

- [Working principles and lightweight PR policy](AGENTS.md)
- [Migration and intake plan](docs/migration-plan.md)
- [Workbook translation blueprint: actual rules, ownership and proposed consolidation](docs/workbook-translation-blueprint.md)
- [Checkpoint A source and schema specification](docs/source-schema-specification.md)
- [Current disposable candidate schema in drawDB](docs/drawdb.md)
- [Earlier workbook structure audit](docs/workbook-structure-audit.md)

Reference project: `/Users/seandm/Projects/27vette`.
Reference workbook: `/Users/seandm/Projects/27vette/stingray_master.xlsx`.

## Status

Checkpoint A specification completed September 5, 2026. Checkpoint B's [disposable relational importer](catalog/README.md) is implemented and verified against the [frozen workbook and matching six-model runtime baseline](baselines/2026-09-06/README.md): all 15,134 source rows and 7,448 availability pairs are accounted for. The separately authorized [Checkpoint C brake intake pilot](sources/README.md#checkpoint-c-local-completion) preserves 26 review assertions, 19 unchanged and 7 ambiguous, with repeatable immutable staging. Checkpoint D now [generates and verifies all six contracts directly from the candidate catalog](catalog/README.md#checkpoint-d-direct-form-generation), preserving the frozen baseline and browser registry. The [schema-3 option consolidation](catalog/README.md#option-consolidation-schema-3) replaces six option tables with one model-owned option table, with source facts and six-model parity preserved. The SQLite database is a disposable candidate; no application, canonical-data change or deployment has been made. No changes were made to 27vette.
