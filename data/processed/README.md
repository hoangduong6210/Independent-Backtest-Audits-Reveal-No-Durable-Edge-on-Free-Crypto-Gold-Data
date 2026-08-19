# Processed evidence

`returns_matrix.csv` is a UTC-indexed `T x N` matrix with `T = 21,949` hourly
bars and `N = 4` strategy variants: `ml_rr`, `ta_funding`, `asym_barrier`, and
`ml_barrier`. A non-zero observation records net P&L at a trade exit; zero means
no exit P&L on that bar. The common axis is required for CSCV-PBO, White Reality
Check, and Hansen SPA comparisons.
