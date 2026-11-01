# v9 brief - 2026-11-01 12:12 UTC (signal from the 2026-11-01 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-25.18 (-12.6% of budget); from peak $-29.17

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.33 | 2.353 | +0.5% | +0.00 | -233.75 | +0.0100% |
| ETHUSDT | -1.3 | 2.595 | +1.0% | +0.00 | +0.00 | -0.0026% |
| SOLUSDT | 1.49 | 3.264 | -0.6% | +0.00 | +0.00 | +0.0100% |
| BNBUSDT | 0.92 | 2.631 | +1.2% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | -0.63 | 2.5 | +0.4% | +0.00 | +0.00 | -0.0058% |
| DOGEUSDT | -0.19 | 2.507 | +0.7% | +0.00 | +0.00 | +0.0075% |
| ADAUSDT | -0.51 | 1.847 | +0.5% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | -0.28 | 1.634 | +4.0% | +0.00 | +0.00 | +0.0100% |
| LINKUSDT | 2.3 | 1.889 | +2.1% | -113.50 | -112.14 | +0.0100% |
| LTCUSDT | 0.69 | 2.132 | +2.1% | +0.00 | +0.00 | +0.0088% |
| TRXUSDT | -0.79 | 1.109 | -3.0% | +0.00 | +0.00 | +0.0055% |
| DOTUSDT | -1.57 | 1.394 | -0.5% | +85.89 | +68.53 | -0.0057% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
