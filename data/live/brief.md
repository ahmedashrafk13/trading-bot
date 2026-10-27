# v9 brief - 2026-10-27 18:13 UTC (signal from the 2026-10-27 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-27.31 (-13.7% of budget); from peak $-31.30

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.4 | 2.105 | +0.2% | +0.00 | -161.11 | +0.0100% |
| ETHUSDT | 0.59 | 3.09 | +0.9% | +0.00 | -93.80 | +0.0100% |
| SOLUSDT | 1.51 | 3.008 | -0.6% | -165.50 | -90.65 | +0.0071% |
| BNBUSDT | 0.67 | 2.495 | +0.6% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | 1.02 | 2.911 | +1.7% | +0.00 | -102.71 | +0.0093% |
| DOGEUSDT | 1.76 | 2.769 | +0.7% | -147.57 | +0.00 | +0.0083% |
| ADAUSDT | -0.62 | 1.876 | -0.8% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | -0.77 | 1.565 | -1.5% | +0.00 | +0.00 | +0.0025% |
| LINKUSDT | -0.4 | 1.616 | -0.2% | +0.00 | +0.00 | +0.0100% |
| LTCUSDT | -0.51 | 1.945 | -0.4% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | -0.62 | 1.116 | -0.7% | +0.00 | +0.00 | +0.0012% |
| DOTUSDT | -1.31 | 1.565 | -2.2% | +0.00 | +0.00 | -0.0124% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
