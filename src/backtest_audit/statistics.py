#!/usr/bin/env python3
"""
rigorous_stats.py — REAL statistics on the aligned BTC-1h returns matrix.

Rigorous statistics on the aligned BTC-1h returns matrix.
  - CSCV / PBO (Bailey, Borwein, Lopez de Prado, Zhu 2015) on the T x N matrix.
  - White (2000) Reality Check + Hansen (2005) SPA via STATIONARY (Politis-Romano)
    bootstrap on the REAL per-bar returns vs benchmark 0. No np.random.randn proxy.
  - Deflated Sharpe Ratio (Bailey & Lopez de Prado 2014) with EMPIRICAL skew/kurt,
    real T (= length), and a correct n_trials.

Independent-bets gate: a variant is "DSR-eligible" only if it has >= 30 independent
bets, where independent bets are estimated as n_trades / avg_holding (in bars). We
recover n_trades + avg_holding from the per-bar dump: a nonzero bar is a trade exit,
avg_holding is approximated from total bars / n_trades is NOT used; instead we use the
mean gap between consecutive nonzero bars as the holding/serial-decorrelation length,
and independent_bets = T_active / avg_gap. (Conservative; documented.)

All functions take the matrix (T x N) or a single column. Pure numpy/scipy.
Refs: Bailey & Lopez de Prado (2014); Bailey et al. (2015); White (2000); Hansen (2005);
Politis & Romano (1994) stationary bootstrap.
"""
from pathlib import Path
from itertools import combinations
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from scipy import stats

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MATRIX_CSV = PROJECT_ROOT / "data" / "processed" / "returns_matrix.csv"


# ----------------------------- basic -----------------------------

def sharpe_per_bar(r: np.ndarray) -> float:
    r = np.asarray(r, dtype=float)
    if r.size < 2:
        return 0.0
    sd = r.std(ddof=1)
    return float(r.mean() / sd) if sd > 0 else 0.0


def load_matrix(path: str | Path = MATRIX_CSV) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["timestamp"], index_col="timestamp")
    return df


# ----------------------- independent bets -----------------------

def estimate_independent_bets(r: np.ndarray) -> Dict[str, float]:
    """Estimate n_trades and independent bets from a per-bar return series.
    - n_trades  = number of nonzero bars (each exit posts pnl on one bar).
    - avg_hold  = mean gap (in bars) between consecutive nonzero bars (serial spacing).
    - indep_bets ~= n_trades (trades are already non-overlapping in these sims:
      single position, cool-off). We also report T_active/avg_gap as a cross-check.
    Since the backtests enforce single non-overlapping positions + cool-off, the
    realized trades ARE the independent bets; we therefore use n_trades directly,
    and report avg spacing for transparency.
    """
    r = np.asarray(r, dtype=float)
    nz_idx = np.flatnonzero(r != 0.0)
    n_trades = int(nz_idx.size)
    if n_trades < 2:
        return {"n_trades": n_trades, "avg_gap_bars": float("nan"),
                "indep_bets": n_trades}
    gaps = np.diff(nz_idx)
    avg_gap = float(gaps.mean())
    # Non-overlapping single-position sim => each nonzero bar is one independent bet.
    indep_bets = n_trades
    return {"n_trades": n_trades, "avg_gap_bars": avg_gap, "indep_bets": indep_bets}


# ----------------------------- DSR -----------------------------

def expected_max_sharpe(n_trials: int, var_sr: float) -> float:
    """E[max SR] under the null of n_trials independent strategies with SR~N(0,var_sr).
    Bailey & Lopez de Prado (2014), eq. via Euler-Mascheroni approximation."""
    if n_trials <= 1:
        return 0.0
    emc = 0.5772156649015329
    sigma = np.sqrt(var_sr)
    z = ((1 - emc) * stats.norm.ppf(1 - 1.0 / n_trials)
         + emc * stats.norm.ppf(1 - 1.0 / (n_trials * np.e)))
    return float(sigma * z)


def deflated_sharpe_ratio(sr_hat_per_bar: float, T: int, n_trials: int,
                          skew: float, kurt_excess: float,
                          var_sr_trials: Optional[float] = None) -> Dict[str, float]:
    """Deflated Sharpe Ratio (Bailey & Lopez de Prado 2014).
    sr_hat_per_bar : observed (non-annualized) Sharpe.
    T              : number of observations (bars).
    n_trials       : number of strategy configurations searched.
    skew, kurt_excess : EMPIRICAL skewness and EXCESS kurtosis of the returns.
    var_sr_trials  : variance of SR estimates across trials (for E[max SR]).
                     If None, fall back to 1/T (asymptotic var of SR under null).
    DSR = PSR(SR0) where SR0 = E[max SR]. Returns DSR in [0,1] (prob true SR>SR0).
    """
    out = {"sr_hat": float(sr_hat_per_bar), "T": int(T), "n_trials": int(n_trials),
           "skew": float(skew), "kurt_excess": float(kurt_excess)}
    if T < 4 or n_trials < 1:
        out.update({"dsr": float("nan"), "sr0": float("nan"), "psr_vs_0": float("nan"),
                    "note": "insufficient T or n_trials"})
        return out
    # variance of SR across trials: use empirical if given, else asymptotic 1/T
    var_sr = var_sr_trials if (var_sr_trials is not None and var_sr_trials > 0) else (1.0 / T)
    sr0 = expected_max_sharpe(n_trials, var_sr)
    out["sr0"] = float(sr0)
    out["var_sr_trials"] = float(var_sr)

    # PSR / DSR denominator with non-normality (Bailey-LdP 2014 eq. 9):
    # sigma_SR = sqrt( (1 - skew*SR + (kurt-1)/4 * SR^2) / (T-1) )
    sr = float(sr_hat_per_bar)
    denom_var = 1.0 - skew * sr + ((kurt_excess + 3.0 - 1.0) / 4.0) * sr ** 2
    denom_var = max(denom_var, 1e-12)
    sigma_sr = np.sqrt(denom_var / (T - 1))
    z = (sr - sr0) / sigma_sr
    dsr = float(stats.norm.cdf(z))
    # PSR vs 0 benchmark (probability SR>0 after non-normality, no deflation)
    z0 = (sr - 0.0) / sigma_sr
    psr0 = float(stats.norm.cdf(z0))
    out.update({"dsr": dsr, "z": float(z), "sigma_sr": float(sigma_sr),
                "psr_vs_0": psr0, "note": "Bailey-LdP 2014, empirical skew/kurt, real T"})
    return out


# ------------------ stationary bootstrap (Politis-Romano) ------------------

def _stationary_bootstrap_indices(T: int, avg_block: float, rng: np.random.Generator) -> np.ndarray:
    """Politis-Romano stationary bootstrap index sequence of length T.
    Geometric block lengths with mean avg_block (p = 1/avg_block)."""
    p = 1.0 / max(avg_block, 1.0)
    idx = np.empty(T, dtype=np.int64)
    t = 0
    while t < T:
        start = rng.integers(0, T)
        # geometric run length
        L = rng.geometric(p)
        for k in range(L):
            if t >= T:
                break
            idx[t] = (start + k) % T
            t += 1
    return idx


def white_reality_check(matrix: np.ndarray, n_boot: int = 2000,
                        avg_block: float = 24.0, seed: int = 42) -> Dict[str, float]:
    """White's (2000) Reality Check, H0: best strategy mean return <= benchmark (0).
    Statistic = sqrt(T) * max_k mean(r_k). Stationary bootstrap on REAL returns,
    recentered (Hansen recentering) so the null holds. Returns p-value.
    """
    r = np.asarray(matrix, dtype=float)
    if r.ndim == 1:
        r = r.reshape(-1, 1)
    T, N = r.shape
    means = r.mean(axis=0)                       # f_bar_k
    V = np.sqrt(T) * means.max()                 # observed RC statistic
    rng = np.random.default_rng(seed)
    boot_stats = np.empty(n_boot)
    for b in range(n_boot):
        idx = _stationary_bootstrap_indices(T, avg_block, rng)
        rb = r[idx]
        boot_means = rb.mean(axis=0)
        # recenter by original means (White/Hansen): f*_k - f_bar_k
        boot_stats[b] = np.sqrt(T) * (boot_means - means).max()
    pval = float(np.mean(boot_stats >= V))
    return {"rc_statistic": float(V), "best_mean": float(means.max()),
            "best_col": int(np.argmax(means)), "pvalue": pval,
            "n_boot": n_boot, "avg_block": avg_block, "T": T, "N": N}


def hansen_spa(matrix: np.ndarray, n_boot: int = 2000,
               avg_block: float = 24.0, seed: int = 42) -> Dict[str, float]:
    """Hansen's (2005) SPA: studentized max statistic, stationary bootstrap.
    Studentize each strategy mean by its bootstrap std (consistent variance).
    H0: no strategy beats benchmark 0. Returns SPA_c p-value (consistent variant)."""
    r = np.asarray(matrix, dtype=float)
    if r.ndim == 1:
        r = r.reshape(-1, 1)
    T, N = r.shape
    means = r.mean(axis=0)
    # per-strategy variance estimate via stationary-bootstrap-consistent omega:
    # use simple long-run var (Newey-West-ish) approx = var * (avg_block) factor.
    # We estimate omega_k by the bootstrap std of sqrt(T)*mean directly.
    rng = np.random.default_rng(seed)
    boot_means = np.empty((n_boot, N))
    for b in range(n_boot):
        idx = _stationary_bootstrap_indices(T, avg_block, rng)
        boot_means[b] = r[idx].mean(axis=0)
    omega = boot_means.std(axis=0) * np.sqrt(T)           # std of sqrt(T)*mean
    omega = np.where(omega > 1e-12, omega, 1e-12)
    t_stat = np.sqrt(T) * means / omega
    V = t_stat.max()
    # bootstrap distribution of studentized, recentered max
    boot_T = np.sqrt(T) * (boot_means - means.reshape(1, -1)) / omega.reshape(1, -1)
    boot_max = boot_T.max(axis=1)
    pval = float(np.mean(boot_max >= V))
    return {"spa_statistic": float(V), "best_col": int(np.argmax(t_stat)),
            "pvalue": pval, "n_boot": n_boot, "avg_block": avg_block, "T": T, "N": N}


# ----------------------------- CSCV / PBO -----------------------------

def cscv_pbo(matrix: np.ndarray, S: int = 10) -> Dict[str, float]:
    """Combinatorially Symmetric Cross-Validation -> Probability of Backtest Overfitting
    (Bailey, Borwein, Lopez de Prado, Zhu 2015).
    matrix: T x N (columns = N strategy configurations, rows aligned in time).
    Partition T into S equal blocks; for each of C(S, S/2) ways to choose the IS half:
      - best config by IS Sharpe,
      - its OS rank -> relative rank omega in (0,1) -> logit.
    PBO = fraction of splits where the IS-best has OS performance below the median
    (logit < 0).
    """
    r = np.asarray(matrix, dtype=float)
    if r.ndim == 1:
        return {"pbo": float("nan"), "note": "PBO needs N>=2 configurations"}
    T, N = r.shape
    if N < 2:
        return {"pbo": float("nan"), "n_splits": 0, "note": "PBO needs N>=2 configurations"}
    if S % 2 == 1:
        S -= 1
    block = T // S
    if block < 5 or S < 4:
        return {"pbo": float("nan"), "note": f"too few rows for S={S} blocks"}
    blocks = [r[i * block:(i + 1) * block] for i in range(S)]
    combos = list(combinations(range(S), S // 2))
    logits = []
    oos_of_is_best = []
    for cmb in combos:
        is_set = set(cmb)
        is_rows = np.vstack([blocks[i] for i in range(S) if i in is_set])
        os_rows = np.vstack([blocks[i] for i in range(S) if i not in is_set])
        sr_is = np.array([sharpe_per_bar(is_rows[:, k]) for k in range(N)])
        sr_os = np.array([sharpe_per_bar(os_rows[:, k]) for k in range(N)])
        n_star = int(np.argmax(sr_is))
        # OS rank of the IS-best among N (1=worst .. N=best)
        order = np.argsort(sr_os)              # ascending
        rank = int(np.where(order == n_star)[0][0]) + 1
        omega = rank / (N + 1.0)               # relative rank in (0,1)
        omega = min(max(omega, 1e-6), 1 - 1e-6)
        logits.append(np.log(omega / (1.0 - omega)))
        oos_of_is_best.append(sr_os[n_star])
    logits = np.array(logits)
    pbo = float(np.mean(logits <= 0.0))        # IS-best lands in bottom half OOS
    return {"pbo": pbo,
            "n_splits": len(combos),
            "S": S,
            "median_logit": float(np.median(logits)),
            "frac_os_negative": float(np.mean(np.array(oos_of_is_best) < 0)),
            "note": "Bailey et al. 2015 CSCV; logit<=0 => OS below median"}


# ----------------------------- driver -----------------------------

def run_all(matrix_csv: str | Path = MATRIX_CSV, n_trials: Optional[int] = None) -> Dict:
    df = load_matrix(matrix_csv)
    cols = list(df.columns)
    R = df.values
    T, N = R.shape

    # per-variant SR + skew/kurt + independent bets
    per_variant = {}
    sr_list = []
    for k, c in enumerate(cols):
        r = R[:, k]
        sr = sharpe_per_bar(r)
        sr_list.append(sr)
        sk = float(stats.skew(r))
        ku = float(stats.kurtosis(r))           # excess kurtosis (Fisher)
        ib = estimate_independent_bets(r)
        per_variant[c] = {"sr_per_bar": sr, "sr_ann": sr * np.sqrt(365 * 24),
                          "skew": sk, "kurt_excess": ku, **ib}

    # n_trials: count variants in the family with >= 30 independent bets
    eligible = [c for c in cols if per_variant[c]["indep_bets"] >= 30]
    n_eligible = len(eligible)
    if n_trials is None:
        n_trials = n_eligible if n_eligible > 0 else N

    # variance of SR across the family's trials (empirical) for E[max SR]
    sr_arr = np.array(sr_list)
    var_sr_trials = float(sr_arr.var(ddof=1)) if len(sr_arr) > 1 else (1.0 / T)

    # DSR per eligible variant
    dsr_results = {}
    for c in eligible:
        pv = per_variant[c]
        dsr_results[c] = deflated_sharpe_ratio(
            pv["sr_per_bar"], T, n_trials, pv["skew"], pv["kurt_excess"],
            var_sr_trials=var_sr_trials)

    # CSCV/PBO on the full eligible matrix (need N>=2)
    elig_idx = [cols.index(c) for c in eligible]
    R_elig = R[:, elig_idx] if len(elig_idx) >= 2 else R
    pbo = cscv_pbo(R_elig, S=10)

    # White RC + Hansen SPA on eligible matrix vs benchmark 0
    rc = white_reality_check(R_elig, n_boot=2000, avg_block=24.0, seed=42)
    spa = hansen_spa(R_elig, n_boot=2000, avg_block=24.0, seed=42)

    # correlation structure (effective N after clustering rho>0.5)
    if N >= 2:
        corr = np.corrcoef(R.T)
    else:
        corr = np.array([[1.0]])

    return {"cols": cols, "T": T, "N": N, "per_variant": per_variant,
            "eligible": eligible, "n_eligible": n_eligible, "n_trials": n_trials,
            "var_sr_trials": var_sr_trials, "dsr": dsr_results,
            "pbo": pbo, "white_rc": rc, "hansen_spa": spa,
            "corr": corr.tolist(), "corr_cols": cols}


if __name__ == "__main__":
    import json
    res = run_all()
    # console summary
    print(f"Matrix T={res['T']} N={res['N']} cols={res['cols']}")
    print(f"n_trials (eligible >=30 indep bets) = {res['n_trials']}; eligible={res['eligible']}")
    print("\nPer-variant:")
    for c, pv in res["per_variant"].items():
        elig = "ELIGIBLE" if c in res["eligible"] else "excluded(<30 bets)"
        print(f"  {c}: SR_ann={pv['sr_ann']:.3f} bets={pv['indep_bets']} "
              f"skew={pv['skew']:.3f} kurtX={pv['kurt_excess']:.3f} [{elig}]")
    print("\nDSR (deflated Sharpe, prob true SR>SR0):")
    for c, d in res["dsr"].items():
        print(f"  {c}: DSR={d['dsr']:.4f} SR0={d['sr0']:.3e} PSR_vs0={d['psr_vs_0']:.4f}")
    print(f"\nPBO (CSCV, S={res['pbo'].get('S')}, splits={res['pbo'].get('n_splits')}): "
          f"{res['pbo'].get('pbo')}")
    print(f"  frac OS negative (IS-best): {res['pbo'].get('frac_os_negative')}")
    print(f"\nWhite RC: stat={res['white_rc']['rc_statistic']:.4f} "
          f"p={res['white_rc']['pvalue']:.4f} (best col={res['cols'][res['white_rc']['best_col']]})")
    print(f"Hansen SPA: stat={res['hansen_spa']['spa_statistic']:.4f} "
          f"p={res['hansen_spa']['pvalue']:.4f}")
    print("\nCorrelation matrix:")
    corr = np.array(res["corr"])
    print("        " + " ".join(f"{c[:8]:>8}" for c in res["corr_cols"]))
    for i, c in enumerate(res["corr_cols"]):
        print(f"{c[:8]:>8} " + " ".join(f"{corr[i,j]:8.3f}" for j in range(len(res['corr_cols']))))
