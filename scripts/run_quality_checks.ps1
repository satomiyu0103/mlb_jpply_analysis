$ErrorActionPreference = "Stop"

function Invoke-Check {
    param([string]$Name, [scriptblock]$Command)
    Write-Host "=== $Name ==="
    & $Command
    if ($LASTEXITCODE -ne 0) {
        throw "$Name failed with exit code $LASTEXITCODE"
    }
}

Invoke-Check "Ruff check" { uv run ruff check . }
Invoke-Check "Ruff format check" { uv run ruff format --check . }
Invoke-Check "Mypy" { uv run mypy src }
Invoke-Check "Pytest" { uv run pytest }
Invoke-Check "Check no raw data commit" { uv run python scripts/check_no_raw_data_commit.py }
Invoke-Check "Check commit atomicity (unit)" { uv run pytest tests/test_check_commit_atomicity.py -q }
Invoke-Check "Check no sensitive patterns" { uv run python scripts/check_no_sensitive_patterns.py }
Invoke-Check "Validate agent docs" { uv run python scripts/validate_agent_docs.py }

Write-Host "=== All checks passed ==="
