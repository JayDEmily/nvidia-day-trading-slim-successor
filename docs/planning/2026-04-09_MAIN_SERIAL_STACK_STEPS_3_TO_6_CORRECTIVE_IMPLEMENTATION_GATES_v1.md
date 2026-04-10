# 2026-04-09_MAIN_SERIAL_STACK_STEPS_3_TO_6_CORRECTIVE_IMPLEMENTATION_GATES_v1

Status: closed planning pack for Gates 236-241 retained as evidence. The pack is closed through Gate 241 in the uploaded workspace copy; no active pack is currently routed.
Version: v1.0

## Purpose

Create the next execution-grade planning tranche for the slim successor repo by correcting the main serial stack across the canonical stages `Options and Flow Context`, `Posture and Risk Permission`, `Playbook Eligibility`, and `Expression and Execution` so the runtime restores clean separation between description, permission, selection, and recommendation without broad optimisation drift.

## Scope

In scope:
- main-serial-stack corrective work for the canonical stages `Options and Flow Context`, `Posture and Risk Permission`, `Playbook Eligibility`, and `Expression and Execution`;
- schema, runtime, and lawful downstream-handoff corrections needed to remove cumulative posture/risk contamination across Steps 3-6;
- bounded DMP/review/handoff updates required to preserve step-local meaning after the contracts are corrected;
- targeted proof using the existing runtime, trace-ledger, perturbation, and acceptance-corpus surfaces.

Out of scope:
- alpha tuning, heuristic quality improvement, or playbook expansion;
- broad redesign outside the Step 3-6 correction boundary;
- close-position logic, carry-horizon lifecycle work, or portfolio-brain logic;
- replacing the repo's existing proof framework with a new test framework;
- routing this pack prematurely without the normal quartet update through repo-root control surfaces.

## Supersession and active authority

- This document is a draft successor pack for planned Gates 236-241.
- It does not become active authority until a later execution thread routes it truthfully through repo-root `PLANS.md`, the canonical gate map, the active leaves ledger, and the active execution log.
- The latest closed retained pack remains evidence input only; it is not the structural template for this tranche:
  - `docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_GATES_v1.md`
  - `docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_LEAVES_v1.json`
  - `docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_EXECUTION_LOG_v1.md`
- The corrective behavioural authority for this pack is the operator-supplied brief `steps_3_to_6_corrective_brief_main_serial_stack_2026-04-09.md`.
- The canonical naming, routing, packet, and workflow-control authorities remain the live repo control surfaces until a later gate edits them lawfully.

## Governing inputs

Frozen doctrine and process inputs:
- `docs/01_NORMATIVE.md`
- `docs/02_OPERATING_MODEL.md`
- `docs/03_DOMAIN_MODEL.md`
- `docs/04_TECHNICAL_ARCHITECTURE.md`
- `docs/05_GUARDRAILS.md`
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md`
- `docs/08_TESTING_AND_PROMOTION.md`
- `AGENTS.md`
- repo-root `PLANS.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`
- `docs/vocabulary/README.md`
- `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`

Evidence-input surfaces reread before drafting this pack:
- `/mnt/data/steps_3_to_6_corrective_brief_main_serial_stack_2026-04-09.md`
- `/mnt/data/serial_stack_gate_leaf_execution_brief_2026-04-09.md`
- `docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_SCOPE_NOTE_v1.md`
- `docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_CONTRADICTION_REPORT_v1.md`
- `docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_LEAVES_v1.json`
- `docs/planning/2026-04-03_GATE188_CAPITAL_DEPLOYMENT_AUTHORITY_CONTRACT.md`

Live workflow/code surfaces traced before drafting this pack:
- `src/nvda_desk/services/cognition_runtime.py`
- `src/nvda_desk/services/options_flow_context.py`
- `src/nvda_desk/services/posture_risk.py`
- `src/nvda_desk/services/playbook_eligibility.py`
- `src/nvda_desk/services/execution_expression.py`
- `src/nvda_desk/services/risk_gateway.py`
- `src/nvda_desk/services/capital_deployment_authority.py`
- `src/nvda_desk/services/review_explanation.py`
- `src/nvda_desk/services/parallel_risk_lane.py`
- `src/nvda_desk/schemas/cognition.py`
- `src/nvda_desk/schemas/parallel_risk.py`
- `src/nvda_desk/schemas/dmp_v2.py`
- `src/nvda_desk/testing/canonical_runtime_harness.py`
- `src/nvda_desk/testing/cognition_fixtures.py`
- `src/nvda_desk/testing/bounded_trace_review.py`

## Workflow placement

This tranche sits inside the opening-position serial cognition path after `Market Regime Context` and before bounded downstream opening-position consumers.

It is a bounded derivation and handoff-correction tranche, not an upstream raw-data tranche and not a review-only tranche.

The canonical workflow anchor for this pack is:

`Temporal Context -> Market Regime Context -> Options and Flow Context -> Posture and Risk Permission -> Playbook Eligibility -> Expression and Execution -> bounded downstream consumers -> Review and Explanation`

This pack uses six gates because the operator-supplied execution brief fixes six distinct responsibilities that must remain independently testable:
1. Step 3 contract isolation;
2. Step 4 contract rewrite;
3. Step 5 decontamination;
4. Step 6 boundary cleanup;
5. cross-step boundary enforcement; and
6. acceptance-corpus revalidation.

Adding or collapsing gates at planning time would blur the exact defect boundary the brief is trying to restore.

## Retain / retire-from-authority / amend / add matrix

### Retain as canonical
- the seven-stage serial spine and current stage order;
- `Options and Flow Context`, `Posture and Risk Permission`, `Playbook Eligibility`, and `Expression and Execution` as the canonical Step 3-6 stage labels;
- `Stage-Local Handoff`, `Modifier Runtime Packet`, `Independent Parallel Risk Lane`, and `Capital Deployment Authority Service` as bounded downstream/runtime surfaces rather than replacements for the serial stack;
- targeted proof through existing runtime and trace-ledger infrastructure rather than broad blind repo sweeps.

### Retire from authority (compatibility-only unless later removed)
- any Step 3 output shape that behaves as hidden permission, hidden veto, or capital semantics;
- any Step 4 surface that acts as deployable-capital state instead of a bounded local permission envelope;
- any Step 5 logic that re-runs posture or reuses posture-derived caution as a generic downstream veto;
- any Step 6 output or runtime join that behaves as fresh-capital sizing or allocator logic inside the serial recommendation layer.

### Mandatory amendments
- `src/nvda_desk/schemas/cognition.py` because the Step 3-6 output contracts currently carry permission reuse and capital-semantics fields across stage boundaries;
- `src/nvda_desk/services/posture_risk.py` because posture currently emits deployable-capital and inventory-bias state that exceeds the corrective brief's permission-envelope boundary;
- `src/nvda_desk/services/playbook_eligibility.py` because eligibility currently consumes posture state in ways that risk repeating posture rather than selecting within a single-use envelope;
- `src/nvda_desk/services/execution_expression.py` because execution currently carries target fresh-deployable sizing semantics and posture re-application inside the recommendation layer;
- `src/nvda_desk/services/cognition_runtime.py` and bounded downstream handoff surfaces because the runtime currently preserves pre-final-risk execution but still mutates execution and carries capital-oriented semantics across the handoff boundary.

### New additions
- one new Gates 236-241 pack for the main serial stack Step 3-6 corrective tranche;
- one new supporting leaves ledger;
- one new supporting contradiction report;
- one new supporting document-touch checklist;
- one new supporting execution log surface for later gate execution;
- one new supporting scope note.

## Vocabulary discipline

- The canonical vocabulary file remains mandatory authority for gate titles, leaf titles, durable planning labels, and future code naming in this tranche.
- The operator brief uses vernacular labels for explanatory richness. This pack maps them explicitly and does not promote them to durable authority:
  - `Flow / Pressure` -> `Options and Flow Context`
  - `Posture / Idea Permission Envelope` -> `Posture and Risk Permission`
  - `Playbook Ladder` -> `Playbook Eligibility`
  - `Serial Output` -> `Expression and Execution`
- Do not use the vernacular labels as new schema, field, class, or gate names unless a later vocabulary leaf routes the admission workflow first.
- Reuse these canonical labels and exact code symbols where applicable: `Stage-Local Handoff`, `Modifier Runtime Packet`, `Independent Parallel Risk Lane`, `Execution Candidate Ownership`, `Overlay Risk Decision`, `Terminal Risk Application`, `Terminal Risk Decision`, `Capital Deployment Authority Service`, and `Capital Deployment Authority Decision`.

## Packet / contract discipline

- `docs/03_DOMAIN_MODEL.md` remains the baseline packet/data-contract authority.
- `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md` remains the latest-state ownership and lawful-reader authority.
- `final_risk_join` remains a compatibility/runtime surface unless a later executed leaf changes that law explicitly.
- The operator brief is authoritative for behavioural correction, but the coding thread must still carry contract changes through the canonical repo-native packet surfaces rather than inventing off-ledger compatibility paths.

## Contradiction scan and state-integrity rules

- The draft contradiction scan is recorded in `docs/planning/2026-04-09_MAIN_SERIAL_STACK_STEPS_3_TO_6_CORRECTIVE_IMPLEMENTATION_CONTRADICTION_REPORT_v1.md`.
- No blocking routing contradiction was found before this pack was written.
- The key non-blocking contradictions are frozen as execution drivers:
  - the operator brief treats the corrective behaviour as authoritative while the repo still requires canonical vocabulary and control-surface law;
  - the corrective brief prohibits capital semantics across Steps 3-6 while the live code still carries deployable-capital state through posture, execution, and bounded downstream consumers;
  - the live runtime still preserves a pre-final-risk seam and then mutates execution before the `Capital Deployment Authority Service` consumes it.
- Closeout invariants for later execution remain:
  - `completed_leaf_ids` and `remaining_leaf_ids` stay disjoint;
  - every referenced leaf id exists in the active leaves ledger;
  - `active_gate = none` is lawful only when `remaining_leaf_ids` and `pending_gate_ids` are empty;
  - the pack is not truthfully closed until Gate 241 records acceptance-corpus proof and the router surfaces move together.

## Document-touch checklist

The checklist file for this tranche is `docs/planning/2026-04-09_MAIN_SERIAL_STACK_STEPS_3_TO_6_CORRECTIVE_IMPLEMENTATION_DOCUMENT_TOUCH_CHECKLIST_v1.md`.
If execution proceeds later, the coding thread must move the checklist together with the gate master, leaves ledger, execution log, and repo-root router surfaces when a gate closeout requires it.

## Testing and promotion discipline

- Repo-local environment required for later execution: `.venv` via repo doctrine `make install` / `uv sync --extra dev`.
- If the later execution sandbox cannot resolve all dependencies online, use the operator-supplied dependency bundle and attached bootstrap instructions rather than changing the repo's dependency law.
- Minimum validation slices by gate are declared in the leaves ledger and remain targeted rather than broad full-suite by default.
- A gate is not complete until:
  - targeted tests ran green in the repo-local environment;
  - `PLANS.md`, the canonical gate map, the active leaves ledger, and the active execution log all moved together when routing state changed;
  - exact branch / commit / validation receipts were recorded in the execution log;
  - a fresh zip was created only when the operator explicitly requested backup, offline handoff, or sandbox transfer packaging.

## Gates

### Gate 236: Step 3 contract isolation for `Options and Flow Context`

**Objective**
- Make `Options and Flow Context` a purely descriptive Step 3 surface and route the new pack cleanly when execution begins.

**In-scope surfaces**
- `PLANS.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- `docs/planning/2026-04-09_MAIN_SERIAL_STACK_STEPS_3_TO_6_CORRECTIVE_IMPLEMENTATION_GATES_v1.md`
- `docs/planning/2026-04-09_MAIN_SERIAL_STACK_STEPS_3_TO_6_CORRECTIVE_IMPLEMENTATION_LEAVES_v1.json`
- `docs/planning/2026-04-09_MAIN_SERIAL_STACK_STEPS_3_TO_6_CORRECTIVE_IMPLEMENTATION_EXECUTION_LOG_v1.md`
- `src/nvda_desk/services/options_flow_context.py`
- `src/nvda_desk/services/cognition_runtime.py`
- `src/nvda_desk/schemas/cognition.py`
- `tests/test_options_flow_context.py`
- `tests/test_gate236_main_serial_step3_contract_isolation.py`

**Definition of done**
- the pack is routed truthfully before Gate 236 execution begins and only Gate 236 is active;
- `Options and Flow Context` emits descriptive landscape state only, with no hidden permission, hidden veto, or capital semantics;
- the Step 3 -> Step 4 interface is explicit, typed, and readable without ambient interpretation;
- targeted Step 3 tests prove descriptive-only behaviour and preserve lawful existing richness.

### Gate 237: Step 4 contract rewrite for `Posture and Risk Permission`

**Objective**
- Rewrite `Posture and Risk Permission` into a bounded local permission envelope that carries no deployable-capital or allocator semantics.

**In-scope surfaces**
- `src/nvda_desk/services/posture_risk.py`
- `src/nvda_desk/services/cognition_runtime.py`
- `src/nvda_desk/schemas/cognition.py`
- `tests/test_posture_risk_and_playbook.py`
- `tests/test_gate237_main_serial_step4_permission_envelope.py`

**Definition of done**
- the Step 4 output contract is reduced to bounded permission-envelope semantics rather than deployable-capital state;
- downstream readers stop consuming Step 4 as generic reusable caution or capital allowance;
- the runtime preserves Step 4 as a single local translation from description to permission;
- targeted tests prove the envelope is applied once and not silently re-used as a later veto.

### Gate 238: Step 5 decontamination for `Playbook Eligibility`

**Objective**
- Ensure `Playbook Eligibility` selects lawful candidates within the Step 4 envelope instead of re-running posture or reusing posture-derived caution as a generic suppressor.

**In-scope surfaces**
- `src/nvda_desk/services/playbook_eligibility.py`
- `src/nvda_desk/services/cognition_runtime.py`
- `src/nvda_desk/schemas/cognition.py`
- `tests/test_posture_risk_and_playbook.py`
- `tests/test_gate238_main_serial_step5_playbook_decontamination.py`

**Definition of done**
- Step 5 consumes the Step 4 envelope once and does not repeat posture logic under another name;
- duplicate veto paths and generic permission reuse are removed from playbook evaluation;
- candidate filtering and lead-selection preparation remain lawful and deterministic;
- targeted tests prove eligibility is selection-only within the envelope.

### Gate 239: Step 6 output boundary cleanup for `Expression and Execution`

**Objective**
- Make `Expression and Execution` a pure stateless recommendation layer with clean bounded downstream handoff and no embedded capital-deployment authority.

**In-scope surfaces**
- `src/nvda_desk/services/execution_expression.py`
- `src/nvda_desk/services/cognition_runtime.py`
- `src/nvda_desk/services/capital_deployment_authority.py`
- `src/nvda_desk/schemas/cognition.py`
- `tests/test_execution_review_runtime.py`
- `tests/test_gate239_main_serial_step6_recommendation_boundary.py`

**Definition of done**
- the Step 6 output contract is stateless recommendation-only and no longer carries hidden allocator or target-deployment behaviour;
- Step 6 does not re-apply posture beyond the lawful Step 5 candidate boundary;
- bounded downstream consumers receive a clean recommendation handoff and any later capital decision remains explicitly downstream;
- targeted tests prove recommendation purity and deterministic output stability.

### Gate 240: Cross-step boundary enforcement across Steps 3-6

**Objective**
- Enforce clean data-flow boundaries across `Options and Flow Context`, `Posture and Risk Permission`, `Playbook Eligibility`, and `Expression and Execution`, including the preserved seam and review-visible carriage.

**In-scope surfaces**
- `src/nvda_desk/services/cognition_runtime.py`
- `src/nvda_desk/services/review_explanation.py`
- `src/nvda_desk/services/risk_gateway.py`
- `src/nvda_desk/schemas/cognition.py`
- `src/nvda_desk/schemas/dmp_v2.py`
- `tests/test_gate229_serial_opportunity_ladder_and_non_cumulative_risk.py`
- `tests/test_gate230_opening_position_seam_and_downstream_handoff.py`
- `tests/test_gate240_main_serial_cross_step_boundary_enforcement.py`

**Definition of done**
- Step 3 remains descriptive only, Step 4 remains permission only, Step 5 remains selection only, and Step 6 remains recommendation only;
- stage-local, review-visible, and compatibility carriage preserve meaning without reintroducing cumulative risk contamination;
- no same-pass serial path silently reuses posture-derived caution as a generic downstream suppressor;
- targeted boundary tests prove the corrected seam and lawful downstream carriage.

### Gate 241: Acceptance corpus revalidation and pack closeout

**Objective**
- Prove the corrective defect no longer reproduces using the repo's existing trace-ledger, perturbation, and deterministic runtime proof surfaces, then close the pack truthfully.

**In-scope surfaces**
- `src/nvda_desk/testing/canonical_runtime_harness.py`
- `src/nvda_desk/testing/cognition_fixtures.py`
- `src/nvda_desk/testing/bounded_trace_review.py`
- `tests/test_gate241_main_serial_acceptance_corpus_revalidation.py`
- `tests/test_dmp_review_trace.py`
- `tests/test_gate132_bounded_trace_scenario_pack.py`
- `tests/test_gate133_bounded_trace_review_regime.py`
- `tests/test_gate134_bounded_trace_reporting.py`
- `tests/test_gate143_stage_local_handoff_runtime.py`
- `tests/test_gate146_admissibility_candidate_ownership.py`
- `tests/test_gate147_overlay_terminal_risk_runtime.py`

**Definition of done**
- the pre-fix defect is either reproduced from the starting point and then shown not to reproduce post-fix, or a truthful equivalent regression witness is recorded from the existing acceptance corpus;
- structural trace, behavioural trace, and perturbation slices all pass deterministically on the corrected boundary;
- the pack closes with router surfaces synchronized, no remaining leaves, and truthful execution receipts;
- the repo is ready for the next tranche without ambiguity about the Step 3-6 boundary law.
