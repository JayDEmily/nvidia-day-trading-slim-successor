# 07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER

## 1. Purpose and authority

This document freezes the current latest-state ownership, compatibility, and downstream read-path law for runtime surfaces on `main`.

This document uses three authority layers only:

- the authorised vocabulary dictionary for canonical labels, slugs, categories, owner slugs, and allowed aliases;
- the current live schema and service code for runtime packet shape, point of production, and downstream read paths;
- the current first-class docs for explanatory architecture and domain-model alignment.

Historical planning receipts may explain why a surface exists. They do not replace latest-code truth as the runtime authority source.

## 2. Vocabulary authority and naming rules

- Every named surface in this document must use the canonical vocabulary label and canonical slug when an authorised entry already exists.
- Allowed aliases may be mentioned only as cross-reference help. They do not replace the canonical label or slug.
- Each ledger row must distinguish:
  - vocabulary authority source;
  - canonical owner slug;
  - point of production;
  - runtime contract or runtime carriage;
  - governing authoritative surface where the row is a compatibility surface or compatibility carriage;
  - allowed downstream readers;
  - prohibited inference.
- Where the authorised vocabulary entry maps to a planning-law artefact rather than a live runtime schema, both must be named separately:
  - the vocabulary authority source; and
  - the live runtime contract.
- New terms may be introduced only if no authorised vocabulary entry already covers the concept and the new term passes the vocabulary-governance workflow.

## 3. Authoritative runtime surface ownership ledger

Section 3 records the current latest-state authority chain for **stage outputs**, **workflow packets**, and **authoritative preserved/additive surfaces** that are read downstream in runtime, review, replay, or bounded-trace paths.

### 3.1 Posture and Risk Permission

- **Canonical label:** Posture and Risk Permission
- **Canonical slug:** `posture_risk_permission`
- **Category:** `stage`
- **Canonical owner slug:** `posture_risk_permission`
- **Vocabulary authority source:** `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json:67-82`
- **Point of production:** `PostureRiskService` output, carried as `PostureRiskOutput`
- **Runtime contract:** `nvda_desk.schemas.cognition.PostureRiskOutput`
- **Authoritative contents:** `permission_state`, `posture_label`, `inventory_posture_state`, `fresh_deployable_capital_pct`, `overnight_deployable_capital_pct`, `inventory_action_bias`, `fresh_vs_inventory_state`, `thesis_state`, `capital_lockup_state`, `adverse_excursion_state`, `time_stop_state`, `signal_conflict_state`, `time_stop_minutes_remaining`, `thesis_pressure_score`, `hard_invariants`, `local_envelope`, `downstream_annotations`, `modifier_compatibility_bridge`, `modifier_runtime_packet`, `parallel_risk_lane_packet`, `stand_down_class`, `conflict_classes`, `degradation_step`
- **Allowed downstream readers:** `StateConditionedModifierService.evaluate(...)`, `PlaybookEligibilityService.evaluate(...)`, `ExecutionExpressionService.evaluate(...)`, `RiskGatewayService.evaluate_overlay(...)`, `RiskGatewayService.build_terminal_risk_application(...)`, `ParallelRiskLaneService.enrich_candidate_semantics(...)`, `ReviewExplanationInput.posture`
- **Prohibited inference:** downstream consumers must not substitute additive sub-surfaces or compatibility carriage for the stage packet itself

### 3.2 Posture Hard Invariants

- **Canonical label:** Posture Hard Invariants
- **Canonical slug:** `posture_hard_invariants`
- **Category:** `compatibility_surface`
- **Canonical owner slug:** `posture_risk_permission`
- **Vocabulary authority source:** `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json:85-102`
- **Point of production:** produced inside `PostureRiskOutput.hard_invariants`
- **Runtime contract:** `nvda_desk.schemas.cognition.PostureHardInvariantsSurface`
- **Authoritative contents:** `block_active`, `hard_block_reasons`, `zero_deployable_required`
- **Allowed downstream readers:** execution through posture carriage, review and explanation through `ReviewExplanationInput.posture`, preserved cited-posture handoff
- **Prohibited inference:** selector citations, downstream annotations, and modifier consequences must not be inferred from this surface

### 3.3 Posture Local Envelope

- **Canonical label:** Posture Local Envelope
- **Canonical slug:** `posture_local_envelope`
- **Category:** `compatibility_surface`
- **Canonical owner slug:** `posture_risk_permission`
- **Vocabulary authority source:** `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json:104-120`
- **Point of production:** produced inside `PostureRiskOutput.local_envelope`
- **Runtime contract:** `nvda_desk.schemas.cognition.PostureLocalEnvelopeSurface`
- **Authoritative contents:** base permission state, deployable-capital envelope, inventory state, thesis state, time-stop state, posture-owned derisk reasons
- **Allowed downstream readers:** execution through posture carriage, review and explanation through `ReviewExplanationInput.posture`, preserved cited-posture handoff
- **Prohibited inference:** downstream consumers must not treat `downstream_annotations` or modifier bridge fields as local-envelope truth

### 3.4 Eligibility Admissibility

- **Canonical label:** Eligibility Admissibility
- **Canonical slug:** `eligibility_admissibility`
- **Category:** `compatibility_surface`
- **Canonical owner slug:** `playbook_eligibility`
- **Vocabulary authority source:** `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json:159-175`
- **Point of production:** produced inside `PlaybookEligibilityOutput.admissibility_surface`
- **Runtime contract:** `nvda_desk.schemas.cognition.EligibilityAdmissibilitySurface`
- **Authoritative contents:** permission state, no-trade reasons, admissible family ids, admissible setup-variant ids, admissible playbook ids, watch-only family ids, watch-only setup-variant ids, watch-only playbook ids
- **Allowed downstream readers:** execution, review and explanation, replay consumers, bounded-trace consumers
- **Prohibited inference:** Stage 6 ranking, adjudication, lead selection, and contradiction resolution must not be inferred from admissibility alone

### 3.5 Modifier Runtime Packet

- **Canonical label:** Modifier Runtime Packet
- **Canonical slug:** `modifier_runtime_packet`
- **Category:** `workflow`
- **Canonical owner slug:** `posture_risk`
- **Vocabulary authority source:** `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json:761-778`
- **Owner clarification:** `posture_risk` is the vocabulary owner for this workflow packet. It is distinct from the Stage 4 stage slug `posture_risk_permission`.
- **Point of production:** `StateConditionedModifierService.evaluate(...)`
- **Runtime contract:** `nvda_desk.schemas.state_policy.ModifierRuntimePacket`
- **Authoritative contents:** `active_policy_ids`, `effective_lineage`, `resolved_surfaces`, effective coefficients, `triggered_kill_switch`
- **Allowed downstream readers:** posture mutation path, execution evaluation, review and explanation via `ReviewExplanationInput.modifier_runtime_packet`, effective-policy reconstruction
- **Prohibited inference:** compatibility bridge fields must not be treated as co-equal authority when the packet is present

### 3.6 Execution Candidate Ownership

- **Canonical label:** Execution Candidate Ownership
- **Canonical slug:** `execution_candidate_ownership`
- **Category:** `compatibility_surface`
- **Canonical owner slug:** `expression_execution`
- **Vocabulary authority source:** `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json:195-210`
- **Point of production:** produced inside `ExecutionExpressionOutput.candidate_ownership`
- **Runtime contract:** `nvda_desk.schemas.cognition.ExecutionCandidateOwnershipSurface`
- **Authoritative contents:** admitted playbook ids seen by execution, watch-only ids seen by execution, adjudicated ids, lead playbook id, contradiction resolution
- **Allowed downstream readers:** review and explanation, replay consumers, bounded-trace consumers
- **Prohibited inference:** downstream consumers must not backfill this surface from Stage 5 admissibility or from flat `active_playbook_ids`

### 3.7 Overlay Risk Decision

- **Canonical label:** Overlay Risk Decision
- **Canonical slug:** `overlay_risk_decision`
- **Category:** `compatibility_surface`
- **Canonical owner slug:** `risk_gateway`
- **Vocabulary authority source:** `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json:214-230`
- **Point of production:** `RiskGatewayService.evaluate_overlay(...)`
- **Runtime contract:** `nvda_desk.schemas.risk.RiskDecision`
- **Authoritative contents:** pre-terminal overlay evaluation result
- **Allowed downstream readers:** preserved stage-local handoff, review and explanation, replay consumers, bounded-trace consumers
- **Prohibited inference:** downstream consumers must not treat overlay evaluation as the final terminal action

### 3.8 Terminal Risk Application

- **Canonical label:** Terminal Risk Application
- **Canonical slug:** `terminal_risk_application`
- **Category:** `compatibility_surface`
- **Canonical owner slug:** `risk_gateway`
- **Vocabulary authority source:** `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json:233-249`
- **Point of production:** `RiskGatewayService.build_terminal_risk_application(...)`
- **Runtime contract:** `nvda_desk.schemas.cognition.TerminalRiskApplicationSurface`
- **Authoritative contents:** posture permission state, overlay decision, final decision, overlap classes, notes
- **Allowed downstream readers:** preserved stage-local handoff, review and explanation, replay consumers, bounded-trace consumers
- **Prohibited inference:** downstream consumers must not reduce terminal application to `final_risk_join` alone when the preserved seam is available

### 3.9 Terminal Risk Decision

- **Canonical label:** Terminal Risk Decision
- **Canonical slug:** `terminal_risk_decision`
- **Category:** `compatibility_surface`
- **Canonical owner slug:** `review_explanation`
- **Vocabulary authority source:** `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json:547-562`
- **Point of production:** produced as `final_risk_decision`, then carried inside `StageLocalHandoffSurface.terminal_risk_decision`
- **Runtime contract:** `nvda_desk.schemas.risk.RiskDecision`
- **Authoritative contents:** the final decision used by `apply_final_join(...)`
- **Allowed downstream readers:** review and explanation, replay consumers, bounded-trace consumers reading preserved handoff truth
- **Prohibited inference:** downstream consumers must not reconstruct this decision solely from `final_risk_join` when the preserved handoff field is present

### 3.10 Stage-Local Handoff

- **Canonical label:** Stage-Local Handoff
- **Canonical slug:** `stage_local_handoff`
- **Category:** `workflow`
- **Canonical owner slug:** `review_explanation`
- **Vocabulary authority source:** `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json:528-543`
- **Point of production:** explicitly constructed inside `DeskCognitionRuntime.evaluate(...)` before review evaluation
- **Runtime contract:** `nvda_desk.schemas.cognition.StageLocalHandoffSurface`
- **Authoritative contents:** cited posture pre-modifier, cited eligibility, execution pre-modifier, execution post-modifier pre-final-risk, overlay-risk decision, terminal-risk application, terminal-risk decision, notes
- **Allowed downstream readers:** `ReviewExplanationInput.stage_local_handoff`, `DeskCognitionRuntimeResult.stage_local_handoff`, replay consumers, bounded-trace consumers
- **Prohibited inference:** downstream consumers must not use this surface to rewrite stage order or replace terminal runtime behaviour; it is preserved additive truth only

### 3.11 Review and Explanation

- **Canonical label:** Review and Explanation
- **Canonical slug:** `review_explanation`
- **Category:** `stage`
- **Canonical owner slug:** `review_explanation`
- **Vocabulary authority source:** `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json:252-267`
- **Point of production:** `ReviewExplanationService.evaluate(...)`
- **Runtime contract:** `nvda_desk.schemas.cognition.ReviewExplanationOutput`
- **Input contract:** `nvda_desk.schemas.cognition.ReviewExplanationInput`
- **Authoritative inputs consumed:** `temporal`, `regime`, `options_flow`, `posture`, `eligibility`, `execution`, `modifier_runtime_packet`, `parallel_risk_lane_packet`, `stage_local_handoff`, `temporal_input`
- **Authoritative contents produced:** summary, stage reason packets, rejected playbooks, contradictions, imported-module citations, effective policy, review governance, event governance, precursor governance, review lineage, failure taxonomy, economic accountability, promotion evidence, packet lineage, carried `stage_local_handoff`, review packet
- **Allowed downstream readers:** review packet services, API surfaces, replay consumers, bounded-trace consumers, human operator review
- **Prohibited inference:** nested compatibility payloads inside `review_packet` must not outrank separately carried authoritative surfaces when both are present

### 3.12 Independent Parallel Risk Lane

- **Canonical label:** Independent Parallel Risk Lane
- **Canonical slug:** `independent_parallel_risk_lane`
- **Category:** `workflow`
- **Canonical owner slug:** `temporal_context`
- **Vocabulary authority source:** `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json:1697-1706`
- **Vocabulary maps-to contract:** `docs/planning/2026-04-02_GATE158_CO_RESIDENT_PARALLEL_RISK_LANE_LAW.md`
- **Point of production:** `ParallelRiskLaneService.evaluate(...)`, then enrichment through market-translation and candidate-semantics steps
- **Runtime packet contract:** `nvda_desk.schemas.parallel_risk.ParallelRiskLanePacket`
- **Authoritative contents:** `lane_id`, `serial_spine_preserved`, `co_resident_from_session_start`, `arbiter_active`, `invariant_reads`, `stage_output_reads`, `temporal_surface`, `market_translation_surface`, `candidate_audit_surface`, `notes`
- **Allowed downstream readers:** posture carriage, execution carriage, review and explanation via `ReviewExplanationInput.parallel_risk_lane_packet`, evaluation-preparation packet builders
- **Prohibited inference:** the lane must not be treated as an eighth serial stage or an independent final arbiter over the seven-stage grammar

## 4. Compatibility surface and bridge ledger

### 4.1 Posture Downstream Annotations

- **Canonical label:** Posture Downstream Annotations
- **Canonical slug:** `posture_downstream_annotations`
- **Category:** `compatibility_surface`
- **Canonical owner slug:** `posture_risk_permission`
- **Vocabulary authority source:** `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json:123-139`
- **Point of production:** selector-contract citations are appended in `DeskCognitionRuntime._posture_with_contract_citations(...)`; later modifier notes are appended in `StateConditionedModifierService.apply_to_posture(...)`
- **Runtime carriage:** `nvda_desk.schemas.cognition.PostureRiskOutput.downstream_annotations`
- **Governing authoritative surfaces:** `PostureRiskOutput`, `PostureHardInvariantsSurface`, `PostureLocalEnvelopeSurface`, `ModifierRuntimePacket`
- **Allowed contents:** selector-contract citations, modifier policy notes, kill-switch notes, stand-down notes, conflict notes, explicit authority markers
- **Allowed downstream readers:** any consumer that reads the full `PostureRiskOutput` packet, including execution, review and explanation, and preserved cited-posture handoff
- **Prohibited use:** `downstream_annotations` must not be treated as posture-owned permission truth, hard-invariant truth, or local-envelope truth

### 4.2 Modifier Compatibility Bridge

- **Canonical label:** Modifier Compatibility Bridge
- **Canonical slug:** `modifier_compatibility_bridge`
- **Category:** `compatibility_surface`
- **Canonical owner slug:** `state_conditioned_modifier`
- **Vocabulary authority source:** `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json:781-797`
- **Point of production:** `_posture_bridge_surface(...)` and `_execution_bridge_surface(...)` inside `StateConditionedModifierService.apply_to_posture(...)` and `StateConditionedModifierService.apply_to_execution(...)`
- **Runtime contract:** `nvda_desk.schemas.cognition.ModifierCompatibilityBridgeSurface`
- **Governing authoritative surface:** `ModifierRuntimePacket`
- **Allowed contents:** `authority_source`, `compatibility_bridge_active`, `applied_policy_ids`, `overridden_fields`, target field echoes, notes
- **Allowed downstream readers:** `PostureRiskOutput`, `ExecutionExpressionOutput`, `ReviewExplanationInput`, `ReviewExplanationOutput`, review-packet compatibility carriage
- **Prohibited use:** the bridge must not outrank `ModifierRuntimePacket`; it exists only to state packet-authoritative field consequences on posture and execution compatibility fields

### 4.3 Execution final-risk compatibility carriage

- **Ledger scope:** `ExecutionExpressionOutput.pre_final_risk_active_playbook_ids`, `ExecutionExpressionOutput.pre_final_risk_lead_playbook_id`, `ExecutionExpressionOutput.pre_final_risk_entry_style`, `ExecutionExpressionOutput.final_risk_join`
- **Point of production:** `RiskGatewayService.apply_final_join(...)`
- **Runtime carriage:** `nvda_desk.schemas.cognition.ExecutionExpressionOutput` and `nvda_desk.schemas.cognition.FinalRiskJoinSurface`
- **Governing authoritative surfaces:** `overlay_risk_decision`, `terminal_risk_application`, `terminal_risk_decision`, `stage_local_handoff`
- **Allowed downstream readers:** `ReviewExplanationService.evaluate(...)`, parity and compatibility tests, bounded-trace comparison paths, legacy-compatible review rendering
- **Allowed use:** preserve what execution looked like before final-risk application and preserve the final joined execution effect for legacy-compatible readers
- **Prohibited use:** these fields must not be the only source used to reconstruct overlay-versus-terminal logic when preserved seam surfaces are available

### 4.4 Review-packet compatibility carriage

- **Ledger scope:** nested and additive compatibility carriage inside `ReviewExplanationOutput.review_packet`
- **Point of production:** `ReviewExplanationService.evaluate(...)`
- **Runtime carriage:** `nvda_desk.schemas.cognition.ReviewExplanationOutput.review_packet`
- **Governing authoritative surfaces:** `ReviewExplanationOutput`, `StageLocalHandoffSurface`, `EligibilityAdmissibilitySurface`, `ExecutionCandidateOwnershipSurface`, `ParallelRiskLanePacket`, `FinalRiskJoinSurface`
- **Allowed carried keys:** `final_risk_join`, `stage_local_handoff`, `overlay_risk_decision`, `terminal_risk_application`, `admissibility_surface`, `candidate_ownership`, `parallel_risk_lane`, `parallel_risk_lane_summary`, plus review-owned governance and lineage packets
- **Allowed downstream readers:** API/rendering consumers, review display helpers, bounded-trace and regression tests, legacy-compatible review consumers
- **Prohibited use:** nested or duplicated payloads inside `review_packet` must not outrank separately carried authoritative surfaces when both are present

### 4.5 Session Clock compatibility wrapper

- **Canonical label:** Session Clock
- **Canonical slug:** `session_clock`
- **Category:** `compatibility_surface`
- **Canonical owner slug:** `temporal_context`
- **Vocabulary authority source:** `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json:289-307`
- **Point of production:** `MarketStateService.get_session_clock(...)`
- **Runtime contract:** `nvda_desk.schemas.temporal_surface.SessionClockCompatibilityPayload`
- **Governing authoritative surface:** `TemporalStateFeaturePayload`
- **Allowed downstream readers:** `/market/session-clock`, compatibility tests, legacy temporal consumers that still require the wrapper shape
- **Prohibited use:** `session_clock` must not be described or treated as canonical Step-1 truth; it is an explicit compatibility wrapper retained over `temporal_state`

## 5. Downstream consumer ledger

### 5.1 Runtime readers

#### 5.1.1 Modifier path

- **Consumer:** `StateConditionedModifierService.evaluate(...)`
- **Reads:** `PostureRiskOutput`
- **Read mode:** required
- **Forbidden fallback:** `posture_hard_invariants` or `posture_local_envelope` alone must not substitute for the full posture packet

#### 5.1.2 Eligibility path

- **Consumer:** `PlaybookEligibilityService.evaluate(...)`
- **Reads:** `PostureRiskOutput`
- **Read mode:** required
- **Forbidden fallback:** selector annotations or downstream annotations must not substitute for posture-owned permission truth

#### 5.1.3 Execution path

- **Consumer:** `ExecutionExpressionService.evaluate(...)`
- **Reads:** `PostureRiskOutput`, `PlaybookEligibilityOutput`, `ModifierRuntimePacket`, `ParallelRiskLanePacket`, bounded `PositionContextInput`
- **Read mode:** required
- **Forbidden fallback:** `EligibilityAdmissibilitySurface` alone must not substitute for the full eligibility stage packet during execution synthesis

#### 5.1.4 Risk-gateway path

- **Consumer:** `RiskGatewayService.evaluate_overlay(...)`
- **Reads:** `TemporalContextInput`, `TemporalContextOutput`, `MarketRegimeContextInput`, `OptionsFlowContextInput`, `PostureRiskOutput`, `ExecutionExpressionOutput`, inventory/risk-budget state
- **Read mode:** required
- **Forbidden fallback:** `FinalRiskJoinSurface` must not be used as an input to overlay evaluation

#### 5.1.5 Terminal-application path

- **Consumer:** `RiskGatewayService.build_terminal_risk_application(...)`
- **Reads:** `overlay_risk_decision`, `PostureRiskOutput.permission_state`
- **Read mode:** required
- **Forbidden fallback:** `final_risk_join` must not substitute for terminal-application computation

#### 5.1.6 Parallel-risk enrichment path

- **Consumer:** `ParallelRiskLaneService.enrich_candidate_semantics(...)`
- **Reads:** `PostureRiskOutput`, `PlaybookEligibilityOutput`, `ExecutionExpressionOutput`
- **Read mode:** required after those stages emit
- **Forbidden fallback:** the lane must not infer candidate state before the owning serial stages have produced lawful outputs

### 5.2 Review and explanation readers

#### 5.2.1 Review reconstruction path

- **Consumer:** `ReviewExplanationService.evaluate(...)`
- **Reads:** `temporal`, `regime`, `options_flow`, `posture`, `eligibility`, `execution`, `modifier_runtime_packet`, `parallel_risk_lane_packet`, `stage_local_handoff`, `temporal_input`
- **Read mode:** required
- **Forbidden fallback:** nested `review_packet` carriage must not substitute for the direct input surfaces used to build `ReviewExplanationOutput`

#### 5.2.2 Review rendering path

- **Consumer:** `ReviewExplanationOutput.review_packet`
- **Reads:** direct stage outputs plus additive seam surfaces during serialisation
- **Read mode:** additive and legacy-compatible
- **Forbidden fallback:** review-packet copies must not become a second authority chain when separately carried surfaces are available

### 5.3 Replay and bounded-trace readers

#### 5.3.1 Bounded trace run capture

- **Consumer:** `BoundedTraceReview._run_one(...)`
- **Reads:** `EligibilityAdmissibilitySurface`, `ExecutionCandidateOwnershipSurface`, `StageLocalHandoffSurface.overlay_risk_decision`, `StageLocalHandoffSurface.terminal_risk_application`, `ExecutionExpressionOutput.final_risk_join`
- **Read mode:** required for preserved-seam capture plus legacy-compatible comparison
- **Forbidden fallback:** `final_risk_join` alone must not replace preserved seam reads when those seams are present

#### 5.3.2 Bounded trace report contract

- **Consumer:** `BoundedTraceRunResult`
- **Reads/carried fields:** `admissibility_surface`, `candidate_ownership`, `overlay_risk_decision`, `terminal_risk_application`, `final_risk_action`
- **Read mode:** explicit preserved-seam carriage for replay/reporting
- **Forbidden fallback:** Stage 6 ownership must not be reconstructed from Stage 5 admissibility inside bounded trace reports

#### 5.3.3 Bounded trace markdown rendering

- **Consumer:** `BoundedTraceReview.render_markdown_report(...)`
- **Reads:** admissibility, candidate ownership, overlay decision, terminal application
- **Read mode:** additive reporting
- **Forbidden fallback:** final-risk action summary must not collapse overlay and terminal surfaces into one undifferentiated field when both are available

### 5.4 API and rendering readers

#### 5.4.1 Temporal API readers

- **Consumer:** `/market/temporal-state`
- **Reads:** `TemporalStateFeaturePayload`
- **Read mode:** authoritative API exposure
- **Forbidden fallback:** `session_clock` must not be returned as the canonical temporal-state endpoint payload

#### 5.4.2 Session-clock API readers

- **Consumer:** `/market/session-clock`
- **Reads:** `SessionClockCompatibilityPayload`
- **Read mode:** explicit compatibility API exposure
- **Forbidden fallback:** callers must not describe this wrapper as the canonical temporal surface

#### 5.4.3 Review API readers

- **Consumers:** `/review/module-health/{module_id}`, `/review/daily-packet`
- **Reads:** review-service outputs and execution-record aggregates
- **Read mode:** review-facing output only
- **Forbidden fallback:** current API does not expose Section 3 surfaces as standalone first-class endpoints; consumers must not infer direct surface authority from the review APIs alone

### 5.5 Legacy-compatible readers

#### 5.5.1 Final-risk compatibility readers

- **Consumer:** `ReviewExplanationService.evaluate(...)` summary and `stage_reason_packets`
- **Reads:** `ExecutionExpressionOutput.final_risk_join`
- **Read mode:** legacy-compatible
- **Forbidden fallback:** this read path must not be used to reconstruct overlay-versus-terminal seam semantics when preserved surfaces are available

#### 5.5.2 Raw/prepared parity readers

- **Consumer:** `tests/test_gate103_raw_prepared_parity.py`
- **Reads:** `pre_final_risk_*`, `final_risk_join`, nested review-packet `final_risk_join`
- **Read mode:** compatibility parity verification
- **Forbidden fallback:** parity assertions do not redefine authority ownership

#### 5.5.3 Review-trace migration readers

- **Consumer:** `tests/test_gate148_review_trace_replay_runtime.py`
- **Reads:** additive `review_packet` top-level `admissibility_surface`, `candidate_ownership`, `terminal_risk_application`, plus bounded-trace seam fields
- **Read mode:** migration and anti-drift verification
- **Forbidden fallback:** legacy comparisons must not demote preserved seam surfaces below `final_risk_join`

## 6. Authority, lineage, and prohibition rules

### 6.1 Authoritative-surface precedence

- Stage packets own stage truth.
- Workflow packets own workflow truth.
- Compatibility surfaces and compatibility carriage may preserve, expose, or bridge truth, but they do not outrank the owning stage packet or workflow packet.
- When a surface is separately carried and also duplicated inside `review_packet`, the separately carried surface is authoritative.
- `ModifierRuntimePacket` outranks `ModifierCompatibilityBridgeSurface`.
- `TemporalStateFeaturePayload` outranks the `session_clock` compatibility wrapper.
- `overlay_risk_decision`, `terminal_risk_application`, and `terminal_risk_decision` outrank `final_risk_join` for seam interpretation.

### 6.2 Lineage and duplication rules

- `DeskCognitionRuntimeResult.stage_packets`, `stage_packet_ids`, and `packet_lineage` are the authoritative packet-lineage surfaces for stage-order and packet-id reconstruction.
- `ReviewExplanationOutput.packet_lineage` is the review-owned lineage surface for review and decision packet reconstruction.
- `review_packet` nested copies exist for rendering, compatibility, and anti-drift comparison. They do not form a second lineage authority chain.
- No consumer may manufacture a new authority chain by preferring duplicated nested payloads over separately carried stage, workflow, or preserved seam surfaces.

### 6.3 Stage-owner inference prohibitions

- Stage 5 admissibility must not be used to infer Stage 6 ranking, lead selection, or contradiction resolution.
- `posture_downstream_annotations` must not be treated as posture-owned permission truth, hard-invariant truth, or local-envelope truth.
- Selector-contract citations and imported-module citations do not change stage ownership.
- Compatibility bridges must not be used to imply that ownership moved away from the canonical owner slug recorded in this ledger.

### 6.4 Terminal-risk inference prohibitions

- `overlay_risk_decision` is not the terminal action.
- `final_risk_join` is not a sufficient substitute for `terminal_risk_application` or `terminal_risk_decision` when those preserved seam surfaces are available.
- `StageLocalHandoffSurface` is additive preserved truth only. It does not change stage order, execution timing, or final runtime behaviour.
- Consumers must not infer terminal-risk application solely from mutated post-join execution fields when preserved seam surfaces are present.

### 6.5 Independent parallel-risk lane restrictions

- The independent parallel risk lane is co-resident with the serial runtime. It is not an eighth serial stage.
- The lane is non-arbiting. It must not replace or overrule the seven-stage serial grammar.
- The lane may read only lawful invariant truth at session start and only lawful stage outputs after those stages have emitted them.
- The lane must not mutate stage order, registry membership, ownership law, or packet-lineage law.
- Review and explanation remain responsible for preserved downstream reconstruction of the lane once runtime execution has completed.
