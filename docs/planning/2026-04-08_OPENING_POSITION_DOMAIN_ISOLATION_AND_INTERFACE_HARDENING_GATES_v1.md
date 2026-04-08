# 2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_GATES_v1

Status: active planning pack for Gates 226-235. Gate 226 is complete on `work/gate-226-pack-bootstrap-and-routing-20260408`; Gate 227 is not yet activated.

## Purpose

Create the next execution-grade planning tranche for the slim successor repo by isolating opening-position work into bounded domains with explicit inputs, outputs, lawful readers, prohibited readers, and later proof slices. This pack preserves the current deterministic seven-stage spine, keeps the repo in opening-position scope only, and freezes the work needed before any Phase 2 stay-in / stay-out or close-position logic begins.

## Scope

In scope:
- opening-position-only domain isolation from ingress through recommendation-ledger persistence;
- upstream isolation of raw / prepared ingress, Step 0 route selection, and Step 1 temporal truth;
- domain isolation of the serial opportunity ladder, the coefficient control plane, the `Independent Parallel Risk Lane`, DMP v2 carriage, and the recommendation ledger;
- one bounded top-to-bottom opening-position proof route for later execution.

Out of scope:
- close-position logic of any kind;
- carry-horizon, overnight, or weekend decisioning expansion;
- capital displacement authority, rotation logic, or any cross-book / portfolio brain;
- full arbiter logic between the serial ladder and the `Independent Parallel Risk Lane`;
- broad blind repo-wide proof by default;
- pretending Gate 227 or later domain work has started before Gate 226 routing closeout says so.

## Supersession and active authority

- This document is the active gate authority for Gates 226-235.
- It is a new pack rather than an amendment because repo-root `PLANS.md` previously named no active pack.
- Gate 226 has completed the routing quartet and activated this pack without activating Gate 227 yet.
- The latest closed retained pack remains evidence input only:
  - `docs/planning/2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_GATES_v1.md`
  - `docs/planning/2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_LEAVES_v1.json`
  - `docs/planning/2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_EXECUTION_LOG_v1.md`
- The latest closed predecessor evidence remains predecessor context only:
  - `docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_GATES_v1.md`
  - `docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_LEAVES_v1.json`
  - `docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_EXECUTION_LOG_v1.md`

## Governing inputs

Frozen doctrine and process inputs:
- `docs/01_NORMATIVE.md`
- `docs/02_OPERATING_MODEL.md`
- `docs/03_DOMAIN_MODEL.md`
- `docs/04_TECHNICAL_ARCHITECTURE.md`
- `docs/05_GUARDRAILS.md`
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `AGENTS.md`
- repo-root `PLANS.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`

Packet / data contract and specialised runtime-ownership inputs:
- `docs/03_DOMAIN_MODEL.md`
- `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md`
- `docs/planning/2026-03-24_DMP_V2_NORMATIVE_SPEC.md`

Evidence-input planning surfaces re-read before writing this pack:
- `docs/planning/2026-03-26_COGNITIVE_WORKFLOW_IMPLEMENTATION_MAP.md`
- `docs/planning/2026-03-26_COGNITIVE_WORKFLOW_BOUNDARY_RULES.md`
- `docs/planning/2026-03-26_CALENDAR_HORIZON_OWNERSHIP.md`
- `docs/planning/2026-04-02_GATE152_STAGE5_STAGE6_AUTHORITY_REPLAN.md`
- `docs/planning/2026-04-02_GATE153_OVERLAY_TERMINAL_FINAL_JOIN_AUTHORITY_REPLAN.md`
- `docs/planning/2026-04-02_GATE160_OWNER_STAGE_AND_ACTIVATION_STATE_LEDGER.md`
- `docs/planning/2026-04-02_GATE161_OPPORTUNITY_VS_CAUTION_SHAPING_LAW.md`
- `docs/planning/2026-04-02_GATE163_OWNERSHIP_OUTPUT_COEFFICIENT_AND_ANTI_DUPLICATION_LAW.md`
- `docs/planning/2026-04-02_GATE167_SERIAL_CONSERVATISM_BINDING_POINT_LAW.md`
- `docs/planning/2026-04-03_GATE188_CAPITAL_DEPLOYMENT_AUTHORITY_CONTRACT.md`

## Workflow placement

This tranche sits after the retained-test cleanup closeout and before any Phase 2 work on staying in, staying out, capital displacement, carry, or exits.

It is not a generic refactor pack. It is an opening-position domain-isolation pack that prepares later execution to:
1. separate the current architecture into bounded question-owning domains;
2. freeze the lawful I/O contracts across those domains;
3. preserve the serial trader-thinking ladder without allowing cumulative generic risk to sludge through later stages;
4. restart the `Independent Parallel Risk Lane` from clean domain law rather than inherited malformed structure;
5. preserve DMP v2 as the canonical packet shell around typed domain payloads; and
6. extend the database so every 30-second opening-position recommendation pass has a first-class receipt.

Ten gates and fifty leaves preserve granularity here because the tranche is larger than one domain but smaller than a multi-pack rewrite. Five leaves per gate gives one bounded pass each for: authority read / trace, contract freeze, prohibited-reader or prohibited-leakage law, proof burden, and gate closeout.

## Intent and workflow anchor

The governing repo lens for this tranche is deterministic opening-position architecture, not broad live-operability polish.

The workflow anchor remains:

`Step 0 route -> Temporal Context -> Market Regime Context -> Options and Flow Context -> Posture and Risk Permission -> Playbook Eligibility -> Expression and Execution -> bounded downstream opening-position consumers -> Review and Explanation`

This pack does **not** replace the seven-stage serial spine. It isolates the domains that already exist or are already implied, then freezes the downstream contracts and later proof burden for opening-position work only.

## Retain / retire-from-authority / amend / add matrix

### Retain as canonical
- the seven-stage serial spine and current workflow order
- `Temporal Context` and Financial Calendar upstream ownership
- the `Playbook Eligibility` versus `Expression and Execution` Stage 5 / Stage 6 non-equivalence law
- DMP v2 as the canonical packet shell with typed object-block payload carriage
- `Capital Deployment Authority Service` as bounded fresh-capital opening-position authority only

### Retire from authority (compatibility-only unless later removed)
- any compatibility or review carriage that currently appears to outrank the primary opening-position seam
- any carried-forward serial decision-risk surface that behaves as a generic cumulative veto after its local decision has already been made
- any inference of Stage 6 ranking or lead selection from Stage 5 admissibility alone
- any future reliance on review-layer nested JSON when canonical packet or primary seam surfaces already exist

### Mandatory amendments
- serial ladder seam law because cumulative generic risk must stop compounding across later serial and downstream decisions
- downstream seam ranking because `Expression and Execution`, `Stage-Local Handoff`, compatibility carriage, and bounded CDA input must be ordered explicitly
- coefficient control-plane law because live-world, owner-stage, activation-state, and shaping splits must stay explicit during domain isolation
- database / execution-record law because the recommendation ledger must persist every opening-position pass without creating a same-pass loop

### New additions
- one new Gates 226-235 pack
- one new supporting leaves ledger
- one new execution log surface
- one new document-touch checklist
- one new bounded scope note
- one new contradiction report
- one new opening-position recommendation-ledger planning surface inside the pack
- one top-to-bottom opening-position flow harness definition

## Vocabulary discipline

- The active baseline vocabulary authority for this draft is `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`.
- This pack deliberately reuses repo-native terms such as `Temporal Context`, `Posture and Risk Permission`, `Playbook Eligibility`, `Expression and Execution`, `Independent Parallel Risk Lane`, `Capital Deployment Authority Service`, and `Capital Deployment Authority Decision`.
- No new governed vocabulary is admitted in this draft pack.
- If later execution proves a genuine naming gap, vocabulary admission must happen explicitly before merge.

## Packet / contract discipline

- `docs/03_DOMAIN_MODEL.md` and `docs/planning/2026-03-24_DMP_V2_NORMATIVE_SPEC.md` are mandatory reading for any later leaf that changes packet shell shape, block shape, lineage, contract ranking, or database linkage to packet identity.
- `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md` is mandatory reading for any later leaf that changes runtime surface ownership, stage-packet versus workflow-packet ranking, compatibility carriage law, or downstream consumer permissions.
- Review carriage and compatibility wrappers remain descriptive unless later execution explicitly promotes them.

## Contradiction scan and state-integrity rules

- The contradiction scan for this draft found no blocking router contradiction: the repo honestly reports no active pack currently routed after Gate 225 closeout.
- Two non-blocking architecture seams are intentionally carried into this tranche as design drivers rather than router contradictions:
  1. current serial decision-risk appears to carry too far downstream as cumulative generic caution;
  2. the `Independent Parallel Risk Lane` requires a clean-law restart rather than incremental patching.
- State-integrity invariants for later execution remain:
  - `completed_leaf_ids` and `remaining_leaf_ids` are disjoint;
  - every referenced leaf id exists in the leaves ledger;
  - `active_gate = none` is lawful only when `remaining_leaf_ids` and `pending_gate_ids` are empty in a live execution state;
  - later planning-guard tests must permit later valid states rather than hard-coding brittle one-moment strings.

## Document-touch checklist

- `2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_DOCUMENT_TOUCH_CHECKLIST_v1.md` is the pack-local checklist for this tranche.
- If execution later proceeds, the planning quartet must move together on the same branch:
  1. repo-root `PLANS.md`
  2. `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
  3. the active leaves ledger for this pack
  4. the active execution log for this pack

## Testing and promotion discipline

- This draft pack is planning-only and does not claim any repo execution occurred in the sandbox.
- Later execution must use the repo's own environment bootstrap and active proof doctrine.
- Minimum later proof style for each gate:
  - one new gate-local planning / contract test
  - `tests/test_planning_state_integrity.py`
  - a bounded existing-family proof slice named by the gate
- Full-suite proof is not default. A gate may widen proof only if its own blast radius proves that necessary.
- A gate is not complete later until tests ran green and the planning quartet moved together on the same branch.

## Gates

### Gate 226: Pack bootstrap, contradiction scan, and active-pack routing closeout

**Objective**
- Create a new activation-ready pack while the repo is in no-active-pack hold, and freeze scope, evidence posture, and later router work before any domain planning starts.

**Families executed**
- `planning_governance__new_pack_bootstrap_and_router_activation_readiness`
- `planning_governance__contradiction_scan_and_no_active_pack_hold_truth`

**Definition of done**
- the pack states why it is a new pack rather than an amendment
- scope, out-of-scope holds, retain/retire/amend/add decisions, and contradiction outcomes are explicit
- repo-root routing has occurred and the active pack is truthful without falsely claiming Gate 227 execution has already started

**Minimum proof slice**
- `pytest -q tests/test_gate226_opening_position_pack_bootstrap_and_routing.py tests/test_planning_state_integrity.py`

### Gate 227: Opening-position ingress substrate and Step 0/Step 1 boundary isolation

**Objective**
- Freeze the opening-position ingress path from raw primitives through prepared runtime into Step 0 route selection and Step 1 temporal truth, without downstream leakage.

**Families executed**
- `ingress_substrate__opening_position_raw_to_prepared_path`
- `temporal_route_boundary__step0_step1_input_separation`

**Definition of done**
- the canonical opening-position ingress path is explicit
- Step 0 route inputs and Step 1 temporal inputs are separated cleanly
- raw-versus-derived signal ownership and later proof burden are frozen

**Minimum proof slice**
- `pytest -q tests/test_gate227_opening_position_ingress_boundary_isolation.py tests/test_planning_state_integrity.py`
- `pytest -q tests/test_gate101_canonical_raw_bundle_admission.py tests/test_gate102_raw_runtime_harness.py tests/test_gate115_normalised_prepared_runtime_features.py tests/test_temporal_context_runtime.py`

### Gate 228: Temporal Context and Financial Calendar domain isolation

**Objective**
- Isolate Temporal Context and Financial Calendar authority as a bounded upstream domain with explicit inputs, outputs, lawful readers, prohibited readers, and harness expectations.

**Families executed**
- `temporal_calendar_domain__input_output_isolation`
- `temporal_calendar_domain__lawful_reader_and_harness_rules`

**Definition of done**
- temporal/calendar inputs and outputs are frozen as one upstream authority domain
- lawful readers and prohibited readers are explicit
- a bounded domain harness and proof slice are defined

**Minimum proof slice**
- `pytest -q tests/test_gate228_temporal_calendar_domain_isolation.py tests/test_planning_state_integrity.py`
- `pytest -q tests/test_temporal_context_runtime.py tests/test_gate175_temporal_calendar_multi_clock_runtime.py tests/test_gate89_financial_calendar_crosswalk_and_dmp_lane.py tests/test_gate91_financial_calendar_canonical_projection.py`

### Gate 229: Serial opportunity ladder isolation and non-cumulative Posture and Risk Permission law

**Objective**
- Isolate the serial opportunity ladder from Posture and Risk Permission through Playbook Eligibility to Expression and Execution, and explicitly stop cumulative carried-forward generic risk from suppressing later decisions.

**Families executed**
- `serial_opportunity_ladder__stage5_stage6_question_owner_split`
- `serial_opportunity_ladder__non_cumulative_decision_risk_reset`

**Definition of done**
- Stage 5 admissibility and Stage 6 candidate ownership remain distinct
- non-cumulative serial decision-risk law is explicit and bounded
- playbook family, setup variant, and execution-expression interfaces are frozen with prohibited leakage rules

**Minimum proof slice**
- `pytest -q tests/test_gate229_serial_opportunity_ladder_and_non_cumulative_risk_law.py tests/test_planning_state_integrity.py`
- `pytest -q tests/test_gate152_stage5_stage6_authority_replan.py tests/test_gate167_serial_conservatism_binding_point_law.py tests/test_posture_risk_and_playbook.py tests/test_gate119_candidate_adjudication.py tests/test_gate120_execution_geometry.py`

### Gate 230: Expression and Execution opening-position seam and bounded downstream consumer handoff

**Objective**
- Freeze the opening-position seam leaving Expression and Execution into Stage-Local Handoff, compatibility carriage, and bounded Capital Deployment Authority inputs, while preserving the non-cumulative risk reset downstream.

**Families executed**
- `expression_seam__opening_position_candidate_and_preserved_handoff`
- `expression_seam__bounded_cda_input_and_non_cumulative_risk_protection`

**Definition of done**
- the opening-position candidate surface leaving Expression and Execution is explicit
- Stage-Local Handoff and compatibility carriage are ranked against primary authority surfaces
- bounded Capital Deployment Authority inputs are frozen without serial risk compounding again

**Minimum proof slice**
- `pytest -q tests/test_gate230_expression_execution_seam_and_cda_input_boundary.py tests/test_planning_state_integrity.py`
- `pytest -q tests/test_gate143_stage_local_handoff_runtime.py tests/test_gate153_overlay_terminal_final_join_authority_replan.py tests/test_gate188_capital_deployment_authority_contract.py tests/test_gate190_capital_deployment_authority_integration.py tests/test_execution_review_runtime.py`

### Gate 231: Coefficient control-plane isolation and owner-stage / activation-state hardening

**Objective**
- Isolate the coefficient world as its own control plane, freeze owner-stage truth, activation-state truth, and the split between opportunity shaping and caution shaping.

**Families executed**
- `coefficient_control_plane__one_live_world_and_reference_truth`
- `coefficient_control_plane__owner_stage_activation_state_and_shaping_split`

**Definition of done**
- one live coefficient world versus reference truth is explicit
- owner-stage and activation-state truth are frozen for opening-position-relevant coefficient surfaces
- opportunity shaping and caution shaping remain separated and bounded

**Minimum proof slice**
- `pytest -q tests/test_gate231_coefficient_control_plane_isolation.py tests/test_planning_state_integrity.py`
- `pytest -q tests/test_gate159_coefficient_world_status_and_inventory_law.py tests/test_gate160_governed_signal_coefficient_reference_workbook_law.py tests/test_gate160_owner_stage_and_activation_state_ledger.py tests/test_gate161_opportunity_vs_caution_shaping_law.py tests/test_gate78_modifier_runtime_integration.py`

### Gate 232: Independent Parallel Risk Lane clean-room planning restart

**Objective**
- Restart Independent Parallel Risk Lane planning from clean domain law, using current repo truth as evidence input without inheriting malformed architecture by default.

**Families executed**
- `independent_parallel_risk_lane__clean_governing_question_and_input_contract`
- `independent_parallel_risk_lane__output_contract_and_anti_duplication_law`

**Definition of done**
- the lane's governing question, lawful inputs, lawful outputs, and anti-duplication law are frozen cleanly
- the lane remains co-resident but not a stage, a second playbook engine, or a hidden arbiter
- a bounded proof slice is frozen for later coding

**Minimum proof slice**
- `pytest -q tests/test_gate232_independent_parallel_risk_lane_clean_restart.py tests/test_planning_state_integrity.py`
- `pytest -q tests/test_gate157_parallel_risk_lane_foundation_bootstrap.py tests/test_gate158_co_resident_parallel_risk_lane_law.py tests/test_gate163_ownership_output_coefficient_and_anti_duplication_law.py tests/test_gate174_parallel_risk_lane_input_contract.py tests/test_gate176_market_options_dependency_dislocation_runtime.py`

### Gate 233: DMP v2 packet-shell and domain-carriage hardening

**Objective**
- Freeze how the isolated opening-position domains travel through DMP v2 packets, preserving shell versus payload, lineage, and downstream reader ranking.

**Families executed**
- `dmp_v2_carriage__domain_packet_shell_and_object_payload_split`
- `dmp_v2_carriage__lineage_identity_and_receipt_linkage`

**Definition of done**
- a DMP v2 packet-ownership map is frozen for the isolated domains
- shell-versus-payload rules are explicit
- packet identity, lineage, and receipt linkage fields are frozen for later persistence

**Minimum proof slice**
- `pytest -q tests/test_gate233_dmp_v2_domain_carriage_hardening.py tests/test_planning_state_integrity.py`
- `pytest -q tests/test_dmp_v2_protocol.py tests/test_execution_review_runtime.py tests/test_gate54_dmp_binding_surface.py tests/test_gate56_58_dmp_promotion.py tests/test_gate89_financial_calendar_crosswalk_and_dmp_lane.py`

### Gate 234: Recommendation ledger and receipt-history foundation extension

**Objective**
- Extend database and execution-record planning so every opening-position recommendation pass is preserved as first-class receipt history without creating a same-pass loop.

**Families executed**
- `recommendation_ledger__opening_position_receipt_extension`
- `receipt_history_foundation__observational_meta_state_only`

**Definition of done**
- current execution-record surfaces are audited against recommendation receipt needs
- the new recommendation-ledger schema and linkage fields are explicit
- receipt-history derived meta-state is observational-only and not same-pass feedback

**Minimum proof slice**
- `pytest -q tests/test_gate234_recommendation_ledger_and_receipt_history_foundation.py tests/test_planning_state_integrity.py`
- `pytest -q tests/test_gate140_execution_ledger_alembic_parity.py tests/test_gate169_calibration_metadata_and_receipts.py tests/test_execution_review_runtime.py tests/test_gate190_capital_deployment_authority_integration.py`

### Gate 235: Cross-flow opening-position harness, planning guards, and pack closeout

**Objective**
- Close the planning pack with one lawful top-to-bottom opening-position proof route, planning guard tests, deterministic execution order, and honest draft closeout.

**Families executed**
- `opening_position_flow_harness__top_to_bottom_proof_route`
- `planning_governance__pack_guard_and_closeout_truth`

**Definition of done**
- one top-to-bottom opening-position flow proof route is explicit
- pack-local planning guard tests and later valid-state rules are named
- the pack closes honestly as draft activation-ready planning material with Phase 2 holds still explicit

**Minimum proof slice**
- `pytest -q tests/test_gate235_opening_position_flow_harness_and_pack_closeout.py tests/test_planning_state_integrity.py`
- `pytest -q tests/test_execution_review_runtime.py tests/test_temporal_context_runtime.py tests/test_posture_risk_and_playbook.py tests/test_dmp_v2_protocol.py tests/test_gate190_capital_deployment_authority_integration.py`
