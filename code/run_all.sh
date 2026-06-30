#!/usr/bin/env bash
# One-command reproduce: figures + load-bearing statistics. Seeds fixed (np.random.seed(42)/seed=7).
set -e
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"
$PY make_figures.py
$PY run_stats.py
echo "Done: figures in ../paper/figures, statistics printed above."
