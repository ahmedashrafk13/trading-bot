# v9 brief - 2026-10-04 10:20 UTC (signal from the 2026-10-04 06:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-7.26 (-3.6% of budget); from peak $-7.65

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -0.01 | 1.23 | +0.3% | +0.00 | +0.00 | +0.0065% |
| ETHUSDT | 0.56 | 2.769 | +0.6% | +0.00 | +0.00 | +0.0082% |
| SOLUSDT | -0.33 | 1.817 | +1.0% | +0.00 | +0.00 | +0.0100% |
| BNBUSDT | -0.55 | 2.15 | +2.6% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | -0.42 | 2.352 | +0.4% | +0.00 | -134.13 | +0.0100% |
| DOGEUSDT | 0.05 | 2.5 | -0.2% | +0.00 | +0.00 | +0.0023% |
| ADAUSDT | -0.38 | 2.007 | -0.9% | +0.00 | +0.00 | +0.0024% |
| AVAXUSDT | 0.59 | 2.463 | +1.7% | +0.00 | +0.00 | -0.0088% |
| LINKUSDT | 0.55 | 1.811 | +0.1% | +0.00 | +0.00 | +0.0077% |
| LTCUSDT | -0.96 | 2.166 | +2.1% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | -0.16 | 1.202 | +0.2% | +0.00 | +0.00 | -0.0283% |
| DOTUSDT | -1.07 | 1.754 | +3.1% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
