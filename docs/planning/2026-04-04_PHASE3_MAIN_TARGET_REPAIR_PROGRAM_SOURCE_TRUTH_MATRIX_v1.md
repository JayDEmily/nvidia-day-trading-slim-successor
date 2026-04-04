# 2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_SOURCE_TRUTH_MATRIX_v1

## Purpose

This matrix freezes the **source-truth-first** interpretation for every Phase 3 repair family.
Tests remain execution evidence, but they are not allowed to outrank the repo's raw code, typed contracts, or governing docs when Phase 3 adjudicates what is actually lawful.

## Rule

For every Phase 3 repair gate:
- inspect the named source modules and governing docs first;
- use failing tests as evidence of drift, not as automatic authority;
- change downstream expectations only after the source-truth decision is written.

## Family matrix

| Phase 3 tranche | Primary source-truth surfaces | Secondary evidence surfaces | Why source truth leads |
|---|---|---|---|
| P3-T01 vocabulary generator reconciliation | `scripts/build_canonical_vocabulary.py::build_document`; `src/nvda_desk/schemas/vocabulary.py::{VocabularyEntry,VocabularyDocument}`; `src/nvda_desk/services/playbook_registry.py::{document,ordered_setup_variants,template_index}`; `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json` | gate `50-89` vocabulary-governance tests including `tests/test_gate50_vocabulary_governance.py`, `tests/test_gate55_vocabulary_governance.py`, `tests/test_gate60_state_policy_ontology.py`, `tests/test_gate67_event_window_semantics.py`, `tests/test_gate78_modifier_runtime_integration.py`, `tests/test_gate89_financial_calendar_crosswalk_and_dmp_lane.py` | The generator and vocabulary schema define what the committed artifact is supposed to contain; tests only detect drift from that truth. |
| P3-T02 vocabulary hygiene leakage reconciliation | `scripts/build_canonical_vocabulary.py` lane/workbook entries; `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`; `src/nvda_desk/schemas/cognition.py::{CapitalDeploymentAuthorityDecision,ReviewExplanationOutput}`; `src/nvda_desk/services/capital_deployment_authority.py`; `src/nvda_desk/services/cognition_runtime.py`; `src/nvda_desk/services/review_explanation.py` | `tests/test_gate179_repo_wide_vocabulary_hygiene.py`; `tests/test_gate190_capital_deployment_authority_integration.py` | The runtime and vocabulary authority determine whether the phrase is a genuine semantic surface or just stale prose leakage in tests/docs. |
| P3-T03 control-surface router and gate-map reconciliation | `PLANS.md`; `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`; `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`; the specific late-pack planning docs/receipts/logs referenced by the gate-map | gate tests `149-156`, `163-165`, `170-172`, `180`, `181` | The router and process law define current-state truth; late pack tests only report when those surfaces disagree. |
| P3-T04 runtime semantic drift reconciliation | `src/nvda_desk/services/options_flow_context.py::{_surface_anchor_state,_options_behavior_cluster}`; `src/nvda_desk/schemas/cognition.py::OptionsFlowContextOutput`; `src/nvda_desk/services/playbook_eligibility.py::_skew_pressure_reversal`; `src/nvda_desk/services/imported_modules/posture_enrichers.py::_compression_regime_detector` | `tests/test_gate96_canonical_runtime_harness.py`; `tests/test_gate102_raw_runtime_harness.py`; `tests/test_gate31_higher_order_context_composites.py`; adjacent proofs `tests/test_real_data_loader.py`, `tests/test_options_flow_context.py` | Runtime services and typed outputs define lawful behaviour. Tests show where expectations and implementation diverge. |
| P3-T05 financial-calendar typing seam | `src/nvda_desk/schemas/financial_calendar.py::{FinancialCalendarCrosswalkRecord,default_financial_calendar_crosswalk}`; `src/nvda_desk/services/financial_calendar_projection.py::{_match_crosswalk,_event_window_datetimes}` | tests `89-92`; `tests/test_financial_calendar_planning_v3.py`; concentrated `mypy` report | Constructor and projection signatures are the seam; tests are downstream consumers of those types. |
| P3-T06 typed helper pressure reduction | `tests/contract_chain_fixtures.py`; `tests/_successor_pack_helpers.py` and any directly coupled typed helper modules identified during execution | `tests/test_gate97_runtime_invariants.py`; `tests/test_gate103_raw_prepared_parity.py`; `tests/test_gate104_property_stateful.py`; `mypy` output | Shared helper definitions and return shapes are the source of the typing debt; failing strict tests are evidence of those helper seams. |
| P3-T07 static hygiene and warning cleanup | `alembic/env.py`; `alembic.ini`; `alembic/versions/*`; `src/nvda_desk/config_models.py`; concrete files named by `ruff`/`mypy` output | `ruff check .`; `mypy src tests`; warning-only parity receipts | Static files and config surfaces are the thing being repaired; tool output is evidence of debt, not a design authority. |

## Operational implication

A Phase 3 leaf is under-specified if it names only tests and does not name the raw code, typed contract, or governing doc surfaces that those tests are supposed to reflect.
