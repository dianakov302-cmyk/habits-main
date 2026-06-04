#!/usr/bin/env bash
set -e

echo "=== Anaida Space — Setup (macOS/Linux) ==="

VENV_DIR=".venv"
VENV_PYTHON="$VENV_DIR/bin/python"

# Check Python 3.11+
python3 --version >/dev/null 2>&1 || { echo "ERROR: python3 not found. Install Python 3.11+"; exit 1; }
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "Python $PYTHON_VERSION detected"

# Create virtual environment
if [ ! -x "$VENV_PYTHON" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    echo "Virtual environment created."
fi

# Install deps into the virtual environment
echo "Installing dependencies..."
"$VENV_PYTHON" -m pip install -r backend/requirements.txt -q
echo "Dependencies installed."

# Copy .env if not exists
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ".env created from .env.example. Please fill in your MONGODB_URI."
else
    echo ".env already exists."
fi

echo ""
echo "=== Setup complete! ==="
echo "Run: bash run.sh"
