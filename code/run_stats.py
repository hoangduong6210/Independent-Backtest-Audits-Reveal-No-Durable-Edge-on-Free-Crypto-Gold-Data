#!/usr/bin/env python3
"""Reproduce the load-bearing statistics (DSR, CSCV-PBO, White RC, Hansen SPA) on the BTC-1h matrix."""
import json, rigorous_stats
res = rigorous_stats.run_all()
print(json.dumps(res, indent=2, default=str))
