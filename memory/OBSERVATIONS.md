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
| 2026-09-17 | weekly-review | — | Inbox CLEARED by the 2026-09-17 weekly review. 12 reproducible contradictions were repaired (see memory/WEEKLY-REVIEW.md, "Instruction repairs applied"); ~28 rows were dropped as unreproducible or already-fixed (see "Observations dropped as unreproducible"); 3 were KEPT as out-of-scope for a text-only repair and are listed under "Observations KEPT" and "ACTION FOR THE HUMAN" in that review. | — |
| 2026-09-18 | research | memory/TRADING-STRATEGY.md:"## Self-amendment — OPEN. Any run may amend (owner directive, 2026-09-16)" and its "TRIGGER: none. Amend whenever the evidence warrants." | The rulebook states that ANY run (scan, execute, research, summary, weekly-review) may edit memory/TRADING-STRATEGY.md at any time with no minimum trade count, the freeze having been removed by owner directive 2026-09-16. | routines/research.md, final section "AMENDMENT FREEZE (v2)": "this run may NEVER edit memory/TRADING-STRATEGY.md. ONLY the weekly-review run may, and only behind its own evidence gate" — and CLAUDE.md "Strategy Hard Rules": "AMENDMENT FREEZE. ONLY the weekly-review run may edit memory/TRADING-STRATEGY.md, and ONLY at >= 10 closed trades". scripts/state.sh prints the >=10 gate as live ("AMENDMENT TRIGGER ... need >= 10 | status: not eligible"), agreeing with the routines and contradicting the rulebook. Three files (routines/research.md, CLAUDE.md, scripts/state.sh) say frozen-and-gated; one (memory/TRADING-STRATEGY.md) says open-and-ungated. Moot this run — nothing was amended, the stricter reading was followed. |
