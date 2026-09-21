# CorvetteCatalog

A local Corvette catalog editor and build-review app for Stingray, Grand Sport,
Grand Sport X, Z06, ZR1 and ZR1X. Edit catalog data, review and accept changes,
create a versioned release, then use that release in the customer form with
pricing, equipment, artwork, order export and dealer-submission preview.

## Set up

Run these commands from the repository root with Python 3.11 or newer:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Activate the environment in each terminal before running the commands below.
The local app uses SQLite and the source records checked into this repository;
there is no separate database service or frontend build step. Keep generated
workspaces and releases under the Git-ignored `.local/` directory.

## Start the catalog editor

On first use, create a source database and a separate editable workspace:

```sh
python -m catalog.releases prepare .local/authoring/source.sqlite
python -m catalog.authoring_server \
  --database .local/authoring/draft.sqlite \
  --initialize-from .local/authoring/source.sqlite
```

Initialization exits after creating the workspace. These commands refuse to
overwrite existing databases. For normal use, start the existing workspace:

```sh
python -m catalog.authoring_server --database .local/authoring/draft.sqlite
```

Open [the catalog editor](http://127.0.0.1:8766). Leave the terminal running;
press `Ctrl+C` to stop it. Saved edits persist in `draft.sqlite`.

| Page | Use it for |
| --- | --- |
| [Option editor](http://127.0.0.1:8766/) | Find an option by model, RPO or name; review and edit its name and base price. |
| [All catalog editors](http://127.0.0.1:8766/records) | Edit products, availability, interiors, prices, connected rules and customer copy; queue related changes together. |
| [Inclusion ownership](http://127.0.0.1:8766/relationships) | Control whether a package preserves or absorbs an earlier independent purchase of an included option. |
| [Shared component prices](http://127.0.0.1:8766/components) | Edit a component rate and review its effect on the interiors that reference it. |
| [Acceptance and releases](http://127.0.0.1:8766/acceptance) | Review saved history and intake evidence, accept the exact draft and build a release. |

Choose the model and record, enter changes and a reason, review their effects,
then save. Use **All catalog editors** for coupled changes that must save together.
A stale review must be reloaded and reviewed again. Saved history retains earlier
values; restoring a value is another reviewed edit. A zero price and an item with
no separate charge have different meanings.

## Create a release

Saving an edit updates the draft. To make that draft available to the customer form:

1. Open **Acceptance and releases**, review the saved changes, and enter a reviewer
   and reason.
2. Review and confirm the acceptance. Later edits require a new acceptance.
3. Click **Create release from accepted draft**. Keep the server running while it
   checks source replay and all six models, generates artifacts and verifies the
   bundle. This can take several minutes.
4. Copy the completed **Release** ID and **Store** path shown on the page. With the
   setup above, the store is `.local/authoring/releases`.

To try the form with the checked-in catalog before making any edits, build a
source release instead:

```sh
python -m catalog.releases prepare .local/preview/draft.sqlite
# Replace DRAFT_SHA256 with the digest printed by prepare.
python -m catalog.releases --store .local/preview/releases freeze \
  .local/preview/draft.sqlite --expected-digest DRAFT_SHA256
# Replace FROZEN_ID with the ID printed by freeze.
python -m catalog.releases --store .local/preview/releases complete FROZEN_ID
```

The last command prints the completed release ID. Use `.local/preview/releases`
as the store when starting this release. Use fresh paths for a new source draft;
keep existing authoring workspaces to preserve their edits and history.

## Run the customer form

In another terminal, substitute the completed release ID and its store path:

```sh
python -m catalog.consumer_server \
  --store .local/authoring/releases --release RELEASE_ID
```

Open [the build-review form](http://127.0.0.1:8765). Both servers accept `--port`
if their default port is occupied, and both bind to `127.0.0.1` for local use.

Choose a model and body/trim configuration, then start a build. Review option and
interior changes before confirming them. Cancel preserves the current build;
**Revert last change** also requires confirmation. Prices, equipment, artwork and
order output follow the confirmed build. Complete required selections and resolve
pending changes before using **Export build** or **Preview dealer submission**.
Build sessions are held in memory and are lost when the consumer server restarts.

Dealer preview prepares the order without sending it or loading the security
check. Live delivery requires starting the consumer server with
`--enable-dealer-submissions` on a qualified host; the browser then uses Turnstile
and the existing dealership endpoint. Local preview does not establish production
delivery or dealer receipt.

Artwork currently covers selected paint/spoiler combinations for coupe and
convertible Grand Sport and Stingray in 3LT, and Z06, ZR1 and ZR1X in 3LZ.
Stingray supports GBA, G8G and GKZ with 5ZU; other supported families have ten
paints. Unsupported combinations, including Grand Sport X, show an unavailable
state. Wheels, interiors, brakes, roof positions and other equipment remain fixed
in the images and may differ from the build.

The form serves a completed release, so editing the draft does not update an
already running form. Create a new release and restart the consumer server with
its new ID to see accepted changes.

## Verify and back up a release

Use the store and completed release ID from your build:

```sh
python -m catalog.releases --store .local/authoring/releases verify RELEASE_ID
python -m catalog.releases --store .local/authoring/releases \
  backup RELEASE_ID .local/release-backup
python -m catalog.releases --store .local/recovered-releases \
  restore .local/release-backup
```

Use a new backup destination for each backup. Restore verifies the bundle and
prints its release ID; it does not publish or deploy it.

If the checkout has changed since a release was created, the consumer may report
**Use the runtime pinned in this release**. Run that bundle's runtime instead
(Python 3.11+; replace `RELEASE_ID` and the store path as needed):

```sh
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=.local/authoring/releases/completed/RELEASE_ID/runtime \
  python -P -m catalog.consumer_server \
  --store .local/authoring/releases --release RELEASE_ID
```

The existing form's canonical source remains `27vette/stingray_master.xlsx`.
Local edits, acceptance and releases do not change that workbook or deploy the
production site. Preserve the checked-in source evidence and release bundles;
use the editor for catalog changes.
