#!/usr/bin/env python3
"""Tecnotaro parallax v2, card build. One card per call:
    v2_build_card.py NN [--force] [--key auto|rembg|flat|none] [--root DIR]
Reads   ROOT/raw/NN-slug/{bg,mid,figure,fg}.png   (bg required, the others optional; optional frame.png, depth.json)
Writes  ROOT/deck/NN-slug/{frame,bg,mid,figure,fg}.webp (@1x) and @2x.webp, thumb.webp, card.json
Updates ROOT/deck/manifest.json (replaces the placeholder entry of that card).
ROOT defaults to the v2 folder (tecnotaro-parallax/v2 locally, v2/ in the repo). See ROOT/SPEC.md."""
import sys, json, pathlib, argparse, numpy as np
from PIL import Image, ImageFilter

HERE = pathlib.Path(__file__).resolve().parent
CANVAS = (2240, 3840)                 # full card @2x (frame size)
WIN = (181, 374, 1892, 3090)          # x, y, w, h of the art window on the @2x canvas
OVERSCAN = 1.12                       # every moving layer covers window * 1.12 (6% margin per side)
LAYER2X = (2120, 3460)                # round(1892*1.12), round(3090*1.12)
LAYER1X = (1060, 1730)
AMPLITUDE = 1.15
DEFAULT_DEPTH = {"bg": -0.030, "mid": -0.015, "figure": 0.0, "fg": 0.036}
MOVING = ["bg", "mid", "figure", "fg"]

def default_root():
    for r in (HERE.parent/"v2", HERE.parent):
        if (r/"deck").is_dir() or (r/"raw").is_dir(): return r
    return HERE.parent/"v2"

def v1_frame_dir(root, cid):
    for d in (root.parent/"deck"/cid, root.parent/"v1"/"deck"/cid):
        if (d/"frame.webp").exists(): return d
    return None

def cover(img, size):
    """scale to cover size, center crop"""
    w, h = img.size; s = max(size[0]/w, size[1]/h)
    img = img.resize((max(size[0], round(w*s)), max(size[1], round(h*s))), Image.LANCZOS)
    w, h = img.size; x, y = (w-size[0])//2, (h-size[1])//2
    return img.crop((x, y, x+size[0], y+size[1]))

def has_alpha(img):
    if img.mode != "RGBA": return False
    a = np.asarray(img.getchannel("A")); return (a < 250).mean() > 0.01

def flat_key(img):
    """background removal for plates generated on a flat chroma or plain colour: estimate the colour from the border,
    soft key by colour distance, despill. Returns RGBA or None when the border is not flat."""
    a = np.asarray(img.convert("RGB")).astype(np.float32); h, w, _ = a.shape; b = max(4, min(h, w)//100)
    border = np.concatenate([a[:b].reshape(-1, 3), a[-b:].reshape(-1, 3), a[:, :b].reshape(-1, 3), a[:, -b:].reshape(-1, 3)])
    key = np.median(border, 0)
    if np.percentile(np.linalg.norm(border-key, axis=1), 90) > 28: return None
    d = np.linalg.norm(a-key, axis=2)
    alpha = np.clip((d-30)/(90-30), 0, 1)
    # despill: pull the key colour out of semi transparent edge pixels
    k = (1-alpha)[..., None]
    rgb = np.clip((a - key*k*0.85) / np.maximum(1-k*0.85, 1e-3), 0, 255)
    kc = int(np.argmax(key))
    if key[kc] - np.delete(key, kc).max() > 60:     # saturated chroma key: clamp its channel to the max of the others
        others = np.delete(rgb, kc, axis=2).max(2); rgb[..., kc] = np.minimum(rgb[..., kc], others)
    alpha = np.asarray(Image.fromarray((alpha*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7)))
    return Image.fromarray(np.dstack([rgb, alpha]).astype(np.uint8), "RGBA")

_sess = None
def rembg_cut(img):
    global _sess
    from rembg import remove, new_session          # pip install rembg onnxruntime
    if _sess is None: _sess = new_session("isnet-general-use")
    return remove(img.convert("RGB"), session=_sess, post_process_mask=True).convert("RGBA")

def cutout(img, mode):
    if has_alpha(img) or mode == "none": return img.convert("RGBA")
    if mode in ("auto", "flat"):
        r = flat_key(img)
        if r is not None: return r
        if mode == "flat": raise SystemExit("flat key: border is not a flat colour, use --key rembg")
    return rembg_cut(img)

def save(img, out, name):
    lossless = False
    img.save(out/f"{name}@2x.webp", "WEBP", quality=92 if name == "frame" else 90, alpha_quality=100, method=6, lossless=lossless)
    s1 = LAYER1X if name != "frame" else (CANVAS[0]//2, CANVAS[1]//2)
    img.resize(s1, Image.LANCZOS).save(out/f"{name}.webp", "WEBP", quality=90 if name == "frame" else 88, alpha_quality=100, method=6, lossless=lossless)

def thumb(layers, frame):
    wx, wy, ww, wh = WIN; comp = Image.new("RGBA", CANVAS, (0, 0, 0, 255))
    win = Image.new("RGBA", (ww, wh), (0, 0, 0, 255))
    for n in MOVING:
        if n in layers: win.alpha_composite(cover(layers[n], (ww, wh)))
    comp.alpha_composite(win, (wx, wy)); comp.alpha_composite(frame)
    return comp.convert("RGB").resize((280, 480), Image.LANCZOS)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("nn", type=int); ap.add_argument("--force", action="store_true")
    ap.add_argument("--key", default="auto", choices=["auto", "rembg", "flat", "none"]); ap.add_argument("--root")
    o = ap.parse_args(); root = pathlib.Path(o.root) if o.root else default_root()
    raws = sorted((root/"raw").glob(f"{o.nn:02d}-*"))
    if not raws: raise SystemExit(f"no raw folder {root/'raw'}/{o.nn:02d}-slug")
    raw = raws[0]; cid = raw.name; out = root/"deck"/cid
    if (out/"card.json").exists() and not o.force: print("skip", cid, "(use --force)"); return
    if not (raw/"bg.png").exists(): raise SystemExit("bg.png is required")
    out.mkdir(parents=True, exist_ok=True)
    mpath = root/"deck"/"manifest.json"; man = json.loads(mpath.read_text())
    prev = next((c for c in man["cards"] if c["id"] == cid or c["index"] == o.nn), {})
    depth = dict(DEFAULT_DEPTH, **{k: v["depth"] for k, v in man.get("layers", {}).items() if "depth" in v})
    if (raw/"depth.json").exists(): depth.update(json.loads((raw/"depth.json").read_text()))
    layers, files = {}, {}
    for n in MOVING:
        p = raw/f"{n}.png"
        if not p.exists(): files[n] = None; continue
        im = Image.open(p)
        im = im.convert("RGBA") if n == "bg" else cutout(im, o.key)
        if n == "bg": im.putalpha(255)
        im = cover(im, LAYER2X); layers[n] = im; save(im, out, n); files[n] = n
        need = 1 + 2*abs(depth[n])*AMPLITUDE
        if need > OVERSCAN: print(f"WARN {n}: depth {depth[n]} needs overscan {need:.3f} > {OVERSCAN}, the viewer will zoom the layer")
        print(f"{n}: {p.name} -> {LAYER2X} / {LAYER1X}")
    if (raw/"frame.png").exists():
        fr = Image.open(raw/"frame.png").convert("RGBA").resize(CANVAS, Image.LANCZOS)
    else:
        d = v1_frame_dir(root, cid)
        if not d: raise SystemExit("no frame.png and no v1 frame for " + cid)
        fr = Image.open(d/"frame@2x.webp" if (d/"frame@2x.webp").exists() else d/"frame.webp").convert("RGBA").resize(CANVAS, Image.LANCZOS)
    save(fr, out, "frame"); files["frame"] = "frame"
    thumb(layers, fr).save(out/"thumb.webp", "WEBP", quality=82); files["thumb"] = "thumb"
    entry = {"id": cid, "index": o.nn, "title": prev.get("title", cid[3:].replace("-", " ").upper()), "suit": prev.get("suit"),
             "files": files, "depth": {k: depth[k] for k in MOVING}, "rect": {k: OVERSCAN for k in MOVING}}
    (out/"card.json").write_text(json.dumps(dict(entry, layerSize={"@2x": LAYER2X, "@1x": LAYER1X}, amplitude=AMPLITUDE), indent=1, ensure_ascii=False))
    man["cards"] = sorted([c for c in man["cards"] if c["index"] != o.nn] + [entry], key=lambda c: c["index"])
    mpath.write_text(json.dumps(man, indent=1, ensure_ascii=False)); print("ok", cid)

if __name__ == "__main__": main()
