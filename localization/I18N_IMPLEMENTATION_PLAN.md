# Kowsar & Ramin Multilingual Website — Implementation Plan

## Decision
Build a **static, first-party multilingual site** with separate language URLs and a compact **globe + current-language** selector in the hero. Do not use flags and do not depend on a third-party runtime translator.

## Launch locales
English, Türkçe, Deutsch, Español, Português, Italiano, فارسی, Français, Azərbaycanca, Հայերեն, ქართული.

## URL map
`/`, `/tr/`, `/de/`, `/es/`, `/pt/`, `/it/`, `/fa/`, `/fr/`, `/az/`, `/hy/`, `/ka/`.

## Visual placement
- Desktop: compact selector pill at the upper-right inside the hero, subordinate to the brand headline.
- Mobile: same trigger; language list opens as a wide anchored panel with large touch targets.
- Trigger: SVG globe + current native language name + chevron.
- Menu: native language names only; current language checkmarked/`aria-current`.
- No flags.
- No automatic IP redirect.
- Browser-language suggestion is deferred until after the explicit selector is proven.

## Architecture
1. `localization/LOCALIZATION_CANONICAL.json` is the machine-readable candidate authority.
2. English remains source authority.
3. Generate static localized pages; do not hand-maintain 11 independent pages.
4. Every page gets its own `lang`, `dir`, localized metadata/share/accessibility/status content.
5. Every page links all language variants with `hreflang`; use `x-default` for English/root.
6. Keep `noindex, follow` unchanged unless separately approved.
7. Remember an explicit user choice only as convenience; never make it the only route to a locale.
8. Persian gets dedicated RTL/bidi CSS QA; phone/email/Latin names remain readable.
9. Existing PostHog event names/enums remain unchanged. Any future `language_selected` event must use a fixed locale enum.

## Ten implementation phases
1. **Authority/translation package** — candidate JSON, review surface, style guide, 100-criterion rubric, 10-wave QA, deterministic checker.
2. **Template/generator** — one HTML template and deterministic generator; escape text and emit locale metadata.
3. **Shared interaction localization** — dynamic copy/share/status strings supplied without inline scripts or CSP weakening.
4. **Selector styling** — globe SVG, focus/keyboard states, 44px+ targets, mobile overflow protection.
5. **Static output** — generate 11 routes reusing existing protected/fingerprinted assets.
6. **Automated tests** — keys/routes/lang/dir/hreflang/ARIA plus analytics/QR/contact invariants.
7. **Visual QA** — narrow/tall phone, common mobile, tablet, desktop; long strings; Persian RTL/mixed Latin.
8. **Production candidate** — existing R7 tests + new i18n suite; no privacy/CSP regression.
9. **Promotion** — merge only after evidence-backed PASS; capture commit/deployment identity.
10. **Live readback** — verify all 11 routes, selector round-trip, `/card`, contact/share, analytics, CSP and metadata.

## Rollback
One Git revert returns to English-only production. The printed QR remains unchanged because `/card` continues to target the default/root route.

## Promotion boundary
This branch is preparation/candidate work only. It does not alter production until merged to `main`.

## Current candidate status

Prepared on branch `i18n-localization-prep`:

- 11 locale routes are generated in the branch.
- Root English page includes the globe/current-language selector.
- Locale pages include localized visible copy, metadata, share text, status text and accessibility labels.
- Persian is emitted with `dir="rtl"`; email and phone values are isolated LTR.
- All pages contain the full native-name language selector and reciprocal `hreflang` links plus `x-default`.
- Shared CSS contains responsive selector styling with 44px+ targets and RTL placement.
- Shared contact logic reads localized page data while preserving English fallbacks and existing share attribution.
- Analytics adds only a bounded `language_selected` event with the fixed 11-locale enum.
- Existing `/card` redirect, contact destinations, QR/UTM taxonomy and protected visual assets are unchanged.
- Connector readback verified all 11 pages have correct `lang`/`dir`, locale canonical URL, resolved translation tokens, language selector and expected locale matrix.

Pre-production qualification is now PASS after a fail→repair→rerun cycle. Remaining gate: merge the verified candidate to `main`, allow the existing Cloudflare Pages production path to deploy it, then perform live readback of all locale routes, `/card`, selector navigation, metadata, CSP/analytics and contact/share behavior.
