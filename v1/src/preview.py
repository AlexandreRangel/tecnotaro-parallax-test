#!/usr/bin/env python3
"""Flat preview (preview.png) and motion preview (preview.mp4) with strong tilts; same rules as index.html:
offset = tilt(-1..1) * depth * window width, on both axes. mid is the zero plane."""
import pathlib, math, subprocess, json, numpy as np
from PIL import Image, ImageChops, ImageDraw
D = pathlib.Path(__file__).resolve().parent.parent; L = D/"layers"
man = json.loads((D/"manifest.json").read_text()); DEPTH = {l["name"]: l["depth"] for l in man["layers"]}
S = 0.5; W, H = 1120, 1920; WX, WY, WW, WH = [round(v*S) for v in (181, 374, 1892, 3090)]
fr, bg, mid, fg = (Image.open(L/f"{n}@1x.png").convert("RGBA") for n in ("frame", "bg", "mid", "fg"))
def comp(x, y):
    win = Image.new("RGBA", (WW, WH), (0, 0, 0, 255))
    ox, oy = (bg.width-WW)/2, (bg.height-WH)/2
    win.alpha_composite(bg, (round(-ox+x*DEPTH["bg"]*WW), round(-oy+y*DEPTH["bg"]*WW)))
    win.alpha_composite(mid, (round(x*DEPTH["mid"]*WW), round(y*DEPTH["mid"]*WW)))
    f = Image.new("RGBA", (WW, WH)); f.paste(fg, (round(x*DEPTH["fg"]*WW), round(y*DEPTH["fg"]*WW)))
    a = np.asarray(f).astype(np.float32); pm = Image.fromarray((a[..., :3]*a[..., 3:]/255).astype(np.uint8))
    w = ImageChops.screen(win.convert("RGB"), pm).convert("RGBA")
    card = Image.new("RGBA", (W, H), (0, 0, 0, 255)); card.paste(w, (WX, WY)); card.alpha_composite(fr)
    return card.convert("RGB")
if __name__ == "__main__":
    comp(0, 0).save(D/"preview.png")
    fd = D/"tmp_frames"; fd.mkdir(exist_ok=True); N = 150
    for i in range(N):
        t = i/N*2*math.pi
        im = comp(math.sin(t), math.sin(2*t)).resize((560, 960), Image.LANCZOS)   # full +-1 tilts (strongest allowed)
        ImageDraw.Draw(im).text((12, 940), f"tilt x {math.sin(t):+.2f}  y {math.sin(2*t):+.2f}", fill=(255, 255, 255))
        im.save(fd/f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-i", str(fd/"%03d.png"), "-vf", "loop=1:150:0",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(D/"preview.mp4")], check=True)
    for p in fd.iterdir(): p.unlink()
    fd.rmdir(); print("ok")
