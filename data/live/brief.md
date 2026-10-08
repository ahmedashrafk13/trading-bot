# v9 brief - 2026-10-08 00:31 UTC (signal from the 2026-10-08 00:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-8.02 (-4.0% of budget); from peak $-8.40

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.51 | 1.69 | -2.6% | -173.99 | +0.00 | +0.0044% |
| ETHUSDT | 2.24 | 3.384 | -4.6% | -138.63 | -231.51 | -0.0063% |
| SOLUSDT | 0.95 | 2.11 | -3.7% | +0.00 | +0.00 | -0.0005% |
| BNBUSDT | 0.26 | 2.311 | -0.9% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | 2.32 | 2.749 | -5.1% | -87.38 | +0.00 | -0.0123% |
| DOGEUSDT | 0.51 | 2.556 | -5.0% | +0.00 | +0.00 | +0.0097% |
| ADAUSDT | 1.3 | 2.534 | -4.5% | +0.00 | +0.00 | +0.0099% |
| AVAXUSDT | 1.03 | 2.614 | -4.1% | +0.00 | +0.00 | +0.0009% |
| LINKUSDT | 0.09 | 1.697 | -4.5% | +0.00 | +0.00 | +0.0063% |
| LTCUSDT | -0.53 | 2.187 | -4.2% | +0.00 | +0.00 | -0.0003% |
| TRXUSDT | -0.48 | 1.164 | +0.0% | +0.00 | +0.00 | +0.0056% |
| DOTUSDT | -1.43 | 1.647 | -7.0% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
