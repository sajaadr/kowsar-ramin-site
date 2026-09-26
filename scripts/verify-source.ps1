$ErrorActionPreference = 'Stop'

$Root = Split-Path -Parent $PSScriptRoot
$Site = Join-Path $Root 'site'
$Required = @(
  (Join-Path $Root '.gitattributes'),
  (Join-Path $Site 'index.html'),
  (Join-Path $Site 'styles.css'),
  (Join-Path $Site 'contact.js'),
  (Join-Path $Site '_redirects'),
  (Join-Path $Site 'assets\kowsar-rahmani.vcf'),
  (Join-Path $Site 'assets\hero-front-art.webp'),
  (Join-Path $Site 'assets\kowsar-badge.webp'),
  (Join-Path $Site 'assets\together-badge.webp'),
  (Join-Path $Site 'assets\ramin-badge.webp')
)

foreach ($path in $Required) {
  if (-not (Test-Path -LiteralPath $path)) {
    throw "Missing required file: $path"
  }
}

if (Test-Path -LiteralPath (Join-Path $Root 'functions')) {
  throw 'A functions/ directory exists. This MVP must remain static so _redirects owns /card.'
}

$activeRules = @(Get-Content -LiteralPath (Join-Path $Site '_redirects') |
  ForEach-Object { $_.Trim() } |
  Where-Object { $_ -and -not $_.StartsWith('#') })

if ($activeRules.Count -ne 1 -or $activeRules[0] -ne '/card / 302') {
  throw "Expected exactly one active redirect rule: /card / 302. Found: $($activeRules -join '; ')"
}

$html = Get-Content -LiteralPath (Join-Path $Site 'index.html') -Raw
$mustContain = @(
  'Kowsar Rahmani &amp; Ramin Fahimi',
  'We build, nourish &amp; bring spaces to life.',
  'Food &amp; Hospitality',
  'Massage &amp; Wellbeing',
  'Live music duo',
  'Events &amp; Creative Projects',
  'Cultural Exchange',
  'Woodwork &amp; Carpentry',
  'Interiors &amp; Painting',
  'Artisan craft',
  'View full portfolio',
  'WhatsApp',
  'https://www.instagram.com/kowsar_rahmanii/',
  'https://www.instagram.com/ramin.kow/',
  'https://www.instagram.com/woodmerit/',
  'kosar.rahmani@gmail.com',
  '+989183871647',
  'mailto:kosar.rahmani@gmail.com',
  'tel:+989183871647',
  'Copy email',
  'Copy phone',
  'Save contact',
  '/assets/kowsar-rahmani.vcf',
  'https://gamma.app/docs/Kowsar-Ramin-t1p9tj36i3krncu',
  'https://wa.me/989183871647'
)
foreach ($needle in $mustContain) {
  if (-not $html.Contains($needle)) {
    throw "index.html is missing expected content: $needle"
  }
}

$mustNotContain = @(
  'class="mark"',
  'Craft · Hospitality · Massage &amp; Wellbeing · Music · Art',
  'Singing',
  'Guitar',
  'RAM &amp; KOW · Music',
  'Mehr Raam'
)
foreach ($needle in $mustNotContain) {
  if ($html.Contains($needle)) {
    throw "index.html contains obsolete starter content: $needle"
  }
}

$instagramLinks = @(
  'https://www.instagram.com/kowsar_rahmanii/',
  'https://www.instagram.com/ramin.kow/',
  'https://www.instagram.com/woodmerit/'
)
foreach ($url in $instagramLinks) {
  $pattern = '<a[^>]+class="identity-card[^\"]*"[^>]+href="' + [regex]::Escape($url) + '"'
  if ($html -notmatch $pattern) {
    throw "Instagram destination is not implemented as a full identity-card anchor: $url"
  }
}

if ($html -notmatch '<script\s+src="/contact\.js"\s+defer></script>') {
  throw 'contact.js is not loaded as the sole deferred contact enhancement.'
}

$styles = Get-Content -LiteralPath (Join-Path $Site 'styles.css') -Raw
if ($styles.Contains('.identity-card li:not(:last-child)::after')) {
  throw 'Decorative capability separator pseudo-elements are still present.'
}
if ($styles -notmatch '@media\s*\(hover:\s*hover\)\s*and\s*\(pointer:\s*fine\)') {
  throw 'Fine-pointer hover interaction is missing.'
}
if ($styles -notmatch 'prefers-reduced-motion:\s*reduce') {
  throw 'Reduced-motion handling is missing.'
}

$script = Get-Content -LiteralPath (Join-Path $Site 'contact.js') -Raw
foreach ($needle in @('navigator.clipboard', 'writeText', 'execCommand', 'aria-live')) {
  if (-not $script.Contains($needle)) {
    throw "contact.js is missing required clipboard/fallback behavior: $needle"
  }
}

$vcfPath = Join-Path $Site 'assets\kowsar-rahmani.vcf'
$vcfBytes = [System.IO.File]::ReadAllBytes($vcfPath)
$vcf = [System.Text.Encoding]::UTF8.GetString($vcfBytes)
$expectedVcf = "BEGIN:VCARD`r`nVERSION:3.0`r`nN:Rahmani;Kowsar;;;`r`nFN:Kowsar Rahmani`r`nEMAIL;TYPE=INTERNET:kosar.rahmani@gmail.com`r`nTEL;TYPE=CELL:+989183871647`r`nEND:VCARD`r`n"
if ($vcf -ne $expectedVcf) {
  throw 'vCard bytes do not match the exact UTF-8 vCard 3.0 CRLF contract.'
}

$gitAttributes = Get-Content -LiteralPath (Join-Path $Root '.gitattributes') -Raw
if ($gitAttributes -notmatch '(?m)^site/assets/\*\.vcf\s+-text\s*$') {
  throw 'Git transport must preserve vCard CRLF bytes with site/assets/*.vcf -text.'
}

Write-Host 'PASS R3 source preflight: social/contact contract present; vCard exact; static site intact; /card invariant is exactly /card / 302.'
