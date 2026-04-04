# 2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_EVIDENCE_BASELINE_v1

## Purpose

Freeze the executed external evidence baseline that this repo-native Phase 3 pack is allowed to consume.

## External evidence summary carried into the target-repo planning pack

The external Phase 2B audit reported the following main-target defect families:

1. vocabulary generator drift with 19 executed failures
2. runtime-harness options-flow behaviour drift with 2 executed failures
3. higher-order context stress-behaviour drift with 1 executed failure
4. control-surface router and gate-map drift with 16 executed failures
5. repo-wide vocabulary hygiene leakage with 1 executed failure
6. `ruff` import-structure and formatting debt with 103 findings
7. concentrated financial-calendar typing seam with 68 type errors inside one dominant file cluster
8. broad untyped-helper pressure across strict test contexts
9. Alembic `path_separator` warning-only suspicious pass

## Repair-family normalisation adopted for this pack

The target repo will treat the executed baseline as seven repair tranches:
- vocabulary generator reconciliation
- vocabulary hygiene leakage reconciliation
- control-surface router and gate-map reconciliation
- runtime semantic drift reconciliation
- financial-calendar typing seam reconciliation
- typed helper pressure reduction
- static hygiene and warning cleanup

## Rule

This note is evidence input only.
It does not replace repo-native gate, leaf, or execution-log authority.
Execution must still close each gate with repo-local proofs.


## Exact evidence anchors carried into leaf planning

- Vocabulary generator drift: failing tests include `tests/test_gate50_vocabulary_governance.py`, `tests/test_gate55_vocabulary_governance.py`, `tests/test_gate60_state_policy_ontology.py`, `tests/test_gate63_review_eligibility_governance.py`, `tests/test_gate67_event_window_semantics.py`, `tests/test_gate78_modifier_runtime_integration.py`, and `tests/test_gate89_financial_calendar_crosswalk_and_dmp_lane.py`; source seam is `scripts/build_canonical_vocabulary.py` versus the committed vocabulary JSON.
- Runtime-harness behaviour drift: exact failing tests are `tests/test_gate96_canonical_runtime_harness.py` and `tests/test_gate102_raw_runtime_harness.py`; adjacent truth surfaces include `tests/test_real_data_loader.py` and `tests/test_options_flow_context.py`; primary runtime seam is `src/nvda_desk/services/options_flow_context.py`.
- Higher-order context stress drift: exact failing test is `tests/test_gate31_higher_order_context_composites.py`; primary runtime seam is `src/nvda_desk/services/imported_modules/posture_enrichers.py`.
- Control-surface router/gate-map drift: exact failing tests span `tests/test_gate149_stage_local_handoff_pack_closeout.py`, `tests/test_gate150_corrective_successor_pack_planning.py`, `tests/test_gate151_field_level_ownership_and_consumer_migration.py`, `tests/test_gate152_stage5_stage6_authority_replan.py`, `tests/test_gate153_overlay_terminal_final_join_authority_replan.py`, `tests/test_gate154_downstream_consumer_reconciliation_replan.py`, `tests/test_gate155_downstream_consequence_routing_and_successor_boundary.py`, `tests/test_gate156_corrective_pack_anti_drift_closeout.py`, `tests/test_gate163_coefficient_architecture_consolidation_closeout.py`, `tests/test_gate164_policy_temporal_observability_successor_pack_planning.py`, `tests/test_gate165_lean_policy_law_externalisation.py`, `tests/test_gate170_policy_temporal_observability_successor_closeout.py`, `tests/test_gate171_master_child_parallel_risk_integration_pack_planning.py`, `tests/test_gate172_master_child_lineage_and_overlap_ledger.py`, `tests/test_gate180_master_child_integration_closeout.py`, and `tests/test_gate181_options_trace_integrity_pack_planning.py`.
- Financial-calendar typing seam: dominant source file is `src/nvda_desk/schemas/financial_calendar.py`; adjacent code is `src/nvda_desk/services/financial_calendar_projection.py`; adjacent proof surfaces include tests `89-92` and `tests/test_financial_calendar_planning_v3.py`.
- Helper typing pressure: highest-concentration tests named by Phase 2B are `tests/test_gate97_runtime_invariants.py`, `tests/test_gate103_raw_prepared_parity.py`, and `tests/test_gate104_property_stateful.py`.
- Static hygiene and warning cleanup: dominant `ruff` surfaces are Alembic modules/migrations, repo-root path insertion in tests, and `src/nvda_desk/config_models.py`; warning-only surface is `alembic.ini`.
