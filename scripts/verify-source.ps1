$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
$Site = Join-Path $Root 'site'

$required = @(
  'index.html', 'styles.css', 'contact.js', 'analytics.js', '_redirects', '_headers',
  'assets\kowsar-rahmani.vcf', 'assets\hero-desktop.51bb0d5c0c1c.webp', 'assets\hero-mobile.26024fe148c4.webp',
  'assets\favicon.svg', 'assets\favicon-32.png', 'assets\favicon.ico',
  'assets\apple-touch-icon.png', 'assets\social-preview-1200x630.fcc87c79c255.jpg',
  'assets\kowsar-badge.webp', 'assets\together-badge.webp', 'assets\ramin-badge.webp'
)
foreach ($relative in $required) {
  if (-not (Test-Path -LiteralPath (Join-Path $Site $relative) -PathType Leaf)) { throw "Missing required file: $relative" }
}
if (Test-Path -LiteralPath (Join-Path $Root 'functions')) { throw 'Site must remain static.' }

$expectedProtected = [ordered]@{
  '_redirects' = 'b068f6f00576f8f7fc8f84987eb38513aa83183417c4ab2340bd5febad93f7eb'
  'assets\kowsar-badge.webp' = '50b63d05ebc51e9118711765d7500755314487396d8701654f1fc78fe3667076'
  'assets\together-badge.webp' = '47ffed8b8a4fb0565e52aa19fdd18e7f59184a4c218ae18cb4c960802a7ee3b2'
  'assets\ramin-badge.webp' = '2a31a415e03ac7e18898e9befc617183a4ac5a281608d1f1f73488229406f493'
}
foreach ($entry in $expectedProtected.GetEnumerator()) {
  $actual = (Get-FileHash -LiteralPath (Join-Path $Site $entry.Key) -Algorithm SHA256).Hash.ToLowerInvariant()
  if ($actual -cne $entry.Value) { throw "Protected-byte mismatch: $($entry.Key) expected $($entry.Value) got $actual" }
}

$activeRules = @(Get-Content -LiteralPath (Join-Path $Site '_redirects') | ForEach-Object { $_.Trim() } | Where-Object { $_ -and -not $_.StartsWith('#') })
if ($activeRules.Count -ne 1 -or $activeRules[0] -cne '/card /?utm_source=business_card&utm_medium=qr&utm_campaign=physical_card 302') { throw 'Expected exactly one attributed temporary /card redirect.' }

$html = Get-Content -LiteralPath (Join-Path $Site 'index.html') -Raw
$mustContain = @(
  'Kowsar &amp; Ramin', '<span>We build, nourish &amp; bring</span>', '<span>spaces to life.</span>',
  'Food &amp; hospitality · Massage &amp; wellbeing',
  'Live music duo · Events &amp; creative projects · Cultural exchange',
  'Woodwork &amp; carpentry · Interiors &amp; painting · Artisan craft',
  'Save Contact', '+98 918 387 1647', 'tel:+989183871647',
  'Know someone we could work with?', 'Share our page',
  'rel="canonical"', 'property="og:title"', 'property="og:image"', 'name="twitter:card"',
  'https://kowsar-ramin.pages.dev/', '/assets/social-preview-1200x630.fcc87c79c255.jpg',
  'href="https://www.instagram.com/kowsar_rahmanii/"', 'href="https://www.instagram.com/ramin.kow/"', 'href="https://www.instagram.com/woodmerit/"',
  'href="https://gamma.app/docs/Kowsar-Ramin-t1p9tj36i3krncu"', 'href="https://wa.me/989183871647"', 'href="mailto:kosar.rahmani@gmail.com"',
  '<meta property="og:site_name" content="Kowsar &amp; Ramin" />', '<meta property="og:locale" content="en_US" />',
  '<meta property="og:image:type" content="image/jpeg" />',
  '<meta property="og:image:alt" content="Kowsar &amp; Ramin — We build, nourish &amp; bring spaces to life." />',
  '<meta name="twitter:image:alt" content="Kowsar &amp; Ramin — We build, nourish &amp; bring spaces to life." />'
)
foreach ($needle in $mustContain) { if (-not $html.Contains($needle)) { throw "index.html missing: $needle" } }
foreach ($obsolete in @('Add to contacts', '>+989183871647<', 'Kowsar Rahmani &amp; Ramin Fahimi</p>')) {
  if ($html.Contains($obsolete)) { throw "index.html contains obsolete content: $obsolete" }
}
if ([regex]::Matches($html, 'class="contact-icon-button').Count -ne 3) { throw 'Expected three shared contact icon controls.' }
if ($html -notmatch '<meta name="robots" content="noindex, follow"') { throw 'Robots policy changed.' }

$styles = Get-Content -LiteralPath (Join-Path $Site 'styles.css') -Raw
foreach ($needle in @('hero-desktop.51bb0d5c0c1c.webp', 'hero-mobile.26024fe148c4.webp', 'prefers-reduced-motion: reduce', 'width: 42px', 'height: 42px', 'width: 40px', 'height: 40px', 'min-height: 44px', '--terracotta: #c86438;', '--terracotta-text: #a94f2b;')) {
  if (-not $styles.Contains($needle)) { throw "styles.css missing: $needle" }
}
if ($styles -notmatch '(?m)^\.contact-label\s*\{[^}]*color:\s*var\(--terracotta-text\);[^}]*font-size:\s*11px;') { throw 'Contact labels must use the AA text terracotta at 11px.' }
if ($styles -notmatch '(?m)^\.copy-button::before\s*\{[^}]*position:\s*absolute;[^}]*inset:\s*-4px;') { throw 'Copy buttons must keep the invisible >=44px hit area.' }
foreach ($stale in @('/assets/hero-desktop.webp', '/assets/hero-mobile.webp', '/assets/social-preview-1200x630.jpg')) {
  if ($styles.Contains($stale) -or $html.Contains($stale)) { throw "Stale unhashed reference: $stale" }
}

# R6 fingerprinted visuals: filename hash prefix must match content SHA-256.
foreach ($name in @('hero-desktop.51bb0d5c0c1c.webp', 'hero-mobile.26024fe148c4.webp', 'social-preview-1200x630.fcc87c79c255.jpg')) {
  $prefix = $name.Split('.')[1]
  $actual = (Get-FileHash -LiteralPath (Join-Path $Site "assets\$name") -Algorithm SHA256).Hash.ToLowerInvariant()
  if (-not $actual.StartsWith($prefix)) { throw "Fingerprint mismatch: $name hashes to $actual" }
  if (Test-Path -LiteralPath (Join-Path $Site ("assets\" + ($name -replace '\.[0-9a-f]{12}\.', '.')))) { throw "Obsolete unhashed copy still deployed for $name" }
}

# R6 security and cache headers.
$headers = Get-Content -LiteralPath (Join-Path $Site '_headers') -Raw
foreach ($needle in @("default-src 'self'", "script-src 'self' https://eu.i.posthog.com https://static.cloudflareinsights.com", "style-src 'self'", "img-src 'self' data:", "object-src 'none'", "base-uri 'none'", "frame-ancestors 'none'", "form-action 'none'", "connect-src 'self' https://eu.i.posthog.com", 'upgrade-insecure-requests', 'X-Content-Type-Options: nosniff', 'Referrer-Policy: strict-origin-when-cross-origin', 'X-Frame-Options: DENY', 'camera=()', 'microphone=()', 'geolocation=()', 'payment=()', 'usb=()')) {
  if (-not $headers.Contains($needle)) { throw "_headers missing: $needle" }
}
foreach ($forbidden in @('unsafe-inline', 'unsafe-eval', 'web-share', 'clipboard')) { if ($headers.Contains($forbidden)) { throw "_headers must not contain: $forbidden" } }
if ([regex]::Matches($headers, 'max-age=31536000, immutable').Count -ne 3) { throw 'Immutable caching must cover exactly the three fingerprinted visuals.' }
foreach ($block in [regex]::Matches($headers, '(?m)^(/\S*)\r?\n((?:[ \t]+.*\r?\n?)+)')) {
  if ($block.Groups[2].Value.Contains('immutable') -and $block.Groups[1].Value -notmatch '^/assets/(hero-desktop|hero-mobile|social-preview-1200x630)\.[0-9a-f]{12}\.(webp|jpg)$') { throw "Immutable cache on non-fingerprinted path: $($block.Groups[1].Value)" }
}

# R6 asset hygiene: archived masters are not deployable and the archive manifest is exact.
$archive = Join-Path $Root 'archive\r5-web-assets'
foreach ($line in Get-Content -LiteralPath (Join-Path $archive 'SHA256SUMS')) {
  $digest, $name = $line -split '  ', 2
  if ((Get-FileHash -LiteralPath (Join-Path $archive $name) -Algorithm SHA256).Hash.ToLowerInvariant() -cne $digest) { throw "Archive manifest mismatch: $name" }
  if (Test-Path -LiteralPath (Join-Path $Site "assets\$name")) { throw "Archived asset still deployable: $name" }
}
$sources = $html + $styles + (Get-Content -LiteralPath (Join-Path $Site 'contact.js') -Raw)
$refs = @([regex]::Matches($sources, '/assets/([A-Za-z0-9._-]+)') | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique)
foreach ($ref in $refs) { if (-not (Test-Path -LiteralPath (Join-Path $Site "assets\$ref"))) { throw "Broken asset reference: $ref" } }
foreach ($file in Get-ChildItem -LiteralPath (Join-Path $Site 'assets') -File) { if ($refs -notcontains $file.Name) { throw "Unreferenced deployable asset: $($file.Name)" } }

$analytics = Get-Content -LiteralPath (Join-Path $Site 'analytics.js') -Raw
foreach ($needle in @("persistence: 'memory'", "cookieless_mode: 'always'", "autocapture: false", "disable_session_recording: true", "advanced_disable_flags: true", 'cta_clicked', 'instagram_clicked', 'contact_action', 'share_action', 'section_viewed')) {
  if (-not $analytics.Contains($needle)) { throw "analytics.js missing: $needle" }
}
foreach ($forbidden in @('posthog.identify', '.identify(', '.alias(', '$set', '$set_once')) {
  if ($analytics.Contains($forbidden)) { throw "analytics.js forbidden identity behavior: $forbidden" }
}

$script = Get-Content -LiteralPath (Join-Path $Site 'contact.js') -Raw
foreach ($needle in @('navigator.share', 'navigator.clipboard', "document.execCommand('copy')", "const shareTitle = 'Meet Kowsar & Ramin — Work & Collaboration'", "const canonicalUrl = 'https://kowsar-ramin.pages.dev/'", "announce(copied ? 'Link copied'")) {
  if (-not $script.Contains($needle)) { throw "contact.js missing: $needle" }
}

$vcfPath = Join-Path $Site 'assets\kowsar-rahmani.vcf'
$vcfBytes = [System.IO.File]::ReadAllBytes($vcfPath)
$vcf = [System.Text.Encoding]::UTF8.GetString($vcfBytes)
foreach ($needle in @(
  'VERSION:3.0',
  'N:Rahmani;Kowsar;;;',
  'FN:Kowsar Rahmani',
  'ORG:Kowsar & Ramin · Iran',
  'TITLE:Music, Craft & Creative Projects',
  'URL;TYPE=WORK:https://kowsar-ramin.pages.dev/',
  'X-SOCIALPROFILE;TYPE=instagram:https://www.instagram.com/kowsar_rahmanii/',
  'URL;TYPE=Instagram:https://www.instagram.com/kowsar_rahmanii/',
  'UID:urn:uuid:c17e8489-084d-5bb5-9ba6-168d0647462b',
  'PHOTO;ENCODING=b;TYPE=JPEG:',
  'NOTE:From Iran. Kowsar & Ramin work across music and creative projects\, woodwork\, hospitality and wellbeing. For bookings\, collaborations\, commissions and other opportunities.'
)) {
  if (-not $vcf.Contains($needle)) { throw "Enhanced vCard missing: $needle" }
}
if ($vcfBytes.Length -lt 20000 -or $vcfBytes.Length -gt 60000) { throw "Enhanced vCard size out of expected range: $($vcfBytes.Length)" }
if (-not $vcf.Contains("`r`n")) { throw 'Enhanced vCard must preserve CRLF line endings.' }

$gitAttributes = Get-Content -LiteralPath (Join-Path $Root '.gitattributes') -Raw
if ($gitAttributes -notmatch '(?m)^site/assets/\*\.vcf\s+-text\s*$') { throw 'Git must preserve vCard CRLF bytes.' }

Write-Host 'PASS R7 source preflight: R5 identity/services/metadata/contact/share/vCard/route/protected hashes plus R6 headers, fingerprints, contrast, hit areas and asset hygiene verified.'
