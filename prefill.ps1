Write-Host "=== Anaida Space - Seeding Demo Data ===" -ForegroundColor Cyan

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Error "Run setup.ps1 first!"
    & .\setup.ps1
}

# Load .env variables
if (Test-Path ".env") {
    Get-Content ".env" | ForEach-Object {
        if ($_ -match "^([^#][^=]*)=(.*)$") {
            [System.Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim(), "Process")
        }
    }
}

Write-Host "Seeding MongoDB with demo data..."
& .\.venv\Scripts\python.exe seed.py
Write-Host "Done! Demo data loaded." -ForegroundColor Green
