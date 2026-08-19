# Experiment protocol

The strategy campaign uses causal, one-bar-lagged features, walk-forward splits,
purging and embargo, explicit transaction costs, and fixed-risk sizing. Audited
claims pass through seven gates:

1. Costs are subtracted from realized P&L.
2. Margin and liquidation are modeled where applicable.
3. Multi-leg capital is normalized correctly.
4. Sampling resolution captures path risk.
5. A forward regime is evaluated separately.
6. At least 30 independent bets support inference.
7. Maker/taker mix, slippage, and fill assumptions are realistic.

The synchronized BTC-hourly family is then evaluated using empirical-skew and
kurtosis-aware DSR, CSCV-PBO with ten blocks, White Reality Check, and Hansen SPA.
Stationary bootstrap tests use 2,000 replications, a 24-bar average block, and
seed 42. Configuration values are recorded in `configs/default.toml`.
