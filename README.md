# Trading Bot

Autonomous, cloud-scheduled swing-trading agent built on Claude Code. Claude *is* the bot —
there is no separate Python process. Every scheduled run is a fresh Claude invocation that
clones this repo, reads `memory/`, pulls live Bybit state, acts, writes memory, and pushes to
`main`.

**Crypto only. No stocks, no options, ever. Long only.** ~$200 on Bybit crypto,
benchmarked against BTCUSDT buy-and-hold.

Two sleeves: **CORE** (~$120, 3 positions, 20% ratcheted trail, no time limit,
no fixed trade count) for letting good trades run, and **TACTICAL** (~$80, 3 positions
of $20, 6% stop, +14% target, frequency bounded by a 1.5%/week fee budget). Entries must clear a
technical screen over all 33 pairs, not just a news catalyst.

## Quickstart (local mode)

1. `cp env.template .env` and fill in your Bybit / Perplexity / ClickUp credentials.
   `.env` is gitignored — never commit it.
2. `chmod +x scripts/*.sh`
3. Open this repo in Claude Code and run `/portfolio`. You should see account and
   positions print cleanly. That's the smoke test.
4. Other local commands: `/trade BTCUSDT 0.0005 buy`, `/scan`, `/research`,
   `/execute`, `/summary`, `/weekly-review`.

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
  - `bybit.sh` — account, positions, orders, quotes, bars, assets
  - `screen.sh` — ranks all 33 tradable pairs; CORE (daily) + TACTICAL (hourly)
    shortlists with PASS/fail reasons. Read-only.
- `routines/` — cloud routine prompts (production path)
- `.claude/commands/` — local slash commands (testing / ad-hoc)
- `memory/` — the agent's entire persistent state, committed to `main`

## Safety notes

- Never commit a real `.env`.
- If it isn't committed and pushed to `main`, it didn't happen.
- `BYBIT_ENDPOINT` must be `https://api-demo.bybit.com` (Demo Trading). Demo
  keys are rejected by `api.bybit.com` with 10003 — that rejection is the
  safety check that the bot cannot touch real funds.
- Bybit spot has no `trailing_stop` order type. A stop is `orderType: Limit`
  plus `triggerPrice`, raised with `amend`, and can still be gapped through
  — see `memory/TRADING-STRATEGY.md`.
- The $200 is a VIRTUAL BOOK isolated by the `tb-` orderLinkId prefix; the
  demo account itself holds ~$181k that is NOT ours. Read `scripts/pnl.sh`.
- Crypto has fees (~0.5% per round trip). Stocks were free; this is not.
- Monitor the first week closely. Read every commit the agent makes.
