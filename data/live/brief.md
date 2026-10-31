# v9 brief - 2026-10-31 13:32 UTC (signal from the 2026-10-31 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-23.43 (-11.7% of budget); from peak $-27.42

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.88 | 2.666 | +0.3% | -253.45 | -154.82 | +0.0100% |
| ETHUSDT | -0.12 | 2.912 | +0.5% | +0.00 | +0.00 | -0.0057% |
| SOLUSDT | 1.19 | 3.045 | -0.7% | +0.00 | +0.00 | +0.0087% |
| BNBUSDT | 1.38 | 2.717 | +0.8% | +0.00 | +0.00 | -0.0096% |
| XRPUSDT | 0.1 | 2.69 | +0.2% | +0.00 | +0.00 | +0.0002% |
| DOGEUSDT | -1.35 | 2.347 | -0.7% | +0.00 | +0.00 | -0.0088% |
| ADAUSDT | -0.5 | 1.857 | -0.3% | +0.00 | +0.00 | -0.0165% |
| AVAXUSDT | -0.72 | 1.521 | +0.4% | +0.00 | +0.00 | -0.0207% |
| LINKUSDT | 1.1 | 1.775 | +3.9% | +0.00 | +0.00 | -0.0068% |
| LTCUSDT | -0.75 | 1.869 | -0.5% | +0.00 | +0.00 | +0.0069% |
| TRXUSDT | -0.35 | 1.165 | -5.8% | +0.00 | -197.47 | -0.0409% |
| DOTUSDT | -1.45 | 1.448 | +1.2% | +0.00 | +68.23 | +0.0021% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
