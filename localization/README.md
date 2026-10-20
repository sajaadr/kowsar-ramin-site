# Localization — production authority

**State:** `localization/LOCALIZATION_CANONICAL.json` is the deployed canonical source for all 11 website languages (`PRODUCTION_CANONICAL`), **not a staged candidate**.

- `LOCALIZATION_CANONICAL.json` — one writable text authority for all locale copy, metadata, accessibility and sharing text.
- `index.template.html` + `../scripts/build-i18n.mjs` — deterministic compilation into static routes in `site/`; avoid manual edits to generated HTML.
- `TRANSLATION_STYLE_GUIDE.md` — copy/style and regional-language decisions.
- `TRANSLATION_REVIEW.md` — language-review notes, not independently certified native-speaker approval.
- `I18N_QA_RUBRIC_100.md` and `I18N_QA_REPORT.md` — historical internal multi-wave translation checks; scores are judgments, not objective certification.
- `PRODUCTION_RECEIPT_20261020.md` — original multilingual launch and selector issue evidence.
- `NAME_LOCALIZATION_CHANGE_20261020.md` — approved name and Together-label release.
- `ESTEDAD_RELEASE_PLAN_20261020.md` — Persian Estedad font source and release receipt pointer.
- `licenses/Estedad-OFL-1.1.txt` — required retained font license.

Before deployment, run `node scripts/build-i18n.mjs`, `python scripts/check-i18n.py`, all tests, and the GitHub browser CI. Never change URL routing, analytics identifiers or durable QR behavior when translating. See repository-root README for current URLs, route matrix and promotion gates.
