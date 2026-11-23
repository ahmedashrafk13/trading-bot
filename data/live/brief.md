# v9 brief - 2026-11-23 06:13 UTC (signal from the 2026-11-23 06:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $+7.04 (+3.5% of budget); from peak $-7.06

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -1.05 | 2.077 | +4.7% | +0.00 | +0.00 | +0.0051% |
| ETHUSDT | -2.07 | 1.879 | +4.5% | +126.22 | +120.97 | -0.0036% |
| SOLUSDT | 0.76 | 3.541 | +4.2% | +0.00 | +0.00 | -0.0046% |
| BNBUSDT | -0.93 | 2.424 | +4.1% | +0.00 | +0.00 | +0.0072% |
| XRPUSDT | -0.77 | 2.664 | +2.9% | +0.00 | +0.00 | +0.0000% |
| DOGEUSDT | -1.93 | 2.228 | +3.3% | +127.06 | +127.69 | +0.0100% |
| ADAUSDT | 1.44 | 2.239 | +3.1% | +0.00 | -111.77 | -0.0062% |
| AVAXUSDT | -0.17 | 1.682 | +3.1% | +0.00 | +0.00 | -0.0042% |
| LINKUSDT | 0.44 | 1.83 | +5.0% | +0.00 | +0.00 | -0.0004% |
| LTCUSDT | -0.27 | 1.952 | +4.5% | +0.00 | +0.00 | +0.0015% |
| TRXUSDT | 0.58 | 1.23 | +0.5% | +0.00 | +0.00 | -0.0035% |
| DOTUSDT | 0.77 | 1.675 | +3.9% | +0.00 | +0.00 | +0.0091% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
