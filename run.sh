#!/usr/bin/env bash
# Simple runner for the app. Make executable: chmod +x run.sh

set -euo pipefail

# If a virtualenv exists in ../Data-visualization/.venv use it, otherwise use system python
VENV="../Data-visualization/.venv"
if [ -x "$VENV/bin/python" ]; then
  PY=$VENV/bin/python
else
  PY=python3
fi

echo "Running with: $($PY --version 2>&1)"
"$PY" "$(dirname "$0")/Main.py"
