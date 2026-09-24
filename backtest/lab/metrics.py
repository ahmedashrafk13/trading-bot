"""
backtest/lab/metrics.py -- performance statistics, overfitting statistics and
benchmarks. numpy + stdlib only (the normal CDF / inverse CDF are implemented
here; there is no scipy on this machine).

Conventions (pinned by test_lab.py):
  * The equity curve is marked at every bar CLOSE; the close time of bar i is
    t[i] + dt. The initial equity is the value just before the first bar.
  * Daily returns use the last equity of each UTC day (a bar closing exactly
    at 00:00 belongs to the day that just ended). The first daily return is
    measured from the initial equity.
  * sharpe  = mean(daily r) / std(daily r, ddof=1) * sqrt(365), rf = 0.
  * sortino = mean(daily r) / sqrt(mean(min(r, 0)^2)) * sqrt(365).
  * cagr    = (E_end / E_0) ** (1 / years) - 1, years = (t[-1] + dt - t[0]) / 365.25 d.
  * max_drawdown is NEGATIVE (-0.25 = a 25% peak-to-trough fall), computed on
    every bar-close equity including the initial value.
  * calmar  = cagr / |max_drawdown|.
  * Monthly stats use UTC calendar months, last equity of each month, the
    first month measured from the initial equity.
"""
from __future__ import annotations

import itertools
import math

import numpy as np

DAY = 86400
YEAR_DAYS = 365.25
ANN = 365.0            # periods per year for daily Sharpe (crypto trades every day)


# --------------------------------------------------------------------------- #
# normal distribution (no scipy)
# --------------------------------------------------------------------------- #
def norm_cdf(x: float) -> float:
    # erfc form: accurate in the lower tail (no 1 - tiny cancellation)
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def norm_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def norm_ppf(p: float) -> float:
    """Inverse standard normal CDF: Acklam's rational approximation (rel. error
    ~1e-9) followed by one Halley step against math.erfc (-> ~1e-15). The
    upper half is computed by symmetry from the lower tail."""
    if not 0.0 < p < 1.0:
        if p == 0.0:
            return -math.inf
        if p == 1.0:
            return math.inf
        raise ValueError("p must be in [0, 1]")
    if p > 0.5:
        return -norm_ppf(1.0 - p)
    a = (-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00)
    b = (-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01)
    c = (-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00)
    d = (7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00)
    plow = 0.02425
    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        x = (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
            ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    elif p <= 1 - plow:
        q = p - 0.5
        r = q * q
        x = (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / \
            (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1)
    else:
        q = math.sqrt(-2 * math.log(1 - p))
        x = -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
            ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    e = norm_cdf(x) - p                      # Halley refinement
    u = e * math.sqrt(2 * math.pi) * math.exp(x * x / 2)
    return x - u / (1 + x * u / 2)


# --------------------------------------------------------------------------- #
# equity-curve statistics
# --------------------------------------------------------------------------- #
def daily_equity(t, dt, equity, initial):
    """(day_keys, equity at the last close of each UTC day), initial prepended
    to the equity array (key -1)."""
    t = np.asarray(t, dtype=np.int64)
    key = (t + int(dt) - 1) // DAY
    last = np.r_[key[1:] != key[:-1], True]
    return key[last], np.r_[float(initial), np.asarray(equity, float)[last]]


def _rets(e: np.ndarray) -> np.ndarray:
    prev = e[:-1]
    with np.errstate(divide="ignore", invalid="ignore"):
        r = np.where(prev > 0, e[1:] / np.where(prev > 0, prev, 1.0) - 1.0, 0.0)
    return r


def daily_returns(t, dt, equity, initial) -> np.ndarray:
    return _rets(daily_equity(t, dt, equity, initial)[1])


def sharpe(r, periods: float = ANN) -> float:
    r = np.asarray(r, float)
    if r.size < 2:
        return 0.0
    sd = r.std(ddof=1)
    return float(r.mean() / sd * math.sqrt(periods)) if sd > 0 else 0.0


def sortino(r, periods: float = ANN) -> float:
    r = np.asarray(r, float)
    if r.size < 2:
        return 0.0
    dd = math.sqrt(float(np.mean(np.minimum(r, 0.0) ** 2)))
    return float(r.mean() / dd * math.sqrt(periods)) if dd > 0 else (math.inf if r.mean() > 0 else 0.0)


def max_drawdown(equity, initial=None) -> float:
    e = np.asarray(equity, float)
    if initial is not None:
        e = np.r_[float(initial), e]
    if e.size == 0:
        return 0.0
    peak = np.maximum.accumulate(e)
    with np.errstate(divide="ignore", invalid="ignore"):
        dd = np.where(peak > 0, e / np.where(peak > 0, peak, 1.0) - 1.0, 0.0)
    return float(dd.min())


def cagr(t, dt, equity, initial) -> float:
    t = np.asarray(t, dtype=np.int64)
    years = (int(t[-1]) + int(dt) - int(t[0])) / (YEAR_DAYS * DAY)
    end = float(np.asarray(equity)[-1])
    if years <= 0:
        return 0.0
    if end <= 0:
        return -1.0
    return float((end / float(initial)) ** (1.0 / years) - 1.0)


def calmar(cagr_v: float, mdd: float) -> float:
    if mdd < 0:
        return float(cagr_v / abs(mdd))
    return math.inf if cagr_v > 0 else 0.0


def monthly_returns(t, dt, equity, initial) -> np.ndarray:
    t = np.asarray(t, dtype=np.int64)
    month = (t + int(dt) - 1).astype("datetime64[s]").astype("datetime64[M]").astype(np.int64)
    last = np.r_[month[1:] != month[:-1], True]
    return _rets(np.r_[float(initial), np.asarray(equity, float)[last]])


def moments(r):
    """(skew, Pearson kurtosis -- normal = 3) of a return series."""
    r = np.asarray(r, float)
    if r.size < 3:
        return 0.0, 3.0
    m = r - r.mean()
    m2 = float(np.mean(m ** 2))
    if m2 <= 0:
        return 0.0, 3.0
    return float(np.mean(m ** 3) / m2 ** 1.5), float(np.mean(m ** 4) / m2 ** 2)


def equity_metrics(t, dt, equity, initial) -> dict:
    t = np.asarray(t, dtype=np.int64)
    eq = np.asarray(equity, float)
    r = daily_returns(t, dt, eq, initial)
    mr = monthly_returns(t, dt, eq, initial)
    years = (int(t[-1]) + int(dt) - int(t[0])) / (YEAR_DAYS * DAY)
    c = cagr(t, dt, eq, initial)
    mdd = max_drawdown(eq, initial)
    sk, ku = moments(r)
    sr = sharpe(r)
    return {
        "start": str(np.datetime64(int(t[0]), "s")),
        "end": str(np.datetime64(int(t[-1]) + int(dt), "s")),
        "years": years, "n_days": int(r.size),
        "initial_equity": float(initial), "final_equity": float(eq[-1]),
        "total_return": float(eq[-1] / float(initial) - 1.0),
        "cagr": c, "max_drawdown": mdd, "sharpe": sr, "sortino": sortino(r),
        "calmar": calmar(c, mdd), "vol_annual": float(r.std(ddof=1) * math.sqrt(ANN)) if r.size > 1 else 0.0,
        "skew": sk, "kurtosis": ku,
        "psr": deflated_sharpe(sr, 1, max(r.size, 2), sk, ku),
        "n_months": int(mr.size),
        "pct_positive_months": float(np.mean(mr > 0)) if mr.size else 0.0,
        "best_month": float(mr.max()) if mr.size else 0.0,
        "worst_month": float(mr.min()) if mr.size else 0.0,
    }


# --------------------------------------------------------------------------- #
# trade statistics
# --------------------------------------------------------------------------- #
def trade_metrics(trades, years: float) -> dict:
    cols = trades.cols
    n_all = len(cols["pnl"])
    closed = ~cols["is_open"]
    pnl = cols["pnl"][closed]
    ret = cols["ret"][closed]
    hold = (cols["close_t"][closed] - cols["open_t"][closed]) / 3600.0
    wins, losses = pnl > 0, pnl < 0
    gw, gl = float(pnl[wins].sum()), float(-pnl[losses].sum())
    weeks = years * YEAR_DAYS / 7.0
    return {
        "n_trades": int(closed.sum()), "n_open_trades": int(n_all - closed.sum()),
        "win_rate": float(wins.mean()) if pnl.size else 0.0,
        "profit_factor": (gw / gl) if gl > 0 else (math.inf if gw > 0 else 0.0),
        "avg_win": float(ret[wins].mean()) if wins.any() else 0.0,      # return on notional
        "avg_loss": float(ret[losses].mean()) if losses.any() else 0.0,
        "avg_win_usd": float(pnl[wins].mean()) if wins.any() else 0.0,
        "avg_loss_usd": float(pnl[losses].mean()) if losses.any() else 0.0,
        "trades_per_week": float(n_all / weeks) if weeks > 0 else 0.0,
        "avg_hold_hours": float(hold.mean()) if hold.size else 0.0,
    }


def compute(res) -> dict:
    """All metrics for a sim.Result."""
    m = equity_metrics(res.t, res.dt, res.equity, res.initial_equity)
    years = m["years"]
    m.update(trade_metrics(res.trades, years))
    m["exposure"] = float(np.mean(res.gross_leverage))
    m["turnover_per_year"] = float(res.turnover / years) if years > 0 else 0.0
    m["fee_drag_per_year"] = float(res.cost_frac_sum / years) if years > 0 else 0.0
    m["funding_per_year"] = float(res.funding_frac_sum / years) if years > 0 else 0.0
    m["fees_paid"] = float(res.fees_paid)
    m["slippage_paid"] = float(res.slippage_paid)
    m["funding_paid"] = float(res.funding_paid)
    m["n_liquidations"] = int(res.n_liquidations)
    m["n_delistings"] = len(res.delistings)
    return m


def fast_sharpe(res) -> float:
    """Daily Sharpe of a Result without building trades (for grids / nulls)."""
    return sharpe(daily_returns(res.t, res.dt, res.equity, res.initial_equity))


# --------------------------------------------------------------------------- #
# overfitting statistics
# --------------------------------------------------------------------------- #
EULER_GAMMA = 0.5772156649015329


def expected_max_sharpe(n_trials: int, sr_std: float) -> float:
    """E[max SR] of n_trials independent zero-skill trials whose SR estimates
    have standard deviation sr_std (Bailey & Lopez de Prado 2014, eq. for SR0)."""
    if n_trials <= 1:
        return 0.0
    n = float(n_trials)
    return sr_std * ((1 - EULER_GAMMA) * norm_ppf(1 - 1 / n)
                     + EULER_GAMMA * norm_ppf(1 - 1 / (n * math.e)))


def deflated_sharpe(sr_annual: float, n_trials: int, n_days: int, skew: float = 0.0,
                    kurt: float = 3.0, trials_sr_std_annual: float | None = None,
                    periods_per_year: float = ANN) -> float:
    """Deflated Sharpe Ratio (Bailey & Lopez de Prado 2014): the probability
    that the true Sharpe exceeds the best Sharpe expected from n_trials
    skill-less trials.

      sr      = sr_annual / sqrt(periods_per_year)     (per-period, daily)
      SR0     = sqrt(V) * ((1-g) Z^-1(1-1/N) + g Z^-1(1-1/(N e)))
      DSR     = Phi( (sr - SR0) sqrt(n-1) / sqrt(1 - skew sr + (kurt-1)/4 sr^2) )

    kurt is PEARSON kurtosis (normal = 3). V is the variance of the trials'
    per-period Sharpe estimates; pass trials_sr_std_annual if you measured it
    across the grid, otherwise the null estimator variance 1/(n_days-1) is
    used. n_trials = 1 gives the Probabilistic Sharpe Ratio vs 0."""
    n = int(n_days)
    if n < 2:
        return float("nan")
    sr = sr_annual / math.sqrt(periods_per_year)
    if trials_sr_std_annual is None:
        sd = math.sqrt(1.0 / (n - 1))
    else:
        sd = trials_sr_std_annual / math.sqrt(periods_per_year)
    sr0 = expected_max_sharpe(n_trials, sd)
    den = 1.0 - skew * sr + (kurt - 1.0) / 4.0 * sr * sr
    if den <= 0:
        den = 1e-12
    return norm_cdf((sr - sr0) * math.sqrt(n - 1) / math.sqrt(den))


def pbo_cscv(returns_matrix, S: int = 16) -> dict:
    """Probability of Backtest Overfitting by Combinatorially Symmetric
    Cross-Validation (Bailey, Borwein, Lopez de Prado, Zhu 2014).

    returns_matrix [T, K]: per-period returns of K candidate configurations
    over the same periods. Rows are cut into S equal contiguous blocks (the
    remainder at the end is dropped); for every choice of S/2 blocks as
    in-sample (C(S, S/2) splits) the best in-sample config (by Sharpe) is
    ranked out-of-sample: w = rank/(K+1), logit = ln(w/(1-w)).
    PBO = share of splits with logit <= 0 (best IS config at or below the
    OOS median)."""
    R = np.asarray(returns_matrix, float)
    if R.ndim != 2 or R.shape[1] < 2:
        raise ValueError("returns_matrix must be [T, K] with K >= 2")
    if S % 2 or S < 2:
        raise ValueError("S must be even")
    T, K = R.shape
    m = T // S
    if m < 2:
        raise ValueError("not enough rows for S blocks")
    R = np.nan_to_num(R[: m * S]).reshape(S, m, K)
    s1 = R.sum(axis=1)               # [S, K]
    s2 = (R ** 2).sum(axis=1)
    combos = np.array(list(itertools.combinations(range(S), S // 2)))
    mask = np.zeros((len(combos), S))
    mask[np.arange(len(combos))[:, None], combos] = 1.0
    n_half = m * S // 2

    def perf(M):
        mu = (M @ s1) / n_half
        var = (M @ s2) / n_half - mu ** 2
        sd = np.sqrt(np.maximum(var, 1e-300))
        return mu / sd

    is_p = perf(mask)
    oos_p = perf(1.0 - mask)
    best = np.argmax(is_p, axis=1)
    rows = np.arange(len(combos))
    oos_best = oos_p[rows, best]
    rank = (oos_p < oos_best[:, None]).sum(axis=1) + 1          # 1..K
    w = rank / (K + 1.0)
    logit = np.log(w / (1 - w))
    return {"pbo": float(np.mean(logit <= 0)), "logits": logit,
            "n_splits": int(len(combos)), "prob_oos_loss": float(np.mean(oos_best < 0)),
            "is_sharpe_best": is_p[rows, best], "oos_sharpe_best": oos_best}


# --------------------------------------------------------------------------- #
# benchmarks
# --------------------------------------------------------------------------- #
def buy_hold(panel, symbol: str = "BTCUSDT", initial: float = 200.0,
             fee: float = 0.00055) -> dict:
    """Spot buy-and-hold: buy at the first valid open (one taker fee), mark at
    each close. No funding, no exit fee."""
    j = list(panel.symbols).index(symbol)
    o = np.asarray(panel.o, float)[:, j]
    c = np.asarray(panel.c, float)[:, j]
    first = int(np.flatnonzero(np.isfinite(o))[0])
    cf = c.copy()
    for k in range(len(cf)):                # forward-fill a 1-D series
        if not np.isfinite(cf[k]):
            cf[k] = cf[k - 1] if k > 0 else np.nan
    units = initial * (1 - fee) / o[first]
    eq = np.where(np.arange(len(c)) < first, initial, units * cf)
    eq = np.where(np.isfinite(eq), eq, initial)
    m = equity_metrics(panel.t, panel.dt, eq, initial)
    m["equity"] = eq
    return m


def btc_buy_hold(panel, initial: float = 200.0, fee: float = 0.00055) -> dict:
    return buy_hold(panel, "BTCUSDT", initial, fee)
