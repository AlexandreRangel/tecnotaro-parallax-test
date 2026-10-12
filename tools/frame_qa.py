#!/usr/bin/env python3
"""Frame invariance QA. Renders every card at the neutral pose and at the four max tilt corners
(and the 4 axis extremes) in headless Chromium, with the whole-card rotation off (?cardtilt=0),
and checks that every pixel where the frame is opaque is identical to the neutral render.
usage: frame_qa.py BASE_URL DECK_DIR [cards e.g. 0-77] ; exits 1 on any mismatch."""
import sys, io, json, pathlib, numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
base, deck = sys.argv[1].rstrip('/'), pathlib.Path(sys.argv[2])
man = json.loads((deck.parent/'manifest.json').read_text()) if (deck.parent/'manifest.json').exists() else json.loads((deck/'manifest.json').read_text())
cards = man['cards']
if len(sys.argv) > 3: a, b = map(int, sys.argv[3].split('-')); cards = [c for c in cards if a <= c['index'] <= b]
POSES = [(1,1),(-1,-1),(1,-1),(-1,1),(1,0),(-1,0),(0,1),(0,-1)]
HIDE = "#top,#bot,#status,#err,#dbg,#msg,#start,#hud{display:none!important}"
fails = []
with sync_playwright() as p:
    br = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--force-device-scale-factor=1'])
    pg = br.new_page(viewport={'width': 560, 'height': 960})
    def shot(c, pose):
        pg.goto(f"{base}{'' if base.endswith('.html') else '/'}?pose={pose[0]},{pose[1]}&cardtilt=0#{c['index']:02d}")
        pg.add_style_tag(content=HIDE)
        pg.wait_for_function("(id)=>{var c=document.getElementById('card');var im=[...c.querySelectorAll('img:not(.empty)')];return c&&getComputedStyle(c).opacity=='1'&&im.every(i=>i.src&&i.complete&&i.naturalWidth>0)&&im[0].src.indexOf(id)>=0}", arg=c['id'], timeout=20000)
        pg.wait_for_timeout(450)
        return np.asarray(Image.open(io.BytesIO(pg.locator('#card').screenshot())).convert('RGB')).astype(int)
    for c in cards:
        ref = shot(c, (0, 0)); h, w = ref.shape[:2]
        fa = Image.open(deck/c['id']/'frame.webp').getchannel('A').resize((w, h), Image.BILINEAR)
        from PIL import ImageFilter
        opaque = np.asarray(fa.filter(ImageFilter.MinFilter(3))) >= 250
        worst = 0
        for pose in POSES:
            d = np.abs(shot(c, pose) - ref).max(2)[opaque]
            n = int((d > 2).sum()); worst = max(worst, n)
            if n: fails.append((c['id'], pose, n, int(d.max())))
        print(f"{c['id']}: frame px checked {int(opaque.sum())}, worst changed px {worst}", flush=True)
    br.close()
print("FAIL" if fails else "PASS: frame region identical at all max tilt poses", len(fails))
for f in fails[:40]: print(f)
sys.exit(1 if fails else 0)
