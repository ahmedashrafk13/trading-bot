#!/usr/bin/env bash
# Archives log entries older than KEEP_DAYS into memory/archive/, so per-run
# context (and therefore cost) stops growing forever. History is preserved —
# nothing is deleted, and git keeps everything regardless.
#
# Usage: bash scripts/rotate-logs.sh [keep_days]   (default 14)

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
KEEP="${1:-14}"
mkdir -p memory/archive

KEEP="$KEEP" python - <<'PY'
import os, re, datetime as dt
from pathlib import Path
keep = int(os.environ['KEEP'])
# Cutoff from the BROKER clock would be ideal, but rotation is not time-critical
# and this machine's clock is 12h fast, so use a date parsed from the newest
# entry in the file instead of "now".
for name in ['RESEARCH-LOG.md', 'TRADE-LOG.md']:
    p = Path('memory')/name
    if not p.exists(): continue
    text = p.read_text(encoding='utf-8')
    # entries start at a top-level "## <date>" heading
    parts = re.split(r'(?m)^(?=## )', text)
    header, entries = parts[0], parts[1:]
    dated = []
    for e in entries:
        m = re.match(r'## (\d{4}-\d{2}-\d{2})', e)
        dated.append((dt.date.fromisoformat(m.group(1)) if m else None, e))
    known = [d for d,_ in dated if d]
    if not known:
        print(f'{name}: no dated entries, skipped'); continue
    cutoff = max(known) - dt.timedelta(days=keep)
    keep_e  = [e for d,e in dated if d is None or d >= cutoff]
    arch_e  = [(d,e) for d,e in dated if d is not None and d < cutoff]
    if not arch_e:
        print(f'{name}: nothing older than {cutoff}, kept {len(keep_e)} entries'); continue
    by_month = {}
    for d,e in arch_e: by_month.setdefault(f'{d:%Y-%m}', []).append(e)
    for month, es in by_month.items():
        a = Path('memory/archive')/f'{name[:-3]}-{month}.md'
        prev = a.read_text(encoding='utf-8') if a.exists() else f'# Archived {name} — {month}\n'
        a.write_text(prev.rstrip('\n') + '\n\n' + '\n'.join(es).rstrip('\n') + '\n', encoding='utf-8')
        print(f'  archived {len(es)} entrie(s) -> {a}')
    note = (f'\n> Entries before {cutoff} are in memory/archive/. Runs read only this file;\n'
            f'> archives exist for audit and for the weekly review to consult on request.\n')
    p.write_text(header.rstrip('\n') + '\n' + note + '\n' + '\n'.join(keep_e), encoding='utf-8')
    print(f'{name}: kept {len(keep_e)}, archived {len(arch_e)}, cutoff {cutoff}')
PY
