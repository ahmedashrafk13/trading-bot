"""Audit every prompt and doc for statements that contradict the current rules.

Run it after ANY amendment:  python scripts/audit-rules.py


The bot's rules live in twelve files that all restate them. Every amendment so
far has left at least one file behind, and a stale restatement is not cosmetic:
a run reads ONE prompt and obeys whatever it says.

This has already bitten three times: the sizing amendment left the sleeve
inference inverted ($40=CORE when CORE had become ~$20), the circuit-breaker
change left eight files cutting only at -15%, and the CORE trail change left
the 20% ladder in ten prompts. Each was found by accident.

Add a BAD entry whenever a rule changes: the old wording becomes the pattern.
Lines that EXPLAIN a removed rule are skipped via the keyword filter, so a
handful of false positives on prohibition lines is expected and harmless.
"""
import pathlib
import re

# (label, regex, why it is wrong now)
BAD = [
    ('old CORE trail 20%', r'20% below high-water|trail 20%', 'CORE trail is 15% since 2026-09-15'),
    ('old CORE rung 14%', r'14% (?:once|at) \+30', 'CORE tightens to 12% at +30%'),
    ('old circuit breaker 3%', r'3%[- ]daily|3% of equity \(~\$6|<= *-?0?\.?03 of equity', 'breaker is 5%'),
    ('old fixed sizing', r'\$40 \(20%\)|\$40 = CORE|\$20 = TACTICAL|\$40 CORE / \$20', 'size is risk-derived'),
    ('deployment floor', r'75-85%|75%-85%', 'deployment has a ceiling only'),
    ('split machinery', r'\[SPLIT ok\]|SPLIT the qty|split: ~half|ORPHAN CHECK', 'split removed'),
    ('resting take-profit', r'resting `?limit`? sell at (?:the )?\+?1?4?|exchange-enforced upside',
     'no resting take-profit exists'),
    ('blanket -15% cut', r'any position at unrealized_plpc <= -0\.15', 'TACTICAL cuts at -6%'),
    ('bybit leftovers', r'bybit|BYBIT|orderLinkId|api-demo', 'reverted to Alpaca'),
]

SKIP = {'memory/TRADE-LOG.md', 'memory/RESEARCH-LOG.md', 'memory/WEEKLY-REVIEW.md',
        'DAILY-SUMMARY.md'}


def main():
    root = pathlib.Path('.')
    files = [p for p in root.rglob('*.md') if '.git' not in p.parts
             and 'archive' not in p.parts]
    files += list(root.glob('scripts/*.sh'))

    findings = 0
    for p in sorted(files):
        rel = p.as_posix().lstrip('./')
        if rel in SKIP:
            continue
        try:
            text = p.read_text(encoding='utf-8')
        except Exception:
            continue
        for i, line in enumerate(text.split('\n'), 1):
            # Lines that EXPLAIN the old rule are fine; lines that INSTRUCT are not.
            if re.search(r'removed|was |old |legacy |since 2026-09-15|NEVER infer|no longer|expired|REJECTED',
                         line, re.I):
                continue
            for label, pat, why in BAD:
                if re.search(pat, line, re.I):
                    print(f'  {rel}:{i}  [{label}] {why}')
                    print(f'      {line.strip()[:100]}')
                    findings += 1
    print(f'\n{findings} suspect line(s)')


if __name__ == '__main__':
    main()
