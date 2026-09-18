# Nioh 3 Equipment Builder

Phone-first loadout builder for Nioh 3. Current version: **v0.8.1**.

## Live URL

https://realcitizensnips.github.io/nioh3-builder/

If that 404s, open the repo on GitHub → **Settings → Pages → Source: GitHub Actions**, then wait a minute and refresh.

## Add to iPhone Home Screen

1. Open the live URL in **Safari** (not Chrome, not Files).
2. Tap Share → **Add to Home Screen**.
3. It opens like an app. Loadouts save on that phone only (Safari localStorage).

## For testers

Send the live URL. After we push a change, they should refresh or close and reopen the Home Screen icon.

## Repo layout

- `index.html` — the builder
- `manifest.json` / `sw.js` / icons — Home Screen (PWA)
- `.github/workflows/pages.yml` — publishes this folder to GitHub Pages
