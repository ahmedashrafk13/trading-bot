# v9 brief - 2026-11-27 18:19 UTC (signal from the 2026-11-27 18:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $+15.03 (+7.5% of budget); from peak $-11.85

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.67 | 2.982 | -1.0% | +0.00 | +0.00 | +0.0024% |
| ETHUSDT | -0.5 | 2.459 | -1.3% | +0.00 | +0.00 | -0.0018% |
| SOLUSDT | 0.37 | 3.527 | +1.4% | +0.00 | +0.00 | +0.0052% |
| BNBUSDT | -0.2 | 2.536 | +0.1% | +0.00 | +0.00 | +0.0100% |
| XRPUSDT | 1.06 | 3.049 | -0.3% | +0.00 | +0.00 | +0.0063% |
| DOGEUSDT | 0.76 | 2.642 | +1.8% | +0.00 | +0.00 | +0.0041% |
| ADAUSDT | 2.13 | 2.578 | +0.3% | -114.33 | -111.53 | +0.0021% |
| AVAXUSDT | -1.12 | 1.508 | +0.4% | +0.00 | +0.00 | -0.0116% |
| LINKUSDT | 1.75 | 2.033 | +1.9% | -108.81 | -105.71 | +0.0090% |
| LTCUSDT | 1.27 | 2.254 | +1.4% | +0.00 | +0.00 | +0.0100% |
| TRXUSDT | -0.81 | 1.071 | -0.8% | +0.00 | +0.00 | -0.0292% |
| DOTUSDT | 1.75 | 1.874 | -0.2% | -117.98 | +0.00 | +0.0100% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
