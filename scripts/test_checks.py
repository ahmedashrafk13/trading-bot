#!/usr/bin/env python3
"""Tests for the deterministic gate. Run: python scripts/test_checks.py

A risk gate nobody has seen reject anything is decoration. Every check below is
proven to FIRE on a bad order and to STAND DOWN on a good one. No network: the
fetch accessors are injected, which is why check_order takes them as an argument.
"""
import os
import sys
import pathlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import checks  # noqa: E402

FAILS = []


def check(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + ("" if ok else f"  -> {detail}"))
    if not ok:
        FAILS.append(name)


def fetch(positions=(), mark=100.0, leverage=3, realized=0.0):
    return {"positions": lambda: list(positions),
            "mark": lambda s: mark,
            "leverage": lambda s: leverage,
            "realized_today": lambda: realized}


def pos(sym, side, value, im=0.0, size=1):
    return {"symbol": sym, "side": side, "positionValue": value,
            "positionIM": im, "size": size}


def rejects(body, f, expect):
    try:
        checks.check_order(body, f)
        return False, "no rejection"
    except checks.GateReject as e:
        return (expect in str(e)), str(e)[:90]


GOOD_SHORT = {"category": "linear", "symbol": "BTCUSDT", "side": "Sell",
              "qty": "1", "stopLoss": "110", "_notional": 100.0}
GOOD_LONG = {"category": "linear", "symbol": "BTCUSDT", "side": "Buy",
             "qty": "1", "stopLoss": "90", "_notional": 100.0}

print("\nDETERMINISTIC GATE")

# --- a well-formed order must PASS, or the gate is just a wall -------------
try:
    v = checks.check_order(dict(GOOD_SHORT), fetch())
    check("a compliant short passes", v == "passed", v)
except checks.GateReject as e:
    check("a compliant short passes", False, str(e))

# --- exits are NEVER blocked, even with the breaker tripped ----------------
ok, d = True, ""
try:
    v = checks.check_order({"category": "linear", "symbol": "X", "side": "Buy",
                            "reduceOnly": True}, fetch(realized=-999))
    ok = "exit" in v
except checks.GateReject as e:
    ok, d = False, str(e)
check("a reduceOnly EXIT passes even with the breaker tripped", ok, d)

ok2 = True
try:
    checks.check_order({"category": "spot", "symbol": "X", "side": "Sell",
                        "orderFilter": "StopOrder"}, fetch(realized=-999))
except checks.GateReject as e:
    ok2 = False
check("a spot protective SELL is never blocked", ok2)

# --- each individual check fires ------------------------------------------
r, d = rejects({"category": "linear", "symbol": "B", "side": "Sell", "qty": "1"},
               fetch(), "naked_perp")
check("blocks an opening perp with no stopLoss", r, d)

r, d = rejects(dict(GOOD_SHORT), fetch(leverage=9), "leverage_cap")
check("blocks leverage above 5x", r, d)

# stop 20% away at 3x: liquidation ~33%, half is 16.5% -> too wide
r, d = rejects({**GOOD_SHORT, "stopLoss": "120"}, fetch(), "liquidation_clearance")
check("blocks a stop wider than half the liquidation distance", r, d)

r, d = rejects({**GOOD_SHORT, "stopLoss": "90"}, fetch(), "stop_side")
check("blocks a SHORT whose stop is BELOW the mark", r, d)

r, d = rejects({**GOOD_LONG, "stopLoss": "110"}, fetch(), "stop_side")
check("blocks a LONG whose stop is ABOVE the mark", r, d)

r, d = rejects(dict(GOOD_SHORT), fetch(realized=-11.0), "circuit_breaker")
check("blocks entries after a -5% realized day", r, d)

r, d = rejects({**GOOD_SHORT, "_notional": 700.0}, fetch(), "notional_cap")
check("blocks an order breaching the 300% gross notional cap", r, d)

r, d = rejects(dict(GOOD_SHORT),
               fetch(positions=[pos(f"S{i}", "Sell", 1, im=40) for i in range(3)]),
               "margin_cap")
check("blocks an order breaching the 50% margin cap", r, d)

r, d = rejects(dict(GOOD_SHORT),
               fetch(positions=[pos(f"S{i}", "Sell", 1) for i in range(12)]),
               "slots_full")
check("blocks a 13th short", r, d)

r, d = rejects(dict(GOOD_SHORT), fetch(positions=[pos("BTCUSDT", "Sell", 1)]),
               "duplicate_position")
check("blocks a duplicate position in the same symbol", r, d)

r, d = rejects(dict(GOOD_SHORT), fetch(positions=[pos("BTCUSDT", "Buy", 1)]),
               "opposing_position")
check("blocks taking the opposite side of a symbol already held", r, d)

r, d = rejects({"category": "inverse", "symbol": "B", "side": "Buy"},
               fetch(), "category")
check("blocks an out-of-mandate category", r, d)

# --- kill switch ----------------------------------------------------------
flag = checks.ROOT / "HALT_TRADING"
created = False
try:
    if not flag.exists():
        flag.write_text("test\n", encoding="utf-8")
        created = True
    r, d = rejects(dict(GOOD_SHORT), fetch(), "kill_switch")
    check("HALT_TRADING blocks every new entry", r, d)
    ok3 = True
    try:
        checks.check_order({"category": "linear", "symbol": "X", "side": "Buy",
                            "reduceOnly": True}, fetch())
    except checks.GateReject:
        ok3 = False
    check("HALT_TRADING still permits exits", ok3)
finally:
    if created:
        flag.unlink()
check("HALT_TRADING removed after the test", not flag.exists())

print()
if FAILS:
    print(f"{len(FAILS)} FAILED: " + ", ".join(FAILS))
    sys.exit(1)
print("gate holds on every check")
