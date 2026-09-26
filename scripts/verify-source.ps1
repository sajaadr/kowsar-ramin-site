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
  'Add to contacts',
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

$visibleText = [System.Net.WebUtility]::HtmlDecode([regex]::Replace($html, '<[^>]+>', ' '))
foreach ($handle in @('@kowsar_rahmanii', 'kowsar_rahmanii', '@ramin.kow', 'ramin.kow', '@woodmerit', 'woodmerit')) {
  if ($visibleText.Contains($handle)) {
    throw "Instagram handle is present in visible text: $handle"
  }
}

if ([regex]::Matches($html, '<span class="instagram-cta-text">View Instagram</span>').Count -ne 3) {
  throw 'Expected exactly three visible View Instagram CTA labels.'
}
if ([regex]::Matches($html, 'class="external-link-icon"[^>]+aria-hidden="true"').Count -ne 3) {
  throw 'Expected exactly three aria-hidden external-link SVG icons.'
}

$serviceParagraphs = @(
  'Food &amp; Hospitality, Massage &amp; Wellbeing',
  'Live music duo, Events &amp; Creative Projects, Cultural Exchange',
  'Woodwork &amp; Carpentry, Interiors &amp; Painting, Artisan craft'
)
foreach ($service in $serviceParagraphs) {
  if ($html -notmatch ('<p class="service-text">' + [regex]::Escape($service) + '</p>')) {
    throw "Missing exact coherent service paragraph: $service"
  }
}
if ($html -match '<ul>|<li>') {
  throw 'Legacy list/flex service presentation remains in the identity cards.'
}

foreach ($label in @('Open Kowsar Rahmani on Instagram', 'Open Together on Instagram', 'Open Ramin Fahimi on Instagram')) {
  if (-not $html.Contains('aria-label="' + $label + '"')) {
    throw "Missing exact human-readable Instagram accessible label: $label"
  }
}

if ([regex]::Matches($html, 'class="copy-button"').Count -ne 2 -or
    [regex]::Matches($html, 'class="copy-icon"[^>]+aria-hidden="true"').Count -ne 2) {
  throw 'Expected two accessible copy buttons with quiet inline SVG icons.'
}
if ([regex]::Matches($html, '<span class="contact-label contact-method-label">Email</span>').Count -ne 1 -or
    [regex]::Matches($html, '<span class="contact-label contact-method-label">Phone</span>').Count -ne 1) {
  throw 'Expected one visible Email label and one visible Phone label in the contact panel.'
}
if ([regex]::Matches($html, 'class="contact-method"').Count -ne 2) {
  throw 'Expected two independently structured contact methods.'
}
if ([regex]::Matches($html, 'class="contact-label').Count -ne 3 -or
    $html -notmatch '<p id="contact-title" class="contact-label contact-eyebrow">Contact</p>') {
  throw 'Contact, Email, and Phone do not share the common contact-label treatment.'
}
if ($html -match '<h2 id="contact-title">Kowsar Rahmani</h2>') {
  throw 'The superseded contact-card name remains visible.'
}
if ($html -notmatch '(?s)<div class="contact-kicker">.*?<a class="add-contact" href="/assets/kowsar-rahmani\.vcf" download>.*?Add to contacts.*?</a>.*?</div>') {
  throw 'The adjacent Add to contacts action is missing from the contact header.'
}
if ($html.Contains('Save contact')) {
  throw 'The superseded Save contact wording remains visible.'
}
if ($html -match '<button[^>]+class="copy-button"[^>]*>\s*Copy\s*</button>') {
  throw 'Persistent visible Copy text remains in a copy button.'
}

if ($html -notmatch '<script\s+src="/contact\.js"\s+defer></script>') {
  throw 'contact.js is not loaded as the sole deferred contact enhancement.'
}

$styles = Get-Content -LiteralPath (Join-Path $Site 'styles.css') -Raw
if ($styles -notmatch '(?s)\.contact-value,\s*\.add-contact\s*\{[^}]*font-family:\s*Georgia,\s*"Times New Roman",\s*serif;') {
  throw 'Add to contacts, email, and telephone do not share the approved Georgia value typography.'
}
if ($styles -notmatch '(?s)\.contact-card\s*\{[^}]*grid-template-columns:\s*max-content\s+minmax\(0,\s*1fr\)') {
  throw 'Mobile contact values do not share one label-sized alignment column.'
}
if ($styles -notmatch '(?s)@media\s*\(min-width:\s*720px\).*?\.contact-card\s*\{[^}]*width:\s*min\(760px,\s*100%\)') {
  throw 'Desktop contact panel does not use the approved 760px balanced width.'
}
if ($styles -notmatch '(?s)\.add-contact\s*\{[^}]*border:\s*0;') {
  throw 'Add to contacts is still rendered as a bordered pill instead of a quiet inline action.'
}
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
if ($script -notmatch "classList\.(add|toggle)\('is-copied'") {
  throw 'contact.js does not expose the temporary copied icon state.'
}
if ($script.Contains("button.textContent = 'Copied'")) {
  throw 'contact.js still replaces the compact icon with persistent text content.'
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

Write-Host 'PASS R4 source preflight: exact Instagram affordances/services present; no visible handles; compact copy icons; vCard exact; /card invariant preserved.'
