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
