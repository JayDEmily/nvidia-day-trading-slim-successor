# 2026-04-04_GATE195_CONTROL_SURFACE_ROUTER_AND_GATE_MAP_RECONCILIATION

Status: Gate 195 complete on `work/gate-195-control-surface-router-gate-map-reconciliation-20260404`; Gate 196 is the next active gate in the Phase 3 main-target repair programme.

## Purpose

Freeze the single lawful current-state narrative for the repo router and canonical gate map, then repair only the bounded historical planning tests that had become stale because they refused later lawful router states.

## Source-truth decision

The controlling current-state surfaces were:
- repo-root `PLANS.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`

Those raw control surfaces were already coherent before Gate 195 implementation:
- `PLANS.md` routed the active Phase 3 pack and named Gate 195 as next active gate;
- the canonical gate map named Gate 195 as the current active gate in the Phase 3 main-target repair programme; and
- the process law explicitly requires later-proof tests to permit later lawful states or be retired/replaced.

The stale surfaces were the historical late-pack tests for Gates 149-181. Those tests still froze old router states and therefore treated lawful later router states as defects.

## Bounded repair applied

- Added `tests/_planning_later_state_helpers.py` to centralise lawful later-state markers for the active Phase 3 pack.
- Updated the bounded historical planning tests for Gates 149-156, 163-165, 170-172, 180, and 181 so they accept later lawful router and gate-map states without weakening their pack-local invariants.
- Did not edit runtime-domain code.
- Did not alter the historical pack docs themselves.

## Validation commands

- `PYTHONPATH=src python -m pytest -q tests/test_gate149_stage_local_handoff_pack_closeout.py tests/test_gate150_corrective_successor_pack_planning.py tests/test_gate151_field_level_ownership_and_consumer_migration.py tests/test_gate152_stage5_stage6_authority_replan.py tests/test_gate153_overlay_terminal_final_join_authority_replan.py tests/test_gate154_downstream_consumer_reconciliation_replan.py tests/test_gate155_downstream_consequence_routing_and_successor_boundary.py tests/test_gate156_corrective_pack_anti_drift_closeout.py tests/test_gate163_coefficient_architecture_consolidation_closeout.py tests/test_gate164_policy_temporal_observability_successor_pack_planning.py tests/test_gate165_lean_policy_law_externalisation.py tests/test_gate170_policy_temporal_observability_successor_closeout.py tests/test_gate171_master_child_parallel_risk_integration_pack_planning.py tests/test_gate172_master_child_lineage_and_overlap_ledger.py tests/test_gate180_master_child_integration_closeout.py tests/test_gate181_options_trace_integrity_pack_planning.py tests/test_planning_state_integrity.py tests/test_document_hygiene.py`

## Validation result

- Gate 195 bounded proof slice passed: `40 passed in 0.63s`.

## What Gate 195 does not claim

- It does not change any runtime semantic surface.
- It does not reopen or rewrite historical pack docs just because they are older.
- It does not start Gate 196 runtime-semantic repair work.
