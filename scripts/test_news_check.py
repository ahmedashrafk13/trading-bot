#!/usr/bin/env python3
"""Tests for the event-risk flags. Run: python scripts/test_news_check.py

No network: analyse() takes the already-fetched source data, so each rule is
proven to FIRE on a risky item and to STAND DOWN on a harmless one.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import news_check as N  # noqa: E402

FAILS = []
NOW = 1_790_000_000.0
H = 3600


def check(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + ("" if ok else f"  -> {detail}"))
    if not ok:
        FAILS.append(name)


def levels(flags, sym=None):
    return [f["level"] for f in flags if sym is None or f["symbol"] == sym]


print("ticker / name matching")
for text, tk, want in [
    ("Delisting of DOTUSDT Perpetual Contract", "DOT", True),
    ("$SOL rallies 8%", "SOL", True),
    ("LINK/USDT margin pair removed", "LINK", True),
    ("Chainlink oracle outage", "LINK", True),
    ("Solana network halts block production", "SOL", True),
    ("Coinbase SOLD its stake", "SOL", False),
    ("Users linked wallets to the dot-com app", "LINK", False),
    ("Users linked wallets to the dot-com app", "DOT", False),
    ("an avalanche of liquidations", "AVAX", False),
    ("ICXUSDT perpetual delisted", "BTC", False),
]:
    check(f"mentions({text!r}, {tk}) == {want}", N.mentions(text, tk) == want)

print("rules")
syms = ["DOTUSDT", "SOLUSDT"]
f = N.analyse(syms, {"bybit_announcements": [
    {"type": "delistings", "t": NOW - H, "text": "Delisting of DOTUSDT Perpetual Contract - ", "title": "x", "url": ""},
    {"type": "delistings", "t": NOW - H, "text": "Delisting of ICXUSDT Perpetual Contract - ", "title": "y", "url": ""}]},
    NOW)
check("Bybit delisting of a held coin -> RED", levels(f, "DOTUSDT") == ["RED"], f)
check("delisting of another coin -> nothing", levels(f, "SOLUSDT") == [], f)

f = N.analyse(syms, {"binance_delist": [{"t": NOW - H, "title": "Binance Will Delist DOT on 2026-10-02", "url": ""}]}, NOW)
check("Binance delisting -> RED", levels(f, "DOTUSDT") == ["RED"], f)

f = N.analyse(syms, {"bybit_status": [{"title": "scheduled maintenance"}]}, NOW)
check("exchange maintenance, no times -> RED for all", levels(f, "*") == ["RED"], f)
f = N.analyse(syms, {"bybit_status": [{"title": "m", "begin": str(int((NOW + 2 * H) * 1000)),
                                        "end": str(int((NOW + 3 * H) * 1000))}]}, NOW)
check("maintenance inside the hold -> RED", levels(f, "*") == ["RED"], f)
f = N.analyse(syms, {"bybit_status": [{"title": "m", "begin": str(int((NOW + 48 * H) * 1000)),
                                        "end": str(int((NOW + 49 * H) * 1000))}]}, NOW)
check("maintenance in 2 days -> INFO", levels(f, "*") == ["INFO"], f)
f = N.analyse(syms, {"bybit_status": []}, NOW)
check("no maintenance -> nothing", f == [], f)

f = N.analyse(syms, {"usdc_usdt": 0.991}, NOW)
check("USDC at 0.991 -> RED depeg", levels(f, "*") == ["RED"], f)
f = N.analyse(syms, {"usdc_usdt": 0.9998}, NOW)
check("USDC at 0.9998 -> nothing", f == [], f)

f = N.analyse(syms, {"macro": [{"t": NOW + 3 * H, "title": "CPI m/m", "forecast": "0.3%"},
                               {"t": NOW + 20 * H, "title": "FOMC Statement", "forecast": ""}]}, NOW)
check("CPI in 3h -> AMBER, FOMC in 20h -> INFO", levels(f, "*") == ["AMBER", "INFO"], f)

f = N.analyse(syms, {"hacks": [
    {"date": NOW - H, "name": "Big CEX", "amount": 250e6, "chain": ["Ethereum"], "technique": "key"},
    {"date": NOW - H, "name": "Some DEX", "amount": 20e6, "chain": ["Solana"], "technique": "bug"},
    {"date": NOW - H, "name": "Polkadot bridge", "amount": 15e6, "chain": ["Ethereum"], "technique": "bug"}]}, NOW)
check("$250M hack anywhere -> AMBER for all", levels(f, "*") == ["AMBER"], f)
check("hack on a coin's chain -> INFO", levels(f, "SOLUSDT") == ["INFO"], f)
check("hack naming the coin -> AMBER", levels(f, "DOTUSDT") == ["AMBER"], f)

f = N.analyse(syms, {"decrypt": [{"t": NOW - H, "title": "Solana network halted for 4 hours", "url": ""},
                                 {"t": NOW - H, "title": "Polkadot launches new parachain", "url": ""}],
                     "coindesk": [{"t": NOW - H, "title": "Solana network halted for 4 hours", "url": ""}]}, NOW)
check("risk-word headline -> AMBER (deduped across feeds)", levels(f, "SOLUSDT") == ["AMBER"], f)
check("plain headline -> INFO", levels(f, "DOTUSDT") == ["INFO"], f)

md = N.render(syms, [], ["a"], ["macro (HTTPError)"], NOW)
check("down sources are named in the output", "SOURCES DOWN" in md and "macro" in md, md)

print(f"\n{'ALL PASS' if not FAILS else f'{len(FAILS)} FAILED: ' + ', '.join(FAILS)}")
sys.exit(1 if FAILS else 0)
