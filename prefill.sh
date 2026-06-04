#!/usr/bin/env bash
set -e

echo "=== Anaida Space — Seeding Demo Data ==="

VENV_DIR=".venv"
VENV_PYTHON="$VENV_DIR/bin/python"

if [ ! -x "$VENV_PYTHON" ]; then
    echo "Run setup.sh first!"
    bash setup.sh
fi

# Optional: load .env
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
fi

echo "Seeding MongoDB with demo data..."
if ! "$VENV_PYTHON" seed.py; then
    exit 1
fi
echo "Done! Demo data loaded."
