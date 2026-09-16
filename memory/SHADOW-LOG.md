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
