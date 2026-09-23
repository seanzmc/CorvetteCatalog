# Form audit and live-migration plan — September 22, 2026

This is an audit of the current checkout (`main` at `dc2618f`, PR #60) and a
proposed path to (1) make routine catalog changes easy and (2) replace the live
order form at `order.stingraychevroletcorvette.com`. It is a planning document:
it changes no code, data, artwork, workbook or deployment, and it does not
authorize implementation, cutover or merge. The owner's September 23 answers
to the open decisions are recorded in §7 and applied in the sections below.

## 1. Where things stand

| Area | State | Evidence |
| --- | --- | --- |
| Catalog and rules | Six models, 32 configurations, server-side evaluator; 6,921-entry audit passes with zero findings | [migration-plan](migration-plan.md), `catalog/evaluator.py` |
| Editor | Local editor for options, prices, rules, interiors, shared component rates, copy, inclusion ownership; reviewed acceptance and release creation | [authoring-operations](authoring-operations.md), `catalog/authoring_server.py` |
| Releases | Prepare, freeze, complete, verify, publish/rollback a channel, backup/restore | [consumer-releases](consumer-releases.md), `catalog/releases.py` |
| Customer form | Familiar step-by-step form; confirm/cancel/undo; review; JSON download; dealer preview | `catalog/web/`, `catalog/consumer_server.py` |
| Dealer delivery | Existing WordPress endpoint and Turnstile wired, off by default; no real receipt yet | [dealer-submission](dealer-submission.md) |
| Artwork | 10 scenes, 192 planes, 146 paint/spoiler combinations, 34 MB | [visualizer-artwork](visualizer-artwork.md) |
| Live site | 27vette static form (`index.html`, `app.js`, `data.js`, `styles.css`), no backend, behind Cloudflare; generated from `stingray_master.xlsx` | `27vette/README.md`, response headers |
| Canonical source | Still the 27vette workbook | [migration-plan §8](migration-plan.md#8-owner-clarifications-and-remaining-decisions) |

The core modeling work is done and well verified. What remains is operational:
the new form can only run on one machine, edits live only on that machine, and
there is no path from an accepted release to the public site.

## 2. Functional gaps

Ranked by how much each one blocks going live.

### 2.1 Blocks going live

1. **The new form needs a server; the live form has none.** The live form is
   static files. The new form calls `/api/session`, `/api/preview` and
   `/api/confirm` on a Python process that loads a ~150 MB `catalog.sqlite`
   from the release. That database is far too large to ship to the browser, and
   rewriting the evaluator in JavaScript would recreate two rule engines. Going
   live means hosting the Python consumer somewhere. See §4.
2. **The consumer server only works locally.** `consumer_server.py` binds to
   `127.0.0.1` and rejects any `Host`/`Origin` other than `127.0.0.1:<port>`.
   It uses the single-threaded `HTTPServer`, so one slow evaluation blocks every
   other visitor. There is no request logging, health check or rate limiting.
3. **Sessions run out and disappear.** Sessions live in an in-memory dict with a
   hard cap of 256 and no expiry. After 256 visitors, every new build fails with
   "Local session limit reached; restart the review server" until a restart.
   Reloading the page or restarting the server also loses the customer's build.
4. **No real dealer receipt proof.** The payload matches the existing wire format
   and failure cases were exercised, but no order has been delivered to and
   confirmed by the dealership. The Content Security Policy also hard-codes the
   loopback origin.
5. **Two sources of truth.** The live form is still generated from the workbook.
   Any workbook change after the catalog's pinned baseline, or any catalog edit
   before cutover, makes the two forms drift. No automated check watches for
   that drift. As of September 23 there is none: `stingray_master.xlsx` still
   has the SHA-256 pinned in `baselines/2026-09-06/manifest.json`
   (`3127e663…8e3c`), and the live `data.js` is byte-identical to
   `27vette/form-app/data.js`.

### 2.2 Blocks easy changes

6. **Edits exist on one machine only.** The editor draft
   (`.local/authoring/draft.sqlite`), its history and every release store are
   Git-ignored. There is no automatic backup, so losing the disk loses every
   reviewed edit since the checked-in source. Backups are manual per release.
7. **Too many steps to see a change.** Edit → save → accept (reviewer and
   reason) → create release (minutes) → copy release ID and store path → stop the
   form → restart it with that ID. `scripts/preview.py` hides this for the
   checked-in catalog only, not for edited drafts. `releases.py` already has a
   channel pointer with publish/rollback, but the consumer server takes a fixed
   `--release`, not a channel.
8. **No CI in this repository.** `.github/` only holds the PR template. Tests
   run only when someone runs them by hand, and the plain
   `python3 -m unittest tests.test_artwork_collection` form fails to import
   (`No module named 'test_consumers'`); it works with
   `python3 -m unittest discover -s tests`. That entry point is not documented.
9. **Out of the editor's scope today:** new model years or model foundations,
   new customer-layout structures (steps and sections beyond the existing ones),
   and a whole-guide parser for the next manufacturer order guide. The next model
   year needs all three.

### 2.3 Form parity with the live site

| Live form has | New form | Note |
| --- | --- | --- |
| CSV build download | JSON only | Customers can open CSV; JSON is for machines |
| Model-card photos (`image_url` from the workbook `asset_map`) | Text drop-downs | Model/body/trim chooser is plainer than live |
| WordPress styling, logo and favicon | Local theme, "Local preview" footer | Needs production copy and branding |
| Works after reload (state in the page) | Build lost on reload | See 2.1 item 3 |
| No server dependency | Offline if the API is down | Needs a friendly outage state |

Not found in either form: shareable build links, print view, saved builds,
analytics. These are optional additions, not parity gaps.

## 3. Photoshop asset audit

### 3.1 What is in use

Source folder: iCloud `C8-iCloud/27img/visualizer-studio_27/visual-studio`.
Each bound scene comes from exactly one PSB:

| Scene | Source PSB (exterior view used) | Trim | Paints | Spoilers |
| --- | --- | --- | --- | --- |
| Grand Sport coupe | `grandsport/e.coupe.exterior.01 - cleaned.psb` | 3LT | 10 | T0F, 5ZV |
| Grand Sport convertible | `grandsport/e.convertible.exterior.01.psb` | 3LT | 10 | T0F, 5ZV |
| Stingray coupe | `stingray/c.coupe.exterior.01.psb` | 3LT | 3 | 5ZU (paint-matched) |
| Stingray convertible | `stingray/c.convertible.exterior.01.psb` | 3LT | 3 | 5ZU (paint-matched) |
| Z06 coupe / convertible | `z06/exterior/27CHCORZ_{COU,CON}_Studio_f02.psb` | 3LZ | 10 | T0F, T0G, 5ZV |
| ZR1 coupe / convertible | `zr1/exterior/27CHCOZR_{COU,CON}_Studio_f02.psb` | 3LZ | 10 | TOM |
| ZR1X coupe / convertible | `zr1x/exterior/27CHCOZR_X_{COU,CON}_Studio_f02.psb` | 3LZ | 10 | TOM |

Every model offers the same ten paints (G8G, GBA, GKA, GBK, GTR, GEC, GPH, G4Z,
G26, GKZ). Recipes, export scripts and native comparisons live in
`27vette-phase1/` (`ASSET-WORKFLOW.md`, `REPRODUCE-PROOFS.md`).

### 3.2 Coverage gaps

- **Configurations:** artwork covers 10 of 32 configurations. 1LT/2LT and
  1LZ/2LZ show "unavailable" because bindings are exact by trim. **Decided:**
  3LT/3LZ scenes must not stand in for lower trims; those trims have subtle
  visual differences. Covering them needs trim-specific exports. The next step
  is to inspect the existing PSBs for lower-trim layers before looking for
  other sources.
- **Grand Sport X:** no source PSB in the folder. Nothing to bind.
- **Stingray:** 3 of 10 paints, and only with 5ZU. Stingray builds without 5ZU,
  or in the other 7 paints, show "unavailable".
- **Components:** only paint and rear spoiler change. Wheels, calipers, stripes,
  roof panels, mirrors, badges, exhaust tips and the convertible top stay fixed.
  The Grand Sport roof proof needs 5 planes; the renderer supports 3 (back,
  spoiler, foreground). Wheels and stripes need a more general stack.
- **Views:** one exterior camera per body. The second exterior view in every
  family (`*.exterior.02.psb`, `*_Studio_f04.psb`) is unused.
- **Interior:** no interior art. Twenty interior PSBs (6–7.6 GB each: 
  `*.interior.01/02.psb`, `*_Interior_f01/f02.psb`) are unused.
- **Unused supporting sets:** `27CHCORV_PaintSwatches`, `_MaterialSwatches`,
  `_WheelSwatches` (several sizes), `_Exterior_360(_v2)`, `_Interior_360(_v2)`,
  `_Cut_Art_v2` and a 3D model. Swatches would give paint, material and wheel
  cards a thumbnail with no compositing work.
- **Housekeeping:** the source folder mixes originals with working copies
  (`e.coupe.exterior.01.copy.psb`, `c.coupe.exterior.01 copy.psb`, the
  "cleaned" file). Proofs pin exact file hashes, so this is safe, but a short
  `SOURCES.md` in that folder naming the authoritative file per scene would make
  re-exports less error-prone. Empty `exports/`, `manifests/`, `tools/` folders
  suggest an unfinished layout.

### 3.3 Rights

The `27CHCORV_*` and `27CHCORZ_*`/`27CHCOZR_*` sets look like manufacturer media
kits. **Decided (September 23):** the owner confirms the images may be published
on the dealer's public site. This settles the rights item in H for the supplied
folder; newly acquired sources need the same confirmation.

### 3.4 Launch scope

**Decided:** artwork launches with the form. With the trim decision above, the
launch shows artwork for the 10 bound 3LT/3LZ scenes, and an explicit
"unavailable" state for Grand Sport X, all 1LT/2LT/1LZ/2LZ configurations and
Stingray outside GBA, G8G and GKZ with 5ZU. The form stays fully usable in each
of those cases. More coverage before launch is optional work under task 8; it
does not block launch.

### 3.5 Delivery weight

34 MB total, about 3.5 MB per scene, three full-canvas lossless WebP planes per
view. Before going live: serve through Cloudflare with long-lived caching (put the
manifest's content hash in each URL so updates bust the cache), load only the chosen scene, and consider lossy WebP
or AVIF for the back plane after a visual comparison against the proof.

## 4. Getting to the live site

### 4.1 Recommended shape

**Decided:** Cloudflare hosts the new form.

```text
Local editor ──accept──▶ release bundle ──build──▶ container image
 (your Mac)             (hashed, verified)         (pinned runtime + release)
                                                      │ deploy
Browser ──▶ Cloudflare Worker ── static files + artwork (cached)
                  │
                  └── /api/* ──▶ Cloudflare Container (Python consumer)
        ──── dealer submit ──▶ existing WordPress endpoint (unchanged)
```

- Keep one evaluator: run the existing Python consumer. Do not port rules to
  JavaScript, and do not ship the SQLite file to browsers.
- Use **Cloudflare Containers** for the consumer, behind a **Worker** that serves
  the static page and artwork and routes `/api/*` to the container. A plain
  Python Worker is not suitable: it cannot hold the ~150 MB release database
  within Worker memory and bundle limits. Confirm current Containers plan limits
  (instance memory, disk, cold start) when implementing task 6.
- Start on a separate hostname (for example `build.stingraychevroletcorvette.com`)
  in the Cloudflare zone that already serves the domain, with the old form
  untouched.
- Build one container image per release: the release's pinned runtime plus its
  verified bundle. Publishing deploys that image; rollback redeploys the
  previous one. The deployed image version plays the role of the `production`
  channel.

**Runtime constraint on channel swaps.** `Application.__init__` rejects a
release whose runtime hashes differ from the running checkout
(`catalog/consumer_server.py`), and each completed release documents its pinned
runtime (`consumer-releases.md`). A pointer swap alone therefore cannot serve a
code-bearing release, and a rollback across runtime versions would keep serving
the old application. Task 4 below must pair channel changes with an atomic
restart/deploy on the target release's pinned runtime — the deploy step uploads
the release, moves the channel and restarts the server on that release's
runtime as one action — or explicitly restrict channel changes to
runtime-compatible releases, including rollback. Per-release container images
satisfy the first option: each image already contains its own pinned runtime,
and a Containers deploy replaces the running version as one action. Planning
acceptance here does not authorize implementation.

### 4.2 Server hardening needed first

1. Configurable bind address and allowed origins; production CSP naming the real
   host, Turnstile and the dealer endpoint.
2. Threaded or process-pooled serving, a `/healthz` endpoint, and access logs
   without personal data.
3. **Decided:** replace the 256-session dict with a signed, client-held build
   token. The token carries the release ID, configuration and the confirmed
   action history; the server verifies the signature and replays the history to
   rebuild the session. That lets the build survive a page reload, a container
   restart or a request landing on another instance, and later enables
   shareable build links. Pending preview tokens stay short-lived and
   server-verified. A token from an older release needs a defined result:
   replay against the current release and show the resulting changes, or ask
   the customer to start over. Keep the signing key in a Cloudflare secret.
4. Per-IP rate limits on `/api/session` and `/api/preview` (Cloudflare rules are
   enough).
5. A friendly "form temporarily unavailable" state in the page.

### 4.3 Staged rollout

| Stage | Outcome | Exit check |
| --- | --- | --- |
| A. Hardening | 4.2 done, still local | Load test of concurrent sessions; existing consumer/dealer/release tests pass |
| B. Staging host | Consumer on a private staging URL, dealer preview only | Full six-model browser pass; release verify on the host |
| C. Dealer proof | One real test order to the dealership, with them expecting it | Dealer confirms receipt and content |
| D. Public beta | Public hostname, linked from the site as "new builder", old form still primary | A week of real traffic without errors; drift check clean |
| E. Cutover | Old URL points to the new form; workbook retired as a generator | Explicit owner approval (G) |
| F. Retire | Old form archived; 27vette read-only | After an agreed quiet period |

Rollback at every stage: repoint DNS or the Cloudflare route to the old static
form, which stays deployed until F.

### 4.4 Canonical cutover (G)

"Freeze" means two different things, and they happen at different times:

1. **Change freeze, now.** Do not edit `stingray_master.xlsx`. The catalog was
   built from the September 6 baseline, and workbook edits do not flow into it;
   any workbook edit would have to be repeated by hand in the catalog editor.
   The workbook is still byte-identical to that baseline (§2.1 item 5), so
   nothing needs reconciling yet. If the live site needs a change before cutover,
   make it in both places and record it.
2. **Generation freeze, at stage E.** Until cutover, keep using the workbook to
   generate the live form's `data.js`, because the old form stays live. At
   cutover the new form replaces it, the workbook stops generating anything, and
   the catalog becomes the only place to make changes.

Before stage E, run a final comparison of the workbook and the catalog for every
model, and record each difference as either an accepted correction or a defect.
Cutover itself still needs explicit owner approval.

## 5. Making changes easy

Target: edit in the browser, click **Publish**, the live form updates, one click
rolls back.

1. **One publish action.** After acceptance, a **Publish** button (or
   `python -m catalog.releases ship`) creates the release, verifies it, uploads
   it to the host and moves the `production` channel. No release IDs to copy.
2. **Automatic backup of edits.** Back up `draft.sqlite` and its history after
   every save, or at least nightly, to a location off the Mac (iCloud folder or
   a private bucket). Keep release backups on the host as well.
3. **Preview edited drafts.** Extend `scripts/preview.py` with a `--draft`
   option that builds a release from the current accepted draft, so checking a
   change does not need manual release commands.
4. **CI.** A GitHub Actions workflow running the focused suites under two
   minutes (consumer, dealer, releases, artwork, authoring) on each PR, and the
   full six-model audit on demand. Document
   `python3 -m unittest discover -s tests` as the test entry point.
5. **A short "how do I" guide** for the five common edits: change a price,
   rename an option, turn an option off, change which options require or exclude
   each other, change customer copy. The README currently documents commands,
   not tasks.
6. **Next model year.** Plan the foundations editor and order-guide intake
   (2.2 item 9) before the 2028 guide arrives; the editor cannot create a new
   year today.

## 6. Suggested task order

Each row is a separately authorized task and PR. The authoritative version of
this sequence lives in [migration-plan.md](migration-plan.md) ("September 22
form audit and live-migration rollout"); this section is retained as audit
detail. Keep the two in sync when tasks are re-ordered or added.

| # | Task | Why now |
| --- | --- | --- |
| 1 | CI workflow and documented test entry point | Protects every later change |
| 2 | Automatic draft/release backup | Protects edits already made |
| 3 | Consumer hardening (4.2) | Required for any hosting |
| 4 | Channel-following server and one-step publish (5.1, 5.3) | Makes edits easy locally and remotely |
| 5 | Parity items: CSV download, model photos, production branding | Customers notice these |
| 6 | Cloudflare staging (stage B): Worker, Container, secrets | Hosting decided |
| 7 | Real dealer receipt proof (stage C) | Needs dealership coordination |
| 8 | Artwork for launch: delivery through Cloudflare, swatches, optional lower-trim exports, second view | Launches with the form; can run in parallel after 3 |
| 9 | Public beta, freeze, cutover (D–E) | Last; needs explicit approval |
| 10 | Model-year foundations and guide intake | Before the next guide |

## 7. Owner decisions — September 23, 2026

| # | Question | Decision |
| --- | --- | --- |
| 1 | Hosting provider (4.1) | Cloudflare |
| 2 | Keeping builds across reloads (4.2) | Signed client-held build token |
| 3 | 3LT/3LZ artwork for lower trims (3.2) | No; 1LT/2LT and 1LZ/2LZ differ visually |
| 4 | Image publication rights (3.3) | Owner confirms the images may be published |
| 5 | Artwork timing (3.4) | Launches with the form |
| 6 | Workbook freeze (4.4) | Change freeze now (workbook unchanged since baseline); generation stops at cutover |

Still open: the cutover date (stage E) and the dealership coordination for the
test order (stage C).

## 8. How this audit was checked

Read the README, roadmap, artwork, release, dealer and authoring docs; the
consumer server, preview script and web client; the 27vette README and live
form; each artwork `source-proof.json` for its PSB; and the iCloud source
folder listing. Counted live paints and trims from `27vette/form-app/data.js`.
Checked the live form's response headers and HTML. Ran
`python3 -m unittest discover -s tests -p test_artwork_collection.py`
(4 tests, OK). On September 23, compared the workbook's SHA-256 with the
September 6 baseline manifest (equal) and the live `data.js` with the 27vette
copy (equal). The full suites and the six-model audit were not run; nothing
here changes behavior. The live host's deployment mechanism behind Cloudflare
was not confirmed from this checkout.
