#!/usr/bin/env python3
"""Reproduce DSR, CSCV-PBO, White RC, and Hansen SPA evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from backtest_audit.statistics import MATRIX_CSV, run_all


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", type=Path, default=MATRIX_CSV)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--trials", type=int)
    args = parser.parse_args()
    result = run_all(args.matrix, n_trials=args.trials)
    payload = json.dumps(result, indent=2, sort_keys=True, default=str) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
