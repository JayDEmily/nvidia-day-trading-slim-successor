"""Gate 158 co-resident independent parallel risk lane law checks."""

from __future__ import annotations

import json
from pathlib import Path

from ._planning_later_state_helpers import (
    CLEANUP_GATE_MAP_MARKERS,
    CLEANUP_PLAN_MARKERS,
    OPENING_POSITION_GATE_MAP_MARKERS,
    OPENING_POSITION_PLAN_MARKERS,
    contains_any,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-02_PARALLEL_RISK_LANE_FOUNDATION_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-02_PARALLEL_RISK_LANE_FOUNDATION_LEAVES_v1.json"
EXECUTION_LOG = (
    REPO_ROOT / "docs/planning/2026-04-02_PARALLEL_RISK_LANE_FOUNDATION_EXECUTION_LOG_v1.md"
)
RECEIPT = REPO_ROOT / "docs/planning/2026-04-02_GATE158_CO_RESIDENT_PARALLEL_RISK_LANE_LAW.md"
NORMATIVE = REPO_ROOT / "docs/01_NORMATIVE.md"
OPERATING_MODEL = REPO_ROOT / "docs/02_OPERATING_MODEL.md"
VOCAB = REPO_ROOT / "docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json"


def test_gate158_is_complete_and_router_has_moved_on() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert (
        contains_any(plans, CLEANUP_PLAN_MARKERS | OPENING_POSITION_PLAN_MARKERS)
        or
        any(
            f"active gate: Gate {gate} on `work/gate-157-parallel-risk-lane-planning-pack-20260402`"
            in plans
            for gate in (159, 160, 161, 162, 163, 164)
        )
        or "closed through Gate 164 on `work/gate-157-parallel-risk-lane-planning-pack-20260402`"
        in plans
    )
    assert (
        contains_any(gate_map, CLEANUP_GATE_MAP_MARKERS | OPENING_POSITION_GATE_MAP_MARKERS)
        or
        any(
            f"Current active gate: **Gate {gate} in the parallel risk lane foundation pack**."
            in gate_map
            for gate in (159, 160, 161, 162, 163, 164)
        )
        or "Current active gate: **none — parallel risk lane foundation pack closed through Gate 164"
        in gate_map
    )
    assert "Status: closed parallel risk lane foundation pack through Gate 164" in gates or any(
        label in gates
        for label in (
            "Gates 157-158 complete",
            "Gates 157-159 complete",
            "Gates 157-160 complete",
            "Gates 157-161 complete",
            "Gates 157-162 complete",
            "Gates 157-163 complete",
            "Gates 157-164 complete",
        )
    )
    assert leaves["completed_gate_ids"][:2] == ["Gate 157", "Gate 158"]
    assert leaves["execution_status"] in {
        "gate_158_complete_gate_159_active_on_work_branch",
        "gate_159_complete_gate_160_active_on_work_branch",
        "gate_160_complete_gate_161_active_on_work_branch",
        "gate_161_complete_gate_162_active_on_work_branch",
        "gate_162_complete_gate_163_active_on_work_branch",
        "gate_163_complete_gate_164_active_on_work_branch",
        "parallel_risk_lane_foundation_pack_closed_through_gate_164_on_work_branch",
    }
    assert any(
        label in execution_log
        for label in (
            "Gates 157-158 complete",
            "Gates 157-159 complete",
            "Gates 157-160 complete",
            "Gates 157-161 complete",
            "Gates 157-162 complete",
            "Gates 157-163 complete",
            "Gates 157-164 complete",
            "closed execution log for the parallel risk lane foundation pack through Gate 164",
        )
    )


def test_gate158_freezes_co_resident_lane_law_without_stage_inflation() -> None:
    normative = NORMATIVE.read_text(encoding="utf-8")
    operating = OPERATING_MODEL.read_text(encoding="utf-8")
    receipt = RECEIPT.read_text(encoding="utf-8")
    vocab = json.loads(VOCAB.read_text(encoding="utf-8"))

    assert "## First-class co-resident independent parallel risk lane (planning law)" in normative
    assert "numbered stage" in normative
    assert "`1.1`" in normative
    assert "step_8" in normative
    assert "approved invariant surfaces directly from session start" in normative
    assert "approved stage outputs only after those stages have produced them" in normative
    assert (
        "review surfaces must be able to reconstruct the lane's reasoning and state progression"
        in normative
    )

    assert "## Co-resident independent parallel risk lane (planning placement)" in operating
    assert "starts with session start" in operating
    assert "preserves the serial desk cognition grammar" in operating

    index = {entry["canonical_slug"]: entry for entry in vocab["entries"]}
    lane = index["independent_parallel_risk_lane"]
    assert "parallel risk pipeline" in lane["allowed_aliases"]
    assert "step_1_1" in lane["disallowed_phrases"]
    assert "step_8" in lane["disallowed_phrases"]

    assert "Approved direct reads from session start" in receipt
    assert "Approved later reads" in receipt
    assert "Forbidden bypasses" in receipt
    assert "Session-start concurrency and review visibility" in receipt


def test_gate158_receipt_and_leaves_preserve_scope_boundary() -> None:
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    receipt = RECEIPT.read_text(encoding="utf-8")
    gate158 = {k: v for k, v in leaves["leaves"].items() if v["gate"] == "Gate 158"}

    assert len(gate158) == 4
    for leaf in gate158.values():
        assert leaf["status"] == "complete"
        assert any(
            "tests/test_gate158_co_resident_parallel_risk_lane_law.py" in cmd
            for cmd in leaf["validation_commands"]
        )

    for phrase in [
        "not the arbiter",
        "not a second playbook engine",
        "no runtime packet is claimed",
        "does not implement the lane",
    ]:
        assert phrase in receipt
