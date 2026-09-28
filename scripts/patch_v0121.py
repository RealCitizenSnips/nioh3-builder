#!/usr/bin/env python3
"""v0.12.1 follow-up: park Level stats, bump version, add dropdown knobs."""
from pathlib import Path

p = Path("index.html")
if not p.exists():
    raise SystemExit("index.html missing")
t = p.read_text(encoding="utf-8")

t = t.replace("v0.12.0", "v0.12.1")
t = t.replace('tune.css?v=012"', 'tune.css?v=0121"')
t = t.replace("title-banner.png?v=012", "title-banner.png?v=0121")

KILL = (
    'pushStat("Life", "Constitution: Life +',
    'pushStat("Life", "Heart: Life +',
    'pushStat("Life", "Stamina: Life +',
    'pushStat("Life", "Strength: Life +',
    'pushStat("Life", "Skill: Life +',
    'pushStat("Life", "Intellect: Life +',
    'pushStat("Life", "Magic: Life +',
    'pushStat("Life", "Level: Life +',
    'pushStat("Melee", "Heart / Strength / Intellect: Melee Attack +',
    'pushStat("Melee", "Heart / Strength / Magic: Melee Attack +',
    'pushStat("Ki", "Heart: Ki +',
    'pushStat("Ki", "Heart: Ki Recovery Speed +',
    'pushStat("Ki", "Intellect: Ki Recovery Speed +',
    'pushStat("Ki", "Heart & Intellect: Ki Recovery Speed +',
    'pushStat("Ki Damage",',
    'pushStat("Ninjutsu", "Skill: Ninjutsu Power +',
    'pushStat("Arts", "Skill: Arts Proficiency Power +',
    'pushStat("Onmyo", "Magic: Onmyo Magic Power +',
    'pushStat("Elemental", "Intellect: Effect Duration +',
    'pushStat("Utility", "Stamina: Weight Limit "',
    'pushStat("Utility", "Stamina: Ninja Weight Limit +',
    'pushStat("Utility", "Stamina: Samurai Weight Limit +',
)

out = []
parked = False
for line in t.splitlines(True):
    if any(s in line for s in KILL):
        if not parked:
            out.append("    /* level-derived core stats parked */\n")
            parked = True
        continue
    out.append(line)
t = "".join(out)

extra = (
    ".dd-list{max-height:var(--n3-drop-max,340px)!important}\n"
    ".dd-list,.dd-list .dd-item,.dd-list .dd-name,.dd-list .dd-set,"
    ".dd-list .dd-tiers,.dd-list .dd-tiers li,.dd-list .wt{"
    "font-size:var(--n3-dd-text,var(--n3-drop,var(--n3-text,16px)))!important}\n"
    ".wchip{font-size:var(--n3-wchip,13px)!important;"
    "padding:var(--n3-wchip-pad,7px 12px)!important;line-height:1.2!important}\n"
    ".needhint,.needhint.bad{display:none!important}\n"
)
if "--n3-drop-max" not in t:
    t = t.replace("/* /n3-chrome */", extra + "/* /n3-chrome */", 1)

p.write_text(t, encoding="utf-8")
print("postpatched v0.12.1", p.stat().st_size, "parked", parked)
if "level-derived core stats parked" not in t:
    raise SystemExit("failed to park Level Life lines")
if "--n3-drop-max" not in t:
    raise SystemExit("dropdown knobs missing")
if "v0.12.1" not in t:
    raise SystemExit("version bump missing")
