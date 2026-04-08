# PLANS.md

## Purpose

This file is the canonical repo-root execution router.
It names the live planning authority and the nearest retained evidence classes; detailed taxonomy law lives in `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`.

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

## Planning taxonomy

- active pack authority: the pack named under `## Active pack`; these are the only live planning surfaces under `docs/planning/`
- latest closed pack retained as evidence: the most recent closed pack kept for closeout context and comparison; not active authority
- latest closed predecessor evidence: the closed pack immediately before the latest retained pack; predecessor context only, not active authority
- older historical planning material: earlier closed planning artefacts under `docs/planning/`; historical only unless this router names them as active
- evidence-input-only material: companion notes such as closeout receipts, scope notes, contradiction reports, salvage matrices, and indexes; informative only unless this router names one as an active surface

## Active pack

- none

## Latest closed pack retained as evidence

- gates: `docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_GATES_v1.md`
- leaves: `docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_LEAVES_v1.json`
- execution log: `docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_EXECUTION_LOG_v1.md`
- document-touch checklist: `docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_DOCUMENT_TOUCH_CHECKLIST_v1.md`
- bounded-scope note: `docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_SCOPE_NOTE_v1.md`
- contradiction report: `docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_CONTRADICTION_REPORT_v1.md`

## Latest closed predecessor evidence

- gates: `docs/planning/2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_GATES_v1.md`
- leaves: `docs/planning/2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_LEAVES_v1.json`
- execution log: `docs/planning/2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_EXECUTION_LOG_v1.md`
- document-touch checklist: `docs/planning/2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_DOCUMENT_TOUCH_CHECKLIST_v1.md`
- bounded-scope note: `docs/planning/2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_SCOPE_NOTE_v1.md`
- contradiction report: `docs/planning/2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_CONTRADICTION_REPORT_v1.md`

## Older historical planning material

- earlier closed planning artefacts remain under `docs/planning/` as historical-only material, including `docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_GATES_v1.md`, `docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_GATES_v1.md`, the workflow hardening and active-repo reset foundation pack, the slim active-repo cutover and substantive test-audit bootstrap pack, and the 2026-04-05 target-repo admitted-evidence successor pack with their closeout/handoff surfaces.

## Current state

- no active pack currently routed; the opening-position domain isolation and interface hardening pack is closed through Gate 235 on `work/gate-235-cross-flow-harness-and-pack-closeout-20260408`
- latest closed pack retained as evidence is the opening-position domain isolation and interface hardening pack closed through Gate 235 on `work/gate-235-cross-flow-harness-and-pack-closeout-20260408`
- latest closed predecessor evidence is the successor retained-test cleanup execution pack closed through Gate 225 on `work/gate-225-retained-test-cleanup-closeout-20260406`

## Sequential execution rule

Active work proceeds one leaf at a time, one gate at a time, with one branch per gate.

## Anti-drift closeout rule

Before any later gate can be treated as active, the closing pass for the current gate must update all of the following together in the same branch:
1. repo-root `PLANS.md`
2. `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
3. the active leaf ledger named by the active pack
4. the active execution log named by the active pack

If no active pack exists, a new gate may not start until a new planning pack is created and routed here explicitly.
