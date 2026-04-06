"""Gate 163 ownership/output/coefficient/anti-duplication law checks."""

from __future__ import annotations

import json
from pathlib import Path

from ._planning_later_state_helpers import (
    CLEANUP_GATE_MAP_MARKERS,
    CLEANUP_PLAN_MARKERS,
    contains_any,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-02_PARALLEL_RISK_LANE_FOUNDATION_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-02_PARALLEL_RISK_LANE_FOUNDATION_LEAVES_v1.json"
RECEIPT = (
    REPO_ROOT
    / "docs/planning/2026-04-02_GATE163_OWNERSHIP_OUTPUT_COEFFICIENT_AND_ANTI_DUPLICATION_LAW.md"
)


def test_gate163_is_complete_and_gate164_is_active() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert (
        contains_any(plans, CLEANUP_PLAN_MARKERS)
        or
        "active gate: Gate 164 on `work/gate-157-parallel-risk-lane-planning-pack-20260402`"
        in plans
        or "closed through Gate 164 on `work/gate-157-parallel-risk-lane-planning-pack-20260402`"
        in plans
    )
    assert (
        contains_any(gate_map, CLEANUP_GATE_MAP_MARKERS)
        or
        "Current active gate: **Gate 164 in the parallel risk lane foundation pack**." in gate_map
        or "Current active gate: **none — parallel risk lane foundation pack closed through Gate 164"
        in gate_map
    )
    assert "Status: closed parallel risk lane foundation pack through Gate 164" in gates or any(
        label in gates for label in ("Gates 157-163 complete", "Gates 157-164 complete")
    )
    assert leaves["active_gate"] in {"Gate 164", "none"}
    assert leaves["execution_status"] in {
        "gate_163_complete_gate_164_active_on_work_branch",
        "parallel_risk_lane_foundation_pack_closed_through_gate_164_on_work_branch",
    }
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


def test_gate163_receipt_freezes_ownership_output_richness_and_anti_duplication_law() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")

    for phrase in [
        "environmental risk weather",
        "candidate-specific risk audit",
        "structural fragility",
        "dependency fragility",
        "event fragility",
        "translation fragility",
        "timing fragility",
        "carry fragility",
        "execution fragility",
        "not at all",
        "wait / defer",
        "smaller",
        "normal",
        "more assertive",
        "reshape",
        "hedge-required",
        "no-carry",
        "distributed caution fog",
        "conservative sludge machine",
    ]:
        assert phrase in receipt


def test_gate163_leaves_are_complete_and_validation_specific() -> None:
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    gate163 = {k: v for k, v in leaves["leaves"].items() if v["gate"] == "Gate 163"}
    assert len(gate163) == 5
    for leaf in gate163.values():
        assert leaf["status"] == "complete"
        assert any(
            "tests/test_gate163_ownership_output_coefficient_and_anti_duplication_law.py" in cmd
            for cmd in leaf["validation_commands"]
        )
