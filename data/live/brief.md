# v9 brief - 2026-10-22 18:14 UTC (signal from the 2026-10-22 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-22.05 (-11.0% of budget); from peak $-26.04

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 2.09 | 2.013 | -4.1% | -110.01 | +0.00 | +0.0038% |
| ETHUSDT | 2.11 | 3.417 | -5.4% | -73.03 | +0.00 | -0.0071% |
| SOLUSDT | 1.76 | 2.814 | -4.6% | -62.53 | +0.00 | +0.0100% |
| BNBUSDT | 1.95 | 2.68 | -3.0% | -95.39 | +0.00 | -0.0120% |
| XRPUSDT | 0.48 | 2.611 | -5.7% | +0.00 | +0.00 | +0.0050% |
| DOGEUSDT | 2.01 | 2.778 | -6.0% | -52.68 | +0.00 | -0.0011% |
| ADAUSDT | -1.16 | 1.835 | -7.3% | +0.00 | +0.00 | -0.0219% |
| AVAXUSDT | -1.64 | 1.418 | -8.3% | +37.49 | +57.44 | -0.0063% |
| LINKUSDT | 0.14 | 1.709 | -6.2% | +0.00 | +0.00 | -0.0147% |
| LTCUSDT | -1.87 | 1.721 | -5.5% | +48.87 | +0.00 | +0.0017% |
| TRXUSDT | -0.92 | 1.078 | -1.4% | +0.00 | +0.00 | -0.0252% |
| DOTUSDT | -0.68 | 1.75 | -5.5% | +0.00 | +0.00 | -0.0165% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
