"""Gate 156 corrective-pack anti-drift closeout checks."""

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
EXECUTION_LOG = (
    REPO_ROOT
    / "docs/planning/2026-04-02_STAGE_LOCAL_HANDOFF_CORRECTIVE_SUCCESSOR_EXECUTION_LOG_v1.md"
)
CHECKLIST = (
    REPO_ROOT
    / "docs/planning/2026-04-02_STAGE_LOCAL_HANDOFF_CORRECTIVE_SUCCESSOR_DOCUMENT_TOUCH_CHECKLIST_v1.md"
)
RECEIPT = REPO_ROOT / "docs/planning/2026-04-02_GATE156_CORRECTIVE_PACK_ANTI_DRIFT_CLOSEOUT.md"


def test_gate156_control_surfaces_close_honestly() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert contains_any(plans, PHASE3_PLAN_MARKERS) or (
        "no active pack currently routed; stage-local handoff corrective successor pack closed through Gate 156 on `main`"
        in plans
        or "latest closed corrective evidence is the stage-local handoff corrective successor pack closed through Gate 156 on `main`" in plans
    )
    assert contains_any(gate_map, PHASE3_GATE_MAP_MARKERS) or (
        "Current active gate: **none — stage-local handoff corrective successor pack closed through Gate 156 on `main`**."
        in gate_map
    )
    assert (
        "Status: closed stage-local handoff corrective successor pack through Gate 156 on `main`"
        in gates
    )
    assert (
        "Status: closed execution log for the stage-local handoff corrective successor pack through Gate 156 on `main`"
        in execution_log
    )
    assert (
        "Current planned sequence: corrective successor pack closed through Gate 156 on `main`."
        in checklist
    )
    assert (
        leaves["execution_status"]
        == "stage_local_handoff_corrective_successor_pack_closed_through_gate_156_on_main"
    )
    assert leaves["active_gate"] == "none"
    assert leaves["remaining_leaf_ids"] == []
    assert leaves["completed_gate_ids"] == [
        "Gate 150",
        "Gate 151",
        "Gate 152",
        "Gate 153",
        "Gate 154",
        "Gate 155",
        "Gate 156",
    ]
    for leaf_id in leaves["leaf_order"]:
        assert leaves["leaves"][leaf_id]["status"] == "complete"


def test_gate156_receipt_records_drift_ledger_exact_proof_and_packaging() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")

    assert "No new governed vocabulary is admitted in Gate 156." in receipt
    assert "## Drift-defect ledger and resolutions" in receipt
    assert (
        "Gate 150 planning guard still assumed only Gate 151-153 or an active pack state" in receipt
    )
    assert (
        "repo-wide `make format-check` / `make lint` even though Gate 150 had already observed broad pre-existing baseline drift"
        in receipt
    )
    assert "## Final proof slice run" in receipt
    assert "48 passed in 1.02s" in receipt
    assert "9 files would be left unchanged." in receipt
    assert "All checks passed!" in receipt
    assert "repo_gate156_corrective_successor_pack_closed_main_2026-04-02.zip" in receipt
    assert "repo_gate156_corrective_successor_pack_closed_main_2026-04-02.zip" in execution_log
