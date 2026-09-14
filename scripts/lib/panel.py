"""Render the $200 book performance panel.

Usage: python panel.py <fills.json...> --tickers <tickers.json> [--json]

Answers one question: what has the bot actually done with its $200? Account
equity is deliberately NOT the denominator -- see scripts/lib/book.py for why.
"""
import datetime as dt
import json
import sys

import book


def fmt_money(x):
    return f'{"-" if x < 0 else "+"}${abs(x):,.2f}'


def fmt_age(ms, now_ms):
    if not ms:
        return '?'
    hours = (now_ms - ms) / 3_600_000
    if hours < 48:
        return f'{hours:.0f}h'
    return f'{hours / 24:.1f}d'


def main() -> None:
    args = sys.argv[1:]
    as_json = '--json' in args
    do_reset = '--reset' in args
    args = [a for a in args if a not in ('--json', '--reset')]
    if do_reset:
        led = book.reset_ledger()
        print(f'book reset — fills before '
              f'{dt.datetime.fromtimestamp(led["epoch_ms"] / 1000, dt.timezone.utc):%Y-%m-%d %H:%M} '
              f'UTC are now excluded; the book starts at ${book.BOOK_SIZE:,.2f}.')
    tick_path = args[args.index('--tickers') + 1]
    fill_paths = args[:args.index('--tickers')]

    led = book.load_ledger()
    added = 0
    for p in fill_paths:
        payload = json.load(open(p, encoding='utf-8'))
        added += book.merge_fills(led, (payload.get('result') or {}).get('list') or [])
    if added:
        book.save_ledger(led)

    marks = {}
    tdata = json.load(open(tick_path, encoding='utf-8'))
    for t in (tdata.get('result') or {}).get('list') or []:
        try:
            marks[t['symbol']] = float(t['lastPrice'])
        except (KeyError, TypeError, ValueError):
            continue

    open_pos, realized, fees = book.build_positions(led)
    now_ms = int(dt.datetime.now(dt.timezone.utc).timestamp() * 1000)

    realized_pnl = sum(r['pnl'] for r in realized if not r.get('orphan'))
    unrealized = 0.0
    for p in open_pos:
        mark = marks.get(p['symbol'])
        p['mark'] = mark
        p['value'] = (mark * p['qty']) if mark else p['cost']
        p['upnl'] = p['value'] - p['cost']
        p['upnl_pct'] = (p['upnl'] / p['cost'] * 100) if p['cost'] else 0.0
        unrealized += p['upnl']

    deployed = sum(p['value'] for p in open_pos)
    # Net P&L is realized + unrealized - fees. Fees are subtracted ONCE here and
    # never folded into the per-trade pnl, so the two never double-count.
    net = realized_pnl + unrealized - fees
    equity = book.BOOK_SIZE + net
    cash = equity - deployed

    wins = [r for r in realized if not r.get('orphan') and r['pnl'] > 0]
    losses = [r for r in realized if not r.get('orphan') and r['pnl'] <= 0]
    closed = len(wins) + len(losses)

    if as_json:
        print(json.dumps({
            'book_size': book.BOOK_SIZE, 'equity': equity, 'cash': cash,
            'deployed': deployed, 'net_pnl': net, 'realized': realized_pnl,
            'unrealized': unrealized, 'fees': fees, 'closed_trades': closed,
            'wins': len(wins), 'losses': len(losses),
            'open_positions': open_pos,
        }, indent=2, default=str))
        return

    pct = net / book.BOOK_SIZE * 100
    bar_n = max(0, min(40, int(round(equity / book.BOOK_SIZE * 20))))
    bar = '#' * bar_n + '.' * (40 - bar_n)

    print()
    print('=' * 62)
    print(f'  $200 BOOK  —  {dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M} UTC')
    print('=' * 62)
    print(f'  EQUITY      ${equity:>9,.2f}   (started ${book.BOOK_SIZE:,.2f})')
    print(f'  NET P&L     {fmt_money(net):>10}   {pct:+.2f}%')
    print(f'  [{bar}]')
    print()
    print(f'  realized    {fmt_money(realized_pnl):>10}')
    print(f'  unrealized  {fmt_money(unrealized):>10}')
    print(f'  fees paid   {fmt_money(-fees):>10}   ({fees / book.BOOK_SIZE * 100:.2f}% of book)')
    print()
    print(f'  cash        ${cash:>9,.2f}')
    print(f'  deployed    ${deployed:>9,.2f}   ({deployed / equity * 100 if equity else 0:.1f}% — target 75-85%)')
    print()

    print(f'  OPEN POSITIONS ({len(open_pos)})')
    if not open_pos:
        print('    none')
    else:
        print(f"    {'coin':10}{'sleeve':10}{'qty':>14}{'entry':>12}{'mark':>12}"
              f"{'value':>10}{'P&L':>10}{'%':>8}  age")
        for p in sorted(open_pos, key=lambda r: -r['value']):
            base = p['symbol'][:-4] if p['symbol'].endswith('USDT') else p['symbol']
            print(f"    {base:10}{p['sleeve']:10}{p['qty']:>14,.6f}"
                  f"{p['avg_entry']:>12,.4f}{(p['mark'] or 0):>12,.4f}"
                  f"{p['value']:>10,.2f}{p['upnl']:>+10,.2f}{p['upnl_pct']:>+8.1f}"
                  f"  {fmt_age(p['opened'], now_ms)}")
    print()

    wr = (len(wins) / closed * 100) if closed else 0.0
    avg_w = (sum(r['pnl'] for r in wins) / len(wins)) if wins else 0.0
    avg_l = (sum(r['pnl'] for r in losses) / len(losses)) if losses else 0.0
    print(f'  CLOSED TRADES  {closed}   win rate {wr:.0f}%  ({len(wins)}W / {len(losses)}L)')
    print(f'                 avg win {fmt_money(avg_w)}   avg loss {fmt_money(avg_l)}')
    if closed:
        print()
        print(f"    {'coin':10}{'sleeve':10}{'entry':>12}{'exit':>12}{'P&L':>10}{'%':>8}  closed")
        for r in sorted((r for r in realized if not r.get('orphan')),
                        key=lambda r: -r['closed'])[:12]:
            base = r['symbol'][:-4] if r['symbol'].endswith('USDT') else r['symbol']
            rpct = ((r['exit'] / r['entry'] - 1) * 100) if r['entry'] else 0.0
            when = dt.datetime.fromtimestamp(r['closed'] / 1000, dt.timezone.utc)
            print(f"    {base:10}{r['sleeve']:10}{r['entry']:>12,.4f}{r['exit']:>12,.4f}"
                  f"{r['pnl']:>+10,.2f}{rpct:>+8.1f}  {when:%m-%d %H:%M}")
    orphans = [r for r in realized if r.get('orphan')]
    if orphans:
        print()
        print(f'  !! {len(orphans)} tagged sell(s) with no matching tagged buy — '
              'the ledger may be missing older fills.')
    print('=' * 62)
    print()


if __name__ == '__main__':
    main()
