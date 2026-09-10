# Cloud Routines

These five prompts are the production path. Each is pasted **verbatim** into its own Claude Code
cloud routine. Do not paraphrase — the env-var check block and the commit-and-push step are
load-bearing.

## What happens on each scheduled run

1. The cron fires in the routine's timezone.
2. Claude's cloud spins up a fresh container.
3. It clones this repo at `main`, so it sees the latest memory.
4. It injects the routine's environment variables into the shell.
5. It starts Claude with the pasted prompt.
6. Claude reads memory, calls the wrappers, writes memory.
7. Claude commits and pushes to `main` — **otherwise everything it did evaporates.**
8. The container is destroyed.

Mental model: the runner is stateless. Git is the memory. If it isn't in `main`, it didn't happen.

## One-time prerequisites

1. **Install the Claude GitHub App** on this repo only (least privilege). This grants clone +
   push. Alternative: run `/web-setup` inside Claude Code to sync your `gh` CLI token.
2. **Enable "Allow unrestricted branch pushes"** on the routine's environment. Without it,
   `git push origin main` silently fails with a proxy error. This is the number-one reason
   first-time setups break.
3. **Set env vars on the routine — NOT in a `.env` file:**

   | Variable | Required? |
   |---|---|
   | `ALPACA_API_KEY` | required |
   | `ALPACA_SECRET_KEY` | required |
   | `ALPACA_ENDPOINT` | optional (defaults to live trading URL) |
   | `ALPACA_DATA_ENDPOINT` | optional (defaults to data URL) |
   | `PERPLEXITY_API_KEY` | required for research workflows |
   | `PERPLEXITY_MODEL` | optional (defaults to `sonar`) |
   | `CLICKUP_API_KEY` | required for notifications |
   | `CLICKUP_WORKSPACE_ID` | required (numeric) |
   | `CLICKUP_CHANNEL_ID` | required (format `4-XXXXXXX-X`) |

### Why the "no .env file" rule matters

The wrappers read `.env` first, then fall back to the process env. In the cloud, a `.env` holding
real credentials is either an immediate secret leak (if pushed) or wasted work (if not). The worst
failure mode is the agent seeing "key not set", helpfully creating a `.env` as a workaround, and
leaking credentials. Every prompt here carries an explicit "do not create a .env file" block.

## Creating a routine

1. Routines -> New Routine.
2. Name it, e.g. "Trading bot pre-market".
3. Select this repository, branch `main`.
4. Add all env vars above.
5. Toggle on **Allow unrestricted branch pushes**.
6. Set the cron and timezone.
7. Paste the matching `routines/*.md` file verbatim into the prompt field.
8. Save, then hit **Run now** once to test — don't wait until tomorrow morning to find out it
   is broken.

## Schedules (America/Chicago)

| File | Cron | Local time |
|---|---|---|
| `pre-market.md` | `0 6 * * 1-5` | 6:00 AM weekdays |
| `market-open.md` | `30 8 * * 1-5` | 8:30 AM weekdays (open) |
| `midday.md` | `0 12 * * 1-5` | noon weekdays |
| `daily-summary.md` | `0 15 * * 1-5` | 3:00 PM weekdays (close) |
| `weekly-review.md` | `0 16 * * 5` | 4:00 PM Fridays only |

Keep the routines hours apart. Two runs scheduled seconds apart is the one scenario where
memory-in-git breaks down.

## Notification philosophy

- pre-market: silent unless genuinely urgent
- market-open: only if a trade was placed
- midday: only if action was taken
- daily-summary: always, one message, under 15 lines
- weekly-review: always, one message, headline numbers

A missed notification is cheap. A chatty bot is expensive — you stop reading, then you miss the
one that mattered.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| "Repository not accessible" / clone fails | Claude GitHub App not installed | Install it, grant access to this repo |
| `git push` fails with proxy/permission error | "Allow unrestricted branch pushes" is off | Enable it on the routine's environment |
| `ALPACA_API_KEY not set in environment` | Env var missing from routine config | Add it on the routine, not in a repo `.env` |
| Agent creates a `.env` anyway | Prompt was paraphrased, losing the DO-NOT block | Re-paste from `routines/*.md` exactly |
| Yesterday's trades missing today | Previous run did not commit + push | Check `git log origin/main`, re-verify the final STEP |
| Push fails "fetch first" / non-fast-forward | Another run pushed between clone and push | Prompts handle it with `git pull --rebase`; if looping, look for a real conflict |
| ClickUp message never arrived | One of the three `CLICKUP_*` vars is missing | Script silently falls back to a local file — add the missing var |
| Perplexity calls did not happen | `PERPLEXITY_API_KEY` missing | Script exits 3 and the agent falls back to WebSearch — add the key or accept the fallback |
| Alpaca rejects the stop with a PDT error | Same-day stop on a same-day buy | The fallback ladder handles it; if it is not cascading, re-paste STEP 5 verbatim |
