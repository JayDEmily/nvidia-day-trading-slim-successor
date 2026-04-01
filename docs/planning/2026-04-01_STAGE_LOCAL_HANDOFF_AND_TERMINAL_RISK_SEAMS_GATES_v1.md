Status: active stage-local handoff and terminal-risk seams pack; Gates 141-148 complete on `main`, Gate 149 active
# 2026-04-01 Stage-Local Handoff and Terminal-Risk Seams Gates v1

## Purpose

Create a clean post-Gate-140 survivor tranche from observed Repo B truth only.

This pack exists to do four things only:
1. activate one new bounded planning pack from the clean Gate 140 baseline on `main`;
2. freeze the observed current runtime handoff chain, terminal-risk authority step, and downstream review-consumer dependencies before any seam edits begin;
3. route later gates so execution can proceed one bounded seam at a time without improvising vocabulary, packet meaning, or stage ownership;
4. keep the router, gate map, leaves ledger, execution log, and changelog truthful while Gate 142 becomes the first runtime-facing gate.

## Why this pack exists

The current deterministic runtime already carries richer execution-stage truth than the pre-Gate-135 baseline, but the live workflow still concentrates multiple downstream authorities inside the same in-place chain: posture is enriched and then modifier-mutated before eligibility runs; execution is compiled and then modifier-mutated again before final-risk application; review consumes the already-mutated execution packet plus the modifier packet rather than a preserved stage-local handoff set.

The repo needs one clean tranche that starts from observed current code and contract truth, not from chat memory, discarded drafts, or speculative architecture. Gate 141 is therefore planning plus workflow-trace only. It does not change runtime behaviour.

## Scope

In scope:
- one new active planning quartet for Gates 141-149;
- current-state workflow trace across the observed handoff chain from posture through review;
- explicit vocabulary and packet/data authority freeze for the later seam work;
- granular leaves sufficient for later coding threads to execute one gate at a time without inventing scope;
- router, gate-map, changelog, and planning-guard updates required to close Gate 141 honestly and advance the repo to Gate 142.

Out of scope:
- runtime code edits in `src/` during Gate 141;
- admission of new governed runtime vocabulary in Gate 141;
- packet/schema changes in Gate 141;
- replay, review, or broker-boundary behaviour changes in Gate 141;
- any attempt to treat discarded same-day planning artefacts as authority.

## Supersession and active authority

- This document becomes the active gate authority for Gates 141-149.
- It supersedes the no-active-pack state that followed clean Gate 140 closeout.
- The latest closed corrective evidence remains the Gate 140 Alembic parity pack.
- Gate 141 is planning-only and is complete on `main` once the router, gate map, leaves ledger, execution log, guard tests, and changelog agree.

## Governing inputs

- `docs/01_NORMATIVE.md`
- `docs/02_OPERATING_MODEL.md`
- `docs/03_DOMAIN_MODEL.md`
- `docs/04_TECHNICAL_ARCHITECTURE.md`
- `docs/05_GUARDRAILS.md`
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `AGENTS.md`
- repo-root `PLANS.md`
- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`
- `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- `docs/TESTING_AND_PROMOTION.md`
- `src/nvda_desk/schemas/cognition.py`
- `src/nvda_desk/services/cognition_runtime.py`
- `src/nvda_desk/services/posture_risk.py`
- `src/nvda_desk/services/state_conditioned_modifier.py`
- `src/nvda_desk/services/playbook_eligibility.py`
- `src/nvda_desk/services/execution_expression.py`
- `src/nvda_desk/services/risk_gateway.py`
- `src/nvda_desk/services/review_explanation.py`
- `tests/test_gate140_execution_ledger_alembic_parity.py`
- `tests/test_execution_review_runtime.py`
- planning-governance tests that guard router truth and active-pack activation

## Active vocabulary authority for execution threads

`docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json` remains the mandatory vocabulary authority for every execution leaf in this pack until a later leaf lawfully amends it.

Canonical vocabulary already admitted and mandatory for this pack:
- `posture_risk_permission`
- `playbook_eligibility`
- `execution_expression`
- `review_explanation`
- `modifier_runtime_packet`
- `position_context`
- `lifecycle_plan`
- `carry_handoff`
- `carry_horizon_branch`

Planning-language only unless a later leaf admits them formally through the vocabulary workflow:
- `stage-local handoff artefact`
- `ownership inventory`
- `terminal-risk application seam`
- `overlap class`

`FinalRiskJoinSurface` may still be cited as the existing packet/data contract name from `docs/03_DOMAIN_MODEL.md` and `src/nvda_desk/schemas/cognition.py`, but Gate 141 does not treat it as a newly admitted canonical vocabulary slug.

## Active packet / data contract authority for execution threads

`docs/03_DOMAIN_MODEL.md` is the mandatory packet/data contract authority for every execution leaf in this pack.

Live schema and service files are implementation surfaces only. They must not be treated as substitutes for the domain model when packet meaning, lineage, stage ownership, or lawful downstream consumption is in question.

## Workflow placement

This tranche spans the downstream seam between Stage 4 (`posture_risk_permission`), Stage 5 (`playbook_eligibility`), Stage 6 (`expression_execution`), the final-risk application step already carried on `ExecutionExpressionOutput.final_risk_join`, and Stage 7 (`review_explanation`).

Gate 141 freezes the observed workflow before any runtime edit:
1. `DeskCognitionRuntime.run(...)` computes posture, adds contract citations, evaluates the modifier packet, and mutates posture before eligibility.
2. eligibility consumes the mutated posture and adds contract citations.
3. execution consumes posture, eligibility, the modifier packet, and the additive `position_context` surface.
4. modifier logic mutates execution after the execution service returns.
5. `RiskGatewayService.evaluate_runtime_join(...)` computes the terminal decision, and `apply_final_join(...)` mutates execution again.
6. review consumes the final mutated execution packet together with `modifier_runtime_packet`.
7. stage packets are built from the final stage outputs only.

The later gates exist to replace that hidden concentration with explicit observed seams, but Gate 141 itself does not prejudge the final implementation beyond freezing the current-state trace.

## Retain / retire-from-authority / amend / add matrix

### Retain as canonical
- the clean Gate 140 runtime and persistence baseline on `main`;
- the current DMP v2 packet envelope and stage ordering frozen by `docs/03_DOMAIN_MODEL.md`;
- the currently admitted lifecycle and carry vocabulary from Gates 135-140;
- the existing Gate 140 corrective pack as latest closed corrective evidence.

### Retire from authority
- the assumption that no new planning pack is required after Gate 140 closeout;
- any attempt to execute later seam work without first freezing the current runtime workflow, vocabulary authority, and packet/data authority explicitly.

### Mandatory amendments
- repo-root `PLANS.md`;
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`;
- `CHANGELOG.jsonl`;
- planning-governance tests that guard router truth and active-pack activation.

### New additions
- `docs/planning/2026-04-01_STAGE_LOCAL_HANDOFF_AND_TERMINAL_RISK_SEAMS_GATES_v1.md`
- `docs/planning/2026-04-01_STAGE_LOCAL_HANDOFF_AND_TERMINAL_RISK_SEAMS_LEAVES_v1.json`
- `docs/planning/2026-04-01_STAGE_LOCAL_HANDOFF_AND_TERMINAL_RISK_SEAMS_EXECUTION_LOG_v1.md`
- `docs/planning/2026-04-01_STAGE_LOCAL_HANDOFF_AND_TERMINAL_RISK_SEAMS_DOCUMENT_TOUCH_CHECKLIST_v1.md`
- `docs/planning/2026-04-01_GATE141_STAGE_LOCAL_HANDOFF_PACK_BOOTSTRAP.md`
- `tests/test_gate141_stage_local_handoff_terminal_risk_seams_planning.py`

## Document-touch checklist

Checklist file: `docs/planning/2026-04-01_STAGE_LOCAL_HANDOFF_AND_TERMINAL_RISK_SEAMS_DOCUMENT_TOUCH_CHECKLIST_v1.md`

## Testing and promotion discipline

- Repo-local environment required: `.venv` created via `uv sync --extra dev`
- Gate 141 is planning-only, so the minimum proof slice is the planning-governance test suite plus the new Gate 141 activation test:
  - `.venv/bin/python -m pytest -q tests/test_gate141_stage_local_handoff_terminal_risk_seams_planning.py tests/test_gate135_opening_drive_continuation_lifecycle_planning.py tests/test_gate134_bounded_trace_reporting.py tests/test_gate128_post_flight_repo_consistency_planning.py tests/test_gate122_signal_coefficient_authority_planning.py tests/test_gate115_historical_evaluation_readiness_planning.py tests/test_gate114_research_mode_clarity_microtranche.py tests/test_gate113_execution_authority_microtranche.py tests/test_gate112_governance_closeout.py tests/test_gate111_governance_guardrails.py tests/test_gate110_agents_reading_order.py tests/test_gate109_template_pack_governance.py tests/test_gate108_router_only_control_surface.py tests/test_gate107_repo_process_governance.py tests/test_document_hygiene.py`
- No runtime seam gate may be called complete later without rereading the active vocabulary authority and `docs/03_DOMAIN_MODEL.md` first.
- No gate may be called complete without the planning quartet moving together on the same branch and a fresh full-history zip from the exact green repo state.

## Gates

### Gate 141: Activate the clean seam pack and freeze the observed workflow trace

**Status**
- complete on `main`

**Objective**
- Activate one new clean planning pack from the Gate 140 baseline, freeze the observed current-stage handoff and terminal-risk workflow, and route the repo truthfully to Gate 142.

**In-scope surfaces**
- repo-root `PLANS.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- `docs/planning/2026-04-01_STAGE_LOCAL_HANDOFF_AND_TERMINAL_RISK_SEAMS_GATES_v1.md`
- `docs/planning/2026-04-01_STAGE_LOCAL_HANDOFF_AND_TERMINAL_RISK_SEAMS_LEAVES_v1.json`
- `docs/planning/2026-04-01_STAGE_LOCAL_HANDOFF_AND_TERMINAL_RISK_SEAMS_EXECUTION_LOG_v1.md`
- `docs/planning/2026-04-01_STAGE_LOCAL_HANDOFF_AND_TERMINAL_RISK_SEAMS_DOCUMENT_TOUCH_CHECKLIST_v1.md`
- `docs/planning/2026-04-01_GATE141_STAGE_LOCAL_HANDOFF_PACK_BOOTSTRAP.md`
- `tests/test_gate141_stage_local_handoff_terminal_risk_seams_planning.py`
- planning-governance tests that must admit the new active pack state
- `CHANGELOG.jsonl`

**Definition of done**
- the new planning quartet exists and is populated from repo truth rather than placeholders;
- the active router surfaces agree that Gate 141 is complete on `main` and Gate 142 is now active;
- the Gate 141 receipt records the observed workflow anchor and the exact planning proof slice;
- the planning-governance proof slice passes in the repo-local installed environment.

### Gate 142: Freeze the observed overwrite and ownership inventory

**Status**
- complete on `main`

**Objective**
- Trace the live overwrite chain, stage-local ownership boundaries, and downstream consumers that currently depend on mutated outputs before any additive seam contract is introduced.

### Gate 143: Admit additive stage-local handoff artefacts only where Gate 142 proves they are necessary

**Status**
- complete on `main`

**Objective**
- add any preserved stage-local handoff contracts and immediate carriage surfaces that Gate 142 proves necessary without changing terminal behaviour yet.

### Gate 144: Separate posture hard invariants from posture-local envelope truth if the current output conflates them

**Status**
- complete on `main`

**Objective**
- make posture-owned hard blocks, local envelope state, and downstream annotations explicit where Gate 142 shows they are currently collapsed.

### Gate 145: Realign modifier authority from mutation-first to emitted-policy-first

**Status**
- complete on `main`

**Objective**
- move modifier authority toward emitted policy, resolved surfaces, and review-visible lineage while keeping a bounded compatibility bridge until consumers migrate.

### Gate 146: Clarify eligibility boundary versus execution candidate ownership

**Status**
- complete on `main`

**Objective**
- keep Stage 5 limited to admissibility/selection truth and isolate Stage 6 candidate/expression ownership where current surfaces overlap.

### Gate 147: Split overlay evaluation from terminal-risk application where the current final step combines them

**Status**
- complete on `main`

**Objective**
- separate observed overlay-evaluation truth from the terminal application step and freeze overlap classes before review consumers are changed.

### Gate 148: Reconcile review, trace, replay, and legacy expectation surfaces to the new seams

**Status**
- complete on `main`

**Objective**
- migrate downstream consumers, reporting, and expectation tests to the preserved-seam model once the new contracts exist.

### Gate 149: Run the absolute anti-drift audit and package the exact green repo state

**Status**
- active on `main`

**Objective**
- prove the active pack, leaves ledger, execution log, vocabulary/data authority references, tests, and packaged repo all agree on the final green state.
