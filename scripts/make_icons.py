#!/usr/bin/env python3
"""Create gray ? placeholder icons when the user has not dropped a file yet.
Does not overwrite an existing png/svg/jpg of the same stem.
"""
from pathlib import Path

ROOT = Path(".")
ICON_DIR = ROOT / "icons"
ICON_DIR.mkdir(exist_ok=True)

PLACEHOLDER = """<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 64 64\">
  <circle cx=\"32\" cy=\"32\" r=\"30\" fill=\"#3a3a3a\" stroke=\"#8a8a8a\" stroke-width=\"3\"/>
  <text x=\"32\" y=\"42\" text-anchor=\"middle\" font-family=\"Arial, Helvetica, sans-serif\"
        font-size=\"36\" font-weight=\"700\" fill=\"#c8c8c8\">?</text>
</svg>
"""

NAMES = [
    "placeholder",
    "stat-constitution", "stat-heart", "stat-stamina", "stat-strength",
    "stat-skill", "stat-intellect", "stat-magic",
    "slot-head", "slot-chest", "slot-arms", "slot-waist", "slot-feet",
    "slot-weapon", "slot-ranged", "slot-accessory",
    "weapon-tonfa", "weapon-dual-ninja-swords", "weapon-talons", "weapon-kusarigama",
    "weapon-ninja-sword", "weapon-hatchets", "weapon-splitstaff",
    "weapon-ninja-hoko-shield", "weapon-sword", "weapon-dual-swords",
    "weapon-spear", "weapon-odachi", "weapon-axe", "weapon-switchglaive",
    "weapon-cestuses", "weapon-hoko-shield", "weapon-bow", "weapon-rifle",
    "weapon-hand-cannon",
]

made = 0
kept = 0
for name in NAMES:
    exists = any((ICON_DIR / f"{name}{ext}").exists() for ext in (".png", ".svg", ".jpg", ".jpeg", ".webp"))
    dest = ICON_DIR / f"{name}.svg"
    if exists:
        kept += 1
        continue
    dest.write_text(PLACEHOLDER, encoding="utf-8")
    made += 1
print(f"icons: wrote {made} placeholders, kept {kept} existing")
