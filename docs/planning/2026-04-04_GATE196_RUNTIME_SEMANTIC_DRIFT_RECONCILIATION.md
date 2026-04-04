# 2026-04-04_GATE196_RUNTIME_SEMANTIC_DRIFT_RECONCILIATION

Status: Gate 196 complete on `work/gate-196-runtime-semantic-drift-reconciliation-20260404`; Gate 197 is the next active gate in the Phase 3 main-target repair programme.

## Purpose

Adjudicate the bounded runtime-semantic drift family from raw code truth first, then repair only the stale runtime-harness and higher-order-context expectation surfaces required by that decision.

## Source-truth decision

The controlling runtime surfaces were:
- `src/nvda_desk/services/options_flow_context.py::{_surface_anchor_state,_options_behavior_cluster}`
- `src/nvda_desk/services/imported_modules/posture_enrichers.py::_compression_regime_detector`
- the real-data harness fixture surfaces that feed those services
- `tests/test_real_data_loader.py` and `tests/test_options_flow_context.py` as adjacent evidence, not primary authority

### Options-flow harness seam

For the canonical prepared and canonical raw harnesses, the ingested fixture surfaces carry `surface_anchor_to_spot_pct` values that classify as `anchored_away`. In `_options_behavior_cluster`, the `anchored_away` branch lawfully returns `anchored_translation_tension` before the fallback `balanced_options_state` path. The runtime code is therefore lawful and the stale surfaces were the Gate 96 / Gate 102 harness expectations.

### Higher-order context seam

For the stressed Gate 31 bundle, `_compression_regime_detector()` only emits `compression_ready`, `compression_absent`, or `compression_mixed` from the current raw code. The stressed fixture lands in the mixed branch, so the stale surface was the Gate 31 expectation set that excluded `compression_mixed`.

## Bounded repair applied

- Updated `tests/test_gate31_higher_order_context_composites.py` to admit `compression_mixed` as a lawful stressed descriptive state.
- Updated `tests/test_gate96_canonical_runtime_harness.py` and `tests/test_gate102_raw_runtime_harness.py` to freeze `anchored_translation_tension` for the canonical harnesses.
- Updated `docs/planning/2026-03-30_GATE102_CANONICAL_RAW_PATH_HARNESS.md` so the recorded deterministic runtime freeze matches the current lawful runtime outputs.
- Did not edit `src/` runtime code because the raw code and adjacent evidence agreed.

## Validation commands

- `PYTHONPATH=src python -m pytest -q tests/test_gate31_higher_order_context_composites.py tests/test_gate96_canonical_runtime_harness.py tests/test_gate102_raw_runtime_harness.py tests/test_real_data_loader.py tests/test_options_flow_context.py tests/test_gate104_property_stateful.py`
- `PYTHONPATH=src python -m pytest -q tests/test_gate192_phase3_main_target_repair_pack_planning.py tests/test_tranche_briefing_template_pack.py tests/test_planning_state_integrity.py tests/test_document_hygiene.py`

## Validation result

- bounded Gate 196 runtime proof slice passed: `19 passed in 1.16s`
- planning/router proof slice passed after Gate 196 closeout: `11 passed in 0.37s`

## What Gate 196 does not claim

- It does not claim the old Gate 102 freeze note was malicious; it was simply stale relative to the current lawful runtime semantics.
- It does not reopen vocabulary, router, or static-quality tranches.
- It does not start the financial-calendar typing seam work for Gate 197.
