# PLANS.md

## Purpose

This file is the canonical repo-root execution pointer.

## Active execution control surfaces

The governing canonical gate authority remains:
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`

The bounded-scope note remains:
- `docs/planning/2026-03-24_CANONICAL_VISION_EXTENSION_EXECUTION_PLAN_v3.md`

The canonical leaf ledger remains:
- `docs/planning/2026-03-24_CANONICAL_VISION_EXTENSION_LEAVES_v3.json`

The sequential execution log remains:
- `docs/planning/2026-03-24_CANONICAL_VISION_EXTENSION_EXECUTION_LOG_v3.md`

The active successor modification pair for Gate 51 onward is:
- `docs/planning/2026-03-26_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v1.md`
- `docs/planning/2026-03-26_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v1.json`

`PLANS.md` remains short. Detailed execution logic lives in the planning files above.

## Binding execution status

- Gates 0–7 — completed baseline on `main`
- Gates 8–23 — complete on `main`
- Gates 24–26 — retired superseded planning placeholders (never leafed on the persisted main branch)
- Gate 27 — planning reset complete on `main`
- Gates 28–34 — complete on `main`
- Gates 35–39 — complete on `main`
- Gate 40 — complete on `main`
- Gates 41–44 — complete on `main`
- Gate 45 — retired placeholder on `main`
- Gates 46–50 — complete on `main`
- Gate 51 — complete on `main`
- Gate 52 — complete on `main`
- Gate 53 — complete on `main`
- Gates 54–55 — planned in the cognitive workflow modification pack

## Sequential execution rule

Active work proceeds one leaf at a time, one gate at a time, with the execution log carrying the receipts once execution begins.

## Current repo state

The persisted `main` baseline is now closed through Gate 51 and records Gate 7 explicitly as baseline leaf `LEAF-G7-BASELINE`. Gates 46–50 are merged on `main`, and Gate 51 closes the workflow-ownership planning pass by:
- freezing the pre-implementation audit in-repo;
- replacing the flat playbook registry with registry v2 hierarchy;
- formalising close-state to carry-horizon handoff for overnight, weekend, and event carry;
- keeping `session_clock` as an explicit outward compatibility wrapper while exposing canonical `temporal_state` surfaces;
- rebasing vocabulary governance onto the current architecture with enforcement tests;
- pinning workflow-stage ownership, candidate-generation boundaries, Step 0 calendar/horizon routing, and carry-branch boundary semantics in Gate 51 planning artefacts.

The next gate is Gate 54 in the cognitive workflow modification pack.
