from pathlib import Path
from PIL import Image
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
ASSETS = SITE / "assets"


class SiteIntegrationTests(unittest.TestCase):
    def test_required_files_exist(self):
        required = [
            SITE / "index.html",
            SITE / "styles.css",
            SITE / "contact.js",
            SITE / "_redirects",
            ASSETS / "kowsar-rahmani.vcf",
            ASSETS / "favicon.svg",
            ASSETS / "favicon.ico",
            ASSETS / "favicon-32.png",
            ASSETS / "apple-touch-icon.png",
            ASSETS / "hero-mobile.webp",
            ASSETS / "hero-desktop.webp",
            ASSETS / "social-preview-1200x630.jpg",
        ]
        for path in required:
            self.assertTrue(path.exists(), f"Missing {path}")

    def test_copy_and_contact_language(self):
        html = (SITE / "index.html").read_text(encoding="utf-8")
        self.assertIn("Kowsar &amp; Ramin", html)
        self.assertIn("We build, nourish &amp; bring", html)
        self.assertIn("spaces to life.", html)
        self.assertIn("Bookings · collaborations · commissions · other opportunities", html)
        self.assertIn("Save Contact", html)
        self.assertIn("Know someone we could work with?", html)
        self.assertIn("Share our page", html)
        self.assertIn("+98 918 387 1647", html)
        self.assertNotIn("Add to contacts", html)

    def test_service_copy(self):
        html = (SITE / "index.html").read_text(encoding="utf-8")
        expected = [
            "Food &amp; hospitality · Massage &amp; wellbeing",
            "Live music duo · Events &amp; creative projects · Cultural exchange",
            "Woodwork &amp; carpentry · Interiors &amp; painting · Artisan craft",
        ]
        for text in expected:
            self.assertIn(text, html)

    def test_metadata(self):
        html = (SITE / "index.html").read_text(encoding="utf-8")
        required = [
            'rel="canonical"',
            'property="og:title"',
            'property="og:description"',
            'property="og:image"',
            'property="og:url"',
            'name="twitter:card"',
            'rel="apple-touch-icon"',
            'rel="preload"',
            '/assets/favicon.svg',
            '/assets/social-preview-1200x630.jpg',
        ]
        for token in required:
            self.assertIn(token, html)

    def test_share_logic(self):
        js = (SITE / "contact.js").read_text(encoding="utf-8")
        self.assertIn("navigator.share", js)
        self.assertIn("Meet Kowsar & Ramin — Work & Collaboration", js)
        self.assertIn("Link copied", js)
        self.assertIn("https://kowsar-ramin.pages.dev/", js)

    def test_vcard_has_url(self):
        vcf = (ASSETS / "kowsar-rahmani.vcf").read_text(encoding="utf-8")
        self.assertIn("URL:https://kowsar-ramin.pages.dev/", vcf)

    def test_asset_dimensions(self):
        expected = {
            "favicon-32.png": (32, 32),
            "apple-touch-icon.png": (180, 180),
            "social-preview-1200x630.jpg": (1200, 630),
        }
        for name, size in expected.items():
            with Image.open(ASSETS / name) as im:
                self.assertEqual(im.size, size)
        for name in ("hero-mobile.webp", "hero-desktop.webp"):
            with Image.open(ASSETS / name) as im:
                self.assertGreaterEqual(im.width, 1000)
                self.assertGreaterEqual(im.height, 350)

    def test_favicon_payload_is_lightweight_and_apple_icon_opaque(self):
        svg = ASSETS / "favicon.svg"
        self.assertLess(svg.stat().st_size, 100_000, "favicon.svg should stay lightweight")
        with Image.open(ASSETS / "apple-touch-icon.png") as im:
            self.assertNotIn("A", im.getbands(), "Apple touch icon should be opaque")

    def test_contact_utility_buttons_are_uniform_and_refined(self):
        html = (SITE / "index.html").read_text(encoding="utf-8")
        css = (SITE / "styles.css").read_text(encoding="utf-8")
        self.assertIn('class="contact-icon-button add-contact-icon-button"', html)
        self.assertEqual(html.count('class="contact-icon-button'), 3, "save + two copy controls should share one visual system")
        self.assertRegex(css, r'\.contact-icon-button\s*\{[^}]*width:\s*42px', "utility buttons should be 42px")
        self.assertRegex(css, r'\.contact-icon-button\s*\{[^}]*height:\s*42px', "utility buttons should be 42px")
        self.assertRegex(css, r'\.add-contact\s*\{[^}]*min-height:\s*44px', "save-contact hit target must remain at least 44px")


if __name__ == "__main__":
    unittest.main()
