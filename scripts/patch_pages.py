#!/usr/bin/env python3
from pathlib import Path
import shutil, subprocess, re, base64

root = Path(".")
html = root / "index.html"
t = html.read_text()

src = root / "icon-180.png"
dst = root / "icon-home.png"
if src.exists():
    try:
        subprocess.check_call([
            "convert", str(src),
            "-gravity", "center",
            "-crop", "78x86%+0+0",
            "+repage",
            "-resize", "180x180!",
            "-modulate", "112,180,100",
            "-sigmoidal-contrast", "6x50%",
            "-sharpen", "0x1.3",
            str(dst),
        ])
    except Exception:
        if not dst.exists():
            shutil.copy(src, dst)

b64p = root / "title-banner.b64"
if b64p.exists():
    raw = re.sub(r"\s+", "", b64p.read_text())
    (root / "title-banner.jpg").write_bytes(base64.b64decode(raw))

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

css = '''
html,body{max-width:none!important}
body{padding:0!important;max-width:none!important;margin:0!important}
body.form-ninja,body.form-samurai{background:var(--bg)!important}
body.form-ninja .dd-btn,body.form-ninja .dd-list{border:1px solid #3d7eff!important}
body.form-samurai .dd-btn,body.form-samurai .dd-list{border:1px solid #c43a3a!important}
.hero{margin:0;padding:calc(8px + env(safe-area-inset-top,0px)) 4px 0;text-align:center;background:transparent;border:0!important;box-shadow:none}
.hero img{display:block;width:100%;max-width:560px;height:auto;max-height:168px;object-fit:contain;margin:0 auto;mix-blend-mode:normal!important;border:0}
.hero h1,.brush-title{display:none!important}
.hero .ver{display:block;margin:2px 0 4px;color:#c4a050}
.sheet{min-height:100vh;background:radial-gradient(ellipse at 50% 0%,rgba(170,18,18,.42),transparent 58%),linear-gradient(180deg,#160808 0%,#070707 100%);border:0;border-radius:0;box-shadow:none;padding:0 12px calc(20px + env(safe-area-inset-bottom,0px))}
.card{background:transparent!important;border:0!important;border-radius:0!important;margin:0!important;border-top:0!important;border-bottom:1px solid rgba(212,168,80,.18)!important}
.legal{font-size:.62rem;color:#8a7040;text-align:center;padding:16px 8px 8px;line-height:1.4}
input[type=range]{-webkit-appearance:none!important;appearance:none;height:4px;background:#4a3a28;border-radius:4px}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;width:22px;height:22px;border-radius:50%;background:#e8c56a;border:0}
body.form-ninja input[type=range]{background:#1d3a6e}
body.form-ninja input[type=range]::-webkit-slider-thumb{background:#4d8dff}
body.form-samurai input[type=range]{background:#5a1c1c}
body.form-samurai input[type=range]::-webkit-slider-thumb{background:#e04a4a}
.statrow{grid-template-columns:52px 28px 1fr 28px 112px!important;align-items:center}
.statrow .side{display:flex;flex-direction:column;align-items:flex-end;justify-content:center;gap:1px;min-width:0}
.statrow .lab{color:#e8c56a!important;font-size:.95rem!important;font-weight:650!important;text-align:right;line-height:1.15}
.needhint{grid-column:auto!important;font-size:.72rem!important;color:#c4a050!important;margin:0!important;text-align:right;line-height:1.2;font-weight:500}
.pm{border:1px solid #c4a050!important;background:transparent!important;color:#e8c56a!important;border-radius:8px}
body.form-ninja .pm{border-color:#3d7eff!important;color:#8ab4ff!important}
body.form-samurai .pm{border-color:#c43a3a!important;color:#e08a8a!important}
'''
if "max-height:168px" not in t:
    t = t.replace("</style>", css + "\n</style>")

for old in ['href="icon.svg"','href="icon-v3.svg"','href="icon-brushed.svg"','href="icon-180.png"','href="icon-home.png?v=083"','href="icon-home.png?v=084"','href="icon-home.png?v=085"']:
    t = t.replace(old, 'href="icon-home.png?v=086"')

hero = '<div class="sheet"><header class="hero"><img src="title-banner.jpg" alt="Nioh 3 Equipment Builder"><span class="ver">v0.8.6</span></header>'
t = re.sub(r'(?:<div class="sheet">)?<header class="hero">.*?</header>', hero, t, count=1, flags=re.S)
t = t.replace('<h1>Nioh 3 Equipment Builder <span class="ver">v0.8.1</span></h1>', hero)
t = re.sub(r'v0\.8\.[0-9]', 'v0.8.6', t)

t = t.replace(
    '<span class="lab">${lab}</span></div>\n       <div class="needhint" data-need="${k}"></div>`',
    '<div class="side"><span class="lab">${lab}</span><div class="needhint" data-need="${k}"></div></div></div>`'
)

legal = '<p class="legal">Unofficial fan-made tool. Not affiliated with Team Ninja, Koei Tecmo, or Nioh 3. All game names and terms belong to their owners.</p>'
if "Unofficial fan-made tool" not in t:
    t = t.replace("\n<script>", legal + "\n<script>", 1)
if t.count('<div class="sheet">') >= 1 and "\n<script>" in t and "</div>\n<script>" not in t:
    t = t.replace("\n<script>", "\n</div>\n<script>", 1)

html.write_text(t)
man = root / "manifest.json"
if man.exists():
    man.write_text(man.read_text().replace("icon.svg","icon-home.png").replace("icon-v3.svg","icon-home.png").replace("icon-180.png","icon-home.png"))
print("patched")
