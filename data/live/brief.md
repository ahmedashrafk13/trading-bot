# v9 brief - 2026-10-15 10:12 UTC (signal from the 2026-10-15 06:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $+3.40 (+1.7% of budget); from peak $-0.59

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.7 | 1.794 | -3.5% | -118.82 | -81.06 | +0.0041% |
| ETHUSDT | 1.38 | 3.219 | -6.2% | +0.00 | -47.35 | +0.0056% |
| SOLUSDT | 2.07 | 2.63 | -5.3% | -69.32 | -51.16 | +0.0100% |
| BNBUSDT | 2.65 | 2.618 | -4.0% | -112.13 | -86.54 | +0.0039% |
| XRPUSDT | 1.56 | 2.708 | -5.2% | -60.92 | -46.59 | +0.0011% |
| DOGEUSDT | -0.65 | 2.349 | -6.5% | +0.00 | +0.00 | +0.0074% |
| ADAUSDT | -1.41 | 1.812 | -6.8% | +0.00 | +0.00 | +0.0062% |
| AVAXUSDT | -2.26 | 1.527 | -6.8% | +38.81 | +28.70 | -0.0083% |
| LINKUSDT | -0.41 | 1.587 | -6.8% | +0.00 | +0.00 | -0.0002% |
| LTCUSDT | -0.01 | 2.173 | -6.9% | +0.00 | +0.00 | -0.0121% |
| TRXUSDT | 0.68 | 1.234 | -0.1% | +0.00 | +0.00 | +0.0018% |
| DOTUSDT | -0.04 | 1.889 | -5.7% | +0.00 | +0.00 | +0.0035% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
