#!/usr/bin/env python3
from pathlib import Path
import shutil, subprocess, re, base64

root = Path(".")
html = root / "index.html"
t = html.read_text()

src = root / "icon-180.png"
dst = root / "icon-home.png"
if src.exists() and not dst.exists():
    try:
        subprocess.check_call([
            "convert", str(src),
            "-gravity", "center", "-crop", "78x86%+0+0", "+repage",
            "-resize", "180x180!",
            str(dst),
        ])
    except Exception:
        shutil.copy(src, dst)

def decode_banner():
    jpg = root / "title-banner.jpg"
    b64p = root / "title-banner.b64"
    if b64p.exists():
        raw = re.sub(r"\s+", "", b64p.read_text())
        raw += "=" * ((4 - len(raw) % 4) % 4)
        if raw and raw != "PLACEHOLDER" and len(raw) > 200:
            try:
                data = base64.b64decode(raw, validate=False)
                if data[:2] == b"\xff\xd8" and len(data) > 4000:
                    jpg.write_bytes(data)
                    return jpg
            except Exception:
                pass
    svg = root / "title-banner.svg"
    if svg.exists() and (not jpg.exists() or jpg.stat().st_size < 4000):
        try:
            subprocess.check_call([
                "convert", "-background", "#160808", str(svg),
                "-resize", "960x280", "-quality", "80", str(jpg),
            ])
        except Exception:
            pass
    return jpg if jpg.exists() and jpg.stat().st_size > 4000 else None

jpg = decode_banner()

css = '''
html,body{max-width:none!important}
body{padding:0!important;max-width:none!important;margin:0!important}
body.form-ninja,body.form-samurai{background:var(--bg)!important}
body.form-ninja .dd-btn,body.form-ninja .dd-list{border:1px solid #3d7eff!important}
body.form-samurai .dd-btn,body.form-samurai .dd-list{border:1px solid #c43a3a!important}
.hero{margin:0 -12px;padding:calc(8px + env(safe-area-inset-top,0px)) 0 0;text-align:center;background:transparent;border:0!important;box-shadow:none;position:relative;overflow:hidden}
.hero::after{content:"";position:absolute;left:0;right:0;bottom:0;height:56px;background:linear-gradient(180deg,rgba(22,8,8,0),#160808);pointer-events:none}
.hero img{display:block!important;width:100%;max-width:none!important;height:auto;max-height:none!important;object-fit:cover;margin:0 auto;border:0;background:transparent}
.hero h1,.brush-title{display:none!important}
.hero .ver{display:block;position:relative;z-index:1;margin:-6px 0 4px;color:#c4a050;letter-spacing:.16em}
.sheet{min-height:100vh;background:radial-gradient(ellipse at 50% 0%,rgba(170,18,18,.42),transparent 58%),linear-gradient(180deg,#160808 0%,#070707 100%);border:0;border-radius:0;box-shadow:none;padding:0 12px calc(20px + env(safe-area-inset-bottom,0px))}
.card{background:transparent!important;border:0!important;border-radius:0!important;margin:0!important;box-shadow:none!important}
.card + .card{border-top:0!important}
.legal{font-size:.62rem;color:#8a7040;text-align:center;padding:16px 8px 8px;line-height:1.4}
input[type=range]{-webkit-appearance:none!important;appearance:none;height:4px;background:#4a3a28;border-radius:4px}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;width:22px;height:22px;border-radius:50%;background:#e8c56a;border:0}
body.form-ninja input[type=range]{background:#1d3a6e}
body.form-ninja input[type=range]::-webkit-slider-thumb{background:#4d8dff}
body.form-samurai input[type=range]{background:#5a1c1c}
body.form-samurai input[type=range]::-webkit-slider-thumb{background:#e04a4a}
.statrow{grid-template-columns:52px 32px 1fr 32px 118px!important;align-items:center}
.statrow .side{display:flex;flex-direction:column;align-items:flex-end;justify-content:center;gap:2px;min-width:0}
.statrow .lab{color:#e8c56a!important;font-size:16px!important;font-weight:700!important;text-align:right;line-height:1.15}
.needhint{grid-column:auto!important;font-size:11px!important;color:#a88a48!important;margin:0!important;text-align:right;line-height:1.2;font-weight:400!important;max-width:118px}
.pm{width:32px;height:32px;border:2px solid #c4a050!important;background:transparent!important;color:#e8c56a!important;border-radius:8px;box-sizing:border-box}
body.form-ninja .pm{border-color:#3d7eff!important;color:#8ab4ff!important}
body.form-samurai .pm{border-color:#c43a3a!important;color:#e08a8a!important}
'''
t = re.sub(r"/\* n3-chrome \*/.*?/\* /n3-chrome \*/", "", t, flags=re.S)
t = t.replace("</style>", "/* n3-chrome */" + css + "/* /n3-chrome */\n</style>")

for old in [
    'href="icon.svg"','href="icon-v3.svg"','href="icon-brushed.svg"',
    'href="icon-180.png"','href="icon-home.png?v=083"','href="icon-home.png?v=084"',
    'href="icon-home.png?v=085"','href="icon-home.png?v=086"','href="icon-home.png?v=087"',
    'href="icon-home.png?v=088"',
]:
    t = t.replace(old, 'href="icon-home.png?v=089"')

banner_src = "title-banner.jpg" if jpg is not None else "title-banner.svg"
hero = '<div class="sheet"><header class="hero"><img src="'+banner_src+'?v=089" alt="Nioh 3 Equipment Builder"><span class="ver">v0.8.9</span></header>'
t = re.sub(r'(?:<div class="sheet">)?<header class="hero">.*?</header>', hero, t, count=1, flags=re.S)
t = t.replace('<h1>Nioh 3 Equipment Builder <span class="ver">v0.8.1</span></h1>', hero)
t = re.sub(r'v0\.8\.[0-9]', 'v0.8.9', t)

t = t.replace(
    '<span class="lab">${lab}</span></div>\n       <div class="needhint" data-need="${k}"></div>`',
    '<div class="side"><span class="lab">${lab}</span><div class="needhint" data-need="${k}"></div></div></div>`'
)

legal = '<p class="legal">Unofficial fan-made tool. Not affiliated with Team Ninja, Koei Tecmo, or Nioh 3. All game names and terms belong to their owners.</p>'
if "Unofficial fan-made tool" not in t:
    t = t.replace("\n<script>", legal + "\n<script>", 1)

html.write_text(t)
man = root / "manifest.json"
if man.exists():
    man.write_text(man.read_text().replace("icon.svg","icon-home.png").replace("icon-v3.svg","icon-home.png").replace("icon-180.png","icon-home.png"))
print("patched", "banner", jpg.stat().st_size if jpg and jpg.exists() else 0)
