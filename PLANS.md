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

## Canonical gate map

- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`

## Active pack

- gates: `docs/planning/2026-03-30_HISTORICAL_EVALUATION_READINESS_GATES_v1.md`
- leaves: `docs/planning/2026-03-30_HISTORICAL_EVALUATION_READINESS_LEAVES_v1.json`
- execution log: `docs/planning/2026-03-30_HISTORICAL_EVALUATION_READINESS_EXECUTION_LOG_v1.md`
- document-touch checklist: `docs/planning/2026-03-30_HISTORICAL_EVALUATION_READINESS_DOCUMENT_TOUCH_CHECKLIST_v1.md`

## Latest closed pack retained as evidence

- gates: `docs/planning/2026-03-30_RESEARCH_MODE_CLARITY_MICROTRANCHE_GATES_v1.md`
- leaves: `docs/planning/2026-03-30_RESEARCH_MODE_CLARITY_MICROTRANCHE_LEAVES_v1.json`
- execution log: `docs/planning/2026-03-30_RESEARCH_MODE_CLARITY_MICROTRANCHE_EXECUTION_LOG_v1.md`
- document-touch checklist: `docs/planning/2026-03-30_RESEARCH_MODE_CLARITY_MICROTRANCHE_DOCUMENT_TOUCH_CHECKLIST_v1.md`
- closeout receipt: `docs/planning/2026-03-30_GATE114_RESEARCH_MODE_CLARITY_CLOSEOUT.md`

## Closed predecessor evidence

- `docs/planning/2026-03-30_EXECUTION_AUTHORITY_MICROTRANCHE_GATES_v1.md`
- `docs/planning/2026-03-30_EXECUTION_AUTHORITY_MICROTRANCHE_LEAVES_v1.json`
- `docs/planning/2026-03-30_EXECUTION_AUTHORITY_MICROTRANCHE_EXECUTION_LOG_v1.md`
- `docs/planning/2026-03-30_REPO_PROCESS_GOVERNANCE_GATES_v1.md`
- `docs/planning/2026-03-30_REPO_PROCESS_GOVERNANCE_LEAVES_v1.json`
- `docs/planning/2026-03-30_REPO_PROCESS_GOVERNANCE_EXECUTION_LOG_v1.md`
- `docs/planning/2026-03-30_TESTING_MODULE_GATES_v1.md`
- `docs/planning/2026-03-30_TESTING_MODULE_LEAVES_v1.json`
- `docs/planning/2026-03-30_TESTING_MODULE_EXECUTION_LOG_v1.md`
- `docs/planning/2026-03-30_TESTING_MODULE_SUCCESSOR_GATES_v1.md`
- `docs/planning/2026-03-30_TESTING_MODULE_SUCCESSOR_LEAVES_v1.json`
- `docs/planning/2026-03-30_TESTING_MODULE_SUCCESSOR_EXECUTION_LOG_v1.md`
- `docs/planning/2026-03-30_TESTING_MODULE_SUCCESSOR_SCOPE_NOTE_v1.md`

## Current state

- historical-evaluation readiness pack active from Gate 115
- Gates 115-116 are complete on `main`
- Gate 117 is the active gate
- Gates 118-121 are planned in dependency order and not yet executable

## Sequential execution rule

Active work proceeds one leaf at a time, one gate at a time, with one branch per gate.

## Anti-drift closeout rule

Before any later gate can be treated as active, the closing pass for the current gate must update all of the following together in the same branch:
1. repo-root `PLANS.md`
2. `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
3. the active leaf ledger named by the active pack
4. the active execution log named by the active pack

If no active pack exists, a new gate may not start until a new planning pack is created and routed here explicitly.
