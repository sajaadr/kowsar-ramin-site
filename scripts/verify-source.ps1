$ErrorActionPreference = 'Stop'

$Root = Split-Path -Parent $PSScriptRoot
$Site = Join-Path $Root 'site'
$Required = @(
  (Join-Path $Site 'index.html'),
  (Join-Path $Site 'styles.css'),
  (Join-Path $Site '_redirects'),
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

Write-Host 'PASS R2 source preflight: final-card content/assets present; static site intact; /card invariant is exactly /card / 302.'
