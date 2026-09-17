# Shadow Log — screened but NOT taken

Purpose: SAMPLE SIZE. This account closes ~2-4 real trades a month, so judging
the entry gate on realised trades alone would take a year. Every candidate that
PASSES a sleeve's technical screen but is not bought is recorded here with its
price, then scored 5 days later. That yields ~40-60 observations a month at zero
cost and zero risk.

What this answers, and nothing else answers:
- Does a screen PASS actually precede an up-move, or is the gate noise?
- Are the trades we DO take better than the ones we skip, or is selection adding
  nothing on top of the screen?
- Would a wider or narrower gate have helped? (Counterfactual, not hindsight.)

RULES
- Append-only. Never delete or edit a row once written; a wrong prediction is the
  entire point of the file.
- Record the price AT THE TIME OF THE SCREEN, from the same `screen.sh` run that
  produced the pass. Never backfill a price later — that is hindsight.
- Score at T+5d in the research run: `outcome` is the % change from screen price,
  and `MFE` is the best close in the window (did it trend at all?).
- Rows are EVIDENCE for the weekly review only. They are NOT a trade trigger and
  never justify an unscheduled amendment.

| date (UTC) | pair | sleeve | screen px | reason not taken | T+5d % | MFE % | scored |
|---|---|---|---|---|---|---|---|
| 2026-09-16 | UNI | CORE | 6.3393 | catalyst stale (~8d old, fee-switch burn), already priced +93%/30d, DeFi narrative has 1 tactical loss (UNI itself, 09-15) | | | |
| 2026-09-16 | ARB | CORE | 0.1538 | same-day token unlock (~$13M, 0.93% supply) is a bearish overhang | | | |
| 2026-09-16 | FIL | CORE | 0.8126 | no confirmed catalyst, momentum/speculation only | | | |
| 2026-09-16 | XTZ | CORE | 0.2448 | catalysts (X mainnet, Etherlink 7.0) undated/ongoing | | | |
| 2026-09-16 | ARB | TACTICAL | 0.1538 | same-day token unlock (~$13M, 0.93% supply) is a bearish overhang | | | |
| 2026-09-16 | XRP | TACTICAL | 1.2944 | catalyst (CLARITY cloture) already failed 09-15, caused this week's tactical stop-out | | | |
| 2026-09-16 | DOT | TACTICAL | 0.9508 | no catalyst found; L1/L2 narrative already has 1 tactical loss (09-14) | | | |
| 2026-09-16 | WIF | TACTICAL | 0.1792 | meme narrative rolling over, no dated catalyst | | | |
| 2026-09-16 | BTC | TACTICAL | 75943.8655 | shared FOMC/macro catalyst only, not idiosyncratic | | | |
| 2026-09-16 | HYPE | TACTICAL | 77.2080 | unlock already happened Sept 6, priced in, no fresh trigger | | | |
| 2026-09-16 | SOL | TACTICAL | 97.1300 | no dated catalyst found | | | |
| 2026-09-16 | ETH | TACTICAL | 2403.9500 | shared FOMC/ETF-flow catalyst only; already the account's CORE exposure, would concentrate risk | | | |
| 2026-09-16 | DOGE | TACTICAL | 0.0801 | meme narrative rolling over, no dated catalyst | | | |
| 2026-09-17 | ONDO | CORE | 0.3748 | closest CORE name (RWA/SEC roundtable 09-17) but catalyst undated and sector-shared, not idiosyncratic | | | |
| 2026-09-17 | AAVE | CORE | 129.1600 | no dated catalyst; DeFi narrative not bid under >60% dominance | | | |
| 2026-09-17 | FET | CORE | 0.1693 | AI narrative present but no dated idiosyncratic catalyst | | | |
| 2026-09-17 | HYPE | CORE | 83.4100 | Sept-6 unlock already priced, no fresh trigger | | | |
| 2026-09-17 | DOT | CORE | 1.0798 | no catalyst; L1 narrative already carries a tactical loss (09-14) | | | |
| 2026-09-17 | INJ | CORE | 5.7340 | no dated catalyst | | | |
| 2026-09-17 | JUP | CORE | 0.2335 | no dated catalyst | | | |
| 2026-09-17 | XLM | CORE | 0.1863 | no dated catalyst | | | |
| 2026-09-17 | LTC | CORE | 53.9100 | no dated catalyst | | | |
| 2026-09-17 | AVAX | CORE | 7.6190 | no dated catalyst | | | |
| 2026-09-17 | BNB | CORE | 735.1000 | no dated catalyst | | | |
| 2026-09-17 | ASTER | CORE | 0.7460 | no dated catalyst | | | |
| 2026-09-17 | AERO | CORE | 0.5873 | no dated catalyst; negative 7p momentum | | | |
| 2026-09-17 | FLOCK | CORE | 0.0679 | no dated catalyst; -5.1%/7p | | | |
| 2026-09-17 | PIEVERSE | CORE | 1.2949 | leads CORE on momentum (+12.9%/7p) but no catalyst found; widest spread on the shortlist (0.16%) | | | |
| 2026-09-17 | ARB | TACTICAL | 0.1774 | dated BEARISH catalyst: 139.15M-token unlock (1.4% supply) on 09-23 | | | |
| 2026-09-17 | CRV | TACTICAL | 0.3312 | no catalyst; DeFi narrative not bid | | | |
| 2026-09-17 | NEAR | TACTICAL | 3.0010 | no dated catalyst | | | |
| 2026-09-17 | BR | TACTICAL | 0.6734 | no dated catalyst; spread 0.19% | | | |
| 2026-09-17 | PEPE | TACTICAL | 0.0000 | meme narrative rolling over, no dated catalyst | | | |
| 2026-09-17 | SHIB | TACTICAL | 0.0000 | meme narrative rolling over, no dated catalyst | | | |
| 2026-09-17 | LINK | TACTICAL | 11.3610 | no dated catalyst | | | |
| 2026-09-17 | ENA | TACTICAL | 0.1550 | no dated catalyst | | | |
| 2026-09-17 | ADA | TACTICAL | 0.2028 | no dated catalyst | | | |
| 2026-09-17 | HBAR | TACTICAL | 0.0756 | no dated catalyst | | | |
| 2026-09-17 | BCH | TACTICAL | 232.7000 | no dated catalyst | | | |
| 2026-09-17 | POL | TACTICAL | 0.0977 | no dated catalyst | | | |
| 2026-09-17 | XPL | TACTICAL | 0.0862 | no dated catalyst | | | |
| 2026-09-17 | APT | TACTICAL | 0.5809 | no dated catalyst | | | |
| 2026-09-17 | WLD | TACTICAL | 0.3809 | no dated catalyst | | | |
