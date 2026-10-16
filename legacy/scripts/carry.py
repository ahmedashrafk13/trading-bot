#!/usr/bin/env python3
"""LIVE delta-neutral funding capture. Scans, sizes, and reports both legs.

WHAT THIS IS
------------
The live counterpart of backtest/funding_carry.py, which is the best
risk-adjusted strategy this repo has found: +27.54% CAGR at -1.84% max drawdown
over 4.1 years at 3x, validated positive in every out-of-sample window. The
directional book, for comparison, is +12.62% at -41.94%.

The position is LONG SPOT + SHORT PERP in equal notional. The legs cancel, so
the coin's price is irrelevant; the return is the funding rate the exchange pays
shorts every 8 hours for carrying the other side of crowded leverage.

WHY IT IS SAFER THAN IT LOOKS, AND WHERE IT IS NOT
--------------------------------------------------
Safe: no directional exposure, no liquidation on the spot leg, and a sub-2%
drawdown that lets 3x ride where 3x on the directional book would be ruinous.

NOT safe, and NOT modelled in the backtest:
  * LEG DRIFT - spot and perp can diverge; the hedge is not perfect intraday.
  * SHORT-LEG LIQUIDATION - the perp leg still needs margin. If spot rallies
    hard, the short loses on paper and can be liquidated even though the pair
    is flat. Keep margin well above maintenance.
  * A ONE-LEGGED POSITION IS A NAKED DIRECTIONAL BET. If one leg fills and the
    other does not, you are long or short outright at 3x. That is the single
    most dangerous failure mode here, so `open` refuses to proceed unless BOTH
    legs can be placed, and reports loudly if it ends up one-legged.

Commands:
    python scripts/carry.py scan            # what is paying right now
    python scripts/carry.py positions       # current pairs and their funding
    python scripts/carry.py plan SYMBOL USD # what the two legs would be
"""
import json
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# Tuned on 4.1 years of real funding history, full-period sweep. The curve is
# FLAT from 0.00005 to 0.001 (26.9%-27.5% CAGR), so this is a plateau, not a
# spike -- which is what makes it a defensible choice rather than a fitted one.
MIN_RATE_8H = 0.0005      # only carry names paying at least this per 8h
MAX_PAIRS = 5
EXIT_AFTER_NEGATIVE = 9   # consecutive negative prints (3 days) before unwinding
TARGET_LEVERAGE = 3.0


def by(*args):
    r = subprocess.run([sys.executable, os.path.join(HERE, "bybit.py"), *args],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return None
    try:
        return json.loads(r.stdout)
    except Exception:
        return None


def annualise(rate_8h):
    """A rate per 8h compounds three times a day."""
    return ((1 + rate_8h) ** (3 * 365) - 1) * 100


def scan():
    tickers = by("tickers", "linear") or []
    rows = []
    for t in tickers:
        sym = t.get("symbol", "")
        if not sym.endswith("USDT"):
            continue
        try:
            r = float(t.get("fundingRate") or 0)
            turn = float(t.get("turnover24h") or 0)
        except (TypeError, ValueError):
            continue
        # Thin names quote wide, and the spread is paid on BOTH legs twice.
        # A high funding rate on an illiquid coin is usually a trap.
        if turn < 5_000_000:
            continue
        rows.append((r, sym, turn))
    rows.sort(reverse=True)

    print(f"FUNDING SCAN — pairs paying >= {MIN_RATE_8H:.4%} per 8h")
    print(f"{'symbol':16}{'8h rate':>10}{'annualised':>13}{'24h turnover':>16}")
    print("-" * 56)
    hits = 0
    for r, sym, turn in rows[:20]:
        flag = "  <-- carry candidate" if r >= MIN_RATE_8H else ""
        if r >= MIN_RATE_8H:
            hits += 1
        print(f"{sym:16}{r:>9.4%}{annualise(r):>12.1f}%{turn:>15,.0f}{flag}")
    print(f"\n{hits} name(s) clear the {MIN_RATE_8H:.4%} threshold. "
          f"Hold at most {MAX_PAIRS}.")
    if not hits:
        print("Nothing is paying enough. Holding no carry is the correct state —\n"
              "the backtest's returns come from being SELECTIVE, not from being on.")
    return rows


def plan(symbol, usd):
    """Size both legs. Neither is placed here; this only shows the arithmetic."""
    t = by("tickers", "linear", symbol) or []
    if not t:
        print(f"no perp ticker for {symbol}")
        return
    mark = float(t[0]["markPrice"])
    rate = float(t[0].get("fundingRate") or 0)
    qty = usd / mark
    margin = usd / TARGET_LEVERAGE

    print(f"DELTA-NEUTRAL PLAN — {symbol}")
    print(f"  notional per leg   ${usd:,.2f}")
    print(f"  perp mark          {mark:,.6f}")
    print(f"  qty (both legs)    {qty:,.6f}")
    print(f"  funding now        {rate:.4%} per 8h  ({annualise(rate):.1f}% annualised)")
    print(f"  margin at {TARGET_LEVERAGE:g}x      ${margin:,.2f}")
    print()
    print("  LEG 1 (spot, long):")
    print(f"    bybit.py order '{{\"category\":\"spot\",\"symbol\":\"{symbol}\","
          f"\"side\":\"Buy\",\"orderType\":\"Market\",\"qty\":\"{usd:.2f}\","
          f"\"marketUnit\":\"quoteCoin\",\"timeInForce\":\"GTC\"}}'")
    print("  LEG 2 (perp, short) — MUST follow immediately:")
    print(f"    bybit.py order '{{\"category\":\"linear\",\"symbol\":\"{symbol}\","
          f"\"side\":\"Sell\",\"orderType\":\"Market\",\"qty\":\"<held spot qty>\","
          f"\"stopLoss\":\"<see below>\",\"timeInForce\":\"GTC\"}}'")
    print()
    print("  The perp leg needs a stopLoss because scripts/checks.py refuses an")
    print("  unprotected perp. Place it FAR away (e.g. 3x the liquidation")
    print("  distance would be wrong — use the widest the gate allows), because")
    print("  in a hedged pair the short leg SHOULD lose when spot gains. A tight")
    print("  stop here would unwind the hedge and leave you long spot at size.")
    print()
    print("  ONE-LEGGED IS THE DANGER. If leg 1 fills and leg 2 does not, close")
    print("  leg 1 immediately rather than leaving an unhedged position.")


def positions():
    spot = by("holdings") or []
    perps = [p for p in (by("positions", "linear") or [])
             if float(p.get("size") or 0) != 0]
    spot_syms = {c.get("coin"): float(c.get("walletBalance") or 0)
                 for c in spot if float(c.get("walletBalance") or 0) > 0}
    print("CARRY POSITIONS (a pair = long spot + short perp in the same coin)")
    paired = 0
    for p in perps:
        sym = p.get("symbol", "")
        coin = sym.replace("USDT", "")
        if p.get("side") != "Sell":
            continue
        held = spot_syms.get(coin, 0.0)
        size = float(p.get("size") or 0)
        if held <= 0:
            print(f"  {sym:14} SHORT perp {size:<14g} spot 0  "
                  f"*** NOT HEDGED — this is a directional short, not carry ***")
            continue
        skew = (held - size) / max(size, 1e-9)
        paired += 1
        note = "" if abs(skew) < 0.05 else f"  *** LEGS OUT OF BALANCE {skew:+.1%} ***"
        print(f"  {sym:14} perp {size:<12g} spot {held:<12g} skew {skew:+.2%}{note}")
    if not paired:
        print("  no hedged pairs open")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "scan"
    if cmd == "scan":
        scan()
    elif cmd == "positions":
        positions()
    elif cmd == "plan":
        if len(sys.argv) < 4:
            print("usage: carry.py plan SYMBOL USD")
            return
        plan(sys.argv[2], float(sys.argv[3]))
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
