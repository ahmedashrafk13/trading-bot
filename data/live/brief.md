# v9 brief - 2026-09-30 06:26 UTC (signal from the 2026-09-30 06:00 bar close)

Budget $200 | vol target 0.55 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-7.77 (-3.9% of budget); from peak $-8.16

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.65 | 1.393 | -0.1% | +0.00 | +0.00 | +0.0034% |
| ETHUSDT | 0.75 | 2.802 | -0.1% | +0.00 | +0.00 | +0.0048% |
| SOLUSDT | -0.56 | 1.782 | +0.7% | +0.00 | +0.00 | -0.0012% |
| BNBUSDT | -0.32 | 2.206 | +0.7% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | 1.2 | 2.532 | +0.6% | +0.00 | +0.00 | +0.0074% |
| DOGEUSDT | 0.07 | 2.461 | +0.1% | +0.00 | +0.00 | +0.0014% |
| ADAUSDT | 0.4 | 2.154 | +0.2% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | 1.55 | 2.712 | +6.2% | -53.26 | -52.42 | +0.0024% |
| LINKUSDT | 2.07 | 2.083 | -2.9% | -64.45 | -62.97 | +0.0031% |
| LTCUSDT | 0.75 | 2.556 | -1.3% | +0.00 | +0.00 | +0.0097% |
| TRXUSDT | -0.58 | 1.107 | +0.9% | +0.00 | +0.00 | -0.0008% |
| DOTUSDT | -0.49 | 1.902 | +3.6% | +0.00 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
