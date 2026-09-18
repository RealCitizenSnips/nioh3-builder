#!/usr/bin/env python3
"""Turn whatever index.html is in the repo into the 0.8.5 red/gold phone UI."""
from pathlib import Path
import re

html = Path("index.html")
t = html.read_text()
t = re.sub(r"/\* n3-chrome \*/.*?/\* /n3-chrome \*/", "", t, flags=re.S)

css = r'''
html,body{max-width:none!important;background:#070707!important}
body{margin:0!important;padding:0!important;color:#e8c56a!important}
body.form-ninja,body.form-samurai{background:#070707!important}
.sheet,body{background:radial-gradient(ellipse at 50% 0%,rgba(170,18,18,.42),transparent 58%),linear-gradient(180deg,#160808 0%,#070707 100%)!important}
.card{background:transparent!important;border:0!important;border-radius:0!important;box-shadow:none!important;backdrop-filter:none!important;margin:0!important;padding:14px 12px 12px!important}
.card + .card{border-top:1px solid rgba(212,168,80,.16)!important}
h1{display:none!important}
.hero{margin:0!important;padding:calc(14px + env(safe-area-inset-top,0px)) 8px 6px!important;text-align:center!important;background:transparent!important;border:0!important}
.hero img{display:none!important}
.hero::after{display:none!important}
.brush-title{display:block!important;margin:0!important;font-family:Palatino,"Palatino Linotype",Georgia,"Times New Roman",serif!important;font-size:44px!important;font-weight:700!important;letter-spacing:.14em!important;color:#e8c56a!important;text-transform:uppercase!important;line-height:1!important;text-shadow:0 2px 18px rgba(160,20,16,.4)!important}
.brush-title small{display:block!important;margin:10px 0 0!important;font-size:13px!important;font-weight:600!important;letter-spacing:.32em!important;color:#d4b060!important}
.hero .ver,.ver{display:block!important;margin:12px auto 4px!important;font-size:.68rem!important;font-weight:600!important;letter-spacing:.16em!important;color:#c4a050!important}
.statrow .lab{color:#e8c56a!important;font-size:16px!important;font-weight:700!important;text-align:right!important}
.needhint{font-size:11px!important;color:#c4a050!important;font-weight:400!important}
.pm{width:28px!important;height:28px!important;border:0!important;border-radius:8px!important;background:#1a0e0e!important;color:#e8c56a!important;box-shadow:none!important}
body.form-ninja .pm,body.form-samurai .pm{border:0!important;background:#1a0e0e!important;color:#e8c56a!important}
h2{color:#c4a050!important}
.filters label,.pill,.tools button,.dd-btn{background:#1a0e0e!important;color:#e8c56a!important}
input[type=tel],.lvrow input,#lv-in{background:#1a0e0e!important;color:#e8c56a!important;border:0!important}
input[type=range]{-webkit-appearance:none!important;appearance:none;height:4px;background:#4a3a28;border-radius:4px}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;width:22px;height:22px;border-radius:50%;background:#e8c56a;border:0}
body.form-ninja input[type=range]{background:#1d3a6e}
body.form-ninja input[type=range]::-webkit-slider-thumb{background:#4d8dff}
body.form-samurai input[type=range]{background:#5a1c1c}
body.form-samurai input[type=range]::-webkit-slider-thumb{background:#e04a4a}
'''

if "</style>" not in t:
    raise SystemExit("no style tag")
t = t.replace("</style>", "/* n3-chrome */" + css + "/* /n3-chrome */\n</style>", 1)

hero = '''<header class="hero">
  <div class="brush-title">Nioh 3<small>Equipment Builder</small></div>
  <span class="ver">v0.9.1</span>
</header>'''

if re.search(r'<header class="hero">', t):
    t = re.sub(r'<header class="hero">.*?</header>', hero, t, count=1, flags=re.S)
elif re.search(r'<h1>.*?</h1>', t, flags=re.S):
    t = re.sub(r'<h1>.*?</h1>', hero, t, count=1, flags=re.S)
else:
    t = t.replace("<body>", "<body>\n" + hero, 1)

t = re.sub(r'v0\.8\.[0-9]', 'v0.9.1', t)
t = re.sub(r'v0\.9\.[0-9]', 'v0.9.1', t)

html.write_text(t)
print("patched", html.stat().st_size)
print("has brush-title", "brush-title" in t)
print("has n3-chrome", "n3-chrome" in t)
