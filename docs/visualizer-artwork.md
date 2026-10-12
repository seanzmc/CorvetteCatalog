# Confirmed-build Photoshop artwork

The application covers one verified camera view for each of ten **2027 model/body
scenes**, using 192 lossless WebP planes (34,859,694 bytes) for 146 supported
paint/spoiler combinations. Every model below has independently exported coupe
and convertible artwork; the source-supported trim is part of the binding.

| Model | Bodies | Trim | Paints | Spoilers | Combinations |
| --- | --- | --- | --- | --- | --- |
| Grand Sport | Coupe, convertible | 3LT | Ten | T0F, 5ZV | 40 |
| Stingray | Coupe, convertible | 3LT | GBA, G8G, GKZ | 5ZU, matched to paint | 6 |
| Z06 | Coupe, convertible | 3LZ | Ten | T0F, T0G, 5ZV | 60 |
| ZR1 | Coupe, convertible | 3LZ | Ten | TOM (`opt_tom_001`) | 20 |
| ZR1X | Coupe, convertible | 3LZ | Ten | TOM (`opt_tom_002`) | 20 |

The ten-paint families cover GBA, G8G, GKZ, GPH, G26, GBK, G4Z, GKA, GTR and GEC.
Every image uses the same uncropped 1500 × 844 canvas. Paint changes both the back
and foreground planes. Stingray's body-color 5ZU also changes the spoiler plane;
other spoilers retain their independently verified model-specific plane.

Wheels, interior, brakes, calipers, roof position and other equipment remain fixed
and may differ from the configured build. Aero-package artwork represents its
rear spoiler only. Convertible scenes retain the native raised/closed top and
nacelle configuration. Other model/body/trim/view combinations show an explicit
unavailable state. Grand Sport X has no corresponding source in the supplied
folder. Equal option IDs or similar cars never justify borrowing another scene.
Audit update: a GSX-named derivative exists; see the [GSX provenance finding](visualizer-asset-gaps.md#gsx-provenance-and-source-drift) before treating it as native GSX coverage.
Internal S-number low-spoiler aliases and source no-spoiler decomposition references
remain unbound; they do not establish an option identity or application default.

## Family evidence

[`index.json`](../catalog/web/artwork/index.json) enumerates the exact scene
directories. Each retains its original native family proof unchanged beside the
compact application manifest and lossless images:

| Model | Coupe proof | Convertible proof |
| --- | --- | --- |
| Grand Sport | [Source proof](../catalog/web/artwork/source-proof.json) | [Source proof](../catalog/web/artwork/grand-sport-convertible/source-proof.json) |
| Stingray | [Source proof](../catalog/web/artwork/stingray-coupe/source-proof.json) | [Source proof](../catalog/web/artwork/stingray-convertible/source-proof.json) |
| Z06 | [Source proof](../catalog/web/artwork/z06-coupe/source-proof.json) | [Source proof](../catalog/web/artwork/z06-convertible/source-proof.json) |
| ZR1 | [Source proof](../catalog/web/artwork/zr1-coupe/source-proof.json) | [Source proof](../catalog/web/artwork/zr1-convertible/source-proof.json) |
| ZR1X | [Source proof](../catalog/web/artwork/zr1x-coupe/source-proof.json) | [Source proof](../catalog/web/artwork/zr1x-convertible/source-proof.json) |

Each proof records its own source/copy hashes, native layers, catalog/guide
anchors, fixed equipment, image hashes and comparison results. All exports ran
from disposable copies and restored native visibility; the originals remained
unchanged. The application stores each body's actual native render, not a
transformed coupe or a model-name substitution. The separate Grand Sport roof
proof requires five planes and remains outside this three-plane renderer.

## Initial Grand Sport coupe proof

The original, unchanged Photoshop source is
`visual-studio/grandsport/e.coupe.exterior.01 - cleaned.psb` under the owner's
`visualizer-studio_27` iCloud folder. Its SHA-256 is
`1e9360c73d3acdb17121e9b2bc8ae8af14c5ea9507b58ab61c4b2b96e1f9345e`.
Exports ran in Photoshop 27.12.0 from a disposable copy. Both batches restored all
1,400 native layer visibility flags; the original and working-copy file hashes
remained unchanged. The raw file reader's additional hidden Tow_Hooks entry is
recorded in the proof rather than silently treated as a native layer.

[`source-proof.json`](../catalog/web/artwork/source-proof.json) is a byte-for-byte
copy of the verified `family-manifest.json`, SHA-256
`aa511cbb6e815699263f5f9915a69a3f7f35157ad5a338a2f4299beb8cc8465f`.
It records the source identity, exact layers and paint recipes, option evidence,
native image/state hashes and per-combination comparison results. Its relative
paths refer to the original proof package, whose absolute location it records;
they are not paths inside a release.

Every composed scene was compared with its native Photoshop reference. Maximum
differences were 2/255 for opaque RGB and 1/255 for alpha. Premultiplied RGB differed
by at most 2.0039/255 at one fixed pixel. All ten paints were visually inspected,
including mount occlusion; lossless WebP RGBA matched each PNG derivative. Each
paint recipe corrects the source's mismatched far mirror with that paint's exact
mirror layer. Browser composition preserves the native order: **back (0), one
spoiler (20), foreground (30)**. Placing a spoiler over an already assembled car
would give the wrong occlusion.

The native PSB, full-size PNG references and export workspace stay outside Git.
The bundled images reproduce the verified browser preview without Photoshop.
The native proof package retains the source recipes and evidence for future
asset regeneration. The capture form's launch and Escape cancellation were
verified; saving through that form is not claimed. Actual exports used native
inventory-bound states through Photoshop UXP.

The Photoshop project `27vette-phase1/REPRODUCE-PROOFS.md` records the exact
regeneration commands. Its `build-asset-states.py` checks the source hash,
`build-export-batch.py` embeds the unchanged UXP exporter and checks restoration,
and `verify-native-compositions.py` independently compares each family's native
scenes. Later families retain their own recipes and comparison plans.
Reproduction writes to a fresh directory and never overwrites the qualified
proof or original source. A fresh render requires renewed review before its
images or proof replace this binding.

## Application and release behavior

[`catalog/artwork.py`](../catalog/artwork.py) checks the image and evidence hashes,
canvas, plane order and exact model/year/body/trim/option ownership against the
native proof. Each `manifest.json` is a compact application binding; the explicit
collection index prevents directory discovery from silently adding a scene.
Overlapping model/year/body/trim scopes are rejected until a view selector exists.
Retired or renamed RPO identities invalidate the affected scene until reviewed;
they do not borrow a different body's or model's images, hide an independently
valid scene, or prevent an otherwise valid catalog edit from releasing.

### Optional no-rear-spoiler state

A scene may opt in with the same `no_spoiler` object in its application manifest
and hash-pinned native proof. The existing v1 formats accept this optional extension:

```json
"no_spoiler": {
  "group_id": "08154d57-e154-4712-ad8d-05589cbfab4c",
  "excluded_option_ids": ["opt_z51_001"]
}
```

This example names the pinned R3 Stingray rear group and excludes Z51 because a
non-Z51 scene's fixed front does not qualify Z51 equipment. IDs must come from
the scene model's own catalog revision: the group must cover the scene's body
and trim, have minimum 0, and contain every bound spoiler choice. Every excluded
option must exist in that model. A stale declaration returns the existing
“Artwork bindings need review” result; unequal manifest/proof declarations fail
package loading. No current scene declares this state; Stingray binding and native
qualification remain batch 2a work.

For a declared scene, exactly one supported paint with **no installed member of
the entire catalog group** renders **back (0), foreground (30)**, labelled
“No rear spoiler.” A single installed bound choice retains the three-plane
composition. An installed unbound member, multiple members, an unsupported paint,
or any installed excluded option makes artwork unavailable, including when a
bound spoiler is present. Scenes without the declaration still require one
bound spoiler; a paint-only Grand Sport does not acquire a bare-car fallback.

The renderer reads resolved installed equipment, with no RPO-specific rules.
ZF1 removes T0A through catalog resolution; ZF1 with TVS retains TVS as a rear
group member and requires its qualified artwork. A non-Z51 scene excluding Z51
refuses **Z51 + ZF1**, with or without TVS, until a dedicated scene exists. ZF1
alone is never an instruction to hide all spoilers. The declaration must reflect
native proof of the fixed front and rear planes, not just an empty rear group.

`release_media()` and `asset_path()` need no change: the two-plane state reuses
the same hash-pinned back and foreground assets and scene-qualified URLs.

### Confirmed projection and packaging

The consumer projects artwork from the same resolved state as prices and order
output. Pending changes cannot replace the confirmed image. Cancel preserves it;
confirm and revert select their resolved planes. All selected images must decode
before display. Missing images hide the whole stack with a readable message;
a later valid selection can recover. Async completions from older selections
cannot replace a newer build's artwork.

Release completion includes the images, application manifest and native proof in
runtime hashes and the artifact inventory. Verification checks the media
declaration and each model's generated visualizer binding against the bundled
evidence and catalog snapshot. Repeated completion and backup/restore preserve
the same release identity. Altered images or rehashed, inconsistent media
declarations fail verification. Scene-qualified media identities keep equal asset
IDs in different families separate. Older single-family releases retain their
original media and visualizer contracts; releases without artwork retain the
empty media contract. Both real prior bundle types were verified with this reader.

The existing [release commands](consumer-releases.md) and
[dealer preview/delivery controls](dealer-submission.md) remain the operational
path. No schema, source business data, pricing, order emission, production host
or canonical authority changes in this artwork integration.

## Verification

Focused checks cover all 146 combinations against native proof identities and
image hashes, foreign-model/body/trim fallback, paint-specific spoilers,
overlapping scene/path rejection, stale per-body binding isolation,
optional no-spoiler proof agreement, model-owned group scope and minimum,
unbound members and fixed-plane exclusions,
pending/cancel/confirm/revert behavior, stale identity refusal, image/evidence
mutation, repeat completion and recovery. Browser checks cover paint changes,
spoiler transactions, a blocked image, recovery and desktop/mobile layout. The PR
records the final revision's combined consumer/dealer/release regression results,
six-model audit and completed-release browser qualification.
