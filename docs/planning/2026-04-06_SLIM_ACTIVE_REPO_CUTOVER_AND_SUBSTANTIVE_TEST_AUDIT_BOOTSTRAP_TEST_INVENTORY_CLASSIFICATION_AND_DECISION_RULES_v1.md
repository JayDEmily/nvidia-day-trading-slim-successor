# 2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_TEST_INVENTORY_CLASSIFICATION_AND_DECISION_RULES_v1

## Purpose

Freeze how the slim successor repo will classify retained tests and decide whether each test family is kept, retired, rewritten, or moved after the cutover.

## Required inventory fields

Every retained-test row must record:
- `test_id`
- `path`
- `historical_gate_lineage`
- `test_family`
- `bug_surface_class`
- `testing_phase_alignment`
- `authoritative_inputs`
- `runtime_owner_or_planning_owner`
- `downstream_consumer_or_control_surface`
- `current_truth_dependency`
- `status_candidate`
- `decision_outcome`
- `evidence_anchor`
- `disagreement_state`
- `next_action_pack`
- `notes`

## Allowed test families

- `planning_governance`
- `control_surface_integrity`
- `runtime_contract`
- `runtime_scenario`
- `invariant_or_lawful_output`
- `compatibility_wrapper`
- `review_or_trace`
- `replay_regression`
- `data_path_or_fixture`
- `repo_hygiene`
- `migration_or_closeout_guard`

## Allowed decision outcomes

- `keep_as_is`
- `keep_but_retarget_authority`
- `rewrite_for_successor_truth`
- `move_to_archive_evidence_repo`
- `retire_duplicate`
- `retire_unproven_or_orphaned`
- `defer_requires_new_anchor_or_runtime_change`

## Classification rules

### 1. Testing doctrine first
Classify against `docs/TESTING_AND_PROMOTION.md` bug-surface and phase law before using file-name heuristics.

### 2. Runtime authority first
If a test touches runtime surface ownership or compatibility-carriage law, classify it against the adopted `07` ledger plus `docs/03_DOMAIN_MODEL.md`.

### 3. Planning guards are not automatically runtime guards
A source-repo planning test may remain useful, but it must not be auto-kept as a successor runtime guard merely because it is green today.

### 4. Historical closeout strings are weak evidence
A test whose primary truth surface is a closed source-repo active/closed string must usually be rewritten for successor truth or moved back to the archive/evidence repo.

### 5. Duplicate derivation paths are not breadth
If multiple tests assert the same narrow control-surface outcome with no new bug surface, the later one is a redundancy candidate.

### 6. Orphan rule
A retained test that no longer maps cleanly to a current successor authority surface, runtime owner, or downstream consumer is an orphan and must not be silently kept.

### 7. Disagreement memory rule
If reviewers disagree on whether a test is stale, the decision register must preserve the rejected reading and the evidence that resolved it.

## What later work must not do

- keep a test only because it has a high gate number;
- retire a test only because it references an older planning pack;
- claim “rewrite” without naming the new authoritative inputs;
- move a test out of the slim repo without proving it is genuinely archive-only;
- hide deferred decisions in prose without a decision-register row.

## Gate 219 family-row interpretation

Gate 219 freezes the retained-test baseline as one row per retained **test family**, not one row per individual file.

Each family row is keyed by `test_id == test_family`. The row's `member_tests` field enumerates the exact retained `tests/test_*.py` modules currently present in the slim successor repo for that family. Gate 220 may later split a family row into narrower decision rows if mixed keep / retire / rewrite / move signals need finer granularity.

Gate 219 satisfies the required inventory fields in two coupled passes:
- `inventory_rows` freeze exact retained membership, path scope, and lineage baseline;
- `family_mappings` later add doctrine, owner, consumer, and explicit state mapping for those same `test_id` values.

## Gate 219 canonical retained-test inventory baseline

```json
[
  {
    "test_id": "compatibility_wrapper",
    "path": "tests/",
    "historical_gate_lineage": "foundational_non_gate_tests + gate_tests_49_through_49",
    "test_family": "compatibility_wrapper",
    "retained_test_count": 2,
    "member_tests": [
      "tests/test_gate49_temporal_compatibility.py",
      "tests/test_session_clock.py"
    ]
  },
  {
    "test_id": "control_surface_integrity",
    "path": "tests/",
    "historical_gate_lineage": "foundational_non_gate_tests + gate_tests_108_through_219",
    "test_family": "control_surface_integrity",
    "retained_test_count": 8,
    "member_tests": [
      "tests/test_gate108_router_only_control_surface.py",
      "tests/test_gate206_workflow_hardening_pack_planning.py",
      "tests/test_gate217_slim_successor_pack_planning.py",
      "tests/test_gate218_retained_surface_inventory_and_runtime_authority.py",
      "tests/test_gate219_test_inventory_classification.py",
      "tests/test_planning_gate_authority_consistency.py",
      "tests/test_planning_state_integrity.py",
      "tests/test_successor_pack_anti_drift.py"
    ]
  },
  {
    "test_id": "data_path_or_fixture",
    "path": "tests/",
    "historical_gate_lineage": "foundational_non_gate_tests + gate_tests_90_through_105",
    "test_family": "data_path_or_fixture",
    "retained_test_count": 8,
    "member_tests": [
      "tests/test_api.py",
      "tests/test_context_scanner_contracts.py",
      "tests/test_db_seed.py",
      "tests/test_gate105_ingress_db_api.py",
      "tests/test_gate90_financial_calendar_reference_import.py",
      "tests/test_import_registry_and_mapping.py",
      "tests/test_module_registry_promotion.py",
      "tests/test_real_data_loader.py"
    ]
  },
  {
    "test_id": "invariant_or_lawful_output",
    "path": "tests/",
    "historical_gate_lineage": "foundational_non_gate_tests + gate_tests_31_through_207",
    "test_family": "invariant_or_lawful_output",
    "retained_test_count": 38,
    "member_tests": [
      "tests/test_gate101_canonical_raw_bundle_admission.py",
      "tests/test_gate110_agents_reading_order.py",
      "tests/test_gate114_research_mode_clarity_microtranche.py",
      "tests/test_gate142_overwrite_and_ownership_inventory.py",
      "tests/test_gate146_admissibility_candidate_ownership.py",
      "tests/test_gate151_field_level_ownership_and_consumer_migration.py",
      "tests/test_gate154_downstream_consumer_reconciliation_replan.py",
      "tests/test_gate155_downstream_consequence_routing_and_successor_boundary.py",
      "tests/test_gate157_parallel_risk_lane_foundation_bootstrap.py",
      "tests/test_gate158_co_resident_parallel_risk_lane_law.py",
      "tests/test_gate158_target_architecture_and_stage_purity_consolidation.py",
      "tests/test_gate159_coefficient_world_status_and_inventory_law.py",
      "tests/test_gate159_workbook_lineage_and_consolidation_audit.py",
      "tests/test_gate160_governed_signal_coefficient_reference_workbook_law.py",
      "tests/test_gate160_owner_stage_and_activation_state_ledger.py",
      "tests/test_gate161_opportunity_vs_caution_shaping_law.py",
      "tests/test_gate162_successor_implementation_routing_for_workstreams_1_4.py",
      "tests/test_gate163_ownership_output_coefficient_and_anti_duplication_law.py",
      "tests/test_gate165_lean_policy_law_externalisation.py",
      "tests/test_gate169_calibration_metadata_and_receipts.py",
      "tests/test_gate172_master_child_lineage_and_overlap_ledger.py",
      "tests/test_gate184_weighting_fail_closed.py",
      "tests/test_gate185_surface_anchor_divergence.py",
      "tests/test_gate207_router_and_doctrine_consolidation.py",
      "tests/test_gate31_higher_order_context_composites.py",
      "tests/test_gate59_doctrine_rebase.py",
      "tests/test_gate61_non_action_conflict.py",
      "tests/test_gate62_stability_metric_corridors.py",
      "tests/test_gate68_precursor_universe.py",
      "tests/test_gate69_phase_carry_policy.py",
      "tests/test_gate71_modifier_control_law.py",
      "tests/test_gate75_precursor_stitching.py",
      "tests/test_gate79_horizon_discovery_harness.py",
      "tests/test_gate80_corrective_pass_reset.py",
      "tests/test_gate85_horizon_economic_behaviour.py",
      "tests/test_module_evaluators.py",
      "tests/test_second_wave_records_and_events.py",
      "tests/test_testing_phase0_foundation.py"
    ]
  },
  {
    "test_id": "migration_or_closeout_guard",
    "path": "tests/",
    "historical_gate_lineage": "gate_tests_86_through_210",
    "test_family": "migration_or_closeout_guard",
    "retained_test_count": 15,
    "member_tests": [
      "tests/test_gate106_successor_closeout.py",
      "tests/test_gate112_governance_closeout.py",
      "tests/test_gate121_historical_evaluation_readiness_closeout.py",
      "tests/test_gate122_signal_coefficient_authority_closeout.py",
      "tests/test_gate149_stage_local_handoff_pack_closeout.py",
      "tests/test_gate156_corrective_pack_anti_drift_closeout.py",
      "tests/test_gate163_coefficient_architecture_consolidation_closeout.py",
      "tests/test_gate164_parallel_risk_lane_foundation_anti_drift_closeout.py",
      "tests/test_gate170_policy_temporal_observability_successor_closeout.py",
      "tests/test_gate180_master_child_integration_closeout.py",
      "tests/test_gate186_options_trace_integrity_closeout.py",
      "tests/test_gate191_capital_deployment_authority_closeout.py",
      "tests/test_gate210_operator_surface_alignment_and_cutover.py",
      "tests/test_gate86_event_ingestion_precedence_and_closeout.py",
      "tests/test_gate95_phase0_closeout.py"
    ]
  },
  {
    "test_id": "planning_governance",
    "path": "tests/",
    "historical_gate_lineage": "foundational_non_gate_tests + gate_tests_46_through_209",
    "test_family": "planning_governance",
    "retained_test_count": 35,
    "member_tests": [
      "tests/test_execution_planning_contracts.py",
      "tests/test_financial_calendar_planning_v3.py",
      "tests/test_gate101_successor_planning.py",
      "tests/test_gate107_repo_process_governance.py",
      "tests/test_gate109_template_pack_governance.py",
      "tests/test_gate111_governance_guardrails.py",
      "tests/test_gate115_historical_evaluation_readiness_planning.py",
      "tests/test_gate122_signal_coefficient_authority_planning.py",
      "tests/test_gate128_post_flight_repo_consistency_planning.py",
      "tests/test_gate135_opening_drive_continuation_lifecycle_planning.py",
      "tests/test_gate141_stage_local_handoff_terminal_risk_seams_planning.py",
      "tests/test_gate144_posture_split_planning.py",
      "tests/test_gate146_admissibility_candidate_ownership_planning.py",
      "tests/test_gate147_overlay_terminal_risk_planning.py",
      "tests/test_gate150_corrective_successor_pack_planning.py",
      "tests/test_gate157_coefficient_architecture_consolidation_pack_planning.py",
      "tests/test_gate164_policy_temporal_observability_successor_pack_planning.py",
      "tests/test_gate166_temporal_governance_status_ledger.py",
      "tests/test_gate171_master_child_parallel_risk_integration_pack_planning.py",
      "tests/test_gate173_child_planning_reference_data_merge.py",
      "tests/test_gate187_capital_deployment_authority_pack_planning.py",
      "tests/test_gate192_phase3_main_target_repair_pack_planning.py",
      "tests/test_gate200_target_repo_admitted_evidence_successor_pack_planning.py",
      "tests/test_gate201_target_repo_evidence_governance_planning.py",
      "tests/test_gate203_target_repo_snapshot_and_collection_planning.py",
      "tests/test_gate204_target_repo_dmp_failure_pack_planning.py",
      "tests/test_gate209_planning_tree_and_evidence_taxonomy.py",
      "tests/test_gate46_50_planning_pack.py",
      "tests/test_gate50_vocabulary_governance.py",
      "tests/test_gate51_cognitive_workflow_planning.py",
      "tests/test_gate55_vocabulary_governance.py",
      "tests/test_gate64_candidate_adjudication_governance.py",
      "tests/test_gate94_testing_module_planning.py",
      "tests/test_planning_ready_import_backlog_partition.py",
      "tests/test_tranche_briefing_template_pack.py"
    ]
  },
  {
    "test_id": "replay_regression",
    "path": "tests/",
    "historical_gate_lineage": "foundational_non_gate_tests + gate_tests_127_through_127",
    "test_family": "replay_regression",
    "retained_test_count": 4,
    "member_tests": [
      "tests/test_gate127_replay_coefficient_visibility.py",
      "tests/test_replay_compare_runtime.py",
      "tests/test_research_eval_replay.py",
      "tests/test_research_replay.py"
    ]
  },
  {
    "test_id": "repo_hygiene",
    "path": "tests/",
    "historical_gate_lineage": "foundational_non_gate_tests + gate_tests_179_through_179",
    "test_family": "repo_hygiene",
    "retained_test_count": 4,
    "member_tests": [
      "tests/test_boundaries_and_config_surface.py",
      "tests/test_document_hygiene.py",
      "tests/test_fixtures_and_config.py",
      "tests/test_gate179_repo_wide_vocabulary_hygiene.py"
    ]
  },
  {
    "test_id": "review_or_trace",
    "path": "tests/",
    "historical_gate_lineage": "foundational_non_gate_tests + gate_tests_38_through_202",
    "test_family": "review_or_trace",
    "retained_test_count": 21,
    "member_tests": [
      "tests/test_carry_review_cli_and_legacy.py",
      "tests/test_dmp_review_trace.py",
      "tests/test_execution_review_runtime.py",
      "tests/test_gate125_review_visible_lineage.py",
      "tests/test_gate132_bounded_trace_scenario_pack.py",
      "tests/test_gate133_bounded_trace_review_regime.py",
      "tests/test_gate134_bounded_trace_reporting.py",
      "tests/test_gate148_review_trace_replay_planning.py",
      "tests/test_gate148_review_trace_replay_runtime.py",
      "tests/test_gate168_review_observability_chain_strengthening.py",
      "tests/test_gate177_parallel_risk_anti_duplication_and_review_integration.py",
      "tests/test_gate181_options_trace_integrity_pack_planning.py",
      "tests/test_gate202_target_repo_review_governance_planning.py",
      "tests/test_gate38_review_ledger_attribution_spine_contracts.py",
      "tests/test_gate39_review_overlays_feedback_chain_contracts.py",
      "tests/test_gate63_review_eligibility_governance.py",
      "tests/test_gate77_review_failure_taxonomy.py",
      "tests/test_gate82_review_surface_runtime_emission.py",
      "tests/test_gate83_review_governance_surface_builders.py",
      "tests/test_review_attribution_contracts.py",
      "tests/test_tranche_a_review_replay.py"
    ]
  },
  {
    "test_id": "runtime_contract",
    "path": "tests/",
    "historical_gate_lineage": "foundational_non_gate_tests + gate_tests_28_through_190",
    "test_family": "runtime_contract",
    "retained_test_count": 44,
    "member_tests": [
      "tests/test_dmp_v2_protocol.py",
      "tests/test_execution_lifecycle_contracts.py",
      "tests/test_gate103_raw_prepared_parity.py",
      "tests/test_gate113_execution_authority_microtranche.py",
      "tests/test_gate123_coefficient_authority.py",
      "tests/test_gate124_mutable_surface_authority.py",
      "tests/test_gate126_temporal_threshold_authority.py",
      "tests/test_gate140_execution_ledger_alembic_parity.py",
      "tests/test_gate143_stage_local_handoff_runtime.py",
      "tests/test_gate152_stage5_stage6_authority_replan.py",
      "tests/test_gate153_overlay_terminal_final_join_authority_replan.py",
      "tests/test_gate161_temporal_calendar_event_and_multi_clock_authority_mapping.py",
      "tests/test_gate167_serial_conservatism_binding_point_law.py",
      "tests/test_gate174_parallel_risk_lane_input_contract.py",
      "tests/test_gate182_options_iv_contract.py",
      "tests/test_gate183_option_surface_raw_contract.py",
      "tests/test_gate188_capital_deployment_authority_contract.py",
      "tests/test_gate189_capital_deployment_authority_service.py",
      "tests/test_gate190_capital_deployment_authority_integration.py",
      "tests/test_gate28_ingress_substrate_contracts.py",
      "tests/test_gate29_market_context_synthesis_contracts.py",
      "tests/test_gate30_options_ingress_primary_flow_contracts.py",
      "tests/test_gate32_archetype_entry_gate_bridge_contracts.py",
      "tests/test_gate33_ladder_execution_readiness_contracts.py",
      "tests/test_gate34_posture_permission_core_contracts.py",
      "tests/test_gate35_execution_orchestration_core_contracts.py",
      "tests/test_gate36_execution_state_ledger_spine_contracts.py",
      "tests/test_gate37_exit_reentry_continuity_contracts.py",
      "tests/test_gate47_registry_v2.py",
      "tests/test_gate48_carry_handoff.py",
      "tests/test_gate53_carry_handoff.py",
      "tests/test_gate54_dmp_binding_surface.py",
      "tests/test_gate60_state_policy_ontology.py",
      "tests/test_gate65_event_taxonomy.py",
      "tests/test_gate66_desk_calendar_contracts.py",
      "tests/test_gate76_precursor_runtime_binding.py",
      "tests/test_gate84_failure_taxonomy_evidence_floor.py",
      "tests/test_market_substrate_contracts.py",
      "tests/test_playbook_registry.py",
      "tests/test_posture_enricher_contracts.py",
      "tests/test_runtime_contract_registry.py",
      "tests/test_runtime_parity_registry_playbooks.py",
      "tests/test_tranche_a_posture_eligibility_contracts.py",
      "tests/test_tranche_a_upstream_contracts.py"
    ]
  },
  {
    "test_id": "runtime_scenario",
    "path": "tests/",
    "historical_gate_lineage": "foundational_non_gate_tests + gate_tests_43_through_178",
    "test_family": "runtime_scenario",
    "retained_test_count": 40,
    "member_tests": [
      "tests/test_gate100_bounded_scenario_matrix.py",
      "tests/test_gate102_raw_runtime_harness.py",
      "tests/test_gate104_property_stateful.py",
      "tests/test_gate115_normalised_prepared_runtime_features.py",
      "tests/test_gate116_event_class_temporal_windows.py",
      "tests/test_gate117_precursor_economics.py",
      "tests/test_gate118_mutable_surface_operability.py",
      "tests/test_gate119_candidate_adjudication.py",
      "tests/test_gate120_execution_geometry.py",
      "tests/test_gate121_final_risk_gateway_join.py",
      "tests/test_gate144_posture_split_runtime.py",
      "tests/test_gate145_modifier_policy_bridge_runtime.py",
      "tests/test_gate147_overlay_terminal_risk_runtime.py",
      "tests/test_gate162_market_options_dependency_and_dislocation_mapping.py",
      "tests/test_gate175_temporal_calendar_multi_clock_runtime.py",
      "tests/test_gate176_market_options_dependency_dislocation_runtime.py",
      "tests/test_gate178_proofs_and_calibration_integration.py",
      "tests/test_gate43_options_playbook_expansion.py",
      "tests/test_gate52_native_playbook_hierarchy.py",
      "tests/test_gate56_58_dmp_promotion.py",
      "tests/test_gate67_event_window_semantics.py",
      "tests/test_gate70_event_options_stress_policy.py",
      "tests/test_gate72_event_ingestion_provenance.py",
      "tests/test_gate73_event_store_query.py",
      "tests/test_gate74_live_event_richness.py",
      "tests/test_gate78_modifier_runtime_integration.py",
      "tests/test_gate81_live_event_temporal_semantics.py",
      "tests/test_gate89_financial_calendar_crosswalk_and_dmp_lane.py",
      "tests/test_gate91_financial_calendar_canonical_projection.py",
      "tests/test_gate92_financial_calendar_temporal_transition.py",
      "tests/test_gate93_financial_calendar_downstream_alignment.py",
      "tests/test_gate96_canonical_runtime_harness.py",
      "tests/test_gate97_runtime_invariants.py",
      "tests/test_gate98_threshold_edges.py",
      "tests/test_gate99_runtime_transitions.py",
      "tests/test_market_regime_context.py",
      "tests/test_options_flow_context.py",
      "tests/test_posture_risk_and_playbook.py",
      "tests/test_temporal_context_runtime.py",
      "tests/test_temporal_context_signal_state.py"
    ]
  }
]
```
