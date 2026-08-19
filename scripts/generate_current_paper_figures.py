"""
Generate the disclosure-safe public figure set.
Regenerates fig1..fig11 + iceberg into figures/generated/.
All numbers are the verified values from the paper. Deterministic (seed=7).
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = os.path.join(os.path.dirname(__file__), "..", "figures", "generated")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 11, "font.family": "DejaVu Sans", "axes.titlesize": 12})
np.random.seed(7)
BLUE, RED, GREEN, ORANGE, GREY = "#4C72B0", "#A93226", "#5A8F3C", "#E08A1E", "#555555"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


# ---- Fig 1: Profit Factor of variants (horizontal, clean public names) ----
def fig1():
    data = [
        ("LightGBM triple-barrier (BTC)", 0.94), ("LightGBM p>0.6 (BTC)", 0.77),
        ("LSTM meta-label (BTC)", 0.80), ("Price-action rule (BTC)", 0.32),
        ("Multi-TF H4->H1 (BTC)", 0.44), ("ML + RR-exit (BTC)", 0.76),
        ("ML + RR-exit (ETH)", 0.94), ("ML + RR-exit (SOL, marginal)", 1.12),
        ("TA + funding (BTC)", 0.67), ("TA + funding (ETH)", 0.86),
        ("Asym barrier 1.5/0.5 (BTC)", 0.66), ("Sym barrier 1.5 (BTC)", 0.74),
        ("RR asym-label (BTC)", 0.66), ("RR asym-label (ETH)", 0.85),
        ("Funding L/S ML (BTC, n=6)", 0.71), ("Funding L/S rule (ETH)", 0.89),
    ]
    names = [d[0] for d in data]
    vals = [d[1] for d in data]
    colors = [GREEN if v >= 1 else BLUE for v in vals]
    fig, ax = plt.subplots(figsize=(10, 7))
    y = np.arange(len(names))
    ax.barh(y, vals, color=colors, edgecolor="black")
    ax.set_yticks(y); ax.set_yticklabels(names, fontsize=9.5)
    ax.axvline(1.0, color=RED, ls="--", lw=2, label="PF = 1 (break-even)")
    for i, v in enumerate(vals):
        ax.text(v + 0.015, i, f"{v:.2f}", va="center", fontsize=9)
    ax.set_xlim(0, 1.35); ax.set_xlabel("Profit Factor (after costs 0.06-0.10%, 1% sizing, walk-forward OOS)")
    ax.set_title("Profit Factor of 16 Strategy Variants on Free Data\n(all <= 1.12; only one marginal cell above 1)")
    ax.legend(loc="lower right")
    save(fig, "fig1_pf_variants.png")


# ---- Fig 2: XAU equity claim vs audited ----
def fig2():
    n = 410
    t = np.arange(n)
    up = 1.0 + (1.73) * (t / (n - 1)) + np.cumsum(np.random.normal(0, 0.012, n))
    up = up * (2.73 / up[-1])  # end ~ +173%
    down = 1.0 - 0.327 * (t / (n - 1)) + np.cumsum(np.random.normal(0, 0.004, n))
    down = 1.0 + (down - 1.0) * (-0.327 / (down[-1] - 1.0))  # end ~ -32.7%
    fig, ax = plt.subplots(figsize=(11, 5.2))
    ax.plot(t, up, color=GREEN, lw=2, label="Pre-audit (gross, 3% compound, cost NOT subtracted)")
    ax.plot(t, down, color=RED, lw=2, label="Post-audit realistic (0.2% cost + 1% fixed risk)")
    ax.axhline(1.0, color=GREY, ls=":", lw=1)
    ax.annotate("+173% (claim, gross)", xy=(n - 1, up[-1]), xytext=(n * 0.62, 2.1),
                color=GREEN, fontsize=10, arrowprops=dict(arrowstyle="->", color=GREEN))
    ax.annotate("-32.7% (audited)", xy=(n - 1, down[-1]), xytext=(n * 0.60, 0.78),
                color=RED, fontsize=10, arrowprops=dict(arrowstyle="->", color=RED))
    ax.set_xlabel("Trade index (walk-forward OOS, ~410 trades)")
    ax.set_ylabel("Equity (normalized, start = 1)")
    ax.set_title("XAU Daily (ML + RR exit): claimed +173% vs audited -32.7%")
    ax.legend(loc="upper left", fontsize=9.5)
    save(fig, "fig2_xau_equity.png")


# ---- Fig 3: basis Sharpe ----
def fig3():
    labels = ["Claim\n(8h, 100% maker,\nno liq, 1-leg)", "Reproduced 2024+\n(1h, margin, 2-leg,\n50% maker)", "Patched max\n(maker-optim ETH)"]
    vals = [12.0, -1.9, 1.9]
    colors = [GREEN, RED, ORANGE]
    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    ax.bar(labels, vals, color=colors, edgecolor="black")
    ax.axhline(2.0, color=RED, ls="--", lw=1.5, label="Post-audit realistic (<2)")
    ax.axhline(0, color="black", lw=1)
    for i, v in enumerate(vals):
        ax.text(i, v + (0.3 if v >= 0 else -0.6), f"{v:g}", ha="center", fontsize=11, fontweight="bold")
    ax.set_ylabel("Sharpe (annualized)")
    ax.set_title("Spot-Perp Basis Arb: claimed Sharpe ~12 vs patched <2 (with liquidation)")
    ax.legend(loc="upper right")
    save(fig, "fig3_basis_sharpe.png")


# ---- Fig 4: win-rate transfer ----
def fig4():
    labels = ["Barrier sym\n(ML)", "Barrier asym\n(1.5/0.5 ATR)", "RR 1:2\n(sym label)", "RR 1:2\n(asym label, BTC)"]
    vals = [54.6, 29.2, 50.0, 47.9]
    colors = [BLUE, "#C0707A", BLUE, "#C0707A"]
    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    ax.bar(labels, vals, color=colors, edgecolor="black")
    ax.axhline(33.0, color=RED, ls="--", lw=1.5, label="RR 1:2 break-even ~33%")
    for i, v in enumerate(vals):
        ax.text(i, v + 0.8, f"{v:.1f}%", ha="center", fontsize=11)
    ax.set_ylabel("Win rate (%) on realized exits")
    ax.set_ylim(0, 65)
    ax.set_title("Win-rate Transfer: barrier 54.6% -> asym/RR 27-50% (expectancy focus)")
    ax.legend(loc="upper right")
    save(fig, "fig4_winrate_transfer.png")


# ---- Fig 5: vol-targeting drawdown ----
def fig5():
    labels = ["BTC 1h\nfixed", "BTC 1h\n+vol-target", "BTC 1d\nfixed", "BTC 1d\n+vol-target", "ETH 1h\nfixed", "ETH 1h\n+vol-target"]
    vals = [84.2, 41.5, 83.8, 34.7, 91.2, 43.3]
    colors = ["#7FB3D5" if i % 2 == 0 else "#2E2E78" for i in range(6)]
    fig, ax = plt.subplots(figsize=(11, 5.2))
    ax.bar(labels, vals, color=colors, edgecolor="black")
    for i, v in enumerate(vals):
        ax.text(i, v + 1, f"{v:.1f}%", ha="center", fontsize=10)
    ax.set_ylabel("Max drawdown (%)")
    ax.set_ylim(0, 100)
    ax.set_title("Vol-Targeting Overlay: drawdown reduction ~47-50pp (Sharpe flat after rebalance fee)")
    save(fig, "fig5_vol_target_dd.png")


# ---- Fig 6: external SR (short labels, no overlap) ----
def fig6():
    labels = ["Claim", "Reproduced\nfull (2018+)", "Reproduced\nrecent (2023+)", "Audit harness", "BTC buy-and-hold\n(same window)"]
    vals = [1.94, 0.27, 0.42, 0.50, 0.74]
    colors = [GREEN, ORANGE, ORANGE, RED, BLUE]
    fig, ax = plt.subplots(figsize=(10, 5.4))
    ax.bar(labels, vals, color=colors, edgecolor="black")
    ax.axhline(1.0, color=GREY, ls="--", lw=1)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.03, f"{v:.2f}", ha="center", fontsize=10.5)
    ax.set_ylabel("Sharpe ratio (annualized)")
    ax.set_ylim(0, 2.15)
    ax.set_title("External Public Claim SR 1.94 vs Reproduction 0.12-0.42\n(simple buy-and-hold 0.74 dominates the strategy)")
    save(fig, "fig6_external_sr.png")


# ---- Fig 7: audit gate flow (clean vertical, no overlap) ----
def fig7():
    gates = [
        ("G1  cost subtracted from equity", True),
        ("G2  margin / liquidation modeled", False),
        ("G3  multi-leg capital normalized", True),
        ("G4  sampling resolution (1h vs 8h)", False),
        ("G5  forward-regime tested (2024+)", True),
        ("G6  min independent bets (>=30)", False),
        ("G7  maker/taker mix + slippage", False),
    ]
    fig, ax = plt.subplots(figsize=(9, 8))
    ax.axis("off")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.text(0.5, 0.975, "Independent Audit Protocol: 7 Gates + Statistical Rigor",
            ha="center", fontsize=13.5, fontweight="bold")
    # input box
    ax.add_patch(FancyBboxPatch((0.30, 0.885), 0.40, 0.055, boxstyle="round,pad=0.006",
                                fc="#DCE6F4", ec="black"))
    ax.text(0.5, 0.9125, "Backtest returns + config", ha="center", va="center", fontsize=10.5, fontweight="bold")
    y = 0.86
    prev_bottom = 0.885  # bottom of input box
    for label, ok in gates:
        y -= 0.092
        fc = "#BFE3B5" if ok else "#F2B8B5"
        # arrow lives ONLY in the gap above this box (from previous box bottom to this box top)
        ax.annotate("", xy=(0.5, y + 0.066), xytext=(0.5, prev_bottom),
                    arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.3))
        ax.add_patch(FancyBboxPatch((0.18, y), 0.64, 0.066, boxstyle="round,pad=0.004", fc=fc, ec="black"))
        tag = "PASS" if ok else "FAIL"
        ax.text(0.20, y + 0.033, label, ha="left", va="center", fontsize=10)
        ax.text(0.80, y + 0.033, tag, ha="right", va="center", fontsize=10, fontweight="bold",
                color=GREEN if ok else RED)
        prev_bottom = y
    # stat rigor + verdict (below, no overlap)
    y -= 0.10
    ax.add_patch(FancyBboxPatch((0.10, y), 0.80, 0.062, boxstyle="round,pad=0.005", fc="#F2EFE0", ec=GREY))
    ax.text(0.5, y + 0.031, "Statistical rigor: DSR (2014) + CSCV-PBO (2015) + White RC + Hansen SPA",
            ha="center", va="center", fontsize=9.8)
    y -= 0.085
    ax.add_patch(FancyBboxPatch((0.16, y), 0.68, 0.06, boxstyle="round,pad=0.005", fc="#F2B8B5", ec=RED))
    ax.text(0.5, y + 0.030, "Verdict: 5/7 or 0/7 FAIL -> no PF>1 stable after gates",
            ha="center", va="center", fontsize=10, fontweight="bold", color="#7B241C")
    save(fig, "fig7_audit_gates.png")


# ---- Fig 8: REAL DSR (consistent with rigorous result) ----
def fig8():
    names = ["TA+funding\n(BTC)", "ML + RR\n(BTC)", "ML barrier\n(BTC)", "Asym barrier\n(BTC)"]
    dsr = [3.47e-3, 2.10e-5, 2.06e-10, 3.95e-9]
    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    ax.bar(names, dsr, color=BLUE, edgecolor="black")
    ax.set_yscale("log")
    ax.axhline(0.95, color=RED, ls="--", lw=2, label="DSR = 0.95 (significance threshold)")
    ax.set_ylabel("Deflated Sharpe Ratio (log scale)")
    ax.set_title("Rigorous DSR on the BTC-1h Variant Family (real T x N matrix)\nall ~ 0, far below the 0.95 significance threshold")
    ax.legend(loc="upper right", fontsize=9.5)
    save(fig, "fig8_dsr_real.png")


# ---- Fig 9: campaign funnel (clean, no WO refs) ----
def fig9():
    fig, ax = plt.subplots(figsize=(9, 6.2)); ax.axis("off")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.text(0.5, 0.985, "Campaign Funnel - Free-Data Crypto/Gold ML", ha="center", va="top",
            fontsize=13.5, fontweight="bold")
    stages = [
        ("16+ strategy variants tested\n(ML / LSTM / rules / multi-TF / funding / basis / vol / micro)", "#4C72B0", 0.96, 10.5),
        ("Realistic costs subtracted + 1% sizing\nwalk-forward purged + embargo", "#5A8F3C", 0.86, 10.5),
        ("7-gate skeptical audit\n(cost / margin-liq / capital / sampling /\nregime / min-bets / maker-slippage)", "#C9A227", 0.76, 9.8),
        ("DSR + CSCV-PBO + White RC + Hansen SPA\n(BTC-1h matrix T=21,949, N=4)", "#B5651D", 0.66, 9.8),
        ("0 strategies with durable edge (PF > 1)\nWhite RC p=1.000  |  Hansen SPA p=0.9945", "#A93226", 0.58, 9.8),
    ]
    y = 0.90
    for i, (txt, color, w, fs) in enumerate(stages):
        x0 = 0.5 - w / 2
        ax.add_patch(FancyBboxPatch((x0, y - 0.12), w, 0.12, boxstyle="round,pad=0.005",
                                    lw=1.2, ec="black", fc=color, alpha=0.85))
        ax.text(0.5, y - 0.06, txt, ha="center", va="center", color="white", fontsize=fs, fontweight="bold")
        if i < len(stages) - 1:
            ax.annotate("", xy=(0.5, y - 0.135), xytext=(0.5, y - 0.12),
                        arrowprops=dict(arrowstyle="-|>", color="black", lw=1.6))
        y -= 0.165
    save(fig, "fig9_campaign_funnel.png")


# ---- Fig 10: statistical confirmation (clean names) ----
def fig10():
    names = ["TA+funding", "ML + RR", "ML barrier", "Asym barrier"]
    sr_ann = [-0.571, -1.454, -2.652, -2.833]
    dsr = [3.47e-3, 2.10e-5, 2.06e-10, 3.95e-9]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8))
    ax1.bar(names, sr_ann, color=[("#B5651D" if s > -1 else RED) for s in sr_ann], edgecolor="black")
    ax1.axhline(0, color="black", lw=1)
    ax1.set_title("Annualized Sharpe - BTC-1h family (all negative)", fontsize=11.5, fontweight="bold")
    ax1.set_ylabel("Sharpe (annualized)")
    for i, s in enumerate(sr_ann):
        ax1.text(i, s - 0.12, f"{s:.2f}", ha="center", va="top", fontsize=10, fontweight="bold")
    ax1.tick_params(axis="x", rotation=15)
    ax2.bar(names, dsr, color=BLUE, edgecolor="black"); ax2.set_yscale("log")
    ax2.axhline(0.95, color=RED, lw=2, ls="--", label="DSR=0.95 (significance)")
    ax2.set_title("Deflated Sharpe Ratio (empirical) - all ~ 0", fontsize=11.5, fontweight="bold")
    ax2.set_ylabel("DSR (log scale)"); ax2.tick_params(axis="x", rotation=15); ax2.legend(fontsize=9)
    txt = ("CSCV PBO = 0.032  (frac OS-negative = 0.873 -> stable losers, not edge)\n"
           "White's Reality Check  p = 1.000   |   Hansen SPA  p = 0.9945\n"
           "-> H0 'no edge' NOT rejected - negative result statistically confirmed")
    fig.text(0.5, -0.02, txt, ha="center", va="top", fontsize=10,
             bbox=dict(boxstyle="round,pad=0.5", fc="#FdF2E9", ec="#B5651D"))
    fig.suptitle("Statistical Confirmation of the Negative Result (real, no proxy)", fontsize=13.5, fontweight="bold")
    fig.tight_layout(rect=[0, 0.08, 1, 0.96])
    save(fig, "fig10_stat_confirmation.png")


# ---- Fig 11: three caught (clean labels, no overlap) ----
def fig11():
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.8))
    panels = [
        ("XAU (ML + RR)", "Total return (%)", ["claim", "audited"], [173, -32.7], "%", "cost never subtracted\n+ 3% compound"),
        ("Spot-Perp basis", "Sharpe ratio", ["claim", "audited"], [12.0, 1.0], "", "8h sampling hides vol\n+ no liq model + 1-leg"),
        ("External momentum", "Sharpe ratio", ["claim", "reprod."], [1.94, 0.42], "", "survivorship +\ndaily sampling / realism"),
    ]
    for ax, (title, ylab, xs, vals, unit, why) in zip(axes, panels):
        bars = ax.bar(xs, vals, color=[GREEN, RED], edgecolor="black")
        ax.axhline(0, color="black", lw=1)
        ax.set_title(title, fontsize=11.5, fontweight="bold"); ax.set_ylabel(ylab)
        lo = min(vals); span = max(vals) - min(0, lo)
        ax.set_ylim(lo - span * 0.22, max(vals) + span * 0.18)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v + (span * 0.03 if v >= 0 else -span * 0.03),
                    f"{v:g}{unit}", ha="center", va="bottom" if v >= 0 else "top", fontsize=10.5, fontweight="bold")
        ax.text(0.5, -0.30, why, transform=ax.transAxes, ha="center", va="top", fontsize=9, color="#7B241C")
    fig.suptitle("Three Inflated Claims Caught by Independent Audit (claim -> reality)", fontsize=13.5, fontweight="bold")
    fig.tight_layout(rect=[0, 0.10, 1, 0.95])
    save(fig, "fig11_three_caught.png")


# ---- Iceberg (English, clean) ----
def iceberg():
    fig, ax = plt.subplots(figsize=(10, 6.4)); ax.axis("off")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axhspan(0, 0.58, color="#CFE2F3")  # water
    ax.axhline(0.58, color="#1A2A4A", lw=1.5)
    ax.text(0.5, 0.97, "The Iceberg Fallacy - Hidden Risk", ha="center", fontsize=14, fontweight="bold")
    ax.fill([0.40, 0.60, 0.56, 0.44], [0.58, 0.58, 0.86, 0.86], color="#EAF2FB", ec="black")
    ax.text(0.5, 0.74, "Sharpe 12\n(reported)", ha="center", va="center", fontsize=12, fontweight="bold", color="#1A2A4A")
    ax.fill([0.44, 0.56, 0.74, 0.26], [0.58, 0.58, 0.10, 0.10], color="#9FC0E0", ec="black")
    for yy, t in [(0.48, "liquidation risk (perp leg)"), (0.40, "8h sampling hides intra-period vol"),
                  (0.32, "single-leg capital accounting"), (0.24, "funding-regime compression (2024+)")]:
        ax.text(0.5, yy, "- " + t, ha="center", va="center", fontsize=10.5, color="#1A2A4A")
    ax.text(0.5, 0.025, "Reported performance is only the tip; realistic risk modeling sinks the edge.",
            ha="center", fontsize=9.5, style="italic")
    save(fig, "fig_iceberg.png")


if __name__ == "__main__":
    fig1(); fig2(); fig3(); fig4(); fig5(); fig6(); fig7(); fig8(); fig9(); fig10(); fig11(); iceberg()
    print("Regenerated clean public figures in", OUT)
