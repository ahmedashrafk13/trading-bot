"""
backtest/lab/sim.py -- bar-level portfolio simulator for the research lab.

Two entry points, sharing ONE accounting core (_Book):

  run_weights(panel, weights, ...)  target-weight strategies (trend, carry,
                                    cross-sectional, vol targeting ...)
  run_events(panel, entries, ...)   discrete trades with stop / target /
                                    time stop / trailing stop

Timing contract (pinned by test_lab.py -- do not relax it):

  * A decision for bar i uses information up to and including the CLOSE of
    bar i. It executes at the OPEN of bar i+1. Never at close i.
  * Positions are held in units (qty) between fills, so their notional drifts
    with price.
  * Every fill pays   |delta notional| * (fee + slippage).   Slippage is booked
    as a cost (not as a worse fill price) so the two can be reported apart.
  * Funding: at every bar whose panel.funding != 0 the account pays
    qty * close * rate  (positive rate: longs pay, shorts receive). The
    settlement happens inside (t, t+dt]; the bar CLOSE is used as the
    settlement price and the qty held at the close as the position -- a
    position opened at the open of bar i does NOT pay a settlement stamped
    exactly t[i] (that one belongs to bar i-1), a position closed at the open
    of bar i DID hold through it.
  * Liquidation (cross margin, deliberately pessimistic): each bar, value every
    position at its ADVERSE extreme (longs at the low, shorts at the high). If
    that worst-case equity <= maint_margin * gross notional (at those prices),
    everything is closed at those prices, fees are charged, equity floors at 0
    (the exchange's insurance fund eats a negative balance) and trading resumes
    from what is left. Equity <= 1% of initial -> the account is dead and stays
    flat (if positions are still open they are closed at the next open). The
    same test is applied at the open before a rebalance (a gap can liquidate
    before you get to trade). run_events applies it along the intrabar path
    so a stop beyond the liquidation price cannot rescue the account.
  * No price at the execution open (NaN bar = delisted / missing): a held
    position that must be closed is closed at the last known close with an
    extra 2% adverse haircut, and logged in Result.delistings.

Speed: run_weights jumps from one possible execution bar to the next and
processes the bars in between (fixed qty) as one vector block -- pinned
against the bar-by-bar reference (_vectorise=False) by test_lab adv24. The
execution step only touches symbols whose target changed. Trade
bookkeeping stays OUT of the loop -- every fill is appended to a log and round
trips are reconstructed vectorised, lazily, the first time Result.trades is
read. Grid searches that never read .trades never pay for it.
"""
from __future__ import annotations

import dataclasses
import math
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

import numpy as np

DEFAULT_FEE = 0.00055          # Bybit VIP0 linear perp taker, per side
DELIST_HAIRCUT = 0.02          # extra adverse haircut when a held symbol loses its price
DEAD_FRACTION = 0.01           # equity <= 1% of initial -> stop trading

# Slippage tiers (basis points, per side).
TOP_TIER = {"BTC", "ETH"}
OTHER_MAJORS = {"SOL", "BNB", "XRP", "DOGE", "ADA", "AVAX", "LINK", "LTC",
                "TRX", "DOT", "BCH"}
SLIP_TOP_BPS, SLIP_MAJOR_BPS, SLIP_OTHER_BPS = 1.0, 3.0, 8.0


# --------------------------------------------------------------------------- #
# small helpers
# --------------------------------------------------------------------------- #
def base_asset(sym: str) -> str:
    """'BTCUSDT' -> 'BTC'. Only strips a quote suffix; '1000PEPEUSDT' -> '1000PEPE'."""
    s = sym.upper()
    for q in ("USDT", "USDC", "BUSD", "PERP", "USD"):
        if s.endswith(q) and len(s) > len(q):
            return s[: -len(q)]
    return s


def default_slippage_bps(symbols) -> np.ndarray:
    """1bp BTC/ETH, 3bp the other long-lived majors, 8bp everything else."""
    out = np.empty(len(symbols))
    for j, s in enumerate(symbols):
        b = base_asset(s)
        out[j] = (SLIP_TOP_BPS if b in TOP_TIER
                  else SLIP_MAJOR_BPS if b in OTHER_MAJORS
                  else SLIP_OTHER_BPS)
    return out


def _slippage_fraction(symbols, slippage_bps) -> np.ndarray:
    n = len(symbols)
    if slippage_bps is None:
        bps = default_slippage_bps(symbols)
    else:
        bps = np.broadcast_to(np.asarray(slippage_bps, dtype=float), (n,)).copy()
    if np.any(bps < 0) or not np.all(np.isfinite(bps)):
        raise ValueError("slippage_bps must be finite and >= 0")
    return bps / 1e4


def _ffill(a: np.ndarray) -> np.ndarray:
    """Forward-fill NaNs down axis 0 of a [T, N] array (leading NaNs stay NaN)."""
    T, N = a.shape
    valid = np.isfinite(a)
    idx = np.where(valid, np.arange(T)[:, None], 0)
    np.maximum.accumulate(idx, axis=0, out=idx)
    return a[idx, np.arange(N)[None, :]]


def _slice_meta(meta: dict, T: int, a: int, b: int) -> dict:
    """Copy of meta with every [T, ...] ndarray cut to rows [a, b).
    data.load_panel stores [T, N] arrays in meta ("valid", "member", "tbqv",
    "n_hours"); leaving them whole would hand a truncated (walk-forward train)
    panel the FUTURE -- e.g. which coins get delisted -- and the lockbox."""
    out = {}
    for k, v in meta.items():
        if isinstance(v, np.ndarray) and v.ndim >= 1 and v.shape[0] == T:
            v = v[a:b]
        elif isinstance(v, dict):
            v = _slice_meta(v, T, a, b)
        out[k] = v
    out["sliced_from"] = (int(a), int(b))
    return out


def slice_panel(panel, a: int, b: int):
    """Rows [a, b) of a Panel (views, no copies). Works for any dataclass whose
    [T, ...] ndarray fields share the length of panel.t. [T, ...] arrays inside
    panel.meta are sliced too."""
    T = len(panel.t)
    a, b = max(0, int(a)), min(T, int(b))
    if dataclasses.is_dataclass(panel):
        kw = {}
        for f in dataclasses.fields(panel):
            v = getattr(panel, f.name)
            if isinstance(v, np.ndarray) and v.ndim >= 1 and v.shape[0] == T:
                v = v[a:b]
            elif isinstance(v, dict):
                v = _slice_meta(v, T, a, b)
            kw[f.name] = v
        return dataclasses.replace(panel, **kw)
    import copy
    p = copy.copy(panel)
    for name, v in vars(panel).items():
        if isinstance(v, np.ndarray) and v.ndim >= 1 and v.shape[0] == T:
            setattr(p, name, v[a:b])
        elif isinstance(v, dict):
            setattr(p, name, _slice_meta(v, T, a, b))
    return p


# --------------------------------------------------------------------------- #
# price preparation (cached per panel object)
# --------------------------------------------------------------------------- #
@dataclass
class _Prep:
    o: np.ndarray        # raw open (NaN where no bar)
    h: np.ndarray
    l: np.ndarray
    c: np.ndarray
    ok_open: np.ndarray  # bool: bar has a usable open price
    ok_bar: np.ndarray   # bool: o,h,l,c all finite
    c_mark: np.ndarray   # last known close at bar close (0 before first ever close)
    c_prev: np.ndarray   # last known close strictly before bar i (0 if none)
    o_mark: np.ndarray   # open if valid, else c_prev  (mark price at the open)
    lo_f: np.ndarray     # low if valid, else o_mark   (adverse price for longs)
    hi_f: np.ndarray     # high if valid, else o_mark  (adverse price for shorts)
    fr: np.ndarray       # funding rate, 0 where none / NaN
    fund_row: np.ndarray  # bool [T]: any funding in this bar


_PREP_CACHE: list = []   # [(panel, fingerprint, prep)], tiny LRU


def _fingerprint(panel) -> tuple:
    """Identity + content checksum of the arrays _prepare reads. Keying the cache
    on the panel object alone served STALE prices/funding after an in-place
    edit (p.c[...] = x) or an attribute swap (p.funding = new). A wrapping
    int64 sum of the raw bits costs ~5 ms per 50k x 150 array."""
    out = []
    for name in ("o", "h", "l", "c", "funding"):
        v = getattr(panel, name, None)
        if v is None:
            out.append(None)
            continue
        a = np.asarray(v)
        if a.dtype == np.float64:
            chk = int(a.view(np.int64).sum())
        else:
            chk = int(np.asarray(a, dtype=float).view(np.int64).sum())
        out.append((id(v), a.shape, chk))
    return tuple(out)


def _prepare(panel) -> _Prep:
    fp = _fingerprint(panel)
    for k, (p, pfp, prep) in enumerate(_PREP_CACHE):
        if p is panel and pfp == fp:
            return prep
    o = np.asarray(panel.o, dtype=float)
    h = np.asarray(panel.h, dtype=float)
    l = np.asarray(panel.l, dtype=float)
    c = np.asarray(panel.c, dtype=float)
    if o.ndim != 2 or not (o.shape == h.shape == l.shape == c.shape):
        raise ValueError("panel o/h/l/c must be [T, N] arrays of equal shape")
    T, N = c.shape
    ok_open = np.isfinite(o)
    ok_bar = ok_open & np.isfinite(h) & np.isfinite(l) & np.isfinite(c)
    cff = _ffill(c)
    c_mark = np.nan_to_num(cff, nan=0.0)
    c_prev = np.zeros_like(c_mark)
    c_prev[1:] = c_mark[:-1]
    o_mark = np.where(ok_open, o, c_prev)
    lo_f = np.where(np.isfinite(l), l, o_mark)
    hi_f = np.where(np.isfinite(h), h, o_mark)
    fund = getattr(panel, "funding", None)
    if fund is None:
        fr = np.zeros_like(c_mark)
    else:
        fr = np.nan_to_num(np.asarray(fund, dtype=float), nan=0.0)
    prep = _Prep(o, h, l, c, ok_open, ok_bar, c_mark, c_prev, o_mark, lo_f, hi_f,
                 fr, (fr != 0).any(axis=1))
    _PREP_CACHE[:] = [e for e in _PREP_CACHE if e[0] is not panel]
    _PREP_CACHE.append((panel, fp, prep))
    if len(_PREP_CACHE) > 4:
        _PREP_CACHE.pop(0)
    return prep


def _tradable(panel) -> np.ndarray:
    tr = getattr(panel, "tradable", None)
    if tr is None:
        return np.isfinite(np.asarray(panel.c, dtype=float))
    return np.asarray(tr, dtype=bool)


def effective_weights(panel, weights, max_gross_leverage: float) -> np.ndarray:
    """The targets the simulator will actually use: NaN -> 0, non-tradable at
    the decision bar -> 0, then each row scaled down so sum|w| <= max gross."""
    W = np.array(weights, dtype=float, copy=True)
    T, N = np.asarray(panel.c).shape
    if W.shape != (T, N):
        raise ValueError(f"weights shape {W.shape} != panel shape {(T, N)}")
    W[~np.isfinite(W)] = 0.0
    W[~_tradable(panel)] = 0.0
    g = np.abs(W).sum(axis=1)
    over = g > max_gross_leverage
    if over.any():
        W[over] *= (max_gross_leverage / g[over])[:, None]
    return W


def _instrument_vectors(instruments, symbols):
    n = len(symbols)
    step, minq, minnot = np.zeros(n), np.zeros(n), np.zeros(n)
    missing = []
    for j, s in enumerate(symbols):
        ins = (instruments or {}).get(s)
        if not ins:
            missing.append(s)
            continue
        step[j] = float(ins.get("qtyStep") or 0.0)
        minq[j] = float(ins.get("minOrderQty") or 0.0)
        minnot[j] = float(ins.get("minNotionalValue") or 0.0)
    return step, minq, minnot, missing


def _round_down(q: np.ndarray, step: np.ndarray) -> np.ndarray:
    """Round |q| DOWN to a multiple of step (step 0 -> untouched)."""
    out = np.array(q, dtype=float, copy=True)
    m = step > 0
    if m.any():
        out[m] = np.round(np.sign(q[m]) * np.floor(np.abs(q[m]) / step[m] + 1e-9)
                          * step[m], 12)
    return out


# --------------------------------------------------------------------------- #
# the accounting core
# --------------------------------------------------------------------------- #
class _Book:
    """Cash + signed qty per symbol. Every change of qty goes through fill();
    every funding payment through pay_funding(). Both append to logs from
    which round trips are rebuilt afterwards."""

    def __init__(self, n: int, initial: float, fee: float, slip: np.ndarray):
        self.cash = float(initial)
        self.qty = np.zeros(n)
        self.fee = float(fee)
        self.slip = slip
        self.fees = 0.0
        self.slippage = 0.0
        self.funding = 0.0
        self.notional = 0.0       # $ traded
        self.turnover = 0.0       # sum |traded notional| / equity at the time
        self.cost_frac = 0.0      # sum (fee+slip) / equity at the time
        self.fund_frac = 0.0      # sum funding / equity at the time (signed, + = paid)
        self.seq = 0
        self.fill_log: list = []  # (seq, bar, when, idx, q0, q1, px, cost)
        self.fund_log: list = []  # (seq, bar, idx, amount)

    def fill(self, i: int, idx: np.ndarray, q1: np.ndarray, px: np.ndarray,
             eq_ref: float, when: int) -> float:
        """Move qty[idx] to q1 at prices px. Returns the cost charged."""
        if idx.size == 0:
            return 0.0
        q0 = self.qty[idx]
        d = q1 - q0
        notional = np.abs(d) * px
        fee = notional * self.fee
        slip = notional * self.slip[idx]
        cost = fee + slip
        ctot = float(cost.sum())
        ntot = float(notional.sum())
        self.cash -= float(np.dot(d, px)) + ctot
        self.qty[idx] = q1
        self.fees += float(fee.sum())
        self.slippage += float(slip.sum())
        self.notional += ntot
        if eq_ref > 0:
            self.turnover += ntot / eq_ref
            self.cost_frac += ctot / eq_ref
        self.fill_log.append((self.seq, i, when, idx, q0, np.asarray(q1, float).copy(),
                              np.asarray(px, float).copy(), cost))
        self.seq += 1
        return ctot

    def pay_funding(self, i: int, rate_row: np.ndarray, px_row: np.ndarray,
                    eq_ref: float) -> None:
        f = self.qty * rate_row * px_row          # + = the account pays
        idx = np.flatnonzero(f)
        if idx.size == 0:
            return
        amt = f[idx]
        tot = float(amt.sum())
        self.cash -= tot
        self.funding += tot
        if eq_ref > 0:
            self.fund_frac += tot / eq_ref
        self.fund_log.append((self.seq, i, idx, amt))
        self.seq += 1


# --------------------------------------------------------------------------- #
# round-trip reconstruction
# --------------------------------------------------------------------------- #
class TradeTable:
    """Round trips as numpy columns. Behaves like a list of dicts
    (len / iteration / indexing) and has .df() for pandas.

    A round trip starts when a symbol's qty leaves 0 (or flips sign) and ends
    when it returns to 0 (or flips). Partial adds/reductions stay in the trip.
      entry  = VWAP of the opening/adding fills
      exit   = VWAP of the reducing/closing fills (NaN if still open)
      pnl    = every $ that trip moved: trade cash flows - fee - slippage -
               funding (+ unrealised value if still open). Summing pnl over
               all trips reproduces equity_end - initial exactly (unless a
               liquidation drove equity below zero; see Result.liquidations).
      ret    = pnl / sum of opening+adding notional
    """

    COLS = ("symbol", "side", "open_t", "close_t", "open_bar", "close_bar",
            "entry", "exit", "qty_max", "entry_notional", "pnl", "ret", "fees",
            "funding", "is_open")

    def __init__(self, cols: dict):
        self.cols = cols

    def __len__(self):
        return len(self.cols["pnl"])

    def __getitem__(self, k):
        return {c: _py(self.cols[c][k]) for c in self.COLS}

    def __iter__(self):
        for k in range(len(self)):
            yield self[k]

    def closed(self) -> np.ndarray:
        return ~self.cols["is_open"]

    def df(self):
        import pandas as pd
        return pd.DataFrame({c: self.cols[c] for c in self.COLS})


def _py(v):
    if isinstance(v, np.generic):
        return v.item()
    return v


def _build_trades(book: _Book, symbols, qty_end, mark_end, dt) -> TradeTable:
    empty = {c: np.array([]) for c in TradeTable.COLS}
    empty["is_open"] = np.array([], dtype=bool)
    empty["symbol"] = np.array([], dtype=object)
    if not book.fill_log:
        return TradeTable(empty)
    lens = [len(e[3]) for e in book.fill_log]
    SEQ = np.repeat([e[0] for e in book.fill_log], lens)
    BAR = np.repeat([e[1] for e in book.fill_log], lens)
    WHEN = np.repeat([e[2] for e in book.fill_log], lens)
    J = np.concatenate([e[3] for e in book.fill_log])
    Q0 = np.concatenate([e[4] for e in book.fill_log])
    Q1 = np.concatenate([e[5] for e in book.fill_log])
    PX = np.concatenate([e[6] for e in book.fill_log])
    C = np.concatenate([e[7] for e in book.fill_log])
    order = np.lexsort((SEQ, J))            # by symbol, then time
    SEQ, BAR, WHEN, J, Q0, Q1, PX, C = (x[order] for x in (SEQ, BAR, WHEN, J, Q0, Q1, PX, C))

    s0, s1 = np.sign(Q0), np.sign(Q1)
    a0, a1 = np.abs(Q0), np.abs(Q1)
    flip = s0 * s1 < 0
    same = s0 * s1 > 0
    opening = (s0 == 0) & (s1 != 0)
    closing = (s0 != 0) & (s1 == 0)
    inc = same & (a1 > a0)
    dec = same & (a1 < a0)
    cq = np.where(flip | closing, a0, np.where(dec, a0 - a1, 0.0))   # qty closed
    oq = np.where(flip | opening, a1, np.where(inc, a1 - a0, 0.0))   # qty opened
    tot = cq + oq
    cfrac = np.divide(cq, tot, out=np.zeros_like(tot), where=tot > 0)
    cost_c = C * cfrac
    cost_o = C - cost_c

    new = flip | opening
    trip = np.cumsum(new) - 1                 # trip holding the position AFTER this fill
    prev = np.maximum(trip - new, 0)          # trip the CLOSING part belongs to
    ntr = int(trip[-1]) + 1
    has_prev = s0 != 0
    bc = lambda idx, w: np.bincount(idx, weights=w, minlength=ntr)  # noqa: E731

    ent_not = bc(trip, oq * PX)
    ent_qty = bc(trip, oq)
    ex_not = bc(prev, np.where(has_prev, cq * PX, 0.0))
    ex_qty = bc(prev, np.where(has_prev, cq, 0.0))
    cash = (bc(prev, np.where(has_prev, s0 * cq * PX - cost_c, 0.0))
            + bc(trip, -s1 * oq * PX - cost_o))
    fees = bc(prev, np.where(has_prev, cost_c, 0.0)) + bc(trip, cost_o)
    qmax = np.zeros(ntr)
    np.maximum.at(qmax, trip, a1)

    side = np.zeros(ntr)
    side[trip[new]] = s1[new]
    sym_j = np.zeros(ntr, dtype=int)
    sym_j[trip[new]] = J[new]
    open_t = np.zeros(ntr, dtype=np.int64)
    open_t[trip[new]] = WHEN[new]
    open_bar = np.zeros(ntr, dtype=np.int64)
    open_bar[trip[new]] = BAR[new]
    fin = flip | closing
    close_t = np.full(ntr, -1, dtype=np.int64)
    close_t[prev[fin]] = WHEN[fin]
    close_bar = np.full(ntr, -1, dtype=np.int64)
    close_bar[prev[fin]] = BAR[fin]
    is_open = close_t < 0

    funding = np.zeros(ntr)
    if book.fund_log:
        flens = [len(e[2]) for e in book.fund_log]
        FSEQ = np.repeat([e[0] for e in book.fund_log], flens)
        FJ = np.concatenate([e[2] for e in book.fund_log])
        FA = np.concatenate([e[3] for e in book.fund_log])
        big = int(max(SEQ.max(), FSEQ.max())) + 1
        key_fill = J.astype(np.int64) * big + SEQ
        key_f = FJ.astype(np.int64) * big + FSEQ
        pos = np.searchsorted(key_fill, key_f, side="right") - 1
        if np.any(pos < 0) or np.any(J[pos] != FJ):
            raise RuntimeError("funding paid on a symbol with no open trip")
        ft = trip[pos]
        funding = bc(ft, FA)
        cash = cash - funding

    # still-open trips: add unrealised value at the last mark
    exit_px = np.divide(ex_not, ex_qty, out=np.full(ntr, np.nan), where=ex_qty > 0)
    if is_open.any():
        k = np.flatnonzero(is_open)
        jj = sym_j[k]
        cash[k] = cash[k] + qty_end[jj] * mark_end[jj]
        exit_px[k] = mark_end[jj]
    entry_px = np.divide(ent_not, ent_qty, out=np.full(ntr, np.nan), where=ent_qty > 0)
    ret = np.divide(cash, ent_not, out=np.zeros(ntr), where=ent_not > 0)
    cols = {
        "symbol": np.array([symbols[j] for j in sym_j], dtype=object),
        "side": side.astype(int), "open_t": open_t, "close_t": close_t,
        "open_bar": open_bar, "close_bar": close_bar,
        "entry": entry_px, "exit": exit_px, "qty_max": qmax,
        "entry_notional": ent_not, "pnl": cash, "ret": ret, "fees": fees,
        "funding": funding, "is_open": is_open,
    }
    o = np.lexsort((sym_j, open_t))
    return TradeTable({k: v[o] for k, v in cols.items()})


# --------------------------------------------------------------------------- #
# result object
# --------------------------------------------------------------------------- #
@dataclass
class Result:
    t: np.ndarray
    dt: int
    symbols: list
    equity: np.ndarray            # [T] mark-to-market at each bar close
    cash: np.ndarray              # [T]
    positions: Any                # [T, N] qty at each close (None if not recorded)
    gross_leverage: np.ndarray    # [T] gross notional / equity at each close
    initial_equity: float
    fees_paid: float
    slippage_paid: float
    funding_paid: float           # signed, + = the account paid
    n_liquidations: int
    liquidations: list
    delistings: list
    turnover: float               # sum |traded notional| / equity  (x equity)
    notional_traded: float        # $
    cost_frac_sum: float          # sum (fee+slip)/equity
    funding_frac_sum: float       # sum funding/equity
    rejected: list = field(default_factory=list)   # run_events: entries not taken
    params: dict = field(default_factory=dict)
    _book: Any = None
    _trades: Any = None
    _qty_end: Any = None
    _mark_end: Any = None

    @property
    def trades(self) -> TradeTable:
        if self._trades is None:
            self._trades = _build_trades(self._book, self.symbols, self._qty_end,
                                         self._mark_end, self.dt)
        return self._trades

    def metrics(self) -> dict:
        try:
            from . import metrics as _m
        except ImportError:
            import metrics as _m
        return _m.compute(self)


def _result(panel, book, eq, cash, pos, gross, initial, liqs, delists, qty_end,
            mark_end, params, rejected=None) -> Result:
    return Result(
        t=np.asarray(panel.t), dt=int(panel.dt), symbols=list(panel.symbols),
        equity=eq, cash=cash, positions=pos, gross_leverage=gross,
        initial_equity=float(initial), fees_paid=book.fees,
        slippage_paid=book.slippage, funding_paid=book.funding,
        n_liquidations=len(liqs), liquidations=liqs, delistings=delists,
        turnover=book.turnover, notional_traded=book.notional,
        cost_frac_sum=book.cost_frac, funding_frac_sum=book.fund_frac,
        rejected=rejected or [], params=params, _book=book,
        _qty_end=qty_end.copy(), _mark_end=mark_end.copy())


def _liquidate(book, i, px_row, worst_eq, when, t_i, liqs):
    idx = np.flatnonzero(book.qty)
    cost = book.fill(i, idx, np.zeros(idx.size), px_row[idx], max(worst_eq, 0.0), when)
    absorbed = 0.0
    if book.cash < 0:
        absorbed = -book.cash
        book.cash = 0.0
    liqs.append({"bar": int(i), "t": int(t_i), "equity_worst": float(worst_eq),
                 "cost": float(cost), "equity_after": float(book.cash),
                 "absorbed_by_insurance": float(absorbed)})


def _close_no_price(book, i, mask, P, eq_ref, when, t_i, delists, symbols):
    """Close held symbols whose execution bar has no price: last known close,
    2% adverse haircut."""
    idx = np.flatnonzero(mask)
    q = book.qty[idx]
    px = P.c_prev[i, idx] * (1.0 - np.sign(q) * DELIST_HAIRCUT)
    book.fill(i, idx, np.zeros(idx.size), px, eq_ref, when)
    for k, j in enumerate(idx):
        delists.append({"bar": int(i), "t": int(t_i), "symbol": symbols[j],
                        "qty": float(q[k]), "last_close": float(P.c_prev[i, j]),
                        "fill": float(px[k])})


# --------------------------------------------------------------------------- #
# run_weights
# --------------------------------------------------------------------------- #
def run_weights(panel, weights, *, fee: float = DEFAULT_FEE, slippage_bps=None,
                funding: bool = True, max_gross_leverage: float = 5.0,
                initial_equity: float = 200.0, maint_margin: float = 0.005,
                instruments: dict | None = None, round_to_qty: bool = False,
                min_trade_frac: float = 0.0, rebalance: str = "on_change",
                record_positions: bool = True, _vectorise: bool = True) -> Result:
    """Simulate target weights.

    weights[i, j] = target SIGNED notional / equity for symbol j, decided at
    the CLOSE of bar i, executed at the OPEN of bar i+1 (sized off the
    mark-to-market equity at that open). The last row never executes.

    rebalance:
      "on_change" (default) -- symbol j is traded only when its effective
          target differs from the target last executed for it; in between
          the qty is held and drifts with price. (After a liquidation, or a
          bar where the symbol had no price, the target is re-applied.)
      "every_bar" -- every symbol is re-sized to its target at every open
          (constant-weight rebalancing; use min_trade_frac to limit churn).
    _vectorise: internal switch -- False runs the same accounting one bar at a
      time (the reference the segment-vectorised path is tested against).
    min_trade_frac: skip a symbol's trade when |target w - current w| is
      below this (full closes to 0 are never skipped).
    round_to_qty: with instruments (load_bybit_instruments()), round each
      target qty DOWN to qtyStep and drop orders below minOrderQty or
      minNotionalValue (full closes are always allowed).
    """
    if rebalance not in ("on_change", "every_bar"):
        raise ValueError("rebalance must be 'on_change' or 'every_bar'")
    P = _prepare(panel)
    T, N = P.c.shape
    t = np.asarray(panel.t, dtype=np.int64)
    dt = int(panel.dt)
    W = effective_weights(panel, weights, max_gross_leverage)
    slip = _slippage_fraction(panel.symbols, slippage_bps)
    book = _Book(N, initial_equity, fee, slip)
    rq = None
    if round_to_qty:
        if instruments is None:
            raise ValueError("round_to_qty=True needs instruments")
        rq = _instrument_vectors(instruments, panel.symbols)
    every = rebalance == "every_bar"
    mm = float(maint_margin)
    dead_level = DEAD_FRACTION * initial_equity
    mtf = float(min_trade_frac)

    eq = np.empty(T)
    cash = np.empty(T)
    gross = np.zeros(T)
    pos = np.zeros((T, N)) if record_positions else None
    liqs, delists = [], []
    last = np.zeros(N)
    all_true = np.ones(N, dtype=bool)
    dead = False
    qty = book.qty                     # alias; fill() writes in place
    half = dt // 2
    lo_f, hi_f, c_mark, o_mark = P.lo_f, P.hi_f, P.c_mark, P.o_mark
    fund_row, fr = P.fund_row, P.fr

    # chg[i]: does the target executed at open i (W[i-1]) differ from the one
    # before it (W[i-2], zeros before the start)? While `last` is known to equal
    # W[i-2] ("clean") a bar with chg False needs no work at all in on_change mode.
    chg = np.zeros(T, dtype=bool)
    if T > 1:
        chg[1] = bool((W[0] != 0).any())
    if T > 2:
        chg[2:] = (W[1:-1] != W[:-2]).any(axis=1)
    last_clean = True

    # derived position vectors, refreshed (in place) after every change of qty:
    #   QA = |qty|, QP = long part, QN = short part (<= 0)
    #   value at adverse extremes = lo @ QP + hi @ QN ; gross there = lo @ QP - hi @ QN
    QA, QP, QN = np.zeros(N), np.zeros(N), np.zeros(N)

    def refresh():
        np.abs(qty, out=QA)
        np.maximum(qty, 0.0, out=QP)
        np.minimum(qty, 0.0, out=QN)
        return bool(qty.any())
    has_pos = refresh()
    kill = False                       # equity <= 1% of initial: flatten at the next open, stop
    zero_row = np.zeros(N)

    flips = np.flatnonzero(chg)
    i = 0
    while i < T:
        # ---- 1. execute the decision taken at close i-1, at open i -------------
        if i > 0 and not dead and (every or not last_clean or chg[i] or kill):
            tgt = zero_row if kill else W[i - 1]
            need = (qty != 0) if kill else (all_true if every else (tgt != last))
            if kill or every or need.any():
                om = o_mark[i]
                if has_pos:
                    eq_open = book.cash + float(om @ qty)
                else:
                    eq_open = book.cash
                if has_pos and eq_open <= mm * float(om @ QA):
                    _liquidate(book, i, om, eq_open, int(t[i]), t[i], liqs)
                    has_pos = refresh()
                    last[:] = 0.0
                    last_clean = False
                    dead = book.cash <= dead_level
                else:
                    # work only on the symbols whose target changed (the rest hold)
                    act = np.flatnonzero(need)
                    ok = P.ok_open[i, act]
                    blocked = ~ok
                    any_blocked = bool(blocked.any())
                    if has_pos and any_blocked:
                        nopx_idx = act[blocked & (qty[act] != 0)]
                        if nopx_idx.size:
                            nopx = np.zeros(N, dtype=bool)
                            nopx[nopx_idx] = True
                            _close_no_price(book, i, nopx, P, eq_open, int(t[i]),
                                            t[i], delists, panel.symbols)
                            has_pos = refresh()
                            eq_open = book.cash + float(om @ qty)   # after the haircut
                    orow = P.o[i, act]
                    ta, qa = tgt[act], qty[act]
                    px = np.where(ok, orow, 1.0)
                    tq = ta * (eq_open / px) if eq_open > 0 else np.zeros(act.size)
                    trade = ok.copy()
                    if mtf > 0.0 and eq_open > 0:
                        cur = qa * px / eq_open
                        small = (np.abs(ta - cur) < mtf) & ~((ta == 0) & (qa != 0))
                        trade &= ~small
                    if rq is not None:
                        step, minq, minnot, _ = rq
                        tq = _round_down(tq, step[act])
                        dq = np.abs(tq - qa)
                        full_close = (tq == 0) & (qa != 0)
                        too_small = ((dq < minq[act] * (1 - 1e-9))
                                     | (dq * px < minnot[act] * (1 - 1e-9)))
                        trade &= full_close | ~too_small
                    trade &= tq != qa
                    if trade.any():
                        book.fill(i, act[trade], tq[trade], orow[trade], eq_open, int(t[i]))
                        has_pos = refresh()
                    last[act] = ta                 # untouched symbols already equal tgt
                    last_clean = True
                    if any_blocked:
                        last[act[blocked]] = np.nan    # retry when the price is back
                        last_clean = False
                    if kill:                       # equity fell to <= 1% of initial
                        dead = True
                        has_pos = refresh()
            else:
                last_clean = True                  # need all False: last == W[i-1]
            kill = False
        # ---- the bars [i, j) until the next possible execution hold qty fixed --
        if dead:
            j = T
        elif every or not last_clean or not _vectorise or kill:
            j = i + 1
        else:
            kf = int(np.searchsorted(flips, i, side="right"))
            j = int(flips[kf]) if kf < flips.size else T
        if not has_pos or dead:
            # flat: equity is cash; nothing can happen until the next execution
            eq[i:j] = book.cash
            cash[i:j] = book.cash
            if not dead and book.cash <= dead_level:   # flat and (nearly) broke: stop
                dead = True
                eq[i:] = book.cash
                cash[i:] = book.cash
                break
            i = j
            continue
        if j - i == 1:
            # ---- 2. intrabar liquidation check (single bar) ----------------------
            a_ = float(lo_f[i] @ QP)
            b_ = float(hi_f[i] @ QN)
            worst = book.cash + a_ + b_
            if worst <= mm * (a_ - b_):
                adv = np.where(qty > 0, lo_f[i], hi_f[i])
                _liquidate(book, i, adv, worst, int(t[i]) + half, t[i], liqs)
                has_pos = refresh()
                last[:] = 0.0
                last_clean = False
                dead = book.cash <= dead_level
                eq[i] = cash[i] = book.cash
                if not dead and book.cash <= dead_level:
                    dead = True
                i += 1
                continue
            # ---- 3. funding + mark to market at the close ------------------------
            cm = c_mark[i]
            mv = float(cm @ qty)
            if funding and fund_row[i]:
                book.pay_funding(i, fr[i], cm, book.cash + mv)
            e = book.cash + mv
            gross[i] = float(cm @ QA) / e if e > 0 else 0.0
            eq[i] = e
            cash[i] = book.cash
            if pos is not None:
                pos[i] = qty
            if e <= dead_level:
                kill = True                        # close everything at the next open
            i += 1
            continue
        # ---- 2+3 vectorised over the segment -------------------------------------
        L = j - i
        lo, hi, cmS = lo_f[i:j], hi_f[i:j], c_mark[i:j]
        qp, qn = np.maximum(qty, 0.0), np.minimum(qty, 0.0)
        vadv = lo @ qp + hi @ qn                    # value at adverse extremes
        gadv = lo @ qp - hi @ qn                    # gross at adverse extremes
        mv = cmS @ qty
        gc = cmS @ np.abs(qty)
        F = np.zeros(L)
        frows = np.flatnonzero(fund_row[i:j]) if funding else np.zeros(0, dtype=np.int64)
        Mf = None
        if frows.size:
            Mf = qty * fr[i + frows] * cmS[frows]  # [R, N] per-symbol payments
            F[frows] = Mf.sum(axis=1)
        c0 = book.cash
        cum = np.cumsum(F)
        cash_after = c0 - cum
        cash_before = c0 - np.r_[0.0, cum[:-1]]
        worst = cash_before + vadv
        liq = np.flatnonzero(worst <= mm * gadv)
        n_ok = int(liq[0]) if liq.size else L
        broke = np.flatnonzero((cash_after[:n_ok] + mv[:n_ok]) <= dead_level)
        if broke.size:                             # kill at the next open
            n_ok = int(broke[0]) + 1
            kill = True
            liq = np.zeros(0, dtype=np.int64)
            L = n_ok
            j = i + n_ok
        if n_ok:
            e_ = cash_after[:n_ok] + mv[:n_ok]
            eq[i:i + n_ok] = e_
            cash[i:i + n_ok] = cash_after[:n_ok]
            gross[i:i + n_ok] = np.where(e_ > 0, gc[:n_ok] / np.where(e_ > 0, e_, 1.0), 0.0)
            if pos is not None:
                pos[i:i + n_ok] = qty
            if frows.size:
                for r, kk in enumerate(frows):
                    if kk >= n_ok:
                        break
                    row = Mf[r]
                    idx = np.flatnonzero(row)
                    if idx.size == 0:
                        continue
                    amt = row[idx]
                    tot = float(amt.sum())
                    book.funding += tot
                    ref = cash_before[kk] + mv[kk]
                    if ref > 0:
                        book.fund_frac += tot / ref
                    book.fund_log.append((book.seq, i + int(kk), idx, amt))
                    book.seq += 1
            book.cash = float(cash_after[n_ok - 1])
        if n_ok == L:
            i = j
            continue
        # liquidation at bar k (cash before its funding; no funding paid)
        k = i + n_ok
        book.cash = float(cash_before[n_ok])
        adv = np.where(qty > 0, lo_f[k], hi_f[k])
        _liquidate(book, k, adv, float(worst[n_ok]), int(t[k]) + half, t[k], liqs)
        has_pos = refresh()
        last[:] = 0.0
        last_clean = False
        dead = book.cash <= dead_level
        eq[k] = cash[k] = book.cash
        i = k + 1
    params = dict(fee=fee, slippage_bps=None if slippage_bps is None else slippage_bps,
                  funding=funding, max_gross_leverage=max_gross_leverage,
                  initial_equity=initial_equity, maint_margin=maint_margin,
                  round_to_qty=round_to_qty, min_trade_frac=min_trade_frac,
                  rebalance=rebalance)
    if rq is not None and rq[3]:
        params["instruments_missing"] = rq[3]
    return _result(panel, book, eq, cash, pos, gross, initial_equity, liqs, delists,
                   qty, P.c_mark[T - 1], params)


# --------------------------------------------------------------------------- #
# run_events
# --------------------------------------------------------------------------- #
_ENTRY_KEYS = ("i", "t", "j", "symbol", "side", "size", "stop", "stop_pct",
               "target", "target_pct", "time_stop", "trail")


def _normalise_entries(entries, panel) -> list:
    """Entries -> list of dicts with integer decision bar 'i' and symbol 'j'.

    Accepted per entry (dict, DataFrame row, or structured-array record):
      i or t      decision bar index, or that bar's OPEN time (epoch s)
      j or symbol symbol index or name
      side        +1 long / -1 short
      size        levered notional as a fraction of equity (3.0 = 3x)
      stop        absolute stop price   | stop_pct   fraction from the fill
      target      absolute target price | target_pct fraction from the fill
      time_stop   bars; exit at the OPEN of entry_bar + time_stop
      trail       trailing stop distance as a fraction of the best price
    """
    if entries is None:
        return []
    if hasattr(entries, "to_dict") and not isinstance(entries, dict):
        entries = entries.to_dict("records")
    elif isinstance(entries, np.ndarray) and entries.dtype.names:
        entries = [dict(zip(entries.dtype.names, r)) for r in entries.tolist()]
    t = np.asarray(panel.t, dtype=np.int64)
    sym_index = {s: k for k, s in enumerate(panel.symbols)}
    out = []
    for n, e in enumerate(entries):
        e = dict(e)
        if e.get("i") is not None and not _isnan(e.get("i")):
            i = int(e["i"])
        elif e.get("t") is not None:
            k = int(np.searchsorted(t, int(e["t"])))
            if k >= len(t) or t[k] != int(e["t"]):
                raise ValueError(f"entry {n}: t={e['t']} is not a bar open time")
            i = k
        else:
            raise ValueError(f"entry {n}: needs 'i' or 't'")
        if e.get("j") is not None and not _isnan(e.get("j")):
            j = int(e["j"])
        else:
            j = sym_index[e["symbol"]]
        side = int(np.sign(e.get("side", 0)))
        if side == 0:
            raise ValueError(f"entry {n}: side must be +1 or -1")
        size = float(e.get("size", 1.0))
        rec = {"n": n, "i": i, "j": j, "side": side, "size": size}
        for k in ("stop", "stop_pct", "target", "target_pct", "trail"):
            v = e.get(k)
            rec[k] = None if v is None or _isnan(v) else float(v)
        ts = e.get("time_stop")
        rec["time_stop"] = None if ts is None or _isnan(ts) else int(ts)
        out.append(rec)
    return out


def _isnan(v) -> bool:
    try:
        return v is None or (isinstance(v, float) and math.isnan(v))
    except TypeError:
        return False


def run_events(panel, entries, *, exits=None, fee: float = DEFAULT_FEE,
               slippage_bps=None, funding: bool = True,
               max_gross_leverage: float = 5.0, initial_equity: float = 200.0,
               maint_margin: float = 0.005, instruments: dict | None = None,
               round_to_qty: bool = False, max_concurrent: int = 5,
               allow_flip: bool = False, record_positions: bool = True) -> Result:
    """Simulate discrete trades with stops.

    Each entry is decided at the CLOSE of bar i and filled at the OPEN of bar
    i+1 (entry bar e). Sizing uses mark-to-market equity at that open; the
    notional is cut to fit max_gross_leverage (entry rejected if no room).

    Order of events inside a bar k:
      1. at the open: time stops due (e + time_stop == k), exit signals
         (exits[k-1, j] True), and positions whose symbol was non-tradable at
         k-1 are closed at the open.
      2. at the open: new entries fill (skipped if the symbol already has a
         position -- or, with allow_flip, an opposite position is closed
         first; skipped at max_concurrent; rejected if the stop/target is
         already on the wrong side of the fill).
      3. intrabar stop / target, INCLUDING the entry bar (the open is the
         first price of the bar, so its whole range happens after the fill):
         open beyond stop -> stop fills at the open; else open beyond target
         -> target fills AT THE TARGET (a resting order is hit at its own
         price; the better open would be optimistic); else low/high through
         stop -> stop price; else through target -> target price. Stop and
         target both inside the range -> the STOP (pessimistic).
         Liquidation is evaluated ALONG the pessimistic intrabar path: all
         open positions move together from the open to their adverse
         extremes; stops fill in the order the path reaches them; if the
         account reaches maintenance margin before a stop does (a stop set
         beyond the liquidation price), the account is liquidated at that
         point and the stop never fills. Targets fill only after the account
         survived the adverse path.
      4. trailing stops ratchet with this bar's high (long) / low (short) --
         only AFTER step 3, so a ratchet can never fill inside its own bar.
      5. liquidation check on what is still open (adverse extremes).
      6. funding, mark to market. Equity <= 1% of initial at a close ->
         everything is closed at the next open and the account stops.
    Stops/targets/time stops are taker fills (fee + slippage)."""
    P = _prepare(panel)
    T, N = P.c.shape
    t = np.asarray(panel.t, dtype=np.int64)
    dt = int(panel.dt)
    tradable = _tradable(panel)
    slip = _slippage_fraction(panel.symbols, slippage_bps)
    book = _Book(N, initial_equity, fee, slip)
    rq = None
    if round_to_qty:
        if instruments is None:
            raise ValueError("round_to_qty=True needs instruments")
        rq = _instrument_vectors(instruments, panel.symbols)
    ex = None if exits is None else np.asarray(exits, dtype=bool)
    if ex is not None and ex.shape != (T, N):
        raise ValueError("exits must be a [T, N] bool array")
    pending = defaultdict(list)
    for e in _normalise_entries(entries, panel):
        if 0 <= e["i"] < T - 1:
            pending[e["i"] + 1].append(e)
    mm = float(maint_margin)
    dead_level = DEAD_FRACTION * initial_equity
    half = dt // 2

    eq = np.empty(T)
    cash = np.empty(T)
    gross = np.zeros(T)
    posarr = np.zeros((T, N)) if record_positions else None
    liqs, delists, rejected = [], [], []
    open_pos: dict = {}      # j -> {side, stop, target, trail, best, exit_bar, entry_bar}
    qty = book.qty
    dead = False
    kill = False

    def close_at_open(i, j):
        if P.ok_open[i, j]:
            book.fill(i, np.array([j]), np.zeros(1), np.array([P.o[i, j]]),
                      book.cash + float(qty @ P.o_mark[i]), int(t[i]))
        else:
            m = np.zeros(N, dtype=bool)
            m[j] = True
            _close_no_price(book, i, m, P, book.cash + float(qty @ P.o_mark[i]),
                            int(t[i]), t[i], delists, panel.symbols)
        open_pos.pop(j, None)

    for i in range(T):
        if not dead and i > 0:
            # ---- 1. scheduled exits at the open ---------------------------------
            if open_pos:
                for j in list(open_pos):
                    p = open_pos[j]
                    if kill or (p["exit_bar"] is not None and p["exit_bar"] <= i) \
                            or (ex is not None and ex[i - 1, j]) or not tradable[i - 1, j]:
                        close_at_open(i, j)
            if kill:                     # equity fell to <= 1% of initial: flat and stop
                dead = True
                kill = False
            # ---- 1b. gap liquidation at the open --------------------------------
            if open_pos:
                om = P.o_mark[i]
                eq_open = book.cash + float(qty @ om)
                if eq_open <= mm * float(np.abs(qty) @ om):
                    _liquidate(book, i, om, eq_open, int(t[i]), t[i], liqs)
                    open_pos.clear()
                    dead = book.cash <= dead_level
            # ---- 2. entries --------------------------------------------------------
            for e in pending.get(i, ()):
                if dead:
                    break
                j, side = e["j"], e["side"]
                why = None
                if not tradable[i - 1, j]:
                    why = "not_tradable"
                elif not P.ok_open[i, j]:
                    why = "no_price"
                elif j in open_pos:
                    if allow_flip and open_pos[j]["side"] != side:
                        close_at_open(i, j)
                    else:
                        why = "already_open"
                if why is None and len(open_pos) >= max_concurrent:
                    why = "max_concurrent"
                if why is None:
                    fill = float(P.o[i, j])
                    stop = e["stop"]
                    if e["stop_pct"] is not None:
                        s2 = fill * (1 - side * e["stop_pct"])
                        stop = s2 if stop is None else (max(stop, s2) if side > 0 else min(stop, s2))
                    target = e["target"]
                    if e["target_pct"] is not None:
                        target = fill * (1 + side * e["target_pct"])
                    if stop is not None and (stop - fill) * side >= 0:
                        why = "stop_wrong_side"
                    elif target is not None and (target - fill) * side <= 0:
                        why = "target_wrong_side"
                if why is None:
                    om = P.o_mark[i]
                    eq_open = book.cash + float(qty @ om)
                    room = max_gross_leverage * eq_open - float(np.abs(qty) @ om)
                    notional = min(e["size"] * eq_open, room)
                    if notional <= 0:
                        why = "no_leverage_room"
                if why is None:
                    q = side * notional / fill
                    if rq is not None:
                        step, minq, minnot, _ = rq
                        q = float(_round_down(np.array([q]), step[j:j + 1])[0])
                        if abs(q) < minq[j] * (1 - 1e-9) or abs(q) * fill < minnot[j] * (1 - 1e-9) or q == 0:
                            why = "below_min"
                if why is not None:
                    rejected.append({"n": e["n"], "i": e["i"], "symbol": panel.symbols[j],
                                     "reason": why})
                    continue
                book.fill(i, np.array([j]), np.array([q]), np.array([fill]), eq_open, int(t[i]))
                trail = e["trail"]
                if trail is not None:
                    tstop = fill * (1 - side * trail)
                    stop = tstop if stop is None else (max(stop, tstop) if side > 0 else min(stop, tstop))
                open_pos[j] = {"side": side, "stop": stop, "target": target, "trail": trail,
                               "best": fill, "entry_bar": i,
                               "exit_bar": None if e["time_stop"] is None else i + e["time_stop"]}
        # ---- 3. intrabar stops / targets (+ liquidation on the way), 4. ratchet --
        if open_pos and not dead:
            gap_exits, path_stops, tgt_hits = [], [], []
            for j in list(open_pos):
                if not P.ok_bar[i, j]:
                    continue
                p = open_pos[j]
                o_, h_, l_ = P.o[i, j], P.h[i, j], P.l[i, j]
                s, stp, tgt = p["side"], p["stop"], p["target"]
                if s > 0:
                    if stp is not None and o_ <= stp:
                        gap_exits.append((j, o_))            # gapped through the stop
                    elif tgt is not None and o_ >= tgt:
                        gap_exits.append((j, tgt))           # resting target fills AT target
                    elif stp is not None and l_ <= stp:
                        path_stops.append(((o_ - stp) / (o_ - l_) if o_ > l_ else 0.0, j, stp))
                    elif tgt is not None and h_ >= tgt:
                        tgt_hits.append((j, tgt))
                else:
                    if stp is not None and o_ >= stp:
                        gap_exits.append((j, o_))
                    elif tgt is not None and o_ <= tgt:
                        gap_exits.append((j, tgt))
                    elif stp is not None and h_ >= stp:
                        path_stops.append(((stp - o_) / (h_ - o_) if h_ > o_ else 0.0, j, stp))
                    elif tgt is not None and l_ <= tgt:
                        tgt_hits.append((j, tgt))
            # a) exits at the open
            for j, px in gap_exits:
                book.fill(i, np.array([j]), np.zeros(1), np.array([float(px)]),
                          book.cash + float(qty @ P.o_mark[i]), int(t[i]))
                del open_pos[j]
            # b) pessimistic intrabar path: every open position moves together
            #    from the open to its ADVERSE extreme. Stops fill as the path
            #    reaches them; if the account hits maintenance margin first (a
            #    stop sitting beyond the liquidation price), it is liquidated
            #    there and the stop never fills. Targets are favourable moves and
            #    are only filled after the account survived the adverse path.
            if qty.any():
                om = P.o_mark[i]
                adv = np.where(qty > 0, P.lo_f[i], P.hi_f[i])
                path_stops.sort(key=lambda x: (x[0], x[1]))
                for frac, j, px in path_stops + [(1.0, -1, None)]:
                    pr = om + frac * (adv - om)
                    if j >= 0:
                        pr[j] = px
                    e_s = book.cash + float(qty @ pr)
                    if qty.any() and e_s <= mm * float(np.abs(qty) @ pr):
                        _liquidate(book, i, pr, e_s, int(t[i]) + half, t[i], liqs)
                        open_pos.clear()
                        tgt_hits = []
                        dead = book.cash <= dead_level
                        break
                    if j >= 0:
                        book.fill(i, np.array([j]), np.zeros(1), np.array([float(px)]),
                                  max(e_s, 0.0), int(t[i]) + half)
                        del open_pos[j]
            # c) targets
            for j, px in tgt_hits:
                book.fill(i, np.array([j]), np.zeros(1), np.array([float(px)]),
                          book.cash + float(qty @ P.c_mark[i]), int(t[i]) + half)
                del open_pos[j]
            # d) trailing ratchet AFTER the checks, on survivors with a valid bar
            for j, p in open_pos.items():
                if p["trail"] is None or not P.ok_bar[i, j]:
                    continue
                if p["side"] > 0:
                    p["best"] = max(p["best"], P.h[i, j])
                    p["stop"] = max(p["stop"], p["best"] * (1 - p["trail"]))
                else:
                    p["best"] = min(p["best"], P.l[i, j])
                    p["stop"] = min(p["stop"], p["best"] * (1 + p["trail"]))
        # ---- 5. liquidation ---------------------------------------------------------
        has = (not dead) and qty.any()
        if has:
            adv = np.where(qty > 0, P.lo_f[i], P.hi_f[i])
            worst = book.cash + float(qty @ adv)
            if worst <= mm * float(np.abs(qty) @ adv):
                _liquidate(book, i, adv, worst, int(t[i]) + half, t[i], liqs)
                open_pos.clear()
                dead = book.cash <= dead_level
                has = False
        # ---- 6. funding + mark ------------------------------------------------------
        cm = P.c_mark[i]
        if has:
            mv = float(qty @ cm)
            if funding and P.fund_row[i]:
                book.pay_funding(i, P.fr[i], cm, book.cash + mv)
            e_ = book.cash + mv
            gross[i] = float(np.abs(qty) @ cm) / e_ if e_ > 0 else 0.0
            if e_ <= dead_level:
                kill = True
        else:
            e_ = book.cash
            if not dead and e_ <= dead_level:      # flat and (nearly) broke: stop
                dead = True
        eq[i] = e_
        cash[i] = book.cash
        if posarr is not None:
            posarr[i] = qty
    params = dict(fee=fee, slippage_bps=slippage_bps, funding=funding,
                  max_gross_leverage=max_gross_leverage, initial_equity=initial_equity,
                  maint_margin=maint_margin, round_to_qty=round_to_qty,
                  max_concurrent=max_concurrent, allow_flip=allow_flip)
    return _result(panel, book, eq, cash, posarr, gross, initial_equity, liqs, delists,
                   qty, P.c_mark[T - 1], params, rejected)
