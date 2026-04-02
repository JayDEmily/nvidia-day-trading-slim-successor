"""Gate 159 coefficient-world status and inventory-law checks."""

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
    REPO_ROOT / "docs/planning/2026-04-02_GATE159_COEFFICIENT_WORLD_STATUS_AND_INVENTORY_LAW.md"
)

ALLOWED_PLAN_MARKERS = {
    "active gate: Gate 165 on `work/gate-164-policy-temporal-observability-pack-20260402`",
    "active gate: Gate 160 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`",
    "active gate: Gate 161 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`",
    "active gate: Gate 161 on `main`",
    "active gate: Gate 162 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`",
    "active gate: Gate 162 on `main`",
    "active gate: Gate 163 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`",
    "active gate: Gate 163 on `main`",
    "no active pack currently routed; coefficient architecture consolidation pack closed through Gate 163 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`",
    "no active pack currently routed; coefficient architecture consolidation pack closed through Gate 163 on `main`",
}

ALLOWED_GATE_MAP_MARKERS = {
    "Current active gate: **Gate 160 in the coefficient architecture consolidation pack**.",
    "Current active gate: **Gate 161 in the coefficient architecture consolidation pack**.",
    "Current active gate: **Gate 162 in the coefficient architecture consolidation pack**.",
    "Current active gate: **Gate 163 in the coefficient architecture consolidation pack**.",
    "Current active gate: **none — coefficient architecture consolidation pack closed through Gate 163 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`**.",
    "Current active gate: **none — coefficient architecture consolidation pack closed through Gate 163 on `main`**.",
}



def test_gate159_control_surfaces_advance_honestly() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert any(marker in plans for marker in ALLOWED_PLAN_MARKERS)
    assert any(marker in gate_map for marker in ALLOWED_GATE_MAP_MARKERS)
    assert (
        "Status: active coefficient architecture consolidation pack; Gates 157-159 complete on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`, Gate 160 active, Gates 161-163 planned"
        in gates
        or "Status: active coefficient architecture consolidation pack; Gates 157-160 complete on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`, Gate 161 active, Gates 162-163 planned"
        in gates
        or "Status: active coefficient architecture consolidation pack; Gates 157-160 complete on `main`, Gate 161 active, Gates 162-163 planned"
        in gates
        or "Status: active coefficient architecture consolidation pack; Gates 157-161 complete on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`, Gate 162 active, Gate 163 planned"
        in gates
        or "Status: active coefficient architecture consolidation pack; Gates 157-161 complete on `main`, Gate 162 active, Gate 163 planned"
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
        "gate_159_complete_gate_160_active_on_work_branch",
        "gate_160_complete_gate_161_active_on_work_branch",
        "gate_160_complete_gate_161_active_on_main",
        "gate_161_complete_gate_162_active_on_work_branch",
        "gate_161_complete_gate_162_active_on_main",
        "gate_162_complete_gate_163_active_on_work_branch",
        "gate_162_complete_gate_163_active_on_main",
        "coefficient_architecture_consolidation_pack_closed_through_gate_163_on_work_branch",
        "coefficient_architecture_consolidation_pack_closed_through_gate_163_on_main",
    }
    assert leaves["active_gate"] in {"Gate 160", "Gate 161", "Gate 162", "Gate 163", "none"}
    for leaf_id in ["LEAF-G159-001", "LEAF-G159-002", "LEAF-G159-003", "LEAF-G159-004"]:
        assert leaves["leaves"][leaf_id]["status"] == "complete"



def test_gate159_receipt_freezes_coefficient_world_classes_inventory_and_migration_law() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")

    assert "No new governed vocabulary is admitted in Gate 159." in receipt
    assert "## One live coefficient world, stated plainly" in receipt
    assert "config/coefficient_authority.v1.yaml" in receipt
    assert "config/coefficients_registry.example.yaml" in receipt
    assert "## Coefficient-world classification law" in receipt
    assert "live_runtime_authority" in receipt
    assert "reference_registry" in receipt
    assert "provenance_workbook" in receipt
    assert "deferred_candidate" in receipt
    assert "Runtime_Surface_Drivers" in receipt
    assert "Coeff_Universe_Index" in receipt
    assert "## Coefficient-status inventory law" in receipt
    assert "activation_state" in receipt
    assert "## Migration law for workbook and salvage surfaces" in receipt
    assert "do not read workbook tabs directly from runtime" in receipt
