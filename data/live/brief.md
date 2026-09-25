# v9 brief - 2026-09-25 18:12 UTC (signal from the 2026-09-25 18:00 bar close)

Budget $200 | vol target 0.55 | gross cap 2.4x | leverage 5x | stop 8%

RISK: P&L since v9 start $-1.66 (-0.8% of budget); from peak $-1.66

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.46 | 1.305 | -0.4% | +0.00 | +0.00 | +0.0022% |
| ETHUSDT | 0.48 | 2.689 | +0.6% | +0.00 | +0.00 | +0.0024% |
| SOLUSDT | -2.01 | 1.508 | +3.6% | +82.87 | +0.00 | +0.0100% |
| BNBUSDT | -0.93 | 2.145 | -0.7% | +0.00 | +0.00 | +0.0016% |
| XRPUSDT | -0.48 | 2.332 | +2.4% | +0.00 | +0.00 | +0.0100% |
| DOGEUSDT | 1.09 | 2.693 | +1.2% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | 1.99 | 2.488 | +3.3% | -67.24 | -70.06 | +0.0100% |
| AVAXUSDT | -0.19 | 2.088 | +1.2% | +0.00 | +0.00 | +0.0027% |
| LINKUSDT | 0.95 | 1.738 | +6.9% | +0.00 | +0.00 | +0.0100% |
| LTCUSDT | 0.49 | 2.451 | -2.6% | +0.00 | +0.00 | +0.0059% |
| TRXUSDT | -0.73 | 1.112 | -0.9% | +0.00 | +0.00 | -0.0318% |
| DOTUSDT | -1.55 | 1.68 | +1.0% | +49.27 | +50.33 | +0.0031% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
