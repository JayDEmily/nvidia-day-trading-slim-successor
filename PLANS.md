# PLANS.md

## Purpose

This file is the canonical repo-root execution pointer.

## Active execution quartet

The governing gate authority is:
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`

The bounded-scope note is:
- `docs/planning/2026-03-24_CANONICAL_VISION_EXTENSION_EXECUTION_PLAN_v3.md`

The canonical leaf ledger is:
- `docs/planning/2026-03-24_CANONICAL_VISION_EXTENSION_LEAVES_v3.json`

The sequential execution log is:
- `docs/planning/2026-03-24_CANONICAL_VISION_EXTENSION_EXECUTION_LOG_v3.md`

`PLANS.md` remains short. Detailed execution logic lives in the active planning files above.

## Binding execution status

- Gates 0–7 — completed baseline on `main`
- Gates 8–23 — complete on `main`
- Gates 24–26 — retired superseded planning placeholders (never leafed on this persisted branch)
- Gate 27 — planning reset complete on `main`
- Gates 28–34 — complete on `main`
- Gates 35–39 — complete on `main`
- Gate 40 — complete on `main`
- Gates 41–44 — complete on `main`
- Gate 45 — downstream placeholder only

## Sequential execution rule

Active work proceeds one leaf at a time, one gate at a time, with the execution log carrying the receipts.

## Current repo state

The repo treats the completed desk rebuild plus doctrine/pointer freeze as the baseline, records Gate 7 explicitly as baseline leaf `LEAF-G7-BASELINE`, records Gate 27 as the planning reset that partitions the remaining 61 ready-for-contract-import items, records Gates 28 through 39 as the closed ingress, higher-order context, bridge, readiness, posture-core, orchestration, state-spine, exit-chain, review-spine, and feedback-overlay tranches, and closes Gate 40 through Gate 44 on `main`, leaving Gate 45 as the next downstream placeholder only.
