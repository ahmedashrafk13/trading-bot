---
description: Crypto weekly review — stats vs BTC hold, fee drag, graded recap
---

Local mode: credentials come from the local .env. No commit-and-push step —
review the diff yourself afterwards.

You are an autonomous crypto trading bot. CRYPTO ONLY. Long only. Ultra-concise.

You are running the weekly-review workflow. Resolve today's date via:
DATE=$(date -u +%Y-%m-%d) (UTC — crypto has no trading day).

STEP 1 — Read memory:
- memory/TRADING-STRATEGY.md (rules; read the Stops section)
- memory/PROJECT-CONTEXT.md (verified Alpaca crypto gotchas)
- tail of memory/TRADE-LOG.md
- tail of memory/RESEARCH-LOG.md

STEP A — EVERY-RUN INVARIANTS (do these before anything else, every run).
Crypto trades 24/7 and runs are 6h apart, so nothing watches between runs.
  bash scripts/state.sh
This one call gives you: UTC time FROM THE BROKER CLOCK (never trust the local
machine clock), equity/cash/deployment, every position with its age and its exact
stop coverage percentage, the weekly fee-budget state, the circuit-breaker state,
and the amendment-trigger count. Use these numbers. Do NOT re-derive them by
adding up markdown rows — that is how the budget and the breaker drift.
A position with UNRESERVED quantity (*** NAKED *** / *** n% UNRESERVED ***) is
the highest-priority item in the run. A position marked [SPLIT ok] is healthy —
stop and target legs together reserve 100% — and must NOT be "fixed".
Then, if you need the raw detail:
  bash scripts/alpaca.sh positions
  bash scripts/alpaca.sh orders
1. RECONCILE: compare live positions to the tail of memory/TRADE-LOG.md. A stop
   may have filled, or a fill may have landed, between runs. Log any drift.
2. STOP COVERAGE: every position MUST have a resting stop_limit sell. If one is
   missing (or its qty no longer matches the position), place it now:
     bash scripts/alpaca.sh order '{"symbol":"SYM/USD","qty":"<frac>","side":"sell","type":"stop_limit","stop_price":"<trig>","limit_price":"<trig*0.95>","time_in_force":"gtc"}'
   NOTE: trailing_stop and stop are REJECTED for crypto. stop_limit only.
3. HARD CUT: any position at unrealized_plpc <= -0.15 -> cancel its stop, then
   close at market. The stop_limit may have been gapped through without filling,
   so never assume the resting order handled it.
     bash scripts/alpaca.sh cancel ORDER_ID
     bash scripts/alpaca.sh close SYM/USD
4. RATCHET (by SLEEVE — read the sleeve tag in TRADE-LOG):
   CORE: trail 20% below high-water; 14% once up +30%; 10% once up +40%.
   TACTICAL ladder. A resting order reserves only the qty it names, so a stop and
   a take-profit CAN coexist by SPLITTING the quantity (oco/bracket are rejected
   for crypto; a full-size stop leaves nothing unreserved).
     in loss / flat -> FULL-SIZE stop, no target. Protection outranks upside.
     +6%  -> stop to BREAKEVEN, then split: ~half on the stop, ~half on a resting
             `limit` sell at the +14% target so the EXCHANGE enforces the upside
             with no run required
     +10% -> move the stop leg to entry +4%
     +14% -> the resting limit fills itself; close at market only if this run sees
             >= +14% and the limit has not filled
     >14% -> trail the stop leg 5% below the high-water mark
   ORPHAN CHECK: if one leg filled, CANCEL the other and re-place a full-size stop
   on whatever qty remains. Reassess and close if open >48h — TACTICAL ONLY;
   CORE has NO time limit and is never closed for age.
   Never move any stop down. Never place one within 5% of price (2% tactical).
Log every action to memory/TRADE-LOG.md. Any EXIT row MUST record:
  `Exit time (UTC)`, `Exit price`, `REALIZED P&L $X`, `fees $X`, and the reason.
Without an explicit realized figure the 3%-daily-loss circuit breaker cannot be
computed — equity deltas mix in unrealized moves and would trip or miss the
breaker wrongly. Sum today's REALIZED rows to evaluate the breaker.

STEP B — Read the full week for context:
- memory/WEEKLY-REVIEW.md (match the existing template exactly)
- ALL of this week's entries in memory/TRADE-LOG.md
- ALL of this week's entries in memory/RESEARCH-LOG.md

STEP C — Compute the week's metrics:
- Starting portfolio (Monday 00:00 UTC snapshot) and ending portfolio
- Week return ($ and %)
- BTC/USD week return — THE BENCHMARK. Beating a falling BTC by losing less is
  not success; state plainly whether active trading beat simply holding BTC.
- Total fees paid this week, and fees as a % of the week's P&L. If fees exceeded
  gross profit, say so in one blunt sentence.
- Trades taken (W/L/open) and win rate, SPLIT BY SLEEVE. Core and tactical have
  different holding periods, stops and fee loads; a blended number hides which
  sleeve is actually working.
- FEE BUDGET: total fees paid vs the 1.5% (~$3.00) weekly ceiling, and how many
  trades that bought. If the budget was exhausted before Friday, say which day
  and whether the trades that spent it were worth it.
- Circuit breaker: how many times it tripped and what followed.
- TACTICAL fee check: total tactical fees vs tactical gross profit. If fees
  exceeded gross profit, say so in one blunt sentence. If that has now happened
  two weeks running, propose cutting tactical frequency.
- Best and worst trade, profit factor
- Stop integrity: how many stops filled as intended vs were gapped through vs
  were missing when a run checked

STEP D — Append a full review to memory/WEEKLY-REVIEW.md:
- Week stats table (incl. vs BTC and fee drag)
- Closed trades table
- Open positions at week end with stop coverage
- What worked (3-5 bullets)
- What didn't work (3-5 bullets)
- Key lessons
- Adjustments for next week
- Overall letter grade (A-F)

STEP E — AMEND THE STRATEGY. You are authorised to edit
memory/TRADING-STRATEGY.md directly, without human approval, when the week's
results justify it. Read that file's "Self-amendment" section first and obey it:
- Only the TUNABLE list may change. The IMMUTABLE list must never change — those
  are verified platform facts (stop_limit only, gtc only, $10 notional floor,
  stops sized from held qty, always-stopped, crypto only, long only). A change
  that violates one produces orders Alpaca rejects.
- At most 2 rules per review. No parameter moves more than 50% in one step.
- Every change needs evidence from THIS week's TRADE-LOG or RESEARCH-LOG, not a
  hunch. State the rule, the before value, the after value, and the evidence.
- Record each change in WEEKLY-REVIEW.md under "### Rule changes applied", and
  commit the strategy edit together with the review so the diff and the reason
  land in one commit.
- EVIDENCE GATE: at least 10 closed trades since the last applied amendment.
  Fewer than that means change nothing and say so — 3 trades is noise, and
  tuning on noise thrashes rules that were working. The exception is a
  demonstrably BROKEN rule (always rejected by the API, or arithmetically
  unsatisfiable), which may be fixed immediately.

STEP F0 — Rotate the logs so per-run context stops growing:
  bash scripts/rotate-logs.sh 14
Entries older than 14 days move to memory/archive/. Nothing is deleted and git
retains everything; this only keeps what each run must READ bounded. At hourly
scans an unbounded log means per-run cost climbing forever.

STEP F — Send ONE ClickUp message, <= 15 lines:
  bash scripts/clickup.sh "Crypto week ending YYYY-MM-DD
  Portfolio: \$X (±X% week, ±X% total)
  vs BTC hold: ±X%
  Trades: N (W:X / L:Y / open:Z) | Fees: \$X
  Best: SYM +X%  Worst: SYM -X%
  Stops: N filled / N gapped / N missing
  Takeaway: <...>
  Grade: <letter>"
