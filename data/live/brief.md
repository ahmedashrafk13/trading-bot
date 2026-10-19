# v9 brief - 2026-10-19 18:12 UTC (signal from the 2026-10-19 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-1.77 (-0.9% of budget); from peak $-5.76

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.97 | 1.587 | +0.9% | +0.00 | +0.00 | +0.0041% |
| ETHUSDT | 0.54 | 2.9 | +1.2% | +0.00 | +0.00 | +0.0063% |
| SOLUSDT | 1.14 | 2.404 | +1.9% | +0.00 | +0.00 | -0.0043% |
| BNBUSDT | 1.51 | 2.524 | +2.0% | -224.15 | -218.14 | +0.0100% |
| XRPUSDT | 0.44 | 2.575 | +2.2% | +0.00 | +0.00 | +0.0028% |
| DOGEUSDT | 0.12 | 2.514 | +1.7% | +0.00 | +0.00 | +0.0052% |
| ADAUSDT | -1.25 | 1.858 | +0.6% | +0.00 | +0.00 | +0.0048% |
| AVAXUSDT | -1.69 | 1.537 | +0.4% | +81.09 | +80.34 | +0.0033% |
| LINKUSDT | -0.74 | 1.551 | +1.2% | +0.00 | +0.00 | +0.0100% |
| LTCUSDT | -1.83 | 1.791 | +2.9% | +119.21 | +0.00 | +0.0069% |
| TRXUSDT | 0.57 | 1.274 | -0.4% | +0.00 | +0.00 | -0.0083% |
| DOTUSDT | -0.33 | 1.804 | +6.4% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
