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

Gate 219 may use the pre-decision placeholder `pending_gate_220_decision` while the inventory and ownership mapping are being frozen. Gate 220 must replace that placeholder with one of the governed outcomes below before any keep / retire / rewrite / move action is treated as decided.

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

## Gate 220 governed decision law

Gate 220 converts the Gate 219 family mapping from pre-decision inventory into a governed classification law. The law below freezes how later packs must record test decisions without silently executing those decisions during classification.

### Allowed outcomes are bounded

Gate 220 may only freeze the following decision outcomes in the first-pass register:
- `keep_as_is`
- `keep_but_retarget_authority`
- `rewrite_for_successor_truth`
- `move_to_archive_evidence_repo`
- `retire_duplicate`
- `retire_unproven_or_orphaned`
- `defer_requires_new_anchor_or_runtime_change`

No synonym, shortened label, or prose-only substitute is allowed in place of those outcome values.

### Allowed disagreement states are bounded

Every Gate 220 decision row must record exactly one of:
- `no_disagreement_recorded`
- `resolved_with_memory`
- `deferred_pending_new_anchor_or_runtime_change`

### Required decision-register memory fields

Every Gate 220 decision row must preserve:
- `decision_id`
- `source_test_family`
- `member_test_count`
- `member_tests`
- `treatment_tags`
- `decision_outcome`
- `authoritative_inputs`
- `runtime_owner_or_planning_owner`
- `downstream_consumer_or_control_surface`
- `evidence_anchor`
- `disagreement_state`
- `rejected_interpretation_ids`
- `rejection_or_deferral_reason`
- `missing_requirement`
- `would_become_valid_if`
- `next_action_pack`
- `archive_destination`
- `classification_not_execution_note`
- `notes`

### Rejected and deferred readings must remain visible

If a row is moved, retired, rewritten, or deferred, the register must retain the rejected interpretation ids and the reason the rejected reading lost. Disagreement memory must remain in the register itself rather than being hidden in surrounding prose.

Rejected or deferred decisions must also preserve:
- the evidence anchors that support the chosen classification;
- the missing requirement or future condition, when the row is deferred or requires rewrite before it can remain canonical; and
- the next action pack that is allowed to execute the later move, rewrite, or retirement.

### Rejection and deferred-decision preservation

`move_to_archive_evidence_repo`, `retire_duplicate`, `retire_unproven_or_orphaned`, `rewrite_for_successor_truth`, and `defer_requires_new_anchor_or_runtime_change` are classificatory outcomes only at Gate 220. They preserve the decision, its disagreement memory, and its future execution boundary. They do not silently delete a test, move a file, or rewrite a runtime or planning surface during this gate.

### Classification is not execution

Gate 220 freezes classification and next action only. A decision row may name archive-only, stale-planning, duplicate, or successor-required treatment, but that classification does not itself execute keep / retire / rewrite / move actions.

## Gate 220 first-pass successor test decision register

```json
[
  {
    "decision_id": "compatibility_wrapper__preserved_reader_shapes",
    "source_test_family": "compatibility_wrapper",
    "member_test_count": 2,
    "member_tests": [
      "tests/test_gate49_temporal_compatibility.py",
      "tests/test_session_clock.py"
    ],
    "treatment_tags": [
      "successor_required",
      "compatibility_surface"
    ],
    "decision_outcome": "keep_but_retarget_authority",
    "authoritative_inputs": [
      "docs/TESTING_AND_PROMOTION.md",
      "docs/03_DOMAIN_MODEL.md",
      "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md"
    ],
    "runtime_owner_or_planning_owner": [
      "compatibility-wrapper surfaces that preserve older read shapes over newer canonical runtime truth"
    ],
    "downstream_consumer_or_control_surface": [
      "legacy-compatible API or reader paths",
      "session-clock compatibility consumers",
      "review and replay readers that still exercise preserved wrapper shapes"
    ],
    "evidence_anchor": [
      "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md",
      "tests/test_gate49_temporal_compatibility.py",
      "tests/test_session_clock.py"
    ],
    "disagreement_state": "no_disagreement_recorded",
    "rejected_interpretation_ids": [],
    "rejection_or_deferral_reason": "none",
    "missing_requirement": "none",
    "would_become_valid_if": "already supported by current evidence anchors",
    "next_action_pack": "Gate 221",
    "archive_destination": "not_applicable",
    "classification_not_execution_note": "Gate 220 freezes classification and next action only; no test move, deletion, rewrite, or runtime mutation is executed in this pack.",
    "notes": "Wrapper guards remain live in the successor repo, but their authority is the adopted docs/07 runtime ledger rather than source-era pack prose."
  },
  {
    "decision_id": "control_surface_integrity__successor_router_quartet",
    "source_test_family": "control_surface_integrity",
    "member_test_count": 8,
    "member_tests": [
      "tests/test_gate108_router_only_control_surface.py",
      "tests/test_gate206_workflow_hardening_pack_planning.py",
      "tests/test_gate217_slim_successor_pack_planning.py",
      "tests/test_gate218_retained_surface_inventory_and_runtime_authority.py",
      "tests/test_gate219_test_inventory_classification.py",
      "tests/test_planning_gate_authority_consistency.py",
      "tests/test_planning_state_integrity.py",
      "tests/test_successor_pack_anti_drift.py"
    ],
    "treatment_tags": [
      "successor_required",
      "planning_control_surface"
    ],
    "decision_outcome": "keep_as_is",
    "authoritative_inputs": [
      "docs/01_NORMATIVE.md",
      "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md",
      "PLANS.md",
      "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md",
      "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_LEAVES_v1.json",
      "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_EXECUTION_LOG_v1.md"
    ],
    "runtime_owner_or_planning_owner": [
      "successor planning quartet and anti-drift control surfaces"
    ],
    "downstream_consumer_or_control_surface": [
      "gate sequencing",
      "closeout integrity proofs",
      "Codex and operator routing behaviour"
    ],
    "evidence_anchor": [
      "PLANS.md",
      "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md",
      "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_LEAVES_v1.json",
      "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_EXECUTION_LOG_v1.md",
      "tests/test_planning_state_integrity.py",
      "tests/test_successor_pack_anti_drift.py"
    ],
    "disagreement_state": "no_disagreement_recorded",
    "rejected_interpretation_ids": [],
    "rejection_or_deferral_reason": "none",
    "missing_requirement": "none",
    "would_become_valid_if": "already supported by current evidence anchors",
    "next_action_pack": "Gate 221",
    "archive_destination": "not_applicable",
    "classification_not_execution_note": "Gate 220 freezes classification and next action only; no test move, deletion, rewrite, or runtime mutation is executed in this pack.",
    "notes": "These tests are already successor-native integrity guards and do not depend on closed source-repo receipts."
  },
  {
    "decision_id": "data_path_or_fixture__retained_reference_and_loader_surfaces",
    "source_test_family": "data_path_or_fixture",
    "member_test_count": 8,
    "member_tests": [
      "tests/test_api.py",
      "tests/test_context_scanner_contracts.py",
      "tests/test_db_seed.py",
      "tests/test_gate105_ingress_db_api.py",
      "tests/test_gate90_financial_calendar_reference_import.py",
      "tests/test_import_registry_and_mapping.py",
      "tests/test_module_registry_promotion.py",
      "tests/test_real_data_loader.py"
    ],
    "treatment_tags": [
      "successor_required",
      "fixture_and_loader_surface"
    ],
    "decision_outcome": "keep_as_is",
    "authoritative_inputs": [
      "docs/TESTING_AND_PROMOTION.md",
      "fixtures/",
      "config/",
      "data/",
      "docs/reference/",
      "src/ import and loader services"
    ],
    "runtime_owner_or_planning_owner": [
      "ingress and import services",
      "reference-data loaders",
      "fixture-bearing support surfaces"
    ],
    "downstream_consumer_or_control_surface": [
      "runtime snapshots and import adapters",
      "fixture-backed runtime and planning tests",
      "reference-data refresh flows"
    ],
    "evidence_anchor": [
      "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_RETAINED_SURFACE_MANIFEST_AND_CUTOVER_RULES_v1.md",
      "tests/test_api.py",
      "tests/test_gate90_financial_calendar_reference_import.py",
      "tests/test_real_data_loader.py"
    ],
    "disagreement_state": "no_disagreement_recorded",
    "rejected_interpretation_ids": [],
    "rejection_or_deferral_reason": "none",
    "missing_requirement": "none",
    "would_become_valid_if": "already supported by current evidence anchors",
    "next_action_pack": "Gate 221",
    "archive_destination": "not_applicable",
    "classification_not_execution_note": "Gate 220 freezes classification and next action only; no test move, deletion, rewrite, or runtime mutation is executed in this pack.",
    "notes": "The retained fixture and loader seams are repo-native in the slim successor, so this family remains live without archival deferral."
  },
  {
    "decision_id": "invariant_or_lawful_output__repo_native_law_and_ownership",
    "source_test_family": "invariant_or_lawful_output",
    "member_test_count": 38,
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
    ],
    "treatment_tags": [
      "successor_required",
      "runtime_authority_retarget"
    ],
    "decision_outcome": "keep_but_retarget_authority",
    "authoritative_inputs": [
      "docs/01_NORMATIVE.md",
      "docs/03_DOMAIN_MODEL.md",
      "docs/05_GUARDRAILS.md",
      "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md",
      "live runtime service and schema surfaces under src/"
    ],
    "runtime_owner_or_planning_owner": [
      "stage and workflow owners named by current doctrine",
      "lawful output and ownership surfaces that downstream consumers rely on"
    ],
    "downstream_consumer_or_control_surface": [
      "downstream stage evaluators",
      "review packets",
      "ownership and consequence readers"
    ],
    "evidence_anchor": [
      "docs/03_DOMAIN_MODEL.md",
      "docs/05_GUARDRAILS.md",
      "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md",
      "tests/test_gate151_field_level_ownership_and_consumer_migration.py",
      "tests/test_gate155_downstream_consequence_routing_and_successor_boundary.py"
    ],
    "disagreement_state": "no_disagreement_recorded",
    "rejected_interpretation_ids": [],
    "rejection_or_deferral_reason": "none",
    "missing_requirement": "none",
    "would_become_valid_if": "already supported by current evidence anchors",
    "next_action_pack": "Gate 221",
    "archive_destination": "not_applicable",
    "classification_not_execution_note": "Gate 220 freezes classification and next action only; no test move, deletion, rewrite, or runtime mutation is executed in this pack.",
    "notes": "The tests remain live, but the governing ownership authority is the successor doctrine stack and adopted runtime ledger, not historical pack wording."
  },
  {
    "decision_id": "planning_governance__live_successor_process_controls",
    "source_test_family": "planning_governance",
    "member_test_count": 6,
    "member_tests": [
      "tests/test_execution_planning_contracts.py",
      "tests/test_gate107_repo_process_governance.py",
      "tests/test_gate109_template_pack_governance.py",
      "tests/test_gate111_governance_guardrails.py",
      "tests/test_gate209_planning_tree_and_evidence_taxonomy.py",
      "tests/test_tranche_briefing_template_pack.py"
    ],
    "treatment_tags": [
      "successor_required",
      "live_planning_control"
    ],
    "decision_outcome": "keep_as_is",
    "authoritative_inputs": [
      "docs/01_NORMATIVE.md",
      "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md",
      "PLANS.md",
      "active planning pack surfaces under docs/planning/"
    ],
    "runtime_owner_or_planning_owner": [
      "planning pack authorship surfaces",
      "repo governance doctrine"
    ],
    "downstream_consumer_or_control_surface": [
      "planning authors",
      "routing and approval workflow",
      "active pack integrity checks"
    ],
    "evidence_anchor": [
      "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md",
      "PLANS.md",
      "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md",
      "tests/test_gate107_repo_process_governance.py",
      "tests/test_gate111_governance_guardrails.py"
    ],
    "disagreement_state": "no_disagreement_recorded",
    "rejected_interpretation_ids": [],
    "rejection_or_deferral_reason": "none",
    "missing_requirement": "none",
    "would_become_valid_if": "already supported by current evidence anchors",
    "next_action_pack": "Gate 221",
    "archive_destination": "not_applicable",
    "classification_not_execution_note": "Gate 220 freezes classification and next action only; no test move, deletion, rewrite, or runtime mutation is executed in this pack.",
    "notes": "These rows still police live successor governance and routing behaviour directly."
  },
  {
    "decision_id": "planning_governance__closed_source_or_historical_pack_receipts",
    "source_test_family": "planning_governance",
    "member_test_count": 29,
    "member_tests": [
      "tests/test_financial_calendar_planning_v3.py",
      "tests/test_gate101_successor_planning.py",
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
      "tests/test_gate46_50_planning_pack.py",
      "tests/test_gate50_vocabulary_governance.py",
      "tests/test_gate51_cognitive_workflow_planning.py",
      "tests/test_gate55_vocabulary_governance.py",
      "tests/test_gate64_candidate_adjudication_governance.py",
      "tests/test_gate94_testing_module_planning.py",
      "tests/test_planning_ready_import_backlog_partition.py"
    ],
    "treatment_tags": [
      "archive_only",
      "stale_planning"
    ],
    "decision_outcome": "move_to_archive_evidence_repo",
    "authoritative_inputs": [
      "docs/01_NORMATIVE.md",
      "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md",
      "PLANS.md",
      "active planning pack surfaces under docs/planning/"
    ],
    "runtime_owner_or_planning_owner": [
      "planning pack authorship surfaces",
      "repo governance doctrine"
    ],
    "downstream_consumer_or_control_surface": [
      "planning authors",
      "routing and approval workflow",
      "active pack integrity checks"
    ],
    "evidence_anchor": [
      "docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_GATES_v1.md",
      "docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_EXECUTION_LOG_v1.md",
      "tests/test_gate200_target_repo_admitted_evidence_successor_pack_planning.py",
      "tests/test_gate204_target_repo_dmp_failure_pack_planning.py"
    ],
    "disagreement_state": "resolved_with_memory",
    "rejected_interpretation_ids": [
      "keep_all_historical_planning_tests_in_successor_repo"
    ],
    "rejection_or_deferral_reason": "Historical pack-specific planning receipts remain valuable evidence but no longer govern the slim successor as live controls.",
    "missing_requirement": "none",
    "would_become_valid_if": "move would become executable once the archive/evidence repo receives the mirrored retained planning receipt set and destination path is confirmed",
    "next_action_pack": "Gate 221",
    "archive_destination": "archive_repo_only",
    "classification_not_execution_note": "Gate 220 freezes classification and next action only; no test move, deletion, rewrite, or runtime mutation is executed in this pack.",
    "notes": "These tests are preserved as evidence-bearing archive candidates only; they are not deleted or moved in Gate 220."
  },
  {
    "decision_id": "replay_regression__canonical_replay_compare_guards",
    "source_test_family": "replay_regression",
    "member_test_count": 2,
    "member_tests": [
      "tests/test_gate127_replay_coefficient_visibility.py",
      "tests/test_replay_compare_runtime.py"
    ],
    "treatment_tags": [
      "successor_required",
      "runtime_authority_retarget"
    ],
    "decision_outcome": "keep_but_retarget_authority",
    "authoritative_inputs": [
      "docs/TESTING_AND_PROMOTION.md",
      "replay and compare services under src/",
      "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md when replay reads preserved ownership seams"
    ],
    "runtime_owner_or_planning_owner": [
      "replay and regression-comparison services"
    ],
    "downstream_consumer_or_control_surface": [
      "replay operators",
      "regression audits",
      "historical comparison workflows"
    ],
    "evidence_anchor": [
      "docs/TESTING_AND_PROMOTION.md",
      "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md",
      "tests/test_gate127_replay_coefficient_visibility.py",
      "tests/test_replay_compare_runtime.py"
    ],
    "disagreement_state": "no_disagreement_recorded",
    "rejected_interpretation_ids": [],
    "rejection_or_deferral_reason": "none",
    "missing_requirement": "none",
    "would_become_valid_if": "already supported by current evidence anchors",
    "next_action_pack": "Gate 221",
    "archive_destination": "not_applicable",
    "classification_not_execution_note": "Gate 220 freezes classification and next action only; no test move, deletion, rewrite, or runtime mutation is executed in this pack.",
    "notes": "Canonical replay compare coverage remains successor-required once anchored to the adopted runtime ledger and current replay services."
  },
  {
    "decision_id": "replay_regression__research_shadow_replays",
    "source_test_family": "replay_regression",
    "member_test_count": 2,
    "member_tests": [
      "tests/test_research_eval_replay.py",
      "tests/test_research_replay.py"
    ],
    "treatment_tags": [
      "duplicate",
      "research_shadow_surface"
    ],
    "decision_outcome": "retire_duplicate",
    "authoritative_inputs": [
      "docs/TESTING_AND_PROMOTION.md",
      "replay and compare services under src/",
      "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md when replay reads preserved ownership seams"
    ],
    "runtime_owner_or_planning_owner": [
      "replay and regression-comparison services"
    ],
    "downstream_consumer_or_control_surface": [
      "replay operators",
      "regression audits",
      "historical comparison workflows"
    ],
    "evidence_anchor": [
      "tests/test_research_eval_replay.py",
      "tests/test_research_replay.py",
      "docs/TESTING_AND_PROMOTION.md",
      "tests/test_replay_compare_runtime.py"
    ],
    "disagreement_state": "resolved_with_memory",
    "rejected_interpretation_ids": [
      "keep_research_shadow_replays_as_parallel_runtime_guards"
    ],
    "rejection_or_deferral_reason": "The research shadow replays do not add a distinct governed bug surface beyond the retained canonical replay compare guards.",
    "missing_requirement": "none",
    "would_become_valid_if": "retirement would become executable once a later pack deletes or archives the redundant research-shadow rows with the same canonical replay coverage still present",
    "next_action_pack": "Gate 221",
    "archive_destination": "not_applicable",
    "classification_not_execution_note": "Gate 220 freezes classification and next action only; no test move, deletion, rewrite, or runtime mutation is executed in this pack.",
    "notes": "Gate 220 freezes the duplicate judgment only; execution is deferred to the next pack."
  },
  {
    "decision_id": "review_or_trace__runtime_review_and_trace_surfaces",
    "source_test_family": "review_or_trace",
    "member_test_count": 18,
    "member_tests": [
      "tests/test_carry_review_cli_and_legacy.py",
      "tests/test_dmp_review_trace.py",
      "tests/test_execution_review_runtime.py",
      "tests/test_gate125_review_visible_lineage.py",
      "tests/test_gate132_bounded_trace_scenario_pack.py",
      "tests/test_gate133_bounded_trace_review_regime.py",
      "tests/test_gate134_bounded_trace_reporting.py",
      "tests/test_gate148_review_trace_replay_runtime.py",
      "tests/test_gate168_review_observability_chain_strengthening.py",
      "tests/test_gate177_parallel_risk_anti_duplication_and_review_integration.py",
      "tests/test_gate38_review_ledger_attribution_spine_contracts.py",
      "tests/test_gate39_review_overlays_feedback_chain_contracts.py",
      "tests/test_gate63_review_eligibility_governance.py",
      "tests/test_gate77_review_failure_taxonomy.py",
      "tests/test_gate82_review_surface_runtime_emission.py",
      "tests/test_gate83_review_governance_surface_builders.py",
      "tests/test_review_attribution_contracts.py",
      "tests/test_tranche_a_review_replay.py"
    ],
    "treatment_tags": [
      "successor_required",
      "runtime_authority_retarget"
    ],
    "decision_outcome": "keep_but_retarget_authority",
    "authoritative_inputs": [
      "docs/03_DOMAIN_MODEL.md",
      "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md",
      "review and trace schemas and services under src/",
      "docs/TESTING_AND_PROMOTION.md"
    ],
    "runtime_owner_or_planning_owner": [
      "review explanation and trace surfaces",
      "bounded-trace and attribution surfaces"
    ],
    "downstream_consumer_or_control_surface": [
      "review packets",
      "trace readers",
      "bounded-trace and explanation consumers"
    ],
    "evidence_anchor": [
      "docs/03_DOMAIN_MODEL.md",
      "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md",
      "tests/test_execution_review_runtime.py",
      "tests/test_gate148_review_trace_replay_runtime.py"
    ],
    "disagreement_state": "no_disagreement_recorded",
    "rejected_interpretation_ids": [],
    "rejection_or_deferral_reason": "none",
    "missing_requirement": "none",
    "would_become_valid_if": "already supported by current evidence anchors",
    "next_action_pack": "Gate 221",
    "archive_destination": "not_applicable",
    "classification_not_execution_note": "Gate 220 freezes classification and next action only; no test move, deletion, rewrite, or runtime mutation is executed in this pack.",
    "notes": "These review and trace tests remain live because they still police repo-native bounded-trace and explanation surfaces."
  },
  {
    "decision_id": "review_or_trace__historical_planning_review_receipts",
    "source_test_family": "review_or_trace",
    "member_test_count": 3,
    "member_tests": [
      "tests/test_gate148_review_trace_replay_planning.py",
      "tests/test_gate181_options_trace_integrity_pack_planning.py",
      "tests/test_gate202_target_repo_review_governance_planning.py"
    ],
    "treatment_tags": [
      "archive_only",
      "stale_planning"
    ],
    "decision_outcome": "move_to_archive_evidence_repo",
    "authoritative_inputs": [
      "docs/03_DOMAIN_MODEL.md",
      "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md",
      "review and trace schemas and services under src/",
      "docs/TESTING_AND_PROMOTION.md"
    ],
    "runtime_owner_or_planning_owner": [
      "review explanation and trace surfaces",
      "bounded-trace and attribution surfaces"
    ],
    "downstream_consumer_or_control_surface": [
      "review packets",
      "trace readers",
      "bounded-trace and explanation consumers"
    ],
    "evidence_anchor": [
      "tests/test_gate148_review_trace_replay_planning.py",
      "tests/test_gate181_options_trace_integrity_pack_planning.py",
      "tests/test_gate202_target_repo_review_governance_planning.py",
      "docs/planning/2026-04-05_GATE202_TARGET_REPO_COVERAGE_REVIEW_AND_DISAGREEMENT_PLANNING.md"
    ],
    "disagreement_state": "resolved_with_memory",
    "rejected_interpretation_ids": [
      "keep_historical_planning_review_tests_as_live_successor_review_guards"
    ],
    "rejection_or_deferral_reason": "These tests freeze historical planning review receipts rather than current successor runtime review semantics.",
    "missing_requirement": "none",
    "would_become_valid_if": "move would become executable once the archive/evidence repo path is confirmed and the evidence copy is preserved there",
    "next_action_pack": "Gate 221",
    "archive_destination": "archive_repo_only",
    "classification_not_execution_note": "Gate 220 freezes classification and next action only; no test move, deletion, rewrite, or runtime mutation is executed in this pack.",
    "notes": "The historical planning review guards stay visible in the register but are no longer treated as live successor controls."
  },
  {
    "decision_id": "repo_hygiene__retained_repo_boundary_surfaces",
    "source_test_family": "repo_hygiene",
    "member_test_count": 4,
    "member_tests": [
      "tests/test_boundaries_and_config_surface.py",
      "tests/test_document_hygiene.py",
      "tests/test_fixtures_and_config.py",
      "tests/test_gate179_repo_wide_vocabulary_hygiene.py"
    ],
    "treatment_tags": [
      "successor_required",
      "repo_boundary"
    ],
    "decision_outcome": "keep_as_is",
    "authoritative_inputs": [
      "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md",
      "README.md",
      "AGENTS.md",
      "config/",
      "fixtures/"
    ],
    "runtime_owner_or_planning_owner": [
      "repo hygiene and configuration boundary surfaces"
    ],
    "downstream_consumer_or_control_surface": [
      "maintainers",
      "tooling and environment discipline",
      "documentation and config boundary checks"
    ],
    "evidence_anchor": [
      "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md",
      "AGENTS.md",
      "tests/test_document_hygiene.py",
      "tests/test_boundaries_and_config_surface.py"
    ],
    "disagreement_state": "no_disagreement_recorded",
    "rejected_interpretation_ids": [],
    "rejection_or_deferral_reason": "none",
    "missing_requirement": "none",
    "would_become_valid_if": "already supported by current evidence anchors",
    "next_action_pack": "Gate 221",
    "archive_destination": "not_applicable",
    "classification_not_execution_note": "Gate 220 freezes classification and next action only; no test move, deletion, rewrite, or runtime mutation is executed in this pack.",
    "notes": "The successor repo still relies on these repo-boundary and config-hygiene guards directly."
  },
  {
    "decision_id": "runtime_contract__current_packet_and_service_contracts",
    "source_test_family": "runtime_contract",
    "member_test_count": 44,
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
    ],
    "treatment_tags": [
      "successor_required",
      "runtime_authority_retarget"
    ],
    "decision_outcome": "keep_but_retarget_authority",
    "authoritative_inputs": [
      "docs/03_DOMAIN_MODEL.md",
      "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md when ownership or compatibility carriage is involved",
      "live schemas and services under src/"
    ],
    "runtime_owner_or_planning_owner": [
      "runtime schema owners",
      "stage and workflow packet owners"
    ],
    "downstream_consumer_or_control_surface": [
      "runtime producers and readers",
      "review and replay consumers of preserved contracts"
    ],
    "evidence_anchor": [
      "docs/03_DOMAIN_MODEL.md",
      "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md",
      "tests/test_gate28_ingress_substrate_contracts.py",
      "tests/test_runtime_contract_registry.py"
    ],
    "disagreement_state": "no_disagreement_recorded",
    "rejected_interpretation_ids": [],
    "rejection_or_deferral_reason": "none",
    "missing_requirement": "none",
    "would_become_valid_if": "already supported by current evidence anchors",
    "next_action_pack": "Gate 221",
    "archive_destination": "not_applicable",
    "classification_not_execution_note": "Gate 220 freezes classification and next action only; no test move, deletion, rewrite, or runtime mutation is executed in this pack.",
    "notes": "The contract tests remain live, but their authority is the current repo-native runtime doctrine rather than source-era pack narratives."
  },
  {
    "decision_id": "runtime_scenario__retained_runtime_paths",
    "source_test_family": "runtime_scenario",
    "member_test_count": 40,
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
    ],
    "treatment_tags": [
      "successor_required",
      "runtime_path"
    ],
    "decision_outcome": "keep_as_is",
    "authoritative_inputs": [
      "docs/03_DOMAIN_MODEL.md",
      "docs/TESTING_AND_PROMOTION.md",
      "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md when scenario assertions depend on ownership or seam law",
      "live service implementations under src/"
    ],
    "runtime_owner_or_planning_owner": [
      "runtime service implementations",
      "scenario-level stage integrations"
    ],
    "downstream_consumer_or_control_surface": [
      "end-to-end runtime flows",
      "downstream stage consumers",
      "integration review paths"
    ],
    "evidence_anchor": [
      "docs/03_DOMAIN_MODEL.md",
      "docs/TESTING_AND_PROMOTION.md",
      "tests/test_gate96_canonical_runtime_harness.py",
      "tests/test_posture_risk_and_playbook.py"
    ],
    "disagreement_state": "no_disagreement_recorded",
    "rejected_interpretation_ids": [],
    "rejection_or_deferral_reason": "none",
    "missing_requirement": "none",
    "would_become_valid_if": "already supported by current evidence anchors",
    "next_action_pack": "Gate 221",
    "archive_destination": "not_applicable",
    "classification_not_execution_note": "Gate 220 freezes classification and next action only; no test move, deletion, rewrite, or runtime mutation is executed in this pack.",
    "notes": "The retained runtime scenario coverage still maps to repo-native services and downstream consumers without requiring archival treatment."
  },
  {
    "decision_id": "migration_or_closeout_guard__successor_cutover_boundary_rule",
    "source_test_family": "migration_or_closeout_guard",
    "member_test_count": 1,
    "member_tests": [
      "tests/test_gate210_operator_surface_alignment_and_cutover.py"
    ],
    "treatment_tags": [
      "successor_required",
      "successor_boundary_rewrite"
    ],
    "decision_outcome": "rewrite_for_successor_truth",
    "authoritative_inputs": [
      "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md",
      "PLANS.md",
      "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md",
      "retained execution logs and closeout surfaces"
    ],
    "runtime_owner_or_planning_owner": [
      "historical pack closeout surfaces",
      "migration and cutover router surfaces"
    ],
    "downstream_consumer_or_control_surface": [
      "closeout truth checks",
      "archive versus successor boundary checks",
      "later planning-pack reconciliation work"
    ],
    "evidence_anchor": [
      "docs/planning/2026-04-06_GATE210_SLIM_ACTIVE_REPO_CUTOVER_ENTRY_CRITERIA.md",
      "tests/test_gate210_operator_surface_alignment_and_cutover.py",
      "PLANS.md"
    ],
    "disagreement_state": "resolved_with_memory",
    "rejected_interpretation_ids": [
      "keep_source_repo_cutover_assertions_verbatim_in_successor_repo"
    ],
    "rejection_or_deferral_reason": "The retained cutover-boundary test still checks a live successor seam, but its source-era assertions must be rewritten against successor-local truth surfaces before it can stay canonical.",
    "missing_requirement": "successor_local_cutover_assertions",
    "would_become_valid_if": "rewrite would become executable once the next pack authors successor-local assertions and removes source-repo-only wording",
    "next_action_pack": "Gate 221",
    "archive_destination": "not_applicable",
    "classification_not_execution_note": "Gate 220 freezes classification and next action only; no test move, deletion, rewrite, or runtime mutation is executed in this pack.",
    "notes": "Gate 220 freezes the rewrite requirement only; no rewrite is executed here."
  },
  {
    "decision_id": "migration_or_closeout_guard__historical_closeout_receipts",
    "source_test_family": "migration_or_closeout_guard",
    "member_test_count": 14,
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
      "tests/test_gate86_event_ingestion_precedence_and_closeout.py",
      "tests/test_gate95_phase0_closeout.py"
    ],
    "treatment_tags": [
      "archive_only",
      "stale_planning"
    ],
    "decision_outcome": "move_to_archive_evidence_repo",
    "authoritative_inputs": [
      "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md",
      "PLANS.md",
      "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md",
      "retained execution logs and closeout surfaces"
    ],
    "runtime_owner_or_planning_owner": [
      "historical pack closeout surfaces",
      "migration and cutover router surfaces"
    ],
    "downstream_consumer_or_control_surface": [
      "closeout truth checks",
      "archive versus successor boundary checks",
      "later planning-pack reconciliation work"
    ],
    "evidence_anchor": [
      "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md",
      "tests/test_gate191_capital_deployment_authority_closeout.py",
      "docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_EXECUTION_LOG_v1.md"
    ],
    "disagreement_state": "resolved_with_memory",
    "rejected_interpretation_ids": [
      "keep_historical_closeout_receipts_as_live_successor_tests"
    ],
    "rejection_or_deferral_reason": "These rows freeze historical closeout evidence and cutover history, not current successor runtime or routing truth.",
    "missing_requirement": "none",
    "would_become_valid_if": "move would become executable once the archive/evidence repo destination is confirmed and the preserved receipts are copied there",
    "next_action_pack": "Gate 221",
    "archive_destination": "archive_repo_only",
    "classification_not_execution_note": "Gate 220 freezes classification and next action only; no test move, deletion, rewrite, or runtime mutation is executed in this pack.",
    "notes": "The closeout evidence remains preserved but is classified as archive-only for later execution."
  }
]
```

## Gate 219 family doctrine and ownership mapping

```json
[
  {
    "test_id": "compatibility_wrapper",
    "bug_surface_class": "compatibility carriage and preserved read-shape wrapper drift",
    "testing_phase_alignment": "compatibility wrapper and downstream reader guard coverage",
    "authoritative_inputs": [
      "docs/TESTING_AND_PROMOTION.md",
      "docs/03_DOMAIN_MODEL.md",
      "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md"
    ],
    "runtime_owner_or_planning_owner": [
      "compatibility-wrapper surfaces that preserve older read shapes over newer canonical runtime truth"
    ],
    "downstream_consumer_or_control_surface": [
      "legacy-compatible API or reader paths",
      "session-clock compatibility consumers",
      "review and replay readers that still exercise preserved wrapper shapes"
    ],
    "current_truth_dependency": "The family remains truthful only while preserved compatibility wrappers remain subordinate to the canonical runtime owners named in docs/03 and docs/07.",
    "status_candidate": [
      "successor_required"
    ],
    "decision_outcome": "pending_gate_220_decision",
    "evidence_anchor": [
      "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md",
      "tests/test_gate49_temporal_compatibility.py",
      "tests/test_session_clock.py"
    ],
    "disagreement_state": "none_recorded_at_gate_219",
    "next_action_pack": "Gate 220",
    "notes": "No family-level orphan or duplicate signal is frozen yet; Gate 220 may still narrow coverage if wrapper guards overlap broader runtime-contract families."
  },
  {
    "test_id": "control_surface_integrity",
    "bug_surface_class": "router, gate-map, leaves-ledger, and execution-log coherence drift",
    "testing_phase_alignment": "planning control-surface integrity and anti-drift closeout coverage",
    "authoritative_inputs": [
      "docs/01_NORMATIVE.md",
      "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md",
      "PLANS.md",
      "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md",
      "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_LEAVES_v1.json",
      "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_EXECUTION_LOG_v1.md"
    ],
    "runtime_owner_or_planning_owner": [
      "successor planning quartet and anti-drift control surfaces"
    ],
    "downstream_consumer_or_control_surface": [
      "gate sequencing",
      "closeout integrity proofs",
      "Codex and operator routing behaviour"
    ],
    "current_truth_dependency": "These tests remain truthful only while the active successor planning quartet is the live routing authority for the slim repo.",
    "status_candidate": [
      "successor_required"
    ],
    "decision_outcome": "pending_gate_220_decision",
    "evidence_anchor": [
      "PLANS.md",
      "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md",
      "tests/test_planning_state_integrity.py",
      "tests/test_successor_pack_anti_drift.py"
    ],
    "disagreement_state": "none_recorded_at_gate_219",
    "next_action_pack": "Gate 220",
    "notes": "This family is the current slim-successor anti-drift spine and is therefore frozen as successor-required unless a later pack proves equivalent coverage elsewhere."
  },
  {
    "test_id": "data_path_or_fixture",
    "bug_surface_class": "fixture, import, reference-data, and ingress data-path drift",
    "testing_phase_alignment": "data-path and fixture integrity coverage",
    "authoritative_inputs": [
      "docs/TESTING_AND_PROMOTION.md",
      "fixtures/",
      "config/",
      "data/",
      "docs/reference/",
      "src/ import and loader services"
    ],
    "runtime_owner_or_planning_owner": [
      "ingress and import services",
      "reference-data loaders",
      "fixture-bearing support surfaces"
    ],
    "downstream_consumer_or_control_surface": [
      "runtime snapshots and import adapters",
      "fixture-backed runtime and planning tests",
      "reference-data refresh flows"
    ],
    "current_truth_dependency": "The family depends on the retained fixture tree and the successor repo's current import and loader seams remaining present and truthful.",
    "status_candidate": [
      "successor_required"
    ],
    "decision_outcome": "pending_gate_220_decision",
    "evidence_anchor": [
      "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_RETAINED_SURFACE_MANIFEST_AND_CUTOVER_RULES_v1.md",
      "tests/test_api.py",
      "tests/test_gate90_financial_calendar_reference_import.py",
      "tests/test_real_data_loader.py"
    ],
    "disagreement_state": "none_recorded_at_gate_219",
    "next_action_pack": "Gate 220",
    "notes": "No family-level orphan is frozen; Gate 220 may still split API/db ingress checks away from reference-data fixture guards if decision law needs narrower rows."
  },
  {
    "test_id": "invariant_or_lawful_output",
    "bug_surface_class": "lawful output, ownership, doctrine, and invariant drift",
    "testing_phase_alignment": "invariant or lawful-output coverage",
    "authoritative_inputs": [
      "docs/01_NORMATIVE.md",
      "docs/03_DOMAIN_MODEL.md",
      "docs/05_GUARDRAILS.md",
      "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md",
      "live runtime service and schema surfaces under src/"
    ],
    "runtime_owner_or_planning_owner": [
      "stage and workflow owners named by current doctrine",
      "lawful output and ownership surfaces that downstream consumers rely on"
    ],
    "downstream_consumer_or_control_surface": [
      "downstream stage evaluators",
      "review packets",
      "ownership and consequence readers"
    ],
    "current_truth_dependency": "This family depends on current repo-native lawful output and ownership doctrine rather than historical pack prose alone.",
    "status_candidate": [
      "successor_required",
      "duplicate_candidate"
    ],
    "decision_outcome": "pending_gate_220_decision",
    "evidence_anchor": [
      "docs/03_DOMAIN_MODEL.md",
      "docs/05_GUARDRAILS.md",
      "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md",
      "tests/test_gate151_field_level_ownership_and_consumer_migration.py",
      "tests/test_gate155_downstream_consequence_routing_and_successor_boundary.py"
    ],
    "disagreement_state": "none_recorded_at_gate_219",
    "next_action_pack": "Gate 220",
    "notes": "Family-level duplicate pressure is explicit because several law and ownership tests overlap adjacent runtime-contract and review families and may need row-splitting before a final keep or retire decision."
  },
  {
    "test_id": "migration_or_closeout_guard",
    "bug_surface_class": "historical closeout, migration, and cutover truth drift",
    "testing_phase_alignment": "migration or closeout guard coverage",
    "authoritative_inputs": [
      "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md",
      "PLANS.md",
      "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md",
      "retained execution logs and closeout surfaces"
    ],
    "runtime_owner_or_planning_owner": [
      "historical pack closeout surfaces",
      "migration and cutover router surfaces"
    ],
    "downstream_consumer_or_control_surface": [
      "closeout truth checks",
      "archive versus successor boundary checks",
      "later planning-pack reconciliation work"
    ],
    "current_truth_dependency": "These tests remain truthful only while the successor repo intentionally retains historical closeout evidence that later packs still consult.",
    "status_candidate": [
      "stale_planning_candidate",
      "orphan_candidate"
    ],
    "decision_outcome": "pending_gate_220_decision",
    "evidence_anchor": [
      "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md",
      "docs/planning/2026-04-06_GATE210_SLIM_ACTIVE_REPO_CUTOVER_ENTRY_CRITERIA.md",
      "tests/test_gate210_operator_surface_alignment_and_cutover.py",
      "tests/test_gate191_capital_deployment_authority_closeout.py"
    ],
    "disagreement_state": "none_recorded_at_gate_219",
    "next_action_pack": "Gate 220",
    "notes": "This family is the strongest archive-sensitive candidate set. Gate 220 must decide which rows remain successor-required and which should move back to archive evidence or be retired as stale planning guards."
  },
  {
    "test_id": "planning_governance",
    "bug_surface_class": "planning doctrine, pack governance, and active-pack authorship drift",
    "testing_phase_alignment": "planning-governance coverage",
    "authoritative_inputs": [
      "docs/01_NORMATIVE.md",
      "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md",
      "PLANS.md",
      "active planning pack surfaces under docs/planning/"
    ],
    "runtime_owner_or_planning_owner": [
      "planning pack authorship surfaces",
      "repo governance doctrine"
    ],
    "downstream_consumer_or_control_surface": [
      "planning authors",
      "routing and approval workflow",
      "active pack integrity checks"
    ],
    "current_truth_dependency": "The family depends on the successor repo's live planning router and active pack, not on source-repo pack state remembered from chat history.",
    "status_candidate": [
      "successor_required",
      "stale_planning_candidate",
      "orphan_candidate"
    ],
    "decision_outcome": "pending_gate_220_decision",
    "evidence_anchor": [
      "PLANS.md",
      "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md",
      "docs/planning/tranche_briefing_template_pack/",
      "tests/test_gate200_target_repo_admitted_evidence_successor_pack_planning.py",
      "tests/test_gate204_target_repo_dmp_failure_pack_planning.py"
    ],
    "disagreement_state": "none_recorded_at_gate_219",
    "next_action_pack": "Gate 220",
    "notes": "This family intentionally freezes both still-needed successor governance guards and likely stale source-era planning proofs. Gate 220 must split rows where successor-required and archive-only signals diverge."
  },
  {
    "test_id": "replay_regression",
    "bug_surface_class": "replay, historical comparison, and regression-detection drift",
    "testing_phase_alignment": "replay regression coverage",
    "authoritative_inputs": [
      "docs/TESTING_AND_PROMOTION.md",
      "replay and compare services under src/",
      "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md when replay reads preserved ownership seams"
    ],
    "runtime_owner_or_planning_owner": [
      "replay and regression-comparison services"
    ],
    "downstream_consumer_or_control_surface": [
      "replay operators",
      "regression audits",
      "historical comparison workflows"
    ],
    "current_truth_dependency": "Replay coverage remains truthful only while preserved seam ownership and replay compare contracts still match the successor runtime surfaces.",
    "status_candidate": [
      "successor_required",
      "duplicate_candidate"
    ],
    "decision_outcome": "pending_gate_220_decision",
    "evidence_anchor": [
      "docs/TESTING_AND_PROMOTION.md",
      "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md",
      "tests/test_replay_compare_runtime.py",
      "tests/test_research_replay.py"
    ],
    "disagreement_state": "none_recorded_at_gate_219",
    "next_action_pack": "Gate 220",
    "notes": "Duplicate pressure is explicit because some replay guards may overlap review-or-trace coverage once Gate 220 inspects exact bug surfaces row by row."
  },
  {
    "test_id": "repo_hygiene",
    "bug_surface_class": "repo hygiene, config boundary, and documentation surface drift",
    "testing_phase_alignment": "repo hygiene coverage",
    "authoritative_inputs": [
      "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md",
      "README.md",
      "AGENTS.md",
      "config/",
      "fixtures/"
    ],
    "runtime_owner_or_planning_owner": [
      "repo hygiene and configuration boundary surfaces"
    ],
    "downstream_consumer_or_control_surface": [
      "maintainers",
      "tooling and environment discipline",
      "documentation and config boundary checks"
    ],
    "current_truth_dependency": "The family depends on the successor repo continuing to retain its current configuration and documentation boundary surfaces.",
    "status_candidate": [
      "successor_required"
    ],
    "decision_outcome": "pending_gate_220_decision",
    "evidence_anchor": [
      "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md",
      "AGENTS.md",
      "tests/test_document_hygiene.py",
      "tests/test_boundaries_and_config_surface.py"
    ],
    "disagreement_state": "none_recorded_at_gate_219",
    "next_action_pack": "Gate 220",
    "notes": "No family-level orphan or stale-planning signal is frozen at Gate 219."
  },
  {
    "test_id": "review_or_trace",
    "bug_surface_class": "review packet, trace, attribution, and bounded-trace reader drift",
    "testing_phase_alignment": "review or trace coverage",
    "authoritative_inputs": [
      "docs/03_DOMAIN_MODEL.md",
      "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md",
      "review and trace schemas and services under src/",
      "docs/TESTING_AND_PROMOTION.md"
    ],
    "runtime_owner_or_planning_owner": [
      "review explanation and trace surfaces",
      "bounded-trace and attribution surfaces"
    ],
    "downstream_consumer_or_control_surface": [
      "review packets",
      "trace readers",
      "bounded-trace and explanation consumers"
    ],
    "current_truth_dependency": "This family depends on the successor repo still carrying the preserved review and trace seams named by docs/03 and docs/07.",
    "status_candidate": [
      "successor_required",
      "duplicate_candidate",
      "stale_planning_candidate"
    ],
    "decision_outcome": "pending_gate_220_decision",
    "evidence_anchor": [
      "docs/03_DOMAIN_MODEL.md",
      "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md",
      "tests/test_execution_review_runtime.py",
      "tests/test_gate148_review_trace_replay_runtime.py"
    ],
    "disagreement_state": "none_recorded_at_gate_219",
    "next_action_pack": "Gate 220",
    "notes": "Family-level duplicate pressure is explicit, and a small stale-planning signal is also visible because some retained review-governance tests still anchor to older planning-control assumptions."
  },
  {
    "test_id": "runtime_contract",
    "bug_surface_class": "runtime schema, packet, and service contract drift",
    "testing_phase_alignment": "runtime contract coverage",
    "authoritative_inputs": [
      "docs/03_DOMAIN_MODEL.md",
      "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md when ownership or compatibility carriage is involved",
      "live schemas and services under src/"
    ],
    "runtime_owner_or_planning_owner": [
      "runtime schema owners",
      "stage and workflow packet owners"
    ],
    "downstream_consumer_or_control_surface": [
      "runtime producers and readers",
      "review and replay consumers of preserved contracts"
    ],
    "current_truth_dependency": "This family is governed by the current runtime contracts actually shipped in the slim successor repo, not by historical pack intent alone.",
    "status_candidate": [
      "successor_required",
      "duplicate_candidate"
    ],
    "decision_outcome": "pending_gate_220_decision",
    "evidence_anchor": [
      "docs/03_DOMAIN_MODEL.md",
      "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md",
      "tests/test_gate28_ingress_substrate_contracts.py",
      "tests/test_runtime_contract_registry.py"
    ],
    "disagreement_state": "none_recorded_at_gate_219",
    "next_action_pack": "Gate 220",
    "notes": "Duplicate pressure is explicit because several narrow gate-local contract guards overlap broader registry and contract-registry coverage."
  },
  {
    "test_id": "runtime_scenario",
    "bug_surface_class": "runtime semantic, integration, and scenario-path drift",
    "testing_phase_alignment": "runtime scenario coverage",
    "authoritative_inputs": [
      "docs/03_DOMAIN_MODEL.md",
      "docs/TESTING_AND_PROMOTION.md",
      "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md when scenario assertions depend on ownership or seam law",
      "live service implementations under src/"
    ],
    "runtime_owner_or_planning_owner": [
      "runtime service implementations",
      "scenario-level stage integrations"
    ],
    "downstream_consumer_or_control_surface": [
      "end-to-end runtime flows",
      "downstream stage consumers",
      "integration review paths"
    ],
    "current_truth_dependency": "Scenario coverage is truthful only while the current runtime implementations and their preserved downstream seams match the retained doctrine surfaces.",
    "status_candidate": [
      "successor_required",
      "duplicate_candidate"
    ],
    "decision_outcome": "pending_gate_220_decision",
    "evidence_anchor": [
      "docs/03_DOMAIN_MODEL.md",
      "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md",
      "tests/test_gate96_canonical_runtime_harness.py",
      "tests/test_posture_risk_and_playbook.py"
    ],
    "disagreement_state": "none_recorded_at_gate_219",
    "next_action_pack": "Gate 220",
    "notes": "Family-level duplicate pressure is explicit because some gate-local scenario tests may later collapse into broader runtime harness or integration rows."
  }
]
```
