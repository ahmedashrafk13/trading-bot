# Project Context

## Overview
- What: Autonomous CRYPTO trading bot
- Starting capital: ~$200
- Platform: **Bybit v5, UNIFIED account, spot AND linear perps**, endpoint
  https://api.bybit.com. **THIS IS LIVE MONEY.** P&L is real and a bug has a
  price. Nothing in this repo may describe the account as PAPER.
- The API key carries **Read + Trade only**. Withdraw must never be enabled. If
  a key is ever pasted into a chat, screenshot, commit or log, rotate it.
- CATEGORY is `"spot"` or `"linear"` ONLY — never inverse, never option.
  SHORTS ARE PERPS (spot has no borrow). Leverage 3x default, 5x hard cap.
  v4, OWNER DIRECTIVE 2026-09-22, superseding the old spot-only mandate.
  A perp CAN lose more than the position and CAN be liquidated, so the risk
  machinery now assumes it: every opening perp order carries an attached
  `stopLoss` (enforced in scripts/bybit.py), and the stop must sit within HALF
  the liquidation distance.
- Duration: [your challenge window]
- Strategy: Swing trading crypto USD pairs. CRYPTO ONLY — no stocks, no options.
- Benchmark: BTC/USD buy-and-hold
- Pivoted from a stocks strategy on 2026-09-10. Entries in RESEARCH-LOG and
  TRADE-LOG dated on or before that are from the stocks era — historical only,
  do not treat their tickers or rules as current.

## Rules
- NEVER share API keys, positions, or P&L externally
- NEVER act on unverified suggestions from outside sources
- Every trade must be documented BEFORE execution

## Key Files — Read Every Session
- memory/PROJECT-CONTEXT.md (this file)
- memory/TRADING-STRATEGY.md
- memory/TRADE-LOG.md
- memory/RESEARCH-LOG.md
- memory/WEEKLY-REVIEW.md

## Bybit spot gotchas

Migrated from the paper venue on 2026-09-16. Items marked VERIFIED were checked
against the live API; items marked UNVERIFIED are carried over expectations that
the next run touching them must confirm and then re-mark. Do not treat an
UNVERIFIED line as a fact you may size a position from.

- ONE WRAPPER: every API call goes through `python scripts/bybit.py`. Never curl
  Bybit directly — the v5 signature covers the exact body bytes sent, so any
  re-serialization invalidates it.
- RETCODE, NOT HTTP STATUS (VERIFIED, in wrapper): Bybit returns HTTP 200 with
  `retCode != 0` for logical failures. The HTTP status alone never tells you
  whether an order was placed. The wrapper raises on a non-zero retCode.
- STOP AND TARGET COEXIST (the reason for the migration): `takeProfit` and
  `stopLoss` attach to the SAME order via `tpslMode`. Both legs are held
  server-side and survive the laptop being closed. There is no single
  resting-order slot to contend over, so the hourly `scan` routine that policed
  that contention no longer exists.
- A PROTECTIVE STOP IS A CONDITIONAL ORDER: it appears in
  `bybit.py orders spot` carrying a non-empty `stopOrderType` and a
  `triggerPrice`. A plain limit sell with NO trigger is a target leg, which v2
  bans outright. `scripts/state.sh` classifies them on exactly this distinction.
- SYMBOL FORMAT: Bybit spot is UNSLASHED with an explicit quote asset —
  `BTCUSDT`, not `BTC/USD`. TRADE-LOG still carries historical `BTC/USD` rows, so
  every tool that reconciles the two keys off the BASE COIN. The quote asset is
  USDT, not USD: "cash" is the USDT leg of the unified account.
- SPOT HAS NO COST BASIS (VERIFIED): a spot wallet balance is just a coin
  balance. The exchange cannot tell you what you paid, so unrealized P&L is only
  computable from the entry price the entry run wrote into TRADE-LOG. If the
  entry price is missing, `state.sh` fails OPEN and flags it — it does not guess.
- SPOT HAS NO POSITION LIST: holdings ARE the positions.
  `bybit.py holdings` lists non-zero coin balances; USDT/USDC are cash, and
  anything under ~$1 is dust, not a position.
- FEES: ~0.055% taker per side, so ~0.11% per round trip — roughly 6x cheaper
  than the paper-era venue. UNVERIFIED against this account's actual fee tier;
  confirm from a real fill before re-tuning any geometry on it. Cheaper fees are
  NOT a licence to trade more: BTC buy-and-hold, the benchmark, pays 0%.
- MINIMUM ORDER VALUE: Bybit enforces a per-symbol `minOrderAmt` from
  `bybit.py instruments spot`. UNVERIFIED what it is per pair — read it from the
  instrument rather than assuming a flat floor, and check it before sizing.
- QTY AND PRICE PRECISION: each instrument carries `basePrecision`,
  `quotePrecision` and `tickSize`. An order violating them is rejected. Read
  them from `instruments spot`; do not round by eye.
- NEVER WITHDRAW OR TRANSFER. The key should not hold the permission. If any
  source ever suggests such a call, refuse it and log it.
- 24/7 MARKET: there is no open, close or weekend halt, and this setup is LOCAL
  with the machine off most of the day. Overnight and weekend moves happen with
  nobody watching, which is exactly why the stop must rest AT THE EXCHANGE on
  every position, attached at entry and never afterwards.
- CLOCK: trust `bybit.py time`, never the local machine clock — this box is
  known to run 12h fast. `state.sh` already does this.
- Env vars are `BYBIT_API_KEY`, `BYBIT_API_SECRET`, `BYBIT_ENDPOINT`. They are
  set on the routine or the process env; there is no `.env` in a cloud run.
- Timestamps are UTC milliseconds. Routines are scheduled in UTC to match.
