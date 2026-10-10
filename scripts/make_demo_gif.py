"""Record docs/demo.gif from the demo page (docs/index.html). No model needed.

Plays the first case twice: with no defence (money reaches the attacker),
then with the provenance defence (blocked). Run it again if the demo
cases change.

Needs: pip install playwright pillow and a Chromium (playwright install
chromium; an existing one at /opt/pw-browsers/chromium is used if present)

Run:  python scripts/make_demo_gif.py
"""

import argparse
import io
import os
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser()
ap.add_argument("--page", default=str(ROOT / "docs/index.html"))
ap.add_argument("--out", default=str(ROOT / "docs/demo.gif"))
args = ap.parse_args()
page_path, out = args.page, args.out
chromium = "/opt/pw-browsers/chromium"
frames = []  # (image, duration ms)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=chromium if os.path.exists(chromium) else None)
    pg = b.new_page(viewport={'width': 1000, 'height': 2400})
    pg.emulate_media(color_scheme='light')
    pg.goto('file://' + page_path); pg.wait_for_timeout(800)
    def clip():
        top = pg.eval_on_selector('#d-none', 'e => e.closest("div").getBoundingClientRect().top + scrollY') - 16
        bot = pg.eval_on_selector('#outcome', 'e => e.getBoundingClientRect().bottom + scrollY') + 24
        return {'x': 0, 'y': top, 'width': 1000, 'height': bot - top}
    def grab(ms):
        frames.append((Image.open(io.BytesIO(pg.screenshot(clip=clip()))).convert('RGB'), ms))
    for btn in ('#d-none', '#d-prov'):
        pg.click(btn); pg.wait_for_timeout(300)
        pg.click('#replay')
        for _ in range(16):   # steps appear 450 ms apart
            pg.wait_for_timeout(225); grab(225)
        pg.wait_for_timeout(400); grab(3500)  # hold on the outcome
    b.close()
H = max(f.height for f, _ in frames); W = 680
imgs = []
for f, _ in frames:
    canvas = Image.new('RGB', (1000, H), f.getpixel((2, 2)))  # pad with the page background
    canvas.paste(f, (0, 0))
    imgs.append(canvas.resize((W, round(H * W / 1000)), Image.LANCZOS))
pal = [im.quantize(colors=128, method=Image.Quantize.MEDIANCUT) for im in imgs]
pal[0].save(out, save_all=True, append_images=pal[1:], duration=[d for _, d in frames], loop=0, optimize=True)
print(len(frames), 'frames', imgs[0].size)
