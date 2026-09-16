# ROUTINE: learn — turn closed trades into tested knowledge

Runs daily at 20:07 UTC, after summary. This is the routine that makes the bot
improve instead of merely remember.

BRANCH POLICY: work on `main` and push straight to `main`. Do not open a PR.

## What this routine is for

Every other routine reacts to the market. This one reacts to THE BOT. Its job is
to convert what happened into something testable, test it, and retire ideas that
are dead so they are never tried again.

The hard rule, which overrides any instinct to be helpful:

**A hypothesis drawn from a trade may NOT change any rule until it has been
tested on history and beaten a random baseline out of sample.**

One trade is ~95% noise. Acting on a single outcome is how this account amended
its rulebook six times in five days on a sample of one, with two amendments
contradicting each other. You have a backtester precisely so you never have to
guess again: it produces hundreds of outcomes in ninety seconds, and your live
account produces about three a week.

---

STEP 1 — READ STATE. In this order, and do not skip the first one:
  1. `memory/HYPOTHESIS-LOG.md` — especially the STANDING VERDICTS table. If your
     idea is already there as REJECTED or CONFIRMED, it is settled. Do not
     re-test it and do not re-propose it. Think of something new.
  2. `memory/TRADE-LOG.md` — every trade that CLOSED since the last learn run.
  3. `memory/OBSERVATIONS.md` — defects logged since the last run.

STEP 2 — ONE HYPOTHESIS PER CLOSED TRADE. Mandatory. For each trade that closed
since the last run, write a falsifiable statement about WHY it went the way it
did, in the form "X caused Y, and if that is true then Z should be measurable in
the backtest."

A hypothesis must be TESTABLE. These are not hypotheses:
  - "the market was volatile"        (not falsifiable)
  - "we should be more careful"      (not measurable)
  - "XRP was a bad pick"             (about one coin, not about a rule)
These are:
  - "stops closer than 10% fire on noise rather than on broken theses"
  - "entries taken within 6h of a CPI print lose more often than average"
  - "coins above 4% daily vol lose money regardless of signal"

If a trade closed for an obvious mechanical reason already in the STANDING
VERDICTS, say so and move on — do not manufacture a new idea to fill the row.

If NO trade closed since the last run, skip to STEP 5. Do not invent hypotheses
from open positions; an unrealized loss is not an outcome yet.

STEP 3 — SPECIFY THE TEST BEFORE RUNNING IT. For each new hypothesis, write down
the exact command AND what result would falsify it. Committing to the falsifier
in advance is what stops you from reading whatever comes back as confirmation.

  - About WHAT TO BUY -> `python backtest/research.py`. If the signal's
    information coefficient does not beat the RANDOM row out of sample, mark it
    REJECTED and STOP. Do not proceed to a backtest. A signal with no predictive
    power cannot be rescued by sizing, stops or frequency.
  - About SIZING, STOPS, FREQUENCY, CAPS -> `python backtest/run.py --set k=v`,
    compared against the unmodified default run.
  - About ROBUSTNESS -> `python backtest/sweep.py`, and read the OUT-OF-SAMPLE
    and WALK-FORWARD sections only. The in-sample winner is meaningless.

If the hypothesis needs a signal that does not exist yet, add it to
`backtest/signals.py` as a function and to `CANDIDATES`, then run research.py.
Writing a new signal is encouraged. Changing a live rule is not.

STEP 4 — RUN THE TESTS AND RECORD THE VERDICT. Append a row per hypothesis to
`memory/HYPOTHESIS-LOG.md` with its number, date, source trade, statement, the
command run, the status and the actual numbers.

Grading, applied literally:
  - `CONFIRMED` — beat the random null OUT OF SAMPLE, same sign in both halves,
    and survived walk-forward. Only this status is eligible for promotion.
  - `REJECTED` — anything else. Record the numbers anyway. A rejected hypothesis
    is a permanent saving: nobody re-tests it, including you next week.

An in-sample improvement with a worse out-of-sample result is REJECTED, not
"promising". Be strict here; the whole file is worthless if this grade is soft.

STEP 5 — TEST ONE STANDING ASSUMPTION, EVEN ON A QUIET DAY. The bot must keep
learning when it is not trading, which is most of the time. Pick one rule in
`memory/TRADING-STRATEGY.md` that has never been tested, state what it assumes,
and test it. Candidates: the 85% deployment ceiling, the 1% monthly fee budget,
the 4/1 slot split, the 06:07 research hour, the CORE/TACTICAL risk ratio, the
hard-cut levels, the universe itself.

Log the result like any other hypothesis. This is the step that compounds — a
year of it means every rule in the book has evidence behind it rather than an
origin story.

STEP 6 — PROMOTE, at most ONE change per run. If any hypothesis is CONFIRMED,
you may now edit `memory/TRADING-STRATEGY.md` to apply it. Requirements:
  - at most ONE rule changed per run, so the next result is attributable
  - cite the hypothesis number and its out-of-sample numbers in the edit
  - set that hypothesis to `PROMOTED` with today's date
  - if two are CONFIRMED, promote the one with the larger out-of-sample effect
    and leave the other CONFIRMED for next time

If nothing is CONFIRMED, change NOTHING. A run that tests three ideas, rejects
all three and edits no rules is a fully successful run. Most runs will look like
this, and that is the system working.

STEP OBS — If this prompt contradicted another file or was too ambiguous to
follow, append one row to `memory/OBSERVATIONS.md` naming both files.

STEP 7 — COMMIT AND PUSH:
  git add memory/HYPOTHESIS-LOG.md memory/TRADING-STRATEGY.md memory/OBSERVATIONS.md backtest/
  git commit -m "learn $(date -u +%Y-%m-%d): <n> tested, <n> confirmed, <n> rejected"
  git push origin main
On push failure: `git pull --rebase origin main`, then push again. Never
force-push.

---

## What good looks like

A good learn run is usually boring: two hypotheses drawn, both tested, both
rejected, nothing changed, three lines added to the log. Over a month that is
~60 tested ideas and a rulebook where every surviving rule has evidence.

A bad learn run changes a rule because a trade lost. That is the failure mode
this entire routine exists to prevent.
