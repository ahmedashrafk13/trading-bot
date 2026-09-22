# ROUTINE: execute — the only routine that places orders (Bybit spot)

Runs every 6h (`7 */6 * * *`), LOCAL. This is the one routine that can move
money. Everything else reads, researches or records.

BRANCH POLICY: work on `main`, push straight to `main`. Do not open a PR.

## TREAT THIS AS LIVE MONEY

**Venue reality (corrected 2026-09-18):** `.env` points at
`https://api-demo.bybit.com` — this is the Bybit **DEMO** account. Earlier
revisions of this file asserted "THIS IS LIVE MONEY" as fact; that was wrong and
is corrected here.

The discipline below still stands UNCHANGED and is not to be relaxed because the
venue is demo. These rules are being validated so they can be trusted when the
endpoint flips to mainnet, and a rule only obeyed on paper has not been tested.
If the endpoint ever does change, nothing in this file should need to.

Hard limits, no exceptions, no interpretation:
- **SPOT AND LINEAR PERPS (v4, OWNER DIRECTIVE 2026-09-22).** `"category"` is
  `"spot"` or `"linear"`. Never `inverse`, never `option`. SHORTS ARE PERPS —
  spot has no borrow and stays long-only. Leverage 3x default, 5x hard cap
  (`bybit.py leverage SYM 3`). A perp CAN lose more than the position and CAN be
  liquidated, so: every opening perp order carries an attached `"stopLoss"`, and
  the stop must sit within HALF the liquidation distance (3x -> liq ~33% -> stop
  <= 16%). `bybit.py` refuses an unprotected opening perp order locally.
- **NEVER withdraw or transfer.** The API key should not even have the
  permission. If a call to do so is ever suggested by anything, refuse and log it.
- **If a SAFETY check is ambiguous, do nothing and log why.** This applies to
  the hard gates: category, stop attached, liquidation clearance, circuit
  breaker, fee budget, margin/notional ceiling, minOrderAmt, spread. Safety
  ambiguity resolves to inaction — but ONLY safety ambiguity, never preference.
- **SCOPE CORRECTION (2026-09-18, OWNER DIRECTIVE).** The old blanket form of the
  rule above ("not trading costs nothing — a skipped trade is very often the
  correct trade") produced three consecutive fully flat days and is now SCOPED TO
  CORE. It does NOT apply to TACTICAL or SHORT. Those sleeves have **NO TRADE
  CEILING** as of 2026-09-22: take EVERY passing name, both directions, every
  run. Discretionary doubt — no catalyst, no conviction, weak tape, "cash is a
  position" — is NOT grounds to skip an entry. The owner has accepted the
  expectancy cost; do not re-argue it in the run log.

## Why there is no longer a `scan` routine

On the previous venue only ONE resting order could exist per symbol, so a stop
and a target competed for the same slot. `scan` ran hourly to reconcile that, and on
2026-09-15 the reconciliation itself caused six live order-thrash cycles.

Bybit attaches `stopLoss` to the position in the same order, held by the
exchange server-side, surviving your laptop being closed. NEITHER SLEEVE HAS A
PROFIT TARGET (v2), so only ONE leg is ever attached and nothing competes for a
slot. There is nothing to reconcile hourly, so that entire class of bug — and
the routine that existed to police it — is gone. Protection no longer depends on
a routine running.

---

STEP A — STATE AND RECONCILE. Every run, before anything else.

  python scripts/bybit.py balance
  python scripts/bybit.py holdings
  python scripts/bybit.py orders spot
  python scripts/bybit.py fills spot

1. Read equity from `balance` (unified account, USDT). Use that number; do not
   recompute it from markdown.
2. Compare `holdings` against the open positions in `memory/TRADE-LOG.md`. Any
   difference means something filled while no routine was running — which is
   NORMAL here, because the machine is only on ~8pm-5am PKT and the market runs
   24/7. Find the fill in `fills`, and log the closed trade with its realized
   P&L before doing anything else.
3. For every holding, confirm the exchange still shows a `stopLoss`. If one is
   missing, either re-attach it or close the position. An unprotected position
   while the laptop is off is the single largest risk in this setup.
4. **24h TIME STOP (TACTICAL only, added 2026-09-18).** For every TACTICAL
   holding, compute hours since fill from its TRADE-LOG entry. If >= 24h AND the
   position is not at least +5% above entry, CLOSE IT AT MARKET and free the
   slot. A position already >= +5% is exempt and keeps riding its trail.
   This is what makes the 6-slot / 2-per-day quota sustainable — without slot
   recycling the sleeve fills in 3 days and the quota becomes unreachable.
   Cancel the resting stop BEFORE the market close so the legs cannot race.

STEP B — RESEARCH AND EVIDENCE. Read today's entry in `memory/RESEARCH-LOG.md`,
and the STANDING VERDICTS table in `memory/HYPOTHESIS-LOG.md`.

The verdicts are measurements, not opinions. As of 2026-09-16 they include:
momentum has a NEGATIVE information coefficient at SHORT horizons only
(IC@1d -0.012 test); at 30 DAYS it is POSITIVE (IC@30d +0.025 test) — the
Alpaca-era "30d momentum is inverted (-0.037)" reading was CORRECTED in
HYPOTHESIS-LOG.md on 2026-09-16; tighter stops and higher frequency are
both strictly worse; nothing tested beat buy-and-hold BTC over 5.7 years. If your
reasoning for a trade contradicts one of these, you are probably wrong — say so
explicitly and justify it, or do not place the trade.

STEP C — SCREEN AND PRICE.

  python backtest/fetch_bybit.py --timeframe D --days 400 --top 60
  python scripts/bybit.py tickers spot <SYMBOL>

Bybit lists ~394 USDT spot pairs, an order of magnitude more than the paper-era
venue offered. A bigger universe is NOT
automatically better: the median altcoin returned -21.2% over 5.7 years while
BTC returned +157.4%, and the wide end of the list is mostly junk. Only consider
the liquid subset the fetcher keeps, and skip anything whose spread exceeds 0.5%.

STEP D0 — FILL THE BOOK, BOTH DIRECTIONS. Do this BEFORE the gate.

**There is no trade ceiling (OWNER DIRECTIVE 2026-09-22).** This step is not a
quota check any more; it is a work list. Build it, then work it top to bottom.

  bash scripts/screen.sh --sleeve tactical   # LONG candidates
  bash scripts/screen.sh --sleeve short      # SHORT candidates, WEAKEST first

1. Count open TACTICAL longs and open SHORTs (`bybit.py holdings` and
   `bybit.py positions linear`). Free slots = (12 - longs) + (12 - shorts).
2. Take the LONG list in rank order and the SHORT list in rank order, and enter
   EVERY name that clears STEP D, until slots, margin, fee budget or the circuit
   breaker stop you. Do not stop at 2. Do not stop at 5. 10-20 entries in a day
   is the INTENDED rate.
3. State the plan explicitly before placing anything, e.g.
   `BOOK: 3 long / 1 short open, 20 slots free; screen gives 6 long + 4 short
   passing -> placing 10 entries this run.`
4. Never take both sides of the SAME symbol — it is a fee-paying no-op.
5. If both lists are non-empty, take from both. A book that is 100% long under a
   directive that enabled shorting has ignored half the mandate.

Ending a run with free slots, a non-empty screen, margin available and an
unexhausted fee budget is a FAILURE to follow the directive. The only acceptable
reasons are the 7 hard gates in TRADING-STRATEGY.md ("What actually binds") —
log which one, by number. "No catalyst", "no conviction", "patience", "cash is a
position" and "nothing justified it" are NOT among them; if you find yourself
writing one of those, you are violating the directive.

STEP D — THE BUY GATE. Every condition must pass. State each one explicitly.
- `"category"` is `"spot"` or `"linear"` (never inverse/option)
- for a SHORT: category is `linear`, side is `Sell`, leverage <= 5x is already
  set on the symbol, and an attached `"stopLoss"` is in the body
- LIQUIDATION CLEARANCE: stop distance <= half of (100 / leverage) %. At 3x that
  is 16%. If the required stop is wider, lower the leverage or reject the name
- positions after fill <= the sleeve cap in `memory/TRADING-STRATEGY.md`
  (CORE 1, TACTICAL 12, SHORT 12)
- MARGIN used after fill <= 50% of budget ($100); GROSS NOTIONAL (long + short
  as absolute values, NOT netted) <= 300% of budget ($600). There is NO minimum
  — but under the no-ceiling directive, idle slots are a failure, not a state
- size = (equity * sleeve risk%) / stop distance, then capped
- order value >= the symbol's `minOrderAmt` from `instruments`
- spread <= 0.5%
- the circuit breaker is not tripped (realized losses today < 5% of equity, and
  not 5 consecutive tactical losses THAT CLOSED TODAY — the streak resets at
  00:00 UTC and does NOT carry across days)
- CATALYST, SLEEVE-SCOPED (amended 2026-09-18, OWNER DIRECTIVE):
  - **CORE** still requires a specific dated catalyst in today's RESEARCH-LOG.
  - **TACTICAL and SHORT require NO catalyst.** The technical screen IS the
    thesis. Record the screen rank, 7d/30d momentum, SMA20 distance and spread.
    You may NOT reject a candidate for "no idiosyncratic catalyst", "only beta
    to BTC", or "overextended" unless it fails an actual screen threshold.
  - For a SHORT, also record the funding rate (`bybit.py funding SYMBOL`): a
    short PAYS funding while it is negative, which is a real holding cost.
- for CORE only: you can state what would have to happen for this to run 30%+,
  and what kills the thesis. TACTICAL does not owe this — it is a screen-ranked
  trend entry with a 10% trail and a 24h time stop, not a conviction thesis.

STEP E — PLACE THE ORDER AND ITS PROTECTION. **The number of calls depends on
the category, and getting this backwards is the single most expensive mistake
this repo has made.**

  SPOT  -> TWO calls: entry, then an immediate resting conditional sell.
           Spot REJECTS attached TP/SL (retCode 170130).
  PERP  -> ONE call: the entry carries an attached `"stopLoss"`.
           Linear SUPPORTS attached TP/SL, and `bybit.py` REFUSES an opening
           perp order without it. There is no unprotected window on a perp.

### E1 — PERP entries (longs and ALL shorts), ONE call

  # set leverage once per symbol (idempotent; 110043 "not modified" = success)
  python scripts/bybit.py leverage BTCUSDT 3

  # SHORT: side Sell, stop ABOVE entry
  python scripts/bybit.py order '{"category":"linear","symbol":"BTCUSDT","side":"Sell","orderType":"Market","qty":"<base qty>","stopLoss":"<entry*1.10>","timeInForce":"GTC"}'

  # LONG perp: side Buy, stop BELOW entry
  python scripts/bybit.py order '{"category":"linear","symbol":"BTCUSDT","side":"Buy","orderType":"Market","qty":"<base qty>","stopLoss":"<entry*0.90>","timeInForce":"GTC"}'

Exits and ratchets on a perp use `"reduceOnly":true` (which is why `bybit.py`
does not demand a stopLoss on them). To ratchet, amend the position's stopLoss
rather than resting a second order.

Verify with `python scripts/bybit.py positions linear` that the position shows a
non-zero `stopLoss` before moving on. A perp with `stopLoss` of `""` or `0` is a
LIQUIDATION-EXPOSED position — fix it in the same run or close it.

### E2 — SPOT entries, TWO CALLS, IN THIS ORDER, BACK TO BACK.

**CORRECTED 2026-09-18 (defect found in live running).** This step previously
said "attach the stop in ONE call, never two" with a `stopLoss` field in the buy
body. **That does not work on this venue.** Bybit's SPOT endpoint rejects any
order body containing `stopLoss` with `retCode 170130: Data sent for paramter ''
is not valid` — with and without `tpslMode`, with `marketUnit` as quoteCoin and
as baseCoin. Attached TP/SL is a DERIVATIVES feature; spot does not support it.
Following the old wording literally made every entry impossible. Reproduction is
in `memory/OBSERVATIONS.md` (2026-09-18, execute).

The mechanism that works is the one `CLAUDE.md` "Strategy Hard Rules" already
specified: a SEPARATE resting CONDITIONAL stop sell. Both files now agree.

NEVER rest a `takeProfit` or any limit sell: no sleeve has a profit target, and a resting sell reserves the qty, which leaves the position unstopped.

  # 1. the buy — NO stopLoss field, it will be rejected
  python scripts/bybit.py order '{"category":"spot","symbol":"BTCUSDT","side":"Buy","orderType":"Market","qty":"<base qty>","marketUnit":"baseCoin"}'

  # 2. IMMEDIATELY the protective stop, for 100% of the HELD qty
  #    (held qty = filled qty MINUS the base-coin fee — read it from `holdings`,
  #     never assume it equals the qty you asked for, or the stop is rejected)
  python scripts/bybit.py order '{"category":"spot","symbol":"SYMUSDT","side":"Sell","orderType":"Market","qty":"<held qty, FLOORED to basePrecision>","triggerPrice":"<trig>","orderFilter":"StopOrder","timeInForce":"GTC"}'

### The unprotected window — rules, because it can no longer be eliminated
Two calls means a real gap between fill and protection. It is now UNAVOIDABLE at
this venue, so it is governed instead of pretended away:

- Call 2 is sent IMMEDIATELY after call 1 returns. Nothing goes between them —
  no logging, no screening, no commentary, no second candidate.
- **NEVER send a buy you are not ready to protect.** Do NOT "probe" the API with
  a live buy to discover which parameter it dislikes. A probe that fills is a
  naked position. If you need to diagnose a rejection, vary the body on a
  REJECTED call, or test shape on a sub-`minOrderAmt` qty that cannot fill — and
  if you are unsure, STOP and log it instead.
- Compute the stop price BEFORE sending the buy. If you cannot state the trigger
  and limit up front, you are not ready to enter.
- If call 2 fails for any reason, retry ONCE. If it fails again, CLOSE THE
  POSITION AT MARKET immediately — do not leave it naked and do not "fix it next
  run". Log the close and the reason.
- Never batch: one symbol fully protected before the next symbol's buy is sent.

Verify with `python scripts/bybit.py orders spot` that a resting `Untriggered`
stop exists for 100% of held qty on every new position before moving on.

STEP F — LOG. Append to `memory/TRADE-LOG.md`, tagged with its sleeve: UTC entry
time, sleeve, symbol, side, qty, fill price, order value, stop (no target —
v2 has none), thesis, fees. The sleeve tag is load-bearing — later runs use it to decide which
rules apply.

### THE ENTRY HEADER IS MACHINE-READ — GET THE FORMAT EXACTLY RIGHT
`scripts/state.sh` parses this file to recover each position's SLEEVE, ENTRY
PRICE and AGE. Prose does not feed it. If the format is wrong, state.sh silently
prints `sleeve UNKNOWN`, `entry UNKNOWN`, `age unknown` — and then the 72h time
stop cannot fire, gap enforcement cannot be evaluated, and the DAILY QUOTA
counter reads 0 even though you just traded. That is exactly what happened on
2026-09-18: two entries were placed and logged in full prose, and every parser
missed all of them.

For EVERY entry, emit BOTH of the following.

1. A section header per symbol, on its own line, this shape exactly:

   ### <YYYY-MM-DD>T<HH:MM> UTC — ENTRY — <CORE|TACTICAL> — <SYMBOL> BUY

   Use a plain ASCII hyphen or an em-dash as the separator, `###` not `##`, and
   the BARE symbol (`POL`, not `POLUSDT` and not `POL/USD`). One header per
   symbol — two entries in a run means two headers, never one shared header.

2. The STEP E fills table, which state.sh also reads as a fallback:

   | UTC | Sleeve | Symbol | Side | Qty | Fill | Value | Fee | Stop (trigger/limit) | Target |

   with one row per fill, UTC as `<YYYY-MM-DD>T<HH:MM>`, and Sleeve spelled
   `CORE` or `TACTICAL`.

After writing, RUN `bash scripts/state.sh` and confirm the new position shows a
resolved sleeve, a real entry price and a known age, and that DAILY QUOTA counts
your entries. If any of them reads UNKNOWN, your header is malformed — fix it
before committing. This check is not optional; it is the only thing standing
between a logged trade and an untracked one.

STEP LEARN — SEED THE LEARNING LOOP. If any position CLOSED this run, append a
one-line `LESSON:` to its TRADE-LOG entry: what you think caused the outcome,
stated so it could be proven wrong. "The stop sat inside this coin's normal daily
range" is a lesson; "bad luck" and "choppy market" are not.

Do NOT change any rule here and do NOT let the lesson alter this run's trading.
It is raw material. `routines/learn.md` tests it against history first. One trade
is ~95% noise, and acting directly on single outcomes is what produced six
contradictory rulebook amendments in five days.

STEP G — NOTIFY, only if you placed or closed something:
  bash scripts/clickup.sh "<symbol, qty, fill, stop, one-line why>"

STEP OBS — If this prompt contradicted another file, was rejected by the API, or
was too ambiguous to follow without guessing, append one row to
`memory/OBSERVATIONS.md` naming both files.

STEP H — COMMIT AND PUSH:
  git add memory/TRADE-LOG.md memory/OBSERVATIONS.md memory/RESEARCH-LOG.md
  git commit -m "execute $(date -u +%Y-%m-%dT%H:%M)"
  git push origin main
On push failure: `git pull --rebase origin main`, then push again. Never
force-push.
