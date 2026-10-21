# v9 brief - 2026-10-21 18:12 UTC (signal from the 2026-10-21 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-1.99 (-1.0% of budget); from peak $-5.98

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -1.24 | 1.054 | +2.2% | +0.00 | +0.00 | +0.0042% |
| ETHUSDT | -2.36 | 2.217 | +2.6% | +204.88 | +0.00 | +0.0076% |
| SOLUSDT | 0.67 | 2.276 | +1.7% | +0.00 | +0.00 | +0.0057% |
| BNBUSDT | 0.72 | 2.412 | +1.7% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | -0.75 | 2.359 | +4.4% | +0.00 | +0.00 | +0.0100% |
| DOGEUSDT | 0.54 | 2.587 | +2.4% | +0.00 | +0.00 | +0.0086% |
| ADAUSDT | -1.05 | 1.876 | +2.6% | +0.00 | +0.00 | +0.0033% |
| AVAXUSDT | -1.71 | 1.436 | +2.4% | +101.10 | +103.74 | +0.0100% |
| LINKUSDT | -0.79 | 1.558 | +3.6% | +0.00 | +0.00 | -0.0071% |
| LTCUSDT | -1.77 | 1.764 | +2.6% | +132.46 | +129.97 | +0.0024% |
| TRXUSDT | -0.58 | 1.122 | +0.5% | +0.00 | +0.00 | -0.0031% |
| DOTUSDT | 0.8 | 2.096 | +0.7% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
