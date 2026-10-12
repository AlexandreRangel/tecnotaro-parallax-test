#!/usr/bin/env python3
"""Tecnotaro parallax, deck build (v3). One card per call: build_card.py NN [--force]
Depth bands: frame (fixed) | bg far (moves most, opposite) | mid = figure/emblem + ground anchor (depth 0) | fg sparse particles.
Ground edge per card: 'fade' (soft blend), 'hard' (cut along a real horizontal edge, with rim and lip shadow) or 'none' (emblems).
Writes deck/NN-slug/{frame,bg,mid,fg}.webp (@1x) and @2x.webp, card.json, plus qa/ jpgs. Skips cards already built."""
import sys, pathlib, json, glob, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter
D = pathlib.Path(__file__).resolve().parent.parent; T = D.parent/"tecnotaro"
W, H = 2240, 3840; WX, WY, WW, WH = 181, 374, 1892, 3090; OV = 1.10; INSET = 60
OVR = json.loads((D/"src/overrides.json").read_text())
SUIT_PAL = {"major": [(255, 40, 200), (40, 230, 255), (255, 170, 40)], "wands": [(255, 150, 30), (255, 90, 40), (255, 210, 120)],
            "cups": [(40, 230, 255), (255, 60, 210), (150, 120, 255)], "swords": [(120, 220, 255), (230, 245, 255), (60, 150, 255)],
            "coins": [(255, 200, 60), (120, 255, 160), (255, 120, 220)]}
SUITS = ["wands", "cups", "swords", "coins"]
def kind_of(i):
    if i < 22: return "major", "figure"
    s, r = SUITS[(i-22)//14], (i-22) % 14
    return s, ("emblem" if r < 10 else "figure")
_sess = None
def seg(img):
    global _sess
    from rembg import remove, new_session
    if _sess is None: _sess = new_session("isnet-general-use")
    return np.asarray(remove(img, session=_sess, only_mask=True, post_process_mask=True)).astype(np.float32)/255
def smooth(e0, e1, x): t = np.clip((x-e0)/np.maximum(e1-e0, 1e-6), 0, 1); return t*t*(3-2*t)

def build(idx, force=False):
    f = sorted(glob.glob(str(T/f"cartas/en/{idx:02d}-*.png")))[0]; name = pathlib.Path(f).stem
    out = D/"deck"/name; out.mkdir(parents=True, exist_ok=True)
    if (out/"card.json").exists() and not force: print("skip", name); return
    o = OVR.get(f"{idx:02d}", {}); pal, kind = kind_of(idx); kind = o.get("kind", kind)
    card = Image.open(f).convert("RGB"); art = card.crop((WX, WY, WX+WW, WY+WH)); A = np.asarray(art).astype(np.float32)
    # frame
    fa = np.asarray(Image.open(T/"moldura/moldura-7x12-4k.png").getchannel("A")).copy(); fa[fa < 8] = 0
    frame = card.copy(); frame.putalpha(Image.fromarray(fa))
    # mask: full pass + optional box passes, at half res
    sm = art.resize((WW//2, WH//2), Image.LANCZOS); sw, sh_ = sm.size
    m = seg(sm)
    for b in o.get("extra_boxes", []):
        x0, y0, x1, y1 = int(b[0]*sw), int(b[1]*sh_), int(b[2]*sw), int(b[3]*sh_)
        m[y0:y1, x0:x1] = np.maximum(m[y0:y1, x0:x1], seg(sm.crop((x0, y0, x1, y1))))
    for b in o.get("drop_boxes", []): m[int(b[1]*sh_):int(b[3]*sh_), int(b[0]*sw):int(b[2]*sw)] = 0
    for b in o.get("keep_boxes", []): m[int(b[1]*sh_):int(b[3]*sh_), int(b[0]*sw):int(b[2]*sw)] = 1
    # remove specks, keep components >0.3% of area
    bm = (m > 0.5).astype(np.uint8); n, lab, st, _ = cv2.connectedComponentsWithStats(bm)
    keep = np.isin(lab, [k for k in range(1, n) if st[k, cv2.CC_STAT_AREA] > 0.003*sw*sh_])
    keep = cv2.dilate(keep.astype(np.uint8), np.ones((9, 9))) > 0
    m = np.clip((cv2.GaussianBlur(m*keep, (0, 0), 0.8)-0.15)/0.7, 0, 1)
    M = cv2.resize(m, (WW, WH), interpolation=cv2.INTER_CUBIC).clip(0, 1)
    B = M > 0.5; rows = np.where(B.any(1))[0]
    foot = float(np.percentile(np.where(B)[0], 99.5))/WH if B.any() else 0.9
    # ground edge
    Lm = cv2.GaussianBlur(A @ np.array([.2126, .7152, .0722], np.float32), (0, 0), 3)
    G = np.abs(cv2.Sobel(Lm, cv2.CV_32F, 0, 1, ksize=5))
    ge = o.get("ground_edge"); ey = o.get("edge_y"); strength = None
    if kind == "emblem": ge = ge or "none"
    elif ge is None or ey is None:
        y0, y1 = int(WH*0.45), int(WH*min(foot-0.02, 0.90))
        if y1 > y0+50:
            free = cv2.dilate(B.astype(np.uint8), np.ones((31, 31))) == 0
            Gm = np.where(free, G, np.nan)[y0:y1, INSET:WW-INSET]
            score = np.nanmedian(Gm, 1); score = np.nan_to_num(score)
            k = int(np.argmax(score)); strength = float(score[k]/(np.median(score)+1e-3))
            ey = ey or (y0+k)/WH
            ge = ge or ("hard" if strength > 3.0 else "fade")
        else:
            ge = ge or "fade"; ey = ey or max(0.5, foot-0.17)
    ey = ey or 0.7
    yy = np.arange(WH, dtype=np.float32)[:, None]
    rim = np.zeros((WH, WW), np.float32); lip = np.zeros((WH, WW), np.float32)
    if ge == "none": g = np.zeros((WH, WW), np.float32)
    elif ge == "fade":
        span = o.get("fade_span", 0.09)*WH; g = np.broadcast_to(smooth(ey*WH-span/2, ey*WH+span/2, yy), (WH, WW)).astype(np.float32)
    else:   # hard: follow the real edge per column (strongest gradient within +-35 px), median-smoothed
        c = int(ey*WH); band = G[max(c-35, 0):c+35]
        ys = (np.argmax(band, 0)+max(c-35, 0)).astype(np.float32)
        ys = cv2.medianBlur(ys.astype(np.float32)[None, :].repeat(3, 0), 5)[1]
        ys = cv2.GaussianBlur(ys[None, :], (0, 0), 25)[0]
        g = smooth(ys[None, :]-1.5, ys[None, :]+1.5, yy).astype(np.float32)
        d = yy - ys[None, :]
        rim = np.exp(-((d-2)/2.5)**2).astype(np.float32)                    # thin light rim on the edge
        lip = np.where(d > 2, np.exp(-np.clip(d-2, 0, 200)/14), 0).astype(np.float32)      # short shadow just under the lip
        ey = float(np.median(ys)/WH)
    # ring: feather the figure into its surroundings (original pixels) so at rest nothing reveals the inpaint
    RING = 22
    dist = cv2.distanceTransform((M < 0.5).astype(np.uint8), cv2.DIST_L2, 5)
    ring = np.clip(1-dist/RING, 0, 1)**1.5*(M.max() > 0)
    # contact shadows (figures on ground)
    shd = np.zeros((WH, WW), np.float32); contacts = []
    if ge != "none" and kind == "figure":
        si = Image.new("L", (WW, WH)); sd = ImageDraw.Draw(si)
        bot = np.array([np.where(B[:, x])[0].max() if B[:, x].any() else 0 for x in range(WW)])
        feet = np.where(bot > max(ey*WH, foot*WH-0.05*WH))[0]
        if len(feet):
            for r in np.split(feet, np.where(np.diff(feet) > 12)[0]+1):
                if len(r) < 10: continue
                cy = bot[r].max(); cx = (r[0]+r[-1])/2; rw = (r[-1]-r[0])/2*1.25+20
                sd.ellipse((cx-rw, cy-rw*0.22, cx+rw, cy+rw*0.22), fill=190); contacts.append([int(cx), int(cy)])
            sd.ellipse((feet.min()-30, foot*WH-40, feet.max()+30, foot*WH+50), fill=80)
        shd = np.asarray(si.filter(ImageFilter.GaussianBlur(22))).astype(np.float32)/255
    mid_a = np.maximum(np.maximum(M, g), ring)
    mid_rgb = A*(1-0.55*shd*(1-M))[..., None]
    mid_rgb = mid_rgb*(1-0.35*lip*(1-M))[..., None] + 60*rim[..., None]*(1-M[..., None])
    mid = np.dstack([mid_rgb.clip(0, 255), mid_a*255]).astype(np.uint8)
    # bg: remove figure (dilated) + everything fully below a hard edge doesn't matter; multi-scale inpaint + borrowed texture
    hole = (M > 0.02).astype(np.uint8)*255
    hole = cv2.dilate(hole, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2*RING+15, 2*RING+15)))
    bgr = cv2.cvtColor(A.astype(np.uint8), cv2.COLOR_RGB2BGR); fill = None
    if hole.any():
        for s in (16, 8, 4):
            smi = cv2.resize(bgr, (WW//s, WH//s), interpolation=cv2.INTER_AREA); hm = cv2.resize(hole, (WW//s, WH//s)) > 0
            if fill is not None:
                smi[hm] = cv2.resize(fill, (WW//s, WH//s))[hm]; hm = cv2.erode(hm.astype(np.uint8), np.ones((3, 3))) > 0
            fill = cv2.inpaint(smi, hm.astype(np.uint8)*255, 6, cv2.INPAINT_NS)
        fill = cv2.GaussianBlur(cv2.cvtColor(cv2.resize(fill, (WW, WH), interpolation=cv2.INTER_CUBIC), cv2.COLOR_BGR2RGB).astype(np.float32), (0, 0), 6)
        hp = (A - cv2.GaussianBlur(A, (0, 0), 8))*(cv2.erode(255-hole, np.ones((41, 41))) > 0)[..., None]
        tex = np.zeros_like(A); half = WW//2
        for s_ in (0.40, 0.48, 0.33, 0.25):
            cand = np.zeros_like(A); cand[:, :half] = np.roll(hp, -int(WW*s_), 1)[:, :half]; cand[:, half:] = np.roll(hp, int(WW*s_), 1)[:, half:]
            tex = np.where(np.abs(tex).sum(2, keepdims=True) == 0, cand, tex)
        hb = cv2.GaussianBlur(hole.astype(np.float32)/255, (0, 0), 8)[..., None]
        bgA = A*(1-hb) + (fill+0.8*tex)*hb
    else: bgA = A
    hole_frac = float(((hole > 0) & (g < 0.99)).mean())
    # amplitude clamp: inpaint strip revealed = shift; allow RING + allowance that shrinks with hole size
    allowance = 40 if kind == "emblem" else (30 if hole_frac < 0.18 else 22 if hole_frac < 0.30 else 12)
    margin = RING + allowance
    bgd = round(min(o.get("bg_depth", 0.03 if kind == "emblem" else 0.025), margin*0.95/WW, 0.045), 4)
    bg = Image.fromarray(bgA.clip(0, 255).astype(np.uint8)).crop((INSET, INSET, WW-INSET, WH-INSET)).resize((round(WW*OV), round(WH*OV)), Image.LANCZOS)
    # fg: few particles, palette per suit, never over the mid figure (faces included)
    rng = np.random.default_rng(idx); cols = SUIT_PAL[pal]
    fgc = Image.new("RGB", (WW, WH)); dr = ImageDraw.Draw(fgc)
    avoid = cv2.dilate((M > 0.1).astype(np.uint8), np.ones((81, 81))) > 0
    n_p = int(rng.integers(18, 34)); placed = 0
    while placed < n_p:
        x, y = rng.uniform(0, WW), rng.uniform(0, WH)
        if avoid[int(y), int(x)]: continue
        r = rng.uniform(3, 10); dr.ellipse((x-r, y-r, x+r, y+r), fill=cols[placed % 3]); placed += 1
    for k in range(int(rng.integers(1, 3))):
        corner = rng.integers(0, 4); x0 = -40 if corner % 2 == 0 else WW+40; y0 = WH*(0.95 if corner < 2 else 0.06)
        sx = WW*rng.uniform(0.2, 0.35)*(1 if corner % 2 == 0 else -1); sy = WH*rng.uniform(0.08, 0.15)*(-1 if corner < 2 else 1)
        for j in range(3):
            t = np.linspace(0, 1, 200); dr.line(list(zip(x0+sx*t+40*np.sin(t*7+j), y0+sy*t+30*np.cos(t*5+j*2))), fill=cols[(k+j) % 3], width=5-j)
    fga = np.asarray(fgc).astype(np.float32); fga = fga*(1-avoid[..., None])  # wisps never over the figure either
    fgc = Image.fromarray(fga.astype(np.uint8))
    gl = np.clip(np.asarray(fgc.filter(ImageFilter.GaussianBlur(18))).astype(np.float32)*1.8 + np.asarray(fgc.filter(ImageFilter.GaussianBlur(2.5))).astype(np.float32)*0.9, 0, 255)
    al = gl.max(2); rgb = np.where(al[..., None] > 0, gl/np.maximum(al[..., None], 1)*255, 0)
    fg = Image.fromarray(np.dstack([rgb, al*0.85]).clip(0, 255).astype(np.uint8), "RGBA")
    layers = dict(frame=frame, bg=bg, mid=Image.fromarray(mid, "RGBA"), fg=fg)
    for n_, im in layers.items():
        im.save(out/f"{n_}@2x.webp", quality=86); im.resize((im.width//2, im.height//2), Image.LANCZOS).save(out/f"{n_}.webp", quality=84)
    meta = dict(id=name, index=idx, title=name[3:].replace("-", " ").upper(), suit=pal, kind=kind, ground_edge=ge,
                edge_y=None if ge == "none" else round(float(ey), 4), edge_strength=None if strength is None else round(strength, 2),
                foot_y=round(foot, 4), contacts=contacts, hole_frac=round(hole_frac, 3), halo_margin_px=margin,
                depth=dict(bg=-bgd, mid=0.0, fg=round(bgd*0.48, 4), frame=0.0))
    (out/"card.json").write_text(json.dumps(meta, indent=1))
    # qa: mid on checker, and composites at rest / strong tilts
    qa = D/"qa"; s = 0.25; w, h = int(WW*s), int(WH*s)
    chk = Image.fromarray(((((np.indices((h, w)).sum(0)//12) % 2)*60+60)).astype(np.uint8)).convert("RGBA")
    chk.alpha_composite(layers["mid"].resize((w, h))); chk.convert("RGB").save(qa/f"{name}-mid.jpg", quality=80)
    def comp(x, y):
        b = bg.resize((int(bg.width*s), int(bg.height*s))); win = Image.new("RGBA", (w, h), (0, 0, 0, 255))
        win.paste(b.convert("RGB"), (round(-(b.width-w)/2 - x*bgd*w), round(-(b.height-h)/2 - y*bgd*w)))
        win.alpha_composite(layers["mid"].resize((w, h)))
        fgs = fg.resize((w, h)); t = Image.new("RGBA", (w, h)); t.paste(fgs, (round(x*bgd*0.48*w), round(y*bgd*0.48*w))); win.alpha_composite(t)
        return win.convert("RGB")
    st = Image.new("RGB", (3*w+8, h)); [st.paste(comp(x, y), (i*(w+4), 0)) for i, (x, y) in enumerate([(-1, -1), (0, 0), (1, 1)])]
    st.save(qa/f"{name}-comp.jpg", quality=80)
    print("ok", name, ge, meta["edge_y"], meta["edge_strength"], "bg", -bgd, "hole", meta["hole_frac"], flush=True)

if __name__ == "__main__":
    force = "--force" in sys.argv
    for a in [x for x in sys.argv[1:] if not x.startswith("--")]:
        if "-" in a: lo, hi = map(int, a.split("-")); [build(i, force) for i in range(lo, hi+1)]
        else: build(int(a), force)
