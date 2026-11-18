# v9 brief - 2026-11-18 18:12 UTC (signal from the 2026-11-18 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-3.42 (-1.7% of budget); from peak $-7.41

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.43 | 3.403 | -1.1% | +0.00 | +0.00 | +0.0023% |
| ETHUSDT | -0.15 | 2.956 | -1.1% | +0.00 | +0.00 | -0.0013% |
| SOLUSDT | 1.0 | 3.572 | +1.7% | +0.00 | +0.00 | +0.0097% |
| BNBUSDT | 0.18 | 2.613 | -0.6% | +0.00 | +0.00 | +0.0066% |
| XRPUSDT | 0.63 | 2.963 | +2.1% | +0.00 | +0.00 | +0.0038% |
| DOGEUSDT | -0.86 | 2.459 | +0.3% | +0.00 | +0.00 | -0.0062% |
| ADAUSDT | 2.3 | 2.238 | -0.1% | -138.97 | -140.44 | -0.0253% |
| AVAXUSDT | -0.16 | 1.655 | -1.6% | +0.00 | +0.00 | -0.0100% |
| LINKUSDT | 0.3 | 1.792 | -0.5% | +0.00 | +0.00 | -0.0187% |
| LTCUSDT | 0.31 | 2.053 | -1.2% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | 0.86 | 1.246 | +0.7% | +0.00 | +0.00 | -0.0143% |
| DOTUSDT | 1.0 | 1.809 | -1.5% | +0.00 | +0.00 | -0.0068% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
