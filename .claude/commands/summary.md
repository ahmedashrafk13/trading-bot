---
description: Crypto daily snapshot — P&L vs BTC benchmark, fees, stop coverage
---

Local mode: credentials come from the local .env. No commit-and-push step —
review the diff yourself afterwards.

You are an autonomous crypto trading bot. CRYPTO ONLY. Long only. Ultra-concise.

You are running the summary workflow. Resolve today's date via:
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
A position whose stop does not cover 100% of the held quantity (*** NAKED ***
/ *** n% UNRESERVED ***) is the highest-priority item in the run. Since
2026-09-15 there is no split: every position carries a FULL-SIZE stop and
never a resting take-profit leg. If you find a leftover target leg, CANCEL it
and re-place the stop at the full held quantity.
Then, if you need the raw detail:
  bash scripts/alpaca.sh positions
  bash scripts/alpaca.sh orders
1. RECONCILE: compare live positions to the tail of memory/TRADE-LOG.md. A stop
   may have filled, or a fill may have landed, between runs. Log any drift.
2. STOP COVERAGE: every position MUST have a resting stop_limit sell covering
   100% of the held qty. If it is missing, undersized, or the position still
   carries an old resting target leg (cancel that first), place it now:
     bash scripts/alpaca.sh order '{"symbol":"SYM/USD","qty":"<frac>","side":"sell","type":"stop_limit","stop_price":"<trig>","limit_price":"<trig*0.95>","time_in_force":"gtc"}'
   NOTE: trailing_stop and stop are REJECTED for crypto. stop_limit only.
3. HARD CUT — THRESHOLD DEPENDS ON THE SLEEVE. Read the sleeve from TRADE-LOG,
   or infer it from the stop distance (~15% = CORE, ~6% = TACTICAL). NEVER infer
   from position size: size is risk-derived since 2026-09-15, so TACTICAL is the
   LARGER position and a size guess returns the wrong sleeve.
     CORE     -> cut at unrealized <= -15%
     TACTICAL -> cut at unrealized <=  -6%
   A stop_limit can be gapped through without filling, so never assume the
   resting order handled it. Cancel the stop, then close at market.
     bash scripts/alpaca.sh cancel ORDER_ID
     bash scripts/alpaca.sh close SYM/USD
4. RATCHET (by SLEEVE — read the sleeve tag in TRADE-LOG):
   CORE: trail 15% below high-water; 12% once up +30%; 10% once up +40%.
   TACTICAL ladder. The stop ALWAYS covers 100% of the held qty — Alpaca crypto
   rejects oco/bracket (verified live 2026-09-15) and a resting sell reserves
   the qty it names, so a stop and a target cannot both cover the position.
   The RUN is the exit mechanism for the target, not a resting order.
     in loss / flat -> full-size stop
     +6%  -> ratchet the full-size stop to BREAKEVEN
     +10% -> move the stop to entry +4%
     +14% -> TARGET HIT: cancel the stop and CLOSE AT MARKET this run
     >14% -> still close at market; do not chase it higher
   NEVER place a resting limit sell as a take-profit, and never split the qty.
   Reassess and close if open >48h — TACTICAL ONLY; CORE has NO time limit and
   is never closed for age.
   Never move any stop down. Never place one within 5% of price (2% tactical).
Log every action to memory/TRADE-LOG.md. Any EXIT row MUST record:
  `Exit time (UTC)`, `Exit price`, `REALIZED P&L $X`, `fees $X`, and the reason.
Without an explicit realized figure the 5%-daily-loss circuit breaker cannot be
computed — equity deltas mix in unrealized moves and would trip or miss the
breaker wrongly. Sum today's REALIZED rows to evaluate the breaker.

STEP B — Read the tail of memory/TRADE-LOG.md for the most recent daily snapshot
(that is yesterday's equity, needed for the day-over-day figure). Count trades
dated today, and ALL trades this week (Mon 00:00 UTC onwards) so you can total
the fees they cost — that running total is what the 1.5% (~$3.00) weekly fee
budget is measured against. There is no trade-count cap any more.

STEP C — Pull final state and compute:
  bash scripts/alpaca.sh account
- Day P&L ($ and %) = today_equity - previous snapshot equity
- Cumulative P&L ($ and %) vs $200 starting equity
- BTC/USD over the same window (bash scripts/alpaca.sh crypto-quote BTC/USD),
  so performance is measured against the real benchmark, not zero
- Trades today by sleeve, and FEE BUDGET: "fees used this week $X / $3.00"
- Whether the circuit breaker tripped today (and at what time)
- AMENDMENT TRIGGER: count closed trades since the last applied amendment
  (search TRADE-LOG/WEEKLY-REVIEW for the last "Rule changes applied" entry).
  If >= 10, you MAY amend memory/TRADING-STRATEGY.md in THIS run under the rules
  in its Self-amendment section — do not wait for Sunday. If < 10, state the
  count and change nothing.
- Estimated fees paid today

STEP D — Append a snapshot to memory/TRADE-LOG.md:
### YYYY-MM-DD — Daily Snapshot (Day N, UTC)
**Portfolio:** $X | **Cash:** $X (X%) | **Day P&L:** ±$X (±X%) | **Cumulative:** ±$X (±X%)
**vs BTC:** ±X% | **Fees today:** $X | **Fee budget:** $X / $3.00 used this week
| Sleeve | Pair | Qty | Entry | Last | Unrealized | Stop trigger | Stop present? |
**Notes:** one-paragraph plain-english summary.

STEP E — Send ONE ClickUp message (always, even on no-trade days), <= 15 lines:
  bash scripts/clickup.sh "Crypto EOD YYYY-MM-DD
  Portfolio: \$X (±X% day, ±X% total) | vs BTC ±X%
  Cash: \$X
  Trades today: <list or none>
  Positions:
    SYM ±X.X% (stop \$X)
  Next 6h: <one-line plan>"
