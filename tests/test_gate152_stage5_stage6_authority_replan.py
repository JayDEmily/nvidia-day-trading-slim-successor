"""Gate 152 Stage 5 / Stage 6 authority replanning checks."""

from __future__ import annotations

import json
from pathlib import Path

from ._planning_later_state_helpers import (
    PHASE3_GATE_MAP_MARKERS,
    PHASE3_PLAN_MARKERS,
    contains_any,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-02_STAGE_LOCAL_HANDOFF_CORRECTIVE_SUCCESSOR_GATES_v1.md"
LEAVES = (
    REPO_ROOT / "docs/planning/2026-04-02_STAGE_LOCAL_HANDOFF_CORRECTIVE_SUCCESSOR_LEAVES_v1.json"
)
RECEIPT = REPO_ROOT / "docs/planning/2026-04-02_GATE152_STAGE5_STAGE6_AUTHORITY_REPLAN.md"


def test_gate152_control_surfaces_advance_honestly() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert contains_any(plans, PHASE3_PLAN_MARKERS) or (
        "active gate: Gate 153 on `main`" in plans
        or "active gate: Gate 154 on `main`" in plans
        or "active gate: Gate 155 on `main`" in plans
        or "active gate: Gate 156 on `main`" in plans
        or "no active pack currently routed; stage-local handoff corrective successor pack closed through Gate 156 on `main`"
        in plans
        or "successor retained-test cleanup execution pack; Gate 224 is active" in plans
        or "Gate 224 is complete on `work/gate-224-runtime-review-and-contract-retarget-20260406`" in plans
        or "successor retained-test cleanup execution pack; Gate 225 is active" in plans
        or "no active pack currently routed" in plans
    )
    assert contains_any(gate_map, PHASE3_GATE_MAP_MARKERS) or (
        "Current active gate: **Gate 153 in the stage-local handoff corrective successor pack**."
        in gate_map
        or "Current active gate: **Gate 154 in the stage-local handoff corrective successor pack**."
        in gate_map
        or "Current active gate: **Gate 155 in the stage-local handoff corrective successor pack**."
        in gate_map
        or "Current active gate: **Gate 156 in the stage-local handoff corrective successor pack**."
        in gate_map
        or "Current active gate: **none — stage-local handoff corrective successor pack closed through Gate 156 on `main`**."
        in gate_map
        or "Current active gate: **Gate 224 active on `work/gate-224-runtime-review-and-contract-retarget-20260406` under the successor retained-test cleanup execution pack.**"
        in gate_map
        or "Current active gate: **No active gate under the successor retained-test cleanup execution pack. Gate 224 is complete on `work/gate-224-runtime-review-and-contract-retarget-20260406`; Gate 225 is not yet activated.**"
        in gate_map
        or "Current active gate: **Gate 225 active on `work/gate-225-retained-test-cleanup-closeout-20260406` under the successor retained-test cleanup execution pack.**"
        in gate_map
        or "Current active gate: **No active gate under the successor retained-test cleanup execution pack. Gate 225 is complete on `work/gate-225-retained-test-cleanup-closeout-20260406`; cleanup pack closed.**"
        in gate_map
        or "Current active gate: **No active pack currently routed. The successor retained-test cleanup execution pack is closed through Gate 225 on `work/gate-225-retained-test-cleanup-closeout-20260406`.**"
        in gate_map
    )
    assert (
        "Status: active stage-local handoff corrective successor pack; Gates 150-152 complete on `main`, Gate 153 active, Gates 154-156 planned"
        in gates
        or "Status: active stage-local handoff corrective successor pack; Gates 150-153 complete on `main`, Gate 154 active, Gates 155-156 planned"
        in gates
        or "Status: active stage-local handoff corrective successor pack; Gates 150-154 complete on `main`, Gate 155 active, Gate 156 planned"
        in gates
        or "Status: active stage-local handoff corrective successor pack; Gates 150-155 complete on `main`, Gate 156 active"
        in gates
        or "Status: closed stage-local handoff corrective successor pack through Gate 156 on `main`"
        in gates
    )
    assert leaves["execution_status"] in {
        "gate_152_complete_gate_153_active_on_main",
        "gate_153_complete_gate_154_active_on_main",
        "gate_154_complete_gate_155_active_on_main",
        "gate_155_complete_gate_156_active_on_main",
        "stage_local_handoff_corrective_successor_pack_closed_through_gate_156_on_main",
    }
    assert leaves["active_gate"] in {"Gate 153", "Gate 154", "Gate 155", "Gate 156", "none"}
    assert leaves["completed_gate_ids"] in (
        ["Gate 150", "Gate 151", "Gate 152"],
        ["Gate 150", "Gate 151", "Gate 152", "Gate 153"],
        ["Gate 150", "Gate 151", "Gate 152", "Gate 153", "Gate 154"],
        ["Gate 150", "Gate 151", "Gate 152", "Gate 153", "Gate 154", "Gate 155"],
        ["Gate 150", "Gate 151", "Gate 152", "Gate 153", "Gate 154", "Gate 155", "Gate 156"],
    )
    for leaf_id in ["LEAF-G152-001", "LEAF-G152-002", "LEAF-G152-003", "LEAF-G152-004"]:
        assert leaves["leaves"][leaf_id]["status"] == "complete"


def test_gate152_receipt_freezes_case_law_and_non_equivalence_rules() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")

    assert "No new governed vocabulary is admitted in Gate 152." in receipt
    assert "## Stage 5 admissibility case table" in receipt
    assert "## Stage 6 candidate-ownership and contradiction proof table" in receipt
    assert "## Stage 5 and Stage 6 agreement-versus-non-equivalence table" in receipt
    assert "event_window_veto" in receipt
    assert "watch_only_candidates_not_promoted_to_execution" in receipt
    assert "single_candidate_clear" in receipt
    assert "mixed_context_resolved_by_score" in receipt
    assert "registry_priority_tiebreak" in receipt
    assert "score_ranked_candidate_pool" in receipt
    assert "Do not infer Stage 5 truth from `lead_playbook_id` alone." in receipt
