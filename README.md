# Kowsar & Ramin — production multilingual landing page

**Status:** live on Cloudflare Pages, served from GitHub `main`. The old “QR / Cloudflare Pages Starter v1.2” instructions were bootstrap history, **not current operating instructions**.

- **Public site:** https://kowsar-ramin.pages.dev/
- **Fixed printed-card route:** https://kowsar-ramin.pages.dev/card
- **Authoritative GitHub repository:** `sajaadr/kowsar-ramin-site`
- **Cloudflare Pages build output:** `site/`
- **Source-of-truth translations:** `localization/LOCALIZATION_CANONICAL.json`, schema `KR_LOCALIZATION/1`
- **Locale template:** `localization/index.template.html`; generator `scripts/build-i18n.mjs`
- **Production font:** self-hosted Estedad 8.5 for Persian only, original SIL Open Font License in `localization/licenses/Estedad-OFL-1.1.txt`
- **CI:** `.github/workflows/i18n-ci.yml`; validates PRs and production `main` pushes across 3 browser engines.

## Languages and routes

| Language | Route | HTML direction |
|---|---|---|
| English | `/` | LTR |
| Turkish | `/tr/` | LTR |
| German | `/de/` | LTR |
| Spanish | `/es/` | LTR |
| Portuguese (European base) | `/pt/` | LTR |
| Italian | `/it/` | LTR |
| Persian (Iranian) | `/fa/` | RTL, self-hosted Estedad |
| French | `/fr/` | LTR |
| Azerbaijani | `/az/` | LTR |
| Armenian (Eastern) | `/hy/` | LTR |
| Georgian | `/ka/` | LTR |

Each locale is a generated, committed static HTML page with matching canonical/hreflang links, translated UI, metadata, status messages and accessibility labels. **Do not edit generated `site/*/index.html` by hand.**

## Change and verification workflow

1. Branch from current `main`; edit the canonical JSON and/or `localization/index.template.html`, plus CSS/JS when necessary.
2. Rebuild with `node scripts/build-i18n.mjs`; commit resulting generated pages.
3. Validate with `python scripts/check-i18n.py`, `python -m unittest discover -s tests -v`, and `pwsh ./scripts/verify-source.ps1`.
4. Qualify via GitHub pull request. CI runs **88 Chromium locale×viewport checks** (320–1920px) and **44 Firefox/WebKit desktop/mobile checks** with link/image checks and actual language switching. Screenshot artifact: `i18n-rendered-qa`.
5. Merge only when regression, browser and Cloudflare preview checks pass. Verify Cloudflare's production deployment at the **exact merge commit**; record significant changes in the corresponding PR.
6. For changes affecting visually nuanced typography, keep a human/real-device review boundary: simulated browser viewports are not physical iOS/Android confirmation.

## Protected behavior

- `/card` is the durable printed QR address and must remain a temporary redirect preserving the existing attribution parameters. **Never remove or silently repurpose it.**
- The Cloudflare `kowsar-ramin.pages.dev` hostname is tied to printed media. Do not delete/recreate the Pages project.
- Keep current Instagram, WhatsApp, contact-email, contact-phone, saved contact and portfolio destinations unless their owners explicitly approve changes.
- Preserve the explicitly approved **`noindex, follow`** search policy; localized canonical/hreflang entries are for metadata consistency, not an indexing authorization.
- Maintain the current strict first-party CSS/font CSP, anonymous/cookieless PostHog configuration and bounded event taxonomy.
- English is the translation source; Persian displays `کوثر و رامین`, `کوثر رحمانی`, `رامین فهیمی`. The trio's **Together** label is translated into each locale, while machine-readable `data-profile="together"` remains stable.
- Do not claim language proofreading by independent native speakers: the earlier translation audit was internal, as noted in `localization/I18N_QA_REPORT.md`.

## Historical audit and design decisions

Original bootstrap guidance and approval history remain traceable in Git history. Relevant in-repo evidence: `localization/PRODUCTION_RECEIPT_20261020.md` (first multilingual release plus selector clipping fix), `localization/NAME_LOCALIZATION_CHANGE_20261020.md` (local names), and `localization/ESTEDAD_RELEASE_PLAN_20261020.md` (font provenance). Current release changes and Cloudflare evidence belong in the most recent merged PR, not in rewritten historical receipts.
