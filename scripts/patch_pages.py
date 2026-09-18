#!/usr/bin/env python3
from pathlib import Path
import base64, subprocess, sys

root = Path(".")
html = root / "index.html"
t = html.read_text()

t = t.replace("--bg:#000;", "--bg:#070707;")
t = t.replace("--card:rgba(28,28,30,.92);", "--card:transparent;")
t = t.replace("--ink:#f5f5f7;", "--ink:#e8c56a;")
t = t.replace("--muted:#8e8e93;", "--muted:#c4a050;")
t = t.replace("--line:rgba(255,255,255,.08);", "--line:rgba(212,168,80,.18);")
t = t.replace("--fill:#1c1c1e;", "--fill:#120808;")
t = t.replace("--btn:#2c2c2e;", "--btn:#1a0e0e;")
t = t.replace("--accent:#0a84ff;", "--accent:#e8c56a;")

sheet_css = """.sheet{background:radial-gradient(ellipse at 50% 0%,rgba(170,18,18,.42),transparent 58%),linear-gradient(180deg,#160808 0%,#070707 100%);border:1px solid rgba(212,168,80,.28);border-radius:16px;box-shadow:inset 0 -24px 40px rgba(40,0,0,.35);overflow:visible;padding:0 10px 12px}.card{background:transparent!important;border:0!important;border-radius:0!important;margin:0!important;border-bottom:1px solid rgba(212,168,80,.18)!important;backdrop-filter:none!important}.hero{margin:0;padding:10px 10px 4px;text-align:center;background:transparent;border:0;box-shadow:none}.hero img{display:block;width:100%;max-height:148px;object-fit:contain;margin:0 auto}.hero .ver{display:block;margin:2px 0 8px;color:#c4a050}\n"""
if ".sheet{" not in t:
    t = t.replace("</style>", sheet_css + "\n</style>")

for old in ['href="icon.svg"','href="icon-v3.svg"','href="icon-brushed.svg"','href="icon-180.png?v=082"','href="icon-180.png"']:
    t = t.replace(old, 'href="icon-home.png?v=083"')

hero = '<div class="sheet"><header class="hero"><h1>Nioh 3 Equipment Builder</h1><img src="title-banner.jpg" alt="Nioh 3 Equipment Builder"><span class="ver">v0.8.3</span></header>'
t = t.replace('<header class="hero"><h1>Nioh 3 Equipment Builder</h1><span class="ver">v0.8.2</span></header>', hero)
t = t.replace('<h1>Nioh 3 Equipment Builder <span class="ver">v0.8.1</span></h1>', hero)
if t.count('<div class="sheet">') == 1 and '\n<script>' in t and '</div>\n<script>' not in t:
    t = t.replace('\n<script>', '\n</div>\n<script>', 1)

html.write_text(t)

b64 = root / "title-banner.b64"
if b64.exists():
    (root / "title-banner.jpg").write_bytes(base64.b64decode(b64.read_text().strip()))

try:
    from PIL import Image
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow", "-q"])
    from PIL import Image

src_path = root / "icon-180.png"
if src_path.exists():
    im = Image.open(src_path).convert("RGB")
    w, h = im.size
    px = im.load()
    l, top, r, btm = w, h, 0, 0
    for y in range(h):
        for x in range(w):
            p = px[x, y]
            s = p[0] + p[1] + p[2]
            if s > 50 and not (p[0] > 230 and p[1] > 230 and p[2] > 230):
                l = min(l, x); top = min(top, y); r = max(r, x); btm = max(btm, y)
    if r > l and btm > top:
        cut = im.crop((l, top, r + 1, btm + 1))
        side = max(cut.size)
        canvas = Image.new("RGB", (side, side), (8, 8, 8))
        canvas.paste(cut, ((side - cut.size[0]) // 2, (side - cut.size[1]) // 2))
        canvas.resize((180, 180), Image.Resampling.LANCZOS).save(root / "icon-home.png", "PNG")
    else:
        im.resize((180, 180), Image.Resampling.LANCZOS).save(root / "icon-home.png", "PNG")
print("patched")
