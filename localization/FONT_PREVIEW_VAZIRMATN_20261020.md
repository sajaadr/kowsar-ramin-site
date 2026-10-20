# Persian typography preview: Vazirmatn v33.003

- **Status:** PREVIEW ONLY — no authorization to change production main for aesthetic choice.
- **Base:** `ede6ae5baf0f78fe7e640592a539e4018abad6e8`.
- **Chosen trial:** Vazirmatn variable non-Latin font (47,972 bytes) upstream Git blob `949ad2639ee4b03502ef4a2a820115c71f9e92fb` at `rastikerdar/vazirmatn@v33.003`.
- **License:** SIL Open Font License 1.1; https://github.com/rastikerdar/vazirmatn/blob/v33.003/OFL.txt.
- **Transport for reversible preview only:** version-pinned jsDelivr WOFF2. CSP adds only font-src for jsDelivr; no widening of script-src, style-src or connect-src. A release should self-host the verified file to eliminate the third-party dependency.
- **Scope:** CSS only targets `html[lang=fa]`. Persian heading typography, letterspacing, line-height, cards, contact labels and selector are tuned. English and nine other non-Persian sites remain unchanged.
- **QA:** 11-locale structural and browser visual regression + explicit font-face loaded assertion for all six Persian viewport sizes. No QR/links/analytics/page translations/assets changed.
