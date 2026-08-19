---
title: Reproduce and Audit Compatibility Page
status: operational annex
last_updated: 2026-08-19
paper_source: false
---

# Reproduce and audit

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
python experiments/run_statistics.py --output results/audit/statistics.json
python scripts/validate_release.py
pytest
python wiki/build.py check
```

Compare `results/audit/statistics.json` with the frozen JSON. Floating-point
values should agree for the declared Python dependency range; exact formatting
is not the scientific contract. Confirm the matrix checksum before interpreting
any numerical difference.

To regenerate public figures, install `.[paper]` and run
`python scripts/generate_current_paper_figures.py`. Figure regeneration does not
recompute historical strategy backtests.
