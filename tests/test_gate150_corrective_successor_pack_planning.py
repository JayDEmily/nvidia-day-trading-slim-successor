"""Gate 150 corrective successor pack planning checks."""

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
EXECUTION_LOG = (
    REPO_ROOT
    / "docs/planning/2026-04-02_STAGE_LOCAL_HANDOFF_CORRECTIVE_SUCCESSOR_EXECUTION_LOG_v1.md"
)
CHECKLIST = (
    REPO_ROOT
    / "docs/planning/2026-04-02_STAGE_LOCAL_HANDOFF_CORRECTIVE_SUCCESSOR_DOCUMENT_TOUCH_CHECKLIST_v1.md"
)
RECEIPT = REPO_ROOT / "docs/planning/2026-04-02_GATE150_CORRECTIVE_SUCCESSOR_PACK_BOOTSTRAP.md"

ALLOWED_CURRENT_GATE_MARKERS = {
    "Current active gate: **Gate 151 in the stage-local handoff corrective successor pack**.",
    "Current active gate: **Gate 152 in the stage-local handoff corrective successor pack**.",
    "Current active gate: **Gate 153 in the stage-local handoff corrective successor pack**.",
    "Current active gate: **Gate 154 in the stage-local handoff corrective successor pack**.",
    "Current active gate: **Gate 155 in the stage-local handoff corrective successor pack**.",
    "Current active gate: **Gate 156 in the stage-local handoff corrective successor pack**.",
    "Current active gate: **none — stage-local handoff corrective successor pack closed through Gate 156 on `main`**.",
}


def test_gate150_pack_is_active_and_non_placeholder() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert "2026-04-02_STAGE_LOCAL_HANDOFF_CORRECTIVE_SUCCESSOR_GATES_v1.md" in plans
    assert "2026-04-02_STAGE_LOCAL_HANDOFF_CORRECTIVE_SUCCESSOR_LEAVES_v1.json" in plans
    assert "2026-04-02_STAGE_LOCAL_HANDOFF_CORRECTIVE_SUCCESSOR_EXECUTION_LOG_v1.md" in plans
    assert (
        "2026-04-02_STAGE_LOCAL_HANDOFF_CORRECTIVE_SUCCESSOR_DOCUMENT_TOUCH_CHECKLIST_v1.md"
        in plans
    )
    assert "active gate: Gate 151 on `work/gate-150-corrective-successor-pack-20260402`" in plans
    assert any(marker in gate_map for marker in ALLOWED_CURRENT_GATE_MARKERS)
    assert (
        "Status: active stage-local handoff corrective successor pack; Gate 150 complete on `work/gate-150-corrective-successor-pack-20260402`, Gate 151 active, Gates 152-156 planned"
        in gates
    )
    assert leaves["execution_status"] == "gate_150_complete_gate_151_active_on_work_branch"
    assert leaves["active_gate"] == "Gate 151"
    assert leaves["completed_gate_ids"] == ["Gate 150"]
    assert leaves["completed_leaf_ids"] == ["LEAF-G150-001", "LEAF-G150-002", "LEAF-G150-003"]
    assert execution_log.startswith(
        "# 2026-04-02_STAGE_LOCAL_HANDOFF_CORRECTIVE_SUCCESSOR_EXECUTION_LOG_v1"
    )
    assert "Gate 150 complete" in checklist


def test_gate150_future_leaves_are_materially_detailed() -> None:
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))["leaves"]

    future_gate_ids = {"Gate 151", "Gate 152", "Gate 153", "Gate 154", "Gate 155", "Gate 156"}
    future_leaves = [leaf for leaf in leaves.values() if leaf["gate"] in future_gate_ids]

    assert future_leaves
    for leaf in future_leaves:
        assert leaf["status"] == "planned"
        assert len(leaf["ordered_actions"]) >= 3
        assert len(leaf["forbidden_actions"]) >= 3
        assert leaf["validation_commands"]
        assert leaf["expected_evidence"]
        assert leaf["definition_of_done"]
        assert leaf["packaging_requirement"]


def test_gate150_receipt_preserves_history_and_freezes_deferred_architecture() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")

    assert "the historical pack stays as evidence" in receipt
    assert (
        "Gate 148's title promised broader downstream reconciliation than the files actually touched"
        in receipt
    )
    assert "Gate 149 had to reopen" in receipt
    assert "independent parallel risk lane" in receipt
    assert "final arbiter" in receipt
    assert "dynamic coefficient redesign" in receipt
    assert "Every operator handoff from this branch must include a fresh full-history zip" in gates
