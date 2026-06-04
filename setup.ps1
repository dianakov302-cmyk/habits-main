Write-Host "=== Anaida Space - Setup (Windows) ===" -ForegroundColor Cyan

$VenvDir = ".venv"
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found: $pythonVersion"
} catch {
    Write-Error "Python not found. Install Python 3.11+ from python.org"
    exit 1
}

# Create virtual environment
if (-not (Test-Path $VenvPython)) {
    Write-Host "Creating virtual environment..."
    python -m venv $VenvDir
    Write-Host "Virtual environment created."
}

# Install dependencies
Write-Host "Installing dependencies..."
& $VenvPython -m pip install -r backend\requirements.txt -q
Write-Host "Dependencies installed."

# Copy .env if not exists
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host ".env created from .env.example. Please fill in your MONGODB_URI." -ForegroundColor Yellow
} else {
    Write-Host ".env already exists."
}

Write-Host ""
Write-Host "=== Setup complete! ===" -ForegroundColor Green
Write-Host "Run: .\run.ps1"
