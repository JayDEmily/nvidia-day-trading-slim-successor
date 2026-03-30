# PLANS.md

## Purpose

This file is the canonical repo-root execution router.

## Frozen process-law surfaces

- `docs/01_NORMATIVE.md`
- `docs/02_OPERATING_MODEL.md`
- `docs/03_DOMAIN_MODEL.md`
- `docs/04_TECHNICAL_ARCHITECTURE.md`
- `docs/05_GUARDRAILS.md`
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `AGENTS.md`

## Active execution control surfaces

The governing canonical gate authority remains:
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`

The active governing pack is:
- `docs/planning/2026-03-30_REPO_PROCESS_GOVERNANCE_GATES_v1.md`

The active canonical leaf ledger is:
- `docs/planning/2026-03-30_REPO_PROCESS_GOVERNANCE_LEAVES_v1.json`

The active sequential execution log is:
- `docs/planning/2026-03-30_REPO_PROCESS_GOVERNANCE_EXECUTION_LOG_v1.md`

The active bounded-scope note is:
- none

Closed predecessor packs retained as evidence include:
- `docs/planning/2026-03-30_TESTING_MODULE_GATES_v1.md`
- `docs/planning/2026-03-30_TESTING_MODULE_LEAVES_v1.json`
- `docs/planning/2026-03-30_TESTING_MODULE_EXECUTION_LOG_v1.md`
- `docs/planning/2026-03-30_TESTING_MODULE_SUCCESSOR_GATES_v1.md`
- `docs/planning/2026-03-30_TESTING_MODULE_SUCCESSOR_LEAVES_v1.json`
- `docs/planning/2026-03-30_TESTING_MODULE_SUCCESSOR_EXECUTION_LOG_v1.md`
- `docs/planning/2026-03-30_TESTING_MODULE_SUCCESSOR_SCOPE_NOTE_v1.md`

## Active execution state

- Gate 107 — complete on `main` in the repo-process governance pack
- Gate 108 — next active gate on `main` in the repo-process governance pack

## Sequential execution rule

Active work proceeds one leaf at a time, one gate at a time, with one branch per gate.

## Anti-drift closeout rule

Before any later gate can be treated as active, the closing pass for the current gate must update all of the following together in the same branch:
1. repo-root `PLANS.md`
2. `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
3. the active leaf ledger named above
4. the active execution log named above

If no active pack exists, a new gate may not start until a new planning pack is created and routed here explicitly.
