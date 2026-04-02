"""Gate 153 overlay / terminal / final-join authority replanning checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-02_STAGE_LOCAL_HANDOFF_CORRECTIVE_SUCCESSOR_GATES_v1.md"
LEAVES = (
    REPO_ROOT / "docs/planning/2026-04-02_STAGE_LOCAL_HANDOFF_CORRECTIVE_SUCCESSOR_LEAVES_v1.json"
)
RECEIPT = (
    REPO_ROOT / "docs/planning/2026-04-02_GATE153_OVERLAY_TERMINAL_FINAL_JOIN_AUTHORITY_REPLAN.md"
)


def test_gate153_control_surfaces_advance_honestly() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert (
        "active gate: Gate 154 on `main`" in plans
        or "active gate: Gate 155 on `main`" in plans
        or "active gate: Gate 156 on `main`" in plans
        or "no active pack currently routed; stage-local handoff corrective successor pack closed through Gate 156 on `main`"
        in plans
    )
    assert (
        "Current active gate: **Gate 154 in the stage-local handoff corrective successor pack**."
        in gate_map
        or "Current active gate: **Gate 155 in the stage-local handoff corrective successor pack**."
        in gate_map
        or "Current active gate: **Gate 156 in the stage-local handoff corrective successor pack**."
        in gate_map
        or "Current active gate: **none — stage-local handoff corrective successor pack closed through Gate 156 on `main`**."
        in gate_map
    )
    assert (
        "Status: active stage-local handoff corrective successor pack; Gates 150-153 complete on `main`, Gate 154 active, Gates 155-156 planned"
        in gates
        or "Status: active stage-local handoff corrective successor pack; Gates 150-154 complete on `main`, Gate 155 active, Gate 156 planned"
        in gates
        or "Status: active stage-local handoff corrective successor pack; Gates 150-155 complete on `main`, Gate 156 active"
        in gates
        or "Status: closed stage-local handoff corrective successor pack through Gate 156 on `main`"
        in gates
    )
    assert leaves["execution_status"] in {
        "gate_153_complete_gate_154_active_on_main",
        "gate_154_complete_gate_155_active_on_main",
        "gate_155_complete_gate_156_active_on_main",
        "stage_local_handoff_corrective_successor_pack_closed_through_gate_156_on_main",
    }
    assert leaves["active_gate"] in {"Gate 154", "Gate 155", "Gate 156", "none"}
    for leaf_id in ["LEAF-G153-001", "LEAF-G153-002", "LEAF-G153-003", "LEAF-G153-004"]:
        assert leaves["leaves"][leaf_id]["status"] == "complete"


def test_gate153_receipt_freezes_overlap_classes_non_equivalence_and_boundary() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")

    assert "No new governed vocabulary is admitted in Gate 153." in receipt
    assert "## Exhaustive overlap-class table" in receipt
    assert "overlay_allow_no_terminal_override" in receipt
    assert "overlay_derisk_no_terminal_override" in receipt
    assert "overlay_block_no_terminal_override" in receipt
    assert "posture_derisk_supersedes_overlay_allow" in receipt
    assert "posture_block_supersedes_overlay_allow" in receipt
    assert "posture_block_supersedes_overlay_derisk" in receipt
    assert "posture_block_aligns_with_overlay_block" in receipt
    assert "## Overlay, terminal application, and final join non-equivalence matrix" in receipt
    assert "Agreement on action does **not** make the surfaces equivalent." in receipt
    assert "independent parallel risk lane" in receipt
    assert "final arbiter" in receipt
    assert "apply_final_join(...)" in receipt
