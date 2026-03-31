"""Gate 128 post-flight repo consistency planning checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-03-31_POST_FLIGHT_REPO_CONSISTENCY_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-31_POST_FLIGHT_REPO_CONSISTENCY_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-03-31_POST_FLIGHT_REPO_CONSISTENCY_EXECUTION_LOG_v1.md"
CHECKLIST = REPO_ROOT / "docs/planning/2026-03-31_POST_FLIGHT_REPO_CONSISTENCY_DOCUMENT_TOUCH_CHECKLIST_v1.md"

ALLOWED_CURRENT_GATE_MARKERS = {
    "Current active gate: **Gate 128 in the post-flight repo consistency pack**.",
    "Current active gate: **Gate 129 in the post-flight repo consistency pack**.",
    "Current active gate: **Gate 130 in the post-flight repo consistency pack**.",
    "Current active gate: **Gate 131 in the post-flight repo consistency pack**.",
    "Current active gate: **none — post-flight repo consistency pack closed through Gate 131 on `main`**.",
}


def test_post_flight_repo_consistency_pack_is_active() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert "2026-03-31_POST_FLIGHT_REPO_CONSISTENCY_GATES_v1.md" in plans
    assert "2026-03-31_POST_FLIGHT_REPO_CONSISTENCY_LEAVES_v1.json" in plans
    assert "2026-03-31_POST_FLIGHT_REPO_CONSISTENCY_EXECUTION_LOG_v1.md" in plans
    assert "2026-03-31_POST_FLIGHT_REPO_CONSISTENCY_DOCUMENT_TOUCH_CHECKLIST_v1.md" in plans
    assert any(marker in gate_map for marker in ALLOWED_CURRENT_GATE_MARKERS)
    assert (
        "Status: active post-flight repo consistency pack; Gate 128 active, Gates 129-131 planned" in gates
        or "Status: active post-flight repo consistency pack; Gate 128 complete on `main`, Gate 129 active, Gates 130-131 planned" in gates
        or "Status: active post-flight repo consistency pack; Gates 128-129 complete on `main`, Gate 130 active, Gate 131 planned" in gates
    )
    assert leaves["execution_status"] in {
        "gate_127_closed_post_flight_repo_consistency_pack_active_from_gate_128",
        "gate_128_complete_gate_129_active_on_main",
        "gate_129_complete_gate_130_active_on_main",
    }
    assert leaves["active_gate"] in {"Gate 128", "Gate 129", "Gate 130"}
    assert len(leaves["remaining_leaf_ids"]) in {11, 8, 5}
    assert execution_log.startswith("# 2026-03-31_POST_FLIGHT_REPO_CONSISTENCY_EXECUTION_LOG_v1")
    assert "Gate 128-131" in checklist or "Gate 128" in checklist


def test_pack_freezes_verified_failure_inventory_and_scope_boundaries() -> None:
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert "429 passed, 14 failed in 33.17s" in gates
    assert leaves["verified_postflight_inventory"]["observed_result"] == "429 passed, 14 failed in 33.17s"
    assert len(leaves["verified_postflight_inventory"]["failing_tests"]) == 14
    assert leaves["global_rules"]["router_assertions_must_track_modern_pack_state_not_obsolete_literal_plans_text"] is True
    assert leaves["global_rules"]["runtime_expectation_updates_must_be_backed_by_current_observed_outputs"] is True
    assert leaves["global_rules"]["no_new_runtime_architecture_or_coefficient_scope_expansion_in_this_pack"] is True
