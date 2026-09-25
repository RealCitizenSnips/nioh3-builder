# How to tweak the builder yourself

Live app: https://realcitizensnips.github.io/nioh3-builder/

You do **not** need to touch `scripts/patch_pages.py` for sizing or button names.

Current published version: **v0.11.0** (set builder). Character Level lives in a **Levels** drawer. Frozen copy of the old full-page Levels: branch `archive/v0.10.0`.

---

## Sizes and icons (easiest)

File: **`tune.css`** at the repo root.

1. Phone or computer → GitHub → `nioh3-builder` → open `tune.css`.
2. Pencil → Edit.
3. Change a number. Example: `--n3-icon-slot: 22px;` → `28px`.
4. Commit to **main**.
5. Wait about a minute. Safari pull-to-refresh. If the Home Screen copy looks old, delete the icon and Add to Home Screen again.

| Variable | What it changes | Start value |
|---|---|---|
| `--n3-text` | Fallback for most reading text | 16px |
| `--n3-drop` | Closed dropdown + open list rows | 16px |
| `--n3-btn` | Copy / Reset / Save / Load / Levels | 16px |
| `--n3-bonus` | Overall Stats bonus lines | 16px |
| `--n3-filter` | Filter check labels | 16px |
| `--n3-h2` | Big section titles (Filters, Overall Stats, Equipment) | 24px |
| `--n3-h2-sub` | Small titles inside Filters (Styles / Equipment / Show / Hide) | 16px |
| `--n3-slot-label` | HEAD / CHEST / ARMS labels | 12.5px |
| `--n3-icon-slot` | Round icons next to those slot labels | 22px |
| `--n3-icon-stat` | Round icons next to Constitution / Heart / … | 24px |
| `--n3-icon-drop` | Icons inside an open dropdown | 18px |
| `--n3-pm` | + and − in the Levels drawer | 28px |
| `--n3-check` | Filter checkboxes | 16px |
| `--n3-banner-max` | Banner image height cap | 168px |
| `--n3-card-pad` | Padding inside each section | 14px |
| `--n3-drop-pad` | Padding inside a dropdown button | 8px |
| `--n3-btn-pad` | Padding inside the loadout buttons | 8px |
| `--n3-drawer-w` | Levels drawer width | 380px |

Keep the `px`. Do not remove the `--n3-…:` name.

Want something `tune.css` does not cover? Add a rule at the bottom of that same file (examples are already commented there) and commit. If it does nothing, tell me the section and I will wire a new knob.

---

## Button and section names

Those strings live in **`index.html`**. GitHub → Find file → `index.html` → Edit, then search:

| What you see | Search for |
|---|---|
| Copy summary | `Copy summary` |
| Reset All | `Reset All` |
| Save loadout | `Save loadout` |
| Load Loadout | `Load Loadout` |
| Levels (opens the drawer) | `>Levels<` |
| Close (inside the drawer) | `>Close<` |
| Filters / Styles / Equipment / Show / Hide | `<h2>Filters</h2>` etc. |
| Overall Stats | `<h2>Overall Stats</h2>` |
| Guardian Spirit | `<h2>Guardian Spirit</h2>` |
| Character Level | `<h2>Character Level</h2>` |
| Head / Chest / Arms / … | `<span>Head</span>` |

Change only the words between the tags. Do not delete `id="btn-copy"` and friends — the buttons break if those ids go away.

Commit to **main**. Same refresh as above.

CI rewrites the page on every push. Your label changes in `index.html` survive as long as you only change the visible words.

---

## Swap an icon picture

Folder: **`icons/`**. Names must match `icons/README.txt` (example: `icons/slot-head.png`).

Drop the new PNG/SVG/JPG with that exact name, commit. The app tries `.png` → `.svg` → `.jpg` → gray `?`.

---

## What not to edit (yet)

- `scripts/patch_pages.py` — gold theme + layout surgery. Easy to break the iPhone PWA.
- `scripts/overlay_logic.js` — Level math and set-name overlays.
- `sw.js` — cache name. Leave it unless we bump a version together.
- Anything inside `/* n3-chrome */` if you ever look at the built page. That block is generated.

---

## Version rule

- Live on `main` is the current published look.
- Every jump (`0.10` → `0.11`) gets a frozen branch `archive/vX.Y.Z` **before** the next jump.
- Character Level work from v0.10.0 is frozen at `archive/v0.10.0`. We will bring it back after the set builder is solid.
- Your `tune.css` experiments stay on `main`. They do not need a new version number unless you want one locked.
