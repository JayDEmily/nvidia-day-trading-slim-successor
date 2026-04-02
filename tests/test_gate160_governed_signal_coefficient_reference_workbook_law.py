"""Gate 160 governed signal coefficient reference workbook law checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-02_PARALLEL_RISK_LANE_FOUNDATION_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-02_PARALLEL_RISK_LANE_FOUNDATION_LEAVES_v1.json"
NORMATIVE = REPO_ROOT / "docs/01_NORMATIVE.md"
CONFIG_README = REPO_ROOT / "config/README.md"
REFERENCE_DOC = REPO_ROOT / "docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md"
RECEIPT = (
    REPO_ROOT
    / "docs/planning/2026-04-02_GATE160_GOVERNED_SIGNAL_COEFFICIENT_REFERENCE_WORKBOOK_LAW.md"
)
WORKBOOK = (
    REPO_ROOT
    / "data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx"
)


def test_gate160_is_complete_and_gate161_or_later_is_active() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert (
        any(
            f"active gate: Gate {gate} on `work/gate-157-parallel-risk-lane-planning-pack-20260402`"
            in plans
            for gate in (161, 162, 163, 164)
        )
        or "closed through Gate 164 on `work/gate-157-parallel-risk-lane-planning-pack-20260402`"
        in plans
    )
    assert (
        any(
            f"Current active gate: **Gate {gate} in the parallel risk lane foundation pack**."
            in gate_map
            for gate in (161, 162, 163, 164)
        )
        or "Current active gate: **none — parallel risk lane foundation pack closed through Gate 164"
        in gate_map
    )
    assert "Status: closed parallel risk lane foundation pack through Gate 164" in gates or any(
        label in gates
        for label in (
            "Gates 157-160 complete",
            "Gates 157-161 complete",
            "Gates 157-162 complete",
            "Gates 157-163 complete",
            "Gates 157-164 complete",
        )
    )
    assert leaves["completed_gate_ids"][:4] == ["Gate 157", "Gate 158", "Gate 159", "Gate 160"]
    assert leaves["execution_status"] in {
        "gate_160_complete_gate_161_active_on_work_branch",
        "gate_161_complete_gate_162_active_on_work_branch",
        "gate_162_complete_gate_163_active_on_work_branch",
        "gate_163_complete_gate_164_active_on_work_branch",
        "parallel_risk_lane_foundation_pack_closed_through_gate_164_on_work_branch",
    }


def test_gate160_freezes_discoverability_promotion_and_subset_law() -> None:
    normative = NORMATIVE.read_text(encoding="utf-8")
    config = CONFIG_README.read_text(encoding="utf-8")
    ref_doc = REFERENCE_DOC.read_text(encoding="utf-8")
    receipt = RECEIPT.read_text(encoding="utf-8")

    assert WORKBOOK.exists()
    assert "docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md" in normative
    assert "governed live reference ledger" in ref_doc
    assert "not direct runtime authority" in ref_doc
    assert "workbook_ref" in ref_doc
    assert "Direct runtime reads from the workbook are forbidden." in ref_doc
    assert "Governed signal workbook lineage" in config
    assert "Temporal_Bounds_Draft" in ref_doc
    assert "Runtime_Surface_Drivers" in ref_doc
    assert "Coeff_Universe_Index" in ref_doc
    assert "Bounds_Method" in ref_doc
    assert "Signal_Coeff_Handoff" in ref_doc
    assert "Update classes" in ref_doc
    assert "update classes" in receipt.lower() or "Update classes" in receipt


def test_gate160_leaves_are_complete_and_validation_specific() -> None:
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    gate160 = {k: v for k, v in leaves["leaves"].items() if v["gate"] == "Gate 160"}
    assert len(gate160) == 4
    for leaf in gate160.values():
        assert leaf["status"] == "complete"
        assert any(
            "tests/test_gate160_governed_signal_coefficient_reference_workbook_law.py" in cmd
            for cmd in leaf["validation_commands"]
        )
