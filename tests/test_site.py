from pathlib import Path
from PIL import Image
import hashlib
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
ASSETS = SITE / "assets"
ARCHIVE = ROOT / "archive" / "r5-web-assets"

# Heavy stable visuals served under content-hash filenames (R6 conservative caching).
FINGERPRINTED = {
    "hero-desktop": "webp",
    "hero-mobile": "webp",
    "social-preview-1200x630": "jpg",
}
ARCHIVED_FROM_DEPLOY = [
    "hero-desktop-review.png",
    "hero-mobile-review.png",
    "hero-front-art.webp",
    "site-icon-1024.png",
    "site-icon-512.png",
    "social-preview-1200x630.png",
]
PRODUCTION = "https://kowsar-ramin.pages.dev"
OG_ALT = "Kowsar &amp; Ramin — We build, nourish &amp; bring spaces to life."


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fingerprinted(stem):
    """Return the single deployable asset named <stem>.<hex>.<ext>."""
    ext = FINGERPRINTED[stem]
    pattern = re.compile(rf"^{re.escape(stem)}\.([0-9a-f]{{8,}})\.{ext}$")
    matches = [p for p in ASSETS.iterdir() if pattern.match(p.name)]
    if len(matches) != 1:
        raise AssertionError(f"expected exactly one fingerprinted {stem}.<hash>.{ext}, found {[p.name for p in matches]}")
    return matches[0]


def css_block(css, selector):
    match = re.search(rf"(?m)^{re.escape(selector)}\s*\{{([^}}]*)\}}", css)
    if not match:
        raise AssertionError(f"missing CSS block {selector}")
    return match.group(1)


def parse_headers(text):
    rules, current = {}, None
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if not raw[0].isspace():
            current = raw.strip()
            rules.setdefault(current, {})
        else:
            name, _, value = raw.strip().partition(":")
            rules[current][name.strip().lower()] = value.strip()
    return rules


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
            SITE / "_headers",
            fingerprinted("hero-mobile"),
            fingerprinted("hero-desktop"),
            fingerprinted("social-preview-1200x630"),
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
            f'/assets/{fingerprinted("social-preview-1200x630").name}',
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
        }
        for name, size in expected.items():
            with Image.open(ASSETS / name) as im:
                self.assertEqual(im.size, size)
        with Image.open(fingerprinted("social-preview-1200x630")) as im:
            self.assertEqual(im.size, (1200, 630))
            self.assertEqual(im.format, "JPEG")
        for stem in ("hero-mobile", "hero-desktop"):
            with Image.open(fingerprinted(stem)) as im:
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


class R6PrecisionHardeningTests(unittest.TestCase):
    def setUp(self):
        self.html = (SITE / "index.html").read_text(encoding="utf-8")
        self.css = (SITE / "styles.css").read_text(encoding="utf-8")

    def headers(self):
        return parse_headers((SITE / "_headers").read_text(encoding="utf-8"))

    def test_security_headers_present_and_strict(self):
        rules = self.headers()
        self.assertIn("/*", rules)
        root = rules["/*"]
        csp = root.get("content-security-policy", "")
        directives = {d.strip().split(" ")[0]: d.strip() for d in csp.split(";") if d.strip()}
        expected = {
            "default-src": "default-src 'self'",
            "script-src": "script-src 'self'",
            "style-src": "style-src 'self'",
            "img-src": "img-src 'self' data:",
            "object-src": "object-src 'none'",
            "base-uri": "base-uri 'none'",
            "frame-ancestors": "frame-ancestors 'none'",
            "form-action": "form-action 'none'",
            "connect-src": "connect-src 'none'",
            "upgrade-insecure-requests": "upgrade-insecure-requests",
        }
        for name, value in expected.items():
            self.assertEqual(directives.get(name), value, f"CSP {name}")
        self.assertNotIn("unsafe-inline", csp)
        self.assertNotIn("unsafe-eval", csp)
        self.assertEqual(root.get("x-content-type-options"), "nosniff")
        self.assertEqual(root.get("referrer-policy"), "strict-origin-when-cross-origin")
        self.assertEqual(root.get("x-frame-options"), "DENY")
        permissions = root.get("permissions-policy", "")
        for feature in ("camera", "microphone", "geolocation", "payment", "usb"):
            self.assertIn(f"{feature}=()", permissions)
        for feature in ("web-share", "clipboard-write", "clipboard-read"):
            self.assertNotIn(feature, permissions, "share/clipboard behavior must stay enabled")
        self.assertNotIn("strict-transport-security", root)

    def test_source_is_csp_compatible(self):
        self.assertNotRegex(self.html, r"<script(?![^>]*\ssrc=)[^>]*>", "no inline scripts")
        self.assertNotRegex(self.html, r"<style[\s>]", "no inline style elements")
        self.assertNotRegex(self.html, r"\sstyle=", "no inline style attributes")
        self.assertNotRegex(self.html, r"\son[a-z]+=", "no inline event handlers")
        self.assertNotRegex(self.html + self.css, r"<(?:script|img)[^>]+src=\"https?://|<link(?![^>]*rel=\"canonical\")[^>]+href=\"https?://|url\(\"?https?://", "no third-party subresources")

    def test_completed_social_metadata(self):
        social = fingerprinted("social-preview-1200x630").name
        required = [
            '<meta property="og:site_name" content="Kowsar &amp; Ramin" />',
            '<meta property="og:locale" content="en_US" />',
            '<meta property="og:image:type" content="image/jpeg" />',
            f'<meta property="og:image:alt" content="{OG_ALT}" />',
            f'<meta name="twitter:image:alt" content="{OG_ALT}" />',
            f'<meta property="og:image" content="{PRODUCTION}/assets/{social}" />',
            f'<meta name="twitter:image" content="{PRODUCTION}/assets/{social}" />',
            '<link rel="canonical" href="https://kowsar-ramin.pages.dev/" />',
            '<meta property="og:url" content="https://kowsar-ramin.pages.dev/" />',
        ]
        for token in required:
            self.assertIn(token, self.html)

    def test_contact_label_contrast_color_and_size(self):
        block = css_block(self.css, ".contact-label")
        self.assertRegex(block, r"color:\s*var\(--terracotta-text\)")
        self.assertIn("--terracotta-text: #a94f2b;", self.css)
        self.assertRegex(block, r"font-size:\s*11px")
        self.assertRegex(block, r"text-transform:\s*uppercase")
        self.assertRegex(block, r"font-weight:\s*800")
        self.assertIn("--terracotta: #c86438;", self.css, "brand terracotta preserved elsewhere")

    def test_visible_utility_box_contract_and_expanded_copy_hit_area(self):
        base = css_block(self.css, ".contact-icon-button")
        self.assertRegex(base, r"(?<![-\w])width:\s*42px")
        self.assertRegex(base, r"(?<![-\w])height:\s*42px")
        desktop = self.css[self.css.index("@media (min-width: 900px)"):]
        self.assertRegex(desktop, r"\.contact-icon-button\s*\{[^}]*(?<![-\w])width:\s*40px")
        self.assertRegex(desktop, r"\.contact-icon-button\s*\{[^}]*(?<![-\w])height:\s*40px")
        hit = css_block(self.css, ".copy-button::before")
        self.assertRegex(hit, r"position:\s*absolute")
        inset = re.search(r"inset:\s*-(\d+)px", hit)
        self.assertIsNotNone(inset, "copy hit area must extend beyond the visible box")
        # absolute inset is measured from the padding box (1px border): 40 - 2 + 2*inset >= 44
        self.assertGreaterEqual(38 + 2 * int(inset.group(1)), 44)
        self.assertRegex(css_block(self.css, ".copy-button"), r"position:\s*relative")

    def test_fingerprinted_visuals_referenced_and_unhashed_removed(self):
        for stem, ext in FINGERPRINTED.items():
            path = fingerprinted(stem)
            digest = re.match(rf"^{re.escape(stem)}\.([0-9a-f]+)\.{ext}$", path.name).group(1)
            self.assertTrue(sha256(path).startswith(digest), f"{path.name} name must match its SHA-256")
            self.assertFalse((ASSETS / f"{stem}.{ext}").exists(), f"stale unhashed {stem}.{ext} still deployed")
            for source in (self.html, self.css):
                self.assertNotIn(f"/assets/{stem}.{ext}", source)
        self.assertIn(f'url("/assets/{fingerprinted("hero-mobile").name}")', self.css)
        self.assertIn(f'url("/assets/{fingerprinted("hero-desktop").name}")', self.css)
        self.assertIn(f'href="/assets/{fingerprinted("hero-mobile").name}"', self.html)
        self.assertIn(f'href="/assets/{fingerprinted("hero-desktop").name}"', self.html)

    def test_immutable_cache_limited_to_fingerprinted_visuals(self):
        rules = self.headers()
        immutable = {path for path, h in rules.items() if "immutable" in h.get("cache-control", "")}
        expected = {f"/assets/{fingerprinted(stem).name}" for stem in FINGERPRINTED}
        self.assertEqual(immutable, expected)
        for path in expected:
            self.assertEqual(rules[path]["cache-control"], "public, max-age=31536000, immutable")
        for path, h in rules.items():
            if path not in expected:
                self.assertNotIn("max-age=31536000", h.get("cache-control", ""), path)

    def test_archived_assets_absent_from_deploy_and_manifest_correct(self):
        for name in ARCHIVED_FROM_DEPLOY:
            self.assertFalse((ASSETS / name).exists(), f"{name} must not be deployed")
        manifest = ARCHIVE / "SHA256SUMS"
        self.assertTrue(manifest.exists())
        entries = {}
        for line in manifest.read_text(encoding="utf-8").splitlines():
            digest, name = line.split("  ", 1)
            entries[name] = digest
        self.assertTrue(set(ARCHIVED_FROM_DEPLOY) <= set(entries))
        archived = {p.name for p in ARCHIVE.iterdir() if p.name not in ("SHA256SUMS", "README.md")}
        self.assertEqual(archived, set(entries))
        for name, digest in entries.items():
            self.assertEqual(sha256(ARCHIVE / name), digest, name)

    def test_every_deployed_asset_is_referenced_and_every_reference_resolves(self):
        sources = self.html + self.css + (SITE / "contact.js").read_text(encoding="utf-8")
        refs = set(re.findall(r"/assets/([A-Za-z0-9._-]+)", sources))
        for ref in refs:
            self.assertTrue((ASSETS / ref).exists(), f"broken reference /assets/{ref}")
        deployed = {p.name for p in ASSETS.iterdir()}
        self.assertEqual(deployed - refs, set(), "unreferenced deployable assets")


if __name__ == "__main__":
    unittest.main()
