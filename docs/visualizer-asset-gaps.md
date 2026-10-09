# Visualizer source coverage and export gaps
Audit date: **October 9, 2026**. This is an inventory and review plan, not artwork acceptance, an export, a binding, or a renderer change. All paths below are local source evidence; no PSB, PNG, manifest or application file is added by this task.

## Findings that change the next artwork task

- **Stingray has all ten paints in all four source views**, including the seven absent from the binding. Its saved sources also contain ten body-color 5ZU variants, 5ZZ, 5ZW, 5V5 and internal low/Z51-looking spoiler families. The last two descriptions are only candidates: internal `S011*` identities are **unmapped**, not accepted TVS/T0A identities. The two existing 5ZU bindings remain on disk but are unusable against the R3 catalog because 5ZU is `factory_unavailable`.
- **Lower-trim layers mostly exist.** `Base / S0507&1LT` is absent from Stingray coupe view 01 (S09); its 2LT peer exists. All other supplied non-GSX body/view files have explicit layers for their catalog trims. A layer is a starting point for a trim-specific recipe, not permission to reuse 3LT/3LZ pixels.
- **GSX is a derived Grand Sport coupe view-01 work product.** S01 is not a separate native manufacturer GSX scene. Its saved source retains `Base / 1YE07`; there is no `1YG07` foundation. It has modified badge/fascia branches and unqualified inherited options. No GSX convertible or second-view source exists in this folder.
- **ZR1X coupe source drift exists.** S21 differs from the file hash pinned by its bound proof; the shipped proof/media remains its own immutable historical artifact. Do not regenerate that binding against the current file without reviewing the differences.
- **Stripes, full aero, wheels and roof are not independent choices in the current renderer.** Their native positions span multiple depth intervals. A rear wing at slot 20 does not represent the rest of its aero package. The owner’s opaque tint is a fixed native-scene treatment, to qualify before lower trims; it needs multiple source placements but no tint selector. Second views also need explicit view identity/selection: `load_collection()` currently rejects overlapping model/year/body/trim scopes.

## Evidence, source safety and reading the matrix

Read: `AGENTS.md`, `README.md`, `docs/visualizer-artwork.md`, `docs/form-audit-and-live-migration.md` §3, the October 7 direction in `docs/migration-plan.md`, `catalog/artwork.py`, the collection index, and all ten application manifests and source proofs. The current launch remains artwork-hidden unless explicitly bundled with `--with-artwork`. Earlier statements that no GSX-named file exists now carry a short pointer to the provenance finding here.

Catalog authority for identities, names, colors, lifecycle and configuration scope is completed release `11f2d01cdfd7c6e472b6f136ed75cbd7b5c634be30cb2647f04d098c72e09dac`, after R3. Its `catalog.sqlite` SHA-256 is `3b24fab82b23b4d3d4babebc7e19ef9b505fbac9d2f823badfa6fe227c94e1dc`. The draft `configuration`, `option`, and `option_configuration` tables were also read and match this release exactly. Tables read: `model`, `model_year`, `catalog_revision`, `configuration`, `option`, `option_configuration`, `consumer_option`, and connected condition/acquisition/content records. Layer labels provide only the location of candidate artwork. They never create a catalog option or override availability. An option identity below is always **model + 2027 + option ID**, even where IDs/RPOs repeat.

Source root **V** = `/Users/seandm/Library/Mobile Documents/com~apple~CloudDocs/C8-iCloud/27img/visualizer-studio_27/visual-studio/`. Workflow root **W** = its sibling `27vette-phase1/`. Read `ASSET-WORKFLOW.md`, `REPRODUCE-PROOFS.md`, `build-asset-states.py`, `build-export-batch.py`, `verify-native-compositions.py`; retained the same state/recipe/export workflow. Reused `build-asset-states.py` SHA-256 helper and the unchanged `dump-layers.psjs` inside a disposable audit wrapper (file picker replaced with JSON capture). No exporter or compositor ran. Binary `psd-tools` inspection of disposable copies supplied an independent saved-layer/XMP comparison, not a replacement rendering pipeline.

Native Photoshop inventories completed for **23/23** distinct saved exterior source copies (22 initial inventories plus S23 in this revision). Two byte-identical duplicate files are registered without repeating their inventory. All inventories were read-only: no visibility flag was changed; before/after snapshots were identical (`sourceVisibilityRestored=true`), and each copy was closed without saving. Original and copy integrity results are in the source register below. Raw-reader extras (including hidden `Tow_Hooks` and several empty second-view branches) are excluded from the native inventory. All shared saved/native IDs, names, parent IDs, sibling indices and visibility flags matched (31,299 native layer records total); raw counts are not substituted for native counts. The pre-existing, unsaved GSX original was left open and untouched; this audit covers its saved bytes only.

The Adobe UXP Developer Tool GUI crashed on launch. The same inventory script was ultimately opened directly in Photoshop as `.psjs`; this changes only script invocation, not the inventory/export workflow. A temporary vendor service used during diagnosis did not establish a Photoshop connection; no developer preference or security setting was changed.

| Code | Requested status | Meaning |
| --- | --- | --- |
| B | bound | An indexed application manifest and native proof already bind the exact model/body/trim/view/component. This is component coverage, not a complete configured car. |
| U | source-available-not-exported | Source layers exist, but there is no qualified current binding for this cell. Some U entries have earlier unbound proof exports, identified below; reuse/review those before re-exporting. Unmapped aliases are explicitly not qualified identities. |
| M | source-missing | The model/body/view file, explicit trim layer or required opaque tint treatment is absent. No other model or upper trim substitutes. |
| R | needs-renderer-change | Source exists, but current independent selection/stack/view contract cannot represent it. Native availability and exact paths are retained in the linked inventory. |
| † | Qualification hold | Derived GSX candidate, unavailable bound 5ZU, or source drift as described; this marker is not a fifth status. |
| — | Not a catalog configuration | ZR1/ZR1X 2LZ does not exist; it is not an artwork gap. |

This matrix is factored to avoid copying thousands of layer paths into each trim row: **configuration/view row → Sxx/component inventory → model option table** is one complete cell. Sxx resolves to the exact PSB and hash in the source register. Component inventories give full parent paths, parent and child layer IDs, native ordering and mapped/unmapped catalog candidates. Model option tables give exact IDs, names/colors and body/trim scope. Read all three keys together; no row inherits another model’s identity. `01` means `.exterior.01` / `f02`; `02` means `.exterior.02` / `f04`.

## Model × body × trim × view coverage

| Model | Body | Trim | View | Paint | Trim/foundation | Rear/no spoiler | Full aero / stripes | Glass / tint | Other choices |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Stingray | coupe | 1LT | 01 | U (10) [S09/paint](#s09-paint) | M [S09/foundation](#s09-foundation) | U [S09/rear](#s09-rear) | R [S09/aero](#s09-aero) / [S09/graphics](#s09-graphics) | U glass / M tint [S09/glass](#s09-glass) | R [S09/other](#s09-other) |
| Stingray | coupe | 1LT | 02 | R (view); U (10 source) [S10/paint](#s10-paint) | U [S10/foundation](#s10-foundation) | R (view) [S10/rear](#s10-rear) | R [S10/aero](#s10-aero) / [S10/graphics](#s10-graphics) | U glass / M tint [S10/glass](#s10-glass) | R [S10/other](#s10-other) |
| Stingray | coupe | 2LT | 01 | U (10) [S09/paint](#s09-paint) | U [S09/foundation](#s09-foundation) | U [S09/rear](#s09-rear) | R [S09/aero](#s09-aero) / [S09/graphics](#s09-graphics) | U glass / M tint [S09/glass](#s09-glass) | R [S09/other](#s09-other) |
| Stingray | coupe | 2LT | 02 | R (view); U (10 source) [S10/paint](#s10-paint) | U [S10/foundation](#s10-foundation) | R (view) [S10/rear](#s10-rear) | R [S10/aero](#s10-aero) / [S10/graphics](#s10-graphics) | U glass / M tint [S10/glass](#s10-glass) | R [S10/other](#s10-other) |
| Stingray | coupe | 3LT | 01 | B (3), U (7)† [S09/paint](#s09-paint) | B† [S09/foundation](#s09-foundation) | B (5ZU), U (others)† [S09/rear](#s09-rear) | R† [S09/aero](#s09-aero) / [S09/graphics](#s09-graphics) | U glass / M tint† [S09/glass](#s09-glass) | R† [S09/other](#s09-other) |
| Stingray | coupe | 3LT | 02 | R (view); U (10 source) [S10/paint](#s10-paint) | U [S10/foundation](#s10-foundation) | R (view) [S10/rear](#s10-rear) | R [S10/aero](#s10-aero) / [S10/graphics](#s10-graphics) | U glass / M tint [S10/glass](#s10-glass) | R [S10/other](#s10-other) |
| Stingray | convertible | 1LT | 01 | U (10) [S07/paint](#s07-paint) | U [S07/foundation](#s07-foundation) | U [S07/rear](#s07-rear) | R [S07/aero](#s07-aero) / [S07/graphics](#s07-graphics) | U glass / M tint [S07/glass](#s07-glass) | R [S07/other](#s07-other) |
| Stingray | convertible | 1LT | 02 | R (view); U (10 source) [S08/paint](#s08-paint) | U [S08/foundation](#s08-foundation) | R (view) [S08/rear](#s08-rear) | R [S08/aero](#s08-aero) / [S08/graphics](#s08-graphics) | U glass / M tint [S08/glass](#s08-glass) | R [S08/other](#s08-other) |
| Stingray | convertible | 2LT | 01 | U (10) [S07/paint](#s07-paint) | U [S07/foundation](#s07-foundation) | U [S07/rear](#s07-rear) | R [S07/aero](#s07-aero) / [S07/graphics](#s07-graphics) | U glass / M tint [S07/glass](#s07-glass) | R [S07/other](#s07-other) |
| Stingray | convertible | 2LT | 02 | R (view); U (10 source) [S08/paint](#s08-paint) | U [S08/foundation](#s08-foundation) | R (view) [S08/rear](#s08-rear) | R [S08/aero](#s08-aero) / [S08/graphics](#s08-graphics) | U glass / M tint [S08/glass](#s08-glass) | R [S08/other](#s08-other) |
| Stingray | convertible | 3LT | 01 | B (3), U (7)† [S07/paint](#s07-paint) | B† [S07/foundation](#s07-foundation) | B (5ZU), U (others)† [S07/rear](#s07-rear) | R† [S07/aero](#s07-aero) / [S07/graphics](#s07-graphics) | U glass / M tint† [S07/glass](#s07-glass) | R† [S07/other](#s07-other) |
| Stingray | convertible | 3LT | 02 | R (view); U (10 source) [S08/paint](#s08-paint) | U [S08/foundation](#s08-foundation) | R (view) [S08/rear](#s08-rear) | R [S08/aero](#s08-aero) / [S08/graphics](#s08-graphics) | U glass / M tint [S08/glass](#s08-glass) | R [S08/other](#s08-other) |
| Grand Sport | coupe | 1LT | 01 | U (10) [S04/paint](#s04-paint)‡ | U [S04/foundation](#s04-foundation)‡ | U [S04/rear](#s04-rear)‡ | R [S04/aero](#s04-aero)‡ / [S04/graphics](#s04-graphics)‡ | U glass / M tint [S04/glass](#s04-glass)‡ | R [S04/other](#s04-other)‡ |
| Grand Sport | coupe | 1LT | 02 | R (view); U (10 source) [S06/paint](#s06-paint) | U [S06/foundation](#s06-foundation) | R (view) [S06/rear](#s06-rear) | R [S06/aero](#s06-aero) / [S06/graphics](#s06-graphics) | U glass / M tint [S06/glass](#s06-glass) | R [S06/other](#s06-other) |
| Grand Sport | coupe | 2LT | 01 | U (10) [S04/paint](#s04-paint)‡ | U [S04/foundation](#s04-foundation)‡ | U [S04/rear](#s04-rear)‡ | R [S04/aero](#s04-aero)‡ / [S04/graphics](#s04-graphics)‡ | U glass / M tint [S04/glass](#s04-glass)‡ | R [S04/other](#s04-other)‡ |
| Grand Sport | coupe | 2LT | 02 | R (view); U (10 source) [S06/paint](#s06-paint) | U [S06/foundation](#s06-foundation) | R (view) [S06/rear](#s06-rear) | R [S06/aero](#s06-aero) / [S06/graphics](#s06-graphics) | U glass / M tint [S06/glass](#s06-glass) | R [S06/other](#s06-other) |
| Grand Sport | coupe | 3LT | 01 | B (10) [S04/paint](#s04-paint)‡ | B [S04/foundation](#s04-foundation)‡ | B (listed), U (others) [S04/rear](#s04-rear)‡ | R [S04/aero](#s04-aero)‡ / [S04/graphics](#s04-graphics)‡ | U glass / M tint [S04/glass](#s04-glass)‡ | R [S04/other](#s04-other)‡ |
| Grand Sport | coupe | 3LT | 02 | R (view); U (10 source) [S06/paint](#s06-paint) | U [S06/foundation](#s06-foundation) | R (view) [S06/rear](#s06-rear) | R [S06/aero](#s06-aero) / [S06/graphics](#s06-graphics) | U glass / M tint [S06/glass](#s06-glass) | R [S06/other](#s06-other) |
| Grand Sport | convertible | 1LT | 01 | U (10) [S02/paint](#s02-paint) | U [S02/foundation](#s02-foundation) | U [S02/rear](#s02-rear) | R [S02/aero](#s02-aero) / [S02/graphics](#s02-graphics) | U glass / M tint [S02/glass](#s02-glass) | R [S02/other](#s02-other) |
| Grand Sport | convertible | 1LT | 02 | R (view); U (10 source) [S03/paint](#s03-paint) | U [S03/foundation](#s03-foundation) | R (view) [S03/rear](#s03-rear) | R [S03/aero](#s03-aero) / [S03/graphics](#s03-graphics) | U glass / M tint [S03/glass](#s03-glass) | R [S03/other](#s03-other) |
| Grand Sport | convertible | 2LT | 01 | U (10) [S02/paint](#s02-paint) | U [S02/foundation](#s02-foundation) | U [S02/rear](#s02-rear) | R [S02/aero](#s02-aero) / [S02/graphics](#s02-graphics) | U glass / M tint [S02/glass](#s02-glass) | R [S02/other](#s02-other) |
| Grand Sport | convertible | 2LT | 02 | R (view); U (10 source) [S03/paint](#s03-paint) | U [S03/foundation](#s03-foundation) | R (view) [S03/rear](#s03-rear) | R [S03/aero](#s03-aero) / [S03/graphics](#s03-graphics) | U glass / M tint [S03/glass](#s03-glass) | R [S03/other](#s03-other) |
| Grand Sport | convertible | 3LT | 01 | B (10) [S02/paint](#s02-paint) | B [S02/foundation](#s02-foundation) | B (listed), U (others) [S02/rear](#s02-rear) | R [S02/aero](#s02-aero) / [S02/graphics](#s02-graphics) | U glass / M tint [S02/glass](#s02-glass) | R [S02/other](#s02-other) |
| Grand Sport | convertible | 3LT | 02 | R (view); U (10 source) [S03/paint](#s03-paint) | U [S03/foundation](#s03-foundation) | R (view) [S03/rear](#s03-rear) | R [S03/aero](#s03-aero) / [S03/graphics](#s03-graphics) | U glass / M tint [S03/glass](#s03-glass) | R [S03/other](#s03-other) |
| Grand Sport X | coupe | 1LT | 01 | U (10)† [S01/paint](#s01-paint) | U† [S01/foundation](#s01-foundation) | U† [S01/rear](#s01-rear) | R† [S01/aero](#s01-aero) / [S01/graphics](#s01-graphics) | U glass / M tint† [S01/glass](#s01-glass) | R† [S01/other](#s01-other) |
| Grand Sport X | coupe | 1LT | 02 | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table |
| Grand Sport X | coupe | 2LT | 01 | U (10)† [S01/paint](#s01-paint) | U† [S01/foundation](#s01-foundation) | U† [S01/rear](#s01-rear) | R† [S01/aero](#s01-aero) / [S01/graphics](#s01-graphics) | U glass / M tint† [S01/glass](#s01-glass) | R† [S01/other](#s01-other) |
| Grand Sport X | coupe | 2LT | 02 | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table |
| Grand Sport X | coupe | 3LT | 01 | U (10)† [S01/paint](#s01-paint) | U† [S01/foundation](#s01-foundation) | U† [S01/rear](#s01-rear) | R† [S01/aero](#s01-aero) / [S01/graphics](#s01-graphics) | U glass / M tint† [S01/glass](#s01-glass) | R† [S01/other](#s01-other) |
| Grand Sport X | coupe | 3LT | 02 | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table |
| Grand Sport X | convertible | 1LT | 01 | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table |
| Grand Sport X | convertible | 1LT | 02 | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table |
| Grand Sport X | convertible | 2LT | 01 | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table |
| Grand Sport X | convertible | 2LT | 02 | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table |
| Grand Sport X | convertible | 3LT | 01 | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table |
| Grand Sport X | convertible | 3LT | 02 | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table | M — PSB/layer absent; grand_sport_x option table |
| Z06 | coupe | 1LZ | 01 | U (10) [S13/paint](#s13-paint) | U [S13/foundation](#s13-foundation) | U [S13/rear](#s13-rear) | R [S13/aero](#s13-aero) / [S13/graphics](#s13-graphics) | U glass / M tint [S13/glass](#s13-glass) | R [S13/other](#s13-other) |
| Z06 | coupe | 1LZ | 02 | R (view); U (10 source) [S14/paint](#s14-paint) | U [S14/foundation](#s14-foundation) | R (view) [S14/rear](#s14-rear) | R [S14/aero](#s14-aero) / [S14/graphics](#s14-graphics) | U glass / M tint [S14/glass](#s14-glass) | R [S14/other](#s14-other) |
| Z06 | coupe | 2LZ | 01 | U (10) [S13/paint](#s13-paint) | U [S13/foundation](#s13-foundation) | U [S13/rear](#s13-rear) | R [S13/aero](#s13-aero) / [S13/graphics](#s13-graphics) | U glass / M tint [S13/glass](#s13-glass) | R [S13/other](#s13-other) |
| Z06 | coupe | 2LZ | 02 | R (view); U (10 source) [S14/paint](#s14-paint) | U [S14/foundation](#s14-foundation) | R (view) [S14/rear](#s14-rear) | R [S14/aero](#s14-aero) / [S14/graphics](#s14-graphics) | U glass / M tint [S14/glass](#s14-glass) | R [S14/other](#s14-other) |
| Z06 | coupe | 3LZ | 01 | B (10) [S13/paint](#s13-paint) | B [S13/foundation](#s13-foundation) | B (listed), U (others) [S13/rear](#s13-rear) | R [S13/aero](#s13-aero) / [S13/graphics](#s13-graphics) | U glass / M tint [S13/glass](#s13-glass) | R [S13/other](#s13-other) |
| Z06 | coupe | 3LZ | 02 | R (view); U (10 source) [S14/paint](#s14-paint) | U [S14/foundation](#s14-foundation) | R (view) [S14/rear](#s14-rear) | R [S14/aero](#s14-aero) / [S14/graphics](#s14-graphics) | U glass / M tint [S14/glass](#s14-glass) | R [S14/other](#s14-other) |
| Z06 | convertible | 1LZ | 01 | U (10) [S11/paint](#s11-paint) | U [S11/foundation](#s11-foundation) | U [S11/rear](#s11-rear) | R [S11/aero](#s11-aero) / [S11/graphics](#s11-graphics) | U glass / M tint [S11/glass](#s11-glass) | R [S11/other](#s11-other) |
| Z06 | convertible | 1LZ | 02 | R (view); U (10 source) [S12/paint](#s12-paint) | U [S12/foundation](#s12-foundation) | R (view) [S12/rear](#s12-rear) | R [S12/aero](#s12-aero) / [S12/graphics](#s12-graphics) | U glass / M tint [S12/glass](#s12-glass) | R [S12/other](#s12-other) |
| Z06 | convertible | 2LZ | 01 | U (10) [S11/paint](#s11-paint) | U [S11/foundation](#s11-foundation) | U [S11/rear](#s11-rear) | R [S11/aero](#s11-aero) / [S11/graphics](#s11-graphics) | U glass / M tint [S11/glass](#s11-glass) | R [S11/other](#s11-other) |
| Z06 | convertible | 2LZ | 02 | R (view); U (10 source) [S12/paint](#s12-paint) | U [S12/foundation](#s12-foundation) | R (view) [S12/rear](#s12-rear) | R [S12/aero](#s12-aero) / [S12/graphics](#s12-graphics) | U glass / M tint [S12/glass](#s12-glass) | R [S12/other](#s12-other) |
| Z06 | convertible | 3LZ | 01 | B (10) [S11/paint](#s11-paint) | B [S11/foundation](#s11-foundation) | B (listed), U (others) [S11/rear](#s11-rear) | R [S11/aero](#s11-aero) / [S11/graphics](#s11-graphics) | U glass / M tint [S11/glass](#s11-glass) | R [S11/other](#s11-other) |
| Z06 | convertible | 3LZ | 02 | R (view); U (10 source) [S12/paint](#s12-paint) | U [S12/foundation](#s12-foundation) | R (view) [S12/rear](#s12-rear) | R [S12/aero](#s12-aero) / [S12/graphics](#s12-graphics) | U glass / M tint [S12/glass](#s12-glass) | R [S12/other](#s12-other) |
| ZR1 | coupe | 1LZ | 01 | U (10) [S17/paint](#s17-paint) | U [S17/foundation](#s17-foundation) | U [S17/rear](#s17-rear) | R [S17/aero](#s17-aero) / [S17/graphics](#s17-graphics) | U glass / M tint [S17/glass](#s17-glass) | R [S17/other](#s17-other) |
| ZR1 | coupe | 1LZ | 02 | R (view); U (10 source) [S18/paint](#s18-paint) | U [S18/foundation](#s18-foundation) | R (view) [S18/rear](#s18-rear) | R [S18/aero](#s18-aero) / [S18/graphics](#s18-graphics) | U glass / M tint [S18/glass](#s18-glass) | R [S18/other](#s18-other) |
| ZR1 | coupe | 3LZ | 01 | B (10) [S17/paint](#s17-paint) | B [S17/foundation](#s17-foundation) | B (listed), U (others) [S17/rear](#s17-rear) | R [S17/aero](#s17-aero) / [S17/graphics](#s17-graphics) | U glass / M tint [S17/glass](#s17-glass) | R [S17/other](#s17-other) |
| ZR1 | coupe | 3LZ | 02 | R (view); U (10 source) [S18/paint](#s18-paint) | U [S18/foundation](#s18-foundation) | R (view) [S18/rear](#s18-rear) | R [S18/aero](#s18-aero) / [S18/graphics](#s18-graphics) | U glass / M tint [S18/glass](#s18-glass) | R [S18/other](#s18-other) |
| ZR1 | convertible | 1LZ | 01 | U (10) [S15/paint](#s15-paint) | U [S15/foundation](#s15-foundation) | U [S15/rear](#s15-rear) | R [S15/aero](#s15-aero) / [S15/graphics](#s15-graphics) | U glass / M tint [S15/glass](#s15-glass) | R [S15/other](#s15-other) |
| ZR1 | convertible | 1LZ | 02 | R (view); U (10 source) [S16/paint](#s16-paint) | U [S16/foundation](#s16-foundation) | R (view) [S16/rear](#s16-rear) | R [S16/aero](#s16-aero) / [S16/graphics](#s16-graphics) | U glass / M tint [S16/glass](#s16-glass) | R [S16/other](#s16-other) |
| ZR1 | convertible | 3LZ | 01 | B (10) [S15/paint](#s15-paint) | B [S15/foundation](#s15-foundation) | B (listed), U (others) [S15/rear](#s15-rear) | R [S15/aero](#s15-aero) / [S15/graphics](#s15-graphics) | U glass / M tint [S15/glass](#s15-glass) | R [S15/other](#s15-other) |
| ZR1 | convertible | 3LZ | 02 | R (view); U (10 source) [S16/paint](#s16-paint) | U [S16/foundation](#s16-foundation) | R (view) [S16/rear](#s16-rear) | R [S16/aero](#s16-aero) / [S16/graphics](#s16-graphics) | U glass / M tint [S16/glass](#s16-glass) | R [S16/other](#s16-other) |
| ZR1X | coupe | 1LZ | 01 | U (10)† [S21/paint](#s21-paint) | U† [S21/foundation](#s21-foundation) | U† [S21/rear](#s21-rear) | R† [S21/aero](#s21-aero) / [S21/graphics](#s21-graphics) | U glass / M tint† [S21/glass](#s21-glass) | R† [S21/other](#s21-other) |
| ZR1X | coupe | 1LZ | 02 | R (view); U (10 source) [S22/paint](#s22-paint) | U [S22/foundation](#s22-foundation) | R (view) [S22/rear](#s22-rear) | R [S22/aero](#s22-aero) / [S22/graphics](#s22-graphics) | U glass / M tint [S22/glass](#s22-glass) | R [S22/other](#s22-other) |
| ZR1X | coupe | 3LZ | 01 | B (10)† [S21/paint](#s21-paint) | B† [S21/foundation](#s21-foundation) | B (listed), U (others)† [S21/rear](#s21-rear) | R† [S21/aero](#s21-aero) / [S21/graphics](#s21-graphics) | U glass / M tint† [S21/glass](#s21-glass) | R† [S21/other](#s21-other) |
| ZR1X | coupe | 3LZ | 02 | R (view); U (10 source) [S22/paint](#s22-paint) | U [S22/foundation](#s22-foundation) | R (view) [S22/rear](#s22-rear) | R [S22/aero](#s22-aero) / [S22/graphics](#s22-graphics) | U glass / M tint [S22/glass](#s22-glass) | R [S22/other](#s22-other) |
| ZR1X | convertible | 1LZ | 01 | U (10) [S19/paint](#s19-paint) | U [S19/foundation](#s19-foundation) | U [S19/rear](#s19-rear) | R [S19/aero](#s19-aero) / [S19/graphics](#s19-graphics) | U glass / M tint [S19/glass](#s19-glass) | R [S19/other](#s19-other) |
| ZR1X | convertible | 1LZ | 02 | R (view); U (10 source) [S20/paint](#s20-paint) | U [S20/foundation](#s20-foundation) | R (view) [S20/rear](#s20-rear) | R [S20/aero](#s20-aero) / [S20/graphics](#s20-graphics) | U glass / M tint [S20/glass](#s20-glass) | R [S20/other](#s20-other) |
| ZR1X | convertible | 3LZ | 01 | B (10) [S19/paint](#s19-paint) | B [S19/foundation](#s19-foundation) | B (listed), U (others) [S19/rear](#s19-rear) | R [S19/aero](#s19-aero) / [S19/graphics](#s19-graphics) | U glass / M tint [S19/glass](#s19-glass) | R [S19/other](#s19-other) |
| ZR1X | convertible | 3LZ | 02 | R (view); U (10 source) [S20/paint](#s20-paint) | U [S20/foundation](#s20-foundation) | R (view) [S20/rear](#s20-rear) | R [S20/aero](#s20-aero) / [S20/graphics](#s20-graphics) | U glass / M tint [S20/glass](#s20-glass) | R [S20/other](#s20-other) |
| ZR1 | coupe | 2LZ | 01 | — not offered | — not offered | — not offered | — not offered | — not offered | — not offered |
| ZR1 | coupe | 2LZ | 02 | — not offered | — not offered | — not offered | — not offered | — not offered | — not offered |
| ZR1 | convertible | 2LZ | 01 | — not offered | — not offered | — not offered | — not offered | — not offered | — not offered |
| ZR1 | convertible | 2LZ | 02 | — not offered | — not offered | — not offered | — not offered | — not offered | — not offered |
| ZR1X | coupe | 2LZ | 01 | — not offered | — not offered | — not offered | — not offered | — not offered | — not offered |
| ZR1X | coupe | 2LZ | 02 | — not offered | — not offered | — not offered | — not offered | — not offered | — not offered |
| ZR1X | convertible | 2LZ | 01 | — not offered | — not offered | — not offered | — not offered | — not offered | — not offered |
| ZR1X | convertible | 2LZ | 02 | — not offered | — not offered | — not offered | — not offered | — not offered | — not offered |

**‡ S04 dependency:** every marked cell is assessed in the [S04/S05 component disposition](#s04-versus-s05-cleanup-disposition); S05-only graphics, glass and other equipment must not be advertised as complete S04 coverage.

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

S21 current SHA-256 `cbc0e678ff44087fb02f3722d783c425653708bdb9ada99a207d15a50a5f2de7` differs from bound proof `3f3096a92f2373a80e45f4b88c96bf52d74572f5d6473c273dd40bc054d28b08`. Current XMP `ModifyDate` records September 25, 14:44:48 −04:00. Compared with its pinned `reference.state.json`, current S21 has 1,055 native layers versus 1,063: IDs 161/166 (Mirrors), 243 (License_Plate), 257 (Multimedia), 779 (IP), 939 (Radio), 1038 (Stripes), and 1124 (Wheels) are absent; no new or renamed IDs were found. Badge visibility changed from `Badges / S0498` #15 to `Badges / S0499` #14. These are observed structural/visibility differences, not a claim that all remaining pixels are unchanged. The pinned proof, S23 and S21 are comparison evidence only; **no regeneration baseline is selected by this audit**. The other nine bound-source hashes match their original proofs.

**S23 is the earlier saved ZR1X coupe copy**, `zr1x/exterior/27CHCOZR_X_COU_Studio_f02 copy.psb`, SHA-256 `88183628a57af8896802f765347d79492f08ff67bda84ac0d77e834bbe177747`. Its saved XMP ModifyDate is **September 25, 12:33:21 −04:00**, before S21’s 14:44:48 save. Native comparison against `W/asset-proofs/2026-09-20-zr1x-coupe-f02/reference.state.json` (captured September 20, 22:15:02Z): all **1,063 IDs, names, paths, traversal order and visibility flags match**. That state file has no explicit parent-ID or sibling-index fields; its serialized traversal order matches S23, and S23’s native parent/sibling fields are retained in JSON.

Compared with S23, S21 removes the same eight IDs listed above, keeps every remaining name/path/parent and relative order, changes 66 root sibling indices solely because preceding groups were removed, and flips only #14/#15 visibility. Thus **the observed structural/order/visibility drift is absent in S23 and present in S21**. S23’s hash matches neither the pinned proof nor S21: layer-tree equivalence does not establish equal pixels, masks, effects or saved bytes. This records the versions’ positions without choosing a regeneration baseline. Exact comparison records are in JSON `comparisons.pinned_reference_to_S23` and `comparisons.S23_to_S21`.


## S04 versus S05 cleanup disposition

S04 is the existing bound “cleaned” Grand Sport coupe view-01 source: **1,400 native records**, versus **1,624 in S05**. It removes exactly **224 IDs**, adds none, and retains the names, paths and relative traversal order of shared layers. Shared visibility is not identical: 20 flags changed, recorded in JSON `comparisons.S05_to_S04.visibility_changes`; 278 sibling indices shifted after removals without changing shared relative order. Remaining pixel equivalence is untested. The full deletion set is `comparisons.S05_to_S04.removed_layers` in the JSON; the grouped list below includes each removed ID exactly once, including empty root groups. Generic `None` names stay **unmapped/other**, even when adjacent to a spoiler; their names do not establish an option or physical component.

All dispositions below apply separately to **Grand Sport / coupe / 1LT, 2LT and 3LT / view 01**. The 3LT bound S04 proof remains frozen and unchanged. S05-only future components require a fresh S05-native recipe/reference and complete composition qualification; they must not be overlaid onto the S04 proof by assumption. Opaque tint removes the need to recover deleted cabin trim variants for exterior scenes, but does not remove exterior glass, graphic, mirror or wheel requirements.

| S04 matrix cell / component | Removed native records | S05-only need and future recipe source |
| --- | --- | --- |
| paint | 0 | No S05-only base or component paint peer was removed. S04 retains all ten; retain S04 for this component. |
| trim/foundation | 0 | No Base/S0507 trim or body foundation removed. S04 has 1LT/2LT/3LT. Deleted cabin variants are intentionally hidden by tint; retain S04 trim foundations, with the complete-scene tint gate below. |
| rear | 0 dedicated Spoiler | No dedicated Spoiler group/child removed. S04 retains T0F/5ZV/S0267/S0268/SIG/5V5 candidates. Unmapped None/S0119 #1532 and D58 #1538 are listed under other, not presumed rear identities; use S05 if their later identification requires them. |
| aero | 0 | No dedicated Front_Fascia/Ground_Effects/Rear_Fascia/Hood layer removed. S04 suffices for retained native candidates; package identity/stack qualification still required. |
| graphics/stripes | 6 | **S05 required** for Decals #1567/#1568/#1573/#1574/#1575 (S0320_B/S0315_B/S0349_B/S0342_B/S0314_B) and empty Stripes #1569. Their catalog identities remain unmapped; S04 cannot claim those source branches. |
| glass / tint | 1 | **S05 required** for Windows #1606 / S0101_B #1608. S04 retains S0101_R #1609 only in that group. Qualify complete opaque tint on S05; do not change or silently replace bound S04 proof. |
| other choices | 42 (27 other + 15 wheels/brakes) | **S05 required** whenever the recipe needs the removed mirror, badges, wheel/cap/brake, engine, hook or anonymous equipment candidates listed below. Empty removed groups alone do not prove missing visible pixels. Retained exterior DWK/DYX peers still exist in S04. |
| interior (not a matrix selector) | 175 | Source-only S05 cabin choices are retained in JSON for provenance. Tint intentionally suppresses visible interiors, so these do not block exterior lower-trim coverage. |

### Removed native layers, grouped by component

Parent IDs distinguish repeated names; `(root)` means no parent. Counts include groups and children. Paint, trim/foundation, dedicated rear Spoiler and dedicated aero each have **zero** removals.

**graphics/stripes — 6 records**

| Parent path / ID | Removed child name / ID (native order) |
| --- | --- |
| `Decals` #1560 | `S0320_B` #1567; `S0315_B` #1568 |
| `(root)` | `Stripes` #1569 |
| `Decals` #1571 | `S0349_B` #1573; `S0342_B` #1574; `S0314_B` #1575 |

**glass — 1 record**

| Parent path / ID | Removed child name / ID (native order) |
| --- | --- |
| `Windows` #1606 | `S0101_B` #1608 |

**wheels/brakes — 15 records**

| Parent path / ID | Removed child name / ID (native order) |
| --- | --- |
| `(root)` | `Wheels` #1633; `Brakes` #1645; `Brakes` #1686 |
| `Wheels` #1633 | `S0455_RR` #1635; `S0465_RR` #1636; `S0447_RR` #1637; `S0446_RR` #1638; `S0440_RR` #1639; `S0427_RR` #1640 |
| `Wheel_Caps` #1641 | `S0825_RR` #1644 |
| `Brakes` #1645 | `S0299_RR` #1647 |
| `Wheel_Caps` #1679 | `S0419_FR` #1681; `S0824_FR` #1683; `S0826_FR` #1684; `S0827_FR` #1685 |

**interior — 175 records**

| Parent path / ID | Removed child name / ID (native order) |
| --- | --- |
| `(root)` | `Multimedia` #440; `IP` #1197; `Radio` #1433 |
| `Stitching` #529 | `S0527_L` #532; `S0632_L` #539; `S0634_R` #545; `S0634_M` #546; `S0634_L` #547; `S0525` #548 |
| `Steering_Wheel` #550 | `S0540&HUV` #552; `S0540&HU7` #553; `S0540&HUL` #554; `S0540&HUK` #556; `S0540&HU6` #557; `S0540&HUU` #570; `S0540&HUE` #572; `S0540&HZN` #574; `S0540&HU0` #576; `S0540&HXO` #577; `S0540&HUW` #579; `S0540&HVZ` #580; `S0540&H8T` #581; `S0540&EPX` #583; `S0540&EJH` #584; `S0540&HAG` #585; `S0540&HTA` #587; `S0540&HTJ` #588; `S0540&HUP` #589; `S0540&HUQ` #590; `S0540&HTM` #591; `S0547&HU7` #595; `S0547&HUL` #596; `S0547&H1Y` #599; `S0547&HTE` #600; `S0547&HVV` #602; `S0547&HU1` #603; `S0547&HU9` #605; `S0547&HVT` #606; `S0547&HUA` #607; `S0547&HU2` #608; `S0547&HTG` #612; `S0547&HZN` #613; `S0547&HUW` #617; `S0547&HUX` #618; `S0547&H8T` #620; `S0547&HUB` #621; `S0547&HUC` #622; `S0547&EPX` #623; `S0547&HAG` #625; `S0547&HUP` #628 |
| `Interior` #633 | `S0530_L&HTE` #637; `S0530_L&HVV` #638; `S0530_L&HZB` #641; `S0530_L&HVT` #642; `S0530_L&HU2` #644; `S0530_L&HUU` #645; `S0530_L&HUE` #647; `S0530_L&HXO` #652; `S0530_L&HUW` #654; `S0530_L&H8T` #657; `S0530_L&HUB` #658; `S0530_L&EPX` #660; `S0530_M&HTT` #664; `S0530_M&HU1` #666; `S0530_M&HMO` #667; `S0530_M&HU9` #668; `S0530_M&HU2` #671; `S0530_M&HZP` #673; `S0530_M&HUE` #674; `S0530_M&HTG` #675; `S0530_M&HXO` #678; `S0530_M&HNK` #679; `S0530_M&HUW` #680; `S0530_M&HUX` #681; `S0530_M&HUB` #684; `S0530_M&EPX` #685; `S0530_M&EJH` #686; `S0530_M&EL9` #688 |
| `Interior_Kit` #689 | `S0551_R&HUR` #694; `S0551_R&HUN` #696; `S0551_R&H1Y` #698; `S0551_R&HTE` #699; `S0551_R&HVV` #701; `S0551_R&HMO` #703; `S0551_R&HU9` #704; `S0551_R&HZB` #705; `S0551_R&HVT` #706; `S0551_R&HUA` #707; `S0551_R&HU2` #708; `S0551_R&HZP` #710; `S0551_R&HTG` #712; `S0551_R&HZN` #713; `S0551_R&HUF` #714; `S0551_R&HXO` #716; `S0551_R&HUX` #719; `S0551_R&EPX` #724; `S0551_R&HAG` #726; `S0551_R&EL9` #727; `S0551_R&HTA` #728 |
| `Interior_Kit` #763 | `S0551_M&HUV` #765; `S0551_M&HUL` #766; `S0551_M&HUR` #767; `S0551_M&HTP` #771; `S0551_M&H1Y` #772; `S0551_M&HTE` #773; `S0551_M&HTT` #774; `S0551_M&HU1` #776; `S0551_M&HMO` #777; `S0551_M&HU9` #778; `S0551_M&HVT` #780; `S0551_M&HU2` #782; `S0551_M&HUE` #785; `S0551_M&HTG` #786; `S0551_M&HZN` #787; `S0551_M&HUX` #792; `S0551_M&HVZ` #793; `S0551_M&EPX` #796; `S0551_M&HAG` #798; `S0551_M&HTA` #800; `S0551_M&HTM` #801; `S0551_M&HTQ` #802; `S0551_L&HUL` #806; `S0551_L&HUK` #808; `S0551_L&HU6` #809; `S0551_L&HUN` #810; `S0551_L&H1Y` #812; `S0551_L&HU1` #816; `S0551_L&HMO` #817; `S0551_L&HVT` #820; `S0551_L&HUA` #821; `S0551_L&HU2` #822; `S0551_L&HUU` #823; `S0551_L&HZP` #824; `S0551_L&HUW` #832; `S0551_L&HUX` #833; `S0551_L&HVZ` #834; `S0551_L&HAG` #840; `S0551_L&HTQ` #842 |
| `Seats_Front` #906 | `AQ9&HU6` #1041 |
| `Floors` #1076 | `VYW&HU7` #1079; `VYW&HTP` #1083; `VYW&HTE` #1085; `VYW&HTT` #1086; `VYW&HMO` #1088; `VYW&HU9` #1089; `VYW&HZB` #1090; `VYW&HVT` #1091; `VYW&HU2` #1092; `VYW&HUE` #1094; `VYW&HNK` #1099; `VYW&HUX` #1100; `VYW&HVZ` #1101; `VYW&H8T` #1102; `VYW&HAG` #1107; `VYW&EL9` #1108; `VYW&HTA` #1109; `VYW&HTJ` #1110; `VYW&HUQ` #1111; `RIA` #1114 |
| `IP` #1197 | `S0550` #1199 |
| `Steering_Wheel` #1694 | `S0539&HTT` #1697; `S0539&HU9` #1701; `S0539&HZB` #1702; `S0539&HVT` #1703; `S0539&HZN` #1709; `S0539&HUF` #1710; `S0539&HU0` #1711; `S0539&HUW` #1714; `S0539&HUB` #1718; `S0539&EJH` #1720; `S0539&HAG` #1721; `S0539&EL9` #1722 |
| `Console` #1723 | `S0578` #1726; `S0575` #1728; `S0574` #1729 |

**other — 27 records**

| Parent path / ID | Removed child name / ID (native order) |
| --- | --- |
| `Badges` #11 | `EYK_B` #16; `S0276` #18 |
| `(root)` | `Mirrors` #317; `Mirrors` #322; `None` #363; `None` #409; `None` #418; `License_Plate` #424; `None` #1500; `None` #1512; `None` #1530; `None` #1536; `Engine` #1542; `Tow_Hooks` #1556 |
| `Mirrors` #322 | `UFT_L` #324 |
| `None` #363 | `S0345` #365 |
| `None` #409 | `S0420` #411 |
| `None` #418 | `VSN` #420 |
| `License_Plate` #424 | `S0235` #426 |
| `Badges` #1192 | `S0500` #1196 |
| `None` #1500 | `S0343` #1502 |
| `None` #1512 | `S0357` #1514 |
| `None` #1530 | `S0119` #1532 |
| `None` #1536 | `D58` #1538 |
| `Engine` #1547 | `S0111` #1549 |
| `Tow_Hooks` #1556 | `S0870` #1558; `S0871` #1559 |

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
| Glass/tint | U glass / M authored tint: fixed owner treatment, with several native depth intervals. | Qualify opaque masks below retained reflections and above cabin; bake into native scene planes. No catalog tint option or independently selectable tint plane is proposed. |
| Second view | R even for existing paint/wing types. | Explicit view identity/selection plus separately qualified recipes; overlapping scopes are rejected today. |

### Owner tint decision — October 9, 2026

Exterior scenes must **not show the cabin**. Every windshield, side window, rear/hatch window, quarter/van window and transparent roof where present receives opaque near-black **`#0b0b0c`, 100% opacity, Normal blend**. The fill must sit above all cabin/interior content within each aperture and below the glass reflection and defroster content. Existing reflection layers stay visible on top. This identical recipe applies to every model/body/trim/paint/view; only the masks and native placement vary with the source geometry. It is a visual simplification, **not a catalog option and not Solar-Ray glass**. Visible-interior trim differences are intentionally not depicted. Exterior trim foundations, mirrors and other exterior equipment still require their correct trim-specific state.

**Placement rule:** for each listed glass/transparent-roof branch, retain reflection/defroster pixels on top and put the aperture-masked opaque fill immediately behind that content, above any cabin pixels seen through the aperture. Several source reflection candidates already lie below cabin roots in the global stack. In those cases a single insertion cannot meet both requirements: future qualification must separate/reposition the masked reflection, tint and occluder pieces by surface; do not simply add one full-canvas top layer or hide reflections. Every source below is split across depth intervals. This is native recipe work that can be baked into the fixed paint back/foreground assemblies; it does not itself require a selectable runtime tint plane.

The inventory identifies candidate glass layers, not pixel masks or anatomy proven from S-code names. S0101_L/R/B, S0104/5/8/122 and Rear_Van_Windows must all be checked for the actual openings; opaque roof/paint alternatives are not to be tinted as glass. CC3 (and source CF8 alternatives, despite current factory-unavailable lifecycle) are transparent-roof candidates where present. If reflections/transmission share a raster leaf, preserve the reflection pixels and create a separate mask in a later task. No tint layer has been authored in this revision; matrix M tint means that missing authored treatment, not absent glass artwork.

The following table gives **every source’s cover targets and insertion constraints**. `#ID @root-index` locates a glass group; child IDs in parentheses are the exact native surface/reflection candidates to preserve above the tint. The detailed names and full paths are in JSON `sources.Sxx.tint.intervals`, with all cabin roots/children to occlude in `tint.cabin_root_ids` / `tint.occlude_cabin_layer_ids`. D01/D02 inherit S09/S05 exactly.

| Source | Glass/roof candidates and retained reflection/defroster targets | Native tint placement / gap |
| --- | --- | --- |
| S01 | `Windows` #332 @30 (#334); `Windows` #347 @32 (#349); `Windows` #415 @38 (#417); `Roof` #442 @41 (#475, #476, #477, #478, #479, #480, #481, #482, #483, #484, #485); `Windows` #1483 @62 (#1485, #1486); `Defroster` #1487 @63 (#1489); `Windows` #1606 @74 (#1609) | **Split — one plane unqualified.** Above-cabin boundary @42; roots #1483, #1487, #1606 are at/below it and need masked reflection/tint separation.  |
| S02 | `Windows` #349 @35 (#351); `Windows` #365 @37 (#367); `Windows` #1495 @73 (#1497); `Defroster` #1498 @74 (#1500); `Windows` #1636 @95 (#1638, #1639) | **Split — one plane unqualified.** Above-cabin boundary @51; roots #1495, #1498, #1636 are at/below it and need masked reflection/tint separation.  |
| S03 | `Windows` #436 @45 (#438, #439); `Defroster` #710 @56 (#712); `Windows` #713 @57 (#715); `Windows` #1662 @90 (#1664); `Windows` #1681 @93 (#1683) | **Split — one plane unqualified.** Above-cabin boundary @29; roots #436, #710, #713, #1662, #1681 are at/below it and need masked reflection/tint separation.  |
| S04 | `Windows` #332 @29 (#334); `Windows` #347 @31 (#349); `Windows` #415 @37 (#417); `Roof` #442 @40 (#475, #476, #477, #478, #479, #480, #481, #482, #483, #484, #485); `Windows` #1483 @61 (#1485, #1486); `Defroster` #1487 @62 (#1489); `Windows` #1606 @74 (#1609) | **Split — one plane unqualified.** Above-cabin boundary @41; roots #1483, #1487, #1606 are at/below it and need masked reflection/tint separation. **S05 required** for removed S0101_B #1608. |
| S05 | `Windows` #332 @31 (#334); `Windows` #347 @33 (#349); `Windows` #415 @41 (#417); `Roof` #442 @47 (#475, #476, #477, #478, #479, #480, #481, #482, #483, #484, #485); `Windows` #1483 @70 (#1485, #1486); `Defroster` #1487 @71 (#1489); `Windows` #1606 @90 (#1608, #1609) | **Split — one plane unqualified.** Above-cabin boundary @48; roots #1483, #1487, #1606 are at/below it and need masked reflection/tint separation.  |
| S06 | `Windows` #376 @38 (#378, #379, #380); `Roof` #594 @48 (#627, #628, #629, #630, #631, #632, #633, #634, #635, #636, #637); `Defroster` #681 @49 (#683); `Windows` #684 @50 (#686); `Windows` #702 @53 (#704); `Windows` #1621 @84 (#1623); `Windows` #1640 @87 (#1642) | **Split — one plane unqualified.** Above-cabin boundary @22; roots #376, #594, #681, #684, #702, #1621, #1640 are at/below it and need masked reflection/tint separation.  |
| S07 | `Windows` #307 @35 (#309); `Windows` #323 @37 (#325); `Windows` #1372 @73 (#1374); `Defroster` #1375 @74 (#1377); `Windows` #1537 @92 (#1539, #1540) | **Split — one plane unqualified.** Above-cabin boundary @51; roots #1372, #1375, #1537 are at/below it and need masked reflection/tint separation.  |
| S08 | `Windows` #458 @46 (#460, #461); `Defroster` #646 @55 (#648); `Windows` #649 @56 (#651); `Windows` #1539 @87 (#1541); `Windows` #1558 @90 (#1560) | **Split — one plane unqualified.** Above-cabin boundary @26; roots #458, #646, #649, #1539, #1558 are at/below it and need masked reflection/tint separation.  |
| S09 | `Windows` #288 @30 (#290); `Windows` #303 @32 (#305); `Windows` #336 @39 (#338); `Roof` #375 @45 (#408, #409, #410, #411, #412, #413, #414, #415, #416, #417, #418); `Windows` #1364 @68 (#1366, #1367); `Defroster` #1368 @69 (#1370); `Windows` #1502 @85 (#1504) | **Split — one plane unqualified.** Above-cabin boundary @44; roots #375, #1364, #1368, #1502 are at/below it and need masked reflection/tint separation.  |
| S10 | `Windows` #389 @39 (#391, #392); `Roof` #524 @47 (#557, #558, #559, #560, #561, #562, #563, #564, #565, #566, #567); `Defroster` #610 @48 (#612); `Windows` #613 @49 (#615); `Windows` #631 @52 (#633); `Windows` #1474 @81 (#1476); `Windows` #1493 @84 (#1495) | **Split — one plane unqualified.** Above-cabin boundary @20; roots #389, #524, #610, #613, #631, #1474, #1493 are at/below it and need masked reflection/tint separation.  |
| S11 | `Windows` #347 @30 (#349); `Windows` #363 @32 (#365); `Windows` #1410 @70 (#1412); `Defroster` #1413 @71 (#1415); `Windows` #1540 @90 (#1542, #1543) | **Split — one plane unqualified.** Above-cabin boundary @44; roots #1410, #1413, #1540 are at/below it and need masked reflection/tint separation.  |
| S12 | `Windows` #426 @43 (#428, #429); `Defroster` #647 @53 (#649); `Windows` #650 @54 (#652); `Windows` #1550 @86 (#1552); `Windows` #1569 @89 (#1571) | **Split — one plane unqualified.** Above-cabin boundary @27; roots #426, #647, #650, #1550, #1569 are at/below it and need masked reflection/tint separation.  |
| S13 | `Windows` #325 @25 (#327); `Windows` #340 @27 (#342); `Windows` #378 @36 (#380); `Roof` #404 @41 (#437, #438, #439, #440, #441, #442, #443, #444, #445, #446, #447); `Windows` #1384 @65 (#1386, #1387); `Defroster` #1388 @66 (#1390); `Windows` #1489 @83 (#1491) | **Split — one plane unqualified.** Above-cabin boundary @42; roots #1384, #1388, #1489 are at/below it and need masked reflection/tint separation.  |
| S14 | `Windows` #357 @36 (#359, #360); `Roof` #522 @45 (#555, #556, #557, #558, #559, #560, #561, #562, #563, #564, #565); `Defroster` #608 @46 (#610); `Windows` #611 @47 (#613); `Windows` #629 @50 (#631); `Windows` #1473 @80 (#1475); `Windows` #1492 @83 (#1494) | **Split — one plane unqualified.** Above-cabin boundary @21; roots #357, #522, #608, #611, #629, #1473, #1492 are at/below it and need masked reflection/tint separation.  |
| S15 | `Windows` #212 @31 (#214); `Windows` #228 @33 (#230); `Windows` #984 @71 (#986); `Defroster` #987 @72 (#989); `Windows` #1090 @87 (#1092, #1093) | **Split — one plane unqualified.** Above-cabin boundary @48; roots #984, #987, #1090 are at/below it and need masked reflection/tint separation.  |
| S16 | `Windows` #301 @41 (#303, #304); `Defroster` #440 @52 (#442); `Windows` #443 @53 (#445); `Windows` #1120 @85 (#1122); `Windows` #1142 @89 (#1144) | **Split — one plane unqualified.** Above-cabin boundary @24; roots #301, #440, #443, #1120, #1142 are at/below it and need masked reflection/tint separation.  |
| S17 | `Windows` #190 @27 (#192); `Windows` #215 @29 (#217); `Windows` #253 @38 (#255); `Roof` #275 @43 (#299, #300, #301, #302, #303, #304, #305, #306, #307, #308); `Windows` #992 @67 (#994, #995); `Defroster` #996 @68 (#998); `Rear_Van_Windows` #1098 @81 (#1100, #1101, #1102, #1103, #1104, #1105, #1106, #1107, #1108, #1109, #1110); `Windows` #1111 @82 (#1113, #1114) | **Split — one plane unqualified.** Above-cabin boundary @44; roots #992, #996, #1098, #1111 are at/below it and need masked reflection/tint separation.  |
| S18 | `Rear_Van_Windows` #133 @15 (#135, #136, #137, #138, #139, #140, #141, #142, #143, #144, #145); `Windows` #294 @35 (#296, #297); `Roof` #401 @45 (#425, #426, #427, #428, #429, #430, #431, #432, #433, #434); `Defroster` #464 @46 (#466); `Windows` #467 @47 (#469); `Windows` #485 @50 (#487); `Windows` #1134 @80 (#1136); `Windows` #1156 @84 (#1158) | **Split — one plane unqualified.** Above-cabin boundary @19; roots #294, #401, #464, #467, #485, #1134, #1156 are at/below it and need masked reflection/tint separation.  |
| S19 | `Windows` #196 @32 (#198); `Windows` #212 @34 (#214); `Windows` #985 @72 (#987); `Defroster` #988 @73 (#990); `Windows` #1092 @88 (#1094, #1095) | **Split — one plane unqualified.** Above-cabin boundary @49; roots #985, #988, #1092 are at/below it and need masked reflection/tint separation.  |
| S20 | `Windows` #286 @42 (#288, #289); `Defroster` #425 @53 (#427); `Windows` #428 @54 (#430); `Windows` #1099 @86 (#1101); `Windows` #1121 @90 (#1123) | **Split — one plane unqualified.** Above-cabin boundary @25; roots #286, #425, #428, #1099, #1121 are at/below it and need masked reflection/tint separation.  |
| S21 | `Windows` #175 @25 (#177); `Windows` #200 @27 (#202); `Windows` #240 @36 (#242); `Roof` #262 @39 (#286, #287, #288, #289, #290, #291, #292, #293, #294, #295); `Windows` #975 @61 (#977, #978); `Defroster` #979 @62 (#981); `Rear_Van_Windows` #1085 @74 (#1087, #1088, #1089, #1090, #1091, #1092, #1093, #1094, #1095, #1096, #1097); `Windows` #1098 @75 (#1100) | **Split — one plane unqualified.** Above-cabin boundary @32; roots #240, #262, #975, #979, #1085, #1098 are at/below it and need masked reflection/tint separation.  |
| S22 | `Rear_Van_Windows` #137 @15 (#139, #140, #141, #142, #143, #144, #145, #146, #147, #148, #149); `Windows` #283 @35 (#285, #286); `Roof` #389 @45 (#413, #414, #415, #416, #417, #418, #419, #420, #421, #422); `Defroster` #452 @46 (#454); `Windows` #455 @47 (#457); `Windows` #473 @50 (#475); `Windows` #1111 @80 (#1113); `Windows` #1133 @84 (#1135) | **Split — one plane unqualified.** Above-cabin boundary @19; roots #283, #389, #452, #455, #473, #1111, #1133 are at/below it and need masked reflection/tint separation.  |
| S23 | `Windows` #175 @27 (#177); `Windows` #200 @29 (#202); `Windows` #240 @38 (#242); `Roof` #262 @43 (#286, #287, #288, #289, #290, #291, #292, #293, #294, #295); `Windows` #975 @67 (#977, #978); `Defroster` #979 @68 (#981); `Rear_Van_Windows` #1085 @81 (#1087, #1088, #1089, #1090, #1091, #1092, #1093, #1094, #1095, #1096, #1097); `Windows` #1098 @82 (#1100) | **Split — one plane unqualified.** Above-cabin boundary @34; roots #240, #262, #975, #979, #1085, #1098 are at/below it and need masked reflection/tint separation.  |

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

### Stingray T0A, TVS and ZF1 scope and source qualification

The same pinned R3 catalog was re-read for this revision. All three options are active and have available context rows for **coupe and convertible, 1LT/2LT/3LT**. Context availability is conditional: T0A (`opt_t0a_001`, Z51 Spoiler) is included and only available with Z51; TVS (`opt_tvs_001`, Low-Profile Rear Spoiler and Front Splitter) requires ZF1 if Z51 is selected; ZF1 (`opt_zf1_001`, Aero Delete) requires Z51 and removes its T0A rear spoiler **and front splitter**. ZF1 does not mean no rear spoiler when TVS is also selected. These facts come from model-owned `option`, `option_configuration` and `consumer_option` records (Stingray source rows 160/161/162), not layer labels.

**Confirmed catalog applicability is not confirmed artwork identity.** No native leaf explicitly identifies T0A or TVS. The existing Stingray family manifests expressly exclude S0117/S0116/S0118/S0114 as unconfirmed T0A/TVS/ZYC aliases. The catalog has no PSB-layer alias table. Accordingly **neither T0A nor TVS currently has a verified source-layer binding**; candidate geometry exists in both bodies/all four views, and no source selection can yet be assigned to a catalog trim. This is an identity-qualification hold, not proof the artwork is missing.

| View-01 source | Rear candidate layers (all remain unmapped) | Catalog body/trim scope and limit |
| --- | --- | --- |
| S07 convertible | Spoiler #1426: S0118 #1428, S0117 ten paints #1429–1438; Spoiler #1443: S0116 ten paints #1445–1454, S0114 #1466 | T0A/TVS available 1LT/2LT/3LT subject to rules; explicit source trim peers exist. No accepted alias-to-option mapping. |
| S09 coupe | Spoiler #1413: S0118 #1415, S0117 ten paints #1416–1425; Spoiler #1430: S0116 ten paints #1432–1441, S0114 #1453 | T0A/TVS available 1LT/2LT/3LT subject to rules; S09 lacks explicit 1LT foundation. No accepted alias-to-option mapping. |

Front-splitter candidates are separate Air_Dam/Front_Fascia branches at foreground depths (S07 Air_Dam #103/#274; S09 #84/#255), without a verified TVS alias. A TVS wing-only export **would misrepresent the option**, because its splitter is part of the named catalog option; TVS belongs with full aero (batch 6), not batch 2a. T0A can be reviewed as a rear-component preview in the existing three-plane contract once identified, but its Z51 context also has a splitter: a T0A rear proof must not be described as complete Z51 artwork. Independent selection of that splitter belongs with full aero; a fixed correct foreground can be qualified in a later component recipe without a renderer change.

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
| S23 | `zr1x/exterior/27CHCOZR_X_COU_Studio_f02 copy.psb` | 88183628a57af8896802f765347d79492f08ff67bda84ac0d77e834bbe177747 | 1063 | 4-way match |
| D01 | `stingray/c.coupe.exterior.01 copy.psb` | 16d97f2bc1fc980372be5a5d1e1f15332a899bb320e5dcb346478f0deeda1584 | 0 added; duplicate of S09 | 4-way match; not reinventoried |
| D02 | `grandsport/e.coupe.exterior.01.copy.psb` | 6f7c28bc216ea47915102f43f3e2388c3d263c7468d4a9a623e52375075ee86f | 0 added; duplicate of S05 | 4-way match; not reinventoried |

Register total: **23 distinct native inventories, 31,299 layers; 25 exterior PSB paths including two byte-identical duplicates**. The additional 20 PSBs under V are separate interior-camera scenes, outside this exterior task; their exact paths are dispositioned in JSON `out_of_scope_interior_files` (no native inventory or hash claim for those files). The complete V traversal therefore accounts for all 45 PSB paths. S23/D01/D02 disposable copies and new integrity evidence are under `/private/tmp/visualizer-review-20261009/`. Duplicate counts are zero additional records; their layers refer to S09/S05.

## Source component index

The complete [machine-readable native inventory](visualizer-asset-inventory.json) uses `sources.Sxx.components.<component>` for layer-ID lists and `sources.Sxx.native_layers` for exact names, paths, parent IDs, sibling order, visibility, catalog candidates and stack disposition. These short anchors are the matrix targets; JSON keys are lookup keys, not pretend browser anchors. `paint` overlaps component families where a paint token occurs. Catalog scope is keyed by the source’s model and option ID.

Native order is top-to-bottom; smaller index draws in front. Stack shorthand: **F** above all spoiler roots, **S** within their interval, **B** below all spoiler roots; **body+ / body= / body−** are above / at / below the paint-body root. Every old exterior ID, empty group, ordered ten-paint family and cabin-root ID is retained; JSON also includes every native cabin child. A paint token maps only paint, not numeric component geometry. Native existence does not qualify alpha, finish, anatomy, legal build or rendering.

### S01 — Grand Sport X coupe view 01

Source and hash: [register](#source-register-and-integrity); JSON key `sources.S01`. Paint-body root @73; spoiler roots @66, @67, @68. derived GSX candidate.

<a id="s01-paint"></a>
<a id="s01-foundation"></a>
<a id="s01-rear"></a>
<a id="s01-aero"></a>
<a id="s01-graphics"></a>
<a id="s01-glass"></a>
<a id="s01-other"></a>

| Component | Native records | JSON lookup |
| --- | --- | --- |
| paint | 171 | `sources.S01.components.paint` |
| foundation | 16 | `sources.S01.components.foundation` |
| rear | 18 | `sources.S01.components.rear` |
| aero | 93 | `sources.S01.components.aero` |
| graphics | 104 | `sources.S01.components.graphics` |
| glass | 13 | `sources.S01.components.glass` |
| other | 382 | `sources.S01.components.other` |

All exact parent paths, order, visibility and stack positions are in `native_layers`; cabin IDs and glass placement are in `tint`.

### S02 — Grand Sport convertible view 01

Source and hash: [register](#source-register-and-integrity); JSON key `sources.S02`. Paint-body root @94; spoiler roots @80, @82, @84. inventory source; not new binding.

<a id="s02-paint"></a>
<a id="s02-foundation"></a>
<a id="s02-rear"></a>
<a id="s02-aero"></a>
<a id="s02-graphics"></a>
<a id="s02-glass"></a>
<a id="s02-other"></a>

| Component | Native records | JSON lookup |
| --- | --- | --- |
| paint | 178 | `sources.S02.components.paint` |
| foundation | 16 | `sources.S02.components.foundation` |
| rear | 18 | `sources.S02.components.rear` |
| aero | 81 | `sources.S02.components.aero` |
| graphics | 101 | `sources.S02.components.graphics` |
| glass | 11 | `sources.S02.components.glass` |
| other | 464 | `sources.S02.components.other` |

All exact parent paths, order, visibility and stack positions are in `native_layers`; cabin IDs and glass placement are in `tint`.

### S03 — Grand Sport convertible view 02

Source and hash: [register](#source-register-and-integrity); JSON key `sources.S03`. Paint-body root @91; spoiler roots @7, @12, @14, @16. inventory source; not new binding.

<a id="s03-paint"></a>
<a id="s03-foundation"></a>
<a id="s03-rear"></a>
<a id="s03-aero"></a>
<a id="s03-graphics"></a>
<a id="s03-glass"></a>
<a id="s03-other"></a>

| Component | Native records | JSON lookup |
| --- | --- | --- |
| paint | 178 | `sources.S03.components.paint` |
| foundation | 16 | `sources.S03.components.foundation` |
| rear | 19 | `sources.S03.components.rear` |
| aero | 78 | `sources.S03.components.aero` |
| graphics | 103 | `sources.S03.components.graphics` |
| glass | 11 | `sources.S03.components.glass` |
| other | 466 | `sources.S03.components.other` |

All exact parent paths, order, visibility and stack positions are in `native_layers`; cabin IDs and glass placement are in `tint`.

### S04 — Grand Sport coupe view 01

Source and hash: [register](#source-register-and-integrity); JSON key `sources.S04`. Paint-body root @73; spoiler roots @65, @66, @67. inventory source; not new binding.

<a id="s04-paint"></a>
<a id="s04-foundation"></a>
<a id="s04-rear"></a>
<a id="s04-aero"></a>
<a id="s04-graphics"></a>
<a id="s04-glass"></a>
<a id="s04-other"></a>

| Component | Native records | JSON lookup |
| --- | --- | --- |
| paint | 160 | `sources.S04.components.paint` |
| foundation | 16 | `sources.S04.components.foundation` |
| rear | 18 | `sources.S04.components.rear` |
| aero | 81 | `sources.S04.components.aero` |
| graphics | 104 | `sources.S04.components.graphics` |
| glass | 13 | `sources.S04.components.glass` |
| other | 383 | `sources.S04.components.other` |

All exact parent paths, order, visibility and stack positions are in `native_layers`; cabin IDs and glass placement are in `tint`. S04 cell-specific S05 dependencies: [cleanup disposition](#s04-versus-s05-cleanup-disposition).

### S05 — Grand Sport coupe view 01

Source and hash: [register](#source-register-and-integrity); JSON key `sources.S05`. Paint-body root @89; spoiler roots @76, @78, @80. uncleaned comparison and required source for removed components.

<a id="s05-paint"></a>
<a id="s05-foundation"></a>
<a id="s05-rear"></a>
<a id="s05-aero"></a>
<a id="s05-graphics"></a>
<a id="s05-glass"></a>
<a id="s05-other"></a>

| Component | Native records | JSON lookup |
| --- | --- | --- |
| paint | 160 | `sources.S05.components.paint` |
| foundation | 16 | `sources.S05.components.foundation` |
| rear | 18 | `sources.S05.components.rear` |
| aero | 81 | `sources.S05.components.aero` |
| graphics | 110 | `sources.S05.components.graphics` |
| glass | 14 | `sources.S05.components.glass` |
| other | 427 | `sources.S05.components.other` |

All exact parent paths, order, visibility and stack positions are in `native_layers`; cabin IDs and glass placement are in `tint`.

### S06 — Grand Sport coupe view 02

Source and hash: [register](#source-register-and-integrity); JSON key `sources.S06`. Paint-body root @85; spoiler roots @2, @7, @9, @11. inventory source; not new binding.

<a id="s06-paint"></a>
<a id="s06-foundation"></a>
<a id="s06-rear"></a>
<a id="s06-aero"></a>
<a id="s06-graphics"></a>
<a id="s06-glass"></a>
<a id="s06-other"></a>

| Component | Native records | JSON lookup |
| --- | --- | --- |
| paint | 160 | `sources.S06.components.paint` |
| foundation | 16 | `sources.S06.components.foundation` |
| rear | 19 | `sources.S06.components.rear` |
| aero | 77 | `sources.S06.components.aero` |
| graphics | 111 | `sources.S06.components.graphics` |
| glass | 14 | `sources.S06.components.glass` |
| other | 441 | `sources.S06.components.other` |

All exact parent paths, order, visibility and stack positions are in `native_layers`; cabin IDs and glass placement are in `tint`.

### S07 — Stingray convertible view 01

Source and hash: [register](#source-register-and-integrity); JSON key `sources.S07`. Paint-body root @91; spoiler roots @79, @81, @83. inventory source; not new binding.

<a id="s07-paint"></a>
<a id="s07-foundation"></a>
<a id="s07-rear"></a>
<a id="s07-aero"></a>
<a id="s07-graphics"></a>
<a id="s07-glass"></a>
<a id="s07-other"></a>

| Component | Native records | JSON lookup |
| --- | --- | --- |
| paint | 194 | `sources.S07.components.paint` |
| foundation | 16 | `sources.S07.components.foundation` |
| rear | 38 | `sources.S07.components.rear` |
| aero | 51 | `sources.S07.components.aero` |
| graphics | 93 | `sources.S07.components.graphics` |
| glass | 11 | `sources.S07.components.glass` |
| other | 421 | `sources.S07.components.other` |

All exact parent paths, order, visibility and stack positions are in `native_layers`; cabin IDs and glass placement are in `tint`.

### S08 — Stingray convertible view 02

Source and hash: [register](#source-register-and-integrity); JSON key `sources.S08`. Paint-body root @88; spoiler roots @8, @10, @12. inventory source; not new binding.

<a id="s08-paint"></a>
<a id="s08-foundation"></a>
<a id="s08-rear"></a>
<a id="s08-aero"></a>
<a id="s08-graphics"></a>
<a id="s08-glass"></a>
<a id="s08-other"></a>

| Component | Native records | JSON lookup |
| --- | --- | --- |
| paint | 199 | `sources.S08.components.paint` |
| foundation | 16 | `sources.S08.components.foundation` |
| rear | 38 | `sources.S08.components.rear` |
| aero | 49 | `sources.S08.components.aero` |
| graphics | 93 | `sources.S08.components.graphics` |
| glass | 11 | `sources.S08.components.glass` |
| other | 455 | `sources.S08.components.other` |

All exact parent paths, order, visibility and stack positions are in `native_layers`; cabin IDs and glass placement are in `tint`.

### S09 — Stingray coupe view 01

Source and hash: [register](#source-register-and-integrity); JSON key `sources.S09`. Paint-body root @84; spoiler roots @73, @75, @77. inventory source; not new binding.

<a id="s09-paint"></a>
<a id="s09-foundation"></a>
<a id="s09-rear"></a>
<a id="s09-aero"></a>
<a id="s09-graphics"></a>
<a id="s09-glass"></a>
<a id="s09-other"></a>

| Component | Native records | JSON lookup |
| --- | --- | --- |
| paint | 170 | `sources.S09.components.paint` |
| foundation | 15 | `sources.S09.components.foundation` |
| rear | 38 | `sources.S09.components.rear` |
| aero | 51 | `sources.S09.components.aero` |
| graphics | 93 | `sources.S09.components.graphics` |
| glass | 13 | `sources.S09.components.glass` |
| other | 391 | `sources.S09.components.other` |

All exact parent paths, order, visibility and stack positions are in `native_layers`; cabin IDs and glass placement are in `tint`.

### S10 — Stingray coupe view 02

Source and hash: [register](#source-register-and-integrity); JSON key `sources.S10`. Paint-body root @82; spoiler roots @3, @5, @7. inventory source; not new binding.

<a id="s10-paint"></a>
<a id="s10-foundation"></a>
<a id="s10-rear"></a>
<a id="s10-aero"></a>
<a id="s10-graphics"></a>
<a id="s10-glass"></a>
<a id="s10-other"></a>

| Component | Native records | JSON lookup |
| --- | --- | --- |
| paint | 170 | `sources.S10.components.paint` |
| foundation | 16 | `sources.S10.components.foundation` |
| rear | 38 | `sources.S10.components.rear` |
| aero | 49 | `sources.S10.components.aero` |
| graphics | 84 | `sources.S10.components.graphics` |
| glass | 13 | `sources.S10.components.glass` |
| other | 430 | `sources.S10.components.other` |

All exact parent paths, order, visibility and stack positions are in `native_layers`; cabin IDs and glass placement are in `tint`.

### S11 — Z06 convertible view 01

Source and hash: [register](#source-register-and-integrity); JSON key `sources.S11`. Paint-body root @89; spoiler roots @77, @79, @81. inventory source; not new binding.

<a id="s11-paint"></a>
<a id="s11-foundation"></a>
<a id="s11-rear"></a>
<a id="s11-aero"></a>
<a id="s11-graphics"></a>
<a id="s11-glass"></a>
<a id="s11-other"></a>

| Component | Native records | JSON lookup |
| --- | --- | --- |
| paint | 217 | `sources.S11.components.paint` |
| foundation | 16 | `sources.S11.components.foundation` |
| rear | 19 | `sources.S11.components.rear` |
| aero | 111 | `sources.S11.components.aero` |
| graphics | 77 | `sources.S11.components.graphics` |
| glass | 11 | `sources.S11.components.glass` |
| other | 396 | `sources.S11.components.other` |

All exact parent paths, order, visibility and stack positions are in `native_layers`; cabin IDs and glass placement are in `tint`.

### S12 — Z06 convertible view 02

Source and hash: [register](#source-register-and-integrity); JSON key `sources.S12`. Paint-body root @87; spoiler roots @6, @11, @13, @15. inventory source; not new binding.

<a id="s12-paint"></a>
<a id="s12-foundation"></a>
<a id="s12-rear"></a>
<a id="s12-aero"></a>
<a id="s12-graphics"></a>
<a id="s12-glass"></a>
<a id="s12-other"></a>

| Component | Native records | JSON lookup |
| --- | --- | --- |
| paint | 212 | `sources.S12.components.paint` |
| foundation | 16 | `sources.S12.components.foundation` |
| rear | 20 | `sources.S12.components.rear` |
| aero | 98 | `sources.S12.components.aero` |
| graphics | 76 | `sources.S12.components.graphics` |
| glass | 11 | `sources.S12.components.glass` |
| other | 458 | `sources.S12.components.other` |

All exact parent paths, order, visibility and stack positions are in `native_layers`; cabin IDs and glass placement are in `tint`.

### S13 — Z06 coupe view 01

Source and hash: [register](#source-register-and-integrity); JSON key `sources.S13`. Paint-body root @82; spoiler roots @71, @73, @75. inventory source; not new binding.

<a id="s13-paint"></a>
<a id="s13-foundation"></a>
<a id="s13-rear"></a>
<a id="s13-aero"></a>
<a id="s13-graphics"></a>
<a id="s13-glass"></a>
<a id="s13-other"></a>

| Component | Native records | JSON lookup |
| --- | --- | --- |
| paint | 192 | `sources.S13.components.paint` |
| foundation | 16 | `sources.S13.components.foundation` |
| rear | 19 | `sources.S13.components.rear` |
| aero | 110 | `sources.S13.components.aero` |
| graphics | 74 | `sources.S13.components.graphics` |
| glass | 13 | `sources.S13.components.glass` |
| other | 363 | `sources.S13.components.other` |

All exact parent paths, order, visibility and stack positions are in `native_layers`; cabin IDs and glass placement are in `tint`.

### S14 — Z06 coupe view 02

Source and hash: [register](#source-register-and-integrity); JSON key `sources.S14`. Paint-body root @81; spoiler roots @1, @6, @8, @10. inventory source; not new binding.

<a id="s14-paint"></a>
<a id="s14-foundation"></a>
<a id="s14-rear"></a>
<a id="s14-aero"></a>
<a id="s14-graphics"></a>
<a id="s14-glass"></a>
<a id="s14-other"></a>

| Component | Native records | JSON lookup |
| --- | --- | --- |
| paint | 181 | `sources.S14.components.paint` |
| foundation | 16 | `sources.S14.components.foundation` |
| rear | 20 | `sources.S14.components.rear` |
| aero | 97 | `sources.S14.components.aero` |
| graphics | 86 | `sources.S14.components.graphics` |
| glass | 13 | `sources.S14.components.glass` |
| other | 408 | `sources.S14.components.other` |

All exact parent paths, order, visibility and stack positions are in `native_layers`; cabin IDs and glass placement are in `tint`.

### S15 — ZR1 convertible view 01

Source and hash: [register](#source-register-and-integrity); JSON key `sources.S15`. Paint-body root @86; spoiler roots @76, @78. inventory source; not new binding.

<a id="s15-paint"></a>
<a id="s15-foundation"></a>
<a id="s15-rear"></a>
<a id="s15-aero"></a>
<a id="s15-graphics"></a>
<a id="s15-glass"></a>
<a id="s15-other"></a>

| Component | Native records | JSON lookup |
| --- | --- | --- |
| paint | 112 | `sources.S15.components.paint` |
| foundation | 15 | `sources.S15.components.foundation` |
| rear | 15 | `sources.S15.components.rear` |
| aero | 38 | `sources.S15.components.aero` |
| graphics | 71 | `sources.S15.components.graphics` |
| glass | 11 | `sources.S15.components.glass` |
| other | 295 | `sources.S15.components.other` |

All exact parent paths, order, visibility and stack positions are in `native_layers`; cabin IDs and glass placement are in `tint`.

### S16 — ZR1 convertible view 02

Source and hash: [register](#source-register-and-integrity); JSON key `sources.S16`. Paint-body root @87; spoiler roots @6, @9, @11. inventory source; not new binding.

<a id="s16-paint"></a>
<a id="s16-foundation"></a>
<a id="s16-rear"></a>
<a id="s16-aero"></a>
<a id="s16-graphics"></a>
<a id="s16-glass"></a>
<a id="s16-other"></a>

| Component | Native records | JSON lookup |
| --- | --- | --- |
| paint | 109 | `sources.S16.components.paint` |
| foundation | 15 | `sources.S16.components.foundation` |
| rear | 16 | `sources.S16.components.rear` |
| aero | 36 | `sources.S16.components.aero` |
| graphics | 73 | `sources.S16.components.graphics` |
| glass | 11 | `sources.S16.components.glass` |
| other | 323 | `sources.S16.components.other` |

All exact parent paths, order, visibility and stack positions are in `native_layers`; cabin IDs and glass placement are in `tint`.

### S17 — ZR1 coupe view 01

Source and hash: [register](#source-register-and-integrity); JSON key `sources.S17`. Paint-body root @80; spoiler roots @71, @73. inventory source; not new binding.

<a id="s17-paint"></a>
<a id="s17-foundation"></a>
<a id="s17-rear"></a>
<a id="s17-aero"></a>
<a id="s17-graphics"></a>
<a id="s17-glass"></a>
<a id="s17-other"></a>

| Component | Native records | JSON lookup |
| --- | --- | --- |
| paint | 121 | `sources.S17.components.paint` |
| foundation | 15 | `sources.S17.components.foundation` |
| rear | 15 | `sources.S17.components.rear` |
| aero | 37 | `sources.S17.components.aero` |
| graphics | 87 | `sources.S17.components.graphics` |
| glass | 26 | `sources.S17.components.glass` |
| other | 271 | `sources.S17.components.other` |

All exact parent paths, order, visibility and stack positions are in `native_layers`; cabin IDs and glass placement are in `tint`.

### S18 — ZR1 coupe view 02

Source and hash: [register](#source-register-and-integrity); JSON key `sources.S18`. Paint-body root @82; spoiler roots @1, @4, @6. inventory source; not new binding.

<a id="s18-paint"></a>
<a id="s18-foundation"></a>
<a id="s18-rear"></a>
<a id="s18-aero"></a>
<a id="s18-graphics"></a>
<a id="s18-glass"></a>
<a id="s18-other"></a>

| Component | Native records | JSON lookup |
| --- | --- | --- |
| paint | 130 | `sources.S18.components.paint` |
| foundation | 15 | `sources.S18.components.foundation` |
| rear | 16 | `sources.S18.components.rear` |
| aero | 37 | `sources.S18.components.aero` |
| graphics | 97 | `sources.S18.components.graphics` |
| glass | 25 | `sources.S18.components.glass` |
| other | 319 | `sources.S18.components.other` |

All exact parent paths, order, visibility and stack positions are in `native_layers`; cabin IDs and glass placement are in `tint`.

### S19 — ZR1X convertible view 01

Source and hash: [register](#source-register-and-integrity); JSON key `sources.S19`. Paint-body root @87; spoiler roots @77, @79. inventory source; not new binding.

<a id="s19-paint"></a>
<a id="s19-foundation"></a>
<a id="s19-rear"></a>
<a id="s19-aero"></a>
<a id="s19-graphics"></a>
<a id="s19-glass"></a>
<a id="s19-other"></a>

| Component | Native records | JSON lookup |
| --- | --- | --- |
| paint | 109 | `sources.S19.components.paint` |
| foundation | 15 | `sources.S19.components.foundation` |
| rear | 15 | `sources.S19.components.rear` |
| aero | 38 | `sources.S19.components.aero` |
| graphics | 76 | `sources.S19.components.graphics` |
| glass | 11 | `sources.S19.components.glass` |
| other | 265 | `sources.S19.components.other` |

All exact parent paths, order, visibility and stack positions are in `native_layers`; cabin IDs and glass placement are in `tint`.

### S20 — ZR1X convertible view 02

Source and hash: [register](#source-register-and-integrity); JSON key `sources.S20`. Paint-body root @88; spoiler roots @7, @10, @12. inventory source; not new binding.

<a id="s20-paint"></a>
<a id="s20-foundation"></a>
<a id="s20-rear"></a>
<a id="s20-aero"></a>
<a id="s20-graphics"></a>
<a id="s20-glass"></a>
<a id="s20-other"></a>

| Component | Native records | JSON lookup |
| --- | --- | --- |
| paint | 105 | `sources.S20.components.paint` |
| foundation | 15 | `sources.S20.components.foundation` |
| rear | 16 | `sources.S20.components.rear` |
| aero | 36 | `sources.S20.components.aero` |
| graphics | 77 | `sources.S20.components.graphics` |
| glass | 11 | `sources.S20.components.glass` |
| other | 292 | `sources.S20.components.other` |

All exact parent paths, order, visibility and stack positions are in `native_layers`; cabin IDs and glass placement are in `tint`.

### S21 — ZR1X coupe view 01

Source and hash: [register](#source-register-and-integrity); JSON key `sources.S21`. Paint-body root @73; spoiler roots @65, @67. inventory source; not new binding.

<a id="s21-paint"></a>
<a id="s21-foundation"></a>
<a id="s21-rear"></a>
<a id="s21-aero"></a>
<a id="s21-graphics"></a>
<a id="s21-glass"></a>
<a id="s21-other"></a>

| Component | Native records | JSON lookup |
| --- | --- | --- |
| paint | 124 | `sources.S21.components.paint` |
| foundation | 15 | `sources.S21.components.foundation` |
| rear | 15 | `sources.S21.components.rear` |
| aero | 37 | `sources.S21.components.aero` |
| graphics | 88 | `sources.S21.components.graphics` |
| glass | 25 | `sources.S21.components.glass` |
| other | 251 | `sources.S21.components.other` |

All exact parent paths, order, visibility and stack positions are in `native_layers`; cabin IDs and glass placement are in `tint`.

### S22 — ZR1X coupe view 02

Source and hash: [register](#source-register-and-integrity); JSON key `sources.S22`. Paint-body root @82; spoiler roots @1, @4, @6. inventory source; not new binding.

<a id="s22-paint"></a>
<a id="s22-foundation"></a>
<a id="s22-rear"></a>
<a id="s22-aero"></a>
<a id="s22-graphics"></a>
<a id="s22-glass"></a>
<a id="s22-other"></a>

| Component | Native records | JSON lookup |
| --- | --- | --- |
| paint | 130 | `sources.S22.components.paint` |
| foundation | 15 | `sources.S22.components.foundation` |
| rear | 16 | `sources.S22.components.rear` |
| aero | 36 | `sources.S22.components.aero` |
| graphics | 103 | `sources.S22.components.graphics` |
| glass | 25 | `sources.S22.components.glass` |
| other | 293 | `sources.S22.components.other` |

All exact parent paths, order, visibility and stack positions are in `native_layers`; cabin IDs and glass placement are in `tint`.

### S23 — ZR1X coupe view 01

Source and hash: [register](#source-register-and-integrity); JSON key `sources.S23`. Paint-body root @80; spoiler roots @71, @73. earlier saved ZR1X comparison; no baseline selected.

<a id="s23-paint"></a>
<a id="s23-foundation"></a>
<a id="s23-rear"></a>
<a id="s23-aero"></a>
<a id="s23-graphics"></a>
<a id="s23-glass"></a>
<a id="s23-other"></a>

| Component | Native records | JSON lookup |
| --- | --- | --- |
| paint | 124 | `sources.S23.components.paint` |
| foundation | 15 | `sources.S23.components.foundation` |
| rear | 15 | `sources.S23.components.rear` |
| aero | 37 | `sources.S23.components.aero` |
| graphics | 89 | `sources.S23.components.graphics` |
| glass | 25 | `sources.S23.components.glass` |
| other | 257 | `sources.S23.components.other` |

All exact parent paths, order, visibility and stack positions are in `native_layers`; cabin IDs and glass placement are in `tint`.

## Prioritized independently reviewable batches

Batch IDs stay stable for review; prerequisites are explicit and do not require finishing unrelated models first. These are future tasks, not authorization to execute exports or code changes now.

- **1. Resolve source/identity holds per affected batch.** Review S21/S23/pinned-proof differences without selecting a baseline in this audit; qualify or reject the derived GSX candidate; identify numeric spoiler/stripe/ground-effect aliases. Use the S04/S05 disposition for GS coupe, and resolve S09’s missing 1LT exterior foundation before that trim’s batch. Do not schedule factory-unavailable 5ZU/5ZZ/5ZW/5VM/5W8/5V7 as active choices.
- **Tint qualification — ahead of 2a and 3.** Apply the October 9 owner recipe on disposable sources, one source/model/body/view per reviewable batch. Cover every aperture with #0b0b0c at 100% Normal, retain reflections/defrosters on top, and prove no cabin is visible. Qualify the separate native depth intervals (including transparent roofs), then bake the fixed treatment into native reference scenes. For GS coupe complete glass use S05, with new proof; leave bound S04 proof frozen. This is not a catalog option or a runtime tint selector.
- **2a. Stingray view-01 paints + T0A rear component, one body per batch.** Reuse the three-paint workflow and add the seven exact paint families plus both mirror peers. Gate on T0A alias identification and tint qualification; preserve the correct fixed foreground and state the component-preview limit. The existing back(0)/spoiler(20)/foreground(30) contract suffices: **no renderer change or no-spoiler contract dependency**. Keep 3LT, 2LT and the missing coupe-1LT foundation independently reviewable. **TVS is excluded from 2a and moves to 6** because its front splitter cannot be represented by a wing-only choice.
- **2b-R. Small renderer no-spoiler contract task.** Separate from general depth/view work: explicitly support a catalog-resolved no-spoiler/default state instead of requiring exactly one spoiler. Define behavior for ZF1 with and without replacement TVS; ZF1 alone is not a blanket “hide every wing” test. This task precedes 2b exports and does not block 2a.
- **2b. Stingray ZF1 / legal no-spoiler states, one body per batch.** **Depends on 2b-R**, tint qualification, source identity resolution and the catalog-resolved rear/front delete combination. Qualify the front-splitter removal in the fixed foreground as well as the hidden rear groups. Do not bind an all-spoilers-off state to ZF1 without evaluating replacement options.
- **3. Lower trims on existing view 01, one model/body per batch.** **Depends on tint qualification.** Use each source’s explicit S0507 trim foundation, trim-correct mirrors and other exterior equipment. Visible-cabin/interior material differences are intentionally not depicted; a “catalog-correct visible cabin” is no longer a prerequisite. Prove the resulting native exterior scene for each trim and never relabel upper-trim pixels. ZR1/ZR1X offer 1LZ only below 3LZ. Tint does not excuse S09’s missing 1LT exterior foundation.
- **4. Existing unbound rear/component proofs.** Review W/asset-proofs/2026-09-21-components/ (218 prior exports / 83 historical comparisons) and the separate five-plane Grand Sport roof proof. Low-spoiler S0267/T0E, wheel/cap and caliper/disc identities remain qualification work. Reuse qualified states/evidence before re-exporting; future exterior proofs must incorporate the owner tint decision.
- **5. Renderer depth/view support.** A separate future task for multiple depth intervals, complete component replacement and explicit view identity. The small no-spoiler contract is already split out as 2b-R. Fixed tint can be baked natively; this batch is not an artificial prerequisite for 2a or tint qualification.
- **6. Full aero, one catalog package/model/body/view per batch.** Qualify rear wing + front splitter + rockers + dive planes/hood pieces and finish dependencies together. **Include Stingray TVS and complete Z51 here**; TVS must not inherit 2a’s rear-only acceptance. Independent front/side selection depends on the needed portion of 5; explicit fixed full-package recipes must demonstrate native equivalence. Give Z06 T0F/T0G/CBF and ZR1/ZR1X TOM/5WN/PCR separate batches; equal RPOs never share implicit bindings.
- **7. Stripes/graphics, one package/color/model/body/view per batch.** Identify numeric aliases and use S05 where S04 removed branches. Capture every front/rear/roof branch at its native depth after relevant support in 5. Catalog controls colors/applicability, including DTC/DUE and retired DUW.
- **8. Remaining equipment and second views.** Wheels/calipers/caps, roof, mirrors/badges/exhaust follow as complete replacement assemblies; qualify second-view equivalents and GSX when sources are accepted. This batch depends on the earlier tint qualification.

Each later export batch uses the existing W workflow: fresh copy → hash-pinned native reference/recipe → `build-asset-states.py` → `build-export-batch.py` / unchanged `export-states.psjs` → `verify-native-compositions.py` plus visual inspection → restored visibility and original/copy hashes. Full-canvas raw evidence remains outside Git. Binding, merge, deployment and release acceptance are separate decisions.

## Validation and limits

Initial audit checks (retained evidence): 22 native inventories / 30,236 records, unchanged visibility and 22 four-way source/copy hashes; native versus saved-layer comparison; 64 offered matrix rows plus eight non-offered rows; catalog scope equality; all ten manifests/proofs and 192 asset hashes loaded; ConsumerCatalog produced eight previews, unavailable Stingray scenes and unbound GSX. Those application checks were not rerun for this documentation-only revision.

Revision checks: verified D01/D02 duplicate hashes against S09/S05; read-only native S23 inventory (1,063 layers) using the unchanged existing dump script; visibility unchanged, copy closed without saving and prior open document unchanged; all three additional files passed original-before = copy-before = original-after = copy-after SHA-256. S23 shared native/raw identity, parent, sibling order and visibility agree. S04/S05/S09/S21 original and disposable-copy hashes were rechecked against the initial pinned values and still match. Compared S23 with pinned reference and S21, including shared traversal order; enumerated all 224 S05-only IDs. Re-read/hash-verified the pinned catalog and T0A/TVS/ZF1 scopes/content. JSON totals match the register: 23 inventories / 31,299 layers, duplicates excluded. Every ID formerly listed in the per-source Markdown inventory is retained in JSON; native parent/order/visibility records match the saved audit inputs. Checked component indexes, matrix rows, internal anchors, cross-document pointers and the final Git diff/whitespace. All 45 PSB paths are dispositioned as 25 exterior (23 distinct + two duplicates) and 20 interior-camera files outside scope.

No new native render, mask/alpha inspection, anatomical/color alias identification, pixel equivalence, tint visibility proof, trim correctness or aero completeness is claimed from layer inventories. Source names alone cannot settle those questions. No exports, images, manifests, renderer, catalog or production changes were made. Existing bound S04 evidence is unchanged, and no ZR1X regeneration baseline is selected. Application tests and browser rendering checks were not run because only documentation and its inventory data changed.
