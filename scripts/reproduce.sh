#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON_BIN="${PYTHON:-python3}"
cd "$ROOT_DIR"
"$PYTHON_BIN" experiments/run_statistics.py --output results/audit/statistics.json
"$PYTHON_BIN" scripts/validate_release.py
"$PYTHON_BIN" scripts/generate_current_paper_figures.py
echo "Reproduction complete."
