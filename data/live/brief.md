# v9 brief - 2026-10-11 12:12 UTC (signal from the 2026-10-11 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-2.91 (-1.5% of budget); from peak $-3.30

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.58 | 1.44 | +0.3% | +0.00 | +0.00 | +0.0045% |
| ETHUSDT | 0.71 | 2.948 | +0.4% | +0.00 | +0.00 | +0.0027% |
| SOLUSDT | 1.73 | 2.418 | -0.2% | -132.41 | -120.70 | -0.0012% |
| BNBUSDT | -0.68 | 2.154 | +0.1% | +0.00 | +0.00 | -0.0012% |
| XRPUSDT | -0.52 | 2.333 | -0.7% | +0.00 | +0.00 | +0.0031% |
| DOGEUSDT | -0.29 | 2.402 | -0.6% | +0.00 | +0.00 | +0.0013% |
| ADAUSDT | -0.4 | 2.054 | -3.3% | +0.00 | +0.00 | -0.0069% |
| AVAXUSDT | -1.95 | 1.644 | -1.9% | +73.96 | +73.15 | +0.0097% |
| LINKUSDT | -0.43 | 1.573 | -0.4% | +0.00 | +0.00 | +0.0100% |
| LTCUSDT | -1.52 | 1.895 | -0.4% | +112.04 | +108.02 | -0.0015% |
| TRXUSDT | -0.94 | 1.081 | -0.2% | +0.00 | +0.00 | -0.0109% |
| DOTUSDT | 1.85 | 2.349 | -1.6% | -81.59 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
