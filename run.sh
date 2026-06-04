#!/usr/bin/env bash
set -e

echo "=== Anaida Space — Starting ==="

VENV_DIR=".venv"
VENV_PYTHON="$VENV_DIR/bin/python"

# Check venv
if [ ! -x "$VENV_PYTHON" ]; then
    echo "Virtual environment not found. Running setup first..."
    bash setup.sh
fi

echo "Starting app at http://127.0.0.1:8080/app"
echo "Press Ctrl+C to stop."
exec "$VENV_PYTHON" dev.py "$@"
