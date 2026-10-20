from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
DATA = json.loads((ROOT / "localization" / "LOCALIZATION_CANONICAL.json").read_text(encoding="utf-8"))

def html_escape(value):
    return (value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;").replace("'", "&#39;"))

def page_path(code):
    return SITE / "index.html" if code == "en" else SITE / code / "index.html"

class I18nTests(unittest.TestCase):
    def test_locale_and_key_parity(self):
        self.assertEqual(DATA["locale_order"], ["en","tr","de","es","pt","it","fa","fr","az","hy","ka"])
        keys = set(DATA["locales"]["en"]["messages"])
        self.assertEqual(len(keys), 39)
        for code in DATA["locale_order"]:
            messages = DATA["locales"][code]["messages"]
            self.assertEqual(set(messages), keys, code)
            self.assertTrue(all(v.strip() for v in messages.values()), code)
            self.assertEqual(messages["language.change_to"].count("{language}"), 1, code)

    def test_all_routes_exist_and_are_localized(self):
        for code in DATA["locale_order"]:
            path = page_path(code)
            self.assertTrue(path.exists(), code)
            html = path.read_text(encoding="utf-8")
            loc = DATA["locales"][code]
            self.assertIn(f'<html lang="{loc["bcp47"]}" dir="{loc["dir"]}">', html)
            self.assertIn(html_escape(loc["messages"]["hero.line1"]), html)
            self.assertIn(html_escape(loc["messages"]["hero.line2"]), html)
            self.assertIn(html_escape(loc["messages"]["kowsar.services"]), html)
            self.assertIn(html_escape(loc["messages"]["contact.intent"]), html)
            self.assertIn(html_escape(loc["messages"]["share.button"]), html)
            self.assertNotIn("{{", html)

    def test_hreflang_matrix_complete(self):
        expected = set(DATA["locales"]) | {"x-default"}
        for code in DATA["locale_order"]:
            html = page_path(code).read_text(encoding="utf-8")
            found = set(re.findall(r'rel="alternate" hreflang="([^"]+)"', html))
            self.assertEqual(found, expected, code)

    def test_canonical_url_matches_locale_route(self):
        base = "https://kowsar-ramin.pages.dev"
        for code in DATA["locale_order"]:
            html = page_path(code).read_text(encoding="utf-8")
            expected = base + DATA["route_policy"][code]
            self.assertIn(f'<link rel="canonical" href="{expected}" />', html)
            self.assertIn(f'<meta property="og:url" content="{expected}" />', html)
            self.assertIn(f'data-canonical-url="{expected}"', html)

    def test_language_menu_uses_native_names_not_flags(self):
        root = (SITE / "index.html").read_text(encoding="utf-8")
        for code in DATA["locale_order"]:
            self.assertIn(DATA["locales"][code]["native_name"], root)
        for flag in ["🇦🇿","🇦🇲","🇬🇪","🇹🇷","🇩🇪","🇪🇸","🇵🇹","🇮🇹","🇫🇷","🇮🇷"]:
            self.assertNotIn(flag, root)
        self.assertIn('class="language-globe"', root)

    def test_rtl_is_persian_only_and_mixed_latin_fields_are_isolated(self):
        self.assertEqual(DATA["locales"]["fa"]["dir"], "rtl")
        for code in DATA["locale_order"]:
            if code != "fa":
                self.assertEqual(DATA["locales"][code]["dir"], "ltr")
        fa = page_path("fa").read_text(encoding="utf-8")
        self.assertIn('id="contact-email" class="contact-value" dir="ltr"', fa)
        self.assertIn('id="contact-phone" class="contact-value" dir="ltr"', fa)


    def test_translated_duo_and_persian_personal_names(self):
        labels = {
            "en": "Together", "tr": "Birlikte", "de": "Gemeinsam",
            "es": "Juntos", "pt": "Juntos", "it": "Insieme",
            "fa": "با هم", "fr": "Ensemble", "az": "Birlikdə",
            "hy": "Միասին", "ka": "ერთად",
        }
        for code, label in labels.items():
            with self.subTest(locale=code):
                msg = DATA["locales"][code]["messages"]
                html = page_path(code).read_text(encoding="utf-8")
                self.assertEqual(msg["together.name"], label)
                self.assertIn(f'<h2>{html_escape(label)}</h2>', html)
                self.assertIn(
                    f'<p class="identity">{html_escape(msg["site.identity"])}</p>', html)
                self.assertIn(
                    f'<meta property="og:site_name" content="{html_escape(msg["site.identity"])}" />',
                    html)
                self.assertIn(html_escape(msg["kowsar.name"]), html)
                self.assertIn(html_escape(msg["ramin.name"]), html)
                self.assertIn(html_escape(msg["aria.open_together_instagram"]), html)
                if code != "en":
                    self.assertNotIn("<h2>Together</h2>", html)
                    self.assertNotIn("Together", msg["aria.open_together_instagram"])

        persian = DATA["locales"]["fa"]["messages"]
        self.assertEqual(persian["site.identity"], "کوثر و رامین")
        self.assertEqual(persian["kowsar.name"], "کوثر رحمانی")
        self.assertEqual(persian["ramin.name"], "رامین فهیمی")
        fa_html = page_path("fa").read_text(encoding="utf-8")
        for name in ("کوثر و رامین", "کوثر رحمانی", "رامین فهیمی", "با هم"):
            self.assertIn(name, fa_html)
        for latin in ("Kowsar & Ramin", "Kowsar Rahmani", "Ramin Fahimi"):
            self.assertNotIn(latin, fa_html)
        for key in ("page.title", "meta.description", "meta.og_title",
                    "meta.image_alt", "share.title", "share.text"):
            self.assertIn("کوثر و رامین", persian[key])

    def test_dynamic_localization_data_present(self):
        attrs = [
            "data-share-title", "data-share-text", "data-status-copied",
            "data-status-select-text", "data-status-link-copied", "data-status-copy-link",
        ]
        for code in DATA["locale_order"]:
            html = page_path(code).read_text(encoding="utf-8")
            for attr in attrs:
                self.assertIn(attr, html, f"{code}: {attr}")

    def test_analytics_language_enum_bounded(self):
        js = (SITE / "analytics.js").read_text(encoding="utf-8")
        self.assertIn("language_selected", js)
        for code in DATA["locale_order"]:
            self.assertIn(f"'{code}'", js)
        self.assertIn("data-language", (SITE / "index.html").read_text(encoding="utf-8"))

    def test_existing_card_route_unchanged(self):
        rules = [x.strip() for x in (SITE / "_redirects").read_text(encoding="utf-8").splitlines()
                 if x.strip() and not x.lstrip().startswith("#")]
        self.assertEqual(rules, ["/card /?utm_source=business_card&utm_medium=qr&utm_campaign=physical_card 302"])

if __name__ == "__main__":
    unittest.main()
