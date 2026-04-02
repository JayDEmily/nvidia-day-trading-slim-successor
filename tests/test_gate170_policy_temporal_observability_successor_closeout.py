"""Gate 170 policy/temporal/observability successor closeout checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-02_POLICY_TEMPORAL_OBSERVABILITY_SUCCESSOR_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-02_POLICY_TEMPORAL_OBSERVABILITY_SUCCESSOR_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-02_POLICY_TEMPORAL_OBSERVABILITY_SUCCESSOR_EXECUTION_LOG_v1.md"
CHECKLIST = REPO_ROOT / "docs/planning/2026-04-02_POLICY_TEMPORAL_OBSERVABILITY_SUCCESSOR_DOCUMENT_TOUCH_CHECKLIST_v1.md"
RECEIPT = REPO_ROOT / "docs/planning/2026-04-02_GATE170_POLICY_TEMPORAL_OBSERVABILITY_SUCCESSOR_AUDIT_AND_CLOSEOUT.md"
SCOPE_NOTE = REPO_ROOT / "docs/planning/2026-04-02_POLICY_TEMPORAL_OBSERVABILITY_SUCCESSOR_SCOPE_NOTE_v1.md"


def test_gate170_control_surfaces_close_honestly_on_work_branch() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert any(
        marker in plans
        for marker in {
            "no active pack currently routed; policy/temporal/observability successor pack closed through Gate 170 on `work/gate-164-policy-temporal-observability-pack-20260402`",
            "active gate: Gate 172 on `work/gate-171-master-child-parallel-risk-integration-pack-20260402`",
        }
    )
    assert any(
        marker in gate_map
        for marker in {
            "Current active gate: **none — policy/temporal/observability successor pack closed through Gate 170 on `work/gate-164-policy-temporal-observability-pack-20260402`**.",
            "Current active gate: **Gate 172 in the master/child parallel-risk integration pack**.",
        }
    )
    assert (
        "Status: closed policy/temporal/observability successor pack through Gate 170 on `work/gate-164-policy-temporal-observability-pack-20260402`"
        in gates
    )
    assert (
        "Current planned sequence: policy/temporal/observability successor pack closed through Gate 170 on `work/gate-164-policy-temporal-observability-pack-20260402`."
        in checklist
    )
    assert leaves["execution_status"] == "policy_temporal_observability_successor_pack_closed_through_gate_170_on_work_branch"
    assert leaves["active_gate"] == "none"
    assert leaves["remaining_leaf_ids"] == []
    assert leaves["pending_gate_ids"] == []
    assert leaves["completed_gate_ids"] == [
        "Gate 164",
        "Gate 165",
        "Gate 166",
        "Gate 167",
        "Gate 168",
        "Gate 169",
        "Gate 170",
    ]
    for leaf_id in leaves["leaf_order"]:
        assert leaves["leaves"][leaf_id]["status"] == "complete"
    assert "repo_gate170_policy_temporal_observability_successor_pack_closed_workbranch_2026-04-02.zip" in execution_log


def test_gate170_receipt_audits_thread_gold_scope_and_packaging() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    scope_note = SCOPE_NOTE.read_text(encoding="utf-8")

    assert "No new governed vocabulary is admitted in Gate 170." in receipt
    assert "## Audit ledger: thread gold captured or missed" in receipt
    assert "### Workstream 7" in receipt
    assert "### Workstream 8" in receipt
    assert "### Workstream 10" in receipt
    assert "### Workstream 6 (non-risk-lane slice)" in receipt
    assert "### Workstream 9 (non-risk-lane slice)" in receipt
    assert "## Workbook-gold preservation audit" in receipt
    assert "Runtime_Surface_Drivers" in receipt
    assert "Coeff_Universe_Index" in receipt
    assert "Raw_Primitives_Catalog" in receipt
    assert "Derived_Features_Catalog" in receipt
    assert "## Scope-boundary audit" in receipt
    assert "## Documentation-bloat audit" in receipt
    assert "## Planning capture versus runtime implementation truth" in receipt
    assert "repo_gate170_policy_temporal_observability_successor_pack_closed_workbranch_2026-04-02.zip" in receipt
    assert "repo_gate170_policy_temporal_observability_successor_pack_closed_workbranch_2026-04-02.zip" in execution_log
    assert "lean-docs rule" in scope_note
    assert "unknown/not verified" in scope_note
