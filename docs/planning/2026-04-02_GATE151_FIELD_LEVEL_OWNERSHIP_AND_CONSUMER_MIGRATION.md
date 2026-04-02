# 2026-04-02 Gate 151 Field-Level Ownership and Consumer Migration

Status: complete on `main`

## Purpose

Convert Gate 142's overwrite inventory into a field-level ownership ledger and a transitive consumer migration matrix so later corrective gates stop inferring authority from broad stage labels alone.

## Scope boundary

Gate 151 is planning-only. It does not change runtime semantics, packet carriage, or review rendering. It freezes which surfaces are authoritative, which are compatibility-only, which consumers read them today, and which later gates must migrate them.

No new governed vocabulary is admitted in Gate 151.

## Frozen authorities re-read for Gate 151

- `docs/01_NORMATIVE.md`
- `docs/03_DOMAIN_MODEL.md`
- `docs/05_GUARDRAILS.md`
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `docs/planning/2026-04-01_GATE142_OVERWRITE_AND_OWNERSHIP_INVENTORY.md`
- `src/nvda_desk/schemas/cognition.py`
- `src/nvda_desk/services/cognition_runtime.py`
- `src/nvda_desk/services/posture_risk.py`
- `src/nvda_desk/services/state_conditioned_modifier.py`
- `src/nvda_desk/services/playbook_eligibility.py`
- `src/nvda_desk/services/execution_expression.py`
- `src/nvda_desk/services/risk_gateway.py`
- `src/nvda_desk/services/review_explanation.py`
- `src/nvda_desk/testing/bounded_trace_review.py`
- `src/nvda_desk/schemas/trace_review.py`
- `src/nvda_desk/services/review_packets.py`
- `src/nvda_desk/api/app.py`
- downstream expectation tests that still read compatibility outputs directly

## Field-level ownership ledger

The table below names every seam-affected downstream field group from posture through final join. Each row records the base owner, later mutation path, current review or trace visibility, and whether the surface is authoritative now or retained only for compatibility.

| Field group | Exact fields frozen here | Base owner | Later mutation path on current baseline | Current readers / visibility | Authority verdict now |
|---|---|---|---|---|---|
| Posture base decision fields | `permission_state`, `posture_label`, `inventory_posture_state`, `fresh_deployable_capital_pct`, `overnight_deployable_capital_pct`, `inventory_action_bias`, `fresh_vs_inventory_state`, `thesis_state`, `capital_lockup_state`, `adverse_excursion_state`, `time_stop_state`, `signal_conflict_state`, `time_stop_minutes_remaining`, `thesis_pressure_score` | `PostureRiskService.evaluate(...)` | selector citations append reasons before modifier evaluation; `StateConditionedModifierService.apply_to_posture(...)` may override `permission_state`, `posture_label`, deployable-capital fields, and `inventory_action_bias` | Stage 5 reads the post-modifier posture packet; review exposes only the final nested `posture` packet unless `stage_local_handoff.cited_posture_pre_modifier` is consulted | Base semantics belong to posture; post-modifier values are authoritative for downstream runtime; pre-modifier truth must be read from `cited_posture_pre_modifier` rather than inferred from final posture |
| Posture ownership split surfaces | `hard_invariants`, `local_envelope`, `downstream_annotations` | `PostureRiskService.evaluate(...)` for `hard_invariants` and `local_envelope`; later services may append `downstream_annotations` only | selector citations and modifier policy append annotations; neither later stage may rewrite `hard_invariants` or `local_envelope` | nested `posture` review packet and `stage_local_handoff.cited_posture_pre_modifier` | `hard_invariants` and `local_envelope` are authoritative posture-owned truth; `downstream_annotations` is explicitly downstream and non-authoritative |
| Posture modifier carriage | `modifier_runtime_packet`, `modifier_compatibility_bridge`, `stand_down_class`, `conflict_classes`, `degradation_step`, `override_disposition`, appended `reasons` | `ModifierRuntimePacket` emitted by `StateConditionedModifierService.evaluate(...)`; bridge built by `apply_to_posture(...)` | packet is attached after selector citations; bridge records which posture fields were overridden | final nested `posture` packet; preserved in `stage_local_handoff.cited_posture_pre_modifier` only before modifier attachment if needed for raw posture inspection | packet and bridge are authoritative for modifier-caused consequences; they do not transfer ownership of posture-only base fields |
| Stage 5 compatibility candidate lists | `active_family_ids`, `watch_family_ids`, `active_setup_variant_ids`, `watch_setup_variant_ids`, `add_candidates`, `hold_candidates`, `trim_candidates`, `reduce_candidates`, `hedge_candidates`, `probe_candidates`, `watch_only_candidates`, `no_trade_reasons`, `rejected_playbook_reasons`, `candidates` | `PlaybookEligibilityService.evaluate(...)` | selector citations append Stage 5 reasons after eligibility evaluation; no later stage mutates the eligibility packet itself | nested `eligibility` review packet; `stage_local_handoff.cited_eligibility`; execution consumes the cited eligibility packet directly | authoritative today for compatibility and downstream display, but too broad to express the Stage 5 / Stage 6 boundary by themselves |
| Stage 5 bounded authority surface | `EligibilityAdmissibilitySurface.permission_state`, `no_trade_reasons`, `admissible_family_ids`, `watch_family_ids`, `admissible_setup_variant_ids`, `watch_setup_variant_ids`, `admissible_playbook_ids`, `watch_only_playbook_ids`, `notes` | `PlaybookEligibilityService.evaluate(...)` | no later stage mutates the surface; Stage 6 reads it when building candidate ownership | top-level `review_packet["admissibility_surface"]`, nested `review_packet["eligibility"]["admissibility_surface"]`, `stage_local_handoff.cited_eligibility.admissibility_surface`, bounded trace `admissibility_surface` | authoritative Stage 5 boundary surface; later stages must not redefine its meaning by implication |
| Stage 6 pre-final execution synthesis | `active_playbook_ids`, `active_setup_variant_ids`, `active_family_ids`, `lead_playbook_id`, `lead_setup_variant_id`, `lead_family_id`, `contradiction_resolution`, `lead_selection_score`, `lead_selection_reasons`, `candidate_adjudication`, `entry_style`, `inventory_action`, `fresh_capital_action`, `target_fresh_deployable_pct`, `lifecycle_plan`, `reasons` | `ExecutionExpressionService.evaluate(...)` | `apply_to_execution(...)` may override operative execution surfaces and attach modifier bridge before overlay evaluation; later `apply_final_join(...)` may rewrite selected final-risk compatibility fields | final nested `execution` review packet; preserved pre-modifier and post-modifier snapshots inside `stage_local_handoff` | authoritative Stage 6 synthesis exists only before final join mutates execution; later readers needing pre-final truth must use `stage_local_handoff.execution_pre_modifier` or `stage_local_handoff.execution_post_modifier_pre_final_risk` |
| Stage 6 bounded authority surface | `ExecutionCandidateOwnershipSurface.admitted_playbook_ids`, `watch_only_playbook_ids`, `adjudicated_playbook_ids`, `lead_playbook_id`, `contradiction_resolution`, `notes` | `ExecutionExpressionService._candidate_ownership_surface(...)` | surface is computed after adjudication and before final risk; later services do not mutate the surface itself | top-level `review_packet["candidate_ownership"]`, nested `review_packet["execution"]["candidate_ownership"]`, bounded trace `candidate_ownership` | authoritative Stage 6 ownership boundary surface; distinct from Stage 5 admissibility and distinct from final-risk compatibility wrappers |
| Execution modifier carriage | `ExecutionExpressionOutput.modifier_runtime_packet`, `modifier_compatibility_bridge`, overridden operative surfaces such as `entry_gate_score_floor`, `zone_score_threshold`, `max_risk_per_trade`, `hedge_required`, `target_fresh_deployable_pct` | `ModifierRuntimePacket` plus `StateConditionedModifierService.apply_to_execution(...)` | execution synthesis is mutated after Stage 6 selection but before overlay evaluation | final nested `execution` review packet; preserved in `stage_local_handoff.execution_post_modifier_pre_final_risk` | authoritative for modifier-caused execution consequences only; does not replace Stage 6 ownership truth |
| Overlay and terminal seam | `StageLocalHandoffSurface.overlay_risk_decision`, `StageLocalHandoffSurface.terminal_risk_application`, `terminal_risk_decision` | `RiskGatewayService.evaluate_overlay(...)` then `build_terminal_risk_application(...)` | final risk decision is created before `apply_final_join(...)` mutates execution | top-level `review_packet["overlay_risk_decision"]`, top-level `review_packet["terminal_risk_application"]`, nested `review_packet["stage_local_handoff"]`, bounded trace `overlay_risk_decision` and `terminal_risk_application` | authoritative additive seam for overlay-versus-terminal inspection; final execution packet alone is insufficient to reconstruct it |
| Final-risk compatibility wrapper | `pre_final_risk_active_playbook_ids`, `pre_final_risk_lead_playbook_id`, `pre_final_risk_entry_style`, `final_risk_join` | `RiskGatewayService.apply_final_join(...)` | mutates execution after terminal decision is already known | nested `review_packet["execution"]`, top-level `review_packet["final_risk_join"]`, compatibility tests, parity tests, runtime invariant tests | compatibility-only wrapper for downstream continuity; not the authoritative source of Stage 5, Stage 6, or overlay-versus-terminal ownership |
| Preserved handoff carrier | `cited_posture_pre_modifier`, `cited_eligibility`, `execution_pre_modifier`, `execution_post_modifier_pre_final_risk`, `overlay_risk_decision`, `terminal_risk_application`, `terminal_risk_decision`, `notes` | `DeskCognitionRuntime.run(...)` | additive carriage only; no downstream mutation | top-level runtime result, nested review packet, bounded trace | authoritative preserved seam carrier for "what existed at that moment"; additive only and not a replacement for the runtime stage outputs |

## Transitive consumer migration matrix

The matrix below names the concrete downstream readers discovered on the current baseline. Priority means "which consumer later gates must reason about first", not "which file is most important globally".

| Consumer | Current read path | Reads authoritative or compatibility surface today | Migration priority | Gate 151 verdict |
|---|---|---|---|---|
| `src/nvda_desk/services/review_explanation.py` | builds nested `posture`, `eligibility`, `execution`, top-level `final_risk_join`, top-level `admissibility_surface`, top-level `candidate_ownership`, and top-level seam exports from `stage_local_handoff` | mixed: authoritative top-level seam surfaces plus compatibility nested packets | P1 | primary runtime-review consumer; later consumer-reconciliation gates must treat it as the canonical migration source of truth |
| `src/nvda_desk/testing/bounded_trace_review.py` | reads `result.eligibility.admissibility_surface`, `result.execution.candidate_ownership`, `result.stage_local_handoff.overlay_risk_decision`, `result.stage_local_handoff.terminal_risk_application`, and `result.execution.final_risk_join` | mixed authoritative + compatibility | P1 | primary trace consumer; later gates must keep bounded trace able to compare preserved seam truth against compatibility wrappers explicitly |
| `src/nvda_desk/schemas/trace_review.py` | `BoundedTraceRunResult` stores `admissibility_surface`, `candidate_ownership`, `overlay_risk_decision`, `terminal_risk_application`, while `final_risk_action` remains a scalar compatibility summary | mixed authoritative + compatibility | P1 | schema already carries the preserved surfaces; later gates should not collapse back to `final_risk_action` alone |
| `tests/test_gate121_final_risk_gateway_join.py` | asserts `final_risk_join`, `pre_final_risk_lead_playbook_id`, and nested review execution compatibility fields | compatibility-only | P2 | keep until later gates lawfully retire compatibility fields; do not misread this test as proving ownership closure |
| `tests/test_gate103_raw_prepared_parity.py` | compares whole review packets and `final_risk_join` across raw/prepared paths | compatibility-heavy | P2 | parity test preserves compatibility surfaces; later migration must keep explicit equality expectations honest |
| `tests/test_gate97_runtime_invariants.py` | freezes final review stage order ending with `final_risk_join` | compatibility-only | P2 | invariant remains valid but does not prove preserved seam sufficiency |
| `tests/test_execution_review_runtime.py` | reads nested review execution packet and other review surfaces; does not currently depend on top-level preserved seam surfaces | mostly compatibility nested packets | P2 | later consumer work must decide whether to add preserved-seam expectations here or leave it as compatibility coverage intentionally |
| `tests/test_gate125_review_visible_lineage.py` | reads review lineage and effective policy outputs, not the new seam surfaces directly | indirect / compatibility-adjacent | P3 | retain as adjacent evidence only |
| `tests/test_dmp_review_trace.py` | exercises DMP review lineage, not stage-local seam fields directly | indirect | P3 | keep as non-blocking adjacent evidence |
| `tests/test_tranche_a_review_replay.py` | exercises imported module maturity and replay review packets, not stage-local seam fields directly | indirect | P3 | keep as non-blocking adjacent evidence |
| `src/nvda_desk/services/review_packets.py` | builds `DailyReviewPacket` from database/account/event services rather than `ReviewExplanationOutput.review_packet` | no direct stage-local seam reads on current baseline | deferred / non-direct | Gate 142 named it as adjacent review infrastructure, but on the observed Gate 149 baseline it is not a direct reader of the preserved seam surfaces |
| `src/nvda_desk/api/app.py` daily review endpoint | returns `ReviewPacketService.daily_packet(...)` rather than runtime `ReviewExplanationOutput` | no direct stage-local seam reads on current baseline | deferred / non-direct | same verdict as `review_packets.py`; keep as adjacent infrastructure only unless future gates wire runtime review packets into the API |

## Preserved-seam sufficiency and residual-gap law

### Sufficient now

The preserved seam is sufficient **now** for three bounded purposes only:
1. proving what the runtime object looked like before modifier mutation, after modifier mutation, and before final join;
2. letting review and bounded-trace consumers inspect Stage 5 admissibility, Stage 6 candidate ownership, and overlay-versus-terminal authority without mining only compatibility wrappers;
3. keeping the historical Gate 141-149 runtime behaviour intact while later gates harden planning truth.

### Not sufficient yet

The preserved seam is **not** sufficient yet to close the following questions:
- exact Stage 5 case completeness across admitted, blocked, watch-only, event-veto, venue-distortion, and no-lead paths;
- exact Stage 6 contradiction, tiebreak, multi-candidate, and watch-only non-promotion law;
- exhaustive overlay-versus-terminal overlap coverage and the precise status of `final_risk_join` as a compatibility wrapper rather than a new arbiter;
- downstream consumer retirement conditions for compatibility surfaces such as `pre_final_risk_*`, nested `execution.final_risk_join`, and review tests that still rely on them;
- any larger architecture question around an independent parallel risk lane, final arbiter, or dynamic coefficient redesign.

## Residual-gap ledger handed to later gates

### Gate 152 input

Gate 152 must treat `EligibilityAdmissibilitySurface` as the authoritative Stage 5 boundary and `ExecutionCandidateOwnershipSurface` as the authoritative Stage 6 boundary, then write exact case law for blocked, watch-only, no-lead, single-candidate, multi-candidate, and contradiction paths.

### Gate 153 input

Gate 153 must treat `overlay_risk_decision` and `terminal_risk_application` as the authoritative additive seam and `final_risk_join` as a compatibility wrapper until a later gate proves otherwise.

### Gate 154 clarification forced by Gate 151

Gate 154 must focus on the **actual** direct consumers discovered here: `review_explanation.py`, `bounded_trace_review.py`, `trace_review.py`, and the compatibility-heavy runtime expectation tests. `review_packets.py` and `src/nvda_desk/api/app.py` remain indirect daily-review surfaces rather than direct stage-local seam readers on the observed Gate 149 baseline.

### Gate 155 input

Gate 155 must route the still-open retirement conditions for compatibility surfaces, especially nested review packet reads and the `pre_final_risk_*` / `final_risk_join` family.

## Gate 151 closeout decision

Gate 151 closes as planning complete because the repo now has:
- a field-level ownership ledger naming the owner, mutation path, and compatibility status of every seam-affected downstream field group from posture through final join;
- a transitive consumer matrix that distinguishes direct readers from adjacent but indirect infrastructure;
- an explicit residual-gap ledger that tightens Gates 152-155 rather than leaving them to implication.
