# Estedad final release candidate — 2026-10-20

Owner selected Estedad after preview comparison (PRs #6 and #7).

- **Source:** Amin Abedi's Estedad v8.5 stable ref `8.5`, commit `97d10596b3a260c040336199c2e83a6305d37663`.
- **Font:** upstream `fonts/Estedad[wght].woff2`, 120924 bytes, official Git blob `01db924b1aa7dea3ab62814d50e73440957df7d3`, byte-identical repository blob.
- **Deployed path:** `/assets/estedad-v8.5-01db924b.woff2`; self-hosted by Cloudflare Pages. Font license retained in `localization/licenses/Estedad-OFL-1.1.txt`.
- **Security:** Previous CSP `site/_headers` unchanged (third-party font CDN permission removed entirely); no new origin, script, tracking or cookie.
- **Design:** only `html[lang="fa"]` CSS selectors; Persian font preload only on `/fa/`; remaining 10 locale fonts unchanged.
- **Preserve:** all locale copy and routing, QR `/card`, contact and Instagram URLs, analytics, hero/card imagery and SEO robots policy.
- **Gates:** upstream binary blob integrity; deterministic HTML generator; Python and PowerShell regressions; Chromium 11 locales × 8 viewport sizes 320 to 1920 with Persian actual FontFace load; Firefox and WebKit 11 locales × desktop/mobile; Cloudflare preview and exact production-commit deployment.
- **Evidence boundary:** browser simulations cover responsive phone/desktop engines but do not replace physical iOS and Android device testing. No production PASS until merge and post-merge deployment verification.
