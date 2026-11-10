# v9 brief - 2026-11-10 12:12 UTC (signal from the 2026-11-10 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-34.32 (-17.2% of budget); from peak $-38.31

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.41 | 2.965 | +0.1% | +0.00 | +0.00 | +0.0051% |
| ETHUSDT | 1.7 | 3.975 | -0.9% | -142.88 | -146.34 | +0.0040% |
| SOLUSDT | 1.63 | 3.655 | -1.6% | -135.81 | +0.00 | -0.0056% |
| BNBUSDT | 0.33 | 2.634 | +0.8% | +0.00 | +0.00 | +0.0006% |
| XRPUSDT | 0.38 | 2.852 | -0.2% | +0.00 | +0.00 | +0.0079% |
| DOGEUSDT | 0.01 | 2.589 | +0.9% | +0.00 | +0.00 | -0.0024% |
| ADAUSDT | 0.53 | 1.905 | +1.2% | +0.00 | +0.00 | -0.0034% |
| AVAXUSDT | 2.77 | 2.073 | +3.5% | -96.92 | +0.00 | -0.0218% |
| LINKUSDT | 1.61 | 1.957 | -0.6% | -104.40 | +0.00 | +0.0052% |
| LTCUSDT | -0.39 | 1.907 | +1.1% | +0.00 | +143.56 | +0.0046% |
| TRXUSDT | -0.4 | 1.153 | +0.5% | +0.00 | +0.00 | +0.0000% |
| DOTUSDT | -0.86 | 1.486 | -0.8% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
