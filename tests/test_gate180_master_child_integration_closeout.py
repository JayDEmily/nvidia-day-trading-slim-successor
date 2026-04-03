"""Gate 180 master/child parallel-risk integration closeout checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-02_MASTER_CHILD_PARALLEL_RISK_INTEGRATION_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-02_MASTER_CHILD_PARALLEL_RISK_INTEGRATION_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-02_MASTER_CHILD_PARALLEL_RISK_INTEGRATION_EXECUTION_LOG_v1.md"
CHECKLIST = REPO_ROOT / "docs/planning/2026-04-02_MASTER_CHILD_PARALLEL_RISK_INTEGRATION_DOCUMENT_TOUCH_CHECKLIST_v1.md"
SCOPE_NOTE = REPO_ROOT / "docs/planning/2026-04-02_MASTER_CHILD_PARALLEL_RISK_INTEGRATION_SCOPE_NOTE_v1.md"
RECEIPT = REPO_ROOT / "docs/planning/2026-04-02_GATE180_MASTER_CHILD_INTEGRATION_AUDIT_AND_CLOSEOUT.md"


def test_gate180_control_surfaces_close_honestly_on_main() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert "master/child parallel-risk integration pack closed through Gate 180 on `main`" in plans
    assert "Current active gate: **Gate 182 in the options-trace integrity repair pack on `main`**." in gate_map
    assert "Status: closed master/child parallel-risk integration pack through Gate 180 on `main`" in gates
    assert leaves["execution_status"] == "master_child_parallel_risk_integration_pack_closed_through_gate_180_on_main"
    assert leaves["active_gate"] == "none"
    assert leaves["remaining_leaf_ids"] == []
    assert leaves["pending_gate_ids"] == []
    assert set(leaves["completed_leaf_ids"]).isdisjoint(leaves["remaining_leaf_ids"])
    assert leaves["completed_gate_ids"] == [
        "Gate 171",
        "Gate 172",
        "Gate 173",
        "Gate 174",
        "Gate 175",
        "Gate 176",
        "Gate 177",
        "Gate 178",
        "Gate 179",
        "Gate 180",
    ]
    assert all(leaf["status"] == "complete" for leaf in leaves["leaves"].values())
    assert "repo_gate180_master_child_parallel_risk_integration_pack_closed_workbranch_2026-04-02.zip" in execution_log
    assert "Fast-forward promoted `main` to commit `e7f8a59`" in execution_log
    assert "Current planned sequence: master/child parallel-risk integration pack closed through Gate 180 on `main`." in checklist


def test_gate180_receipt_audits_merge_runtime_hygiene_and_packaging() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")
    scope_note = SCOPE_NOTE.read_text(encoding="utf-8")

    assert "Independent Parallel Risk Lane" in receipt
    assert "Signal-Coefficient Reference Workbook" in receipt
    assert "Calibration has not started." in receipt
    assert "## Audit ledger: child planning law merged or missed" in receipt
    assert "## Runtime implementation truth audit" in receipt
    assert "## Workbook-governance audit" in receipt
    assert "## Vocabulary and hygiene audit" in receipt
    assert "## Proof and build audit" in receipt
    assert "## Remaining deferred items" in receipt
    assert "complete on `main`" in receipt
    assert "repo_gate180_master_child_parallel_risk_integration_pack_closed_workbranch_2026-04-02.zip" in receipt
    assert "Do not let the new lane become an arbiter" in scope_note
