"""Gate 158 target-architecture and stage-purity consolidation checks."""

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
    / "docs/planning/2026-04-02_GATE158_TARGET_ARCHITECTURE_AND_STAGE_PURITY_CONSOLIDATION.md"
)

ALLOWED_PLAN_MARKERS = {
    "active gate: Gate 159 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`",
    "active gate: Gate 160 on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`",
    "active gate: Gate 161 on `main`",
    "active gate: Gate 162 on `main`",
    "active gate: Gate 163 on `main`",
    "no active pack currently routed; coefficient architecture consolidation pack closed through Gate 163 on `main`",
}

ALLOWED_GATE_MAP_MARKERS = {
    "Current active gate: **Gate 159 in the coefficient architecture consolidation pack**.",
    "Current active gate: **Gate 160 in the coefficient architecture consolidation pack**.",
    "Current active gate: **Gate 161 in the coefficient architecture consolidation pack**.",
    "Current active gate: **Gate 162 in the coefficient architecture consolidation pack**.",
    "Current active gate: **Gate 163 in the coefficient architecture consolidation pack**.",
    "Current active gate: **none — coefficient architecture consolidation pack closed through Gate 163 on `main`**.",
}



def test_gate158_control_surfaces_advance_honestly() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert any(marker in plans for marker in ALLOWED_PLAN_MARKERS)
    assert any(marker in gate_map for marker in ALLOWED_GATE_MAP_MARKERS)
    assert (
        "Status: active coefficient architecture consolidation pack; Gates 157-158 complete on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`, Gate 159 active, Gates 160-163 planned"
        in gates
        or "Status: active coefficient architecture consolidation pack; Gates 157-159 complete on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`, Gate 160 active, Gates 161-163 planned"
        in gates
        or "Status: active coefficient architecture consolidation pack; Gates 157-160 complete on `main`, Gate 161 active, Gates 162-163 planned"
        in gates
        or "Status: active coefficient architecture consolidation pack; Gates 157-161 complete on `main`, Gate 162 active, Gate 163 planned"
        in gates
        or "Status: active coefficient architecture consolidation pack; Gates 157-162 complete on `main`, Gate 163 active"
        in gates
        or "Status: closed coefficient architecture consolidation pack through Gate 163 on `main`"
        in gates
    )
    assert leaves["execution_status"] in {
        "gate_158_complete_gate_159_active_on_work_branch",
        "gate_159_complete_gate_160_active_on_work_branch",
        "gate_160_complete_gate_161_active_on_main",
        "gate_161_complete_gate_162_active_on_main",
        "gate_162_complete_gate_163_active_on_main",
        "coefficient_architecture_consolidation_pack_closed_through_gate_163_on_main",
    }
    assert leaves["active_gate"] in {"Gate 159", "Gate 160", "Gate 161", "Gate 162", "Gate 163", "none"}
    for leaf_id in ["LEAF-G158-001", "LEAF-G158-002", "LEAF-G158-003", "LEAF-G158-004"]:
        assert leaves["leaves"][leaf_id]["status"] == "complete"



def test_gate158_receipt_freezes_architecture_stage_purity_and_no_new_vocabulary() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")

    assert "Gate 158 does not invent a new architecture." in receipt
    assert "## Repo-native target architecture statement" in receipt
    assert "state-policy deformation plane" in receipt
    assert "review-visible lineage" in receipt
    assert "## Workbook-derived raw-versus-derived ordering law" in receipt
    assert "Raw_Primitives_Catalog" in receipt
    assert "Derived_Features_Catalog" in receipt
    assert "Options_Chain_Raw_Spec" in receipt
    assert "Volume_Baseline_Raw_Spec" in receipt
    assert "## Step 1 stage-purity law frozen by Gate 158" in receipt
    assert "Temporal_Step1_Framework" in receipt
    assert "No new governed vocabulary is admitted in Gate 158." in receipt
    assert "activation state" in receipt
    assert "opportunity shaping / caution shaping" in receipt
