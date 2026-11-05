# v9 brief - 2026-11-05 00:12 UTC (signal from the 2026-11-05 00:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-18.61 (-9.3% of budget); from peak $-22.60

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -1.04 | 1.391 | +3.9% | +0.00 | +0.00 | +0.0064% |
| ETHUSDT | -3.62 | 1.831 | +6.6% | +169.88 | +169.78 | +0.0047% |
| SOLUSDT | 0.69 | 2.943 | +2.9% | +0.00 | +0.00 | -0.0035% |
| BNBUSDT | -0.76 | 2.334 | +3.1% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | -0.69 | 2.5 | +2.2% | +0.00 | +0.00 | +0.0046% |
| DOGEUSDT | 0.07 | 2.56 | +2.5% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | 0.39 | 1.99 | +3.9% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | 1.19 | 1.982 | +2.6% | +0.00 | +0.00 | -0.0006% |
| LINKUSDT | 1.35 | 1.835 | +3.8% | +0.00 | +0.00 | +0.0100% |
| LTCUSDT | -2.16 | 1.62 | +3.6% | +151.99 | +151.69 | +0.0100% |
| TRXUSDT | -0.68 | 1.117 | -0.6% | +0.00 | +0.00 | +0.0047% |
| DOTUSDT | -0.35 | 1.66 | +1.8% | +0.00 | +0.00 | -0.0044% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
