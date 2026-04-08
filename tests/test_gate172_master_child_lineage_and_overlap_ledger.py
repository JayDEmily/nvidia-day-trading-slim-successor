"""Gate 172 master/child lineage and overlap ledger checks."""

from __future__ import annotations

import json
from pathlib import Path

from ._planning_later_state_helpers import (
    CLEANUP_GATE_MAP_MARKERS,
    CLEANUP_PLAN_MARKERS,
    OPENING_POSITION_GATE_MAP_MARKERS,
    OPENING_POSITION_PLAN_MARKERS,
    PHASE3_GATE_MAP_MARKERS,
    PHASE3_PLAN_MARKERS,
    contains_any,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-02_MASTER_CHILD_PARALLEL_RISK_INTEGRATION_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-02_MASTER_CHILD_PARALLEL_RISK_INTEGRATION_LEAVES_v1.json"
RECEIPT = REPO_ROOT / "docs/planning/2026-04-02_GATE172_MASTER_CHILD_LINEAGE_AND_OVERLAP_LEDGER.md"


def test_gate172_is_complete_and_pack_has_moved_to_gate176_or_later() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert (
        contains_any(plans, PHASE3_PLAN_MARKERS | CLEANUP_PLAN_MARKERS | OPENING_POSITION_PLAN_MARKERS)
        or "active gate: Gate 176 on `work/gate-171-master-child-parallel-risk-integration-pack-20260402`" in plans
        or "closed through Gate 180" in plans
    )
    assert (
        contains_any(gate_map, PHASE3_GATE_MAP_MARKERS | CLEANUP_GATE_MAP_MARKERS | OPENING_POSITION_GATE_MAP_MARKERS)
        or "Current active gate: **Gate 176 in the master/child parallel-risk integration pack**." in gate_map
        or "Current active gate: **none — master/child parallel-risk integration pack closed through Gate 180" in gate_map
    )
    assert "Gate 172 | complete" in gates
    assert leaves["active_gate"] in {"Gate 176", "Gate 177", "Gate 178", "Gate 179", "Gate 180", "none"}
    assert leaves["completed_gate_ids"][:2] == ["Gate 171", "Gate 172"]


def test_gate172_receipt_freezes_shared_base_commit_ranges_and_manual_merge_law() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")
    for phrase in [
        "4640f70",
        "b73c306",
        "0e3a300",
        "fc4ea50",
        "fad9a68",
        "a6790b4",
        "5d5590e",
        "5634036",
        "ad32306",
        "ff8f32c",
        "1bec0e2",
        "ce3f373",
        "ef165c8",
        "no verified `src/` runtime delta",
        "manual merge law",
        "Master remains canonical",
        "child wins on parallel-risk planning law",
    ]:
        assert phrase in receipt
