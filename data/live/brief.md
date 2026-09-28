# v9 brief - 2026-09-28 18:13 UTC (signal from the 2026-09-28 18:00 bar close)

Budget $200 | vol target 0.55 | gross cap 2.4x | leverage 5x | stop 8%

RISK: P&L since v9 start $-9.42 (-4.7% of budget); from peak $-9.80

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.56 | 1.355 | -0.8% | +0.00 | +0.00 | +0.0045% |
| ETHUSDT | -0.04 | 2.569 | +0.2% | +0.00 | +0.00 | +0.0100% |
| SOLUSDT | -0.39 | 1.827 | -1.9% | +0.00 | +0.00 | +0.0100% |
| BNBUSDT | -0.93 | 2.103 | -1.0% | +0.00 | +0.00 | +0.0044% |
| XRPUSDT | 0.82 | 2.486 | -1.1% | +0.00 | +0.00 | +0.0100% |
| DOGEUSDT | 0.21 | 2.49 | -2.5% | +0.00 | +0.00 | +0.0032% |
| ADAUSDT | 0.58 | 2.183 | -2.3% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | 0.4 | 2.281 | -4.2% | +0.00 | +0.00 | -0.0026% |
| LINKUSDT | 2.0 | 2.007 | +7.3% | -67.89 | +0.00 | +0.0100% |
| LTCUSDT | 1.11 | 2.632 | -2.4% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | -0.61 | 1.112 | +0.4% | +0.00 | +0.00 | -0.0252% |
| DOTUSDT | -0.63 | 1.874 | -4.7% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
