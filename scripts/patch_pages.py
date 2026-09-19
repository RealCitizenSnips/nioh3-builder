#!/usr/bin/env python3
"""v0.9.4 UI-only overlay. Does not change gear data or JS."""
from pathlib import Path
import re

p = Path("index.html")
t = p.read_text()
t = re.sub(r"/\* n3-chrome \*/.*?/\* /n3-chrome \*/", "", t, flags=re.S)

css = r"""
html,body{max-width:none!important;color:#e8c56a!important}
html,body,body.form-ninja,body.form-samurai,.sheet{
  background:radial-gradient(ellipse at 50% 0%,rgba(170,18,18,.42),transparent 58%),linear-gradient(180deg,#160808 0%,#070707 100%)!important;
}
body{margin:0!important;padding:0!important;font-size:16px!important;line-height:1.35!important;color:#e8c56a!important}
.card{background:transparent!important;border:0!important;border-radius:0!important;box-shadow:none!important;backdrop-filter:none!important;margin:0!important;padding:14px 12px 12px!important}
.card + .card{border-top:1px solid rgba(212,168,80,.16)!important}
h1,.brush-title{display:none!important}
.hero{margin:0!important;padding:calc(10px + env(safe-area-inset-top,0px)) 8px 4px!important;text-align:center!important;background:transparent!important;border:0!important}
.hero::after{display:none!important}
.hero img{display:block!important;width:100%!important;max-width:640px!important;height:auto!important;max-height:150px!important;object-fit:contain!important;object-position:center center!important;margin:0 auto!important;border:0!important;background:transparent!important}
.hero .ver,.ver{display:block!important;margin:6px auto 8px!important;font-size:.68rem!important;font-weight:600!important;letter-spacing:.16em!important;color:#c4a050!important}
h2,.slot>span{font-size:.68rem!important;letter-spacing:.06em!important;text-transform:uppercase!important;color:#c4a050!important;font-weight:600!important}
.dd-btn,.dd-name,.dd-item,.bonus,.bmain,.pill,.filters label,.tools button,
input[type=tel],.lvrow input,#lv-in,.locked,.live,.note,.mini label{
  font-size:16px!important;color:#e8c56a!important
}
.statrow .lab{color:#e8c56a!important;font-size:16px!important;font-weight:700!important;text-align:right!important}
.needhint{font-size:11px!important;color:#c4a050!important;font-weight:400!important}
.pm{width:28px!important;height:28px!important;border:0!important;border-radius:8px!important;background:#1a0e0e!important;color:#e8c56a!important;box-shadow:none!important}
body.form-ninja .pm,body.form-samurai .pm{border:0!important;background:#1a0e0e!important;color:#e8c56a!important}
.filters label,.pill,.tools button,.dd-btn{background:#1a0e0e!important}
.dd-btn,.dd-list{border:0 solid transparent!important}
body.form-ninja .dd-btn,body.form-ninja .dd-list{border:2px solid #3d7eff!important}
body.form-samurai .dd-btn,body.form-samurai .dd-list{border:2px solid #c43a3a!important}
input[type=tel],.lvrow input,#lv-in{background:#1a0e0e!important;color:#e8c56a!important;border:0!important}
input[type=range]{-webkit-appearance:none!important;appearance:none;height:4px;background:#4a3a28;border-radius:4px}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;width:22px;height:22px;border-radius:50%;background:#e8c56a;border:0}
body.form-ninja input[type=range]{background:#1d3a6e}
body.form-ninja input[type=range]::-webkit-slider-thumb{background:#4d8dff}
body.form-samurai input[type=range]{background:#5a1c1c}
body.form-samurai input[type=range]::-webkit-slider-thumb{background:#e04a4a}
.legal{display:block!important;font-size:.62rem!important;color:#a88848!important;text-align:center;padding:16px 8px 24px;line-height:1.4}
.lvrow{color:#c4a050!important}
"""

if "</style>" not in t:
    raise SystemExit("no style tag")
t = t.replace("</style>", "/* n3-chrome */" + css + "/* /n3-chrome */\n</style>", 1)

hero = '''<header class="hero">
  <img src="title-banner.svg?v=094" alt="Nioh 3 Equipment Builder">
  <span class="ver">v0.9.4</span>
</header>'''

if re.search(r'<header class="hero">', t):
    t = re.sub(r'<header class="hero">.*?</header>', hero, t, count=1, flags=re.S)
elif re.search(r"<h1>.*?</h1>", t, flags=re.S):
    t = re.sub(r"<h1>.*?</h1>", hero, t, count=1, flags=re.S)
else:
    t = t.replace("<body>", "<body>\n" + hero, 1)

legal = '<p class="legal">Unofficial fan-made tool. Not affiliated with Team Ninja, Koei Tecmo, or Nioh 3. All game names and terms belong to their owners.</p>'
if "Unofficial fan-made tool" not in t:
    if "</script>" in t and t.rfind("<script>") > 0:
        t = t.replace("<script>", legal + "\n<script>", 1)
    else:
        t = t.replace("</body>", legal + "\n</body>")

p.write_text(t)
print("patched v0.9.4", p.stat().st_size)
