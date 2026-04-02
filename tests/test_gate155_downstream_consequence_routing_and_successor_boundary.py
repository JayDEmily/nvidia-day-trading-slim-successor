"""Gate 155 downstream consequence routing and successor-boundary checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-02_STAGE_LOCAL_HANDOFF_CORRECTIVE_SUCCESSOR_GATES_v1.md"
LEAVES = (
    REPO_ROOT / "docs/planning/2026-04-02_STAGE_LOCAL_HANDOFF_CORRECTIVE_SUCCESSOR_LEAVES_v1.json"
)
RECEIPT = (
    REPO_ROOT
    / "docs/planning/2026-04-02_GATE155_DOWNSTREAM_CONSEQUENCE_ROUTING_AND_SUCCESSOR_BOUNDARY.md"
)


def test_gate155_control_surfaces_advance_honestly() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert (
        "active gate: Gate 156 on `main`" in plans
        or "no active pack currently routed; stage-local handoff corrective successor pack closed through Gate 156 on `main`"
        in plans
    )
    assert (
        "Current active gate: **Gate 156 in the stage-local handoff corrective successor pack**."
        in gate_map
        or "Current active gate: **none — stage-local handoff corrective successor pack closed through Gate 156 on `main`**."
        in gate_map
    )
    assert (
        "Status: active stage-local handoff corrective successor pack; Gates 150-155 complete on `main`, Gate 156 active"
        in gates
        or "Status: closed stage-local handoff corrective successor pack through Gate 156 on `main`"
        in gates
    )
    assert leaves["execution_status"] in {
        "gate_155_complete_gate_156_active_on_main",
        "stage_local_handoff_corrective_successor_pack_closed_through_gate_156_on_main",
    }
    assert leaves["active_gate"] in {"Gate 156", "none"}
    for leaf_id in ["LEAF-G155-001", "LEAF-G155-002", "LEAF-G155-003"]:
        assert leaves["leaves"][leaf_id]["status"] == "complete"


def test_gate155_receipt_freezes_consequence_ledger_and_successor_boundary() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")

    assert "No new governed vocabulary is admitted in Gate 155." in receipt
    assert "## Downstream consequence ledger" in receipt
    assert "bounded-trace retirement or rename of `final_risk_action`" in receipt
    assert "API daily-review route changes" in receipt
    assert "## Successor-boundary statement" in receipt
    assert "independent parallel risk lane" in receipt
    assert "final arbiter" in receipt
    assert "dynamic-coefficient redesign" in receipt
    assert (
        "After this corrective pack closes, the repo should be in one of two honest states only:"
        in receipt
    )
