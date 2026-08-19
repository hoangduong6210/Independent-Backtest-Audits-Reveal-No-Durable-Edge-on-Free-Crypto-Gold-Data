# Evidence sources

## E1

**Claim:** the aligned BTC-hourly family contains 21,949 rows, four variants, and
negative annualized Sharpe ratios. **Source:**
[`data/processed/returns_matrix.csv`](../data/processed/returns_matrix.csv),
identified by [`data/manifest.json`](../data/manifest.json), evaluated by
[`src/backtest_audit/statistics.py`](../src/backtest_audit/statistics.py).

## E2

**Claim:** maximum DSR is about 0.00347, CSCV-PBO about 0.032 with 87.3% negative
OOS splits, White RC `p = 1.000`, and Hansen SPA `p = 0.9945`. **Source:** frozen
[`statistics.json`](../results/frozen/20260630_public_release/statistics.json),
recomputed by [`experiments/run_statistics.py`](../experiments/run_statistics.py).

## E3

**Claim:** the XAU headline changes from +173% gross to -32.7% under the audited
cost and sizing corner. **Source:** Sections 5.2 and Appendix A of the
[current manuscript](../paper/current_state/manuscript.md). This claim is a
documented case-study reconstruction, not part of the aligned BTC matrix.

## E4

**Claim:** the spot-perpetual basis Sharpe near 12 falls below 2 after the audit
patches. **Source:** Sections 5.3 and Appendix A of the
[current manuscript](../paper/current_state/manuscript.md). Cells with one or two
entries are descriptive and excluded from inferential claims.

## E5

**Claim:** the external momentum Sharpe 1.94 reproduces at 0.12-0.42 depending
on window. **Source:** Section 5.4 and Appendix A of the
[current manuscript](../paper/current_state/manuscript.md). Survivorship and
sample construction are acknowledged limitations.

## E6

**Claim:** the public evidence bundle is checksum-bound and points to one frozen
release. **Source:** [`data/checksums.sha256`](../data/checksums.sha256),
[`results/CURRENT`](../results/CURRENT), and
[`scripts/validate_release.py`](../scripts/validate_release.py).
