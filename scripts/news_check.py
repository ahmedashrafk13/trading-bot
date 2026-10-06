#!/usr/bin/env python
"""v9 event-risk check - free public feeds, no API keys, never trades.

    python scripts/news_check.py            # coins the plan targets or holds
    python scripts/news_check.py --all      # all 12 strategy coins
    python scripts/news_check.py SOLUSDT    # specific symbols

Reads data/live/plan.json, pulls announcements / macro calendar / hacks / headlines,
and prints flags (also saved to data/live/news.md + news.json):

    RED    strong case to SKIP or cut size (delisting or maintenance on a coin we
           trade, stablecoin depeg, a big hack naming the coin)
    AMBER  consider resize < 1 (high-impact USD macro print inside the hold,
           risk-keyword headline naming the coin, very large hack anywhere)
    INFO   context only - never a reason to override on its own

Flags only justify skip / resize <= 1, never a bigger or flipped trade. Its value
is measured: prefix the decision reason with "NEWS:" when a flag drove it and
`v9.py scorecard` reports those overrides as their own line.
A source that fails is listed under "sources down" - check it by WebSearch.
"""
from __future__ import annotations

import datetime as dt
import email.utils
import json
import os
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LIVE = os.path.join(ROOT, "data", "live")
PLAN = os.path.join(LIVE, "plan.json")
OUT_MD = os.path.join(LIVE, "news.md")
OUT_JSON = os.path.join(LIVE, "news.json")
MACRO_CACHE = os.path.join(LIVE, "macro_cache.json")

HOLD_H = 8            # 6h hold + slack for late runs
NEWS_LOOKBACK_H = 24
HACK_LOOKBACK_H = 72
HACK_NOTE_USD = 10e6          # list hacks at least this big
HACK_MARKET_USD = 100e6       # AMBER for everyone: market-wide risk-off
DEPEG = 0.005                 # USDC/USDT off by more than 0.5% -> RED
UA = {"User-Agent": "Mozilla/5.0 (v9 news_check)"}

# ticker -> extra names; a ticker is matched upper-case as a whole word
NAMES = {
    "BTC": ["Bitcoin"], "ETH": ["Ethereum", "Ether"], "SOL": ["Solana"], "BNB": ["BNB Chain"],
    "XRP": ["Ripple", "XRP Ledger"], "DOGE": ["Dogecoin"], "ADA": ["Cardano"],
    "AVAX": ["Avalanche"], "LINK": ["Chainlink"], "LTC": ["Litecoin"], "TRX": ["Tron", "TRON"],
    "DOT": ["Polkadot"],
}
CHAINS = {"BTC": "Bitcoin", "ETH": "Ethereum", "SOL": "Solana", "BNB": "BSC", "XRP": "XRPL",
          "AVAX": "Avalanche", "TRX": "Tron", "DOT": "Polkadot", "ADA": "Cardano", "LTC": "Litecoin"}
RISK_WORDS = re.compile(
    r"\b(hack(ed|er|s)?|exploit(ed|s)?|drain(ed)?|breach|attack|stolen|delist(s|ed|ing)?|"
    r"suspend(s|ed)?|halt(s|ed)?|outage|downtime|depeg(ged)?|insolven\w*|bankrupt\w*|"
    r"lawsuit|sues|sued|charges|SEC|CFTC|DOJ|seiz(e|ed|ure)|unlock(s)?|vulnerabilit\w*|"
    r"rollback|chain (split|stall)|network (halt|down))\b", re.I)
FEEDS = {
    "cointelegraph": "https://cointelegraph.com/rss",
    "decrypt": "https://decrypt.co/feed",
    "theblock": "https://www.theblock.co/rss.xml",
    "coindesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
}


def get(url, timeout=12):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def get_json(url):
    return json.loads(get(url).decode("utf-8"))


def mentions(text, tk):
    """Whole-word upper-case ticker (also $SOL, DOTUSDT, LINK/USDT) or one of its proper
    names, case-sensitive so "an avalanche of ..." is not Avalanche."""
    if re.search(rf"(?<![A-Za-z0-9]){tk}(/?USDT|/?USDC|/?USD)?(?![A-Za-z0-9])", text):
        return True
    return any(re.search(rf"\b{re.escape(n)}\b", text) for n in NAMES.get(tk, []))


# ------------------------------------------------------------------ sources
def src_bybit_announcements(now):
    items = []
    for typ in ("delistings", "maintenance_updates", "product_updates"):
        d = get_json(f"https://api.bybit.com/v5/announcements/index?locale=en-US&type={typ}&limit=30")
        for a in d["result"]["list"]:
            t = (a.get("publishTime") or a.get("dateTimestamp") or 0) / 1000
            if now - t <= 72 * 3600:
                items.append({"type": typ, "t": t, "text": f"{a['title']} - {a.get('description', '')}",
                              "title": a["title"], "url": a["url"]})
    return items


def src_bybit_status(_now):
    return get_json("https://api.bybit.com/v5/system/status")["result"]["list"]


def src_binance_delist(now):
    d = get_json("https://www.binance.com/bapi/composite/v1/public/cms/article/list/query"
                 "?type=1&catalogId=161&pageNo=1&pageSize=20")
    arts = d["data"]["catalogs"][0]["articles"]
    return [{"t": a["releaseDate"] / 1000, "title": a["title"],
             "url": f"https://www.binance.com/en/support/announcement/{a['code']}"}
            for a in arts if now - a["releaseDate"] / 1000 <= 72 * 3600]


def src_macro(now):
    """ForexFactory week calendar. It rate-limits hard (429 for ~5 min), so the last good
    copy is cached and used for up to 24h if a fetch fails."""
    try:
        ev = get_json("https://nfs.faireconomy.media/ff_calendar_thisweek.json")
        with open(MACRO_CACHE, "w", encoding="utf-8") as f:
            json.dump(ev, f)
    except Exception:
        if not os.path.exists(MACRO_CACHE) or now - os.path.getmtime(MACRO_CACHE) > 24 * 3600:
            raise
        with open(MACRO_CACHE, encoding="utf-8") as f:
            ev = json.load(f)
    out = []
    for e in ev:
        if e.get("country") != "USD" or e.get("impact") != "High":
            continue
        t = dt.datetime.fromisoformat(e["date"]).timestamp()
        if -1800 <= t - now <= 36 * 3600:
            out.append({"t": t, "title": e["title"], "forecast": e.get("forecast", "")})
    return out


def src_hacks(now):
    d = get_json("https://api.llama.fi/hacks")
    return [h for h in d if now - (h.get("date") or 0) <= HACK_LOOKBACK_H * 3600
            and (h.get("amount") or 0) >= HACK_NOTE_USD]


def src_peg(_now):
    d = get_json("https://api.bybit.com/v5/market/tickers?category=spot&symbol=USDCUSDT")
    return float(d["result"]["list"][0]["lastPrice"])


def src_feed(url):
    def run(now):
        root = ET.fromstring(get(url))
        out = []
        for it in root.iter("item"):
            title = (it.findtext("title") or "").strip()
            pub = it.findtext("pubDate")
            try:
                t = email.utils.parsedate_to_datetime(pub).timestamp()
            except (TypeError, ValueError):
                continue
            if now - t <= NEWS_LOOKBACK_H * 3600:
                out.append({"t": t, "title": title, "url": (it.findtext("link") or "").strip()})
        return out
    return run


# ------------------------------------------------------------------ logic
def coins_of_interest(args):
    syms = [a.upper() for a in args if not a.startswith("-")]
    plan = None
    if os.path.exists(PLAN):
        with open(PLAN, encoding="utf-8") as f:
            plan = json.load(f)
    if not syms and plan:
        rows = plan["rows"]
        if "--all" in args:
            syms = [r["symbol"] for r in rows]
        else:
            syms = [r["symbol"] for r in rows if abs(r["target_usd"]) > 0 or abs(r["current_usd"]) > 0]
        syms += list(plan.get("non_strategy_positions", {}))
    return list(dict.fromkeys(syms)), plan


def hours(sec):
    return f"{sec / 3600:+.1f}h"


def analyse(syms, got, now):
    flags = []

    def flag(level, sym, src, text, url=""):
        flags.append({"level": level, "symbol": sym, "source": src, "text": text, "url": url})

    tks = {s: s.removesuffix("USDT") for s in syms}

    for m in got.get("bybit_status", []):
        # begin/end are ms strings; missing -> treat as ongoing (fail towards caution)
        begin = float(m.get("begin") or now * 1000) / 1000
        end = float(m.get("end") or now * 1000 + 1) / 1000
        hits_hold = begin <= now + HOLD_H * 3600 and end >= now
        flag("RED" if hits_hold else "INFO", "*", "bybit status",
             f"maintenance {m.get('title') or m} ({hours(begin - now)} to {hours(end - now)})", m.get("href", ""))
    for a in got.get("bybit_announcements", []):
        for s, tk in tks.items():
            if mentions(a["text"], tk):
                lvl = "RED" if a["type"] in ("delistings", "maintenance_updates") else "AMBER"
                flag(lvl, s, f"bybit {a['type']}", f"{a['title']} ({hours(a['t'] - now)})", a["url"])
    for a in got.get("binance_delist", []):
        for s, tk in tks.items():
            if mentions(a["title"], tk):
                flag("RED", s, "binance delisting", f"{a['title']} ({hours(a['t'] - now)}) - "
                     "the signal is Binance's ratio", a["url"])
    if "usdc_usdt" in got:
        px = got["usdc_usdt"]
        if abs(px - 1) > DEPEG:
            flag("RED", "*", "peg", f"USDC/USDT at {px:.4f} - stablecoin stress")
    for e in got.get("macro", []):
        dt_s = e["t"] - now
        when = dt.datetime.fromtimestamp(e["t"], dt.timezone.utc).strftime("%a %H:%M UTC")
        txt = f"USD {e['title']} {when} ({hours(dt_s)})" + (f", forecast {e['forecast']}" if e["forecast"] else "")
        flag("AMBER" if dt_s <= HOLD_H * 3600 else "INFO", "*", "macro calendar", txt)
    for h in got.get("hacks", []):
        amt = h.get("amount") or 0
        chains = h.get("chain") or []
        hit = [s for s, tk in tks.items() if mentions(h.get("name", ""), tk) or CHAINS.get(tk) in chains]
        txt = (f"{h.get('name')} ${amt / 1e6:.0f}M ({h.get('technique') or h.get('classification')}, "
               f"{'/'.join(chains)}, {hours(h['date'] - now)})")
        if amt >= HACK_MARKET_USD:
            flag("AMBER", "*", "hack", txt + " - large enough to move the whole market")
        for s in hit:
            flag("AMBER" if mentions(h.get("name", ""), tks[s]) else "INFO", s, "hack", txt)
    seen = set()
    for src in FEEDS:
        for n in got.get(src, []):
            key = n["title"].lower()
            if key in seen:
                continue
            seen.add(key)
            for s, tk in tks.items():
                if mentions(n["title"], tk):
                    lvl = "AMBER" if RISK_WORDS.search(n["title"]) else "INFO"
                    flag(lvl, s, src, f"{n['title']} ({hours(n['t'] - now)})", n["url"])
    return flags


def render(syms, flags, ok, down, now):
    stamp = dt.datetime.fromtimestamp(now, dt.timezone.utc).strftime("%Y-%m-%d %H:%M")
    L = [f"# v9 news check - {stamp} UTC", "",
         f"Coins: {', '.join(syms) if syms else '(none targeted or held)'} | hold window {HOLD_H}h | "
         f"sources ok: {len(ok)}/{len(ok) + len(down)}"]
    if down:
        L.append(f"SOURCES DOWN (check by WebSearch): {', '.join(down)}")
    order = {"RED": 0, "AMBER": 1, "INFO": 2}
    red = [f for f in flags if f["level"] == "RED"]
    amber = [f for f in flags if f["level"] == "AMBER"]
    L += ["", f"Summary: {len(red)} RED, {len(amber)} AMBER"
          + (" - nothing found that argues against the strategy's trades." if not red and not amber else "")]
    info_per = {}
    for f in sorted(flags, key=lambda x: (order[x["level"]], x["symbol"])):
        if f["level"] == "INFO":
            info_per[f["symbol"]] = info_per.get(f["symbol"], 0) + 1
            if info_per[f["symbol"]] > 4:
                continue
        url = f" <{f['url']}>" if f["url"] else ""
        L.append(f"- {f['level']:5s} {f['symbol']:9s} [{f['source']}] {f['text']}{url}")
    L += ["", "RED = strong case to skip/cut; AMBER = consider resize < 1; INFO = context only.",
          "Flags never justify a bigger or flipped trade. Prefix the reason with NEWS: when a flag drove it."]
    return "\n".join(L)


def main(args):
    now = time.time()
    syms, _plan = coins_of_interest(args)
    jobs = {"bybit_status": src_bybit_status, "bybit_announcements": src_bybit_announcements,
            "binance_delist": src_binance_delist, "macro": src_macro, "hacks": src_hacks,
            "usdc_usdt": src_peg, **{k: src_feed(u) for k, u in FEEDS.items()}}
    got, down = {}, []
    with ThreadPoolExecutor(max_workers=len(jobs)) as ex:
        fut = {k: ex.submit(fn, now) for k, fn in jobs.items()}
        for k, f in fut.items():
            try:
                got[k] = f.result(timeout=40)
            except Exception as e:           # noqa: BLE001 - any source may fail; never block the run
                down.append(f"{k} ({type(e).__name__})")
    flags = analyse(syms, got, now)
    md = render(syms, flags, list(got), down, now)
    os.makedirs(LIVE, exist_ok=True)
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write(md + "\n")
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump({"run_utc": dt.datetime.fromtimestamp(now, dt.timezone.utc).strftime("%Y-%m-%d %H:%M"),
                   "symbols": syms, "flags": flags, "sources_down": down}, f, indent=1)
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(md)


if __name__ == "__main__":
    main(sys.argv[1:])
