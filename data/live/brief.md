# v9 brief - 2026-10-09 00:21 UTC (signal from the 2026-10-09 00:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-4.17 (-2.1% of budget); from peak $-4.55

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.85 | 1.869 | -1.9% | -97.75 | -81.71 | +0.0100% |
| ETHUSDT | 1.98 | 3.363 | -3.8% | -73.52 | -74.24 | +0.0064% |
| SOLUSDT | 1.66 | 2.337 | -5.7% | -57.11 | -65.39 | -0.0043% |
| BNBUSDT | 1.64 | 2.561 | -4.8% | -88.30 | +0.00 | -0.0288% |
| XRPUSDT | 1.59 | 2.648 | -2.9% | -48.30 | -60.49 | -0.0232% |
| DOGEUSDT | -0.35 | 2.4 | -5.6% | +0.00 | +0.00 | -0.0196% |
| ADAUSDT | -0.03 | 2.143 | -9.1% | +0.00 | +0.00 | -0.0495% |
| AVAXUSDT | -0.9 | 1.982 | -9.5% | +0.00 | +0.00 | -0.0259% |
| LINKUSDT | -0.34 | 1.602 | -4.6% | +0.00 | +0.00 | -0.0057% |
| LTCUSDT | -0.79 | 2.106 | -4.4% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | -0.26 | 1.201 | -0.8% | +0.00 | +0.00 | +0.0088% |
| DOTUSDT | -1.75 | 1.569 | -2.4% | +35.02 | +48.58 | -0.0300% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
