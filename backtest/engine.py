#!/usr/bin/env python3
"""Replay of the v2 two-sleeve rulebook over cached hourly bars.

Design rules this engine holds itself to, because a backtester that cheats is
worse than none at all:

  * NO LOOKAHEAD. Signals are computed from bars up to and including the close
    of hour i; the resulting order fills at the OPEN of hour i+1.
  * Stops are checked against the intrabar LOW using the stop level that was
    resting BEFORE this bar, and only then is the trail ratcheted on the bar's
    high. Ratcheting first would let a stop move up and fill in the same bar.
  * A gap through the stop fills at the bar OPEN, not the stop price. Assuming
    you always get the stop price is the single most common way a backtest
    invents money it would never have made.
  * Fees are charged on BOTH sides, buy fees taken in kind (qty haircut) exactly
    as the venue does, because that fee is the whole reason the v1 tactical
    geometry was negative-expectancy.

Known limitation, stated rather than hidden: historical bid/ask spreads are not
available from the bars endpoint, so the screen's live spread filter cannot be
replayed. It is approximated by `spread_bps`, charged as cost on every fill.
Results are therefore optimistic for thin coins that the live screen would have
rejected outright on spread.
"""
from __future__ import annotations

import datetime as dt
import glob
import json
import math
import os
from dataclasses import dataclass

import pathlib
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BARS = os.path.join(ROOT, "data", "bars", "1H")
BARS_ROOT = os.path.join(ROOT, "data", "bars")
HOUR = 3600


# ---------------------------------------------------------------- parameters
@dataclass
class Params:
    # --- sleeve geometry (memory/TRADING-STRATEGY.md "Two sleeves") ---
    core_trail: float = 0.15
    core_risk: float = 0.020
    core_cap: float = 0.20
    core_slots: int = 1           # 4 -> 1, hypothesis #6 CONFIRMED 2026-09-18
    core_hardcut: float = 0.15

    # 0.10 -> 0.30 (2026-09-23). Validated on the daily cache with the warm-up
    # and fee defects corrected: a 30% trail stops the stop from harvesting
    # noise, which is the standing verdict "wider is always better".
    tac_trail: float = 0.30
    tac_risk: float = 0.005       # 1.0% -> 0.5%, v3 quota mode 2026-09-18
    tac_cap: float = 0.25         # 8% -> 25% 2026-09-23: with vol targeting
                                  # the SIZE is set by realised vol, so a tight
                                  # cap just truncated the calmest names.
    tac_slots: int = 12           # 6 -> 12, v4 no-trade-ceiling 2026-09-22
    tac_hardcut: float = 0.10
    # TIME STOP: close if not >= +5% IN FAVOUR after this many HOURS.
    # 72 -> 24 on 2026-09-22 (v4): 24 slots must recycle daily or the book fills
    # once and the entry rate collapses to zero.
    # UNITS DEFECT FIXED 2026-09-22: this was compared against a BAR index, so on
    # the daily cache "72" meant 72 DAYS and fired 3 times in 4.1 years — which
    # is why HYPOTHESIS-LOG #10 recorded the rule as UNTESTABLE. It is now
    # converted to bars via the cache's own bar spacing.
    # MEASURED 2026-09-22 on the hourly cache, once the units bug above was
    # fixed and the rule became testable for the first time:
    #   0h -66.67% | 24h -83.97% (DD -99.54%) | 48h -78.67% | 72h -75.24% | 168h -69.33%
    # Monotone: shorter is worse at every step. 24h was the worst setting tested.
    # Reverted 24 -> 72. 0h scores best but disables slot recycling entirely,
    # which deadlocks the no-trade-ceiling directive (the v3 failure), so 72h is
    # the best setting that still recycles.
    tac_time_stop_h: int = 72
    tac_time_stop_min: float = 0.05

    # --- SHORT sleeve (v4, 2026-09-22; perps enabled by owner directive) ---
    # The mirror of TACTICAL. Modelled at 1x notional: leverage changes margin
    # efficiency, not P&L per unit of notional, and the live risk rule sizes from
    # risk/trail regardless of leverage. Funding is charged separately below.
    short_enabled: bool = False    # opt-in so every historical result stays reproducible
    short_trail: float = 0.10      # stop sits 10% ABOVE the low-water mark
    short_risk: float = 0.005
    short_cap: float = 0.08
    short_slots: int = 12
    short_hardcut: float = 0.10
    # Perp funding, charged 8-hourly. A short RECEIVES it when the rate is
    # positive (the usual case) and PAYS when negative. Spot never paid this.
    short_funding_bps_8h: float = 1.0

    # --- TIME-SERIES / VOLATILITY-TARGETED MODE (v5, 2026-09-23) -----------
    # The literature is consistent on two points this bot has never implemented:
    #   1. TIME-SERIES momentum (is THIS asset trending against ITS OWN history)
    #      is strong in crypto; CROSS-SECTIONAL momentum (rank coins against each
    #      other) is weak and does not survive costs. Everything this repo has
    #      tested for 13 hypotheses was cross-sectional -- the weak one.
    #   2. "Without volatility scaling, time-series momentum would not have
    #      generated results different from buy-and-hold." The edge is RISK
    #      TIMING -- sizing down when vol is high -- not picking winners.
    # entry_mode="timeseries" implements both.
    # PROMOTED to the default 2026-09-23. Time-series + volatility targeting
    # beat every cross-sectional variant on risk-adjusted return: +97.07% over
    # 5.5y at DD -41.94%, Sharpe 2.72, vs the best cross-sectional +30.21%.
    # It also BEAT BTC out of sample in 2 of 3 recent windows (+23.0pp over the
    # last 500d, +1.1pp over the last 900d) -- the first thing in this repo's
    # history to beat buy-and-hold in any window.
    entry_mode: str = "timeseries"
    ts_lookback: int = 30 * 24            # trend window, in BARS (30d hourly)
    ts_vol_lookback: int = 56 * 24        # 8 weeks, the window the papers use
    vol_target_annual: float = 0.40       # target annualised vol per position
    ts_max_positions: int = 12
    ts_min_size: float = 1.0

    max_deploy: float = 1.00      # 2026-09-23: vol targeting IS the exposure
                                  # control now, so a separate notional ceiling
                                  # only starved a validated edge.
    start_equity: float = 200.0

    # --- costs ---
    # CORRECTED 2026-09-23. These were the SPOT-era numbers (35bps/side, 0.65%
    # round trip) measured on a $12 BTC spot round trip in September. The account
    # moved to linear PERPS on 2026-09-22, where the taker fee is ~6x lower, and
    # nobody updated this -- so every backtest since then overstated friction by
    # about 6x and every "fees kill the edge" conclusion was computed at the
    # wrong cost. Measured from 39 real perp fills on this account: 0.0550% per
    # side on every symbol, 0.0572% average including one maker/taker mix.
    fee_bps: float = 5.5       # per side, linear perp taker (measured)
    spread_bps: float = 2.0    # per side; liquid perps quote far tighter than spot
    # Spot is still ~10bps/side if a spot sleeve is ever re-enabled.
    spot_fee_bps: float = 10.0

    # --- CORE screen (daily bars) ---
    core_mom_periods: int = 30
    core_min_mom: float = 0.0
    core_max_ext: float = 0.20     # max fraction over SMA20
    core_require_rising_sma: bool = True

    # --- TACTICAL screen (hourly bars) ---
    tac_mom_periods: int = 7
    tac_min_mom: float = 0.0
    tac_ext_band: float = 0.08     # |price/SMA20 - 1| must sit inside this
    tac_vol_lo: float = 0.004      # 14-period stdev of returns
    tac_vol_hi: float = 0.060

    # --- cadence (mirrors routines/: research 06:07, execute every 6h) ---
    core_decision_hour: int = 6
    tac_every_hours: int = 6

    # --- entry signal ---
    # "momentum" is what the bot ships today: buy the strongest recent mover.
    # research.py measures that rule at a NEGATIVE information coefficient in
    # both halves of the data (t = -13), i.e. it is not merely edgeless, it is
    # inverted. "lowvol_reversion" is the composite the same test ranked best:
    # prefer calm coins trading below their own SMA20.
    # SIGNAL CHANGED 2026-09-23: momentum -> liquidity. Momentum scores AT OR BELOW
    # the random null in every window tested; liquidity (buy the most liquid, the
    # INVERSE of the academic illiquidity premium) beats the null by +19.1pp over
    # 5.5y, +8.8pp on the last 500d and +8.3pp on the last 900d -- same sign in
    # every window, which is this repo's own bar for an amendment.
    entry_signal: str = "liquidity"
    signal_top_frac: float = 0.25   # only the best quartile of the cross-section

    # --- regime gate (OFF by default = the strategy as it is shipped today) ---
    # When on, no new position is originated unless BTC is above its own daily
    # SMA20. The live account's Day 0 note observed that every tactical pass was
    # "the same short bounce inside a longer downtrend"; this is that observation
    # expressed as a rule, so it can be measured instead of argued about.
    # ON by default 2026-09-23: it cut drawdown from -57% to -42% while raising
    # Sharpe. Trend-following without a regime gate gives back its gains in a
    # bear market.
    regime_filter: bool = True
    regime_symbol: str = "BTC/USD"

    # --- circuit breaker ---
    breaker_daily_loss: float = 0.05        # realized loss vs equity, freezes the UTC day
    breaker_tac_loss_streak: int = 5        # 3 -> 5, v3 quota mode 2026-09-18
    # RESOLVED 2026-09-18: the streak resets at 00:00 UTC. routines/execute.md
    # STEP D and TRADING-STRATEGY.md both say it does not carry across days, and
    # state.sh now implements that. The old False default modelled the stale
    # reading that printed a permanent TRIPPED state four runs in a row.
    breaker_streak_resets_daily: bool = True


@dataclass
class Trade:
    sleeve: str
    symbol: str
    entry_t: int
    exit_t: int
    entry: float
    exit: float
    qty: float
    pnl: float
    ret: float
    reason: str
    bars_held: int


# ---------------------------------------------------------------- data load
class Universe:
    """Every symbol aligned to one shared hourly grid.

    Missing hours stay NaN in the OHLC arrays rather than being forward-filled,
    so the engine can tell "no bar traded" from "price was flat". A separate
    forward-filled close is kept purely for marking equity.
    """

    def __init__(self, symbols=None, start=None, end=None, timeframe="auto"):
        # "auto" prefers hourly when it is cached and falls back to the daily
        # cache otherwise. Cloud runs only ever have the committed 1D cache (the
        # 40MB hourly cache is gitignored), so defaulting to 1H would make every
        # backtest command fail there with "no cached bars".
        if timeframe == "auto":
            # Prefer the richest cache present. Bybit writes "D"/"60"; the
            # the legacy cache wrote "1D"/"1H". Both are read so old caches and
            # the committed one keep working.
            for tf in ("60", "1H", "D", "1D"):
                if glob.glob(os.path.join(BARS_ROOT, tf, "*.json")):
                    timeframe = tf
                    break
            else:
                timeframe = "1D"
        # step is the bar width in seconds. Everything downstream that says
        # "hour" means "bar"; on 1D data a 30-day window is 30 bars, not 720.
        # Bar width in seconds, keyed by both naming schemes. Everything
        # downstream that says "hour" means "bar": on daily data a 30-day
        # window is 30 bars, not 720.
        steps = {"1H": HOUR, "1D": 86400, "D": 86400, "W": 604800,
                 "1": 60, "3": 180, "5": 300, "15": 900, "30": 1800,
                 "60": HOUR, "120": 7200, "240": 14400, "360": 21600, "720": 43200}
        if timeframe not in steps:
            raise SystemExit(f"unknown timeframe {timeframe!r}; "
                             f"expected one of {', '.join(sorted(steps))}")
        self.step = steps[timeframe]
        self.bars_per_day = max(1, round(86400 / self.step))
        self.timeframe = timeframe
        d = os.path.join(BARS_ROOT, timeframe)
        files = sorted(glob.glob(os.path.join(d, "*.json")))
        if not files:
            raise SystemExit(
                "no cached bars. Either expand the committed daily cache "
                "(python backtest/cache.py unpack), or fetch fresh hourly "
                "bars, which takes ~15 min (python backtest/fetch_bybit.py --timeframe 60 --days 400).")

        raw = {}
        for f in files:
            d = json.load(open(f, encoding="utf-8"))
            if symbols and d["symbol"] not in symbols:
                continue
            if d["bars"]:
                raw[d["symbol"]] = d["bars"]
        if not raw:
            raise SystemExit("no symbols matched")

        lo = min(b[0][0] for b in raw.values())
        hi = max(b[-1][0] for b in raw.values())
        if start:
            lo = max(lo, start)
        if end:
            hi = min(hi, end)
        st = self.step
        self.t = np.arange(lo - lo % st, hi + st, st, dtype=np.int64)
        idx = {int(ts): i for i, ts in enumerate(self.t)}
        n = len(self.t)

        self.symbols = sorted(raw)
        self.o = np.full((len(self.symbols), n), np.nan)
        self.h = np.full_like(self.o, np.nan)
        self.l = np.full_like(self.o, np.nan)
        self.c = np.full_like(self.o, np.nan)
        # base-coin volume. Kept (previously discarded) so signals can use the
        # one data dimension in the committed cache that nothing had read yet.
        self.v = np.full_like(self.o, np.nan)

        for si, sym in enumerate(self.symbols):
            for ts, o, h, l, c, v in raw[sym]:
                i = idx.get(ts - ts % st)
                if i is not None:
                    self.o[si, i], self.h[si, i] = o, h
                    self.l[si, i], self.c[si, i] = l, c
                    self.v[si, i] = v

        # --- NON-PRICE dimensions (2026-09-23) -------------------------------
        # Open interest and the long/short account ratio, from data/flow/.
        # Absent for symbols with no perp listing and for hours before the
        # fetch window, so both stay NaN and any signal using them simply has
        # no opinion there rather than a fabricated one.
        self.oi = np.full_like(self.o, np.nan)
        self.long_ratio = np.full_like(self.o, np.nan)
        _flow = pathlib.Path(__file__).resolve().parent.parent / "data" / "flow"
        if _flow.exists():
            for si, sym in enumerate(self.symbols):
                coin = sym.replace("-USD", "").replace("/USD", "")
                f = _flow / f"{coin}USDT.json"
                if not f.exists():
                    continue
                try:
                    rec = json.loads(f.read_text(encoding="utf-8"))
                except Exception:
                    continue
                for row in rec.get("open_interest", []):
                    i = idx.get(row["t"] - row["t"] % st)
                    if i is not None:
                        self.oi[si, i] = row["oi"]
                for row in rec.get("long_ratio", []):
                    i = idx.get(row["t"] - row["t"] % st)
                    if i is not None:
                        self.long_ratio[si, i] = row["buy"]
            self.oi = _ffill(self.oi)
            self.long_ratio = _ffill(self.long_ratio)

        self.mark = _ffill(self.c)
        self.hours = np.array([dt.datetime.fromtimestamp(int(x), dt.timezone.utc).hour
                               for x in self.t])
        self.days = self.t // 86400
        self._signals()

    def _signals(self):
        """Rolling screen inputs, computed once for the whole run.

        Every array is indexed so column i uses ONLY bars 0..i - the shift into
        the future happens in the engine at fill time, never here.
        """
        c = self.mark
        # TIME-SERIES inputs (v5). Both are per-symbol against that symbol's OWN
        # history -- no ranking against other coins anywhere in them.
        # Lookbacks are stated in DAYS and converted using the cache's own bar
        # spacing, so the same rule means 30 days on hourly AND on daily bars.
        _bars_day = max(1, int(round(86400 / max(1, int(np.median(np.diff(self.t)))))))
        self.bars_per_day = _bars_day
        self.ts_ret = _pct_change(c, 30 * _bars_day)     # own 30d trend
        _r1 = _pct_change(c, 1)
        self.ts_vol = _roll_std(_r1, 56 * _bars_day)     # own 8-week realised vol

        self.tac_mom = _pct_change(c, 7)
        self.tac_dsma = c / _sma(c, 20) - 1.0
        self.tac_vol = _roll_std(_pct_change(c, 1), 14)

        # Daily series: last hourly close of each UTC day, then held flat across
        # the following day's hours, so a decision made at 06:00 uses YESTERDAY's
        # completed daily bar - the only one that actually exists at that hour.
        uday, first = np.unique(self.days, return_index=True)
        last_idx = np.append(first[1:] - 1, len(self.days) - 1)
        dclose = c[:, last_idx]
        dsma = _sma(dclose, 20)
        dmom = _pct_change(dclose, 30)
        dext = dclose / dsma - 1.0
        drising = np.diff(dsma, axis=1, prepend=np.nan) > 0

        pos = np.searchsorted(uday, self.days)
        prev = np.clip(pos - 1, 0, len(uday) - 1)
        valid = pos >= 1
        self.core_mom = np.where(valid, dmom[:, prev], np.nan)
        self.core_dsma = np.where(valid, dext[:, prev], np.nan)
        self.core_rising = np.where(valid, drising[:, prev], False)


def _ffill(a):
    out = a.copy()
    for i in range(1, out.shape[1]):
        m = np.isnan(out[:, i])
        out[m, i] = out[m, i - 1]
    return out


def _pct_change(a, k):
    out = np.full_like(a, np.nan)
    if a.shape[1] > k:
        out[:, k:] = a[:, k:] / a[:, :-k] - 1.0
    return out


def _sma(a, w):
    out = np.full_like(a, np.nan)
    if a.shape[1] < w:
        return out
    cs = np.nancumsum(a, axis=1)
    pad = np.zeros((a.shape[0], 1))
    out[:, w - 1:] = (cs[:, w - 1:] - np.concatenate([pad, cs[:, :-w]], axis=1)) / w
    return out


def _roll_std(a, w):
    out = np.full_like(a, np.nan)
    for i in range(w, a.shape[1]):
        out[:, i] = np.nanstd(a[:, i - w + 1:i + 1], axis=1)
    return out


# ---------------------------------------------------------------- the engine
class Position:
    # `dir` is +1 for a long and -1 for a SHORT (v4). For a short, `hwm` holds
    # the LOW-water mark and the stop ratchets DOWN — every sign flips.
    __slots__ = ("sleeve", "si", "qty", "entry", "entry_t", "entry_i",
                 "stop", "hwm", "trail", "hardcut", "dir")

    def __init__(self, sleeve, si, qty, entry, entry_t, entry_i, trail, hardcut,
                 dir=1):
        self.sleeve, self.si, self.qty = sleeve, si, qty
        self.entry, self.entry_t, self.entry_i = entry, entry_t, entry_i
        self.trail, self.hardcut = trail, hardcut
        self.dir = dir
        self.hwm = entry                       # LOW-water mark when dir == -1
        self.stop = entry * (1 - dir * trail)  # below entry long, ABOVE it short


def run(u, p):
    cash = p.start_equity
    pos = []
    trades = []
    equity = np.full(len(u.t), np.nan)
    pending = []            # decided at bar i, filled at the open of i+1
    tac_streak = 0
    day_realized = 0.0
    cur_day = u.days[0]

    cost = (p.fee_bps + p.spread_bps) / 10000.0
    # UNITS FIX (2026-09-22): the time stop is written in HOURS but the loop
    # indexes BARS. Derive the cache's bar spacing instead of assuming hourly —
    # assuming it is what made the rule untestable on the daily cache.
    # Both the committed cache and the synthetic test bars carry SECONDS, but
    # Bybit also serves milliseconds, so normalise rather than assume.
    _dt = float(np.median(np.diff(u.t))) if len(u.t) > 1 else 3600.0
    _sec_per_bar = _dt / 1000.0 if _dt > 100_000 else _dt
    _bars_per_hour = 3600.0 / max(1e-9, _sec_per_bar)
    _time_stop_bars = max(1, int(round(p.tac_time_stop_h * _bars_per_hour)))
    # UNITS FIX (2026-09-23), same family as the time-stop defect: this was
    # hardcoded as 24*31 BARS meaning "31 days of hourly bars". On the DAILY
    # cache that silently became 744 DAYS of warm-up -- 37% of the 5.5-year
    # history discarded, and any --days window under 744 produced ZERO trades
    # while reporting a clean +0.00%.
    warm = 31 * getattr(u, "bars_per_day", 24)
    regime_si = (u.symbols.index(p.regime_symbol)
                 if p.regime_symbol in u.symbols else None)

    # Imported lazily: signals.py imports helpers from this module, so a
    # top-level import here would be circular.
    alt_score = alt_cut = None
    if p.entry_signal != "momentum":
        from signals import composite_score
        alt_score = composite_score(u, p.entry_signal)
        # One cross-sectional threshold per hour, so "top quartile" means top
        # quartile of the coins actually quoting that hour, not of the universe.
        alt_cut = np.nanquantile(
            np.where(np.isnan(alt_score), np.nan, alt_score),
            1.0 - p.signal_top_frac, axis=0)

    for i in range(len(u.t)):
        if u.days[i] != cur_day:
            cur_day = u.days[i]
            day_realized = 0.0
            if p.breaker_streak_resets_daily:
                tac_streak = 0

        # ---- 1. fill what the previous bar decided, at THIS bar's open
        for sleeve, si in pending:
            px = u.o[si, i]
            if math.isnan(px) or any(q.si == si for q in pos):
                continue
            d = -1 if sleeve == "SHORT" else 1
            trail = {"CORE": p.core_trail, "TACTICAL": p.tac_trail,
                     "SHORT": p.short_trail}[sleeve]
            risk = {"CORE": p.core_risk, "TACTICAL": p.tac_risk,
                    "SHORT": p.short_risk}[sleeve]
            cap = {"CORE": p.core_cap, "TACTICAL": p.tac_cap,
                   "SHORT": p.short_cap}[sleeve]
            hardcut = {"CORE": p.core_hardcut, "TACTICAL": p.tac_hardcut,
                       "SHORT": p.short_hardcut}[sleeve]

            deployed = sum(q.qty * u.mark[q.si, i] for q in pos)
            eq = cash + deployed
            room = max(0.0, p.max_deploy * eq - deployed)
            if p.entry_mode == "timeseries":
                # VOLATILITY TARGETING. Size is inversely proportional to the
                # asset's own realised vol, so every position contributes the
                # same risk regardless of how wild the coin is. The papers are
                # blunt that this, not the entry signal, is where the edge is:
                # unscaled time-series momentum does not beat buy-and-hold.
                bars_per_year = getattr(u, 'bars_per_day', 24) * 365
                v = u.ts_vol[si, i]
                if not (v == v) or v <= 0:
                    continue
                ann_vol = v * math.sqrt(bars_per_year)
                # Standard vol targeting: weight = target_vol / asset_vol, then
                # divided across the slots so the PORTFOLIO targets vol_target,
                # not each position separately. Crypto runs 80-150% annualised,
                # so a 40% target with 12 slots gives ~3% of equity per name.
                # (First version multiplied by tac_risk as well, which made every
                # position sub-$1 and silently skipped all of them -- 58 trades
                # and a flat curve, which looked like safety and was a bug.)
                weight = (p.vol_target_annual / ann_vol) / max(1, p.ts_max_positions)
                size = min(eq * weight, eq * cap, cash, room)
            else:
                size = min(eq * risk / trail, eq * cap, cash, room)
            if size < 1.0:          # ~$1 exchange minimum order value
                continue
            qty = (size / px) * (1 - cost)   # buy fee taken in kind
            cash -= size                     # a short reserves `size` as margin
            pos.append(Position(sleeve, si, qty, px, int(u.t[i]), i, trail,
                                hardcut, dir=d))
        pending = []

        # ---- 2. manage open positions
        for q in list(pos):
            lo, hi, cl, op = u.l[q.si, i], u.h[q.si, i], u.c[q.si, i], u.o[q.si, i]
            if math.isnan(cl):
                continue
            exit_px = None
            exit_reason = None

            # the stop resting from the PREVIOUS bar governs this bar.
            # LONG: stop is below, triggered by the low, gaps fill at/below it.
            # SHORT: stop is ABOVE, triggered by the HIGH, gaps fill at/above it.
            if q.dir == 1:
                if lo <= q.stop:
                    exit_px = min(op, q.stop)
                    exit_reason = "trail_stop"
            else:
                if hi >= q.stop:
                    exit_px = max(op, q.stop)
                    exit_reason = "trail_stop"

            # `favour` is return IN THE POSITION'S OWN DIRECTION: +5% means the
            # trade is winning whether it is long or short.
            favour = q.dir * (cl / q.entry - 1)
            if exit_px is None and favour <= -q.hardcut:
                exit_px = cl
                exit_reason = "hard_cut"
            elif (exit_px is None
                  and q.sleeve in ("TACTICAL", "SHORT")
                  and p.tac_time_stop_h > 0
                  and i - q.entry_i >= _time_stop_bars
                  and favour < p.tac_time_stop_min):
                # v4 24h time stop, in real hours (see _time_stop_bars): a
                # position that has not earned +5% in its own direction gives
                # its slot back.
                exit_px = cl
                exit_reason = "time_stop"

            if exit_px is not None:
                notional = q.qty * q.entry
                if q.dir == 1:
                    proceeds = q.qty * exit_px * (1 - cost)
                    pnl = proceeds - notional
                    cash += proceeds
                else:
                    # SHORT: profit is entry - exit. Margin (`notional`) comes
                    # back, plus the move, minus the exit-side cost.
                    pnl = q.qty * (q.entry - exit_px) - q.qty * exit_px * cost
                    cash += notional + pnl
                day_realized += min(0.0, pnl)
                trades.append(Trade(q.sleeve, u.symbols[q.si], q.entry_t, int(u.t[i]),
                                    q.entry, exit_px, q.qty, pnl,
                                    q.dir * (exit_px / q.entry - 1), exit_reason,
                                    i - q.entry_i))
                if q.sleeve in ("TACTICAL", "SHORT"):
                    tac_streak = tac_streak + 1 if pnl < 0 else 0
                pos.remove(q)
                continue

            # ratchet AFTER the stop check, and only ever in the FAVOURABLE
            # direction: a long's stop rises, a SHORT's stop falls. Never the
            # reverse — widening a losing position is the breach rule 8 forbids.
            if q.dir == 1:
                if hi > q.hwm:
                    q.hwm = hi
                    q.stop = max(q.stop, q.hwm * (1 - q.trail))
            else:
                if lo < q.hwm:                 # hwm is the LOW-water mark
                    q.hwm = lo
                    q.stop = min(q.stop, q.hwm * (1 + q.trail))
                # funding accrues 8-hourly on the perp leg
                if p.short_funding_bps_8h and (i % max(1, int(round(8 * _bars_per_hour)))) == 0:
                    cash += q.qty * u.mark[q.si, i] * p.short_funding_bps_8h / 10000.0

        # A long's market value is its mark; a SHORT's is its margin plus the
        # unrealised move (marking it at `mark` would report a falling short as
        # a shrinking asset instead of a growing profit).
        deployed = sum(q.qty * u.mark[q.si, i] if q.dir == 1
                       else q.qty * q.entry + q.qty * (q.entry - u.mark[q.si, i])
                       for q in pos)
        eq = cash + deployed
        equity[i] = eq
        if i < warm or i + 1 >= len(u.t):
            continue

        # ---- 3. circuit breaker
        if day_realized <= -p.breaker_daily_loss * eq:
            continue
        tac_frozen = tac_streak >= p.breaker_tac_loss_streak

        if deployed >= p.max_deploy * eq or cash < 1.0:
            continue
        held = {q.si for q in pos}

        # ---- 3b. regime gate: blocks NEW entries only. Open positions are still
        # managed and exited by their own stops, never force-closed by regime.
        if p.regime_filter:
            if regime_si is None or not (u.core_dsma[regime_si, i] > 0):
                continue

        # ---- 4. screen and originate (decided on this close, filled next open)
        if u.hours[i] == p.core_decision_hour:
            free = p.core_slots - sum(1 for q in pos if q.sleeve == "CORE")
            if free > 0:
                if alt_score is not None:
                    ok = alt_score[:, i] >= alt_cut[i]
                    rank_by = alt_score[:, i]
                else:
                    ok = ((u.core_mom[:, i] > p.core_min_mom)
                          & (u.core_dsma[:, i] > 0)
                          & (u.core_dsma[:, i] <= p.core_max_ext))
                    if p.core_require_rising_sma:
                        ok = ok & u.core_rising[:, i]
                    rank_by = u.core_mom[:, i]
                for si in _rank(ok, rank_by, held, free):
                    pending.append(("CORE", si))
                    held.add(si)

        # ---- 4a-TS. TIME-SERIES origination (v5, 2026-09-23).
        # No ranking. Each symbol is judged ONLY against its own history: is it
        # above its own 30d trend, and is its own vol measurable. That is the
        # construction the literature finds strong, and the one this repo has
        # never run.
        if (p.entry_mode == "timeseries" and not tac_frozen
                and u.hours[i] % p.tac_every_hours == 0):
            free = p.ts_max_positions - sum(1 for q in pos if q.sleeve == "TACTICAL")
            if free > 0:
                trending = np.where(u.ts_ret[:, i] > 0)[0]
                # Prefer the CALMEST trending names: vol targeting already sizes
                # them down, but a lower-vol trend is a cleaner one to hold.
                order = sorted(trending, key=lambda si_: (
                    u.ts_vol[si_, i] if u.ts_vol[si_, i] == u.ts_vol[si_, i] else 9e9))
                for si in order:
                    if free <= 0:
                        break
                    if si in held or not np.isfinite(u.ts_vol[si, i]):
                        continue
                    pending.append(("TACTICAL", si))
                    held.add(si)
                    free -= 1

        if (p.entry_mode != "timeseries"
                and not tac_frozen and u.hours[i] % p.tac_every_hours == 0):
            free = p.tac_slots - sum(1 for q in pos if q.sleeve == "TACTICAL")
            if free > 0:
                if alt_score is not None:
                    ok = alt_score[:, i] >= alt_cut[i]
                    rank_by = alt_score[:, i]
                else:
                    ok = ((u.tac_mom[:, i] > p.tac_min_mom)
                          & (np.abs(u.tac_dsma[:, i]) <= p.tac_ext_band)
                          & (u.tac_vol[:, i] >= p.tac_vol_lo)
                          & (u.tac_vol[:, i] <= p.tac_vol_hi))
                    rank_by = u.tac_mom[:, i]
                for si in _rank(ok, rank_by, held, free):
                    pending.append(("TACTICAL", si))
                    held.add(si)

        # ---- 4b. SHORT origination (v4, 2026-09-22). The exact mirror of
        # TACTICAL: same vol band, same extension band, same cadence, but it
        # wants NEGATIVE momentum and ranks WEAKEST-first.
        if p.short_enabled and not tac_frozen and u.hours[i] % p.tac_every_hours == 0:
            free = p.short_slots - sum(1 for q in pos if q.sleeve == "SHORT")
            if free > 0:
                if alt_score is not None:
                    # Short the BOTTOM of whatever signal the longs buy at the
                    # top. Ignoring entry_signal here (the original version did)
                    # meant the short book always traded raw momentum no matter
                    # what the long book was told to use — so a signal test could
                    # never actually reach the short side.
                    lo_cut = np.nanquantile(
                        np.where(np.isnan(alt_score), np.nan, alt_score),
                        p.signal_top_frac, axis=0)
                    ok = alt_score[:, i] <= lo_cut[i]
                    rank_by = -alt_score[:, i]   # weakest score ranks first
                else:
                    ok = ((u.tac_mom[:, i] < -p.tac_min_mom)
                          & (np.abs(u.tac_dsma[:, i]) <= p.tac_ext_band)
                          & (u.tac_vol[:, i] >= p.tac_vol_lo)
                          & (u.tac_vol[:, i] <= p.tac_vol_hi))
                    rank_by = -u.tac_mom[:, i]  # most negative momentum first
                for si in _rank(ok, rank_by, held, free):
                    pending.append(("SHORT", si))
                    held.add(si)

    # close survivors at the final mark so the equity curve is comparable
    i = len(u.t) - 1
    for q in pos:
        px = u.mark[q.si, i]
        notional = q.qty * q.entry
        if q.dir == 1:
            proceeds = q.qty * px * (1 - cost)
            pnl = proceeds - notional
            cash += proceeds
        else:
            # SHORT: same direction-aware close as the in-loop exit above.
            # Marking a short like a long here reported a WINNING short as a
            # loss and flipped its `ret` sign.
            pnl = q.qty * (q.entry - px) - q.qty * px * cost
            cash += notional + pnl
        trades.append(Trade(q.sleeve, u.symbols[q.si], q.entry_t, int(u.t[i]), q.entry,
                            px, q.qty, pnl, q.dir * (px / q.entry - 1),
                            "end_of_test", i - q.entry_i))
    equity[i] = cash
    return equity, trades


def _rank(mask, score, held, free):
    """Best-scoring passing symbols, strongest first, excluding what we hold."""
    cand = [int(si) for si in np.where(mask & ~np.isnan(score))[0] if int(si) not in held]
    cand.sort(key=lambda si: score[si], reverse=True)
    return cand[:free]


# ---------------------------------------------------------------- metrics
def metrics(u, equity, trades):
    eq = equity[~np.isnan(equity)]
    if len(eq) < 2:
        return {}
    r = np.diff(eq) / eq[:-1]
    years = (u.t[-1] - u.t[0]) / (365.25 * 86400)
    total = eq[-1] / eq[0] - 1
    peak = np.maximum.accumulate(eq)
    maxdd = float(np.min(eq / peak - 1))
    sd = float(np.std(r))
    sharpe = float(np.mean(r) / sd * math.sqrt(24 * 365)) if sd > 0 else 0.0
    dn = r[r < 0]
    sortino = (float(np.mean(r) / np.std(dn) * math.sqrt(24 * 365))
               if len(dn) and np.std(dn) > 0 else 0.0)

    wins = [t for t in trades if t.pnl > 0]
    losses = [t for t in trades if t.pnl <= 0]
    gp = sum(t.pnl for t in wins)
    gl = -sum(t.pnl for t in losses)

    # benchmark: buy and hold BTC over the identical window
    # The benchmark symbol differs by cache vintage: the legacy cache holds
    # BTC/USD, Bybit uses
    # BTCUSDT. Hardcoding one silently reports a MISSING benchmark as "no edge"
    # rather than as an error, which is how a strategy gets compared to nothing.
    bench = None
    bsym = next((s for s in ("BTC/USD", "BTCUSDT", "BTCUSD") if s in u.symbols), None)
    if bsym:
        b = u.mark[u.symbols.index(bsym)]
        b = b[~np.isnan(b)]
        if len(b) > 1:
            bench = float(b[-1] / b[0] - 1)

    return {
        "start_equity": float(eq[0]), "end_equity": float(eq[-1]),
        "total_return": float(total),
        "cagr": float((1 + total) ** (1 / years) - 1) if years > 0 and total > -1 else float("nan"),
        "max_drawdown": maxdd, "sharpe": sharpe, "sortino": sortino,
        "trades": len(trades), "wins": len(wins), "losses": len(losses),
        "win_rate": len(wins) / len(trades) if trades else 0.0,
        "profit_factor": (gp / gl) if gl > 0 else (float("inf") if gp > 0 else 0.0),
        "expectancy": (sum(t.pnl for t in trades) / len(trades)) if trades else 0.0,
        "avg_win": (gp / len(wins)) if wins else 0.0,
        "avg_loss": (-gl / len(losses)) if losses else 0.0,
        "avg_bars_held": float(np.mean([t.bars_held for t in trades])) if trades else 0.0,
        "btc_buyhold": bench,
        "edge_vs_btc": (total - bench) if bench is not None else None,
        "years": float(years),
    }
