#!/usr/bin/env python3
"""v0.9.5 UI overlay. Does not change gear catalog data."""
from pathlib import Path
import base64
import re
import sys

ROOT = Path(".")
INDEX = ROOT / "index.html"
if not INDEX.exists():
    sys.exit("index.html missing — nothing to patch")

t = INDEX.read_text(encoding="utf-8")
t = re.sub(r"/\* n3-chrome \*/.*?/\* /n3-chrome \*/", "", t, flags=re.S)

# Always emit the transparent brush PNG from the text payload so the
# hero never falls back to SVG/CSS title text.
b64_path = ROOT / "scripts" / "title-banner.png.b64"
if b64_path.exists():
    png = base64.b64decode(re.sub(r"\s+", "", b64_path.read_text()))
    (ROOT / "title-banner.png").write_bytes(png)

SET_COLORS = {
    "kato": "#7ec8e3",
    "iga": "#9ad27a",
    "fuma": "#c9a0e8",
    "onzoshi": "#e3b36a",
    "lastNinja": "#e08a8a",
    "kusaMaster": "#8fd0c0",
    "heizo": "#d0c07a",
    "blessed": "#8ab4e8",
    "gallant": "#d4a0c0",
    "kobo": "#b8d48a",
    "exalted": "#e0c070",
    "priest": "#c8c0a8",
    "sage": "#a8c8b8",
    "demonHorde": "#d08070",
    "moon": "#a0b8e0",
    "brave": "#d09060",
    "crimson": "#e07070",
    "eccentric": "#c0a070",
    "firstCap": "#90c0d0",
    "goi": "#b090d0",
    "hachiryo": "#d0b070",
    "monk": "#90c090",
    "brother": "#d0a080",
    "swallow": "#e8c07a",
    "woe": "#d4c06a",
    "tatenashi": "#c8b090",
    "kamakura": "#90b8d0",
    "shuri": "#b09070",
    "buddha": "#e0d0a0",
    "minamoto": "#80c0c8",
    "hollyhock": "#e090b0",
    "righteous": "#a0d090",
    "lilac": "#c090d8",
    "tigerKai": "#e07040",
    "tamura": "#d0a060",
    "malefactor": "#c06070",
    "kintaro": "#e0b050",
    "retreat": "#70b0a0",
    "peerless": "#90c0a8",
    "swordmaster": "#c0c090",
    "wayfarer": "#a8b8c8",
    "gunner": "#8aa0b8",
    "grace": "#8ee08a",
}
set_css = []
for name, color in SET_COLORS.items():
    sel = f".pill.set-{name},.dd-name.set-{name},.dd-btn.set-{name},.dd-set.set-{name},.dd-item .set-{name}"
    set_css.append(f"{sel}{{color:{color}!important}}")
set_css.append(
    ".dd-name.set-grace,.dd-btn.set-grace,.pill.set-grace,.dd-set.set-grace"
    "{color:#8ee08a!important}"
)
set_block = "\n".join(set_css)

css = r"""
html{color-scheme:only dark;-webkit-text-size-adjust:100%;text-size-adjust:100%}
html,body{max-width:none!important;color:#e8c56a!important;background-color:#160808!important}
html,body,body.form-ninja,body.form-samurai,.sheet,#app{
  background-color:#160808!important;
  background-image:radial-gradient(ellipse at 50% 0%,rgba(170,18,18,.42),transparent 58%),linear-gradient(180deg,#160808 0%,#070707 100%)!important;
  background-attachment:fixed!important;
}
body{margin:0!important;padding:0!important;font-size:16px!important;line-height:1.35!important;color:#e8c56a!important}
.card{background:transparent!important;border:0!important;border-radius:0!important;box-shadow:none!important;backdrop-filter:none!important;margin:0!important;padding:14px 12px 12px!important}
.card + .card{border-top:1px solid rgba(212,168,80,.16)!important}
h1,.brush-title{display:none!important}
.hero{margin:0!important;padding:calc(8px + env(safe-area-inset-top,0px)) 8px 4px!important;text-align:center!important;background:transparent!important;border:0!important}
.hero::after{display:none!important}
.hero img{display:block!important;width:100%!important;max-width:640px!important;height:auto!important;max-height:168px!important;object-fit:contain!important;object-position:center center!important;margin:0 auto!important;border:0!important;background:transparent!important}
.hero .ver,.ver{display:block!important;margin:6px auto 8px!important;font-size:.68rem!important;font-weight:600!important;letter-spacing:.16em!important;color:#c4a050!important}
h2,.slot>span{font-size:.68rem!important;letter-spacing:.06em!important;text-transform:uppercase!important;color:#c4a050!important;font-weight:600!important}
.dd-btn,.dd-name,.dd-item,.bonus,.bmain,.filters label,.tools button,
input[type=tel],.lvrow input,#lv-in,.locked,.live,.note,.mini label{
  font-size:16px!important
}
.filters label,.tools button,.bonus,.bmain,.locked,.live,.note,.mini label{
  color:#e8c56a!important
}
.statrow .lab{color:#e8c56a!important;font-size:16px!important;font-weight:700!important;text-align:right!important}
.lvrow,.needhint,.needhint.bad{
  font-size:16px!important;line-height:1.35!important;font-weight:400!important;
  -webkit-text-size-adjust:100%!important;text-size-adjust:100%!important
}
.lvrow,.needhint{color:#c4a050!important}
.needhint.bad{color:#e07070!important}
.pm{width:28px!important;height:28px!important;border:0!important;border-radius:8px!important;background:#1a0e0e!important;color:#e8c56a!important;box-shadow:none!important}
body.form-ninja .pm,body.form-samurai .pm{border:0!important;background:#1a0e0e!important;color:#e8c56a!important}
.filters label,.pill,.tools button,.dd-btn{background:#1a0e0e!important}
.dd-btn,.dd-list{border:0 solid transparent!important}
body.form-ninja .dd-btn,body.form-ninja .dd-list{border:2px solid #3d7eff!important}
body.form-samurai .dd-btn,body.form-samurai .dd-list{border:2px solid #c43a3a!important}
input[type=tel],.lvrow input,#lv-in{background:#1a0e0e!important;color:#e8c56a!important;border:0!important}
input[type=range]{-webkit-appearance:none!important;appearance:none;height:4px;background:#4a3a28;border-radius:4px;accent-color:#e8c56a}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;width:22px;height:22px;border-radius:50%;background:#e8c56a;border:0}
body.form-ninja input[type=range]{background:#1d3a6e;accent-color:#4d8dff}
body.form-ninja input[type=range]::-webkit-slider-thumb{background:#4d8dff}
body.form-samurai input[type=range]{background:#5a1c1c;accent-color:#e04a4a}
body.form-samurai input[type=range]::-webkit-slider-thumb{background:#e04a4a}
.filters input[type=checkbox]{
  -webkit-appearance:none!important;appearance:none!important;
  width:16px!important;height:16px!important;margin:0!important;
  border:2px solid #c4a050!important;border-radius:4px!important;
  background:#1a0e0e!important;accent-color:#e8c56a!important;
  display:inline-grid!important;place-content:center!important;
  flex:0 0 16px!important
}
.filters input[type=checkbox]:checked{
  background:#e8c56a!important;border-color:#e8c56a!important
}
.filters input[type=checkbox]:checked::after{
  content:"\u2713"!important;color:#1a0e0e!important;font-size:12px!important;
  font-weight:800!important;line-height:1!important
}
.legal{display:block!important;font-size:.62rem!important;color:#a88848!important;text-align:center;padding:16px 8px 24px;line-height:1.4}
""" + set_block

if "</style>" not in t:
    sys.exit("no style tag")
t = t.replace("</style>", "/* n3-chrome */" + css + "/* /n3-chrome */\n</style>", 1)

# Status bar / Safari chrome: dark red, draw under the notch.
t = t.replace(
    'content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no"',
    'content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover"',
)
t = t.replace('content="#0d2b4a"', 'content="#160808"')
if 'name="theme-color" content="#160808"' in t and 'prefers-color-scheme' not in t:
    t = t.replace(
        '<meta name="theme-color" content="#160808">',
        '<meta name="theme-color" content="#160808">\n'
        '<meta name="theme-color" content="#160808" media="(prefers-color-scheme: light)">\n'
        '<meta name="theme-color" content="#160808" media="(prefers-color-scheme: dark)">',
    )

hero = '''<header class="hero">
  <img src="title-banner.png?v=095" alt="Nioh 3 Equipment Builder">
  <span class="ver">v0.9.5</span>
</header>'''

if re.search(r'<header class="hero">', t):
    t = re.sub(r'<header class="hero">.*?</header>', hero, t, count=1, flags=re.S)
elif re.search(r"<h1>.*?</h1>", t, flags=re.S):
    t = re.sub(r"<h1>.*?</h1>", hero, t, count=1, flags=re.S)
else:
    t = t.replace("<body>", "<body>\n" + hero, 1)

# Never leave an SVG/text title in the hero.
t = t.replace("title-banner.svg", "title-banner.png")
t = re.sub(r"v0\.9\.[0-4]\b", "v0.9.5", t)

t = t.replace(">Empty all gear<", ">Reset All<")
t = t.replace('confirm("Empty all gear?")', 'confirm("Reset All?")')
t = t.replace(
    "Switching Form will reset all selections below, continue?",
    "Switching Style will clear all Equipment. Continue?",
)

legal = (
    '<p class="legal">Unofficial fan-made tool. Not affiliated with Team Ninja, '
    "Koei Tecmo, or Nioh 3. All game names and terms belong to their owners.</p>"
)
if "Unofficial fan-made tool" not in t:
    if "<script>" in t:
        t = t.replace("<script>", legal + "\n<script>", 1)
    else:
        t = t.replace("</body>", legal + "\n</body>")

INDEX.write_text(t, encoding="utf-8")
print("patched v0.9.5", INDEX.stat().st_size)
