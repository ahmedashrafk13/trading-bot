# v9 brief - 2026-10-06 00:27 UTC (signal from the 2026-10-06 00:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-7.42 (-3.7% of budget); from peak $-7.81

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -0.67 | 1.086 | -0.9% | +0.00 | +0.00 | +0.0086% |
| ETHUSDT | -0.42 | 2.495 | -0.6% | +0.00 | +0.00 | +0.0091% |
| SOLUSDT | -0.76 | 1.697 | -0.7% | +0.00 | +0.00 | +0.0100% |
| BNBUSDT | -0.39 | 2.196 | -1.1% | +0.00 | +0.00 | -0.0079% |
| XRPUSDT | -1.46 | 2.211 | -0.9% | +0.00 | +0.00 | +0.0100% |
| DOGEUSDT | 0.77 | 2.631 | -0.5% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | 1.25 | 2.458 | +4.0% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | -1.4 | 1.857 | +0.2% | +0.00 | +0.00 | +0.0100% |
| LINKUSDT | -0.08 | 1.678 | -2.9% | +0.00 | +0.00 | -0.0132% |
| LTCUSDT | -1.19 | 2.09 | -0.9% | +0.00 | +0.00 | +0.0013% |
| TRXUSDT | -0.26 | 1.194 | +0.1% | +0.00 | +0.00 | -0.0425% |
| DOTUSDT | -1.09 | 1.729 | +2.1% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
