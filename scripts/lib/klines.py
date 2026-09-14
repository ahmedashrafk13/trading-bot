"""Flatten one Bybit /v5/market/kline response to {'symbol', 'closes'} NDJSON.

Usage: python klines.py <SYMBOL> <kline.json>

Bybit returns klines NEWEST FIRST — index 0 is the most recent bar, the reverse
of Alpaca. Every indicator downstream assumes chronological order, so the
reversal happens HERE, once, rather than being re-derived (and eventually got
wrong) at each call site. Getting this backwards does not error; it silently
inverts every momentum number.

Kline row layout: [startTime, open, high, low, close, volume, turnover]
"""
import json
import sys

CLOSE_IDX = 4


def main() -> None:
    sym, path = sys.argv[1], sys.argv[2]
    data = json.load(open(path, encoding='utf-8'))
    rows = (data.get('result') or {}).get('list') or []
    rows = list(reversed(rows))

    closes = []
    for row in rows:
        try:
            closes.append(float(row[CLOSE_IDX]))
        except (TypeError, ValueError, IndexError):
            continue

    print(json.dumps({'symbol': sym, 'closes': closes}))


if __name__ == '__main__':
    main()
