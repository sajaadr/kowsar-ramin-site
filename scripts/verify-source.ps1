$ErrorActionPreference = 'Stop'

$Root = Split-Path -Parent $PSScriptRoot
$Site = Join-Path $Root 'site'
$Required = @(
  (Join-Path $Site 'index.html'),
  (Join-Path $Site 'styles.css'),
  (Join-Path $Site '_redirects')
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
  'We build, nourish &amp; bring spaces to life.',
  'https://gamma.app/docs/Kowsar-Ramin-t1p9tj36i3krncu',
  'https://wa.me/989183871647'
)
foreach ($needle in $mustContain) {
  if (-not $html.Contains($needle)) {
    throw "index.html is missing expected content: $needle"
  }
}

Write-Host 'PASS source preflight: static site intact; /card invariant is exactly /card / 302.'
