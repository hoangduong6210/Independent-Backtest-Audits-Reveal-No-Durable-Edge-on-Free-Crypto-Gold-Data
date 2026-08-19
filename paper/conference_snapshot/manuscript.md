# Independent Backtest Audits Reveal No Durable Edge on Free Crypto/Gold Data: A Negative Baseline, Two Inflated Claims, and a Validation Checklist

**Anonymous Author(s)** — Submission under double-blind review, ICAIF '26

## Abstract

We conduct a large-scale, cost-honest empirical campaign on free public data — hourly crypto klines with funding, open interest and CVD proxies, and daily gold futures — across nineteen experiments spanning gradient-boosted and LSTM triple-barrier classifiers, price-action rules, multi-timeframe filters, funding long–short, spot–perpetual basis, volatility targeting, and micro trade-flow signals. Under walk-forward purged validation, strictly causal features, and realistic round-trip costs subtracted from equity with fixed 1% risk sizing, no configuration sustains a profit factor above one. We contribute a formalized seven-gate skeptical audit protocol and apply it to internal variants and one fully reproduced external public claim, detecting two severely inflated cases: a gold strategy claiming +173% collapses to −33% once costs are actually subtracted and sizing is realistic; a spot–perpetual basis trade claiming Sharpe ~12 falls to an APR near zero, with liquidation events, under hourly sampling, two-leg capital, and a realistic maker mix. An external cross-sectional momentum claim (Sharpe 1.94) reproduces at 0.12–0.42 — a gap that opens, honestly, chiefly through survivorship and missing realism *before* our gates apply. On the one variant family that admits a synchronized returns matrix (four hourly-BTC strategies, T = 21,949), every annualized Sharpe is negative, every Deflated Sharpe Ratio is ≈ 0, the White Reality Check returns p = 1.000 and the Hansen SPA p = 0.994: the no-edge null is not rejected. We release a fully reproducible bundle. The contribution is a validation checklist and a transparent negative baseline, not a new method.

**Keywords:** backtest overfitting, Deflated Sharpe Ratio, reproducibility, cryptocurrency, technical analysis, negative results, survivorship bias

## 1. Introduction

Retail quantitative researchers operating on free public OHLCV, funding rates, and basic order-flow proxies (CVD, open interest) in crypto and gold futures face a deceptively difficult environment. Apparent edges discovered in-sample or under optimistic accounting frequently vanish once costs are truly subtracted from equity, path-dependent risks (liquidation, intra-period volatility) are modeled, capital for multi-leg strategies is correctly normalized, and forward regimes are isolated.

![The recurring framing: a small visible "apparent edge" sits atop a much larger submerged mass of realism costs — execution and slippage, liquidation and margin, survivorship, and multiple-testing inflation. The audit protocol makes the submerged mass explicit.](figures_concept/fig_iceberg.png)

This paper consolidates a nineteen-experiment empirical campaign that systematically tested machine-learning classifiers (gradient-boosted P(win), LSTM meta-labels), classical rules, multi-timeframe filters, mean reversion on funding, spot–perpetual basis harvesting, volatility targeting, and micro-flow signals. The unifying result after all realism patches is the absence of durable positive expectancy: no configuration sustains a profit factor PF > 1.0 under walk-forward, causal features, and explicit costs on the tested free datasets.

The most valuable asset produced is not a "winning" strategy but a skeptical, code-backed audit protocol that caught two inflated internal claims (gold +173%; basis Sharpe ~12) and failed to reproduce a third, external public claim (momentum Sharpe 1.94). We formalize seven gates, and on the one family that admits a synchronized returns matrix we compute the rigorous Deflated Sharpe Ratio (DSR) [1], CSCV probability of backtest overfitting (PBO) [2], White Reality Check [5], and Hansen SPA [6]. We frame results honestly: external non-reproducibility is driven largely by survivorship and missing realism, not merely our gates; and the inflated internal cells reflect an accounting bug (gold) and optimistic pre-patch execution assumptions (basis), not adversarial fabrication.

We do not claim a novel statistical method — the components are due to Bailey, López de Prado, Harvey, White, and Hansen. The contribution is a *formalized validation checklist* with worked before/after case studies and a transparent, fully reproducible negative baseline on free data, addressing the reproducibility literature in quantitative finance.

## 2. Related Work

Skeptical backtesting protocols are well established. Bailey and López de Prado [1] introduced the DSR to adjust for multiple testing; Bailey et al. [2] formalized PBO via CSCV; López de Prado [3] devotes chapters to purging, embargo, and combinatorial cross-validation; Harvey [4] documents the "factor zoo" and publication bias against negative results. The multiple-comparison null is supplied by White's Reality Check [5] and Hansen's SPA [6], with the stationary bootstrap of Politis and Romano [7]. On tabular data, tree ensembles frequently outperform deep learning [8, 9] — consistent with our internal finding that a small gradient-boosted model on lagged technical and funding features was competitive with, and often less harmful than, LSTM meta-labelers. Microstructure work on free proxies is sobering: order-flow imbalance yields pre-cost Sharpe near 0.12, and stress tests show catastrophic drawdowns once costs and realistic execution are added. Funding-arbitrage practice repeatedly warns of liquidity squeezes and post-2022 regime compression, and volatility targeting [10] reduces drawdowns yet often fails to improve Sharpe after rebalancing costs at high frequency. The crypto assets we test are liquid majors whose aggregate return behaviour and arbitrage frictions are well documented [12, 13]. Closest in spirit is an auditable expert-system framework for execution-constrained auto-tuning of perpetual-futures strategies [11], which likewise documents that fee-only and zero-cost backtests materially overestimate returns; our work is complementary in applying a formalized checklist to both internal variants and one fully reproduced external strategy, with explicit before/after numbers.

## 3. Data and Methods

**Data (all free/public).** Hourly and daily spot/futures klines for BTC, ETH and SOL (multi-year windows); exchange funding-rate, taker-buy, and open-interest history; daily gold futures (2000–2026); and public one-minute aggregated trades for micro flow.

**Labeling and modeling.** Triple-barrier labels (vertical 8–16 bars, k = 1.2–1.5 ATR) or vertical for trend; gradient-boosted trees or a small LSTM for P(win) or direction. Walk-forward with train windows of 1200–5500 bars, test 250–820, embargo 3–5 bars; features lagged one bar; no future leakage.

**Costs and sizing.** Round-trip 0.06–0.12% (crypto) / 0.05–0.20% (gold) *subtracted from per-trade PnL or equity*. Fixed 1% equity risk per R; no optimistic 3% compounding. Basis adds 5 bps turnover with a 50% maker assumption.

**Entry timing.** All risk-reward variants enter at the *close of the signal bar* with one-bar-lagged features; this close-fill is mildly look-ahead-favorable. The conservative next-open alternative was tested for gold and degraded it (win-rate 52.93% → 50.38%, gross PF 1.225 → 1.137; with 0.2% cost and 1% sizing, total return → −36.99%). Reported PFs therefore sit at the optimistic end of the entry-timing spectrum; the realistic corner is uniformly worse.

**External reproduction.** An exact rule port of a public 120-day cross-sectional momentum strategy (rank, demean, 5 bps cost) on eight long-history symbols, over four period slices, using real daily closes.

## 4. The Audit Protocol

We formalize seven gates in a public audit script. A strategy passes only if all are satisfied.

1. **cost_subtracted_real** — costs actually subtracted from equity/PnL, not merely computed.
2. **margin_liq_model** — explicit margin, maintenance margin, and liquidation penalty when leverage or derivatives are used.
3. **multi_leg_capital** — correct capital normalization across legs.
4. **sampling_resolution** — frequency sufficient to capture path risk (hourly preferred over 8h/daily for crypto).
5. **regime_forward_test** — a recent/forward slice (2024+) evaluated separately.
6. **min_independent_bets** — at least 30 time-disjoint bets for DSR/PBO validity.
7. **maker_taker_slippage** — realistic fill mix (50% maker) with slippage sensitivity.

Post-gate, on the family that admits a synchronized returns matrix, we compute rigorous DSR / CSCV-PBO / White RC / Hansen SPA (§5.5); elsewhere we report per-variant DSR only, and flag limitations throughout.

![The seven-gate audit funnel. Attractive raw backtests are progressively eliminated by cost subtraction, margin/liquidation modeling, multi-leg capital, sampling resolution, forward-regime isolation, a minimum-independent-bets threshold, and a realistic maker/taker-plus-slippage mix, down to the negative baseline.](figures/fig7_audit_7gate_flow.png)

## 5. Results

### 5.1 Negative Baseline: All Variants PF < 1

Across the representative variants after realistic costs and 1% sizing under walk-forward OOS (Table 1, Figure 3), profit factors are uniformly below unity (maximum 0.94, GBT barrier BTC). Every per-asset walk-forward run loses net of costs; the R-exit risk-reward variants on BTC/ETH/SOL all cluster at PF ≈ 0.73–0.82, and the deepest drawdowns (56.9%, 41.5%, 34.2%) occur exactly on those R-exit runs. Funding and CVD features rank high in feature importance yet never translate into PF > 1 net of costs.

**Table 1.** Representative variants after realistic costs (0.10% round-trip) and 1% fixed sizing, walk-forward OOS. Every cell is read directly from the per-variant real-run output; no variant reaches PF > 1 (maximum 0.94, GBT barrier BTC). These are per-asset walk-forward backtests and are distinct from the synchronized hourly matrix of Table 4.

| Variant | PF | WR | Sharpe | MaxDD | n |
|---|---|---|---|---|---|
| GBT barrier (BTC) | 0.944 | 54.6% | −0.17 | 0.4% | 141 |
| LSTM meta (BTC) | 0.798 | 51.4% | −1.15 | 20.4% | 284 |
| Price-action rule (BTC) | 0.322 | 18.1% | −4.17 | 61.8% | 171 |
| Multi-TF H4→H1 (BTC) | 0.444 | 22.8% | −3.23 | 88.2% | 232 |
| Risk-reward (BTC) | 0.730 | 51.6% | −1.71 | 56.9% | 512 |
| Risk-reward (ETH) | 0.815 | 51.8% | −1.02 | 41.5% | 417 |
| Risk-reward (SOL) | 0.801 | 47.3% | −1.01 | 34.2% | 338 |
| TA+funding+CVD (BTC) | 0.668 | 51.9% | −0.94 | 22.9% | 106 |
| Asym. barrier (BTC) | 0.659 | 29.2% | −2.83 | 0.8% | 744 |

![Profit factor across the representative variants after realistic costs and 1% fixed sizing, walk-forward OOS. All values lie beneath the PF = 1 line (maximum 0.94).](figures/fig1_pf_16_variants.png)

**Cost sensitivity (gold).** At fixed 1% sizing the gold variant crosses break-even near a 0.112% round-trip cost (Table 2). Realistic gold-futures round-trip cost (0.10–0.20%) straddles or exceeds break-even, so the strategy is not deployable. Crypto variants at their single documented 0.10% anchor already sit below PF = 1, so their break-even cost is *below* realistic crypto fees.

**Table 2.** Gold total return versus round-trip cost at fixed 1% sizing; break-even near 0.112%. Intermediate cells are linear interpolations between documented anchors (0.05%, 0.20%).

| Round-trip cost | Gold total return (1% sizing) |
|---|---|
| 0.05% | +23.3% (PF 1.131) |
| 0.08% | +12.1% |
| 0.10% | +4.6% |
| **0.112%** | **0.0% (break-even)** |
| 0.15% | −14.0% |
| 0.20% | −32.7% (PF ~0.83) |

### 5.2 Case Study 1: Gold +173% Is an Accounting Bug

The original claim on daily gold futures: 410 trades, win-rate 52.9–53.1%, gross PF 1.225–1.232, total return +173%, MaxDD 51.7%, Sharpe ~0.36 (under 3%-risk compounding and a 0.03% cost). After patches: at 0.2% cost with 3% risk, +23%; at 0.2% cost with 1% fixed sizing (fully realistic), **−32.7%** (Sharpe −0.34); at next-open entry, −37% (Figure 4). Win-rate drops from 54.6% (symmetric barriers) to 29.2% (asymmetric). The inflation was an accounting bug — costs were computed but never subtracted from equity, compounded at an optimistic 3%, under a low assumed gold-futures cost — not adversarial fabrication; the bug is documented and reproducible from the patch sequence.

![Gold (daily futures, risk-reward) equity curves: the original +173% claim versus the post-patch realistic run (1% sizing, 0.2% cost, −32.7%). Costs computed-but-not-subtracted, optimistic compounding, and a low assumed cost produced the inflated curve.](figures/fig2_xau_equity.png)

### 5.3 Case Study 2: Basis Sharpe ~12 → < 2 with Liquidation

The original spot–perpetual basis run (8h sampling, 2020–2026): APR 8–11%, Sharpe 11.8–13.9, MaxDD < 2%, 7–11 entries, ~2-year holds, 100% maker assumed — and 0/7 gates passed. Repatched to 2024–2026 (hourly, margin/liquidation, two-leg capital, 50% maker): APR ≈ −0.31%, daily Sharpe −1.9 to +1.9, liquidation events in most configurations, and only 1–2 entries — statistically meaningless (Figure 5). The gross-to-patched gap reflects optimistic pre-patch execution assumptions (coarse sampling that hides intra-period volatility, single-leg capital, 100% maker, a pre-2024 funding regime), not deliberate distortion.

![Spot–perpetual basis Sharpe by configuration: the original 8h gross run (Sharpe 11.8–13.9) versus the patched hourly, margin/liquidation, two-leg-capital, 50%-maker, 2024+ runs (Sharpe −1.9 to +1.9, APR ≈ −0.31%). Coarse sampling and optimistic execution manufactured the apparent edge.](figures/fig3_basis_sharpe.png)

### 5.4 Case Study 3 (External): Momentum Sharpe 1.94 → 0.12–0.42

Exact reproduction of a published 120-day cross-sectional long–short momentum rule (5 bps turnover) on an eight-coin liquid universe. The claim ("Sep 2020–present"): annual return 155.8%, Sharpe 1.94. Reproduced on real data, the Sharpe collapses across every slice (Table 3, Figure 6): full sample (2018+) 0.27; claim-window 0.12; recent-best (2023+) 0.42; while BTC buy-and-hold on the same recent window returns 0.74 — simple holding dominates. Our harness reports SR ~0.50, DSR 0.40, and overall gates FALSE (sampling and maker/slippage fail).

**Table 3.** External momentum claim versus exact reproduction on real exchange data. The 4–10× Sharpe gap opens across every period slice; buy-and-hold dominates on the recent window.

| Slice | Ann. return | Sharpe |
|---|---|---|
| Published claim | 155.8% | **1.94** |
| Reproduced, full (2018+) | 9.3% | 0.27 |
| Reproduced, claim window | 4.6% | 0.12 |
| Reproduced, recent-best (2023+) | 7.7% | 0.42 |
| BTC buy-and-hold (recent) | 28.9% | 0.74 |

![External stat-arb momentum: claimed Sharpe (1.94) versus reproduced Sharpe across period slices (full 0.27, claim-window 0.12, recent-best 0.42) and BTC buy-and-hold (0.74) on the same window. The gap opens before any gate is applied.](figures/fig6_external_sr.png)

*Honest framing.* The 4–10× gap between the claimed and reproduced Sharpe opens *even before* the gates apply: re-running the published rule on the full real history of the same exchange already loses most of the edge. The collapse is driven primarily by survivorship — the original likely used a broader universe including newer, more volatile alts not liquid throughout the sample, whereas we restrict to eight persistent majors with continuous history since 2018+ — plus realism gaps (daily bars hide intra-day risk; no maker/slippage sensitivity). The gates then formalize and confirm the issues, but the root discrepancy is data selection and missing realism, not solely our checklist.

### 5.5 Statistical Rigor on the Synchronized BTC-Hourly Family

The rigorous joint statistics are valid only on the one family that admits a synchronized T×N net-return matrix: four hourly-BTC variants dumped per bar (0.10% round-trip already subtracted). The matrix has T = 21,949 hourly bars, N = 4, common window 2023-12-27 to 2026-06-28 UTC; maximum off-diagonal |ρ| = 0.162 (no cluster collapse); all four clear the ≥ 30-bet threshold. Annualized Sharpes are all negative (−0.57, −1.45, −2.65, −2.83). With SR₀ = 1.20 × 10⁻² from the cross-trial variance, every DSR is ≈ 0 (maximum 3.5 × 10⁻³, all ≪ 0.95; Table 4). CSCV PBO is a low 0.032, but this is *not* evidence of an edge: since all four Sharpes are negative, the in-sample-best variant is merely the "least bad," and 87.3% of OOS splits remain negative — PBO here measures the stability of losers. The White Reality Check (stationary bootstrap, mean block 24 bars, 2000 resamples, vs. a zero benchmark) gives statistic −5.25 × 10⁻⁵, p = 1.000; the Hansen SPA gives −0.881, p = 0.994. The no-edge null is not rejected (Figure 7).

**Table 4.** Deflated Sharpe Ratio on the BTC-hourly family (empirical skew/kurtosis; SR₀ from cross-trial variance). Every DSR is ≈ 0; since all Sharpes are negative, no variant can exceed SR₀ > 0.

| Variant | SR (ann.) | DSR | skew / exc. kurt |
|---|---|---|---|
| TA+funding | −0.571 | **3.5 × 10⁻³** | −3.44 / 427.9 |
| Risk-reward | −1.454 | 2.1 × 10⁻⁵ | −0.96 / 66.2 |
| Asym. barrier | −2.833 | 4.0 × 10⁻⁹ | +4.61 / 156.2 |
| GBT barrier | −2.652 | 2.1 × 10⁻¹⁰ | −3.91 / 114.3 |

![Rigorous confirmation on the synchronized BTC-hourly family: all annualized Sharpes negative, all Deflated Sharpe Ratios ≈ 0, White Reality Check p = 1.000, Hansen SPA p = 0.994. The no-edge-over-zero null is not rejected.](figures/fig10_stat_confirmation.png)

![The three claims the audit caught, before versus after realism: gold +173% → −33% (accounting bug), basis Sharpe ~12 → < 2 (execution assumptions), and external momentum Sharpe 1.94 → 0.12–0.42 (survivorship). Each "attractive" result reduces to a documented, reproducible artefact.](figures/fig11_three_caught.png)

## 6. Discussion and Limitations

The negative baseline is robust within scope: free hourly/daily OHLCV plus funding/CVD/open interest on liquid majors, walk-forward, causal features, explicit costs, 1% risk. Funding and CVD rank high in feature importance yet never produce stable PF > 1 after costs. Volatility targeting reduces drawdown by ~47–50 pp but leaves Sharpe flat or worse after rebalance drag at hourly frequency (Figure 10); asymmetric barriers drop win-rate ~20 pp (54.6% → 29.2%) without rescuing expectancy (Figure 9) — a direct illustration that a favourable hit-rate is not positive expectancy when the loss tail is heavy.

![Win-rate across assets and barrier geometries: the ~20 pp drop from symmetric (54.6%) to asymmetric 1.5/0.5 barriers (29.2%) does not rescue expectancy. Win-rate and profitability are decoupled once the loss tail is fat.](figures/fig4_winrate_transfer.png)

![Volatility targeting reduces maximum drawdown by ~47–50 pp yet leaves Sharpe flat or worse after rebalance drag at hourly frequency — risk is reshaped, not improved on a risk-adjusted basis.](figures/fig5_vol_target_dd.png)

*Limitations.* The rigorous joint CSCV/RC/SPA is valid only for the BTC-hourly family; cross-asset/period variants do not align into a common matrix and carry per-variant DSR only. Several patched cells have tiny N (basis 1–2 entries; one funding-rule cell n = 6) and are marked "no inference." Scope is free data only: paid limit-order-book depth, on-chain cohorts, or higher-frequency paid feeds lie outside budget and may harbor edge. The external reproduction used eight persistent liquid symbols with continuous history since 2018+; the original may have used a broader, survivorship-tilted universe whose exact composition is unavailable. There is no live forward paper-trading beyond the campaign window, and the one-minute micro-flow proxy shows near-zero information coefficient after costs.

## 7. Conclusion

On the free-data surface commonly accessible to retail researchers, systematic walk-forward, causal labeling, realistic cost subtraction, and a seven-gate skeptical checklist yield a clean negative result: no durable edge across machine-learning, rule, funding, basis, and micro variants. On the one family that admits a synchronized returns matrix, rigorous DSR/PBO/RC/SPA confirm no edge over a zero benchmark. Two internally generated "attractive" results were shown to be inflated by an accounting bug (gold) and optimistic pre-patch execution assumptions (basis), and one external public claim collapsed largely under survivorship and missing realism. The contribution is a formalized checklist, worked before/after case studies, and a transparent, fully reproducible negative baseline; the underlying statistical methods are prior art. We recommend that any future claim on public or low-cost data be accompanied by (1) gate-checklist output, (2) DSR/PBO/RC/SPA on a synchronized returns matrix (per-variant DSR otherwise), and (3) an explicit survivorship discussion. A fully reproducible bundle — input hashes (SHA-256), pinned versions, and a fixed seed — is released for exact reproduction.

## References

[1] D. H. Bailey and M. López de Prado. 2014. The Deflated Sharpe Ratio. *J. Portf. Manag.* 40, 5 (2014), 94–107.
[2] D. H. Bailey, J. M. Borwein, M. López de Prado, and Q. J. Zhu. 2015. The Probability of Backtest Overfitting. *J. Comput. Finance* 20, 4 (2015), 39–69.
[3] M. López de Prado. 2018. *Advances in Financial Machine Learning*. Wiley.
[4] C. R. Harvey. 2019. Backtesting. Working paper (SSRN).
[5] H. White. 2000. A Reality Check for Data Snooping. *Econometrica* 68, 5 (2000), 1097–1126.
[6] P. R. Hansen. 2005. A Test for Superior Predictive Ability. *J. Bus. Econ. Stat.* 23, 4 (2005), 365–380.
[7] D. N. Politis and J. P. Romano. 1994. The Stationary Bootstrap. *J. Amer. Statist. Assoc.* 89, 428 (1994), 1303–1313.
[8] L. Grinsztajn, E. Oyallon, and G. Varoquaux. 2022. Why Do Tree-Based Models Still Outperform Deep Learning on Tabular Data? *arXiv:2207.08815*.
[9] R. Shwartz-Ziv and A. Armon. 2021. Tabular Data: Deep Learning Is Not All You Need. *arXiv:2106.03253*.
[10] A. Moreira and T. Muir. 2017. Volatility-Managed Portfolios. *J. Finance* 72, 4 (2017), 1611–1644.
[11] K. Deng. 2025. AutoQuant: An Auditable Expert-System Framework for Execution-Constrained Auto-Tuning in Cryptocurrency Perpetual Futures. *arXiv:2512.22476*.
[12] Y. Liu and A. Tsyvinski. 2021. Risks and Returns of Cryptocurrency. *Rev. Financ. Stud.* 34, 6 (2021), 2689–2727.
[13] I. Makarov and A. Schoar. 2020. Trading and Arbitrage in Cryptocurrency Markets. *J. Financ. Econ.* 135, 2 (2020), 293–319.
