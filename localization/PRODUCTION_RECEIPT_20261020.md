# Kowsar & Ramin Multilingual Production Receipt — 2026-10-20

## Decision
**PRODUCTION PASS** for the 11-locale static multilingual implementation.

## Production identity
- Repository: `sajaadr/kowsar-ramin-site`
- Promotion PR: `#1`
- Production merge commit: `53f130c20394948c41d1731fa1bd3b034fa68400`
- Cloudflare Pages deployment: `c30a3675-ef4b-4439-b4a3-7fcfbe800111`
- Cloudflare deployment check: **success / Deployed successfully**
- Cloudflare preview URL: `https://c30a3675.kowsar-ramin.pages.dev`
- Canonical production URL: `https://kowsar-ramin.pages.dev/`

## Qualified locales
`en`, `tr`, `de`, `es`, `pt`, `it`, `fa`, `fr`, `az`, `hy`, `ka`.

## Evidence chain
1. Canonical localization authority: **PASS — 11 locales × 35 keys = 385 strings**.
2. Generator reproducibility: **PASS**.
3. Python regression suite: **31/31 PASS**.
4. Existing R7 source/security/privacy preflight: **PASS**.
5. Whitespace integrity: **PASS**.
6. Rendered browser QA: **44/44 locale×viewport checks PASS** across 360×640, 390×844, 768×1024 and 1440×1000.
7. Rendered QA reported **0 console errors** and **0 page errors**.
8. Language selector target geometry: **PASS**.
9. Persian RTL + LTR phone/email isolation: **PASS**.
10. Final rendered evidence artifact SHA-256: `d212abf1df00907a4f6a47512b5a7dfa7a14072eccdb3c825c420db8afabb086`.
11. Manual screenshot montage review: **PASS** for mobile and desktop composition.
12. Cloudflare Pages deployment of exact merge commit: **PASS**.
13. Connected-browser production root readback: **PASS**; live root shows the 11-language selector and approved content.
14. Production Git tree contains root plus all ten non-English locale pages: **PASS**.

## Failures found and corrected before promotion
- Initial rendered QA correctly failed on multilingual service-card clipping caused by fixed heights.
- Cards were changed to preserved minimum heights with natural expansion; rerun passed all 44 viewport checks.
- Turkish hero person agreement was corrected and matching social-preview alt text aligned.
- CI artifact handling was adjusted so an early gate failure does not create a misleading second failure.

## Preserved invariants
- Permanent printed QR and `/card` attribution route unchanged.
- Contact phone/email/WhatsApp/Instagram/portfolio destinations unchanged.
- `noindex, follow` policy unchanged.
- PostHog remains cookieless/anonymous and existing event taxonomy is preserved; only bounded `language_selected` with the fixed locale enum was added.
- Existing CSP/security header model is preserved.
- Protected visual assets are unchanged.
- No runtime translation vendor or automatic IP redirect was introduced.

## Qualification boundary
The 9.8–10.0 linguistic scores in the QA report are internal expert-model review scores, not independent native-speaker certification. Azerbaijani, Armenian and Georgian in particular would still benefit from optional native-speaker proofreading if such reviewers become available. This does not block the current production release because the translations passed the defined internal linguistic, structural and rendered gates.

## Readback limitation
The available public web reader could not directly fetch each Cloudflare locale route. Route deployment is therefore verified through the exact deployed Git tree, successful Cloudflare Pages check, generated-route tests, and live root selector readback rather than eleven separate external HTTP body receipts.
