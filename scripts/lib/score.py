"""Score the screened universe and print the per-sleeve shortlist.

Usage: FORMAT=table SLEEVE=core IV=D python score.py <bars.ndjson> <tickers.json>

Thresholds here mirror memory/TRADING-STRATEGY.md. They are TIGHTER than the
Alpaca originals on spread for one reason: Bybit quotes far more pairs, and the
long tail is where a $200 book gets quietly bled. Alpaca's 1.0%/0.5% spread caps
were generous because Alpaca only listed ~20 deeply liquid coins; applied to
Bybit's 397 USDT pairs they would wave through names whose round-trip friction
alone exceeds the tactical target.
"""
import json
import os
import statistics as st
import sys

# Meme basket. Memes are allowed ONLY in the TACTICAL sleeve, and only when they
# clear the same spread/turnover bar as anything else. Measured on Bybit spot,
# most meme pairs run 0.04-0.31% spreads against a ~$3.00/week fee budget, so a
# meme-focused book would exhaust that budget in a handful of round trips.
MEMES = {
    'DOGE', 'SHIB', 'PEPE', 'WIF', 'BONK', 'FLOKI', 'MEME', 'POPCAT', 'MEW',
    'BRETT', 'TURBO', 'NEIRO', 'GOAT', 'PNUT', 'ACT', 'MOODENG', 'CHILLGUY',
    'FARTCOIN', 'SPX', 'TRUMP', 'BOME', 'MYRO', 'SLERF', 'DEGEN', 'TOSHI',
    'MOG', 'BABYDOGE', 'LADYS', 'WEN', 'AIDOGE', 'PEOPLE', 'COQ',
}

CORE_MIN_TURNOVER = 20_000_000
TAC_MIN_TURNOVER = 5_000_000
CORE_MAX_SPREAD = 0.10
TAC_MAX_SPREAD = 0.15


def score_row(sym, closes, tick):
    """Return a scored dict, or None if there is not enough history to judge."""
    if len(closes) < 21:
        return None

    base = sym[:-4]
    last = closes[-1]
    sma20 = sum(closes[-20:]) / 20
    prev_sma20 = sum(closes[-21:-1]) / 20
    sma_rising = sma20 > prev_sma20

    rets = [closes[i] / closes[i - 1] - 1
            for i in range(1, len(closes)) if closes[i - 1]]
    vol = st.pstdev(rets[-14:]) * 100 if len(rets) >= 14 else float('nan')
    m7 = (last / closes[-8] - 1) * 100 if len(closes) > 8 else float('nan')
    m30 = (last / closes[-31] - 1) * 100 if len(closes) > 31 else float('nan')
    dsma = (last / sma20 - 1) * 100 if sma20 else float('nan')

    bid = float(tick.get('bid1Price') or 0)
    ask = float(tick.get('ask1Price') or 0)
    spread = ((ask - bid) / ((ask + bid) / 2) * 100) if (ask and bid) else float('nan')
    turnover = float(tick.get('turnover24h') or 0)
    is_meme = base in MEMES

    # --- CORE (daily bars): an established uptrend, priced above a RISING
    # SMA20, not yet extended. Demanding a rising SMA and dsma>0 is what makes
    # this selective. Memes are structurally excluded: the sleeve holds for
    # weeks to months with a 20% trailing stop, and a meme has no valuation
    # floor to hold through that drawdown.
    core_why = []
    if not (m30 > 0):
        core_why.append('30p<=0')
    if not (dsma > 0):
        core_why.append('below SMA20')
    if not sma_rising:
        core_why.append('SMA20 falling')
    if not (dsma <= 20):
        core_why.append('>20% over SMA20')
    if not (spread <= CORE_MAX_SPREAD):
        core_why.append(f'spread>{CORE_MAX_SPREAD}%')
    if turnover < CORE_MIN_TURNOVER:
        core_why.append('turnover<$20M')
    if is_meme:
        core_why.append('meme: tactical-only')

    # --- TACTICAL (hourly bars): a short-horizon push that is not yet extended,
    # with enough movement to reach the target and a spread cheap enough that
    # the round-trip friction does not eat the edge.
    tac_why = []
    if not (m7 > 0):
        tac_why.append('short-mom<=0')
    if not (-8 <= dsma <= 8):
        tac_why.append('too far from SMA20')
    if not (0.4 <= vol <= 6.0):
        tac_why.append('vol outside band')
    if not (spread <= TAC_MAX_SPREAD):
        tac_why.append(f'spread>{TAC_MAX_SPREAD}%')
    if turnover < TAC_MIN_TURNOVER:
        tac_why.append('turnover<$5M')

    return dict(symbol=sym, base=base, last=last, m7=m7, m30=m30, dsma=dsma,
                vol=vol, spread=spread, turnover=turnover, meme=is_meme,
                sma20_rising=sma_rising,
                core_pass=not core_why, core_fail=core_why,
                tactical_pass=not tac_why, tactical_fail=tac_why)


def main() -> None:
    fmt = os.environ.get('FORMAT', 'table')
    sleeve = os.environ.get('SLEEVE', 'core')
    iv = os.environ.get('IV', 'D')

    tick = {x['symbol']: x for x in
            json.load(open(sys.argv[2], encoding='utf-8'))['result']['list']}

    rows, dropped = [], []
    for line in open(sys.argv[1], encoding='utf-8'):
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        scored = score_row(rec['symbol'], rec['closes'], tick.get(rec['symbol'], {}))
        if scored is None:
            dropped.append(rec['symbol'])
        else:
            rows.append(scored)

    if dropped:
        print(f'WARNING: {len(dropped)} coin(s) skipped for <21 periods of history: '
              + ' '.join(sorted(s[:-4] for s in dropped)), file=sys.stderr)

    rows.sort(key=lambda r: (r['m7'] if r['m7'] == r['m7'] else -999), reverse=True)

    if fmt == 'json':
        print(json.dumps(rows, indent=2))
        return

    print(f'UNIVERSE SCREEN [{iv}] — {len(rows)} coins with >=21 periods   (M = meme)')
    print(f"{'coin':11}{'last':>12}{'7p%':>8}{'30p%':>8}{'vsSMA20':>9}"
          f"{'vol%':>7}{'spr%':>7}{'24h$M':>8}  {'CORE':<6}{'TACTICAL':<9}")
    print('-' * 96)
    for r in rows:
        core = 'PASS' if r['core_pass'] else 'fail'
        tac = 'PASS' if r['tactical_pass'] else 'fail'
        tag = ('M ' if r['meme'] else '  ') + r['base']
        print(f"{tag:11}{r['last']:>12,.4f}{r['m7']:>8.1f}{r['m30']:>8.1f}"
              f"{r['dsma']:>9.1f}{r['vol']:>7.1f}{r['spread']:>7.3f}"
              f"{r['turnover'] / 1e6:>8.1f}  {core:<6}{tac:<9}")
    print()

    key = 'core_pass' if sleeve == 'core' else 'tactical_pass'
    passes = [r for r in rows if r[key]]
    label = ' '.join(('M:' if r['meme'] else '') + r['base'] for r in passes) or '(none)'
    print(f'{sleeve.upper()} SHORTLIST ({len(passes)}): {label}')


if __name__ == '__main__':
    main()
