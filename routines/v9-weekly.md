# v9 weekly review — Sunday 13:37 PKT (08:37 UTC)

Read-only for the market: this routine places NO orders. Work from the repo root.
Goal: measure honestly, keep Claude's lessons current, and flag (not enact)
strategy changes. One week of a strategy that wins ~45% of trades is mostly
noise — judge on the running totals, not the week.

## 1. Measure

    python scripts/v9.py status
    python scripts/v9.py scorecard
    python scripts/v9.py revalidate

Record: P&L since the v9 start and this week (from `memory/V9-JOURNAL.md` /
status), drawdown from peak, Claude's value-add by action type, maker-fill share
(backtest assumed 70%), paper return of the frozen strategy over 30/60/90 days,
and live-vs-paper gap (execution cost + Claude's overrides).

## 2. Judge against pre-committed ranges

- Paper 90d return below about −25% at vol 0.55 = outside the tested range →
  write `EDGE ALERT` in the review and recommend the owner lower the risk level
  or pause. Do not change VOL_TARGET yourself.
- Maker-fill share below 40% → the fee assumption is wrong; note it (at 0% maker
  the tested return roughly halves).
- Live P&L far below paper over 4+ weeks → execution or overrides are costing
  money; say which, with the scorecard numbers.
- Claude's value-add negative over 60+ scored runs → the lesson is to override
  less; say so in the lessons file.

## 3. Update `memory/V9-LESSONS.md`

Keep it under ~15 bullets. Add or revise lessons ONLY when the scorecard supports
them (state the numbers and sample size). Remove lessons the data no longer
supports. This file is what the 6h runs read to improve Claude's judgement.

## 4. Strategy changes: propose, never enact

If the evidence suggests a change to the strategy itself (signal, threshold,
vol target, universe), write it up in `memory/V9-REVIEW.md` as a PROPOSAL with
the numbers, and name the lab test that would confirm it (`backtest/lab/`,
walk-forward, then a single out-of-sample check). The owner approves changes;
scheduled runs never edit `scripts/v9.py`, `scripts/checks.py` or VOL_TARGET.

## 5. Record

Append the week's entry to `memory/V9-REVIEW.md` (date, P&L, drawdown, paper
90d, Claude value-add, maker share, alerts, proposals), then

    git add memory/V9-REVIEW.md memory/V9-LESSONS.md
    git commit -m "v9 weekly review <date>"
    git push origin main

Push straight to `main` (never a `claude/*` branch or a PR). If the push is
rejected because the remote moved, run `git pull --rebase origin main` and push
again. If it still fails (network), say so in the reply and move on - the commit
is safe locally and the next run pushes it. Never let a push problem delay or
change trading.

Reply with a 5-line summary for the owner: P&L, how it compares with the tested
range, whether Claude's decisions are helping, any alert, any proposal.
