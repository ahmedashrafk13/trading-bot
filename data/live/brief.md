# v9 brief - 2026-10-10 08:42 UTC (signal from the 2026-10-10 06:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-2.88 (-1.4% of budget); from peak $-3.26

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.85 | 1.534 | +0.6% | +0.00 | +0.00 | -0.0085% |
| ETHUSDT | 1.11 | 3.07 | +0.3% | +0.00 | +0.00 | -0.0016% |
| SOLUSDT | 1.8 | 2.414 | -0.1% | -163.23 | -153.70 | -0.0050% |
| BNBUSDT | -0.16 | 2.241 | +1.2% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | 0.1 | 2.426 | +1.0% | +0.00 | +0.00 | +0.0078% |
| DOGEUSDT | -0.05 | 2.443 | +1.6% | +0.00 | +0.00 | +0.0031% |
| ADAUSDT | -0.44 | 2.034 | +6.8% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | -1.28 | 1.849 | +3.3% | +0.00 | +0.00 | +0.0087% |
| LINKUSDT | -0.44 | 1.575 | +0.5% | +0.00 | +0.00 | +0.0100% |
| LTCUSDT | -1.25 | 1.983 | -0.1% | +0.00 | +0.00 | +0.0023% |
| TRXUSDT | -0.71 | 1.124 | -0.4% | +0.00 | +0.00 | -0.0458% |
| DOTUSDT | 1.77 | 2.341 | +9.2% | -98.98 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
