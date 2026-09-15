# Observations — defects found in the bot's OWN instructions

This is an INBOX, not a journal. One line per defect found in a prompt, a
script or a doc. Trading opinions do NOT belong here — those go to TRADE-LOG.md
or RESEARCH-LOG.md.

Only the `weekly-review` run acts on this file: it fixes what it can, records
the fix, and deletes the handled rows. Every other run only APPENDS.

## What belongs here

- Two files state the same rule differently (the file you are reading vs
  memory/TRADING-STRATEGY.md, or vs another prompt).
- An instruction cannot be followed — the API rejects it, a script does not
  exist, a step references a file that is not there.
- An instruction is ambiguous enough that two runs could reasonably act
  differently.

## What does NOT belong here

- "The rule is wrong / the strategy should change." That is STEP E of the
  weekly review, behind the 10-closed-trade evidence gate. This file is for
  defects, not for tuning.
- Anything about a position, a fill, a price or a P&L.

## Format — one line, append at the bottom, never rewrite an existing row

`| DATE | RUN | FILE:LINE | what the file says | what it contradicts |`

Write the contradiction so the next reader can REPRODUCE it without rerunning
anything: name both files. A row that cannot be reproduced from the row itself
gets dropped by the review, not investigated.

| Date | Run | File:line | Says | Contradicts |
|---|---|---|---|---|
| 2026-09-15 | (seeded by hand) | — | — | Inbox created empty. First real rows come from live runs. |
| 2026-09-15 | execute (18:08 UTC) | memory/TRADING-STRATEGY.md:29 | "Require a minimum 2:1 reward:risk AFTER the measured 0.65% friction" | routines/execute.md STEP E: "NO R:R REQUIREMENT, because there is no target in either sleeve to compute one against. Do NOT invent a target to satisfy a ratio." Line 29 is a stale pre-v2 (2026-09-15 rulebook rewrite) leftover never updated when targets were removed. Did not block this run (no order was gated on it), but the next run that reads TRADING-STRATEGY.md literally could demand an R:R figure that cannot exist. |
| 2026-09-15 | summary | scripts/state.sh:108 (`re.findall(r'REALIZED P&L \$(-?[0-9.]+)', log)`) | Regex requires the literal substring `REALIZED P&L $`, so it computes today's realized losses and closed-trade count for the circuit breaker / amendment trigger. | Contradicts the actual TRADE-LOG formats used for closed trades: DOT's exit (line ~328) is `**TOTAL REALIZED P&L: -$1.609**` and UNI's exit (line ~1079) is `\| **REALIZED P&L** \| **≈ -$3.17** ...\|` — neither matches, so `state.sh` printed "realized losses logged $0.00" and "closed trades logged: 0" on 2026-09-15T18:08 UTC when the true values are $3.17 realized today (2 total closed trades). Reproduce: run `bash scripts/state.sh` after this date and diff its circuit-breaker/amendment lines against a manual grep of `REALIZED P&L` in TRADE-LOG.md. Concrete impact: the 18:08 UTC execute run logged in this same file trusted the script and wrote "0 consecutive tactical losses — UNI/DOT stops are prior days, today's tally is 0", which is factually wrong (UNI closed today, 2026-09-15T14:51 UTC). |
| 2026-09-15 | summary | routines/summary.md:85-86 vs memory/TRADE-LOG.md (no snapshot 2026-09-12 to 2026-09-14) | STEP B says to read "the most recent daily snapshot (that is yesterday's equity)" and treat it as the day-over-day baseline. | Ambiguous when the most recent snapshot isn't from yesterday: no Daily Snapshot was logged 2026-09-12 through 2026-09-14, so the only prior snapshot is 2026-09-11 ($198.77), 4 days stale. The prompt does not say whether to (a) use that stale figure and call it "Day P&L" anyway, (b) fall back to the broker's `last_equity` field, or (c) flag it and abstain. This run picked (a) and labelled it a ~4-day delta in the Notes; reproduce by diffing TRADE-LOG's snapshot dates against the run dates in the file. |
