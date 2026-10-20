# Persian typography preview: Estedad 8.5

**State:** Preview candidate only. The owner will choose between the Vazirmatn and Estedad preview; do not merge before approval.

- Source production main: `ede6ae5baf0f78fe7e640592a539e4018abad6e8`.
- Typeface: Estedad by Amin Abedi, official stable release 8.5, pinned git commit `97d10596b3a260c040336199c2e83a6305d37663`.
- Variable font: `fonts/Estedad[wght].woff2`, official upstream Git blob `01db924b1aa7dea3ab62814d50e73440957df7d3`, 120,924 bytes.
- Font license: SIL Open Font License 1.1. Source: https://github.com/aminabedi68/Estedad/blob/8.5/OFL.txt.
- External font CDN: exact version/commit pinned jsDelivr (preview only); styles remain same as Vazirmatn preview except font identity/URL. After choice, prefer first-party vendored font with explicit license retention.
- Scope: `html[lang=fa]` only. English and all other locales visually unchanged. Navigation, contact links, printed QR, scripts, analytics and translations unchanged.
- Security: `font-src 'self' https://cdn.jsdelivr.net` for preview; all other CSP directives unchanged; no weakening of scripts/styles.
- Gates: deterministic page generation, full regression/source verification and 11 locale × 6 viewport browser QA, including explicit Estedad FontFace loaded checks for Persian viewports.
- Compare: Estedad against Vazirmatn preview at same viewport and unchanged content. Keep both proposals open until user selects.
