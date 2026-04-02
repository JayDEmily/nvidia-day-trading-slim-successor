"""Gate 160 owner-stage and activation-state ledger checks."""

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
RECEIPT = (
    REPO_ROOT
    / "docs/planning/2026-04-02_GATE160_OWNER_STAGE_AND_ACTIVATION_STATE_LEDGER.md"
)

ALLOWED_PLAN_MARKERS = {
    "active gate: Gate 161 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`",
    "active gate: Gate 162 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`",
    "active gate: Gate 163 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`",
    "active gate: Gate 163 on `main`",
    "no active pack currently routed; coefficient architecture consolidation pack closed through Gate 163 on `main`",
}

ALLOWED_GATE_MAP_MARKERS = {
    "Current active gate: **Gate 161 in the coefficient architecture consolidation pack**.",
    "Current active gate: **Gate 162 in the coefficient architecture consolidation pack**.",
    "Current active gate: **Gate 163 in the coefficient architecture consolidation pack**.",
    "Current active gate: **none — coefficient architecture consolidation pack closed through Gate 163 on `main`**.",
}


def test_gate160_control_surfaces_advance_honestly() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert any(marker in plans for marker in ALLOWED_PLAN_MARKERS)
    assert any(marker in gate_map for marker in ALLOWED_GATE_MAP_MARKERS)
    assert (
        "Status: active coefficient architecture consolidation pack; Gates 157-160 complete on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`, Gate 161 active, Gates 162-163 planned"
        in gates
        or "Status: active coefficient architecture consolidation pack; Gates 157-161 complete on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`, Gate 162 active, Gate 163 planned"
        in gates
        or "Status: active coefficient architecture consolidation pack; Gates 157-162 complete on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`, Gate 163 active"
        in gates
        or "Status: active coefficient architecture consolidation pack; Gates 157-162 complete on `main`, Gate 163 active"
        in gates
        or "Status: closed coefficient architecture consolidation pack through Gate 163 on `main`"
        in gates
    )
    assert leaves["execution_status"] in {
        "gate_160_complete_gate_161_active_on_work_branch",
        "gate_161_complete_gate_162_active_on_work_branch",
        "gate_162_complete_gate_163_active_on_work_branch",
        "gate_162_complete_gate_163_active_on_main",
        "coefficient_architecture_consolidation_pack_closed_through_gate_163_on_main",
    }
    assert leaves["active_gate"] in {"Gate 161", "Gate 162", "Gate 163", "none"}
    for leaf_id in ["LEAF-G160-001", "LEAF-G160-002", "LEAF-G160-003", "LEAF-G160-004"]:
        assert leaves["leaves"][leaf_id]["status"] == "complete"


def test_gate160_receipt_freezes_owner_stage_activation_state_and_closure_modes() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")

    assert "No new governed vocabulary is admitted in Gate 160." in receipt
    assert "## Activation-state classes frozen by Gate 160" in receipt
    assert "dynamically_active_direct_consumer" in receipt
    assert "governed_baseline_only_direct_consumer" in receipt
    assert "dynamically_active_multi_consumer" in receipt
    assert "## Owner-stage and activation-state ledger for admitted mutable surfaces" in receipt
    assert "entry_gate_score_floor" in receipt
    assert "zone_score_threshold" in receipt
    assert "distance_to_vwap_soft_limit_pct" in receipt
    assert "risk_vix_caution_threshold" in receipt
    assert "risk_vix_hot_threshold" in receipt
    assert "max_risk_per_trade" in receipt
    assert "target_fresh_deployable_pct" in receipt
    assert "hedge_required" in receipt
    assert "## Direct-consumer versus compatibility-carriage interpretation law" in receipt
    assert "modifier_compatibility_bridge" in receipt
    assert "## Mismatch classes frozen by Gate 160" in receipt
    assert "declared_owner_downstream_consumer_drift" in receipt
    assert "declared_owner_later_risk_drift" in receipt
    assert "declared_owner_multi_consumer_overlap" in receipt
    assert "## Allowed closure modes frozen by Gate 160" in receipt
    assert "Rewire consumer truth" in receipt
    assert "Relabel owner truth" in receipt
    assert "Split the surface" in receipt
