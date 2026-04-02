"""Gate 163 coefficient-architecture consolidation closeout checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-02_COEFFICIENT_ARCHITECTURE_CONSOLIDATION_GATES_v1.md"
LEAVES = (
    REPO_ROOT / "docs/planning/2026-04-02_COEFFICIENT_ARCHITECTURE_CONSOLIDATION_LEAVES_v1.json"
)
EXECUTION_LOG = (
    REPO_ROOT / "docs/planning/2026-04-02_COEFFICIENT_ARCHITECTURE_CONSOLIDATION_EXECUTION_LOG_v1.md"
)
CHECKLIST = (
    REPO_ROOT / "docs/planning/2026-04-02_COEFFICIENT_ARCHITECTURE_CONSOLIDATION_DOCUMENT_TOUCH_CHECKLIST_v1.md"
)
RECEIPT = (
    REPO_ROOT
    / "docs/planning/2026-04-02_GATE163_COEFFICIENT_ARCHITECTURE_CONSOLIDATION_AUDIT_AND_CLOSEOUT.md"
)
SCOPE_NOTE = (
    REPO_ROOT / "docs/planning/2026-04-02_COEFFICIENT_ARCHITECTURE_CONSOLIDATION_SCOPE_NOTE_v1.md"
)


def test_gate163_control_surfaces_close_honestly_on_work_branch() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert any(
        marker in plans
        for marker in {
            "no active pack currently routed; coefficient architecture consolidation pack closed through Gate 163 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`",
            "active gate: Gate 165 on `work/gate-164-policy-temporal-observability-pack-20260402`",
    "active gate: Gate 166 on `work/gate-164-policy-temporal-observability-pack-20260402`",
    "active gate: Gate 167 on `work/gate-164-policy-temporal-observability-pack-20260402`",
    "active gate: Gate 168 on `work/gate-164-policy-temporal-observability-pack-20260402`",
    "active gate: Gate 169 on `work/gate-164-policy-temporal-observability-pack-20260402`",
    "active gate: Gate 170 on `work/gate-164-policy-temporal-observability-pack-20260402`",
            "active gate: Gate 172 on `work/gate-171-master-child-parallel-risk-integration-pack-20260402`",
            "no active pack currently routed; master/child parallel-risk integration pack closed through Gate 180 on `work/gate-171-master-child-parallel-risk-integration-pack-20260402`",
        }
    )
    assert any(
        marker in gate_map
        for marker in {
            "Current active gate: **none — coefficient architecture consolidation pack closed through Gate 163 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`**.",
            "Current active gate: **Gate 165 in the policy/temporal/observability successor pack**.",
    "Current active gate: **Gate 166 in the policy/temporal/observability successor pack**.",
    "Current active gate: **Gate 167 in the policy/temporal/observability successor pack**.",
    "Current active gate: **Gate 168 in the policy/temporal/observability successor pack**.",
    "Current active gate: **Gate 169 in the policy/temporal/observability successor pack**.",
    "Current active gate: **Gate 170 in the policy/temporal/observability successor pack**.",
            "Current active gate: **Gate 172 in the master/child parallel-risk integration pack**.",
            "Current active gate: **none — master/child parallel-risk integration pack closed through Gate 180 on `work/gate-171-master-child-parallel-risk-integration-pack-20260402`**.",
            "Current active gate: **none — policy/temporal/observability successor pack closed through Gate 170 on `work/gate-164-policy-temporal-observability-pack-20260402`**.",
        }
    )
    assert (
        "Status: closed coefficient architecture consolidation pack through Gate 163 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`"
        in gates
    )
    assert (
        "Status: closed execution log for the coefficient architecture consolidation pack through Gate 163 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`"
        in execution_log
    )
    assert (
        "Current planned sequence: coefficient architecture consolidation pack closed through Gate 163 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`."
        in checklist
    )
    assert (
        leaves["execution_status"]
        == "coefficient_architecture_consolidation_pack_closed_through_gate_163_on_work_branch"
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
    ]
    for leaf_id in leaves["leaf_order"]:
        assert leaves["leaves"][leaf_id]["status"] == "complete"


def test_gate163_receipt_audits_thread_to_pack_coverage_and_packaging() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    scope_note = SCOPE_NOTE.read_text(encoding="utf-8")

    assert "No new governed vocabulary is admitted in Gate 163." in receipt
    assert "## Audit ledger: thread-to-pack coverage against the approved brief" in receipt
    assert "### Workstream 1" in receipt
    assert "### Workstream 2" in receipt
    assert "### Workstream 3" in receipt
    assert "### Workstream 4" in receipt
    assert "## Workbook-gold preservation audit" in receipt
    assert "Runtime_Surface_Drivers" in receipt
    assert "Coeff_Universe_Index" in receipt
    assert "Raw_Primitives_Catalog" in receipt
    assert "Derived_Features_Catalog" in receipt
    assert "Playbook_Module_Audit" in receipt
    assert "## Scope-boundary audit" in receipt
    assert "## Drift-defect ledger and resolutions" in receipt
    assert "closed-through-Gate-163-on-work-branch state" in receipt
    assert "## Final proof slice run" in receipt
    assert "passed in" in receipt
    assert "repo_gate163_coefficient_architecture_consolidation_pack_closed_workbranch_2026-04-02.zip" in receipt
    assert "repo_gate163_coefficient_architecture_consolidation_pack_closed_workbranch_2026-04-02.zip" in execution_log
    assert "implementation routing" in scope_note
    assert "independent risk-lane successor boundary" in scope_note
