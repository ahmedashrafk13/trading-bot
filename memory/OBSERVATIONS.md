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
