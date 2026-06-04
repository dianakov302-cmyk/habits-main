Write-Host "=== Anaida Space - Starting ===" -ForegroundColor Cyan

# Check venv
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Virtual environment not found. Running setup first..."
    & .\setup.ps1
}

Write-Host "Starting app at http://127.0.0.1:8080/app" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop."
& .\.venv\Scripts\python.exe dev.py $args
