# Public audit bundle

The minimum self-contained audit bundle consists of:

- the current manuscript and its generated figures;
- the processed return matrix and both manifests;
- `src/backtest_audit/statistics.py`;
- `experiments/run_statistics.py`;
- the frozen statistics JSON and checksums;
- claims, provenance, protocol, and reproduction documentation;
- tests and CI configuration.

The local `archive/legacy-source/` is deliberately excluded. It is preserved for
author traceability but is not needed to reproduce the published statistical
conclusion.
