$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
$Site = Join-Path $Root 'site'

$required = @(
  'index.html', 'styles.css', 'contact.js', '_redirects',
  'assets\kowsar-rahmani.vcf', 'assets\hero-desktop.webp', 'assets\hero-mobile.webp',
  'assets\favicon.svg', 'assets\favicon-32.png', 'assets\favicon.ico',
  'assets\apple-touch-icon.png', 'assets\social-preview-1200x630.jpg',
  'assets\kowsar-badge.webp', 'assets\together-badge.webp', 'assets\ramin-badge.webp'
)
foreach ($relative in $required) {
  if (-not (Test-Path -LiteralPath (Join-Path $Site $relative) -PathType Leaf)) { throw "Missing required file: $relative" }
}
if (Test-Path -LiteralPath (Join-Path $Root 'functions')) { throw 'Site must remain static.' }

$expectedProtected = [ordered]@{
  '_redirects' = 'c25556b76cbac32b49632c1807d7c752278352f44fd32f95f864b12d658dc95c'
  'assets\kowsar-badge.webp' = '50b63d05ebc51e9118711765d7500755314487396d8701654f1fc78fe3667076'
  'assets\together-badge.webp' = '47ffed8b8a4fb0565e52aa19fdd18e7f59184a4c218ae18cb4c960802a7ee3b2'
  'assets\ramin-badge.webp' = '2a31a415e03ac7e18898e9befc617183a4ac5a281608d1f1f73488229406f493'
}
foreach ($entry in $expectedProtected.GetEnumerator()) {
  $actual = (Get-FileHash -LiteralPath (Join-Path $Site $entry.Key) -Algorithm SHA256).Hash.ToLowerInvariant()
  if ($actual -cne $entry.Value) { throw "Protected-byte mismatch: $($entry.Key) expected $($entry.Value) got $actual" }
}

$activeRules = @(Get-Content -LiteralPath (Join-Path $Site '_redirects') | ForEach-Object { $_.Trim() } | Where-Object { $_ -and -not $_.StartsWith('#') })
if ($activeRules.Count -ne 1 -or $activeRules[0] -cne '/card / 302') { throw 'Expected exactly one active redirect: /card / 302' }

$html = Get-Content -LiteralPath (Join-Path $Site 'index.html') -Raw
$mustContain = @(
  'Kowsar &amp; Ramin', '<span>We build, nourish &amp; bring</span>', '<span>spaces to life.</span>',
  'Food &amp; hospitality · Massage &amp; wellbeing',
  'Live music duo · Events &amp; creative projects · Cultural exchange',
  'Woodwork &amp; carpentry · Interiors &amp; painting · Artisan craft',
  'Save Contact', '+98 918 387 1647', 'tel:+989183871647',
  'Know someone we could work with?', 'Share our page',
  'rel="canonical"', 'property="og:title"', 'property="og:image"', 'name="twitter:card"',
  'https://kowsar-ramin.pages.dev/', '/assets/social-preview-1200x630.jpg'
)
foreach ($needle in $mustContain) { if (-not $html.Contains($needle)) { throw "index.html missing: $needle" } }
foreach ($obsolete in @('Add to contacts', '>+989183871647<', 'Kowsar Rahmani &amp; Ramin Fahimi</p>')) {
  if ($html.Contains($obsolete)) { throw "index.html contains obsolete content: $obsolete" }
}
if ([regex]::Matches($html, 'class="contact-icon-button').Count -ne 3) { throw 'Expected three shared contact icon controls.' }
if ($html -notmatch '<meta name="robots" content="noindex, follow"') { throw 'Robots policy changed.' }

$styles = Get-Content -LiteralPath (Join-Path $Site 'styles.css') -Raw
foreach ($needle in @('hero-desktop.webp', 'hero-mobile.webp', 'prefers-reduced-motion: reduce', 'width: 42px', 'height: 42px', 'min-height: 44px')) {
  if (-not $styles.Contains($needle)) { throw "styles.css missing: $needle" }
}

$script = Get-Content -LiteralPath (Join-Path $Site 'contact.js') -Raw
foreach ($needle in @('navigator.share', 'navigator.clipboard', "document.execCommand('copy')", "const shareTitle = 'Meet Kowsar & Ramin — Work & Collaboration'", "const canonicalUrl = 'https://kowsar-ramin.pages.dev/'", "announce(copied ? 'Link copied'")) {
  if (-not $script.Contains($needle)) { throw "contact.js missing: $needle" }
}

$vcfPath = Join-Path $Site 'assets\kowsar-rahmani.vcf'
$vcf = [System.Text.Encoding]::UTF8.GetString([System.IO.File]::ReadAllBytes($vcfPath))
$expectedVcf = "BEGIN:VCARD`r`nVERSION:3.0`r`nN:Rahmani;Kowsar;;;`r`nFN:Kowsar Rahmani`r`nEMAIL;TYPE=INTERNET:kosar.rahmani@gmail.com`r`nTEL;TYPE=CELL:+989183871647`r`nURL:https://kowsar-ramin.pages.dev/`r`nEND:VCARD`r`n"
if ($vcf -cne $expectedVcf) { throw 'vCard bytes do not match the exact R5 UTF-8 CRLF contract.' }

$gitAttributes = Get-Content -LiteralPath (Join-Path $Root '.gitattributes') -Raw
if ($gitAttributes -notmatch '(?m)^site/assets/\*\.vcf\s+-text\s*$') { throw 'Git must preserve vCard CRLF bytes.' }

Write-Host 'PASS R5 source preflight: identity, services, metadata, contact/share behavior, vCard, route, and protected hashes verified.'
