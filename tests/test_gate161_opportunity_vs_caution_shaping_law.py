"""Gate 161 opportunity-versus-caution shaping law checks."""

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
GATES = REPO_ROOT / "docs/planning/2026-04-02_COEFFICIENT_ARCHITECTURE_CONSOLIDATION_GATES_v1.md"
LEAVES = (
    REPO_ROOT / "docs/planning/2026-04-02_COEFFICIENT_ARCHITECTURE_CONSOLIDATION_LEAVES_v1.json"
)
RECEIPT = (
    REPO_ROOT
    / "docs/planning/2026-04-02_GATE161_OPPORTUNITY_VS_CAUTION_SHAPING_LAW.md"
)

ALLOWED_PLAN_MARKERS = {
    "active gate: Gate 165 on `work/gate-164-policy-temporal-observability-pack-20260402`",
    "active gate: Gate 166 on `work/gate-164-policy-temporal-observability-pack-20260402`",
    "active gate: Gate 167 on `work/gate-164-policy-temporal-observability-pack-20260402`",
    "active gate: Gate 168 on `work/gate-164-policy-temporal-observability-pack-20260402`",
    "active gate: Gate 169 on `work/gate-164-policy-temporal-observability-pack-20260402`",
    "active gate: Gate 170 on `work/gate-164-policy-temporal-observability-pack-20260402`",
    "active gate: Gate 162 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`",
    "active gate: Gate 163 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`",
    "active gate: Gate 163 on `main`",
    "no active pack currently routed; coefficient architecture consolidation pack closed through Gate 163 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`",
    "no active pack currently routed; coefficient architecture consolidation pack closed through Gate 163 on `main`",
}

ALLOWED_GATE_MAP_MARKERS = {
    "Current active gate: **Gate 162 in the coefficient architecture consolidation pack**.",
    "Current active gate: **Gate 163 in the coefficient architecture consolidation pack**.",
    "Current active gate: **none — coefficient architecture consolidation pack closed through Gate 163 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`**.",
    "Current active gate: **none — coefficient architecture consolidation pack closed through Gate 163 on `main`**.",
}


def test_gate161_control_surfaces_advance_honestly() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert contains_any(plans, ALLOWED_PLAN_MARKERS | CLEANUP_PLAN_MARKERS | OPENING_POSITION_PLAN_MARKERS)
    assert contains_any(gate_map, ALLOWED_GATE_MAP_MARKERS | CLEANUP_GATE_MAP_MARKERS | OPENING_POSITION_GATE_MAP_MARKERS)
    assert (
        "Status: active coefficient architecture consolidation pack; Gates 157-161 complete on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`, Gate 162 active, Gate 163 planned"
        in gates
        or "Status: active coefficient architecture consolidation pack; Gates 157-162 complete on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`, Gate 163 active"
        in gates
        or "Status: active coefficient architecture consolidation pack; Gates 157-162 complete on `main`, Gate 163 active"
        in gates
        or "Status: closed coefficient architecture consolidation pack through Gate 163 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`"
        in gates
        or "Status: closed coefficient architecture consolidation pack through Gate 163 on `main`"
        in gates
    )
    assert leaves["execution_status"] in {
        "gate_161_complete_gate_162_active_on_work_branch",
        "gate_162_complete_gate_163_active_on_work_branch",
        "gate_162_complete_gate_163_active_on_main",
        "coefficient_architecture_consolidation_pack_closed_through_gate_163_on_work_branch",
        "coefficient_architecture_consolidation_pack_closed_through_gate_163_on_main",
    }
    assert leaves["active_gate"] in {"Gate 162", "Gate 163", "none"}
    for leaf_id in ["LEAF-G161-001", "LEAF-G161-002", "LEAF-G161-003", "LEAF-G161-004"]:
        assert leaves["leaves"][leaf_id]["status"] == "complete"


def test_gate161_receipt_freezes_caution_reality_upstream_path_and_non_duplication() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")

    assert "No new governed vocabulary is admitted in Gate 161." in receipt
    assert "## Current live reality: the modifier plane is caution-heavy" in receipt
    assert "target_fresh_deployable_pct" in receipt
    assert "entry_gate_score_floor" in receipt
    assert "max_risk_per_trade" in receipt
    assert "hedge_required" in receipt
    assert "zone_score_threshold" in receipt
    assert "distance_to_vwap_soft_limit_pct" in receipt
    assert "risk_vix_caution_threshold" in receipt
    assert "risk_vix_hot_threshold" in receipt
    assert "## Upstream opportunity path frozen by Gate 161" in receipt
    assert "Raw_Primitives_Catalog" in receipt
    assert "Options_Chain_Raw_Spec" in receipt
    assert "Volume_Baseline_Raw_Spec" in receipt
    assert "Derived_Features_Catalog" in receipt
    assert "Playbook_Module_Audit" in receipt
    assert "Gate_41_44_Summary" in receipt
    assert "Test_Use_Cases" in receipt
    assert "## Opportunity-versus-caution separation law" in receipt
    assert "## Bounded-surface discipline frozen by Gate 161" in receipt
    assert "## Non-duplication law against the independent risk lane" in receipt
