# v9 brief - 2026-10-28 15:10 UTC (signal from the 2026-10-28 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-29.78 (-14.9% of budget); from peak $-33.77

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.76 | 1.827 | +1.8% | +0.00 | +0.00 | +0.0059% |
| ETHUSDT | 0.01 | 2.903 | +2.0% | +0.00 | +0.00 | +0.0075% |
| SOLUSDT | 1.25 | 2.903 | +2.6% | +0.00 | -161.49 | +0.0063% |
| BNBUSDT | -0.16 | 2.339 | +2.8% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | 0.71 | 2.83 | +1.7% | +0.00 | +0.00 | +0.0100% |
| DOGEUSDT | 0.25 | 2.57 | +3.8% | +0.00 | -149.69 | +0.0081% |
| ADAUSDT | -0.35 | 1.927 | +1.5% | +0.00 | +0.00 | +0.0076% |
| AVAXUSDT | -0.65 | 1.591 | +2.7% | +0.00 | +0.00 | -0.0038% |
| LINKUSDT | -0.26 | 1.632 | +3.9% | +0.00 | +0.00 | +0.0011% |
| LTCUSDT | -0.51 | 1.937 | +2.9% | +0.00 | +0.00 | -0.0118% |
| TRXUSDT | 0.2 | 1.215 | +1.2% | +0.00 | +0.00 | +0.0100% |
| DOTUSDT | -1.44 | 1.523 | +3.5% | +0.00 | +0.00 | +0.0018% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
