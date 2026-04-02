"""Gate 157 coefficient architecture consolidation pack planning checks."""

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
    REPO_ROOT
    / "docs/planning/2026-04-02_COEFFICIENT_ARCHITECTURE_CONSOLIDATION_DOCUMENT_TOUCH_CHECKLIST_v1.md"
)
SCOPE_NOTE = (
    REPO_ROOT / "docs/planning/2026-04-02_COEFFICIENT_ARCHITECTURE_CONSOLIDATION_SCOPE_NOTE_v1.md"
)
RECEIPT = REPO_ROOT / "docs/planning/2026-04-02_GATE157_COEFFICIENT_ARCHITECTURE_CONSOLIDATION_PACK_BOOTSTRAP.md"

ALLOWED_CURRENT_GATE_MARKERS = {
    "Current active gate: **Gate 165 in the policy/temporal/observability successor pack**.",
    'Current active gate: **Gate 158 in the coefficient architecture consolidation pack**.',
    'Current active gate: **Gate 159 in the coefficient architecture consolidation pack**.',
    'Current active gate: **Gate 160 in the coefficient architecture consolidation pack**.',
    'Current active gate: **Gate 161 in the coefficient architecture consolidation pack**.',
    'Current active gate: **Gate 162 in the coefficient architecture consolidation pack**.',
    'Current active gate: **Gate 163 in the coefficient architecture consolidation pack**.',
    'Current active gate: **none — coefficient architecture consolidation pack closed through Gate 163 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`**.',
    'Current active gate: **none — coefficient architecture consolidation pack closed through Gate 163 on `main`**.',
}

ALLOWED_PLAN_MARKERS = {
    "active gate: Gate 165 on `work/gate-164-policy-temporal-observability-pack-20260402`",
    "active gate: Gate 158 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`",
    "active gate: Gate 159 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`",
    "active gate: Gate 160 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`",
    "active gate: Gate 161 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`",
    "active gate: Gate 161 on `main`",
    "active gate: Gate 162 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`",
    "active gate: Gate 162 on `main`",
    "active gate: Gate 163 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`",
    "active gate: Gate 163 on `main`",
    "no active pack currently routed; coefficient architecture consolidation pack closed through Gate 163 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`",
    "no active pack currently routed; coefficient architecture consolidation pack closed through Gate 163 on `main`",
}

ALLOWED_GATE_STATUS = {
    "Status: active coefficient architecture consolidation pack; Gate 157 complete on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`, Gate 158 active, Gates 159-163 planned",
    "Status: active coefficient architecture consolidation pack; Gates 157-158 complete on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`, Gate 159 active, Gates 160-163 planned",
    "Status: active coefficient architecture consolidation pack; Gates 157-159 complete on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`, Gate 160 active, Gates 161-163 planned",
    "Status: active coefficient architecture consolidation pack; Gates 157-160 complete on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`, Gate 161 active, Gates 162-163 planned",
    "Status: active coefficient architecture consolidation pack; Gates 157-160 complete on `main`, Gate 161 active, Gates 162-163 planned",
    "Status: active coefficient architecture consolidation pack; Gates 157-161 complete on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`, Gate 162 active, Gate 163 planned",
    "Status: active coefficient architecture consolidation pack; Gates 157-161 complete on `main`, Gate 162 active, Gate 163 planned",
    "Status: active coefficient architecture consolidation pack; Gates 157-162 complete on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`, Gate 163 active",
    "Status: active coefficient architecture consolidation pack; Gates 157-162 complete on `main`, Gate 163 active",
    "Status: closed coefficient architecture consolidation pack through Gate 163 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`",
    "Status: closed coefficient architecture consolidation pack through Gate 163 on `main`",
}


def test_gate157_pack_is_active_and_non_placeholder() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    scope_note = SCOPE_NOTE.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert "2026-04-02_COEFFICIENT_ARCHITECTURE_CONSOLIDATION_GATES_v1.md" in plans
    assert "2026-04-02_COEFFICIENT_ARCHITECTURE_CONSOLIDATION_LEAVES_v1.json" in plans
    assert "2026-04-02_COEFFICIENT_ARCHITECTURE_CONSOLIDATION_EXECUTION_LOG_v1.md" in plans
    assert "2026-04-02_COEFFICIENT_ARCHITECTURE_CONSOLIDATION_DOCUMENT_TOUCH_CHECKLIST_v1.md" in plans
    assert "2026-04-02_COEFFICIENT_ARCHITECTURE_CONSOLIDATION_SCOPE_NOTE_v1.md" in plans
    assert any(marker in plans for marker in ALLOWED_PLAN_MARKERS)
    assert any(marker in gate_map for marker in ALLOWED_CURRENT_GATE_MARKERS)
    assert any(marker in gates for marker in ALLOWED_GATE_STATUS)
    assert leaves["execution_status"] in {
        "gate_157_complete_gate_158_active_on_work_branch",
        "gate_158_complete_gate_159_active_on_main",
        "gate_159_complete_gate_160_active_on_work_branch",
        "gate_159_complete_gate_160_active_on_main",
        "gate_160_complete_gate_161_active_on_work_branch",
        "gate_160_complete_gate_161_active_on_main",
        "gate_161_complete_gate_162_active_on_work_branch",
        "gate_161_complete_gate_162_active_on_main",
        "gate_162_complete_gate_163_active_on_work_branch",
        "gate_162_complete_gate_163_active_on_main",
        "coefficient_architecture_consolidation_pack_closed_through_gate_163_on_work_branch",
        "coefficient_architecture_consolidation_pack_closed_through_gate_163_on_main",
    }
    assert leaves["active_gate"] in {"Gate 158", "Gate 159", "Gate 160", "Gate 161", "Gate 162", "Gate 163", "none"}
    assert leaves["completed_gate_ids"] in (
        ["Gate 157"],
        ["Gate 157", "Gate 158"],
        ["Gate 157", "Gate 158", "Gate 159"],
        ["Gate 157", "Gate 158", "Gate 159", "Gate 160"],
        ["Gate 157", "Gate 158", "Gate 159", "Gate 160", "Gate 161"],
        ["Gate 157", "Gate 158", "Gate 159", "Gate 160", "Gate 161", "Gate 162"],
        ["Gate 157", "Gate 158", "Gate 159", "Gate 160", "Gate 161", "Gate 162", "Gate 163"],
    )
    assert leaves["completed_leaf_ids"][:4] == [
        "LEAF-G157-001",
        "LEAF-G157-002",
        "LEAF-G157-003",
        "LEAF-G157-004",
    ]
    assert execution_log.startswith("# 2026-04-02_COEFFICIENT_ARCHITECTURE_CONSOLIDATION_EXECUTION_LOG_v1")
    assert "Workstreams 1-4" in scope_note
    assert "Gate 157" in checklist


def test_gate157_future_leaves_are_materially_detailed_and_audit_gate_exists() -> None:
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))["leaves"]

    future_gate_ids = {"Gate 158", "Gate 159", "Gate 160", "Gate 161", "Gate 162", "Gate 163"}
    future_leaves = [leaf for leaf in leaves.values() if leaf["gate"] in future_gate_ids]

    assert future_leaves
    assert any(leaf["gate"] == "Gate 163" for leaf in future_leaves)
    for leaf in future_leaves:
        assert len(leaf["ordered_actions"]) >= 3
        assert len(leaf["forbidden_actions"]) >= 3
        assert leaf["validation_commands"]
        assert leaf["expected_evidence"]
        assert leaf["definition_of_done"]
        assert leaf["packaging_requirement"]


def test_gate157_receipt_and_scope_note_preserve_workbook_gold_and_risk_lane_boundary() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")
    scope_note = SCOPE_NOTE.read_text(encoding="utf-8")

    assert "The next problem is different." in receipt
    assert "docs/planning/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3.xlsx" in receipt
    assert "independent parallel risk lane" in receipt
    assert "Runtime_Surface_Drivers" in scope_note
    assert "Coeff_Universe_Index" in scope_note
    assert "Raw_Primitives_Catalog" in scope_note
    assert "Derived_Features_Catalog" in scope_note
    assert "Playbook_Module_Audit" in scope_note
