---
title: Start Here
status: canonical onboarding
last_updated: 2026-08-19
paper_source: false
---

# Start Here

This project independently audits sixteen public-data crypto and gold strategy
variants under realistic costs, walk-forward validation, seven gates, and
multiple-testing-aware statistics. The core campaign ran 28--30 June 2026;
manuscript revisions continued to 17 July 2026.

Read [Project Status](status/Project-Status.md), [Current Claims](claims/Current-Claim-Language.md),
[Dataset Registry](datasets/Dataset-Registry.md), [Evidence Ledger](evidence/Evidence-Ledger.md),
and [Limitations](LIMITATIONS.md). Reproduction begins with:

```bash
python -m pip install -e '.[test]'
python experiments/run_statistics.py --output results/audit/statistics.json
python scripts/validate_release.py
pytest
python wiki/build.py check
```
