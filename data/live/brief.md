# v9 brief - 2026-10-09 07:17 UTC (signal from the 2026-10-09 06:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.0x | leverage 4x | stop 12%

RISK: P&L since v9 start $-5.62 (-2.8% of budget); from peak $-6.01

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 1.68 | 1.816 | -0.4% | -120.00 | -82.51 | +0.0050% |
| ETHUSDT | 1.35 | 3.137 | -2.8% | +0.00 | -49.97 | +0.0015% |
| SOLUSDT | 1.73 | 2.367 | -4.0% | -70.18 | -55.21 | -0.0033% |
| BNBUSDT | 1.65 | 2.569 | -3.3% | -108.14 | -81.64 | -0.0147% |
| XRPUSDT | 1.98 | 2.719 | -0.2% | -59.28 | -46.88 | -0.0069% |
| DOGEUSDT | -0.32 | 2.404 | -2.2% | +0.00 | +0.00 | -0.0087% |
| ADAUSDT | -0.36 | 2.054 | -5.9% | +0.00 | +0.00 | -0.0091% |
| AVAXUSDT | -1.23 | 1.886 | -5.0% | +0.00 | +0.00 | +0.0000% |
| LINKUSDT | -0.45 | 1.58 | -1.8% | +0.00 | +0.00 | +0.0100% |
| LTCUSDT | -1.17 | 2.017 | -0.4% | +0.00 | +0.00 | -0.0001% |
| TRXUSDT | -0.59 | 1.148 | -0.8% | +0.00 | +0.00 | -0.0123% |
| DOTUSDT | -2.17 | 1.484 | +5.8% | +42.40 | +35.53 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
