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

- gates: `docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_GATES_v1.md`
- leaves: `docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_LEAVES_v1.json`
- execution log: `docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_EXECUTION_LOG_v1.md`
- document-touch checklist: `docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_DOCUMENT_TOUCH_CHECKLIST_v1.md`
- bounded-scope note: `docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_SCOPE_NOTE_v1.md`
- contradiction report: `docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_CONTRADICTION_REPORT_v1.md`
- next active gate: `Gate 208`

## Latest closed pack retained as evidence

- gates: `docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_GATES_v1.md`
- leaves: `docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_LEAVES_v1.json`
- execution log: `docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_EXECUTION_LOG_v1.md`
- document-touch checklist: `docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_DOCUMENT_TOUCH_CHECKLIST_v1.md`
- bounded-scope note: `docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_SCOPE_NOTE_v1.md`
- contradiction report: `docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_CONTRADICTION_REPORT_v1.md`
- salvage matrix: `docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_SALVAGE_MATRIX_v1.md`
- index / cross-reference: `docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_INDEX_AND_CROSS_REFERENCE_v1.md`
- closeout proof-order and receipt requirements: `docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_CLOSEOUT_PROOF_ORDER_AND_RECEIPT_REQUIREMENTS_v1.md`
- planning-to-coding handoff boundary: `docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_PLANNING_TO_CODING_HANDOFF_BOUNDARY_v1.md`
- closeout receipt: `docs/planning/2026-04-05_GATE205_TARGET_REPO_SUCCESSOR_PACK_CLOSEOUT_AND_HANDOFF.md`

## Latest closed predecessor evidence

- gates: `docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_GATES_v1.md`
- leaves: `docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_LEAVES_v1.json`
- execution log: `docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_EXECUTION_LOG_v1.md`
- document-touch checklist: `docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_DOCUMENT_TOUCH_CHECKLIST_v1.md`
- bounded-scope note: `docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_SCOPE_NOTE_v1.md`
- evidence baseline: `docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_EVIDENCE_BASELINE_v1.md`
- source-truth matrix: `docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_SOURCE_TRUTH_MATRIX_v1.md`
- closeout receipt: `docs/planning/2026-04-04_GATE199_PHASE3_MAIN_TARGET_REPAIR_CLOSEOUT.md`

## Current state

- active pack: workflow hardening and active-repo reset foundation pack with Gate 208 active on `work/gate-207-router-and-doctrine-consolidation-20260406`
- latest closed pack retained as evidence is the target-repo admitted-evidence successor planning pack closed through Gate 205 on `main`
- latest closed predecessor evidence is the Phase 3 main-target repair programme closed through Gate 199 on `main`

## Sequential execution rule

Active work proceeds one leaf at a time, one gate at a time, with one branch per gate.

## Anti-drift closeout rule

Before any later gate can be treated as active, the closing pass for the current gate must update all of the following together in the same branch:
1. repo-root `PLANS.md`
2. `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
3. the active leaf ledger named by the active pack
4. the active execution log named by the active pack

If no active pack exists, a new gate may not start until a new planning pack is created and routed here explicitly.
