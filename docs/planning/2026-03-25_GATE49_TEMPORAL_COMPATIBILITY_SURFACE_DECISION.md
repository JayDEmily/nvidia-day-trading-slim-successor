# Gate 49 — Temporal Compatibility Surface Decision

Status: planned on current planning branch

## Purpose

Make an explicit architecture decision about whether outward `session_clock` surfaces remain as named compatibility wrappers or are retired in favour of `temporal_state`-named surfaces.

## Why this gate exists

Step 1 truth now lives in `temporal_state`, but several outward surfaces still expose `session_clock`. The repo needs an explicit migration policy instead of lingering halfway language.

## Leaves in Gate 49

1. `LEAF-G49-001` — inventory every outward `session_clock` surface across API, services, replay, schemas, tests, and docs.
2. `LEAF-G49-002` — choose and document the compatibility policy: keep-as-wrapper or retire-and-migrate.
3. `LEAF-G49-003` — implement the chosen policy across outward surfaces with bounded compatibility tests.
4. `LEAF-G49-004` — update docs, changelog, and rollback notes so the migration or wrapper policy is explicit and durable.

## Entry rule

Gate 46 must be complete, and Gate 48 must already define how close-state semantics are named upstream of carry.

## Exit rule

The repo has one explicit outward naming policy for Step 1, and tests enforce it.

## Non-goals

- no hidden renames of DMP payload identity;
- no silent API breakage;
- no reintroduction of elapsed-minute bucket truth.
