#!/usr/bin/env python3
"""Tecno Tarot Parallax 3 HQ build: 7 moving layers + static frame.
   v3_build_hq.py NN RAWDIR   (RAWDIR holds bg,mid,figure,energy .png at 2120x3460)"""
import sys, json, pathlib
from PIL import Image
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import v2_build_card as B
ROOT = pathlib.Path(__file__).resolve().parent.parent
ORDER = ["bg", "mid", "figure", "energy"]
DEPTH = {"bg": -0.040, "mid": -0.018, "figure": 0.0, "energy": 0.040}
Z = {"bg": 10, "mid": 20, "figure": 30, "energy": 40}
def main():
    nn = int(sys.argv[1]); raw = pathlib.Path(sys.argv[2])
    mpath = ROOT/"deck"/"manifest.json"; man = json.loads(mpath.read_text())
    prev = next((c for c in man["cards"] if c["index"] == nn), {})
    cid = raw.name; out = ROOT/"deck"/cid
    fr = None
    for p in (out/"frame@2x.webp", ROOT.parent/"v1"/"deck"/cid/"frame@2x.webp", ROOT.parent/"v1"/"deck"/cid/"frame.webp", ROOT.parent/"deck"/cid/"frame.webp"):
        if p.exists(): fr = Image.open(p).convert("RGBA").resize(B.CANVAS, Image.LANCZOS); break
    if fr is None: raise SystemExit("no frame for "+cid)
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("*.webp"): f.unlink()
    layers, files = {}, {}
    for n in ORDER:
        im = Image.open(raw/f"{n}.png").convert("RGBA")
        if n == "bg": im.putalpha(255)
        im = B.cover(im, B.LAYER2X); layers[n] = im; B.save(im, out, n); files[n] = n
    B.save(fr, out, "frame"); files["frame"] = "frame"
    B.MOVING = ORDER; B.thumb(layers, fr).save(out/"thumb.webp", "WEBP", quality=82); files["thumb"] = "thumb"
    entry = {"schema": "tecnotaro-parallax-v3", "layerCount": 4, "order": ORDER+["frame"], "id": cid, "index": nn, "title": prev.get("title", cid[3:].replace("-", " ").upper()), "suit": prev.get("suit"),
             "files": files, "layers": {**{k: {"depth": DEPTH[k], "z": Z[k], "blend": "normal", "rect": B.OVERSCAN} for k in ORDER}, "frame": {"moving": False, "z": 50, "blend": "normal"}}, "depth": dict(DEPTH), "rect": {k: B.OVERSCAN for k in ORDER}}
    (out/"card.json").write_text(json.dumps(dict(entry, layerSize={"@2x": B.LAYER2X, "@1x": B.LAYER1X}, amplitude=B.AMPLITUDE, style="hq7"), indent=1, ensure_ascii=False))
    man["schema"] = "tecnotaro-parallax-v3"; man["layerCount"] = 4; man["order"] = ORDER+["frame"]
    man["legacyLayers"] = {"fg": "only for placeholder cards that still point to v1 layers; HQ cards use energy"}
    L = man.setdefault("layers", {})
    for k in ORDER: L[k] = {"z": Z[k], "depth": DEPTH[k], "blend": "normal", "rect": B.OVERSCAN}
    L["frame"] = L.get("frame", {"moving": False, "z": 50}); L["frame"]["z"] = 50
    man["cards"] = sorted([c for c in man["cards"] if c["index"] != nn]+[entry], key=lambda c: c["index"])
    mpath.write_text(json.dumps(man, indent=1, ensure_ascii=False)); print("ok", cid)
if __name__ == "__main__": main()
