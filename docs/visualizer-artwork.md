# Confirmed-build Photoshop artwork

The first application binding covers one camera view of the **2027 Grand Sport
Coupe 3LT**, with ten paints and two spoilers. A confirmed paint changes both the
back and foreground planes; a confirmed spoiler changes the plane between them.
The preview explicitly identifies the paint, spoiler and limits of its coverage.

| Paints | Spoilers | Shared canvas |
| --- | --- | --- |
| GBA, G8G, GKZ, GPH, G26, GBK, G4Z, GKA, GTR, GEC | T0F, 5ZV | 1500 × 844, uncropped |

The 22 lossless WebP planes total 3,896,762 bytes and support twenty combinations.
Wheels, interior, brakes, calipers and other equipment remain fixed and may differ
from the configured build. T0F represents its spoiler only, not CFZ ground effects
or the rest of that package. Other model/body/trim/view combinations show an
explicit unavailable state. Equal option IDs in another model never grant use of
Grand Sport artwork. Low-spoiler/SIG candidates remain unbound because their
S0267-to-T0E identity was inferred rather than established.

## Native source and proof

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

## Application and release behavior

[`catalog/artwork.py`](../catalog/artwork.py) checks the image and evidence hashes,
canvas, plane order and exact model/year/body/trim/option ownership against the
native proof. [`manifest.json`](../catalog/web/artwork/manifest.json) is the compact
application binding. Retired or renamed RPO identities invalidate that catalog's
art binding until reviewed; they do not borrow a different model's images or
prevent an otherwise valid catalog edit from releasing.

The consumer projects artwork from the same resolved state as prices and order
output. Pending changes cannot replace the confirmed image. Cancel preserves it;
confirm and revert select their resolved planes. All three images must decode
before display. Missing images hide the whole stack with a readable message;
a later valid selection can recover. Async completions from older selections
cannot replace a newer build's artwork.

Release completion includes the images, application manifest and native proof in
runtime hashes and the artifact inventory. Verification checks the media
declaration and each model's generated visualizer binding against the bundled
evidence and catalog snapshot. Repeated completion and backup/restore preserve
the same release identity. Altered images or rehashed, inconsistent media
declarations fail verification. Older releases without an artwork runtime retain
their original empty media contract.

The existing [release commands](consumer-releases.md) and
[dealer preview/delivery controls](dealer-submission.md) remain the operational
path. No schema, source business data, pricing, order emission, production host
or canonical authority changes in this artwork integration.

## Verification

Focused checks cover all twenty combinations, foreign-model/body/trim fallback,
pending/cancel/confirm/revert behavior, stale identity refusal, image/evidence
mutation, repeat completion and recovery. Browser checks cover paint changes,
spoiler transactions, a blocked image, recovery and desktop/mobile layout. The PR
records the final revision's combined consumer/dealer/release regression results,
six-model audit and completed-release browser qualification.
