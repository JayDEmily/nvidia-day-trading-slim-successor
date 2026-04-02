"""Gate 162 successor implementation routing checks."""

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
SCOPE_NOTE = (
    REPO_ROOT / "docs/planning/2026-04-02_COEFFICIENT_ARCHITECTURE_CONSOLIDATION_SCOPE_NOTE_v1.md"
)
RECEIPT = (
    REPO_ROOT
    / "docs/planning/2026-04-02_GATE162_SUCCESSOR_IMPLEMENTATION_ROUTING_FOR_WORKSTREAMS_1_4.md"
)

ALLOWED_PLAN_MARKERS = {
    "active gate: Gate 165 on `work/gate-164-policy-temporal-observability-pack-20260402`",
    "active gate: Gate 166 on `work/gate-164-policy-temporal-observability-pack-20260402`",
    "active gate: Gate 167 on `work/gate-164-policy-temporal-observability-pack-20260402`",
    "active gate: Gate 168 on `work/gate-164-policy-temporal-observability-pack-20260402`",
    "active gate: Gate 169 on `work/gate-164-policy-temporal-observability-pack-20260402`",
    "active gate: Gate 170 on `work/gate-164-policy-temporal-observability-pack-20260402`",
    "active gate: Gate 163 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`",
    "active gate: Gate 163 on `main`",
    "no active pack currently routed; coefficient architecture consolidation pack closed through Gate 163 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`",
    "no active pack currently routed; coefficient architecture consolidation pack closed through Gate 163 on `main`",
}

ALLOWED_GATE_MAP_MARKERS = {
    "Current active gate: **Gate 163 in the coefficient architecture consolidation pack**.",
    "Current active gate: **none — coefficient architecture consolidation pack closed through Gate 163 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`**.",
    "Current active gate: **none — coefficient architecture consolidation pack closed through Gate 163 on `main`**.",
}


def test_gate162_control_surfaces_advance_honestly() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert any(marker in plans for marker in ALLOWED_PLAN_MARKERS)
    assert any(marker in gate_map for marker in ALLOWED_GATE_MAP_MARKERS)
    assert (
        "Status: active coefficient architecture consolidation pack; Gates 157-162 complete on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`, Gate 163 active"
        in gates
        or "Status: active coefficient architecture consolidation pack; Gates 157-162 complete on `main`, Gate 163 active"
        in gates
        or "Status: closed coefficient architecture consolidation pack through Gate 163 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`"
        in gates
        or "Status: closed coefficient architecture consolidation pack through Gate 163 on `main`"
        in gates
    )
    assert leaves["execution_status"] in {
        "gate_162_complete_gate_163_active_on_work_branch",
        "gate_162_complete_gate_163_active_on_main",
        "coefficient_architecture_consolidation_pack_closed_through_gate_163_on_work_branch",
        "coefficient_architecture_consolidation_pack_closed_through_gate_163_on_main",
    }
    assert leaves["active_gate"] in {"Gate 163", "none"}
    for leaf_id in ["LEAF-G162-001", "LEAF-G162-002", "LEAF-G162-003", "LEAF-G162-004"]:
        assert leaves["leaves"][leaf_id]["status"] == "complete"


def test_gate162_receipt_freezes_successor_order_move_together_rules_and_risk_lane_boundary() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")
    scope_note = SCOPE_NOTE.read_text(encoding="utf-8")

    assert "No new governed vocabulary is admitted in Gate 162." in receipt
    assert "## Successor implementation order frozen by Gate 162" in receipt
    assert "Step 1 — Materialise the coefficient-status inventory from Gate 159" in receipt
    assert "Step 2 — Close owner-stage truth for admitted mutable surfaces" in receipt
    assert "Step 3 — Resolve baseline-only versus dynamically-active truth" in receipt
    assert "Step 4 — Tighten the upstream opportunity path without widening knobs" in receipt
    assert "Step 5 — Only then decide whether any new governed surface is justified" in receipt
    assert "## Mandatory move-together rules" in receipt
    assert "config/coefficient_authority.v1.yaml" in receipt
    assert "src/nvda_desk/config_models.py" in receipt
    assert "docs/03_DOMAIN_MODEL.md" in receipt
    assert "## Hard stop rules before widening live behaviour" in receipt
    assert "## Successor boundary against the independent risk-lane thread" in receipt
    assert "Allowed coordination seam" in receipt
    assert "implementation routing" in scope_note
    assert "independent risk-lane successor boundary" in scope_note
