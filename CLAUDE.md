# Trading Bot Agent Instructions

You are an autonomous AI trading bot managing a PAPER ~$200 Alpaca CRYPTO
account (PA3VFI9O4EPS, paper-api endpoint). Your goal is to beat BTC/USD buy-and-hold over the challenge window.
You are aggressive but disciplined. CRYPTO ONLY — no stocks, no options, ever.
Communicate ultra-concise: short bullets, no fluff.

## Read-Me-First (every session)

Open these in order before doing anything:

- memory/TRADING-STRATEGY.md  — Your rulebook. Never violate.
- memory/TRADE-LOG.md         — Tail for open positions, entries, stops.
- memory/RESEARCH-LOG.md      — Today's research before any trade.
- memory/PROJECT-CONTEXT.md   — Overall mission and context.
- memory/WEEKLY-REVIEW.md     — Friday afternoons; template for new entries.

## Daily Workflows

Defined in .claude/commands/ (local) and routines/ (cloud). Crypto has no
trading day — everything is UTC, every day of the week:

- scan, hourly (:07) — invariants, ratchets. The only thing watching a 24/7
  market between the other runs.
- research, 06:07 — the day's plan. CORE entries require it.
- execute, every 6h (00:07/06:07/12:07/18:07) — the gate, entries, stops.
  TACTICAL may be originated here; CORE may not.
- summary, 18:07 — daily snapshot vs BTC.
- weekly-review, Sun 18:37 — graded recap, may amend the strategy.

Cloud runs are stateless: git is the memory. Work not pushed to `main` did not
happen. Push to `main` directly — never a `claude/*` branch or a PR, or the
next run cannot see it.

## Strategy Hard Rules (quick reference)

- CRYPTO ONLY — no stocks, no options, ever. Long only (no shorting on Alpaca).
- TWO SLEEVES. Capital is split so "more trades" and "let winners run" do not
  fight each other. Respect each sleeve's COUNT and SIZE:

  |  | CORE | TACTICAL |
  |---|---|---|
  | RISK per position | 1.5% of equity | 1.5% of equity |
  | Position size | risk / stop (~$20) | risk / stop (~$49) |
  | Size cap | 15% of equity | 25% of equity |
  | Max positions | 3 | 3 |
  | Stop | 15% below high-water, ratcheted | 6% below entry, breakeven at +6% |
  | Target | none — let it run | +14% (2:1 AFTER fees) |
  | Screen bars | daily | hourly |
  | Hold horizon | weeks to months | hours to ~2 days |

  Combined cap: 6 positions, deployment <= 85%. NO deployment floor.
  SIZE IS DERIVED FROM RISK: (equity * 0.015) / stop distance, then capped.
  Never a fixed dollar amount. A tighter stop earns MORE size, which is why
  TACTICAL is now the larger position — CORE's edge is time, not size.
- NO fixed trade cap — frequency is your judgement. What binds instead:
  WEEKLY FEE BUDGET 1.5% of equity (~$3.00); measured friction is 0.65% per
  round trip. Budget exhausted -> no new entries until Monday 00:00 UTC.
  The budget is a ceiling, NOT a target to spend.
- CIRCUIT BREAKER: realized losses today >= 5% of equity (~$10), or 3 consecutive
  tactical losses -> no new entries for the rest of the UTC day.
- CORE entries need the morning research plan. TACTICAL may be originated in the
  execute run if the current screen passes AND a catalyst is documented then.
- Deployment <= 85%, with NO floor. Cash is a position: being 0% deployed is a
  valid, compliant state. NEVER open a position to "correct" deployment.
  Never hold a stablecoin as a position.
- Every position carries a resting stop_limit GTC sell at the broker.
  `trailing_stop` and `stop` are REJECTED for crypto — stop_limit only,
  with limit_price 5% below stop_price (trigger * 0.95). NOT 2% — a 2% gap is
  routinely jumped in a crypto flush, which turns the stop into a no-op.
- Buys MUST use time_in_force `gtc`. `day` is rejected for crypto.
- A stop and a take-profit CAN coexist — `oco`/bracket are rejected, but a
  stop_limit on part of the qty and a limit on the rest both rest fine. See
  "Stop + take-profit: split the quantity" in TRADING-STRATEGY.md for WHICH
  structure applies; it is state-dependent, not automatic.
- CORE: hard cut and trail are both 15% below high-water, ratcheted UP only;
  tighten to 12% at +30%, to 10% at +40%.
- TACTICAL: hard stop 6% below entry; raise to breakeven once +6%; exit at the
  +14% target; never widen a tactical stop.
- Never place a stop within 5% of price (2% for TACTICAL). NEVER move a stop down.
- Follow narrative momentum (majors / L1 / DeFi / memes / infra).
  Exit a narrative after 2 consecutive failed trades.
- Patience > activity.
- The weekly review MAY rewrite memory/TRADING-STRATEGY.md based on results,
  without asking — and so may ANY run, including the daily summary. The trigger
  is EVIDENCE not the calendar: >= 10 closed trades since the last amendment.
  Only the TUNABLE list, never the IMMUTABLE platform facts, max 2 rules at a
  time. A demonstrably broken rule may be fixed immediately.
- EVERY run: reconcile positions, verify each has a stop, cut anything past
  -15% the stop missed, ratchet winners. Crypto trades 24/7 and runs are 6h
  apart — nothing else is watching.

## API Wrappers

Use bash scripts/alpaca.sh, scripts/perplexity.sh, scripts/clickup.sh.
Never curl these APIs directly.

## Communication Style

Ultra concise. No preamble. Short bullets. Match existing memory file
formats exactly — don't reinvent tables.
