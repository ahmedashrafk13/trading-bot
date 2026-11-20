# v9 brief - 2026-11-20 16:00 UTC (signal from the 2026-11-20 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $+14.10 (+7.0% of budget); from peak $+0.00

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.94 | 3.093 | -3.3% | +0.00 | +0.00 | +0.0100% |
| ETHUSDT | -1.06 | 2.487 | -3.2% | +0.00 | +0.00 | +0.0100% |
| SOLUSDT | 1.03 | 3.604 | -4.1% | +0.00 | +0.00 | +0.0100% |
| BNBUSDT | 0.16 | 2.613 | -3.8% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | 0.64 | 2.986 | -3.7% | +0.00 | +0.00 | +0.0100% |
| DOGEUSDT | -0.55 | 2.495 | -4.6% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | 3.12 | 2.463 | -4.5% | -143.00 | -130.85 | +0.0100% |
| AVAXUSDT | -0.47 | 1.595 | -3.5% | +0.00 | +0.00 | +0.0100% |
| LINKUSDT | 0.16 | 1.786 | -4.5% | +0.00 | +0.00 | +0.0100% |
| LTCUSDT | -0.36 | 1.932 | -7.2% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | 1.31 | 1.314 | -1.9% | +0.00 | -235.95 | +0.0100% |
| DOTUSDT | 0.99 | 1.75 | -3.2% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
