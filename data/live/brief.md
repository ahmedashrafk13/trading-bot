# v9 brief - 2026-09-30 00:22 UTC (signal from the 2026-09-30 00:00 bar close)

Budget $200 | vol target 0.55 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-9.51 (-4.8% of budget); from peak $-9.89

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.62 | 1.383 | +0.2% | +0.00 | +0.00 | +0.0043% |
| ETHUSDT | 0.55 | 2.741 | -0.4% | +0.00 | +0.00 | +0.0018% |
| SOLUSDT | -0.55 | 1.786 | +0.2% | +0.00 | +0.00 | -0.0140% |
| BNBUSDT | -0.11 | 2.247 | -0.7% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | 1.44 | 2.561 | -0.4% | +0.00 | -71.95 | +0.0042% |
| DOGEUSDT | 0.18 | 2.482 | -0.0% | +0.00 | +0.00 | +0.0015% |
| ADAUSDT | 0.68 | 2.229 | -1.2% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | 1.73 | 2.768 | +7.8% | -53.26 | -53.52 | +0.0100% |
| LINKUSDT | 1.93 | 2.034 | -5.5% | -64.45 | -63.51 | +0.0032% |
| LTCUSDT | 0.93 | 2.601 | -3.5% | +0.00 | +0.00 | +0.0014% |
| TRXUSDT | -0.62 | 1.102 | -0.3% | +0.00 | +0.00 | -0.0667% |
| DOTUSDT | -0.83 | 1.824 | +1.0% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
