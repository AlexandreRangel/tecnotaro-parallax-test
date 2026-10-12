#!/usr/bin/env python3
"""Contact sheets per batch: qa/sheet-mid-AA-BB.jpg and qa/sheet-comp-AA-BB.jpg (comp = tilt -1 | rest | +1)."""
import sys, glob, pathlib
from PIL import Image, ImageDraw
D = pathlib.Path(__file__).resolve().parent.parent/"qa"
def sheet(kind, lo, hi, cols, tw):
    fs = [f for i in range(lo, hi+1) for f in glob.glob(str(D/f"{i:02d}-*-{kind}.jpg"))]
    if not fs: return
    ims = [Image.open(f) for f in fs]; r = tw/ims[0].width; th = int(ims[0].height*r)
    s = Image.new("RGB", (cols*tw, -(-len(ims)//cols)*(th+16)), (30, 30, 30))
    for k, (f, im) in enumerate(zip(fs, ims)):
        x, y = (k % cols)*tw, (k//cols)*(th+16); s.paste(im.resize((tw, th)), (x, y+16))
        ImageDraw.Draw(s).text((x+4, y+2), pathlib.Path(f).name[:-len(kind)-5], fill=(255, 220, 120))
    out = D/f"sheet-{kind}-{lo:02d}-{hi:02d}.jpg"; s.save(out, quality=82); print(out)
lo, hi = int(sys.argv[1]), int(sys.argv[2])
sheet("mid", lo, hi, 7, 180); sheet("comp", lo, hi, 3, 420)
