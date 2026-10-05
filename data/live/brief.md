# v9 brief - 2026-10-05 18:12 UTC (signal from the 2026-10-05 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-7.33 (-3.7% of budget); from peak $-7.71

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -0.47 | 1.129 | +0.1% | +0.00 | +0.00 | -0.0011% |
| ETHUSDT | 0.02 | 2.615 | +0.1% | +0.00 | +0.00 | +0.0016% |
| SOLUSDT | -0.33 | 1.798 | -1.2% | +0.00 | +0.00 | -0.0082% |
| BNBUSDT | -0.48 | 2.174 | -0.2% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | -0.41 | 2.348 | -0.4% | +0.00 | +0.00 | -0.0035% |
| DOGEUSDT | 0.62 | 2.606 | -0.8% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | 1.06 | 2.397 | +6.7% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | -1.13 | 1.937 | -1.6% | +0.00 | +0.00 | -0.0040% |
| LINKUSDT | 0.21 | 1.74 | -2.0% | +0.00 | +0.00 | +0.0092% |
| LTCUSDT | -1.2 | 2.091 | -0.5% | +0.00 | +126.76 | +0.0100% |
| TRXUSDT | -0.43 | 1.165 | +0.4% | +0.00 | +0.00 | -0.0479% |
| DOTUSDT | -0.95 | 1.762 | +0.0% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
