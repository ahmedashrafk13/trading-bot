# Bootstrap prompts — paste these ONCE, never re-paste again

## Current setup: Bybit spot, LOCAL, live money

Five routines, all run on your own machine. Times are UTC; Pakistan is UTC+5, so
a machine awake 8pm-5am PKT covers roughly 15:00-00:00 UTC. Every cadence below
is chosen to land inside that window — a routine scheduled while the laptop is
off simply does not run.

| routine | cron (UTC) | PKT | places orders? |
|---|---|---|---|
| research | `7 15 * * *` | 8:07 pm | no |
| execute  | `7 16,20 * * *` | 9:07 pm, 1:07 am | **YES** |
| summary  | `7 22 * * *` | 3:07 am | no |
| learn    | `7 23 * * *` | 4:07 am | no |
| weekly-review | `37 23 * * 0` | 4:37 am Mon | no |

Positions are protected by exchange-side stops, so the hours the machine is off
carry no unprotected exposure.

## The problem these solve

`routines/*.md` were pasted VERBATIM into each cloud routine. That makes every
routine a frozen snapshot of the rulebook at paste time. When the repo changed
and the paste did not, the two disagreed — and on 2026-09-15 that produced six
live order-thrash cycles in one day: `execute` placed target legs per the repo
while `scan` cancelled them per a months-stale pasted prompt. Both runs were
obeying their instructions. The instructions were different.

A pasted prompt cannot be fixed by editing the repo. It has to be re-pasted, by
hand, every single time any rule changes — across five routines. That will fail
again, because it always fails eventually.

## The fix

Paste a 4-line BOOTSTRAP instead of the routine body. The bootstrap does one
thing: read the routine file from the freshly cloned repo and follow it. The
repo then becomes the single source of truth for real, and a rule change takes
effect on the next run with no re-pasting anywhere.

Paste these once. After that, `git push` is the only deployment step forever.

---

## scan — DELETED (2026-09-16, Bybit migration)

Do NOT create this routine. Delete it if it exists.

It existed only because Alpaca allowed ONE resting order per symbol, so a stop
and a target competed for the same slot and had to be reconciled hourly. That
reconciliation is itself what caused six live order-thrash cycles on 2026-09-15.

Bybit attaches `takeProfit` AND `stopLoss` to the position in the same order.
Both legs are held server-side by the exchange and survive the laptop being
closed, so there is nothing to reconcile. Protection no longer depends on a
routine running — which matters here, because this setup is LOCAL and the
machine is off for most of the day.

The old file is kept at `routines/archive/scan-alpaca-era.md` for history only.

## execute  (`7 */6 * * *`)

```
Read the file routines/execute.md in this repository and follow it exactly, from
the first line to the last, as if its full text had been given to you directly
as your instructions for this run.

That file is the ONLY authority for this run. If anything in this prompt, in
your memory, or in any summary you have seen disagrees with it, the file wins.
Do not substitute remembered rules for what the file says; do not skip steps
because a step looks routine. If routines/execute.md cannot be read, STOP,
report that plainly, and place no orders.
```

## research  (`7 6 * * *`)

```
Read the file routines/research.md in this repository and follow it exactly,
from the first line to the last, as if its full text had been given to you
directly as your instructions for this run.

That file is the ONLY authority for this run. If anything in this prompt, in
your memory, or in any summary you have seen disagrees with it, the file wins.
If routines/research.md cannot be read, STOP and report that plainly.
```

## summary  (`7 18 * * *`)

```
Read the file routines/summary.md in this repository and follow it exactly, from
the first line to the last, as if its full text had been given to you directly
as your instructions for this run.

That file is the ONLY authority for this run. If anything in this prompt, in
your memory, or in any summary you have seen disagrees with it, the file wins.
If routines/summary.md cannot be read, STOP and report that plainly.
```

## weekly-review  (`37 18 * * 0`)

```
Read the file routines/weekly-review.md in this repository and follow it exactly,
from the first line to the last, as if its full text had been given to you
directly as your instructions for this run.

That file is the ONLY authority for this run. If anything in this prompt, in
your memory, or in any summary you have seen disagrees with it, the file wins.
Rule changes now flow through the learn routine, which tests every hypothesis
before promoting it. If this review wants a rule changed, it writes a hypothesis
into memory/HYPOTHESIS-LOG.md rather than editing memory/TRADING-STRATEGY.md on
a week of noise. If routines/weekly-review.md cannot be read, STOP and report
that plainly.
```

## learn  (`7 20 * * *`)

NEW ROUTINE — create this one in the Routines panel, it does not exist yet.
This is the routine that makes the bot improve rather than merely remember:
every closed trade becomes a falsifiable hypothesis, every hypothesis is tested
against history in `backtest/`, and only results that beat a random baseline out
of sample are allowed to change a rule.

```
Read the file routines/learn.md in this repository and follow it exactly, from
the first line to the last, as if its full text had been given to you directly
as your instructions for this run.

That file is the ONLY authority for this run. If anything in this prompt, in
your memory, or in any summary you have seen disagrees with it, the file wins.

This run PLACES NO ORDERS and TOUCHES NO POSITIONS under any circumstance. It
reads history, forms hypotheses, tests them with the backtester, and records
verdicts. If you find yourself about to call scripts/bybit.py with anything
other than a read-only subcommand, you have misread the routine — stop.

You MAY edit memory/TRADING-STRATEGY.md, but ONLY to promote a hypothesis that
this run has tested and graded CONFIRMED, and at most ONE rule per run. A
hypothesis that has not been tested against history must not change anything,
however obvious it seems: one trade is ~95% noise, and acting on single outcomes
is what produced six contradictory amendments in five days on this account.

If routines/learn.md cannot be read, STOP and report that plainly.
```

---

## What does NOT change

Everything in README.md's one-time prerequisites still applies to each routine,
because it is configured on the routine and not in the prompt:

- the Claude GitHub App installed on this repo (clone + push)
- network access Full, or Custom allowing `paper-api.alpaca.markets`,
  `data.alpaca.markets`, `api.alpaca.markets`, `api.perplexity.ai`,
  `api.clickup.com`
- `ALPACA_API_KEY`, `ALPACA_SECRET_KEY`, `ALPACA_ENDPOINT` set as routine env
  vars — never in a `.env` file
- the cron expression and timezone (UTC)

## How to verify a routine is on the bootstrap

Its next run's transcript should begin by READING `routines/<name>.md`. If a run
starts executing steps without reading the file first, that routine is still on
a pasted copy and is a thrash risk.
