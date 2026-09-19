#!/usr/bin/env python3
"""Minimal deploy patch: banner IMAGE + the reported UI fixes only."""
from pathlib import Path
import base64, gzip, re

root = Path(".")
html_path = root / "index.html"
t = html_path.read_text() if html_path.exists() else ""

def join_b64(prefix: str):
    parts = sorted(root.glob(prefix + ".*"))
    blob = root / prefix
    raw = ""
    if parts:
        raw = "".join(p.read_text() for p in parts)
    elif blob.exists():
        raw = blob.read_text()
    else:
        return None
    raw = re.sub(r"\s+", "", raw)
    raw += "=" * ((4 - len(raw) % 4) % 4)
    try:
        return base64.b64decode(raw)
    except Exception:
        return None

ban = join_b64("title-banner.b64")
banner_src = "title-banner.svg"
if ban and ban[:2] == b"\xff\xd8" and len(ban) > 30000:
    (root / "title-banner.jpg").write_bytes(ban)
    banner_src = "title-banner.jpg?v=092"
    print("wrote banner jpg", len(ban))
elif (root / "title-banner.jpg").exists() and (root / "title-banner.jpg").stat().st_size > 30000:
    banner_src = "title-banner.jpg?v=092"

packed = join_b64("index.gz.b64") or join_b64("index.html.gz.b64")
if packed:
    if packed[:2] == b"\x1f\x8b":
        packed = gzip.decompress(packed)
    html_path.write_bytes(packed)
    t = packed.decode("utf-8", "replace")
    print("wrote packed index", len(packed))

t = re.sub(r"/\* n3-chrome \*/.*?/\* /n3-chrome \*/", "", t, flags=re.S)

css = """
.hero img{display:block!important;width:100%;max-width:640px;height:auto;max-height:168px;object-fit:contain!important;object-position:center center;margin:0 auto;border:0}
.hero h1,.brush-title{display:none!important}
.hero .ver{display:block;margin:4px 0 8px;color:#c4a050;letter-spacing:.16em;font-size:.68rem}
.lvrow{color:#c4a050!important;font-size:.78rem!important}
.needhint{font-size:10px!important;color:#c4a050!important;font-weight:400!important}
.pm{border:0!important}
.legal{display:block!important;font-size:.62rem;color:#a88848;text-align:center;padding:16px 8px 8px;line-height:1.4}
"""

if "</style>" in t:
    t = t.replace("</style>", "/* n3-chrome */" + css + "/* /n3-chrome */\n</style>", 1)

hero = f'''<header class="hero">
  <img src="{banner_src}" alt="Nioh 3 Equipment Builder">
  <span class="ver">v0.9.2</span>
</header>'''

if re.search(r'<header class="hero">', t):
    t = re.sub(r'<header class="hero">.*?</header>', hero, t, count=1, flags=re.S)
elif re.search(r'<h1>.*?</h1>', t, flags=re.S):
    t = re.sub(r'<h1>.*?</h1>', hero, t, count=1, flags=re.S)

if "Unofficial fan-made tool" not in t:
    legal = '<p class="legal">Unofficial fan-made tool. Not affiliated with Team Ninja, Koei Tecmo, or Nioh 3. All game names and terms belong to their owners.</p>'
    if "</body>" in t:
        t = t.replace("</body>", legal + "\n</body>", 1)
    else:
        t += legal

t = re.sub(r"v0\.9\.[0-9]", "v0.9.2", t)
html_path.write_text(t)
print("patched", html_path.stat().st_size, "banner", banner_src)
