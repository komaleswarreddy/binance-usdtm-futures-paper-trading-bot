# Run full pytest suite from trading_bot root (installs dev deps).
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
Write-Host "Installing dependencies..." -ForegroundColor Cyan
py -3 -m pip install -r requirements-dev.txt
Write-Host "Running pytest..." -ForegroundColor Cyan
py -3 -m pytest tests/
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "All tests passed." -ForegroundColor Green
