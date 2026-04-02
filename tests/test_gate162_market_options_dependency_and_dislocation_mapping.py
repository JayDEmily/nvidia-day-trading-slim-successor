"""Gate 162 market/options/dependency/dislocation mapping checks."""

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
    / "docs/planning/2026-04-02_GATE162_MARKET_OPTIONS_DEPENDENCY_AND_DISLOCATION_MAPPING.md"
)


def test_gate162_is_complete_and_gate163_or_164_is_active() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert (
        any(
            f"active gate: Gate {gate} on `work/gate-157-parallel-risk-lane-planning-pack-20260402`"
            in plans
            for gate in (163, 164)
        )
        or "closed through Gate 164 on `work/gate-157-parallel-risk-lane-planning-pack-20260402`"
        in plans
    )
    assert (
        any(
            f"Current active gate: **Gate {gate} in the parallel risk lane foundation pack**."
            in gate_map
            for gate in (163, 164)
        )
        or "Current active gate: **none — parallel risk lane foundation pack closed through Gate 164"
        in gate_map
    )
    assert "Status: closed parallel risk lane foundation pack through Gate 164" in gates or any(
        label in gates
        for label in ("Gates 157-162 complete", "Gates 157-163 complete", "Gates 157-164 complete")
    )
    assert leaves["completed_gate_ids"][:6] == [
        "Gate 157",
        "Gate 158",
        "Gate 159",
        "Gate 160",
        "Gate 161",
        "Gate 162",
    ]


def test_gate162_receipt_freezes_market_translation_dependency_and_dislocation_concepts() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")

    for phrase in [
        "market_regime_context",
        "beta_leadership_score",
        "cross_asset_pressure_score",
        "options and flow context",
        "term_structure_state",
        "dealer_pressure_state",
        "flow_tension_score",
        "headline is not the trade",
        "direct read-through",
        "active enough to matter now",
        "dislocation",
        "justified repricing",
        "impairment",
        "price alone cannot answer that question",
    ]:
        assert phrase in receipt


def test_gate162_leaves_are_complete_and_validation_specific() -> None:
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    gate162 = {k: v for k, v in leaves["leaves"].items() if v["gate"] == "Gate 162"}
    assert len(gate162) == 5
    for leaf in gate162.values():
        assert leaf["status"] == "complete"
        assert any(
            "tests/test_gate162_market_options_dependency_and_dislocation_mapping.py" in cmd
            for cmd in leaf["validation_commands"]
        )
