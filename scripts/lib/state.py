"""Compute every guardrail number, so no run has to do arithmetic over markdown.

Usage: python state.py <orders.json> <tickers.json> <fills.json...>

All equity-relative rules are measured against the $200 BOOK, never against
Bybit account equity (~$181k on this demo account) -- see scripts/lib/book.py.
Using account equity would set the fee budget at ~$2,700/week and the circuit
breaker at ~$5,400, i.e. would disable both.
"""
import datetime as dt
import json
import sys

import book

WEEKLY_FEE_BUDGET_PCT = 0.015     # 1.5% of the book
CIRCUIT_LOSS_PCT = 0.03           # 3% of the book, realized, in one UTC day
CIRCUIT_LOSS_STREAK = 3


def main() -> None:
    orders_path, tickers_path = sys.argv[1], sys.argv[2]
    fill_paths = sys.argv[3:]

    led = book.load_ledger()
    added = 0
    for p in fill_paths:
        payload = json.load(open(p, encoding='utf-8'))
        added += book.merge_fills(led, (payload.get('result') or {}).get('list') or [])
    if added:
        book.save_ledger(led)

    marks = {}
    for t in (json.load(open(tickers_path, encoding='utf-8')).get('result')
              or {}).get('list') or []:
        try:
            marks[t['symbol']] = float(t['lastPrice'])
        except (KeyError, TypeError, ValueError):
            continue

    orders = (json.load(open(orders_path, encoding='utf-8')).get('result')
              or {}).get('list') or []
    # Only the bot's own resting orders count as protection. A leftover sell
    # from the account's prior life is not a stop the bot placed or will manage.
    bot_orders = [o for o in orders if book.is_bot(o)]

    open_pos, realized, fees = book.build_positions(led)

    # NEVER trust the local clock — this machine is known to run fast. Bybit has
    # no /clock endpoint, but every response carries a server `time` field; the
    # caller passes it through in tickers.json.
    srv = json.load(open(tickers_path, encoding='utf-8')).get('time')
    now = (dt.datetime.fromtimestamp(int(srv) / 1000, dt.timezone.utc) if srv
           else dt.datetime.now(dt.timezone.utc))
    now_ms = int(now.timestamp() * 1000)
    today = now.date()
    monday = today - dt.timedelta(days=today.weekday())
    monday_ms = int(dt.datetime.combine(
        monday, dt.time.min, tzinfo=dt.timezone.utc).timestamp() * 1000)
    midnight_ms = int(dt.datetime.combine(
        today, dt.time.min, tzinfo=dt.timezone.utc).timestamp() * 1000)

    realized_pnl = sum(r['pnl'] for r in realized if not r.get('orphan'))
    unrealized = 0.0
    for p in open_pos:
        mark = marks.get(p['symbol'])
        p['mark'] = mark
        p['value'] = (mark * p['qty']) if mark else p['cost']
        p['upnl_pct'] = ((p['value'] - p['cost']) / p['cost'] * 100) if p['cost'] else 0.0
        unrealized += p['value'] - p['cost']

    equity = book.BOOK_SIZE + realized_pnl + unrealized - fees
    deployed = sum(p['value'] for p in open_pos)
    cash = equity - deployed

    print(f'UTC NOW (Bybit server clock)  {now:%Y-%m-%d %H:%M} UTC   '
          f'[local clock is NOT trusted]')
    print(f'BOOK ${book.BOOK_SIZE:.2f} | EQUITY ${equity:.2f} | CASH ${cash:.2f} '
          f'| DEPLOYED {deployed / equity * 100 if equity else 0:.1f}% (target 75-85%)')
    print()

    # --- positions, ages, stop coverage ---------------------------------------
    print(f'OPEN POSITIONS ({len(open_pos)})')
    if not open_pos:
        print('  none')
    for p in sorted(open_pos, key=lambda r: -r['value']):
        sym = p['symbol']
        qty = p['qty']
        resting = [o for o in bot_orders if o.get('symbol') == sym
                   and o.get('side') == 'Sell']
        # A stop on Bybit spot is an order carrying a triggerPrice; a bare Limit
        # sell with no trigger is the take-profit leg.
        stop_qty = sum(float(o.get('qty') or 0) for o in resting
                       if o.get('triggerPrice'))
        tgt_qty = sum(float(o.get('qty') or 0) for o in resting
                      if not o.get('triggerPrice'))
        pct_cov = stop_qty / qty * 100 if qty else 0
        pct_tgt = tgt_qty / qty * 100 if qty else 0
        unreserved = max(0.0, 100 - pct_cov - pct_tgt)
        # What matters is UNRESERVED quantity, not stop share. A split position
        # shows 50% stop / 50% target and is fully accounted for — flagging that
        # as a gap would make a run "fix" it by cancelling the target leg.
        if unreserved > 0.5:
            flag = '*** NAKED ***' if pct_cov < 0.5 else f'*** {unreserved:.0f}% UNRESERVED ***'
        elif pct_tgt > 0.5:
            flag = 'SPLIT ok'
        else:
            flag = 'OK full stop'
        age_h = (now_ms - p['opened']) / 3_600_000 if p['opened'] else 0
        print(f"  {sym:12} {p['sleeve']:9} qty={qty:<14.6f} P&L {p['upnl_pct']:+6.2f}%  "
              f"stop {pct_cov:5.1f}% / target {pct_tgt:5.1f}% / unreserved "
              f"{unreserved:4.1f}%  [{flag}]  age {age_h:.1f}h")
        if p['sleeve'] == 'TACTICAL' and age_h > 48:
            print('    !! open >48h — reassess-or-close rule applies')
        if p['upnl_pct'] <= -15:
            print('    !! past -15% — hard cut applies, the stop missed')
    print()

    # --- fee budget -----------------------------------------------------------
    fees_wk = 0.0
    for f in led['fills'].values():
        if f['ts'] >= monday_ms:
            fx = f['fee']
            fees_wk += fx * f['price'] if (f['side'] == 'Buy'
                                           and f['feeCoin'] not in ('USDT', '')) else fx
    budget = book.BOOK_SIZE * WEEKLY_FEE_BUDGET_PCT
    print(f'FEE BUDGET  ${fees_wk:.2f} / ${budget:.2f} used this week '
          f'(1.5% of the ${book.BOOK_SIZE:.0f} book)')
    print('            ' + (f'HEADROOM ${budget - fees_wk:.2f}' if fees_wk < budget
                            else '*** EXHAUSTED — no new entries until Monday ***'))
    print(f'            week started {monday}')
    print()

    # --- circuit breaker ------------------------------------------------------
    today_trades = [r for r in realized
                    if not r.get('orphan') and r['closed'] >= midnight_ms]
    today_loss = sum(r['pnl'] for r in today_trades if r['pnl'] < 0)
    streak = 0
    for r in sorted((r for r in realized if not r.get('orphan')),
                    key=lambda r: -r['closed']):
        if r['pnl'] < 0:
            streak += 1
        else:
            break
    limit = book.BOOK_SIZE * CIRCUIT_LOSS_PCT
    tripped = abs(today_loss) >= limit or streak >= CIRCUIT_LOSS_STREAK
    print(f'CIRCUIT BREAKER  realized losses today ${abs(today_loss):.2f} '
          f'vs ${limit:.2f} limit (3% of book)')
    print(f'                 consecutive losing closes: {streak} '
          f'({CIRCUIT_LOSS_STREAK} stops entries for the UTC day)')
    print(f'                 status: '
          f"{'TRIPPED — no new entries' if tripped else 'clear'}")
    print()

    # --- amendment trigger ----------------------------------------------------
    closed = len([r for r in realized if not r.get('orphan')])
    print(f'AMENDMENT TRIGGER  closed trades logged: {closed} | need >= 10 '
          'since last amendment')
    print(f"                   status: "
          f"{'ELIGIBLE' if closed >= 10 else 'not eligible — change nothing'}")


if __name__ == '__main__':
    main()
