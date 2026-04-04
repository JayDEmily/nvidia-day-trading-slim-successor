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
It is paired with `docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_SOURCE_TRUTH_MATRIX_v1.md`, which records the raw-code-first authority surfaces for each repair family.


## Exact evidence anchors carried into leaf planning

- Vocabulary generator drift:
  - primary source surfaces: `scripts/build_canonical_vocabulary.py::build_document`, `src/nvda_desk/schemas/vocabulary.py::{VocabularyEntry,VocabularyDocument}`, `src/nvda_desk/services/playbook_registry.py::{document,ordered_setup_variants,template_index}`, and `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`
  - secondary evidence tests: `tests/test_gate50_vocabulary_governance.py`, `tests/test_gate55_vocabulary_governance.py`, `tests/test_gate60_state_policy_ontology.py`, `tests/test_gate63_review_eligibility_governance.py`, `tests/test_gate67_event_window_semantics.py`, `tests/test_gate78_modifier_runtime_integration.py`, `tests/test_gate89_financial_calendar_crosswalk_and_dmp_lane.py`
- Runtime-harness behaviour drift:
  - primary source surfaces: `src/nvda_desk/services/options_flow_context.py::{_surface_anchor_state,_options_behavior_cluster}`, `src/nvda_desk/schemas/cognition.py::OptionsFlowContextOutput`, and `src/nvda_desk/services/playbook_eligibility.py::_skew_pressure_reversal`
  - secondary evidence tests: `tests/test_gate96_canonical_runtime_harness.py`, `tests/test_gate102_raw_runtime_harness.py`; adjacent evidence: `tests/test_real_data_loader.py`, `tests/test_options_flow_context.py`
- Higher-order context stress drift:
  - primary source surfaces: `src/nvda_desk/services/imported_modules/posture_enrichers.py::_compression_regime_detector` and its emitted contract output
  - secondary evidence test: `tests/test_gate31_higher_order_context_composites.py`
- Control-surface router/gate-map drift:
  - primary source surfaces: repo-root `PLANS.md`, `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`, `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`, and the exact late-pack planning docs/receipts/logs implicated by the executed drift
  - secondary evidence tests span `tests/test_gate149_stage_local_handoff_pack_closeout.py`, `tests/test_gate150_corrective_successor_pack_planning.py`, `tests/test_gate151_field_level_ownership_and_consumer_migration.py`, `tests/test_gate152_stage5_stage6_authority_replan.py`, `tests/test_gate153_overlay_terminal_final_join_authority_replan.py`, `tests/test_gate154_downstream_consumer_reconciliation_replan.py`, `tests/test_gate155_downstream_consequence_routing_and_successor_boundary.py`, `tests/test_gate156_corrective_pack_anti_drift_closeout.py`, `tests/test_gate163_coefficient_architecture_consolidation_closeout.py`, `tests/test_gate164_policy_temporal_observability_successor_pack_planning.py`, `tests/test_gate165_lean_policy_law_externalisation.py`, `tests/test_gate170_policy_temporal_observability_successor_closeout.py`, `tests/test_gate171_master_child_parallel_risk_integration_pack_planning.py`, `tests/test_gate172_master_child_lineage_and_overlap_ledger.py`, `tests/test_gate180_master_child_integration_closeout.py`, and `tests/test_gate181_options_trace_integrity_pack_planning.py`
- Residual vocabulary hygiene leakage:
  - primary source surfaces: the lane/workbook entries in `scripts/build_canonical_vocabulary.py`, the committed vocabulary artifact, `src/nvda_desk/schemas/cognition.py::{CapitalDeploymentAuthorityDecision,ReviewExplanationOutput}`, `src/nvda_desk/services/capital_deployment_authority.py`, `src/nvda_desk/services/cognition_runtime.py`, and `src/nvda_desk/services/review_explanation.py`
  - secondary evidence tests: `tests/test_gate179_repo_wide_vocabulary_hygiene.py`, `tests/test_gate190_capital_deployment_authority_integration.py`
- Financial-calendar typing seam:
  - primary source surfaces: `src/nvda_desk/schemas/financial_calendar.py::{FinancialCalendarCrosswalkRecord,default_financial_calendar_crosswalk}` and `src/nvda_desk/services/financial_calendar_projection.py::{_match_crosswalk,_event_window_datetimes}`
  - secondary evidence tests: tests `89-92` and `tests/test_financial_calendar_planning_v3.py`
- Helper typing pressure:
  - primary source surfaces: `tests/contract_chain_fixtures.py` and `tests/_successor_pack_helpers.py` plus any directly coupled helper module proven necessary during execution
  - secondary evidence tests: `tests/test_gate97_runtime_invariants.py`, `tests/test_gate103_raw_prepared_parity.py`, `tests/test_gate104_property_stateful.py`
- Static hygiene and warning cleanup:
  - primary source surfaces: `alembic/env.py`, `alembic.ini`, the exact Alembic/migration files named by lint output, repo-root path insertion test files, and `src/nvda_desk/config_models.py`
  - secondary evidence tools: `ruff check .`, `mypy src tests`, warning-only parity receipts

## Source-truth precedence

If a failing test and a source module disagree, the leaf must first adjudicate the code/contracts/docs named above. Only after that decision may the test be changed or retained.
