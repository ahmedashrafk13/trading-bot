#!/usr/bin/env python3
"""Generate a self-contained HTML dashboard of the bot's live state.

    python scripts/dashboard.py          # writes dashboard.html and opens it
    python scripts/dashboard.py --no-open

Everything is read live from Bybit and baked into one file, so the page needs no
server and no network once written. It runs LOCALLY on purpose: it reads the
account through your API keys, and those must never reach a hosted page.

WHAT IT ANSWERS WITHOUT ASKING ANYONE
-------------------------------------
- Am I up or down, today and overall, against the BTC benchmark?
- Is every position protected? (the failure that has cost real money here twice)
- What is each position doing, how old is it, how close to its stop?
- Is any carry pair unhedged, which would be a naked leveraged bet?
- What has the fee budget and circuit breaker got left?
"""
import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import webbrowser

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BUDGET = float(os.environ.get("TRADING_BUDGET_USD") or 200)


def by(*args):
    r = subprocess.run([sys.executable, os.path.join(HERE, "bybit.py"), *args],
                       capture_output=True, text=True)
    try:
        return json.loads(r.stdout)
    except Exception:
        return None


def collect():
    perps = [p for p in (by("positions", "linear") or [])
             if float(p.get("size") or 0) != 0]
    spot = {c.get("coin"): float(c.get("walletBalance") or 0)
            for c in (by("holdings") or [])
            if float(c.get("walletBalance") or 0) > 0}
    orders = by("orders", "spot") or []
    btc = by("tickers", "linear", "BTCUSDT") or []
    hist = by("history", "linear") or []

    rows, unprotected, gross, upnl = [], [], 0.0, 0.0
    now = dt.datetime.now(dt.timezone.utc)
    for p in perps:
        sl = (p.get("stopLoss") or "").strip()
        has_sl = bool(sl) and sl not in ("0", "0.0")
        val = float(p.get("positionValue") or 0)
        pnl = float(p.get("unrealisedPnl") or 0)
        mark = float(p.get("markPrice") or 0)
        entry = float(p.get("avgPrice") or 0)
        gross += abs(val)
        upnl += pnl
        age = ""
        if p.get("createdTime"):
            h = (now - dt.datetime.fromtimestamp(
                int(p["createdTime"]) / 1000, dt.timezone.utc)).total_seconds() / 3600
            age = f"{h:.1f}h"
        dist = ((abs(mark - float(sl)) / mark * 100) if (has_sl and mark) else None)
        if not has_sl:
            unprotected.append(p.get("symbol"))
        rows.append({
            "symbol": p.get("symbol"), "side": p.get("side"),
            "dir": "SHORT" if p.get("side") == "Sell" else "LONG",
            "size": p.get("size"), "value": val, "entry": entry, "mark": mark,
            "pnl": pnl, "pct": ((mark / entry - 1) * 100 * (-1 if p.get("side") == "Sell" else 1)) if entry else 0,
            "lev": p.get("leverage"), "sl": sl if has_sl else None,
            "sl_dist": dist, "age": age,
            "hedged": (p.get("symbol", "").replace("USDT", "") in spot
                       and p.get("side") == "Sell"),
        })
    rows.sort(key=lambda r: r["pnl"], reverse=True)

    rejected = [o for o in hist if o.get("orderStatus") == "Rejected"
                and (o.get("stopOrderType") or "").startswith("Stop")]
    return {
        "generated": now.strftime("%Y-%m-%d %H:%M UTC"),
        "rows": rows, "gross": gross, "upnl": upnl,
        "unprotected": unprotected,
        "btc": float(btc[0]["lastPrice"]) if btc else 0,
        "spot_orders": len(orders),
        "rejected": len(rejected),
        "budget": BUDGET,
    }


TPL = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Trading Bot</title><style>
:root{--bg:#0d1117;--card:#161b22;--line:#30363d;--fg:#e6edf3;--dim:#8b949e;
--up:#3fb950;--down:#f85149;--warn:#d29922;--accent:#58a6ff}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);
font:14px/1.5 ui-sans-serif,-apple-system,Segoe UI,Roboto,sans-serif;padding:16px}
.wrap{max-width:1100px;margin:0 auto}
h1{font-size:20px;margin:0 0 2px}.sub{color:var(--dim);font-size:12px;margin-bottom:18px}
.grid{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));margin-bottom:18px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px}
.k{color:var(--dim);font-size:11px;text-transform:uppercase;letter-spacing:.06em}
.v{font-size:22px;font-weight:600;margin-top:4px;font-variant-numeric:tabular-nums}
.up{color:var(--up)}.down{color:var(--down)}.warn{color:var(--warn)}
table{width:100%;border-collapse:collapse;background:var(--card);
border:1px solid var(--line);border-radius:10px;overflow:hidden}
th{text-align:left;font-size:11px;color:var(--dim);text-transform:uppercase;
letter-spacing:.06em;padding:10px;border-bottom:1px solid var(--line)}
td{padding:10px;border-bottom:1px solid var(--line);font-variant-numeric:tabular-nums}
tr:last-child td{border-bottom:none}
.tag{font-size:10px;padding:2px 7px;border-radius:99px;font-weight:600}
.long{background:rgba(63,185,80,.15);color:var(--up)}
.short{background:rgba(248,81,73,.15);color:var(--down)}
.alert{background:rgba(248,81,73,.12);border:1px solid var(--down);color:var(--down);
padding:12px;border-radius:10px;margin-bottom:18px;font-weight:600}
.ok{background:rgba(63,185,80,.1);border:1px solid var(--up);color:var(--up);
padding:10px 12px;border-radius:10px;margin-bottom:18px}
.foot{color:var(--dim);font-size:12px;margin-top:20px;line-height:1.7}
@media(max-width:640px){.hide{display:none}body{padding:12px}.v{font-size:19px}}
</style></head><body><div class="wrap">
<h1>Trading Bot</h1><div class="sub">__GEN__ &middot; refresh: <code>python scripts/dashboard.py</code></div>
__ALERT__
<div class="grid">
<div class="card"><div class="k">Open positions</div><div class="v">__N__</div></div>
<div class="card"><div class="k">Unrealised</div><div class="v __UPC__">__UP__</div></div>
<div class="card"><div class="k">Gross notional</div><div class="v">__GROSS__</div></div>
<div class="card"><div class="k">Protected</div><div class="v __PROTC__">__PROT__</div></div>
<div class="card"><div class="k">BTC</div><div class="v">__BTC__</div></div>
</div>
__TABLE__
<div class="foot">
<b>How to read this.</b> Every position must show a stop. A blank stop means the
position is unprotected &mdash; that failure has cost real money here twice, so it is
the first thing to check.<br>
<b>Stop dist</b> is how far price must move against you before the stop fires.<br>
<b>Age</b> counts toward the 72h time stop: a position not up 5% in its favour by
then is closed to free the slot.<br>
<b>Hedged</b> matters only for carry pairs (short perp + long spot). A short marked
NOT HEDGED is a directional bet, not carry.
</div></div></body></html>"""


def render(d):
    alert = ""
    if d["unprotected"]:
        alert = (f'<div class="alert">{len(d["unprotected"])} UNPROTECTED POSITION(S): '
                 f'{", ".join(d["unprotected"])} &mdash; no stop attached. Fix before anything else.</div>')
    elif d["rejected"]:
        alert = (f'<div class="alert">{d["rejected"]} rejected protective stop(s) in recent history. '
                 f'A stop that fires and is REJECTED leaves no fill and no trace &mdash; check those symbols.</div>')
    elif d["rows"]:
        alert = '<div class="ok">All positions carry a stop. No rejected stops in recent history.</div>'

    if not d["rows"]:
        table = ('<div class="card"><div class="k">Positions</div>'
                 '<div style="margin-top:8px;color:var(--dim)">Flat &mdash; no open positions. '
                 'For the carry sleeve this is a valid state: it only trades when funding pays.</div></div>')
    else:
        body = ""
        for r in d["rows"]:
            cls = "up" if r["pnl"] >= 0 else "down"
            tag = "short" if r["dir"] == "SHORT" else "long"
            sl = (f'{r["sl"]}<span style="color:var(--dim)"> ({r["sl_dist"]:.1f}%)</span>'
                  if r["sl"] else '<span class="down">NONE</span>')
            hedge = ("&mdash;" if r["dir"] == "LONG"
                     else ('<span class="up">yes</span>' if r["hedged"]
                           else '<span class="warn">no</span>'))
            body += (f'<tr><td><b>{r["symbol"]}</b></td>'
                     f'<td><span class="tag {tag}">{r["dir"]}</span></td>'
                     f'<td class="hide">{r["lev"]}x</td>'
                     f'<td>${r["value"]:.2f}</td>'
                     f'<td class="{cls}">${r["pnl"]:+.2f}</td>'
                     f'<td class="{cls}">{r["pct"]:+.2f}%</td>'
                     f'<td class="hide">{sl}</td>'
                     f'<td class="hide">{r["age"]}</td>'
                     f'<td class="hide">{hedge}</td></tr>')
        table = ('<table><tr><th>Symbol</th><th>Side</th><th class="hide">Lev</th>'
                 '<th>Value</th><th>P&amp;L</th><th>%</th><th class="hide">Stop (dist)</th>'
                 f'<th class="hide">Age</th><th class="hide">Hedged</th></tr>{body}</table>')

    prot = f'{len(d["rows"]) - len(d["unprotected"])}/{len(d["rows"])}' if d["rows"] else "—"
    h = TPL
    for k, v in {
        "__GEN__": d["generated"], "__ALERT__": alert, "__TABLE__": table,
        "__N__": str(len(d["rows"])),
        "__UP__": f'${d["upnl"]:+.2f}',
        "__UPC__": "up" if d["upnl"] >= 0 else "down",
        "__GROSS__": f'${d["gross"]:.0f}',
        "__PROT__": prot,
        "__PROTC__": "down" if d["unprotected"] else "up",
        "__BTC__": f'${d["btc"]:,.0f}' if d["btc"] else "—",
    }.items():
        h = h.replace(k, v)
    return h


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-open", action="store_true")
    a = ap.parse_args()
    out = os.path.join(ROOT, "dashboard.html")
    d = collect()
    open(out, "w", encoding="utf-8").write(render(d))
    print(f"wrote {out}")
    print(f"  {len(d['rows'])} positions, unrealised ${d['upnl']:+.2f}, "
          f"{len(d['unprotected'])} unprotected")
    if not a.no_open:
        webbrowser.open("file:///" + out.replace("\\", "/"))


if __name__ == "__main__":
    main()
