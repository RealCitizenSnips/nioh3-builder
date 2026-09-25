# Nioh 3 Equipment Builder

Phone-first loadout builder for Nioh 3. Current version: **v0.12.0** (set builder).

Character Level is **not** in the published app. Frozen copies:

- Full-page Levels: `archive/v0.10.0`
- Levels drawer: `archive/v0.11.0`

## Live URL

https://realcitizensnips.github.io/nioh3-builder/

## Tweak sizes and names yourself

Read **[TUNE.md](TUNE.md)**. Short version:

1. Edit **`tune.css`** for icon and text sizes.
2. Search **`index.html`** for button labels if you want to rename them.
3. Commit to `main`. Wait about a minute. Refresh.

## Add to iPhone Home Screen

1. Open the live URL in **Safari** (not Chrome, not Files).
2. Tap Share → **Add to Home Screen**.
3. After a version bump, delete the icon and add it again so the service worker picks up v0.12.0.

## Repo layout

- `index.html` — catalog. UI chrome is applied on deploy by `scripts/patch_pages.py`
- `tune.css` — **your** size knobs
- `TUNE.md` — how to edit sizes and names
- `scripts/patch_pages.py` — gold theme, loadout bar, Character Level stripped on publish
- `manifest.json` / `sw.js` / `icons/` — Home Screen (PWA)
- `archive/*` branches — frozen published versions
- `.github/workflows/pages.yml` — publishes this folder to GitHub Pages
