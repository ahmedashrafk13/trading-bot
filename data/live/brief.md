# v9 brief - 2026-10-16 06:10 UTC (signal from the 2026-10-16 06:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $+0.74 (+0.4% of budget); from peak $-3.25

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.01 | 1.543 | +2.0% | +0.00 | +0.00 | +0.0095% |
| ETHUSDT | -0.26 | 2.636 | +4.2% | +0.00 | +0.00 | +0.0018% |
| SOLUSDT | 1.42 | 2.394 | +4.4% | +0.00 | +0.00 | +0.0061% |
| BNBUSDT | 1.84 | 2.519 | +2.4% | -100.11 | -211.61 | +0.0028% |
| XRPUSDT | 1.38 | 2.689 | +3.5% | +0.00 | +0.00 | +0.0100% |
| DOGEUSDT | 0.13 | 2.486 | +4.2% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | -1.55 | 1.778 | +5.0% | +43.96 | +56.94 | +0.0100% |
| AVAXUSDT | -1.88 | 1.579 | +6.2% | +34.86 | +45.35 | +0.0080% |
| LINKUSDT | -0.51 | 1.575 | +4.1% | +0.00 | +0.00 | +0.0085% |
| LTCUSDT | -0.9 | 1.983 | +6.4% | +0.00 | +0.00 | +0.0080% |
| TRXUSDT | 1.55 | 1.322 | +1.2% | -221.08 | +0.00 | +0.0100% |
| DOTUSDT | -0.27 | 1.835 | +5.6% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
