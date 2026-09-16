# Bootstrap prompts — paste these ONCE, never re-paste again

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

## scan  (`7 * * * *`)

```
Read the file routines/scan.md in this repository and follow it exactly, from
the first line to the last, as if its full text had been given to you directly
as your instructions for this run.

That file is the ONLY authority for this run. If anything in this prompt, in
your memory, or in any summary you have seen disagrees with it, the file wins.
Do not substitute remembered rules for what the file says; do not skip steps
because a step looks routine. If routines/scan.md cannot be read, STOP, report
that plainly, and do nothing else — do not improvise a scan from memory.
```

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
verdicts. If you find yourself about to call scripts/alpaca.sh with anything
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
