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

css = r"""
html{color-scheme:only dark;-webkit-text-size-adjust:100%;text-size-adjust:100%}
html,body{max-width:none!important;color:#e8c56a!important;background-color:#160808!important}
html,body,body.form-ninja,body.form-samurai,.sheet,#app{
  background-color:#160808!important;
  background-image:radial-gradient(ellipse at 50% 0%,rgba(170,18,18,.42),transparent 58%),linear-gradient(180deg,#160808 0%,#070707 100%)!important;
  background-attachment:fixed!important;
}
body{margin:0!important;padding:0!important;font-size:var(--n3-text,16px)!important;line-height:1.35!important;color:#e8c56a!important}
#boot-msg{display:none!important}
.card{background:transparent!important;border:0!important;border-radius:0!important;box-shadow:none!important;backdrop-filter:none!important;margin:0!important;padding:var(--n3-card-pad,14px) 12px 12px!important}
.card + .card{border-top:1px solid rgba(212,168,80,.16)!important}
h1,.brush-title,.brush-title .n,.brush-title .s{display:none!important}
.hero{margin:0!important;padding:calc(8px + env(safe-area-inset-top,0px)) 8px 2px!important;text-align:center!important;background:transparent!important;border:0!important}
.hero::after{display:none!important}
.hero img{display:block!important;width:92%!important;max-width:520px!important;height:auto!important;max-height:var(--n3-banner-max,168px)!important;object-fit:contain!important;object-position:center center!important;margin:0 auto!important;border:0!important;background:transparent!important}
.hero .ver,.ver{display:block!important;margin:4px auto 8px!important;font-size:.68rem!important;font-weight:600!important;letter-spacing:.16em!important;color:#c4a050!important}
.card > h2{
  font-size:var(--n3-h2,24px)!important;letter-spacing:.08em!important;text-transform:uppercase!important;
  color:#e8c56a!important;font-weight:700!important;line-height:1.2!important;margin:0 0 10px!important
}
.filter-grid h2{
  font-size:var(--n3-h2-sub,16px)!important;letter-spacing:.06em!important;text-transform:uppercase!important;
  color:#e8c56a!important;font-weight:600!important;line-height:1.2!important;margin:0 0 8px!important
}
.slot>span{font-size:var(--n3-slot-label,12.5px)!important;letter-spacing:.06em!important;text-transform:uppercase!important;color:#c4a050!important;font-weight:600!important;display:flex!important;align-items:center!important;gap:8px!important}
.statrow{display:flex!important;align-items:center!important;gap:6px!important;flex-wrap:wrap!important}
.statrow .lab{display:inline-flex!important;align-items:center!important;gap:8px!important}
img.ico{width:var(--n3-icon-slot,22px)!important;height:var(--n3-icon-slot,22px)!important;border-radius:50%!important;object-fit:cover!important;background:#2a2a2a!important;flex:0 0 var(--n3-icon-slot,22px)!important;display:inline-block!important;vertical-align:middle!important}
.statrow img.ico{width:var(--n3-icon-stat,24px)!important;height:var(--n3-icon-stat,24px)!important;flex-basis:var(--n3-icon-stat,24px)!important}
.wchip img.ico,.dd-name img.ico{width:var(--n3-icon-drop,18px)!important;height:var(--n3-icon-drop,18px)!important;flex-basis:var(--n3-icon-drop,18px)!important}
.dd-name{display:flex!important;align-items:center!important;gap:6px!important}
.dd-btn,.dd-name,.dd-item{font-size:var(--n3-drop,var(--n3-text,16px))!important}
.dd-btn{padding:var(--n3-drop-pad,8px) 10px!important}
.bonus,.bmain,.live{font-size:var(--n3-bonus,var(--n3-text,16px))!important}
.filters label{font-size:var(--n3-filter,var(--n3-text,16px))!important}
.tools button{font-size:var(--n3-btn,var(--n3-text,16px))!important;padding:var(--n3-btn-pad,8px) 12px!important}
input[type=tel],.lvrow input,#lv-in,.locked,.note,.mini label{font-size:var(--n3-text,16px)!important}
.filters label,.tools button,.bonus,.bmain,.locked,.live,.note,.mini label{color:#e8c56a!important}
.statrow .lab{color:#e8c56a!important;font-size:var(--n3-text,16px)!important;font-weight:700!important;text-align:right!important}
.lvrow,.needhint,.needhint.bad{font-size:var(--n3-text,16px)!important;line-height:1.35!important;font-weight:400!important;-webkit-text-size-adjust:100%!important;text-size-adjust:100%!important}
.lvrow,.needhint{color:#c4a050!important}
.needhint.bad{color:#e07070!important}
.pm{width:var(--n3-pm,28px)!important;height:var(--n3-pm,28px)!important;border:0!important;border-radius:8px!important;background:#1a0e0e!important;color:#e8c56a!important;box-shadow:none!important}
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
  width:var(--n3-check,16px)!important;height:var(--n3-check,16px)!important;margin:0!important;
  border:2px solid #c4a050!important;border-radius:4px!important;
  background-color:#1a0e0e!important;accent-color:#e8c56a!important;
  display:inline-block!important;flex:0 0 var(--n3-check,16px)!important;
  background-repeat:no-repeat!important;background-position:center!important;background-size:12px 12px!important
}
.filters input[type=checkbox]:checked{
  background-color:#e8c56a!important;border-color:#e8c56a!important;
  background-image:url(\