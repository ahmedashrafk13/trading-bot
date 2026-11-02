# v9 brief - 2026-11-02 17:14 UTC (signal from the 2026-11-02 12:00 bar close)

Budget $200 | vol target 0.8 | gross cap 2.4x | leverage 5x | stop 10%

RISK: P&L since v9 start $-20.30 (-10.1% of budget); from peak $-24.29

Strategy: fade the retail crowd. z_crowd >= +1.5 = crowd long-heavy -> SHORT; <= -1.5 -> LONG. Hold 6h.

| symbol | z_crowd | L/S | 24h | strategy target $ | now $ | funding 8h |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.84 | 2.11 | -0.1% | +0.00 | +0.00 | +0.0064% |
| ETHUSDT | -2.16 | 2.332 | +0.8% | +177.96 | +0.00 | +0.0046% |
| SOLUSDT | 1.41 | 3.268 | -1.3% | +0.00 | +0.00 | +0.0064% |
| BNBUSDT | 1.17 | 2.705 | -1.2% | +0.00 | +0.00 | +0.0054% |
| XRPUSDT | -0.47 | 2.536 | -0.3% | +0.00 | +0.00 | +0.0006% |
| DOGEUSDT | -0.06 | 2.522 | -0.4% | +0.00 | +0.00 | +0.0100% |
| ADAUSDT | -0.32 | 1.874 | -1.4% | +0.00 | +0.00 | +0.0077% |
| AVAXUSDT | 0.27 | 1.775 | -2.5% | +0.00 | +0.00 | +0.0100% |
| LINKUSDT | 2.68 | 1.952 | -4.0% | -113.50 | -106.97 | +0.0090% |
| LTCUSDT | 0.89 | 2.159 | -2.1% | +0.00 | +0.00 | +0.0005% |
| TRXUSDT | -0.64 | 1.127 | +1.8% | +0.00 | +0.00 | -0.0061% |
| DOTUSDT | -1.18 | 1.466 | -1.0% | +0.00 | +85.47 | +0.0067% |

Write data/live/decisions.json (see routines/v9.md), then run `python scripts/v9.py execute`.
