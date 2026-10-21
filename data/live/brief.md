# v9 brief - 2026-10-21 00:24 UTC (signal from the 2026-10-21 00:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-5.80 (-2.9% of budget); from peak $-9.79

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.59 | 1.497 | +1.3% | +0.00 | +0.00 | +0.0100% |
| ETHUSDT | -0.13 | 2.736 | +1.7% | +0.00 | +0.00 | +0.0100% |
| SOLUSDT | 1.36 | 2.545 | +1.4% | +0.00 | +0.00 | +0.0005% |
| BNBUSDT | 0.77 | 2.414 | +1.3% | +0.00 | -252.48 | +0.0100% |
| XRPUSDT | 0.14 | 2.527 | +2.5% | +0.00 | +0.00 | +0.0064% |
| DOGEUSDT | 0.89 | 2.627 | +2.6% | +0.00 | +0.00 | -0.0069% |
| ADAUSDT | -1.15 | 1.865 | +2.7% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | -1.94 | 1.408 | +1.5% | +101.10 | +101.65 | +0.0100% |
| LINKUSDT | -0.93 | 1.532 | +2.2% | +0.00 | +0.00 | -0.0115% |
| LTCUSDT | -0.53 | 2.037 | +3.1% | +0.00 | +0.00 | -0.0089% |
| TRXUSDT | -0.08 | 1.189 | -0.2% | +0.00 | +0.00 | +0.0085% |
| DOTUSDT | 1.22 | 2.193 | -0.1% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
