#!/usr/bin/env python3
"""Global manifest.json (deck/) and thumbnails from all deck/NN-slug/card.json."""
import json, glob, pathlib
from PIL import Image
D = pathlib.Path(__file__).resolve().parent.parent; T = D.parent/"tecnotaro"
cards = [json.loads(open(f).read()) for f in sorted(glob.glob(str(D/"deck/*/card.json")))]
for c in cards:
    t = D/"deck"/c["id"]/"thumb.webp"
    if not t.exists(): Image.open(T/f"cartas/en/{c['id']}.png").convert("RGB").resize((200, 343), Image.LANCZOS).save(t, quality=80)
m = dict(deck="Tecnotarô Alexandre Rangel", version=3, aspect=[7, 12], canvas=[2240, 3840],
         window=dict(x=181, y=374, w=1892, h=3090, cornerRadius=0.04), overscan=1.10,
         files={"@1x": "{id}/{layer}.webp", "@2x": "{id}/{layer}@2x.webp", "thumb": "{id}/thumb.webp"},
         layers=[dict(name="bg", rect="window*overscan", blend="normal", note="far plane, moves most, opposite to tilt"),
                 dict(name="mid", rect="window", blend="normal", note="figure or emblem + ground anchor, zero plane"),
                 dict(name="fg", rect="window", blend="screen", note="sparse particles, small move with the tilt"),
                 dict(name="frame", rect="canvas", blend="normal", note="fixed")],
         rule="offset = tilt(-1..1, clamped) * depth * window width on both axes; |bg depth| * window width <= 0.95 * halo_margin_px",
         motion=dict(maxTiltDeg=22, smoothing=0.10, cardTiltDeg=4),
         ground_edges={c["id"]: dict(ground_edge=c["ground_edge"], edge_y=c["edge_y"]) for c in cards},
         cards=cards)
(D/"deck/manifest.json").write_text(json.dumps(m, indent=1, ensure_ascii=False)); print(len(cards), "cards")
