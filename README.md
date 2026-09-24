# CorvetteCatalog

A local Corvette catalog editor and build-review app for Stingray, Grand Sport,
Grand Sport X, Z06, ZR1 and ZR1X. Edit catalog data, review and accept changes,
create a versioned release, then use that release in the customer form with
pricing, equipment, artwork, order export and dealer-submission preview.

## Open the current build

From the repository folder, run:

```sh
python3 scripts/preview.py
```

The command opens the customer form in your browser. It reuses a verified build
matching the current code and catalog, or prepares one automatically. The first
launch can take several minutes; later launches reuse the build until its code
or source data changes. No environment setup, release IDs or copied hashes are
needed for this preview. Python 3.11 or newer is required.

Leave the terminal open while using the app; press `Ctrl+C` to stop. If port 8765
is already in use, run `python3 scripts/preview.py --port 8767`. Add `--no-browser`
to print the address without opening a browser.

Choose a model and configuration, then click **Start build**. Review and confirm
option/interior changes. For an artwork example, try **Corvette Grand Sport Coupe 3LT**,
then select and confirm **GBA Black** paint and the **5ZV** spoiler. Other equipment
remains fixed in the image. Dealer submission stays in preview mode.

This opens the checked-in catalog. Unsaved or unreleased editor changes are not
included. The instructions below are only needed for editing catalog data or
managing a specific release.

<details>
<summary>Catalog editing and release administration</summary>

## Set up the editing environment

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
overwrite existing databases. For normal use, start the existing workspace with
backups going to iCloud Drive:

```sh
python -m catalog.authoring_server --database .local/authoring/draft.sqlite \
  --backup-dir ~/Library/Mobile\ Documents/com~apple~CloudDocs/CorvetteCatalog-backups
```

Open [the catalog editor](http://127.0.0.1:8766). Leave the terminal running;
press `Ctrl+C` to stop it. Saved edits persist in `draft.sqlite`.

With `--backup-dir`, the editor saves a compressed copy of the draft when it
starts and after every saved edit, acceptance or intake decision, and copies
each release it creates into `releases/` there. It keeps the newest 20 draft
copies plus the newest one from each of the last 30 days; each is about 25 MB
and each release copy is about 190 MB. If the folder cannot be written, the
editor refuses to start; if a later backup fails, the edit stays saved and the
terminal reports the failure. Without `--backup-dir` the editor warns that
backups are off.

To see or restore backups:

```sh
python -m catalog.draft_backup list ~/Library/Mobile\ Documents/com~apple~CloudDocs/CorvetteCatalog-backups
python -m catalog.draft_backup restore BACKUP_FILE --database .local/authoring/restored.sqlite
```

Restore returns the draft exactly as it was, including saved edits that were
not yet accepted, and never overwrites an existing file. Start the editor with
`--database` pointing at the restored file. Restore a release copy with the
`restore` command under "Verify and back up a release".

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
5. To make it the production release, click **Publish to production** and confirm.
   This writes a deploy package to `.local/authoring/deploy/RELEASE_ID` and then
   moves the `production` pointer. Uploading the package to the host is a separate
   step that is not set up yet.

To preview an accepted draft in the customer form without copying IDs, run
`python3 scripts/preview.py --draft .local/authoring/draft.sqlite`. It reuses the
release of that exact draft or builds one; a draft with unaccepted edits must be
accepted first.

The same release, publish and package steps run from the command line with
`python -m catalog.deploy ship --database .local/authoring/draft.sqlite`. Add
`--backup-dir` to copy the release there too.

A deploy package holds a `Dockerfile`, a `start.sh` and a store with only that
release, which runs on the code pinned in it. The container needs
`CATALOG_ORIGIN` (the public address) and `CATALOG_BUILD_TOKEN_KEY`, and listens on
port 8080. To roll back, move the pointer with `python -m catalog.releases
--store .local/authoring/releases rollback --channel production
--expected-version N` and deploy the previous release's package, recreating it
with `python -m catalog.deploy package --store .local/authoring/releases
--release RELEASE_ID` if needed. To serve whatever production names locally, use
`python -m catalog.consumer_server --store .local/authoring/releases --channel production`.

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

To serve the form beyond this Mac, set a signing key of at least 32 characters,
listen on all interfaces and name the public address browsers will use:

```sh
CATALOG_BUILD_TOKEN_KEY=... python -m catalog.consumer_server \
  --store STORE --release RELEASE_ID --host 0.0.0.0 --origin https://build.example.com
```

The server refuses to start beyond loopback without the key. Keep the same key
across restarts and instances so saved builds stay valid; changing it starts
every customer over. `GET /healthz` reports the release for platform health
checks. Access logs record the request and status but not client addresses.
Apply request rate limits in front of the server (for example Cloudflare rules
for `/api/session` and `/api/preview`).

Choose a model, body style and trim, then click **Choose options**. Use the step
navigation or **Continue** to work through one group at a time. Option cards show
the change to your build total; **Select** or **Remove** opens a confirmation with
equipment and price changes. **Keep current build** cancels; **Undo last change**
restores the previous build after confirmation. Seats and interior colors narrow
to the catalog's exact interior choices.

Use **Review build** to see your selections, remaining requirements and total.
Complete required selections before using **Download build** or **Preview dealer
submission**. **Start over** asks before clearing your selections. Prices,
equipment, artwork and order output follow the confirmed build.

The server keeps no builds in memory. Each response carries a signed build token
that the browser keeps, so a page reload reopens the same build. Without a
configured key, tokens are valid only until the server restarts, and the form
then asks to start a new build. If the catalog has changed since the build was
saved, the form replays it on the current catalog and says so; a build that no
longer fits starts over.

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

## Run the tests

From the repository root, with the editing environment active:

```sh
python -m unittest discover -s tests
```

To run one file, add its name, for example `-p test_consumers.py`. Run tests
through `discover` from the repository root; importing a test module directly
(`python -m unittest tests.test_artwork_collection`) cannot find its sibling
test helpers. The whole suite takes about half an hour on one machine; the
authoring, release and model-discovery files are the slowest.

GitHub Actions runs the same tests on every pull request and push to `main`,
split into parallel jobs, and validates the model handoffs. The Git-ignored raw
manufacturer guide is not available there, so the checks that read it report
as skipped in CI and still run locally. Missing local raw evidence continues to
fail rather than skip. The full six-model semantic audit runs only when started
by hand from the **Tests** workflow with **Also run the full six-model semantic
audit** selected.

</details>
