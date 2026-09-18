#!/usr/bin/env python3
"""Force the 0.8.5-style CSS title, gold labels, and borderless +/- buttons."""
from pathlib import Path
import re

root = Path(".")
html = root / "index.html"
t = html.read_text()

# Strip any previous chrome override
t = re.sub(r"/\* n3-chrome \*/.*?/\* /n3-chrome \*/", "", t, flags=re.S)

css = r'''
.hero{margin:0!important;padding:calc(10px + env(safe-area-inset-top,0px)) 8px 2px!important;text-align:center!important;background:transparent!important;border:0!important;box-shadow:none!important;position:relative!important;overflow:visible!important}
.hero::after{display:none!important;content:none!important;background:none!important;height:0!important}
.hero img{display:none!important;width:0!important;height:0!important;max-height:0!important}
.hero h1,.brush-title{display:block!important;margin:0!important;padding:4px 0 0!important;font-family:Palatino,"Palatino Linotype",Georgia,"Times New Roman",serif!important;font-size:44px!important;font-weight:700!important;letter-spacing:.14em!important;color:#e8c56a!important;text-transform:uppercase!important;line-height:1!important;text-shadow:0 2px 18px rgba(160,20,16,.4)!important}
.brush-title small{display:block!important;margin:10px 0 0!important;font-size:13px!important;font-weight:600!important;letter-spacing:.32em!important;color:#d4b060!important}
.hero .ver{display:block!important;position:static!important;margin:12px 0 4px!important;font-size:.68rem!important;font-weight:600!important;letter-spacing:.16em!important;color:#c4a050!important;text-transform:none!important}
.statrow .lab{color:#e8c56a!important;font-size:16px!important;font-weight:700!important}
.needhint{font-size:11px!important;color:#c4a050!important;font-weight:400!important}
.pm{width:28px!important;height:28px!important;border:0!important;border-radius:8px!important;background:#1a0e0e!important;color:#e8c56a!important;box-shadow:none!important}
body.form-ninja .pm,body.form-samurai .pm{border:0!important;background:#1a0e0e!important;color:#e8c56a!important}
'''

t = t.replace("</style>", "/* n3-chrome */" + css + "/* /n3-chrome */\n</style>")

hero = '''<header class="hero">
  <div class="brush-title">Nioh 3<small>Equipment Builder</small></div>
  <span class="ver">v0.9.1</span>
</header>'''
t2, n = re.subn(r'<header class="hero">.*?</header>', hero, t, count=1, flags=re.S)
if n == 1:
    t = t2

t = re.sub(r'v0\.8\.[0-9]', 'v0.9.1', t)
t = re.sub(r'v0\.9\.[0-9]', 'v0.9.1', t)

html.write_text(t)
print("patched", html.stat().st_size, "header_replaced", n)
