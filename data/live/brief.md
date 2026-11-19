# v9 brief - 2026-11-19 16:33 UTC (signal from the 2026-11-19 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-1.84 (-0.9% of budget); from peak $-5.83

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.33 | 2.623 | -0.4% | +0.00 | +0.00 | +0.0100% |
| ETHUSDT | -1.72 | 2.205 | +0.4% | +164.81 | +0.00 | -0.0011% |
| SOLUSDT | 0.29 | 3.316 | +0.5% | +0.00 | +0.00 | -0.0113% |
| BNBUSDT | -0.7 | 2.467 | +0.5% | +0.00 | +0.00 | -0.0018% |
| XRPUSDT | 0.44 | 2.925 | +0.1% | +0.00 | +0.00 | -0.0055% |
| DOGEUSDT | -1.24 | 2.397 | +0.5% | +0.00 | +0.00 | -0.0033% |
| ADAUSDT | 1.42 | 2.129 | +0.7% | +0.00 | -141.46 | -0.0091% |
| AVAXUSDT | -0.42 | 1.599 | -0.1% | +0.00 | +0.00 | -0.0397% |
| LINKUSDT | -0.07 | 1.75 | +0.5% | +0.00 | +0.00 | -0.0060% |
| LTCUSDT | -0.02 | 1.99 | +0.8% | +0.00 | +0.00 | -0.0003% |
| TRXUSDT | 1.94 | 1.38 | +0.9% | -244.18 | -241.34 | -0.0327% |
| DOTUSDT | 0.83 | 1.764 | -0.9% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
