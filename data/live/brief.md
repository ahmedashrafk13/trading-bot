# v9 brief - 2026-11-26 13:53 UTC (signal from the 2026-11-26 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $+12.27 (+6.1% of budget); from peak $-14.60

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | -0.1 | 2.556 | +3.5% | +0.00 | +0.00 | +0.0082% |
| ETHUSDT | -1.25 | 2.11 | +3.8% | +0.00 | +0.00 | +0.0054% |
| SOLUSDT | 0.27 | 3.484 | +4.9% | +0.00 | -121.02 | +0.0100% |
| BNBUSDT | -0.57 | 2.478 | +2.4% | +0.00 | +0.00 | +0.0038% |
| XRPUSDT | 0.01 | 2.817 | +4.8% | +0.00 | +0.00 | +0.0100% |
| DOGEUSDT | -0.33 | 2.46 | +6.0% | +0.00 | +0.00 | +0.0087% |
| ADAUSDT | 1.03 | 2.26 | +6.3% | +0.00 | +0.00 | +0.0100% |
| AVAXUSDT | -0.82 | 1.569 | +3.9% | +0.00 | +0.00 | +0.0020% |
| LINKUSDT | 1.01 | 1.929 | +7.3% | +0.00 | +0.00 | +0.0080% |
| LTCUSDT | 0.2 | 2.04 | +8.5% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | -1.02 | 1.054 | -1.5% | +0.00 | +0.00 | -0.0515% |
| DOTUSDT | 1.24 | 1.778 | +6.3% | +0.00 | +0.00 | +0.0006% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
