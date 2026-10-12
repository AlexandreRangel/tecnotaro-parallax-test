#!/usr/bin/env python3
"""Tecnotaro parallax test v2, card 00 The Fool: depth bands.
  frame (fixed) | bg = far city+sky, moves most, opposite | mid = figure + ground strip + contact shadows, ZERO plane (anchor)
  | fg = sparse neon particles, small move the other way.
Source: approved card window pixels. Figure: rembg (isnet-general-use). bg: figure removed, multi-scale inpaint + borrowed
texture, overscanned 10%. Output: 2240x3840 card-space layers (frame) and window-space layers, @1x and @2x."""
import pathlib, json, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter
from rembg import remove, new_session
D = pathlib.Path(__file__).resolve().parent.parent; T = D.parent/"tecnotaro"; L = D/"layers"; L.mkdir(exist_ok=True)
W, H = 2240, 3840; WX, WY, WW, WH = 181, 374, 1892, 3090   # window: 113,234,1182x1931 CSS x1.6
OV = 1.10
GROUND_TOP, GROUND_FULL = 0.655, 0.745        # ground strip: feather from GROUND_TOP to opaque at GROUND_FULL (fraction of window h)
card = Image.open(T/"cartas/en/00-the-fool.png").convert("RGB")
art = card.crop((WX, WY, WX+WW, WY+WH)); A = np.asarray(art).astype(np.float32)
# 1 frame
fa = np.asarray(Image.open(T/"moldura/moldura-7x12-4k.png").getchannel("A")).copy(); fa[fa < 8] = 0
frame = card.copy(); frame.putalpha(Image.fromarray(fa)); frame.save(L/"frame.png")
# figure mask (man + dog)
sess = new_session("isnet-general-use")
small = art.resize((WW//2, WH//2), Image.LANCZOS)
m = np.asarray(remove(small, session=sess, only_mask=True, post_process_mask=True)).astype(np.float32)/255
x0, y0 = int(small.width*0.42), int(small.height*0.62)
md = np.asarray(remove(small.crop((x0, y0, small.width, int(small.height*0.90))), session=sess, only_mask=True, post_process_mask=True)).astype(np.float32)/255
m[y0:y0+md.shape[0], x0:] = np.maximum(m[y0:y0+md.shape[0], x0:], md)
m = np.clip((cv2.GaussianBlur(m, (0, 0), 0.8)-0.15)/0.7, 0, 1)
M = cv2.resize(m, (WW, WH), interpolation=cv2.INTER_CUBIC).clip(0, 1)
# 2 mid: figure + ground strip, with baked contact shadows
yy = np.arange(WH)[:, None]/WH
g = np.clip((yy-GROUND_TOP)/(GROUND_FULL-GROUND_TOP), 0, 1); g = g*g*(3-2*g); g = np.broadcast_to(g, (WH, WW))
sh = Image.new("L", (WW, WH)); sd = ImageDraw.Draw(sh)
B = M > 0.5; cols = np.where(B.any(0))[0]; bot = np.array([np.where(B[:, c])[0].max() if B[:, c].any() else 0 for c in range(WW)])
contacts = []
for c0, c1 in [(0, int(WW*0.47)), (int(WW*0.47), WW)]:       # man (left), dog (right)
    seg = np.arange(c0, c1); seg = seg[bot[seg] > WH*0.7]
    if not len(seg): continue
    yb = bot[seg].max(); feet = seg[bot[seg] > yb-WH*0.05]       # columns touching the floor
    # one ellipse per contiguous run (each boot / paw)
    runs = np.split(feet, np.where(np.diff(feet) > 12)[0]+1)
    for r in runs:
        if len(r) < 10: continue
        cy = bot[r].max(); cx = (r[0]+r[-1])/2; rw = (r[-1]-r[0])/2*1.25+20
        sd.ellipse((cx-rw, cy-rw*0.22, cx+rw, cy+rw*0.22), fill=200); contacts.append([int(cx), int(cy)])
    sd.ellipse((seg.min()-30, yb-40, seg.max()+30, yb+50), fill=90)  # wider soft ambient shadow
sh = np.asarray(sh.filter(ImageFilter.GaussianBlur(22))).astype(np.float32)/255
shadow = 1-0.55*sh*(1-M)                                            # darken floor only, never the figure
mid_rgb = A*shadow[..., None]
mid_a = np.maximum(M, g)
mid = Image.fromarray(np.dstack([mid_rgb, mid_a*255]).clip(0, 255).astype(np.uint8), "RGBA"); mid.save(L/"mid.png")
# 3 bg: remove figure with large dilation (covers bells glow and boot marks), coarse-to-fine inpaint + borrowed texture
hole = (M > 0.02).astype(np.uint8)*255
hole = cv2.dilate(hole, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (121, 121)))
# extra hand-placed cleanups: bell glows near the hat, dark marks around the boots
for (cx, cy, r) in [(0.36, 0.165, 70), (0.66, 0.235, 70), (0.30, 0.86, 140), (0.60, 0.88, 110)]:
    cv2.circle(hole, (int(cx*WW), int(cy*WH)), r, 255, -1)
bgr = cv2.cvtColor(A.astype(np.uint8), cv2.COLOR_RGB2BGR); fill = None
for s in (16, 8, 4):
    sm = cv2.resize(bgr, (WW//s, WH//s), interpolation=cv2.INTER_AREA); hm = cv2.resize(hole, (WW//s, WH//s)) > 0
    if fill is not None:
        sm[hm] = cv2.resize(fill, (WW//s, WH//s))[hm]
        hm = cv2.erode(hm.astype(np.uint8), np.ones((3, 3))) > 0     # keep coarse result, refine only the core
    fill = cv2.inpaint(sm, hm.astype(np.uint8)*255, 6, cv2.INPAINT_NS)
fill = cv2.cvtColor(cv2.resize(fill, (WW, WH), interpolation=cv2.INTER_CUBIC), cv2.COLOR_BGR2RGB).astype(np.float32)
fill = cv2.GaussianBlur(fill, (0, 0), 6)
# borrowed texture: high-pass detail (rain, window lights) from the left and right edges of the same rows
hp = (A - cv2.GaussianBlur(A, (0, 0), 8)) * (cv2.erode(255-hole, np.ones((41, 41))) > 0)[..., None]   # detail only from clean pixels
tex = np.zeros_like(A); half = WW//2
for sh_ in (0.40, 0.48, 0.33):   # first non-empty source wins per pixel
    cand = np.zeros_like(A); cand[:, :half] = np.roll(hp, -int(WW*sh_), axis=1)[:, :half]; cand[:, half:] = np.roll(hp, int(WW*sh_), axis=1)[:, half:]
    empty = (np.abs(tex).sum(2, keepdims=True) == 0); tex = np.where(empty, cand, tex)
hb = cv2.GaussianBlur(hole.astype(np.float32)/255, (0, 0), 25)[..., None]
bg = A*(1-hb) + (fill + 0.8*tex)*hb
BW, BH = round(WW*OV), round(WH*OV)
I = 60   # rounded frame corners: inset crop so no brass leaks in
bg = Image.fromarray(bg.clip(0, 255).astype(np.uint8)).crop((I, I, WW-I, WH-I)).resize((BW, BH), Image.LANCZOS); bg.save(L/"bg.png")
# 4 fg: sparse particles and corner wisps (screen blend), face kept clear
rng = np.random.default_rng(0)
fgc = Image.new("RGB", (WW, WH)); dr = ImageDraw.Draw(fgc)
colors = [(255, 40, 200), (40, 230, 255), (255, 170, 40)]; face = (WW*0.38, WH*0.10, WW*0.75, WH*0.36)
for i in range(38):
    x, y = rng.uniform(0, WW), rng.uniform(0, WH)
    if face[0] < x < face[2] and face[1] < y < face[3]: continue
    r = rng.uniform(3, 11); dr.ellipse((x-r, y-r, x+r, y+r), fill=colors[i % 3])
def wisp(x0, y0, sx, sy, c, n=3):
    for k in range(n):
        t = np.linspace(0, 1, 200); dr.line(list(zip(x0+sx*t+40*np.sin(t*7+k), y0+sy*t+30*np.cos(t*5+k*2))), fill=c, width=5-k)
wisp(-40, WH*0.97, WW*0.38, -WH*0.16, colors[0]); wisp(WW+40, WH*0.80, -WW*0.30, WH*0.14, colors[1]); wisp(-20, WH*0.05, WW*0.22, WH*0.10, colors[2], 2)
gl = np.clip(np.asarray(fgc.filter(ImageFilter.GaussianBlur(18))).astype(np.float32)*1.8 + np.asarray(fgc.filter(ImageFilter.GaussianBlur(2.5))).astype(np.float32)*0.9, 0, 255)
al = gl.max(2); rgb = np.where(al[..., None] > 0, gl/np.maximum(al[..., None], 1)*255, 0)
Image.fromarray(np.dstack([rgb, al*0.85]).clip(0, 255).astype(np.uint8), "RGBA").save(L/"fg.png")
# halo budget: smallest distance between the figure edge and the edge of the inpainted hole (px, window space)
dist = cv2.distanceTransform((M < 0.02).astype(np.uint8), cv2.DIST_L2, 5)
margin = float(dist[(hole > 0) & (dist > 0) & (cv2.dilate(hole, np.ones((3, 3))) > 0) & (cv2.erode(hole, np.ones((3, 3))) == 0)].min())
(L/"layout.json").write_text(json.dumps(dict(card=[W, H], window=[WX, WY, WW, WH], overscan=OV, ground=[GROUND_TOP, GROUND_FULL],
                                              contacts=contacts, halo_margin_px=margin), indent=1))
for n in ["frame", "bg", "mid", "fg"]:
    im = Image.open(L/f"{n}.png"); im.resize((im.width//2, im.height//2), Image.LANCZOS).save(L/f"{n}@1x.png")
    im.save(L/f"{n}@2x.webp", quality=88); im.resize((im.width//2, im.height//2), Image.LANCZOS).save(L/f"{n}.webp", quality=88)
print("ok contacts", contacts, "halo margin px", margin)
