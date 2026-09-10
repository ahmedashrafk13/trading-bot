# Cloud Routines

These five prompts are the production path (crypto, 24/7). Each is pasted **verbatim** into its own Claude Code
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
   | `ALPACA_ENDPOINT` | set to `https://paper-api.alpaca.markets/v2` for paper |
   | `ALPACA_DATA_ENDPOINT` | optional (defaults to data URL) |
   | `PERPLEXITY_API_KEY` | optional — falls back to WebSearch |
   | `PERPLEXITY_MODEL` | optional (defaults to `sonar`) |
   | `CLICKUP_API_KEY` | optional — falls back to a local file |
   | `CLICKUP_WORKSPACE_ID` | optional (numeric; needed only with the API key) |
   | `CLICKUP_CHANNEL_ID` | optional (format `4-XXXXXXX-X`) |

### Why the "no .env file" rule matters

The wrappers read `.env` first, then fall back to the process env. In the cloud, a `.env` holding
real credentials is either an immediate secret leak (if pushed) or wasted work (if not). The worst
failure mode is the agent seeing "key not set", helpfully creating a `.env` as a workaround, and
leaking credentials. Every prompt here carries an explicit "do not create a .env file" block.

## Creating a routine

1. Routines -> New Routine.
2. Name it, e.g. "Crypto bot research".
3. Select this repository, branch `main`.
4. Add all env vars above.
5. Toggle on **Allow unrestricted branch pushes**.
6. Set the cron and set the timezone to **UTC**.
7. Paste the matching `routines/*.md` file verbatim into the prompt field.
8. Save, then hit **Run now** once to test — don't wait until tomorrow morning to find out it
   is broken.

## Schedules (UTC — crypto has no trading day, and UTC avoids DST entirely)

| File | Cron | UTC | Role |
|---|---|---|---|
| `scan.md` | `7 * * * *` | every hour :07 | ratchet stops + safety sweep |
| `research.md` | `7 6 * * *` | 06:07 | research + write the day's plan |
| `execute.md` | `7 12 * * *` | 12:07 | run the gate, place entries + stops |
| `summary.md` | `7 18 * * *` | 18:07 | daily snapshot, P&L vs BTC |
| `weekly-review.md` | `37 18 * * 0` | Sun 18:37 | graded weekly recap |

Every day of the week, including weekends — crypto never closes. The `:07` and
`:37` offsets keep these off the `:00` minute that everyone else schedules on,
and keep the Sunday weekly review from colliding with that day's summary.

### Helper scripts the prompts rely on
- `scripts/state.sh` — ONE call giving broker-clock UTC, equity/cash/deployment,
  every position with age + exact stop-coverage % (with a NAKED flag), the weekly
  fee-budget state, the circuit-breaker state and the amendment trigger. Every
  run uses it instead of doing arithmetic over markdown, which is where the
  guardrail numbers used to drift.
- `scripts/screen.sh` — ranks all 33 tradable pairs; CORE on daily bars,
  TACTICAL on hourly. Hard-fails rather than truncating if pagination overruns.
- `scripts/rotate-logs.sh` — archives log entries older than 14 days into
  memory/archive/. Run by the weekly review. Without it, per-run context (and
  cost) grows forever at hourly scan cadence.

`scan` runs HOURLY, not daily. It is cheap (a positions call, an orders call and
at most a stop re-placement) and it is the only thing standing between a spike
and a round trip: a take-profit limit cannot rest alongside a stop on Alpaca
crypto, so profit is locked in by ratcheting the resting stop, and a ratchet only
happens when a run happens. Hourly means at most ~1h of a favourable move goes
uncaptured, instead of up to 6h.

`scan` is deliberately LEAN (~1,100 tokens, self-contained, reads no memory
files) because it runs ~720x/month. The other four read memory and are ~1,700-2,500
tokens each but run only once a day.

Every routine begins with the same STEP A invariants: reconcile positions,
verify every position has a resting `stop_limit`, force-close anything past -15%
that the stop missed, and ratchet stops upward. That repetition is deliberate —
runs are 6h apart and nothing else is watching a 24/7 market.

## Notification philosophy

- scan: only if it acted (a cut, a stop placed, a ratchet)
- research: silent unless urgent (stop gapped, exploit/depeg on a holding, macro shock)
- execute: only if a trade was placed
- summary: always, one message, under 15 lines
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
| `invalid order type for crypto order` | Prompt used `trailing_stop` or `stop` | Crypto supports `stop_limit` only — re-paste the prompt |
| `invalid crypto time_in_force` | Order used `time_in_force: day` | Crypto requires `gtc` (or `ioc`) |
| A position has no resting stop | Stop was rejected after the buy filled | STEP A of every run re-places it; if it fails twice the prompt closes the position |
