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
