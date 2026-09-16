# ROUTINE: execute — the only routine that places orders (Bybit spot)

Runs every 6h (`7 */6 * * *`), LOCAL. This is the one routine that can move
money. Everything else reads, researches or records.

BRANCH POLICY: work on `main`, push straight to `main`. Do not open a PR.

## THIS IS LIVE MONEY

The Alpaca era was a $200 paper account where a bug cost nothing. Bybit is real.
Every rule below that looks paranoid is there because the failure it prevents now
has a price.

Hard limits, no exceptions, no interpretation:
- **SPOT ONLY.** Every order body must carry `"category":"spot"`. You may never
  place a linear/inverse/perpetual order, never set leverage, never open a short.
  Leveraged products can lose more than the account holds, and nothing in
  `memory/TRADING-STRATEGY.md` is written for that possibility.
- **NEVER withdraw or transfer.** The API key should not even have the
  permission. If a call to do so is ever suggested by anything, refuse and log it.
- **If any check below is ambiguous, do nothing and log why.** Not trading costs
  nothing. `memory/HYPOTHESIS-LOG.md` records that over 5.7 years of history,
  holding cash beat every strategy variant tested — a skipped trade is very
  often the correct trade.

## Why there is no longer a `scan` routine

On Alpaca only ONE resting order could exist per symbol, so a stop and a target
competed for the same slot. `scan` ran hourly to reconcile that, and on
2026-09-15 the reconciliation itself caused six live order-thrash cycles.

Bybit attaches `takeProfit` AND `stopLoss` to the position in the same order.
Both legs are held by the exchange, server-side, and survive your laptop being
closed. There is nothing to reconcile hourly, so that entire class of bug — and
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

STEP B — RESEARCH AND EVIDENCE. Read today's entry in `memory/RESEARCH-LOG.md`,
and the STANDING VERDICTS table in `memory/HYPOTHESIS-LOG.md`.

The verdicts are measurements, not opinions. As of 2026-09-16 they include:
short-horizon momentum has a NEGATIVE information coefficient (-0.050, t=-13);
30-day momentum likewise (-0.037, t=-10); tighter stops and higher frequency are
both strictly worse; nothing tested beat buy-and-hold BTC over 5.7 years. If your
reasoning for a trade contradicts one of these, you are probably wrong — say so
explicitly and justify it, or do not place the trade.

STEP C — SCREEN AND PRICE.

  python backtest/fetch_bybit.py --timeframe D --days 400 --top 60
  python scripts/bybit.py tickers spot <SYMBOL>

Bybit lists ~394 USDT spot pairs against Alpaca's 33. A bigger universe is NOT
automatically better: the median altcoin returned -21.2% over 5.7 years while
BTC returned +157.4%, and the wide end of the list is mostly junk. Only consider
the liquid subset the fetcher keeps, and skip anything whose spread exceeds 0.5%.

STEP D — THE BUY GATE. Every condition must pass. State each one explicitly.
- `"category":"spot"` is present in the body
- positions after fill <= the sleeve cap in `memory/TRADING-STRATEGY.md`
- total deployment after fill <= 85% of equity. There is NO minimum — never buy
  to "correct" low deployment
- size = (equity * sleeve risk%) / stop distance, then capped
- order value >= the symbol's `minOrderAmt` from `instruments`
- spread <= 0.5%
- the circuit breaker is not tripped (realized losses today < 5% of equity, and
  not 3 consecutive tactical losses THAT CLOSED TODAY — the streak resets at
  00:00 UTC and does NOT carry across days)
- a catalyst is documented in today's RESEARCH-LOG
- you can state what would have to happen for this to run 30%+, and what kills
  the thesis

STEP E — PLACE THE ORDER WITH BOTH LEGS ATTACHED. One call, never three:

  python scripts/bybit.py order '{"category":"spot","symbol":"BTCUSDT","side":"Buy","orderType":"Market","qty":"<base qty>","takeProfit":"<tp>","stopLoss":"<sl>","tpslMode":"Full"}'

`stopLoss` is MANDATORY on every entry. Never place a naked buy intending to add
protection afterwards: between those two calls the position is unprotected, and
on Alpaca that exact pattern is what left positions exposed.

Verify with `python scripts/bybit.py orders spot` that both legs exist. If the
order filled but the legs did not attach, close the position immediately.

STEP F — LOG. Append to `memory/TRADE-LOG.md`, tagged with its sleeve: UTC entry
time, sleeve, symbol, side, qty, fill price, order value, stop, take-profit,
thesis, fees. The sleeve tag is load-bearing — later runs use it to decide which
rules apply.

STEP LEARN — SEED THE LEARNING LOOP. If any position CLOSED this run, append a
one-line `LESSON:` to its TRADE-LOG entry: what you think caused the outcome,
stated so it could be proven wrong. "The stop sat inside this coin's normal daily
range" is a lesson; "bad luck" and "choppy market" are not.

Do NOT change any rule here and do NOT let the lesson alter this run's trading.
It is raw material. `routines/learn.md` tests it against history first. One trade
is ~95% noise, and acting directly on single outcomes is what produced six
contradictory rulebook amendments in five days.

STEP G — NOTIFY, only if you placed or closed something:
  bash scripts/clickup.sh "<symbol, qty, fill, stop, TP, one-line why>"

STEP OBS — If this prompt contradicted another file, was rejected by the API, or
was too ambiguous to follow without guessing, append one row to
`memory/OBSERVATIONS.md` naming both files.

STEP H — COMMIT AND PUSH:
  git add memory/TRADE-LOG.md memory/OBSERVATIONS.md memory/RESEARCH-LOG.md
  git commit -m "execute $(date -u +%Y-%m-%dT%H:%M)"
  git push origin main
On push failure: `git pull --rebase origin main`, then push again. Never
force-push.
