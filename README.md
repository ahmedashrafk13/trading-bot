# Trading Bot

Autonomous, cloud-scheduled swing-trading agent built on Claude Code. Claude *is* the bot —
there is no separate Python process. Every scheduled run is a fresh Claude invocation that
clones this repo, reads `memory/`, pulls live Alpaca state, acts, writes memory, and pushes to
`main`.

**Stocks only. No options, ever.**

## Quickstart (local mode)

1. `cp env.template .env` and fill in your Alpaca / Perplexity / ClickUp credentials.
   `.env` is gitignored — never commit it.
2. `chmod +x scripts/*.sh`
3. Open this repo in Claude Code and run `/portfolio`. You should see account and
   positions print cleanly. That's the smoke test.
4. Other local commands: `/trade SYM SHARES buy`, `/pre-market`, `/market-open`,
   `/midday`, `/daily-summary`, `/weekly-review`.

## Production (cloud mode)

See `routines/README.md`. Summary:

1. Install the Claude GitHub App on this repo.
2. Create five routines, one per file in `routines/`.
3. On each routine: set the env vars (NOT a `.env` file), enable
   **"Allow unrestricted branch pushes"**, and paste the prompt file verbatim.
4. Cron schedules (America/Chicago):

   | Routine        | Cron          | Local time            |
   |----------------|---------------|-----------------------|
   | pre-market     | `0 6 * * 1-5` | 6:00 AM weekdays      |
   | market-open    | `30 8 * * 1-5`| 8:30 AM weekdays      |
   | midday         | `0 12 * * 1-5`| 12:00 PM weekdays     |
   | daily-summary  | `0 15 * * 1-5`| 3:00 PM weekdays      |
   | weekly-review  | `0 16 * * 5`  | 4:00 PM Fridays       |

5. Hit **Run now** on pre-market first and watch the logs before creating the rest.

## Layout

- `CLAUDE.md` — agent rulebook, auto-loaded every session
- `scripts/` — the only way the agent touches the outside world
- `routines/` — cloud routine prompts (production path)
- `.claude/commands/` — local slash commands (testing / ad-hoc)
- `memory/` — the agent's entire persistent state, committed to `main`

## Safety notes

- Never commit a real `.env`.
- If it isn't committed and pushed to `main`, it didn't happen.
- Seed `memory/TRADE-LOG.md` with a Day 0 snapshot before the first `daily-summary` run
  (already done in this repo).
- Monitor the first week closely. Read every commit the agent makes.
