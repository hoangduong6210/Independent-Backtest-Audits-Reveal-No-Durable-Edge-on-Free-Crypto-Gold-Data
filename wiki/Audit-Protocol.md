# Audit protocol

The audit proceeds from accounting to inference:

1. Verify costs are subtracted from P&L.
2. Model margin and liquidation for leveraged positions.
3. Normalize capital across all strategy legs.
4. Test at a resolution that captures path risk.
5. Isolate a forward market regime.
6. Require enough independent bets for inference.
7. Stress maker/taker, slippage, and fill assumptions.
8. Apply DSR and, where a synchronized matrix exists, CSCV-PBO, White Reality
   Check, and Hansen SPA.

A strategy is not promoted because it passes one statistic. Accounting,
execution, sample size, and multiple testing are joint requirements.
