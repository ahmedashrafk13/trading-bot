"""
backtest/lab/test_lab.py -- pins every accounting rule of the lab harness on
synthetic panels with hand-computable answers.

    python backtest/lab/test_lab.py            # all tests
    python backtest/lab/test_lab.py -k funding # tests whose name contains 'funding'
    python backtest/lab/test_lab.py --bench    # also time run_weights on 50k x 20

Prints PASS/FAIL per test, exits non-zero if anything fails.
"""
from __future__ import annotations

import math
import os
import statistics
import sys
import tempfile
import time
import traceback
from dataclasses import dataclass, field

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import metrics as M  # noqa: E402
import nulls as NU  # noqa: E402
import sim as S  # noqa: E402
import wf as WF  # noqa: E402

try:                                   # the real Panel, if the data agent's module is importable
    from data import Panel             # noqa: E402
except Exception:                      # pragma: no cover - fallback, same fields
    @dataclass
    class Panel:
        t: np.ndarray
        dt: int
        symbols: list
        o: np.ndarray
        h: np.ndarray
        l: np.ndarray
        c: np.ndarray
        v: np.ndarray
        qv: np.ndarray
        funding: np.ndarray
        tradable: np.ndarray
        meta: dict = field(default_factory=dict)

T0 = int(np.datetime64("2024-01-01T00:00:00", "s").astype(np.int64))


def make_panel(c, o=None, h=None, l=None, funding=None, tradable=None,
               symbols=None, dt=3600, t0=T0):
    """Synthetic Panel. c/o/h/l are [T] or [T, N]. Defaults: o = c (no gaps),
    h = max(o, c), l = min(o, c), funding 0, tradable = finite close."""
    c = np.asarray(c, float)
    if c.ndim == 1:
        c = c[:, None]
    T, N = c.shape

    def arr(x, default):
        if x is None:
            return default
        x = np.asarray(x, float)
        return x[:, None] if x.ndim == 1 else x

    o = arr(o, c.copy())
    h = arr(h, np.fmax(o, c))
    l = arr(l, np.fmin(o, c))
    f = arr(funding, np.zeros((T, N)))
    tr = np.isfinite(c) & np.isfinite(o) if tradable is None else np.asarray(tradable, bool).reshape(T, N)
    syms = symbols or [f"S{j}USDT" for j in range(N)]
    t = t0 + np.arange(T, dtype=np.int64) * dt
    v = np.where(np.isfinite(c), 1.0, np.nan)
    return Panel(t=t, dt=dt, symbols=list(syms), o=o, h=h, l=l, c=c, v=v, qv=v * c,
                 funding=f, tradable=tr, meta={"synthetic": True})


def random_panel(T, N, dt=3600, seed=0, vol=0.01, funding_every=8, symbols=None):
    rng = np.random.default_rng(seed)
    lr = rng.normal(0, vol, (T, N))
    c = 100 * np.exp(np.cumsum(lr, axis=0))
    o = np.vstack([c[:1], c[:-1]]) * np.exp(rng.normal(0, vol / 4, (T, N)))
    h = np.fmax(o, c) * np.exp(np.abs(rng.normal(0, vol / 2, (T, N))))
    l = np.fmin(o, c) * np.exp(-np.abs(rng.normal(0, vol / 2, (T, N))))
    f = np.zeros((T, N))
    if funding_every:
        f[::funding_every] = rng.normal(0.0001, 0.0002, f[::funding_every].shape)
    return make_panel(c, o, h, l, funding=f, dt=dt, symbols=symbols)


NOCOST = dict(fee=0.0, slippage_bps=0.0)
TESTS = []


def test(fn):
    TESTS.append(fn)
    return fn


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# =========================================================================== #
# (1) execution timing
# =========================================================================== #
@test
def t01_future_peek_only_pays_if_executed_at_close():
    # Price alternates 100, 110, 100, 110 ... and the whole move happens as a
    # GAP between close i and open i+1 (open i+1 == close i+1, no intrabar move).
    T = 40        # (was 60; at 60 the correct curve falls below 1% of initial, where
                  # the account is now stopped per the spec -- adversarial pass)
    c = np.where(np.arange(T) % 2 == 0, 100.0, 110.0)
    p = make_panel(c, o=c.copy())
    assert all(p.c[i, 0] != p.o[i + 1, 0] for i in range(T - 1))
    w = np.zeros((T, 1))
    w[:-1, 0] = np.sign(c[1:] - c[:-1])          # peeks at the NEXT close
    res = S.run_weights(p, w, **NOCOST)
    # Wrongly filling at close i would earn every move:
    naive = 200.0 * np.prod(1 + np.abs(c[1:] / c[:-1] - 1))
    # Correctly filling at open i+1 (== c[i+1]) the peeked move is already gone
    # and the position rides the NEXT gap, which always goes the other way.
    exp = 200.0
    for i in range(T - 2):
        exp *= 1 - abs(c[i + 2] / c[i + 1] - 1)
    assert naive > 5e3, naive
    assert close(res.equity[-1], exp, 1e-9), (res.equity[-1], exp)
    assert res.equity[-1] < 20.0


@test
def t01b_fill_is_next_open_and_last_row_never_executes():
    p = random_panel(50, 2, seed=3)
    w = np.zeros((50, 2))
    w[10, 1] = 1.0                    # decided at close 10
    w[11, 1] = 0.0
    w[49, 0] = 1.0                    # last row: must never execute
    res = S.run_weights(p, w)
    tr = res.trades
    assert len(tr) == 1
    t0 = tr[0]
    assert t0["open_bar"] == 11 and t0["close_bar"] == 12, t0
    assert close(t0["entry"], p.o[11, 1]) and close(t0["exit"], p.o[12, 1])
    assert np.all(res.positions[:, 0] == 0)
    assert res.positions[10, 1] == 0 and res.positions[11, 1] != 0 and res.positions[12, 1] == 0


# =========================================================================== #
# (2) costs
# =========================================================================== #
@test
def t02_flat_prices_hand_computed_round_trip():
    p = make_panel(np.full(10, 100.0), symbols=["XYZUSDT"])     # 8bp tier
    w = np.zeros((10, 1))
    w[0] = 1.0
    res = S.run_weights(p, w)
    # buy 2 units at open 1 (notional 200), sell 2 at open 2 (notional 200)
    per_leg = 200 * (0.00055 + 0.0008)
    assert close(res.equity[-1], 200 - 2 * per_leg), res.equity[-1]
    assert close(res.fees_paid, 2 * 200 * 0.00055) and close(res.slippage_paid, 2 * 200 * 0.0008)


@test
def t02b_flat_prices_churn_loses_exactly_costs():
    T = 300
    p = make_panel(np.full((T, 3), 50.0), symbols=["BTCUSDT", "SOLUSDT", "ABCUSDT"])
    rng = np.random.default_rng(1)
    w = rng.uniform(-1.5, 1.5, (T, 3))
    res = S.run_weights(p, w, funding=False)
    assert res.fees_paid > 0
    assert close(res.equity[-1], 200 - res.fees_paid - res.slippage_paid, 1e-10)
    assert close(res.fees_paid, 0.00055 * res.notional_traded, 1e-10)
    # slippage tiers: 1bp BTC, 3bp SOL, 8bp other
    assert np.allclose(S.default_slippage_bps(["BTCUSDT", "SOLUSDT", "ABCUSDT", "ETHUSDT"]),
                       [1, 3, 8, 1])
    # flat price => all trip pnl are pure costs and sum to the loss
    tot = sum(x["pnl"] for x in res.trades)
    assert close(tot, res.equity[-1] - 200, 1e-9), (tot, res.equity[-1] - 200)


# =========================================================================== #
# (3) funding
# =========================================================================== #
@test
def t03_funding_sign_and_timing():
    T = 10
    f = np.zeros(T)
    f[0] = 0.05          # settles during bar 0 -- before the long exists (fills at open 1)
    f[4] = 0.01          # held through it
    p = make_panel(np.full(T, 100.0), funding=f)
    for side, exp in ((1.0, 198.0), (-1.0, 202.0)):
        w = np.zeros((T, 1))
        w[:-2] = side
        res = S.run_weights(p, w, **NOCOST)
        assert close(res.equity[-1], exp), (side, res.equity[-1])
        assert close(res.funding_paid, 2.0 * side)
        assert close(res.trades[0]["funding"], 2.0 * side)
    res = S.run_weights(p, np.where(np.arange(T)[:, None] < 8, 1.0, 0.0), funding=False, **NOCOST)
    assert close(res.equity[-1], 200.0)


@test
def t03b_funding_uses_qty_at_close_after_intrabar_exit():
    # A position closed at the OPEN of bar 4 does not pay bar-4 funding.
    T = 8
    f = np.zeros(T)
    f[4] = 0.01
    p = make_panel(np.full(T, 100.0), funding=f)
    w = np.zeros((T, 1))
    w[0:3] = 1.0              # executes at opens 1..3, closed at open 4
    res = S.run_weights(p, w, **NOCOST)
    assert close(res.equity[-1], 200.0), res.equity[-1]


# =========================================================================== #
# (4) liquidation
# =========================================================================== #
def _wick_panel(drop, T=10, k=5):
    c = np.full(T, 100.0)
    l = c.copy()
    l[k] = 100 * (1 - drop)
    return make_panel(c, l=l, h=c.copy())


@test
def t04_liquidation_5x_through_25pct_wick_not_1x():
    p = _wick_panel(0.25)
    w5 = np.full((10, 1), 5.0)
    r5 = S.run_weights(p, w5, **NOCOST)
    assert r5.n_liquidations == 1, r5.n_liquidations
    assert r5.liquidations[0]["bar"] == 5
    assert r5.equity[5] == 0.0 and r5.equity[-1] == 0.0      # floored, dead
    assert r5.liquidations[0]["equity_worst"] < 0
    r1 = S.run_weights(p, np.full((10, 1), 1.0), **NOCOST)
    assert r1.n_liquidations == 0 and close(r1.equity[-1], 200.0)
    r3 = S.run_weights(p, np.full((10, 1), 3.0), **NOCOST)      # 200-600+450=50 > 0.5%*450
    assert r3.n_liquidations == 0


@test
def t04b_liquidation_leaves_remainder_and_trading_continues():
    # 5x (qty 10 @100, cash -800). Low 80.3 -> worst = -800 + 803 = 3 <= 0.5% * 803
    p = _wick_panel(0.197)
    r = S.run_weights(p, np.full((10, 1), 5.0), **NOCOST)
    assert r.n_liquidations == 1
    assert close(r.liquidations[0]["equity_after"], 3.0, 1e-9)
    assert close(r.equity[5], 3.0, 1e-9)
    assert r.positions[6, 0] > 0, "targets are re-applied after a liquidation"
    # just above the threshold: no liquidation (worst 10 > 4.05)
    assert S.run_weights(_wick_panel(0.19), np.full((10, 1), 5.0), **NOCOST).n_liquidations == 0
    # liquidation costs are charged: with fees the remainder is smaller
    rf = S.run_weights(p, np.full((10, 1), 5.0), fee=0.001, slippage_bps=0.0)
    assert rf.liquidations[0]["cost"] > 0


@test
def t04c_short_liquidation_uses_high_and_gap_at_open():
    c = np.full(10, 100.0)
    h = c.copy()
    h[5] = 125.0
    p = make_panel(c, h=h)
    assert S.run_weights(p, np.full((10, 1), -5.0), **NOCOST).n_liquidations == 1
    assert S.run_weights(p, np.full((10, 1), -1.0), **NOCOST).n_liquidations == 0
    # gap: open of bar 5 at 70, then the strategy wants to rebalance at that open
    o = c.copy()
    o[5] = 70.0
    c2 = c.copy()
    c2[5] = 70.0
    p2 = make_panel(c2, o=o)
    w = np.full((10, 1), 5.0)
    w[4] = 4.0                         # forces a rebalance at the gapped open
    r = S.run_weights(p2, w, **NOCOST)
    assert r.n_liquidations == 1 and r.liquidations[0]["bar"] == 5


# =========================================================================== #
# (5)(6)(7) event stops
# =========================================================================== #
def _bars(rows):
    """rows of (o, h, l, c)"""
    a = np.asarray(rows, float)
    return make_panel(a[:, 3], o=a[:, 0], h=a[:, 1], l=a[:, 2])


FLAT = (100, 100, 100, 100)


@test
def t05_stop_gap_fills_at_open():
    p = _bars([FLAT, FLAT, FLAT, FLAT, (90, 92, 88, 91), FLAT, FLAT])
    r = S.run_events(p, [{"i": 2, "j": 0, "side": 1, "size": 1.0, "stop": 95.0}], **NOCOST)
    tr = r.trades[0]
    assert tr["entry"] == 100 and tr["exit"] == 90 and tr["close_bar"] == 4, tr
    assert close(r.equity[-1], 200 * 0.9)
    # short mirror: stop 105, bar opens 110
    p = _bars([FLAT, FLAT, FLAT, FLAT, (110, 112, 108, 109), FLAT])
    r = S.run_events(p, [{"i": 2, "j": 0, "side": -1, "size": 1.0, "stop": 105.0}], **NOCOST)
    assert r.trades[0]["exit"] == 110
    # no gap: fills AT the stop
    p = _bars([FLAT, FLAT, FLAT, FLAT, (99, 99, 90, 92), FLAT])
    r = S.run_events(p, [{"i": 2, "j": 0, "side": 1, "size": 1.0, "stop": 95.0}], **NOCOST)
    assert r.trades[0]["exit"] == 95


@test
def t06_same_bar_stop_and_target_takes_stop():
    p = _bars([FLAT, FLAT, FLAT, FLAT, (100, 112, 94, 105), FLAT])
    r = S.run_events(p, [{"i": 2, "j": 0, "side": 1, "size": 1.0, "stop": 95.0,
                          "target": 110.0}], **NOCOST)
    assert r.trades[0]["exit"] == 95.0, r.trades[0]
    # target only
    p = _bars([FLAT, FLAT, FLAT, FLAT, (100, 112, 99, 105), FLAT])
    r = S.run_events(p, [{"i": 2, "j": 0, "side": 1, "size": 1.0, "stop": 95.0,
                          "target": 110.0}], **NOCOST)
    assert r.trades[0]["exit"] == 110.0
    # open gaps THROUGH the target -> filled AT the target (a resting order is
    # hit at its own price; the better open would be optimistic). Changed from
    # 115 by the adversarial pass.
    p = _bars([FLAT, FLAT, FLAT, FLAT, (115, 116, 94, 105), FLAT])
    r = S.run_events(p, [{"i": 2, "j": 0, "side": 1, "size": 1.0, "stop": 95.0,
                          "target": 110.0}], **NOCOST)
    assert r.trades[0]["exit"] == 110.0


@test
def t07_trailing_ratchets_only_after_the_bar_check():
    # bar 3 entry @100, trail 10% -> stop 90.  bar 4: high 120, low 105: the old
    # stop (90) is checked first -> no exit; THEN ratchet to 108.  bar 5 low 107
    # -> exit at 108.  (Ratchet-before-check would exit in bar 4.)
    p = _bars([FLAT, FLAT, FLAT, FLAT, (100, 120, 105, 115), (110, 111, 107, 108), FLAT])
    r = S.run_events(p, [{"i": 2, "j": 0, "side": 1, "size": 1.0, "trail": 0.10}], **NOCOST)
    tr = r.trades[0]
    assert tr["close_bar"] == 5 and close(tr["exit"], 108.0), tr
    # short mirror
    p = _bars([FLAT, FLAT, FLAT, FLAT, (100, 95, 80, 85), (87, 93, 86, 92), FLAT])
    r = S.run_events(p, [{"i": 2, "j": 0, "side": -1, "size": 1.0, "trail": 0.10}], **NOCOST)
    tr = r.trades[0]
    assert tr["close_bar"] == 5 and close(tr["exit"], 88.0), tr


@test
def t07b_events_time_stop_rejects_and_concurrency():
    p = random_panel(60, 3, seed=5, funding_every=0)
    ents = [{"i": 5, "j": 0, "side": 1, "size": 1.0, "time_stop": 4},
            {"i": 6, "j": 0, "side": 1, "size": 1.0},                     # already open
            {"i": 6, "j": 1, "side": -1, "size": 1.0, "stop": 1.0},       # short stop below price
            {"i": 7, "j": 1, "side": 1, "size": 1.0},
            {"i": 7, "j": 2, "side": 1, "size": 1.0}]                     # > max_concurrent=2
    r = S.run_events(p, ents, max_concurrent=2)
    reasons = sorted(x["reason"] for x in r.rejected)
    assert reasons == ["already_open", "max_concurrent", "stop_wrong_side"], reasons
    t0 = [x for x in r.trades if x["symbol"] == "S0USDT"][0]
    assert t0["open_bar"] == 6 and t0["close_bar"] == 10
    assert close(t0["exit"], p.o[10, 0])


@test
def t07c_events_gross_cap_and_liquidation():
    p = _wick_panel(0.25)
    r = S.run_events(p, [{"i": 1, "j": 0, "side": 1, "size": 9.0}], max_gross_leverage=5.0,
                     **NOCOST)
    assert close(r.trades[0]["entry_notional"], 1000.0)          # cut to 5x
    assert r.n_liquidations == 1 and r.equity[-1] == 0
    r = S.run_events(p, [{"i": 1, "j": 0, "side": 1, "size": 1.0}], **NOCOST)
    assert r.n_liquidations == 0


# =========================================================================== #
# (8) metrics
# =========================================================================== #
@test
def t08_metrics_hand_computed():
    eq = np.array([110.0, 99.0, 108.9, 120.0])
    t = T0 + np.arange(4) * 86400
    m = M.equity_metrics(t, 86400, eq, 100.0)
    r = [0.1, -0.1, 0.1, 120 / 108.9 - 1]
    sr = statistics.mean(r) / statistics.stdev(r) * math.sqrt(365)
    assert close(m["sharpe"], sr, 1e-12), (m["sharpe"], sr)
    assert close(m["cagr"], 1.2 ** (365.25 / 4) - 1, 1e-12)
    assert close(m["max_drawdown"], -0.1, 1e-12)
    assert close(m["calmar"], m["cagr"] / 0.1)
    dd = math.sqrt(sum(min(x, 0) ** 2 for x in r) / 4)
    assert close(m["sortino"], statistics.mean(r) / dd * math.sqrt(365), 1e-12)
    # hourly bars: the daily sample is the last close of each UTC day; a bar
    # closing exactly at 00:00 belongs to the day that ended.
    th = T0 + np.arange(48) * 3600
    eqh = 100 + np.arange(48, dtype=float)
    k, de = M.daily_equity(th, 3600, eqh, 100.0)
    assert list(de) == [100.0, 123.0, 147.0], de
    # monthly: Jan ends at 130, Feb at 117 -> +30%, -10%
    td = T0 + np.arange(60) * 86400                          # 2024-01-01 .. 2024-02-29
    eqd = np.where(np.arange(60) < 31, 130.0, 117.0)
    mm = M.monthly_returns(td, 86400, eqd, 100.0)
    assert np.allclose(mm, [0.30, -0.10]), mm


@test
def t08b_trade_metrics_and_accounting_identity():
    p = random_panel(3000, 4, seed=11)
    rng = np.random.default_rng(2)
    w = np.repeat(rng.choice([-1.0, 0.0, 1.0], (100, 4)), 30, axis=0) * 0.8
    res = S.run_weights(p, w)
    assert res.n_liquidations == 0
    tot = sum(x["pnl"] for x in res.trades)          # every $ is attributed to a trip
    assert close(tot, res.equity[-1] - 200.0, 1e-8), (tot, res.equity[-1] - 200)
    tf = sum(x["funding"] for x in res.trades)
    assert close(tf, res.funding_paid, 1e-9)
    m = res.metrics()
    cl = [x for x in res.trades if not x["is_open"]]
    assert m["n_trades"] == len(cl)
    assert close(m["win_rate"], np.mean([x["pnl"] > 0 for x in cl]))
    gw = sum(x["pnl"] for x in cl if x["pnl"] > 0)
    gl = -sum(x["pnl"] for x in cl if x["pnl"] < 0)
    assert close(m["profit_factor"], gw / gl)
    # the same identity for the event engine (with stops and funding)
    ents = [{"i": int(i), "j": int(i % 4), "side": 1 if i % 3 else -1, "size": 1.5,
             "stop_pct": 0.02, "target_pct": 0.04, "time_stop": 48} for i in range(10, 2900, 37)]
    r = S.run_events(p, ents, max_concurrent=3)
    tot = sum(x["pnl"] for x in r.trades)
    assert close(tot, r.equity[-1] - 200.0, 1e-8), (tot, r.equity[-1] - 200)
    assert len(r.trades) > 20


# =========================================================================== #
# (9) walk-forward and lockbox
# =========================================================================== #
def _daily_panel(start="2019-01-01", end="2026-01-01", N=2, seed=7):
    t0 = int(np.datetime64(start, "s").astype(np.int64))
    t1 = int(np.datetime64(end, "s").astype(np.int64))
    T = (t1 - t0) // 86400
    p = random_panel(T, N, dt=86400, seed=seed, vol=0.03, funding_every=0)
    p.t = t0 + np.arange(T, dtype=np.int64) * 86400
    return p


def _mom_strategy(log):
    def fn(panel, params):
        log.append((dict(params), len(panel.t), int(panel.t[-1]) + int(panel.dt)))
        c = panel.c
        lb = params["lb"]
        w = np.zeros_like(c)
        w[lb:] = np.sign(c[lb:] - c[:-lb]) * params["lev"]
        return w
    return fn


@test
def t09_walk_forward_never_selects_on_test_data():
    p = _daily_panel()
    log = []
    grid = [{"lb": lb, "lev": 1.0} for lb in (5, 20, 60)]
    out = WF.walk_forward(p, _mom_strategy(log), grid, train_days=730, test_days=182,
                          step_days=182, causality_checks=0)   # exact call-order audit below
    # nothing past the lockbox was ever handed to the strategy
    assert max(x[2] for x in log) <= WF.LOCKBOX_TS
    # call order per fold: len(grid) selection calls, then one test-fold call
    k = 0
    for fi in out["folds"]:
        ia, ib, ic = fi["bars"]
        test_start = int(p.t[ib])
        for g in range(len(grid)):
            params, n, last_close = log[k]
            assert n == ib and last_close <= test_start, (fi, log[k])
            k += 1
        params, n, last_close = log[k]
        assert n == ic and params == fi["params"]
        k += 1
    assert k == len(log)
    assert out["oos_metrics"]["n_trials"] == 3 and 0 <= out["oos_metrics"]["dsr"] <= 1
    # stitched equity: one simulation over the whole OOS span
    assert len(out["oos_equity"]) == out["folds"][-1]["bars"][2] - out["folds"][0]["bars"][1]
    # rolling folds: 730-day train windows
    ia, ib, _ = out["folds"][1]["bars"]
    assert ib - ia == 730
    # anchored: every train window starts at the first bar
    out2 = WF.walk_forward(p, _mom_strategy([]), grid, mode="anchored")
    assert all(f["bars"][0] == 0 for f in out2["folds"])


@test
def t09b_lockbox_refusal_and_audit_log():
    p = _daily_panel()
    grid = [{"lb": 20, "lev": 1.0}]
    try:
        WF.walk_forward(p, _mom_strategy([]), grid, end="2025-09-01")
        raise AssertionError("walk_forward accepted an end inside the lockbox")
    except ValueError:
        pass
    WF.walk_forward(p, _mom_strategy([]), grid, end="2025-07-01")   # the boundary itself is fine
    with tempfile.TemporaryDirectory() as d:
        out = WF.walk_forward(p, _mom_strategy([]), grid, end="2025-09-01", allow_lockbox=True,
                              lockbox_log_path=os.path.join(d, "wf.log"))
    assert out["data_end"].startswith("2025-09-01")
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "lockbox.log")
        a = WF.evaluate_lockbox(p, _mom_strategy([]), grid[0], "first look", log_path=path)
        b = WF.evaluate_lockbox(p, _mom_strategy([]), grid[0], "second look", log_path=path)
        lines = open(path, encoding="utf-8").read().strip().splitlines()
        assert (a["counter"], b["counter"]) == (1, 2) and len(lines) == 2
        assert lines[1].split("\t")[0] == "2" and "second look" in lines[1]
        assert int(a["result"].t[0]) >= WF.LOCKBOX_TS


@test
def t09c_causality_checker_catches_peeking():
    p = _daily_panel("2020-01-01", "2021-06-01")
    ok = WF.check_causality(p, _mom_strategy([]), {"lb": 10, "lev": 1.0})
    assert ok["ok"], ok

    def zscore_full_sample(panel, params):               # uses future mean/std
        c = panel.c
        return (c - c.mean(axis=0)) / c.std(axis=0)
    bad = WF.check_causality(p, zscore_full_sample, {})
    assert not bad["ok"]


# =========================================================================== #
# (10) qty rounding
# =========================================================================== #
@test
def t10_round_to_qty_drops_sub_minimum_orders():
    ins = {"XYZUSDT": {"minOrderQty": 0.01, "qtyStep": 0.01, "minNotionalValue": 5.0}}
    p = make_panel(np.full(10, 100.0), symbols=["XYZUSDT"])
    w = np.full((10, 1), 0.02)                       # $4 < $5 min notional
    r = S.run_weights(p, w, instruments=ins, round_to_qty=True, **NOCOST)
    assert np.all(r.positions == 0) and len(r.trades) == 0
    w = np.full((10, 1), 0.5033)                     # 1.0066 units -> 1.00
    r = S.run_weights(p, w, instruments=ins, round_to_qty=True, **NOCOST)
    assert np.allclose(r.positions[1:, 0], 1.00), r.positions[:, 0]
    # a change of 0.004 units (below minOrderQty) is dropped; a full close is not
    w = np.full((10, 1), 0.5)
    w[4] = 0.502                                     # 1.004 -> rounds to 1.00: no order
    w[6:] = 0.0
    r = S.run_weights(p, w, instruments=ins, round_to_qty=True, **NOCOST)
    assert np.allclose(r.positions[1:7, 0], 1.0) and np.all(r.positions[7:, 0] == 0)
    w = np.full((10, 1), 0.5)
    w[4] = 0.52                                      # +0.04 units: $4 < $5 -> dropped
    r = S.run_weights(p, w, instruments=ins, round_to_qty=True, **NOCOST)
    assert np.allclose(r.positions[1:, 0], 1.0)
    # events
    r = S.run_events(p, [{"i": 1, "j": 0, "side": 1, "size": 0.02}], instruments=ins,
                     round_to_qty=True)
    assert r.rejected and r.rejected[0]["reason"] == "below_min"


# =========================================================================== #
# further accounting rules
# =========================================================================== #
@test
def t11_delisted_symbol_closes_at_last_close_with_haircut():
    T = 12
    c = np.full(T, 100.0)
    c[6:] = np.nan                                   # gone after bar 5
    p = make_panel(c, o=c.copy())
    w = np.full((T, 1), 1.0)
    r = S.run_weights(p, w, **NOCOST)
    assert len(r.delistings) == 1 and r.delistings[0]["bar"] == 7
    # 2 units closed at 100 * 0.98
    assert close(r.equity[-1], 200 - 2 * 100 * 0.02), r.equity[-1]
    s = S.run_weights(p, -w, **NOCOST)               # shorts are hair-cut upwards
    assert close(s.equity[-1], 200 - 2 * 100 * 0.02)


@test
def t12_non_tradable_forces_close_at_next_open_and_gross_clip():
    p = random_panel(30, 2, seed=9, funding_every=0)
    p.tradable[10:, 1] = False
    w = np.full((30, 2), 1.0)
    r = S.run_weights(p, w)
    assert r.positions[10, 1] != 0 and np.all(r.positions[11:, 1] == 0)
    tr = [x for x in r.trades if x["symbol"] == "S1USDT"][0]
    assert tr["close_bar"] == 11 and close(tr["exit"], p.o[11, 1])
    # gross clip: [4, 4] with max 5 -> 2.5 each
    p2 = make_panel(np.full((6, 2), 100.0))
    r2 = S.run_weights(p2, np.full((6, 2), 4.0), max_gross_leverage=5.0, **NOCOST)
    assert np.allclose(r2.positions[1] * 100 / 200, [2.5, 2.5])


@test
def t13_on_change_holds_units_every_bar_rebalances():
    c = 100 * 1.01 ** np.arange(50)
    p = make_panel(c)
    w = np.full((50, 1), 2.0)
    r = S.run_weights(p, w, **NOCOST)
    assert np.allclose(r.positions[1:, 0], r.positions[1, 0])          # units held
    g = 1.01 ** 48                                                     # 2x long, price x g
    assert close(r.gross_leverage[-1], 2 * g / (2 * g - 1), 1e-9)      # leverage drifted down
    r2 = S.run_weights(p, w, rebalance="every_bar", **NOCOST)
    assert len(np.unique(np.round(r2.positions[1:, 0], 12))) > 40
    r3 = S.run_weights(p, w, rebalance="every_bar", min_trade_frac=0.05, **NOCOST)
    n_fills = len(r3._book.fill_log)                 # one fill call per executed bar here
    assert 5 < n_fills < 30, n_fills


# =========================================================================== #
# overfitting statistics and nulls
# =========================================================================== #
@test
def t14_normal_ppf_and_deflated_sharpe():
    for pr, z, tol in ((0.975, 1.959963984540054, 1e-12), (0.5, 0.0, 1e-15),
                       (0.001, -3.090232306167813, 1e-12), (1e-6, -4.753424308822899, 1e-11),
                       (0.999999, 4.753424308822899, 1e-8)):   # 0.999999 is not exact in binary
        assert abs(M.norm_ppf(pr) - z) < tol, (pr, M.norm_ppf(pr))
        assert abs(M.norm_cdf(M.norm_ppf(pr)) - pr) < 1e-15
    # n_trials = 1 -> PSR vs 0
    sr, n, sk, ku = 1.5, 730, -0.3, 6.0
    s = sr / math.sqrt(365)
    psr = M.norm_cdf(s * math.sqrt(n - 1) / math.sqrt(1 - sk * s + (ku - 1) / 4 * s * s))
    assert close(M.deflated_sharpe(sr, 1, n, sk, ku), psr, 1e-12)
    d = [M.deflated_sharpe(sr, k, n, sk, ku) for k in (1, 10, 100, 1000)]
    assert all(a > b for a, b in zip(d, d[1:])), d
    # E[max] of 100 N(0,1) draws ~ 2.5 (known ~2.508)
    assert abs(M.expected_max_sharpe(100, 1.0) - 2.53) < 0.05


@test
def t15_pbo_cscv():
    rng = np.random.default_rng(0)
    noise = rng.normal(0, 0.01, (1600, 20))
    pb = M.pbo_cscv(noise, S=16)["pbo"]
    assert 0.25 < pb < 0.8, pb                                # skill-less grid: overfit ~half the time
    edge = noise.copy()
    edge[:, 0] += 0.004                                       # one genuinely better config
    pe = M.pbo_cscv(edge, S=16)["pbo"]
    assert pe < 0.05, pe


@test
def t16_nulls_seeded_and_preserve_exposure():
    p = random_panel(2000, 3, seed=4, funding_every=0)
    rng = np.random.default_rng(3)
    w = np.repeat(rng.choice([-1.0, 0.0, 1.0], (100, 3)), 20, axis=0)
    a = NU.random_timing_null(p, w, n=20, seed=5)
    b = NU.random_timing_null(p, w, n=20, seed=5)
    assert np.array_equal(a["null"], b["null"]) and a["method"] == "runs"
    assert 0 < a["p_value"] <= 1
    s = NU.sign_flip_null(p, w, n=20, seed=1)
    assert abs(s["null_exposure_mean"] - s["strategy_exposure"]) < 0.1 * s["strategy_exposure"]
    # a strategy with genuine foresight must sit at the top of both nulls
    cheat = np.zeros_like(w)
    cheat[:-2] = np.sign(p.o[2:] - p.o[1:-1])                 # knows the next open-to-open move
    z = NU.sign_flip_null(p, cheat, n=30, seed=2, sim_kwargs=NOCOST)
    assert z["p_value"] < 0.05, z["p_value"]
    y = NU.random_timing_null(p, cheat, n=30, seed=2, sim_kwargs=NOCOST, method="shift")
    assert y["p_value"] < 0.05, y["p_value"]


# =========================================================================== #
# ADVERSARIAL SECTION -- written by the verification pass to try to make the
# harness report an optimistic number. Each test names the failure it hunts.
# =========================================================================== #
@test
def adv01_events_future_peek_fills_next_open_not_decision_close():
    # Same trap as t01 but through run_events: side = sign of the NEXT move.
    T = 41
    c = np.where(np.arange(T) % 2 == 0, 100.0, 110.0)
    p = make_panel(c, o=c.copy())
    ents = [{"i": i, "j": 0, "side": int(np.sign(c[i + 1] - c[i])), "size": 1.0, "time_stop": 1}
            for i in range(0, T - 3, 2)]
    r = S.run_events(p, ents, **NOCOST)
    # fill at open i+1 (=110, the move already happened), exit at open i+2 (=100)
    exp = 200.0 * (100.0 / 110.0) ** len(ents)
    assert close(r.equity[-1], exp, 1e-9), (r.equity[-1], exp)
    assert all(tr["open_bar"] == e["i"] + 1 for tr, e in zip(r.trades, ents))


@test
def adv02_decision_bar_wick_cannot_stop_or_liquidate_a_position_not_yet_held():
    p = _bars([FLAT, FLAT, (100, 100, 70, 100), FLAT, FLAT, FLAT])
    r = S.run_events(p, [{"i": 2, "j": 0, "side": 1, "size": 1.0, "stop": 95.0}], **NOCOST)
    assert len(r.trades) == 1 and r.trades[0]["is_open"], r.trades[0]
    assert r.trades[0]["open_bar"] == 3
    w = np.zeros((6, 1))
    w[2:] = 5.0                                    # decided at close 2 -> held from open 3
    rw = S.run_weights(p, w, **NOCOST)
    assert rw.n_liquidations == 0 and close(rw.equity[-1], 200.0)


@test
def adv03_costs_are_charged_on_levered_notional_both_sides():
    p = make_panel(np.full(8, 100.0), symbols=["XYZUSDT"])       # 8bp tier
    exp = 200.0 - 2 * 600.0 * (0.00055 + 0.0008)                  # 3x, in and out
    w = np.zeros((8, 1))
    w[0] = 3.0
    r = S.run_weights(p, w)
    assert close(r.equity[-1], exp, 1e-12), (r.equity[-1], exp)
    e = S.run_events(p, [{"i": 0, "j": 0, "side": 1, "size": 3.0, "time_stop": 1}])
    assert close(e.equity[-1], exp, 1e-12), (e.equity[-1], exp)
    s = S.run_events(p, [{"i": 0, "j": 0, "side": -1, "size": 3.0, "time_stop": 1}])
    assert close(s.equity[-1], exp, 1e-12), (s.equity[-1], exp)


@test
def adv04_every_exit_path_pays_fee_and_slippage():
    # all symbols in the 8bp tier -> fees == 0.00055 * notional, slippage == 0.0008 * notional
    p = random_panel(1500, 3, seed=21)
    ents = [{"i": int(i), "j": int(i % 3), "side": 1 if i % 2 else -1, "size": 2.0,
             "stop_pct": 0.01, "target_pct": 0.015, "time_stop": 30, "trail": 0.02}
            for i in range(5, 1450, 11)]
    ex = np.zeros((1500, 3), bool)
    ex[::17, 1] = True
    r = S.run_events(p, ents, exits=ex, max_concurrent=3)
    assert r.notional_traded > 0 and len(r.trades) > 50
    assert close(r.fees_paid, 0.00055 * r.notional_traded, 1e-10)
    assert close(r.slippage_paid, 0.0008 * r.notional_traded, 1e-10)
    # liquidation fill and delisting fill are charged too
    lq = S.run_weights(_wick_panel(0.25), np.full((10, 1), 5.0))
    assert lq.n_liquidations == 1
    assert close(lq.slippage_paid, 0.0008 * lq.notional_traded, 1e-10)
    c = np.full(12, 100.0)
    c[6:] = np.nan
    dl = S.run_weights(make_panel(c, o=c.copy()), np.full((12, 1), 1.0))
    assert len(dl.delistings) == 1
    assert close(dl.fees_paid, 0.00055 * dl.notional_traded, 1e-10)
    assert close(dl.equity[-1], 200 - 200 * (0.00055 + 0.0008) - 2 * 98 * (0.00055 + 0.0008)
                 - 2 * 100 * 0.02, 1e-10), dl.equity[-1]


@test
def adv05_funding_on_event_path_both_signs():
    T = 10
    for rate in (0.01, -0.01):
        f = np.zeros(T)
        f[4] = rate
        p = make_panel(np.full(T, 100.0), funding=f)
        for side in (1, -1):
            r = S.run_events(p, [{"i": 0, "j": 0, "side": side, "size": 1.0}], **NOCOST)
            exp = 200.0 - side * rate * 200.0
            assert close(r.equity[-1], exp), (rate, side, r.equity[-1], exp)
            assert close(r.funding_paid, side * rate * 200.0)


@test
def adv06_funding_charged_on_current_notional_not_entry_notional():
    c = np.full(10, 100.0)
    c[3:] = 200.0
    f = np.zeros(10)
    f[5] = 0.01
    p = make_panel(c, o=c.copy(), funding=f)
    w = np.full((10, 1), 1.0)
    r = S.run_weights(p, w, **NOCOST)                 # 2 units bought at 100
    assert close(r.funding_paid, 2 * 200 * 0.01), r.funding_paid
    assert close(r.equity[-1], 200 + 200 - 4.0)


@test
def adv07_gross_leverage_clip_applies_in_both_engines():
    p = make_panel(np.full((6, 3), 100.0))
    r = S.run_weights(p, np.tile([4.0, -4.0, 2.0], (6, 1)), **NOCOST)   # gross 10 -> 5
    assert np.allclose(r.positions[1] * 100 / 200, [2.0, -2.0, 1.0]), r.positions[1]
    r = S.run_weights(p, np.full((6, 3), 10.0), max_gross_leverage=3.0, **NOCOST)
    assert np.allclose(np.abs(r.positions[1]).sum() * 100 / 200, 3.0)
    e = S.run_events(p, [{"i": 0, "j": 0, "side": 1, "size": 4.0},
                         {"i": 1, "j": 1, "side": -1, "size": 4.0}], **NOCOST)
    assert close(e.trades[1]["entry_notional"], 200.0), e.trades[1]      # only 1x room left


@test
def adv08_liquidation_values_every_leg_at_its_own_adverse_extreme():
    # hedged book: long A 2.5x, short B 2.5x. A wicks down 20%, B wicks up 20% in
    # the same bar, both close unchanged. Worst case = 200 + 5*80 - 5*120 = 0.
    T = 10
    c = np.full((T, 2), 100.0)
    h, l = c.copy(), c.copy()
    l[5, 0] = 80.0
    h[5, 1] = 120.0
    p = make_panel(c, h=h, l=l)
    w = np.tile([2.5, -2.5], (T, 1))
    r = S.run_weights(p, w, **NOCOST)
    assert r.n_liquidations == 1 and r.liquidations[0]["bar"] == 5, r.liquidations
    l[5, 0], h[5, 1] = 90.0, 110.0                    # worst = 100 > 0.5% * 1000
    r = S.run_weights(make_panel(c, h=h, l=l), w, **NOCOST)
    assert r.n_liquidations == 0


@test
def adv09_stop_beyond_the_liquidation_price_is_a_liquidation():
    # 5x long @100 (qty 10, cash -800). The bar trades down to 70. A stop at 75
    # sits BELOW the liquidation level (~80.4): the account is liquidated on the
    # way down; the stop can never "save" it and equity must never go negative.
    rows = [FLAT, FLAT, FLAT, FLAT, (100, 100, 70, 72), FLAT, FLAT, FLAT]
    p = _bars(rows)
    ents = [{"i": 2, "j": 0, "side": 1, "size": 5.0, "stop": 75.0},
            {"i": 5, "j": 0, "side": 1, "size": 1.0}]
    r = S.run_events(p, ents, **NOCOST)
    assert r.n_liquidations == 1, (r.n_liquidations, r.equity)
    assert np.all(r.equity >= 0.0), r.equity
    assert r.equity[-1] == 0.0 and np.all(r.positions[5:] == 0)
    # a stop ABOVE the liquidation level fills first and the account survives
    ents[0]["stop"] = 82.0
    r = S.run_events(p, ents[:1], **NOCOST)
    assert r.n_liquidations == 0 and close(r.equity[-1], 200 - 10 * 18.0), r.equity[-1]
    # the same for a short: 5x short @100, stop 125, bar trades up to 130
    rows = [FLAT, FLAT, FLAT, FLAT, (100, 130, 100, 128), FLAT, FLAT]
    r = S.run_events(_bars(rows), [{"i": 2, "j": 0, "side": -1, "size": 5.0, "stop": 125.0}],
                     **NOCOST)
    assert r.n_liquidations == 1 and np.all(r.equity >= 0.0), r.equity


@test
def adv10_target_gapped_through_fills_at_the_target_not_the_better_open():
    p = _bars([FLAT, FLAT, FLAT, FLAT, (115, 116, 109, 112), FLAT])
    r = S.run_events(p, [{"i": 2, "j": 0, "side": 1, "size": 1.0, "stop": 95.0,
                          "target": 110.0}], **NOCOST)
    assert r.trades[0]["exit"] == 110.0, r.trades[0]
    p = _bars([FLAT, FLAT, FLAT, FLAT, (85, 91, 84, 88), FLAT])
    r = S.run_events(p, [{"i": 2, "j": 0, "side": -1, "size": 1.0, "stop": 105.0,
                          "target": 90.0}], **NOCOST)
    assert r.trades[0]["exit"] == 90.0, r.trades[0]


@test
def adv11_event_position_in_a_delisted_symbol_pays_the_haircut():
    T = 12
    c = np.full(T, 100.0)
    c[6:] = np.nan
    p = make_panel(c, o=c.copy())
    for side in (1, -1):
        r = S.run_events(p, [{"i": 1, "j": 0, "side": side, "size": 1.0}], **NOCOST)
        assert len(r.delistings) == 1, r.delistings
        assert close(r.equity[-1], 200 - 2 * 100 * 0.02), (side, r.equity[-1])


@test
def adv12_drawdown_is_on_marked_equity_not_cash():
    c = np.array([100, 100, 50, 50, 100, 100, 100.0])
    p = make_panel(c, o=c.copy())
    r = S.run_weights(p, np.ones((7, 1)), **NOCOST)
    assert close(float(np.ptp(r.cash[1:])), 0.0)             # cash never moves
    m = r.metrics()
    assert close(m["max_drawdown"], -0.5, 1e-12), m["max_drawdown"]
    assert close(m["total_return"], 0.0, 1e-12)


@test
def adv13_sharpe_uses_daily_utc_returns_and_cagr_uses_365_25_days():
    rng = np.random.default_rng(8)
    T = 24 * 40
    th = T0 + np.arange(T, dtype=np.int64) * 3600
    eq = 100 * np.exp(np.cumsum(rng.normal(0.0002, 0.01, T)))
    m = M.equity_metrics(th, 3600, eq, 100.0)
    daily = [100.0] + [eq[k] for k in range(23, T, 24)]
    r = [daily[k + 1] / daily[k] - 1 for k in range(len(daily) - 1)]
    exp = statistics.mean(r) / statistics.stdev(r) * math.sqrt(365)
    assert close(m["sharpe"], exp, 1e-12), (m["sharpe"], exp)
    rb = np.diff(np.r_[100.0, eq]) / np.r_[100.0, eq][:-1]
    per_bar = rb.mean() / rb.std(ddof=1) * math.sqrt(365 * 24)
    assert abs(per_bar - m["sharpe"]) > 1e-3                 # not the per-bar version
    # CAGR: exactly 731 days, doubled
    td = T0 + np.arange(731, dtype=np.int64) * 86400
    e2 = np.linspace(100, 200, 731)
    assert close(M.cagr(td, 86400, e2, 100.0), 2 ** (365.25 / 731) - 1, 1e-12)


@test
def adv14_deflated_sharpe_matches_the_papers_worked_example():
    # Bailey & Lopez de Prado (2014) numerical example: SR 2.5 (annualised with
    # 250 days), T = 1250, N = 100 trials, V[SR] = 0.5, skew -3, kurt 10 -> 0.9004
    d = M.deflated_sharpe(2.5, 100, 1250, -3.0, 10.0, trials_sr_std_annual=math.sqrt(0.5),
                          periods_per_year=250)
    assert abs(d - 0.9004) < 5e-4, d


@test
def adv15_meta_arrays_are_truncated_with_the_panel():
    # data.load_panel puts [T, N] arrays in meta ("valid", "member", "tbqv",
    # "n_hours"). If slicing leaves them whole, a strategy reading them during
    # walk-forward selection sees test-fold and lockbox data (e.g. future
    # delistings via meta["valid"]).
    p = _daily_panel()
    T = len(p.t)
    p.meta = {"future": np.arange(T, dtype=float), "valid2d": np.ones((T, 2), bool),
              "scalar": 3}
    seen = []

    def strat(panel, params):
        seen.append((len(panel.t), panel.meta["future"].shape[0], panel.meta["valid2d"].shape[0],
                     float(panel.meta["future"].max())))
        return np.zeros((len(panel.t), len(panel.symbols)))
    WF.walk_forward(p, strat, [{"a": 1}], causality_checks=0)
    assert all(a == b == c and m == a - 1 for a, b, c, m in seen), seen[:3]
    # the causality checker must now catch a strategy that peeks through meta
    def peek(panel, params):
        x = panel.meta["future"]
        return np.tile((x / x[-1])[:, None], (1, len(panel.symbols)))
    assert not WF.check_causality(p, peek, {})["ok"]


@test
def adv16_price_cache_is_not_stale_after_the_panel_is_edited():
    p = make_panel(np.full(10, 100.0))
    w = np.ones((10, 1))
    S.run_weights(p, w, **NOCOST)
    p.c[5:] = 200.0                                   # in-place edit
    p.o[5:] = 200.0
    p.h[5:] = 200.0
    p.l[5:] = 200.0
    r = S.run_weights(p, w, **NOCOST)
    assert close(r.equity[-1], 400.0), r.equity[-1]
    p.funding = np.zeros((10, 1))                     # attribute replaced
    p.funding[7, 0] = 0.01
    r = S.run_weights(p, w, **NOCOST)
    assert close(r.equity[-1], 400.0 - 2 * 200 * 0.01), r.equity[-1]


@test
def adv17_walk_forward_and_lockbox_refuse_a_peeking_strategy():
    p = _daily_panel()

    def peek(panel, params):
        c = panel.c
        w = np.zeros_like(c)
        w[:-1] = np.sign(c[1:] - c[:-1])            # tomorrow's close
        return w
    try:
        out = WF.walk_forward(p, peek, [{"a": 1}])
        raise AssertionError(f"accepted a peeking strategy (OOS sharpe "
                             f"{out['oos_metrics']['sharpe']:.1f})")
    except ValueError as e:
        assert "causal" in str(e), e
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "lockbox.log")
        try:
            WF.evaluate_lockbox(p, peek, {"a": 1}, "peek", log_path=path)
            raise AssertionError("evaluate_lockbox accepted a peeking strategy")
        except ValueError as e:
            assert "causal" in str(e), e


@test
def adv18_walk_forward_carries_capital_across_folds():
    p = _daily_panel()
    grid = [{"lb": lb, "lev": 1.0} for lb in (5, 20)]
    out = WF.walk_forward(p, _mom_strategy([]), grid)
    f = out["folds"]
    assert len(f) >= 4
    assert close(f[0]["test_metrics"]["initial_equity"], 200.0)
    for a, b in zip(f, f[1:]):
        assert close(b["test_metrics"]["initial_equity"], a["test_metrics"]["final_equity"])
    growth = np.prod([x["test_metrics"]["final_equity"] / x["test_metrics"]["initial_equity"]
                      for x in f])
    assert close(200.0 * growth, out["oos_equity"][-1], 1e-9)


@test
def adv19_walk_forward_into_the_lockbox_is_logged():
    p = _daily_panel()
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "lockbox.log")
        WF.walk_forward(p, _mom_strategy([]), [{"lb": 20, "lev": 1.0}], end="2025-07-01",
                        lockbox_log_path=path)
        assert WF.lockbox_count(path) == 0
        WF.walk_forward(p, _mom_strategy([]), [{"lb": 20, "lev": 1.0}], end="2025-09-01",
                        allow_lockbox=True, lockbox_log_path=path)
        assert WF.lockbox_count(path) == 1
        assert "walk_forward" in open(path, encoding="utf-8").read()


@test
def adv20_trailing_stop_does_not_use_the_entry_bars_own_high():
    # entry @100 (open of bar 3), trail 10%: bar 3 runs to 120 and dips to 95.
    # Ratchet-before-check would exit at 108 inside bar 3 (a phantom +8%).
    p = _bars([FLAT, FLAT, FLAT, (100, 120, 95, 118), (112, 113, 105, 106), FLAT])
    r = S.run_events(p, [{"i": 2, "j": 0, "side": 1, "size": 1.0, "trail": 0.10}], **NOCOST)
    tr = r.trades[0]
    assert tr["close_bar"] == 4 and close(tr["exit"], 108.0), tr


@test
def adv21_nulls_keep_what_is_held_and_only_move_when():
    p = random_panel(1200, 2, seed=13, funding_every=0)
    rng = np.random.default_rng(4)
    w = np.repeat(rng.choice([-0.5, 0.0, 0.5, 1.0], (60, 2)), 20, axis=0)
    seen = []
    orig = S.run_weights

    def spy(panel, weights, **kw):
        seen.append(np.array(weights, float, copy=True))
        return orig(panel, weights, **kw)
    S.run_weights = spy
    try:
        NU.sign_flip_null(p, w, n=5, seed=1)
        base, nulls_sf = seen[0], seen[1:]
        for x in nulls_sf:
            assert np.array_equal(np.abs(x), np.abs(base))
        seen.clear()
        NU.random_timing_null(p, w, n=5, seed=1, method="runs")
        base, nulls_rt = seen[0], seen[1:]
        for x in nulls_rt:
            for j in range(2):
                assert np.array_equal(np.sort(x[:, j]), np.sort(base[:, j]))   # same exposure
                nb = int(np.sum(np.diff(base[:, j]) != 0))
                nx = int(np.sum(np.diff(x[:, j]) != 0))
                assert nx <= nb + 1, (nb, nx)                                   # no extra churn
        assert any(not np.array_equal(x, base) for x in nulls_rt)
    finally:
        S.run_weights = orig


@test
def adv22_gap_through_liquidation_without_a_rebalance():
    c = np.full(10, 100.0)
    c[5:] = 70.0
    p = make_panel(c, o=c.copy())                    # open of bar 5 gaps to 70
    r = S.run_weights(p, np.full((10, 1), 5.0), **NOCOST)
    assert r.n_liquidations == 1 and r.equity[-1] == 0.0
    r = S.run_weights(p, np.full((10, 1), 3.0), **NOCOST)
    assert r.n_liquidations == 0 and close(r.equity[-1], 200 - 6 * 30.0)


@test
def adv23_min_trade_frac_never_blocks_a_full_close():
    p = make_panel(np.full(8, 100.0))
    w = np.zeros((8, 1))
    w[0:3] = 0.5
    r = S.run_weights(p, w, min_trade_frac=0.9, **NOCOST)
    assert np.all(r.positions == 0)                  # 0 -> 0.5 is below the threshold
    r = S.run_weights(p, w, min_trade_frac=0.4, **NOCOST)
    assert r.positions[2, 0] != 0 and np.all(r.positions[4:] == 0)
    w[3:] = 0.1                                      # 0.5 -> 0.1: skipped, still held
    r = S.run_weights(p, w, min_trade_frac=0.45, **NOCOST)
    assert np.all(r.positions[1:, 0] != 0)


@test
def adv24_vectorised_segments_match_the_bar_by_bar_reference():
    # run_weights processes the bars between executions as one vector block.
    # It must reproduce the bar-by-bar accounting exactly: liquidations inside a
    # block, funding inside a block, gaps / delistings / universe exits.
    n_liq = n_del = 0
    for seed in range(6):
        rng = np.random.default_rng(100 + seed)
        T, N = 3000, 5
        p = random_panel(T, N, seed=seed, vol=0.02 if seed % 2 else 0.01)
        p.h[rng.integers(0, T, 15), rng.integers(0, N, 15)] *= 1.6        # squeeze wicks
        p.l[rng.integers(0, T, 15), rng.integers(0, N, 15)] *= 0.5        # crash wicks
        for j in range(N):                                                # NaN gaps
            g = rng.integers(0, T - 20)
            for arr in (p.o, p.h, p.l, p.c):
                arr[g:g + rng.integers(1, 6), j] = np.nan
        p.c[2500:, 4] = p.o[2500:, 4] = p.h[2500:, 4] = p.l[2500:, 4] = np.nan   # delisting
        p.tradable = np.isfinite(p.c) & np.isfinite(p.o)
        p.tradable[1000:1400, 2] = False                                  # universe exit
        hold = int(rng.integers(5, 60))
        w = np.repeat(rng.choice([-2.0, -1.0, 0.0, 1.0, 2.0], (T // hold + 1, N)), hold,
                      axis=0)[:T] * (1.0 + seed % 3)
        for kw in ({}, {"min_trade_frac": 0.3}, {"max_gross_leverage": 3.0, "slippage_bps": 5.0}):
            a = S.run_weights(p, w, **kw)
            b = S.run_weights(p, w, _vectorise=False, **kw)
            assert np.allclose(a.equity, b.equity, rtol=1e-11, atol=1e-9), (seed, kw)
            assert np.allclose(a.positions, b.positions, rtol=1e-10, atol=1e-12), (seed, kw)
            n_liq += a.n_liquidations
            n_del += len(a.delistings)
            assert np.allclose(a.gross_leverage, b.gross_leverage, rtol=1e-11, atol=1e-12)
            assert a.n_liquidations == b.n_liquidations and len(a.delistings) == len(b.delistings)
            assert close(a.funding_paid, b.funding_paid, 1e-10) and close(a.fees_paid, b.fees_paid, 1e-12)
            assert close(a.funding_frac_sum, b.funding_frac_sum, 1e-9)
            ta, tb = a.trades, b.trades
            assert len(ta) == len(tb) and np.allclose(ta.cols["pnl"], tb.cols["pnl"], atol=1e-9)
    # the scenarios above must actually exercise liquidations and delistings
    assert n_liq >= 3 and n_del >= 3, (n_liq, n_del)


@test
def adv25_account_below_one_percent_is_flattened_and_stops():
    T = 80
    c = 100 * 0.9 ** np.arange(T)
    p = make_panel(c, o=c.copy())
    r = S.run_weights(p, np.ones((T, 1)), **NOCOST)          # 1x long: never liquidated
    k = int(np.flatnonzero(r.equity <= 2.0)[0])             # 1% of 200
    assert r.n_liquidations == 0
    assert r.positions[k, 0] != 0 and np.all(r.positions[k + 1:] == 0), k
    assert np.all(r.equity[k + 1:] == r.equity[k + 1])
    e = S.run_events(p, [{"i": 0, "j": 0, "side": 1, "size": 1.0},
                         {"i": k + 3, "j": 0, "side": 1, "size": 1.0}], **NOCOST)
    ke = int(np.flatnonzero(e.equity <= 2.0)[0])
    assert np.all(e.positions[ke + 1:] == 0) and len(e.trades) == 1


@test
def adv26_event_walk_forward_guard_and_pre_lockbox():
    p = _daily_panel()

    def ev(peek):
        def fn(panel, params):
            c = panel.c[:, 0]
            out = []
            for i in range(30, len(c), 7):             # every bar, including the last
                if peek:
                    s = np.sign(c[i + 1] - c[i]) if i + 1 < len(c) else 0.0
                else:
                    s = np.sign(c[i] - c[i - params["lb"]])
                if s:
                    out.append({"i": i, "j": 0, "side": int(s), "size": 1.0, "time_stop": 1})
            return out
        return fn
    out = WF.walk_forward(p, ev(False), [{"lb": 10}, {"lb": 20}], kind="events")
    assert out["oos_metrics"]["n_trades"] > 50
    try:
        WF.walk_forward(p, ev(True), [{"lb": 10}], kind="events")
        raise AssertionError("event walk_forward accepted a peeking strategy")
    except ValueError as e:
        assert "causal" in str(e)
    q = WF.pre_lockbox(p)
    assert int(q.t[-1]) + int(q.dt) <= WF.LOCKBOX_TS and len(q.t) < len(p.t)


# =========================================================================== #
def bench():
    p = random_panel(50_000, 20, seed=0)
    rng = np.random.default_rng(0)
    cases = {
        "trend-like weights (change ~every 48 bars)":
            np.repeat(rng.choice([-0.25, 0.0, 0.25], (50_000 // 48 + 1, 20)), 48, axis=0)[:50_000],
        "random weights EVERY bar (worst case)": rng.uniform(-0.25, 0.25, (50_000, 20)),
    }
    S.run_weights(p, np.zeros((50_000, 20)))                  # warm the price-prep cache
    # zero costs so the account never hits the 1%-of-initial stop: the timing
    # must cover all 50,000 bars (with costs these churny weights die early).
    for name, w in cases.items():
        t0 = time.perf_counter()
        r = S.run_weights(p, w, record_positions=False, **NOCOST)
        t1 = time.perf_counter()
        n = len(r.trades)
        t2 = time.perf_counter()
        alive = bool(r.equity[-1] > 0.01 * 200)
        print(f"BENCH run_weights 50,000 x 20, {name}: {t1 - t0:.3f}s "
              f"(+{t2 - t1:.3f}s to build {n} round trips on first .trades access; "
              f"ran all bars: {alive})")
    t0 = time.perf_counter()
    S._PREP_CACHE.clear()
    S.run_weights(p, cases["trend-like weights (change ~every 48 bars)"], record_positions=False,
                  **NOCOST)
    print(f"BENCH same, cold cache (includes price prep): {time.perf_counter() - t0:.3f}s")


def main(argv):
    sel = None
    if "-k" in argv:
        sel = argv[argv.index("-k") + 1]
    fails = 0
    for fn in TESTS:
        if sel and sel not in fn.__name__:
            continue
        try:
            fn()
            print(f"PASS {fn.__name__}")
        except Exception:
            fails += 1
            print(f"FAIL {fn.__name__}")
            traceback.print_exc()
    print(f"\n{len(TESTS) - fails if not sel else '-'} passed, {fails} failed")
    if "--bench" in argv:
        bench()
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
