# Trading Bot

Autonomous, cloud-scheduled swing-trading agent built on Claude Code. Claude *is* the bot —
there is no separate Python process. Every scheduled run is a fresh Claude invocation that
clones this repo, reads `memory/`, pulls live Bybit state, acts, writes memory, and pushes to
`main`.

**Crypto spot AND linear perps. LONG AND SHORT. Leverage <=5x (v4, 2026-09-22
owner directive).** A LIVE Bybit UNIFIED account — this is real money — benchmarked against BTC
buy-and-hold.

Two sleeves: **CORE** (~$120, 3 positions, 20% ratcheted trail, no time limit,
no fixed trade count) for letting good trades run, and **TACTICAL** (~$80, 3 positions
of $20, 6% stop, +14% target, frequency bounded by a 1.5%/week fee budget). Entries must clear a
technical screen over the liquid end of Bybit's USDT spot list, not just a news
catalyst.

## Quickstart (local mode)

1. `cp env.template .env` and fill in your Bybit / Perplexity / ClickUp credentials.
   The Bybit key must be Read + Trade ONLY — never enable Withdraw.
   `.env` is gitignored — never commit it.
2. `chmod +x scripts/*.sh`
3. Open this repo in Claude Code and run `bash scripts/state.sh`. You should see
   equity, holdings and stop coverage print cleanly. That's the smoke test.
4. The routines in `routines/` are the only workflows; there are no local slash
   commands.

## Production (cloud mode)

See `routines/README.md`. Summary:

1. Install the Claude GitHub App on this repo.
2. Create five routines, one per file in `routines/`.
3. On each routine: set the env vars (NOT a `.env` file), enable
   **"Allow unrestricted branch pushes"**, and paste the prompt file verbatim.
4. Cron schedules (UTC, every day — crypto never closes):

   | Routine | Cron | UTC |
   |---------|------|-----|
   | scan | `7 * * * *` | hourly at :07 |
   | research | `7 6 * * *` | 06:07 |
   | execute | `7 12 * * *` | 12:07 |
   | summary | `7 18 * * *` | 18:07 |
   | weekly-review | `37 18 * * 0` | Sun 18:37 |

5. Hit **Run now** on pre-market first and watch the logs before creating the rest.

## Layout

- `CLAUDE.md` — agent rulebook, auto-loaded every session
- `scripts/` — the only way the agent touches the outside world
  - `bybit.py` — balance, holdings, orders, fills, tickers, klines, order entry
  - `state.sh` — every guardrail number. Run it first, every run. Read-only.
  - `screen.sh` — ranks the top USDT spot pairs by turnover; CORE (daily) +
    TACTICAL (hourly) shortlists with PASS/fail reasons. Read-only.
- `routines/` — the routine prompts (production path)
- `memory/` — the agent's entire persistent state, committed to `main`

## Safety notes

- Never commit a real `.env`.
- If it isn't committed and pushed to `main`, it didn't happen.
- `BYBIT_ENDPOINT` must be `https://api.bybit.com`. The API key carries Read +
  Trade only; if Withdraw is ever enabled, rotate the key.
- Every order body must carry `"category":"spot"`. Stops are conditional orders
  and can still be gapped through — see `memory/TRADING-STRATEGY.md`.
- Crypto has fees (~0.11% per round trip on Bybit). This is real money.
- Monitor the first week closely. Read every commit the agent makes.
