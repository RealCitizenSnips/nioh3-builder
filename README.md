# Nioh 3 Equipment Builder

Phone-first loadout builder for Nioh 3. Current version: **v0.9.5**.

## Live URL

https://realcitizensnips.github.io/nioh3-builder/

If that 404s, open the repo on GitHub \u2192 **Settings \u2192 Pages \u2192 Source: GitHub Actions**, then wait a minute and refresh.

## Add to iPhone Home Screen

1. Open the live URL in **Safari** (not Chrome, not Files).
2. Tap Share \u2192 **Add to Home Screen**.
3. It opens like an app. Loadouts save on that phone only (Safari localStorage).

## For testers

Send the live URL. After we push a change, they should refresh or close and reopen the Home Screen icon.

## Repo layout

- `index.html` \u2014 the builder (catalog). UI chrome is applied on deploy by `scripts/patch_pages.py`
- `scripts/title-banner.png.b64` \u2014 transparent brush banner, decoded on deploy
- `manifest.json` / `sw.js` / icons \u2014 Home Screen (PWA)
- `archive/*` branches \u2014 frozen published versions
- `.github/workflows/pages.yml` \u2014 publishes this folder to GitHub Pages
