"""Gate 165 lean policy-law externalisation checks."""

from __future__ import annotations

import json
from pathlib import Path

from ._planning_later_state_helpers import (
    PHASE3_GATE_MAP_MARKERS,
    PHASE3_PLAN_MARKERS,
    contains_any,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-02_POLICY_TEMPORAL_OBSERVABILITY_SUCCESSOR_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-02_POLICY_TEMPORAL_OBSERVABILITY_SUCCESSOR_LEAVES_v1.json"
RECEIPT = REPO_ROOT / "docs/planning/2026-04-02_GATE165_LEAN_POLICY_LAW_EXTERNALISATION.md"
SCOPE_NOTE = REPO_ROOT / "docs/planning/2026-04-02_POLICY_TEMPORAL_OBSERVABILITY_SUCCESSOR_SCOPE_NOTE_v1.md"


def test_gate165_control_surfaces_advance_honestly() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert contains_any(plans, PHASE3_PLAN_MARKERS) or any(
        marker in plans
        for marker in {
            "active gate: Gate 168 on `work/gate-164-policy-temporal-observability-pack-20260402`",
            "no active pack currently routed; policy/temporal/observability successor pack closed through Gate 170 on `work/gate-164-policy-temporal-observability-pack-20260402`",
        }
    )
    assert contains_any(gate_map, PHASE3_GATE_MAP_MARKERS) or any(
        marker in gate_map
        for marker in {
            "Current active gate: **Gate 168 in the policy/temporal/observability successor pack**.",
            "Current active gate: **none — policy/temporal/observability successor pack closed through Gate 170 on `work/gate-164-policy-temporal-observability-pack-20260402`**.",
        }
    )
    assert any(
        marker in gates
        for marker in {
            "Status: active policy/temporal/observability successor pack; Gates 164-167 complete on `work/gate-164-policy-temporal-observability-pack-20260402`, Gate 168 active, Gates 169-170 planned",
            "Status: closed policy/temporal/observability successor pack through Gate 170 on `work/gate-164-policy-temporal-observability-pack-20260402`",
        }
    )
    assert leaves["execution_status"] in {
        "gate_167_complete_gate_168_active_on_work_branch",
        "policy_temporal_observability_successor_pack_closed_through_gate_170_on_work_branch",
    }
    assert leaves["active_gate"] in {"Gate 168", "none"}
    for leaf_id in ["LEAF-G165-001", "LEAF-G165-002", "LEAF-G165-003", "LEAF-G165-004"]:
        assert leaves["leaves"][leaf_id]["status"] == "complete"


def test_gate165_receipt_freezes_live_policy_inventory_and_lean_matrix_schema() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")
    scope_note = SCOPE_NOTE.read_text(encoding="utf-8")

    assert "No new governed vocabulary is admitted in Gate 165." in receipt
    assert "phase_carry" in receipt
    assert "event_options:negative_gamma_stress" in receipt
    assert "event_options:pin_risk" in receipt
    assert "precursor:stand_down_pressure" in receipt
    assert "regime:stressed_weak_breadth" in receipt
    assert "target_fresh_deployable_pct" in receipt
    assert "entry_gate_score_floor" in receipt
    assert "max_risk_per_trade" in receipt
    assert "hedge_required" in receipt
    assert "zone_score_threshold" in receipt
    assert "distance_to_vwap_soft_limit_pct" in receipt
    assert "risk_vix_caution_threshold" in receipt
    assert "risk_vix_hot_threshold" in receipt
    assert "policy_id" in receipt
    assert "precedence_band" in receipt
    assert "trigger_summary" in receipt
    assert "clamp_source" in receipt
    assert "materialisation_status" in receipt
    assert "Fields deliberately **not** added now" in receipt
    assert "DMP v2" in receipt
    assert "unknown / not verified" in receipt
    assert "do not write more policy prose than the repo can actually use" in scope_note
