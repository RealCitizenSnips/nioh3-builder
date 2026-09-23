#!/usr/bin/env python3
"""v0.10.0 UI overlay + Level-tab lookups + icon files + sheet names.
Expects title-banner.png already written by scripts/make_banner.py.
Expects scripts/overlay_v010.js (Level table + sheet truth).
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

css = r"""
html{color-scheme:only dark;-webkit-text-size-adjust:100%;text-size-adjust:100%}
html,body{max-width:none!important;color:#e8c56a!important;background-color:#160808!important}
html,body,body.form-ninja,body.form-samurai,.sheet,#app{
  background-color:#160808!important;
  background-image:radial-gradient(ellipse at 50% 0%,rgba(170,18,18,.42),transparent 58%),linear-gradient(180deg,#160808 0%,#070707 100%)!important;
  background-attachment:fixed!important;
}
body{margin:0!important;padding:0!important;font-size:16px!important;line-height:1.35!important;color:#e8c56a!important}
#boot-msg{display:none!important}
.card{background:transparent!important;border:0!important;border-radius:0!important;box-shadow:none!important;backdrop-filter:none!important;margin:0!important;padding:14px 12px 12px!important}
.card + .card{border-top:1px solid rgba(212,168,80,.16)!important}
h1,.brush-title,.brush-title .n,.brush-title .s{display:none!important}
.hero{margin:0!important;padding:calc(8px + env(safe-area-inset-top,0px)) 8px 2px!important;text-align:center!important;background:transparent!important;border:0!important}
.hero::after{display:none!important}
.hero img{display:block!important;width:92%!important;max-width:520px!important;height:auto!important;max-height:168px!important;object-fit:contain!important;object-position:center center!important;margin:0 auto!important;border:0!important;background:transparent!important}
.hero .ver,.ver{display:block!important;margin:4px auto 8px!important;font-size:.68rem!important;font-weight:600!important;letter-spacing:.16em!important;color:#c4a050!important}
.card > h2{
  font-size:24px!important;letter-spacing:.08em!important;text-transform:uppercase!important;
  color:#e8c56a!important;font-weight:700!important;line-height:1.2!important;margin:0 0 10px!important
}
.filter-grid h2{
  font-size:16px!important;letter-spacing:.06em!important;text-transform:uppercase!important;
  color:#e8c56a!important;font-weight:600!important;line-height:1.2!important;margin:0 0 8px!important
}
.slot>span{font-size:.78rem!important;letter-spacing:.06em!important;text-transform:uppercase!important;color:#c4a050!important;font-weight:600!important;display:flex!important;align-items:center!important;gap:8px!important}
.statrow{display:flex!important;align-items:center!important;gap:6px!important;flex-wrap:wrap!important}
.statrow .lab{display:inline-flex!important;align-items:center!important;gap:8px!important}
img.ico{width:22px!important;height:22px!important;border-radius:50%!important;object-fit:cover!important;background:#2a2a2a!important;flex:0 0 22px!important;display:inline-block!important;vertical-align:middle!important}
.statrow img.ico{width:24px!important;height:24px!important;flex-basis:24px!important}
.wchip img.ico,.dd-name img.ico{width:18px!important;height:18px!important;flex-basis:18px!important}
.dd-name{display:flex!important;align-items:center!important;gap:6px!important}
.dd-btn,.dd-name,.dd-item,.bonus,.bmain,.filters label,.tools button,
input[type=tel],.lvrow input,#lv-in,.locked,.live,.note,.mini label{font-size:16px!important}
.filters label,.tools button,.bonus,.bmain,.locked,.live,.note,.mini label{color:#e8c56a!important}
.statrow .lab{color:#e8c56a!important;font-size:16px!important;font-weight:700!important;text-align:right!important}
.lvrow,.needhint,.needhint.bad{font-size:16px!important;line-height:1.35!important;font-weight:400!important;-webkit-text-size-adjust:100%!important;text-size-adjust:100%!important}
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
input[type=checkbox]{accent-color:#e8c56a!important}
.filters input[type=checkbox]{
  -webkit-appearance:none!important;appearance:none!important;
  width:16px!important;height:16px!important;margin:0!important;
  border:2px solid #c4a050!important;border-radius:4px!important;
  background-color:#1a0e0e!important;accent-color:#e8c56a!important;
  display:inline-block!important;flex:0 0 16px!important;
  background-repeat:no-repeat!important;background-position:center!important;background-size:12px 12px!important
}
.filters input[type=checkbox]:checked{
  background-color:#e8c56a!important;border-color:#e8c56a!important;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><path fill='none' stroke='%231a0e0e' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round' d='M3.2 8.2l3.1 3.1 6.5-6.6'/></svg>")!important
}
.legal{display:block!important;font-size:.62rem!important;color:#a88848!important;text-align:center;padding:16px 8px 24px;line-height:1.4}
""" + set_block

if "</style>" not in t:
    sys.exit("no style tag")
t = t.replace("</style>", "/* n3-chrome */" + css + "/* /n3-chrome */\n</style>", 1)

t = t.replace(
    'content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no"',
    'content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover"',
)
t = t.replace('content="#0d2b4a"', 'content="#160808"')
if 'name="theme-color" content="#160808"' in t and "prefers-color-scheme" not in t:
    t = t.replace(
        '<meta name="theme-color" content="#160808">',
        '<meta name="theme-color" content="#160808">\n'
        '<meta name="theme-color" content="#160808" media="(prefers-color-scheme: light)">\n'
        '<meta name="theme-color" content="#160808" media="(prefers-color-scheme: dark)">\n'
        '<meta name="color-scheme" content="dark">',
    )

hero = """<header class="hero">
  <img src="title-banner.png?v=010" alt="Nioh 3 Equipment Builder" width="442" height="253">
  <span class="ver">v0.10.0</span>
</header>"""

if re.search(r'<header class="hero">', t):
    t = re.sub(r'<header class="hero">.*?</header>', hero, t, count=1, flags=re.S)
elif re.search(r"<h1>.*?</h1>", t, flags=re.S):
    t = t.sub if False else re.sub(r"<h1>.*?</h1>", hero, t, count=1, flags=re.S)
else:
    t = t.replace("<body>", "<body>\n" + hero, 1)

t = t.replace("title-banner.svg", "title-banner.png")
t = re.sub(r"v0\.9\.[0-9]\b", "v0.10.0", t)
t = t.replace("v0.8.1", "v0.10.0")
t = t.replace("v0.9.9", "v0.10.0")

t = t.replace(">Empty all gear<", ">Reset All<")
t = t.replace("Empty all gear?", "Reset All? This clears gear, levels, sliders, and filters.")
t = t.replace(
    "Switching Form will reset all selections below, continue?",
    "Switching Style will clear all Equipment. Continue?",
)
t = t.replace(
    'el.textContent = bits.join(" · ");',
    'el.textContent = bits.join(" · ");el.style.fontSize="16px";el.style.webkitTextSizeAdjust="100%";',
)

new_reset = """document.getElementById("btn-clear")?.addEventListener("click", () => {
  if(!confirm("Reset All? This clears gear, levels, sliders, and filters.")) return;
  clearGear();
  gsState.id=""; gsState.style="";
  STATS.forEach(([k]) => { char[k]=5; });
  char.cap = 200;
  document.querySelectorAll(".flt-style").forEach(el => { el.checked=false; });
  document.querySelectorAll(".flt-kind").forEach(el => { el.checked=true; });
  const cmb=document.getElementById("flt-combine"); if(cmb) cmb.checked=false;
  const gs=document.getElementById("flt-gs"); if(gs) gs.checked=true;
  SLOTS.forEach(([id]) => { state[id].wtype="all"; state[id].cruOnly=false; });
  fillSelects(); drawGS(); drawChar(); syncCharFields(); render();
});"""
m = re.search(
    r'document\.getElementById\("btn-clear"\)\?\.addEventListener\("click", \(\) => \{.*?\n\}\);',
    t,
    flags=re.S,
)
if not m:
    sys.exit("reset handler not found")
t = t[:m.start()] + new_reset + t[m.end():]

legal = (
    '<p class="legal">Unofficial fan-made tool. Not affiliated with Team Ninja, '
    "Koei Tecmo, or Nioh 3. All game names and terms belong to their owners.</p>"
)
if "Unofficial fan-made tool" not in t:
    if "<script>" in t:
        t = t.replace("<script>", legal + "\n<script>", 1)
    else:
        t = t.replace("</body>", legal + "\n</body>")

old_core_push = '''    pushStat("Life", "Constitution: Life +"+(char.con*40));
    pushStat("Life", "Level: Life +"+core.life);
    if(sOn) pushStat("Melee", "Heart / Strength / Intellect: Melee Attack +"+(char.hrt*2+char.str*2+char.int*2));
    if(nOn) pushStat("Melee", "Heart / Strength / Magic: Melee Attack +"+(char.hrt+char.str+char.mag));
    pushStat("Ki", "Heart: Ki +"+core.ki);
    pushStat("Ki", "Heart & Intellect: Ki Recovery Speed +"+core.kiRec);
    pushStat("Ki Damage", "Strength: Melee Ki Damage +"+core.meleeKi);
    if(nOn) pushStat("Ninjutsu", "Skill: Ninjutsu Power +"+core.ninPow);
    if(sOn) pushStat("Arts", "Skill: Arts Proficiency Power +"+core.arts);
    pushStat("Onmyo", "Magic: Onmyo Magic Power +"+core.onmyo);
    pushStat("Elemental", "Intellect: Effect Duration +"+core.dur);
    if(nOn) pushStat("Utility", "Stamina: Weight Limit "+(15+char.sta*0.3).toFixed(1));
    if(sOn) pushStat("Utility", "Stamina: Weight Limit "+(20+char.sta*1.1).toFixed(1));'''
new_core_push = '''    pushStat("Life", "Constitution: Life +"+n3val(char.con,"conLife"));
    pushStat("Life", "Heart: Life +"+n3val(char.hrt,"hrtLife"));
    pushStat("Life", "Stamina: Life +"+n3val(char.sta,"staLife"));
    pushStat("Life", "Strength: Life +"+n3val(char.str,"strLife"));
    pushStat("Life", "Skill: Life +"+n3val(char.skl,"sklLife"));
    pushStat("Life", "Intellect: Life +"+n3val(char.int,"intLife"));
    pushStat("Life", "Magic: Life +"+n3val(char.mag,"magLife"));
    pushStat("Life", "Level: Life +"+core.life);
    if(sOn) pushStat("Melee", "Heart / Strength / Intellect: Melee Attack +"+(char.hrt*2+char.str*2+char.int*2));
    if(nOn) pushStat("Melee", "Heart / Strength / Magic: Melee Attack +"+(char.hrt+char.str+char.mag));
    pushStat("Ki", "Heart: Ki +"+core.ki);
    pushStat("Ki", "Heart: Ki Recovery Speed +"+n3val(char.hrt,"hrtKiRec"));
    pushStat("Ki", "Intellect: Ki Recovery Speed +"+n3val(char.int,"intKiRec"));
    pushStat("Ki", "Heart & Intellect: Ki Recovery Speed +"+core.kiRec);
    pushStat("Ki Damage", "Strength: Ki Damage Dealt +"+core.meleeKi);
    if(nOn) pushStat("Ninjutsu", "Skill: Ninjutsu Power +"+core.ninPow);
    if(sOn) pushStat("Arts", "Skill: Arts Proficiency Power +"+core.arts);
    pushStat("Onmyo", "Magic: Onmyo Magic Power +"+core.onmyo);
    pushStat("Elemental", "Intellect: Effect Duration +"+core.dur);
    if(nOn) pushStat("Utility", "Stamina: Ninja Weight Limit +"+n3val(char.sta,"staNinWt")+" (total "+core.wlim+")");
    if(sOn) pushStat("Utility", "Stamina: Samurai Weight Limit +"+n3val(char.sta,"staSamWt")+" (total "+core.wlim+")");'''
if old_core_push not in t:
    sys.exit("core pushStat block not found")
t = t.replace(old_core_push, new_core_push)

overlay = ROOT / "scripts" / "overlay_v010.js"
if not overlay.exists():
    sys.exit("scripts/overlay_v010.js missing")
ov = overlay.read_text(encoding="utf-8")
if "function boot(){" not in t:
    sys.exit("boot() not found")
t = t.replace("function boot(){", ov + "\nfunction boot(){", 1)

INDEX.write_text(t, encoding="utf-8")
print("patched v0.10.0", INDEX.stat().st_size, "banner", len(png))
