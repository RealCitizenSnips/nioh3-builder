#!/usr/bin/env python3
from pathlib import Path
import base64, shutil, subprocess

root = Path(".")
html = root / "index.html"
t = html.read_text()

def join_b64(prefix, dest):
    parts = sorted(root.glob(f"assets/{prefix}-*.b64"))
    single = root / f"{prefix}.b64"
    data = "".join(p.read_text().strip() for p in parts) if parts else (single.read_text().strip() if single.exists() else "")
    if data:
        (root / dest).write_bytes(base64.b64decode(data))
        return True
    return False

join_b64("title-banner", "title-banner.jpg")
join_b64("icon-home", "icon-home.png")

src = root / "icon-180.png"
dst = root / "icon-home.png"
if src.exists():
    try:
        subprocess.check_call([
            "convert", str(src),
            "-gravity", "center",
            "-crop", "70x90%+0+0",
            "+repage",
            "-resize", "180x180^",
            "-gravity", "center",
            "-background", "#080808",
            "-extent", "180x180",
            str(dst),
        ])
    except Exception:
        if not dst.exists():
            shutil.copy(src, dst)

repls = [
    ('width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no"',
     'width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover"'),
    ("--bg:#000;", "--bg:#070707;"),
    ("--card:rgba(28,28,30,.92);", "--card:transparent;"),
    ("--ink:#f5f5f7;", "--ink:#e8c56a;"),
    ("--muted:#8e8e93;", "--muted:#c4a050;"),
    ("--line:rgba(255,255,255,.08);", "--line:rgba(212,168,80,.18);"),
    ("--fill:#1c1c1e;", "--fill:#120808;"),
    ("--btn:#2c2c2e;", "--btn:#1a0e0e;"),
    ("--accent:#0a84ff;", "--accent:#e8c56a;"),
    ('content="#0d2b4a"', 'content="#160808"'),
]
for a,b in repls:
    t = t.replace(a,b)

has_title = (root / "title-banner.jpg").exists()
title_img = '<img src="title-banner.jpg" alt="">' if has_title else ""
css = '''
@import url("https://fonts.googleapis.com/css2?family=Yuji+Boku&display=swap");
html,body{max-width:none!important}
body{padding:0!important;max-width:none!important;margin:0!important}
body.form-ninja,body.form-samurai{background:var(--bg)!important}
body.form-ninja input[type=range]{accent-color:#3d7eff}
body.form-samurai input[type=range]{accent-color:#c43a3a}
body.form-ninja .dd-btn,body.form-ninja .dd-list{border:1px solid #3d7eff}
body.form-samurai .dd-btn,body.form-samurai .dd-list{border:1px solid #c43a3a}
.hero{margin:0;padding:calc(12px + env(safe-area-inset-top,0px)) 12px 4px;text-align:center;background:transparent;border:0;box-shadow:none}
.hero img{display:block;width:92%;max-height:120px;object-fit:contain;margin:0 auto;mix-blend-mode:screen}
.hero h1{display:none!important}
.brush-title{font-family:"Yuji Boku",serif;color:#e8c56a;font-size:1.7rem;line-height:1.1;letter-spacing:.04em;text-shadow:0 0 18px rgba(160,20,20,.55);margin:0}
.brush-title small{display:block;font-size:1rem;margin-top:4px}
.hero .ver{display:block;margin:6px 0 8px;color:#c4a050}
.sheet{min-height:100vh;background:radial-gradient(ellipse at 50% 0%,rgba(170,18,18,.42),transparent 58%),linear-gradient(180deg,#160808 0%,#070707 100%);border:0;border-radius:0;box-shadow:none;padding:0 12px calc(20px + env(safe-area-inset-bottom,0px))}
.card{background:transparent!important;border:0!important;border-radius:0!important;margin:0!important;border-bottom:1px solid rgba(212,168,80,.18)!important}
.legal{font-size:.62rem;color:#8a7040;text-align:center;padding:16px 8px 8px;line-height:1.4}
'''
if has_title:
    css += ".brush-title{display:none!important}\n"
else:
    css += ".hero img{display:none!important}.brush-title{display:block!important}\n"
if "Yuji Boku" not in t:
    t = t.replace("</style>", css + "\n</style>")

for old in ['href="icon.svg"','href="icon-v3.svg"','href="icon-brushed.svg"','href="icon-180.png?v=082"','href="icon-180.png"','href="icon-home.png?v=083"']:
    t = t.replace(old, 'href="icon-home.png?v=085"')

hero = '<div class="sheet"><header class="hero">' + title_img + '<div class="brush-title">Nioh 3<small>Equipment Builder</small></div><span class="ver">v0.8.4</span></header>'
for old in [
    '<header class="hero"><h1>Nioh 3 Equipment Builder</h1><img src="title-banner.jpg" alt="Nioh 3 Equipment Builder"><span class="ver">v0.8.3</span></header>',
    '<header class="hero"><h1>Nioh 3 Equipment Builder</h1><span class="ver">v0.8.2</span></header>',
    '<h1>Nioh 3 Equipment Builder <span class="ver">v0.8.1</span></h1>',
]:
    t = t.replace(old, hero)

legal = '<p class="legal">Unofficial fan-made tool. Not affiliated with Team Ninja, Koei Tecmo, or Nioh 3. All game names and terms belong to their owners.</p>'
if "Unofficial fan-made tool" not in t:
    t = t.replace("\n<script>", legal + "\n<script>", 1)
if t.count('<div class="sheet">') >= 1 and "\n<script>" in t and "</div>\n<script>" not in t:
    t = t.replace("\n<script>", "\n</div>\n<script>", 1)

html.write_text(t)
man = root / "manifest.json"
if man.exists():
    man.write_text(man.read_text().replace("icon.svg", "icon-home.png").replace("icon-v3.svg", "icon-home.png").replace("icon-180.png", "icon-home.png"))
print("patched")
