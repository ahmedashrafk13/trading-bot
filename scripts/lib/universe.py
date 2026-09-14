"""Pick the tradable spot universe from a Bybit /v5/market/tickers dump.

Usage: TOP=60 python universe.py <tickers.json> <out.txt>

Writes one symbol per line, ranked by 24h turnover. The turnover ranking IS the
liquidity gate: klines cost one API call per symbol, so scoring all ~397 USDT
pairs is both slow and pointless — anything outside the top tier cannot absorb
even a $20 tactical clip without the spread eating the edge.
"""
import json
import os
import sys

# Stables and wrapped/staked majors are not trade candidates: a stable has no
# momentum by construction, and a wrapper just re-prices its underlying, so
# holding one is the same trade as holding the underlying with extra spread.
SKIP_BASE = {
    'USDC', 'USDT', 'USDE', 'FDUSD', 'TUSD', 'DAI', 'BUSD', 'USDD', 'PYUSD',
    'EURT', 'USDR', 'USD1', 'RLUSD',
    'WSTETH', 'STETH', 'WBETH', 'WBTC', 'SOLVBTC', 'BBSOL', 'JITOSOL', 'MSOL',
}


def main() -> None:
    src, dst = sys.argv[1], sys.argv[2]
    data = json.load(open(src, encoding='utf-8'))['result']['list']

    rows = []
    for x in data:
        sym = x['symbol']
        if not sym.endswith('USDT'):
            continue
        base = sym[:-4]
        if base in SKIP_BASE:
            continue
        try:
            turnover = float(x.get('turnover24h') or 0)
        except (TypeError, ValueError):
            continue
        if turnover <= 0:
            continue
        rows.append((sym, turnover))

    rows.sort(key=lambda r: -r[1])
    top = int(os.environ.get('TOP', '60'))
    picked = rows[:top]
    # newline='' is load-bearing on Windows: the default text mode rewrites
    # '\n' to '\r\n', and the bash `while read` loop downstream then hands curl
    # a symbol with a trailing CR -> "curl: (3) Malformed input to a URL
    # function" for EVERY symbol, i.e. a silently empty screen.
    with open(dst, 'w', encoding='utf-8', newline='') as fh:
        # Trailing newline matters too: `while read -r` discards a final line
        # that is not newline-terminated, which would drop the last symbol.
        for sym, _ in picked:
            fh.write(sym + '\n')
    print(
        f'universe: {len(rows)} live USDT pairs -> top {len(picked)} by 24h turnover',
        file=sys.stderr,
    )


if __name__ == '__main__':
    main()
