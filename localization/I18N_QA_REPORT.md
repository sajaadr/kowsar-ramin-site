> **Historical QA record.** The scores and early candidate identifiers below document the original i18n implementation, not the latest deployed revision or native-speaker certification. The current release is documented in the repository README; responsive/browser acceptance is enforced by the CI workflow.

# Kowsar & Ramin I18N — 10-Wave QA Report

**Candidate:** `KR_LOCALIZATION/1 v1.0.0-candidate`  
**Locales:** en, tr, de, es, pt, it, fa, fr, az, hy, ka  
**Important:** Scores are an **internal expert-model QA signal**, not native-speaker certification. Structural checks are deterministic; linguistic scores remain expert-review judgments.

| Wave | Focus | Internal minimum after revision | Result |
|---|---|---:|---|
| 1 | Source inventory, semantic fidelity, intent | 10.0 | PASS |
| 2 | Grammar, morphology, syntax | 9.9 | PASS |
| 3 | Idiomaticity, common vocabulary, anti-calque review | 9.8 | PASS |
| 4 | Tone, warmth, plain language, non-synthetic voice | 9.9 | PASS |
| 5 | Terminology consistency, professional/cultural fit | 9.9 | PASS |
| 6 | Concision, UI fit, text expansion, mobile density | 9.8 | PASS |
| 7 | Accessibility, Unicode, script, punctuation, RTL/bidi | 9.9 | PASS |
| 8 | Metadata, social/share language, navigation semantics | 9.9 | PASS |
| 9 | Technical invariants, analytics/privacy, key/placeholder parity | 10.0 | PASS |
| 10 | Adversarial final read, cross-locale consistency, regression readiness | 9.9 | PASS |

## Locale final internal review
| Locale | Final internal score | Notes |
|---|---:|---|
| English | 10.0 | Source authority |
| Türkçe | 9.9 | Standard Turkey Turkish; hero adapted idiomatically |
| Deutsch | 9.9 | Literal “nourish” avoided in favor of natural phrasing |
| Español | 9.9 | Neutral international register |
| Português | 9.8 | PT-PT base; variant split remains an evidence decision |
| Italiano | 9.9 | Natural standard register |
| فارسی | 9.9 | Iranian Persian; RTL/mixed-Latin requires visual QA |
| Français | 9.8 | Warm standard register; contemporary music wording |
| Azərbaycanca | 9.8 | Azerbaijan standard; native review would still add value |
| Հայերեն | 9.8 | Eastern Armenian; native review would still add value |
| ქართული | 9.8 | Modern Georgian; native review would still add value |

## Deterministic gates before production
- Exact key parity across all 11 locales.
- No empty translations.
- `{language}` placeholder parity.
- NFC Unicode normalization.
- Only Persian marked RTL.
- Unique route map.
- No translation changes URL, phone, email, QR/UTM or analytics enums.
- Localized HTML declares `lang` and `dir`.
- Language links use native labels plus `lang` and `hreflang`.
- Localized metadata/share/status/ARIA strings exist.
- Mobile/desktop regression and Persian bidi QA.

## Evidence-backed qualification checkpoint — 2026-10-20

The first rendered qualification run correctly **failed** Wave 6/UI-fit because fixed-height service cards clipped longer localized copy in Turkish, German, Spanish, Portuguese, Italian, French, Azerbaijani, Armenian and Georgian. Armenian exposed the largest expansion. The candidate was **not promoted**.

Remediation:
- service cards changed from fixed heights to preserved minimum heights with natural expansion;
- Turkish hero agreement was corrected from mixed person marking to `İnşa ediyoruz, özen gösteriyoruz ve / mekânlara hayat katıyoruz.`;
- Turkish social-preview alt text was aligned with the corrected grammar;
- the visual test was strengthened to include hero overflow checks.

Final qualifying runs for commit `8152427fb5c3445dbeba68b717ebee6b7a644d2e`:
- generator reproducibility / clean diff: **PASS**;
- canonical structural validator: **PASS — 11 locales × 35 keys**;
- Python regression suite: **PASS — 31/31**;
- R7 PowerShell source preflight: **PASS**;
- whitespace integrity: **PASS**;
- rendered Playwright QA: **PASS — 11 locales × 4 viewports = 44 rendered viewport checks**;
- console errors: **0** across the rendered matrix;
- page errors: **0** across the rendered matrix;
- language selector geometry/target-size checks: **PASS**;
- Persian RTL plus LTR email/phone isolation: **PASS**;
- screenshot/summary artifact: `i18n-rendered-qa`, SHA-256 `d212abf1df00907a4f6a47512b5a7dfa7a14072eccdb3c825c420db8afabb086`.

A manual montage review of the final mobile and desktop screenshots also found the candidate visually coherent: hero art remains intact, selector remains subordinate, longer scripts expand rather than clip, and Persian maintains a coherent RTL composition.

**Pre-production qualification status: PASS.** This remains distinct from live-production verification and from independent native-speaker certification.

## Production language-menu incident and corrective qualification — 2026-10-20

A real Chrome 100% screenshot at approximately **1416×862** exposed a production defect that the initial selector QA had not actually ruled out: the language panel contained all 11 options in the DOM, but the hero container had `overflow: hidden`, so the lower options were visually clipped at the hero boundary. This made only the first several languages visible; `Italiano` was partially cut off. The earlier selector test checked option count, panel horizontal bounds and target height, but did **not** prove that every option was visually exposed and hittable after ancestor clipping.

Root-cause repair:
- hero container now permits overflow so the language panel can escape the hero;
- hero artwork itself receives the clipping/radius, preserving the rounded visual treatment;
- desktop/laptop selector uses a compact **two-column** panel showing all 11 languages without scrolling;
- mobile selector remains one column with an explicit viewport-bounded overlay;
- selector z-index was raised above the following cards;
- the QA matrix added 1366×768 and the reported 1416×862 viewport;
- each language option is now tested with viewport bounds **and** `elementFromPoint` hit-testing;
- panel scroll dimensions are checked so desktop/laptop must not require hidden vertical or horizontal scrolling;
- open-menu screenshots are captured for mobile, 1416×862 and desktop.

Corrective qualification for commit `32dd724eacefd4618d72f60f63d53fc06adb2fcb`:
- canonical validator: **PASS — 11 locales × 35 keys**;
- Python regression: **31/31 PASS**;
- R7 source/security/privacy preflight: **PASS**;
- whitespace integrity: **PASS**;
- rendered selector/site QA: **PASS — 11 locales × 6 viewports = 66 rendered viewport checks**;
- viewports: 360×640, 390×844, 768×1024, 1366×768, **1416×862**, 1440×1000;
- every language option visible/hittable: **PASS**;
- desktop/laptop panel no-scroll requirement: **PASS**;
- mobile panel viewport containment: **PASS**;
- console/page errors: **0**;
- evidence artifact SHA-256: `9f9c85981328f54465a43ebe93a85e3830b2fe06603a44504e7aeed64bff941b`.

Manual review of the 1416×862 open-menu screenshot confirms all 11 languages are fully visible in the two-column panel, including `Italiano`, `فارسی`, `Français`, `Azərbaycanca`, `Հայերեն` and `ქართული`.

**Corrective UX qualification: PASS.**
