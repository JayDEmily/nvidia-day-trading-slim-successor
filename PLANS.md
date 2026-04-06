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

- gates: `docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_GATES_v1.md`
- leaves: `docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_LEAVES_v1.json`
- execution log: `docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_EXECUTION_LOG_v1.md`
- document-touch checklist: `docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_DOCUMENT_TOUCH_CHECKLIST_v1.md`
- bounded-scope note: `docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_SCOPE_NOTE_v1.md`
- contradiction report: `docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_CONTRADICTION_REPORT_v1.md`
- retained-surface manifest and cutover rules: `docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_RETAINED_SURFACE_MANIFEST_AND_CUTOVER_RULES_v1.md`
- runtime-surface audit read-trigger and authority adoption: `docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_RUNTIME_SURFACE_AUDIT_READ_TRIGGER_AND_AUTHORITY_ADOPTION_v1.md`
- test-inventory classification and decision rules: `docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_TEST_INVENTORY_CLASSIFICATION_AND_DECISION_RULES_v1.md`
- test-audit proof slice and successor handoff: `docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_TEST_AUDIT_PROOF_SLICE_AND_SUCCESSOR_HANDOFF_v1.md`
- 07 source diff and AGENTS read-trigger note: `docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_07_SOURCE_DIFF_AND_AGENTS_READ_TRIGGER_NOTE_v1.md`
- next active gate: `Gate 219`

## Latest closed pack retained as evidence

- gates: `docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_GATES_v1.md`
- leaves: `docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_LEAVES_v1.json`
- execution log: `docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_EXECUTION_LOG_v1.md`
- document-touch checklist: `docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_DOCUMENT_TOUCH_CHECKLIST_v1.md`
- bounded-scope note: `docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_SCOPE_NOTE_v1.md`
- contradiction report: `docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_CONTRADICTION_REPORT_v1.md`
- cutover brief: `docs/planning/2026-04-06_GATE210_SLIM_ACTIVE_REPO_CUTOVER_ENTRY_CRITERIA.md`

## Latest closed predecessor evidence

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

## Current state

- active pack: slim active-repo cutover and substantive test-audit bootstrap pack with Gate 218 complete on `work/gate-218-retained-surface-inventory-and-runtime-authority-20260406`; Gate 219 not yet activated
- latest closed pack retained as evidence is the workflow hardening and active-repo reset foundation pack closed through Gate 210 on `work/gate-210-operator-surface-alignment-and-active-repo-cutover-criteria-20260406`
- latest closed predecessor evidence is the target-repo admitted-evidence successor planning pack closed through Gate 205 on `main`

## Sequential execution rule

Active work proceeds one leaf at a time, one gate at a time, with one branch per gate.

## Anti-drift closeout rule

Before any later gate can be treated as active, the closing pass for the current gate must update all of the following together in the same branch:
1. repo-root `PLANS.md`
2. `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
3. the active leaf ledger named by the active pack
4. the active execution log named by the active pack

If no active pack exists, a new gate may not start until a new planning pack is created and routed here explicitly.
