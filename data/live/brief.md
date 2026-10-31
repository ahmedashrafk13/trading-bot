# v9 brief - 2026-10-31 18:12 UTC (signal from the 2026-10-31 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-24.20 (-12.1% of budget); from peak $-28.19

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.75 | 2.598 | +0.7% | -204.09 | -232.92 | +0.0063% |
| ETHUSDT | -0.37 | 2.836 | +0.5% | +0.00 | +0.00 | -0.0003% |
| SOLUSDT | 1.2 | 3.063 | +1.7% | +0.00 | +0.00 | +0.0061% |
| BNBUSDT | 1.06 | 2.65 | +1.1% | +0.00 | +0.00 | +0.0016% |
| XRPUSDT | 0.07 | 2.682 | +0.8% | +0.00 | +0.00 | -0.0033% |
| DOGEUSDT | -1.72 | 2.291 | +0.6% | +115.35 | +0.00 | -0.0018% |
| ADAUSDT | -0.46 | 1.865 | +0.7% | +0.00 | +0.00 | +0.0043% |
| AVAXUSDT | -0.57 | 1.562 | +1.9% | +0.00 | +0.00 | -0.0226% |
| LINKUSDT | 1.83 | 1.857 | +4.4% | -91.40 | +0.00 | -0.0066% |
| LTCUSDT | -1.05 | 1.815 | +0.4% | +0.00 | +0.00 | +0.0032% |
| TRXUSDT | -0.76 | 1.114 | -8.0% | +0.00 | +0.00 | -0.0785% |
| DOTUSDT | -1.53 | 1.423 | -0.2% | +69.16 | +0.00 | -0.0013% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
