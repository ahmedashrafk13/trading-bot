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

STEP 0 — MAKE THE BACKTESTER RUNNABLE. Before anything else:
  python backtest/cache.py unpack
  python backtest/test_engine.py

`unpack` expands the committed Bybit daily bar cache (60 liquid USDT spot
pairs, ~4.1 years) into data/bars/D/. It is
idempotent and takes a second; the per-symbol hourly cache is gitignored and
would cost ~15 minutes of API calls to rebuild, which is longer than this run
should take.

`test_engine.py` must print "all invariants hold". If it does NOT, the
backtester is lying and every verdict this run produces would be worthless.
STOP: change no rules, log the failure to memory/OBSERVATIONS.md, notify via
scripts/clickup.sh, and end the run. A broken measuring instrument is worse than
no measurement, because its output still looks like evidence.

If a specific backtest command errors mid-run, do NOT guess the result and do
NOT fall back to reasoning it out from the trade log. Mark that hypothesis
`TESTING` with the error text, and move to the next one.

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

  - About WHAT TO BUY -> `python backtest/research.py --timeframe D`. If the signal's
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

STEP 4B — GENERATE YOUR OWN IDEAS. Do not wait for a losing trade to think.
Every run, propose at least TWO new signals that nothing in HYPOTHESIS-LOG has
tested, write them as real code, and measure them. This is the step that makes
the bot a researcher rather than a record-keeper.

Where to look for candidates, in rough order of remaining promise:

  1. NON-PRICE DATA. Every price-derived idea is close to exhausted — momentum,
     reversal, volatility, breakout and relative strength have all been measured
     at every horizon, long-only and long/short. The unexplored data is:
       - funding rate (`/v5/market/funding/history`) — a crowding measure, not a
         price derivative. Extreme funding precedes squeezes. Best remaining bet.
       - open interest (`/v5/market/open-interest`) — leverage build-up.
       - long/short account ratio, order-book imbalance, basis vs spot.
     Add a fetcher for these under `backtest/` if one does not exist yet.
  2. COMBINATIONS. A weak signal conditioned on another can beat either alone —
     e.g. momentum ONLY when funding is negative, or reversion ONLY in the
     bottom volatility tercile.
  3. WEB RESEARCH. You may use WebSearch for published crypto factor research,
     then implement and TEST what you find. Never adopt a claim because a paper
     or a post asserts it; the whole point of this routine is that claims get
     measured on our data before they touch the account.

Write each candidate as a function in `backtest/signals.py`, register it in
`CANDIDATES`, and run `python backtest/research.py --timeframe D`. That is a
cheap, fully reversible experiment — new signal code changes NOTHING about live
trading until STEP 6 promotes it.

THE SKEW CHECK — MANDATORY before proposing any short leg. A positive
information coefficient is NOT sufficient to justify shorting. IC measures the
MEDIAN relationship; P&L is paid on the MEAN. Low volatility beats high
volatility on 30d median by 5.0pp and LOSES on mean by 4.6pp, because high-vol
crypto returns are lottery-shaped (p99 +207%, max +832%). `neutral.py` lost 93%
learning this. So for any signal you intend to short, report the mean AND the
median of forward returns for both tails, and if the mean disagrees with the
median, the short leg is rejected regardless of its IC.

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

STEP NOTIFY — Report what was learned, always, even on a quiet run:
  bash scripts/clickup.sh "learn: <n> tested, <n> confirmed, <n> rejected — <the single most interesting verdict, or 'nothing changed'>"
This is the only visibility into whether the loop is working without opening the
repo, so it runs on quiet days too.

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

A good learn run is usually boring: two or three ideas proposed, all tested, all
rejected, nothing changed, a few lines added to the log. Over a month that is
~60-90 tested ideas and a rulebook where every surviving rule has evidence.

Rejecting your own idea is the job, not a failure. The owner's instinct that
"some coin is always up 2% while another is down, so there must be money there"
is correct about the dispersion and wrong about the difficulty: capturing it
requires predicting WHICH coin, and the best signal measured so far is right
about 53% of the time. Your job is to keep hunting for the signal that does
better, and to be honest every time one does not.

A bad learn run changes a rule because a trade lost. That is the failure mode
this entire routine exists to prevent.
