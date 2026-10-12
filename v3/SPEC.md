# Tecnotarô parallax v2: asset spec

Viewer: `v2/index.html` (status line shows `v2-engine`). Deck: `v2/deck/`. Engine config and card list: `v2/deck/manifest.json`.

## Layers (back to front)

| order | layer  | file          | content | alpha | default depth |
|-------|--------|---------------|---------|-------|---------------|
| 1 | bg     | `bg.webp`     | far background, sky, city, horizon. Full and opaque, NO figures, no props | opaque | -0.030 |
| 2 | mid    | `mid.webp`    | midground scenery between bg and figure (buildings, trees, arches, distant machines) | transparent | -0.015 |
| 3 | figure | `figure.webp` | the character (or emblem) plus the ground it stands on | transparent | 0.000 (zero plane) |
| 4 | fg     | `fg.webp`     | foreground: energies, sparks, smoke, plants, props. Big, present, may cross the figure and the window edges | transparent | +0.036 |
| 5 | frame  | `frame.webp`  | the card frame with title, fixed, always on top, never moves | window is transparent | fixed |

Negative depth moves against the tilt (far), positive moves with it (near).
Offset in px = tilt(-1..1) x depth x amplitude (1.15) x window width. The 1.15 amplitude makes v2 15% stronger than v1 (v5 viewer).
Per card overrides go in `raw/NN-slug/depth.json`, e.g. `{"fg": 0.045}`.

## Canvas and overscan

- Full card (frame): 2240 x 3840 @2x, 1120 x 1920 @1x, aspect 7:12.
- Art window inside the frame: x 181, y 374, w 1892, h 3090 (@2x).
- Every moving layer (bg, mid, figure, fg) is delivered at window x 1.12: **2120 x 3460 @2x, 1060 x 1730 @1x**, centered on the window. That is a 6% margin per side (114 px @2x horizontally, 185 px vertically).
- Rule: 1 + 2 x |depth| x 1.15 must stay <= 1.12, so |depth| <= 0.052. The viewer enforces it anyway: if a depth needs more, it zooms that layer instead of showing an edge.
- Keep important content (faces, symbols) inside the central window area, at least 6% away from every side; the margin is only seen at max tilt.
- bg must be fully painted to the edges. Transparent layers may have content touching the edges (fg especially), the overscan hides the cut.

## How to generate raw plates

Put them in `v2/raw/NN-slug/` (slug as in v1, e.g. `44-nine-of-cups`), PNG, any size with a 0.613 (2120:3460) aspect or larger; they are cover fitted and center cropped.

- `bg.png`: same scene with the figure and the foreground removed, empty stage.
- `mid.png`, `figure.png`, `fg.png`: either real transparent PNG, or generated on a flat plain background (pure green #00FF00 or magenta #FF00FF, never a colour used in the element). Avoid soft shadows and glows touching the background colour when possible.
- Optional `frame.png` (2240 x 3840, transparent window). If absent, the v1 frame of the same card is reused.
- Optional `depth.json` overrides.
- Generate all four plates from the same composition and camera, so they line up without manual alignment.

## Build

```
python3 src/v2_build_card.py NN [--force] [--key auto|rembg|flat|none]
```

For each card it: reads the raw plates, removes the background of mid/figure/fg when they have no alpha (`auto`: flat colour key with despill when the border is uniform, otherwise rembg `isnet-general-use`; requires `pip install rembg onnxruntime`), cover fits to 2120 x 3460, writes `@2x` and `@1x` webp, the frame, `thumb.webp` (280 x 480 composite), `card.json`, and replaces the card entry in `deck/manifest.json` (placeholders point to the v1 layers until then).

## Frame rule (QA)

The frame is the topmost element, never transformed. All moving layers live inside `#win`, which is clipped by `win-mask.png` (the inverted frame alpha, cropped to the window) via CSS `mask-image`. The whole card tilt is a flat (non preserve-3d) transform, so the browser never depth sorts the frame against the layers.
Check with `python3 tools/frame_qa.py http://localhost:PORT/v2 v1/deck`: renders every card at the 8 max tilt poses and requires the opaque frame pixels to be identical to the neutral render.
