# v9 brief - 2026-11-24 15:17 UTC (signal from the 2026-11-24 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $+17.85 (+8.9% of budget); from peak $+0.00

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.13 | 2.644 | -1.6% | +0.00 | +0.00 | +0.0036% |
| ETHUSDT | -1.16 | 2.228 | -1.3% | +0.00 | +0.00 | +0.0005% |
| SOLUSDT | 1.85 | 3.916 | -2.3% | -106.08 | +0.00 | -0.0031% |
| BNBUSDT | -0.35 | 2.516 | -0.9% | +0.00 | +0.00 | +0.0063% |
| XRPUSDT | 1.26 | 3.108 | -0.9% | +0.00 | +0.00 | -0.0093% |
| DOGEUSDT | -0.64 | 2.421 | +0.3% | +0.00 | +0.00 | -0.0061% |
| ADAUSDT | 2.79 | 2.57 | +0.8% | -96.84 | -105.18 | +0.0000% |
| AVAXUSDT | 0.02 | 1.738 | +0.1% | +0.00 | +0.00 | -0.0073% |
| LINKUSDT | 1.1 | 1.925 | +0.7% | +0.00 | +0.00 | -0.0022% |
| LTCUSDT | -0.38 | 1.939 | +0.8% | +0.00 | +0.00 | +0.0027% |
| TRXUSDT | 1.61 | 1.369 | +0.2% | -178.33 | +0.00 | -0.0036% |
| DOTUSDT | 1.88 | 1.826 | -0.8% | -98.75 | +0.00 | -0.0055% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
