# Together and Persian name localization — candidate — 20 October 2026

Source: `main` commit `9fbbc811ae7ed8df84aa4ab3472b32ddb7ebf606`. Not a production PASS receipt.

All 11 locale labels: `en` `Together`; `tr` `Birlikte`; `de` `Gemeinsam`; `es` `Juntos`; `pt` `Juntos`; `it` `Insieme`; `fa` `با هم`; `fr` `Ensemble`; `az` `Birlikdə`; `hy` `Միասին`; `ka` `ერთად`.

Persian name authority: `کوثر رحمانی`, `رامین فهیمی`, joint `کوثر و رامین`. Persian duo label: `با هم`.

Source canonical JSON now v1.0.1 with 39 keys/locale; template+generator own the 11 rendered routes. Persian name normalization covers meta title/description, social-sharing text, image alt, hero, cards and accessibility.

Precommit check PASS: 11 keys, translated titles and aria labels, RTL fa, no leftover Latin display names in fa. The prior 11 rendered locale pages matched the deterministic generator byte-for-byte. External link targets, QR route, analytics identifiers, contact information, CSP and image assets are not intentionally changed.

**Release gate:** Python tests, generator clean diff, CI rendered QA, then independently verified Cloudflare deployment and readback before any production PASS assertion.
