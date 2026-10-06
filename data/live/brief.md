# v9 brief - 2026-10-06 13:11 UTC (signal from the 2026-10-06 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-7.42 (-3.7% of budget); from peak $-7.81

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -0.99 | 1.02 | +0.1% | +0.00 | +0.00 | +0.0072% |
| ETHUSDT | -0.58 | 2.452 | -0.1% | +0.00 | +0.00 | +0.0073% |
| SOLUSDT | -0.53 | 1.745 | -0.4% | +0.00 | +0.00 | +0.0068% |
| BNBUSDT | -0.11 | 2.249 | -0.9% | +0.00 | +0.00 | +0.0099% |
| XRPUSDT | -1.88 | 2.153 | -0.3% | +140.09 | +0.00 | +0.0100% |
| DOGEUSDT | 0.27 | 2.521 | -0.6% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | 1.19 | 2.454 | +2.5% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | -0.43 | 2.128 | +3.8% | +0.00 | +0.00 | +0.0100% |
| LINKUSDT | -0.49 | 1.593 | -1.0% | +0.00 | +0.00 | -0.0001% |
| LTCUSDT | -1.71 | 1.97 | -0.6% | +136.93 | +0.00 | +0.0073% |
| TRXUSDT | -0.09 | 1.224 | -0.3% | +0.00 | +0.00 | -0.0268% |
| DOTUSDT | -0.48 | 1.857 | +1.4% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
