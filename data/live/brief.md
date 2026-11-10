# v9 brief - 2026-11-10 18:12 UTC (signal from the 2026-11-10 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-23.76 (-11.9% of budget); from peak $-27.75

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.55 | 3.115 | -2.0% | -224.55 | +0.00 | +0.0100% |
| ETHUSDT | 1.14 | 3.627 | -4.6% | +0.00 | -121.56 | -0.0009% |
| SOLUSDT | 1.59 | 3.643 | -5.0% | -145.78 | -131.87 | -0.0032% |
| BNBUSDT | 0.86 | 2.745 | -1.9% | +0.00 | +0.00 | -0.0084% |
| XRPUSDT | 0.57 | 2.905 | -3.7% | +0.00 | +0.00 | +0.0100% |
| DOGEUSDT | -0.0 | 2.589 | -4.1% | +0.00 | +0.00 | -0.0203% |
| ADAUSDT | 1.26 | 1.961 | -3.4% | +0.00 | +0.00 | -0.0060% |
| AVAXUSDT | 3.08 | 2.163 | -4.7% | -109.68 | -95.94 | +0.0011% |
| LINKUSDT | 1.48 | 1.94 | -3.8% | +0.00 | -101.12 | -0.0113% |
| LTCUSDT | 0.08 | 1.999 | -2.9% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | -0.5 | 1.141 | +0.2% | +0.00 | +0.00 | -0.0049% |
| DOTUSDT | -0.82 | 1.492 | -3.7% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
