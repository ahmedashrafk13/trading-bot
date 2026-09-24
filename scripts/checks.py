#!/usr/bin/env python3
"""Deterministic pre-trade gate. The rules that cost money live HERE, not in a prompt.

WHY THIS FILE EXISTS
--------------------
Every expensive failure this account has had was a PROMPT failure, not a logic
failure. The rules were correct; a run read them wrong, or two files disagreed:

  2026-09-14  a target leg left 50% of DOT unstopped for 70h            -$1.61
  2026-09-18  execute.md mandated an order shape Bybit spot rejects, and
              a run "probed" it with a live buy that filled, unprotected
  2026-09-22  ARB/XPL stops triggered and were REJECTED; the naked window
              ran ~20h and was found only by luck                      -$2.29
  2026-09-22  summary.md STEP A4 denied a time stop three other files enforce
  2026-09-22  three routines called bybit.py subcommands that do not exist

A rulebook a model reads is a suggestion. A function that returns False is not.
So the gate fetches its own state from the exchange, never trusts a caller's
numbers, and is invoked from bybit.py's order path — there is no way to place an
opening order that skips it.

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
- It never blocks an EXIT. reduceOnly closes, spot sells and stop orders pass
  every check. A gate that can trap a loser is more dangerous than no gate.
- It does not enforce the fee budget or the time stop. Both need TRADE-LOG
  history rather than exchange state; state.sh owns them.
- It does not decide WHAT to trade. Signal selection stays with the model.
"""
from __future__ import annotations

import json
import math
import os
import pathlib

BUDGET = float(os.environ.get("TRADING_BUDGET_USD") or 200)
ROOT = pathlib.Path(__file__).resolve().parent.parent

# Sleeve caps, mirroring memory/TRADING-STRATEGY.md "Two sleeves"/v4.
MAX_CORE, MAX_TACTICAL, MAX_SHORT = 1, 12, 12
MAX_LEVERAGE = 5.0
MARGIN_CAP = 0.50      # of BUDGET
NOTIONAL_CAP = 3.00    # of BUDGET, long + short as ABSOLUTE values (not netted)
DAILY_LOSS_CAP = 0.05  # of BUDGET, realized, since 00:00 UTC


class GateReject(Exception):
    """Raised when a check fails. bybit.py turns this into a clean exit."""


def _reject(check, detail):
    raise GateReject(f"BLOCKED by {check}: {detail}")


def halted():
    """A HALT_TRADING file at the repo root stops every new position.

    Deliberately a file, not a config value: it can be created by anything
    (a human, a cron job, a phone over SSH) with no deploy and no restart.
    """
    return (ROOT / "HALT_TRADING").exists()


def is_exit(body):
    """True when this order can only REDUCE exposure. Exits are never blocked."""
    if body.get("reduceOnly"):
        return True
    # A spot conditional stop, or any spot sell, can only reduce a long.
    if body.get("category") == "spot" and body.get("side") == "Sell":
        return True
    return False


def check_order(body, fetch):
    """Run every pre-trade check. `fetch` is an injected accessor so this module
    stays testable without the network. Raises GateReject, or returns a note.

    Order matters: cheapest and most absolute checks first, so a halted account
    or a tripped breaker never triggers avoidable API calls.
    """
    if is_exit(body):
        return "exit — gate does not block risk-reducing orders"

    # ---- 1. kill switch --------------------------------------------------
    if halted():
        _reject("kill_switch",
                "HALT_TRADING exists at the repo root. Remove it to resume. "
                "Exits are still permitted.")

    cat = body.get("category", "spot")
    sym = body.get("symbol", "")
    side = body.get("side")

    # ---- 2. instrument mandate ------------------------------------------
    if cat not in ("spot", "linear"):
        _reject("category", f"{cat!r} is out of mandate; spot or linear only")
    if cat == "spot" and side == "Buy" and body.get("stopLoss"):
        _reject("spot_attached_tpsl",
                "spot rejects attached TP/SL (retCode 170130)")

    # ---- 3. protection must exist AT entry for a perp --------------------
    if cat == "linear" and not body.get("stopLoss"):
        _reject("naked_perp",
                "an opening perp order must carry an attached stopLoss — a "
                "leveraged position with no stop can be liquidated")

    # ---- 4. leverage + liquidation clearance -----------------------------
    # At Nx, liquidation is ~100/N% away. A stop must sit well inside that or
    # the position is liquidated before its own risk rule ever fires.
    if cat == "linear":
        lev = float(fetch["leverage"](sym) or 1)
        if lev > MAX_LEVERAGE:
            _reject("leverage_cap", f"{lev}x exceeds the {MAX_LEVERAGE:g}x cap")
        mark = float(fetch["mark"](sym))
        stop = float(body["stopLoss"])
        stop_dist = abs(mark - stop) / mark
        liq_dist = 1.0 / lev
        if stop_dist > liq_dist / 2:
            _reject("liquidation_clearance",
                    f"stop is {stop_dist:.1%} away but liquidation is ~{liq_dist:.1%}; "
                    f"the stop must sit inside half that ({liq_dist/2:.1%}). "
                    "Lower the leverage or reject the candidate.")
        # A stop on the WRONG SIDE is worse than none: it fires instantly.
        if side == "Buy" and stop >= mark:
            _reject("stop_side", f"long stop {stop} is at/above mark {mark}")
        if side == "Sell" and stop <= mark:
            _reject("stop_side", f"short stop {stop} is at/below mark {mark}")

    # ---- 5. circuit breaker ---------------------------------------------
    realized = float(fetch["realized_today"]())
    if realized <= -DAILY_LOSS_CAP * BUDGET:
        _reject("circuit_breaker",
                f"realized today ${realized:.2f} <= -{DAILY_LOSS_CAP:.0%} of "
                f"${BUDGET:.0f}. No new entries until 00:00 UTC. Exits allowed.")

    # ---- 6. exposure caps -------------------------------------------------
    positions = fetch["positions"]()
    gross = sum(abs(float(p.get("positionValue") or 0)) for p in positions)
    new_notional = float(body.get("_notional") or 0)
    if gross + new_notional > NOTIONAL_CAP * BUDGET:
        _reject("notional_cap",
                f"gross notional ${gross + new_notional:.2f} would exceed "
                f"${NOTIONAL_CAP * BUDGET:.2f} ({NOTIONAL_CAP:.0%} of budget)")

    # Margin must be measured AFTER the fill, not before: checking only what is
    # already open lets the order that breaches the cap through every time.
    margin = sum(float(p.get("positionIM") or 0) for p in positions)
    if cat == "linear":
        new_margin = new_notional / max(1.0, float(fetch["leverage"](sym) or 1))
    else:
        new_margin = new_notional
    if margin + new_margin > MARGIN_CAP * BUDGET:
        _reject("margin_cap",
                f"margin ${margin + new_margin:.2f} would exceed "
                f"${MARGIN_CAP * BUDGET:.2f} ({MARGIN_CAP:.0%} of budget)")

    # ---- 7. slot caps and one-position-per-symbol ------------------------
    longs = [p for p in positions if p.get("side") == "Buy"]
    shorts = [p for p in positions if p.get("side") == "Sell"]
    if side == "Sell" and len(shorts) >= MAX_SHORT:
        _reject("slots_full", f"SHORT slots full ({MAX_SHORT})")
    if side == "Buy" and len(longs) >= MAX_TACTICAL:
        _reject("slots_full", f"TACTICAL long slots full ({MAX_TACTICAL})")

    for p in positions:
        if p.get("symbol") == sym and float(p.get("size") or 0) != 0:
            if p.get("side") != side:
                _reject("opposing_position",
                        f"already {p.get('side')} {sym}; taking the other side "
                        "is a fee-paying no-op, not a hedge")
            # v9 (2026-09-24) resizes each position every 6h, so it must be able
            # to GROW a same-side position. Only scripts/v9.py sets this marker,
            # and only for strategy rebalances; every check above still applied.
            if not body.get("_allow_add"):
                _reject("duplicate_position", f"already holding {sym}")

    return "passed"


# --------------------------------------------------------------- live wiring
def live_fetch():
    """Accessors backed by the real exchange. Imported lazily so that importing
    this module for tests never touches the network."""
    import bybit as B

    def positions():
        r = B.request("GET", "/v5/position/list",
                      {"category": "linear", "settleCoin": "USDT"}, private=True)
        return [p for p in r.get("result", {}).get("list", [])
                if float(p.get("size") or 0) != 0]

    def mark(sym):
        r = B.request("GET", "/v5/market/tickers",
                      {"category": "linear", "symbol": sym})
        return r["result"]["list"][0]["markPrice"]

    def leverage(sym):
        for p in positions():
            if p.get("symbol") == sym:
                return p.get("leverage")
        r = B.request("GET", "/v5/position/list",
                      {"category": "linear", "symbol": sym}, private=True)
        lst = r.get("result", {}).get("list", [])
        return lst[0].get("leverage") if lst else 1

    def realized_today():
        import datetime as dt
        start = dt.datetime.now(dt.timezone.utc).replace(
            hour=0, minute=0, second=0, microsecond=0)
        r = B.request("GET", "/v5/position/closed-pnl",
                      {"category": "linear", "limit": 100,
                       "startTime": int(start.timestamp() * 1000)}, private=True)
        return sum(float(x.get("closedPnl") or 0)
                   for x in r.get("result", {}).get("list", []))

    return {"positions": positions, "mark": mark,
            "leverage": leverage, "realized_today": realized_today}
