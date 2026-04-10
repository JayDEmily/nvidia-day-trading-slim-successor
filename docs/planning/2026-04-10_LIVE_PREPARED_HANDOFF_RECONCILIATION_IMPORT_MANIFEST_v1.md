# 2026-04-10_LIVE_PREPARED_HANDOFF_RECONCILIATION_IMPORT_MANIFEST_v1

Status: retained import manifest for Gate 255 closeout.

## Source

- prepared comparison copy: `.incoming/prepared_handoff/codex_handoff_package_2026-04-10/nvidia-day-trading-slim-successor-main_prepared_2026-04-10/`
- prepared import source: `/tmp/gate255_handoff_source/codex_handoff_package_2026-04-10/nvidia-day-trading-slim-successor-main_prepared_2026-04-10/`
- live git-authoritative base: `main` at `88ffb8f92d95b6dbf44b34d962d9ca552b960f02`

## Summary

- added files: 60
- modified tracked files: 38
- deleted tracked files: 0
- adapted-on-import surfaces: 8
- deferred surfaces: 2
- hard conflicts before apply: 0 beyond the known deferred `AGENTS.md` contradiction

## Added

- Gate 236-254 planning packs and closeout notes under `docs/planning/2026-04-09_*` and `docs/planning/2026-04-10_*`
- 2026-04-06 tranche briefing template generation files
- `alembic/versions/20260409_0008_options_flow_history_lane.py`
- `src/nvda_desk/schemas/checkpoints.py`
- `src/nvda_desk/schemas/options_flow_history.py`
- `src/nvda_desk/services/options_flow_history.py`
- `src/nvda_desk/services/upstream_signal_checkpointing.py`
- `src/nvda_desk/services/upstream_signal_ingress.py`
- tests for Gates 236-254 and upstream follow-up corrections

## Modified

- doctrine/control surfaces: `docs/01_NORMATIVE.md`, `docs/03_DOMAIN_MODEL.md`, `docs/04_TECHNICAL_ARCHITECTURE.md`, `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`, `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md`, `docs/TESTING_AND_PROMOTION.md`
- runtime/schema surfaces: `src/nvda_desk/config.py`, `src/nvda_desk/db/models.py`, `src/nvda_desk/schemas/cognition.py`, `src/nvda_desk/schemas/dataset.py`, `src/nvda_desk/services/chain_to_cognition.py`, `src/nvda_desk/services/real_data_loader.py`, `src/nvda_desk/services/cognition_runtime.py`, `src/nvda_desk/services/execution_expression.py`, `src/nvda_desk/services/review_explanation.py`, `src/nvda_desk/services/capital_deployment_authority.py`
- fixtures and evidence artefacts: `fixtures/real_data/gate_e_prepared_runtime_fixture_pack.json`, `fixtures/trace_review/gate_134_bounded_trace_report.json`, `docs/status/2026-03-31_BOUNDED_TRACE_SCENARIO_REVIEW_REPORT.md`, `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`, `uv.lock`
- bounded later-state test updates, including `tests/test_gate134_bounded_trace_reporting.py`

## Adapted On Import

- `tests/test_tranche_briefing_template_pack.py`
- `tests/test_upstream_signal_followup_corrections.py`
- `tests/test_gate254_workflow_law_and_template_pack_refresh.py`
- new `tests/test_gate255_live_prepared_handoff_reconciliation.py`
- `tests/test_gate242_options_flow_history_lane_vocabulary_and_boundary.py`
- `tests/test_gate246_options_flow_history_replay_closeout.py`
- `tests/test_gate247_upstream_signal_coverage_map_and_scope_lock.py`
- `tests/test_gate252_upstream_non_interference_and_sanity_traces.py`

Reason:
- the prepared versions hard-code the deferred Gate 253/254 `AGENTS.md` state or the intermediate prepared-router wording and therefore must be adapted to live Gate 255 truth rather than copied verbatim.

## Deferred

- `AGENTS.md`
- `tests/test_gate110_agents_reading_order.py`

Reason:
- `AGENTS.md` depends on missing `docs/08_GITHUB_OR_CHATGPT_GITHUB_INTERACTIONS.md`
- `tests/test_gate110_agents_reading_order.py` is not a required Gate 255 proof surface and does not encode Gate 255 reconciliation truth

## Hard-conflict Scan

- no additional hard conflict found before apply
- inspected overlap with live post-Gate-235 corrective commit: `tests/test_gate134_bounded_trace_reporting.py`
- resolution: prepared later-state tolerance accepted
