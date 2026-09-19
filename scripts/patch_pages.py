#!/usr/bin/env python3
"""Revert deploy to the original builder. No theme, no banner overlay."""
from pathlib import Path
import re

p = Path("index.html")
t = p.read_text()
t = re.sub(r"/\* n3-chrome \*/.*?/\* /n3-chrome \*/", "", t, flags=re.S)
t = re.sub(
    r"<header class=\"hero\">.*?</header>",
    '<h1>Nioh 3 Equipment Builder <span class="ver">v0.8.2</span></h1>',
    t,
    count=1,
    flags=re.S,
)
t = re.sub(
    r"<h1>Nioh 3 Equipment Builder <span class=\"ver\">v0\.\d+\.\d+</span></h1>",
    '<h1>Nioh 3 Equipment Builder <span class="ver">v0.8.2</span></h1>',
    t,
    count=1,
)
p.write_text(t)
print("reverted to v0.8.2", p.stat().st_size)
