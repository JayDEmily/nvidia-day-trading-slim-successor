"""Gate 164 parallel risk lane foundation anti-drift closeout checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-02_PARALLEL_RISK_LANE_FOUNDATION_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-02_PARALLEL_RISK_LANE_FOUNDATION_LEAVES_v1.json"
EXECUTION_LOG = (
    REPO_ROOT / "docs/planning/2026-04-02_PARALLEL_RISK_LANE_FOUNDATION_EXECUTION_LOG_v1.md"
)
CHECKLIST = (
    REPO_ROOT
    / "docs/planning/2026-04-02_PARALLEL_RISK_LANE_FOUNDATION_DOCUMENT_TOUCH_CHECKLIST_v1.md"
)
RECEIPT = (
    REPO_ROOT
    / "docs/planning/2026-04-02_GATE164_PARALLEL_RISK_LANE_FOUNDATION_ANTI_DRIFT_CLOSEOUT.md"
)
ZIP_NAME = "repo_gate164_parallel_risk_lane_foundation_pack_closed_2026-04-02_slim.zip"


def test_gate164_control_surfaces_close_honestly() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert (
        "none currently routed; parallel risk lane foundation pack closed through Gate 164" in plans
    )
    assert (
        "Current active gate: **none — parallel risk lane foundation pack closed through Gate 164"
        in gate_map
    )
    assert "Status: closed parallel risk lane foundation pack through Gate 164" in gates
    assert (
        "Status: closed execution log for the parallel risk lane foundation pack through Gate 164"
        in execution_log
    )
    assert (
        "Current planned sequence: parallel risk lane foundation pack closed through Gate 164"
        in checklist
    )
    assert (
        leaves["execution_status"]
        == "parallel_risk_lane_foundation_pack_closed_through_gate_164_on_work_branch"
    )
    assert leaves["active_gate"] == "none"
    assert leaves["remaining_leaf_ids"] == []
    assert leaves["pending_gate_ids"] == []
    assert leaves["completed_gate_ids"] == [
        "Gate 157",
        "Gate 158",
        "Gate 159",
        "Gate 160",
        "Gate 161",
        "Gate 162",
        "Gate 163",
        "Gate 164",
    ]
    for leaf_id in leaves["leaf_order"]:
        assert leaves["leaves"][leaf_id]["status"] == "complete"


def test_gate164_receipt_records_audit_semantic_coverage_and_packaging() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")

    assert "## Drift-defect ledger and resolutions" in receipt
    assert "workbook-lineage closure audit" in receipt
    assert "semantic-coverage checklist" in receipt
    assert "multi-clock model" in receipt
    assert "dependency activation" in receipt
    assert "dislocation-versus-impairment" in receipt
    assert "environmental risk weather" in receipt
    assert "candidate-specific risk audit" in receipt
    assert "expression-posture consequences" in receipt
    assert ZIP_NAME in receipt
    assert ZIP_NAME in execution_log
