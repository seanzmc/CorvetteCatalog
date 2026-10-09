# Visualizer source coverage and export gaps
Audit date: **October 9, 2026**. This is an inventory and review plan, not artwork acceptance, an export, a binding, or a renderer change. All paths below are local source evidence; no PSB, PNG, manifest or application file is added by this task.

## Findings that change the next artwork task

- **Stingray has all ten paints in all four source views**, including the seven absent from the binding. Its saved sources also contain ten body-color 5ZU variants, 5ZZ, 5ZW, 5V5 and internal low/Z51-looking spoiler families. The last two descriptions are only candidates: internal `S011*` identities are **unmapped**, not accepted TVS/T0A identities. The two existing 5ZU bindings remain on disk but are unusable against the R3 catalog because 5ZU is `factory_unavailable`.
- **Lower-trim layers mostly exist.** `Base / S0507&1LT` is absent from Stingray coupe view 01 (S09); its 2LT peer exists. All other supplied non-GSX body/view files have explicit layers for their catalog trims. A layer is a starting point for a trim-specific recipe, not permission to reuse 3LT/3LZ pixels.
- **GSX is a derived Grand Sport coupe view-01 work product.** S01 is not a separate native manufacturer GSX scene. Its saved source retains `Base / 1YE07`; there is no `1YG07` foundation. It has modified badge/fascia branches and unqualified inherited options. No GSX convertible or second-view source exists in this folder.
- **ZR1X coupe source drift exists.** S21 differs from the file hash pinned by its bound proof; the shipped proof/media remains its own immutable historical artifact. Do not regenerate that binding against the current file without reviewing the differences.
- **Stripes, full aero, glass/tint, wheels and roof are not independent choices in the current renderer.** Their native positions span multiple depth intervals. A rear wing at slot 20 does not represent the rest of its aero package. Second views also need explicit view identity/selection: `load_collection()` currently rejects overlapping model/year/body/trim scopes.

## Evidence, source safety and reading the matrix

Read: `AGENTS.md`, `README.md`, `docs/visualizer-artwork.md`, `docs/form-audit-and-live-migration.md` §3, the October 7 direction in `docs/migration-plan.md`, `catalog/artwork.py`, the collection index, and all ten application manifests and source proofs. The current launch remains artwork-hidden unless explicitly bundled with `--with-artwork`. Earlier statements that no GSX-named file exists are superseded by the saved-file evidence here; they are not silently rewritten.

Catalog authority for identities, names, colors, lifecycle and configuration scope is completed release `11f2d01cdfd7c6e472b6f136ed75cbd7b5c634be30cb2647f04d098c72e09dac`, after R3. Its `catalog.sqlite` SHA-256 is `3b24fab82b23b4d3d4babebc7e19ef9b505fbac9d2f823badfa6fe227c94e1dc`. The draft `configuration`, `option`, and `option_configuration` tables were also read and match this release exactly. Tables read: `model`, `model_year`, `catalog_revision`, `configuration`, `option`, `option_configuration`, `consumer_option`, and connected condition/acquisition/content records. Layer labels provide only the location of candidate artwork. They never create a catalog option or override availability. An option identity below is always **model + 2027 + option ID**, even where IDs/RPOs repeat.

Source root **V** = `/Users/seandm/Library/Mobile Documents/com~apple~CloudDocs/C8-iCloud/27img/visualizer-studio_27/visual-studio/`. Workflow root **W** = its sibling `27vette-phase1/`. Read `ASSET-WORKFLOW.md`, `REPRODUCE-PROOFS.md`, `build-asset-states.py`, `build-export-batch.py`, `verify-native-compositions.py`; retained the same state/recipe/export workflow. Reused `build-asset-states.py` SHA-256 helper and the unchanged `dump-layers.psjs` inside a disposable audit wrapper (file picker replaced with JSON capture). No exporter or compositor ran. Binary `psd-tools` inspection of disposable copies supplied an independent saved-layer/XMP comparison, not a replacement rendering pipeline.

Native Photoshop inventories completed for **22/22** saved source copies. All inventories were read-only: no visibility flag was changed; before/after snapshots were identical (`sourceVisibilityRestored=true`), and each copy was closed without saving. Original and copy integrity results are in the source register below. Raw-reader extras (including hidden `Tow_Hooks` and several empty second-view branches) are excluded from the native inventory. All shared saved/native IDs, names, parent IDs, sibling indices and visibility flags matched (30,236 native layer records total); raw counts are not substituted for native counts. The pre-existing, unsaved GSX original was left open and untouched; this audit covers its saved bytes only.

The Adobe UXP Developer Tool GUI crashed on launch. The same inventory script was ultimately opened directly in Photoshop as `.psjs`; this changes only script invocation, not the inventory/export workflow. A temporary vendor service used during diagnosis did not establish a Photoshop connection; no developer preference or security setting was changed.

| Code | Requested status | Meaning |
| --- | --- | --- |
| B | bound | An indexed application manifest and native proof already bind the exact model/body/trim/view/component. This is component coverage, not a complete configured car. |
| U | source-available-not-exported | Source layers exist, but there is no qualified current binding for this cell. Some U entries have earlier unbound proof exports, identified below; reuse/review those before re-exporting. Unmapped aliases are explicitly not qualified identities. |
| M | source-missing | The model/body/view file or explicit trim layer is absent. No other model or upper trim substitutes. |
| R | needs-renderer-change | Source exists, but current independent selection/stack/view contract cannot represent it. Native availability and exact paths are retained in the linked inventory. |
| † | Qualification hold | Derived GSX candidate, unavailable bound 5ZU, or source drift as described; this marker is not a fifth status. |
| — | Not a catalog configuration | ZR1/ZR1X 2LZ does not exist; it is not an artwork gap. |

This matrix is factored to avoid copying thousands of layer paths into each trim row: **configuration/view row → Sxx/component inventory → model option table** is one complete cell. Sxx resolves to the exact PSB and hash in the source register. Component inventories give full parent paths, parent and child layer IDs, native ordering and mapped/unmapped catalog candidates. Model option tables give exact IDs, names/colors and body/trim scope. Read all three keys together; no row inherits another model’s identity. `01` means `.exterior.01` / `f02`; `02` means `.exterior.02` / `f04`.

## Model × body × trim × view coverage

| Model | Body | Trim | View | Paint | Trim/foundation | Rear/no spoiler | Full aero / stripes | Glass / tint | Other choices |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Stingray | coupe | 1LT | 01 | U (10) [S09/paint](#s09-paint) | M [S09/foundation](#s09-foundation) | U [S09/rear](#s09-rear) | R [S09/aero](#s09-aero) / [S09/graphics](#s09-graphics) | R [S09/glass](#s09-glass) | R [S09/other](#s09-other) |
| Stingray | coupe | 1LT | 02 | R (view); U (10 source) [S10/paint](#s10-paint) | U [S10/foundation](#s10-foundation) | R (view) [S10/rear](#s10-rear) | R [S10/aero](#s10-aero) / [S10/graphics](#s10-graphics) | R [S10/glass](#s10-glass) | R [S10/other](#s10-other) |
| Stingray | coupe | 2LT | 01 | U (10) [S09/paint](#s09-paint) | U [S09/foundation](#s09-foundation) | U [S09/rear](#s09-rear) | R [S09/aero](#s09-aero) / [S09/graphics](#s09-graphics) | R [S09/glass](#s09-glass) | R [S09/other](#s09-other) |
| Stingray | coupe | 2LT | 02 | R (view); U (10 source) [S10/paint](#s10-paint) | U [S10/foundation](#s10-foundation) | R (view) [S10/rear](#s10-rear) | R [S10/aero](#s10-aero) / [S10/graphics](#s10-graphics) | R [S10/glass](#s10-glass) | R [S10/other](#s10-other) |
| Stingray | coupe | 3LT | 01 | B (3), U (7)† [S09/paint](#s09-paint) | B† [S09/foundation](#s09-foundation) | B (5ZU), U (others)† [S09/rear](#s09-rear) | R† [S09/aero](#s09-aero) / [S09/graphics](#s09-graphics) | R† [S09/glass](#s09-glass) | R† [S09/other](#s09-other) |
| Stingray | coupe | 3LT | 02 | R (view); U (10 source) [S10/paint](#s10-paint) | U [S10/foundation](#s10-foundation) | R (view) [S10/rear](#s10-rear) | R [S10/aero](#s10-aero) / [S10/graphics](#s10-graphics) | R [S10/glass](#s10-glass) | R [S10/other](#s10-other) |
| Stingray | convertible | 1LT | 01 | U (10) [S07/paint](#s07-paint) | U [S07/foundation](#s07-foundation) | U [S07/rear](#s07-rear) | R [S07/aero](#s07-aero) / [S07/graphics](#s07-graphics) | R [S07/glass](#s07-glass) | R [S07/other](#s07-other) |
| Stingray | convertible | 1LT | 02 | R (view); U (10 source) [S08/paint](#s08-paint) | U [S08/foundation](#s08-foundation) | R (view) [S08/rear](#s08-rear) | R [S08/aero](#s08-aero) / [S08/graphics](#s08-graphics) | R [S08/glass](#s08-glass) | R [S08/other](#s08-other) |
| Stingray | convertible | 2LT | 01 | U (10) [S07/paint](#s07-paint) | U [S07/foundation](#s07-foundation) | U [S07/rear](#s07-rear) | R [S07/aero](#s07-aero) / [S07/graphics](#s07-graphics) | R [S07/glass](#s07-glass) | R [S07/other](#s07-other) |
| Stingray | convertible | 2LT | 02 | R (view); U (10 source) [S08/paint](#s08-paint) | U [S08/foundation](#s08-foundation) | R (view) [S08/rear](#s08-rear) | R [S08/aero](#s08-aero) / [S08/graphics](#s08-graphics) | R [S08/glass](#s08-glass) | R [S08/other](#s08-other) |
| Stingray | convertible | 3LT | 01 | B (3), U (7)† [S07/paint](#s07-paint) | B† [S07/foundation](#s07-foundation) | B (5ZU), U (others)† [S07/rear](#s07-rear) | R† [S07/aero](#s07-aero) / [S07/graphics](#s07-graphics) | R† [S07/glass](#s07-glass) | R† [S07/other](#s07-other) |
| Stingray | convertible | 3LT | 02 | R (view); U (10 source) [S08/paint](#s08-paint) | U [S08/foundation](#s08-foundation) | R (view) [S08/rear](#s08-rear) | R [S08/aero](#s08-aero) / [S08/graphics](#s08-graphics) | R [S08/glass](#s08-glass) | R [S08/other](#s08-other) |
| Grand Sport | coupe | 1LT | 01 | U (10) [S04/paint](#s04-paint) | U [S04/foundation](#s04-foundation) | U [S04/rear](#s04-rear) | R [S04/aero](#s04-aero) / [S04/graphics](#s04-graphics) | R [S04/glass](#s04-glass) | R [S04/other](#s04-other) |
| Grand Sport | coupe | 1LT | 02 | R (view); U (10 source) [S06/paint](#s06-paint) | U [S06/foundation](#s06-foundation) | R (view) [S06/rear](#s06-rear) | R [S06/aero](#s06-aero) / [S06/graphics](#s06-graphics) | R [S06/glass](#s06-glass) | R [S06/other](#s06-other) |
| Grand Sport | coupe | 2LT | 01 | U (10) [S04/paint](#s04-paint) | U [S04/foundation](#s04-foundation) | U [S04/rear](#s04-rear) | R [S04/aero](#s04-aero) / [S04/graphics](#s04-graphics) | R [S04/glass](#s04-glass) | R [S04/other](#s04-other) |
| Grand Sport | coupe | 2LT | 02 | R (view); U (10 source) [S06/paint](#s06-paint) | U [S06/foundation](#s06-foundation) | R (view) [S06/rear](#s06-rear) | R [S06/aero](#s06-aero) / [S06/graphics](#s06-graphics) | R [S06/glass](#s06-glass) | R [S06/other](#s06-other) |
| Grand Sport | coupe | 3LT | 01 | B (10) [S04/paint](#s04-paint) | B [S04/foundation](#s04-foundation) | B (listed), U (others) [S04/rear](#s04-rear) | R [S04/aero](#s04-aero) / [S04/graphics](#s04-graphics) | R [S04/glass](#s04-glass) | R [S04/other](#s04-other) |
| Grand Sport | coupe | 3LT | 02 | R (view); U (10 source) [S06/paint](#s06-paint) | U [S06/foundation](#s06-foundation) | R (view) [S06/rear](#s06-rear) | R [S06/aero](#s06-aero) / [S06/graphics](#s06-graphics) | R [S06/glass](#s06-glass) | R [S06/other](#s06-other) |
| Grand Sport | convertible | 1LT | 01 | U (10) [S02/paint](#s02-paint) | U [S02/foundation](#s02-foundation) | U [S02/rear](#s02-rear) | R [S02/aero](#s02-aero) / [S02/graphics](#s02-graphics) | R [S02/glass](#s02-glass) | R [S02/other](#s02-other) |
| Grand Sport | convertible | 1LT | 02 | R (view); U (10 source) [S03/paint](#s03-paint) | U [S03/foundation](#s03-foundation) | R (view) [S03/rear](#s03-rear) | R [S03/aero](#s03-aero) / [S03/graphics](#s03-graphics) | R [S03/glass](#s03-glass) | R [S03/other](#s03-other) |
| Grand Sport | convertible | 2LT | 01 | U (10) [S02/paint](#s02-paint) | U [S02/foundation](#s02-foundation) | U [S02/rear](#s02-rear) | R [S02/aero](#s02-aero) / [S02/graphics](#s02-graphics) | R [S02/glass](#s02-glass) | R [S02/other](#s02-other) |
| Grand Sport | convertible | 2LT | 02 | R (view); U (10 source) [S03/paint](#s03-paint) | U [S03/foundation](#s03-foundation) | R (view) [S03/rear](#s03-rear) | R [S03/aero](#s03-aero) / [S03/graphics](#s03-graphics) | R [S03/glass](#s03-glass) | R [S03/other](#s03-other) |
| Grand Sport | convertible | 3LT | 01 | B (10) [S02/paint](#s02-paint) | B [S02/foundation](#s02-foundation) | B (listed), U (others) [S02/rear](#s02-rear) | R [S02/aero](#s02-aero) / [S02/graphics](#s02-graphics) | R [S02/glass](#s02-glass) | R [S02/other](#s02-other) |
| Grand Sport | convertible | 3LT | 02 | R (view); U (10 source) [S03/paint](#s03-paint) | U [S03/foundation](#s03-foundation) | R (view) [S03/rear](#s03-rear) | R [S03/aero](#s03-aero) / [S03/graphics](#s03-graphics) | R [S03/glass](#s03-glass) | R [S03/other](#s03-other) |
| Grand Sport X | coupe | 1LT | 01 | U (10)† [S01/paint](#s01-paint) | U† [S01/foundation](#s01-foundation) | U† [S01/rear](#s01-rear) | R† [S01/aero](#s01-aero) / [S01/graphics](#s01-graphics) | R† [S01/glass](#s01-glass) | R† [S01/other](#s01-other) |
| Grand Sport X | coupe | 1LT | 02 | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table |
| Grand Sport X | coupe | 2LT | 01 | U (10)† [S01/paint](#s01-paint) | U† [S01/foundation](#s01-foundation) | U† [S01/rear](#s01-rear) | R† [S01/aero](#s01-aero) / [S01/graphics](#s01-graphics) | R† [S01/glass](#s01-glass) | R† [S01/other](#s01-other) |
| Grand Sport X | coupe | 2LT | 02 | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table |
| Grand Sport X | coupe | 3LT | 01 | U (10)† [S01/paint](#s01-paint) | U† [S01/foundation](#s01-foundation) | U† [S01/rear](#s01-rear) | R† [S01/aero](#s01-aero) / [S01/graphics](#s01-graphics) | R† [S01/glass](#s01-glass) | R† [S01/other](#s01-other) |
| Grand Sport X | coupe | 3LT | 02 | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table |
| Grand Sport X | convertible | 1LT | 01 | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table |
| Grand Sport X | convertible | 1LT | 02 | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table |
| Grand Sport X | convertible | 2LT | 01 | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table |
| Grand Sport X | convertible | 2LT | 02 | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table |
| Grand Sport X | convertible | 3LT | 01 | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table |
| Grand Sport X | convertible | 3LT | 02 | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table |
| Z06 | coupe | 1LZ | 01 | U (10) [S13/paint](#s13-paint) | U [S13/foundation](#s13-foundation) | U [S13/rear](#s13-rear) | R [S13/aero](#s13-aero) / [S13/graphics](#s13-graphics) | R [S13/glass](#s13-glass) | R [S13/other](#s13-other) |
| Z06 | coupe | 1LZ | 02 | R (view); U (10 source) [S14/paint](#s14-paint) | U [S14/foundation](#s14-foundation) | R (view) [S14/rear](#s14-rear) | R [S14/aero](#s14-aero) / [S14/graphics](#s14-graphics) | R [S14/glass](#s14-glass) | R [S14/other](#s14-other) |
| Z06 | coupe | 2LZ | 01 | U (10) [S13/paint](#s13-paint) | U [S13/foundation](#s13-foundation) | U [S13/rear](#s13-rear) | R [S13/aero](#s13-aero) / [S13/graphics](#s13-graphics) | R [S13/glass](#s13-glass) | R [S13/other](#s13-other) |
| Z06 | coupe | 2LZ | 02 | R (view); U (10 source) [S14/paint](#s14-paint) | U [S14/foundation](#s14-foundation) | R (view) [S14/rear](#s14-rear) | R [S14/aero](#s14-aero) / [S14/graphics](#s14-graphics) | R [S14/glass](#s14-glass) | R [S14/other](#s14-other) |
| Z06 | coupe | 3LZ | 01 | B (10) [S13/paint](#s13-paint) | B [S13/foundation](#s13-foundation) | B (listed), U (others) [S13/rear](#s13-rear) | R [S13/aero](#s13-aero) / [S13/graphics](#s13-graphics) | R [S13/glass](#s13-glass) | R [S13/other](#s13-other) |
| Z06 | coupe | 3LZ | 02 | R (view); U (10 source) [S14/paint](#s14-paint) | U [S14/foundation](#s14-foundation) | R (view) [S14/rear](#s14-rear) | R [S14/aero](#s14-aero) / [S14/graphics](#s14-graphics) | R [S14/glass](#s14-glass) | R [S14/other](#s14-other) |
| Z06 | convertible | 1LZ | 01 | U (10) [S11/paint](#s11-paint) | U [S11/foundation](#s11-foundation) | U [S11/rear](#s11-rear) | R [S11/aero](#s11-aero) / [S11/graphics](#s11-graphics) | R [S11/glass](#s11-glass) | R [S11/other](#s11-other) |
| Z06 | convertible | 1LZ | 02 | R (view); U (10 source) [S12/paint](#s12-paint) | U [S12/foundation](#s12-foundation) | R (view) [S12/rear](#s12-rear) | R [S12/aero](#s12-aero) / [S12/graphics](#s12-graphics) | R [S12/glass](#s12-glass) | R [S12/other](#s12-other) |
| Z06 | convertible | 2LZ | 01 | U (10) [S11/paint](#s11-paint) | U [S11/foundation](#s11-foundation) | U [S11/rear](#s11-rear) | R [S11/aero](#s11-aero) / [S11/graphics](#s11-graphics) | R [S11/glass](#s11-glass) | R [S11/other](#s11-other) |
| Z06 | convertible | 2LZ | 02 | R (view); U (10 source) [S12/paint](#s12-paint) | U [S12/foundation](#s12-foundation) | R (view) [S12/rear](#s12-rear) | R [S12/aero](#s12-aero) / [S12/graphics](#s12-graphics) | R [S12/glass](#s12-glass) | R [S12/other](#s12-other) |
| Z06 | convertible | 3LZ | 01 | B (10) [S11/paint](#s11-paint) | B [S11/foundation](#s11-foundation) | B (listed), U (others) [S11/rear](#s11-rear) | R [S11/aero](#s11-aero) / [S11/graphics](#s11-graphics) | R [S11/glass](#s11-glass) | R [S11/other](#s11-other) |
| Z06 | convertible | 3LZ | 02 | R (view); U (10 source) [S12/paint](#s12-paint) | U [S12/foundation](#s12-foundation) | R (view) [S12/rear](#s12-rear) | R [S12/aero](#s12-aero) / [S12/graphics](#s12-graphics) | R [S12/glass](#s12-glass) | R [S12/other](#s12-other) |
| ZR1 | coupe | 1LZ | 01 | U (10) [S17/paint](#s17-paint) | U [S17/foundation](#s17-foundation) | U [S17/rear](#s17-rear) | R [S17/aero](#s17-aero) / [S17/graphics](#s17-graphics) | R [S17/glass](#s17-glass) | R [S17/other](#s17-other) |
| ZR1 | coupe | 1LZ | 02 | R (view); U (10 source) [S18/paint](#s18-paint) | U [S18/foundation](#s18-foundation) | R (view) [S18/rear](#s18-rear) | R [S18/aero](#s18-aero) / [S18/graphics](#s18-graphics) | R [S18/glass](#s18-glass) | R [S18/other](#s18-other) |
| ZR1 | coupe | 3LZ | 01 | B (10) [S17/paint](#s17-paint) | B [S17/foundation](#s17-foundation) | B (listed), U (others) [S17/rear](#s17-rear) | R [S17/aero](#s17-aero) / [S17/graphics](#s17-graphics) | R [S17/glass](#s17-glass) | R [S17/other](#s17-other) |
| ZR1 | coupe | 3LZ | 02 | R (view); U (10 source) [S18/paint](#s18-paint) | U [S18/foundation](#s18-foundation) | R (view) [S18/rear](#s18-rear) | R [S18/aero](#s18-aero) / [S18/graphics](#s18-graphics) | R [S18/glass](#s18-glass) | R [S18/other](#s18-other) |
| ZR1 | convertible | 1LZ | 01 | U (10) [S15/paint](#s15-paint) | U [S15/foundation](#s15-foundation) | U [S15/rear](#s15-rear) | R [S15/aero](#s15-aero) / [S15/graphics](#s15-graphics) | R [S15/glass](#s15-glass) | R [S15/other](#s15-other) |
| ZR1 | convertible | 1LZ | 02 | R (view); U (10 source) [S16/paint](#s16-paint) | U [S16/foundation](#s16-foundation) | R (view) [S16/rear](#s16-rear) | R [S16/aero](#s16-aero) / [S16/graphics](#s16-graphics) | R [S16/glass](#s16-glass) | R [S16/other](#s16-other) |
| ZR1 | convertible | 3LZ | 01 | B (10) [S15/paint](#s15-paint) | B [S15/foundation](#s15-foundation) | B (listed), U (others) [S15/rear](#s15-rear) | R [S15/aero](#s15-aero) / [S15/graphics](#s15-graphics) | R [S15/glass](#s15-glass) | R [S15/other](#s15-other) |
| ZR1 | convertible | 3LZ | 02 | R (view); U (10 source) [S16/paint](#s16-paint) | U [S16/foundation](#s16-foundation) | R (view) [S16/rear](#s16-rear) | R [S16/aero](#s16-aero) / [S16/graphics](#s16-graphics) | R [S16/glass](#s16-glass) | R [S16/other](#s16-other) |
| ZR1X | coupe | 1LZ | 01 | U (10)† [S21/paint](#s21-paint) | U† [S21/foundation](#s21-foundation) | U† [S21/rear](#s21-rear) | R† [S21/aero](#s21-aero) / [S21/graphics](#s21-graphics) | R† [S21/glass](#s21-glass) | R† [S21/other](#s21-other) |
| ZR1X | coupe | 1LZ | 02 | R (view); U (10 source) [S22/paint](#s22-paint) | U [S22/foundation](#s22-foundation) | R (view) [S22/rear](#s22-rear) | R [S22/aero](#s22-aero) / [S22/graphics](#s22-graphics) | R [S22/glass](#s22-glass) | R [S22/other](#s22-other) |
| ZR1X | coupe | 3LZ | 01 | B (10)† [S21/paint](#s21-paint) | B† [S21/foundation](#s21-foundation) | B (listed), U (others)† [S21/rear](#s21-rear) | R† [S21/aero](#s21-aero) / [S21/graphics](#s21-graphics) | R† [S21/glass](#s21-glass) | R† [S21/other](#s21-other) |
| ZR1X | coupe | 3LZ | 02 | R (view); U (10 source) [S22/paint](#s22-paint) | U [S22/foundation](#s22-foundation) | R (view) [S22/rear](#s22-rear) | R [S22/aero](#s22-aero) / [S22/graphics](#s22-graphics) | R [S22/glass](#s22-glass) | R [S22/other](#s22-other) |
| ZR1X | convertible | 1LZ | 01 | U (10) [S19/paint](#s19-paint) | U [S19/foundation](#s19-foundation) | U [S19/rear](#s19-rear) | R [S19/aero](#s19-aero) / [S19/graphics](#s19-graphics) | R [S19/glass](#s19-glass) | R [S19/other](#s19-other) |
| ZR1X | convertible | 1LZ | 02 | R (view); U (10 source) [S20/paint](#s20-paint) | U [S20/foundation](#s20-foundation) | R (view) [S20/rear](#s20-rear) | R [S20/aero](#s20-aero) / [S20/graphics](#s20-graphics) | R [S20/glass](#s20-glass) | R [S20/other](#s20-other) |
| ZR1X | convertible | 3LZ | 01 | B (10) [S19/paint](#s19-paint) | B [S19/foundation](#s19-foundation) | B (listed), U (others) [S19/rear](#s19-rear) | R [S19/aero](#s19-aero) / [S19/graphics](#s19-graphics) | R [S19/glass](#s19-glass) | R [S19/other](#s19-other) |
| ZR1X | convertible | 3LZ | 02 | R (view); U (10 source) [S20/paint](#s20-paint) | U [S20/foundation](#s20-foundation) | R (view) [S20/rear](#s20-rear) | R [S20/aero](#s20-aero) / [S20/graphics](#s20-graphics) | R [S20/glass](#s20-glass) | R [S20/other](#s20-other) |
| ZR1 | coupe | 2LZ | 01 | — not offered | — not offered | — not offered | — not offered | — not offered | — not offered |
| ZR1 | coupe | 2LZ | 02 | — not offered | — not offered | — not offered | — not offered | — not offered | — not offered |
| ZR1 | convertible | 2LZ | 01 | — not offered | — not offered | — not offered | — not offered | — not offered | — not offered |
| ZR1 | convertible | 2LZ | 02 | — not offered | — not offered | — not offered | — not offered | — not offered | — not offered |
| ZR1X | coupe | 2LZ | 01 | — not offered | — not offered | — not offered | — not offered | — not offered | — not offered |
| ZR1X | coupe | 2LZ | 02 | — not offered | — not offered | — not offered | — not offered | — not offered | — not offered |
| ZR1X | convertible | 2LZ | 01 | — not offered | — not offered | — not offered | — not offered | — not offered | — not offered |
| ZR1X | convertible | 2LZ | 02 | — not offered | — not offered | — not offered | — not offered | — not offered | — not offered |

All 64 valid configuration/view rows and eight non-offered rows are explicit above. The eight requested ZR1/ZR1X × coupe/convertible × 2LZ × 01/02 combinations are **— not offered by the catalog**. On S09/1LT/01, paint and component files are present but the missing trim foundation blocks a complete 1LT scene. On every view 02 row, the view-selector requirement applies to the whole scene, including cells otherwise marked U. On every GSX S01 row, derived-source qualification applies to every component.

## Existing bindings and current blockers

| Scope (view 01 only) | PSB | Under catalog/web/artwork/ | Bound paints | Bound rear choice IDs | Current disposition |
| --- | --- | --- | --- | --- | --- |
| grand_sport/coupe/3lt | S04 | (root) | GBA, G8G, GKZ, GPH, G26, GBK, G4Z, GKA, GTR, GEC | T0F opt_t0f_001, 5ZV opt_5zv_001 | source hash matches |
| zr1x/convertible/3lz | S19 | zr1x-convertible | GBA, G8G, GKZ, GPH, G26, GBK, G4Z, GKA, GTR, GEC | TOM opt_tom_002 | source hash matches |
| zr1/convertible/3lz | S15 | zr1-convertible | GBA, G8G, GKZ, GPH, G26, GBK, G4Z, GKA, GTR, GEC | TOM opt_tom_001 | source hash matches |
| z06/convertible/3lz | S11 | z06-convertible | GBA, G8G, GKZ, GPH, G26, GBK, G4Z, GKA, GTR, GEC | T0F opt_t0f_001, T0G opt_t0g_001, 5ZV opt_5zv_001 | source hash matches |
| stingray/convertible/3lt | S07 | stingray-convertible | GBA, G8G, GKZ | 5ZU opt_5zu_001 | 5ZU factory_unavailable: whole scene contract refused |
| stingray/coupe/3lt | S09 | stingray-coupe | GBA, G8G, GKZ | 5ZU opt_5zu_001 | 5ZU factory_unavailable: whole scene contract refused |
| z06/coupe/3lz | S13 | z06-coupe | GBA, G8G, GKZ, GPH, G26, GBK, G4Z, GKA, GTR, GEC | T0F opt_t0f_001, T0G opt_t0g_001, 5ZV opt_5zv_001 | source hash matches |
| zr1/coupe/3lz | S17 | zr1-coupe | GBA, G8G, GKZ, GPH, G26, GBK, G4Z, GKA, GTR, GEC | TOM opt_tom_001 | source hash matches |
| zr1x/coupe/3lz | S21 | zr1x-coupe | GBA, G8G, GKZ, GPH, G26, GBK, G4Z, GKA, GTR, GEC | TOM opt_tom_002 | source hash drift; frozen binding still independently valid |
| grand_sport/convertible/3lt | S02 | grand-sport-convertible | GBA, G8G, GKZ, GPH, G26, GBK, G4Z, GKA, GTR, GEC | T0F opt_t0f_001, 5ZV opt_5zv_001 | source hash matches |

`catalog_contract()` requires every bound option to be active; thus R3 invalidates each entire Stingray scene, not just its 5ZU selector. `project()` requires exactly one selected spoiler choice and has no no-spoiler/default-body branch. The current package binds **no stripe, glass, wheel, caliper, trim-switch, roof-switch, front splitter, rocker or dive-plane asset**. Aero option IDs in the existing manifest qualify the rear wing only.

## GSX provenance and source drift

S01 SHA-256 `60f268dc5bbd8c73f269bea7644e8489acf3b2a3c34206d7aa06b144ef3e73c4` shares XMP `OriginalDocumentID=xmp.did:9e97e5bb-bc29-4fde-8c93-1ba5a2e66ce0` with S04. Both retain the same created event (June 23) and saved event `xmp.iid:3831e2ed-7a01-4155-8938-e67d1133f3d7` (September 20, 15:13:51 −04:00). S01 has a different DocumentID, `adobe:docid:photoshop:4d865c1d-c5d0-b949-9863-6f98d4a15180`, and a September 25, 17:24:02 −04:00 save. This establishes shared Grand Sport ancestry, not the exact person/action that duplicated the file or a direct child relationship to the final S04 save.

Saved-layer comparison with S04: 1,399 shared raw layer IDs; 13 added IDs; two absent IDs. Added branches include `gsx-Badges / eyk` #1732 and `Front_Fascia_HP1` #1745 with ten `S0220&paint` children #1735–1744; added `Front_Fascia / S0220&GEC` #1733. Existing badge #1546 moved/renamed to `gsx-Badges / eyt`; Grand Sport badge #91 and group #1544 are absent. Group labels were also changed (`Badges_nose`, `gs_LPO_Badges`, `Int`, `Int-Headliner-Effects`). Body #1605 is still `Base / 1YE07`; trim layers #1430–1432 and inherited Grand Sport spoiler branches remain. `Front_Fascia_HP1` is a candidate for catalog GSX HP1, not proof of the physical content, and inherited T0F has no GSX option to bind. No new GSX badge render, pixel-geometry equivalence, manufacturer GSX foundation or all-trim legal-build proof is established.

S21 current SHA-256 `cbc0e678ff44087fb02f3722d783c425653708bdb9ada99a207d15a50a5f2de7` differs from bound proof `3f3096a92f2373a80e45f4b88c96bf52d74572f5d6473c273dd40bc054d28b08`. Current XMP `ModifyDate` records September 25, 14:44:48 −04:00. Compared with its pinned `reference.state.json`, current S21 has 1,055 native layers versus 1,063: IDs 161/166 (Mirrors), 243 (License_Plate), 257 (Multimedia), 779 (IP), 939 (Radio), 1038 (Stripes), and 1124 (Wheels) are absent; no new or renamed IDs were found. Badge visibility changed from `Badges / S0498` #15 to `Badges / S0499` #14. These are observed structural/visibility differences, not a claim that all remaining pixels are unchanged. The old inventory/proof remains the regeneration baseline until reviewed. The other nine bound-source hashes match their original proofs.

## Composition constraints and tint readiness

Native order is recorded top-to-bottom (smaller root/sibling index draws **in front**). This is distinct from renderer `stack_order`, where larger values draw in front. Every stripe/aero child inherits its parent root position; its listed order within the parent supplies the second coordinate. The per-source inventories explicitly locate each group relative to the body-paint root and all spoiler roots. “Foreground-side” means ahead of the first spoiler; “back-side” means behind the last spoiler; it is not a claim that a transparent overlay can be pasted onto an already flattened car.

| Component | Three-plane disposition | Additional work required |
| --- | --- | --- |
| Existing qualified rear wings | Fits back(0)/one spoiler(20)/foreground(30), exactly as the ten native proofs recorded. | Reuse exact source/recipe; retain model/body/trim/paint qualification. |
| Stingray no-spoiler state | Existing source-off-spoiler decomposition fits back + foreground geometrically. | R: project() requires a spoiler; add an explicit catalog-resolved no-spoiler branch later. Qualify ZF1/default separately; do not identify it solely by hidden layers. |
| Other rear spoilers and extensions | U: occupy native spoiler interval; low-spoiler/extension may be baked into one reviewed rear plane. | Resolve S011*/S0267 aliases first. SIG plus base spoiler needs a composite recipe or multiple independently selectable rear planes. |
| Front splitter, rockers, fascia/dive-plane pieces, hood spoiler | R: usually on foreground-side, with some second-view branches between/behind spoiler roots. | Independent component planes at each native depth interval, or explicit complete-package foreground recipes. A wing proof does not qualify front surfaces. Internal S-code anatomy/finish remains unmapped. |
| Stripes, stingers, hashes and hood/roof graphics | R: Decals/Stripes branches occur above and below spoiler and interleave with roof/fascia/body. | Split one catalog option across all its native branches; preserve occlusion at each intervening fixed surface. Cannot put all graphics in slot 20 or a single top overlay. S-code colors need identification, not inference. |
| Roof | R: existing Grand Sport roof proof already requires five planes. | Reuse W/asset-proofs/2026-09-20-grand-sport-coupe-01-roof/roof-manifest.json; qualify other views/bodies separately. |
| Wheels, calipers, caps, discs | R: near/far groups have different depths; replacement must remove the fixed wheel/brake/cap. | Independent near/far assembly planes or precomposed qualified assemblies. Do not overlay on baked wheels; include tire/cap/rotor dependencies. |
| Glass/tint | R: several Windows groups are separated by roof, interior, body and spoiler depth. | Isolate each surface and its reflection/defroster/occluder dependencies; qualify tint blend/alpha against native reference after an actual tint specification is supplied. |
| Second view | R even for existing paint/wing types. | Explicit view identity/selection plus separately qualified recipes; overlapping scopes are rejected today. |

The request references a “tint plan below” but supplies no tint percentages, window exclusions or compositing specification. This audit inventories glass only and does not invent those requirements. Catalog Solar-Ray Light-Tinted Glass is standard equipment (model-specific IDs in the tables); it is not a selectable aftermarket tint percentage. `S0101_L/R/B`, `S0104`, `S0105`, `S0108`, `S0122`, `Rear_Van_Windows`, `Defroster` and transparent `Roof` candidates remain separate where present. No S-code’s anatomical meaning, tint strength, mask quality or independent blend compatibility is accepted from its name.

## Catalog identities, colors and applicability

Each table is model-owned. Scope strings are **coupe / convertible**, in that model’s catalog trim order: `1LT,2LT,3LT` or `1LZ,2LZ,3LZ`; ZR1/ZR1X use **1LZ,3LZ** only. `A`=available, `S`=standard, `–`=unavailable, `?`=no context row. Lifecycle is a separate overriding constraint: A does not make a factory-unavailable/retired option selectable. These are configuration scopes, not unrestricted legal-build promises; catalog requirements/conflicts and paint/package conditions still apply. IDs after Sxx refer to exact layer paths in that source inventory. Literal RPO matches are location candidates only; numeric S-codes remain unmapped. Empty location does not prove pixels are absent when an unidentified S-code family exists.

<details>
<summary>Stingray — catalog option identities and scope</summary>

| RPO / option ID | Catalog name / color | Scope | Lifecycle | Source layer IDs; unmapped if no supported identification |
| --- | --- | --- | --- | --- |
| 5DG `opt_5dg_001` | Tech Bronze 20-Spoke Aluminum Accessory Wheels | AAA/AAA | active | Unmapped; see component families |
| 5DO `opt_5do_001` | Bright Polished 15-Spoke Aluminum Accessory Wheels | AAA/AAA | active | Unmapped; see component families |
| 5JR `opt_5jr_001` | Visible Carbon Fiber Outside Mirror Covers | ––A/––A | active | S07: 297, 1553; S08: 447, 1573; S09: 278, 1517; S10: 378, 1508 |
| 5JS `opt_5js_001` | Torch Red Mirror Caps | AAA/AAA | active | Unmapped; see component families |
| 5V7 `opt_5v7_001` | Black Ground Effects | AAA/AAA | factory_unavailable | S07: 280; S08: 434; S09: 261; S10: 365 |
| 5VM `opt_5vm_001` | Visible Carbon Fiber Ground Effects | ––A/––A | factory_unavailable | S07: 277; S08: 431; S09: 258; S10: 362 |
| 5W8 `opt_5w8_001` | Carbon Flash Metallic Carbon Fiber Ground Effects | ––A/––A | factory_unavailable | S07: 276; S08: 430; S09: 257; S10: 361 |
| 5ZC `opt_5zc_001` | Jake Logo Wheel Center Caps | AAA/AAA | active | Unmapped; see component families |
| 5ZD `opt_5zd_001` | Carbon Flash Crossed Flags Wheel Center Caps | AAA/AAA | active | Unmapped; see component families |
| 5ZU `opt_5zu_001` | Body-Color High Wing Spoiler | AAA/AAA | factory_unavailable | S07: 1456, 1457, 1458, 1459, 1460, 1461, 1462, 1463, 1464, 1465; S08: 94, 95, 96, 97, 98, 99, 100, 101, 102, 103; S09: 1443, 1444, 1445, 1446, 1447, 1448, 1449, 1450, 1451, 1452; S10: 72, 73, 74, 75, 76, 77, 78, 79, 80, 81 |
| 5ZW `opt_5zw_001` | Visible Carbon Fiber Two-Stanchion Spoiler | AAA/AAA | factory_unavailable | S07: 1421; S08: 59; S09: 1408; S10: 37 |
| 5ZZ `opt_5zz_001` | Carbon Flash Metallic High Wing Spoiler | AAA/AAA | factory_unavailable | S07: 1455; S08: 93; S09: 1442; S10: 71 |
| B6P `opt_b6p_001` | Coupe Engine Appearance Package | AAA/––– | active | Unmapped; see component families |
| BC4 `opt_bc4_001` | Blue LS6 Engine Cover | AAA/AAA | active | Unmapped; see component families |
| BC7 `opt_bc7_001` | Black LS6 Engine Cover | SSS/AAA | active | S08: 1508 |
| BCP `opt_bcp_001` | Edge Red LS6 Engine Cover | AAA/AAA | active | Unmapped; see component families |
| BCS `opt_bcs_001` | Sterling Silver LS6 Engine Cover | AAA/AAA | active | S07: 1469 |
| BV4 `opt_bv4_001` | Personalized Specification Plaque | AAA/AAA | active | S08: 1263; S09: 1083; S10: 1203 |
| C2Z `opt_c2z_001` | Visible Carbon Fiber Roof Panel | AAA/––– | active | S09: 388, 389, 390, 391, 392, 393, 394, 395, 396, 397; S10: 537, 538, 539, 540, 541, 542, 543, 544, 545, 546 |
| CC3 `opt_cc3_001` | Transparent Roof Panel | AAA/––– | active | S09: 418; S10: 567 |
| CF7 `opt_cf7_001` | Body-Color Roof Panel | SSS/––– | active | S09: 398, 399, 400, 401, 402, 403, 404, 405, 406, 407; S10: 547, 548, 549, 550, 551, 552, 553, 554, 555, 556 |
| CF8 `opt_cf8_001` | Electrochromic Dimming Removable Roof Panel | –AA/––– | factory_unavailable | S09: 408, 409, 410, 411, 412, 413, 414, 415, 416, 417; S10: 557, 558, 559, 560, 561, 562, 563, 564, 565, 566 |
| CFX `opt_cfx_001` | Personalized Corvette Museum Plaque | AAA/AAA | active | S07: 1090; S08: 1262; S09: 1082; S10: 1202 |
| CM9 `opt_cm9_001` | Body-Color Power Convertible Hardtop | –––/SSS | active | S07: 418, 419, 420, 421, 422, 423, 424, 425, 426, 427; S08: 594, 595, 596, 597, 598, 599, 600, 601, 602, 603 |
| D3V `opt_d3v_001` | Engine Lighting | AAA/––– | active | Unmapped; see component families |
| D84 `opt_d84_001` | Carbon Flash Convertible Top | –––/AAA | active | Unmapped; see component families |
| D86 `opt_d86_001` | Body-Color Roof, Carbon Flash-painted Nacelles | –––/AAA | active | Unmapped; see component families |
| DPB `opt_dpb_001` | Carbon Flash/Blue Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DPC `opt_dpc_001` | Carbon Flash/Yellow Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DPG `opt_dpg_001` | Carbon Flash/Orange Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DPL `opt_dpl_001` | Carbon Flash/Red Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DPT `opt_dpt_001` | Carbon Flash/Silver Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DRG `opt_drg_001` | Carbon Flash Outside Mirrors | AAA/AAA | active | S07: 302, 1559; S08: 452, 1578; S09: 283, 1523; S10: 383, 1513 |
| DSY `opt_dsy_001` | Edge Orange Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DSZ `opt_dsz_001` | Edge Red Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DT0 `opt_dt0_001` | Competition Yellow Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DTC `f17637a9-4db7-4601-a507-2b237df38b0e` | Royal Blue Full Length Dual Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DTH `opt_dth_001` | Carbon Flash Metallic Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DUB `opt_dub_001` | Sterling Silver Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DUE `opt_due_001` | Royal Blue/Carbon Flash Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DUK `opt_duk_001` | Edge Red/Carbon Flash Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DUW `opt_duw_001` | Edge Blue Racing Stripes | AAA/AAA | retired | Unmapped; see component families |
| DWK `opt_dwk_001` | Heated Power-Adjustable Outside Mirrors | S––/S–– | active | S07: 306, 1563; S08: 457, 1582; S09: 287, 1527; S10: 388, 1517 |
| DYX `opt_dyx_001` | Heated Power-Folding Outside Mirrors | –SS/–SS | active | S07: 305, 1562; S08: 456, 1581; S09: 286, 1526; S10: 387, 1516 |
| DZU `opt_dzu_001` | Carbon Flash/Competition Yellow Stinger Stripe | AAA/AAA | active | S07: 57; S08: 140; S09: 38; S10: 116 |
| DZV `opt_dzv_001` | Carbon Flash/Midnight Silver Stinger Stripe | AAA/AAA | active | S07: 56; S08: 139; S09: 37; S10: 115 |
| DZX `opt_dzx_001` | Carbon Flash/Edge Red Stinger Stripe | AAA/AAA | active | S07: 55; S08: 138; S09: 36; S10: 114 |
| EDU `opt_edu_001` | Body-Color and Carbon Flash Accents | AAA/AAA | active | Unmapped; see component families |
| EFR `opt_efr_001` | Carbon Flash Painted Accents | SSS/SSS | active | Unmapped; see component families |
| EFY `opt_efy_001` | Body-Color Exterior Accents | AAA/AAA | active | Unmapped; see component families |
| EYK `opt_eyk_001` | Chrome Exterior Badge Package | AAA/AAA | active | S07: 30; S08: 111; S09: 8; S10: 88 |
| EYT `opt_eyt_001` | Carbon Flash Exterior Badge Package | SSS/SSS | active | S07: 31; S08: 110, 112; S09: 9, 10; S10: 89 |
| G26 `opt_g26_001` | Sebring Orange Tintcoat | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| G4Z `opt_g4z_001` | Roswell Green Metallic | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| G8G `opt_g8g_001` | Arctic White | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GBA `opt_gba_001` | Black | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GBK `opt_gbk_001` | Competition Yellow Tintcoat Metallic | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GEC `opt_gec_001` | Pitch Gray Metallic | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GKA `opt_gka_001` | Blade Silver Metallic | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GKZ `opt_gkz_001` | Torch Red | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GPH `opt_gph_001` | Red Mist Metallic Tintcoat | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GTR `opt_gtr_001` | Admiral Blue Metallic | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| J55 `opt_j55_001` | Z51 Performance Brakes | AAA/AAA | active | S07: 196, 266; S08: 333, 402; S09: 177, 247, 1567; S10: 288, 357 |
| J6A `opt_j6a_001` | Black Painted Calipers | SSS/SSS | active | Unmapped; see component families |
| J6B `opt_j6b_001` | Blue-Painted Calipers | AAA/AAA | active | Unmapped; see component families |
| J6E `opt_j6e_001` | Velocity Yellow-Painted Calipers | AAA/AAA | active | Unmapped; see component families |
| J6F `opt_j6f_001` | Bright Red-Painted Calipers | AAA/AAA | active | Unmapped; see component families |
| J6N `opt_j6n_001` | Edge Red-Painted Calipers | AAA/AAA | active | Unmapped; see component families |
| JL9 `opt_jl9_001` | Four-Wheel Antilock Disc Brakes | SSS/SSS | active | S07: 197, 267, 1602; S08: 332, 403; S09: 178, 248; S10: 287, 358 |
| LS6 `opt_ls6_001` | High-Output 6.7L V8 DI Engine | SSS/SSS | active | S07: 1470; S08: 1509; S09: 1456; S10: 1444 |
| NGA `opt_nga_001` | Black Exhaust Tips | SSS/SSS | active | Unmapped; see component families |
| NWI `opt_nwi_001` | Bright Chrome Exhaust Tips | AAA/AAA | active | Unmapped; see component families |
| PCU `opt_pcu_001` | Stingray Protection Package | AAA/AAA | active | Unmapped; see component families |
| PCX `opt_pcx_001` | Tech Bronze Accent Package | AAA/AAA | active | Unmapped; see component families |
| PDV `opt_pdv_001` | Stingray R Appearance Package | AAA/AAA | active | Unmapped; see component families |
| Q99 `opt_q99_001` | Bright Machined-Face 20-Spoke Forged Aluminum Wheels | AAA/AAA | active | Unmapped; see component families |
| Q9A `opt_q9a_001` | Midnight Gray 20-Spoke Forged Aluminum Wheels with Red Stripe | AAA/AAA | active | Unmapped; see component families |
| Q9I `opt_q9i_001` | Gloss Black 20-Spoke Forged Aluminum Wheels | AAA/AAA | active | Unmapped; see component families |
| Q9O `opt_q9o_001` | Satin Graphite 5-Split-Spoke Forged Aluminum Wheels with Machined Edge | AAA/AAA | active | Unmapped; see component families |
| QE6 `opt_qe6_001` | Gloss Black 10-Spoke Forged Aluminum Wheels | AAA/AAA | active | Unmapped; see component families |
| QEB `opt_qeb_001` | Pearl Nickel 5-Split-Spoke Forged Aluminum Wheels | SSS/SSS | active | Unmapped; see component families |
| R88 `opt_r88_001` | Front Illuminated Crossed Flags Emblem | AAA/AAA | factory_unavailable | S07: 34; S08: 117; S09: 14, 15; S10: 93 |
| RIK `opt_rik_001` | Torch Red Rear Corvette Script Badge | AAA/AAA | active | S07: 29; S08: 109; S09: 7; S10: 87 |
| RIN `opt_rin_001` | Arctic White Rear Corvette Script Badge | AAA/AAA | active | S08: 108; S10: 86 |
| RNX `opt_rnx_001` | Gray Premium Outdoor Car Cover with Access Panels | AAA/AAA | active | Unmapped; see component families |
| RWH `opt_rwh_001` | Black Premium Indoor Car Cover | AAA/AAA | active | Unmapped; see component families |
| RWJ `opt_rwj_001` | Gray Premium Outdoor Car Cover | AAA/AAA | active | Unmapped; see component families |
| RXH `opt_rxh_001` | Silver Stingray Logo Wheel Center Caps with Red Outline | AAA/AAA | active | Unmapped; see component families |
| RXJ `opt_rxj_001` | Black Wheel Center Caps with Gray Stingray Logo | AAA/AAA | active | Unmapped; see component families |
| RYQ `opt_ryq_001` | Visible Carbon Fiber Door Intake Trim | AAA/AAA | factory_unavailable | S07: 74; S08: 249; S09: 55; S10: 204 |
| RZ9 `opt_rz9_001` | Visible Carbon Fiber Grille Insert | AAA/AAA | active | Unmapped; see component families |
| S47 `opt_s47_001` | Chrome Lug Nuts | AAA/AAA | active | Unmapped; see component families |
| SB7 `opt_sb7_001` | Corvette Racing Themed Jake and Stingray R Graphics Package | AAA/AAA | active | Unmapped; see component families |
| SBT `opt_sbt_001` | Dual Roof Package | AAA/––– | active | S09: 377; S10: 526 |
| SC7 `opt_sc7_001` | Roof Panel Storage Pouch | AAA/––– | active | Unmapped; see component families |
| SDA `opt_sda_001` | Black Recovery Hook | AAA/AAA | active | Unmapped; see component families |
| SFE `opt_sfe_001` | Chrome Wheel Locks | AAA/AAA | active | Unmapped; see component families |
| SFZ `opt_sfz_001` | Dark Stealth Crossed Flags Front Emblem | AAA/AAA | active | S07: 32; S08: 113, 114; S09: 11; S10: 90 |
| SHQ `opt_shq_001` | Silver Fender Hash Stripes with Carbon Flash Accent | AAA/AAA | active | Unmapped; see component families |
| SHT `opt_sht_001` | Tech Bronze Jake Hood Graphic | AAA/AAA | active | Unmapped; see component families |
| SHW `opt_shw_001` | Carbon Flash Fender Hash Stripes with Edge Red Accent | AAA/AAA | active | Unmapped; see component families |
| SL1 `opt_sl1_001` | Red Premium Indoor Car Cover | AAA/AAA | active | Unmapped; see component families |
| SL8 `opt_sl8_001` | Edge Red Rear Corvette Script Badge | AAA/AAA | active | S07: 28; S08: 107; S09: 6; S10: 85 |
| SL9 `opt_sl9_001` | Engine Specification Plaque | AAA/AAA | active | Unmapped; see component families |
| SLK `opt_slk_001` | Edge Red Rear Hatch Strut Bracket | AAA/––– | active | Unmapped; see component families |
| SLN `opt_sln_001` | Visible Carbon Fiber Engine Cross Brace | AAA/––– | factory_unavailable | Unmapped; see component families |
| SNG `opt_sng_001` | Carbon Flash Fender Hash Stripes with Tech Bronze Accent | AAA/AAA | active | Unmapped; see component families |
| SPY `opt_spy_001` | Black Lug Nuts | AAA/AAA | active | Unmapped; see component families |
| SPZ `opt_spz_001` | Black Wheel Locks | AAA/AAA | active | Unmapped; see component families |
| STI `opt_sti_001` | Black Composite Rocker Extensions | AAA/AAA | active | S07: 273; S08: 263; S09: 254; S10: 218 |
| T0A `opt_t0a_001` | Z51 Spoiler | AAA/AAA | active | Unmapped; see component families |
| T4L `opt_t4l_001` | LED Headlamps | SSS/SSS | active | S07: 71; S08: 654; S09: 52; S10: 618 |
| TVS `opt_tvs_001` | Low-Profile Rear Spoiler and Front Splitter | AAA/AAA | active | Unmapped; see component families |
| UFT `opt_uft_001` | Side Blind Zone Alert | –SS/–SS | active | S07: 1556; S09: 1520 |
| UG1 `opt_ug1_001` | Three-Channel Programmable Universal Home Remote | –SS/–SS | active | S07: 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469; S08: 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 639, 640, 641, 642, 643, 644, 645; S09: 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460; S10: 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609 |
| VK3 `opt_vk3_001` | Front License Plate Bracket | AAA/AAA | active | Unmapped; see component families |
| VQK `opt_vqk_001` | Black Custom Splash Guards | AAA/AAA | active | S07: 200, 270; S08: 266, 336; S09: 181, 251; S10: 221, 291 |
| VTB `opt_vtb_001` | Black Rear Fascia/Roof Protector | AAA/AAA | active | Unmapped; see component families |
| VUP `opt_vup_001` | Engine Bay Closeout Graphics | AAA/––– | active | Unmapped; see component families |
| VWD `opt_vwd_001` | Stingray R Logo Wheel Center Caps | AAA/AAA | active | Unmapped; see component families |
| VWE `opt_vwe_001` | Front Radiator Grille Screens | AAA/AAA | active | S07: 118; S08: 1557; S09: 99; S10: 1492 |
| WKQ `opt_wkq_001` | Black Premium Indoor Car Cover with Access Panels | AAA/AAA | active | Unmapped; see component families |
| WKR `opt_wkr_001` | GT3.R Premium Indoor Car Cover | AAA/AAA | active | Unmapped; see component families |
| WUB `opt_wub_001` | Quad Center Exit Exhaust | AAA/AAA | active | S07: 1474; S08: 1520; S09: 1460; S10: 1455 |
| Z51 `opt_z51_001` | Z51 Performance Package | AAA/AAA | active | Unmapped; see component families |
| ZF1 `opt_zf1_001` | Aero Delete | AAA/AAA | active | Unmapped; see component families |
| ZYC `opt_zyc_001` | Carbon Flash Mirrors and Spoiler | AAA/AAA | active | Unmapped; see component families |
| ZZ3 `opt_zz3_001` | Convertible Engine Appearance Package | –––/AAA | active | Unmapped; see component families |
| no RPO `opt_022` | Solar-Ray Light-Tinted Glass | SSS/SSS | active | Unmapped; see component families |

</details>

<details>
<summary>Grand Sport — catalog option identities and scope</summary>

| RPO / option ID | Catalog name / color | Scope | Lifecycle | Source layer IDs; unmapped if no supported identification |
| --- | --- | --- | --- | --- |
| 17A `opt_17a_001` | Blade Silver Hash Marks | AAA/AAA | active | S02: 73; S03: 133; S04: 57; S06: 110 |
| 20A `opt_20a_001` | Admiral Blue Hash Marks | AAA/AAA | active | S02: 74; S03: 134; S04: 58; S06: 111 |
| 55A `opt_55a_001` | Competition Yellow Hash Marks. | AAA/AAA | active | S02: 75; S03: 135; S04: 59; S06: 112 |
| 5JR `opt_5jr_001` | Visible Carbon Fiber Outside Mirror Covers | ––A/––A | active | S02: 338, 1652; S03: 424, 1696; S04: 321, 1622; S06: 365, 1655 |
| 5JS `opt_5js_001` | Torch Red Mirror Caps | AAA/AAA | active | Unmapped; see component families |
| 5ZB `opt_5zb_001` | Grand Sport Logo Wheel Center Caps | AAA/AAA | active | Unmapped; see component families |
| 5ZC `opt_5zc_001` | Jake Logo Wheel Center Caps | AAA/AAA | active | Unmapped; see component families |
| 5ZD `opt_5zd_001` | Carbon Flash Crossed Flags Wheel Center Caps | AAA/AAA | active | Unmapped; see component families |
| 5ZV `opt_5zv_001` | Carbon Flash Metallic Three-Stanchion High Wing Spoiler | AAA/AAA | active | S02: 1554; S03: 89; S04: 1541; S06: 66 |
| 75A `opt_75a_001` | Torch Red Hash Marks | AAA/AAA | active | S02: 76; S03: 136; S04: 60; S06: 113 |
| 97A `opt_97a_001` | Carbon Flash Hash Marks | AAA/AAA | active | S02: 77; S03: 137; S04: 61; S06: 114 |
| B6P `opt_b6p_001` | Coupe Engine Appearance Package | AAA/––– | active | Unmapped; see component families |
| BC4 `opt_bc4_002` | Blue LS6 Engine Cover | AAA/AAA | active | S06: 1584 |
| BC7 `opt_bc7_001` | Black LS6 Engine Cover | SSS/AAA | active | S02: 1557 |
| BCP `opt_bcp_002` | Edge Red LS6 Engine Cover | AAA/AAA | active | Unmapped; see component families |
| BCS `opt_bcs_002` | Sterling Silver LS6 Engine Cover | AAA/AAA | active | Unmapped; see component families |
| BV4 `opt_bv4_001` | Personalized Specification Plaque | AAA/AAA | active | S02: 1207; S03: 1375; S04: 1195; S06: 1334 |
| C2Z `opt_c2z_001` | Visible Carbon Fiber Roof Panel | AAA/––– | active | S04: 455, 456, 457, 458, 459, 460, 461, 462, 463, 464; S06: 607, 608, 609, 610, 611, 612, 613, 614, 615, 616 |
| CC3 `opt_cc3_001` | Transparent Roof Panel | AAA/––– | active | S04: 485; S06: 637 |
| CF7 `opt_cf7_001` | Body-Color Roof Panel | SSS/––– | active | S04: 465, 466, 467, 468, 469, 470, 471, 472, 473, 474; S06: 617, 618, 619, 620, 621, 622, 623, 624, 625, 626 |
| CF8 `opt_cf8_001` | Electrochromic Dimming Roof Panel | –AA/––– | factory_unavailable | S04: 475, 476, 477, 478, 479, 480, 481, 482, 483, 484; S06: 627, 628, 629, 630, 631, 632, 633, 634, 635, 636 |
| CFL `opt_cfl_001` | Extended Front Splitter, Carbon Flash | AAA/AAA | active | Unmapped; see component families |
| CFV `opt_cfv_001` | Visible Carbon Fiber Ground Effects | AAA/AAA | active | Unmapped; see component families |
| CFX `opt_cfx_001` | Personalized Corvette Museum Plaque | AAA/AAA | active | S02: 1206; S03: 1374; S06: 1333 |
| CFZ `opt_cfz_001` | Carbon Flash Carbon Fiber Ground Effects | AAA/AAA | active | Unmapped; see component families |
| CM9 `opt_cm9_001` | Body-Color Power Convertible Hardtop | –––/SSS | active | S02: 480, 481, 482, 483, 484, 485, 486, 487, 488, 489; S03: 657, 658, 659, 660, 661, 662, 663, 664, 665, 666 |
| D3V `opt_d3v_001` | Engine Lighting | AAA/––– | active | Unmapped; see component families |
| D84 `opt_d84_001` | Carbon Flash Convertible Top | –––/AAA | active | Unmapped; see component families |
| D86 `opt_d86_001` | Body-Color Roof, Carbon Flash-painted Nacelles | –––/AAA | active | Unmapped; see component families |
| DMU `opt_dmu_001` | Carbon Flash Center Stripe | AAA/AAA | active | Unmapped; see component families |
| DMV `opt_dmv_001` | Blade Silver Center Stripe | AAA/AAA | active | Unmapped; see component families |
| DMW `opt_dmw_001` | Arctic White Center Stripe | AAA/AAA | active | Unmapped; see component families |
| DMX `opt_dmx_001` | Admiral Blue Center Stripe | AAA/AAA | active | Unmapped; see component families |
| DMY `opt_dmy_001` | Red Mist Center Stripe | AAA/AAA | active | Unmapped; see component families |
| DPB `opt_dpb_001` | Carbon Flash/Blue Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DPC `opt_dpc_001` | Carbon Flash/Yellow Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DPG `opt_dpg_001` | Carbon Flash/Orange Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DPL `opt_dpl_001` | Carbon Flash/Red Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DPT `opt_dpt_001` | Carbon Flash/Silver Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DRG `opt_drg_001` | Carbon Flash Outside Mirrors | AAA/AAA | active | S02: 344, 1658; S03: 430, 1702; S04: 327, 1628; S06: 370, 1660 |
| DSY `opt_dsy_001` | Edge Orange Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DSZ `opt_dsz_001` | Edge Red Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DT0 `opt_dt0_001` | Competition Yellow Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DTC `502b1c0d-3deb-4aa8-b1d5-6481ec049793` | Royal Blue Full Length Dual Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DTH `opt_dth_001` | Carbon Flash Metallic Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DUB `opt_dub_001` | Sterling Silver Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DUE `opt_due_001` | Royal Blue/Carbon Flash Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DUK `opt_duk_001` | Edge Red/Carbon Flash Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DUW `opt_duw_001` | Edge Blue Racing Stripes | AAA/AAA | retired | Unmapped; see component families |
| DWK `opt_dwk_001` | Heated Power-Adjustable Outside Mirrors | S––/S–– | active | S02: 348, 1662; S03: 435, 1706; S04: 331, 1632; S06: 375, 1664 |
| DX4 `opt_dx4_001` | Red Mist Hash Marks | AAA/AAA | active | S02: 78; S03: 138; S04: 62; S06: 115 |
| DYX `opt_dyx_001` | Heated Power-Folding Outside Mirrors | –SS/–SS | active | S02: 347, 1661; S03: 434, 1705; S04: 330, 1631; S06: 374, 1663 |
| DZU `opt_dzu_001` | Carbon Flash/Competition Yellow Stinger Stripe | AAA/AAA | active | S02: 70; S03: 130; S04: 54; S06: 107 |
| DZV `opt_dzv_001` | Carbon Flash/Midnight Silver Stinger Stripe | AAA/AAA | active | S02: 69; S03: 129; S04: 53; S06: 106 |
| DZX `opt_dzx_001` | Carbon Flash/Edge Red Stinger Stripe | AAA/AAA | active | S02: 68; S03: 128; S04: 52; S06: 105 |
| EDU `opt_edu_001` | Body-Color and Carbon Flash Accents | AAA/AAA | active | Unmapped; see component families |
| EFR `opt_efr_001` | Carbon Flash Painted Accents | SSS/SSS | active | Unmapped; see component families |
| EYK `opt_eyk_001` | Chrome Exterior Badge Package | AAA/AAA | active | S02: 31; S03: 95, 97; S04: 14; S06: 73 |
| EYT `opt_eyt_001` | Carbon Flash Exterior Badge Package | SSS/SSS | active | S02: 32; S03: 96, 98; S04: 15; S06: 72, 74 |
| FEB `opt_feb_001` | Z52 Sport Performance Package | AAA/AAA | active | Unmapped; see component families |
| FEY `opt_fey_001` | Z52 Track Performance Package | AAA/AAA | active | Unmapped; see component families |
| G26 `opt_g26_001` | Sebring Orange Tintcoat | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| G4Z `opt_g4z_001` | Roswell Green Metallic | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| G8G `opt_g8g_001` | Arctic White | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GBA `opt_gba_001` | Black | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GBK `opt_gbk_001` | Competition Yellow Tintcoat Metallic | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GEC `opt_gec_001` | Pitch Gray Metallic | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GKA `opt_gka_001` | Blade Silver Metallic | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GKZ `opt_gkz_001` | Torch Red | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GPH `opt_gph_001` | Red Mist Metallic Tintcoat | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GTR `opt_gtr_001` | Admiral Blue Metallic | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| J56 `opt_j56_001` | Performance Disc Brakes | AAA/AAA | active | S02: 243, 314; S03: 316, 385; S04: 227, 298; S06: 281, 350, 1732 |
| J57 `opt_j57_001` | Carbon Ceramic Brakes | AAA/AAA | active | S02: 242, 313; S03: 315, 387, 1763; S04: 226, 297; S06: 280, 352, 1704, 1731 |
| J6A `opt_j6a_001` | Black Painted Calipers | SSS/SSS | active | Unmapped; see component families |
| J6B `opt_j6b_001` | Blue-Painted Calipers | AAA/AAA | active | Unmapped; see component families |
| J6D `opt_j6d_001` | Dark Gray Metallic-Painted Calipers | AAA/AAA | active | Unmapped; see component families |
| J6E `opt_j6e_001` | Velocity Yellow-Painted Calipers | AAA/AAA | active | Unmapped; see component families |
| J6F `opt_j6f_001` | Bright Red-Painted Calipers | AAA/AAA | active | Unmapped; see component families |
| J6L `opt_j6l_001` | Orange-Painted Calipers | AAA/AAA | active | Unmapped; see component families |
| J6N `opt_j6n_001` | Edge Red-Painted Calipers | AAA/AAA | active | Unmapped; see component families |
| JX6 `opt_jx6_001` | Low-Dust Touring Brakes | SSS/SSS | active | S02: 244, 315; S03: 317, 386, 1736; S04: 228, 299; S06: 282, 351 |
| LS6 `opt_ls6_001` | 6.7L V8 Engine | SSS/SSS | active | S02: 1563; S03: 1632; S04: 1550; S06: 1591 |
| NGA `opt_nga_001` | Black Exhaust Tips | SSS/SSS | active | Unmapped; see component families |
| NWI `opt_nwi_001` | Bright Chrome Exhaust Tips | AAA/AAA | active | Unmapped; see component families |
| PCQ `opt_pcq_001` | Grille Screen Protection Package | AAA/AAA | active | Unmapped; see component families |
| PDA `opt_pda_001` | Jake C8.R Graphics Package | AAA/AAA | active | Unmapped; see component families |
| R88 `opt_r88_001` | Front Illuminated Crossed Flags Emblem | AAA/AAA | factory_unavailable | S02: 35; S03: 102; S04: 19; S06: 78 |
| RIK `opt_rik_001` | Torch Red Rear Corvette Script Badge | AAA/AAA | active | S03: 94; S06: 71 |
| RIN `opt_rin_001` | Arctic White Rear Corvette Script Badge | AAA/AAA | active | S03: 93; S04: 13; S06: 70 |
| ROU `opt_rou_001` | Pearl Nickel Forged Aluminum Wheels | AAA/AAA | active | Unmapped; see component families |
| ROX `opt_rox_001` | Carbon Flash with Machined Edge Forged Aluminum Wheels | AAA/AAA | active | Unmapped; see component families |
| ROY `opt_roy_001` | Carbon Flash-Painted Carbon Fiber Wheels | AAA/AAA | active | Unmapped; see component families |
| ROZ `opt_roz_001` | Visible Carbon Fiber Wheels | AAA/AAA | active | Unmapped; see component families |
| RWH `opt_rwh_001` | Black Premium Indoor Car Cover | AAA/AAA | active | Unmapped; see component families |
| RWJ `opt_rwj_001` | Gray Premium Outdoor Car Cover | AAA/AAA | active | Unmapped; see component families |
| RZ9 `opt_rz9_001` | Visible Carbon Fiber Grille Insert | AAA/AAA | factory_unavailable | Unmapped; see component families |
| S47 `opt_s47_001` | Chrome Lug Nuts | AAA/AAA | active | Unmapped; see component families |
| SBT `opt_sbt_001` | Dual Roof Package | AAA/––– | active | S04: 444; S06: 596 |
| SC7 `opt_sc7_001` | Roof Panel Storage Pouch | AAA/––– | active | Unmapped; see component families |
| SDA `opt_sda_001` | Black Recovery Hook | AAA/AAA | active | Unmapped; see component families |
| SFE `opt_sfe_001` | Chrome Wheel Locks | AAA/AAA | active | Unmapped; see component families |
| SFZ `opt_sfz_001` | Dark Stealth Crossed Flags Emblems | AAA/AAA | active | S02: 33; S03: 99; S04: 17; S06: 75 |
| SHT `opt_sht_001` | Tech Bronze Jake Hood Graphic | AAA/AAA | active | Unmapped; see component families |
| SIG `opt_sig_001` | Clear Smoked Spoiler Extension | AAA/AAA | active | S02: 1542; S03: 38; S04: 1529; S06: 15 |
| SL8 `opt_sl8_001` | Edge Red Rear Corvette Script Badge | AAA/AAA | active | S03: 92; S06: 69 |
| SL9 `opt_sl9_001` | Engine Specification Plaque | AAA/AAA | active | Unmapped; see component families |
| SLK `opt_slk_001` | Edge Red Rear Hatch Strut Bracket | AAA/––– | active | Unmapped; see component families |
| SLN `opt_sln_001` | Visible Carbon Fiber Engine Cross Brace | AAA/––– | factory_unavailable | Unmapped; see component families |
| SNE `opt_sne_001` | Jake Hood Graphic | AAA/AAA | active | Unmapped; see component families |
| SOM `opt_som_001` | Bright Polished Forged Aluminum Wheels | AAA/AAA | active | Unmapped; see component families |
| SON `opt_son_001` | Gloss Black Forged Aluminum Wheels | AAA/AAA | active | Unmapped; see component families |
| SPY `opt_spy_001` | Black Lug Nuts | AAA/AAA | active | Unmapped; see component families |
| SPZ `opt_spz_001` | Black Wheel Locks | AAA/AAA | active | Unmapped; see component families |
| STZ `opt_stz_001` | Visible Carbon Fiber Red Stripe Wheels | AAA/AAA | active | Unmapped; see component families |
| SUP `opt_sup_001` | Red Grand Sport Badges | AAA/AAA | active | Unmapped; see component families |
| SWM `opt_swm_001` | Pearl Nickel 10-Spoke Forged Aluminum Wheels | SSS/SSS | active | Unmapped; see component families |
| SWN `opt_swn_001` | Gloss Black 10-Spoke Forged Aluminum Wheels | AAA/AAA | active | Unmapped; see component families |
| SWO `opt_swo_001` | High-Polished 10-Spoke Forged Aluminum Wheels | AAA/AAA | active | Unmapped; see component families |
| SWP `opt_swp_001` | Carbon Flash Bright Polished-Face 10-Spoke Forged Aluminum Wheels | AAA/AAA | active | Unmapped; see component families |
| T0E `opt_t0e_001` | Low Rear Spoiler | SSS/SSS | active | Unmapped; see component families |
| T0E `opt_t0e_002` | Low Rear Spoiler | SSS/SSS | retired | Unmapped; see component families |
| T0F `opt_t0f_001` | Carbon Flash-Painted Carbon Fiber Aero Package | AAA/AAA | active | S02: 1530; S03: 66; S04: 1517; S06: 43 |
| T4L `opt_t4l_001` | LED Headlamps | SSS/SSS | active | S02: 84; S03: 718; S04: 68; S06: 689 |
| UFT `opt_uft_001` | Side Blind Zone Alert | –SS/–SS | active | S02: 341, 1655; S03: 427, 1699; S04: 1625 |
| UG1 `opt_ug1_001` | Three-Channel Programmable Universal Home Remote | –SS/–SS | active | S02: 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532; S03: 668, 669, 670, 671, 672, 673, 674, 675, 676, 677, 678, 679, 680, 681, 682, 683, 684, 685, 686, 687, 688, 689, 690, 691, 692, 693, 694, 695, 696, 697, 698, 699, 700, 701, 702, 703, 704, 705, 706, 707, 708, 709; S04: 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528; S06: 639, 640, 641, 642, 643, 644, 645, 646, 647, 648, 649, 650, 651, 652, 653, 654, 655, 656, 657, 658, 659, 660, 661, 662, 663, 664, 665, 666, 667, 668, 669, 670, 671, 672, 673, 674, 675, 676, 677, 678, 679, 680 |
| VPO `opt_vpo_001` | Tech Bronze Jake C8.R Rear Hash Graphic | AAA/AAA | active | S02: 72; S03: 132; S04: 56; S06: 109 |
| VPW `opt_vpw_001` | Jake C8.R Rear Hash Graphic | AAA/AAA | active | Unmapped; see component families |
| VTB `opt_vtb_001` | Black Rear Fascia/Roof Protector | AAA/AAA | active | Unmapped; see component families |
| VUP `opt_vup_001` | Engine Bay Closeout Graphics | AAA/––– | active | Unmapped; see component families |
| VWE `opt_vwe_001` | Front Radiator Grille Screens | AAA/AAA | active | S02: 161; S03: 1680; S04: 145; S06: 1639 |
| VWT `opt_vwt_001` | Insect Protection Grille Screen | AAA/AAA | active | Unmapped; see component families |
| WKR `opt_wkr_001` | GT3.R Premium Indoor Car Cover | AAA/AAA | active | Unmapped; see component families |
| WUB `opt_wub_001` | Quad Center Exit Exhaust | AAA/AAA | active | S02: 1567; S03: 1643; S04: 1554; S06: 1602 |
| Z15 `opt_z15_001` | Grand Sport Heritage Graphics | AAA/AAA | active | Unmapped; see component families |
| Z25 `opt_z25_001` | Grand Sport Launch Edition | ––A/––A | active | Unmapped; see component families |
| ZYC `opt_zyc_001` | Carbon Flash Mirrors and Spoiler | AAA/AAA | active | Unmapped; see component families |
| ZZ3 `opt_zz3_001` | Convertible Engine Appearance Package | –––/AAA | active | Unmapped; see component families |
| no RPO `opt_018` | Solar-Ray Light-Tinted Glass | SSS/SSS | active | Unmapped; see component families |

</details>

<details>
<summary>Grand Sport X — catalog option identities and scope</summary>

| RPO / option ID | Catalog name / color | Scope | Lifecycle | Source layer IDs; unmapped if no supported identification |
| --- | --- | --- | --- | --- |
| 17A `opt_17a_001` | Blade Silver Hash Marks | AAA/AAA | active | S01: 57 |
| 20A `opt_20a_001` | Admiral Blue Hash Marks | AAA/AAA | active | S01: 58 |
| 55A `opt_55a_001` | Competition Yellow Hash Marks. | AAA/AAA | active | S01: 59 |
| 5JR `opt_5jr_001` | Visible Carbon Fiber Outside Mirror Covers | ––A/––A | active | S01: 321, 1622 |
| 5JS `opt_5js_001` | Torch Red Mirror Caps | AAA/AAA | active | Unmapped; see component families |
| 5ZB `opt_5zb_001` | Grand Sport Logo Wheel Center Caps | AAA/AAA | retired | Unmapped; see component families |
| 5ZC `opt_5zc_001` | Jake Logo Wheel Center Caps | AAA/AAA | active | Unmapped; see component families |
| 5ZD `opt_5zd_001` | Carbon Flash Crossed Flags Wheel Center Caps | AAA/AAA | active | Unmapped; see component families |
| 5ZV `opt_5zv_001` | Carbon Flash Metallic Three-Stanchion High Wing Spoiler | AAA/AAA | active | S01: 1541 |
| 75A `opt_75a_001` | Torch Red Hash Marks | AAA/AAA | active | S01: 60 |
| 97A `opt_97a_001` | Carbon Flash Hash Marks | AAA/AAA | active | S01: 61 |
| B6P `opt_b6p_001` | Coupe Engine Appearance Package | AAA/––– | active | Unmapped; see component families |
| BC4 `opt_bc4_001` | Blue LS6 Engine Cover | AAA/AAA | active | Unmapped; see component families |
| BC7 `opt_bc7_001` | Black LS6 Engine Cover | SSS/AAA | active | Unmapped; see component families |
| BCP `opt_bcp_001` | Edge Red LS6 Engine Cover | AAA/AAA | active | Unmapped; see component families |
| BCS `opt_bcs_001` | Sterling Silver LS6 Engine Cover | AAA/AAA | active | Unmapped; see component families |
| BV4 `opt_bv4_001` | Personalized Specification Plaque | AAA/AAA | active | S01: 1195 |
| C2Z `opt_c2z_001` | Visible Carbon Fiber Roof Panel | AAA/––– | active | S01: 455, 456, 457, 458, 459, 460, 461, 462, 463, 464 |
| CC3 `opt_cc3_001` | Transparent Roof Panel | AAA/––– | active | S01: 485 |
| CF7 `opt_cf7_001` | Body-Color Roof Panel | SSS/––– | active | S01: 465, 466, 467, 468, 469, 470, 471, 472, 473, 474 |
| CF8 `opt_cf8_001` | Electrochromic Dimming Roof Panel | –AA/––– | factory_unavailable | S01: 475, 476, 477, 478, 479, 480, 481, 482, 483, 484 |
| CFL `opt_cfl_001` | Extended Front Splitter, Carbon Flash | AAA/AAA | active | Unmapped; see component families |
| CFV `opt_cfv_001` | Visible Carbon Fiber Ground Effects | AAA/AAA | active | Unmapped; see component families |
| CFZ `opt_cfz_001` | Carbon Flash Carbon Fiber Ground Effects | AAA/AAA | active | Unmapped; see component families |
| CM9 `opt_cm9_001` | Body-Color Power Convertible Hardtop | –––/SSS | active | Unmapped; see component families |
| D3V `opt_d3v_001` | Engine Lighting | AAA/––– | active | Unmapped; see component families |
| D84 `opt_d84_001` | Carbon Flash Convertible Top | –––/AAA | active | Unmapped; see component families |
| D86 `opt_d86_001` | Body-Color Roof, Carbon Flash-painted Nacelles | –––/AAA | active | Unmapped; see component families |
| DMU `opt_dmu_001` | Carbon Flash Center Stripe | AAA/AAA | active | Unmapped; see component families |
| DMV `opt_dmv_001` | Blade Silver Center Stripe | AAA/AAA | active | Unmapped; see component families |
| DMW `opt_dmw_001` | Arctic White Center Stripe | AAA/AAA | active | Unmapped; see component families |
| DMX `opt_dmx_001` | Admiral Blue Center Stripe | AAA/AAA | active | Unmapped; see component families |
| DMY `opt_dmy_001` | Red Mist Center Stripe | AAA/AAA | active | Unmapped; see component families |
| DPB `opt_dpb_001` | Carbon Flash/Blue Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DPC `opt_dpc_001` | Carbon Flash/Yellow Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DPG `opt_dpg_001` | Carbon Flash/Orange Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DPL `opt_dpl_001` | Carbon Flash/Red Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DPT `opt_dpt_001` | Carbon Flash/Silver Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DRG `opt_drg_001` | Carbon Flash Outside Mirrors | AAA/AAA | active | S01: 327, 1628 |
| DSY `opt_dsy_001` | Edge Orange Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DSZ `opt_dsz_001` | Edge Red Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DT0 `opt_dt0_001` | Competition Yellow Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DTC `opt_dtc_001` | Royal Blue Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DTH `opt_dth_001` | Carbon Flash Metallic Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DUB `opt_dub_001` | Sterling Silver Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DUE `opt_due_001` | Royal Blue/Carbon Flash Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DUK `opt_duk_001` | Edge Red/Carbon Flash Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DWK `opt_dwk_001` | Heated Power-Adjustable Outside Mirrors | S––/S–– | active | S01: 331, 1632 |
| DX4 `opt_dx4_001` | Red Mist Hash Marks | AAA/AAA | active | S01: 62 |
| DYX `opt_dyx_001` | Heated Power-Folding Outside Mirrors | –SS/–SS | active | S01: 330, 1631 |
| DZU `opt_dzu_001` | Carbon Flash/Competition Yellow Stinger Stripe | AAA/AAA | active | S01: 54 |
| DZV `opt_dzv_001` | Carbon Flash/Midnight Silver Stinger Stripe | AAA/AAA | active | S01: 53 |
| DZX `opt_dzx_001` | Carbon Flash/Edge Red Stinger Stripe | AAA/AAA | active | S01: 52 |
| EDU `opt_edu_001` | Body-Color and Carbon Flash Accents | AAA/AAA | active | Unmapped; see component families |
| EFR `opt_efr_001` | Carbon Flash Painted Accents | SSS/SSS | active | Unmapped; see component families |
| EYK `opt_eyk_001` | Chrome Exterior Badge Package | AAA/AAA | active | S01: 14, 1732 |
| EYT `opt_eyt_001` | Carbon Flash Exterior Badge Package | SSS/SSS | active | S01: 15, 1546 |
| FED `opt_fed_001` | Sport Performance Package | AAA/AAA | active | Unmapped; see component families |
| G26 `opt_g26_001` | Sebring Orange Tintcoat | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| G4Z `opt_g4z_001` | Roswell Green Metallic | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| G8G `opt_g8g_001` | Arctic White | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GBA `opt_gba_001` | Black | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GBK `opt_gbk_001` | Competition Yellow Tintcoat Metallic | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GEC `opt_gec_001` | Pitch Gray Metallic | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GKA `opt_gka_001` | Blade Silver Metallic | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GKZ `opt_gkz_001` | Torch Red | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GPH `opt_gph_001` | Red Mist Metallic Tintcoat | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GTR `opt_gtr_001` | Admiral Blue Metallic | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| HP1 `opt_hp1_001` | Electrified Front Axle | SSS/SSS | active | Unmapped; see component families |
| J57 `opt_j57_001` | Carbon Ceramic Brakes | SSS/SSS | active | S01: 226, 297 |
| J6B `opt_j6b_001` | Blue-Painted Calipers | AAA/AAA | active | Unmapped; see component families |
| J6D `opt_j6d_001` | Dark Gray Metallic-Painted Calipers | SSS/SSS | active | Unmapped; see component families |
| J6E `opt_j6e_001` | Velocity Yellow-Painted Calipers | AAA/AAA | active | Unmapped; see component families |
| J6F `opt_j6f_001` | Bright Red-Painted Calipers | AAA/AAA | active | Unmapped; see component families |
| J6L `opt_j6l_001` | Orange-Painted Calipers | AAA/AAA | active | Unmapped; see component families |
| J6N `opt_j6n_001` | Edge Red-Painted Calipers | AAA/AAA | active | Unmapped; see component families |
| LS6 `opt_ls6_001` | 6.7L V8 Engine | SSS/SSS | active | S01: 1550 |
| NGA `opt_nga_001` | Black Exhaust Tips | SSS/SSS | active | Unmapped; see component families |
| NWI `opt_nwi_001` | Bright Chrome Exhaust Tips | AAA/AAA | active | Unmapped; see component families |
| PCQ `opt_pcq_001` | Grille Screen Protection Package | AAA/AAA | active | Unmapped; see component families |
| PDA `opt_pda_001` | Jake C8.R Graphics Package | AAA/AAA | active | Unmapped; see component families |
| R88 `opt_r88_001` | Front Illuminated Crossed Flags Emblem | AAA/AAA | factory_unavailable | S01: 19 |
| RIK `opt_rik_001` | Torch Red Rear Corvette Script Badge | AAA/AAA | active | Unmapped; see component families |
| RIN `opt_rin_001` | Arctic White Rear Corvette Script Badge | AAA/AAA | active | S01: 13 |
| ROU `opt_rou_001` | Pearl Nickel Forged Aluminum Wheels | AAA/AAA | active | Unmapped; see component families |
| ROX `opt_rox_001` | Carbon Flash with Machined Edge Forged Aluminum Wheels | AAA/AAA | active | Unmapped; see component families |
| ROY `opt_roy_001` | Carbon Flash-Painted Carbon Fiber Wheels | AAA/AAA | active | Unmapped; see component families |
| ROZ `opt_roz_001` | Visible Carbon Fiber Wheels | AAA/AAA | active | Unmapped; see component families |
| RWH `opt_rwh_001` | Black Premium Indoor Car Cover | AAA/AAA | active | Unmapped; see component families |
| RWJ `opt_rwj_001` | Gray Premium Outdoor Car Cover | AAA/AAA | active | Unmapped; see component families |
| RZ9 `opt_rz9_001` | Visible Carbon Fiber Grille Insert | AAA/AAA | factory_unavailable | Unmapped; see component families |
| S47 `opt_s47_001` | Chrome Lug Nuts | AAA/AAA | active | Unmapped; see component families |
| SBT `opt_sbt_001` | Dual Roof Package | AAA/––– | active | S01: 444 |
| SC7 `opt_sc7_001` | Roof Panel Storage Pouch | AAA/––– | active | Unmapped; see component families |
| SDA `opt_sda_001` | Black Recovery Hook | AAA/AAA | active | Unmapped; see component families |
| SFE `opt_sfe_001` | Chrome Wheel Locks | AAA/AAA | active | Unmapped; see component families |
| SFZ `opt_sfz_001` | Dark Stealth Crossed Flags Emblems | AAA/AAA | active | S01: 17 |
| SHT `opt_sht_001` | Tech Bronze Jake Hood Graphic | AAA/AAA | active | Unmapped; see component families |
| SIG `opt_sig_001` | Clear Smoked Spoiler Extension | AAA/AAA | active | S01: 1529 |
| SL8 `opt_sl8_001` | Edge Red Rear Corvette Script Badge | AAA/AAA | active | Unmapped; see component families |
| SL9 `opt_sl9_001` | Engine Specification Plaque | AAA/AAA | active | Unmapped; see component families |
| SLK `opt_slk_001` | Edge Red Rear Hatch Strut Bracket | AAA/––– | active | Unmapped; see component families |
| SLN `opt_sln_001` | Visible Carbon Fiber Engine Cross Brace | AAA/––– | factory_unavailable | Unmapped; see component families |
| SNE `opt_sne_001` | Jake Hood Graphic | AAA/AAA | active | Unmapped; see component families |
| SOM `opt_som_001` | Bright Polished Forged Aluminum Wheels | AAA/AAA | active | Unmapped; see component families |
| SON `opt_son_001` | Gloss Black Forged Aluminum Wheels | AAA/AAA | active | Unmapped; see component families |
| SPY `opt_spy_001` | Black Lug Nuts | AAA/AAA | active | Unmapped; see component families |
| SPZ `opt_spz_001` | Black Wheel Locks | AAA/AAA | active | Unmapped; see component families |
| STZ `opt_stz_001` | Visible Carbon Fiber Red Stripe Wheels | AAA/AAA | active | Unmapped; see component families |
| SWM `opt_swm_001` | Pearl Nickel 10-Spoke Forged Aluminum Wheels | SSS/SSS | active | Unmapped; see component families |
| SWN `opt_swn_001` | Gloss Black 10-Spoke Forged Aluminum Wheels | AAA/AAA | active | Unmapped; see component families |
| SWO `opt_swo_001` | High-Polished 10-Spoke Forged Aluminum Wheels | AAA/AAA | active | Unmapped; see component families |
| SWP `opt_swp_001` | Carbon Flash Bright Polished-Face 10-Spoke Forged Aluminum Wheels | AAA/AAA | active | Unmapped; see component families |
| T0E `opt_t0e_001` | Low Rear Spoiler | SSS/SSS | active | Unmapped; see component families |
| T4L `opt_t4l_001` | LED Headlamps | SSS/SSS | active | S01: 68 |
| UFT `opt_uft_001` | Side Blind Zone Alert | –SS/–SS | active | S01: 1625 |
| UG1 `opt_ug1_001` | Three-Channel Programmable Universal Home Remote | –SS/–SS | active | S01: 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528 |
| VK3 `opt_vk3_001` | Front License Plate Bracket | AAA/AAA | active | Unmapped; see component families |
| VPO `opt_vpo_001` | Tech Bronze Jake C8.R Rear Hash Graphic | AAA/AAA | active | S01: 56 |
| VPW `opt_vpw_001` | Jake C8.R Rear Hash Graphic | AAA/AAA | active | Unmapped; see component families |
| VTB `opt_vtb_001` | Black Rear Fascia/Roof Protector | AAA/AAA | active | Unmapped; see component families |
| VUP `opt_vup_001` | Engine Bay Closeout Graphics | AAA/––– | active | Unmapped; see component families |
| VWE `opt_vwe_001` | Front Radiator Grille Screens | AAA/AAA | active | S01: 145 |
| VWT `opt_vwt_001` | Insect Protection Grille Screen | AAA/AAA | active | Unmapped; see component families |
| WKR `opt_wkr_001` | GT3.R Premium Indoor Car Cover | AAA/AAA | active | Unmapped; see component families |
| WUB `opt_wub_001` | Quad Center Exit Exhaust | AAA/AAA | active | S01: 1554 |
| Z15 `opt_z15_001` | Grand Sport Heritage Graphics | AAA/AAA | active | Unmapped; see component families |
| Z25 `opt_z25_001` | Grand Sport Launch Edition | ––A/––A | active | Unmapped; see component families |
| ZYC `opt_zyc_001` | Carbon Flash Mirrors and Spoiler | AAA/AAA | active | Unmapped; see component families |
| ZZ3 `opt_zz3_001` | Convertible Engine Appearance Package | –––/AAA | active | Unmapped; see component families |
| no RPO `opt_018` | Solar-Ray Light-Tinted Glass | SSS/SSS | active | Unmapped; see component families |

</details>

<details>
<summary>Z06 — catalog option identities and scope</summary>

| RPO / option ID | Catalog name / color | Scope | Lifecycle | Source layer IDs; unmapped if no supported identification |
| --- | --- | --- | --- | --- |
| 5DH `opt_5dh_001` | Satin Graphite Spider Wheels with Red Stripe | AAA/AAA | active | Unmapped; see component families |
| 5DK `opt_5dk_001` | Tech Bronze Spider Wheels | AAA/AAA | active | Unmapped; see component families |
| 5JR `opt_5jr_001` | Visible Carbon Fiber Outside Mirror Covers | ––A/––A | active | S11: 337, 1556; S12: 415, 1584; S13: 315, 1504; S14: 346, 1507 |
| 5JS `opt_5js_001` | Torch Red Mirror Caps | AAA/AAA | active | Unmapped; see component families |
| 5V5 `opt_5v5_001` | Visible Carbon Fiber Spoiler | ––A/––A | factory_unavailable | S11: 1467; S12: 76; S13: 1436; S14: 53 |
| 5ZC `opt_5zc_001` | Jake Logo Wheel Center Caps | AAA/AAA | active | Unmapped; see component families |
| 5ZD `opt_5zd_001` | Carbon Flash Crossed Flags Wheel Center Caps | AAA/AAA | active | Unmapped; see component families |
| 5ZV `opt_5zv_001` | Carbon Flash Metallic Three-Stanchion High Wing Spoiler | AAA/AAA | active | S11: 1473; S12: 82; S13: 1442; S14: 59 |
| B6P `opt_b6p_001` | Coupe Engine Appearance Package | AAA/––– | active | Unmapped; see component families |
| BCW `opt_bcw_001` | Red Engine Intake | AAA/AAA | active | Unmapped; see component families |
| BV4 `opt_bv4_001` | Personalized Specification Plaque | AAA/AAA | active | S11: 1123; S12: 1274; S13: 1097; S14: 1201 |
| C2Z `opt_c2z_001` | Visible Carbon Fiber Roof Panel | AAA/––– | active | S13: 417, 418, 419, 420, 421, 422, 423, 424, 425, 426; S14: 535, 536, 537, 538, 539, 540, 541, 542, 543, 544 |
| CBF `opt_cbf_001` | Body-color painted Rockers and splitter | AAA/AAA | active | Unmapped; see component families |
| CC3 `opt_cc3_001` | Transparent Roof Panel | AAA/––– | active | S13: 447; S14: 565 |
| CF7 `opt_cf7_001` | Body-Color Roof Panel | SSS/––– | active | S13: 427, 428, 429, 430, 431, 432, 433, 434, 435, 436; S14: 545, 546, 547, 548, 549, 550, 551, 552, 553, 554 |
| CF8 `opt_cf8_001` | Electrochromic Dimming Roof Panel | –AA/––– | factory_unavailable | S13: 437, 438, 439, 440, 441, 442, 443, 444, 445, 446; S14: 555, 556, 557, 558, 559, 560, 561, 562, 563, 564 |
| CFL `opt_cfl_001` | Extended Front Splitter, Carbon Flash | AAA/AAA | active | Unmapped; see component families |
| CFV `opt_cfv_002` | Visible Carbon Fiber Ground Effects | AAA/AAA | active | Unmapped; see component families |
| CFX `opt_cfx_001` | Personalized Corvette Museum Plaque | AAA/AAA | active | S11: 1122; S12: 1273; S13: 1096; S14: 1200 |
| CFZ `opt_cfz_001` | Carbon Flash Carbon Fiber Ground Effects | AAA/AAA | active | Unmapped; see component families |
| CM9 `opt_cm9_001` | Body-Color Power Convertible Hardtop | –––/SSS | active | S11: 452, 453, 454, 455, 456, 457, 458, 459, 460, 461; S12: 595, 596, 597, 598, 599, 600, 601, 602, 603, 604 |
| D3V `opt_d3v_001` | Engine Lighting | AAA/––– | active | Unmapped; see component families |
| D84 `opt_d84_001` | Carbon Flash Convertible Top | –––/AAA | active | Unmapped; see component families |
| D86 `opt_d86_001` | Body-Color Roof, Carbon Flash-painted Nacelles | –––/AAA | active | Unmapped; see component families |
| DPB `opt_dpb_001` | Carbon Flash/Blue Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DPC `opt_dpc_001` | Carbon Flash/Yellow Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DPG `opt_dpg_001` | Carbon Flash/Orange Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DPL `opt_dpl_001` | Carbon Flash/Red Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DPT `opt_dpt_001` | Carbon Flash/Silver Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DRG `opt_drg_001` | Carbon Flash Outside Mirrors | AAA/AAA | active | S11: 342, 1562; S12: 420, 1589; S13: 320, 1510; S14: 351, 1513 |
| DSY `opt_dsy_001` | Edge Orange Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DSZ `opt_dsz_001` | Edge Red Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DT0 `opt_dt0_001` | Competition Yellow Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DTC `f2c83936-8376-49a6-8408-d17e9f75aba0` | Royal Blue Full Length Dual Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DTH `opt_dth_001` | Carbon Flash Metallic Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DUB `opt_dub_001` | Sterling Silver Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DUE `opt_due_001` | Royal Blue/Carbon Flash Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DUK `opt_duk_001` | Edge Red/Carbon Flash Racing Stripes | AAA/AAA | active | Unmapped; see component families |
| DUW `opt_duw_001` | Edge Blue Racing Stripes | AAA/AAA | retired | Unmapped; see component families |
| DWK `opt_dwk_001` | Heated Power-Adjustable Outside Mirrors | S––/S–– | active | S11: 346, 1566; S12: 425, 1593; S13: 324, 1514; S14: 356, 1517 |
| DYX `opt_dyx_001` | Heated Power-Folding Outside Mirrors | –SS/–SS | active | S11: 345, 1565; S12: 424, 1592; S13: 323, 1513; S14: 355, 1516 |
| DZU `opt_dzu_001` | Carbon Flash/Competition Yellow Stinger Stripe | AAA/AAA | active | S11: 61; S12: 117; S13: 39; S14: 94 |
| DZV `opt_dzv_001` | Carbon Flash/Midnight Silver Stinger Stripe | AAA/AAA | active | S11: 60; S12: 116; S13: 38; S14: 93 |
| DZX `opt_dzx_001` | Carbon Flash/Edge Red Stinger Stripe | AAA/AAA | active | S11: 59; S12: 115; S13: 37; S14: 92 |
| EDU `opt_edu_001` | Body-Color and Carbon Flash Accents | AAA/AAA | active | Unmapped; see component families |
| EFR `opt_efr_001` | Carbon Flash Painted Accents | SSS/SSS | active | Unmapped; see component families |
| EFY `opt_efy_001` | Body-Color Exterior Accents | AAA/AAA | active | Unmapped; see component families |
| EYK `opt_eyk_001` | Chrome Exterior Badge Package | AAA/AAA | active | S11: 31; S12: 89; S13: 7; S14: 65 |
| EYT `opt_eyt_001` | Carbon Flash Exterior Badge Package | SSS/SSS | active | S11: 32, 33; S12: 88, 90; S13: 8; S14: 66 |
| G26 `opt_g26_001` | Sebring Orange Tintcoat | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| G4Z `opt_g4z_001` | Roswell Green Metallic | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| G8G `opt_g8g_001` | Arctic White | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GBA `opt_gba_001` | Black | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GBK `opt_gbk_001` | Competition Yellow Tintcoat Metallic | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GEC `opt_gec_001` | Pitch Gray Metallic | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GKA `opt_gka_001` | Blade Silver Metallic | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GKZ `opt_gkz_001` | Torch Red | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GPH `opt_gph_001` | Red Mist Metallic Tintcoat | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GTR `opt_gtr_001` | Admiral Blue Metallic | AAA/AAA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| J56 `opt_j56_001` | Performance Disc Brakes | SSS/SSS | active | S11: 239, 305; S12: 312, 377, 1648; S13: 217, 283; S14: 267, 332, 1569 |
| J57 `opt_j57_001` | Carbon Ceramic Brakes | AAA/AAA | active | S11: 238, 304, 1603; S12: 311, 378, 1647; S13: 216, 282, 1549; S14: 266, 333, 1568, 1597 |
| J6A `opt_j6a_001` | Black Painted Calipers | SSS/SSS | active | Unmapped; see component families |
| J6B `opt_j6b_001` | Blue-Painted Calipers | AAA/AAA | active | Unmapped; see component families |
| J6D `opt_j6d_001` | Dark Gray Metallic-Painted Calipers | AAA/AAA | active | Unmapped; see component families |
| J6E `opt_j6e_001` | Velocity Yellow-Painted Calipers | AAA/AAA | active | Unmapped; see component families |
| J6F `opt_j6f_001` | Bright Red-Painted Calipers | AAA/AAA | active | Unmapped; see component families |
| J6L `opt_j6l_001` | Orange-Painted Calipers | AAA/AAA | active | Unmapped; see component families |
| J6N `opt_j6n_001` | Edge Red-Painted Calipers | AAA/AAA | active | Unmapped; see component families |
| LT6 `opt_lt6_002` | 5.5L V8 LT6 Engine | SSS/SSS | active | S11: 1476; S12: 1523; S14: 1446 |
| NGA `opt_nga_001` | Black Exhaust Tips | SSS/SSS | active | Unmapped; see component families |
| NWI `opt_nwi_001` | Bright Chrome Exhaust Tips | AAA/AAA | active | Unmapped; see component families |
| PCQ `opt_pcq_001` | Grille Screen Protection Package | AAA/AAA | active | Unmapped; see component families |
| PCZ `opt_pcz_001` | Tech Bronze Accent Package | AAA/AAA | active | Unmapped; see component families |
| PDA `opt_pda_001` | Jake C8.R Graphics Package | AAA/AAA | active | Unmapped; see component families |
| PDB `opt_pdb_001` | Carbon Fiber Wheel and Brake Package | AAA/AAA | active | Unmapped; see component families |
| PDD `opt_pdd_001` | Z07 Carbon Flash Aero and Wheel Package | AAA/AAA | active | Unmapped; see component families |
| PDF `opt_pdf_001` | Z07 Visible Carbon Aero and Wheel Package | AAA/AAA | active | Unmapped; see component families |
| R88 `opt_r88_001` | Front Illuminated Crossed Flags Emblem | AAA/AAA | factory_unavailable | S11: 35; S12: 94; S13: 13; S14: 71 |
| RIK `opt_rik_001` | Torch Red Rear Corvette Script Badge | AAA/AAA | active | S12: 87; S14: 64 |
| RIN `opt_rin_001` | Arctic White Rear Corvette Script Badge | AAA/AAA | active | S12: 86; S13: 6; S14: 63 |
| ROU `opt_rou_001` | Pearl Nickel Wheels | AAA/AAA | active | Unmapped; see component families |
| ROX `opt_rox_001` | Carbon Flash Machined-Edge Wheels | AAA/AAA | active | Unmapped; see component families |
| ROY `opt_roy_001` | Carbon Flash-Painted Carbon Fiber Wheels | AAA/AAA | active | Unmapped; see component families |
| ROZ `opt_roz_001` | Visible Carbon Fiber Wheels | AAA/AAA | active | Unmapped; see component families |
| RWH `opt_rwh_001` | Black Premium Indoor Car Cover | AAA/AAA | active | Unmapped; see component families |
| RWJ `opt_rwj_001` | Gray Premium Outdoor Car Cover | AAA/AAA | active | Unmapped; see component families |
| RXI `opt_rxi_001` | Visible Carbon Fiber LT6 Engine Cover | AAA/––– | active | S13: 1446 |
| RYQ `opt_ryq_001` | Visible Carbon Fiber Door Intake Trim | ––A/––A | factory_unavailable | S11: 74; S12: 220; S13: 52; S14: 175 |
| S47 `opt_s47_001` | Chrome Lug Nuts | AAA/AAA | active | Unmapped; see component families |
| SBT `opt_sbt_001` | Dual Roof Package | AAA/––– | active | S13: 406; S14: 524 |
| SC7 `opt_sc7_001` | Roof Panel Storage Pouch | AAA/––– | active | Unmapped; see component families |
| SDA `opt_sda_001` | Black Recovery Hook | AAA/AAA | active | Unmapped; see component families |
| SFE `opt_sfe_001` | Chrome Wheel Locks | AAA/AAA | active | Unmapped; see component families |
| SFZ `opt_sfz_001` | Dark Stealth Crossed Flags Emblems | AAA/AAA | active | S11: 34; S12: 91; S13: 9, 10; S14: 67, 68 |
| SG1 `opt_sg1_001` | Edge Red Z06 Badges | AAA/AAA | active | S11: 36; S12: 26; S13: 14 |
| SHT `opt_sht_001` | Tech Bronze Jake Hood Graphic | AAA/AAA | active | Unmapped; see component families |
| SIG `opt_sig_001` | Clear Smoked Spoiler Extension | AAA/AAA | active | S11: 1461; S12: 31; S13: 1430; S14: 8 |
| SL8 `opt_sl8_001` | Edge Red Rear Corvette Script Badge | AAA/AAA | active | S12: 85; S14: 62 |
| SL9 `opt_sl9_001` | Engine Specification Plaque | AAA/AAA | active | Unmapped; see component families |
| SLK `opt_slk_001` | Edge Red Rear Hatch Strut Bracket | AAA/––– | active | Unmapped; see component families |
| SLN `opt_sln_001` | Visible Carbon Fiber Engine Cross Brace | AAA/––– | active | S13: 1445 |
| SNE `opt_sne_001` | Jake Hood Graphic | AAA/AAA | active | Unmapped; see component families |
| SOA `opt_soa_001` | Black Spider Wheels | AAA/AAA | active | Unmapped; see component families |
| SOE `opt_soe_002` | Titanium Satin Spider Wheels | SSS/SSS | active | Unmapped; see component families |
| SOM `opt_som_001` | Bright Polished Wheels | AAA/AAA | active | Unmapped; see component families |
| SON `opt_son_001` | Gloss Black Wheels | AAA/AAA | active | Unmapped; see component families |
| SPY `opt_spy_001` | Black Lug Nuts | AAA/AAA | active | Unmapped; see component families |
| SPZ `opt_spz_001` | Black Wheel Locks | AAA/AAA | active | Unmapped; see component families |
| SRK `opt_srk_001` | 10-Spoke Pearl Nickel Wheels | AAA/AAA | active | Unmapped; see component families |
| SRN `opt_srn_001` | 10-Spoke Gloss Black Wheels | AAA/AAA | active | Unmapped; see component families |
| STX `opt_stx_001` | 10-Spoke Bright Polished Wheels | AAA/AAA | active | Unmapped; see component families |
| STZ `opt_stz_001` | Visible Carbon Fiber Red Stripe Wheels | AAA/AAA | active | Unmapped; see component families |
| T0E `opt_t0e_001` | Low Rear Spoiler | SSS/SSS | active | Unmapped; see component families |
| T0F `opt_t0f_001` | Carbon Flash-Painted Carbon Fiber Aero Package | AAA/AAA | active | S11: 1449; S12: 59; S13: 1418; S14: 36 |
| T0G `opt_t0g_001` | Visible Carbon Fiber Aero Package | AAA/AAA | active | S11: 1448; S12: 58; S13: 1417; S14: 35 |
| T4L `opt_t4l_001` | LED Headlamps | SSS/SSS | active | S11: 71; S12: 655; S13: 49; S14: 616 |
| UFT `opt_uft_001` | Side Blind Zone Alert | –SS/–SS | active | S11: 1559; S13: 1507; S14: 1510 |
| UG1 `opt_ug1_001` | Three-Channel Programmable Universal Home Remote | –SS/–SS | active | S11: 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503; S12: 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 639, 640, 641, 642, 643, 644, 645, 646; S13: 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489; S14: 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607 |
| VPO `opt_vpo_001` | Tech Bronze Jake C8.R Rear Hash Graphic | AAA/AAA | active | S11: 63; S12: 119; S13: 41; S14: 96 |
| VPW `opt_vpw_001` | Jake C8.R Rear Hash Graphic | AAA/AAA | active | S11: 64; S12: 120; S13: 42; S14: 97 |
| VTB `opt_vtb_001` | Black Rear Fascia/Roof Protector | AAA/AAA | active | Unmapped; see component families |
| VUP `opt_vup_001` | Engine Bay Closeout Graphics | AAA/––– | active | Unmapped; see component families |
| VWE `opt_vwe_001` | Front Radiator Grille Screens | AAA/AAA | active | S11: 161; S12: 1568; S13: 139; S14: 1491 |
| VWT `opt_vwt_001` | Insect Protection Grille Screen | AAA/AAA | active | Unmapped; see component families |
| WKR `opt_wkr_001` | GT3.R Premium Indoor Car Cover | AAA/AAA | active | Unmapped; see component families |
| WKS `opt_wks_001` | Premium Indoor Car Cover | AAA/AAA | active | Unmapped; see component families |
| WUB `opt_wub_001` | Quad Center Exit Exhaust | SSS/SSS | active | S11: 1479; S12: 1531; S13: 1451; S14: 1454 |
| Z07 `opt_z07_001` | Z07 Performance Package | AAA/AAA | active | Unmapped; see component families |
| ZYC `opt_zyc_001` | Carbon Flash Mirrors and Spoiler | AAA/AAA | active | Unmapped; see component families |
| ZZ3 `opt_zz3_001` | Convertible Engine Appearance Package | –––/AAA | active | Unmapped; see component families |
| no RPO `opt_203` | Solar-Ray Light-Tinted Glass | SSS/SSS | active | Unmapped; see component families |

</details>

<details>
<summary>ZR1 — catalog option identities and scope</summary>

| RPO / option ID | Catalog name / color | Scope | Lifecycle | Source layer IDs; unmapped if no supported identification |
| --- | --- | --- | --- | --- |
| 5JR `opt_5jr_001` | Visible Carbon Fiber Outside Mirror Covers | AA/AA | active | S15: 202, 1106; S16: 290, 1157; S17: 180, 1127; S18: 283, 1171 |
| 5JS `opt_5js_001` | Torch Red Mirror Caps | AA/AA | active | Unmapped; see component families |
| 5WN `opt_5wn_001` | ZR1 and ZR1X Aero Enhancement Kit | AA/–– | active | Unmapped; see component families |
| 5ZC `opt_5zc_001` | Jake Logo Wheel Center Caps | AA/AA | active | Unmapped; see component families |
| 5ZD `opt_5zd_001` | Carbon Flash Crossed Flags Wheel Center Caps | AA/AA | active | Unmapped; see component families |
| BV4 `opt_bv4_001` | Personalized Specification Plaque | AA/AA | active | S15: 774; S16: 909; S17: 782; S18: 912 |
| C2Z `opt_c2z_001` | Visible Carbon Fiber Roof Panel | SS/–– | active | S17: 289, 290, 291, 292, 293, 294, 295, 296, 297, 298; S18: 415, 416, 417, 418, 419, 420, 421, 422, 423, 424 |
| CFC `opt_cfc_002` | Visible Carbon Fiber Retractable Hardtop | ––/SS | active | S15: 302, 303, 304, 305, 306, 307, 308, 309, 310, 311; S16: 401, 402, 403, 404, 405, 406, 407, 408, 409, 410 |
| CFV `opt_cfv_002` | Visible Carbon Fiber Ground Effects | SS/SS | active | Unmapped; see component families |
| CFX `opt_cfx_001` | Personalized Corvette Museum Plaque | AA/AA | active | S16: 908; S17: 781; S18: 911 |
| DPB `opt_dpb_001` | Carbon Flash/Blue Racing Stripes | AA/AA | active | Unmapped; see component families |
| DPC `opt_dpc_001` | Carbon Flash/Yellow Racing Stripes | AA/AA | active | Unmapped; see component families |
| DPG `opt_dpg_001` | Carbon Flash/Orange Racing Stripes | AA/AA | active | Unmapped; see component families |
| DPL `opt_dpl_001` | Carbon Flash/Red Racing Stripes | AA/AA | active | Unmapped; see component families |
| DPT `opt_dpt_001` | Carbon Flash/Silver Racing Stripes | AA/AA | active | Unmapped; see component families |
| DRG `opt_drg_001` | Carbon Flash Outside Mirrors | AA/AA | active | S15: 207, 1111; S16: 295, 1162; S17: 185, 1132; S18: 288, 1176 |
| DSY `opt_dsy_001` | Edge Orange Racing Stripes | AA/AA | active | Unmapped; see component families |
| DSZ `opt_dsz_001` | Edge Red Racing Stripes | AA/AA | active | Unmapped; see component families |
| DT0 `opt_dt0_001` | Competition Yellow Racing Stripes | AA/AA | active | Unmapped; see component families |
| DTC `opt_dtc_001` | Royal Blue Full-Length Dual Racing Stripes | AA/AA | active | Unmapped; see component families |
| DTH `opt_dth_001` | Carbon Flash Metallic Racing Stripes | AA/AA | active | Unmapped; see component families |
| DUB `opt_dub_001` | Sterling Silver Racing Stripes | AA/AA | active | Unmapped; see component families |
| DUE `opt_due_001` | Royal Blue/Carbon Flash Racing Stripes | AA/AA | active | Unmapped; see component families |
| DUK `opt_duk_001` | Edge Red/Carbon Flash Racing Stripes | AA/AA | active | Unmapped; see component families |
| DUW `opt_duw_001` | Edge Blue Racing Stripes | AA/AA | retired | Unmapped; see component families |
| DWK `opt_dwk_001` | Heated Power-Adjustable Outside Mirrors | S–/S– | active | S15: 211, 1115; S16: 300, 1166; S17: 189, 1136; S18: 293, 1180 |
| DYX `opt_dyx_001` | Heated Power-Folding Outside Mirrors | –S/–S | active | S15: 210, 1114; S16: 299, 1165; S17: 188, 1135; S18: 292, 1179 |
| EFR `opt_efr_001` | Carbon Flash Painted Accents | SS/SS | active | Unmapped; see component families |
| ETV `opt_etv_001` | Body-Color Carbon Fiber Split-Window Trim | AA/–– | active | S17: 1100, 1101, 1102, 1103, 1104, 1105, 1106, 1107, 1108, 1109; S18: 135, 136, 137, 138, 139, 140, 141, 142, 143, 144 |
| EYK `opt_eyk_001` | Chrome Exterior Badge Package | AA/AA | active | S15: 30; S16: 72; S17: 10; S18: 51, 53 |
| EYT `opt_eyt_001` | Carbon Flash Exterior Badge Package | SS/SS | active | S15: 31, 32; S16: 73; S17: 11; S18: 52, 54 |
| G26 `opt_g26_001` | Sebring Orange Tintcoat | AA/AA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| G4Z `opt_g4z_001` | Roswell Green Metallic | AA/AA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| G8G `opt_g8g_001` | Arctic White | AA/AA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GBA `opt_gba_001` | Black | AA/AA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GBK `opt_gbk_001` | Competition Yellow Tintcoat Metallic | AA/AA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GEC `opt_gec_001` | Pitch Gray Metallic | AA/AA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GKA `opt_gka_001` | Blade Silver Metallic | AA/AA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GKZ `opt_gkz_001` | Torch Red | AA/AA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GPH `opt_gph_001` | Red Mist Metallic Tintcoat | AA/AA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GTR `opt_gtr_001` | Admiral Blue Metallic | AA/AA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| J58 `opt_j58_002` | ZR1-Specific Carbon Ceramic Brakes | SS/SS | active | S15: 139, 182, 1134, 1152; S16: 220, 263, 1202, 1225; S17: 117, 160, 1164; S18: 227, 270, 1214, 1236 |
| J59 `opt_j59_002` | 10-Piston Front / 6-Piston Rear Carbon Ceramic Brakes | AA/AA | active | S15: 138, 181, 1151; S16: 219, 262, 1201; S17: 116, 159, 1163; S18: 226, 269, 1213 |
| J6B `opt_j6b_001` | Blue-Painted Calipers | AA/AA | active | Unmapped; see component families |
| J6D `opt_j6d_001` | Dark Gray Metallic-Painted Calipers | SS/SS | active | Unmapped; see component families |
| J6E `opt_j6e_001` | Velocity Yellow-Painted Calipers | AA/AA | active | Unmapped; see component families |
| J6F `opt_j6f_001` | Bright Red-Painted Calipers | AA/AA | active | Unmapped; see component families |
| J6L `opt_j6l_001` | Orange-Painted Calipers | AA/AA | active | Unmapped; see component families |
| J6N `opt_j6n_001` | Edge Red-Painted Calipers | AA/AA | active | Unmapped; see component families |
| J6O `opt_j6o_001` | Bronze-Painted Calipers | AA/AA | active | Unmapped; see component families |
| LT7 `opt_lt7_002` | 5.5L Twin-Turbo V8 Engine | SS/SS | active | S15: 1036; S16: 1093; S18: 1107 |
| NGA `opt_nga_001` | Black Exhaust Tips | SS/SS | active | Unmapped; see component families |
| NWI `opt_nwi_001` | Bright Chrome Exhaust Tips | AA/AA | active | Unmapped; see component families |
| PCQ `opt_pcq_001` | Grille Screen Protection Package | AA/AA | factory_unavailable | Unmapped; see component families |
| PCR `opt_pcr_001` | ZTK Track Performance Package with Aero Enhancement Kit | AA/–– | active | Unmapped; see component families |
| R88 `opt_r88_001` | Front Illuminated Crossed Flags Emblem | AA/AA | factory_unavailable | S15: 35; S16: 77; S17: 13; S18: 58, 59 |
| RIK `opt_rik_001` | Torch Red Rear Corvette Script Badge | AA/AA | active | S16: 71; S18: 50 |
| RIN `opt_rin_001` | Arctic White Rear Corvette Script Badge | AA/AA | active | S16: 70; S18: 49 |
| RWH `opt_rwh_001` | Black Premium Indoor Car Cover | AA/AA | active | Unmapped; see component families |
| RWJ `opt_rwj_001` | Gray Premium Outdoor Car Cover | AA/AA | active | Unmapped; see component families |
| S47 `opt_s47_001` | Chrome Lug Nuts | AA/AA | active | Unmapped; see component families |
| SB9 `opt_sb9_001` | Hood and Roof Decal Package | AA/AA | active | Unmapped; see component families |
| SBT `opt_sbt_001` | Dual Roof Package | AA/–– | active | S17: 278; S18: 404 |
| SC7 `opt_sc7_001` | Roof Panel Storage Pouch | AA/–– | active | Unmapped; see component families |
| SDA `opt_sda_001` | Black Recovery Hook | AA/AA | active | Unmapped; see component families |
| SFE `opt_sfe_001` | Chrome Wheel Locks | AA/AA | active | Unmapped; see component families |
| SFZ `opt_sfz_001` | Dark Stealth Crossed Flags Emblems | AA/AA | active | S15: 33; S16: 74; S17: 12; S18: 55 |
| SIG `opt_sig_001` | Clear Smoked Spoiler Extension | AA/AA | active | S15: 1027; S16: 28; S17: 1031; S18: 7 |
| SL8 `opt_sl8_001` | Edge Red Rear Corvette Script Badge | AA/AA | active | S16: 69; S17: 9; S18: 48 |
| SLK `opt_slk_001` | Edge Red Rear Hatch Strut Bracket | AA/–– | active | Unmapped; see component families |
| SLN `opt_sln_001` | Visible Carbon Fiber Engine Cross Brace | AA/–– | factory_unavailable | Unmapped; see component families |
| SOF `opt_sof_001` | 20-Spoke Edge Blue-Painted Forged Aluminum Wheels | AA/AA | active | Unmapped; see component families |
| SOG `opt_sog_001` | 20-Spoke Carbon Flash-Painted Forged Aluminum Wheels | AA/AA | active | Unmapped; see component families |
| SOH `opt_soh_001` | 20-Spoke Bright Machined Forged Aluminum Wheels | AA/AA | active | Unmapped; see component families |
| SOJ `opt_soj_002` | 20-Spoke Sterling Silver-Painted Forged Aluminum Wheels | SS/SS | active | Unmapped; see component families |
| SPY `opt_spy_001` | Black Lug Nuts | AA/AA | active | Unmapped; see component families |
| SPZ `opt_spz_001` | Black Wheel Locks | AA/AA | active | Unmapped; see component families |
| SU1 `opt_su1_001` | 10-Spoke Visible Carbon Fiber Wheels | AA/AA | active | Unmapped; see component families |
| T0E `opt_t0e_001` | Low Rear Spoiler | SS/SS | active | Unmapped; see component families |
| T4L `opt_t4l_001` | LED Headlamps | SS/SS | active | S15: 67; S16: 448; S17: 45; S18: 472 |
| TOM `opt_tom_001` | Visible Carbon Fiber Aero Package | AA/AA | active | S15: 1033; S16: 66; S17: 1037; S18: 45 |
| UG1 `opt_ug1_001` | Three-Channel Programmable Universal Home Remote | –S/–S | active | S15: 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342; S16: 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439; S17: 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338; S18: 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463 |
| VTB `opt_vtb_001` | Black Rear Fascia/Roof Protector | AA/AA | active | Unmapped; see component families |
| VWE `opt_vwe_001` | Front Radiator Grille Screens | AA/AA | active | S15: 84; S16: 1141; S17: 62; S18: 1155 |
| VWT `opt_vwt_001` | Insect Protection Grille Screen | AA/AA | factory_unavailable | Unmapped; see component families |
| WKR `opt_wkr_001` | GT3.R Premium Indoor Car Cover | AA/AA | active | Unmapped; see component families |
| WUB `opt_wub_001` | Quad Center Exit Exhaust | SS/SS | active | S15: 1039; S16: 1101; S17: 1042; S18: 1115 |
| ZTK `opt_ztk_001` | ZTK Track Performance Package | AA/AA | active | Unmapped; see component families |
| ZYC `opt_zyc_001` | Carbon Flash Mirrors and Spoiler | AA/AA | active | Unmapped; see component families |
| no RPO `opt_731` | Solar-Ray Light-Tinted Glass | SS/SS | active | Unmapped; see component families |

</details>

<details>
<summary>ZR1X — catalog option identities and scope</summary>

| RPO / option ID | Catalog name / color | Scope | Lifecycle | Source layer IDs; unmapped if no supported identification |
| --- | --- | --- | --- | --- |
| 5JR `opt_5jr_001` | Visible Carbon Fiber Outside Mirror Covers | AA/AA | active | S19: 186, 1108; S20: 275, 1136; S21: 165, 1113; S22: 272, 1148 |
| 5JS `opt_5js_001` | Torch Red Mirror Caps | AA/AA | active | Unmapped; see component families |
| 5WN `opt_5wn_001` | ZR1 and ZR1X Aero Enhancement Kit | AA/–– | active | Unmapped; see component families |
| 5ZC `opt_5zc_001` | Jake Logo Wheel Center Caps | AA/AA | active | Unmapped; see component families |
| 5ZD `opt_5zd_001` | Carbon Flash Crossed Flags Wheel Center Caps | AA/AA | active | Unmapped; see component families |
| BV4 `opt_bv4_001` | Personalized Specification Plaque | AA/AA | active | S19: 775; S20: 887; S21: 766; S22: 895 |
| C2Z `opt_c2z_001` | Visible Carbon Fiber Roof Panel | SS/–– | active | S21: 276, 277, 278, 279, 280, 281, 282, 283, 284, 285; S22: 403, 404, 405, 406, 407, 408, 409, 410, 411, 412 |
| CFC `opt_cfc_002` | Visible Carbon Fiber Retractable Hardtop | ––/SS | active | S19: 287, 288, 289, 290, 291, 292, 293, 294, 295, 296; S20: 386, 387, 388, 389, 390, 391, 392, 393, 394, 395 |
| CFX `opt_cfx_001` | Personalized Corvette Museum Plaque | AA/AA | active | S19: 774; S20: 886; S21: 765; S22: 894 |
| DPB `opt_dpb_001` | Carbon Flash/Blue Racing Stripes | AA/AA | active | Unmapped; see component families |
| DPC `opt_dpc_001` | Carbon Flash/Yellow Racing Stripes | AA/AA | active | Unmapped; see component families |
| DPG `opt_dpg_001` | Carbon Flash/Orange Racing Stripes | AA/AA | active | Unmapped; see component families |
| DPL `opt_dpl_001` | Carbon Flash/Red Racing Stripes | AA/AA | active | Unmapped; see component families |
| DPT `opt_dpt_001` | Carbon Flash/Silver Racing Stripes | AA/AA | active | Unmapped; see component families |
| DRG `opt_drg_001` | Carbon Flash Outside Mirrors | AA/AA | active | S19: 191, 1113; S20: 280, 1141; S21: 170, 1119; S22: 277, 1153 |
| DSY `opt_dsy_001` | Edge Orange Racing Stripes | AA/AA | active | Unmapped; see component families |
| DSZ `opt_dsz_001` | Edge Red Racing Stripes | AA/AA | active | Unmapped; see component families |
| DT0 `opt_dt0_001` | Competition Yellow Racing Stripes | AA/AA | active | Unmapped; see component families |
| DTC `opt_dtc_001` | Royal Blue Full-Length Dual Racing Stripes | AA/AA | active | Unmapped; see component families |
| DTH `opt_dth_001` | Carbon Flash Metallic Racing Stripes | AA/AA | active | Unmapped; see component families |
| DUB `opt_dub_001` | Sterling Silver Racing Stripes | AA/AA | active | Unmapped; see component families |
| DUE `opt_due_001` | Asymmetrical Royal Blue/Carbon Flash Full Length Dual Racing Stripes | AA/AA | active | Unmapped; see component families |
| DUK `opt_duk_001` | Edge Red/Carbon Flash Racing Stripes | AA/AA | active | Unmapped; see component families |
| DUW `opt_duw_001` | Edge Blue Racing Stripes | AA/AA | retired | Unmapped; see component families |
| DWK `opt_dwk_001` | Heated Power-Adjustable Outside Mirrors | S–/S– | active | S19: 195, 1117; S20: 285, 1145; S21: 174, 1123; S22: 282, 1157 |
| DYX `opt_dyx_001` | Heated Power-Folding Outside Mirrors | –S/–S | active | S19: 194, 1116; S20: 284, 1144; S21: 173, 1122; S22: 281, 1156 |
| EFR `opt_efr_001` | Carbon Flash Painted Accents | SS/SS | active | Unmapped; see component families |
| ETV `opt_etv_001` | Body-Color Carbon Fiber Split-Window Trim | AA/–– | active | S21: 1087, 1088, 1089, 1090, 1091, 1092, 1093, 1094, 1095, 1096; S22: 139, 140, 141, 142, 143, 144, 145, 146, 147, 148 |
| EYK `opt_eyk_001` | Chrome Exterior Badge Package | AA/AA | active | S19: 30; S20: 70; S21: 9; S22: 53 |
| EYT `opt_eyt_001` | Carbon Flash Exterior Badge Package | SS/SS | active | S19: 31; S20: 71; S21: 10, 11; S22: 52, 54 |
| G26 `opt_g26_001` | Sebring Orange Tintcoat | AA/AA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| G4Z `opt_g4z_001` | Roswell Green Metallic | AA/AA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| G8G `opt_g8g_001` | Arctic White | AA/AA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GBA `opt_gba_001` | Black | AA/AA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GBK `opt_gbk_001` | Competition Yellow Tintcoat Metallic | AA/AA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GEC `opt_gec_001` | Pitch Gray Metallic | AA/AA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GKA `opt_gka_001` | Blade Silver Metallic | AA/AA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GKZ `opt_gkz_001` | Torch Red | AA/AA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GPH `opt_gph_001` | Red Mist Metallic Tintcoat | AA/AA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| GTR `opt_gtr_001` | Admiral Blue Metallic | AA/AA | active | Each Sxx/paint inventory: exact base and matching component paint peers |
| HP1 `opt_hp1_002` | Electrified Front Axle | SS/SS | active | Unmapped; see component families |
| J59 `opt_j59_002` | 10-Piston Front / 6-Piston Rear Carbon Ceramic Brakes | SS/SS | active | S19: 131, 166, 1143; S20: 213, 248, 1173; S21: 110, 145, 1145; S22: 224, 259, 1185 |
| J6B `opt_j6b_001` | Blue-Painted Calipers | AA/AA | active | Unmapped; see component families |
| J6D `opt_j6d_001` | Dark Gray Metallic-Painted Calipers | SS/SS | active | Unmapped; see component families |
| J6E `opt_j6e_001` | Velocity Yellow-Painted Calipers | AA/AA | active | Unmapped; see component families |
| J6F `opt_j6f_001` | Bright Red-Painted Calipers | AA/AA | active | Unmapped; see component families |
| J6L `opt_j6l_001` | Orange-Painted Calipers | AA/AA | active | Unmapped; see component families |
| J6N `opt_j6n_001` | Edge Red-Painted Calipers | AA/AA | active | Unmapped; see component families |
| J6O `opt_j6o_001` | Bronze-Painted Calipers | AA/AA | active | Unmapped; see component families |
| LT7 `opt_lt7_002` | 5.5L Twin-Turbo V8 Engine | SS/SS | active | S19: 1036; S20: 1072; S21: 1025; S22: 1084 |
| NGA `opt_nga_001` | Black Exhaust Tips | SS/SS | active | Unmapped; see component families |
| NWI `opt_nwi_001` | Bright Chrome Exhaust Tips | AA/AA | active | Unmapped; see component families |
| PCQ `opt_pcq_001` | Grille Screen Protection Package | AA/AA | factory_unavailable | Unmapped; see component families |
| PCR `opt_pcr_001` | ZTK Track Performance Package with Aero Enhancement Kit | AA/–– | active | Unmapped; see component families |
| R88 `opt_r88_001` | Front Illuminated Crossed Flags Emblem | AA/AA | factory_unavailable | S19: 34; S20: 75, 76; S21: 13; S22: 58 |
| RIK `opt_rik_001` | Torch Red Rear Corvette Script Badge | AA/AA | active | S20: 69; S22: 51 |
| RIN `opt_rin_001` | Arctic White Rear Corvette Script Badge | AA/AA | active | S20: 68; S22: 50 |
| RWH `opt_rwh_001` | Black Premium Indoor Car Cover | AA/AA | active | Unmapped; see component families |
| RWJ `opt_rwj_001` | Gray Premium Outdoor Car Cover | AA/AA | active | Unmapped; see component families |
| S47 `opt_s47_001` | Chrome Lug Nuts | AA/AA | active | Unmapped; see component families |
| SB9 `opt_sb9_001` | Hood and Roof Decal Package | AA/AA | active | Unmapped; see component families |
| SBT `opt_sbt_001` | Dual Roof Package | AA/–– | active | S21: 265; S22: 392 |
| SC7 `opt_sc7_001` | Roof Panel Storage Pouch | AA/–– | active | Unmapped; see component families |
| SDA `opt_sda_001` | Black Recovery Hook | AA/AA | active | Unmapped; see component families |
| SFE `opt_sfe_001` | Chrome Wheel Locks | AA/AA | active | Unmapped; see component families |
| SFZ `opt_sfz_001` | Dark Stealth Crossed Flags Emblems | AA/AA | active | S19: 32, 33; S20: 72; S21: 12; S22: 55 |
| SL8 `opt_sl8_001` | Edge Red Rear Corvette Script Badge | AA/AA | active | S20: 67; S22: 49 |
| SLK `opt_slk_001` | Edge Red Rear Hatch Strut Bracket | AA/–– | active | Unmapped; see component families |
| SLN `opt_sln_001` | Visible Carbon Fiber Engine Cross Brace | AA/–– | factory_unavailable | S21: 1024 |
| SOF `opt_sof_001` | 20-Spoke Edge Blue-Painted Forged Aluminum Wheels | AA/AA | active | Unmapped; see component families |
| SOG `opt_sog_001` | 20-Spoke Carbon Flash-Painted Forged Aluminum Wheels | AA/AA | active | Unmapped; see component families |
| SOH `opt_soh_001` | 20-Spoke Bright Machined Forged Aluminum Wheels | AA/AA | active | Unmapped; see component families |
| SOJ `opt_soj_002` | 20-Spoke Sterling Silver-Painted Forged Aluminum Wheels | SS/SS | active | Unmapped; see component families |
| SPY `opt_spy_001` | Black Lug Nuts | AA/AA | active | Unmapped; see component families |
| SPZ `opt_spz_001` | Black Wheel Locks | AA/AA | active | Unmapped; see component families |
| SU1 `opt_su1_001` | 10-Spoke Visible Carbon Fiber Wheels | AA/AA | active | Unmapped; see component families |
| T0E `opt_t0e_001` | Low Rear Spoiler | SS/SS | active | Unmapped; see component families |
| T4L `opt_t4l_001` | LED Headlamps | SS/SS | active | S19: 67; S20: 433; S21: 46; S22: 460 |
| TOM `opt_tom_002` | Visible Carbon Fiber Aero Package | AA/AA | active | S19: 1033; S20: 64; S21: 1021; S22: 46 |
| UFT `opt_uft_001` | Side Blind Zone Alert | –S/–S | active | S21: 1116 |
| UG1 `opt_ug1_001` | Three-Channel Programmable Universal Home Remote | –S/–S | active | S19: 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327; S20: 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424; S21: 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328; S22: 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451 |
| VTB `opt_vtb_001` | Black Rear Fascia/Roof Protector | AA/AA | active | Unmapped; see component families |
| VWE `opt_vwe_001` | Front Radiator Grille Screens | AA/AA | active | S19: 84; S20: 1120; S21: 63; S22: 1132 |
| VWT `opt_vwt_001` | Insect Protection Grille Screen | AA/AA | factory_unavailable | Unmapped; see component families |
| WKR `opt_wkr_001` | GT3.R Premium Indoor Car Cover | AA/AA | active | Unmapped; see component families |
| WUB `opt_wub_001` | Quad Center Exit Exhaust | SS/SS | active | S19: 1039; S20: 1080; S21: 1028; S22: 1092 |
| ZTK `opt_ztk_001` | ZTK Track Performance Package | AA/AA | active | Unmapped; see component families |
| ZYC `opt_zyc_001` | Carbon Flash Mirrors and Spoiler | AA/AA | active | Unmapped; see component families |
| no RPO `opt_732` | Solar-Ray Light-Tinted Glass | SS/SS | active | Unmapped; see component families |

</details>

Package completeness: Stingray TVS/T0A/Z51/ZF1 must cover the front-splitter/rear-spoiler or delete combination actually resolved by the catalog; current 5ZU art does not establish it. Grand Sport T0F/FEB/FEY needs the connected ground-effects/brake context; GSX has no T0F identity. Z06 T0F/T0G, CFZ/CFV/CBF and Z07/PDD/PDF require front/side pieces as well as the wing. ZR1/ZR1X TOM and ZTK are separate identities; 5WN/PCR are also catalog options and need a complete aero-enhancement source mapping. No layer labelled 5WN or PCR was found; unidentified Front_Fascia/Hood/Ground_Effects branches do not establish those kits.

## Source register and integrity

Each PSB is **V + relative path**. Disposable copies are `/private/tmp/visualizer-audit-20261009/Sxx.psb`. The table pins the saved original and identical starting copy. “4-way match” means original before = copy before = original after = copy after. Original files were never opened by the audit; the GSX original was already open beforehand. S05 is the uncleaned Grand Sport view-01 comparison, not the selected binding source S04.

| Key | PSB path relative to V | SHA-256 (original/copy before) | Native layer count | Final integrity |
| --- | --- | --- | --- | --- |
| S01 | `27vette-grand-sport-X-asset-proof copy.psb` | 60f268dc5bbd8c73f269bea7644e8489acf3b2a3c34206d7aa06b144ef3e73c4 | 1411 | 4-way match |
| S02 | `grandsport/e.convertible.exterior.01.psb` | 5015b3f7c16f102f957ae122f1f5e84c6851e55164cc9ca13a27835e80a95347 | 1653 | 4-way match |
| S03 | `grandsport/e.convertible.exterior.02.psb` | 5cc688c2182aafa7ba45e4d59c8a7aa8c46e7200f6531fd509a3f9eee2b114dc | 1667 | 4-way match |
| S04 | `grandsport/e.coupe.exterior.01 - cleaned.psb` | 1e9360c73d3acdb17121e9b2bc8ae8af14c5ea9507b58ab61c4b2b96e1f9345e | 1400 | 4-way match |
| S05 | `grandsport/e.coupe.exterior.01.psb` | 6f7c28bc216ea47915102f43f3e2388c3d263c7468d4a9a623e52375075ee86f | 1624 | 4-way match |
| S06 | `grandsport/e.coupe.exterior.02.psb` | 5d74a227f5ae73e72da105c7abaa1ebcd450d3b9ef5156a488d3016a7f6df5ac | 1638 | 4-way match |
| S07 | `stingray/c.convertible.exterior.01.psb` | bdd130f64833eb9b676e2ca6b3c31bd9f99a290931bf43a29ee1cf555924627e | 1510 | 4-way match |
| S08 | `stingray/c.convertible.exterior.02.psb` | 12c3420dec6d76834757f66726edc6e2cf0832062480b52ff11664a14d510e53 | 1551 | 4-way match |
| S09 | `stingray/c.coupe.exterior.01.psb` | 16d97f2bc1fc980372be5a5d1e1f15332a899bb320e5dcb346478f0deeda1584 | 1482 | 4-way match |
| S10 | `stingray/c.coupe.exterior.02.psb` | c51162b8c3928923d09e859c94819dc0964e254ca4a3a93ba9aa2daae6640402 | 1489 | 4-way match |
| S11 | `z06/exterior/27CHCORZ_CON_Studio_f02.psb` | 00b87965e6e59e038967231b9fe6fb742ab9e71a6dc047bcdcd293666faeb73f | 1513 | 4-way match |
| S12 | `z06/exterior/27CHCORZ_CON_Studio_f04.psb` | 625a9d3e568cc27d120dcfd9bfe8675571c185016afb66536f1d74777a681d10 | 1586 | 4-way match |
| S13 | `z06/exterior/27CHCORZ_COU_Studio_f02.psb` | f00141f41e261f585ed375508fc41b5458196506ef93613df44dcb6fa5dcd2ee | 1464 | 4-way match |
| S14 | `z06/exterior/27CHCORZ_COU_Studio_f04.psb` | 88859ad64dd93de69f9c065c60cb7f06b2dd6df6bfcfb52f77af6f7f825e6041 | 1506 | 4-way match |
| S15 | `zr1/exterior/27CHCOZR_CON_Studio_f02.psb` | d18c6bb1ad86b0256292316da337c783f428d5112f9b7d6d3675485054bae766 | 1065 | 4-way match |
| S16 | `zr1/exterior/27CHCOZR_CON_Studio_f04.psb` | a8afdcdc84c231eb48602e2bde313cbaeb85b798b5f4e414976e6f1c31b450e9 | 1131 | 4-way match |
| S17 | `zr1/exterior/27CHCOZR_COU_Studio_f02.psb` | 4018247080d4fd64a3e70f61dd88eeb8b9db986068a441db5f6c357036ac7ee8 | 1082 | 4-way match |
| S18 | `zr1/exterior/27CHCOZR_COU_Studio_f04.psb` | f43aa7380520e04d674a426812c3f7470beee9552793fac01cd3ba0c16575a0d | 1145 | 4-way match |
| S19 | `zr1x/exterior/27CHCOZR_X_CON_Studio_f02.psb` | 333c0b08109d90c0904f8f98ae1d892274a5cedddc5b8726ec9aa4db8511eb4b | 1054 | 4-way match |
| S20 | `zr1x/exterior/27CHCOZR_X_CON_Studio_f04.psb` | f7d3165ae86979d50f69658e047bc2d3be05005192509aac97c6dff6b1f87714 | 1098 | 4-way match |
| S21 | `zr1x/exterior/27CHCOZR_X_COU_Studio_f02.psb` | cbc0e678ff44087fb02f3722d783c425653708bdb9ada99a207d15a50a5f2de7 | 1055 | 4-way match |
| S22 | `zr1x/exterior/27CHCOZR_X_COU_Studio_f04.psb` | 5006066de88b88cb931e272a3d8bd586fa1a2bd4474908c0473748b1581f8a7c | 1112 | 4-way match |

## Layer paths and native stacking inventory

Entries below are **parent path #ID @ root index : child-name#ID**. Child lists retain native top-to-bottom order (zero-based sibling index is the list position); duplicate parent names are distinguished by ID. Each child’s full path is `parent / child-name`. `{P}` compresses an exact ten-paint run only; following IDs correspond in order to GBA, G8G, GKZ, GPH, G26, GBK, G4Z, GKA, GTR, GEC (the native order). This is not a wildcard promise. `U` marks source availability; `R` marks independent renderer work. Every name not explicitly linked to a model-owned RPO in that model’s table is **unmapped**. A paint token maps the paint only, not the S-code component geometry. Stack shorthand: F=above every spoiler, S=within the spoiler-root interval, B=below every spoiler; body+=above the paint-body root, body-=below it, body==that root. Every top-level group is accounted for, including empty/inert and cabin groups. Native existence does not prove nonempty alpha, correct finish, legal configuration or render equivalence.

<details>
<summary>S01 — Grand Sport X coupe view 01 (derived candidate)</summary>

PSB: **V/27vette-grand-sport-X-asset-proof copy.psb**. Body-paint root index 73; spoiler root indices 66, 67, 68. All subsequent cells are derived-source candidates, not native GSX qualification.

<a id="s01-paint"></a>

**Paint — U†; inherited ten-paint base**

| Parent path / ID / root index | Exact paint-bearing peers (each maps only its paint token) | Native placement |
| --- | --- | --- |
| `Molding` #72 @11 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Ground_Effects` #97 @15 | 40 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Front_Fascia_HP1` #1745 @17 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Front_Fascia` #146 @18 | 11 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Mirror_Cap` #305 @26 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `B_Pillars` #335 @31 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Rear_Fascia` #427 @40 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Roof` #442 @41 | 40 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Spoiler` #1515 @66 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | S/body+ |
| `Base` #1593 @73 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body= |
| `Mirror_Cap` #1610 @75 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body- |

<a id="s01-foundation"></a>

**Trim and body foundation**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Base` #1428 @60 | `S0507&3LT`#1430; `S0507&2LT`#1431; `S0507&1LT`#1432 | Configuration/trim candidates | F/body+ |
| `Base` #1593 @73 | `GBA`#1595; `G8G`#1596; `GKZ`#1597; `GPH`#1598; `G26`#1599; `GBK`#1600; `G4Z`#1601; `GKA`#1602; `GTR`#1603; `GEC`#1604; `1YE07`#1605 | Configuration/trim candidates | B/body= |

<a id="s01-rear"></a>

**Rear spoiler / source-off-spoiler state**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Spoiler` #1515 @66 | `T0F`#1517; `S0268`#1518; `S0267&{P}` IDs [1519, 1520, 1521, 1522, 1523, 1524, 1525, 1526, 1527, 1528]; `SIG`#1529 | SIG; rest unmapped | S/body+ |
| `Spoiler` #1533 @67 | `5V5`#1535 | Unmapped | S/body+ |
| `Spoiler` #1539 @68 | `5ZV`#1541 | 5ZV; rest unmapped | S/body+ |

Source-off-spoiler state: hide every `Spoiler` parent listed here; this is a visibility recipe, **not a catalog option ID**. No legal no-spoiler configuration is established by this operation.

<a id="s01-aero"></a>

**Front/side/hood/fascia aero candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Ground_Effects` #69 @10 | `RAU`#71 | Unmapped | F/body+ |
| `Front_Fascia` #85 @12 | `S0274`#87; `S0273`#88 | Unmapped | F/body+ |
| `Front_Fascia` #92 @14 | `S0227`#94; `S0224`#95; `S0221`#96 | Unmapped | F/body+ |
| `Ground_Effects` #97 @15 | `S0396`#99; `S0395`#100; `S0368`#101; `S0367`#102; `S0258&{P}` IDs [103, 104, 105, 106, 107, 108, 109, 110, 111, 112]; `S0872&{P}` IDs [113, 114, 115, 116, 117, 118, 119, 120, 121, 122]; `S0873&{P}` IDs [123, 124, 125, 126, 127, 128, 129, 130, 131, 132]; `S0278&{P}` IDs [133, 134, 135, 136, 137, 138, 139, 140, 141, 142] | Unmapped | F/body+ |
| `Front_Fascia_HP1` #1745 @17 | `S0220&{P}` IDs [1744, 1743, 1742, 1741, 1740, 1739, 1738, 1737, 1736, 1735] | Unmapped | F/body+ |
| `Front_Fascia` #146 @18 | `S0220&GBA`#148; `S0220&G8G`#149; `S0220&GKZ`#150; `S0220&GPH`#151; `S0220&G26`#152; `S0220&GBK`#153; `S0220&G4Z`#154; `S0220&GKA`#155; `S0220&GTR`#156; `S0220&GEC`#1733; `S0220&GEC`#157 | Unmapped | F/body+ |
| `Ground_Effects` #300 @25 | `S0366`#302; `S0365`#303; `S0237`#304 | Unmapped | F/body+ |
| `Rear_Fascia` #427 @40 | `S0204`#429; `S0203&{P}` IDs [430, 431, 432, 433, 434, 435, 436, 437, 438, 439] | Unmapped | F/body+ |

<a id="s01-graphics"></a>

**Stripes / decals / color candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Decals` #4 @1 | `S0889`#6; `S0899`#7; `S0898`#8; `S0897`#9; `S0896`#10 | Unmapped | F/body+ |
| `Decals` #20 @3 | `S0891`#22 | Unmapped | F/body+ |
| `Decals` #27 @5 | `S0837_F`#29; `S0855_F`#30; `S0302_F`#31; `S0330_F`#32; `S0325_F`#33; `S0320_F`#34; `S0315_F`#35; `S0307_F`#36; `S0860_F`#37; `S0875_F`#38; `S0880_F`#39; `S0890_F`#40; `S0893_F`#41 | Unmapped | F/body+ |
| `Stripes` #42 @6 | `S0369_F`#44 | Unmapped | F/body+ |
| `Decals` #45 @7 | `S0362_F`#47; `S0349_F`#48; `S0342_F`#49; `S0314_F`#50; `S0306_F`#51; `DZX`#52; `DZV`#53; `DZU`#54; `S0379`#55; `VPO`#56; `17A`#57; `20A`#58; `55A`#59; `75A`#60; `97A`#61; `DX4`#62 | 17A, 20A, 55A, 75A, 97A, DX4, DZU, DZV, DZX, VPO; rest unmapped | F/body+ |
| `Decals` #353 @34 | `S0866`#355; `S0858`#356; `S0361`#357; `S0348`#358; `S0341`#359; `S0334`#360; `S0876`#361; `S0313`#362 | Unmapped | F/body+ |
| `Decals` #366 @35 | `S0332`#368; `S0327`#369; `S0322`#370; `S0317`#371; `S0304`#372; `S0303`#373; `S0881`#374; `S0894`#375; `S0861`#376; `S0308`#377 | Unmapped | F/body+ |
| `Decals` #421 @39 | `S0892`#423 | Unmapped | F/body+ |
| `Decals` #1490 @64 | `S0877`#1492; `S0874`#1493; `S0363`#1494; `S0358`#1495; `S0344`#1496; `S0338`#1497; `S0857`#1498; `S0319`#1499 | Unmapped | F/body+ |
| `Decals` #1503 @65 | `S0333`#1505; `S0328`#1506; `S0323`#1507; `S0318`#1508; `S0310`#1509; `S0309`#1510; `S0311`#1511 | Unmapped | F/body+ |
| `Decals` #1560 @71 | `S0860_B`#1562; `S0875_B`#1563; `S0890_B`#1564; `S0893_B`#1565; `S0880_B`#1566 | Unmapped | B/body+ |
| `Decals` #1571 @72 | `S0882`#1576; `S0838`#1577; `S0862`#1578; `S0895`#1579; `S0360`#1580; `S0347`#1581; `S0340`#1582; `S0329`#1583; `S0312`#1584; `S0331`#1585; `S0326`#1586; `S0321`#1587; `S0316`#1588; `S0301`#1589; `S0300`#1590; `S0859`#1591; `S0305`#1592 | Unmapped | B/body+ |

<a id="s01-glass"></a>

**Glass and window candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Windows` #332 @30 | `S0105`#334 | Unmapped | F/body+ |
| `Windows` #347 @32 | `S0101_L`#349 | Unmapped | F/body+ |
| `Windows` #415 @38 | `S0108`#417 | Unmapped | F/body+ |
| `Windows` #1483 @62 | `S0122`#1485; `S0104`#1486 | Unmapped | F/body+ |
| `Defroster` #1487 @63 | `S0107`#1489 | Unmapped | F/body+ |
| `Windows` #1606 @74 | `S0101_R`#1609 | Unmapped | B/body- |

<a id="s01-other"></a>

**Other exterior option-driven and fixed groups**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Tow_Hooks` #1 @0 | No native children | Unmapped | F/body+ |
| `Badges_nose` #11 @2 | `RIN`#13; `EYK_F`#14; `EYT_F`#15; `SFZ_F`#17; `R88_F`#19 | EYK, EYT, R88, RIN, SFZ; rest unmapped | F/body+ |
| `gs_LPO_Badges` #23 @4 | `S0374`#25; `S0399`#26 | Unmapped | F/body+ |
| `Tail_Lamps` #63 @8 | `S0200`#65 | Unmapped | F/body+ |
| `Headlamps` #66 @9 | `T4L`#68 | T4L; rest unmapped | F/body+ |
| `Molding` #72 @11 | `S0211&{P}` IDs [74, 75, 76, 77, 78, 79, 80, 81, 82, 83]; `S0209`#84 | Unmapped | F/body+ |
| `gsx-Badges` #89 @13 | `eyk`#1732; `eyt`#1546 | EYK, EYT; rest unmapped | F/body+ |
| `Grille` #143 @16 | `VWE`#145 | VWE; rest unmapped | F/body+ |
| `Wheels` #158 @19 | `S0816_RL`#160; `S0820_RL`#161; `S0815_RL`#162; `S0810_RL`#163; `S0466_RL`#164; `S0455_RL`#165; `S0443_RL`#166; `S0441_RL`#167; `S0465_RL`#168; `S0462_RL`#169; `S0442_RL`#170; `S0453_RL`#171; `S0452_RL`#172; `S0447_RL`#173; `S0446_RL`#174; `S0439_RL`#175; `S0440_RL`#176; `S0451_RL`#177; `S0450_RL`#178; `S0449_RL`#179; `S0448_RL`#180; `S0433_RL`#181; `S0434_RL`#182; `S0431_RL`#183; `S0432_RL`#184; `S0454_RL`#185; `S0427_RL`#186; `S0428_RL`#187; `S0426_RL`#188; `S0425_RL`#189; `S0476_RL`#190; `S0497_RL`#191; `S0471_RL`#192; `S0397_RL`#193; `S0398_RL`#194; `S0232_RL`#195 | Unmapped | F/body+ |
| `Wheel_Caps` #196 @20 | `S0383_RL`#198; `S0264_RL`#199; `S0419_RL`#200; `S0418_RL`#201; `S0416_RL`#202; `S0415_RL`#203; `S0405_RL`#204; `S0234_RL`#205; `S0202_RL`#206; `S0251_RL`#207; `S0824_RL`#208; `S0825_RL`#209; `S0826_RL`#210; `S0828_RL`#211; `S0827_RL`#212 | Unmapped | F/body+ |
| `Brakes` #213 @21 | `S0299_RL`#215; `S0381_RL`#216; `S0292_RL`#217; `S0290_RL`#218; `S0289_RL`#219; `S0293_RL`#220; `S0288_RL`#221; `S0296_RL`#222; `S0295_RL`#223; `S0294_RL`#224; `S0291_RL`#225; `J57_RL`#226; `J56_RL`#227; `JX6_RL`#228 | J57; rest unmapped | F/body+ |
| `Wheels` #229 @22 | `S0816_FL`#231; `S0820_FL`#232; `S0815_FL`#233; `S0426_FL`#234; `S0427_FL`#235; `S0428_FL`#236; `S0425_FL`#237; `S0810_FL`#238; `S0476_FL`#239; `S0497_FL`#240; `S0466_FL`#241; `S0455_FL`#242; `S0442_FL`#243; `S0441_FL`#244; `S0465_FL`#245; `S0462_FL`#246; `S0443_FL`#247; `S0453_FL`#248; `S0452_FL`#249; `S0447_FL`#250; `S0446_FL`#251; `S0439_FL`#252; `S0440_FL`#253; `S0451_FL`#254; `S0450_FL`#255; `S0449_FL`#256; `S0448_FL`#257; `S0433_FL`#258; `S0434_FL`#259; `S0431_FL`#260; `S0432_FL`#261; `S0454_FL`#262; `S0471_FL`#263; `S0397_FL`#264; `S0398_FL`#265; `S0232_FL`#266 | Unmapped | F/body+ |
| `Wheel_Caps` #267 @23 | `S0234_FL`#269; `S0202_FL`#270; `S0251_FL`#271; `S0824_FL`#272; `S0825_FL`#273; `S0826_FL`#274; `S0828_FL`#275; `S0827_FL`#276; `S0264_FL`#277; `S0383_FL`#278; `S0419_FL`#279; `S0418_FL`#280; `S0416_FL`#281; `S0415_FL`#282; `S0405_FL`#283 | Unmapped | F/body+ |
| `Brakes` #284 @24 | `S0291_FL`#286; `S0290_FL`#287; `S0299_FL`#288; `S0381_FL`#289; `S0292_FL`#290; `S0289_FL`#291; `S0288_FL`#292; `S0296_FL`#293; `S0295_FL`#294; `S0294_FL`#295; `S0293_FL`#296; `J57_FL`#297; `J56_FL`#298; `JX6_FL`#299 | J57; rest unmapped | F/body+ |
| `Mirror_Cap` #305 @26 | `S0102_L&{P}` IDs [307, 308, 309, 310, 311, 312, 313, 314, 315, 316] | Unmapped | F/body+ |
| `Mirror_Cap` #319 @27 | `5JR_L`#321 | 5JR; rest unmapped | F/body+ |
| `Mirror_Cap` #325 @28 | `DRG_L`#327 | DRG; rest unmapped | F/body+ |
| `Mirrors` #328 @29 | `DYX_L`#330; `DWK_L`#331 | DWK, DYX; rest unmapped | F/body+ |
| `B_Pillars` #335 @31 | `S0212&{P}` IDs [337, 338, 339, 340, 341, 342, 343, 344, 345, 346] | Unmapped | F/body+ |
| `Primer` #350 @33 | `S0115`#352 | Unmapped | F/body+ |
| `Doors` #378 @36 | `S0559&HTE`#380; `S0559&HTT`#381; `S0559&HVV`#382; `S0559&HU1`#383; `S0559&HMO`#384; `S0559&HU9`#385; `S0559&HZB`#386; `S0559&HVT`#387; `S0559&HUA`#388; `S0559&HU2`#389; `S0559&HUU`#390; `S0559&HZP`#391; `S0559&HUE`#392; `S0559&HTG`#393; `S0559&HZN`#394; `S0559&HUF`#395; `S0559&HU0`#396; `S0559&HXO`#397; `S0559&HNK`#398; `S0559&HUW`#399; `S0559&HUX`#400; `S0559&HVZ`#401; `S0559&H8T`#402; `S0559&HUB`#403; `S0559&HUC`#404; `S0559&EPX`#405; `S0559&EJH`#406; `S0559&HAG`#407; `S0559&EL9`#408 | Unmapped | F/body+ |
| `Splashguards` #412 @37 | `S0390`#414 | Unmapped | F/body+ |
| `Roof` #442 @41 | `SBT`#444; `S0243&{P}` IDs [445, 446, 447, 448, 449, 450, 451, 452, 453, 454]; `C2Z&{P}` IDs [455, 456, 457, 458, 459, 460, 461, 462, 463, 464]; `CF7&{P}` IDs [465, 466, 467, 468, 469, 470, 471, 472, 473, 474]; `CF8&{P}` IDs [475, 476, 477, 478, 479, 480, 481, 482, 483, 484]; `CC3`#485; `S0506`#486; `UG1&HUV`#487; `UG1&HU7`#488; `UG1&HUL`#489; `UG1&HUR`#490; `UG1&HUK`#491; `UG1&HU6`#492; `UG1&HUN`#493; `UG1&HTP`#494; `UG1&H1Y`#495; `UG1&HTE`#496; `UG1&HTT`#497; `UG1&HVV`#498; `UG1&HU1`#499; `UG1&HMO`#500; `UG1&HU9`#501; `UG1&HZB`#502; `UG1&HVT`#503; `UG1&HUA`#504; `UG1&HU2`#505; `UG1&HUU`#506; `UG1&HZP`#507; `UG1&HUE`#508; `UG1&HTG`#509; `UG1&HZN`#510; `UG1&HUF`#511; `UG1&HU0`#512; `UG1&HXO`#513; `UG1&HNK`#514; `UG1&HUW`#515; `UG1&HUX`#516; `UG1&HVZ`#517; `UG1&H8T`#518; `UG1&HUB`#519; `UG1&HUC`#520; `UG1&EPX`#521; `UG1&EJH`#522; `UG1&HAG`#523; `UG1&EL9`#524; `UG1&HTA`#525; `UG1&HTM`#526; `UG1&HTQ`#527; `UG1&HTN`#528 | C2Z, CC3, CF7, CF8, SBT, UG1; rest unmapped | F/body+ |
| `Badges` #1192 @54 | `S0508`#1194; `BV4`#1195 | BV4; rest unmapped | F/body+ |
| `Engine` #1547 @69 | `LS6`#1550 | LS6; rest unmapped | B/body+ |
| `Exhaust` #1551 @70 | `S0229`#1553; `WUB`#1554; `S0865`#1555 | WUB; rest unmapped | B/body+ |
| `Mirror_Cap` #1610 @75 | `S0102_R&{P}` IDs [1612, 1613, 1614, 1615, 1616, 1617, 1618, 1619, 1620, 1621]; `5JR_R`#1622 | 5JR; rest unmapped | B/body- |
| `Mirrors` #1623 @76 | `UFT_R`#1625 | UFT; rest unmapped | B/body- |
| `Mirror_Cap` #1626 @77 | `DRG_R`#1628 | DRG; rest unmapped | B/body- |
| `Mirrors` #1629 @78 | `DYX_R`#1631; `DWK_R`#1632 | DWK, DYX; rest unmapped | B/body- |
| `Wheel_Caps` #1641 @79 | `S0251_RR`#1643 | Unmapped | B/body- |
| `Wheels` #1648 @80 | `S0810_FR`#1650; `S0476_FR`#1651; `S0497_FR`#1652; `S0466_FR`#1653; `S0455_FR`#1654; `S0443_FR`#1655; `S0442_FR`#1656; `S0441_FR`#1657; `S0465_FR`#1658; `S0462_FR`#1659; `S0453_FR`#1660; `S0452_FR`#1661; `S0447_FR`#1662; `S0446_FR`#1663; `S0471_FR`#1664; `S0439_FR`#1665; `S0440_FR`#1666; `S0451_FR`#1667; `S0450_FR`#1668; `S0449_FR`#1669; `S0448_FR`#1670; `S0433_FR`#1671; `S0434_FR`#1672; `S0431_FR`#1673; `S0432_FR`#1674; `S0454_FR`#1675; `S0397_FR`#1676; `S0398_FR`#1677; `S0232_FR`#1678 | Unmapped | B/body- |
| `Wheel_Caps` #1679 @81 | `S0251_FR`#1682 | Unmapped | B/body- |
| `Shadow` #1688 @82 | `S0902`#1690 | Unmapped | B/body- |
| `Background` #1691 @83 | `S0100`#1693 | Unmapped | B/body- |

Cabin/trim-dependent groups visible through glass (separate interior scenes are outside this audit): `Stitching` #529 @42 (13 children); `Steering_Wheel` #550 @43 (37 children); `Interior_Kit` #630 @44 (1 children); `Interior` #633 @45 (26 children); `Interior_Kit` #689 @46 (20 children); `Interior` #732 @47 (29 children); `Interior_Kit` #763 @48 (40 children); `Stitching` #844 @49 (38 children); `Seat_Belts` #884 @50 (20 children); `Seats_Front` #906 @51 (167 children); `Floors` #1076 @52 (17 children); `Cluster` #1115 @53 (75 children); `Stitching` #1200 @55 (3 children); `IP` #1205 @56 (1 children); `Int` #1208 @57 (45 children); `Int` #1255 @58 (43 children); `Speakers` #1300 @59 (126 children); `Int-Headliner-Effects` #1435 @61 (46 children); `Steering_Wheel` #1694 @84 (15 children); `Console` #1723 @85 (3 children). Their seat/material/trim state must be recaptured for lower trims; no upper-trim interior is authorized as a substitute.

</details>

<details>
<summary>S02 — Grand Sport convertible view 01</summary>

PSB: **V/grandsport/e.convertible.exterior.01.psb**. Body-paint root index 94; spoiler root indices 80, 82, 84.

<a id="s02-paint"></a>

**Paint — U; all ten base paints**

| Parent path / ID / root index | Exact paint-bearing peers (each maps only its paint token) | Native placement |
| --- | --- | --- |
| `Enclosure_Rear` #19 @5 | 8 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Molding` #88 @15 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Ground_Effects` #113 @19 | 40 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Front_Fascia` #162 @21 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Mirror_Cap` #321 @29 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `B_Pillars` #352 @36 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Rear_Fascia` #438 @47 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Tailgate` #453 @49 | 20 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Roof` #477 @50 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Spoiler` #1528 @80 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | S/body+ |
| `Tailgate` #1598 @93 | 20 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Base` #1623 @94 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body= |
| `Mirror_Cap` #1640 @96 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body- |

<a id="s02-foundation"></a>

**Trim and body foundation**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Base` #1440 @70 | `S0507&3LT`#1442; `S0507&2LT`#1443; `S0507&1LT`#1444 | Configuration/trim candidates | F/body+ |
| `Base` #1623 @94 | `GBA`#1625; `G8G`#1626; `GKZ`#1627; `GPH`#1628; `G26`#1629; `GBK`#1630; `G4Z`#1631; `GKA`#1632; `GTR`#1633; `GEC`#1634; `1YE67`#1635 | Configuration/trim candidates | B/body= |

<a id="s02-rear"></a>

**Rear spoiler / source-off-spoiler state**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Spoiler` #1528 @80 | `T0F`#1530; `S0268`#1531; `S0267&{P}` IDs [1532, 1533, 1534, 1535, 1536, 1537, 1538, 1539, 1540, 1541]; `SIG`#1542 | SIG, T0F; rest unmapped | S/body+ |
| `Spoiler` #1546 @82 | `5V5`#1548 | Unmapped | S/body+ |
| `Spoiler` #1552 @84 | `5ZV`#1554 | 5ZV; rest unmapped | S/body+ |

Source-off-spoiler state: hide every `Spoiler` parent listed here; this is a visibility recipe, **not a catalog option ID**. No legal no-spoiler configuration is established by this operation.

<a id="s02-aero"></a>

**Front/side/hood/fascia aero candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Ground_Effects` #85 @14 | `RAU`#87 | Unmapped | F/body+ |
| `Front_Fascia` #101 @16 | `S0274`#103; `S0273`#104 | Unmapped | F/body+ |
| `Front_Fascia` #108 @18 | `S0227`#110; `S0224`#111; `S0221`#112 | Unmapped | F/body+ |
| `Ground_Effects` #113 @19 | `S0396`#115; `S0395`#116; `S0368`#117; `S0367`#118; `S0258&{P}` IDs [119, 120, 121, 122, 123, 124, 125, 126, 127, 128]; `S0872&{P}` IDs [129, 130, 131, 132, 133, 134, 135, 136, 137, 138]; `S0873&{P}` IDs [139, 140, 141, 142, 143, 144, 145, 146, 147, 148]; `S0278&{P}` IDs [149, 150, 151, 152, 153, 154, 155, 156, 157, 158] | Unmapped | F/body+ |
| `Front_Fascia` #162 @21 | `S0220&{P}` IDs [164, 165, 166, 167, 168, 169, 170, 171, 172, 173] | Unmapped | F/body+ |
| `Ground_Effects` #316 @28 | `S0366`#318; `S0365`#319; `S0237`#320 | Unmapped | F/body+ |
| `Rear_Fascia` #438 @47 | `S0204`#440; `S0203&{P}` IDs [441, 442, 443, 444, 445, 446, 447, 448, 449, 450] | Unmapped | F/body+ |

<a id="s02-graphics"></a>

**Stripes / decals / color candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Stripes` #4 @1 | No native children | Unmapped | F/body+ |
| `Decals` #6 @2 | `S0889`#8; `S0899`#9; `S0898`#10; `S0897`#11; `S0896`#12; `S0494`#13 | Unmapped | F/body+ |
| `Decals` #36 @7 | `S0891`#38 | Unmapped | F/body+ |
| `Decals` #43 @9 | `S0837_F`#45; `S0855_F`#46; `S0302_F`#47; `S0330_F`#48; `S0325_F`#49; `S0320_F`#50; `S0315_F`#51; `S0307_F`#52; `S0860_F`#53; `S0875_F`#54; `S0880_F`#55; `S0890_F`#56; `S0893_F`#57 | Unmapped | F/body+ |
| `Stripes` #58 @10 | `S0369_F`#60 | Unmapped | F/body+ |
| `Decals` #61 @11 | `S0362_F`#63; `S0349_F`#64; `S0342_F`#65; `S0314_F`#66; `S0306_F`#67; `DZX`#68; `DZV`#69; `DZU`#70; `S0379`#71; `VPO`#72; `17A`#73; `20A`#74; `55A`#75; `75A`#76; `97A`#77; `DX4`#78 | 17A, 20A, 55A, 75A, 97A, DX4, DZU, DZV, DZX, VPO; rest unmapped | F/body+ |
| `Decals` #371 @39 | `S0866`#373; `S0858`#374; `S0361`#375; `S0348`#376; `S0341`#377; `S0334`#378; `S0876`#379; `S0313`#380 | Unmapped | F/body+ |
| `Decals` #384 @41 | `S0332`#386; `S0327`#387; `S0322`#388; `S0317`#389; `S0304`#390; `S0303`#391; `S0881`#392; `S0894`#393; `S0861`#394; `S0308`#395 | Unmapped | F/body+ |
| `Decals` #1504 @76 | `S0874`#1506; `S0363`#1507; `S0358`#1508; `S0344`#1509; `S0338`#1510; `S0857`#1511; `S0319`#1512 | Unmapped | F/body+ |
| `Decals` #1516 @78 | `S0333`#1518; `S0328`#1519; `S0323`#1520; `S0318`#1521; `S0310`#1522; `S0309`#1523; `S0311`#1524 | Unmapped | F/body+ |
| `Decals` #1573 @90 | `S0855_B`#1575; `S0837_B`#1576; `S0860_B`#1577; `S0875_B`#1578; `S0890_B`#1579; `S0893_B`#1580; `S0880_B`#1581; `S0330_B`#1582; `S0320_B`#1583; `S0315_B`#1584; `S0307_B`#1585; `S0325_B`#1586 | Unmapped | B/body+ |
| `Stripes` #1587 @91 | `S0369_B`#1589 | Unmapped | B/body+ |
| `Decals` #1590 @92 | `S0362_B`#1592; `S0349_B`#1593; `S0342_B`#1594; `S0314_B`#1595; `S0306_B`#1596; `S0302_B`#1597 | Unmapped | B/body+ |

<a id="s02-glass"></a>

**Glass and window candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Windows` #349 @35 | `S0105`#351 | Unmapped | F/body+ |
| `Windows` #365 @37 | `S0101_L`#367 | Unmapped | F/body+ |
| `Windows` #1495 @73 | `S0104`#1497 | Unmapped | F/body+ |
| `Defroster` #1498 @74 | `S0107`#1500 | Unmapped | F/body+ |
| `Windows` #1636 @95 | `S0101_B`#1638; `S0101_R`#1639 | Unmapped | B/body- |

<a id="s02-other"></a>

**Other exterior option-driven and fixed groups**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Tow_Hooks` #1 @0 | No native children | Unmapped | F/body+ |
| `Tailgate` #14 @3 | `S0475`#16 | Unmapped | F/body+ |
| `Engine` #17 @4 | No native children | Unmapped | F/body+ |
| `Enclosure_Rear` #19 @5 | `S0127&GBA`#21; `S0127&G8G`#22; `S0127&GPH`#23; `S0127&G26`#24; `S0127&GBK`#25; `S0127&G4Z`#26; `S0127&GKA`#27; `S0127&GTR`#28 | Unmapped | F/body+ |
| `Badges` #29 @6 | `EYK_F`#31; `EYT_F`#32; `SFZ_F`#33; `S0279`#34; `R88_F`#35 | EYK, EYT, R88, SFZ; rest unmapped | F/body+ |
| `Badges` #39 @8 | `S0374`#41; `S0399`#42 | Unmapped | F/body+ |
| `Tail_Lamps` #79 @12 | `S0200`#81 | Unmapped | F/body+ |
| `Headlamps` #82 @13 | `T4L`#84 | T4L; rest unmapped | F/body+ |
| `Molding` #88 @15 | `S0211&{P}` IDs [90, 91, 92, 93, 94, 95, 96, 97, 98, 99]; `S0209`#100 | Unmapped | F/body+ |
| `Badges` #105 @17 | `S0271`#107 | Unmapped | F/body+ |
| `Grille` #159 @20 | `VWE`#161 | VWE; rest unmapped | F/body+ |
| `Wheels` #174 @22 | `S0816_RL`#176; `S0820_RL`#177; `S0815_RL`#178; `S0810_RL`#179; `S0466_RL`#180; `S0455_RL`#181; `S0443_RL`#182; `S0441_RL`#183; `S0465_RL`#184; `S0462_RL`#185; `S0442_RL`#186; `S0453_RL`#187; `S0452_RL`#188; `S0447_RL`#189; `S0446_RL`#190; `S0439_RL`#191; `S0440_RL`#192; `S0451_RL`#193; `S0450_RL`#194; `S0449_RL`#195; `S0448_RL`#196; `S0433_RL`#197; `S0434_RL`#198; `S0431_RL`#199; `S0432_RL`#200; `S0454_RL`#201; `S0427_RL`#202; `S0428_RL`#203; `S0426_RL`#204; `S0425_RL`#205; `S0476_RL`#206; `S0497_RL`#207; `S0471_RL`#208; `S0397_RL`#209; `S0398_RL`#210; `S0232_RL`#211 | Unmapped | F/body+ |
| `Wheel_Caps` #212 @23 | `S0383_RL`#214; `S0264_RL`#215; `S0419_RL`#216; `S0418_RL`#217; `S0416_RL`#218; `S0415_RL`#219; `S0405_RL`#220; `S0234_RL`#221; `S0202_RL`#222; `S0251_RL`#223; `S0824_RL`#224; `S0825_RL`#225; `S0826_RL`#226; `S0828_RL`#227; `S0827_RL`#228 | Unmapped | F/body+ |
| `Brakes` #229 @24 | `S0299_RL`#231; `S0381_RL`#232; `S0292_RL`#233; `S0290_RL`#234; `S0289_RL`#235; `S0293_RL`#236; `S0288_RL`#237; `S0296_RL`#238; `S0295_RL`#239; `S0294_RL`#240; `S0291_RL`#241; `J57_RL`#242; `J56_RL`#243; `JX6_RL`#244 | J56, J57, JX6; rest unmapped | F/body+ |
| `Wheels` #245 @25 | `S0816_FL`#247; `S0820_FL`#248; `S0815_FL`#249; `S0426_FL`#250; `S0427_FL`#251; `S0428_FL`#252; `S0425_FL`#253; `S0810_FL`#254; `S0476_FL`#255; `S0497_FL`#256; `S0466_FL`#257; `S0455_FL`#258; `S0442_FL`#259; `S0441_FL`#260; `S0465_FL`#261; `S0462_FL`#262; `S0443_FL`#263; `S0453_FL`#264; `S0452_FL`#265; `S0447_FL`#266; `S0446_FL`#267; `S0439_FL`#268; `S0440_FL`#269; `S0451_FL`#270; `S0450_FL`#271; `S0449_FL`#272; `S0448_FL`#273; `S0433_FL`#274; `S0434_FL`#275; `S0431_FL`#276; `S0432_FL`#277; `S0454_FL`#278; `S0471_FL`#279; `S0397_FL`#280; `S0398_FL`#281; `S0232_FL`#282 | Unmapped | F/body+ |
| `Wheel_Caps` #283 @26 | `S0234_FL`#285; `S0202_FL`#286; `S0251_FL`#287; `S0824_FL`#288; `S0825_FL`#289; `S0826_FL`#290; `S0828_FL`#291; `S0827_FL`#292; `S0264_FL`#293; `S0383_FL`#294; `S0419_FL`#295; `S0418_FL`#296; `S0416_FL`#297; `S0415_FL`#298; `S0405_FL`#299 | Unmapped | F/body+ |
| `Brakes` #300 @27 | `S0291_FL`#302; `S0290_FL`#303; `S0299_FL`#304; `S0381_FL`#305; `S0292_FL`#306; `S0289_FL`#307; `S0288_FL`#308; `S0296_FL`#309; `S0295_FL`#310; `S0294_FL`#311; `S0293_FL`#312; `J57_FL`#313; `J56_FL`#314; `JX6_FL`#315 | J56, J57, JX6; rest unmapped | F/body+ |
| `Mirror_Cap` #321 @29 | `S0102_L&{P}` IDs [323, 324, 325, 326, 327, 328, 329, 330, 331, 332] | Unmapped | F/body+ |
| `Mirrors` #333 @30 | `VA5`#335 | Unmapped | F/body+ |
| `Mirror_Cap` #336 @31 | `5JR_L`#338 | 5JR; rest unmapped | F/body+ |
| `Mirrors` #339 @32 | `UFT_L`#341 | UFT; rest unmapped | F/body+ |
| `Mirror_Cap` #342 @33 | `DRG_L`#344 | DRG; rest unmapped | F/body+ |
| `Mirrors` #345 @34 | `DYX_L`#347; `DWK_L`#348 | DWK, DYX; rest unmapped | F/body+ |
| `B_Pillars` #352 @36 | `S0213`#354; `S0212&{P}` IDs [355, 356, 357, 358, 359, 360, 361, 362, 363, 364] | Unmapped | F/body+ |
| `Primer` #368 @38 | `S0115`#370 | Unmapped | F/body+ |
| `None` #381 @40 | `S0345`#383 | Unmapped | F/body+ |
| `Doors` #396 @42 | `S0559&HTE`#398; `S0559&HTT`#399; `S0559&HVV`#400; `S0559&HU1`#401; `S0559&HMO`#402; `S0559&HU9`#403; `S0559&HZB`#404; `S0559&HVT`#405; `S0559&HUA`#406; `S0559&HU2`#407; `S0559&HUU`#408; `S0559&HZP`#409; `S0559&HUE`#410; `S0559&HTG`#411; `S0559&HZN`#412; `S0559&HUF`#413; `S0559&HU0`#414; `S0559&HXO`#415; `S0559&HNK`#416; `S0559&HUW`#417; `S0559&HUX`#418; `S0559&HVZ`#419; `S0559&H8T`#420; `S0559&HUB`#421; `S0559&HUC`#422; `S0559&EPX`#423; `S0559&EJH`#424; `S0559&HAG`#425; `S0559&EL9`#426 | Unmapped | F/body+ |
| `None` #427 @43 | `S0420`#429 | Unmapped | F/body+ |
| `Splashguards` #430 @44 | `S0390`#432 | Unmapped | F/body+ |
| `None` #433 @45 | `VSN`#435 | Unmapped | F/body+ |
| `License_Plate` #436 @46 | No native children | Unmapped | F/body+ |
| `Multimedia` #451 @48 | No native children | Unmapped | F/body+ |
| `Tailgate` #453 @49 | `S0135_L&{P}` IDs [455, 456, 457, 458, 459, 460, 461, 462, 463, 464]; `S0136_L`#465; `S0113_L`#466; `S0112_L&{P}` IDs [467, 468, 469, 470, 471, 472, 473, 474, 475, 476] | Unmapped | F/body+ |
| `Roof` #477 @50 | `S0216`#479; `CM9&{P}` IDs [480, 481, 482, 483, 484, 485, 486, 487, 488, 489]; `S0506`#490; `UG1&HUV`#491; `UG1&HU7`#492; `UG1&HUL`#493; `UG1&HUR`#494; `UG1&HUK`#495; `UG1&HU6`#496; `UG1&HUN`#497; `UG1&HTP`#498; `UG1&H1Y`#499; `UG1&HTE`#500; `UG1&HTT`#501; `UG1&HVV`#502; `UG1&HU1`#503; `UG1&HMO`#504; `UG1&HU9`#505; `UG1&HZB`#506; `UG1&HVT`#507; `UG1&HUA`#508; `UG1&HU2`#509; `UG1&HUU`#510; `UG1&HZP`#511; `UG1&HUE`#512; `UG1&HTG`#513; `UG1&HZN`#514; `UG1&HUF`#515; `UG1&HU0`#516; `UG1&HXO`#517; `UG1&HNK`#518; `UG1&HUW`#519; `UG1&HUX`#520; `UG1&HVZ`#521; `UG1&H8T`#522; `UG1&HUB`#523; `UG1&HUC`#524; `UG1&EPX`#525; `UG1&EJH`#526; `UG1&HAG`#527; `UG1&EL9`#528; `UG1&HTA`#529; `UG1&HTM`#530; `UG1&HTQ`#531; `UG1&HTN`#532 | CM9, UG1; rest unmapped | F/body+ |
| `Badges` #1203 @63 | `S0508`#1205; `CFX`#1206; `BV4`#1207; `S0500`#1208 | BV4, CFX; rest unmapped | F/body+ |
| `Radio` #1445 @71 | No native children | Unmapped | F/body+ |
| `Tailgate` #1501 @75 | `S0479`#1503 | Unmapped | F/body+ |
| `None` #1513 @77 | `S0343`#1515 | Unmapped | F/body+ |
| `None` #1525 @79 | `S0357`#1527 | Unmapped | F/body+ |
| `None` #1543 @81 | `S0119`#1545 | Unmapped | S/body+ |
| `None` #1549 @83 | `D58`#1551 | Unmapped | S/body+ |
| `Engine` #1555 @85 | `BC7`#1557 | BC7; rest unmapped | B/body+ |
| `Badges` #1558 @86 | `S0270`#1560 | Unmapped | B/body+ |
| `Engine` #1561 @87 | `LS6`#1563 | LS6; rest unmapped | B/body+ |
| `Exhaust` #1564 @88 | `S0229`#1566; `WUB`#1567; `S0865`#1568 | WUB; rest unmapped | B/body+ |
| `Tow_Hooks` #1569 @89 | `S0870`#1571; `S0871`#1572 | Unmapped | B/body+ |
| `Tailgate` #1598 @93 | `S0883`#1600; `S0135_R&{P}` IDs [1601, 1602, 1603, 1604, 1605, 1606, 1607, 1608, 1609, 1610]; `S0136_R`#1611; `S0113_R`#1612; `S0112_R&{P}` IDs [1613, 1614, 1615, 1616, 1617, 1618, 1619, 1620, 1621, 1622] | Unmapped | B/body+ |
| `Mirror_Cap` #1640 @96 | `S0102_R&{P}` IDs [1642, 1643, 1644, 1645, 1646, 1647, 1648, 1649, 1650, 1651]; `5JR_R`#1652 | 5JR; rest unmapped | B/body- |
| `Mirrors` #1653 @97 | `UFT_R`#1655 | UFT; rest unmapped | B/body- |
| `Mirror_Cap` #1656 @98 | `DRG_R`#1658 | DRG; rest unmapped | B/body- |
| `Mirrors` #1659 @99 | `DYX_R`#1661; `DWK_R`#1662 | DWK, DYX; rest unmapped | B/body- |
| `Wheels` #1663 @100 | `S0447_RR`#1665; `S0446_RR`#1666; `S0451_RR`#1667; `S0448_RR`#1668; `S0462_RR`#1669; `S0476_RR`#1670; `S0398_RR`#1671; `S0426_RR`#1672; `S0425_RR`#1673 | Unmapped | B/body- |
| `Wheel_Caps` #1674 @101 | `S0251_RR`#1676; `S0264_RR`#1677; `S0416_RR`#1678; `S0415_RR`#1679; `S0405_RR`#1680 | Unmapped | B/body- |
| `Brakes` #1681 @102 | `S0291_RR`#1683 | Unmapped | B/body- |
| `Wheels` #1684 @103 | `S0816_FR`#1686; `S0815_FR`#1687; `S0810_FR`#1688; `S0426_FR`#1689; `S0476_FR`#1690; `S0497_FR`#1691; `S0466_FR`#1692; `S0455_FR`#1693; `S0443_FR`#1694; `S0442_FR`#1695; `S0441_FR`#1696; `S0465_FR`#1697; `S0462_FR`#1698; `S0453_FR`#1699; `S0452_FR`#1700; `S0447_FR`#1701; `S0446_FR`#1702; `S0471_FR`#1703; `S0439_FR`#1704; `S0440_FR`#1705; `S0451_FR`#1706; `S0450_FR`#1707; `S0449_FR`#1708; `S0448_FR`#1709; `S0433_FR`#1710; `S0434_FR`#1711; `S0431_FR`#1712; `S0432_FR`#1713; `S0454_FR`#1714; `S0397_FR`#1715; `S0398_FR`#1716; `S0232_FR`#1717 | Unmapped | B/body- |
| `Wheel_Caps` #1718 @104 | `S0405_FR`#1720; `S0251_FR`#1721; `S0826_FR`#1722 | Unmapped | B/body- |
| `Brakes` #1723 @105 | No native children | Unmapped | B/body- |
| `Shadow` #1725 @106 | `S0902`#1727 | Unmapped | B/body- |
| `Background` #1728 @107 | `S0100`#1730 | Unmapped | B/body- |

Cabin/trim-dependent groups visible through glass (separate interior scenes are outside this audit): `Stitching` #533 @51 (19 children); `Steering_Wheel` #554 @52 (81 children); `Interior_Kit` #637 @53 (1 children); `Interior` #640 @54 (55 children); `Interior_Kit` #697 @55 (40 children); `Interior` #739 @56 (29 children); `Interior_Kit` #770 @57 (82 children); `Stitching` #854 @58 (38 children); `Seat_Belts` #894 @59 (20 children); `Seats_Front` #916 @60 (167 children); `Floors` #1085 @61 (39 children); `Cluster` #1126 @62 (75 children); `IP` #1209 @64 (1 children); `Stitching` #1212 @65 (3 children); `IP` #1217 @66 (1 children); `Decal_Stickers` #1220 @67 (45 children); `IP` #1267 @68 (43 children); `Speakers` #1312 @69 (126 children); `Effects` #1447 @72 (46 children); `Steering_Wheel` #1731 @108 (26 children); `Console` #1759 @109 (4 children). Their seat/material/trim state must be recaptured for lower trims; no upper-trim interior is authorized as a substitute.

</details>

<details>
<summary>S03 — Grand Sport convertible view 02</summary>

PSB: **V/grandsport/e.convertible.exterior.02.psb**. Body-paint root index 91; spoiler root indices 7, 12, 14, 16.

<a id="s03-paint"></a>

**Paint — U; all ten base paints**

| Parent path / ID / root index | Exact paint-bearing peers (each maps only its paint token) | Native placement |
| --- | --- | --- |
| `Enclosure_Rear` #19 @4 | 8 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Spoiler` #64 @12 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | S/body+ |
| `Tailgate` #168 @25 | 20 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Molding` #229 @32 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Tailgate` #388 @40 | 20 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Mirror_Cap` #412 @41 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Ground_Effects` #605 @53 | 40 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Roof` #654 @55 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Front_Fascia` #719 @59 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `B_Pillars` #1612 @81 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Rear_Fascia` #1644 @87 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Base` #1665 @91 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body= |
| `Mirror_Cap` #1684 @94 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body- |

<a id="s03-foundation"></a>

**Trim and body foundation**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Base` #1557 @78 | `S0507&3LT`#1559; `S0507&2LT`#1560; `S0507&1LT`#1561 | Configuration/trim candidates | B/body+ |
| `Base` #1665 @91 | `GBA`#1667; `G8G`#1668; `GKZ`#1669; `GPH`#1670; `G26`#1671; `GBK`#1672; `G4Z`#1673; `GKA`#1674; `GTR`#1675; `GEC`#1676; `1YE67`#1677 | Configuration/trim candidates | B/body= |

<a id="s03-rear"></a>

**Rear spoiler / source-off-spoiler state**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Spoiler` #36 @7 | `SIG`#38 | SIG; rest unmapped | S/body+ |
| `Spoiler` #64 @12 | `T0F`#66; `S0268`#67; `S0267&{P}` IDs [68, 69, 70, 71, 72, 73, 74, 75, 76, 77] | T0F; rest unmapped | S/body+ |
| `Spoiler` #81 @14 | `5V5`#83 | Unmapped | S/body+ |
| `Spoiler` #87 @16 | `5ZV`#89 | 5ZV; rest unmapped | S/body+ |

Source-off-spoiler state: hide every `Spoiler` parent listed here; this is a visibility recipe, **not a catalog option ID**. No legal no-spoiler configuration is established by this operation.

<a id="s03-aero"></a>

**Front/side/hood/fascia aero candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Rear_Fascia` #223 @30 | `S0204`#225 | Unmapped | B/body+ |
| `Ground_Effects` #242 @33 | `RAU`#244; `S0366`#245; `S0365`#246; `S0237`#247 | Unmapped | B/body+ |
| `Front_Fascia` #596 @50 | No native children | Unmapped | B/body+ |
| `Front_Fascia` #601 @52 | `S0227`#603; `S0221`#604 | Unmapped | B/body+ |
| `Ground_Effects` #605 @53 | `S0396`#607; `S0395`#608; `S0368`#609; `S0367`#610; `S0258&{P}` IDs [611, 612, 613, 614, 615, 616, 617, 618, 619, 620]; `S0872&{P}` IDs [621, 622, 623, 624, 625, 626, 627, 628, 629, 630]; `S0873&{P}` IDs [631, 632, 633, 634, 635, 636, 637, 638, 639, 640]; `S0278&{P}` IDs [641, 642, 643, 644, 645, 646, 647, 648, 649, 650] | Unmapped | B/body+ |
| `Front_Fascia` #719 @59 | `S0220&{P}` IDs [721, 722, 723, 724, 725, 726, 727, 728, 729, 730] | Unmapped | B/body+ |
| `Rear_Fascia` #1644 @87 | `S0203&{P}` IDs [1646, 1647, 1648, 1649, 1650, 1651, 1652, 1653, 1654, 1655] | Unmapped | B/body+ |

<a id="s03-graphics"></a>

**Stripes / decals / color candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Stripes` #1 @0 | No native children | Unmapped | F/body+ |
| `Decals` #4 @1 | `S0490`#6; `S0489`#7; `S0486`#8; `S0889`#9; `S0899`#10; `S0898`#11; `S0897`#12; `S0896`#13; `S0494`#14 | Unmapped | F/body+ |
| `Decals` #29 @5 | `S0891`#31 | Unmapped | F/body+ |
| `Decals` #39 @8 | `S0876`#41; `S0874`#42; `S0363`#43; `S0358`#44; `S0344`#45; `S0338`#46; `S0857`#47; `S0319`#48 | Unmapped | S/body+ |
| `Decals` #52 @10 | `S0333`#54; `S0328`#55; `S0323`#56; `S0318`#57; `S0310`#58; `S0309`#59; `S0311`#60 | Unmapped | S/body+ |
| `Decals` #103 @18 | `S0837_F`#105; `S0855_F`#106; `S0302_F`#107; `S0330_F`#108; `S0325_F`#109; `S0320_F`#110; `S0315_F`#111; `S0307_F`#112; `S0860_F`#113; `S0875_F`#114; `S0880_F`#115; `S0890_F`#116; `S0893_F`#117 | Unmapped | B/body+ |
| `Stripes` #118 @19 | `S0369_F`#120 | Unmapped | B/body+ |
| `Decals` #121 @20 | `S0362_F`#123; `S0349_F`#124; `S0342_F`#125; `S0314_F`#126; `S0306_F`#127; `DZX`#128; `DZV`#129; `DZU`#130; `S0379`#131; `VPO`#132; `17A`#133; `20A`#134; `55A`#135; `75A`#136; `97A`#137; `DX4`#138; `S0866`#139; `S0858`#140; `S0361`#141; `S0348`#142; `S0341`#143; `S0334`#144; `S0313`#145 | 17A, 20A, 55A, 75A, 97A, DX4, DZU, DZV, DZX, VPO; rest unmapped | B/body+ |
| `Decals` #149 @22 | `S0332`#151; `S0327`#152; `S0322`#153; `S0317`#154; `S0304`#155; `S0303`#156; `S0881`#157; `S0894`#158; `S0861`#159; `S0308`#160 | Unmapped | B/body+ |
| `Decals` #195 @26 | `S0855_B`#197; `S0837_B`#198; `S0860_B`#199; `S0875_B`#200; `S0890_B`#201; `S0893_B`#202; `S0880_B`#203; `S0330_B`#204; `S0320_B`#205; `S0315_B`#206; `S0307_B`#207; `S0325_B`#208 | Unmapped | B/body+ |
| `Stripes` #209 @27 | `S0369_B`#211 | Unmapped | B/body+ |
| `Decals` #212 @28 | `S0362_B`#214; `S0349_B`#215; `S0342_B`#216; `S0314_B`#217; `S0306_B`#218; `S0302_B`#219 | Unmapped | B/body+ |

<a id="s03-glass"></a>

**Glass and window candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Windows` #436 @45 | `S0101_R`#438; `S0101_B`#439 | Unmapped | B/body+ |
| `Defroster` #710 @56 | `S0107`#712 | Unmapped | B/body+ |
| `Windows` #713 @57 | `S0104`#715 | Unmapped | B/body+ |
| `Windows` #1662 @90 | `S0105`#1664 | Unmapped | B/body+ |
| `Windows` #1681 @93 | `S0101_L`#1683 | Unmapped | B/body- |

<a id="s03-other"></a>

**Other exterior option-driven and fixed groups**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Tailgate` #15 @2 | No native children | Unmapped | F/body+ |
| `Engine` #17 @3 | No native children | Unmapped | F/body+ |
| `Enclosure_Rear` #19 @4 | `S0127&GBA`#21; `S0127&G8G`#22; `S0127&GPH`#23; `S0127&G26`#24; `S0127&GBK`#25; `S0127&G4Z`#26; `S0127&GKA`#27; `S0127&GEC`#28 | Unmapped | F/body+ |
| `Badges` #32 @6 | `S0374`#34; `S0399`#35 | Unmapped | F/body+ |
| `None` #49 @9 | `S0343`#51 | Unmapped | S/body+ |
| `None` #61 @11 | `S0357`#63 | Unmapped | S/body+ |
| `None` #78 @13 | `S0119`#80 | Unmapped | S/body+ |
| `None` #84 @15 | `D58`#86 | Unmapped | S/body+ |
| `Badges` #90 @17 | `SL8`#92; `RIN`#93; `RIK`#94; `EYK_F`#95; `EYT_F`#96; `EYK_B`#97; `EYT_B`#98; `SFZ_B`#99; `S0276`#100; `S0279`#101; `R88_B`#102 | EYK, EYT, R88, RIK, RIN, SFZ, SL8; rest unmapped | B/body+ |
| `None` #146 @21 | `S0345`#148 | Unmapped | B/body+ |
| `Tailgate` #161 @23 | `S0883`#163; `S0863`#164 | Unmapped | B/body+ |
| `Tail_Lamps` #165 @24 | `S0200`#167 | Unmapped | B/body+ |
| `Tailgate` #168 @25 | `S0135_R&{P}` IDs [170, 171, 172, 173, 174, 175, 176, 177, 178, 179]; `S0136_R`#180; `S0113_R`#181; `S0112_R&{P}` IDs [182, 183, 184, 185, 186, 187, 188, 189, 190, 191]; `S0884`#192; `S0885`#193; `S0217`#194 | Unmapped | B/body+ |
| `Multimedia` #220 @29 | `S0244`#222 | Unmapped | B/body+ |
| `License_Plate` #226 @31 | `S0235`#228 | Unmapped | B/body+ |
| `Molding` #229 @32 | `S0211&{P}` IDs [231, 232, 233, 234, 235, 236, 237, 238, 239, 240]; `S0209`#241 | Unmapped | B/body+ |
| `Wheels` #248 @34 | `S0820_FR`#250; `S0815_FR`#251; `S0810_FR`#252; `S0427_FR`#253; `S0426_FR`#254; `S0428_FR`#255; `S0425_FR`#256; `S0476_FR`#257; `S0497_FR`#258; `S0466_FR`#259; `S0455_FR`#260; `S0443_FR`#261; `S0442_FR`#262; `S0441_FR`#263; `S0465_FR`#264; `S0462_FR`#265; `S0453_FR`#266; `S0452_FR`#267; `S0447_FR`#268; `S0446_FR`#269; `S0471_FR`#270; `S0439_FR`#271; `S0440_FR`#272; `S0451_FR`#273; `S0450_FR`#274; `S0449_FR`#275; `S0448_FR`#276; `S0433_FR`#277; `S0434_FR`#278; `S0431_FR`#279; `S0432_FR`#280; `S0454_FR`#281; `S0397_FR`#282; `S0398_FR`#283; `S0232_FR`#284 | Unmapped | B/body+ |
| `Wheel_Caps` #285 @35 | `S0383_FR`#287; `S0264_FR`#288; `S0419_FR`#289; `S0418_FR`#290; `S0416_FR`#291; `S0415_FR`#292; `S0405_FR`#293; `S0234_FR`#294; `S0202_FR`#295; `S0251_FR`#296; `S0824_FR`#297; `S0825_FR`#298; `S0826_FR`#299; `S0828_FR`#300; `S0827_FR`#301 | Unmapped | B/body+ |
| `Brakes` #302 @36 | `S0299_FR`#304; `S0381_FR`#305; `S0291_FR`#306; `S0290_FR`#307; `S0293_FR`#308; `S0289_FR`#309; `S0288_FR`#310; `S0296_FR`#311; `S0295_FR`#312; `S0294_FR`#313; `S0292_FR`#314; `J57_FR`#315; `J56_FR`#316; `JX6_FR`#317 | J56, J57, JX6; rest unmapped | B/body+ |
| `Wheels` #318 @37 | `S0820_RR`#320; `S0815_RR`#321; `S0427_RR`#322; `S0426_RR`#323; `S0428_RR`#324; `S0425_RR`#325; `S0810_RR`#326; `S0455_RR`#327; `S0443_RR`#328; `S0442_RR`#329; `S0441_RR`#330; `S0465_RR`#331; `S0466_RR`#332; `S0453_RR`#333; `S0452_RR`#334; `S0447_RR`#335; `S0446_RR`#336; `S0439_RR`#337; `S0440_RR`#338; `S0451_RR`#339; `S0450_RR`#340; `S0449_RR`#341; `S0448_RR`#342; `S0433_RR`#343; `S0434_RR`#344; `S0431_RR`#345; `S0432_RR`#346; `S0454_RR`#347; `S0462_RR`#348; `S0471_RR`#349; `S0476_RR`#350; `S0497_RR`#351; `S0397_RR`#352; `S0398_RR`#353; `S0232_RR`#354 | Unmapped | B/body+ |
| `Wheel_Caps` #355 @38 | `S0234_RR`#357; `S0202_RR`#358; `S0251_RR`#359; `S0383_RR`#360; `S0264_RR`#361; `S0419_RR`#362; `S0418_RR`#363; `S0416_RR`#364; `S0415_RR`#365; `S0405_RR`#366; `S0824_RR`#367; `S0825_RR`#368; `S0826_RR`#369; `S0828_RR`#370; `S0827_RR`#371 | Unmapped | B/body+ |
| `Brakes` #372 @39 | `S0381_RR`#374; `S0299_RR`#375; `S0289_RR`#376; `S0293_RR`#377; `S0292_RR`#378; `S0288_RR`#379; `S0296_RR`#380; `S0295_RR`#381; `S0294_RR`#382; `S0291_RR`#383; `S0290_RR`#384; `J56_RR`#385; `JX6_RR`#386; `J57_RR`#387 | J56, J57, JX6; rest unmapped | B/body+ |
| `Tailgate` #388 @40 | `S0135_L&{P}` IDs [390, 391, 392, 393, 394, 395, 396, 397, 398, 399]; `S0136_L`#400; `S0113_L`#401; `S0112_L&{P}` IDs [402, 403, 404, 405, 406, 407, 408, 409, 410, 411] | Unmapped | B/body+ |
| `Mirror_Cap` #412 @41 | `S0102_R&{P}` IDs [414, 415, 416, 417, 418, 419, 420, 421, 422, 423]; `5JR_R`#424 | 5JR; rest unmapped | B/body+ |
| `Mirrors` #425 @42 | `UFT_R`#427 | UFT; rest unmapped | B/body+ |
| `Mirror_Cap` #428 @43 | `DRG_R`#430 | DRG; rest unmapped | B/body+ |
| `Mirrors` #431 @44 | `VA5`#433; `DYX_R`#434; `DWK_R`#435 | DWK, DYX; rest unmapped | B/body+ |
| `Doors` #440 @46 | `S0559&HTE`#442; `S0559&HTT`#443; `S0559&HVV`#444; `S0559&HU1`#445; `S0559&HMO`#446; `S0559&HZB`#447; `S0559&HVT`#448; `S0559&HUA`#449; `S0559&HUU`#450; `S0559&HZP`#451; `S0559&HUE`#452; `S0559&HZN`#453; `S0559&HUF`#454; `S0559&HU0`#455; `S0559&HXO`#456; `S0559&HNK`#457; `S0559&HUW`#458; `S0559&HUX`#459; `S0559&H8T`#460; `S0559&HUB`#461; `S0559&HUC`#462; `S0559&EPX`#463; `S0559&EJH`#464; `S0559&HAG`#465; `S0559&EL9`#466 | Unmapped | B/body+ |
| `None` #593 @49 | `S0420`#595 | Unmapped | B/body+ |
| `Badges` #598 @51 | `S0271`#600 | Unmapped | B/body+ |
| `None` #651 @54 | `VSN`#653 | Unmapped | B/body+ |
| `Roof` #654 @55 | `S0216`#656; `CM9&{P}` IDs [657, 658, 659, 660, 661, 662, 663, 664, 665, 666]; `S0506`#667; `UG1&HUV`#668; `UG1&HU7`#669; `UG1&HUL`#670; `UG1&HUR`#671; `UG1&HUK`#672; `UG1&HU6`#673; `UG1&HUN`#674; `UG1&HTP`#675; `UG1&H1Y`#676; `UG1&HTE`#677; `UG1&HTT`#678; `UG1&HVV`#679; `UG1&HU1`#680; `UG1&HMO`#681; `UG1&HU9`#682; `UG1&HZB`#683; `UG1&HVT`#684; `UG1&HUA`#685; `UG1&HU2`#686; `UG1&HUU`#687; `UG1&HZP`#688; `UG1&HUE`#689; `UG1&HTG`#690; `UG1&HZN`#691; `UG1&HUF`#692; `UG1&HU0`#693; `UG1&HXO`#694; `UG1&HNK`#695; `UG1&HUW`#696; `UG1&HUX`#697; `UG1&HVZ`#698; `UG1&H8T`#699; `UG1&HUB`#700; `UG1&HUC`#701; `UG1&EPX`#702; `UG1&EJH`#703; `UG1&HAG`#704; `UG1&EL9`#705; `UG1&HTA`#706; `UG1&HTM`#707; `UG1&HTQ`#708; `UG1&HTN`#709 | CM9, UG1; rest unmapped | B/body+ |
| `Headlamps` #716 @58 | `T4L`#718 | T4L; rest unmapped | B/body+ |
| `Badges` #1371 @73 | `S0508`#1373; `CFX`#1374; `BV4`#1375; `S0500`#1376 | BV4, CFX; rest unmapped | B/body+ |
| `Radio` #1562 @79 | No native children | Unmapped | B/body+ |
| `B_Pillars` #1612 @81 | `S0213`#1614; `S0212&{P}` IDs [1615, 1616, 1617, 1618, 1619, 1620, 1621, 1622, 1623, 1624] | Unmapped | B/body+ |
| `Engine` #1625 @82 | No native children | Unmapped | B/body+ |
| `Badges` #1627 @83 | `S0270`#1629 | Unmapped | B/body+ |
| `Engine` #1630 @84 | `LS6`#1632 | LS6; rest unmapped | B/body+ |
| `Tow_Hooks` #1633 @85 | `S0870`#1635; `S0871`#1636 | Unmapped | B/body+ |
| `Exhaust` #1637 @86 | `S0865`#1639; `S0229`#1640; `S0867`#1641; `S0868`#1642; `WUB`#1643 | WUB; rest unmapped | B/body+ |
| `Splashguards` #1656 @88 | `S0390`#1658 | Unmapped | B/body+ |
| `Primer` #1659 @89 | `S0115`#1661 | Unmapped | B/body+ |
| `Grille` #1678 @92 | `VWE`#1680 | VWE; rest unmapped | B/body- |
| `Mirror_Cap` #1684 @94 | `S0102_L&{P}` IDs [1686, 1687, 1688, 1689, 1690, 1691, 1692, 1693, 1694, 1695]; `5JR_L`#1696 | 5JR; rest unmapped | B/body- |
| `Mirrors` #1697 @95 | `UFT_L`#1699 | UFT; rest unmapped | B/body- |
| `Mirror_Cap` #1700 @96 | `DRG_L`#1702 | DRG; rest unmapped | B/body- |
| `Mirrors` #1703 @97 | `DYX_L`#1705; `DWK_L`#1706 | DWK, DYX; rest unmapped | B/body- |
| `Wheels` #1707 @98 | `S0820_RL`#1709; `S0466_RL`#1710; `S0455_RL`#1711; `S0446_RL`#1712; `S0450_RL`#1713; `S0449_RL`#1714; `S0448_RL`#1715; `S0434_RL`#1716; `S0232_RL`#1717 | Unmapped | B/body- |
| `Wheel_Caps` #1718 @99 | `S0383_RL`#1720; `S0419_RL`#1721; `S0416_RL`#1722; `S0415_RL`#1723; `S0234_RL`#1724; `S0251_RL`#1725; `S0826_RL`#1726; `S0828_RL`#1727; `S0827_RL`#1728 | Unmapped | B/body- |
| `Brakes` #1729 @100 | `S0381_RL`#1731; `S0293_RL`#1732; `S0296_RL`#1733; `S0294_RL`#1734; `S0291_RL`#1735; `JX6_RL`#1736 | JX6; rest unmapped | B/body- |
| `Wheels` #1737 @101 | `S0426_FL`#1739; `S0476_FL`#1740; `S0455_FL`#1741; `S0442_FL`#1742; `S0452_FL`#1743; `S0447_FL`#1744; `S0439_FL`#1745; `S0451_FL`#1746; `S0433_FL`#1747; `S0397_FL`#1748 | Unmapped | B/body- |
| `Wheel_Caps` #1749 @102 | `S0202_FL`#1751; `S0251_FL`#1752; `S0824_FL`#1753; `S0419_FL`#1754; `S0405_FL`#1755 | Unmapped | B/body- |
| `Brakes` #1756 @103 | `S0291_FL`#1758; `S0288_FL`#1759; `S0294_FL`#1760; `S0299_FL`#1761; `S0381_FL`#1762; `J57_FL`#1763 | J57; rest unmapped | B/body- |
| `Shadow` #1764 @104 | `S0902`#1766 | Unmapped | B/body- |
| `Background` #1767 @105 | `S0100`#1769 | Unmapped | B/body- |
| `Tow_Hooks` #1770 @106 | `S0869`#1772 | Unmapped | B/body- |
| `Wheels` #1773 @107 | `S0816_FR`#1775; `S0816_RR`#1776 | Unmapped | B/body- |

Cabin/trim-dependent groups visible through glass (separate interior scenes are outside this audit): `Stitching` #467 @47 (3 children); `Steering_Wheel` #472 @48 (119 children); `Seat_Belts` #731 @60 (19 children); `Interior` #752 @61 (55 children); `Interior_Kit` #809 @62 (41 children); `Interior` #852 @63 (28 children); `Interior_Kit` #882 @64 (78 children); `IP` #962 @65 (1 children); `Cluster` #965 @66 (75 children); `Stitching` #1042 @67 (59 children); `Floors` #1103 @68 (44 children); `Interior_Kit` #1149 @69 (1 children); `IP` #1152 @70 (43 children); `Seats_Front` #1197 @71 (169 children); `Interior` #1368 @72 (1 children); `Speakers` #1377 @74 (121 children); `IP` #1500 @75 (1 children); `Decal_Stickers` #1503 @76 (45 children); `Console` #1550 @77 (5 children); `Effects` #1564 @80 (46 children). Their seat/material/trim state must be recaptured for lower trims; no upper-trim interior is authorized as a substitute.

</details>

<details>
<summary>S04 — Grand Sport coupe view 01</summary>

PSB: **V/grandsport/e.coupe.exterior.01 - cleaned.psb**. Body-paint root index 73; spoiler root indices 65, 66, 67.

<a id="s04-paint"></a>

**Paint — U; all ten base paints**

| Parent path / ID / root index | Exact paint-bearing peers (each maps only its paint token) | Native placement |
| --- | --- | --- |
| `Molding` #72 @11 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Ground_Effects` #97 @15 | 40 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Front_Fascia` #146 @17 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Mirror_Cap` #305 @25 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `B_Pillars` #335 @30 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Rear_Fascia` #427 @39 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Roof` #442 @40 | 40 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Spoiler` #1515 @65 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | S/body+ |
| `Base` #1593 @73 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body= |
| `Mirror_Cap` #1610 @75 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body- |

<a id="s04-foundation"></a>

**Trim and body foundation**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Base` #1428 @59 | `S0507&3LT`#1430; `S0507&2LT`#1431; `S0507&1LT`#1432 | Configuration/trim candidates | F/body+ |
| `Base` #1593 @73 | `GBA`#1595; `G8G`#1596; `GKZ`#1597; `GPH`#1598; `G26`#1599; `GBK`#1600; `G4Z`#1601; `GKA`#1602; `GTR`#1603; `GEC`#1604; `1YE07`#1605 | Configuration/trim candidates | B/body= |

<a id="s04-rear"></a>

**Rear spoiler / source-off-spoiler state**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Spoiler` #1515 @65 | `T0F`#1517; `S0268`#1518; `S0267&{P}` IDs [1519, 1520, 1521, 1522, 1523, 1524, 1525, 1526, 1527, 1528]; `SIG`#1529 | SIG, T0F; rest unmapped | S/body+ |
| `Spoiler` #1533 @66 | `5V5`#1535 | Unmapped | S/body+ |
| `Spoiler` #1539 @67 | `5ZV`#1541 | 5ZV; rest unmapped | S/body+ |

Source-off-spoiler state: hide every `Spoiler` parent listed here; this is a visibility recipe, **not a catalog option ID**. No legal no-spoiler configuration is established by this operation.

<a id="s04-aero"></a>

**Front/side/hood/fascia aero candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Ground_Effects` #69 @10 | `RAU`#71 | Unmapped | F/body+ |
| `Front_Fascia` #85 @12 | `S0274`#87; `S0273`#88 | Unmapped | F/body+ |
| `Front_Fascia` #92 @14 | `S0227`#94; `S0224`#95; `S0221`#96 | Unmapped | F/body+ |
| `Ground_Effects` #97 @15 | `S0396`#99; `S0395`#100; `S0368`#101; `S0367`#102; `S0258&{P}` IDs [103, 104, 105, 106, 107, 108, 109, 110, 111, 112]; `S0872&{P}` IDs [113, 114, 115, 116, 117, 118, 119, 120, 121, 122]; `S0873&{P}` IDs [123, 124, 125, 126, 127, 128, 129, 130, 131, 132]; `S0278&{P}` IDs [133, 134, 135, 136, 137, 138, 139, 140, 141, 142] | Unmapped | F/body+ |
| `Front_Fascia` #146 @17 | `S0220&{P}` IDs [148, 149, 150, 151, 152, 153, 154, 155, 156, 157] | Unmapped | F/body+ |
| `Ground_Effects` #300 @24 | `S0366`#302; `S0365`#303; `S0237`#304 | Unmapped | F/body+ |
| `Rear_Fascia` #427 @39 | `S0204`#429; `S0203&{P}` IDs [430, 431, 432, 433, 434, 435, 436, 437, 438, 439] | Unmapped | F/body+ |

<a id="s04-graphics"></a>

**Stripes / decals / color candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Decals` #4 @1 | `S0889`#6; `S0899`#7; `S0898`#8; `S0897`#9; `S0896`#10 | Unmapped | F/body+ |
| `Decals` #20 @3 | `S0891`#22 | Unmapped | F/body+ |
| `Decals` #27 @5 | `S0837_F`#29; `S0855_F`#30; `S0302_F`#31; `S0330_F`#32; `S0325_F`#33; `S0320_F`#34; `S0315_F`#35; `S0307_F`#36; `S0860_F`#37; `S0875_F`#38; `S0880_F`#39; `S0890_F`#40; `S0893_F`#41 | Unmapped | F/body+ |
| `Stripes` #42 @6 | `S0369_F`#44 | Unmapped | F/body+ |
| `Decals` #45 @7 | `S0362_F`#47; `S0349_F`#48; `S0342_F`#49; `S0314_F`#50; `S0306_F`#51; `DZX`#52; `DZV`#53; `DZU`#54; `S0379`#55; `VPO`#56; `17A`#57; `20A`#58; `55A`#59; `75A`#60; `97A`#61; `DX4`#62 | 17A, 20A, 55A, 75A, 97A, DX4, DZU, DZV, DZX, VPO; rest unmapped | F/body+ |
| `Decals` #353 @33 | `S0866`#355; `S0858`#356; `S0361`#357; `S0348`#358; `S0341`#359; `S0334`#360; `S0876`#361; `S0313`#362 | Unmapped | F/body+ |
| `Decals` #366 @34 | `S0332`#368; `S0327`#369; `S0322`#370; `S0317`#371; `S0304`#372; `S0303`#373; `S0881`#374; `S0894`#375; `S0861`#376; `S0308`#377 | Unmapped | F/body+ |
| `Decals` #421 @38 | `S0892`#423 | Unmapped | F/body+ |
| `Decals` #1490 @63 | `S0877`#1492; `S0874`#1493; `S0363`#1494; `S0358`#1495; `S0344`#1496; `S0338`#1497; `S0857`#1498; `S0319`#1499 | Unmapped | F/body+ |
| `Decals` #1503 @64 | `S0333`#1505; `S0328`#1506; `S0323`#1507; `S0318`#1508; `S0310`#1509; `S0309`#1510; `S0311`#1511 | Unmapped | F/body+ |
| `Decals` #1560 @71 | `S0860_B`#1562; `S0875_B`#1563; `S0890_B`#1564; `S0893_B`#1565; `S0880_B`#1566 | Unmapped | B/body+ |
| `Decals` #1571 @72 | `S0882`#1576; `S0838`#1577; `S0862`#1578; `S0895`#1579; `S0360`#1580; `S0347`#1581; `S0340`#1582; `S0329`#1583; `S0312`#1584; `S0331`#1585; `S0326`#1586; `S0321`#1587; `S0316`#1588; `S0301`#1589; `S0300`#1590; `S0859`#1591; `S0305`#1592 | Unmapped | B/body+ |

<a id="s04-glass"></a>

**Glass and window candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Windows` #332 @29 | `S0105`#334 | Unmapped | F/body+ |
| `Windows` #347 @31 | `S0101_L`#349 | Unmapped | F/body+ |
| `Windows` #415 @37 | `S0108`#417 | Unmapped | F/body+ |
| `Windows` #1483 @61 | `S0122`#1485; `S0104`#1486 | Unmapped | F/body+ |
| `Defroster` #1487 @62 | `S0107`#1489 | Unmapped | F/body+ |
| `Windows` #1606 @74 | `S0101_R`#1609 | Unmapped | B/body- |

<a id="s04-other"></a>

**Other exterior option-driven and fixed groups**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Tow_Hooks` #1 @0 | No native children | Unmapped | F/body+ |
| `Badges` #11 @2 | `RIN`#13; `EYK_F`#14; `EYT_F`#15; `SFZ_F`#17; `R88_F`#19 | EYK, EYT, R88, RIN, SFZ; rest unmapped | F/body+ |
| `Badges` #23 @4 | `S0374`#25; `S0399`#26 | Unmapped | F/body+ |
| `Tail_Lamps` #63 @8 | `S0200`#65 | Unmapped | F/body+ |
| `Headlamps` #66 @9 | `T4L`#68 | T4L; rest unmapped | F/body+ |
| `Molding` #72 @11 | `S0211&{P}` IDs [74, 75, 76, 77, 78, 79, 80, 81, 82, 83]; `S0209`#84 | Unmapped | F/body+ |
| `Badges` #89 @13 | `S0271`#91 | Unmapped | F/body+ |
| `Grille` #143 @16 | `VWE`#145 | VWE; rest unmapped | F/body+ |
| `Wheels` #158 @18 | `S0816_RL`#160; `S0820_RL`#161; `S0815_RL`#162; `S0810_RL`#163; `S0466_RL`#164; `S0455_RL`#165; `S0443_RL`#166; `S0441_RL`#167; `S0465_RL`#168; `S0462_RL`#169; `S0442_RL`#170; `S0453_RL`#171; `S0452_RL`#172; `S0447_RL`#173; `S0446_RL`#174; `S0439_RL`#175; `S0440_RL`#176; `S0451_RL`#177; `S0450_RL`#178; `S0449_RL`#179; `S0448_RL`#180; `S0433_RL`#181; `S0434_RL`#182; `S0431_RL`#183; `S0432_RL`#184; `S0454_RL`#185; `S0427_RL`#186; `S0428_RL`#187; `S0426_RL`#188; `S0425_RL`#189; `S0476_RL`#190; `S0497_RL`#191; `S0471_RL`#192; `S0397_RL`#193; `S0398_RL`#194; `S0232_RL`#195 | Unmapped | F/body+ |
| `Wheel_Caps` #196 @19 | `S0383_RL`#198; `S0264_RL`#199; `S0419_RL`#200; `S0418_RL`#201; `S0416_RL`#202; `S0415_RL`#203; `S0405_RL`#204; `S0234_RL`#205; `S0202_RL`#206; `S0251_RL`#207; `S0824_RL`#208; `S0825_RL`#209; `S0826_RL`#210; `S0828_RL`#211; `S0827_RL`#212 | Unmapped | F/body+ |
| `Brakes` #213 @20 | `S0299_RL`#215; `S0381_RL`#216; `S0292_RL`#217; `S0290_RL`#218; `S0289_RL`#219; `S0293_RL`#220; `S0288_RL`#221; `S0296_RL`#222; `S0295_RL`#223; `S0294_RL`#224; `S0291_RL`#225; `J57_RL`#226; `J56_RL`#227; `JX6_RL`#228 | J56, J57, JX6; rest unmapped | F/body+ |
| `Wheels` #229 @21 | `S0816_FL`#231; `S0820_FL`#232; `S0815_FL`#233; `S0426_FL`#234; `S0427_FL`#235; `S0428_FL`#236; `S0425_FL`#237; `S0810_FL`#238; `S0476_FL`#239; `S0497_FL`#240; `S0466_FL`#241; `S0455_FL`#242; `S0442_FL`#243; `S0441_FL`#244; `S0465_FL`#245; `S0462_FL`#246; `S0443_FL`#247; `S0453_FL`#248; `S0452_FL`#249; `S0447_FL`#250; `S0446_FL`#251; `S0439_FL`#252; `S0440_FL`#253; `S0451_FL`#254; `S0450_FL`#255; `S0449_FL`#256; `S0448_FL`#257; `S0433_FL`#258; `S0434_FL`#259; `S0431_FL`#260; `S0432_FL`#261; `S0454_FL`#262; `S0471_FL`#263; `S0397_FL`#264; `S0398_FL`#265; `S0232_FL`#266 | Unmapped | F/body+ |
| `Wheel_Caps` #267 @22 | `S0234_FL`#269; `S0202_FL`#270; `S0251_FL`#271; `S0824_FL`#272; `S0825_FL`#273; `S0826_FL`#274; `S0828_FL`#275; `S0827_FL`#276; `S0264_FL`#277; `S0383_FL`#278; `S0419_FL`#279; `S0418_FL`#280; `S0416_FL`#281; `S0415_FL`#282; `S0405_FL`#283 | Unmapped | F/body+ |
| `Brakes` #284 @23 | `S0291_FL`#286; `S0290_FL`#287; `S0299_FL`#288; `S0381_FL`#289; `S0292_FL`#290; `S0289_FL`#291; `S0288_FL`#292; `S0296_FL`#293; `S0295_FL`#294; `S0294_FL`#295; `S0293_FL`#296; `J57_FL`#297; `J56_FL`#298; `JX6_FL`#299 | J56, J57, JX6; rest unmapped | F/body+ |
| `Mirror_Cap` #305 @25 | `S0102_L&{P}` IDs [307, 308, 309, 310, 311, 312, 313, 314, 315, 316] | Unmapped | F/body+ |
| `Mirror_Cap` #319 @26 | `5JR_L`#321 | 5JR; rest unmapped | F/body+ |
| `Mirror_Cap` #325 @27 | `DRG_L`#327 | DRG; rest unmapped | F/body+ |
| `Mirrors` #328 @28 | `DYX_L`#330; `DWK_L`#331 | DWK, DYX; rest unmapped | F/body+ |
| `B_Pillars` #335 @30 | `S0212&{P}` IDs [337, 338, 339, 340, 341, 342, 343, 344, 345, 346] | Unmapped | F/body+ |
| `Primer` #350 @32 | `S0115`#352 | Unmapped | F/body+ |
| `Doors` #378 @35 | `S0559&HTE`#380; `S0559&HTT`#381; `S0559&HVV`#382; `S0559&HU1`#383; `S0559&HMO`#384; `S0559&HU9`#385; `S0559&HZB`#386; `S0559&HVT`#387; `S0559&HUA`#388; `S0559&HU2`#389; `S0559&HUU`#390; `S0559&HZP`#391; `S0559&HUE`#392; `S0559&HTG`#393; `S0559&HZN`#394; `S0559&HUF`#395; `S0559&HU0`#396; `S0559&HXO`#397; `S0559&HNK`#398; `S0559&HUW`#399; `S0559&HUX`#400; `S0559&HVZ`#401; `S0559&H8T`#402; `S0559&HUB`#403; `S0559&HUC`#404; `S0559&EPX`#405; `S0559&EJH`#406; `S0559&HAG`#407; `S0559&EL9`#408 | Unmapped | F/body+ |
| `Splashguards` #412 @36 | `S0390`#414 | Unmapped | F/body+ |
| `Roof` #442 @40 | `SBT`#444; `S0243&{P}` IDs [445, 446, 447, 448, 449, 450, 451, 452, 453, 454]; `C2Z&{P}` IDs [455, 456, 457, 458, 459, 460, 461, 462, 463, 464]; `CF7&{P}` IDs [465, 466, 467, 468, 469, 470, 471, 472, 473, 474]; `CF8&{P}` IDs [475, 476, 477, 478, 479, 480, 481, 482, 483, 484]; `CC3`#485; `S0506`#486; `UG1&HUV`#487; `UG1&HU7`#488; `UG1&HUL`#489; `UG1&HUR`#490; `UG1&HUK`#491; `UG1&HU6`#492; `UG1&HUN`#493; `UG1&HTP`#494; `UG1&H1Y`#495; `UG1&HTE`#496; `UG1&HTT`#497; `UG1&HVV`#498; `UG1&HU1`#499; `UG1&HMO`#500; `UG1&HU9`#501; `UG1&HZB`#502; `UG1&HVT`#503; `UG1&HUA`#504; `UG1&HU2`#505; `UG1&HUU`#506; `UG1&HZP`#507; `UG1&HUE`#508; `UG1&HTG`#509; `UG1&HZN`#510; `UG1&HUF`#511; `UG1&HU0`#512; `UG1&HXO`#513; `UG1&HNK`#514; `UG1&HUW`#515; `UG1&HUX`#516; `UG1&HVZ`#517; `UG1&H8T`#518; `UG1&HUB`#519; `UG1&HUC`#520; `UG1&EPX`#521; `UG1&EJH`#522; `UG1&HAG`#523; `UG1&EL9`#524; `UG1&HTA`#525; `UG1&HTM`#526; `UG1&HTQ`#527; `UG1&HTN`#528 | C2Z, CC3, CF7, CF8, SBT, UG1; rest unmapped | F/body+ |
| `Badges` #1192 @53 | `S0508`#1194; `BV4`#1195 | BV4; rest unmapped | F/body+ |
| `Badges` #1544 @68 | `S0270`#1546 | Unmapped | B/body+ |
| `Engine` #1547 @69 | `LS6`#1550 | LS6; rest unmapped | B/body+ |
| `Exhaust` #1551 @70 | `S0229`#1553; `WUB`#1554; `S0865`#1555 | WUB; rest unmapped | B/body+ |
| `Mirror_Cap` #1610 @75 | `S0102_R&{P}` IDs [1612, 1613, 1614, 1615, 1616, 1617, 1618, 1619, 1620, 1621]; `5JR_R`#1622 | 5JR; rest unmapped | B/body- |
| `Mirrors` #1623 @76 | `UFT_R`#1625 | UFT; rest unmapped | B/body- |
| `Mirror_Cap` #1626 @77 | `DRG_R`#1628 | DRG; rest unmapped | B/body- |
| `Mirrors` #1629 @78 | `DYX_R`#1631; `DWK_R`#1632 | DWK, DYX; rest unmapped | B/body- |
| `Wheel_Caps` #1641 @79 | `S0251_RR`#1643 | Unmapped | B/body- |
| `Wheels` #1648 @80 | `S0810_FR`#1650; `S0476_FR`#1651; `S0497_FR`#1652; `S0466_FR`#1653; `S0455_FR`#1654; `S0443_FR`#1655; `S0442_FR`#1656; `S0441_FR`#1657; `S0465_FR`#1658; `S0462_FR`#1659; `S0453_FR`#1660; `S0452_FR`#1661; `S0447_FR`#1662; `S0446_FR`#1663; `S0471_FR`#1664; `S0439_FR`#1665; `S0440_FR`#1666; `S0451_FR`#1667; `S0450_FR`#1668; `S0449_FR`#1669; `S0448_FR`#1670; `S0433_FR`#1671; `S0434_FR`#1672; `S0431_FR`#1673; `S0432_FR`#1674; `S0454_FR`#1675; `S0397_FR`#1676; `S0398_FR`#1677; `S0232_FR`#1678 | Unmapped | B/body- |
| `Wheel_Caps` #1679 @81 | `S0251_FR`#1682 | Unmapped | B/body- |
| `Shadow` #1688 @82 | `S0902`#1690 | Unmapped | B/body- |
| `Background` #1691 @83 | `S0100`#1693 | Unmapped | B/body- |

Cabin/trim-dependent groups visible through glass (separate interior scenes are outside this audit): `Stitching` #529 @41 (13 children); `Steering_Wheel` #550 @42 (37 children); `Interior_Kit` #630 @43 (1 children); `Interior` #633 @44 (26 children); `Interior_Kit` #689 @45 (20 children); `Interior` #732 @46 (29 children); `Interior_Kit` #763 @47 (40 children); `Stitching` #844 @48 (38 children); `Seat_Belts` #884 @49 (20 children); `Seats_Front` #906 @50 (167 children); `Floors` #1076 @51 (17 children); `Cluster` #1115 @52 (75 children); `Stitching` #1200 @54 (3 children); `IP` #1205 @55 (1 children); `Decal_Stickers` #1208 @56 (45 children); `IP` #1255 @57 (43 children); `Speakers` #1300 @58 (126 children); `Effects` #1435 @60 (46 children); `Steering_Wheel` #1694 @84 (15 children); `Console` #1723 @85 (3 children). Their seat/material/trim state must be recaptured for lower trims; no upper-trim interior is authorized as a substitute.

</details>

<details>
<summary>S05 — Grand Sport coupe view 01 (uncleaned comparison)</summary>

PSB: **V/grandsport/e.coupe.exterior.01.psb**. Body-paint root index 89; spoiler root indices 76, 78, 80.

<a id="s05-paint"></a>

**Paint — U; all ten base paints**

| Parent path / ID / root index | Exact paint-bearing peers (each maps only its paint token) | Native placement |
| --- | --- | --- |
| `Molding` #72 @11 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Ground_Effects` #97 @15 | 40 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Front_Fascia` #146 @17 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Mirror_Cap` #305 @25 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `B_Pillars` #335 @32 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Rear_Fascia` #427 @45 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Roof` #442 @47 | 40 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Spoiler` #1515 @76 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | S/body+ |
| `Base` #1593 @89 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body= |
| `Mirror_Cap` #1610 @91 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body- |

<a id="s05-foundation"></a>

**Trim and body foundation**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Base` #1428 @67 | `S0507&3LT`#1430; `S0507&2LT`#1431; `S0507&1LT`#1432 | Configuration/trim candidates | F/body+ |
| `Base` #1593 @89 | `GBA`#1595; `G8G`#1596; `GKZ`#1597; `GPH`#1598; `G26`#1599; `GBK`#1600; `G4Z`#1601; `GKA`#1602; `GTR`#1603; `GEC`#1604; `1YE07`#1605 | Configuration/trim candidates | B/body= |

<a id="s05-rear"></a>

**Rear spoiler / source-off-spoiler state**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Spoiler` #1515 @76 | `T0F`#1517; `S0268`#1518; `S0267&{P}` IDs [1519, 1520, 1521, 1522, 1523, 1524, 1525, 1526, 1527, 1528]; `SIG`#1529 | SIG, T0F; rest unmapped | S/body+ |
| `Spoiler` #1533 @78 | `5V5`#1535 | Unmapped | S/body+ |
| `Spoiler` #1539 @80 | `5ZV`#1541 | 5ZV; rest unmapped | S/body+ |

Source-off-spoiler state: hide every `Spoiler` parent listed here; this is a visibility recipe, **not a catalog option ID**. No legal no-spoiler configuration is established by this operation.

<a id="s05-aero"></a>

**Front/side/hood/fascia aero candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Ground_Effects` #69 @10 | `RAU`#71 | Unmapped | F/body+ |
| `Front_Fascia` #85 @12 | `S0274`#87; `S0273`#88 | Unmapped | F/body+ |
| `Front_Fascia` #92 @14 | `S0227`#94; `S0224`#95; `S0221`#96 | Unmapped | F/body+ |
| `Ground_Effects` #97 @15 | `S0396`#99; `S0395`#100; `S0368`#101; `S0367`#102; `S0258&{P}` IDs [103, 104, 105, 106, 107, 108, 109, 110, 111, 112]; `S0872&{P}` IDs [113, 114, 115, 116, 117, 118, 119, 120, 121, 122]; `S0873&{P}` IDs [123, 124, 125, 126, 127, 128, 129, 130, 131, 132]; `S0278&{P}` IDs [133, 134, 135, 136, 137, 138, 139, 140, 141, 142] | Unmapped | F/body+ |
| `Front_Fascia` #146 @17 | `S0220&{P}` IDs [148, 149, 150, 151, 152, 153, 154, 155, 156, 157] | Unmapped | F/body+ |
| `Ground_Effects` #300 @24 | `S0366`#302; `S0365`#303; `S0237`#304 | Unmapped | F/body+ |
| `Rear_Fascia` #427 @45 | `S0204`#429; `S0203&{P}` IDs [430, 431, 432, 433, 434, 435, 436, 437, 438, 439] | Unmapped | F/body+ |

<a id="s05-graphics"></a>

**Stripes / decals / color candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Decals` #4 @1 | `S0889`#6; `S0899`#7; `S0898`#8; `S0897`#9; `S0896`#10 | Unmapped | F/body+ |
| `Decals` #20 @3 | `S0891`#22 | Unmapped | F/body+ |
| `Decals` #27 @5 | `S0837_F`#29; `S0855_F`#30; `S0302_F`#31; `S0330_F`#32; `S0325_F`#33; `S0320_F`#34; `S0315_F`#35; `S0307_F`#36; `S0860_F`#37; `S0875_F`#38; `S0880_F`#39; `S0890_F`#40; `S0893_F`#41 | Unmapped | F/body+ |
| `Stripes` #42 @6 | `S0369_F`#44 | Unmapped | F/body+ |
| `Decals` #45 @7 | `S0362_F`#47; `S0349_F`#48; `S0342_F`#49; `S0314_F`#50; `S0306_F`#51; `DZX`#52; `DZV`#53; `DZU`#54; `S0379`#55; `VPO`#56; `17A`#57; `20A`#58; `55A`#59; `75A`#60; `97A`#61; `DX4`#62 | 17A, 20A, 55A, 75A, 97A, DX4, DZU, DZV, DZX, VPO; rest unmapped | F/body+ |
| `Decals` #353 @35 | `S0866`#355; `S0858`#356; `S0361`#357; `S0348`#358; `S0341`#359; `S0334`#360; `S0876`#361; `S0313`#362 | Unmapped | F/body+ |
| `Decals` #366 @37 | `S0332`#368; `S0327`#369; `S0322`#370; `S0317`#371; `S0304`#372; `S0303`#373; `S0881`#374; `S0894`#375; `S0861`#376; `S0308`#377 | Unmapped | F/body+ |
| `Decals` #421 @43 | `S0892`#423 | Unmapped | F/body+ |
| `Decals` #1490 @72 | `S0877`#1492; `S0874`#1493; `S0363`#1494; `S0358`#1495; `S0344`#1496; `S0338`#1497; `S0857`#1498; `S0319`#1499 | Unmapped | F/body+ |
| `Decals` #1503 @74 | `S0333`#1505; `S0328`#1506; `S0323`#1507; `S0318`#1508; `S0310`#1509; `S0309`#1510; `S0311`#1511 | Unmapped | F/body+ |
| `Decals` #1560 @86 | `S0860_B`#1562; `S0875_B`#1563; `S0890_B`#1564; `S0893_B`#1565; `S0880_B`#1566; `S0320_B`#1567; `S0315_B`#1568 | Unmapped | B/body+ |
| `Stripes` #1569 @87 | No native children | Unmapped | B/body+ |
| `Decals` #1571 @88 | `S0349_B`#1573; `S0342_B`#1574; `S0314_B`#1575; `S0882`#1576; `S0838`#1577; `S0862`#1578; `S0895`#1579; `S0360`#1580; `S0347`#1581; `S0340`#1582; `S0329`#1583; `S0312`#1584; `S0331`#1585; `S0326`#1586; `S0321`#1587; `S0316`#1588; `S0301`#1589; `S0300`#1590; `S0859`#1591; `S0305`#1592 | Unmapped | B/body+ |

<a id="s05-glass"></a>

**Glass and window candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Windows` #332 @31 | `S0105`#334 | Unmapped | F/body+ |
| `Windows` #347 @33 | `S0101_L`#349 | Unmapped | F/body+ |
| `Windows` #415 @41 | `S0108`#417 | Unmapped | F/body+ |
| `Windows` #1483 @70 | `S0122`#1485; `S0104`#1486 | Unmapped | F/body+ |
| `Defroster` #1487 @71 | `S0107`#1489 | Unmapped | F/body+ |
| `Windows` #1606 @90 | `S0101_B`#1608; `S0101_R`#1609 | Unmapped | B/body- |

<a id="s05-other"></a>

**Other exterior option-driven and fixed groups**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Tow_Hooks` #1 @0 | No native children | Unmapped | F/body+ |
| `Badges` #11 @2 | `RIN`#13; `EYK_F`#14; `EYT_F`#15; `EYK_B`#16; `SFZ_F`#17; `S0276`#18; `R88_F`#19 | EYK, EYT, R88, RIN, SFZ; rest unmapped | F/body+ |
| `Badges` #23 @4 | `S0374`#25; `S0399`#26 | Unmapped | F/body+ |
| `Tail_Lamps` #63 @8 | `S0200`#65 | Unmapped | F/body+ |
| `Headlamps` #66 @9 | `T4L`#68 | T4L; rest unmapped | F/body+ |
| `Molding` #72 @11 | `S0211&{P}` IDs [74, 75, 76, 77, 78, 79, 80, 81, 82, 83]; `S0209`#84 | Unmapped | F/body+ |
| `Badges` #89 @13 | `S0271`#91 | Unmapped | F/body+ |
| `Grille` #143 @16 | `VWE`#145 | VWE; rest unmapped | F/body+ |
| `Wheels` #158 @18 | `S0816_RL`#160; `S0820_RL`#161; `S0815_RL`#162; `S0810_RL`#163; `S0466_RL`#164; `S0455_RL`#165; `S0443_RL`#166; `S0441_RL`#167; `S0465_RL`#168; `S0462_RL`#169; `S0442_RL`#170; `S0453_RL`#171; `S0452_RL`#172; `S0447_RL`#173; `S0446_RL`#174; `S0439_RL`#175; `S0440_RL`#176; `S0451_RL`#177; `S0450_RL`#178; `S0449_RL`#179; `S0448_RL`#180; `S0433_RL`#181; `S0434_RL`#182; `S0431_RL`#183; `S0432_RL`#184; `S0454_RL`#185; `S0427_RL`#186; `S0428_RL`#187; `S0426_RL`#188; `S0425_RL`#189; `S0476_RL`#190; `S0497_RL`#191; `S0471_RL`#192; `S0397_RL`#193; `S0398_RL`#194; `S0232_RL`#195 | Unmapped | F/body+ |
| `Wheel_Caps` #196 @19 | `S0383_RL`#198; `S0264_RL`#199; `S0419_RL`#200; `S0418_RL`#201; `S0416_RL`#202; `S0415_RL`#203; `S0405_RL`#204; `S0234_RL`#205; `S0202_RL`#206; `S0251_RL`#207; `S0824_RL`#208; `S0825_RL`#209; `S0826_RL`#210; `S0828_RL`#211; `S0827_RL`#212 | Unmapped | F/body+ |
| `Brakes` #213 @20 | `S0299_RL`#215; `S0381_RL`#216; `S0292_RL`#217; `S0290_RL`#218; `S0289_RL`#219; `S0293_RL`#220; `S0288_RL`#221; `S0296_RL`#222; `S0295_RL`#223; `S0294_RL`#224; `S0291_RL`#225; `J57_RL`#226; `J56_RL`#227; `JX6_RL`#228 | J56, J57, JX6; rest unmapped | F/body+ |
| `Wheels` #229 @21 | `S0816_FL`#231; `S0820_FL`#232; `S0815_FL`#233; `S0426_FL`#234; `S0427_FL`#235; `S0428_FL`#236; `S0425_FL`#237; `S0810_FL`#238; `S0476_FL`#239; `S0497_FL`#240; `S0466_FL`#241; `S0455_FL`#242; `S0442_FL`#243; `S0441_FL`#244; `S0465_FL`#245; `S0462_FL`#246; `S0443_FL`#247; `S0453_FL`#248; `S0452_FL`#249; `S0447_FL`#250; `S0446_FL`#251; `S0439_FL`#252; `S0440_FL`#253; `S0451_FL`#254; `S0450_FL`#255; `S0449_FL`#256; `S0448_FL`#257; `S0433_FL`#258; `S0434_FL`#259; `S0431_FL`#260; `S0432_FL`#261; `S0454_FL`#262; `S0471_FL`#263; `S0397_FL`#264; `S0398_FL`#265; `S0232_FL`#266 | Unmapped | F/body+ |
| `Wheel_Caps` #267 @22 | `S0234_FL`#269; `S0202_FL`#270; `S0251_FL`#271; `S0824_FL`#272; `S0825_FL`#273; `S0826_FL`#274; `S0828_FL`#275; `S0827_FL`#276; `S0264_FL`#277; `S0383_FL`#278; `S0419_FL`#279; `S0418_FL`#280; `S0416_FL`#281; `S0415_FL`#282; `S0405_FL`#283 | Unmapped | F/body+ |
| `Brakes` #284 @23 | `S0291_FL`#286; `S0290_FL`#287; `S0299_FL`#288; `S0381_FL`#289; `S0292_FL`#290; `S0289_FL`#291; `S0288_FL`#292; `S0296_FL`#293; `S0295_FL`#294; `S0294_FL`#295; `S0293_FL`#296; `J57_FL`#297; `J56_FL`#298; `JX6_FL`#299 | J56, J57, JX6; rest unmapped | F/body+ |
| `Mirror_Cap` #305 @25 | `S0102_L&{P}` IDs [307, 308, 309, 310, 311, 312, 313, 314, 315, 316] | Unmapped | F/body+ |
| `Mirrors` #317 @26 | No native children | Unmapped | F/body+ |
| `Mirror_Cap` #319 @27 | `5JR_L`#321 | 5JR; rest unmapped | F/body+ |
| `Mirrors` #322 @28 | `UFT_L`#324 | UFT; rest unmapped | F/body+ |
| `Mirror_Cap` #325 @29 | `DRG_L`#327 | DRG; rest unmapped | F/body+ |
| `Mirrors` #328 @30 | `DYX_L`#330; `DWK_L`#331 | DWK, DYX; rest unmapped | F/body+ |
| `B_Pillars` #335 @32 | `S0212&{P}` IDs [337, 338, 339, 340, 341, 342, 343, 344, 345, 346] | Unmapped | F/body+ |
| `Primer` #350 @34 | `S0115`#352 | Unmapped | F/body+ |
| `None` #363 @36 | `S0345`#365 | Unmapped | F/body+ |
| `Doors` #378 @38 | `S0559&HTE`#380; `S0559&HTT`#381; `S0559&HVV`#382; `S0559&HU1`#383; `S0559&HMO`#384; `S0559&HU9`#385; `S0559&HZB`#386; `S0559&HVT`#387; `S0559&HUA`#388; `S0559&HU2`#389; `S0559&HUU`#390; `S0559&HZP`#391; `S0559&HUE`#392; `S0559&HTG`#393; `S0559&HZN`#394; `S0559&HUF`#395; `S0559&HU0`#396; `S0559&HXO`#397; `S0559&HNK`#398; `S0559&HUW`#399; `S0559&HUX`#400; `S0559&HVZ`#401; `S0559&H8T`#402; `S0559&HUB`#403; `S0559&HUC`#404; `S0559&EPX`#405; `S0559&EJH`#406; `S0559&HAG`#407; `S0559&EL9`#408 | Unmapped | F/body+ |
| `None` #409 @39 | `S0420`#411 | Unmapped | F/body+ |
| `Splashguards` #412 @40 | `S0390`#414 | Unmapped | F/body+ |
| `None` #418 @42 | `VSN`#420 | Unmapped | F/body+ |
| `License_Plate` #424 @44 | `S0235`#426 | Unmapped | F/body+ |
| `Multimedia` #440 @46 | No native children | Unmapped | F/body+ |
| `Roof` #442 @47 | `SBT`#444; `S0243&{P}` IDs [445, 446, 447, 448, 449, 450, 451, 452, 453, 454]; `C2Z&{P}` IDs [455, 456, 457, 458, 459, 460, 461, 462, 463, 464]; `CF7&{P}` IDs [465, 466, 467, 468, 469, 470, 471, 472, 473, 474]; `CF8&{P}` IDs [475, 476, 477, 478, 479, 480, 481, 482, 483, 484]; `CC3`#485; `S0506`#486; `UG1&HUV`#487; `UG1&HU7`#488; `UG1&HUL`#489; `UG1&HUR`#490; `UG1&HUK`#491; `UG1&HU6`#492; `UG1&HUN`#493; `UG1&HTP`#494; `UG1&H1Y`#495; `UG1&HTE`#496; `UG1&HTT`#497; `UG1&HVV`#498; `UG1&HU1`#499; `UG1&HMO`#500; `UG1&HU9`#501; `UG1&HZB`#502; `UG1&HVT`#503; `UG1&HUA`#504; `UG1&HU2`#505; `UG1&HUU`#506; `UG1&HZP`#507; `UG1&HUE`#508; `UG1&HTG`#509; `UG1&HZN`#510; `UG1&HUF`#511; `UG1&HU0`#512; `UG1&HXO`#513; `UG1&HNK`#514; `UG1&HUW`#515; `UG1&HUX`#516; `UG1&HVZ`#517; `UG1&H8T`#518; `UG1&HUB`#519; `UG1&HUC`#520; `UG1&EPX`#521; `UG1&EJH`#522; `UG1&HAG`#523; `UG1&EL9`#524; `UG1&HTA`#525; `UG1&HTM`#526; `UG1&HTQ`#527; `UG1&HTN`#528 | C2Z, CC3, CF7, CF8, SBT, UG1; rest unmapped | F/body+ |
| `Badges` #1192 @60 | `S0508`#1194; `BV4`#1195; `S0500`#1196 | BV4; rest unmapped | F/body+ |
| `Radio` #1433 @68 | No native children | Unmapped | F/body+ |
| `None` #1500 @73 | `S0343`#1502 | Unmapped | F/body+ |
| `None` #1512 @75 | `S0357`#1514 | Unmapped | F/body+ |
| `None` #1530 @77 | `S0119`#1532 | Unmapped | S/body+ |
| `None` #1536 @79 | `D58`#1538 | Unmapped | S/body+ |
| `Engine` #1542 @81 | No native children | Unmapped | B/body+ |
| `Badges` #1544 @82 | `S0270`#1546 | Unmapped | B/body+ |
| `Engine` #1547 @83 | `S0111`#1549; `LS6`#1550 | LS6; rest unmapped | B/body+ |
| `Exhaust` #1551 @84 | `S0229`#1553; `WUB`#1554; `S0865`#1555 | WUB; rest unmapped | B/body+ |
| `Tow_Hooks` #1556 @85 | `S0870`#1558; `S0871`#1559 | Unmapped | B/body+ |
| `Mirror_Cap` #1610 @91 | `S0102_R&{P}` IDs [1612, 1613, 1614, 1615, 1616, 1617, 1618, 1619, 1620, 1621]; `5JR_R`#1622 | 5JR; rest unmapped | B/body- |
| `Mirrors` #1623 @92 | `UFT_R`#1625 | UFT; rest unmapped | B/body- |
| `Mirror_Cap` #1626 @93 | `DRG_R`#1628 | DRG; rest unmapped | B/body- |
| `Mirrors` #1629 @94 | `DYX_R`#1631; `DWK_R`#1632 | DWK, DYX; rest unmapped | B/body- |
| `Wheels` #1633 @95 | `S0455_RR`#1635; `S0465_RR`#1636; `S0447_RR`#1637; `S0446_RR`#1638; `S0440_RR`#1639; `S0427_RR`#1640 | Unmapped | B/body- |
| `Wheel_Caps` #1641 @96 | `S0251_RR`#1643; `S0825_RR`#1644 | Unmapped | B/body- |
| `Brakes` #1645 @97 | `S0299_RR`#1647 | Unmapped | B/body- |
| `Wheels` #1648 @98 | `S0810_FR`#1650; `S0476_FR`#1651; `S0497_FR`#1652; `S0466_FR`#1653; `S0455_FR`#1654; `S0443_FR`#1655; `S0442_FR`#1656; `S0441_FR`#1657; `S0465_FR`#1658; `S0462_FR`#1659; `S0453_FR`#1660; `S0452_FR`#1661; `S0447_FR`#1662; `S0446_FR`#1663; `S0471_FR`#1664; `S0439_FR`#1665; `S0440_FR`#1666; `S0451_FR`#1667; `S0450_FR`#1668; `S0449_FR`#1669; `S0448_FR`#1670; `S0433_FR`#1671; `S0434_FR`#1672; `S0431_FR`#1673; `S0432_FR`#1674; `S0454_FR`#1675; `S0397_FR`#1676; `S0398_FR`#1677; `S0232_FR`#1678 | Unmapped | B/body- |
| `Wheel_Caps` #1679 @99 | `S0419_FR`#1681; `S0251_FR`#1682; `S0824_FR`#1683; `S0826_FR`#1684; `S0827_FR`#1685 | Unmapped | B/body- |
| `Brakes` #1686 @100 | No native children | Unmapped | B/body- |
| `Shadow` #1688 @101 | `S0902`#1690 | Unmapped | B/body- |
| `Background` #1691 @102 | `S0100`#1693 | Unmapped | B/body- |

Cabin/trim-dependent groups visible through glass (separate interior scenes are outside this audit): `Stitching` #529 @48 (19 children); `Steering_Wheel` #550 @49 (78 children); `Interior_Kit` #630 @50 (1 children); `Interior` #633 @51 (54 children); `Interior_Kit` #689 @52 (41 children); `Interior` #732 @53 (29 children); `Interior_Kit` #763 @54 (79 children); `Stitching` #844 @55 (38 children); `Seat_Belts` #884 @56 (20 children); `Seats_Front` #906 @57 (168 children); `Floors` #1076 @58 (37 children); `Cluster` #1115 @59 (75 children); `IP` #1197 @61 (1 children); `Stitching` #1200 @62 (3 children); `IP` #1205 @63 (1 children); `Decal_Stickers` #1208 @64 (45 children); `IP` #1255 @65 (43 children); `Speakers` #1300 @66 (126 children); `Effects` #1435 @69 (46 children); `Steering_Wheel` #1694 @103 (27 children); `Console` #1723 @104 (6 children). Their seat/material/trim state must be recaptured for lower trims; no upper-trim interior is authorized as a substitute.

</details>

<details>
<summary>S06 — Grand Sport coupe view 02</summary>

PSB: **V/grandsport/e.coupe.exterior.02.psb**. Body-paint root index 85; spoiler root indices 2, 7, 9, 11.

<a id="s06-paint"></a>

**Paint — U; all ten base paints**

| Parent path / ID / root index | Exact paint-bearing peers (each maps only its paint token) | Native placement |
| --- | --- | --- |
| `Spoiler` #41 @7 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | S/body+ |
| `Molding` #194 @26 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Mirror_Cap` #353 @34 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Ground_Effects` #545 @46 | 40 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Roof` #594 @48 | 40 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Front_Fascia` #690 @52 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `B_Pillars` #1570 @75 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Rear_Fascia` #1603 @81 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Base` #1624 @85 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body= |
| `Mirror_Cap` #1643 @88 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body- |

<a id="s06-foundation"></a>

**Trim and body foundation**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Base` #1515 @72 | `S0507&3LT`#1517; `S0507&2LT`#1518; `S0507&1LT`#1519 | Configuration/trim candidates | B/body+ |
| `Base` #1624 @85 | `GBA`#1626; `G8G`#1627; `GKZ`#1628; `GPH`#1629; `G26`#1630; `GBK`#1631; `G4Z`#1632; `GKA`#1633; `GTR`#1634; `GEC`#1635; `1YE07`#1636 | Configuration/trim candidates | B/body= |

<a id="s06-rear"></a>

**Rear spoiler / source-off-spoiler state**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Spoiler` #13 @2 | `SIG`#15 | SIG; rest unmapped | S/body+ |
| `Spoiler` #41 @7 | `T0F`#43; `S0268`#44; `S0267&{P}` IDs [45, 46, 47, 48, 49, 50, 51, 52, 53, 54] | T0F; rest unmapped | S/body+ |
| `Spoiler` #58 @9 | `5V5`#60 | Unmapped | S/body+ |
| `Spoiler` #64 @11 | `5ZV`#66 | 5ZV; rest unmapped | S/body+ |

Source-off-spoiler state: hide every `Spoiler` parent listed here; this is a visibility recipe, **not a catalog option ID**. No legal no-spoiler configuration is established by this operation.

<a id="s06-aero"></a>

**Front/side/hood/fascia aero candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Rear_Fascia` #185 @23 | `S0204`#187 | Unmapped | B/body+ |
| `Ground_Effects` #207 @27 | `RAU`#209; `S0366`#210; `S0365`#211; `S0237`#212 | Unmapped | B/body+ |
| `Front_Fascia` #537 @43 | `S0274`#539 | Unmapped | B/body+ |
| `Front_Fascia` #543 @45 | No native children | Unmapped | B/body+ |
| `Ground_Effects` #545 @46 | `S0396`#547; `S0395`#548; `S0368`#549; `S0367`#550; `S0258&{P}` IDs [551, 552, 553, 554, 555, 556, 557, 558, 559, 560]; `S0872&{P}` IDs [561, 562, 563, 564, 565, 566, 567, 568, 569, 570]; `S0873&{P}` IDs [571, 572, 573, 574, 575, 576, 577, 578, 579, 580]; `S0278&{P}` IDs [581, 582, 583, 584, 585, 586, 587, 588, 589, 590] | Unmapped | B/body+ |
| `Front_Fascia` #690 @52 | `S0220&{P}` IDs [692, 693, 694, 695, 696, 697, 698, 699, 700, 701] | Unmapped | B/body+ |
| `Rear_Fascia` #1603 @81 | `S0203&{P}` IDs [1605, 1606, 1607, 1608, 1609, 1610, 1611, 1612, 1613, 1614] | Unmapped | B/body+ |

<a id="s06-graphics"></a>

**Stripes / decals / color candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Decals` #1 @0 | No native children | Unmapped | F/body+ |
| `Decals` #16 @3 | `S0876`#18; `S0874`#19; `S0363`#20; `S0358`#21; `S0344`#22; `S0338`#23; `S0857`#24; `S0319`#25 | Unmapped | S/body+ |
| `Decals` #29 @5 | `S0333`#31; `S0328`#32; `S0323`#33; `S0318`#34; `S0310`#35; `S0309`#36; `S0311`#37 | Unmapped | S/body+ |
| `Decals` #79 @13 | `S0877`#81; `S0837_F`#82; `S0855_F`#83; `S0302_F`#84; `S0330_F`#85; `S0325_F`#86; `S0320_F`#87; `S0315_F`#88; `S0307_F`#89; `S0860_F`#90; `S0875_F`#91; `S0880_F`#92; `S0890_F`#93; `S0893_F`#94 | Unmapped | B/body+ |
| `Stripes` #95 @14 | `S0369_F`#97 | Unmapped | B/body+ |
| `Decals` #98 @15 | `S0362_F`#100; `S0349_F`#101; `S0342_F`#102; `S0314_F`#103; `S0306_F`#104; `DZX`#105; `DZV`#106; `DZU`#107; `S0379`#108; `VPO`#109; `17A`#110; `20A`#111; `55A`#112; `75A`#113; `97A`#114; `DX4`#115; `S0866`#116; `S0858`#117; `S0361`#118; `S0348`#119; `S0341`#120; `S0334`#121; `S0313`#122 | 17A, 20A, 55A, 75A, 97A, DX4, DZU, DZV, DZX, VPO; rest unmapped | B/body+ |
| `Decals` #125 @17 | `S0332`#127; `S0327`#128; `S0322`#129; `S0317`#130; `S0304`#131; `S0303`#132; `S0881`#133; `S0894`#134; `S0861`#135; `S0308`#136; `S0882`#137; `S0838`#138; `S0862`#139; `S0895`#140; `S0360`#141; `S0347`#142; `S0340`#143; `S0329`#144; `S0312`#145; `S0331`#146; `S0326`#147; `S0321`#148; `S0316`#149; `S0301`#150; `S0300`#151; `S0859`#152; `S0305`#153 | Unmapped | B/body+ |
| `Decals` #157 @19 | `S0855_B`#159; `S0837_B`#160; `S0860_B`#161; `S0875_B`#162; `S0890_B`#163; `S0893_B`#164; `S0880_B`#165; `S0330_B`#166; `S0320_B`#167; `S0315_B`#168; `S0307_B`#169; `S0325_B`#170 | Unmapped | B/body+ |
| `Stripes` #171 @20 | `S0369_B`#173 | Unmapped | B/body+ |
| `Decals` #174 @21 | `S0362_B`#176; `S0349_B`#177; `S0342_B`#178; `S0314_B`#179; `S0306_B`#180; `S0302_B`#181 | Unmapped | B/body+ |
| `Decals` #191 @25 | `S0892`#193 | Unmapped | B/body+ |

<a id="s06-glass"></a>

**Glass and window candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Windows` #376 @38 | `S0101_R`#378; `S0108`#379; `S0101_B`#380 | Unmapped | B/body+ |
| `Defroster` #681 @49 | `S0107`#683 | Unmapped | B/body+ |
| `Windows` #684 @50 | `S0104`#686 | Unmapped | B/body+ |
| `Windows` #702 @53 | `S0122`#704 | Unmapped | B/body+ |
| `Windows` #1621 @84 | `S0105`#1623 | Unmapped | B/body+ |
| `Windows` #1640 @87 | `S0101_L`#1642 | Unmapped | B/body- |

<a id="s06-other"></a>

**Other exterior option-driven and fixed groups**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Badges` #9 @1 | `S0374`#11; `S0399`#12 | Unmapped | F/body+ |
| `None` #26 @4 | `S0343`#28 | Unmapped | S/body+ |
| `None` #38 @6 | `S0357`#40 | Unmapped | S/body+ |
| `None` #55 @8 | `S0119`#57 | Unmapped | S/body+ |
| `None` #61 @10 | `D58`#63 | Unmapped | S/body+ |
| `Badges` #67 @12 | `SL8`#69; `RIN`#70; `RIK`#71; `EYT_F`#72; `EYK_B`#73; `EYT_B`#74; `SFZ_B`#75; `S0276`#76; `S0279`#77; `R88_B`#78 | EYK, EYT, R88, RIK, RIN, SFZ, SL8; rest unmapped | B/body+ |
| `None` #123 @16 | No native children | Unmapped | B/body+ |
| `Tail_Lamps` #154 @18 | `S0200`#156 | Unmapped | B/body+ |
| `Multimedia` #182 @22 | `S0244`#184 | Unmapped | B/body+ |
| `License_Plate` #188 @24 | `S0235`#190 | Unmapped | B/body+ |
| `Molding` #194 @26 | `S0211&{P}` IDs [196, 197, 198, 199, 200, 201, 202, 203, 204, 205]; `S0209`#206 | Unmapped | B/body+ |
| `Wheels` #213 @28 | `S0820_FR`#215; `S0815_FR`#216; `S0810_FR`#217; `S0427_FR`#218; `S0426_FR`#219; `S0428_FR`#220; `S0425_FR`#221; `S0476_FR`#222; `S0497_FR`#223; `S0466_FR`#224; `S0455_FR`#225; `S0443_FR`#226; `S0442_FR`#227; `S0441_FR`#228; `S0465_FR`#229; `S0462_FR`#230; `S0453_FR`#231; `S0452_FR`#232; `S0447_FR`#233; `S0446_FR`#234; `S0471_FR`#235; `S0439_FR`#236; `S0440_FR`#237; `S0451_FR`#238; `S0450_FR`#239; `S0449_FR`#240; `S0448_FR`#241; `S0433_FR`#242; `S0434_FR`#243; `S0431_FR`#244; `S0432_FR`#245; `S0454_FR`#246; `S0397_FR`#247; `S0398_FR`#248; `S0232_FR`#249 | Unmapped | B/body+ |
| `Wheel_Caps` #250 @29 | `S0383_FR`#252; `S0264_FR`#253; `S0419_FR`#254; `S0418_FR`#255; `S0416_FR`#256; `S0415_FR`#257; `S0405_FR`#258; `S0234_FR`#259; `S0202_FR`#260; `S0251_FR`#261; `S0824_FR`#262; `S0825_FR`#263; `S0826_FR`#264; `S0828_FR`#265; `S0827_FR`#266 | Unmapped | B/body+ |
| `Brakes` #267 @30 | `S0299_FR`#269; `S0381_FR`#270; `S0291_FR`#271; `S0290_FR`#272; `S0293_FR`#273; `S0289_FR`#274; `S0288_FR`#275; `S0296_FR`#276; `S0295_FR`#277; `S0294_FR`#278; `S0292_FR`#279; `J57_FR`#280; `J56_FR`#281; `JX6_FR`#282 | J56, J57, JX6; rest unmapped | B/body+ |
| `Wheels` #283 @31 | `S0820_RR`#285; `S0815_RR`#286; `S0427_RR`#287; `S0426_RR`#288; `S0428_RR`#289; `S0425_RR`#290; `S0810_RR`#291; `S0455_RR`#292; `S0443_RR`#293; `S0442_RR`#294; `S0441_RR`#295; `S0465_RR`#296; `S0466_RR`#297; `S0453_RR`#298; `S0452_RR`#299; `S0447_RR`#300; `S0446_RR`#301; `S0439_RR`#302; `S0440_RR`#303; `S0451_RR`#304; `S0450_RR`#305; `S0449_RR`#306; `S0448_RR`#307; `S0433_RR`#308; `S0434_RR`#309; `S0431_RR`#310; `S0432_RR`#311; `S0454_RR`#312; `S0462_RR`#313; `S0471_RR`#314; `S0476_RR`#315; `S0497_RR`#316; `S0397_RR`#317; `S0398_RR`#318; `S0232_RR`#319 | Unmapped | B/body+ |
| `Wheel_Caps` #320 @32 | `S0234_RR`#322; `S0202_RR`#323; `S0251_RR`#324; `S0383_RR`#325; `S0264_RR`#326; `S0419_RR`#327; `S0418_RR`#328; `S0416_RR`#329; `S0415_RR`#330; `S0405_RR`#331; `S0824_RR`#332; `S0825_RR`#333; `S0826_RR`#334; `S0828_RR`#335; `S0827_RR`#336 | Unmapped | B/body+ |
| `Brakes` #337 @33 | `S0381_RR`#339; `S0299_RR`#340; `S0289_RR`#341; `S0293_RR`#342; `S0292_RR`#343; `S0288_RR`#344; `S0296_RR`#345; `S0295_RR`#346; `S0294_RR`#347; `S0291_RR`#348; `S0290_RR`#349; `J56_RR`#350; `JX6_RR`#351; `J57_RR`#352 | J56, J57, JX6; rest unmapped | B/body+ |
| `Mirror_Cap` #353 @34 | `S0102_R&{P}` IDs [355, 356, 357, 358, 359, 360, 361, 362, 363, 364]; `5JR_R`#365 | 5JR; rest unmapped | B/body+ |
| `Mirrors` #366 @35 | No native children | Unmapped | B/body+ |
| `Mirror_Cap` #368 @36 | `DRG_R`#370 | DRG; rest unmapped | B/body+ |
| `Mirrors` #371 @37 | `VA5`#373; `DYX_R`#374; `DWK_R`#375 | DWK, DYX; rest unmapped | B/body+ |
| `Doors` #381 @39 | `S0559&HTE`#383; `S0559&HTT`#384; `S0559&HU1`#385; `S0559&HMO`#386; `S0559&HU9`#387; `S0559&HZB`#388; `S0559&HVT`#389; `S0559&HUA`#390; `S0559&HU2`#391; `S0559&HZP`#392; `S0559&HTG`#393; `S0559&HZN`#394; `S0559&HUF`#395; `S0559&HU0`#396; `S0559&HXO`#397; `S0559&HUW`#398; `S0559&HUX`#399; `S0559&HVZ`#400; `S0559&H8T`#401; `S0559&HUB`#402; `S0559&HUC`#403; `S0559&EPX`#404; `S0559&EJH`#405; `S0559&HAG`#406; `S0559&EL9`#407 | Unmapped | B/body+ |
| `None` #534 @42 | `S0420`#536 | Unmapped | B/body+ |
| `Badges` #540 @44 | `S0271`#542 | Unmapped | B/body+ |
| `None` #591 @47 | `VSN`#593 | Unmapped | B/body+ |
| `Roof` #594 @48 | `SBT`#596; `S0243&{P}` IDs [597, 598, 599, 600, 601, 602, 603, 604, 605, 606]; `C2Z&{P}` IDs [607, 608, 609, 610, 611, 612, 613, 614, 615, 616]; `CF7&{P}` IDs [617, 618, 619, 620, 621, 622, 623, 624, 625, 626]; `CF8&{P}` IDs [627, 628, 629, 630, 631, 632, 633, 634, 635, 636]; `CC3`#637; `S0506`#638; `UG1&HUV`#639; `UG1&HU7`#640; `UG1&HUL`#641; `UG1&HUR`#642; `UG1&HUK`#643; `UG1&HU6`#644; `UG1&HUN`#645; `UG1&HTP`#646; `UG1&H1Y`#647; `UG1&HTE`#648; `UG1&HTT`#649; `UG1&HVV`#650; `UG1&HU1`#651; `UG1&HMO`#652; `UG1&HU9`#653; `UG1&HZB`#654; `UG1&HVT`#655; `UG1&HUA`#656; `UG1&HU2`#657; `UG1&HUU`#658; `UG1&HZP`#659; `UG1&HUE`#660; `UG1&HTG`#661; `UG1&HZN`#662; `UG1&HUF`#663; `UG1&HU0`#664; `UG1&HXO`#665; `UG1&HNK`#666; `UG1&HUW`#667; `UG1&HUX`#668; `UG1&HVZ`#669; `UG1&H8T`#670; `UG1&HUB`#671; `UG1&HUC`#672; `UG1&EPX`#673; `UG1&EJH`#674; `UG1&HAG`#675; `UG1&EL9`#676; `UG1&HTA`#677; `UG1&HTM`#678; `UG1&HTQ`#679; `UG1&HTN`#680 | C2Z, CC3, CF7, CF8, SBT, UG1; rest unmapped | B/body+ |
| `Headlamps` #687 @51 | `T4L`#689 | T4L; rest unmapped | B/body+ |
| `Badges` #1331 @67 | `CFX`#1333; `BV4`#1334 | BV4, CFX; rest unmapped | B/body+ |
| `Radio` #1520 @73 | No native children | Unmapped | B/body+ |
| `B_Pillars` #1570 @75 | `S0212&{P}` IDs [1572, 1573, 1574, 1575, 1576, 1577, 1578, 1579, 1580, 1581] | Unmapped | B/body+ |
| `Engine` #1582 @76 | `BC4`#1584 | BC4; rest unmapped | B/body+ |
| `Badges` #1585 @77 | `S0270`#1587 | Unmapped | B/body+ |
| `Engine` #1588 @78 | `S0111`#1590; `LS6`#1591 | LS6; rest unmapped | B/body+ |
| `Tow_Hooks` #1592 @79 | `S0870`#1594; `S0871`#1595 | Unmapped | B/body+ |
| `Exhaust` #1596 @80 | `S0865`#1598; `S0229`#1599; `S0867`#1600; `S0868`#1601; `WUB`#1602 | WUB; rest unmapped | B/body+ |
| `Splashguards` #1615 @82 | `S0390`#1617 | Unmapped | B/body+ |
| `Primer` #1618 @83 | `S0115`#1620 | Unmapped | B/body+ |
| `Grille` #1637 @86 | `VWE`#1639 | VWE; rest unmapped | B/body- |
| `Mirror_Cap` #1643 @88 | `S0102_L&{P}` IDs [1645, 1646, 1647, 1648, 1649, 1650, 1651, 1652, 1653, 1654]; `5JR_L`#1655 | 5JR; rest unmapped | B/body- |
| `Mirrors` #1656 @89 | No native children | Unmapped | B/body- |
| `Mirror_Cap` #1658 @90 | `DRG_L`#1660 | DRG; rest unmapped | B/body- |
| `Mirrors` #1661 @91 | `DYX_L`#1663; `DWK_L`#1664 | DWK, DYX; rest unmapped | B/body- |
| `Wheels` #1665 @92 | `S0820_RL`#1667; `S0815_RL`#1668; `S0810_RL`#1669; `S0455_RL`#1670; `S0443_RL`#1671; `S0441_RL`#1672; `S0462_RL`#1673; `S0442_RL`#1674; `S0446_RL`#1675; `S0433_RL`#1676; `S0431_RL`#1677; `S0432_RL`#1678; `S0426_RL`#1679; `S0425_RL`#1680; `S0476_RL`#1681; `S0497_RL`#1682; `S0471_RL`#1683; `S0398_RL`#1684 | Unmapped | B/body- |
| `Wheel_Caps` #1685 @93 | `S0383_RL`#1687; `S0264_RL`#1688; `S0419_RL`#1689; `S0418_RL`#1690; `S0415_RL`#1691; `S0234_RL`#1692; `S0251_RL`#1693; `S0826_RL`#1694; `S0828_RL`#1695 | Unmapped | B/body- |
| `Brakes` #1696 @94 | `S0299_RL`#1698; `S0292_RL`#1699; `S0293_RL`#1700; `S0288_RL`#1701; `S0296_RL`#1702; `S0294_RL`#1703; `J57_RL`#1704 | J57; rest unmapped | B/body- |
| `Wheels` #1705 @95 | `S0820_FL`#1707; `S0815_FL`#1708; `S0426_FL`#1709; `S0428_FL`#1710; `S0455_FL`#1711; `S0465_FL`#1712; `S0446_FL`#1713; `S0440_FL`#1714; `S0451_FL`#1715; `S0232_FL`#1716 | Unmapped | B/body- |
| `Wheel_Caps` #1717 @96 | `S0251_FL`#1719; `S0824_FL`#1720; `S0826_FL`#1721; `S0383_FL`#1722; `S0415_FL`#1723 | Unmapped | B/body- |
| `Brakes` #1724 @97 | `S0292_FL`#1726; `S0288_FL`#1727; `S0295_FL`#1728; `S0293_FL`#1729; `S0381_FL`#1730; `J57_FL`#1731; `J56_FL`#1732 | J56, J57; rest unmapped | B/body- |
| `Shadow` #1733 @98 | `S0902`#1735 | Unmapped | B/body- |
| `Background` #1736 @99 | `S0100`#1738 | Unmapped | B/body- |
| `Tow_Hooks` #1739 @100 | `S0869`#1741 | Unmapped | B/body- |
| `Wheels` #1742 @101 | `S0816_FR`#1744; `S0816_RL`#1745; `S0816_RR`#1746 | Unmapped | B/body- |

Cabin/trim-dependent groups visible through glass (separate interior scenes are outside this audit): `Stitching` #408 @40 (3 children); `Steering_Wheel` #413 @41 (119 children); `Seat_Belts` #705 @54 (19 children); `Interior` #726 @55 (59 children); `Interior_Kit` #787 @56 (39 children); `Interior` #828 @57 (29 children); `Interior_Kit` #859 @58 (82 children); `IP` #943 @59 (1 children); `Cluster` #946 @60 (75 children); `Stitching` #1023 @61 (54 children); `Floors` #1079 @62 (42 children); `Interior_Kit` #1123 @63 (1 children); `IP` #1126 @64 (43 children); `Seats_Front` #1171 @65 (155 children); `Interior` #1328 @66 (1 children); `Speakers` #1335 @68 (119 children); `IP` #1456 @69 (1 children); `Decal_Stickers` #1459 @70 (45 children); `Console` #1506 @71 (7 children); `Effects` #1522 @74 (46 children). Their seat/material/trim state must be recaptured for lower trims; no upper-trim interior is authorized as a substitute.

</details>

<details>
<summary>S07 — Stingray convertible view 01</summary>

PSB: **V/stingray/c.convertible.exterior.01.psb**. Body-paint root index 91; spoiler root indices 79, 81, 83.

<a id="s07-paint"></a>

**Paint — U; all ten base paints**

| Parent path / ID / root index | Exact paint-bearing peers (each maps only its paint token) | Native placement |
| --- | --- | --- |
| `Tailgate` #9 @3 | 1 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Enclosure_Rear` #14 @5 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Molding` #72 @13 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Front_Fascia` #86 @14 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Air_Dam` #103 @15 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Front_Fascia` #119 @17 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Mirror_Cap` #281 @29 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `B_Pillars` #310 @36 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Rear_Fascia` #366 @47 | 20 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Tailgate` #391 @49 | 20 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Roof` #415 @50 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Tailgate` #1378 @75 | 3 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Spoiler` #1426 @81 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | S/body+ |
| `Spoiler` #1443 @83 | 20 paint-bearing children; exact names/IDs below (partial families remain explicit) | S/body+ |
| `Tailgate` #1500 @90 | 20 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Base` #1524 @91 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body= |
| `Mirror_Cap` #1541 @93 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body- |

<a id="s07-foundation"></a>

**Trim and body foundation**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Base` #1318 @70 | `S0507&3LT`#1320; `S0507&2LT`#1321; `S0507&1LT`#1322 | Configuration/trim candidates | F/body+ |
| `Base` #1524 @91 | `GBA`#1526; `G8G`#1527; `GKZ`#1528; `GPH`#1529; `G26`#1530; `GBK`#1531; `G4Z`#1532; `GKA`#1533; `GTR`#1534; `GEC`#1535; `1YC67`#1536 | Configuration/trim candidates | B/body= |

<a id="s07-rear"></a>

**Rear spoiler / source-off-spoiler state**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Spoiler` #1419 @79 | `5ZW`#1421 | 5ZW; rest unmapped | S/body+ |
| `Spoiler` #1426 @81 | `S0118`#1428; `S0117&{P}` IDs [1429, 1430, 1431, 1432, 1433, 1434, 1435, 1436, 1437, 1438]; `5V5`#1439 | Unmapped | S/body+ |
| `Spoiler` #1443 @83 | `S0116&{P}` IDs [1445, 1446, 1447, 1448, 1449, 1450, 1451, 1452, 1453, 1454]; `5ZZ`#1455; `5ZU&{P}` IDs [1456, 1457, 1458, 1459, 1460, 1461, 1462, 1463, 1464, 1465]; `S0114`#1466 | 5ZU, 5ZZ; rest unmapped | S/body+ |

Source-off-spoiler state: hide every `Spoiler` parent listed here; this is a visibility recipe, **not a catalog option ID**. Prior native no-spoiler decomposition exists for GBA/G8G/GKZ; source identity to default/ZF1 is still unqualified; renderer needs a no-spoiler branch.

<a id="s07-aero"></a>

**Front/side/hood/fascia aero candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Front_Fascia` #86 @14 | `S0233`#88; `S0272`#89; `S0227`#90; `S0224`#91; `S0223&{P}` IDs [92, 93, 94, 95, 96, 97, 98, 99, 100, 101]; `S0221`#102 | Unmapped | F/body+ |
| `Front_Fascia` #119 @17 | `S0220&{P}` IDs [121, 122, 123, 124, 125, 126, 127, 128, 129, 130] | Unmapped | F/body+ |
| `Ground_Effects` #278 @28 | `5V7`#280 | 5V7; rest unmapped | F/body+ |
| `Rear_Fascia` #366 @47 | `S0205&{P}` IDs [368, 369, 370, 371, 372, 373, 374, 375, 376, 377]; `S0204`#378; `S0203&{P}` IDs [379, 380, 381, 382, 383, 384, 385, 386, 387, 388] | Unmapped | F/body+ |

<a id="s07-graphics"></a>

**Stripes / decals / color candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Stripes` #4 @1 | No native children | Unmapped | F/body+ |
| `Decals` #6 @2 | `S0879`#8 | Unmapped | F/body+ |
| `Decals` #35 @7 | `S0837_F`#37; `S0855_F`#38; `S0302_F`#39; `S0330_F`#40; `S0325_F`#41; `S0320_F`#42; `S0315_F`#43; `S0307_F`#44 | Unmapped | F/body+ |
| `Stripes` #45 @8 | `S0369_F`#47 | Unmapped | F/body+ |
| `Decals` #48 @9 | `S0362_F`#50; `S0349_F`#51; `S0342_F`#52; `S0314_F`#53; `S0306_F`#54; `DZX`#55; `DZV`#56; `DZU`#57; `S0379`#58; `S0336`#59; `S0335`#60 | DZU, DZV, DZX; rest unmapped | F/body+ |
| `Decals` #329 @39 | `S0866`#331; `S0858`#332; `S0361`#333; `S0348`#334; `S0341`#335; `S0334`#336; `S0313`#337 | Unmapped | F/body+ |
| `Decals` #341 @41 | `S0332`#343; `S0327`#344; `S0322`#345; `S0317`#346; `S0304`#347; `S0303`#348; `S0308`#349 | Unmapped | F/body+ |
| `Decals` #1384 @76 | `S0878`#1386; `S0874`#1387; `S0364`#1388; `S0363`#1389; `S0359`#1390; `S0358`#1391; `S0346`#1392; `S0344`#1393; `S0338`#1394; `S0324`#1395; `S0339`#1396; `S0857`#1397; `S0856`#1398; `S0319`#1399; `S0356`#1400; `S0355`#1401; `S0354`#1402; `S0353`#1403; `S0351`#1404; `S0350`#1405 | Unmapped | F/body+ |
| `Decals` #1409 @78 | `S0333`#1411; `S0328`#1412; `S0323`#1413; `S0318`#1414; `S0310`#1415; `S0309`#1416; `S0311`#1417; `S0352`#1418 | Unmapped | F/body+ |
| `Decals` #1480 @87 | `S0855_B`#1482; `S0837_B`#1483; `S0330_B`#1484; `S0320_B`#1485; `S0315_B`#1486; `S0307_B`#1487; `S0325_B`#1488 | Unmapped | B/body+ |
| `Stripes` #1489 @88 | `S0369_B`#1491 | Unmapped | B/body+ |
| `Decals` #1492 @89 | `S0362_B`#1494; `S0349_B`#1495; `S0342_B`#1496; `S0314_B`#1497; `S0306_B`#1498; `S0302_B`#1499 | Unmapped | B/body+ |

<a id="s07-glass"></a>

**Glass and window candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Windows` #307 @35 | `S0105`#309 | Unmapped | F/body+ |
| `Windows` #323 @37 | `S0101_L`#325 | Unmapped | F/body+ |
| `Windows` #1372 @73 | `S0104`#1374 | Unmapped | F/body+ |
| `Defroster` #1375 @74 | `S0107`#1377 | Unmapped | F/body+ |
| `Windows` #1537 @92 | `S0101_B`#1539; `S0101_R`#1540 | Unmapped | B/body- |

<a id="s07-other"></a>

**Other exterior option-driven and fixed groups**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Tow_Hooks` #1 @0 | No native children | Unmapped | F/body+ |
| `Tailgate` #9 @3 | `S0477&GEC`#11 | Unmapped | F/body+ |
| `Engine` #12 @4 | No native children | Unmapped | F/body+ |
| `Enclosure_Rear` #14 @5 | `S0127&{P}` IDs [16, 17, 18, 19, 20, 21, 22, 23, 24, 25] | Unmapped | F/body+ |
| `Badges` #26 @6 | `SL8`#28; `RIK`#29; `EYK_F`#30; `EYT_F`#31; `SFZ_F`#32; `S0262`#33; `R88_F`#34 | EYK, EYT, R88, RIK, SFZ, SL8; rest unmapped | F/body+ |
| `Tail_Lamps` #66 @11 | `S0200`#68 | Unmapped | F/body+ |
| `Headlamps` #69 @12 | `T4L`#71 | T4L; rest unmapped | F/body+ |
| `Molding` #72 @13 | `RYQ`#74; `S0211&{P}` IDs [75, 76, 77, 78, 79, 80, 81, 82, 83, 84]; `S0209`#85 | RYQ; rest unmapped | F/body+ |
| `Air_Dam` #103 @15 | `S0903&{P}` IDs [105, 106, 107, 108, 109, 110, 111, 112, 113, 114]; `S0226`#115 | Unmapped | F/body+ |
| `Grille` #116 @16 | `VWE`#118 | VWE; rest unmapped | F/body+ |
| `Wheels` #131 @18 | `S0812_RL`#133; `S0813_RL`#134; `S0811_RL`#135; `S0814_RL`#136; `S0417_RL`#137; `S0444_RL`#138; `S0445_RL`#139; `S0474_RL`#140; `S0467_RL`#141; `S0456_RL`#142; `S0470_RL`#143; `S0469_RL`#144; `S0468_RL`#145; `S0464_RL`#146; `S0463_RL`#147; `S0459_RL`#148; `S0458_RL`#149; `S0457_RL`#150; `S0473_RL`#151; `S0472_RL`#152 | Unmapped | F/body+ |
| `Wheel_Caps` #153 @19 | `S0385_RL`#155; `S0257_RL`#156; `S0256_RL`#157; `S0238_RL`#158; `S0261_RL`#159; `S0260_RL`#160; `S0248_RL`#161; `S0246_RL`#162; `S0245_RL`#163; `S0230_RL`#164; `S0266_RL`#165; `S0265_RL`#166; `S0247_RL`#167; `S0231_RL`#168; `S0386_RL`#169; `S0413_RL`#170; `S0412_RL`#171; `S0411_RL`#172; `S0410_RL`#173; `S0409_RL`#174; `S0408_RL`#175; `S0407_RL`#176; `S0414_RL`#177; `S0404_RL`#178; `S0403_RL`#179; `S0402_RL`#180; `S0401_RL`#181; `S0400_RL`#182; `S0388_RL`#183 | Unmapped | F/body+ |
| `Brakes` #184 @20 | `S0888_RL`#186; `S0887_RL`#187; `S0284_RL`#188; `S0283_RL`#189; `S0282_RL`#190; `S0281_RL`#191; `S0252_RL`#192; `S0241_RL`#193; `S0239_RL`#194; `S0240_RL`#195; `J55_RL`#196; `JL9_RL`#197 | J55, JL9; rest unmapped | F/body+ |
| `Splashguards` #198 @21 | `VQK_RL`#200 | VQK; rest unmapped | F/body+ |
| `Wheels` #201 @22 | `S0812_FL`#203; `S0813_FL`#204; `S0811_FL`#205; `S0814_FL`#206; `S0417_FL`#207; `S0444_FL`#208; `S0445_FL`#209; `S0474_FL`#210; `S0467_FL`#211; `S0456_FL`#212; `S0473_FL`#213; `S0470_FL`#214; `S0469_FL`#215; `S0468_FL`#216; `S0464_FL`#217; `S0463_FL`#218; `S0459_FL`#219; `S0458_FL`#220; `S0457_FL`#221; `S0472_FL`#222 | Unmapped | F/body+ |
| `Wheel_Caps` #223 @23 | `S0266_FL`#225; `S0265_FL`#226; `S0257_FL`#227; `S0256_FL`#228; `S0238_FL`#229; `S0261_FL`#230; `S0248_FL`#231; `S0247_FL`#232; `S0245_FL`#233; `S0231_FL`#234; `S0230_FL`#235; `S0385_FL`#236; `S0260_FL`#237; `S0246_FL`#238; `S0386_FL`#239; `S0413_FL`#240; `S0412_FL`#241; `S0411_FL`#242; `S0410_FL`#243; `S0409_FL`#244; `S0408_FL`#245; `S0407_FL`#246; `S0414_FL`#247; `S0404_FL`#248; `S0403_FL`#249; `S0402_FL`#250; `S0401_FL`#251; `S0400_FL`#252; `S0388_FL`#253 | Unmapped | F/body+ |
| `Brakes` #254 @24 | `S0284_FL`#256; `S0283_FL`#257; `S0282_FL`#258; `S0281_FL`#259; `S0252_FL`#260; `S0241_FL`#261; `S0240_FL`#262; `S0887_FL`#263; `S0888_FL`#264; `S0239_FL`#265; `J55_FL`#266; `JL9_FL`#267 | J55, JL9; rest unmapped | F/body+ |
| `Splashguards` #268 @25 | `VQK_FL`#270 | VQK; rest unmapped | F/body+ |
| `Assist_Steps` #271 @26 | `STI`#273 | STI; rest unmapped | F/body+ |
| `Air_Dam` #274 @27 | `5W8`#276; `5VM`#277 | 5VM, 5W8; rest unmapped | F/body+ |
| `Mirror_Cap` #281 @29 | `S0102_L&{P}` IDs [283, 284, 285, 286, 287, 288, 289, 290, 291, 292] | Unmapped | F/body+ |
| `Mirrors` #293 @30 | No native children | Unmapped | F/body+ |
| `Mirror_Cap` #295 @31 | `5JR_L`#297 | 5JR; rest unmapped | F/body+ |
| `Mirrors` #298 @32 | No native children | Unmapped | F/body+ |
| `Mirror_Cap` #300 @33 | `DRG_L`#302 | DRG; rest unmapped | F/body+ |
| `Mirrors` #303 @34 | `DYX_L`#305; `DWK_L`#306 | DWK, DYX; rest unmapped | F/body+ |
| `B_Pillars` #310 @36 | `S0213`#312; `S0212&{P}` IDs [313, 314, 315, 316, 317, 318, 319, 320, 321, 322] | Unmapped | F/body+ |
| `Primer` #326 @38 | `S0115`#328 | Unmapped | F/body+ |
| `None` #338 @40 | `S0345`#340 | Unmapped | F/body+ |
| `None` #350 @42 | `S0420`#352 | Unmapped | F/body+ |
| `Splashguards` #353 @43 | `S0390`#355 | Unmapped | F/body+ |
| `None` #356 @44 | `VSN`#358 | Unmapped | F/body+ |
| `Grille_Inserts` #359 @45 | `S0254`#361; `S0253`#362 | Unmapped | F/body+ |
| `License_Plate` #363 @46 | `S0235`#365 | Unmapped | F/body+ |
| `Multimedia` #389 @48 | No native children | Unmapped | F/body+ |
| `Tailgate` #391 @49 | `S0135_L&{P}` IDs [393, 394, 395, 396, 397, 398, 399, 400, 401, 402]; `S0136_L`#403; `S0113_L`#404; `S0112_L&{P}` IDs [405, 406, 407, 408, 409, 410, 411, 412, 413, 414] | Unmapped | F/body+ |
| `Roof` #415 @50 | `S0216`#417; `CM9&{P}` IDs [418, 419, 420, 421, 422, 423, 424, 425, 426, 427]; `S0506`#428; `UG1&HUV`#429; `UG1&HU7`#430; `UG1&HUL`#431; `UG1&HUR`#432; `UG1&HUK`#433; `UG1&HU6`#434; `UG1&HUN`#435; `UG1&HTP`#436; `UG1&H1Y`#437; `UG1&HTE`#438; `UG1&HTT`#439; `UG1&HVV`#440; `UG1&HU1`#441; `UG1&HMO`#442; `UG1&HU9`#443; `UG1&HZB`#444; `UG1&HVT`#445; `UG1&HUA`#446; `UG1&HU2`#447; `UG1&HUU`#448; `UG1&HZP`#449; `UG1&HUE`#450; `UG1&HTG`#451; `UG1&HZN`#452; `UG1&HUF`#453; `UG1&HU0`#454; `UG1&HXO`#455; `UG1&HNK`#456; `UG1&HUW`#457; `UG1&HUX`#458; `UG1&HVZ`#459; `UG1&H8T`#460; `UG1&HUB`#461; `UG1&HUC`#462; `UG1&EPX`#463; `UG1&EJH`#464; `UG1&HAG`#465; `UG1&HTA`#466; `UG1&HTM`#467; `UG1&HTQ`#468; `UG1&HTN`#469 | CM9, UG1; rest unmapped | F/body+ |
| `Badges` #1088 @63 | `CFX`#1090; `S0500`#1091 | CFX; rest unmapped | F/body+ |
| `Radio` #1323 @71 | No native children | Unmapped | F/body+ |
| `Tailgate` #1378 @75 | `S0478&GEC`#1380; `S0219&GKZ`#1381; `S0219&GPH`#1382; `S0217`#1383 | Unmapped | F/body+ |
| `None` #1406 @77 | `S0343`#1408 | Unmapped | F/body+ |
| `None` #1422 @80 | `S0357`#1424; `S0119`#1425 | Unmapped | S/body+ |
| `None` #1440 @82 | `D58`#1442 | Unmapped | S/body+ |
| `Engine` #1467 @84 | `BCS`#1469; `LS6`#1470 | BCS, LS6; rest unmapped | B/body+ |
| `Exhaust` #1471 @85 | `S0229`#1473; `WUB`#1474; `S0865`#1475 | WUB; rest unmapped | B/body+ |
| `Tow_Hooks` #1476 @86 | `S0870`#1478; `S0871`#1479 | Unmapped | B/body+ |
| `Tailgate` #1500 @90 | `S0135_R&{P}` IDs [1502, 1503, 1504, 1505, 1506, 1507, 1508, 1509, 1510, 1511]; `S0136_R`#1512; `S0113_R`#1513; `S0112_R&{P}` IDs [1514, 1515, 1516, 1517, 1518, 1519, 1520, 1521, 1522, 1523] | Unmapped | B/body+ |
| `Mirror_Cap` #1541 @93 | `S0102_R&{P}` IDs [1543, 1544, 1545, 1546, 1547, 1548, 1549, 1550, 1551, 1552]; `5JR_R`#1553 | 5JR; rest unmapped | B/body- |
| `Mirrors` #1554 @94 | `UFT_R`#1556 | UFT; rest unmapped | B/body- |
| `Mirror_Cap` #1557 @95 | `DRG_R`#1559 | DRG; rest unmapped | B/body- |
| `Mirrors` #1560 @96 | `DYX_R`#1562; `DWK_R`#1563 | DWK, DYX; rest unmapped | B/body- |
| `Wheels` #1564 @97 | `S0467_RR`#1566; `S0469_RR`#1567; `S0459_RR`#1568; `S0458_RR`#1569; `S0445_RR`#1570; `S0474_RR`#1571; `S0811_RR`#1572; `S0814_RR`#1573 | Unmapped | B/body- |
| `Wheel_Caps` #1574 @98 | `S0257_RR`#1576; `S0248_RR`#1577; `S0246_RR`#1578; `S0413_RR`#1579; `S0412_RR`#1580; `S0408_RR`#1581 | Unmapped | B/body- |
| `Brakes` #1582 @99 | `S0283_RR`#1584; `S0239_RR`#1585 | Unmapped | B/body- |
| `Splashguards` #1586 @100 | No native children | Unmapped | B/body- |
| `Wheels` #1588 @101 | No native children | Unmapped | B/body- |
| `Wheel_Caps` #1590 @102 | `S0245_FR`#1592; `S0231_FR`#1593; `S0413_FR`#1594; `S0408_FR`#1595; `S0404_FR`#1596; `S0402_FR`#1597; `S0400_FR`#1598 | Unmapped | B/body- |
| `Brakes` #1599 @103 | `S0281_FR`#1601; `JL9_FR`#1602 | JL9; rest unmapped | B/body- |
| `Splashguards` #1603 @104 | No native children | Unmapped | B/body- |
| `Shadow` #1605 @105 | `S0900`#1607 | Unmapped | B/body- |
| `Background` #1608 @106 | `S0100`#1610 | Unmapped | B/body- |

Cabin/trim-dependent groups visible through glass (separate interior scenes are outside this audit): `Decal_Stickers` #61 @10 (3 children); `Stitching` #470 @51 (20 children); `Steering_Wheel` #492 @52 (81 children); `Interior_Kit` #575 @53 (1 children); `Interior` #578 @54 (48 children); `Interior_Kit` #628 @55 (38 children); `Interior` #668 @56 (28 children); `Interior_Kit` #698 @57 (77 children); `Stitching` #777 @58 (37 children); `Seat_Belts` #816 @59 (20 children); `Seats_Front` #838 @60 (162 children); `Floors` #1002 @61 (37 children); `Cluster` #1041 @62 (45 children); `IP` #1092 @64 (1 children); `Stitching` #1095 @65 (3 children); `IP` #1100 @66 (1 children); `Decal_Stickers` #1103 @67 (44 children); `IP` #1149 @68 (42 children); `Speakers` #1193 @69 (123 children); `Effects` #1325 @72 (45 children); `Console` #1611 @107 (7 children). Their seat/material/trim state must be recaptured for lower trims; no upper-trim interior is authorized as a substitute.

</details>

<details>
<summary>S08 — Stingray convertible view 02</summary>

PSB: **V/stingray/c.convertible.exterior.02.psb**. Body-paint root index 88; spoiler root indices 8, 10, 12.

<a id="s08-paint"></a>

**Paint — U; all ten base paints**

| Parent path / ID / root index | Exact paint-bearing peers (each maps only its paint token) | Native placement |
| --- | --- | --- |
| `Enclosure_Rear` #11 @4 | 9 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Spoiler` #64 @10 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | S/body+ |
| `Spoiler` #81 @12 | 20 paint-bearing children; exact names/IDs below (partial families remain explicit) | S/body+ |
| `Tailgate` #173 @22 | 30 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Rear_Fascia` #231 @27 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Molding` #247 @29 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Tailgate` #404 @39 | 20 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Mirror_Cap` #435 @42 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Front_Fascia` #560 @50 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Air_Dam` #574 @51 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Roof` #591 @54 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Front_Fascia` #655 @58 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `B_Pillars` #1493 @80 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Rear_Fascia` #1521 @84 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Base` #1542 @88 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body= |
| `Mirror_Cap` #1561 @91 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body- |

<a id="s08-foundation"></a>

**Trim and body foundation**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Base` #1439 @77 | `S0507&3LT`#1441; `S0507&2LT`#1442; `S0507&1LT`#1443 | Configuration/trim candidates | B/body+ |
| `Base` #1542 @88 | `GBA`#1544; `G8G`#1545; `GKZ`#1546; `GPH`#1547; `G26`#1548; `GBK`#1549; `G4Z`#1550; `GKA`#1551; `GTR`#1552; `GEC`#1553; `1YC67`#1554 | Configuration/trim candidates | B/body= |

<a id="s08-rear"></a>

**Rear spoiler / source-off-spoiler state**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Spoiler` #57 @8 | `5ZW`#59 | 5ZW; rest unmapped | S/body+ |
| `Spoiler` #64 @10 | `S0118`#66; `S0117&{P}` IDs [67, 68, 69, 70, 71, 72, 73, 74, 75, 76]; `5V5`#77 | Unmapped | S/body+ |
| `Spoiler` #81 @12 | `S0116&{P}` IDs [83, 84, 85, 86, 87, 88, 89, 90, 91, 92]; `5ZZ`#93; `5ZU&{P}` IDs [94, 95, 96, 97, 98, 99, 100, 101, 102, 103]; `S0114`#104 | 5ZU, 5ZZ; rest unmapped | S/body+ |

Source-off-spoiler state: hide every `Spoiler` parent listed here; this is a visibility recipe, **not a catalog option ID**. No legal no-spoiler configuration is established by this operation.

<a id="s08-aero"></a>

**Front/side/hood/fascia aero candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Rear_Fascia` #231 @27 | `S0205&{P}` IDs [233, 234, 235, 236, 237, 238, 239, 240, 241, 242]; `S0204`#243 | Unmapped | B/body+ |
| `Ground_Effects` #432 @41 | `5V7`#434 | 5V7; rest unmapped | B/body+ |
| `Front_Fascia` #560 @50 | `S0272`#562; `S0233`#563; `S0223&{P}` IDs [564, 565, 566, 567, 568, 569, 570, 571, 572, 573] | Unmapped | B/body+ |
| `Front_Fascia` #655 @58 | `S0220&{P}` IDs [657, 658, 659, 660, 661, 662, 663, 664, 665, 666] | Unmapped | B/body+ |
| `Rear_Fascia` #1521 @84 | `S0203&{P}` IDs [1523, 1524, 1525, 1526, 1527, 1528, 1529, 1530, 1531, 1532] | Unmapped | B/body+ |

<a id="s08-graphics"></a>

**Stripes / decals / color candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Stripes` #1 @0 | No native children | Unmapped | F/body+ |
| `Decals` #4 @1 | `S0494`#6 | Unmapped | F/body+ |
| `Decals` #22 @5 | `S0878`#24; `S0874`#25; `S0364`#26; `S0363`#27; `S0359`#28; `S0358`#29; `S0346`#30; `S0344`#31; `S0338`#32; `S0324`#33; `S0339`#34; `S0857`#35; `S0856`#36; `S0319`#37; `S0356`#38; `S0355`#39; `S0354`#40; `S0353`#41; `S0351`#42; `S0350`#43 | Unmapped | F/body+ |
| `Decals` #47 @7 | `S0333`#49; `S0328`#50; `S0323`#51; `S0318`#52; `S0310`#53; `S0309`#54; `S0311`#55; `S0352`#56 | Unmapped | F/body+ |
| `Decals` #118 @14 | `S0837_F`#120; `S0855_F`#121; `S0302_F`#122; `S0330_F`#123; `S0325_F`#124; `S0320_F`#125; `S0315_F`#126; `S0307_F`#127 | Unmapped | B/body+ |
| `Stripes` #128 @15 | `S0369_F`#130 | Unmapped | B/body+ |
| `Decals` #131 @16 | `S0362_F`#133; `S0349_F`#134; `S0342_F`#135; `S0314_F`#136; `S0306_F`#137; `DZX`#138; `DZV`#139; `DZU`#140; `S0379`#141 | DZU, DZV, DZX; rest unmapped | B/body+ |
| `Decals` #147 @18 | `S0336`#149; `S0335`#150; `S0866`#151; `S0858`#152; `S0361`#153; `S0348`#154; `S0341`#155; `S0334`#156; `S0313`#157 | Unmapped | B/body+ |
| `Decals` #161 @20 | `S0332`#163; `S0327`#164; `S0322`#165; `S0317`#166; `S0304`#167; `S0303`#168; `S0308`#169 | Unmapped | B/body+ |
| `Decals` #208 @23 | `S0855_B`#210; `S0837_B`#211; `S0330_B`#212; `S0320_B`#213; `S0315_B`#214; `S0307_B`#215; `S0325_B`#216 | Unmapped | B/body+ |
| `Stripes` #217 @24 | `S0369_B`#219 | Unmapped | B/body+ |
| `Decals` #220 @25 | `S0362_B`#222; `S0349_B`#223; `S0342_B`#224; `S0314_B`#225; `S0306_B`#226; `S0302_B`#227 | Unmapped | B/body+ |

<a id="s08-glass"></a>

**Glass and window candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Windows` #458 @46 | `S0101_R`#460; `S0101_B`#461 | Unmapped | B/body+ |
| `Defroster` #646 @55 | `S0107`#648 | Unmapped | B/body+ |
| `Windows` #649 @56 | `S0104`#651 | Unmapped | B/body+ |
| `Windows` #1539 @87 | `S0105`#1541 | Unmapped | B/body+ |
| `Windows` #1558 @90 | `S0101_L`#1560 | Unmapped | B/body- |

<a id="s08-other"></a>

**Other exterior option-driven and fixed groups**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Tailgate` #7 @2 | No native children | Unmapped | F/body+ |
| `Engine` #9 @3 | No native children | Unmapped | F/body+ |
| `Enclosure_Rear` #11 @4 | `S0127&GBA`#13; `S0127&G8G`#14; `S0127&GKZ`#15; `S0127&GPH`#16; `S0127&G26`#17; `S0127&GBK`#18; `S0127&GKA`#19; `S0127&GTR`#20; `S0127&GEC`#21 | Unmapped | F/body+ |
| `None` #44 @6 | `S0343`#46 | Unmapped | F/body+ |
| `None` #60 @9 | `S0357`#62; `S0119`#63 | Unmapped | S/body+ |
| `None` #78 @11 | `D58`#80 | Unmapped | S/body+ |
| `Badges` #105 @13 | `SL8`#107; `RIN`#108; `RIK`#109; `EYT_F`#110; `EYK_B`#111; `EYT_B`#112; `SFZ_F`#113; `SFZ_B`#114; `S0263`#115; `S0262`#116; `R88_B`#117 | EYK, EYT, R88, RIK, RIN, SFZ, SL8; rest unmapped | B/body+ |
| `None` #158 @19 | `S0345`#160 | Unmapped | B/body+ |
| `Tail_Lamps` #170 @21 | `S0200`#172 | Unmapped | B/body+ |
| `Tailgate` #173 @22 | `S0135_R&{P}` IDs [175, 176, 177, 178, 179, 180, 181, 182, 183, 184]; `S0136_R`#185; `S0113_R`#186; `S0112_R&{P}` IDs [187, 188, 189, 190, 191, 192, 193, 194, 195, 196]; `S0219&{P}` IDs [197, 198, 199, 200, 201, 202, 203, 204, 205, 206]; `S0217`#207 | Unmapped | B/body+ |
| `Multimedia` #228 @26 | `S0244`#230 | Unmapped | B/body+ |
| `License_Plate` #244 @28 | `S0235`#246 | Unmapped | B/body+ |
| `Molding` #247 @29 | `RYQ`#249; `S0211&{P}` IDs [250, 251, 252, 253, 254, 255, 256, 257, 258, 259]; `S0209`#260 | RYQ; rest unmapped | B/body+ |
| `Assist_Steps` #261 @30 | `STI`#263 | STI; rest unmapped | B/body+ |
| `Splashguards` #264 @31 | `VQK_FR`#266 | VQK; rest unmapped | B/body+ |
| `Wheels` #267 @32 | `S0813_FR`#269; `S0812_FR`#270; `S0811_FR`#271; `S0814_FR`#272; `S0417_FR`#273; `S0444_FR`#274; `S0445_FR`#275; `S0474_FR`#276; `S0467_FR`#277; `S0456_FR`#278; `S0470_FR`#279; `S0468_FR`#280; `S0464_FR`#281; `S0463_FR`#282; `S0459_FR`#283; `S0458_FR`#284; `S0457_FR`#285; `S0473_FR`#286; `S0472_FR`#287; `S0469_FR`#288 | Unmapped | B/body+ |
| `Wheel_Caps` #289 @33 | `S0265_FR`#291; `S0257_FR`#292; `S0256_FR`#293; `S0238_FR`#294; `S0261_FR`#295; `S0260_FR`#296; `S0248_FR`#297; `S0247_FR`#298; `S0246_FR`#299; `S0245_FR`#300; `S0231_FR`#301; `S0230_FR`#302; `S0266_FR`#303; `S0386_FR`#304; `S0413_FR`#305; `S0412_FR`#306; `S0411_FR`#307; `S0410_FR`#308; `S0409_FR`#309; `S0408_FR`#310; `S0407_FR`#311; `S0414_FR`#312; `S0385_FR`#313; `S0404_FR`#314; `S0403_FR`#315; `S0402_FR`#316; `S0401_FR`#317; `S0400_FR`#318; `S0388_FR`#319 | Unmapped | B/body+ |
| `Brakes` #320 @34 | `S0284_FR`#322; `S0283_FR`#323; `S0282_FR`#324; `S0281_FR`#325; `S0888_FR`#326; `S0887_FR`#327; `S0252_FR`#328; `S0241_FR`#329; `S0240_FR`#330; `S0239_FR`#331; `JL9_FR`#332; `J55_FR`#333 | J55, JL9; rest unmapped | B/body+ |
| `Splashguards` #334 @35 | `VQK_RR`#336 | VQK; rest unmapped | B/body+ |
| `Wheels` #337 @36 | `S0813_RR`#339; `S0812_RR`#340; `S0811_RR`#341; `S0814_RR`#342; `S0468_RR`#343; `S0467_RR`#344; `S0456_RR`#345; `S0470_RR`#346; `S0469_RR`#347; `S0464_RR`#348; `S0463_RR`#349; `S0459_RR`#350; `S0458_RR`#351; `S0457_RR`#352; `S0473_RR`#353; `S0472_RR`#354; `S0417_RR`#355; `S0444_RR`#356; `S0445_RR`#357; `S0474_RR`#358 | Unmapped | B/body+ |
| `Wheel_Caps` #359 @37 | `S0266_RR`#361; `S0265_RR`#362; `S0257_RR`#363; `S0256_RR`#364; `S0238_RR`#365; `S0260_RR`#366; `S0248_RR`#367; `S0247_RR`#368; `S0246_RR`#369; `S0245_RR`#370; `S0231_RR`#371; `S0230_RR`#372; `S0261_RR`#373; `S0386_RR`#374; `S0385_RR`#375; `S0413_RR`#376; `S0412_RR`#377; `S0411_RR`#378; `S0410_RR`#379; `S0409_RR`#380; `S0408_RR`#381; `S0407_RR`#382; `S0414_RR`#383; `S0404_RR`#384; `S0403_RR`#385; `S0402_RR`#386; `S0401_RR`#387; `S0400_RR`#388; `S0388_RR`#389 | Unmapped | B/body+ |
| `Brakes` #390 @38 | `S0888_RR`#392; `S0887_RR`#393; `S0284_RR`#394; `S0283_RR`#395; `S0282_RR`#396; `S0281_RR`#397; `S0252_RR`#398; `S0241_RR`#399; `S0240_RR`#400; `S0239_RR`#401; `J55_RR`#402; `JL9_RR`#403 | J55, JL9; rest unmapped | B/body+ |
| `Tailgate` #404 @39 | `S0135_L&{P}` IDs [406, 407, 408, 409, 410, 411, 412, 413, 414, 415]; `S0136_L`#416; `S0113_L`#417; `S0112_L&{P}` IDs [418, 419, 420, 421, 422, 423, 424, 425, 426, 427] | Unmapped | B/body+ |
| `Air_Dam` #428 @40 | `5W8`#430; `5VM`#431 | 5VM, 5W8; rest unmapped | B/body+ |
| `Mirror_Cap` #435 @42 | `S0102_R&{P}` IDs [437, 438, 439, 440, 441, 442, 443, 444, 445, 446]; `5JR_R`#447 | 5JR; rest unmapped | B/body+ |
| `Mirrors` #448 @43 | No native children | Unmapped | B/body+ |
| `Mirror_Cap` #450 @44 | `DRG_R`#452 | DRG; rest unmapped | B/body+ |
| `Mirrors` #453 @45 | `VA5`#455; `DYX_R`#456; `DWK_R`#457 | DWK, DYX; rest unmapped | B/body+ |
| `None` #557 @49 | `S0420`#559 | Unmapped | B/body+ |
| `Air_Dam` #574 @51 | `S0903&{P}` IDs [576, 577, 578, 579, 580, 581, 582, 583, 584, 585]; `S0226`#586 | Unmapped | B/body+ |
| `None` #587 @52 | No native children | Unmapped | B/body+ |
| `Grille_Inserts` #589 @53 | No native children | Unmapped | B/body+ |
| `Roof` #591 @54 | `S0216`#593; `CM9&{P}` IDs [594, 595, 596, 597, 598, 599, 600, 601, 602, 603]; `S0506`#604; `UG1&HUV`#605; `UG1&HU7`#606; `UG1&HUL`#607; `UG1&HUR`#608; `UG1&HUK`#609; `UG1&HU6`#610; `UG1&HUN`#611; `UG1&HTP`#612; `UG1&H1Y`#613; `UG1&HTE`#614; `UG1&HTT`#615; `UG1&HVV`#616; `UG1&HU1`#617; `UG1&HMO`#618; `UG1&HU9`#619; `UG1&HZB`#620; `UG1&HVT`#621; `UG1&HUA`#622; `UG1&HU2`#623; `UG1&HUU`#624; `UG1&HZP`#625; `UG1&HUE`#626; `UG1&HTG`#627; `UG1&HZN`#628; `UG1&HUF`#629; `UG1&HU0`#630; `UG1&HXO`#631; `UG1&HNK`#632; `UG1&HUW`#633; `UG1&HUX`#634; `UG1&HVZ`#635; `UG1&H8T`#636; `UG1&HUB`#637; `UG1&HUC`#638; `UG1&EPX`#639; `UG1&EJH`#640; `UG1&HAG`#641; `UG1&HTA`#642; `UG1&HTM`#643; `UG1&HTQ`#644; `UG1&HTN`#645 | CM9, UG1; rest unmapped | B/body+ |
| `Headlamps` #652 @57 | `T4L`#654 | T4L; rest unmapped | B/body+ |
| `Badges` #1260 @72 | `CFX`#1262; `BV4`#1263; `S0500`#1264 | BV4, CFX; rest unmapped | B/body+ |
| `Radio` #1444 @78 | No native children | Unmapped | B/body+ |
| `B_Pillars` #1493 @80 | `S0213`#1495; `S0212&{P}` IDs [1496, 1497, 1498, 1499, 1500, 1501, 1502, 1503, 1504, 1505] | Unmapped | B/body+ |
| `Engine` #1506 @81 | `BC7`#1508; `LS6`#1509 | BC7, LS6; rest unmapped | B/body+ |
| `Tow_Hooks` #1510 @82 | `S0870`#1512; `S0871`#1513 | Unmapped | B/body+ |
| `Exhaust` #1514 @83 | `S0865`#1516; `S0229`#1517; `S0867`#1518; `S0868`#1519; `WUB`#1520 | WUB; rest unmapped | B/body+ |
| `Splashguards` #1533 @85 | `S0390`#1535 | Unmapped | B/body+ |
| `Primer` #1536 @86 | `S0115`#1538 | Unmapped | B/body+ |
| `Grille` #1555 @89 | `VWE`#1557 | VWE; rest unmapped | B/body- |
| `Mirror_Cap` #1561 @91 | `S0102_L&{P}` IDs [1563, 1564, 1565, 1566, 1567, 1568, 1569, 1570, 1571, 1572]; `5JR_L`#1573 | 5JR; rest unmapped | B/body- |
| `Mirrors` #1574 @92 | No native children | Unmapped | B/body- |
| `Mirror_Cap` #1576 @93 | `DRG_L`#1578 | DRG; rest unmapped | B/body- |
| `Mirrors` #1579 @94 | `DYX_L`#1581; `DWK_L`#1582 | DWK, DYX; rest unmapped | B/body- |
| `Wheels` #1583 @95 | `S0417_RL`#1585; `S0444_RL`#1586; `S0445_RL`#1587; `S0474_RL`#1588; `S0467_RL`#1589; `S0456_RL`#1590; `S0470_RL`#1591; `S0469_RL`#1592; `S0468_RL`#1593; `S0464_RL`#1594; `S0463_RL`#1595; `S0459_RL`#1596; `S0458_RL`#1597; `S0457_RL`#1598; `S0473_RL`#1599; `S0472_RL`#1600 | Unmapped | B/body- |
| `Wheel_Caps` #1601 @96 | `S0245_RL`#1603; `S0230_RL`#1604; `S0265_RL`#1605; `S0231_RL`#1606; `S0386_RL`#1607; `S0413_RL`#1608; `S0409_RL`#1609; `S0408_RL`#1610; `S0414_RL`#1611; `S0404_RL`#1612; `S0403_RL`#1613 | Unmapped | B/body- |
| `Brakes` #1614 @97 | `S0887_RL`#1616; `S0252_RL`#1617; `S0240_RL`#1618 | Unmapped | B/body- |
| `Splashguards` #1619 @98 | No native children | Unmapped | B/body- |
| `Wheels` #1621 @99 | `S0811_FL`#1623; `S0417_FL`#1624; `S0444_FL`#1625; `S0445_FL`#1626; `S0474_FL`#1627; `S0467_FL`#1628; `S0473_FL`#1629; `S0470_FL`#1630; `S0469_FL`#1631; `S0468_FL`#1632; `S0472_FL`#1633 | Unmapped | B/body- |
| `Wheel_Caps` #1634 @100 | `S0266_FL`#1636; `S0265_FL`#1637; `S0256_FL`#1638; `S0247_FL`#1639; `S0231_FL`#1640; `S0412_FL`#1641; `S0411_FL`#1642; `S0410_FL`#1643; `S0409_FL`#1644; `S0408_FL`#1645 | Unmapped | B/body- |
| `Brakes` #1646 @101 | No native children | Unmapped | B/body- |
| `Splashguards` #1648 @102 | No native children | Unmapped | B/body- |
| `Shadow` #1650 @103 | `S0900`#1652 | Unmapped | B/body- |
| `Background` #1653 @104 | `S0100`#1655 | Unmapped | B/body- |
| `Tow_Hooks` #1656 @105 | `S0869`#1658 | Unmapped | B/body- |

Cabin/trim-dependent groups visible through glass (separate interior scenes are outside this audit): `Decal_Stickers` #142 @17 (3 children); `Stitching` #462 @47 (3 children); `Steering_Wheel` #467 @48 (88 children); `Seat_Belts` #667 @59 (20 children); `Interior` #689 @60 (56 children); `Interior_Kit` #747 @61 (41 children); `Interior` #790 @62 (25 children); `Interior_Kit` #817 @63 (74 children); `IP` #893 @64 (1 children); `Cluster` #896 @65 (45 children); `Stitching` #943 @66 (57 children); `Floors` #1002 @67 (41 children); `Interior_Kit` #1045 @68 (1 children); `IP` #1048 @69 (42 children); `Seats_Front` #1092 @70 (163 children); `Interior` #1257 @71 (1 children); `Speakers` #1265 @73 (114 children); `IP` #1381 @74 (1 children); `Decal_Stickers` #1384 @75 (44 children); `Console` #1430 @76 (7 children); `Effects` #1446 @79 (45 children). Their seat/material/trim state must be recaptured for lower trims; no upper-trim interior is authorized as a substitute.

</details>

<details>
<summary>S09 — Stingray coupe view 01</summary>

PSB: **V/stingray/c.coupe.exterior.01.psb**. Body-paint root index 84; spoiler root indices 73, 75, 77.

<a id="s09-paint"></a>

**Paint — U; all ten base paints**

| Parent path / ID / root index | Exact paint-bearing peers (each maps only its paint token) | Native placement |
| --- | --- | --- |
| `Molding` #53 @8 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Front_Fascia` #67 @9 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Air_Dam` #84 @10 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Front_Fascia` #100 @12 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Mirror_Cap` #262 @24 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `B_Pillars` #291 @31 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Rear_Fascia` #349 @43 | 20 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Roof` #375 @45 | 40 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Spoiler` #1413 @75 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | S/body+ |
| `Spoiler` #1430 @77 | 20 paint-bearing children; exact names/IDs below (partial families remain explicit) | S/body+ |
| `Base` #1489 @84 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body= |
| `Mirror_Cap` #1505 @86 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body- |

<a id="s09-foundation"></a>

**Trim and body foundation**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Base` #1311 @65 | `S0507&3LT`#1313; `S0507&2LT`#1314 | Configuration/trim candidates | F/body+ |
| `Base` #1489 @84 | `GBA`#1491; `G8G`#1492; `GKZ`#1493; `GPH`#1494; `G26`#1495; `GBK`#1496; `G4Z`#1497; `GKA`#1498; `GTR`#1499; `GEC`#1500; `1YC07`#1501 | Configuration/trim candidates | B/body= |

<a id="s09-rear"></a>

**Rear spoiler / source-off-spoiler state**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Spoiler` #1406 @73 | `5ZW`#1408 | 5ZW; rest unmapped | S/body+ |
| `Spoiler` #1413 @75 | `S0118`#1415; `S0117&{P}` IDs [1416, 1417, 1418, 1419, 1420, 1421, 1422, 1423, 1424, 1425]; `5V5`#1426 | Unmapped | S/body+ |
| `Spoiler` #1430 @77 | `S0116&{P}` IDs [1432, 1433, 1434, 1435, 1436, 1437, 1438, 1439, 1440, 1441]; `5ZZ`#1442; `5ZU&{P}` IDs [1443, 1444, 1445, 1446, 1447, 1448, 1449, 1450, 1451, 1452]; `S0114`#1453 | 5ZU, 5ZZ; rest unmapped | S/body+ |

Source-off-spoiler state: hide every `Spoiler` parent listed here; this is a visibility recipe, **not a catalog option ID**. Prior native no-spoiler decomposition exists for GBA/G8G/GKZ; source identity to default/ZF1 is still unqualified; renderer needs a no-spoiler branch.

<a id="s09-aero"></a>

**Front/side/hood/fascia aero candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Front_Fascia` #67 @9 | `S0233`#69; `S0272`#70; `S0227`#71; `S0224`#72; `S0223&{P}` IDs [73, 74, 75, 76, 77, 78, 79, 80, 81, 82]; `S0221`#83 | Unmapped | F/body+ |
| `Front_Fascia` #100 @12 | `S0220&{P}` IDs [102, 103, 104, 105, 106, 107, 108, 109, 110, 111] | Unmapped | F/body+ |
| `Ground_Effects` #259 @23 | `5V7`#261 | 5V7; rest unmapped | F/body+ |
| `Rear_Fascia` #349 @43 | `S0205&{P}` IDs [351, 352, 353, 354, 355, 356, 357, 358, 359, 360]; `S0204`#361; `S0203&{P}` IDs [362, 363, 364, 365, 366, 367, 368, 369, 370, 371] | Unmapped | F/body+ |

<a id="s09-graphics"></a>

**Stripes / decals / color candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Decals` #16 @2 | `S0837_F`#18; `S0855_F`#19; `S0302_F`#20; `S0330_F`#21; `S0325_F`#22; `S0320_F`#23; `S0315_F`#24; `S0307_F`#25 | Unmapped | F/body+ |
| `Stripes` #26 @3 | `S0369_F`#28 | Unmapped | F/body+ |
| `Decals` #29 @4 | `S0362_F`#31; `S0349_F`#32; `S0342_F`#33; `S0314_F`#34; `S0306_F`#35; `DZX`#36; `DZV`#37; `DZU`#38; `S0379`#39; `S0336`#40; `S0335`#41 | DZU, DZV, DZX; rest unmapped | F/body+ |
| `Decals` #309 @34 | `S0866`#311; `S0858`#312; `S0361`#313; `S0348`#314; `S0341`#315; `S0334`#316; `S0313`#317 | Unmapped | F/body+ |
| `Decals` #321 @36 | `S0332`#323; `S0327`#324; `S0322`#325; `S0317`#326; `S0304`#327; `S0303`#328; `S0308`#329 | Unmapped | F/body+ |
| `Decals` #1371 @70 | `S0878`#1373; `S0874`#1374; `S0364`#1375; `S0363`#1376; `S0359`#1377; `S0358`#1378; `S0346`#1379; `S0344`#1380; `S0338`#1381; `S0324`#1382; `S0339`#1383; `S0857`#1384; `S0856`#1385; `S0319`#1386; `S0356`#1387; `S0355`#1388; `S0354`#1389; `S0353`#1390; `S0351`#1391; `S0350`#1392 | Unmapped | F/body+ |
| `Decals` #1396 @72 | `S0333`#1398; `S0328`#1399; `S0323`#1400; `S0318`#1401; `S0310`#1402; `S0309`#1403; `S0311`#1404; `S0352`#1405 | Unmapped | F/body+ |
| `Decals` #1466 @81 | `S0837_B`#1468; `S0325_B`#1469 | Unmapped | B/body+ |
| `Stripes` #1470 @82 | No native children | Unmapped | B/body+ |
| `Decals` #1472 @83 | `S0342_B`#1474; `S0838`#1475; `S0360`#1476; `S0347`#1477; `S0340`#1478; `S0329`#1479; `S0312`#1480; `S0331`#1481; `S0326`#1482; `S0321`#1483; `S0316`#1484; `S0301`#1485; `S0300`#1486; `S0859`#1487; `S0305`#1488 | Unmapped | B/body+ |

<a id="s09-glass"></a>

**Glass and window candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Windows` #288 @30 | `S0105`#290 | Unmapped | F/body+ |
| `Windows` #303 @32 | `S0101_L`#305 | Unmapped | F/body+ |
| `Windows` #336 @39 | `S0108`#338 | Unmapped | F/body+ |
| `Windows` #1364 @68 | `S0122`#1366; `S0104`#1367 | Unmapped | F/body+ |
| `Defroster` #1368 @69 | `S0107`#1370 | Unmapped | F/body+ |
| `Windows` #1502 @85 | `S0101_R`#1504 | Unmapped | B/body- |

<a id="s09-other"></a>

**Other exterior option-driven and fixed groups**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Tow_Hooks` #1 @0 | No native children | Unmapped | F/body+ |
| `Badges` #4 @1 | `SL8`#6; `RIK`#7; `EYK_F`#8; `EYT_F`#9; `EYT_B`#10; `SFZ_F`#11; `S0263`#12; `S0262`#13; `R88_F`#14; `R88_B`#15 | EYK, EYT, R88, RIK, SFZ, SL8; rest unmapped | F/body+ |
| `Tail_Lamps` #47 @6 | `S0200`#49 | Unmapped | F/body+ |
| `Headlamps` #50 @7 | `T4L`#52 | T4L; rest unmapped | F/body+ |
| `Molding` #53 @8 | `RYQ`#55; `S0211&{P}` IDs [56, 57, 58, 59, 60, 61, 62, 63, 64, 65]; `S0209`#66 | RYQ; rest unmapped | F/body+ |
| `Air_Dam` #84 @10 | `S0903&{P}` IDs [86, 87, 88, 89, 90, 91, 92, 93, 94, 95]; `S0226`#96 | Unmapped | F/body+ |
| `Grille` #97 @11 | `VWE`#99 | VWE; rest unmapped | F/body+ |
| `Wheels` #112 @13 | `S0812_RL`#114; `S0813_RL`#115; `S0811_RL`#116; `S0814_RL`#117; `S0417_RL`#118; `S0444_RL`#119; `S0445_RL`#120; `S0474_RL`#121; `S0467_RL`#122; `S0456_RL`#123; `S0470_RL`#124; `S0469_RL`#125; `S0468_RL`#126; `S0464_RL`#127; `S0463_RL`#128; `S0459_RL`#129; `S0458_RL`#130; `S0457_RL`#131; `S0473_RL`#132; `S0472_RL`#133 | Unmapped | F/body+ |
| `Wheel_Caps` #134 @14 | `S0385_RL`#136; `S0257_RL`#137; `S0256_RL`#138; `S0238_RL`#139; `S0261_RL`#140; `S0260_RL`#141; `S0248_RL`#142; `S0246_RL`#143; `S0245_RL`#144; `S0230_RL`#145; `S0266_RL`#146; `S0265_RL`#147; `S0247_RL`#148; `S0231_RL`#149; `S0386_RL`#150; `S0413_RL`#151; `S0412_RL`#152; `S0411_RL`#153; `S0410_RL`#154; `S0409_RL`#155; `S0408_RL`#156; `S0407_RL`#157; `S0414_RL`#158; `S0404_RL`#159; `S0403_RL`#160; `S0402_RL`#161; `S0401_RL`#162; `S0400_RL`#163; `S0388_RL`#164 | Unmapped | F/body+ |
| `Brakes` #165 @15 | `S0888_RL`#167; `S0887_RL`#168; `S0284_RL`#169; `S0283_RL`#170; `S0282_RL`#171; `S0281_RL`#172; `S0252_RL`#173; `S0241_RL`#174; `S0239_RL`#175; `S0240_RL`#176; `J55_RL`#177; `JL9_RL`#178 | J55, JL9; rest unmapped | F/body+ |
| `Splashguards` #179 @16 | `VQK_RL`#181 | VQK; rest unmapped | F/body+ |
| `Wheels` #182 @17 | `S0812_FL`#184; `S0813_FL`#185; `S0811_FL`#186; `S0814_FL`#187; `S0417_FL`#188; `S0444_FL`#189; `S0445_FL`#190; `S0474_FL`#191; `S0467_FL`#192; `S0456_FL`#193; `S0473_FL`#194; `S0470_FL`#195; `S0469_FL`#196; `S0468_FL`#197; `S0464_FL`#198; `S0463_FL`#199; `S0459_FL`#200; `S0458_FL`#201; `S0457_FL`#202; `S0472_FL`#203 | Unmapped | F/body+ |
| `Wheel_Caps` #204 @18 | `S0266_FL`#206; `S0265_FL`#207; `S0257_FL`#208; `S0256_FL`#209; `S0238_FL`#210; `S0261_FL`#211; `S0248_FL`#212; `S0247_FL`#213; `S0245_FL`#214; `S0231_FL`#215; `S0230_FL`#216; `S0385_FL`#217; `S0260_FL`#218; `S0246_FL`#219; `S0386_FL`#220; `S0413_FL`#221; `S0412_FL`#222; `S0411_FL`#223; `S0410_FL`#224; `S0409_FL`#225; `S0408_FL`#226; `S0407_FL`#227; `S0414_FL`#228; `S0404_FL`#229; `S0403_FL`#230; `S0402_FL`#231; `S0401_FL`#232; `S0400_FL`#233; `S0388_FL`#234 | Unmapped | F/body+ |
| `Brakes` #235 @19 | `S0284_FL`#237; `S0283_FL`#238; `S0282_FL`#239; `S0281_FL`#240; `S0252_FL`#241; `S0241_FL`#242; `S0240_FL`#243; `S0887_FL`#244; `S0888_FL`#245; `S0239_FL`#246; `J55_FL`#247; `JL9_FL`#248 | J55, JL9; rest unmapped | F/body+ |
| `Splashguards` #249 @20 | `VQK_FL`#251 | VQK; rest unmapped | F/body+ |
| `Assist_Steps` #252 @21 | `STI`#254 | STI; rest unmapped | F/body+ |
| `Air_Dam` #255 @22 | `5W8`#257; `5VM`#258 | 5VM, 5W8; rest unmapped | F/body+ |
| `Mirror_Cap` #262 @24 | `S0102_L&{P}` IDs [264, 265, 266, 267, 268, 269, 270, 271, 272, 273] | Unmapped | F/body+ |
| `Mirrors` #274 @25 | No native children | Unmapped | F/body+ |
| `Mirror_Cap` #276 @26 | `5JR_L`#278 | 5JR; rest unmapped | F/body+ |
| `Mirrors` #279 @27 | No native children | Unmapped | F/body+ |
| `Mirror_Cap` #281 @28 | `DRG_L`#283 | DRG; rest unmapped | F/body+ |
| `Mirrors` #284 @29 | `DYX_L`#286; `DWK_L`#287 | DWK, DYX; rest unmapped | F/body+ |
| `B_Pillars` #291 @31 | `S0212&{P}` IDs [293, 294, 295, 296, 297, 298, 299, 300, 301, 302] | Unmapped | F/body+ |
| `Primer` #306 @33 | `S0115`#308 | Unmapped | F/body+ |
| `None` #318 @35 | `S0345`#320 | Unmapped | F/body+ |
| `None` #330 @37 | `S0420`#332 | Unmapped | F/body+ |
| `Splashguards` #333 @38 | `S0390`#335 | Unmapped | F/body+ |
| `None` #339 @40 | `VSN`#341 | Unmapped | F/body+ |
| `Grille_Inserts` #342 @41 | `S0254`#344; `S0253`#345 | Unmapped | F/body+ |
| `License_Plate` #346 @42 | `S0235`#348 | Unmapped | F/body+ |
| `Multimedia` #372 @44 | `S0244`#374 | Unmapped | F/body+ |
| `Roof` #375 @45 | `SBT`#377; `S0243&{P}` IDs [378, 379, 380, 381, 382, 383, 384, 385, 386, 387]; `C2Z&{P}` IDs [388, 389, 390, 391, 392, 393, 394, 395, 396, 397]; `CF7&{P}` IDs [398, 399, 400, 401, 402, 403, 404, 405, 406, 407]; `CF8&{P}` IDs [408, 409, 410, 411, 412, 413, 414, 415, 416, 417]; `CC3`#418; `S0506`#419; `UG1&HUV`#420; `UG1&HU7`#421; `UG1&HUL`#422; `UG1&HUR`#423; `UG1&HUK`#424; `UG1&HU6`#425; `UG1&HUN`#426; `UG1&HTP`#427; `UG1&H1Y`#428; `UG1&HTE`#429; `UG1&HTT`#430; `UG1&HVV`#431; `UG1&HU1`#432; `UG1&HMO`#433; `UG1&HU9`#434; `UG1&HZB`#435; `UG1&HVT`#436; `UG1&HUA`#437; `UG1&HU2`#438; `UG1&HUU`#439; `UG1&HZP`#440; `UG1&HUE`#441; `UG1&HTG`#442; `UG1&HZN`#443; `UG1&HUF`#444; `UG1&HU0`#445; `UG1&HXO`#446; `UG1&HNK`#447; `UG1&HUW`#448; `UG1&HUX`#449; `UG1&HVZ`#450; `UG1&H8T`#451; `UG1&HUB`#452; `UG1&HUC`#453; `UG1&EPX`#454; `UG1&EJH`#455; `UG1&HAG`#456; `UG1&HTA`#457; `UG1&HTM`#458; `UG1&HTQ`#459; `UG1&HTN`#460 | C2Z, CC3, CF7, CF8, SBT, UG1; rest unmapped | F/body+ |
| `Badges` #1080 @58 | `CFX`#1082; `BV4`#1083; `S0500`#1084 | BV4, CFX; rest unmapped | F/body+ |
| `Radio` #1315 @66 | No native children | Unmapped | F/body+ |
| `None` #1393 @71 | `S0343`#1395 | Unmapped | F/body+ |
| `None` #1409 @74 | `S0357`#1411; `S0119`#1412 | Unmapped | S/body+ |
| `None` #1427 @76 | `D58`#1429 | Unmapped | S/body+ |
| `Engine` #1454 @78 | `LS6`#1456 | LS6; rest unmapped | B/body+ |
| `Exhaust` #1457 @79 | `S0229`#1459; `WUB`#1460; `S0865`#1461 | WUB; rest unmapped | B/body+ |
| `Tow_Hooks` #1462 @80 | `S0870`#1464; `S0871`#1465 | Unmapped | B/body+ |
| `Mirror_Cap` #1505 @86 | `S0102_R&{P}` IDs [1507, 1508, 1509, 1510, 1511, 1512, 1513, 1514, 1515, 1516]; `5JR_R`#1517 | 5JR; rest unmapped | B/body- |
| `Mirrors` #1518 @87 | `UFT_R`#1520 | UFT; rest unmapped | B/body- |
| `Mirror_Cap` #1521 @88 | `DRG_R`#1523 | DRG; rest unmapped | B/body- |
| `Mirrors` #1524 @89 | `DYX_R`#1526; `DWK_R`#1527 | DWK, DYX; rest unmapped | B/body- |
| `Wheels` #1528 @90 | `S0468_RR`#1530; `S0464_RR`#1531; `S0445_RR`#1532 | Unmapped | B/body- |
| `Wheel_Caps` #1533 @91 | `S0265_RR`#1535; `S0238_RR`#1536; `S0247_RR`#1537; `S0246_RR`#1538; `S0403_RR`#1539; `S0401_RR`#1540; `S0400_RR`#1541 | Unmapped | B/body- |
| `Brakes` #1542 @92 | `S0888_RR`#1544 | Unmapped | B/body- |
| `Splashguards` #1545 @93 | No native children | Unmapped | B/body- |
| `Wheels` #1547 @94 | `S0811_FR`#1549; `S0463_FR`#1550; `S0458_FR`#1551; `S0472_FR`#1552 | Unmapped | B/body- |
| `Wheel_Caps` #1553 @95 | `S0245_FR`#1555; `S0231_FR`#1556; `S0411_FR`#1557; `S0410_FR`#1558; `S0414_FR`#1559; `S0404_FR`#1560; `S0402_FR`#1561; `S0401_FR`#1562 | Unmapped | B/body- |
| `Brakes` #1563 @96 | `S0283_FR`#1565; `S0887_FR`#1566; `J55_FR`#1567 | J55; rest unmapped | B/body- |
| `Splashguards` #1568 @97 | No native children | Unmapped | B/body- |
| `Shadow` #1570 @98 | `S0900`#1572 | Unmapped | B/body- |
| `Background` #1573 @99 | `S0100`#1575 | Unmapped | B/body- |

Cabin/trim-dependent groups visible through glass (separate interior scenes are outside this audit): `Decal_Stickers` #42 @5 (3 children); `Stitching` #461 @46 (18 children); `Steering_Wheel` #481 @47 (83 children); `Interior_Kit` #566 @48 (1 children); `Interior` #569 @49 (55 children); `Interior_Kit` #626 @50 (33 children); `Interior` #661 @51 (28 children); `Interior_Kit` #691 @52 (76 children); `Stitching` #769 @53 (37 children); `Seat_Belts` #808 @54 (20 children); `Seats_Front` #830 @55 (162 children); `Floors` #994 @56 (37 children); `Cluster` #1033 @57 (45 children); `IP` #1085 @59 (1 children); `Stitching` #1088 @60 (3 children); `IP` #1093 @61 (1 children); `Decal_Stickers` #1096 @62 (44 children); `IP` #1142 @63 (42 children); `Speakers` #1186 @64 (123 children); `Effects` #1317 @67 (45 children); `Console` #1576 @100 (7 children). Their seat/material/trim state must be recaptured for lower trims; no upper-trim interior is authorized as a substitute.

</details>

<details>
<summary>S10 — Stingray coupe view 02</summary>

PSB: **V/stingray/c.coupe.exterior.02.psb**. Body-paint root index 82; spoiler root indices 3, 5, 7.

<a id="s10-paint"></a>

**Paint — U; all ten base paints**

| Parent path / ID / root index | Exact paint-bearing peers (each maps only its paint token) | Native placement |
| --- | --- | --- |
| `Spoiler` #42 @5 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | S/body+ |
| `Spoiler` #59 @7 | 20 paint-bearing children; exact names/IDs below (partial families remain explicit) | S/body+ |
| `Rear_Fascia` #186 @21 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Molding` #202 @23 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Mirror_Cap` #366 @35 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Front_Fascia` #491 @43 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Air_Dam` #505 @44 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Roof` #524 @47 | 40 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Front_Fascia` #619 @51 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `B_Pillars` #1430 @74 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Rear_Fascia` #1456 @78 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Base` #1477 @82 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body= |
| `Mirror_Cap` #1496 @85 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body- |

<a id="s10-foundation"></a>

**Trim and body foundation**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Base` #1376 @71 | `S0507&3LT`#1378; `S0507&2LT`#1379; `S0507&1LT`#1380 | Configuration/trim candidates | B/body+ |
| `Base` #1477 @82 | `GBA`#1479; `G8G`#1480; `GKZ`#1481; `GPH`#1482; `G26`#1483; `GBK`#1484; `G4Z`#1485; `GKA`#1486; `GTR`#1487; `GEC`#1488; `1YC07`#1489 | Configuration/trim candidates | B/body= |

<a id="s10-rear"></a>

**Rear spoiler / source-off-spoiler state**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Spoiler` #35 @3 | `5ZW`#37 | 5ZW; rest unmapped | S/body+ |
| `Spoiler` #42 @5 | `S0118`#44; `S0117&{P}` IDs [45, 46, 47, 48, 49, 50, 51, 52, 53, 54]; `5V5`#55 | Unmapped | S/body+ |
| `Spoiler` #59 @7 | `S0116&{P}` IDs [61, 62, 63, 64, 65, 66, 67, 68, 69, 70]; `5ZZ`#71; `5ZU&{P}` IDs [72, 73, 74, 75, 76, 77, 78, 79, 80, 81]; `S0114`#82 | 5ZU, 5ZZ; rest unmapped | S/body+ |

Source-off-spoiler state: hide every `Spoiler` parent listed here; this is a visibility recipe, **not a catalog option ID**. No legal no-spoiler configuration is established by this operation.

<a id="s10-aero"></a>

**Front/side/hood/fascia aero candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Rear_Fascia` #186 @21 | `S0205&{P}` IDs [188, 189, 190, 191, 192, 193, 194, 195, 196, 197]; `S0204`#198 | Unmapped | B/body+ |
| `Ground_Effects` #363 @34 | `5V7`#365 | 5V7; rest unmapped | B/body+ |
| `Front_Fascia` #491 @43 | `S0272`#493; `S0233`#494; `S0223&{P}` IDs [495, 496, 497, 498, 499, 500, 501, 502, 503, 504] | Unmapped | B/body+ |
| `Front_Fascia` #619 @51 | `S0220&{P}` IDs [621, 622, 623, 624, 625, 626, 627, 628, 629, 630] | Unmapped | B/body+ |
| `Rear_Fascia` #1456 @78 | `S0203&{P}` IDs [1458, 1459, 1460, 1461, 1462, 1463, 1464, 1465, 1466, 1467] | Unmapped | B/body+ |

<a id="s10-graphics"></a>

**Stripes / decals / color candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Decals` #1 @0 | No native children | Unmapped | F/body+ |
| `Decals` #25 @2 | `S0333`#27; `S0328`#28; `S0323`#29; `S0318`#30; `S0310`#31; `S0309`#32; `S0311`#33; `S0352`#34 | Unmapped | F/body+ |
| `Decals` #94 @9 | `S0837_F`#96; `S0855_F`#97; `S0302_F`#98; `S0330_F`#99; `S0325_F`#100; `S0320_F`#101; `S0315_F`#102; `S0307_F`#103 | Unmapped | B/body+ |
| `Stripes` #104 @10 | `S0369_F`#106 | Unmapped | B/body+ |
| `Decals` #107 @11 | `S0362_F`#109; `S0349_F`#110; `S0342_F`#111; `S0314_F`#112; `S0306_F`#113; `DZX`#114; `DZV`#115; `DZU`#116; `S0379`#117 | DZU, DZV, DZX; rest unmapped | B/body+ |
| `Decals` #123 @13 | `S0336`#125; `S0335`#126; `S0866`#127; `S0858`#128; `S0361`#129; `S0348`#130; `S0341`#131; `S0334`#132; `S0313`#133 | Unmapped | B/body+ |
| `Decals` #137 @15 | `S0332`#139; `S0327`#140; `S0322`#141; `S0317`#142; `S0304`#143; `S0303`#144; `S0308`#145; `S0838`#146; `S0360`#147; `S0347`#148; `S0340`#149; `S0329`#150; `S0312`#151; `S0331`#152; `S0326`#153; `S0321`#154; `S0316`#155; `S0301`#156; `S0300`#157; `S0859`#158; `S0305`#159 | Unmapped | B/body+ |
| `Decals` #163 @17 | `S0855_B`#165; `S0837_B`#166; `S0330_B`#167; `S0320_B`#168; `S0315_B`#169; `S0307_B`#170; `S0325_B`#171 | Unmapped | B/body+ |
| `Stripes` #172 @18 | `S0369_B`#174 | Unmapped | B/body+ |
| `Decals` #175 @19 | `S0362_B`#177; `S0349_B`#178; `S0342_B`#179; `S0314_B`#180; `S0306_B`#181; `S0302_B`#182 | Unmapped | B/body+ |

<a id="s10-glass"></a>

**Glass and window candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Windows` #389 @39 | `S0101_R`#391; `S0108`#392 | Unmapped | B/body+ |
| `Defroster` #610 @48 | `S0107`#612 | Unmapped | B/body+ |
| `Windows` #613 @49 | `S0104`#615 | Unmapped | B/body+ |
| `Windows` #631 @52 | `S0122`#633 | Unmapped | B/body+ |
| `Windows` #1474 @81 | `S0105`#1476 | Unmapped | B/body+ |
| `Windows` #1493 @84 | `S0101_L`#1495 | Unmapped | B/body- |

<a id="s10-other"></a>

**Other exterior option-driven and fixed groups**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `None` #23 @1 | No native children | Unmapped | F/body+ |
| `None` #38 @4 | `S0357`#40; `S0119`#41 | Unmapped | S/body+ |
| `None` #56 @6 | `D58`#58 | Unmapped | S/body+ |
| `Badges` #83 @8 | `SL8`#85; `RIN`#86; `RIK`#87; `EYK_B`#88; `EYT_B`#89; `SFZ_F`#90; `S0263`#91; `S0262`#92; `R88_B`#93 | EYK, EYT, R88, RIK, RIN, SFZ, SL8; rest unmapped | B/body+ |
| `None` #134 @14 | `S0345`#136 | Unmapped | B/body+ |
| `Tail_Lamps` #160 @16 | `S0200`#162 | Unmapped | B/body+ |
| `Multimedia` #183 @20 | `S0244`#185 | Unmapped | B/body+ |
| `License_Plate` #199 @22 | `S0235`#201 | Unmapped | B/body+ |
| `Molding` #202 @23 | `RYQ`#204; `S0211&{P}` IDs [205, 206, 207, 208, 209, 210, 211, 212, 213, 214]; `S0209`#215 | RYQ; rest unmapped | B/body+ |
| `Assist_Steps` #216 @24 | `STI`#218 | STI; rest unmapped | B/body+ |
| `Splashguards` #219 @25 | `VQK_FR`#221 | VQK; rest unmapped | B/body+ |
| `Wheels` #222 @26 | `S0813_FR`#224; `S0812_FR`#225; `S0811_FR`#226; `S0814_FR`#227; `S0417_FR`#228; `S0444_FR`#229; `S0445_FR`#230; `S0474_FR`#231; `S0467_FR`#232; `S0456_FR`#233; `S0470_FR`#234; `S0468_FR`#235; `S0464_FR`#236; `S0463_FR`#237; `S0459_FR`#238; `S0458_FR`#239; `S0457_FR`#240; `S0473_FR`#241; `S0472_FR`#242; `S0469_FR`#243 | Unmapped | B/body+ |
| `Wheel_Caps` #244 @27 | `S0265_FR`#246; `S0257_FR`#247; `S0256_FR`#248; `S0238_FR`#249; `S0261_FR`#250; `S0260_FR`#251; `S0248_FR`#252; `S0247_FR`#253; `S0246_FR`#254; `S0245_FR`#255; `S0231_FR`#256; `S0230_FR`#257; `S0266_FR`#258; `S0386_FR`#259; `S0413_FR`#260; `S0412_FR`#261; `S0411_FR`#262; `S0410_FR`#263; `S0409_FR`#264; `S0408_FR`#265; `S0407_FR`#266; `S0414_FR`#267; `S0385_FR`#268; `S0404_FR`#269; `S0403_FR`#270; `S0402_FR`#271; `S0401_FR`#272; `S0400_FR`#273; `S0388_FR`#274 | Unmapped | B/body+ |
| `Brakes` #275 @28 | `S0284_FR`#277; `S0283_FR`#278; `S0282_FR`#279; `S0281_FR`#280; `S0888_FR`#281; `S0887_FR`#282; `S0252_FR`#283; `S0241_FR`#284; `S0240_FR`#285; `S0239_FR`#286; `JL9_FR`#287; `J55_FR`#288 | J55, JL9; rest unmapped | B/body+ |
| `Splashguards` #289 @29 | `VQK_RR`#291 | VQK; rest unmapped | B/body+ |
| `Wheels` #292 @30 | `S0813_RR`#294; `S0812_RR`#295; `S0811_RR`#296; `S0814_RR`#297; `S0468_RR`#298; `S0467_RR`#299; `S0456_RR`#300; `S0470_RR`#301; `S0469_RR`#302; `S0464_RR`#303; `S0463_RR`#304; `S0459_RR`#305; `S0458_RR`#306; `S0457_RR`#307; `S0473_RR`#308; `S0472_RR`#309; `S0417_RR`#310; `S0444_RR`#311; `S0445_RR`#312; `S0474_RR`#313 | Unmapped | B/body+ |
| `Wheel_Caps` #314 @31 | `S0266_RR`#316; `S0265_RR`#317; `S0257_RR`#318; `S0256_RR`#319; `S0238_RR`#320; `S0260_RR`#321; `S0248_RR`#322; `S0247_RR`#323; `S0246_RR`#324; `S0245_RR`#325; `S0231_RR`#326; `S0230_RR`#327; `S0261_RR`#328; `S0386_RR`#329; `S0385_RR`#330; `S0413_RR`#331; `S0412_RR`#332; `S0411_RR`#333; `S0410_RR`#334; `S0409_RR`#335; `S0408_RR`#336; `S0407_RR`#337; `S0414_RR`#338; `S0404_RR`#339; `S0403_RR`#340; `S0402_RR`#341; `S0401_RR`#342; `S0400_RR`#343; `S0388_RR`#344 | Unmapped | B/body+ |
| `Brakes` #345 @32 | `S0888_RR`#347; `S0887_RR`#348; `S0284_RR`#349; `S0283_RR`#350; `S0282_RR`#351; `S0281_RR`#352; `S0252_RR`#353; `S0241_RR`#354; `S0240_RR`#355; `S0239_RR`#356; `J55_RR`#357; `JL9_RR`#358 | J55, JL9; rest unmapped | B/body+ |
| `Air_Dam` #359 @33 | `5W8`#361; `5VM`#362 | 5VM, 5W8; rest unmapped | B/body+ |
| `Mirror_Cap` #366 @35 | `S0102_R&{P}` IDs [368, 369, 370, 371, 372, 373, 374, 375, 376, 377]; `5JR_R`#378 | 5JR; rest unmapped | B/body+ |
| `Mirrors` #379 @36 | No native children | Unmapped | B/body+ |
| `Mirror_Cap` #381 @37 | `DRG_R`#383 | DRG; rest unmapped | B/body+ |
| `Mirrors` #384 @38 | `VA5`#386; `DYX_R`#387; `DWK_R`#388 | DWK, DYX; rest unmapped | B/body+ |
| `None` #488 @42 | `S0420`#490 | Unmapped | B/body+ |
| `Air_Dam` #505 @44 | `S0903&{P}` IDs [507, 508, 509, 510, 511, 512, 513, 514, 515, 516]; `S0226`#517 | Unmapped | B/body+ |
| `None` #518 @45 | `VSN`#520 | Unmapped | B/body+ |
| `Grille_Inserts` #521 @46 | `S0254`#523 | Unmapped | B/body+ |
| `Roof` #524 @47 | `SBT`#526; `S0243&{P}` IDs [527, 528, 529, 530, 531, 532, 533, 534, 535, 536]; `C2Z&{P}` IDs [537, 538, 539, 540, 541, 542, 543, 544, 545, 546]; `CF7&{P}` IDs [547, 548, 549, 550, 551, 552, 553, 554, 555, 556]; `CF8&{P}` IDs [557, 558, 559, 560, 561, 562, 563, 564, 565, 566]; `CC3`#567; `S0506`#568; `UG1&HUV`#569; `UG1&HU7`#570; `UG1&HUL`#571; `UG1&HUR`#572; `UG1&HUK`#573; `UG1&HU6`#574; `UG1&HUN`#575; `UG1&HTP`#576; `UG1&H1Y`#577; `UG1&HTE`#578; `UG1&HTT`#579; `UG1&HVV`#580; `UG1&HU1`#581; `UG1&HMO`#582; `UG1&HU9`#583; `UG1&HZB`#584; `UG1&HVT`#585; `UG1&HUA`#586; `UG1&HU2`#587; `UG1&HUU`#588; `UG1&HZP`#589; `UG1&HUE`#590; `UG1&HTG`#591; `UG1&HZN`#592; `UG1&HUF`#593; `UG1&HU0`#594; `UG1&HXO`#595; `UG1&HNK`#596; `UG1&HUW`#597; `UG1&HUX`#598; `UG1&HVZ`#599; `UG1&H8T`#600; `UG1&HUB`#601; `UG1&HUC`#602; `UG1&EPX`#603; `UG1&EJH`#604; `UG1&HAG`#605; `UG1&HTA`#606; `UG1&HTM`#607; `UG1&HTQ`#608; `UG1&HTN`#609 | C2Z, CC3, CF7, CF8, SBT, UG1; rest unmapped | B/body+ |
| `Headlamps` #616 @50 | `T4L`#618 | T4L; rest unmapped | B/body+ |
| `Badges` #1200 @66 | `CFX`#1202; `BV4`#1203; `S0500`#1204 | BV4, CFX; rest unmapped | B/body+ |
| `Radio` #1381 @72 | No native children | Unmapped | B/body+ |
| `B_Pillars` #1430 @74 | `S0212&{P}` IDs [1432, 1433, 1434, 1435, 1436, 1437, 1438, 1439, 1440, 1441] | Unmapped | B/body+ |
| `Engine` #1442 @75 | `LS6`#1444 | LS6; rest unmapped | B/body+ |
| `Tow_Hooks` #1445 @76 | `S0870`#1447; `S0871`#1448 | Unmapped | B/body+ |
| `Exhaust` #1449 @77 | `S0865`#1451; `S0229`#1452; `S0867`#1453; `S0868`#1454; `WUB`#1455 | WUB; rest unmapped | B/body+ |
| `Splashguards` #1468 @79 | `S0390`#1470 | Unmapped | B/body+ |
| `Primer` #1471 @80 | `S0115`#1473 | Unmapped | B/body+ |
| `Grille` #1490 @83 | `VWE`#1492 | VWE; rest unmapped | B/body- |
| `Mirror_Cap` #1496 @85 | `S0102_L&{P}` IDs [1498, 1499, 1500, 1501, 1502, 1503, 1504, 1505, 1506, 1507]; `5JR_L`#1508 | 5JR; rest unmapped | B/body- |
| `Mirrors` #1509 @86 | No native children | Unmapped | B/body- |
| `Mirror_Cap` #1511 @87 | `DRG_L`#1513 | DRG; rest unmapped | B/body- |
| `Mirrors` #1514 @88 | `DYX_L`#1516; `DWK_L`#1517 | DWK, DYX; rest unmapped | B/body- |
| `Wheels` #1518 @89 | `S0811_RL`#1520; `S0814_RL`#1521; `S0417_RL`#1522; `S0444_RL`#1523; `S0445_RL`#1524; `S0474_RL`#1525; `S0467_RL`#1526; `S0456_RL`#1527; `S0470_RL`#1528; `S0469_RL`#1529; `S0468_RL`#1530; `S0464_RL`#1531; `S0463_RL`#1532; `S0459_RL`#1533; `S0458_RL`#1534; `S0457_RL`#1535; `S0473_RL`#1536; `S0472_RL`#1537 | Unmapped | B/body- |
| `Wheel_Caps` #1538 @90 | `S0385_RL`#1540; `S0256_RL`#1541; `S0260_RL`#1542; `S0266_RL`#1543; `S0386_RL`#1544; `S0412_RL`#1545; `S0410_RL`#1546; `S0409_RL`#1547; `S0414_RL`#1548; `S0404_RL`#1549; `S0403_RL`#1550; `S0401_RL`#1551; `S0388_RL`#1552 | Unmapped | B/body- |
| `Brakes` #1553 @91 | `S0888_RL`#1555; `S0887_RL`#1556; `S0241_RL`#1557 | Unmapped | B/body- |
| `Splashguards` #1558 @92 | No native children | Unmapped | B/body- |
| `Wheels` #1560 @93 | `S0814_FL`#1562; `S0417_FL`#1563; `S0444_FL`#1564; `S0445_FL`#1565; `S0474_FL`#1566; `S0467_FL`#1567; `S0456_FL`#1568; `S0473_FL`#1569; `S0470_FL`#1570; `S0469_FL`#1571; `S0468_FL`#1572; `S0458_FL`#1573; `S0472_FL`#1574 | Unmapped | B/body- |
| `Wheel_Caps` #1575 @94 | `S0266_FL`#1577; `S0265_FL`#1578; `S0256_FL`#1579; `S0238_FL`#1580; `S0248_FL`#1581; `S0245_FL`#1582; `S0231_FL`#1583; `S0385_FL`#1584; `S0413_FL`#1585; `S0411_FL`#1586; `S0410_FL`#1587; `S0409_FL`#1588; `S0408_FL`#1589; `S0404_FL`#1590; `S0403_FL`#1591; `S0401_FL`#1592; `S0400_FL`#1593; `S0388_FL`#1594 | Unmapped | B/body- |
| `Brakes` #1595 @95 | `S0241_FL`#1597; `S0888_FL`#1598 | Unmapped | B/body- |
| `Splashguards` #1599 @96 | No native children | Unmapped | B/body- |
| `Shadow` #1601 @97 | `S0900`#1603 | Unmapped | B/body- |
| `Background` #1604 @98 | `S0100`#1606 | Unmapped | B/body- |
| `Tow_Hooks` #1607 @99 | `S0869`#1609 | Unmapped | B/body- |

Cabin/trim-dependent groups visible through glass (separate interior scenes are outside this audit): `Decal_Stickers` #118 @12 (3 children); `Stitching` #393 @40 (3 children); `Steering_Wheel` #398 @41 (88 children); `Seat_Belts` #634 @53 (18 children); `Interior` #654 @54 (54 children); `Interior_Kit` #710 @55 (39 children); `Interior` #751 @56 (24 children); `Interior_Kit` #777 @57 (78 children); `IP` #857 @58 (1 children); `Cluster` #860 @59 (45 children); `Stitching` #907 @60 (52 children); `Floors` #961 @61 (42 children); `Interior_Kit` #1005 @62 (1 children); `IP` #1008 @63 (42 children); `Seats_Front` #1052 @64 (143 children); `Interior` #1197 @65 (1 children); `Speakers` #1205 @67 (112 children); `IP` #1319 @68 (1 children); `Decal_Stickers` #1322 @69 (44 children); `Console` #1368 @70 (6 children); `Effects` #1383 @73 (45 children). Their seat/material/trim state must be recaptured for lower trims; no upper-trim interior is authorized as a substitute.

</details>

<details>
<summary>S11 — Z06 convertible view 01</summary>

PSB: **V/z06/exterior/27CHCORZ_CON_Studio_f02.psb**. Body-paint root index 89; spoiler root indices 77, 79, 81.

<a id="s11-paint"></a>

**Paint — U; all ten base paints**

| Parent path / ID / root index | Exact paint-bearing peers (each maps only its paint token) | Native placement |
| --- | --- | --- |
| `Tailgate` #10 @3 | 3 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Enclosure_Rear` #19 @5 | 8 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Molding` #72 @12 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Front_Fascia` #86 @13 | 20 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Ground_Effects` #113 @14 | 40 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Front_Fascia` #162 @16 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Ground_Effects` #306 @23 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Mirror_Cap` #321 @24 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `B_Pillars` #350 @31 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Rear_Fascia` #406 @43 | 13 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Tailgate` #425 @45 | 20 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Roof` #449 @46 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Tailgate` #1416 @72 | 3 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Spoiler` #1446 @77 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | S/body+ |
| `Tailgate` #1503 @88 | 20 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Base` #1527 @89 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body= |
| `Mirror_Cap` #1544 @91 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body- |

<a id="s11-foundation"></a>

**Trim and body foundation**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Base` #1356 @67 | `S0507&1LZ`#1358; `S0507&3LZ`#1359; `S0507&2LZ`#1360 | Configuration/trim candidates | F/body+ |
| `Base` #1527 @89 | `GBA`#1529; `G8G`#1530; `GKZ`#1531; `GPH`#1532; `G26`#1533; `GBK`#1534; `G4Z`#1535; `GKA`#1536; `GTR`#1537; `GEC`#1538; `1YH67`#1539 | Configuration/trim candidates | B/body= |

<a id="s11-rear"></a>

**Rear spoiler / source-off-spoiler state**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Spoiler` #1446 @77 | `T0G`#1448; `T0F`#1449; `S0268`#1450; `S0267&{P}` IDs [1451, 1452, 1453, 1454, 1455, 1456, 1457, 1458, 1459, 1460]; `SIG`#1461 | SIG, T0F, T0G; rest unmapped | S/body+ |
| `Spoiler` #1465 @79 | `5V5`#1467 | 5V5; rest unmapped | S/body+ |
| `Spoiler` #1471 @81 | `5ZV`#1473 | 5ZV; rest unmapped | S/body+ |

Source-off-spoiler state: hide every `Spoiler` parent listed here; this is a visibility recipe, **not a catalog option ID**. No legal no-spoiler configuration is established by this operation.

<a id="s11-aero"></a>

**Front/side/hood/fascia aero candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Front_Fascia` #86 @13 | `S0461&{P}` IDs [88, 89, 90, 91, 92, 93, 94, 95, 96, 97]; `S0460&{P}` IDs [98, 99, 100, 101, 102, 103, 104, 105, 106, 107]; `S0274`#108; `S0273`#109; `S0227`#110; `S0224`#111; `S0221`#112 | Unmapped | F/body+ |
| `Ground_Effects` #113 @14 | `S0396`#115; `S0395`#116; `S0368`#117; `S0367`#118; `S0258&{P}` IDs [119, 120, 121, 122, 123, 124, 125, 126, 127, 128]; `S0872&{P}` IDs [129, 130, 131, 132, 133, 134, 135, 136, 137, 138]; `S0873&{P}` IDs [139, 140, 141, 142, 143, 144, 145, 146, 147, 148]; `S0278&{P}` IDs [149, 150, 151, 152, 153, 154, 155, 156, 157, 158] | Unmapped | F/body+ |
| `Front_Fascia` #162 @16 | `S0220&{P}` IDs [164, 165, 166, 167, 168, 169, 170, 171, 172, 173] | Unmapped | F/body+ |
| `Ground_Effects` #306 @23 | `S0366`#308; `S0250&{P}` IDs [309, 310, 311, 312, 313, 314, 315, 316, 317, 318]; `S0365`#319; `S0237`#320 | Unmapped | F/body+ |
| `Rear_Fascia` #406 @43 | `S0205&GPH`#408; `S0205&G26`#409; `S0205&GBK`#410; `S0204`#411; `S0203&{P}` IDs [412, 413, 414, 415, 416, 417, 418, 419, 420, 421] | Unmapped | F/body+ |

<a id="s11-graphics"></a>

**Stripes / decals / color candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Stripes` #4 @1 | No native children | Unmapped | F/body+ |
| `Decals` #6 @2 | `S0490`#8; `S0879`#9 | Unmapped | F/body+ |
| `Decals` #39 @7 | `S0837_F`#41; `S0855_F`#42; `S0302_F`#43; `S0330_F`#44; `S0325_F`#45; `S0320_F`#46; `S0315_F`#47; `S0307_F`#48 | Unmapped | F/body+ |
| `Stripes` #49 @8 | `S0369_F`#51 | Unmapped | F/body+ |
| `Decals` #52 @9 | `S0362_F`#54; `S0349_F`#55; `S0342_F`#56; `S0314_F`#57; `S0306_F`#58; `DZX`#59; `DZV`#60; `DZU`#61; `S0379`#62; `VPO`#63; `VPW`#64; `S0337`#65 | DZU, DZV, DZX, VPO, VPW; rest unmapped | F/body+ |
| `Decals` #369 @34 | `S0866`#371; `S0858`#372; `S0361`#373; `S0348`#374; `S0341`#375; `S0334`#376; `S0313`#377 | Unmapped | F/body+ |
| `Decals` #381 @36 | `S0332`#383; `S0327`#384; `S0322`#385; `S0317`#386; `S0304`#387; `S0303`#388; `S0308`#389 | Unmapped | F/body+ |
| `Decals` #1422 @73 | `S0874`#1424; `S0363`#1425; `S0358`#1426; `S0344`#1427; `S0338`#1428; `S0857`#1429; `S0319`#1430 | Unmapped | F/body+ |
| `Decals` #1434 @75 | `S0333`#1436; `S0328`#1437; `S0323`#1438; `S0318`#1439; `S0310`#1440; `S0309`#1441; `S0311`#1442 | Unmapped | F/body+ |
| `Decals` #1483 @85 | `S0855_B`#1485; `S0837_B`#1486; `S0330_B`#1487; `S0320_B`#1488; `S0315_B`#1489; `S0307_B`#1490; `S0325_B`#1491 | Unmapped | B/body+ |
| `Stripes` #1492 @86 | `S0369_B`#1494 | Unmapped | B/body+ |
| `Decals` #1495 @87 | `S0362_B`#1497; `S0349_B`#1498; `S0342_B`#1499; `S0314_B`#1500; `S0306_B`#1501; `S0302_B`#1502 | Unmapped | B/body+ |

<a id="s11-glass"></a>

**Glass and window candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Windows` #347 @30 | `S0105`#349 | Unmapped | F/body+ |
| `Windows` #363 @32 | `S0101_L`#365 | Unmapped | F/body+ |
| `Windows` #1410 @70 | `S0104`#1412 | Unmapped | F/body+ |
| `Defroster` #1413 @71 | `S0107`#1415 | Unmapped | F/body+ |
| `Windows` #1540 @90 | `S0101_B`#1542; `S0101_R`#1543 | Unmapped | B/body- |

<a id="s11-other"></a>

**Other exterior option-driven and fixed groups**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Tow_Hooks` #1 @0 | No native children | Unmapped | F/body+ |
| `Tailgate` #10 @3 | `S0477&GBK`#12; `S0477&GTR`#13; `S0477&GEC`#14 | Unmapped | F/body+ |
| `Engine` #15 @4 | `S0125`#17; `S0126`#18 | Unmapped | F/body+ |
| `Enclosure_Rear` #19 @5 | `S0127&GKZ`#21; `S0127&GPH`#22; `S0127&G26`#23; `S0127&GBK`#24; `S0127&G4Z`#25; `S0127&GKA`#26; `S0127&GTR`#27; `S0127&GEC`#28 | Unmapped | F/body+ |
| `Badges` #29 @6 | `EYK_F`#31; `EYT_F`#32; `EYT_B`#33; `SFZ_F`#34; `R88_F`#35; `SG1`#36; `S0215`#37; `S0214`#38 | EYK, EYT, R88, SFZ, SG1; rest unmapped | F/body+ |
| `Tail_Lamps` #66 @10 | `S0200`#68 | Unmapped | F/body+ |
| `Headlamps` #69 @11 | `T4L`#71 | T4L; rest unmapped | F/body+ |
| `Molding` #72 @12 | `RYQ`#74; `S0211&{P}` IDs [75, 76, 77, 78, 79, 80, 81, 82, 83, 84]; `S0209`#85 | RYQ; rest unmapped | F/body+ |
| `Grille` #159 @15 | `VWE`#161 | VWE; rest unmapped | F/body+ |
| `Wheels` #174 @17 | `S0816_RL`#176; `S0829_RL`#177; `S0820_RL`#178; `S0817_RL`#179; `S0818_RL`#180; `S0819_RL`#181; `S0453_RL`#182; `S0447_RL`#183; `S0439_RL`#184; `S0440_RL`#185; `S0451_RL`#186; `S0449_RL`#187; `S0435_RL`#188; `S0436_RL`#189; `S0437_RL`#190; `S0438_RL`#191; `S0433_RL`#192; `S0434_RL`#193; `S0431_RL`#194; `S0432_RL`#195; `S0429_RL`#196; `S0430_RL`#197; `S0423_RL`#198; `S0424_RL`#199; `S0427_RL`#200; `S0428_RL`#201; `S0426_RL`#202; `S0425_RL`#203; `S0391_RL`#204; `S0392_RL`#205; `S0393_RL`#206; `S0394_RL`#207; `S0421_RL`#208; `S0422_RL`#209 | Unmapped | F/body+ |
| `Wheel_Caps` #210 @18 | `S0387_RL`#212; `S0383_RL`#213; `S0382_RL`#214; `S0269_RL`#215; `S0380_RL`#216; `S0264_RL`#217; `S0419_RL`#218; `S0418_RL`#219; `S0416_RL`#220; `S0415_RL`#221; `S0406_RL`#222; `S0405_RL`#223; `S0384_RL`#224 | Unmapped | F/body+ |
| `Brakes` #225 @19 | `S0299_RL`#227; `S0381_RL`#228; `S0292_RL`#229; `S0290_RL`#230; `S0289_RL`#231; `S0293_RL`#232; `S0288_RL`#233; `S0296_RL`#234; `S0295_RL`#235; `S0294_RL`#236; `S0291_RL`#237; `J57_RL`#238; `J56_RL`#239 | J56, J57; rest unmapped | F/body+ |
| `Wheels` #240 @20 | `S0816_FL`#242; `S0829_FL`#243; `S0820_FL`#244; `S0817_FL`#245; `S0818_FL`#246; `S0819_FL`#247; `S0426_FL`#248; `S0427_FL`#249; `S0428_FL`#250; `S0425_FL`#251; `S0424_FL`#252; `S0453_FL`#253; `S0447_FL`#254; `S0439_FL`#255; `S0440_FL`#256; `S0451_FL`#257; `S0449_FL`#258; `S0435_FL`#259; `S0436_FL`#260; `S0437_FL`#261; `S0438_FL`#262; `S0433_FL`#263; `S0434_FL`#264; `S0431_FL`#265; `S0432_FL`#266; `S0429_FL`#267; `S0430_FL`#268; `S0423_FL`#269; `S0391_FL`#270; `S0392_FL`#271; `S0393_FL`#272; `S0394_FL`#273; `S0421_FL`#274; `S0422_FL`#275 | Unmapped | F/body+ |
| `Wheel_Caps` #276 @21 | `S0384_FL`#278; `S0264_FL`#279; `S0382_FL`#280; `S0383_FL`#281; `S0380_FL`#282; `S0269_FL`#283; `S0387_FL`#284; `S0419_FL`#285; `S0418_FL`#286; `S0416_FL`#287; `S0415_FL`#288; `S0406_FL`#289; `S0405_FL`#290 | Unmapped | F/body+ |
| `Brakes` #291 @22 | `S0291_FL`#293; `S0290_FL`#294; `S0299_FL`#295; `S0381_FL`#296; `S0292_FL`#297; `S0289_FL`#298; `S0288_FL`#299; `S0296_FL`#300; `S0295_FL`#301; `S0294_FL`#302; `S0293_FL`#303; `J57_FL`#304; `J56_FL`#305 | J56, J57; rest unmapped | F/body+ |
| `Mirror_Cap` #321 @24 | `S0102_L&{P}` IDs [323, 324, 325, 326, 327, 328, 329, 330, 331, 332] | Unmapped | F/body+ |
| `Mirrors` #333 @25 | No native children | Unmapped | F/body+ |
| `Mirror_Cap` #335 @26 | `5JR_L`#337 | 5JR; rest unmapped | F/body+ |
| `Mirrors` #338 @27 | No native children | Unmapped | F/body+ |
| `Mirror_Cap` #340 @28 | `DRG_L`#342 | DRG; rest unmapped | F/body+ |
| `Mirrors` #343 @29 | `DYX_L`#345; `DWK_L`#346 | DWK, DYX; rest unmapped | F/body+ |
| `B_Pillars` #350 @31 | `S0213`#352; `S0212&{P}` IDs [353, 354, 355, 356, 357, 358, 359, 360, 361, 362] | Unmapped | F/body+ |
| `Primer` #366 @33 | `S0115`#368 | Unmapped | F/body+ |
| `None` #378 @35 | `S0345`#380 | Unmapped | F/body+ |
| `Doors` #392 @38 | `S0536`#394 | Unmapped | F/body+ |
| `None` #395 @39 | `S0420`#397 | Unmapped | F/body+ |
| `Splashguards` #398 @40 | `S0390`#400 | Unmapped | F/body+ |
| `None` #401 @41 | `VSN`#403 | Unmapped | F/body+ |
| `License_Plate` #404 @42 | No native children | Unmapped | F/body+ |
| `Multimedia` #422 @44 | `S0244`#424 | Unmapped | F/body+ |
| `Tailgate` #425 @45 | `S0135_L&{P}` IDs [427, 428, 429, 430, 431, 432, 433, 434, 435, 436]; `S0136_L`#437; `S0113_L`#438; `S0112_L&{P}` IDs [439, 440, 441, 442, 443, 444, 445, 446, 447, 448] | Unmapped | F/body+ |
| `Roof` #449 @46 | `S0216`#451; `CM9&{P}` IDs [452, 453, 454, 455, 456, 457, 458, 459, 460, 461]; `S0506`#462; `UG1&HUV`#463; `UG1&HU7`#464; `UG1&HUL`#465; `UG1&HUR`#466; `UG1&HUK`#467; `UG1&HU6`#468; `UG1&HUN`#469; `UG1&HTP`#470; `UG1&H1Y`#471; `UG1&HTE`#472; `UG1&HTT`#473; `UG1&HVV`#474; `UG1&HU1`#475; `UG1&HMO`#476; `UG1&HU9`#477; `UG1&HZB`#478; `UG1&HVT`#479; `UG1&HUA`#480; `UG1&HU2`#481; `UG1&HUU`#482; `UG1&HZP`#483; `UG1&HUE`#484; `UG1&HTG`#485; `UG1&HZN`#486; `UG1&HUF`#487; `UG1&HU0`#488; `UG1&HXO`#489; `UG1&HNK`#490; `UG1&HUW`#491; `UG1&HUX`#492; `UG1&HVZ`#493; `UG1&H8T`#494; `UG1&HUB`#495; `UG1&HUC`#496; `UG1&EPX`#497; `UG1&EJH`#498; `UG1&HAG`#499; `UG1&HTA`#500; `UG1&HTM`#501; `UG1&HTQ`#502; `UG1&HTN`#503 | CM9, UG1; rest unmapped | F/body+ |
| `Badges` #1120 @59 | `CFX`#1122; `BV4`#1123; `S0500`#1124 | BV4, CFX; rest unmapped | F/body+ |
| `Radio` #1361 @68 | No native children | Unmapped | F/body+ |
| `Tailgate` #1416 @72 | `S0478&GEC`#1418; `S0219&G8G`#1419; `S0219&GTR`#1420; `S0217`#1421 | Unmapped | F/body+ |
| `None` #1431 @74 | `S0343`#1433 | Unmapped | F/body+ |
| `None` #1443 @76 | `S0357`#1445 | Unmapped | F/body+ |
| `None` #1462 @78 | `S0119`#1464 | Unmapped | S/body+ |
| `None` #1468 @80 | `D58`#1470 | Unmapped | S/body+ |
| `Engine` #1474 @82 | `LT6`#1476 | LT6; rest unmapped | B/body+ |
| `Exhaust` #1477 @83 | `WUB`#1479 | WUB; rest unmapped | B/body+ |
| `Tow_Hooks` #1480 @84 | `S0871`#1482 | Unmapped | B/body+ |
| `Tailgate` #1503 @88 | `S0135_R&{P}` IDs [1505, 1506, 1507, 1508, 1509, 1510, 1511, 1512, 1513, 1514]; `S0136_R`#1515; `S0113_R`#1516; `S0112_R&{P}` IDs [1517, 1518, 1519, 1520, 1521, 1522, 1523, 1524, 1525, 1526] | Unmapped | B/body+ |
| `Mirror_Cap` #1544 @91 | `S0102_R&{P}` IDs [1546, 1547, 1548, 1549, 1550, 1551, 1552, 1553, 1554, 1555]; `5JR_R`#1556 | 5JR; rest unmapped | B/body- |
| `Mirrors` #1557 @92 | `UFT_R`#1559 | UFT; rest unmapped | B/body- |
| `Mirror_Cap` #1560 @93 | `DRG_R`#1562 | DRG; rest unmapped | B/body- |
| `Mirrors` #1563 @94 | `DYX_R`#1565; `DWK_R`#1566 | DWK, DYX; rest unmapped | B/body- |
| `Wheels` #1567 @95 | `S0440_RR`#1569; `S0435_RR`#1570; `S0433_RR`#1571; `S0430_RR`#1572; `S0425_RR`#1573; `S0817_RR`#1574 | Unmapped | B/body- |
| `Wheel_Caps` #1575 @96 | `S0382_RR`#1577; `S0269_RR`#1578; `S0384_RR`#1579 | Unmapped | B/body- |
| `Brakes` #1580 @97 | No native children | Unmapped | B/body- |
| `Wheels` #1582 @98 | `S0425_FR`#1584; `S0438_FR`#1585; `S0432_FR`#1586; `S0430_FR`#1587; `S0393_FR`#1588; `S0421_FR`#1589 | Unmapped | B/body- |
| `Wheel_Caps` #1590 @99 | `S0383_FR`#1592; `S0382_FR`#1593; `S0380_FR`#1594; `S0415_FR`#1595 | Unmapped | B/body- |
| `Brakes` #1596 @100 | `S0381_FR`#1598; `S0293_FR`#1599; `S0289_FR`#1600; `S0288_FR`#1601; `S0292_FR`#1602; `J57_FR`#1603 | J57; rest unmapped | B/body- |
| `Shadow` #1604 @101 | `S0902`#1606 | Unmapped | B/body- |
| `Background` #1607 @102 | `S0100`#1609 | Unmapped | B/body- |

Cabin/trim-dependent groups visible through glass (separate interior scenes are outside this audit): `Console` #390 @37 (0 children); `Stitching` #504 @47 (23 children); `Steering_Wheel` #529 @48 (62 children); `Interior_Kit` #593 @49 (1 children); `Interior` #596 @50 (53 children); `Interior_Kit` #651 @51 (41 children); `Interior` #694 @52 (28 children); `Interior_Kit` #724 @53 (79 children); `Stitching` #805 @54 (37 children); `Seat_Belts` #844 @55 (20 children); `Seats_Front` #866 @56 (163 children); `Floors` #1031 @57 (39 children); `Cluster` #1072 @58 (46 children); `IP` #1125 @60 (1 children); `Decal_Stickers` #1128 @61 (1 children); `Stitching` #1131 @62 (3 children); `IP` #1136 @63 (1 children); `Decal_Stickers` #1139 @64 (44 children); `IP` #1185 @65 (44 children); `Speakers` #1231 @66 (123 children); `Effects` #1363 @69 (45 children); `Console` #1610 @103 (7 children). Their seat/material/trim state must be recaptured for lower trims; no upper-trim interior is authorized as a substitute.

</details>

<details>
<summary>S12 — Z06 convertible view 02</summary>

PSB: **V/z06/exterior/27CHCORZ_CON_Studio_f04.psb**. Body-paint root index 87; spoiler root indices 6, 11, 13, 15.

<a id="s12-paint"></a>

**Paint — U; all ten base paints**

| Parent path / ID / root index | Exact paint-bearing peers (each maps only its paint token) | Native placement |
| --- | --- | --- |
| `Tailgate` #7 @2 | 2 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Enclosure_Rear` #13 @4 | 9 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Spoiler` #56 @11 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | S/body+ |
| `Tailgate` #144 @23 | 30 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Rear_Fascia` #202 @28 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Molding` #218 @30 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Ground_Effects` #232 @31 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Tailgate` #379 @38 | 20 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Mirror_Cap` #403 @39 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Front_Fascia` #537 @49 | 1 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Ground_Effects` #543 @50 | 40 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Roof` #592 @52 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Front_Fascia` #656 @56 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `B_Pillars` #1508 @79 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Rear_Fascia` #1532 @83 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Base` #1553 @87 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body= |
| `Mirror_Cap` #1572 @90 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body- |

<a id="s12-foundation"></a>

**Trim and body foundation**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Base` #1454 @76 | `S0507&1LZ`#1456; `S0507&3LZ`#1457; `S0507&2LZ`#1458 | Configuration/trim candidates | B/body+ |
| `Base` #1553 @87 | `GBA`#1555; `G8G`#1556; `GKZ`#1557; `GPH`#1558; `G26`#1559; `GBK`#1560; `G4Z`#1561; `GKA`#1562; `GTR`#1563; `GEC`#1564; `1YH67`#1565 | Configuration/trim candidates | B/body= |

<a id="s12-rear"></a>

**Rear spoiler / source-off-spoiler state**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Spoiler` #29 @6 | `SIG`#31 | SIG; rest unmapped | S/body+ |
| `Spoiler` #56 @11 | `T0G`#58; `T0F`#59; `S0268`#60; `S0267&{P}` IDs [61, 62, 63, 64, 65, 66, 67, 68, 69, 70] | T0F, T0G; rest unmapped | S/body+ |
| `Spoiler` #74 @13 | `5V5`#76 | 5V5; rest unmapped | S/body+ |
| `Spoiler` #80 @15 | `5ZV`#82 | 5ZV; rest unmapped | S/body+ |

Source-off-spoiler state: hide every `Spoiler` parent listed here; this is a visibility recipe, **not a catalog option ID**. No legal no-spoiler configuration is established by this operation.

<a id="s12-aero"></a>

**Front/side/hood/fascia aero candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Rear_Fascia` #202 @28 | `S0205&{P}` IDs [204, 205, 206, 207, 208, 209, 210, 211, 212, 213]; `S0204`#214 | Unmapped | B/body+ |
| `Ground_Effects` #232 @31 | `S0366`#234; `S0250&{P}` IDs [235, 236, 237, 238, 239, 240, 241, 242, 243, 244]; `S0365`#245; `S0237`#246 | Unmapped | B/body+ |
| `Front_Fascia` #537 @49 | `S0460&G8G`#539; `S0274`#540; `S0273`#541; `S0227`#542 | Unmapped | B/body+ |
| `Ground_Effects` #543 @50 | `S0396`#545; `S0395`#546; `S0368`#547; `S0367`#548; `S0258&{P}` IDs [549, 550, 551, 552, 553, 554, 555, 556, 557, 558]; `S0872&{P}` IDs [559, 560, 561, 562, 563, 564, 565, 566, 567, 568]; `S0873&{P}` IDs [569, 570, 571, 572, 573, 574, 575, 576, 577, 578]; `S0278&{P}` IDs [579, 580, 581, 582, 583, 584, 585, 586, 587, 588] | Unmapped | B/body+ |
| `Front_Fascia` #656 @56 | `S0220&{P}` IDs [658, 659, 660, 661, 662, 663, 664, 665, 666, 667] | Unmapped | B/body+ |
| `Rear_Fascia` #1532 @83 | `S0203&{P}` IDs [1534, 1535, 1536, 1537, 1538, 1539, 1540, 1541, 1542, 1543] | Unmapped | B/body+ |

<a id="s12-graphics"></a>

**Stripes / decals / color candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Stripes` #1 @0 | No native children | Unmapped | F/body+ |
| `Decals` #3 @1 | `S0491`#5; `S0494`#6 | Unmapped | F/body+ |
| `Decals` #32 @7 | `S0874`#34; `S0363`#35; `S0358`#36; `S0344`#37; `S0338`#38; `S0857`#39; `S0319`#40 | Unmapped | S/body+ |
| `Decals` #44 @9 | `S0333`#46; `S0328`#47; `S0323`#48; `S0318`#49; `S0310`#50; `S0309`#51; `S0311`#52 | Unmapped | S/body+ |
| `Decals` #95 @17 | `S0837_F`#97; `S0855_F`#98; `S0302_F`#99; `S0330_F`#100; `S0325_F`#101; `S0320_F`#102; `S0315_F`#103; `S0307_F`#104 | Unmapped | B/body+ |
| `Stripes` #105 @18 | `S0369_F`#107 | Unmapped | B/body+ |
| `Decals` #108 @19 | `S0362_F`#110; `S0349_F`#111; `S0342_F`#112; `S0314_F`#113; `S0306_F`#114; `DZX`#115; `DZV`#116; `DZU`#117; `S0379`#118; `VPO`#119; `VPW`#120; `S0337`#121; `S0866`#122; `S0858`#123; `S0361`#124; `S0348`#125; `S0341`#126; `S0334`#127; `S0313`#128 | DZU, DZV, DZX, VPO, VPW; rest unmapped | B/body+ |
| `Decals` #132 @21 | `S0332`#134; `S0327`#135; `S0322`#136; `S0317`#137; `S0304`#138; `S0303`#139; `S0308`#140 | Unmapped | B/body+ |
| `Decals` #179 @24 | `S0855_B`#181; `S0837_B`#182; `S0330_B`#183; `S0320_B`#184; `S0315_B`#185; `S0307_B`#186; `S0325_B`#187 | Unmapped | B/body+ |
| `Stripes` #188 @25 | `S0369_B`#190 | Unmapped | B/body+ |
| `Decals` #191 @26 | `S0362_B`#193; `S0349_B`#194; `S0342_B`#195; `S0314_B`#196; `S0306_B`#197; `S0302_B`#198 | Unmapped | B/body+ |

<a id="s12-glass"></a>

**Glass and window candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Windows` #426 @43 | `S0101_R`#428; `S0101_B`#429 | Unmapped | B/body+ |
| `Defroster` #647 @53 | `S0107`#649 | Unmapped | B/body+ |
| `Windows` #650 @54 | `S0104`#652 | Unmapped | B/body+ |
| `Windows` #1550 @86 | `S0105`#1552 | Unmapped | B/body+ |
| `Windows` #1569 @89 | `S0101_L`#1571 | Unmapped | B/body- |

<a id="s12-other"></a>

**Other exterior option-driven and fixed groups**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Tailgate` #7 @2 | `S0478&G4Z`#9; `S0477&G8G`#10 | Unmapped | F/body+ |
| `Engine` #11 @3 | No native children | Unmapped | F/body+ |
| `Enclosure_Rear` #13 @4 | `S0127&GBA`#15; `S0127&G8G`#16; `S0127&GKZ`#17; `S0127&GPH`#18; `S0127&G26`#19; `S0127&GBK`#20; `S0127&G4Z`#21; `S0127&GKA`#22; `S0127&GEC`#23 | Unmapped | F/body+ |
| `Badges` #24 @5 | `SG1`#26; `S0215`#27; `S0214`#28 | SG1; rest unmapped | F/body+ |
| `None` #41 @8 | `S0343`#43 | Unmapped | S/body+ |
| `None` #53 @10 | `S0357`#55 | Unmapped | S/body+ |
| `None` #71 @12 | `S0119`#73 | Unmapped | S/body+ |
| `None` #77 @14 | `D58`#79 | Unmapped | S/body+ |
| `Badges` #83 @16 | `SL8`#85; `RIN`#86; `RIK`#87; `EYT_F`#88; `EYK_B`#89; `EYT_B`#90; `SFZ_B`#91; `S0276`#92; `S0279`#93; `R88_B`#94 | EYK, EYT, R88, RIK, RIN, SFZ, SL8; rest unmapped | B/body+ |
| `None` #129 @20 | `S0345`#131 | Unmapped | B/body+ |
| `Tail_Lamps` #141 @22 | `S0200`#143 | Unmapped | B/body+ |
| `Tailgate` #144 @23 | `S0135_R&{P}` IDs [146, 147, 148, 149, 150, 151, 152, 153, 154, 155]; `S0136_R`#156; `S0113_R`#157; `S0112_R&{P}` IDs [158, 159, 160, 161, 162, 163, 164, 165, 166, 167]; `S0219&{P}` IDs [168, 169, 170, 171, 172, 173, 174, 175, 176, 177]; `S0217`#178 | Unmapped | B/body+ |
| `Multimedia` #199 @27 | `S0244`#201 | Unmapped | B/body+ |
| `License_Plate` #215 @29 | `S0235`#217 | Unmapped | B/body+ |
| `Molding` #218 @30 | `RYQ`#220; `S0211&{P}` IDs [221, 222, 223, 224, 225, 226, 227, 228, 229, 230]; `S0209`#231 | RYQ; rest unmapped | B/body+ |
| `Wheels` #247 @32 | `S0829_FR`#249; `S0820_FR`#250; `S0816_FR`#251; `S0817_FR`#252; `S0818_FR`#253; `S0819_FR`#254; `S0427_FR`#255; `S0426_FR`#256; `S0428_FR`#257; `S0425_FR`#258; `S0453_FR`#259; `S0447_FR`#260; `S0439_FR`#261; `S0440_FR`#262; `S0451_FR`#263; `S0449_FR`#264; `S0435_FR`#265; `S0436_FR`#266; `S0437_FR`#267; `S0438_FR`#268; `S0433_FR`#269; `S0434_FR`#270; `S0431_FR`#271; `S0432_FR`#272; `S0429_FR`#273; `S0430_FR`#274; `S0423_FR`#275; `S0424_FR`#276; `S0391_FR`#277; `S0392_FR`#278; `S0393_FR`#279; `S0394_FR`#280; `S0421_FR`#281; `S0422_FR`#282 | Unmapped | B/body+ |
| `Wheel_Caps` #283 @33 | `S0387_FR`#285; `S0383_FR`#286; `S0382_FR`#287; `S0380_FR`#288; `S0269_FR`#289; `S0264_FR`#290; `S0419_FR`#291; `S0418_FR`#292; `S0416_FR`#293; `S0415_FR`#294; `S0406_FR`#295; `S0405_FR`#296; `S0384_FR`#297 | Unmapped | B/body+ |
| `Brakes` #298 @34 | `S0299_FR`#300; `S0381_FR`#301; `S0291_FR`#302; `S0290_FR`#303; `S0293_FR`#304; `S0289_FR`#305; `S0288_FR`#306; `S0296_FR`#307; `S0295_FR`#308; `S0294_FR`#309; `S0292_FR`#310; `J57_FR`#311; `J56_FR`#312 | J56, J57; rest unmapped | B/body+ |
| `Wheels` #313 @35 | `S0829_RR`#315; `S0816_RR`#316; `S0820_RR`#317; `S0817_RR`#318; `S0818_RR`#319; `S0819_RR`#320; `S0427_RR`#321; `S0426_RR`#322; `S0428_RR`#323; `S0425_RR`#324; `S0453_RR`#325; `S0447_RR`#326; `S0439_RR`#327; `S0440_RR`#328; `S0451_RR`#329; `S0449_RR`#330; `S0435_RR`#331; `S0436_RR`#332; `S0437_RR`#333; `S0438_RR`#334; `S0433_RR`#335; `S0434_RR`#336; `S0431_RR`#337; `S0432_RR`#338; `S0429_RR`#339; `S0430_RR`#340; `S0423_RR`#341; `S0424_RR`#342; `S0391_RR`#343; `S0392_RR`#344; `S0393_RR`#345; `S0394_RR`#346; `S0421_RR`#347; `S0422_RR`#348 | Unmapped | B/body+ |
| `Wheel_Caps` #349 @36 | `S0383_RR`#351; `S0382_RR`#352; `S0380_RR`#353; `S0264_RR`#354; `S0387_RR`#355; `S0419_RR`#356; `S0418_RR`#357; `S0416_RR`#358; `S0415_RR`#359; `S0406_RR`#360; `S0405_RR`#361; `S0269_RR`#362; `S0384_RR`#363 | Unmapped | B/body+ |
| `Brakes` #364 @37 | `S0381_RR`#366; `S0299_RR`#367; `S0289_RR`#368; `S0293_RR`#369; `S0292_RR`#370; `S0288_RR`#371; `S0296_RR`#372; `S0295_RR`#373; `S0294_RR`#374; `S0291_RR`#375; `S0290_RR`#376; `J56_RR`#377; `J57_RR`#378 | J56, J57; rest unmapped | B/body+ |
| `Tailgate` #379 @38 | `S0135_L&{P}` IDs [381, 382, 383, 384, 385, 386, 387, 388, 389, 390]; `S0136_L`#391; `S0113_L`#392; `S0112_L&{P}` IDs [393, 394, 395, 396, 397, 398, 399, 400, 401, 402] | Unmapped | B/body+ |
| `Mirror_Cap` #403 @39 | `S0102_R&{P}` IDs [405, 406, 407, 408, 409, 410, 411, 412, 413, 414]; `5JR_R`#415 | 5JR; rest unmapped | B/body+ |
| `Mirrors` #416 @40 | No native children | Unmapped | B/body+ |
| `Mirror_Cap` #418 @41 | `DRG_R`#420 | DRG; rest unmapped | B/body+ |
| `Mirrors` #421 @42 | `VA5`#423; `DYX_R`#424; `DWK_R`#425 | DWK, DYX; rest unmapped | B/body+ |
| `Doors` #433 @45 | `S0536`#435 | Unmapped | B/body+ |
| `None` #534 @48 | `S0420`#536 | Unmapped | B/body+ |
| `None` #589 @51 | `VSN`#591 | Unmapped | B/body+ |
| `Roof` #592 @52 | `S0216`#594; `CM9&{P}` IDs [595, 596, 597, 598, 599, 600, 601, 602, 603, 604]; `S0506`#605; `UG1&HUV`#606; `UG1&HU7`#607; `UG1&HUL`#608; `UG1&HUR`#609; `UG1&HUK`#610; `UG1&HU6`#611; `UG1&HUN`#612; `UG1&HTP`#613; `UG1&H1Y`#614; `UG1&HTE`#615; `UG1&HTT`#616; `UG1&HVV`#617; `UG1&HU1`#618; `UG1&HMO`#619; `UG1&HU9`#620; `UG1&HZB`#621; `UG1&HVT`#622; `UG1&HUA`#623; `UG1&HU2`#624; `UG1&HUU`#625; `UG1&HZP`#626; `UG1&HUE`#627; `UG1&HTG`#628; `UG1&HZN`#629; `UG1&HUF`#630; `UG1&HU0`#631; `UG1&HXO`#632; `UG1&HNK`#633; `UG1&HUW`#634; `UG1&HUX`#635; `UG1&HVZ`#636; `UG1&H8T`#637; `UG1&HUB`#638; `UG1&HUC`#639; `UG1&EPX`#640; `UG1&EJH`#641; `UG1&HAG`#642; `UG1&HTA`#643; `UG1&HTM`#644; `UG1&HTQ`#645; `UG1&HTN`#646 | CM9, UG1; rest unmapped | B/body+ |
| `Headlamps` #653 @55 | `T4L`#655 | T4L; rest unmapped | B/body+ |
| `Badges` #1271 @71 | `CFX`#1273; `BV4`#1274; `S0500`#1275 | BV4, CFX; rest unmapped | B/body+ |
| `Radio` #1459 @77 | No native children | Unmapped | B/body+ |
| `B_Pillars` #1508 @79 | `S0213`#1510; `S0212&{P}` IDs [1511, 1512, 1513, 1514, 1515, 1516, 1517, 1518, 1519, 1520] | Unmapped | B/body+ |
| `Engine` #1521 @80 | `LT6`#1523 | LT6; rest unmapped | B/body+ |
| `Tow_Hooks` #1524 @81 | `S0871`#1526 | Unmapped | B/body+ |
| `Exhaust` #1527 @82 | `S0867`#1529; `S0868`#1530; `WUB`#1531 | WUB; rest unmapped | B/body+ |
| `Splashguards` #1544 @84 | `S0390`#1546 | Unmapped | B/body+ |
| `Primer` #1547 @85 | `S0115`#1549 | Unmapped | B/body+ |
| `Grille` #1566 @88 | `VWE`#1568 | VWE; rest unmapped | B/body- |
| `Mirror_Cap` #1572 @90 | `S0102_L&{P}` IDs [1574, 1575, 1576, 1577, 1578, 1579, 1580, 1581, 1582, 1583]; `5JR_L`#1584 | 5JR; rest unmapped | B/body- |
| `Mirrors` #1585 @91 | No native children | Unmapped | B/body- |
| `Mirror_Cap` #1587 @92 | `DRG_L`#1589 | DRG; rest unmapped | B/body- |
| `Mirrors` #1590 @93 | `DYX_L`#1592; `DWK_L`#1593 | DWK, DYX; rest unmapped | B/body- |
| `Wheels` #1594 @94 | `S0820_RL`#1596; `S0819_RL`#1597; `S0453_RL`#1598; `S0447_RL`#1599; `S0439_RL`#1600; `S0440_RL`#1601; `S0451_RL`#1602; `S0449_RL`#1603; `S0435_RL`#1604; `S0436_RL`#1605; `S0437_RL`#1606; `S0438_RL`#1607; `S0433_RL`#1608; `S0434_RL`#1609; `S0431_RL`#1610; `S0432_RL`#1611; `S0429_RL`#1612; `S0430_RL`#1613; `S0423_RL`#1614; `S0424_RL`#1615; `S0427_RL`#1616; `S0426_RL`#1617; `S0428_RL`#1618; `S0425_RL`#1619; `S0391_RL`#1620; `S0392_RL`#1621; `S0393_RL`#1622; `S0394_RL`#1623; `S0421_RL`#1624; `S0422_RL`#1625 | Unmapped | B/body- |
| `Wheel_Caps` #1626 @95 | `S0383_RL`#1628; `S0382_RL`#1629; `S0269_RL`#1630; `S0380_RL`#1631; `S0418_RL`#1632; `S0406_RL`#1633; `S0405_RL`#1634; `S0384_RL`#1635 | Unmapped | B/body- |
| `Brakes` #1636 @96 | `S0292_RL`#1638; `S0290_RL`#1639; `S0289_RL`#1640; `S0293_RL`#1641; `S0288_RL`#1642; `S0296_RL`#1643; `S0295_RL`#1644; `S0294_RL`#1645; `S0291_RL`#1646; `J57_RL`#1647; `J56_RL`#1648 | J56, J57; rest unmapped | B/body- |
| `Wheels` #1649 @97 | `S0817_FL`#1651; `S0427_FL`#1652; `S0426_FL`#1653; `S0428_FL`#1654; `S0453_FL`#1655; `S0449_FL`#1656; `S0435_FL`#1657; `S0436_FL`#1658; `S0437_FL`#1659; `S0438_FL`#1660; `S0434_FL`#1661; `S0429_FL`#1662; `S0430_FL`#1663; `S0394_FL`#1664; `S0421_FL`#1665 | Unmapped | B/body- |
| `Wheel_Caps` #1666 @98 | `S0384_FL`#1668; `S0264_FL`#1669; `S0382_FL`#1670; `S0419_FL`#1671; `S0418_FL`#1672; `S0416_FL`#1673; `S0415_FL`#1674 | Unmapped | B/body- |
| `Brakes` #1675 @99 | `S0291_FL`#1677; `S0289_FL`#1678; `S0299_FL`#1679; `S0381_FL`#1680 | Unmapped | B/body- |
| `Shadow` #1681 @100 | `S0902`#1683 | Unmapped | B/body- |
| `Background` #1684 @101 | `S0100`#1686 | Unmapped | B/body- |
| `Tow_Hooks` #1687 @102 | `S0869`#1689 | Unmapped | B/body- |

Cabin/trim-dependent groups visible through glass (separate interior scenes are outside this audit): `Console` #430 @44 (1 children); `Stitching` #436 @46 (6 children); `Steering_Wheel` #444 @47 (88 children); `Seat_Belts` #668 @57 (20 children); `Interior` #690 @58 (56 children); `Interior_Kit` #748 @59 (36 children); `Interior` #786 @60 (27 children); `Interior_Kit` #815 @61 (78 children); `IP` #895 @62 (1 children); `Decal_Stickers` #898 @63 (1 children); `Cluster` #901 @64 (46 children); `Stitching` #949 @65 (57 children); `Floors` #1008 @66 (45 children); `Interior_Kit` #1055 @67 (0 children); `IP` #1057 @68 (44 children); `Seats_Front` #1103 @69 (163 children); `Interior` #1268 @70 (1 children); `Speakers` #1276 @72 (118 children); `IP` #1396 @73 (1 children); `Decal_Stickers` #1399 @74 (44 children); `Console` #1445 @75 (7 children); `Effects` #1461 @78 (45 children). Their seat/material/trim state must be recaptured for lower trims; no upper-trim interior is authorized as a substitute.

</details>

<details>
<summary>S13 — Z06 coupe view 01</summary>

PSB: **V/z06/exterior/27CHCORZ_COU_Studio_f02.psb**. Body-paint root index 82; spoiler root indices 71, 73, 75.

<a id="s13-paint"></a>

**Paint — U; all ten base paints**

| Parent path / ID / root index | Exact paint-bearing peers (each maps only its paint token) | Native placement |
| --- | --- | --- |
| `Molding` #50 @7 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Front_Fascia` #64 @8 | 20 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Ground_Effects` #91 @9 | 40 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Front_Fascia` #140 @11 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Ground_Effects` #284 @18 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Mirror_Cap` #299 @19 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `B_Pillars` #328 @26 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Rear_Fascia` #387 @39 | 12 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Roof` #404 @41 | 40 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Spoiler` #1415 @71 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | S/body+ |
| `Base` #1476 @82 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body= |
| `Mirror_Cap` #1492 @84 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body- |

<a id="s13-foundation"></a>

**Trim and body foundation**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Base` #1330 @62 | `S0507&1LZ`#1332; `S0507&3LZ`#1333; `S0507&2LZ`#1334 | Configuration/trim candidates | F/body+ |
| `Base` #1476 @82 | `GBA`#1478; `G8G`#1479; `GKZ`#1480; `GPH`#1481; `G26`#1482; `GBK`#1483; `G4Z`#1484; `GKA`#1485; `GTR`#1486; `GEC`#1487; `1YH07`#1488 | Configuration/trim candidates | B/body= |

<a id="s13-rear"></a>

**Rear spoiler / source-off-spoiler state**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Spoiler` #1415 @71 | `T0G`#1417; `T0F`#1418; `S0268`#1419; `S0267&{P}` IDs [1420, 1421, 1422, 1423, 1424, 1425, 1426, 1427, 1428, 1429]; `SIG`#1430 | SIG, T0F, T0G; rest unmapped | S/body+ |
| `Spoiler` #1434 @73 | `5V5`#1436 | 5V5; rest unmapped | S/body+ |
| `Spoiler` #1440 @75 | `5ZV`#1442 | 5ZV; rest unmapped | S/body+ |

Source-off-spoiler state: hide every `Spoiler` parent listed here; this is a visibility recipe, **not a catalog option ID**. No legal no-spoiler configuration is established by this operation.

<a id="s13-aero"></a>

**Front/side/hood/fascia aero candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Front_Fascia` #64 @8 | `S0461&{P}` IDs [66, 67, 68, 69, 70, 71, 72, 73, 74, 75]; `S0460&{P}` IDs [76, 77, 78, 79, 80, 81, 82, 83, 84, 85]; `S0274`#86; `S0273`#87; `S0227`#88; `S0224`#89; `S0221`#90 | Unmapped | F/body+ |
| `Ground_Effects` #91 @9 | `S0396`#93; `S0395`#94; `S0368`#95; `S0367`#96; `S0258&{P}` IDs [97, 98, 99, 100, 101, 102, 103, 104, 105, 106]; `S0872&{P}` IDs [107, 108, 109, 110, 111, 112, 113, 114, 115, 116]; `S0873&{P}` IDs [117, 118, 119, 120, 121, 122, 123, 124, 125, 126]; `S0278&{P}` IDs [127, 128, 129, 130, 131, 132, 133, 134, 135, 136] | Unmapped | F/body+ |
| `Front_Fascia` #140 @11 | `S0220&{P}` IDs [142, 143, 144, 145, 146, 147, 148, 149, 150, 151] | Unmapped | F/body+ |
| `Ground_Effects` #284 @18 | `S0366`#286; `S0250&{P}` IDs [287, 288, 289, 290, 291, 292, 293, 294, 295, 296]; `S0365`#297; `S0237`#298 | Unmapped | F/body+ |
| `Rear_Fascia` #387 @39 | `S0205&G8G`#389; `S0205&GEC`#390; `S0204`#391; `S0203&{P}` IDs [392, 393, 394, 395, 396, 397, 398, 399, 400, 401] | Unmapped | F/body+ |

<a id="s13-graphics"></a>

**Stripes / decals / color candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Decals` #17 @2 | `S0837_F`#19; `S0855_F`#20; `S0302_F`#21; `S0330_F`#22; `S0325_F`#23; `S0320_F`#24; `S0315_F`#25; `S0307_F`#26 | Unmapped | F/body+ |
| `Stripes` #27 @3 | `S0369_F`#29 | Unmapped | F/body+ |
| `Decals` #30 @4 | `S0362_F`#32; `S0349_F`#33; `S0342_F`#34; `S0314_F`#35; `S0306_F`#36; `DZX`#37; `DZV`#38; `DZU`#39; `S0379`#40; `VPO`#41; `VPW`#42; `S0337`#43 | DZU, DZV, DZX, VPO, VPW; rest unmapped | F/body+ |
| `Decals` #346 @29 | `S0866`#348; `S0858`#349; `S0361`#350; `S0348`#351; `S0341`#352; `S0334`#353; `S0313`#354 | Unmapped | F/body+ |
| `Decals` #358 @31 | `S0332`#360; `S0327`#361; `S0322`#362; `S0317`#363; `S0304`#364; `S0303`#365; `S0308`#366 | Unmapped | F/body+ |
| `Decals` #1391 @67 | `S0874`#1393; `S0363`#1394; `S0358`#1395; `S0344`#1396; `S0338`#1397; `S0857`#1398; `S0319`#1399 | Unmapped | F/body+ |
| `Decals` #1403 @69 | `S0333`#1405; `S0328`#1406; `S0323`#1407; `S0318`#1408; `S0310`#1409; `S0309`#1410; `S0311`#1411 | Unmapped | F/body+ |
| `Decals` #1455 @79 | `S0330_B`#1457 | Unmapped | B/body+ |
| `Stripes` #1458 @80 | No native children | Unmapped | B/body+ |
| `Decals` #1460 @81 | `S0838`#1462; `S0360`#1463; `S0347`#1464; `S0340`#1465; `S0329`#1466; `S0312`#1467; `S0331`#1468; `S0326`#1469; `S0321`#1470; `S0316`#1471; `S0301`#1472; `S0300`#1473; `S0859`#1474; `S0305`#1475 | Unmapped | B/body+ |

<a id="s13-glass"></a>

**Glass and window candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Windows` #325 @25 | `S0105`#327 | Unmapped | F/body+ |
| `Windows` #340 @27 | `S0101_L`#342 | Unmapped | F/body+ |
| `Windows` #378 @36 | `S0108`#380 | Unmapped | F/body+ |
| `Windows` #1384 @65 | `S0122`#1386; `S0104`#1387 | Unmapped | F/body+ |
| `Defroster` #1388 @66 | `S0107`#1390 | Unmapped | F/body+ |
| `Windows` #1489 @83 | `S0101_R`#1491 | Unmapped | B/body- |

<a id="s13-other"></a>

**Other exterior option-driven and fixed groups**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Tow_Hooks` #1 @0 | No native children | Unmapped | F/body+ |
| `Badges` #4 @1 | `RIN`#6; `EYK_F`#7; `EYT_F`#8; `SFZ_F`#9; `SFZ_B`#10; `S0276`#11; `S0279`#12; `R88_F`#13; `SG1`#14; `S0215`#15; `S0214`#16 | EYK, EYT, R88, RIN, SFZ, SG1; rest unmapped | F/body+ |
| `Tail_Lamps` #44 @5 | `S0200`#46 | Unmapped | F/body+ |
| `Headlamps` #47 @6 | `T4L`#49 | T4L; rest unmapped | F/body+ |
| `Molding` #50 @7 | `RYQ`#52; `S0211&{P}` IDs [53, 54, 55, 56, 57, 58, 59, 60, 61, 62]; `S0209`#63 | RYQ; rest unmapped | F/body+ |
| `Grille` #137 @10 | `VWE`#139 | VWE; rest unmapped | F/body+ |
| `Wheels` #152 @12 | `S0816_RL`#154; `S0829_RL`#155; `S0820_RL`#156; `S0817_RL`#157; `S0818_RL`#158; `S0819_RL`#159; `S0453_RL`#160; `S0447_RL`#161; `S0439_RL`#162; `S0440_RL`#163; `S0451_RL`#164; `S0449_RL`#165; `S0435_RL`#166; `S0436_RL`#167; `S0437_RL`#168; `S0438_RL`#169; `S0433_RL`#170; `S0434_RL`#171; `S0431_RL`#172; `S0432_RL`#173; `S0429_RL`#174; `S0430_RL`#175; `S0423_RL`#176; `S0424_RL`#177; `S0427_RL`#178; `S0428_RL`#179; `S0426_RL`#180; `S0425_RL`#181; `S0391_RL`#182; `S0392_RL`#183; `S0393_RL`#184; `S0394_RL`#185; `S0421_RL`#186; `S0422_RL`#187 | Unmapped | F/body+ |
| `Wheel_Caps` #188 @13 | `S0387_RL`#190; `S0383_RL`#191; `S0382_RL`#192; `S0269_RL`#193; `S0380_RL`#194; `S0264_RL`#195; `S0419_RL`#196; `S0418_RL`#197; `S0416_RL`#198; `S0415_RL`#199; `S0406_RL`#200; `S0405_RL`#201; `S0384_RL`#202 | Unmapped | F/body+ |
| `Brakes` #203 @14 | `S0299_RL`#205; `S0381_RL`#206; `S0292_RL`#207; `S0290_RL`#208; `S0289_RL`#209; `S0293_RL`#210; `S0288_RL`#211; `S0296_RL`#212; `S0295_RL`#213; `S0294_RL`#214; `S0291_RL`#215; `J57_RL`#216; `J56_RL`#217 | J56, J57; rest unmapped | F/body+ |
| `Wheels` #218 @15 | `S0816_FL`#220; `S0829_FL`#221; `S0820_FL`#222; `S0817_FL`#223; `S0818_FL`#224; `S0819_FL`#225; `S0426_FL`#226; `S0427_FL`#227; `S0428_FL`#228; `S0425_FL`#229; `S0424_FL`#230; `S0453_FL`#231; `S0447_FL`#232; `S0439_FL`#233; `S0440_FL`#234; `S0451_FL`#235; `S0449_FL`#236; `S0435_FL`#237; `S0436_FL`#238; `S0437_FL`#239; `S0438_FL`#240; `S0433_FL`#241; `S0434_FL`#242; `S0431_FL`#243; `S0432_FL`#244; `S0429_FL`#245; `S0430_FL`#246; `S0423_FL`#247; `S0391_FL`#248; `S0392_FL`#249; `S0393_FL`#250; `S0394_FL`#251; `S0421_FL`#252; `S0422_FL`#253 | Unmapped | F/body+ |
| `Wheel_Caps` #254 @16 | `S0384_FL`#256; `S0264_FL`#257; `S0382_FL`#258; `S0383_FL`#259; `S0380_FL`#260; `S0269_FL`#261; `S0387_FL`#262; `S0419_FL`#263; `S0418_FL`#264; `S0416_FL`#265; `S0415_FL`#266; `S0406_FL`#267; `S0405_FL`#268 | Unmapped | F/body+ |
| `Brakes` #269 @17 | `S0291_FL`#271; `S0290_FL`#272; `S0299_FL`#273; `S0381_FL`#274; `S0292_FL`#275; `S0289_FL`#276; `S0288_FL`#277; `S0296_FL`#278; `S0295_FL`#279; `S0294_FL`#280; `S0293_FL`#281; `J57_FL`#282; `J56_FL`#283 | J56, J57; rest unmapped | F/body+ |
| `Mirror_Cap` #299 @19 | `S0102_L&{P}` IDs [301, 302, 303, 304, 305, 306, 307, 308, 309, 310] | Unmapped | F/body+ |
| `Mirrors` #311 @20 | No native children | Unmapped | F/body+ |
| `Mirror_Cap` #313 @21 | `5JR_L`#315 | 5JR; rest unmapped | F/body+ |
| `Mirrors` #316 @22 | No native children | Unmapped | F/body+ |
| `Mirror_Cap` #318 @23 | `DRG_L`#320 | DRG; rest unmapped | F/body+ |
| `Mirrors` #321 @24 | `DYX_L`#323; `DWK_L`#324 | DWK, DYX; rest unmapped | F/body+ |
| `B_Pillars` #328 @26 | `S0212&{P}` IDs [330, 331, 332, 333, 334, 335, 336, 337, 338, 339] | Unmapped | F/body+ |
| `Primer` #343 @28 | `S0115`#345 | Unmapped | F/body+ |
| `None` #355 @30 | `S0345`#357 | Unmapped | F/body+ |
| `Doors` #369 @33 | `S0536`#371 | Unmapped | F/body+ |
| `None` #372 @34 | `S0420`#374 | Unmapped | F/body+ |
| `Splashguards` #375 @35 | `S0390`#377 | Unmapped | F/body+ |
| `None` #381 @37 | `VSN`#383 | Unmapped | F/body+ |
| `License_Plate` #384 @38 | `S0235`#386 | Unmapped | F/body+ |
| `Multimedia` #402 @40 | No native children | Unmapped | F/body+ |
| `Roof` #404 @41 | `SBT`#406; `S0243&{P}` IDs [407, 408, 409, 410, 411, 412, 413, 414, 415, 416]; `C2Z&{P}` IDs [417, 418, 419, 420, 421, 422, 423, 424, 425, 426]; `CF7&{P}` IDs [427, 428, 429, 430, 431, 432, 433, 434, 435, 436]; `CF8&{P}` IDs [437, 438, 439, 440, 441, 442, 443, 444, 445, 446]; `CC3`#447; `S0506`#448; `UG1&HUV`#449; `UG1&HU7`#450; `UG1&HUL`#451; `UG1&HUR`#452; `UG1&HUK`#453; `UG1&HU6`#454; `UG1&HUN`#455; `UG1&HTP`#456; `UG1&H1Y`#457; `UG1&HTE`#458; `UG1&HTT`#459; `UG1&HVV`#460; `UG1&HU1`#461; `UG1&HMO`#462; `UG1&HU9`#463; `UG1&HZB`#464; `UG1&HVT`#465; `UG1&HUA`#466; `UG1&HU2`#467; `UG1&HUU`#468; `UG1&HZP`#469; `UG1&HUE`#470; `UG1&HTG`#471; `UG1&HZN`#472; `UG1&HUF`#473; `UG1&HU0`#474; `UG1&HXO`#475; `UG1&HNK`#476; `UG1&HUW`#477; `UG1&HUX`#478; `UG1&HVZ`#479; `UG1&H8T`#480; `UG1&HUB`#481; `UG1&HUC`#482; `UG1&EPX`#483; `UG1&EJH`#484; `UG1&HAG`#485; `UG1&HTA`#486; `UG1&HTM`#487; `UG1&HTQ`#488; `UG1&HTN`#489 | C2Z, CC3, CF7, CF8, SBT, UG1; rest unmapped | F/body+ |
| `Badges` #1094 @54 | `CFX`#1096; `BV4`#1097; `S0500`#1098 | BV4, CFX; rest unmapped | F/body+ |
| `Radio` #1335 @63 | No native children | Unmapped | F/body+ |
| `None` #1400 @68 | `S0343`#1402 | Unmapped | F/body+ |
| `None` #1412 @70 | `S0357`#1414 | Unmapped | F/body+ |
| `None` #1431 @72 | `S0119`#1433 | Unmapped | S/body+ |
| `None` #1437 @74 | `D58`#1439 | Unmapped | S/body+ |
| `Engine` #1443 @76 | `SLN`#1445; `RXI`#1446; `S0110`#1447; `S0111`#1448 | RXI, SLN; rest unmapped | B/body+ |
| `Exhaust` #1449 @77 | `WUB`#1451 | WUB; rest unmapped | B/body+ |
| `Tow_Hooks` #1452 @78 | `S0871`#1454 | Unmapped | B/body+ |
| `Mirror_Cap` #1492 @84 | `S0102_R&{P}` IDs [1494, 1495, 1496, 1497, 1498, 1499, 1500, 1501, 1502, 1503]; `5JR_R`#1504 | 5JR; rest unmapped | B/body- |
| `Mirrors` #1505 @85 | `UFT_R`#1507 | UFT; rest unmapped | B/body- |
| `Mirror_Cap` #1508 @86 | `DRG_R`#1510 | DRG; rest unmapped | B/body- |
| `Mirrors` #1511 @87 | `DYX_R`#1513; `DWK_R`#1514 | DWK, DYX; rest unmapped | B/body- |
| `Wheels` #1515 @88 | `S0449_RR`#1517; `S0433_RR`#1518; `S0434_RR`#1519; `S0431_RR`#1520; `S0427_RR`#1521; `S0426_RR`#1522; `S0816_RR`#1523; `S0817_RR`#1524 | Unmapped | B/body- |
| `Wheel_Caps` #1525 @89 | `S0269_RR`#1527; `S0384_RR`#1528 | Unmapped | B/body- |
| `Brakes` #1529 @90 | `S0381_RR`#1531; `S0295_RR`#1532 | Unmapped | B/body- |
| `Wheels` #1533 @91 | `S0820_FR`#1535; `S0817_FR`#1536; `S0449_FR`#1537; `S0437_FR`#1538; `S0438_FR`#1539; `S0433_FR`#1540; `S0432_FR`#1541 | Unmapped | B/body- |
| `Wheel_Caps` #1542 @92 | `S0264_FR`#1544; `S0418_FR`#1545 | Unmapped | B/body- |
| `Brakes` #1546 @93 | `S0299_FR`#1548; `J57_FR`#1549 | J57; rest unmapped | B/body- |
| `Shadow` #1550 @94 | `S0902`#1552 | Unmapped | B/body- |
| `Background` #1553 @95 | `S0100`#1555 | Unmapped | B/body- |

Cabin/trim-dependent groups visible through glass (separate interior scenes are outside this audit): `Console` #367 @32 (0 children); `Stitching` #490 @42 (21 children); `Steering_Wheel` #513 @43 (59 children); `Interior_Kit` #574 @44 (1 children); `Interior` #577 @45 (53 children); `Interior_Kit` #632 @46 (38 children); `Interior` #672 @47 (28 children); `Interior_Kit` #702 @48 (75 children); `Stitching` #779 @49 (37 children); `Seat_Belts` #818 @50 (20 children); `Seats_Front` #840 @51 (162 children); `Floors` #1004 @52 (40 children); `Cluster` #1046 @53 (46 children); `IP` #1099 @55 (1 children); `Decal_Stickers` #1102 @56 (1 children); `Stitching` #1105 @57 (3 children); `IP` #1110 @58 (1 children); `Decal_Stickers` #1113 @59 (44 children); `IP` #1159 @60 (44 children); `Speakers` #1205 @61 (123 children); `Effects` #1337 @64 (45 children); `Console` #1556 @96 (5 children). Their seat/material/trim state must be recaptured for lower trims; no upper-trim interior is authorized as a substitute.

</details>

<details>
<summary>S14 — Z06 coupe view 02</summary>

PSB: **V/z06/exterior/27CHCORZ_COU_Studio_f04.psb**. Body-paint root index 81; spoiler root indices 1, 6, 8, 10.

<a id="s14-paint"></a>

**Paint — U; all ten base paints**

| Parent path / ID / root index | Exact paint-bearing peers (each maps only its paint token) | Native placement |
| --- | --- | --- |
| `Spoiler` #33 @6 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | S/body+ |
| `Rear_Fascia` #157 @22 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Molding` #173 @24 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Ground_Effects` #187 @25 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Mirror_Cap` #334 @32 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Front_Fascia` #468 @42 | 1 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Ground_Effects` #473 @43 | 40 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Roof` #522 @45 | 40 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Front_Fascia` #617 @49 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `B_Pillars` #1431 @73 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Rear_Fascia` #1455 @77 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Base` #1476 @81 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body= |
| `Mirror_Cap` #1495 @84 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body- |

<a id="s14-foundation"></a>

**Trim and body foundation**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Base` #1377 @70 | `S0507&1LZ`#1379; `S0507&3LZ`#1380; `S0507&2LZ`#1381 | Configuration/trim candidates | B/body+ |
| `Base` #1476 @81 | `GBA`#1478; `G8G`#1479; `GKZ`#1480; `GPH`#1481; `G26`#1482; `GBK`#1483; `G4Z`#1484; `GKA`#1485; `GTR`#1486; `GEC`#1487; `1YH07`#1488 | Configuration/trim candidates | B/body= |

<a id="s14-rear"></a>

**Rear spoiler / source-off-spoiler state**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Spoiler` #6 @1 | `SIG`#8 | SIG; rest unmapped | S/body+ |
| `Spoiler` #33 @6 | `T0G`#35; `T0F`#36; `S0268`#37; `S0267&{P}` IDs [38, 39, 40, 41, 42, 43, 44, 45, 46, 47] | T0F, T0G; rest unmapped | S/body+ |
| `Spoiler` #51 @8 | `5V5`#53 | 5V5; rest unmapped | S/body+ |
| `Spoiler` #57 @10 | `5ZV`#59 | 5ZV; rest unmapped | S/body+ |

Source-off-spoiler state: hide every `Spoiler` parent listed here; this is a visibility recipe, **not a catalog option ID**. No legal no-spoiler configuration is established by this operation.

<a id="s14-aero"></a>

**Front/side/hood/fascia aero candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Rear_Fascia` #157 @22 | `S0205&{P}` IDs [159, 160, 161, 162, 163, 164, 165, 166, 167, 168]; `S0204`#169 | Unmapped | B/body+ |
| `Ground_Effects` #187 @25 | `S0366`#189; `S0250&{P}` IDs [190, 191, 192, 193, 194, 195, 196, 197, 198, 199]; `S0365`#200; `S0237`#201 | Unmapped | B/body+ |
| `Front_Fascia` #468 @42 | `S0461&GEC`#470; `S0274`#471; `S0273`#472 | Unmapped | B/body+ |
| `Ground_Effects` #473 @43 | `S0396`#475; `S0395`#476; `S0368`#477; `S0367`#478; `S0258&{P}` IDs [479, 480, 481, 482, 483, 484, 485, 486, 487, 488]; `S0872&{P}` IDs [489, 490, 491, 492, 493, 494, 495, 496, 497, 498]; `S0873&{P}` IDs [499, 500, 501, 502, 503, 504, 505, 506, 507, 508]; `S0278&{P}` IDs [509, 510, 511, 512, 513, 514, 515, 516, 517, 518] | Unmapped | B/body+ |
| `Front_Fascia` #617 @49 | `S0220&{P}` IDs [619, 620, 621, 622, 623, 624, 625, 626, 627, 628] | Unmapped | B/body+ |
| `Rear_Fascia` #1455 @77 | `S0203&{P}` IDs [1457, 1458, 1459, 1460, 1461, 1462, 1463, 1464, 1465, 1466] | Unmapped | B/body+ |

<a id="s14-graphics"></a>

**Stripes / decals / color candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Decals` #9 @2 | `S0874`#11; `S0363`#12; `S0358`#13; `S0344`#14; `S0338`#15; `S0857`#16; `S0319`#17 | Unmapped | S/body+ |
| `Decals` #21 @4 | `S0333`#23; `S0328`#24; `S0323`#25; `S0318`#26; `S0310`#27; `S0309`#28; `S0311`#29 | Unmapped | S/body+ |
| `Decals` #72 @12 | `S0837_F`#74; `S0855_F`#75; `S0302_F`#76; `S0330_F`#77; `S0325_F`#78; `S0320_F`#79; `S0315_F`#80; `S0307_F`#81 | Unmapped | B/body+ |
| `Stripes` #82 @13 | `S0369_F`#84 | Unmapped | B/body+ |
| `Decals` #85 @14 | `S0362_F`#87; `S0349_F`#88; `S0342_F`#89; `S0314_F`#90; `S0306_F`#91; `DZX`#92; `DZV`#93; `DZU`#94; `S0379`#95; `VPO`#96; `VPW`#97; `S0337`#98; `S0866`#99; `S0858`#100; `S0361`#101; `S0348`#102; `S0341`#103; `S0334`#104; `S0313`#105 | DZU, DZV, DZX, VPO, VPW; rest unmapped | B/body+ |
| `Decals` #108 @16 | `S0332`#110; `S0327`#111; `S0322`#112; `S0317`#113; `S0304`#114; `S0303`#115; `S0308`#116; `S0838`#117; `S0360`#118; `S0347`#119; `S0340`#120; `S0329`#121; `S0312`#122; `S0331`#123; `S0326`#124; `S0321`#125; `S0316`#126; `S0301`#127; `S0300`#128; `S0859`#129; `S0305`#130 | Unmapped | B/body+ |
| `Decals` #134 @18 | `S0855_B`#136; `S0837_B`#137; `S0330_B`#138; `S0320_B`#139; `S0315_B`#140; `S0307_B`#141; `S0325_B`#142 | Unmapped | B/body+ |
| `Stripes` #143 @19 | `S0369_B`#145 | Unmapped | B/body+ |
| `Decals` #146 @20 | `S0362_B`#148; `S0349_B`#149; `S0342_B`#150; `S0314_B`#151; `S0306_B`#152; `S0302_B`#153 | Unmapped | B/body+ |

<a id="s14-glass"></a>

**Glass and window candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Windows` #357 @36 | `S0101_R`#359; `S0108`#360 | Unmapped | B/body+ |
| `Defroster` #608 @46 | `S0107`#610 | Unmapped | B/body+ |
| `Windows` #611 @47 | `S0104`#613 | Unmapped | B/body+ |
| `Windows` #629 @50 | `S0122`#631 | Unmapped | B/body+ |
| `Windows` #1473 @80 | `S0105`#1475 | Unmapped | B/body+ |
| `Windows` #1492 @83 | `S0101_L`#1494 | Unmapped | B/body- |

<a id="s14-other"></a>

**Other exterior option-driven and fixed groups**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Badges` #1 @0 | No native children | Unmapped | F/body+ |
| `None` #18 @3 | `S0343`#20 | Unmapped | S/body+ |
| `None` #30 @5 | `S0357`#32 | Unmapped | S/body+ |
| `None` #48 @7 | `S0119`#50 | Unmapped | S/body+ |
| `None` #54 @9 | `D58`#56 | Unmapped | S/body+ |
| `Badges` #60 @11 | `SL8`#62; `RIN`#63; `RIK`#64; `EYK_B`#65; `EYT_B`#66; `SFZ_F`#67; `SFZ_B`#68; `S0276`#69; `S0279`#70; `R88_B`#71 | EYK, EYT, R88, RIK, RIN, SFZ, SL8; rest unmapped | B/body+ |
| `None` #106 @15 | No native children | Unmapped | B/body+ |
| `Tail_Lamps` #131 @17 | `S0200`#133 | Unmapped | B/body+ |
| `Multimedia` #154 @21 | `S0244`#156 | Unmapped | B/body+ |
| `License_Plate` #170 @23 | `S0235`#172 | Unmapped | B/body+ |
| `Molding` #173 @24 | `RYQ`#175; `S0211&{P}` IDs [176, 177, 178, 179, 180, 181, 182, 183, 184, 185]; `S0209`#186 | RYQ; rest unmapped | B/body+ |
| `Wheels` #202 @26 | `S0829_FR`#204; `S0820_FR`#205; `S0816_FR`#206; `S0817_FR`#207; `S0818_FR`#208; `S0819_FR`#209; `S0427_FR`#210; `S0426_FR`#211; `S0428_FR`#212; `S0425_FR`#213; `S0453_FR`#214; `S0447_FR`#215; `S0439_FR`#216; `S0440_FR`#217; `S0451_FR`#218; `S0449_FR`#219; `S0435_FR`#220; `S0436_FR`#221; `S0437_FR`#222; `S0438_FR`#223; `S0433_FR`#224; `S0434_FR`#225; `S0431_FR`#226; `S0432_FR`#227; `S0429_FR`#228; `S0430_FR`#229; `S0423_FR`#230; `S0424_FR`#231; `S0391_FR`#232; `S0392_FR`#233; `S0393_FR`#234; `S0394_FR`#235; `S0421_FR`#236; `S0422_FR`#237 | Unmapped | B/body+ |
| `Wheel_Caps` #238 @27 | `S0387_FR`#240; `S0383_FR`#241; `S0382_FR`#242; `S0380_FR`#243; `S0269_FR`#244; `S0264_FR`#245; `S0419_FR`#246; `S0418_FR`#247; `S0416_FR`#248; `S0415_FR`#249; `S0406_FR`#250; `S0405_FR`#251; `S0384_FR`#252 | Unmapped | B/body+ |
| `Brakes` #253 @28 | `S0299_FR`#255; `S0381_FR`#256; `S0291_FR`#257; `S0290_FR`#258; `S0293_FR`#259; `S0289_FR`#260; `S0288_FR`#261; `S0296_FR`#262; `S0295_FR`#263; `S0294_FR`#264; `S0292_FR`#265; `J57_FR`#266; `J56_FR`#267 | J56, J57; rest unmapped | B/body+ |
| `Wheels` #268 @29 | `S0829_RR`#270; `S0816_RR`#271; `S0820_RR`#272; `S0817_RR`#273; `S0818_RR`#274; `S0819_RR`#275; `S0427_RR`#276; `S0426_RR`#277; `S0428_RR`#278; `S0425_RR`#279; `S0453_RR`#280; `S0447_RR`#281; `S0439_RR`#282; `S0440_RR`#283; `S0451_RR`#284; `S0449_RR`#285; `S0435_RR`#286; `S0436_RR`#287; `S0437_RR`#288; `S0438_RR`#289; `S0433_RR`#290; `S0434_RR`#291; `S0431_RR`#292; `S0432_RR`#293; `S0429_RR`#294; `S0430_RR`#295; `S0423_RR`#296; `S0424_RR`#297; `S0391_RR`#298; `S0392_RR`#299; `S0393_RR`#300; `S0394_RR`#301; `S0421_RR`#302; `S0422_RR`#303 | Unmapped | B/body+ |
| `Wheel_Caps` #304 @30 | `S0383_RR`#306; `S0382_RR`#307; `S0380_RR`#308; `S0264_RR`#309; `S0387_RR`#310; `S0419_RR`#311; `S0418_RR`#312; `S0416_RR`#313; `S0415_RR`#314; `S0406_RR`#315; `S0405_RR`#316; `S0269_RR`#317; `S0384_RR`#318 | Unmapped | B/body+ |
| `Brakes` #319 @31 | `S0381_RR`#321; `S0299_RR`#322; `S0289_RR`#323; `S0293_RR`#324; `S0292_RR`#325; `S0288_RR`#326; `S0296_RR`#327; `S0295_RR`#328; `S0294_RR`#329; `S0291_RR`#330; `S0290_RR`#331; `J56_RR`#332; `J57_RR`#333 | J56, J57; rest unmapped | B/body+ |
| `Mirror_Cap` #334 @32 | `S0102_R&{P}` IDs [336, 337, 338, 339, 340, 341, 342, 343, 344, 345]; `5JR_R`#346 | 5JR; rest unmapped | B/body+ |
| `Mirrors` #347 @33 | No native children | Unmapped | B/body+ |
| `Mirror_Cap` #349 @34 | `DRG_R`#351 | DRG; rest unmapped | B/body+ |
| `Mirrors` #352 @35 | `VA5`#354; `DYX_R`#355; `DWK_R`#356 | DWK, DYX; rest unmapped | B/body+ |
| `Doors` #364 @38 | `S0536`#366 | Unmapped | B/body+ |
| `None` #465 @41 | `S0420`#467 | Unmapped | B/body+ |
| `None` #519 @44 | `VSN`#521 | Unmapped | B/body+ |
| `Roof` #522 @45 | `SBT`#524; `S0243&{P}` IDs [525, 526, 527, 528, 529, 530, 531, 532, 533, 534]; `C2Z&{P}` IDs [535, 536, 537, 538, 539, 540, 541, 542, 543, 544]; `CF7&{P}` IDs [545, 546, 547, 548, 549, 550, 551, 552, 553, 554]; `CF8&{P}` IDs [555, 556, 557, 558, 559, 560, 561, 562, 563, 564]; `CC3`#565; `S0506`#566; `UG1&HUV`#567; `UG1&HU7`#568; `UG1&HUL`#569; `UG1&HUR`#570; `UG1&HUK`#571; `UG1&HU6`#572; `UG1&HUN`#573; `UG1&HTP`#574; `UG1&H1Y`#575; `UG1&HTE`#576; `UG1&HTT`#577; `UG1&HVV`#578; `UG1&HU1`#579; `UG1&HMO`#580; `UG1&HU9`#581; `UG1&HZB`#582; `UG1&HVT`#583; `UG1&HUA`#584; `UG1&HU2`#585; `UG1&HUU`#586; `UG1&HZP`#587; `UG1&HUE`#588; `UG1&HTG`#589; `UG1&HZN`#590; `UG1&HUF`#591; `UG1&HU0`#592; `UG1&HXO`#593; `UG1&HNK`#594; `UG1&HUW`#595; `UG1&HUX`#596; `UG1&HVZ`#597; `UG1&H8T`#598; `UG1&HUB`#599; `UG1&HUC`#600; `UG1&EPX`#601; `UG1&EJH`#602; `UG1&HAG`#603; `UG1&HTA`#604; `UG1&HTM`#605; `UG1&HTQ`#606; `UG1&HTN`#607 | C2Z, CC3, CF7, CF8, SBT, UG1; rest unmapped | B/body+ |
| `Headlamps` #614 @48 | `T4L`#616 | T4L; rest unmapped | B/body+ |
| `Badges` #1198 @65 | `CFX`#1200; `BV4`#1201; `S0500`#1202 | BV4, CFX; rest unmapped | B/body+ |
| `Radio` #1382 @71 | No native children | Unmapped | B/body+ |
| `B_Pillars` #1431 @73 | `S0212&{P}` IDs [1433, 1434, 1435, 1436, 1437, 1438, 1439, 1440, 1441, 1442] | Unmapped | B/body+ |
| `Engine` #1443 @74 | `S0495`#1445; `LT6`#1446 | LT6; rest unmapped | B/body+ |
| `Tow_Hooks` #1447 @75 | `S0871`#1449 | Unmapped | B/body+ |
| `Exhaust` #1450 @76 | `S0867`#1452; `S0868`#1453; `WUB`#1454 | WUB; rest unmapped | B/body+ |
| `Splashguards` #1467 @78 | `S0390`#1469 | Unmapped | B/body+ |
| `Primer` #1470 @79 | `S0115`#1472 | Unmapped | B/body+ |
| `Grille` #1489 @82 | `VWE`#1491 | VWE; rest unmapped | B/body- |
| `Mirror_Cap` #1495 @84 | `S0102_L&{P}` IDs [1497, 1498, 1499, 1500, 1501, 1502, 1503, 1504, 1505, 1506]; `5JR_L`#1507 | 5JR; rest unmapped | B/body- |
| `Mirrors` #1508 @85 | `UFT_L`#1510 | UFT; rest unmapped | B/body- |
| `Mirror_Cap` #1511 @86 | `DRG_L`#1513 | DRG; rest unmapped | B/body- |
| `Mirrors` #1514 @87 | `DYX_L`#1516; `DWK_L`#1517 | DWK, DYX; rest unmapped | B/body- |
| `Wheels` #1518 @88 | `S0817_RL`#1520; `S0818_RL`#1521; `S0453_RL`#1522; `S0447_RL`#1523; `S0439_RL`#1524; `S0440_RL`#1525; `S0451_RL`#1526; `S0449_RL`#1527; `S0435_RL`#1528; `S0436_RL`#1529; `S0437_RL`#1530; `S0438_RL`#1531; `S0433_RL`#1532; `S0434_RL`#1533; `S0431_RL`#1534; `S0432_RL`#1535; `S0429_RL`#1536; `S0430_RL`#1537; `S0423_RL`#1538; `S0424_RL`#1539; `S0427_RL`#1540; `S0426_RL`#1541; `S0428_RL`#1542; `S0425_RL`#1543; `S0391_RL`#1544; `S0392_RL`#1545; `S0393_RL`#1546; `S0394_RL`#1547; `S0421_RL`#1548; `S0422_RL`#1549 | Unmapped | B/body- |
| `Wheel_Caps` #1550 @89 | `S0387_RL`#1552; `S0383_RL`#1553; `S0269_RL`#1554; `S0380_RL`#1555; `S0406_RL`#1556 | Unmapped | B/body- |
| `Brakes` #1557 @90 | `S0292_RL`#1559; `S0290_RL`#1560; `S0289_RL`#1561; `S0293_RL`#1562; `S0288_RL`#1563; `S0296_RL`#1564; `S0295_RL`#1565; `S0294_RL`#1566; `S0291_RL`#1567; `J57_RL`#1568; `J56_RL`#1569 | J56, J57; rest unmapped | B/body- |
| `Wheels` #1570 @91 | `S0817_FL`#1572; `S0819_FL`#1573; `S0426_FL`#1574; `S0428_FL`#1575; `S0447_FL`#1576; `S0440_FL`#1577; `S0449_FL`#1578; `S0433_FL`#1579; `S0432_FL`#1580; `S0391_FL`#1581; `S0394_FL`#1582; `S0422_FL`#1583 | Unmapped | B/body- |
| `Wheel_Caps` #1584 @92 | `S0384_FL`#1586; `S0382_FL`#1587; `S0383_FL`#1588; `S0380_FL`#1589; `S0387_FL`#1590; `S0419_FL`#1591; `S0416_FL`#1592; `S0415_FL`#1593 | Unmapped | B/body- |
| `Brakes` #1594 @93 | `S0289_FL`#1596; `J57_FL`#1597 | J57; rest unmapped | B/body- |
| `Shadow` #1598 @94 | `S0902`#1600 | Unmapped | B/body- |
| `Background` #1601 @95 | `S0100`#1603 | Unmapped | B/body- |
| `Tow_Hooks` #1604 @96 | `S0869`#1606 | Unmapped | B/body- |

Cabin/trim-dependent groups visible through glass (separate interior scenes are outside this audit): `Console` #361 @37 (1 children); `Stitching` #367 @39 (6 children); `Steering_Wheel` #375 @40 (88 children); `Seat_Belts` #632 @51 (19 children); `Interior` #653 @52 (56 children); `Interior_Kit` #711 @53 (40 children); `Interior` #753 @54 (26 children); `Interior_Kit` #781 @55 (78 children); `IP` #861 @56 (1 children); `Decal_Stickers` #864 @57 (1 children); `Cluster` #867 @58 (46 children); `Stitching` #915 @59 (58 children); `Floors` #975 @60 (38 children); `Interior_Kit` #1015 @61 (1 children); `IP` #1018 @62 (44 children); `Seats_Front` #1064 @63 (129 children); `Interior` #1195 @64 (1 children); `Speakers` #1203 @66 (114 children); `IP` #1319 @67 (1 children); `Decal_Stickers` #1322 @68 (44 children); `Console` #1368 @69 (7 children); `Effects` #1384 @72 (45 children). Their seat/material/trim state must be recaptured for lower trims; no upper-trim interior is authorized as a substitute.

</details>

<details>
<summary>S15 — ZR1 convertible view 01</summary>

PSB: **V/zr1/exterior/27CHCOZR_CON_Studio_f02.psb**. Body-paint root index 86; spoiler root indices 76, 78.

<a id="s15-paint"></a>

**Paint — U; all ten base paints**

| Parent path / ID / root index | Exact paint-bearing peers (each maps only its paint token) | Native placement |
| --- | --- | --- |
| `Enclosure_Rear` #16 @5 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Front_Fascia` #85 @17 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Mirror_Cap` #186 @25 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `B_Pillars` #215 @32 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Rear_Fascia` #268 @43 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Tailgate` #286 @46 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Roof` #300 @47 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Tailgate` #990 @73 | 2 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Spoiler` #1014 @76 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | S/body+ |
| `Tailgate` #1063 @85 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Base` #1077 @86 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body= |
| `Mirror_Cap` #1094 @88 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body- |

<a id="s15-foundation"></a>

**Trim and body foundation**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Base` #944 @68 | `S0507&1LZ`#946; `S0507&3LZ`#947 | Configuration/trim candidates | F/body+ |
| `Base` #1077 @86 | `GBA`#1079; `G8G`#1080; `GKZ`#1081; `GPH`#1082; `G26`#1083; `GBK`#1084; `G4Z`#1085; `GKA`#1086; `GTR`#1087; `GEC`#1088; `1YR67`#1089 | Configuration/trim candidates | B/body= |

<a id="s15-rear"></a>

**Rear spoiler / source-off-spoiler state**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Spoiler` #1014 @76 | `S0268`#1016; `S0267&{P}` IDs [1017, 1018, 1019, 1020, 1021, 1022, 1023, 1024, 1025, 1026]; `SIG`#1027 | SIG; rest unmapped | S/body+ |
| `Spoiler` #1031 @78 | `TOM`#1033 | TOM; rest unmapped | S/body+ |

Source-off-spoiler state: hide every `Spoiler` parent listed here; this is a visibility recipe, **not a catalog option ID**. No legal no-spoiler configuration is established by this operation.

<a id="s15-aero"></a>

**Front/side/hood/fascia aero candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Hood` #38 @7 | `S0298`#40 | Unmapped | F/body+ |
| `Front_Fascia` #71 @14 | `S0274`#73; `S0273`#74; `S0227`#75; `S0224`#76; `S0221`#77 | Unmapped | F/body+ |
| `Ground_Effects` #78 @15 | `S0396`#80; `S0368`#81 | Unmapped | F/body+ |
| `Front_Fascia` #85 @17 | `S0220&{P}` IDs [87, 88, 89, 90, 91, 92, 93, 94, 95, 96] | Unmapped | F/body+ |
| `Ground_Effects` #183 @24 | `S0366`#185 | Unmapped | F/body+ |
| `Rear_Fascia` #268 @43 | `S0204`#270; `S0203&{P}` IDs [271, 272, 273, 274, 275, 276, 277, 278, 279, 280] | Unmapped | F/body+ |
| `Hood` #283 @45 | `S0297`#285 | Unmapped | F/body+ |

<a id="s15-graphics"></a>

**Stripes / decals / color candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Stripes` #4 @1 | No native children | Unmapped | F/body+ |
| `Decals` #6 @2 | `S0484`#8; `S0911`#9; `S0879`#10 | Unmapped | F/body+ |
| `Decals` #41 @8 | `S0837_F`#43; `S0855_F`#44; `S0302_F`#45; `S0330_F`#46; `S0325_F`#47; `S0320_F`#48; `S0315_F`#49; `S0307_F`#50 | Unmapped | F/body+ |
| `Stripes` #51 @9 | `S0369_F`#53 | Unmapped | F/body+ |
| `Decals` #54 @10 | `S0362_F`#56; `S0349_F`#57; `S0342_F`#58; `S0314_F`#59; `S0306_F`#60; `S0910`#61 | Unmapped | F/body+ |
| `Decals` #234 @35 | `S0866`#236; `S0858`#237; `S0361`#238; `S0348`#239; `S0341`#240; `S0334`#241; `S0313`#242 | Unmapped | F/body+ |
| `Decals` #246 @37 | `S0332`#248; `S0327`#249; `S0322`#250; `S0317`#251; `S0304`#252; `S0303`#253; `S0308`#254 | Unmapped | F/body+ |
| `Decals` #995 @74 | `S0874`#997; `S0363`#998; `S0358`#999; `S0344`#1000; `S0338`#1001; `S0857`#1002; `S0319`#1003; `S0333`#1004; `S0328`#1005; `S0323`#1006; `S0318`#1007; `S0310`#1008; `S0309`#1009; `S0311`#1010 | Unmapped | F/body+ |
| `Decals` #1043 @82 | `S0855_B`#1045; `S0837_B`#1046; `S0330_B`#1047; `S0320_B`#1048; `S0315_B`#1049; `S0307_B`#1050; `S0325_B`#1051 | Unmapped | B/body+ |
| `Stripes` #1052 @83 | `S0369_B`#1054 | Unmapped | B/body+ |
| `Decals` #1055 @84 | `S0362_B`#1057; `S0349_B`#1058; `S0342_B`#1059; `S0314_B`#1060; `S0306_B`#1061; `S0302_B`#1062 | Unmapped | B/body+ |

<a id="s15-glass"></a>

**Glass and window candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Windows` #212 @31 | `S0105`#214 | Unmapped | F/body+ |
| `Windows` #228 @33 | `S0101_L`#230 | Unmapped | F/body+ |
| `Windows` #984 @71 | `S0104`#986 | Unmapped | F/body+ |
| `Defroster` #987 @72 | `S0107`#989 | Unmapped | F/body+ |
| `Windows` #1090 @87 | `S0101_B`#1092; `S0101_R`#1093 | Unmapped | B/body- |

<a id="s15-other"></a>

**Other exterior option-driven and fixed groups**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Tow_Hooks` #1 @0 | No native children | Unmapped | F/body+ |
| `Tailgate` #11 @3 | `S0475`#13 | Unmapped | F/body+ |
| `Engine` #14 @4 | No native children | Unmapped | F/body+ |
| `Enclosure_Rear` #16 @5 | `S0127&{P}` IDs [18, 19, 20, 21, 22, 23, 24, 25, 26, 27] | Unmapped | F/body+ |
| `Badges` #28 @6 | `EYK_F`#30; `EYT_F`#31; `EYT_B`#32; `SFZ_F`#33; `S0279`#34; `R88_F`#35; `S0499`#36; `S0498`#37 | EYK, EYT, R88, SFZ; rest unmapped | F/body+ |
| `Tail_Lamps` #62 @11 | `S0200`#64 | Unmapped | F/body+ |
| `Headlamps` #65 @12 | `T4L`#67 | T4L; rest unmapped | F/body+ |
| `Molding` #68 @13 | `S0209`#70 | Unmapped | F/body+ |
| `Grille` #82 @16 | `VWE`#84 | VWE; rest unmapped | F/body+ |
| `Wheels` #97 @18 | `S0821_RL`#99; `S0822_RL`#100; `S0804_RL`#101; `S0805_RL`#102; `S0802_RL`#103; `S0803_RL`#104; `S0808_RL`#105; `S0809_RL`#106; `S0800_RL`#107; `S0801_RL`#108; `S0806_RL`#109; `S0807_RL`#110 | Unmapped | F/body+ |
| `Wheel_Caps` #111 @19 | `S0835_RL`#113; `S0836_RL`#114; `S0832_RL`#115; `S0833_RL`#116; `S0834_RL`#117; `S0831_RL`#118; `S0830_RL`#119; `S0906_RL`#120; `S0905_RL`#121 | Unmapped | F/body+ |
| `Brakes` #122 @20 | `S0286_RL`#124; `S0222_RL`#125; `S0206_RL`#126; `S0208_RL`#127; `S0210_RL`#128; `S0218_RL`#129; `S0225_RL`#130; `S0228_RL`#131; `S0285_RL`#132; `S0375_RL`#133; `S0376_RL`#134; `S0377_RL`#135; `S0378_RL`#136; `S0389_RL`#137; `J59_RL`#138; `J58_RL`#139 | J58, J59; rest unmapped | F/body+ |
| `Wheels` #140 @21 | `S0821_FL`#142; `S0822_FL`#143; `S0804_FL`#144; `S0805_FL`#145; `S0802_FL`#146; `S0803_FL`#147; `S0808_FL`#148; `S0809_FL`#149; `S0800_FL`#150; `S0801_FL`#151; `S0806_FL`#152; `S0807_FL`#153 | Unmapped | F/body+ |
| `Wheel_Caps` #154 @22 | `S0906_FL`#156; `S0905_FL`#157; `S0835_FL`#158; `S0836_FL`#159; `S0832_FL`#160; `S0833_FL`#161; `S0834_FL`#162; `S0831_FL`#163; `S0830_FL`#164 | Unmapped | F/body+ |
| `Brakes` #165 @23 | `S0286_FL`#167; `S0206_FL`#168; `S0208_FL`#169; `S0210_FL`#170; `S0218_FL`#171; `S0222_FL`#172; `S0225_FL`#173; `S0228_FL`#174; `S0285_FL`#175; `S0375_FL`#176; `S0376_FL`#177; `S0377_FL`#178; `S0378_FL`#179; `S0389_FL`#180; `J59_FL`#181; `J58_FL`#182 | J58, J59; rest unmapped | F/body+ |
| `Mirror_Cap` #186 @25 | `S0102_L&{P}` IDs [188, 189, 190, 191, 192, 193, 194, 195, 196, 197] | Unmapped | F/body+ |
| `Mirrors` #198 @26 | No native children | Unmapped | F/body+ |
| `Mirror_Cap` #200 @27 | `5JR_L`#202 | 5JR; rest unmapped | F/body+ |
| `Mirrors` #203 @28 | No native children | Unmapped | F/body+ |
| `Mirror_Cap` #205 @29 | `DRG_L`#207 | DRG; rest unmapped | F/body+ |
| `Mirrors` #208 @30 | `DYX_L`#210; `DWK_L`#211 | DWK, DYX; rest unmapped | F/body+ |
| `B_Pillars` #215 @32 | `S0236&{P}` IDs [217, 218, 219, 220, 221, 222, 223, 224, 225, 226]; `S0213`#227 | Unmapped | F/body+ |
| `Primer` #231 @34 | `S0115`#233 | Unmapped | F/body+ |
| `None` #243 @36 | `S0345`#245 | Unmapped | F/body+ |
| `Doors` #257 @39 | `S0536`#259 | Unmapped | F/body+ |
| `None` #260 @40 | `S0420`#262 | Unmapped | F/body+ |
| `Splashguards` #263 @41 | `S0390`#265 | Unmapped | F/body+ |
| `License_Plate` #266 @42 | No native children | Unmapped | F/body+ |
| `Multimedia` #281 @44 | No native children | Unmapped | F/body+ |
| `Tailgate` #286 @46 | `S0135_L&{P}` IDs [288, 289, 290, 291, 292, 293, 294, 295, 296, 297]; `S0136_L`#298; `S0113_L`#299 | Unmapped | F/body+ |
| `Roof` #300 @47 | `CFC&{P}` IDs [302, 303, 304, 305, 306, 307, 308, 309, 310, 311]; `S0841`#312; `S0840`#313; `S0506`#314; `UG1&HTE`#315; `UG1&HTT`#316; `UG1&HVV`#317; `UG1&HU1`#318; `UG1&HMO`#319; `UG1&HU9`#320; `UG1&HZB`#321; `UG1&HVT`#322; `UG1&HUA`#323; `UG1&HU2`#324; `UG1&HUU`#325; `UG1&HZP`#326; `UG1&HUE`#327; `UG1&HTG`#328; `UG1&HZN`#329; `UG1&HUF`#330; `UG1&HU0`#331; `UG1&HXO`#332; `UG1&HNK`#333; `UG1&HUW`#334; `UG1&HUX`#335; `UG1&HVZ`#336; `UG1&H8T`#337; `UG1&HUB`#338; `UG1&HUC`#339; `UG1&EPX`#340; `UG1&EJH`#341; `UG1&HAG`#342 | CFC, UG1; rest unmapped | F/body+ |
| `Badges` #772 @60 | `BV4`#774; `S0500`#775 | BV4; rest unmapped | F/body+ |
| `Radio` #948 @69 | No native children | Unmapped | F/body+ |
| `Tailgate` #990 @73 | `S0478&GKA`#992; `S0478&GTR`#993; `S0217`#994 | Unmapped | F/body+ |
| `None` #1011 @75 | `S0357`#1013 | Unmapped | F/body+ |
| `None` #1028 @77 | `S0119`#1030 | Unmapped | S/body+ |
| `Engine` #1034 @79 | `LT7`#1036 | LT7; rest unmapped | B/body+ |
| `Exhaust` #1037 @80 | `WUB`#1039 | WUB; rest unmapped | B/body+ |
| `Tow_Hooks` #1040 @81 | `S0871`#1042 | Unmapped | B/body+ |
| `Tailgate` #1063 @85 | `S0135_R&{P}` IDs [1065, 1066, 1067, 1068, 1069, 1070, 1071, 1072, 1073, 1074]; `S0136_R`#1075; `S0113_R`#1076 | Unmapped | B/body+ |
| `Mirror_Cap` #1094 @88 | `S0102_R&{P}` IDs [1096, 1097, 1098, 1099, 1100, 1101, 1102, 1103, 1104, 1105]; `5JR_R`#1106 | 5JR; rest unmapped | B/body- |
| `Mirrors` #1107 @89 | No native children | Unmapped | B/body- |
| `Mirror_Cap` #1109 @90 | `DRG_R`#1111 | DRG; rest unmapped | B/body- |
| `Mirrors` #1112 @91 | `DYX_R`#1114; `DWK_R`#1115 | DWK, DYX; rest unmapped | B/body- |
| `Wheels` #1116 @92 | `S0804_RR`#1118; `S0805_RR`#1119; `S0802_RR`#1120; `S0803_RR`#1121; `S0809_RR`#1122; `S0800_RR`#1123; `S0801_RR`#1124; `S0806_RR`#1125; `S0807_RR`#1126; `S0822_RR`#1127 | Unmapped | B/body- |
| `Wheel_Caps` #1128 @93 | `S0833_RR`#1130 | Unmapped | B/body- |
| `Brakes` #1131 @94 | `S0210_RR`#1133; `J58_RR`#1134 | J58; rest unmapped | B/body- |
| `Wheels` #1135 @95 | `S0822_FR`#1137; `S0808_FR`#1138; `S0809_FR`#1139 | Unmapped | B/body- |
| `Wheel_Caps` #1140 @96 | `S0835_FR`#1142; `S0836_FR`#1143; `S0833_FR`#1144; `S0831_FR`#1145; `S0830_FR`#1146 | Unmapped | B/body- |
| `Brakes` #1147 @97 | `S0376_FR`#1149; `S0389_FR`#1150; `J59_FR`#1151; `J58_FR`#1152 | J58, J59; rest unmapped | B/body- |
| `Shadow` #1153 @98 | `S0902`#1155 | Unmapped | B/body- |
| `Background` #1156 @99 | `S0100`#1158 | Unmapped | B/body- |

Cabin/trim-dependent groups visible through glass (separate interior scenes are outside this audit): `Console` #255 @38 (0 children); `Stitching` #343 @48 (9 children); `Steering_Wheel` #354 @49 (38 children); `Interior_Kit` #394 @50 (1 children); `Interior` #397 @51 (51 children); `Interior_Kit` #450 @52 (24 children); `Interior` #476 @53 (28 children); `Interior_Kit` #506 @54 (51 children); `Stitching` #559 @55 (34 children); `Seat_Belts` #595 @56 (20 children); `Seats_Front` #617 @57 (119 children); `Floors` #738 @58 (28 children); `Cluster` #768 @59 (2 children); `IP` #776 @61 (1 children); `Decal_Stickers` #779 @62 (1 children); `Stitching` #782 @63 (3 children); `IP` #787 @64 (1 children); `Decal_Stickers` #790 @65 (32 children); `IP` #824 @66 (32 children); `Speakers` #858 @67 (84 children); `Effects` #950 @70 (32 children); `Console` #1159 @100 (7 children). Their seat/material/trim state must be recaptured for lower trims; no upper-trim interior is authorized as a substitute.

</details>

<details>
<summary>S16 — ZR1 convertible view 02</summary>

PSB: **V/zr1/exterior/27CHCOZR_CON_Studio_f04.psb**. Body-paint root index 87; spoiler root indices 6, 9, 11.

<a id="s16-paint"></a>

**Paint — U; all ten base paints**

| Parent path / ID / root index | Exact paint-bearing peers (each maps only its paint token) | Native placement |
| --- | --- | --- |
| `Tailgate` #7 @2 | 1 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Enclosure_Rear` #12 @4 | 8 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Spoiler` #48 @9 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | S/body+ |
| `Tailgate` #124 @20 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Tailgate` #264 @36 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Mirror_Cap` #278 @37 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Roof` #399 @51 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Front_Fascia` #449 @55 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `B_Pillars` #1078 @78 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Rear_Fascia` #1102 @82 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Base` #1126 @87 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body= |
| `Mirror_Cap` #1145 @90 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body- |

<a id="s16-foundation"></a>

**Trim and body foundation**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Base` #1038 @75 | `S0507&1LZ`#1040; `S0507&3LZ`#1041 | Configuration/trim candidates | B/body+ |
| `Base` #1126 @87 | `GBA`#1128; `G8G`#1129; `GKZ`#1130; `GPH`#1131; `G26`#1132; `GBK`#1133; `G4Z`#1134; `GKA`#1135; `GTR`#1136; `GEC`#1137; `1YR67`#1138 | Configuration/trim candidates | B/body= |

<a id="s16-rear"></a>

**Rear spoiler / source-off-spoiler state**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Spoiler` #26 @6 | `SIG`#28 | SIG; rest unmapped | S/body+ |
| `Spoiler` #48 @9 | `S0268`#50; `S0267&{P}` IDs [51, 52, 53, 54, 55, 56, 57, 58, 59, 60] | Unmapped | S/body+ |
| `Spoiler` #64 @11 | `TOM`#66 | TOM; rest unmapped | S/body+ |

Source-off-spoiler state: hide every `Spoiler` parent listed here; this is a visibility recipe, **not a catalog option ID**. No legal no-spoiler configuration is established by this operation.

<a id="s16-aero"></a>

**Front/side/hood/fascia aero candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Hood` #78 @13 | `S0298`#80 | Unmapped | B/body+ |
| `Rear_Fascia` #163 @25 | `S0204`#165 | Unmapped | B/body+ |
| `Ground_Effects` #175 @29 | `S0366`#177 | Unmapped | B/body+ |
| `Front_Fascia` #384 @47 | `S0274`#386; `S0273`#387 | Unmapped | B/body+ |
| `Ground_Effects` #388 @48 | `S0396`#390; `S0368`#391 | Unmapped | B/body+ |
| `Front_Fascia` #449 @55 | `S0220&{P}` IDs [451, 452, 453, 454, 455, 456, 457, 458, 459, 460] | Unmapped | B/body+ |
| `Rear_Fascia` #1102 @82 | `S0203&{P}` IDs [1104, 1105, 1106, 1107, 1108, 1109, 1110, 1111, 1112, 1113] | Unmapped | B/body+ |
| `Hood` #1123 @86 | `S0297`#1125 | Unmapped | B/body+ |

<a id="s16-graphics"></a>

**Stripes / decals / color candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Stripes` #1 @0 | No native children | Unmapped | F/body+ |
| `Decals` #3 @1 | `S0489`#5; `S0494`#6 | Unmapped | F/body+ |
| `Decals` #29 @7 | `S0874`#31; `S0363`#32; `S0358`#33; `S0344`#34; `S0338`#35; `S0857`#36; `S0319`#37; `S0333`#38; `S0328`#39; `S0323`#40; `S0318`#41; `S0310`#42; `S0309`#43; `S0311`#44 | Unmapped | S/body+ |
| `Decals` #81 @14 | `S0837_F`#83; `S0855_F`#84; `S0302_F`#85; `S0330_F`#86; `S0325_F`#87; `S0320_F`#88; `S0315_F`#89; `S0307_F`#90 | Unmapped | B/body+ |
| `Stripes` #91 @15 | `S0369_F`#93 | Unmapped | B/body+ |
| `Decals` #94 @16 | `S0362_F`#96; `S0349_F`#97; `S0342_F`#98; `S0314_F`#99; `S0306_F`#100; `S0910`#101; `S0866`#102; `S0858`#103; `S0361`#104; `S0348`#105; `S0341`#106; `S0334`#107; `S0313`#108 | Unmapped | B/body+ |
| `Decals` #112 @18 | `S0332`#114; `S0327`#115; `S0322`#116; `S0317`#117; `S0304`#118; `S0303`#119; `S0308`#120 | Unmapped | B/body+ |
| `Decals` #139 @21 | `S0855_B`#141; `S0837_B`#142; `S0330_B`#143; `S0320_B`#144; `S0315_B`#145; `S0307_B`#146; `S0325_B`#147 | Unmapped | B/body+ |
| `Stripes` #148 @22 | `S0369_B`#150 | Unmapped | B/body+ |
| `Decals` #151 @23 | `S0362_B`#153; `S0349_B`#154; `S0342_B`#155; `S0314_B`#156; `S0306_B`#157; `S0302_B`#158 | Unmapped | B/body+ |
| `Decals` #169 @27 | `S0912`#171 | Unmapped | B/body+ |
| `Decals` #396 @50 | `S0911`#398 | Unmapped | B/body+ |

<a id="s16-glass"></a>

**Glass and window candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Windows` #301 @41 | `S0101_R`#303; `S0101_B`#304 | Unmapped | B/body+ |
| `Defroster` #440 @52 | `S0107`#442 | Unmapped | B/body+ |
| `Windows` #443 @53 | `S0104`#445 | Unmapped | B/body+ |
| `Windows` #1120 @85 | `S0105`#1122 | Unmapped | B/body+ |
| `Windows` #1142 @89 | `S0101_L`#1144 | Unmapped | B/body- |

<a id="s16-other"></a>

**Other exterior option-driven and fixed groups**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Tailgate` #7 @2 | `S0478&GKA`#9 | Unmapped | F/body+ |
| `Engine` #10 @3 | No native children | Unmapped | F/body+ |
| `Enclosure_Rear` #12 @4 | `S0127&GBA`#14; `S0127&G8G`#15; `S0127&GPH`#16; `S0127&G26`#17; `S0127&GBK`#18; `S0127&G4Z`#19; `S0127&GKA`#20; `S0127&GTR`#21 | Unmapped | F/body+ |
| `Badges` #22 @5 | `S0499`#24; `S0498`#25 | Unmapped | F/body+ |
| `None` #45 @8 | `S0357`#47 | Unmapped | S/body+ |
| `None` #61 @10 | `S0119`#63 | Unmapped | S/body+ |
| `Badges` #67 @12 | `SL8`#69; `RIN`#70; `RIK`#71; `EYK_B`#72; `EYT_B`#73; `SFZ_B`#74; `S0276`#75; `S0279`#76; `R88_B`#77 | EYK, EYT, R88, RIK, RIN, SFZ, SL8; rest unmapped | B/body+ |
| `None` #109 @17 | `S0345`#111 | Unmapped | B/body+ |
| `Tail_Lamps` #121 @19 | `S0200`#123 | Unmapped | B/body+ |
| `Tailgate` #124 @20 | `S0135_R&{P}` IDs [126, 127, 128, 129, 130, 131, 132, 133, 134, 135]; `S0136_R`#136; `S0113_R`#137; `S0217`#138 | Unmapped | B/body+ |
| `Multimedia` #159 @24 | `S0287`#161; `S0244`#162 | Unmapped | B/body+ |
| `License_Plate` #166 @26 | `S0235`#168 | Unmapped | B/body+ |
| `Molding` #172 @28 | `S0209`#174 | Unmapped | B/body+ |
| `Wheels` #178 @30 | `S0821_FR`#180; `S0822_FR`#181; `S0804_FR`#182; `S0805_FR`#183; `S0802_FR`#184; `S0803_FR`#185; `S0808_FR`#186; `S0809_FR`#187; `S0800_FR`#188; `S0801_FR`#189; `S0806_FR`#190; `S0807_FR`#191 | Unmapped | B/body+ |
| `Wheel_Caps` #192 @31 | `S0905_FR`#194; `S0906_FR`#195; `S0835_FR`#196; `S0836_FR`#197; `S0832_FR`#198; `S0833_FR`#199; `S0834_FR`#200; `S0831_FR`#201; `S0830_FR`#202 | Unmapped | B/body+ |
| `Brakes` #203 @32 | `S0286_FR`#205; `S0222_FR`#206; `S0206_FR`#207; `S0208_FR`#208; `S0210_FR`#209; `S0218_FR`#210; `S0225_FR`#211; `S0228_FR`#212; `S0285_FR`#213; `S0375_FR`#214; `S0376_FR`#215; `S0377_FR`#216; `S0378_FR`#217; `S0389_FR`#218; `J59_FR`#219; `J58_FR`#220 | J58, J59; rest unmapped | B/body+ |
| `Wheels` #221 @33 | `S0821_RR`#223; `S0822_RR`#224; `S0804_RR`#225; `S0805_RR`#226; `S0802_RR`#227; `S0803_RR`#228; `S0808_RR`#229; `S0809_RR`#230; `S0800_RR`#231; `S0801_RR`#232; `S0806_RR`#233; `S0807_RR`#234 | Unmapped | B/body+ |
| `Wheel_Caps` #235 @34 | `S0905_RR`#237; `S0906_RR`#238; `S0835_RR`#239; `S0836_RR`#240; `S0833_RR`#241; `S0832_RR`#242; `S0834_RR`#243; `S0831_RR`#244; `S0830_RR`#245 | Unmapped | B/body+ |
| `Brakes` #246 @35 | `S0286_RR`#248; `S0222_RR`#249; `S0206_RR`#250; `S0208_RR`#251; `S0210_RR`#252; `S0218_RR`#253; `S0225_RR`#254; `S0228_RR`#255; `S0285_RR`#256; `S0375_RR`#257; `S0376_RR`#258; `S0377_RR`#259; `S0378_RR`#260; `S0389_RR`#261; `J59_RR`#262; `J58_RR`#263 | J58, J59; rest unmapped | B/body+ |
| `Tailgate` #264 @36 | `S0135_L&{P}` IDs [266, 267, 268, 269, 270, 271, 272, 273, 274, 275]; `S0136_L`#276; `S0113_L`#277 | Unmapped | B/body+ |
| `Mirror_Cap` #278 @37 | `S0102_R&{P}` IDs [280, 281, 282, 283, 284, 285, 286, 287, 288, 289]; `5JR_R`#290 | 5JR; rest unmapped | B/body+ |
| `Mirrors` #291 @38 | No native children | Unmapped | B/body+ |
| `Mirror_Cap` #293 @39 | `DRG_R`#295 | DRG; rest unmapped | B/body+ |
| `Mirrors` #296 @40 | `VA5`#298; `DYX_R`#299; `DWK_R`#300 | DWK, DYX; rest unmapped | B/body+ |
| `Doors` #307 @43 | `S0536`#309 | Unmapped | B/body+ |
| `None` #381 @46 | `S0420`#383 | Unmapped | B/body+ |
| `Roof` #392 @49 | `S0841`#394; `S0840`#395 | Unmapped | B/body+ |
| `Roof` #399 @51 | `CFC&{P}` IDs [401, 402, 403, 404, 405, 406, 407, 408, 409, 410]; `S0506`#411; `UG1&HTE`#412; `UG1&HTT`#413; `UG1&HVV`#414; `UG1&HU1`#415; `UG1&HMO`#416; `UG1&HU9`#417; `UG1&HZB`#418; `UG1&HVT`#419; `UG1&HUA`#420; `UG1&HU2`#421; `UG1&HUU`#422; `UG1&HZP`#423; `UG1&HUE`#424; `UG1&HTG`#425; `UG1&HZN`#426; `UG1&HUF`#427; `UG1&HU0`#428; `UG1&HXO`#429; `UG1&HNK`#430; `UG1&HUW`#431; `UG1&HUX`#432; `UG1&HVZ`#433; `UG1&H8T`#434; `UG1&HUB`#435; `UG1&HUC`#436; `UG1&EPX`#437; `UG1&EJH`#438; `UG1&HAG`#439 | CFC, UG1; rest unmapped | B/body+ |
| `Headlamps` #446 @54 | `T4L`#448 | T4L; rest unmapped | B/body+ |
| `Badges` #906 @70 | `CFX`#908; `BV4`#909; `S0500`#910 | BV4, CFX; rest unmapped | B/body+ |
| `Radio` #1042 @76 | No native children | Unmapped | B/body+ |
| `B_Pillars` #1078 @78 | `S0236&{P}` IDs [1080, 1081, 1082, 1083, 1084, 1085, 1086, 1087, 1088, 1089]; `S0213`#1090 | Unmapped | B/body+ |
| `Engine` #1091 @79 | `LT7`#1093 | LT7; rest unmapped | B/body+ |
| `Tow_Hooks` #1094 @80 | `S0871`#1096 | Unmapped | B/body+ |
| `Exhaust` #1097 @81 | `S0867`#1099; `S0868`#1100; `WUB`#1101 | WUB; rest unmapped | B/body+ |
| `Splashguards` #1114 @83 | `S0390`#1116 | Unmapped | B/body+ |
| `Primer` #1117 @84 | `S0115`#1119 | Unmapped | B/body+ |
| `Grille` #1139 @88 | `VWE`#1141 | VWE; rest unmapped | B/body- |
| `Mirror_Cap` #1145 @90 | `S0102_L&{P}` IDs [1147, 1148, 1149, 1150, 1151, 1152, 1153, 1154, 1155, 1156]; `5JR_L`#1157 | 5JR; rest unmapped | B/body- |
| `Mirrors` #1158 @91 | No native children | Unmapped | B/body- |
| `Mirror_Cap` #1160 @92 | `DRG_L`#1162 | DRG; rest unmapped | B/body- |
| `Mirrors` #1163 @93 | `DYX_L`#1165; `DWK_L`#1166 | DWK, DYX; rest unmapped | B/body- |
| `Wheels` #1167 @94 | `S0822_RL`#1169; `S0804_RL`#1170; `S0805_RL`#1171; `S0802_RL`#1172; `S0803_RL`#1173; `S0808_RL`#1174; `S0809_RL`#1175; `S0800_RL`#1176; `S0801_RL`#1177; `S0806_RL`#1178; `S0807_RL`#1179 | Unmapped | B/body- |
| `Wheel_Caps` #1180 @95 | `S0833_RL`#1182; `S0831_RL`#1183; `S0830_RL`#1184 | Unmapped | B/body- |
| `Brakes` #1185 @96 | `S0286_RL`#1187; `S0222_RL`#1188; `S0206_RL`#1189; `S0208_RL`#1190; `S0210_RL`#1191; `S0218_RL`#1192; `S0225_RL`#1193; `S0228_RL`#1194; `S0285_RL`#1195; `S0375_RL`#1196; `S0376_RL`#1197; `S0377_RL`#1198; `S0378_RL`#1199; `S0389_RL`#1200; `J59_RL`#1201; `J58_RL`#1202 | J58, J59; rest unmapped | B/body- |
| `Wheels` #1203 @97 | `S0822_FL`#1205; `S0805_FL`#1206; `S0809_FL`#1207; `S0800_FL`#1208; `S0801_FL`#1209; `S0806_FL`#1210; `S0807_FL`#1211 | Unmapped | B/body- |
| `Wheel_Caps` #1212 @98 | `S0905_FL`#1214; `S0832_FL`#1215; `S0831_FL`#1216 | Unmapped | B/body- |
| `Brakes` #1217 @99 | `S0285_FL`#1219; `S0376_FL`#1220; `S0378_FL`#1221; `S0222_FL`#1222; `S0206_FL`#1223; `S0210_FL`#1224; `J58_FL`#1225 | J58; rest unmapped | B/body- |
| `Shadow` #1226 @100 | `S0902`#1228 | Unmapped | B/body- |
| `Background` #1229 @101 | `S0100`#1231 | Unmapped | B/body- |
| `Tow_Hooks` #1232 @102 | `S0869`#1234 | Unmapped | B/body- |

Cabin/trim-dependent groups visible through glass (separate interior scenes are outside this audit): `Console` #305 @42 (0 children); `Stitching` #310 @44 (3 children); `Steering_Wheel` #315 @45 (64 children); `Seat_Belts` #461 @56 (18 children); `Interior` #481 @57 (58 children); `Interior_Kit` #541 @58 (26 children); `Interior` #569 @59 (27 children); `Interior_Kit` #598 @60 (54 children); `IP` #654 @61 (1 children); `Decal_Stickers` #657 @62 (1 children); `Cluster` #660 @63 (2 children); `Stitching` #664 @64 (46 children); `Floors` #712 @65 (32 children); `Interior_Kit` #746 @66 (0 children); `IP` #748 @67 (32 children); `Seats_Front` #782 @68 (119 children); `Interior` #903 @69 (1 children); `Speakers` #911 @71 (80 children); `IP` #993 @72 (0 children); `Decal_Stickers` #995 @73 (32 children); `Console` #1029 @74 (7 children); `Effects` #1044 @77 (32 children). Their seat/material/trim state must be recaptured for lower trims; no upper-trim interior is authorized as a substitute.

</details>

<details>
<summary>S17 — ZR1 coupe view 01</summary>

PSB: **V/zr1/exterior/27CHCOZR_COU_Studio_f02.psb**. Body-paint root index 80; spoiler root indices 71, 73.

<a id="s17-paint"></a>

**Paint — U; all ten base paints**

| Parent path / ID / root index | Exact paint-bearing peers (each maps only its paint token) | Native placement |
| --- | --- | --- |
| `Front_Fascia` #63 @13 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Mirror_Cap` #164 @21 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `B_Pillars` #193 @28 | 20 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Rear_Fascia` #258 @40 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Roof` #275 @43 | 31 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Spoiler` #1018 @71 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | S/body+ |
| `Base` #1085 @80 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body= |
| `Rear_Van_Windows` #1098 @81 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body- |
| `Mirror_Cap` #1115 @83 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body- |

<a id="s17-foundation"></a>

**Trim and body foundation**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Base` #952 @64 | `S0507&1LZ`#954; `S0507&3LZ`#955 | Configuration/trim candidates | F/body+ |
| `Base` #1085 @80 | `GBA`#1087; `G8G`#1088; `GKZ`#1089; `GPH`#1090; `G26`#1091; `GBK`#1092; `G4Z`#1093; `GKA`#1094; `GTR`#1095; `GEC`#1096; `1YR07`#1097 | Configuration/trim candidates | B/body= |

<a id="s17-rear"></a>

**Rear spoiler / source-off-spoiler state**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Spoiler` #1018 @71 | `S0268`#1020; `S0267&{P}` IDs [1021, 1022, 1023, 1024, 1025, 1026, 1027, 1028, 1029, 1030]; `SIG`#1031 | SIG; rest unmapped | S/body+ |
| `Spoiler` #1035 @73 | `TOM`#1037 | TOM; rest unmapped | S/body+ |

Source-off-spoiler state: hide every `Spoiler` parent listed here; this is a visibility recipe, **not a catalog option ID**. No legal no-spoiler configuration is established by this operation.

<a id="s17-aero"></a>

**Front/side/hood/fascia aero candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Hood` #16 @3 | `S0298`#18 | Unmapped | F/body+ |
| `Front_Fascia` #49 @10 | `S0274`#51; `S0273`#52; `S0227`#53; `S0224`#54; `S0221`#55 | Unmapped | F/body+ |
| `Ground_Effects` #56 @11 | `S0396`#58; `S0368`#59 | Unmapped | F/body+ |
| `Front_Fascia` #63 @13 | `S0220&{P}` IDs [65, 66, 67, 68, 69, 70, 71, 72, 73, 74] | Unmapped | F/body+ |
| `Ground_Effects` #161 @20 | `S0366`#163 | Unmapped | F/body+ |
| `Rear_Fascia` #258 @40 | `S0203&{P}` IDs [260, 261, 262, 263, 264, 265, 266, 267, 268, 269] | Unmapped | F/body+ |
| `Hood` #272 @42 | `S0297`#274 | Unmapped | F/body+ |

<a id="s17-graphics"></a>

**Stripes / decals / color candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Decals` #4 @1 | `S0911`#6 | Unmapped | F/body+ |
| `Decals` #19 @4 | `S0837_F`#21; `S0855_F`#22; `S0302_F`#23; `S0330_F`#24; `S0325_F`#25; `S0320_F`#26; `S0315_F`#27; `S0307_F`#28 | Unmapped | F/body+ |
| `Stripes` #29 @5 | `S0369_F`#31 | Unmapped | F/body+ |
| `Decals` #32 @6 | `S0362_F`#34; `S0349_F`#35; `S0342_F`#36; `S0314_F`#37; `S0306_F`#38; `S0910`#39 | Unmapped | F/body+ |
| `Decals` #221 @31 | `S0866`#223; `S0858`#224; `S0361`#225; `S0348`#226; `S0341`#227; `S0334`#228; `S0313`#229 | Unmapped | F/body+ |
| `Decals` #233 @33 | `S0332`#235; `S0327`#236; `S0322`#237; `S0317`#238; `S0304`#239; `S0303`#240; `S0308`#241 | Unmapped | F/body+ |
| `Decals` #999 @69 | `S0874`#1001; `S0363`#1002; `S0358`#1003; `S0344`#1004; `S0338`#1005; `S0857`#1006; `S0319`#1007; `S0333`#1008; `S0328`#1009; `S0323`#1010; `S0318`#1011; `S0310`#1012; `S0309`#1013; `S0311`#1014 | Unmapped | F/body+ |
| `Decals` #1046 @77 | `S0855_B`#1048; `S0837_B`#1049; `S0315_B`#1050 | Unmapped | B/body+ |
| `Stripes` #1051 @78 | No native children | Unmapped | B/body+ |
| `Decals` #1053 @79 | `S0349_B`#1055; `S0302_B`#1056; `S0886`#1057; `S0838`#1058; `S0853`#1059; `S0852`#1060; `S0851`#1061; `S0849`#1062; `S0848`#1063; `S0847`#1064; `S0846`#1065; `S0845`#1066; `S0844`#1067; `S0843`#1068; `S0842`#1069; `S0850`#1070; `S0360`#1071; `S0347`#1072; `S0340`#1073; `S0329`#1074; `S0312`#1075; `S0331`#1076; `S0326`#1077; `S0321`#1078; `S0316`#1079; `S0301`#1080; `S0300`#1081; `S0864`#1082; `S0859`#1083; `S0305`#1084 | Unmapped | B/body+ |

<a id="s17-glass"></a>

**Glass and window candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Windows` #190 @27 | `S0105`#192 | Unmapped | F/body+ |
| `Windows` #215 @29 | `S0101_L`#217 | Unmapped | F/body+ |
| `Windows` #253 @38 | `S0108`#255 | Unmapped | F/body+ |
| `Windows` #992 @67 | `S0122`#994; `S0104`#995 | Unmapped | F/body+ |
| `Defroster` #996 @68 | `S0107`#998 | Unmapped | F/body+ |
| `Rear_Van_Windows` #1098 @81 | `ETV&{P}` IDs [1100, 1101, 1102, 1103, 1104, 1105, 1106, 1107, 1108, 1109]; `S0201`#1110 | ETV; rest unmapped | B/body- |
| `Windows` #1111 @82 | `S0101_B`#1113; `S0101_R`#1114 | Unmapped | B/body- |

<a id="s17-other"></a>

**Other exterior option-driven and fixed groups**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Tow_Hooks` #1 @0 | No native children | Unmapped | F/body+ |
| `Badges` #7 @2 | `SL8`#9; `EYK_F`#10; `EYT_F`#11; `SFZ_F`#12; `R88_F`#13; `S0499`#14; `S0498`#15 | EYK, EYT, R88, SFZ, SL8; rest unmapped | F/body+ |
| `Tail_Lamps` #40 @7 | `S0200`#42 | Unmapped | F/body+ |
| `Headlamps` #43 @8 | `T4L`#45 | T4L; rest unmapped | F/body+ |
| `Molding` #46 @9 | `S0209`#48 | Unmapped | F/body+ |
| `Grille` #60 @12 | `VWE`#62 | VWE; rest unmapped | F/body+ |
| `Wheels` #75 @14 | `S0821_RL`#77; `S0822_RL`#78; `S0804_RL`#79; `S0805_RL`#80; `S0802_RL`#81; `S0803_RL`#82; `S0808_RL`#83; `S0809_RL`#84; `S0800_RL`#85; `S0801_RL`#86; `S0806_RL`#87; `S0807_RL`#88 | Unmapped | F/body+ |
| `Wheel_Caps` #89 @15 | `S0835_RL`#91; `S0836_RL`#92; `S0832_RL`#93; `S0833_RL`#94; `S0834_RL`#95; `S0831_RL`#96; `S0830_RL`#97; `S0906_RL`#98; `S0905_RL`#99 | Unmapped | F/body+ |
| `Brakes` #100 @16 | `S0286_RL`#102; `S0222_RL`#103; `S0206_RL`#104; `S0208_RL`#105; `S0210_RL`#106; `S0218_RL`#107; `S0225_RL`#108; `S0228_RL`#109; `S0285_RL`#110; `S0375_RL`#111; `S0376_RL`#112; `S0377_RL`#113; `S0378_RL`#114; `S0389_RL`#115; `J59_RL`#116; `J58_RL`#117 | J58, J59; rest unmapped | F/body+ |
| `Wheels` #118 @17 | `S0821_FL`#120; `S0822_FL`#121; `S0804_FL`#122; `S0805_FL`#123; `S0802_FL`#124; `S0803_FL`#125; `S0808_FL`#126; `S0809_FL`#127; `S0800_FL`#128; `S0801_FL`#129; `S0806_FL`#130; `S0807_FL`#131 | Unmapped | F/body+ |
| `Wheel_Caps` #132 @18 | `S0906_FL`#134; `S0905_FL`#135; `S0835_FL`#136; `S0836_FL`#137; `S0832_FL`#138; `S0833_FL`#139; `S0834_FL`#140; `S0831_FL`#141; `S0830_FL`#142 | Unmapped | F/body+ |
| `Brakes` #143 @19 | `S0286_FL`#145; `S0206_FL`#146; `S0208_FL`#147; `S0210_FL`#148; `S0218_FL`#149; `S0222_FL`#150; `S0225_FL`#151; `S0228_FL`#152; `S0285_FL`#153; `S0375_FL`#154; `S0376_FL`#155; `S0377_FL`#156; `S0378_FL`#157; `S0389_FL`#158; `J59_FL`#159; `J58_FL`#160 | J58, J59; rest unmapped | F/body+ |
| `Mirror_Cap` #164 @21 | `S0102_L&{P}` IDs [166, 167, 168, 169, 170, 171, 172, 173, 174, 175] | Unmapped | F/body+ |
| `Mirrors` #176 @22 | No native children | Unmapped | F/body+ |
| `Mirror_Cap` #178 @23 | `5JR_L`#180 | 5JR; rest unmapped | F/body+ |
| `Mirrors` #181 @24 | No native children | Unmapped | F/body+ |
| `Mirror_Cap` #183 @25 | `DRG_L`#185 | DRG; rest unmapped | F/body+ |
| `Mirrors` #186 @26 | `DYX_L`#188; `DWK_L`#189 | DWK, DYX; rest unmapped | F/body+ |
| `B_Pillars` #193 @28 | `S0236&{P}` IDs [195, 196, 197, 198, 199, 200, 201, 202, 203, 204]; `S0212&{P}` IDs [205, 206, 207, 208, 209, 210, 211, 212, 213, 214] | Unmapped | F/body+ |
| `Primer` #218 @30 | `S0115`#220 | Unmapped | F/body+ |
| `None` #230 @32 | `S0345`#232 | Unmapped | F/body+ |
| `Doors` #244 @35 | `S0536`#246 | Unmapped | F/body+ |
| `None` #247 @36 | `S0420`#249 | Unmapped | F/body+ |
| `Splashguards` #250 @37 | `S0390`#252 | Unmapped | F/body+ |
| `License_Plate` #256 @39 | No native children | Unmapped | F/body+ |
| `Multimedia` #270 @41 | No native children | Unmapped | F/body+ |
| `Roof` #275 @43 | `S0242`#277; `SBT`#278; `S0243&{P}` IDs [279, 280, 281, 282, 283, 284, 285, 286, 287, 288]; `C2Z&{P}` IDs [289, 290, 291, 292, 293, 294, 295, 296, 297, 298]; `CF8&{P}` IDs [299, 300, 301, 302, 303, 304, 305, 306, 307, 308]; `S0839&GEC`#309; `S0506`#310; `UG1&HTE`#311; `UG1&HTT`#312; `UG1&HVV`#313; `UG1&HU1`#314; `UG1&HMO`#315; `UG1&HU9`#316; `UG1&HZB`#317; `UG1&HVT`#318; `UG1&HUA`#319; `UG1&HU2`#320; `UG1&HUU`#321; `UG1&HZP`#322; `UG1&HUE`#323; `UG1&HTG`#324; `UG1&HZN`#325; `UG1&HUF`#326; `UG1&HU0`#327; `UG1&HXO`#328; `UG1&HNK`#329; `UG1&HUW`#330; `UG1&HUX`#331; `UG1&HVZ`#332; `UG1&H8T`#333; `UG1&HUB`#334; `UG1&HUC`#335; `UG1&EPX`#336; `UG1&EJH`#337; `UG1&HAG`#338 | C2Z, SBT, UG1; rest unmapped | F/body+ |
| `Badges` #779 @56 | `CFX`#781; `BV4`#782; `S0500`#783 | BV4, CFX; rest unmapped | F/body+ |
| `Radio` #956 @65 | No native children | Unmapped | F/body+ |
| `None` #1015 @70 | `S0357`#1017 | Unmapped | F/body+ |
| `None` #1032 @72 | `S0119`#1034 | Unmapped | S/body+ |
| `Engine` #1038 @74 | No native children | Unmapped | B/body+ |
| `Exhaust` #1040 @75 | `WUB`#1042 | WUB; rest unmapped | B/body+ |
| `Tow_Hooks` #1043 @76 | `S0871`#1045 | Unmapped | B/body+ |
| `Mirror_Cap` #1115 @83 | `S0102_R&{P}` IDs [1117, 1118, 1119, 1120, 1121, 1122, 1123, 1124, 1125, 1126]; `5JR_R`#1127 | 5JR; rest unmapped | B/body- |
| `Mirrors` #1128 @84 | No native children | Unmapped | B/body- |
| `Mirror_Cap` #1130 @85 | `DRG_R`#1132 | DRG; rest unmapped | B/body- |
| `Mirrors` #1133 @86 | `DYX_R`#1135; `DWK_R`#1136 | DWK, DYX; rest unmapped | B/body- |
| `Wheels` #1137 @87 | `S0800_RR`#1139 | Unmapped | B/body- |
| `Wheel_Caps` #1140 @88 | `S0836_RR`#1142 | Unmapped | B/body- |
| `Brakes` #1143 @89 | `S0222_RR`#1145; `S0208_RR`#1146; `S0218_RR`#1147; `S0225_RR`#1148; `S0285_RR`#1149; `S0375_RR`#1150; `S0376_RR`#1151; `S0389_RR`#1152 | Unmapped | B/body- |
| `Wheels` #1153 @90 | `S0801_FR`#1155; `S0806_FR`#1156 | Unmapped | B/body- |
| `Wheel_Caps` #1157 @91 | No native children | Unmapped | B/body- |
| `Brakes` #1159 @92 | `S0228_FR`#1161; `S0375_FR`#1162; `J59_FR`#1163; `J58_FR`#1164 | J58, J59; rest unmapped | B/body- |
| `Shadow` #1165 @93 | `S0902`#1167 | Unmapped | B/body- |
| `Background` #1168 @94 | `S0100`#1170 | Unmapped | B/body- |

Cabin/trim-dependent groups visible through glass (separate interior scenes are outside this audit): `Console` #242 @34 (0 children); `Stitching` #339 @44 (11 children); `Steering_Wheel` #352 @45 (36 children); `Interior_Kit` #390 @46 (1 children); `Interior` #393 @47 (56 children); `Interior_Kit` #451 @48 (25 children); `Interior` #478 @49 (28 children); `Interior_Kit` #508 @50 (55 children); `Stitching` #565 @51 (34 children); `Seat_Belts` #601 @52 (20 children); `Seats_Front` #623 @53 (119 children); `Floors` #744 @54 (29 children); `Cluster` #775 @55 (2 children); `IP` #784 @57 (1 children); `Decal_Stickers` #787 @58 (1 children); `Stitching` #790 @59 (3 children); `IP` #795 @60 (1 children); `Decal_Stickers` #798 @61 (32 children); `IP` #832 @62 (32 children); `Speakers` #866 @63 (84 children); `Effects` #958 @66 (32 children); `Console` #1171 @95 (7 children). Their seat/material/trim state must be recaptured for lower trims; no upper-trim interior is authorized as a substitute.

</details>

<details>
<summary>S18 — ZR1 coupe view 02</summary>

PSB: **V/zr1/exterior/27CHCOZR_COU_Studio_f04.psb**. Body-paint root index 82; spoiler root indices 1, 4, 6.

<a id="s18-paint"></a>

**Paint — U; all ten base paints**

| Parent path / ID / root index | Exact paint-bearing peers (each maps only its paint token) | Native placement |
| --- | --- | --- |
| `Spoiler` #27 @4 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | S/body+ |
| `Rear_Van_Windows` #133 @15 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Mirror_Cap` #271 @31 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Roof` #386 @43 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Roof` #401 @45 | 30 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Front_Fascia` #473 @49 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `B_Pillars` #1083 @73 | 20 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Rear_Fascia` #1116 @77 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Base` #1140 @82 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body= |
| `Mirror_Cap` #1159 @85 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body- |

<a id="s18-foundation"></a>

**Trim and body foundation**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Base` #1043 @70 | `S0507&1LZ`#1045; `S0507&3LZ`#1046 | Configuration/trim candidates | B/body+ |
| `Base` #1140 @82 | `GBA`#1142; `G8G`#1143; `GKZ`#1144; `GPH`#1145; `G26`#1146; `GBK`#1147; `G4Z`#1148; `GKA`#1149; `GTR`#1150; `GEC`#1151; `1YR07`#1152 | Configuration/trim candidates | B/body= |

<a id="s18-rear"></a>

**Rear spoiler / source-off-spoiler state**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Spoiler` #5 @1 | `SIG`#7 | SIG; rest unmapped | S/body+ |
| `Spoiler` #27 @4 | `S0268`#29; `S0267&{P}` IDs [30, 31, 32, 33, 34, 35, 36, 37, 38, 39] | Unmapped | S/body+ |
| `Spoiler` #43 @6 | `TOM`#45 | TOM; rest unmapped | S/body+ |

Source-off-spoiler state: hide every `Spoiler` parent listed here; this is a visibility recipe, **not a catalog option ID**. No legal no-spoiler configuration is established by this operation.

<a id="s18-aero"></a>

**Front/side/hood/fascia aero candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Hood` #60 @8 | `S0298`#62 | Unmapped | B/body+ |
| `Rear_Fascia` #170 @20 | `S0204`#172 | Unmapped | B/body+ |
| `Ground_Effects` #182 @24 | `S0366`#184 | Unmapped | B/body+ |
| `Front_Fascia` #377 @41 | `S0274`#379; `S0273`#380; `S0227`#381 | Unmapped | B/body+ |
| `Ground_Effects` #382 @42 | `S0396`#384; `S0368`#385 | Unmapped | B/body+ |
| `Front_Fascia` #473 @49 | `S0220&{P}` IDs [475, 476, 477, 478, 479, 480, 481, 482, 483, 484] | Unmapped | B/body+ |
| `Rear_Fascia` #1116 @77 | `S0203&{P}` IDs [1118, 1119, 1120, 1121, 1122, 1123, 1124, 1125, 1126, 1127] | Unmapped | B/body+ |
| `Hood` #1137 @81 | `S0297`#1139 | Unmapped | B/body+ |

<a id="s18-graphics"></a>

**Stripes / decals / color candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Decals` #8 @2 | `S0874`#10; `S0363`#11; `S0358`#12; `S0344`#13; `S0338`#14; `S0857`#15; `S0319`#16; `S0333`#17; `S0328`#18; `S0323`#19; `S0318`#20; `S0310`#21; `S0309`#22; `S0311`#23 | Unmapped | S/body+ |
| `Decals` #63 @9 | `S0837_F`#65; `S0855_F`#66; `S0302_F`#67; `S0330_F`#68; `S0325_F`#69; `S0320_F`#70; `S0315_F`#71; `S0307_F`#72 | Unmapped | B/body+ |
| `Stripes` #73 @10 | `S0369_F`#75 | Unmapped | B/body+ |
| `Decals` #76 @11 | `S0362_F`#78; `S0349_F`#79; `S0342_F`#80; `S0314_F`#81; `S0306_F`#82; `S0910`#83; `S0866`#84; `S0858`#85; `S0361`#86; `S0348`#87; `S0341`#88; `S0334`#89; `S0313`#90 | Unmapped | B/body+ |
| `Decals` #93 @13 | `S0332`#95; `S0327`#96; `S0322`#97; `S0317`#98; `S0304`#99; `S0303`#100; `S0308`#101; `S0886`#102; `S0838`#103; `S0853`#104; `S0852`#105; `S0851`#106; `S0849`#107; `S0848`#108; `S0847`#109; `S0846`#110; `S0845`#111; `S0844`#112; `S0843`#113; `S0842`#114; `S0850`#115; `S0360`#116; `S0347`#117; `S0340`#118; `S0329`#119; `S0312`#120; `S0331`#121; `S0326`#122; `S0321`#123; `S0316`#124; `S0301`#125; `S0300`#126; `S0864`#127; `S0859`#128; `S0305`#129 | Unmapped | B/body+ |
| `Decals` #146 @16 | `S0855_B`#148; `S0837_B`#149; `S0330_B`#150; `S0320_B`#151; `S0315_B`#152; `S0307_B`#153; `S0325_B`#154 | Unmapped | B/body+ |
| `Stripes` #155 @17 | `S0369_B`#157 | Unmapped | B/body+ |
| `Decals` #158 @18 | `S0362_B`#160; `S0349_B`#161; `S0342_B`#162; `S0314_B`#163; `S0306_B`#164; `S0302_B`#165 | Unmapped | B/body+ |
| `Decals` #176 @22 | `S0912`#178 | Unmapped | B/body+ |
| `Decals` #398 @44 | `S0911`#400 | Unmapped | B/body+ |

<a id="s18-glass"></a>

**Glass and window candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Rear_Van_Windows` #133 @15 | `ETV&{P}` IDs [135, 136, 137, 138, 139, 140, 141, 142, 143, 144]; `S0201`#145 | ETV; rest unmapped | B/body+ |
| `Windows` #294 @35 | `S0101_R`#296; `S0108`#297 | Unmapped | B/body+ |
| `Defroster` #464 @46 | `S0107`#466 | Unmapped | B/body+ |
| `Windows` #467 @47 | `S0104`#469 | Unmapped | B/body+ |
| `Windows` #485 @50 | `S0122`#487 | Unmapped | B/body+ |
| `Windows` #1134 @80 | `S0105`#1136 | Unmapped | B/body+ |
| `Windows` #1156 @84 | `S0101_L`#1158 | Unmapped | B/body- |

<a id="s18-other"></a>

**Other exterior option-driven and fixed groups**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Badges` #1 @0 | No native children | Unmapped | F/body+ |
| `None` #24 @3 | `S0357`#26 | Unmapped | S/body+ |
| `None` #40 @5 | `S0119`#42 | Unmapped | S/body+ |
| `Badges` #46 @7 | `SL8`#48; `RIN`#49; `RIK`#50; `EYK_F`#51; `EYT_F`#52; `EYK_B`#53; `EYT_B`#54; `SFZ_B`#55; `S0276`#56; `S0279`#57; `R88_F`#58; `R88_B`#59 | EYK, EYT, R88, RIK, RIN, SFZ, SL8; rest unmapped | B/body+ |
| `None` #91 @12 | No native children | Unmapped | B/body+ |
| `Tail_Lamps` #130 @14 | `S0200`#132 | Unmapped | B/body+ |
| `Multimedia` #166 @19 | `S0287`#168; `S0244`#169 | Unmapped | B/body+ |
| `License_Plate` #173 @21 | `S0235`#175 | Unmapped | B/body+ |
| `Molding` #179 @23 | `S0209`#181 | Unmapped | B/body+ |
| `Wheels` #185 @25 | `S0821_FR`#187; `S0822_FR`#188; `S0804_FR`#189; `S0805_FR`#190; `S0802_FR`#191; `S0803_FR`#192; `S0808_FR`#193; `S0809_FR`#194; `S0800_FR`#195; `S0801_FR`#196; `S0806_FR`#197; `S0807_FR`#198 | Unmapped | B/body+ |
| `Wheel_Caps` #199 @26 | `S0905_FR`#201; `S0906_FR`#202; `S0835_FR`#203; `S0836_FR`#204; `S0832_FR`#205; `S0833_FR`#206; `S0834_FR`#207; `S0831_FR`#208; `S0830_FR`#209 | Unmapped | B/body+ |
| `Brakes` #210 @27 | `S0286_FR`#212; `S0222_FR`#213; `S0206_FR`#214; `S0208_FR`#215; `S0210_FR`#216; `S0218_FR`#217; `S0225_FR`#218; `S0228_FR`#219; `S0285_FR`#220; `S0375_FR`#221; `S0376_FR`#222; `S0377_FR`#223; `S0378_FR`#224; `S0389_FR`#225; `J59_FR`#226; `J58_FR`#227 | J58, J59; rest unmapped | B/body+ |
| `Wheels` #228 @28 | `S0821_RR`#230; `S0822_RR`#231; `S0804_RR`#232; `S0805_RR`#233; `S0802_RR`#234; `S0803_RR`#235; `S0808_RR`#236; `S0809_RR`#237; `S0800_RR`#238; `S0801_RR`#239; `S0806_RR`#240; `S0807_RR`#241 | Unmapped | B/body+ |
| `Wheel_Caps` #242 @29 | `S0905_RR`#244; `S0906_RR`#245; `S0835_RR`#246; `S0836_RR`#247; `S0833_RR`#248; `S0832_RR`#249; `S0834_RR`#250; `S0831_RR`#251; `S0830_RR`#252 | Unmapped | B/body+ |
| `Brakes` #253 @30 | `S0286_RR`#255; `S0222_RR`#256; `S0206_RR`#257; `S0208_RR`#258; `S0210_RR`#259; `S0218_RR`#260; `S0225_RR`#261; `S0228_RR`#262; `S0285_RR`#263; `S0375_RR`#264; `S0376_RR`#265; `S0377_RR`#266; `S0378_RR`#267; `S0389_RR`#268; `J59_RR`#269; `J58_RR`#270 | J58, J59; rest unmapped | B/body+ |
| `Mirror_Cap` #271 @31 | `S0102_R&{P}` IDs [273, 274, 275, 276, 277, 278, 279, 280, 281, 282]; `5JR_R`#283 | 5JR; rest unmapped | B/body+ |
| `Mirrors` #284 @32 | No native children | Unmapped | B/body+ |
| `Mirror_Cap` #286 @33 | `DRG_R`#288 | DRG; rest unmapped | B/body+ |
| `Mirrors` #289 @34 | `VA5`#291; `DYX_R`#292; `DWK_R`#293 | DWK, DYX; rest unmapped | B/body+ |
| `Doors` #300 @37 | `S0536`#302 | Unmapped | B/body+ |
| `None` #374 @40 | `S0420`#376 | Unmapped | B/body+ |
| `Roof` #386 @43 | `S0839&{P}` IDs [388, 389, 390, 391, 392, 393, 394, 395, 396, 397] | Unmapped | B/body+ |
| `Roof` #401 @45 | `S0242`#403; `SBT`#404; `S0243&{P}` IDs [405, 406, 407, 408, 409, 410, 411, 412, 413, 414]; `C2Z&{P}` IDs [415, 416, 417, 418, 419, 420, 421, 422, 423, 424]; `CF8&{P}` IDs [425, 426, 427, 428, 429, 430, 431, 432, 433, 434]; `S0506`#435; `UG1&HTE`#436; `UG1&HTT`#437; `UG1&HVV`#438; `UG1&HU1`#439; `UG1&HMO`#440; `UG1&HU9`#441; `UG1&HZB`#442; `UG1&HVT`#443; `UG1&HUA`#444; `UG1&HU2`#445; `UG1&HUU`#446; `UG1&HZP`#447; `UG1&HUE`#448; `UG1&HTG`#449; `UG1&HZN`#450; `UG1&HUF`#451; `UG1&HU0`#452; `UG1&HXO`#453; `UG1&HNK`#454; `UG1&HUW`#455; `UG1&HUX`#456; `UG1&HVZ`#457; `UG1&H8T`#458; `UG1&HUB`#459; `UG1&HUC`#460; `UG1&EPX`#461; `UG1&EJH`#462; `UG1&HAG`#463 | C2Z, SBT, UG1; rest unmapped | B/body+ |
| `Headlamps` #470 @48 | `T4L`#472 | T4L; rest unmapped | B/body+ |
| `Badges` #909 @65 | `CFX`#911; `BV4`#912 | BV4, CFX; rest unmapped | B/body+ |
| `Radio` #1047 @71 | No native children | Unmapped | B/body+ |
| `B_Pillars` #1083 @73 | `S0236&{P}` IDs [1085, 1086, 1087, 1088, 1089, 1090, 1091, 1092, 1093, 1094]; `S0212&{P}` IDs [1095, 1096, 1097, 1098, 1099, 1100, 1101, 1102, 1103, 1104] | Unmapped | B/body+ |
| `Engine` #1105 @74 | `LT7`#1107 | LT7; rest unmapped | B/body+ |
| `Tow_Hooks` #1108 @75 | `S0871`#1110 | Unmapped | B/body+ |
| `Exhaust` #1111 @76 | `S0867`#1113; `S0868`#1114; `WUB`#1115 | WUB; rest unmapped | B/body+ |
| `Splashguards` #1128 @78 | `S0390`#1130 | Unmapped | B/body+ |
| `Primer` #1131 @79 | `S0115`#1133 | Unmapped | B/body+ |
| `Grille` #1153 @83 | `VWE`#1155 | VWE; rest unmapped | B/body- |
| `Mirror_Cap` #1159 @85 | `S0102_L&{P}` IDs [1161, 1162, 1163, 1164, 1165, 1166, 1167, 1168, 1169, 1170]; `5JR_L`#1171 | 5JR; rest unmapped | B/body- |
| `Mirrors` #1172 @86 | No native children | Unmapped | B/body- |
| `Mirror_Cap` #1174 @87 | `DRG_L`#1176 | DRG; rest unmapped | B/body- |
| `Mirrors` #1177 @88 | `DYX_L`#1179; `DWK_L`#1180 | DWK, DYX; rest unmapped | B/body- |
| `Wheels` #1181 @89 | `S0804_RL`#1183; `S0805_RL`#1184; `S0802_RL`#1185; `S0803_RL`#1186; `S0808_RL`#1187; `S0809_RL`#1188; `S0800_RL`#1189; `S0801_RL`#1190; `S0806_RL`#1191; `S0807_RL`#1192 | Unmapped | B/body- |
| `Wheel_Caps` #1193 @90 | `S0835_RL`#1195; `S0836_RL`#1196; `S0831_RL`#1197 | Unmapped | B/body- |
| `Brakes` #1198 @91 | `S0286_RL`#1200; `S0222_RL`#1201; `S0206_RL`#1202; `S0208_RL`#1203; `S0210_RL`#1204; `S0218_RL`#1205; `S0225_RL`#1206; `S0228_RL`#1207; `S0285_RL`#1208; `S0375_RL`#1209; `S0376_RL`#1210; `S0378_RL`#1211; `S0389_RL`#1212; `J59_RL`#1213; `J58_RL`#1214 | J58, J59; rest unmapped | B/body- |
| `Wheels` #1215 @92 | `S0805_FL`#1217; `S0802_FL`#1218; `S0803_FL`#1219; `S0806_FL`#1220 | Unmapped | B/body- |
| `Wheel_Caps` #1221 @93 | `S0832_FL`#1223; `S0831_FL`#1224; `S0830_FL`#1225 | Unmapped | B/body- |
| `Brakes` #1226 @94 | `S0286_FL`#1228; `S0376_FL`#1229; `S0377_FL`#1230; `S0222_FL`#1231; `S0206_FL`#1232; `S0208_FL`#1233; `S0218_FL`#1234; `S0225_FL`#1235; `J58_FL`#1236 | J58; rest unmapped | B/body- |
| `Shadow` #1237 @95 | `S0902`#1239 | Unmapped | B/body- |
| `Background` #1240 @96 | `S0100`#1242 | Unmapped | B/body- |
| `Tow_Hooks` #1243 @97 | `S0869`#1245 | Unmapped | B/body- |

Cabin/trim-dependent groups visible through glass (separate interior scenes are outside this audit): `Console` #298 @36 (0 children); `Stitching` #303 @38 (3 children); `Steering_Wheel` #308 @39 (64 children); `Seat_Belts` #488 @51 (18 children); `Interior` #508 @52 (55 children); `Interior_Kit` #565 @53 (27 children); `Interior` #594 @54 (23 children); `Interior_Kit` #619 @55 (52 children); `IP` #673 @56 (1 children); `Decal_Stickers` #676 @57 (1 children); `Cluster` #679 @58 (2 children); `Stitching` #683 @59 (41 children); `Floors` #726 @60 (30 children); `Interior_Kit` #758 @61 (1 children); `IP` #761 @62 (32 children); `Seats_Front` #795 @63 (109 children); `Interior` #906 @64 (1 children); `Speakers` #913 @66 (82 children); `IP` #997 @67 (1 children); `Decal_Stickers` #1000 @68 (32 children); `Console` #1034 @69 (7 children); `Effects` #1049 @72 (32 children). Their seat/material/trim state must be recaptured for lower trims; no upper-trim interior is authorized as a substitute.

</details>

<details>
<summary>S19 — ZR1X convertible view 01</summary>

PSB: **V/zr1x/exterior/27CHCOZR_X_CON_Studio_f02.psb**. Body-paint root index 87; spoiler root indices 77, 79.

<a id="s19-paint"></a>

**Paint — U; all ten base paints**

| Parent path / ID / root index | Exact paint-bearing peers (each maps only its paint token) | Native placement |
| --- | --- | --- |
| `Enclosure_Rear` #17 @6 | 9 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Front_Fascia` #85 @18 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Mirror_Cap` #170 @26 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `B_Pillars` #199 @33 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Rear_Fascia` #253 @44 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Tailgate` #271 @47 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Roof` #285 @48 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Spoiler` #1014 @77 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | S/body+ |
| `Tailgate` #1065 @86 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Base` #1079 @87 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body= |
| `Mirror_Cap` #1096 @89 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body- |

<a id="s19-foundation"></a>

**Trim and body foundation**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Base` #945 @69 | `S0507&1LZ`#947; `S0507&3LZ`#948 | Configuration/trim candidates | F/body+ |
| `Base` #1079 @87 | `GBA`#1081; `G8G`#1082; `GKZ`#1083; `GPH`#1084; `G26`#1085; `GBK`#1086; `G4Z`#1087; `GKA`#1088; `GTR`#1089; `GEC`#1090; `1YS67`#1091 | Configuration/trim candidates | B/body= |

<a id="s19-rear"></a>

**Rear spoiler / source-off-spoiler state**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Spoiler` #1014 @77 | `S0268`#1016; `S0267&{P}` IDs [1017, 1018, 1019, 1020, 1021, 1022, 1023, 1024, 1025, 1026]; `SIG`#1027 | Unmapped | S/body+ |
| `Spoiler` #1031 @79 | `TOM`#1033 | TOM; rest unmapped | S/body+ |

Source-off-spoiler state: hide every `Spoiler` parent listed here; this is a visibility recipe, **not a catalog option ID**. No legal no-spoiler configuration is established by this operation.

<a id="s19-aero"></a>

**Front/side/hood/fascia aero candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Hood` #37 @8 | `S0298`#39 | Unmapped | F/body+ |
| `Front_Fascia` #71 @15 | `S0274`#73; `S0273`#74; `S0227`#75; `S0224`#76; `S0221`#77 | Unmapped | F/body+ |
| `Ground_Effects` #78 @16 | `S0396`#80; `S0368`#81 | Unmapped | F/body+ |
| `Front_Fascia` #85 @18 | `S0220&{P}` IDs [87, 88, 89, 90, 91, 92, 93, 94, 95, 96] | Unmapped | F/body+ |
| `Ground_Effects` #167 @25 | `S0366`#169 | Unmapped | F/body+ |
| `Rear_Fascia` #253 @44 | `S0204`#255; `S0203&{P}` IDs [256, 257, 258, 259, 260, 261, 262, 263, 264, 265] | Unmapped | F/body+ |
| `Hood` #268 @46 | `S0297`#270 | Unmapped | F/body+ |

<a id="s19-graphics"></a>

**Stripes / decals / color candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Decals` #4 @1 | `S0493`#6 | Unmapped | F/body+ |
| `Stripes` #7 @2 | No native children | Unmapped | F/body+ |
| `Decals` #9 @3 | `S0484`#11; `S0911`#12 | Unmapped | F/body+ |
| `Decals` #40 @9 | `S0837_F`#42; `S0855_F`#43; `S0302_F`#44; `S0330_F`#45; `S0325_F`#46; `S0320_F`#47; `S0315_F`#48; `S0307_F`#49; `S0372_F`#50 | Unmapped | F/body+ |
| `Stripes` #51 @10 | `S0369_F`#53 | Unmapped | F/body+ |
| `Decals` #54 @11 | `S0362_F`#56; `S0349_F`#57; `S0342_F`#58; `S0314_F`#59; `S0306_F`#60; `S0910`#61 | Unmapped | F/body+ |
| `Decals` #218 @36 | `S0866`#220; `S0858`#221; `S0361`#222; `S0348`#223; `S0341`#224; `S0334`#225; `S0313`#226; `S0371`#227 | Unmapped | F/body+ |
| `Decals` #231 @38 | `S0332`#233; `S0327`#234; `S0322`#235; `S0317`#236; `S0304`#237; `S0303`#238; `S0308`#239 | Unmapped | F/body+ |
| `Decals` #994 @75 | `S0874`#996; `S0363`#997; `S0358`#998; `S0344`#999; `S0338`#1000; `S0857`#1001; `S0373`#1002; `S0319`#1003; `S0333`#1004; `S0328`#1005; `S0323`#1006; `S0318`#1007; `S0310`#1008; `S0309`#1009; `S0311`#1010 | Unmapped | F/body+ |
| `Decals` #1044 @83 | `S0855_B`#1046; `S0837_B`#1047; `S0330_B`#1048; `S0320_B`#1049; `S0315_B`#1050; `S0307_B`#1051; `S0325_B`#1052; `S0372_B`#1053 | Unmapped | B/body+ |
| `Stripes` #1054 @84 | `S0369_B`#1056 | Unmapped | B/body+ |
| `Decals` #1057 @85 | `S0362_B`#1059; `S0349_B`#1060; `S0342_B`#1061; `S0314_B`#1062; `S0306_B`#1063; `S0302_B`#1064 | Unmapped | B/body+ |

<a id="s19-glass"></a>

**Glass and window candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Windows` #196 @32 | `S0105`#198 | Unmapped | F/body+ |
| `Windows` #212 @34 | `S0101_L`#214 | Unmapped | F/body+ |
| `Windows` #985 @72 | `S0104`#987 | Unmapped | F/body+ |
| `Defroster` #988 @73 | `S0107`#990 | Unmapped | F/body+ |
| `Windows` #1092 @88 | `S0101_B`#1094; `S0101_R`#1095 | Unmapped | B/body- |

<a id="s19-other"></a>

**Other exterior option-driven and fixed groups**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Tow_Hooks` #1 @0 | No native children | Unmapped | F/body+ |
| `Tailgate` #13 @4 | No native children | Unmapped | F/body+ |
| `Engine` #15 @5 | No native children | Unmapped | F/body+ |
| `Enclosure_Rear` #17 @6 | `S0127&GBA`#19; `S0127&G8G`#20; `S0127&GKZ`#21; `S0127&GPH`#22; `S0127&G26`#23; `S0127&GBK`#24; `S0127&G4Z`#25; `S0127&GKA`#26; `S0127&GEC`#27 | Unmapped | F/body+ |
| `Badges` #28 @7 | `EYK_F`#30; `EYT_F`#31; `SFZ_F`#32; `SFZ_B`#33; `R88_F`#34; `S0499`#35; `S0498`#36 | EYK, EYT, R88, SFZ; rest unmapped | F/body+ |
| `Tail_Lamps` #62 @12 | `S0200`#64 | Unmapped | F/body+ |
| `Headlamps` #65 @13 | `T4L`#67 | T4L; rest unmapped | F/body+ |
| `Molding` #68 @14 | `S0209`#70 | Unmapped | F/body+ |
| `Grille` #82 @17 | `VWE`#84 | VWE; rest unmapped | F/body+ |
| `Wheels` #97 @19 | `S0821_RL`#99; `S0822_RL`#100; `S0804_RL`#101; `S0805_RL`#102; `S0802_RL`#103; `S0803_RL`#104; `S0808_RL`#105; `S0809_RL`#106; `S0800_RL`#107; `S0801_RL`#108; `S0806_RL`#109; `S0807_RL`#110 | Unmapped | F/body+ |
| `Wheel_Caps` #111 @20 | `S0835_RL`#113; `S0836_RL`#114; `S0832_RL`#115; `S0833_RL`#116; `S0834_RL`#117; `S0831_RL`#118; `S0830_RL`#119; `S0906_RL`#120; `S0905_RL`#121 | Unmapped | F/body+ |
| `Brakes` #122 @21 | `S0222_RL`#124; `S0206_RL`#125; `S0208_RL`#126; `S0210_RL`#127; `S0218_RL`#128; `S0225_RL`#129; `S0228_RL`#130; `J59_RL`#131 | J59; rest unmapped | F/body+ |
| `Wheels` #132 @22 | `S0821_FL`#134; `S0822_FL`#135; `S0804_FL`#136; `S0805_FL`#137; `S0802_FL`#138; `S0803_FL`#139; `S0808_FL`#140; `S0809_FL`#141; `S0800_FL`#142; `S0801_FL`#143; `S0806_FL`#144; `S0807_FL`#145 | Unmapped | F/body+ |
| `Wheel_Caps` #146 @23 | `S0906_FL`#148; `S0905_FL`#149; `S0835_FL`#150; `S0836_FL`#151; `S0832_FL`#152; `S0833_FL`#153; `S0834_FL`#154; `S0831_FL`#155; `S0830_FL`#156 | Unmapped | F/body+ |
| `Brakes` #157 @24 | `S0206_FL`#159; `S0208_FL`#160; `S0210_FL`#161; `S0218_FL`#162; `S0222_FL`#163; `S0225_FL`#164; `S0228_FL`#165; `J59_FL`#166 | J59; rest unmapped | F/body+ |
| `Mirror_Cap` #170 @26 | `S0102_L&{P}` IDs [172, 173, 174, 175, 176, 177, 178, 179, 180, 181] | Unmapped | F/body+ |
| `Mirrors` #182 @27 | No native children | Unmapped | F/body+ |
| `Mirror_Cap` #184 @28 | `5JR_L`#186 | 5JR; rest unmapped | F/body+ |
| `Mirrors` #187 @29 | No native children | Unmapped | F/body+ |
| `Mirror_Cap` #189 @30 | `DRG_L`#191 | DRG; rest unmapped | F/body+ |
| `Mirrors` #192 @31 | `DYX_L`#194; `DWK_L`#195 | DWK, DYX; rest unmapped | F/body+ |
| `B_Pillars` #199 @33 | `S0236&{P}` IDs [201, 202, 203, 204, 205, 206, 207, 208, 209, 210]; `S0213`#211 | Unmapped | F/body+ |
| `Primer` #215 @35 | `S0115`#217 | Unmapped | F/body+ |
| `None` #228 @37 | `S0345`#230 | Unmapped | F/body+ |
| `Doors` #242 @40 | `S0536`#244 | Unmapped | F/body+ |
| `None` #245 @41 | `S0420`#247 | Unmapped | F/body+ |
| `Splashguards` #248 @42 | `S0390`#250 | Unmapped | F/body+ |
| `License_Plate` #251 @43 | No native children | Unmapped | F/body+ |
| `Multimedia` #266 @45 | No native children | Unmapped | F/body+ |
| `Tailgate` #271 @47 | `S0135_L&{P}` IDs [273, 274, 275, 276, 277, 278, 279, 280, 281, 282]; `S0136_L`#283; `S0113_L`#284 | Unmapped | F/body+ |
| `Roof` #285 @48 | `CFC&{P}` IDs [287, 288, 289, 290, 291, 292, 293, 294, 295, 296]; `S0841`#297; `S0840`#298; `S0506`#299; `UG1&HTE`#300; `UG1&HTT`#301; `UG1&HVV`#302; `UG1&HU1`#303; `UG1&HMO`#304; `UG1&HU9`#305; `UG1&HZB`#306; `UG1&HVT`#307; `UG1&HUA`#308; `UG1&HU2`#309; `UG1&HUU`#310; `UG1&HZP`#311; `UG1&HUE`#312; `UG1&HTG`#313; `UG1&HZN`#314; `UG1&HUF`#315; `UG1&HU0`#316; `UG1&HXO`#317; `UG1&HNK`#318; `UG1&HUW`#319; `UG1&HUX`#320; `UG1&HVZ`#321; `UG1&H8T`#322; `UG1&HUB`#323; `UG1&HUC`#324; `UG1&EPX`#325; `UG1&EJH`#326; `UG1&HAG`#327 | CFC, UG1; rest unmapped | F/body+ |
| `Badges` #772 @61 | `CFX`#774; `BV4`#775; `S0500`#776 | BV4, CFX; rest unmapped | F/body+ |
| `Radio` #949 @70 | No native children | Unmapped | F/body+ |
| `Tailgate` #991 @74 | `S0217`#993 | Unmapped | F/body+ |
| `None` #1011 @76 | `S0357`#1013 | Unmapped | F/body+ |
| `None` #1028 @78 | `S0119`#1030 | Unmapped | S/body+ |
| `Engine` #1034 @80 | `LT7`#1036 | LT7; rest unmapped | B/body+ |
| `Exhaust` #1037 @81 | `WUB`#1039; `S0867`#1040 | WUB; rest unmapped | B/body+ |
| `Tow_Hooks` #1041 @82 | `S0871`#1043 | Unmapped | B/body+ |
| `Tailgate` #1065 @86 | `S0135_R&{P}` IDs [1067, 1068, 1069, 1070, 1071, 1072, 1073, 1074, 1075, 1076]; `S0136_R`#1077; `S0113_R`#1078 | Unmapped | B/body+ |
| `Mirror_Cap` #1096 @89 | `S0102_R&{P}` IDs [1098, 1099, 1100, 1101, 1102, 1103, 1104, 1105, 1106, 1107]; `5JR_R`#1108 | 5JR; rest unmapped | B/body- |
| `Mirrors` #1109 @90 | No native children | Unmapped | B/body- |
| `Mirror_Cap` #1111 @91 | `DRG_R`#1113 | DRG; rest unmapped | B/body- |
| `Mirrors` #1114 @92 | `DYX_R`#1116; `DWK_R`#1117 | DWK, DYX; rest unmapped | B/body- |
| `Wheels` #1118 @93 | `S0804_RR`#1120; `S0805_RR`#1121; `S0802_RR`#1122; `S0803_RR`#1123; `S0809_RR`#1124; `S0800_RR`#1125; `S0801_RR`#1126; `S0806_RR`#1127; `S0807_RR`#1128 | Unmapped | B/body- |
| `Wheel_Caps` #1129 @94 | `S0834_RR`#1131 | Unmapped | B/body- |
| `Brakes` #1132 @95 | `S0208_RR`#1134 | Unmapped | B/body- |
| `Wheels` #1135 @96 | `S0809_FR`#1137 | Unmapped | B/body- |
| `Wheel_Caps` #1138 @97 | No native children | Unmapped | B/body- |
| `Brakes` #1140 @98 | `S0228_FR`#1142; `J59_FR`#1143 | J59; rest unmapped | B/body- |
| `Shadow` #1144 @99 | `S0902`#1146 | Unmapped | B/body- |
| `Background` #1147 @100 | `S0100`#1149 | Unmapped | B/body- |

Cabin/trim-dependent groups visible through glass (separate interior scenes are outside this audit): `Console` #240 @39 (0 children); `Stitching` #328 @49 (12 children); `Steering_Wheel` #342 @50 (41 children); `Interior_Kit` #385 @51 (1 children); `Interior` #388 @52 (55 children); `Interior_Kit` #445 @53 (25 children); `Interior` #472 @54 (28 children); `Interior_Kit` #502 @55 (55 children); `Stitching` #559 @56 (34 children); `Seat_Belts` #595 @57 (20 children); `Seats_Front` #617 @58 (119 children); `Floors` #738 @59 (28 children); `Cluster` #768 @60 (2 children); `IP` #777 @62 (1 children); `Decal_Stickers` #780 @63 (1 children); `Stitching` #783 @64 (3 children); `IP` #788 @65 (1 children); `Decal_Stickers` #791 @66 (32 children); `IP` #825 @67 (32 children); `Speakers` #859 @68 (84 children); `Effects` #951 @71 (32 children); `Console` #1150 @101 (6 children). Their seat/material/trim state must be recaptured for lower trims; no upper-trim interior is authorized as a substitute.

</details>

<details>
<summary>S20 — ZR1X convertible view 02</summary>

PSB: **V/zr1x/exterior/27CHCOZR_X_CON_Studio_f04.psb**. Body-paint root index 88; spoiler root indices 7, 10, 12.

<a id="s20-paint"></a>

**Paint — U; all ten base paints**

| Parent path / ID / root index | Exact paint-bearing peers (each maps only its paint token) | Native placement |
| --- | --- | --- |
| `Enclosure_Rear` #12 @5 | 5 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Spoiler` #46 @10 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | S/body+ |
| `Tailgate` #124 @21 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Tailgate` #249 @37 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Mirror_Cap` #263 @38 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Roof` #384 @52 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Front_Fascia` #434 @56 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `B_Pillars` #1057 @79 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Rear_Fascia` #1081 @83 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Base` #1105 @88 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body= |
| `Mirror_Cap` #1124 @91 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body- |

<a id="s20-foundation"></a>

**Trim and body foundation**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Base` #1017 @76 | `S0507&1LZ`#1019; `S0507&3LZ`#1020 | Configuration/trim candidates | B/body+ |
| `Base` #1105 @88 | `GBA`#1107; `G8G`#1108; `GKZ`#1109; `GPH`#1110; `G26`#1111; `GBK`#1112; `G4Z`#1113; `GKA`#1114; `GTR`#1115; `GEC`#1116; `1YS67`#1117 | Configuration/trim candidates | B/body= |

<a id="s20-rear"></a>

**Rear spoiler / source-off-spoiler state**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Spoiler` #23 @7 | `SIG`#25 | Unmapped | S/body+ |
| `Spoiler` #46 @10 | `S0268`#48; `S0267&{P}` IDs [49, 50, 51, 52, 53, 54, 55, 56, 57, 58] | Unmapped | S/body+ |
| `Spoiler` #62 @12 | `TOM`#64 | TOM; rest unmapped | S/body+ |

Source-off-spoiler state: hide every `Spoiler` parent listed here; this is a visibility recipe, **not a catalog option ID**. No legal no-spoiler configuration is established by this operation.

<a id="s20-aero"></a>

**Front/side/hood/fascia aero candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Hood` #77 @14 | `S0298`#79 | Unmapped | B/body+ |
| `Rear_Fascia` #164 @26 | `S0204`#166 | Unmapped | B/body+ |
| `Ground_Effects` #176 @30 | `S0366`#178 | Unmapped | B/body+ |
| `Front_Fascia` #369 @48 | `S0274`#371; `S0273`#372 | Unmapped | B/body+ |
| `Ground_Effects` #373 @49 | `S0396`#375; `S0368`#376 | Unmapped | B/body+ |
| `Front_Fascia` #434 @56 | `S0220&{P}` IDs [436, 437, 438, 439, 440, 441, 442, 443, 444, 445] | Unmapped | B/body+ |
| `Rear_Fascia` #1081 @83 | `S0203&{P}` IDs [1083, 1084, 1085, 1086, 1087, 1088, 1089, 1090, 1091, 1092] | Unmapped | B/body+ |
| `Hood` #1102 @87 | `S0297`#1104 | Unmapped | B/body+ |

<a id="s20-graphics"></a>

**Stripes / decals / color candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Decals` #1 @0 | No native children | Unmapped | F/body+ |
| `Stripes` #3 @1 | No native children | Unmapped | F/body+ |
| `Decals` #5 @2 | `S0486`#7 | Unmapped | F/body+ |
| `Decals` #26 @8 | `S0874`#28; `S0363`#29; `S0358`#30; `S0344`#31; `S0338`#32; `S0857`#33; `S0373`#34; `S0319`#35; `S0333`#36; `S0328`#37; `S0323`#38; `S0318`#39; `S0310`#40; `S0309`#41; `S0311`#42 | Unmapped | S/body+ |
| `Decals` #80 @15 | `S0837_F`#82; `S0855_F`#83; `S0302_F`#84; `S0330_F`#85; `S0325_F`#86; `S0320_F`#87; `S0315_F`#88; `S0307_F`#89; `S0372_F`#90 | Unmapped | B/body+ |
| `Stripes` #91 @16 | `S0369_F`#93 | Unmapped | B/body+ |
| `Decals` #94 @17 | `S0362_F`#96; `S0349_F`#97; `S0342_F`#98; `S0314_F`#99; `S0306_F`#100; `S0910`#101; `S0866`#102; `S0858`#103; `S0361`#104; `S0348`#105; `S0341`#106; `S0334`#107; `S0313`#108; `S0371`#109 | Unmapped | B/body+ |
| `Decals` #112 @19 | `S0332`#114; `S0327`#115; `S0322`#116; `S0317`#117; `S0304`#118; `S0303`#119; `S0308`#120 | Unmapped | B/body+ |
| `Decals` #139 @22 | `S0855_B`#141; `S0837_B`#142; `S0330_B`#143; `S0320_B`#144; `S0315_B`#145; `S0307_B`#146; `S0325_B`#147; `S0372_B`#148 | Unmapped | B/body+ |
| `Stripes` #149 @23 | `S0369_B`#151 | Unmapped | B/body+ |
| `Decals` #152 @24 | `S0362_B`#154; `S0349_B`#155; `S0342_B`#156; `S0314_B`#157; `S0306_B`#158; `S0302_B`#159 | Unmapped | B/body+ |
| `Decals` #170 @28 | `S0912`#172 | Unmapped | B/body+ |
| `Decals` #381 @51 | `S0911`#383 | Unmapped | B/body+ |

<a id="s20-glass"></a>

**Glass and window candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Windows` #286 @42 | `S0101_R`#288; `S0101_B`#289 | Unmapped | B/body+ |
| `Defroster` #425 @53 | `S0107`#427 | Unmapped | B/body+ |
| `Windows` #428 @54 | `S0104`#430 | Unmapped | B/body+ |
| `Windows` #1099 @86 | `S0105`#1101 | Unmapped | B/body+ |
| `Windows` #1121 @90 | `S0101_L`#1123 | Unmapped | B/body- |

<a id="s20-other"></a>

**Other exterior option-driven and fixed groups**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Tailgate` #8 @3 | No native children | Unmapped | F/body+ |
| `Engine` #10 @4 | No native children | Unmapped | F/body+ |
| `Enclosure_Rear` #12 @5 | `S0127&GKZ`#14; `S0127&GPH`#15; `S0127&G26`#16; `S0127&G4Z`#17; `S0127&GEC`#18 | Unmapped | F/body+ |
| `Badges` #19 @6 | `S0499`#21; `S0498`#22 | Unmapped | F/body+ |
| `None` #43 @9 | `S0357`#45 | Unmapped | S/body+ |
| `None` #59 @11 | `S0119`#61 | Unmapped | S/body+ |
| `Badges` #65 @13 | `SL8`#67; `RIN`#68; `RIK`#69; `EYK_B`#70; `EYT_B`#71; `SFZ_B`#72; `S0276`#73; `S0279`#74; `R88_F`#75; `R88_B`#76 | EYK, EYT, R88, RIK, RIN, SFZ, SL8; rest unmapped | B/body+ |
| `None` #110 @18 | No native children | Unmapped | B/body+ |
| `Tail_Lamps` #121 @20 | `S0200`#123 | Unmapped | B/body+ |
| `Tailgate` #124 @21 | `S0135_R&{P}` IDs [126, 127, 128, 129, 130, 131, 132, 133, 134, 135]; `S0136_R`#136; `S0113_R`#137; `S0217`#138 | Unmapped | B/body+ |
| `Multimedia` #160 @25 | `S0287`#162; `S0244`#163 | Unmapped | B/body+ |
| `License_Plate` #167 @27 | `S0235`#169 | Unmapped | B/body+ |
| `Molding` #173 @29 | `S0209`#175 | Unmapped | B/body+ |
| `Wheels` #179 @31 | `S0821_FR`#181; `S0822_FR`#182; `S0804_FR`#183; `S0805_FR`#184; `S0802_FR`#185; `S0803_FR`#186; `S0808_FR`#187; `S0809_FR`#188; `S0800_FR`#189; `S0801_FR`#190; `S0806_FR`#191; `S0807_FR`#192 | Unmapped | B/body+ |
| `Wheel_Caps` #193 @32 | `S0905_FR`#195; `S0906_FR`#196; `S0835_FR`#197; `S0836_FR`#198; `S0832_FR`#199; `S0833_FR`#200; `S0834_FR`#201; `S0831_FR`#202; `S0830_FR`#203 | Unmapped | B/body+ |
| `Brakes` #204 @33 | `S0222_FR`#206; `S0206_FR`#207; `S0208_FR`#208; `S0210_FR`#209; `S0218_FR`#210; `S0225_FR`#211; `S0228_FR`#212; `J59_FR`#213 | J59; rest unmapped | B/body+ |
| `Wheels` #214 @34 | `S0821_RR`#216; `S0822_RR`#217; `S0804_RR`#218; `S0805_RR`#219; `S0802_RR`#220; `S0803_RR`#221; `S0808_RR`#222; `S0809_RR`#223; `S0800_RR`#224; `S0801_RR`#225; `S0806_RR`#226; `S0807_RR`#227 | Unmapped | B/body+ |
| `Wheel_Caps` #228 @35 | `S0905_RR`#230; `S0906_RR`#231; `S0835_RR`#232; `S0836_RR`#233; `S0833_RR`#234; `S0832_RR`#235; `S0834_RR`#236; `S0831_RR`#237; `S0830_RR`#238 | Unmapped | B/body+ |
| `Brakes` #239 @36 | `S0222_RR`#241; `S0206_RR`#242; `S0208_RR`#243; `S0210_RR`#244; `S0218_RR`#245; `S0225_RR`#246; `S0228_RR`#247; `J59_RR`#248 | J59; rest unmapped | B/body+ |
| `Tailgate` #249 @37 | `S0135_L&{P}` IDs [251, 252, 253, 254, 255, 256, 257, 258, 259, 260]; `S0136_L`#261; `S0113_L`#262 | Unmapped | B/body+ |
| `Mirror_Cap` #263 @38 | `S0102_R&{P}` IDs [265, 266, 267, 268, 269, 270, 271, 272, 273, 274]; `5JR_R`#275 | 5JR; rest unmapped | B/body+ |
| `Mirrors` #276 @39 | No native children | Unmapped | B/body+ |
| `Mirror_Cap` #278 @40 | `DRG_R`#280 | DRG; rest unmapped | B/body+ |
| `Mirrors` #281 @41 | `VA5`#283; `DYX_R`#284; `DWK_R`#285 | DWK, DYX; rest unmapped | B/body+ |
| `Doors` #292 @44 | `S0536`#294 | Unmapped | B/body+ |
| `None` #366 @47 | `S0420`#368 | Unmapped | B/body+ |
| `Roof` #377 @50 | `S0841`#379; `S0840`#380 | Unmapped | B/body+ |
| `Roof` #384 @52 | `CFC&{P}` IDs [386, 387, 388, 389, 390, 391, 392, 393, 394, 395]; `S0506`#396; `UG1&HTE`#397; `UG1&HTT`#398; `UG1&HVV`#399; `UG1&HU1`#400; `UG1&HMO`#401; `UG1&HU9`#402; `UG1&HZB`#403; `UG1&HVT`#404; `UG1&HUA`#405; `UG1&HU2`#406; `UG1&HUU`#407; `UG1&HZP`#408; `UG1&HUE`#409; `UG1&HTG`#410; `UG1&HZN`#411; `UG1&HUF`#412; `UG1&HU0`#413; `UG1&HXO`#414; `UG1&HNK`#415; `UG1&HUW`#416; `UG1&HUX`#417; `UG1&HVZ`#418; `UG1&H8T`#419; `UG1&HUB`#420; `UG1&HUC`#421; `UG1&EPX`#422; `UG1&EJH`#423; `UG1&HAG`#424 | CFC, UG1; rest unmapped | B/body+ |
| `Headlamps` #431 @55 | `T4L`#433 | T4L; rest unmapped | B/body+ |
| `Badges` #884 @71 | `CFX`#886; `BV4`#887; `S0500`#888 | BV4, CFX; rest unmapped | B/body+ |
| `Radio` #1021 @77 | No native children | Unmapped | B/body+ |
| `B_Pillars` #1057 @79 | `S0236&{P}` IDs [1059, 1060, 1061, 1062, 1063, 1064, 1065, 1066, 1067, 1068]; `S0213`#1069 | Unmapped | B/body+ |
| `Engine` #1070 @80 | `LT7`#1072 | LT7; rest unmapped | B/body+ |
| `Tow_Hooks` #1073 @81 | `S0871`#1075 | Unmapped | B/body+ |
| `Exhaust` #1076 @82 | `S0867`#1078; `S0868`#1079; `WUB`#1080 | WUB; rest unmapped | B/body+ |
| `Splashguards` #1093 @84 | `S0390`#1095 | Unmapped | B/body+ |
| `Primer` #1096 @85 | `S0115`#1098 | Unmapped | B/body+ |
| `Grille` #1118 @89 | `VWE`#1120 | VWE; rest unmapped | B/body- |
| `Mirror_Cap` #1124 @91 | `S0102_L&{P}` IDs [1126, 1127, 1128, 1129, 1130, 1131, 1132, 1133, 1134, 1135]; `5JR_L`#1136 | 5JR; rest unmapped | B/body- |
| `Mirrors` #1137 @92 | No native children | Unmapped | B/body- |
| `Mirror_Cap` #1139 @93 | `DRG_L`#1141 | DRG; rest unmapped | B/body- |
| `Mirrors` #1142 @94 | `DYX_L`#1144; `DWK_L`#1145 | DWK, DYX; rest unmapped | B/body- |
| `Wheels` #1146 @95 | `S0804_RL`#1148; `S0805_RL`#1149; `S0802_RL`#1150; `S0803_RL`#1151; `S0808_RL`#1152; `S0809_RL`#1153; `S0800_RL`#1154; `S0801_RL`#1155; `S0806_RL`#1156; `S0807_RL`#1157 | Unmapped | B/body- |
| `Wheel_Caps` #1158 @96 | `S0835_RL`#1160; `S0836_RL`#1161; `S0832_RL`#1162; `S0831_RL`#1163 | Unmapped | B/body- |
| `Brakes` #1164 @97 | `S0222_RL`#1166; `S0206_RL`#1167; `S0208_RL`#1168; `S0210_RL`#1169; `S0218_RL`#1170; `S0225_RL`#1171; `S0228_RL`#1172; `J59_RL`#1173 | J59; rest unmapped | B/body- |
| `Wheels` #1174 @98 | `S0822_FL`#1176; `S0805_FL`#1177; `S0803_FL`#1178; `S0808_FL`#1179; `S0801_FL`#1180 | Unmapped | B/body- |
| `Wheel_Caps` #1181 @99 | `S0835_FL`#1183; `S0905_FL`#1184; `S0833_FL`#1185; `S0831_FL`#1186; `S0830_FL`#1187 | Unmapped | B/body- |
| `Brakes` #1188 @100 | `S0222_FL`#1190; `S0206_FL`#1191; `S0210_FL`#1192; `S0218_FL`#1193; `S0228_FL`#1194 | Unmapped | B/body- |
| `Shadow` #1195 @101 | `S0902`#1197 | Unmapped | B/body- |
| `Background` #1198 @102 | `S0100`#1200 | Unmapped | B/body- |
| `Tow_Hooks` #1201 @103 | No native children | Unmapped | B/body- |

Cabin/trim-dependent groups visible through glass (separate interior scenes are outside this audit): `Console` #290 @43 (0 children); `Stitching` #295 @45 (3 children); `Steering_Wheel` #300 @46 (64 children); `Seat_Belts` #446 @57 (19 children); `Interior` #467 @58 (54 children); `Interior_Kit` #523 @59 (28 children); `Interior` #553 @60 (28 children); `Interior_Kit` #583 @61 (52 children); `IP` #637 @62 (1 children); `Decal_Stickers` #640 @63 (1 children); `Cluster` #643 @64 (2 children); `Stitching` #647 @65 (39 children); `Floors` #688 @66 (33 children); `Interior_Kit` #723 @67 (1 children); `IP` #726 @68 (32 children); `Seats_Front` #760 @69 (119 children); `Interior` #881 @70 (1 children); `Speakers` #889 @72 (81 children); `IP` #972 @73 (1 children); `Decal_Stickers` #975 @74 (32 children); `Console` #1009 @75 (6 children); `Effects` #1023 @78 (32 children). Their seat/material/trim state must be recaptured for lower trims; no upper-trim interior is authorized as a substitute.

</details>

<details>
<summary>S21 — ZR1X coupe view 01</summary>

PSB: **V/zr1x/exterior/27CHCOZR_X_COU_Studio_f02.psb**. Body-paint root index 73; spoiler root indices 65, 67.

<a id="s21-paint"></a>

**Paint — U; all ten base paints**

| Parent path / ID / root index | Exact paint-bearing peers (each maps only its paint token) | Native placement |
| --- | --- | --- |
| `Front_Fascia` #64 @13 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Mirror_Cap` #149 @21 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `B_Pillars` #178 @26 | 20 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Rear_Fascia` #245 @37 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Roof` #262 @39 | 34 paint-bearing children; exact names/IDs below (partial families remain explicit) | F/body+ |
| `Spoiler` #1002 @65 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | S/body+ |
| `Base` #1072 @73 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body= |
| `Rear_Van_Windows` #1085 @74 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body- |
| `Mirror_Cap` #1101 @76 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body- |

<a id="s21-foundation"></a>

**Trim and body foundation**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Base` #935 @59 | `S0507&1LZ`#937; `S0507&3LZ`#938 | Configuration/trim candidates | F/body+ |
| `Base` #1072 @73 | `GBA`#1074; `G8G`#1075; `GKZ`#1076; `GPH`#1077; `G26`#1078; `GBK`#1079; `G4Z`#1080; `GKA`#1081; `GTR`#1082; `GEC`#1083; `1YS07`#1084 | Configuration/trim candidates | B/body= |

<a id="s21-rear"></a>

**Rear spoiler / source-off-spoiler state**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Spoiler` #1002 @65 | `S0268`#1004; `S0267&{P}` IDs [1005, 1006, 1007, 1008, 1009, 1010, 1011, 1012, 1013, 1014]; `SIG`#1015 | Unmapped | S/body+ |
| `Spoiler` #1019 @67 | `TOM`#1021 | TOM; rest unmapped | S/body+ |

Source-off-spoiler state: hide every `Spoiler` parent listed here; this is a visibility recipe, **not a catalog option ID**. No legal no-spoiler configuration is established by this operation.

<a id="s21-aero"></a>

**Front/side/hood/fascia aero candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Hood` #16 @3 | `S0298`#18 | Unmapped | F/body+ |
| `Front_Fascia` #50 @10 | `S0274`#52; `S0273`#53; `S0227`#54; `S0224`#55; `S0221`#56 | Unmapped | F/body+ |
| `Ground_Effects` #57 @11 | `S0396`#59; `S0368`#60 | Unmapped | F/body+ |
| `Front_Fascia` #64 @13 | `S0220&{P}` IDs [66, 67, 68, 69, 70, 71, 72, 73, 74, 75] | Unmapped | F/body+ |
| `Ground_Effects` #146 @20 | `S0366`#148 | Unmapped | F/body+ |
| `Rear_Fascia` #245 @37 | `S0203&{P}` IDs [247, 248, 249, 250, 251, 252, 253, 254, 255, 256] | Unmapped | F/body+ |
| `Hood` #259 @38 | `S0297`#261 | Unmapped | F/body+ |

<a id="s21-graphics"></a>

**Stripes / decals / color candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Decals` #4 @1 | `S0911`#6 | Unmapped | F/body+ |
| `Decals` #19 @4 | `S0837_F`#21; `S0855_F`#22; `S0302_F`#23; `S0330_F`#24; `S0325_F`#25; `S0320_F`#26; `S0315_F`#27; `S0307_F`#28; `S0372_F`#29 | Unmapped | F/body+ |
| `Stripes` #30 @5 | `S0369_F`#32 | Unmapped | F/body+ |
| `Decals` #33 @6 | `S0362_F`#35; `S0349_F`#36; `S0342_F`#37; `S0314_F`#38; `S0306_F`#39; `S0910`#40 | Unmapped | F/body+ |
| `Decals` #206 @29 | `S0866`#208; `S0858`#209; `S0361`#210; `S0348`#211; `S0341`#212; `S0334`#213; `S0313`#214; `S0371`#215 | Unmapped | F/body+ |
| `Decals` #219 @31 | `S0332`#221; `S0327`#222; `S0322`#223; `S0317`#224; `S0304`#225; `S0303`#226; `S0308`#227 | Unmapped | F/body+ |
| `Decals` #982 @63 | `S0874`#984; `S0363`#985; `S0358`#986; `S0344`#987; `S0338`#988; `S0857`#989; `S0373`#990; `S0319`#991; `S0333`#992; `S0328`#993; `S0323`#994; `S0318`#995; `S0310`#996; `S0309`#997; `S0311`#998 | Unmapped | F/body+ |
| `Decals` #1034 @71 | `S0912`#1036; `S0325_B`#1037 | Unmapped | B/body+ |
| `Decals` #1040 @72 | `S0886`#1042; `S0838`#1043; `S0854`#1044; `S0853`#1045; `S0852`#1046; `S0851`#1047; `S0849`#1048; `S0848`#1049; `S0847`#1050; `S0846`#1051; `S0845`#1052; `S0844`#1053; `S0843`#1054; `S0842`#1055; `S0850`#1056; `S0360`#1057; `S0370`#1058; `S0347`#1059; `S0340`#1060; `S0329`#1061; `S0312`#1062; `S0331`#1063; `S0326`#1064; `S0321`#1065; `S0316`#1066; `S0301`#1067; `S0300`#1068; `S0864`#1069; `S0859`#1070; `S0305`#1071 | Unmapped | B/body+ |

<a id="s21-glass"></a>

**Glass and window candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Windows` #175 @25 | `S0105`#177 | Unmapped | F/body+ |
| `Windows` #200 @27 | `S0101_L`#202 | Unmapped | F/body+ |
| `Windows` #240 @36 | `S0108`#242 | Unmapped | F/body+ |
| `Windows` #975 @61 | `S0122`#977; `S0104`#978 | Unmapped | F/body+ |
| `Defroster` #979 @62 | `S0107`#981 | Unmapped | F/body+ |
| `Rear_Van_Windows` #1085 @74 | `ETV&{P}` IDs [1087, 1088, 1089, 1090, 1091, 1092, 1093, 1094, 1095, 1096]; `S0201`#1097 | ETV; rest unmapped | B/body- |
| `Windows` #1098 @75 | `S0101_R`#1100 | Unmapped | B/body- |

<a id="s21-other"></a>

**Other exterior option-driven and fixed groups**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Tow_Hooks` #1 @0 | No native children | Unmapped | F/body+ |
| `Badges` #7 @2 | `EYK_F`#9; `EYT_F`#10; `EYT_B`#11; `SFZ_F`#12; `R88_F`#13; `S0499`#14; `S0498`#15 | EYK, EYT, R88, SFZ; rest unmapped | F/body+ |
| `Tail_Lamps` #41 @7 | `S0200`#43 | Unmapped | F/body+ |
| `Headlamps` #44 @8 | `T4L`#46 | T4L; rest unmapped | F/body+ |
| `Molding` #47 @9 | `S0209`#49 | Unmapped | F/body+ |
| `Grille` #61 @12 | `VWE`#63 | VWE; rest unmapped | F/body+ |
| `Wheels` #76 @14 | `S0821_RL`#78; `S0822_RL`#79; `S0804_RL`#80; `S0805_RL`#81; `S0802_RL`#82; `S0803_RL`#83; `S0808_RL`#84; `S0809_RL`#85; `S0800_RL`#86; `S0801_RL`#87; `S0806_RL`#88; `S0807_RL`#89 | Unmapped | F/body+ |
| `Wheel_Caps` #90 @15 | `S0835_RL`#92; `S0836_RL`#93; `S0832_RL`#94; `S0833_RL`#95; `S0834_RL`#96; `S0831_RL`#97; `S0830_RL`#98; `S0906_RL`#99; `S0905_RL`#100 | Unmapped | F/body+ |
| `Brakes` #101 @16 | `S0222_RL`#103; `S0206_RL`#104; `S0208_RL`#105; `S0210_RL`#106; `S0218_RL`#107; `S0225_RL`#108; `S0228_RL`#109; `J59_RL`#110 | J59; rest unmapped | F/body+ |
| `Wheels` #111 @17 | `S0821_FL`#113; `S0822_FL`#114; `S0804_FL`#115; `S0805_FL`#116; `S0802_FL`#117; `S0803_FL`#118; `S0808_FL`#119; `S0809_FL`#120; `S0800_FL`#121; `S0801_FL`#122; `S0806_FL`#123; `S0807_FL`#124 | Unmapped | F/body+ |
| `Wheel_Caps` #125 @18 | `S0906_FL`#127; `S0905_FL`#128; `S0835_FL`#129; `S0836_FL`#130; `S0832_FL`#131; `S0833_FL`#132; `S0834_FL`#133; `S0831_FL`#134; `S0830_FL`#135 | Unmapped | F/body+ |
| `Brakes` #136 @19 | `S0206_FL`#138; `S0208_FL`#139; `S0210_FL`#140; `S0218_FL`#141; `S0222_FL`#142; `S0225_FL`#143; `S0228_FL`#144; `J59_FL`#145 | J59; rest unmapped | F/body+ |
| `Mirror_Cap` #149 @21 | `S0102_L&{P}` IDs [151, 152, 153, 154, 155, 156, 157, 158, 159, 160] | Unmapped | F/body+ |
| `Mirror_Cap` #163 @22 | `5JR_L`#165 | 5JR; rest unmapped | F/body+ |
| `Mirror_Cap` #168 @23 | `DRG_L`#170 | DRG; rest unmapped | F/body+ |
| `Mirrors` #171 @24 | `DYX_L`#173; `DWK_L`#174 | DWK, DYX; rest unmapped | F/body+ |
| `B_Pillars` #178 @26 | `S0236&{P}` IDs [180, 181, 182, 183, 184, 185, 186, 187, 188, 189]; `S0212&{P}` IDs [190, 191, 192, 193, 194, 195, 196, 197, 198, 199] | Unmapped | F/body+ |
| `Primer` #203 @28 | `S0115`#205 | Unmapped | F/body+ |
| `None` #216 @30 | `S0345`#218 | Unmapped | F/body+ |
| `Doors` #231 @33 | `S0536`#233 | Unmapped | F/body+ |
| `None` #234 @34 | `S0420`#236 | Unmapped | F/body+ |
| `Splashguards` #237 @35 | `S0390`#239 | Unmapped | F/body+ |
| `Roof` #262 @39 | `S0242`#264; `SBT`#265; `S0243&{P}` IDs [266, 267, 268, 269, 270, 271, 272, 273, 274, 275]; `C2Z&{P}` IDs [276, 277, 278, 279, 280, 281, 282, 283, 284, 285]; `CF8&{P}` IDs [286, 287, 288, 289, 290, 291, 292, 293, 294, 295]; `S0839&G26`#296; `S0839&GBK`#297; `S0839&GKA`#298; `S0839&GEC`#299; `S0506`#300; `UG1&HTE`#301; `UG1&HTT`#302; `UG1&HVV`#303; `UG1&HU1`#304; `UG1&HMO`#305; `UG1&HU9`#306; `UG1&HZB`#307; `UG1&HVT`#308; `UG1&HUA`#309; `UG1&HU2`#310; `UG1&HUU`#311; `UG1&HZP`#312; `UG1&HUE`#313; `UG1&HTG`#314; `UG1&HZN`#315; `UG1&HUF`#316; `UG1&HU0`#317; `UG1&HXO`#318; `UG1&HNK`#319; `UG1&HUW`#320; `UG1&HUX`#321; `UG1&HVZ`#322; `UG1&H8T`#323; `UG1&HUB`#324; `UG1&HUC`#325; `UG1&EPX`#326; `UG1&EJH`#327; `UG1&HAG`#328 | C2Z, SBT, UG1; rest unmapped | F/body+ |
| `Badges` #763 @52 | `CFX`#765; `BV4`#766; `S0500`#767 | BV4, CFX; rest unmapped | F/body+ |
| `None` #999 @64 | `S0357`#1001 | Unmapped | F/body+ |
| `None` #1016 @66 | `S0119`#1018 | Unmapped | S/body+ |
| `Engine` #1022 @68 | `SLN`#1024; `LT7`#1025 | LT7, SLN; rest unmapped | B/body+ |
| `Exhaust` #1026 @69 | `WUB`#1028; `S0867`#1029; `S0868`#1030 | WUB; rest unmapped | B/body+ |
| `Tow_Hooks` #1031 @70 | `S0871`#1033 | Unmapped | B/body+ |
| `Mirror_Cap` #1101 @76 | `S0102_R&{P}` IDs [1103, 1104, 1105, 1106, 1107, 1108, 1109, 1110, 1111, 1112]; `5JR_R`#1113 | 5JR; rest unmapped | B/body- |
| `Mirrors` #1114 @77 | `UFT_R`#1116 | UFT; rest unmapped | B/body- |
| `Mirror_Cap` #1117 @78 | `DRG_R`#1119 | DRG; rest unmapped | B/body- |
| `Mirrors` #1120 @79 | `DYX_R`#1122; `DWK_R`#1123 | DWK, DYX; rest unmapped | B/body- |
| `Wheel_Caps` #1126 @80 | `S0905_RR`#1128 | Unmapped | B/body- |
| `Brakes` #1129 @81 | `S0208_RR`#1131; `S0218_RR`#1132 | Unmapped | B/body- |
| `Wheels` #1133 @82 | `S0822_FR`#1135; `S0805_FR`#1136; `S0808_FR`#1137 | Unmapped | B/body- |
| `Wheel_Caps` #1138 @83 | `S0836_FR`#1140; `S0830_FR`#1141 | Unmapped | B/body- |
| `Brakes` #1142 @84 | `S0210_FR`#1144; `J59_FR`#1145 | J59; rest unmapped | B/body- |
| `Shadow` #1146 @85 | `S0902`#1148 | Unmapped | B/body- |
| `Background` #1149 @86 | `S0100`#1151 | Unmapped | B/body- |

Cabin/trim-dependent groups visible through glass (separate interior scenes are outside this audit): `Console` #228 @32 (1 children); `Stitching` #329 @40 (11 children); `Steering_Wheel` #342 @41 (41 children); `Interior_Kit` #385 @42 (1 children); `Interior` #388 @43 (52 children); `Interior_Kit` #442 @44 (26 children); `Interior` #470 @45 (28 children); `Interior_Kit` #500 @46 (50 children); `Stitching` #552 @47 (34 children); `Seat_Belts` #588 @48 (20 children); `Seats_Front` #610 @49 (119 children); `Floors` #731 @50 (26 children); `Cluster` #759 @51 (2 children); `IP` #768 @53 (1 children); `Decal_Stickers` #771 @54 (1 children); `Stitching` #774 @55 (3 children); `Decal_Stickers` #781 @56 (32 children); `IP` #815 @57 (32 children); `Speakers` #849 @58 (84 children); `Effects` #941 @60 (32 children); `Console` #1152 @87 (7 children). Their seat/material/trim state must be recaptured for lower trims; no upper-trim interior is authorized as a substitute.

</details>

<details>
<summary>S22 — ZR1X coupe view 02</summary>

PSB: **V/zr1x/exterior/27CHCOZR_X_COU_Studio_f04.psb**. Body-paint root index 82; spoiler root indices 1, 4, 6.

<a id="s22-paint"></a>

**Paint — U; all ten base paints**

| Parent path / ID / root index | Exact paint-bearing peers (each maps only its paint token) | Native placement |
| --- | --- | --- |
| `Spoiler` #28 @4 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | S/body+ |
| `Rear_Van_Windows` #137 @15 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Mirror_Cap` #260 @31 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Roof` #374 @43 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Roof` #389 @45 | 30 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Front_Fascia` #461 @49 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `B_Pillars` #1060 @73 | 20 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Rear_Fascia` #1093 @77 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body+ |
| `Base` #1117 @82 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body= |
| `Mirror_Cap` #1136 @85 | 10 paint-bearing children; exact names/IDs below (partial families remain explicit) | B/body- |

<a id="s22-foundation"></a>

**Trim and body foundation**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Base` #1020 @70 | `S0507&1LZ`#1022; `S0507&3LZ`#1023 | Configuration/trim candidates | B/body+ |
| `Base` #1117 @82 | `GBA`#1119; `G8G`#1120; `GKZ`#1121; `GPH`#1122; `G26`#1123; `GBK`#1124; `G4Z`#1125; `GKA`#1126; `GTR`#1127; `GEC`#1128; `1YS07`#1129 | Configuration/trim candidates | B/body= |

<a id="s22-rear"></a>

**Rear spoiler / source-off-spoiler state**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Spoiler` #5 @1 | `SIG`#7 | Unmapped | S/body+ |
| `Spoiler` #28 @4 | `S0268`#30; `S0267&{P}` IDs [31, 32, 33, 34, 35, 36, 37, 38, 39, 40] | Unmapped | S/body+ |
| `Spoiler` #44 @6 | `TOM`#46 | TOM; rest unmapped | S/body+ |

Source-off-spoiler state: hide every `Spoiler` parent listed here; this is a visibility recipe, **not a catalog option ID**. No legal no-spoiler configuration is established by this operation.

<a id="s22-aero"></a>

**Front/side/hood/fascia aero candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Hood` #59 @8 | `S0298`#61 | Unmapped | B/body+ |
| `Rear_Fascia` #175 @20 | `S0204`#177 | Unmapped | B/body+ |
| `Ground_Effects` #187 @24 | `S0366`#189 | Unmapped | B/body+ |
| `Front_Fascia` #366 @41 | `S0274`#368; `S0273`#369 | Unmapped | B/body+ |
| `Ground_Effects` #370 @42 | `S0396`#372; `S0368`#373 | Unmapped | B/body+ |
| `Front_Fascia` #461 @49 | `S0220&{P}` IDs [463, 464, 465, 466, 467, 468, 469, 470, 471, 472] | Unmapped | B/body+ |
| `Rear_Fascia` #1093 @77 | `S0203&{P}` IDs [1095, 1096, 1097, 1098, 1099, 1100, 1101, 1102, 1103, 1104] | Unmapped | B/body+ |
| `Hood` #1114 @81 | `S0297`#1116 | Unmapped | B/body+ |

<a id="s22-graphics"></a>

**Stripes / decals / color candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Decals` #8 @2 | `S0874`#10; `S0363`#11; `S0358`#12; `S0344`#13; `S0338`#14; `S0857`#15; `S0373`#16; `S0319`#17; `S0333`#18; `S0328`#19; `S0323`#20; `S0318`#21; `S0310`#22; `S0309`#23; `S0311`#24 | Unmapped | S/body+ |
| `Decals` #62 @9 | `S0837_F`#64; `S0855_F`#65; `S0302_F`#66; `S0330_F`#67; `S0325_F`#68; `S0320_F`#69; `S0315_F`#70; `S0307_F`#71; `S0372_F`#72 | Unmapped | B/body+ |
| `Stripes` #73 @10 | `S0369_F`#75 | Unmapped | B/body+ |
| `Decals` #76 @11 | `S0362_F`#78; `S0349_F`#79; `S0342_F`#80; `S0314_F`#81; `S0306_F`#82; `S0910`#83; `S0866`#84; `S0858`#85; `S0361`#86; `S0348`#87; `S0341`#88; `S0334`#89; `S0313`#90; `S0371`#91 | Unmapped | B/body+ |
| `Decals` #95 @13 | `S0332`#97; `S0327`#98; `S0322`#99; `S0317`#100; `S0304`#101; `S0303`#102; `S0308`#103; `S0886`#104; `S0838`#105; `S0854`#106; `S0853`#107; `S0852`#108; `S0851`#109; `S0849`#110; `S0848`#111; `S0847`#112; `S0846`#113; `S0845`#114; `S0844`#115; `S0843`#116; `S0842`#117; `S0850`#118; `S0360`#119; `S0370`#120; `S0347`#121; `S0340`#122; `S0329`#123; `S0312`#124; `S0331`#125; `S0326`#126; `S0321`#127; `S0316`#128; `S0301`#129; `S0300`#130; `S0864`#131; `S0859`#132; `S0305`#133 | Unmapped | B/body+ |
| `Decals` #150 @16 | `S0855_B`#152; `S0837_B`#153; `S0330_B`#154; `S0320_B`#155; `S0315_B`#156; `S0307_B`#157; `S0325_B`#158; `S0372_B`#159 | Unmapped | B/body+ |
| `Stripes` #160 @17 | `S0369_B`#162 | Unmapped | B/body+ |
| `Decals` #163 @18 | `S0362_B`#165; `S0349_B`#166; `S0342_B`#167; `S0314_B`#168; `S0306_B`#169; `S0302_B`#170 | Unmapped | B/body+ |
| `Decals` #181 @22 | `S0912`#183 | Unmapped | B/body+ |
| `Decals` #386 @44 | `S0911`#388 | Unmapped | B/body+ |

<a id="s22-glass"></a>

**Glass and window candidates**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Rear_Van_Windows` #137 @15 | `ETV&{P}` IDs [139, 140, 141, 142, 143, 144, 145, 146, 147, 148]; `S0201`#149 | ETV; rest unmapped | B/body+ |
| `Windows` #283 @35 | `S0101_R`#285; `S0108`#286 | Unmapped | B/body+ |
| `Defroster` #452 @46 | `S0107`#454 | Unmapped | B/body+ |
| `Windows` #455 @47 | `S0104`#457 | Unmapped | B/body+ |
| `Windows` #473 @50 | `S0122`#475 | Unmapped | B/body+ |
| `Windows` #1111 @80 | `S0105`#1113 | Unmapped | B/body+ |
| `Windows` #1133 @84 | `S0101_L`#1135 | Unmapped | B/body- |

<a id="s22-other"></a>

**Other exterior option-driven and fixed groups**

| Parent path / ID / root index | Native child paths (ordered) | Catalog mapping disposition | Stack relative to body / spoiler |
| --- | --- | --- | --- |
| `Badges` #1 @0 | No native children | Unmapped | F/body+ |
| `None` #25 @3 | `S0357`#27 | Unmapped | S/body+ |
| `None` #41 @5 | `S0119`#43 | Unmapped | S/body+ |
| `Badges` #47 @7 | `SL8`#49; `RIN`#50; `RIK`#51; `EYT_F`#52; `EYK_B`#53; `EYT_B`#54; `SFZ_B`#55; `S0276`#56; `S0279`#57; `R88_B`#58 | EYK, EYT, R88, RIK, RIN, SFZ, SL8; rest unmapped | B/body+ |
| `None` #92 @12 | `S0345`#94 | Unmapped | B/body+ |
| `Tail_Lamps` #134 @14 | `S0200`#136 | Unmapped | B/body+ |
| `Multimedia` #171 @19 | `S0287`#173; `S0244`#174 | Unmapped | B/body+ |
| `License_Plate` #178 @21 | `S0235`#180 | Unmapped | B/body+ |
| `Molding` #184 @23 | `S0209`#186 | Unmapped | B/body+ |
| `Wheels` #190 @25 | `S0821_FR`#192; `S0822_FR`#193; `S0804_FR`#194; `S0805_FR`#195; `S0802_FR`#196; `S0803_FR`#197; `S0808_FR`#198; `S0809_FR`#199; `S0800_FR`#200; `S0801_FR`#201; `S0806_FR`#202; `S0807_FR`#203 | Unmapped | B/body+ |
| `Wheel_Caps` #204 @26 | `S0905_FR`#206; `S0906_FR`#207; `S0835_FR`#208; `S0836_FR`#209; `S0832_FR`#210; `S0833_FR`#211; `S0834_FR`#212; `S0831_FR`#213; `S0830_FR`#214 | Unmapped | B/body+ |
| `Brakes` #215 @27 | `S0222_FR`#217; `S0206_FR`#218; `S0208_FR`#219; `S0210_FR`#220; `S0218_FR`#221; `S0225_FR`#222; `S0228_FR`#223; `J59_FR`#224 | J59; rest unmapped | B/body+ |
| `Wheels` #225 @28 | `S0821_RR`#227; `S0822_RR`#228; `S0804_RR`#229; `S0805_RR`#230; `S0802_RR`#231; `S0803_RR`#232; `S0808_RR`#233; `S0809_RR`#234; `S0800_RR`#235; `S0801_RR`#236; `S0806_RR`#237; `S0807_RR`#238 | Unmapped | B/body+ |
| `Wheel_Caps` #239 @29 | `S0905_RR`#241; `S0906_RR`#242; `S0835_RR`#243; `S0836_RR`#244; `S0833_RR`#245; `S0832_RR`#246; `S0834_RR`#247; `S0831_RR`#248; `S0830_RR`#249 | Unmapped | B/body+ |
| `Brakes` #250 @30 | `S0222_RR`#252; `S0206_RR`#253; `S0208_RR`#254; `S0210_RR`#255; `S0218_RR`#256; `S0225_RR`#257; `S0228_RR`#258; `J59_RR`#259 | J59; rest unmapped | B/body+ |
| `Mirror_Cap` #260 @31 | `S0102_R&{P}` IDs [262, 263, 264, 265, 266, 267, 268, 269, 270, 271]; `5JR_R`#272 | 5JR; rest unmapped | B/body+ |
| `Mirrors` #273 @32 | No native children | Unmapped | B/body+ |
| `Mirror_Cap` #275 @33 | `DRG_R`#277 | DRG; rest unmapped | B/body+ |
| `Mirrors` #278 @34 | `VA5`#280; `DYX_R`#281; `DWK_R`#282 | DWK, DYX; rest unmapped | B/body+ |
| `Doors` #289 @37 | `S0536`#291 | Unmapped | B/body+ |
| `None` #363 @40 | `S0420`#365 | Unmapped | B/body+ |
| `Roof` #374 @43 | `S0839&{P}` IDs [376, 377, 378, 379, 380, 381, 382, 383, 384, 385] | Unmapped | B/body+ |
| `Roof` #389 @45 | `S0242`#391; `SBT`#392; `S0243&{P}` IDs [393, 394, 395, 396, 397, 398, 399, 400, 401, 402]; `C2Z&{P}` IDs [403, 404, 405, 406, 407, 408, 409, 410, 411, 412]; `CF8&{P}` IDs [413, 414, 415, 416, 417, 418, 419, 420, 421, 422]; `S0506`#423; `UG1&HTE`#424; `UG1&HTT`#425; `UG1&HVV`#426; `UG1&HU1`#427; `UG1&HMO`#428; `UG1&HU9`#429; `UG1&HZB`#430; `UG1&HVT`#431; `UG1&HUA`#432; `UG1&HU2`#433; `UG1&HUU`#434; `UG1&HZP`#435; `UG1&HUE`#436; `UG1&HTG`#437; `UG1&HZN`#438; `UG1&HUF`#439; `UG1&HU0`#440; `UG1&HXO`#441; `UG1&HNK`#442; `UG1&HUW`#443; `UG1&HUX`#444; `UG1&HVZ`#445; `UG1&H8T`#446; `UG1&HUB`#447; `UG1&HUC`#448; `UG1&EPX`#449; `UG1&EJH`#450; `UG1&HAG`#451 | C2Z, SBT, UG1; rest unmapped | B/body+ |
| `Headlamps` #458 @48 | `T4L`#460 | T4L; rest unmapped | B/body+ |
| `Badges` #892 @65 | `CFX`#894; `BV4`#895; `S0500`#896 | BV4, CFX; rest unmapped | B/body+ |
| `Radio` #1024 @71 | No native children | Unmapped | B/body+ |
| `B_Pillars` #1060 @73 | `S0236&{P}` IDs [1062, 1063, 1064, 1065, 1066, 1067, 1068, 1069, 1070, 1071]; `S0212&{P}` IDs [1072, 1073, 1074, 1075, 1076, 1077, 1078, 1079, 1080, 1081] | Unmapped | B/body+ |
| `Engine` #1082 @74 | `LT7`#1084 | LT7; rest unmapped | B/body+ |
| `Tow_Hooks` #1085 @75 | `S0871`#1087 | Unmapped | B/body+ |
| `Exhaust` #1088 @76 | `S0867`#1090; `S0868`#1091; `WUB`#1092 | WUB; rest unmapped | B/body+ |
| `Splashguards` #1105 @78 | `S0390`#1107 | Unmapped | B/body+ |
| `Primer` #1108 @79 | `S0115`#1110 | Unmapped | B/body+ |
| `Grille` #1130 @83 | `VWE`#1132 | VWE; rest unmapped | B/body- |
| `Mirror_Cap` #1136 @85 | `S0102_L&{P}` IDs [1138, 1139, 1140, 1141, 1142, 1143, 1144, 1145, 1146, 1147]; `5JR_L`#1148 | 5JR; rest unmapped | B/body- |
| `Mirrors` #1149 @86 | No native children | Unmapped | B/body- |
| `Mirror_Cap` #1151 @87 | `DRG_L`#1153 | DRG; rest unmapped | B/body- |
| `Mirrors` #1154 @88 | `DYX_L`#1156; `DWK_L`#1157 | DWK, DYX; rest unmapped | B/body- |
| `Wheels` #1158 @89 | `S0822_RL`#1160; `S0804_RL`#1161; `S0805_RL`#1162; `S0802_RL`#1163; `S0803_RL`#1164; `S0808_RL`#1165; `S0809_RL`#1166; `S0800_RL`#1167; `S0801_RL`#1168; `S0806_RL`#1169; `S0807_RL`#1170 | Unmapped | B/body- |
| `Wheel_Caps` #1171 @90 | `S0832_RL`#1173; `S0830_RL`#1174; `S0905_RL`#1175 | Unmapped | B/body- |
| `Brakes` #1176 @91 | `S0222_RL`#1178; `S0206_RL`#1179; `S0208_RL`#1180; `S0210_RL`#1181; `S0218_RL`#1182; `S0225_RL`#1183; `S0228_RL`#1184; `J59_RL`#1185 | J59; rest unmapped | B/body- |
| `Wheels` #1186 @92 | `S0805_FL`#1188; `S0809_FL`#1189; `S0806_FL`#1190; `S0807_FL`#1191 | Unmapped | B/body- |
| `Wheel_Caps` #1192 @93 | `S0835_FL`#1194; `S0836_FL`#1195; `S0832_FL`#1196; `S0833_FL`#1197; `S0834_FL`#1198; `S0831_FL`#1199; `S0830_FL`#1200 | Unmapped | B/body- |
| `Brakes` #1201 @94 | `S0210_FL`#1203 | Unmapped | B/body- |
| `Shadow` #1204 @95 | `S0902`#1206 | Unmapped | B/body- |
| `Background` #1207 @96 | `S0100`#1209 | Unmapped | B/body- |
| `Tow_Hooks` #1210 @97 | `S0869`#1212 | Unmapped | B/body- |

Cabin/trim-dependent groups visible through glass (separate interior scenes are outside this audit): `Console` #287 @36 (0 children); `Stitching` #292 @38 (3 children); `Steering_Wheel` #297 @39 (64 children); `Seat_Belts` #476 @51 (20 children); `Interior` #498 @52 (54 children); `Interior_Kit` #554 @53 (27 children); `Interior` #583 @54 (23 children); `Interior_Kit` #608 @55 (55 children); `IP` #665 @56 (1 children); `Decal_Stickers` #668 @57 (1 children); `Cluster` #671 @58 (2 children); `Stitching` #675 @59 (45 children); `Floors` #722 @60 (26 children); `Interior_Kit` #750 @61 (1 children); `IP` #753 @62 (32 children); `Seats_Front` #787 @63 (100 children); `Interior` #889 @64 (1 children); `Speakers` #897 @66 (75 children); `IP` #974 @67 (1 children); `Decal_Stickers` #977 @68 (32 children); `Console` #1011 @69 (7 children); `Effects` #1026 @72 (32 children). Their seat/material/trim state must be recaptured for lower trims; no upper-trim interior is authorized as a substitute.

</details>

## Prioritized independently reviewable batches

1. **Source/identity decisions before exports.** Resolve S09 coupe-01 1LT missing peer, review S21 drift against its pinned native inventory, qualify or reject S01 as a GSX-derived scene, and identify internal spoiler/stripe/ground-effect aliases against catalog evidence. Keep GSX body/view gaps explicit. Do not schedule unavailable 5ZU/5ZZ/5ZW/5V7 as selectable coverage.
2. **Stingray view-01 paints and usable rear states, one body per batch.** Reuse the existing three-paint recipe and no-spoiler native references; add the seven exact paint families and both mirror peers. First establish default/TVS/T0A/ZF1 identities and a renderer no-spoiler contract. Keep 3LT baseline, 2LT exports and missing 1LT work independently reviewable.
3. **Lower trims on existing view 01, one model/body per batch.** Use that PSB’s explicit `S0507` layer plus catalog-correct visible cabin, mirrors and other trim-dependent equipment. Prove native references for each trim; never relabel current 3LT/3LZ images. ZR1/ZR1X have 1LZ only below 3LZ.
4. **Existing unbound rear/component proofs.** Review W/asset-proofs/2026-09-21-components/ (218 prior exports / 83 historical comparisons) and the separate five-plane Grand Sport roof proof. Low-spoiler S0267/T0E, wheel/cap and caliper/disc identities remain qualification work. Reuse qualified states/evidence; do not rerun them simply because no application binding exists.
5. **Renderer depth/view support as a separate future code task.** Establish multiple depth intervals, component replacement, no-spoiler state and view identity before consuming new independent overlays. This audit does not prescribe a renderer rewrite or authorize one.
6. **Full aero, one catalog package/model/body/view per batch.** Rear wing + splitter + rockers + dive planes/hood pieces and finish dependencies must be reviewed together, then compared with a native full scene. Give Z06 T0F/T0G/CBF and ZR1/ZR1X TOM/5WN/PCR separate batches; equal RPOs never share implicit bindings.
7. **Stripes/graphics, one package/color/model/body/view per batch.** Resolve S-code identities first, then capture every front/rear/roof branch at its native depth. Color names and applicability come from the catalog tables, including Royal Blue DTC/DUE and retired DUW; do not infer a palette from numeric layer aliases.
8. **Glass/tint and remaining equipment.** Obtain the actual tint specification, then qualify per-window masks/reflections/defrosters and transparent roof interaction. Wheels/calipers/caps, roof, mirrors/badges/exhaust follow as separate complete replacement assemblies. Finally qualify second-view equivalents and GSX sources when available.

Each later export batch uses the existing W workflow: fresh copy → hash-pinned native reference/recipe → `build-asset-states.py` → `build-export-batch.py` / unchanged `export-states.psjs` → `verify-native-compositions.py` plus visual inspection → restored visibility and original/copy hashes. Full-canvas raw evidence remains outside Git. Binding, merge, deployment and release acceptance are separate decisions.

## Validation and limits

Checks executed: 22/22 native inventories (30,236 layer records); unchanged visibility for all; 22/22 original/copy four-way SHA-256 matches; native versus binary identity/order/visibility comparison for every shared layer; all 64 catalog configuration/view rows and ten paints in every supplied source; current draft/release option and configuration equality; `artwork.load_collection()` verified all ten manifests/proofs and 192 asset hashes; `ConsumerCatalog` against the R3 release produced eight component previews, two unavailable Stingray scenes and unbound GSX. Markdown references, table consistency and the one-file Git diff were reviewed. No application test suite or browser-render check was needed for this documentation-only change. No new native render, transparent-alpha inspection, stripe-color recognition, pixel equivalence, trim correctness or package completeness is claimed from an inventory. Existing proof assertions remain historical evidence. No artwork, manifests, renderer, catalog data or deployment was changed.
