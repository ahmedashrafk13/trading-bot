# v9 brief - 2026-10-16 00:26 UTC (signal from the 2026-10-16 00:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $+0.80 (+0.4% of budget); from peak $-3.19

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.86 | 1.502 | +0.7% | +0.00 | +0.00 | +0.0019% |
| ETHUSDT | -0.27 | 2.639 | +0.8% | +0.00 | +0.00 | +0.0002% |
| SOLUSDT | 1.44 | 2.401 | +1.1% | +0.00 | -73.75 | +0.0041% |
| BNBUSDT | 1.94 | 2.531 | -0.1% | -223.74 | -123.94 | +0.0037% |
| XRPUSDT | 1.41 | 2.691 | +0.3% | +0.00 | -71.59 | +0.0100% |
| DOGEUSDT | 0.3 | 2.511 | -0.9% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | -1.57 | 1.772 | -0.1% | +98.32 | +57.02 | +0.0100% |
| AVAXUSDT | -2.05 | 1.541 | +0.3% | +77.94 | +45.09 | +0.0100% |
| LINKUSDT | -0.53 | 1.569 | +0.2% | +0.00 | +0.00 | +0.0067% |
| LTCUSDT | -1.08 | 1.948 | +3.0% | +0.00 | +0.00 | +0.0007% |
| TRXUSDT | 1.07 | 1.27 | +0.1% | +0.00 | +0.00 | +0.0100% |
| DOTUSDT | -0.82 | 1.72 | +0.3% | +0.00 | +0.00 | +0.0014% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
