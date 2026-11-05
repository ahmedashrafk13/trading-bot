# v9 brief - 2026-11-05 15:54 UTC (signal from the 2026-11-05 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-44.17 (-22.1% of budget); from peak $-48.16

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -1.03 | 1.414 | +2.5% | +0.00 | +0.00 | +0.0100% |
| ETHUSDT | -2.86 | 1.955 | +4.0% | +169.88 | +156.52 | +0.0100% |
| SOLUSDT | 0.14 | 2.713 | +3.1% | +0.00 | +0.00 | +0.0000% |
| BNBUSDT | -0.51 | 2.388 | +2.1% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | -0.65 | 2.52 | +2.4% | +0.00 | +0.00 | +0.0100% |
| DOGEUSDT | 0.93 | 2.697 | +2.1% | +0.00 | +0.00 | +0.0033% |
| ADAUSDT | 0.93 | 2.079 | +3.3% | +0.00 | +0.00 | +0.0081% |
| AVAXUSDT | 1.18 | 1.974 | +0.9% | +0.00 | +0.00 | +0.0056% |
| LINKUSDT | 1.94 | 1.932 | +3.3% | -116.70 | +0.00 | +0.0100% |
| LTCUSDT | -0.86 | 1.821 | +1.8% | +0.00 | +139.13 | -0.0005% |
| TRXUSDT | -0.84 | 1.095 | -0.0% | +0.00 | +0.00 | -0.0248% |
| DOTUSDT | -0.51 | 1.612 | -1.0% | +0.00 | +0.00 | -0.0036% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
