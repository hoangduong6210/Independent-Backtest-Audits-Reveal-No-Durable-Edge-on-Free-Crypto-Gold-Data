# Independent Backtest Audits Reveal No Durable Edge on Free Crypto/Gold Data

**Author:** Duong Viet Hoang — Da-Yeh University — Hoangduong4316@icloud.com

A negative-results / reproducibility case study. Across an empirical campaign on **free public data**
(Binance 1h klines + funding/OI/CVD; Yahoo GC=F daily), no machine-learning, rule, funding, or basis
strategy achieves a stable Profit Factor > 1 after realistic costs. An independent 7-gate skeptical audit
protocol catches two internally inflated results (XAU +173% → −33%; spot-perp basis Sharpe ~12 → < 2) and
shows a public external claim (Sharpe 1.94) reproduces at only 0.12–0.42. Rigorous, non-proxy statistics on
the one synchronized BTC-1h return matrix (Deflated Sharpe Ratio, CSCV-PBO, White's Reality Check, Hansen
SPA) confirm the negative result: H0 "no edge over a zero benchmark" is **not** rejected.

## Repository layout

```
paper/         PREPRINT.md, PREPRINT.pdf, figures/ (all figures)
code/          make_figures.py, rigorous_stats.py, run_stats.py, build_pdf.py, run_all.{sh,ps1}, requirements.txt
data/          returns_matrix.csv (BTC-1h variant net returns), data_manifest.json (SHA-256)
```

## Reproduce

```bash
cd code
pip install -r requirements.txt
bash run_all.sh          # or: powershell -ExecutionPolicy Bypass -File run_all.ps1
```

- `make_figures.py` regenerates every figure in `paper/figures/` (deterministic).
- `run_stats.py` recomputes the load-bearing statistics (DSR / CSCV-PBO / White RC / Hansen SPA) on
  `data/returns_matrix.csv` and reproduces the Section 5.5 numbers exactly.
- `build_pdf.py` rebuilds `paper/PREPRINT.pdf` from `paper/PREPRINT.md`.
- All scripts fix random seeds for bit-stable output.

Raw OHLCV / funding inputs are freely re-downloadable from Binance and Yahoo Finance and are not shipped
to keep the repository light; `data/returns_matrix.csv` carries the aligned per-bar returns behind the
load-bearing statistical result.

## License

Code: MIT (see `LICENSE`). Manuscript and figures: CC BY 4.0.
