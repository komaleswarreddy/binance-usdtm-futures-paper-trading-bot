#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
echo "Installing dependencies..."
python3 -m pip install -r requirements-dev.txt
echo "Running pytest..."
python3 -m pytest tests/
echo "All tests passed."
