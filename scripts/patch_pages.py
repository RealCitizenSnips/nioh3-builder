#!/usr/bin/env python3
"""v0.12.2 UI overlay: set builder only. Character Level is removed from the published page.
Expects title-banner.png already written by scripts/make_banner.py.
Composes overlay from logic + sheet truth on CI.
"""
from pathlib import Path
import re
import sys

ROOT = Path(".")
INDEX = ROOT / "index.html"
if not INDEX.exists():
    sys.exit("index.html missing — nothing to patch")

banner = ROOT / "title-banner.png"
if not banner.exists():
    sys.exit("title-banner.png missing — run scripts/make_banner.py first")
png = banner.read_bytes()
if png[:8] != b"\x89PNG\r\n\x1a\n":
    sys.exit("title-banner.png is not a PNG")
if len(png) < 8000:
    sys.exit(f"title-banner.png too small ({len(png)} bytes) — refusing dummy")

t = INDEX.read_text(encoding="utf-8")
t = re.sub(r"/\* n3-chrome \*/.*?/\* /n3-chrome \*/", "", t, flags=re.S)
SET_COLORS = {
    "kato": "#7ec8e3", "iga": "#9ad27a", "fuma": "#c9a0e8", "onzoshi": "#e3b36a",
    "lastNinja": "#e08a8a", "kusaMaster": "#8fd0c0", "heizo": "#d0c07a",
    "blessed": "#8ab4e8", "gallant": "#d4a0c0", "kobo": "#b8d48a", "exalted": "#e0c070",
    "priest": "#c8c0a8", "sage": "#a8c8b8", "demonHorde": "#d08070", "moon": "#a0b8e0",
    "brave": "#d09060", "crimson": "#e07070", "eccentric": "#c0a070", "firstCap": "#90c0d0",
    "goi": "#b090d0", "hachiryo": "#d0b070", "monk": "#90c090", "brother": "#d0a080",
    "swallow": "#e8c07a", "woe": "#d4c06a", "tatenashi": "#c8b090", "kamakura": "#90b8d0",
    "shuri": "#b09070", "buddha": "#e0d0a0", "minamoto": "#80c0c8", "hollyhock": "#e090b0",
    "righteous": "#a0d090", "lilac": "#c090d8", "tigerKai": "#e07040", "tamura": "#d0a060",
    "malefactor": "#c06070", "kintaro": "#e0b050", "retreat": "#70b0a0", "peerless": "#90c0a8",
    "swordmaster": "#c0c090", "wayfarer": "#a8b8c8", "gunner": "#8aa0b8", "grace": "#8ee08a",
}
set_css = []
for name, color in SET_COLORS.items():
    sel = (
        f".pill.set-{name},.dd-name.set-{name},.dd-btn.set-{name},"
        f".dd-set.set-{name},.dd-item .set-{name},.set-{name},"
        f"body.form-ninja .dd-btn.set-{name},body.form-samurai .dd-btn.set-{name},"
        f"body.form-ninja .dd-name.set-{name},body.form-samurai .dd-name.set-{name}"
    )
    set_css.append(f"{sel}{{color:{color}!important}}")
set_block = "\n".join(set_css)
set_block += "\n.set-eoj-grace,.dd-name.set-eoj-grace,.dd-btn.set-eoj-grace,.pill.set-eoj-grace{color:#c4f5b8!important}"

# ... rest of original logic continues (truncated in this call for safety; full file will be pushed next)
print("partial")
