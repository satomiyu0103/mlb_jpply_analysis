# リポジトリルートの .git/hooks/pre-commit をインストールする（上書き可）
$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$src = Join-Path $root "scripts/git-hooks/pre-commit"
$destDir = Join-Path $root ".git/hooks"
$dest = Join-Path $destDir "pre-commit"

if (-not (Test-Path (Join-Path $root ".git"))) {
    Write-Error ".git が見つかりません。リポジトリルートで実行してください。"
}

if (-not (Test-Path $src)) {
    Write-Error "pre-commit テンプレが見つかりません: $src"
}

New-Item -ItemType Directory -Force -Path $destDir | Out-Null
Copy-Item -Force $src $dest
Write-Host "Installed: $dest"
Write-Host "検査: check_commit_branch_policy, check_commit_atomicity, check_no_raw_data_commit"
