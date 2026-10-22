# v9 brief - 2026-10-22 12:13 UTC (signal from the 2026-10-22 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-21.32 (-10.7% of budget); from peak $-25.31

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.58 | 1.82 | -2.1% | -172.76 | +0.00 | -0.0006% |
| ETHUSDT | 1.35 | 3.167 | -2.8% | +0.00 | +0.00 | -0.0062% |
| SOLUSDT | 1.56 | 2.697 | -2.3% | -98.30 | +0.00 | -0.0014% |
| BNBUSDT | 1.66 | 2.609 | -1.9% | -150.09 | +0.00 | -0.0145% |
| XRPUSDT | 0.53 | 2.619 | -2.2% | +0.00 | +0.00 | +0.0002% |
| DOGEUSDT | 1.26 | 2.676 | -3.4% | +0.00 | +0.00 | -0.0031% |
| ADAUSDT | -0.8 | 1.924 | -4.1% | +0.00 | +0.00 | -0.0182% |
| AVAXUSDT | -1.69 | 1.414 | -4.9% | +58.85 | +96.03 | -0.0044% |
| LINKUSDT | -0.0 | 1.684 | -2.8% | +0.00 | +0.00 | -0.0019% |
| LTCUSDT | 0.33 | 2.209 | -3.7% | +0.00 | +124.55 | +0.0016% |
| TRXUSDT | -0.92 | 1.079 | -0.1% | +0.00 | +0.00 | +0.0082% |
| DOTUSDT | -0.8 | 1.724 | -2.4% | +0.00 | +0.00 | -0.0027% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
