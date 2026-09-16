# Scan Gate — shadow validation log

`scripts/state.sh` prints a `SCAN-VERDICT:` line predicting whether a scan run
has any work to do. It is ADVISORY ONLY right now: runs ignore it and execute in
full, and log here what the verdict said against what the run actually did.

Purpose: prove the gate never says NO-ACTION on a run that acted. One such
disagreement is a defect — do NOT enable the gate until the count is zero over a
meaningful sample (~50 runs, about two days at hourly).

The gate fails open by construction: unknown sleeve, unreadable stop price,
missing price, odd order counts and near-threshold P&L all force ACTION. So the
expected failure mode is a needless ACTION, never a missed one.

Rows are appended ONLY by runs that acted. A quiet run logs nothing and commits
nothing, so the hourly cadence stays cheap during validation. That loses no
signal: a quiet run agrees with the verdict either way (NO-ACTION is correct,
ACTION is the safe direction), and the only defect worth catching is a run that
acted after a NO-ACTION verdict — which always produces a row.

| UTC | verdict | what the run did | agree? |
|-----|---------|------------------|--------|

`agree?` is NO only when verdict=NO-ACTION. Any such row blocks enabling the gate
until it is explained and fixed.

## Rows
