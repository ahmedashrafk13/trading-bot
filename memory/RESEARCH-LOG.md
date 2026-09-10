# Research Log

Daily pre-market research entries will be appended here.
Format each entry:

## YYYY-MM-DD — Pre-market Research

### Account
- Equity: $X
- Cash: $X
- Buying power: $X
- Daytrade count: N

### Market Context
- WTI / Brent:
- S&P 500 futures:
- VIX:
- Today's catalysts:
- Earnings before open:
- Economic calendar:
- Sector momentum:

### Trade Ideas
1. TICKER — catalyst, entry $X, stop $X, target $X, R:R X:1
2. ...

### Risk Factors
- ...

### Decision
TRADE or HOLD (default HOLD if no edge)

## 2026-09-10 — Pre-market Research (OFF-CYCLE local run, ~14:40 ET, market open)

> Run context: executed manually via /pre-market at 14:40 ET, ~80 min before the
> close — not the scheduled 06:00 CT slot. Perplexity unconfigured, so research
> used the native WebSearch fallback (no Perplexity citations). Date taken from
> the Alpaca market clock, NOT the local machine clock, which is 12h fast.

### Account
- Equity: $200.00
- Cash: $200.00 (settled, cash account — multiplier 1)
- Buying power: $200.00
- Daytrade count: not reported (cash account; PDT N/A)
- Positions: none. Open orders: none.

### Market Context
- WTI / Brent: Brent settled $101.21 (+3.4%) on 9/9, highest since July; renewed
  Iran-U.S. attacks near the Strait of Hormuz driving energy supply fear.
- S&P 500: closed 7,636.36 (-37.16, -0.5%) on 9/9. S&P and Nasdaq declining again
  today on the oil move.
- VIX: ~16.3-17.6, up ~7% intraday. Near 10-yr average — no panic, but hedging
  demand is picking up into a seasonally volatile stretch.
- Today's catalysts: PPI released 08:30 ET today. Treasury yields at 52-week highs.
- Economic calendar: **CPI tomorrow (Fri 9/11) 08:30 ET** — the dominant near-term risk.
- Sector momentum: Energy leading (oil shock). Tech slumping. Rate-sensitives
  pressured by the yield move.

### Candidates screened (live Alpaca quotes, $40 whole-share ceiling)
| Ticker | Ask | Spread | Verdict |
|--------|-----|--------|---------|
| HAL  | 36.13 | 0.03% | PASSES — 1 sh = 18.1% of equity |
| KMI  | 31.19 | 0.03% | PASSES — 1 sh = 15.6% of equity |
| RIG  |  5.76 | 0.17% | PASSES — 6 sh = $34.56 (17.3%) |
| CTRA | 34.54 | 11.32% | SKIP — spread far too wide (see feed caveat) |
| OKE  | 99.35 | 3.93% | SKIP — over $40 cap AND wide spread |
| DVN  | 49.81 | 0.02% | SKIP — over the 20% cap ($40) |
| APA  | 44.89 | 0.02% | SKIP — over the 20% cap ($40) |
| SLB  | 56.12 | 0.02% | SKIP — over the 20% cap ($40) |

### Trade Ideas (WATCHLIST ONLY — not actionable today)
1. HAL — oilfield services levered to a sustained crude bid. Entry <= $36.50,
   stop $33.96 (-7%), target $41.58 (+14%), R:R 2:1. Needs oil strength to hold
   through CPI.
2. KMI — midstream, lower beta, steadier than E&P on an oil spike. Entry <= $31.40,
   stop $29.20 (-7%), target $35.80 (+14%), R:R 2:1.
3. RIG — speculative offshore driller, highest beta to crude of the three. Only
   with a smaller size; skip if CPI turns risk-off.

### Risk Factors
- CPI tomorrow 08:30 ET is binary and unhedgeable at this size. A hot print with
  yields already at 52-wk highs is the obvious downside path.
- Oil is 3 days into a geopolitical spike. Buying day 3 of a headline move is
  chasing; Hormuz headlines mean-revert violently on any de-escalation.
- 80 minutes to the close is not enough time for a thesis to work, and a same-day
  buy leaves the stop exposed to an overnight gap that trailing stops do not cover.
- T+1 settlement: all $200 is settled now, but any exit locks proceeds until the
  next business day.

### Decision
**HOLD.** No orders. Three independent reasons: this is an off-cycle run with 80
minutes left in the session, CPI lands tomorrow pre-open, and the leading sector is
mid-spike rather than early. Re-evaluate at the 06:00 CT pre-market run tomorrow
AFTER the CPI print is known. Patience > activity.

---
## 2026-09-10 — PIVOT: stocks -> crypto
The entry above (HAL/KMI/RIG energy screen) is from the stocks era — historical
only, do not act on it. The account now trades crypto USD pairs exclusively.
Next research run screens crypto pairs against the new gate.

---
## 2026-09-10 — Crypto Research (local run, 19:39 UTC)

> Perplexity unconfigured -> native WebSearch fallback, no Perplexity citations.
> Date from the Alpaca clock (19:39 UTC); the machine clock is 12h fast.
> First run under the two-sleeve model.

### Account
- Equity: $200.00 | Cash: $200.00 | Deployed: 0%
- Positions: none. Open orders: none. Stop coverage: N/A.
- Capacity: CORE 3 slots ($120), TACTICAL 3 slots ($80). Trades used: 0/3 wk, 0/3 day.

### Market Context
- BTC $77,155 (screen) / ~$78,039 earlier, -1% on 24h. ETH $2,464, -0.7%.
- Global market cap -0.9% to $2.76T. Both majors opened at week lows.
- **FOMC starts Tuesday with a 62.2% implied chance of a RATE HIKE.** Higher
  rates are directly negative for crypto.
- **CPI tomorrow (2026-09-11) 08:30 ET**, after today's PPI. Last inflation
  reads before the Fed decides.
- Macro backdrop from the equity session: Brent >$100 on Iran/Hormuz, Treasury
  yields at 52-week highs. Risk-off, not risk-on.

### Universe screen (all 33 pairs — scripts/screen.sh)
CORE shortlist, daily bars (5): DOT XTZ SUSHI GRT UNI
TACTICAL shortlist, hourly bars (19): SKY UNI POL ETH RENDER LDO TRUMP SOL AAVE
CRV SHIB DOT GRT YFI ADA ARB FIL DOGE LINK

Read the tactical list carefully: the hourly 30-period momentum is NEGATIVE for
every single one of the 33 coins (-0.4% to -11.9%). All 19 "passes" are a ~7-hour
bounce inside a 30-hour downtrend, driven by one macro move. They are not 19
independent setups — they are one correlated setup wearing 19 tickers. Taking 3
tactical positions here would be three bets on the same bounce.

### Candidate notes
- DOT — the only strong catalyst in the universe: OpenGov Referendum 1944 for a
  native stablecoin (dotUSD) at ~97.5% in favour, a 150% transaction spike and
  record XCM throughput on 9/7, plus a short-liquidation squeeze. But +24% on
  the week and +18.1% over SMA20 — it barely clears the <=20% extension filter,
  and a squeeze-driven leg is exactly the kind that retraces.
- XTZ — Tezos X mainnet targeted for summer 2026, named an altseason contender
  on 8/23. Real but vague; no dated near-term catalyst.
- SUSHI / GRT / UNI — pass on trend mechanics with no specific catalyst found.
  Gate requires a documented catalyst, so none are entry-eligible today.

### Risk Factors
- A 62% probability of a rate hike is the single most important fact here, and
  it lands 2 trading days out. CORE holds are weeks-long by design; opening one
  into that is choosing the worst entry window available.
- CPI tomorrow pre-open. A tactical 6% stop is well inside a normal CPI-day
  range for alts, so a stop-out is likelier than a 12% target being reached.
- Everything is correlated to the same macro driver, so position count would
  overstate diversification.
- Fees: 3 tactical round trips cost ~1.05%/wk of the account. Paying that to
  express one macro guess is poor value.

### Decision
**HOLD both sleeves. No orders.**
- CORE: HOLD. Only DOT has a real catalyst and it is extended after a squeeze,
  two days before a probable hike. Waiting costs nothing; the dotUSD narrative
  is not a one-day event.
- TACTICAL: HOLD. 19 nominal passes are one correlated bounce, and CPI tomorrow
  makes a 6% stop a coin flip.

### Triggers for the next run (2026-09-11, post-CPI)
1. CPI printing at or below expectations AND hike odds falling below ~50%
   -> re-screen; DOT becomes CORE-eligible if it has cooled to <=12% over SMA20.
2. CPI hot / hike odds rising -> stay flat. Do not "buy the dip" into a hiking
   Fed; that is not a catalyst, it is hope.
3. Tactical entries only once hourly 30-period momentum turns positive for the
   candidate, so the bounce is confirmed rather than assumed.
