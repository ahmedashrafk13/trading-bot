# v9 brief - 2026-10-30 18:12 UTC (signal from the 2026-10-30 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-31.58 (-15.8% of budget); from peak $-35.58

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 2.02 | 2.651 | -4.6% | -202.76 | -154.02 | +0.0100% |
| ETHUSDT | -0.18 | 2.885 | -4.2% | +0.00 | +0.00 | -0.0099% |
| SOLUSDT | 1.46 | 3.165 | -6.6% | +0.00 | +0.00 | -0.0020% |
| BNBUSDT | 1.27 | 2.676 | -6.3% | +0.00 | +0.00 | -0.0201% |
| XRPUSDT | -0.5 | 2.525 | -3.7% | +0.00 | +0.00 | -0.0189% |
| DOGEUSDT | -1.31 | 2.361 | -5.3% | +0.00 | +0.00 | -0.0116% |
| ADAUSDT | -1.4 | 1.692 | -5.5% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | -0.69 | 1.543 | -5.2% | +0.00 | +0.00 | -0.0046% |
| LINKUSDT | 0.16 | 1.67 | -4.8% | +0.00 | +0.00 | -0.0278% |
| LTCUSDT | -0.54 | 1.913 | -4.1% | +0.00 | +0.00 | -0.0157% |
| TRXUSDT | 1.56 | 1.436 | +0.8% | -208.67 | -207.02 | -0.0379% |
| DOTUSDT | -1.82 | 1.387 | -3.6% | +68.57 | +68.83 | -0.0237% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
