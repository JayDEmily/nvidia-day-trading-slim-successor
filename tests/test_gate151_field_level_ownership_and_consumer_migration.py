"""Gate 151 field-level ownership and consumer-migration planning checks."""

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
RECEIPT = (
    REPO_ROOT / "docs/planning/2026-04-02_GATE151_FIELD_LEVEL_OWNERSHIP_AND_CONSUMER_MIGRATION.md"
)

ALLOWED_PLAN_MARKERS = {
    "active gate: Gate 152 on `main`",
    "active gate: Gate 153 on `main`",
    "active gate: Gate 154 on `main`",
    "active gate: Gate 155 on `main`",
    "active gate: Gate 156 on `main`",
    "active gate: Gate 152 on `work/gate-151-field-level-ownership-and-consumer-migration-20260402`",
    "active gate: Gate 153 on `work/gate-152-stage5-stage6-authority-replan-20260402`",
    "no active pack currently routed; stage-local handoff corrective successor pack closed through Gate 156 on `main`",
}

ALLOWED_GATE_MAP_MARKERS = {
    "Current active gate: **Gate 152 in the stage-local handoff corrective successor pack**.",
    "Current active gate: **Gate 153 in the stage-local handoff corrective successor pack**.",
    "Current active gate: **Gate 154 in the stage-local handoff corrective successor pack**.",
    "Current active gate: **Gate 155 in the stage-local handoff corrective successor pack**.",
    "Current active gate: **Gate 156 in the stage-local handoff corrective successor pack**.",
    "Current active gate: **none — stage-local handoff corrective successor pack closed through Gate 156 on `main`**.",
}


def test_gate151_control_surfaces_advance_honestly() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert contains_any(plans, ALLOWED_PLAN_MARKERS | PHASE3_PLAN_MARKERS)
    assert contains_any(gate_map, ALLOWED_GATE_MAP_MARKERS | PHASE3_GATE_MAP_MARKERS)
    assert (
        "Status: active stage-local handoff corrective successor pack; Gates 150-151 complete on `main`, Gate 152 active, Gates 153-156 planned"
        in gates
        or "Status: active stage-local handoff corrective successor pack; Gates 150-152 complete on `main`, Gate 153 active, Gates 154-156 planned"
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
        "gate_151_complete_gate_152_active_on_main",
        "gate_152_complete_gate_153_active_on_main",
        "gate_153_complete_gate_154_active_on_main",
        "gate_154_complete_gate_155_active_on_main",
        "gate_155_complete_gate_156_active_on_main",
        "stage_local_handoff_corrective_successor_pack_closed_through_gate_156_on_main",
    }
    assert leaves["active_gate"] in {
        "Gate 152",
        "Gate 153",
        "Gate 154",
        "Gate 155",
        "Gate 156",
        "none",
    }
    assert leaves["completed_gate_ids"] in (
        ["Gate 150", "Gate 151"],
        ["Gate 150", "Gate 151", "Gate 152"],
        ["Gate 150", "Gate 151", "Gate 152", "Gate 153"],
        ["Gate 150", "Gate 151", "Gate 152", "Gate 153", "Gate 154"],
        ["Gate 150", "Gate 151", "Gate 152", "Gate 153", "Gate 154", "Gate 155"],
        ["Gate 150", "Gate 151", "Gate 152", "Gate 153", "Gate 154", "Gate 155", "Gate 156"],
    )
    for leaf_id in ["LEAF-G151-001", "LEAF-G151-002", "LEAF-G151-003", "LEAF-G151-004"]:
        assert leaves["leaves"][leaf_id]["status"] == "complete"


def test_gate151_receipt_freezes_field_ownership_consumer_scope_and_residual_gaps() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")

    assert "No new governed vocabulary is admitted in Gate 151." in receipt
    assert "## Field-level ownership ledger" in receipt
    assert "## Transitive consumer migration matrix" in receipt
    assert "## Preserved-seam sufficiency and residual-gap law" in receipt
    assert "cited_posture_pre_modifier" in receipt
    assert "EligibilityAdmissibilitySurface.permission_state" in receipt
    assert "ExecutionCandidateOwnershipSurface.admitted_playbook_ids" in receipt
    assert (
        "review_packets.py` and `src/nvda_desk/api/app.py` remain indirect daily-review surfaces"
        in receipt
    )
    assert "Gate 154 must focus on the **actual** direct consumers discovered here" in receipt
