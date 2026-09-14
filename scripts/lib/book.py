"""The $200 virtual book: isolate the bot's own trades from the account.

The Bybit demo account is NOT a $200 account. It ships with ~$181k of equity,
leftover coin balances, stale resting orders and an open perp position from
prior use, and demo funds can only be ADDED (adjustType 0), never withdrawn --
so the account can never be shrunk to $200.

Every bot order therefore carries an orderLinkId prefixed with BOT_TAG, and all
accounting here counts ONLY tagged fills. The pre-existing clutter is invisible
to the book. This is also what makes "how am I doing on $200?" answerable at
all: account equity is meaningless as a denominator, so every equity-relative
rule (fee budget, circuit breaker, deployment %) is measured against BOOK_SIZE.

Consequence worth stating plainly: an untagged manual trade placed in the Bybit
UI will NOT appear in the book. That is deliberate -- the book measures the bot.
"""
import json
import os
import time
from pathlib import Path

BOT_TAG = os.environ.get('BOT_TAG', 'tb')
BOOK_SIZE = float(os.environ.get('BOOK_SIZE', '200'))
LEDGER = Path('memory/LEDGER.json')

# Bybit spot sells deduct fee in the QUOTE coin (USDT) and buys deduct it in the
# BASE coin. Netting that correctly matters at $20 clip sizes, where a
# mis-signed fee is a meaningful share of the edge.


def new_link_id(sleeve: str, symbol: str) -> str:
    """Build the orderLinkId every bot order must carry."""
    return f'{BOT_TAG}-{sleeve[:3].lower()}-{symbol}-{int(time.time() * 1000)}'


def is_bot(fill: dict) -> bool:
    return str(fill.get('orderLinkId') or '').startswith(BOT_TAG + '-')


def sleeve_of(fill: dict) -> str:
    """Recover the sleeve from the link id: tb-<sleeve>-<symbol>-<ts>."""
    parts = str(fill.get('orderLinkId') or '').split('-')
    if len(parts) >= 2:
        return {'cor': 'CORE', 'tac': 'TACTICAL'}.get(parts[1], '?')
    return '?'


def load_ledger() -> dict:
    if LEDGER.exists():
        led = json.loads(LEDGER.read_text(encoding='utf-8'))
        led.setdefault('fills', {})
        return led
    return {'fills': {}, 'epoch_ms': 0}


def reset_ledger() -> dict:
    """Start a fresh $200 run from now: drop every fill and move the epoch."""
    led = {'fills': {}, 'epoch_ms': int(time.time() * 1000)}
    save_ledger(led)
    return led


def save_ledger(led: dict) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    # newline='' — Windows text mode would otherwise write CRLF into a file that
    # git and the cloud runs both read; see scripts/lib/universe.py for the
    # same trap biting a symbol list.
    with open(LEDGER, 'w', encoding='utf-8', newline='') as fh:
        json.dump(led, fh, indent=2, sort_keys=True)
        fh.write('\n')


def epoch_ms(led: dict) -> int:
    """Fills before this timestamp are not part of the book.

    Deleting LEDGER.json is NOT a reset: the next run re-fetches the same fills
    from /v5/execution/list and they reappear. The epoch is the actual start
    line — set it with `bash scripts/pnl.sh --reset` to begin a clean $200 run.
    """
    return int(led.get('epoch_ms') or 0)


def merge_fills(led: dict, fills: list) -> int:
    """Add new tagged fills to the ledger, deduped by execId. Returns count added.

    The ledger is persisted because /v5/execution/list has a retention window;
    once a fill ages out of the API it must still count toward the book's
    realized P&L, or the performance number silently improves over time.
    """
    added = 0
    start = epoch_ms(led)
    for f in fills:
        if not is_bot(f):
            continue
        if start and int(f.get('execTime') or 0) < start:
            continue
        eid = f.get('execId')
        if not eid or eid in led['fills']:
            continue
        led['fills'][eid] = {
            'symbol': f.get('symbol'),
            'side': f.get('side'),
            'qty': float(f.get('execQty') or 0),
            'price': float(f.get('execPrice') or 0),
            'fee': float(f.get('execFee') or 0),
            'feeCoin': f.get('feeCurrency') or '',
            'ts': int(f.get('execTime') or 0),
            'linkId': f.get('orderLinkId'),
            'sleeve': sleeve_of(f),
        }
        added += 1
    return added


def build_positions(led: dict):
    """FIFO-match the tagged fills into open lots and realized trades.

    Returns (open_positions, realized_trades, total_fees_usdt).
    """
    fills = sorted(led['fills'].values(), key=lambda f: f['ts'])
    lots: dict[str, list] = {}       # symbol -> [[qty, cost_per_unit, ts, sleeve]]
    realized = []
    fees_usdt = 0.0

    for f in fills:
        sym, qty, px = f['symbol'], f['qty'], f['price']
        if qty <= 0:
            continue
        fee = f['fee']
        # A buy's fee is charged in the BASE coin, so convert at the fill price
        # to keep every fee figure in one unit (USDT).
        fee_usdt = fee * px if (f['side'] == 'Buy' and f['feeCoin'] not in ('USDT', '')) else fee
        fees_usdt += fee_usdt

        if f['side'] == 'Buy':
            # The buy fee is deducted in the BASE coin, so the wallet receives
            # LESS than execQty. Booking execQty would overstate the position and
            # make any "sell everything" order fail with 170131 Insufficient
            # balance — measured: bought 6.936737 XRP, wallet held 6.92980022.
            # Entry stays the RAW fill price and the fee is counted once, in
            # fees_usdt. That keeps the identity cost + fees == USDT actually
            # spent: cost = (qty-fee)*px, fees = fee*px, sum = qty*px. Folding
            # the fee into the entry price instead would double-count it, since
            # net P&L already subtracts fees separately.
            recv = qty - fee if f['feeCoin'] not in ('USDT', '') else qty
            lots.setdefault(sym, []).append([recv, px, f['ts'], f['sleeve']])
        else:
            remaining = qty
            queue = lots.get(sym, [])
            while remaining > 1e-12 and queue:
                lot = queue[0]
                take = min(remaining, lot[0])
                pnl = (px - lot[1]) * take
                realized.append({
                    'symbol': sym, 'qty': take, 'entry': lot[1], 'exit': px,
                    'pnl': pnl, 'opened': lot[2], 'closed': f['ts'],
                    'sleeve': lot[3],
                })
                lot[0] -= take
                remaining -= take
                if lot[0] <= 1e-12:
                    queue.pop(0)
            # A sell with no matching buy means the bot sold something it never
            # bought under its own tag. Surface it rather than silently dropping
            # the proceeds, which would understate the book.
            if remaining > 1e-9:
                realized.append({
                    'symbol': sym, 'qty': remaining, 'entry': float('nan'),
                    'exit': px, 'pnl': 0.0, 'opened': None, 'closed': f['ts'],
                    'sleeve': f['sleeve'], 'orphan': True,
                })

    open_positions = []
    for sym, queue in lots.items():
        tot_qty = sum(l[0] for l in queue)
        if tot_qty <= 1e-12:
            continue
        cost = sum(l[0] * l[1] for l in queue)
        open_positions.append({
            'symbol': sym,
            'qty': tot_qty,
            'avg_entry': cost / tot_qty,
            'cost': cost,
            'opened': min(l[2] for l in queue),
            'sleeve': queue[0][3],
        })

    return open_positions, realized, fees_usdt
