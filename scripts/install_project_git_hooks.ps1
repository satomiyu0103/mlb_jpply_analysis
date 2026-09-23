# Install .git/hooks/pre-commit from scripts/git-hooks/pre-commit
$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$src = Join-Path $root "scripts/git-hooks/pre-commit"
$destDir = Join-Path $root ".git/hooks"
$dest = Join-Path $destDir "pre-commit"

if (-not (Test-Path (Join-Path $root ".git"))) {
    Write-Error "Run from repository root (.git not found)."
}

if (-not (Test-Path $src)) {
    Write-Error "Missing template: $src"
}

New-Item -ItemType Directory -Force -Path $destDir | Out-Null
Copy-Item -Force $src $dest
Write-Host "Installed: $dest"
