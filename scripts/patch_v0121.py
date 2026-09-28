#!/usr/bin/env python3
"""v0.12.1 follow-up: park Level stats, bump version, add dropdown knobs."""
from pathlib import Path
import re

p = Path("index.html")
if not p.exists():
    raise SystemExit("index.html missing")
t = p.read_text(encoding="utf-8")

t = t.replace("v0.12.0", "v0.12.1")
t = t.replace("tune.css?v=012\"", "tune.css?v=0121\"")
t = t.replace("title-banner.png?v=012", "title-banner.png?v=0121")

t = re.sub(
    r'    pushStat\("Life", "Constitution: Life \+"\+n3val\(char\.con,"conLife"\);[\s\S]*?if\(sOn\) pushStat\("Utility", "Stamina: Samurai Weight Limit \+"\+n3val\(char\.sta,"staSamWt"\)\+" \(total "\+core\.wlim\+"\)"\);',
    "    /* level-derived core stats parked */",
    t,
    count=1,
)
t = re.sub(
    r'    pushStat\("Life", "Constitution: Life \+"\+\(char\.con\*40\);[\s\S]*?if\(sOn\) pushStat\("Utility", "Stamina: Weight Limit "\+\(20\+char\.sta\*1\.1\)\.toFixed\(1\)\);',
    "    /* level-derived core stats parked */",
    t,
    count=1,
)

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
print("postpatched v0.12.1", p.stat().st_size)
if "level-derived core stats parked" not in t:
    raise SystemExit("failed to park Level Life lines")
if "--n3-drop-max" not in t:
    raise SystemExit("dropdown knobs missing")
