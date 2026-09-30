# v9 brief - 2026-09-30 12:12 UTC (signal from the 2026-09-30 12:00 bar close)

Budget $200 | vol target 0.55 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-8.11 (-4.1% of budget); from peak $-8.49

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.46 | 1.343 | -0.5% | +0.00 | +0.00 | +0.0041% |
| ETHUSDT | 0.31 | 2.674 | -1.3% | +0.00 | +0.00 | +0.0098% |
| SOLUSDT | -0.69 | 1.752 | -0.5% | +0.00 | +0.00 | +0.0100% |
| BNBUSDT | -0.93 | 2.094 | +0.4% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | 1.24 | 2.54 | -0.1% | +0.00 | +0.00 | +0.0100% |
| DOGEUSDT | -0.29 | 2.392 | +0.1% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | 0.21 | 2.105 | -2.1% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | 1.75 | 2.802 | -5.9% | -53.26 | -52.30 | -0.0002% |
| LINKUSDT | 2.27 | 2.154 | -6.0% | -64.45 | -63.43 | -0.0086% |
| LTCUSDT | -0.15 | 2.333 | -2.0% | +0.00 | +0.00 | +0.0069% |
| TRXUSDT | -0.6 | 1.103 | +1.5% | +0.00 | +0.00 | +0.0100% |
| DOTUSDT | -0.05 | 2.008 | +0.4% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
