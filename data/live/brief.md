# v9 brief - 2026-11-04 19:06 UTC (signal from the 2026-11-04 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-19.10 (-9.6% of budget); from peak $-23.09

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -1.02 | 1.393 | +3.6% | +0.00 | +0.00 | -0.0003% |
| ETHUSDT | -3.44 | 1.921 | +5.6% | +169.88 | +169.22 | +0.0067% |
| SOLUSDT | 0.37 | 2.786 | +2.5% | +0.00 | +0.00 | +0.0062% |
| BNBUSDT | -0.73 | 2.338 | +2.9% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | -1.36 | 2.336 | +2.1% | +0.00 | +0.00 | -0.0038% |
| DOGEUSDT | -0.02 | 2.546 | +2.1% | +0.00 | +0.00 | +0.0009% |
| ADAUSDT | -0.1 | 1.903 | +3.4% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | 0.81 | 1.875 | +3.8% | +0.00 | +0.00 | +0.0100% |
| LINKUSDT | 0.91 | 1.772 | +3.7% | +0.00 | -115.67 | +0.0046% |
| LTCUSDT | -2.56 | 1.571 | +3.5% | +151.99 | +0.00 | +0.0100% |
| TRXUSDT | -0.63 | 1.124 | -1.1% | +0.00 | +0.00 | +0.0048% |
| DOTUSDT | -0.43 | 1.637 | +2.9% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
