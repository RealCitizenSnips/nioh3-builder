# How to tweak the builder yourself

Live app: https://realcitizensnips.github.io/nioh3-builder/

You do **not** need to touch `scripts/patch_pages.py` for sizing or button names.

## Sizes and icons (easiest)

File: **`tune.css`** at the repo root.

1. GitHub → `nioh3-builder` → open `tune.css`.
2. Pencil → Edit.
3. Change a number. Example: `--n3-icon-slot: 22px;` → `28px`.
4. Commit to **main**.
5. Wait about a minute. Safari refresh, or delete and re-add the Home Screen icon.

| Variable | What it changes |
|---|---|
| `--n3-text` | Almost all reading text: dropdowns, bonuses, buttons, filters |
| `--n3-h2` | Big section titles (Filters, Overall Stats, Equipment) |
| `--n3-h2-sub` | Small titles inside Filters (Styles / Equipment / Show / Hide) |
| `--n3-slot-label` | HEAD / CHEST / ARMS labels |
| `--n3-icon-slot` | Round icons next to those slot labels |
| `--n3-icon-stat` | Round icons next to Constitution / Heart / … |
| `--n3-icon-drop` | Icons inside an open dropdown |
| `--n3-pm` | + and − buttons in the Levels drawer |
| `--n3-check` | Filter checkboxes |
| `--n3-banner-max` | Banner image height cap |

Keep the `px`. Do not remove the `--n3-…:` name.

## Button and section names

Those strings live in **`index.html`**. GitHub → Find file → `index.html` → Edit, then search:

| What you see | Search for |
|---|---|
| Copy summary | `Copy summary` |
| Reset All | `Reset All` |
| Save loadout | `Save loadout` |
| Load Loadout | `Load Loadout` |
| Levels (opens the drawer) | `>Levels<` |
| Filters / Styles / Equipment / Show / Hide | `<h2>Filters</h2>` etc. |
| Overall Stats | `<h2>Overall Stats</h2>` |
| Guardian Spirit | `<h2>Guardian Spirit</h2>` |

Change only the words between the tags. Do not delete `id="btn-copy"` and friends — the buttons break if those ids go away.

Commit to **main**. Same refresh as above.

## Swap an icon picture

Folder: **`icons/`**. Names must match `icons/README.txt` (example: `icons/slot-head.png`).

Drop the new PNG/SVG/JPG with that exact name, commit. The App tries `.png` → `.svg` → `.jpg` → gray `?`.

## What not to edit (yet)

- `scripts/patch_pages.py` — gold theme + layout surgery. Easy to break the iPhone PWA.
- `scripts/overlay_logic.js` — Level math and set-name overlays.
- `sw.js` — cache name. Leave it unless we bump a version together.

## Version rule

- Live on `main` is the current published look.
- Every jump (0.10 → 0.11) gets a frozen branch `archive/vX.Y.Z` **before** the next jump.
- Character Level work from v0.10.0 is frozen at `archive/v0.10.0`. We will bring it back after the set builder is solid.
