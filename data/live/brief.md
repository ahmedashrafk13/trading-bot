# v9 brief - 2026-11-22 12:11 UTC (signal from the 2026-11-22 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $+5.22 (+2.6% of budget); from peak $-8.88

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -0.52 | 2.309 | +4.9% | +0.00 | +0.00 | +0.0018% |
| ETHUSDT | -2.12 | 1.935 | +3.4% | +126.22 | +119.86 | +0.0024% |
| SOLUSDT | 0.49 | 3.448 | +2.6% | +0.00 | +0.00 | +0.0100% |
| BNBUSDT | -1.23 | 2.372 | +4.3% | +0.00 | +0.00 | +0.0065% |
| XRPUSDT | -0.47 | 2.733 | +2.8% | +0.00 | +0.00 | +0.0063% |
| DOGEUSDT | -1.63 | 2.292 | +3.1% | +127.06 | +127.11 | +0.0004% |
| ADAUSDT | 1.9 | 2.306 | +3.9% | -111.67 | -111.84 | +0.0054% |
| AVAXUSDT | -0.31 | 1.645 | +4.0% | +0.00 | +0.00 | -0.0084% |
| LINKUSDT | -0.34 | 1.735 | +4.1% | +0.00 | +0.00 | +0.0005% |
| LTCUSDT | -0.24 | 1.958 | +2.0% | +0.00 | +0.00 | -0.0028% |
| TRXUSDT | 0.37 | 1.203 | +0.7% | +0.00 | +0.00 | -0.0036% |
| DOTUSDT | 0.54 | 1.662 | +2.4% | +0.00 | +0.00 | +0.0068% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
