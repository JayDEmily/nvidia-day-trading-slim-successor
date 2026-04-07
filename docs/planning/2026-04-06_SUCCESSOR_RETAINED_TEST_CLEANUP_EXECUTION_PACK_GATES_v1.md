# 2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_GATES_v1

Status: closed successor execution pack through Gate 225 on `work/gate-225-retained-test-cleanup-closeout-20260406`; no active pack is currently routed. Intended successor gate range: Gates 222-225. This pack is successor-repo-only and does not reopen the source/archive repo.

## Purpose

Execute the already-classified retained-test cleanup work frozen by the closed bootstrap pack, then leave the slim successor repo ready for architecture and real-data runtime progress rather than another audit loop.

This pack was created because repo-root `PLANS.md` on successor `main` had no active pack routed, while the latest closed evidence pack had already frozen:
1. the retained-test inventory;
2. the governed keep / retarget / rewrite / move / retire decision register; and
3. the bounded proof and handoff boundary for the first successor retained-test execution pack.

## Scope

In scope:
- executing the Gate 220 and Gate 221 classified retained-test actions inside the successor repo only;
- moving archive-only historical planning and closeout tests out of the live active test surface;
- retiring duplicate replay-shadow tests once the canonical replay guards remain green;
- rewriting the one retained successor-boundary migration test that Gate 220 marked as `rewrite_for_successor_truth`;
- retargeting kept test families whose authority must move from source-era pack wording to successor-native doctrine and runtime surfaces;
- proving each gate with bounded family-specific proof slices;
- closing the cleanup pack truthfully so the next work can return to architecture and bounded real-data execution planning.

Out of scope:
- reopening or rerouting the source/archive repo;
- inventing new runtime architecture or packet law not already governed by `docs/01_NORMATIVE.md`, `docs/03_DOMAIN_MODEL.md`, `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`, `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md`, and `docs/TESTING_AND_PROMOTION.md`;
- broad blind repo-wide test execution by default;
- creating a second cleanup pack merely to finish work this pack already classifies;
- pretending classification work still needs to happen before execution begins.

## Supersession and active authority

- This document is the canonical gate authority surface for the current successor retained-test cleanup execution pack.
- It is a new pack because the prior bootstrap pack is already honestly closed through Gate 221 and repo-root `PLANS.md` now says no active pack is routed.
- It does not amend or reopen the closed bootstrap pack.
- It uses the closed bootstrap pack's decision register and handoff surface as evidence-input authority for execution sequencing.

## Governing inputs

Frozen doctrine and process inputs:
- `docs/01_NORMATIVE.md`
- `docs/03_DOMAIN_MODEL.md`
- `docs/05_GUARDRAILS.md`
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `docs/TESTING_AND_PROMOTION.md`
- `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md`
- `AGENTS.md`

Required closed-pack execution inputs:
- repo-root `PLANS.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- `docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_TEST_INVENTORY_CLASSIFICATION_AND_DECISION_RULES_v1.md`
- `docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_TEST_AUDIT_PROOF_SLICE_AND_SUCCESSOR_HANDOFF_v1.md`
- `docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_EXECUTION_LOG_v1.md`
- `docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_GATES_v1.md`
- `docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_LEAVES_v1.json`
- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`

## Workflow placement

This pack sits after the closed bootstrap pack and before any new architecture or runtime-extension pack.

It is the terminal retained-test cleanup tranche:
- clean the retained test surface decisively;
- remove archive-only and duplicate baggage;
- rewrite or retarget only what the decision register already froze; and
- stop with the repo ready for new substantive architecture planning.

## Controlled multi-gate execution authority

This pack is intentionally fatter than the bootstrap pack because the operator wants to reduce relay overhead.

For this pack only, Codex may continue from Gate 222 to Gate 225 in one continuous operator-approved run **without coming back between gates**, but only if all higher-law execution rules remain true:
- one leaf at a time;
- one gate at a time;
- one branch per gate;
- no next gate until the current gate is actually closed;
- the planning quartet must move together for each gate;
- each gate must merge back to `main` before the next gate branch opens;
- if any stop condition fires, Codex must stop immediately and report instead of opening the next gate.

This does **not** waive `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`. It is a controlled continuity rule for a terminal cleanup tranche, not free-run autonomy.

## Why four gates and four leaves each

The closed bootstrap pack already grouped the future work into four execution families:
1. archive-evidence moves;
2. successor-boundary rewrite plus replay-authority retarget;
3. duplicate retirement after replay-authority retarget; and
4. retained keep / retarget families.

The chosen gate count preserves those real differences while still making the pack fat enough to avoid operator tennis:
- Gate 222 removes archive-only clutter first;
- Gate 223 performs the smallest, highest-certainty successor-local rewrites and retargets, then retires the duplicate replay-shadow tests on the same branch only after replay-authority retarget proof lands;
- Gate 224 performs medium-blast retarget work on runtime review and contract families;
- Gate 225 finishes remaining invariant-family retarget and closes the cleanup tranche.

## Intent and workflow anchor

The repo lens remains:
- human desk operator lens first;
- runtime law and ownership authority before old pack prose;
- auditability and replayability preserved;
- no source-repo mutation;
- no silent drift from cleanup into architecture work.

This pack therefore exists to finish the test cleanup, not to become another long-lived governance nest.

## Retain / retire-from-authority / amend / add matrix

### Retain as live in the successor repo
- current doctrine stack and routing surfaces;
- successor runtime, fixture, and test surfaces that Gate 220 classified as `keep_as_is` or `keep_but_retarget_authority`;
- Gate 220 / Gate 221 decision-memory and handoff surfaces as retained evidence.

### Remove from the live active test surface
- `planning_governance__closed_source_or_historical_pack_receipts`
- `review_or_trace__historical_planning_review_receipts`
- `migration_or_closeout_guard__historical_closeout_receipts`
- `replay_regression__research_shadow_replays` after Gate 223 replay-authority retarget lands and the canonical replay guards remain green

### Rewrite in-place for successor truth
- `migration_or_closeout_guard__successor_cutover_boundary_rule`

### Retarget in-place to successor-native doctrine/runtime authority
- `compatibility_wrapper__preserved_reader_shapes`
- `replay_regression__canonical_replay_compare_guards`
- `review_or_trace__runtime_review_and_trace_surfaces`
- `runtime_contract__current_packet_and_service_contracts`
- `invariant_or_lawful_output__repo_native_law_and_ownership`

### No-change retained families that must stay provably intact
- `control_surface_integrity__successor_router_quartet`
- `data_path_or_fixture__retained_reference_and_loader_surfaces`
- `planning_governance__live_successor_process_controls`
- `repo_hygiene__retained_repo_boundary_surfaces`
- `runtime_scenario__retained_runtime_paths`

## Testing and promotion discipline

- Use successor repo-local `.venv` if it exists.
- If successor `.venv` still does not exist, reuse the already-provisioned interpreter and record that exact fact in every gate receipt.
- Do not widen to repo-wide `make check` unless a gate-local stop condition says the blast radius escaped its declared surfaces.
- Every gate must add or update exactly one gate-specific planning/execution proof surface under `tests/`.
- Every gate must also run the family-specific targeted test slice frozen for that gate below.
- The gate-specific planning/execution proof surface and `tests/test_planning_state_integrity.py` are mandatory for every gate closeout.

## Gate-level stop conditions

Stop immediately and do not open the next gate if any of the following happens:
- a gate needs to mutate `src/`, schemas, Alembic, or API code to make test cleanup truthful;
- a file classified as archive-only is needed by a still-live successor test and no lawful replacement is obvious;
- the successor-boundary rewrite cannot name its replacement successor-local authority inputs exactly;
- a retarget family proves to require more than its declared family scope and would spill into a second untouched family not already in the same gate;
- broad blind execution becomes necessary without a concrete blast-radius reason;
- source-repo mutation appears necessary.

## Gates

### Gate 222: Archive-only move execution

**Objective**
- Execute the archive-evidence move families so the active successor test surface no longer carries historical planning receipts or historical closeout receipts.

**Families executed**
- `planning_governance__closed_source_or_historical_pack_receipts`
- `review_or_trace__historical_planning_review_receipts`
- `migration_or_closeout_guard__historical_closeout_receipts`

**Definition of done**
- archive-only families are no longer in the active `tests/` surface;
- a successor-local archive-evidence destination exists and carries preserved evidence anchors plus disagreement memory;
- successor quartet routes Gate 222 complete and Gate 223 next.

**Minimum proof slice**
- `pytest -q tests/test_gate222_archive_and_duplicate_retirement.py tests/test_planning_state_integrity.py`

### Gate 223: Successor-boundary rewrite and light retarget execution

**Objective**
- Perform the smallest, highest-certainty successor-native rewrites and authority retargets so no retained test still asserts source-era cutover truth or stale compatibility/replay authority, then retire the duplicate replay-shadow tests on the same branch once the replay-authority retarget is proven.

**Families executed**
- `migration_or_closeout_guard__successor_cutover_boundary_rule`
- `compatibility_wrapper__preserved_reader_shapes`
- `replay_regression__canonical_replay_compare_guards`
- `replay_regression__research_shadow_replays`

**Definition of done**
- the retained cutover-boundary test is rewritten against successor-local authority surfaces;
- compatibility wrapper tests now anchor to adopted successor doctrine and runtime ownership;
- canonical replay compare guards now anchor to successor-local replay/runtime authority rather than source-era wording;
- duplicate research-shadow replay tests are retired only after the canonical replay compare guards remain green on the same Gate 223 branch;
- successor quartet routes Gate 223 complete and Gate 224 next.

**Minimum proof slice**
- `pytest -q tests/test_gate223_successor_boundary_and_light_retarget.py tests/test_planning_state_integrity.py`
- `pytest -q tests/test_gate49_temporal_compatibility.py tests/test_session_clock.py tests/test_replay_compare_runtime.py tests/test_gate127_replay_coefficient_visibility.py`

### Gate 224: Runtime review and contract-family retarget execution

**Objective**
- Retarget the medium-blast live successor families that still depend on old authority wording, while preserving no-change families unless fallout repair is strictly necessary.

**Families executed**
- `review_or_trace__runtime_review_and_trace_surfaces`
- `runtime_contract__current_packet_and_service_contracts`

**Guarded no-change families**
- `control_surface_integrity__successor_router_quartet`
- `data_path_or_fixture__retained_reference_and_loader_surfaces`
- `planning_governance__live_successor_process_controls`
- `repo_hygiene__retained_repo_boundary_surfaces`

**Definition of done**
- review/trace runtime family is successor-native in its authority references;
- runtime-contract family is successor-native in its authority references;
- guarded no-change families remain green except for strictly necessary fallout repairs;
- successor quartet routes Gate 224 complete and Gate 225 next.

**Minimum proof slice**
- `pytest -q tests/test_gate224_runtime_review_and_contract_retarget.py tests/test_planning_state_integrity.py`
- `pytest -q tests/test_carry_review_cli_and_legacy.py tests/test_dmp_review_trace.py tests/test_execution_review_runtime.py tests/test_gate125_review_visible_lineage.py tests/test_gate132_bounded_trace_scenario_pack.py tests/test_gate133_bounded_trace_review_regime.py tests/test_gate134_bounded_trace_reporting.py tests/test_gate148_review_trace_replay_runtime.py tests/test_gate168_review_observability_chain_strengthening.py tests/test_gate177_parallel_risk_anti_duplication_and_review_integration.py tests/test_gate38_review_ledger_attribution_spine_contracts.py tests/test_gate39_review_overlays_feedback_chain_contracts.py tests/test_gate63_review_eligibility_governance.py tests/test_gate77_review_failure_taxonomy.py tests/test_gate82_review_surface_runtime_emission.py tests/test_gate83_review_governance_surface_builders.py tests/test_review_attribution_contracts.py tests/test_tranche_a_review_replay.py tests/test_dmp_v2_protocol.py tests/test_execution_lifecycle_contracts.py tests/test_gate103_raw_prepared_parity.py tests/test_gate113_execution_authority_microtranche.py tests/test_gate123_coefficient_authority.py tests/test_gate124_mutable_surface_authority.py tests/test_gate126_temporal_threshold_authority.py tests/test_gate140_execution_ledger_alembic_parity.py tests/test_gate143_stage_local_handoff_runtime.py tests/test_gate152_stage5_stage6_authority_replan.py tests/test_gate153_overlay_terminal_final_join_authority_replan.py tests/test_gate161_temporal_calendar_event_and_multi_clock_authority_mapping.py tests/test_gate167_serial_conservatism_binding_point_law.py tests/test_gate174_parallel_risk_lane_input_contract.py tests/test_gate182_options_iv_contract.py tests/test_gate183_option_surface_raw_contract.py tests/test_gate188_capital_deployment_authority_contract.py tests/test_gate189_capital_deployment_authority_service.py tests/test_gate190_capital_deployment_authority_integration.py tests/test_gate28_ingress_substrate_contracts.py tests/test_gate29_market_context_synthesis_contracts.py tests/test_gate30_options_ingress_primary_flow_contracts.py tests/test_gate32_archetype_entry_gate_bridge_contracts.py tests/test_gate33_ladder_execution_readiness_contracts.py tests/test_gate34_posture_permission_core_contracts.py tests/test_gate35_execution_orchestration_core_contracts.py tests/test_gate36_execution_state_ledger_spine_contracts.py tests/test_gate37_exit_reentry_continuity_contracts.py tests/test_gate47_registry_v2.py tests/test_gate48_carry_handoff.py tests/test_gate53_carry_handoff.py tests/test_gate54_dmp_binding_surface.py tests/test_gate60_state_policy_ontology.py tests/test_gate65_event_taxonomy.py tests/test_gate66_desk_calendar_contracts.py tests/test_gate76_precursor_runtime_binding.py tests/test_gate84_failure_taxonomy_evidence_floor.py tests/test_market_substrate_contracts.py tests/test_playbook_registry.py tests/test_posture_enricher_contracts.py tests/test_runtime_contract_registry.py tests/test_runtime_parity_registry_playbooks.py tests/test_tranche_a_posture_eligibility_contracts.py tests/test_tranche_a_upstream_contracts.py`

### Gate 225: Invariant-family retarget and terminal cleanup closeout

**Objective**
- Finish the remaining live successor-law retarget work, then close the cleanup tranche with the repo explicitly ready for new architecture or bounded real-data execution planning.

**Families executed**
- `invariant_or_lawful_output__repo_native_law_and_ownership`

**Final no-change confirmation families**
- `runtime_scenario__retained_runtime_paths`
- all previously retained `keep_as_is` families after fallout repair

**Definition of done**
- invariant-family tests that remain in the successor repo reference successor-native lawful output and ownership doctrine rather than source-era pack wording;
- the retained runtime-scenario family and other keep-as-is families remain green after cleanup fallout;
- the new cleanup pack closes truthfully with either no active pack routed or an explicit architecture-planning-ready hold state, but without opening a fresh test-cleanup pack.

**Minimum proof slice**
- `pytest -q tests/test_gate225_retained_test_cleanup_closeout.py tests/test_planning_state_integrity.py`
- `pytest -q tests/test_gate101_canonical_raw_bundle_admission.py tests/test_gate110_agents_reading_order.py tests/test_gate114_research_mode_clarity_microtranche.py tests/test_gate142_overwrite_and_ownership_inventory.py tests/test_gate146_admissibility_candidate_ownership.py tests/test_gate151_field_level_ownership_and_consumer_migration.py tests/test_gate154_downstream_consumer_reconciliation_replan.py tests/test_gate155_downstream_consequence_routing_and_successor_boundary.py tests/test_gate157_parallel_risk_lane_foundation_bootstrap.py tests/test_gate158_co_resident_parallel_risk_lane_law.py tests/test_gate158_target_architecture_and_stage_purity_consolidation.py tests/test_gate159_coefficient_world_status_and_inventory_law.py tests/test_gate159_workbook_lineage_and_consolidation_audit.py tests/test_gate160_governed_signal_coefficient_reference_workbook_law.py tests/test_gate160_owner_stage_and_activation_state_ledger.py tests/test_gate161_opportunity_vs_caution_shaping_law.py tests/test_gate162_successor_implementation_routing_for_workstreams_1_4.py tests/test_gate163_ownership_output_coefficient_and_anti_duplication_law.py tests/test_gate165_lean_policy_law_externalisation.py tests/test_gate169_calibration_metadata_and_receipts.py tests/test_gate172_master_child_lineage_and_overlap_ledger.py tests/test_gate184_weighting_fail_closed.py tests/test_gate185_surface_anchor_divergence.py tests/test_gate207_router_and_doctrine_consolidation.py tests/test_gate31_higher_order_context_composites.py tests/test_gate59_doctrine_rebase.py tests/test_gate61_non_action_conflict.py tests/test_gate62_stability_metric_corridors.py tests/test_gate68_precursor_universe.py tests/test_gate69_phase_carry_policy.py tests/test_gate71_modifier_control_law.py tests/test_gate75_precursor_stitching.py tests/test_gate79_horizon_discovery_harness.py tests/test_gate80_corrective_pass_reset.py tests/test_gate85_horizon_economic_behaviour.py tests/test_module_evaluators.py tests/test_second_wave_records_and_events.py tests/test_testing_phase0_foundation.py tests/test_gate100_bounded_scenario_matrix.py tests/test_gate102_raw_runtime_harness.py tests/test_gate104_property_stateful.py tests/test_gate115_normalised_prepared_runtime_features.py tests/test_gate116_event_class_temporal_windows.py tests/test_gate117_precursor_economics.py tests/test_gate118_mutable_surface_operability.py tests/test_gate119_candidate_adjudication.py tests/test_gate120_execution_geometry.py tests/test_gate121_final_risk_gateway_join.py tests/test_gate144_posture_split_runtime.py tests/test_gate145_modifier_policy_bridge_runtime.py tests/test_gate147_overlay_terminal_risk_runtime.py tests/test_gate162_market_options_dependency_and_dislocation_mapping.py tests/test_gate175_temporal_calendar_multi_clock_runtime.py tests/test_gate176_market_options_dependency_dislocation_runtime.py tests/test_gate178_proofs_and_calibration_integration.py tests/test_gate43_options_playbook_expansion.py tests/test_gate52_native_playbook_hierarchy.py tests/test_gate56_58_dmp_promotion.py tests/test_gate67_event_window_semantics.py tests/test_gate70_event_options_stress_policy.py tests/test_gate72_event_ingestion_provenance.py tests/test_gate73_event_store_query.py tests/test_gate74_live_event_richness.py tests/test_gate78_modifier_runtime_integration.py tests/test_gate81_live_event_temporal_semantics.py tests/test_gate89_financial_calendar_crosswalk_and_dmp_lane.py tests/test_gate91_financial_calendar_canonical_projection.py tests/test_gate92_financial_calendar_temporal_transition.py tests/test_gate93_financial_calendar_downstream_alignment.py tests/test_gate96_canonical_runtime_harness.py tests/test_gate97_runtime_invariants.py tests/test_gate98_threshold_edges.py tests/test_gate99_runtime_transitions.py tests/test_market_regime_context.py tests/test_options_flow_context.py tests/test_posture_risk_and_playbook.py tests/test_temporal_context_runtime.py tests/test_temporal_context_signal_state.py`
