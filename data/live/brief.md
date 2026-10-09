# v9 brief - 2026-10-09 12:12 UTC (signal from the 2026-10-09 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-6.92 (-3.5% of budget); from peak $-7.30

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.15 | 1.627 | +0.9% | +0.00 | -83.28 | +0.0059% |
| ETHUSDT | 1.01 | 3.024 | -1.2% | +0.00 | +0.00 | +0.0028% |
| SOLUSDT | 1.68 | 2.356 | -1.7% | -163.23 | -66.63 | +0.0008% |
| BNBUSDT | -0.04 | 2.268 | -2.5% | +0.00 | -96.69 | -0.0053% |
| XRPUSDT | -0.14 | 2.391 | +0.3% | +0.00 | -56.82 | +0.0027% |
| DOGEUSDT | -0.39 | 2.391 | -2.5% | +0.00 | +0.00 | -0.0037% |
| ADAUSDT | -0.51 | 2.012 | -4.0% | +0.00 | +0.00 | -0.0020% |
| AVAXUSDT | -1.21 | 1.886 | -3.0% | +0.00 | +0.00 | -0.0017% |
| LINKUSDT | -0.64 | 1.544 | -0.7% | +0.00 | +0.00 | -0.0039% |
| LTCUSDT | -1.16 | 2.015 | +0.1% | +0.00 | +0.00 | -0.0067% |
| TRXUSDT | -0.65 | 1.137 | -0.8% | +0.00 | +0.00 | -0.0222% |
| DOTUSDT | -1.82 | 1.538 | +6.7% | +98.64 | +40.68 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
