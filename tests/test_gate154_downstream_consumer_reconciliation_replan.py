"""Gate 154 downstream consumer reconciliation replanning checks."""

from __future__ import annotations

import json
from pathlib import Path

from ._planning_later_state_helpers import (
    CLEANUP_GATE_MAP_MARKERS,
    CLEANUP_PLAN_MARKERS,
    PHASE3_GATE_MAP_MARKERS,
    PHASE3_PLAN_MARKERS,
    contains_any,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-02_STAGE_LOCAL_HANDOFF_CORRECTIVE_SUCCESSOR_GATES_v1.md"
LEAVES = (
    REPO_ROOT / "docs/planning/2026-04-02_STAGE_LOCAL_HANDOFF_CORRECTIVE_SUCCESSOR_LEAVES_v1.json"
)
RECEIPT = (
    REPO_ROOT / "docs/planning/2026-04-02_GATE154_DOWNSTREAM_CONSUMER_RECONCILIATION_REPLAN.md"
)


def test_gate154_control_surfaces_advance_honestly() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert contains_any(plans, PHASE3_PLAN_MARKERS | CLEANUP_PLAN_MARKERS) or (
        "active gate: Gate 155 on `main`" in plans
        or "active gate: Gate 156 on `main`" in plans
        or "no active pack currently routed; stage-local handoff corrective successor pack closed through Gate 156 on `main`"
        in plans
    )
    assert contains_any(gate_map, PHASE3_GATE_MAP_MARKERS | CLEANUP_GATE_MAP_MARKERS) or (
        "Current active gate: **Gate 155 in the stage-local handoff corrective successor pack**."
        in gate_map
        or "Current active gate: **Gate 156 in the stage-local handoff corrective successor pack**."
        in gate_map
        or "Current active gate: **none — stage-local handoff corrective successor pack closed through Gate 156 on `main`**."
        in gate_map
    )
    assert (
        "Status: active stage-local handoff corrective successor pack; Gates 150-154 complete on `main`, Gate 155 active, Gate 156 planned"
        in gates
        or "Status: active stage-local handoff corrective successor pack; Gates 150-155 complete on `main`, Gate 156 active"
        in gates
        or "Status: closed stage-local handoff corrective successor pack through Gate 156 on `main`"
        in gates
    )
    assert leaves["execution_status"] in {
        "gate_154_complete_gate_155_active_on_main",
        "gate_155_complete_gate_156_active_on_main",
        "stage_local_handoff_corrective_successor_pack_closed_through_gate_156_on_main",
    }
    assert leaves["active_gate"] in {"Gate 155", "Gate 156", "none"}
    for leaf_id in ["LEAF-G154-001", "LEAF-G154-002", "LEAF-G154-003", "LEAF-G154-004"]:
        assert leaves["leaves"][leaf_id]["status"] == "complete"


def test_gate154_receipt_freezes_exact_consumers_and_residual_compatibility_dependencies() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")

    assert "No new governed vocabulary is admitted in Gate 154." in receipt
    assert "## Exact downstream consumer set" in receipt
    assert "ReviewExplanationService.evaluate(...)" in receipt
    assert "BoundedTraceRunResult.final_risk_action" in receipt
    assert "ReviewPacketService.daily_packet(...)` in `review_packets.py`" in receipt
    assert (
        "`/review/daily-packet` and `/review/module-health/{module_id}` routes in `api/app.py`"
        in receipt
    )
    assert "## Residual compatibility dependency law" in receipt
    assert (
        'a consumer is not "reconciled" merely because preserved-seam fields were exposed nearby'
        in receipt
    )
    assert (
        "Gate 154 does **not** claim that replay or every legacy consumer is already migrated."
        in receipt
    )
