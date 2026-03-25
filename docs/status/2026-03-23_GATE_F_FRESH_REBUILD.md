# 2026-03-23 — Gate F fresh rebuild

## Scope

Rebuilt the replay, calibration, and stack-comparison harness from scratch on a
fresh Gate F work branch.

## What changed

- Replaced the old thin comparison scaffold with explicit stack-definition,
  coefficient-set, walk-forward-slice, run-result, audit-packet, and
  stack-versus-stack report contracts.
- Rebuilt `ReplayComparisonService` so replay now:
  - loads checked-in stack definitions and fixture packs;
  - filters active playbooks by stack definition;
  - applies module weights and sub-coefficients materially in replay scoring;
  - emits coefficient audit packets per run;
  - aggregates veto correctness, contradiction rate, playbook precision,
    review completeness, and deployable-capital metrics;
  - emits walk-forward slice reports and deterministic stack delta summaries;
  - serialises stable JSON reports.
- Added a checked-in Gate F replay regression fixture pack and a checked-in
  expected report baseline.
- Added a focused `make gate-f-check` target.

## Validation

- `make gate-f-check`
- `make check`

## Notes

The repo still contains earlier legacy replay-related modules for other
surfaces. Gate F was rebuilt by replacing the dedicated deterministic
comparison harness rather than attempting a risky repo-wide replay migration in
one pass.
