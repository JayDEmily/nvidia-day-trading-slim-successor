"""Gate 161 temporal/calendar/event and multi-clock authority mapping checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-02_PARALLEL_RISK_LANE_FOUNDATION_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-02_PARALLEL_RISK_LANE_FOUNDATION_LEAVES_v1.json"
RECEIPT = (
    REPO_ROOT
    / "docs/planning/2026-04-02_GATE161_TEMPORAL_CALENDAR_EVENT_AND_MULTI_CLOCK_AUTHORITY_MAPPING.md"
)


def test_gate161_is_complete_and_gate162_or_later_is_active() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert (
        any(
            f"active gate: Gate {gate} on `work/gate-157-parallel-risk-lane-planning-pack-20260402`"
            in plans
            for gate in (162, 163, 164)
        )
        or "closed through Gate 164 on `work/gate-157-parallel-risk-lane-planning-pack-20260402`"
        in plans
        or "successor retained-test cleanup execution pack; Gate 224 is active" in plans
        or "Gate 224 is complete on `work/gate-224-runtime-review-and-contract-retarget-20260406`" in plans
        or "successor retained-test cleanup execution pack; Gate 225 is active" in plans
        or "no active pack currently routed" in plans
    )
    assert (
        any(
            f"Current active gate: **Gate {gate} in the parallel risk lane foundation pack**."
            in gate_map
            for gate in (162, 163, 164)
        )
        or "Current active gate: **none — parallel risk lane foundation pack closed through Gate 164"
        in gate_map
        or "Current active gate: **Gate 224 active on `work/gate-224-runtime-review-and-contract-retarget-20260406` under the successor retained-test cleanup execution pack.**"
        in gate_map
        or "Current active gate: **No active gate under the successor retained-test cleanup execution pack. Gate 224 is complete on `work/gate-224-runtime-review-and-contract-retarget-20260406`; Gate 225 is not yet activated.**"
        in gate_map
        or "Current active gate: **Gate 225 active on `work/gate-225-retained-test-cleanup-closeout-20260406` under the successor retained-test cleanup execution pack.**"
        in gate_map
        or "Current active gate: **No active gate under the successor retained-test cleanup execution pack. Gate 225 is complete on `work/gate-225-retained-test-cleanup-closeout-20260406`; cleanup pack closed.**"
        in gate_map
    )
    assert "Status: closed parallel risk lane foundation pack through Gate 164" in gates or any(
        label in gates
        for label in (
            "Gates 157-161 complete",
            "Gates 157-162 complete",
            "Gates 157-163 complete",
            "Gates 157-164 complete",
        )
    )
    assert leaves["completed_gate_ids"][:5] == [
        "Gate 157",
        "Gate 158",
        "Gate 159",
        "Gate 160",
        "Gate 161",
    ]


def test_gate161_receipt_freezes_timing_and_multi_clock_authority() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")

    for phrase in [
        "temporal_context",
        "temporal_state",
        "desk_window",
        "clock_envelope",
        "session_phase",
        "behavioural_phase",
        "calendar_horizon_gate",
        "desk_calendar_contract",
        "financial_calendar_reference_bundle",
        "financial_calendar_crosswalk",
        "event_proximity_state",
        "event_window_state",
        "event_overlap_class",
        "event_carry_sensitivity",
        "precursor_universe",
        "precursor_runtime_packet",
        "raw scheduled fact",
        "multi-clock model",
        "slower structural truth",
        "event / calendar truth",
        "tape / translation truth",
        "expression / carry truth",
    ]:
        assert phrase in receipt


def test_gate161_leaves_are_complete_and_validation_specific() -> None:
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    gate161 = {k: v for k, v in leaves["leaves"].items() if v["gate"] == "Gate 161"}
    assert len(gate161) == 4
    for leaf in gate161.values():
        assert leaf["status"] == "complete"
        assert any(
            "tests/test_gate161_temporal_calendar_event_and_multi_clock_authority_mapping.py" in cmd
            for cmd in leaf["validation_commands"]
        )
