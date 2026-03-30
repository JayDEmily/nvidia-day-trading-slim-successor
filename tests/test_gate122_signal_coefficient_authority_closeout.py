"""Gate 122 signal-coefficient authority closeout checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_EXECUTION_LOG_v1.md"
RECEIPT = REPO_ROOT / "docs/planning/2026-03-31_GATE122_COEFFICIENT_SCOPE_FREEZE.md"


def test_gate122_is_closed_honestly_and_gate123_is_active() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")

    assert (
        "Gate 122 complete and Gate 123 now active" in plans
        or "Gates 122-123 complete and Gate 124 now active" in plans
        or "Gates 122-124 complete and Gate 125 now active" in plans
        or "Gates 122-125 complete and Gate 126 now active" in plans
        or "Gates 122-126 complete and Gate 127 now active" in plans
        or "signal-coefficient authority pack closed through Gate 127" in plans
    )
    assert (
        "Current active gate: **Gate 123 in the signal-coefficient authority pack**." in gate_map
        or "Current active gate: **Gate 124 in the signal-coefficient authority pack**." in gate_map
        or "Current active gate: **Gate 125 in the signal-coefficient authority pack**." in gate_map
        or "Current active gate: **Gate 126 in the signal-coefficient authority pack**." in gate_map
        or "Current active gate: **Gate 127 in the signal-coefficient authority pack**." in gate_map
        or "Current active gate: **none — signal-coefficient authority pack closed through Gate 127 on `main`**." in gate_map
    )
    assert (
        "Status: active signal-coefficient authority pack; Gate 122 complete on `main`, Gate 123 active, Gates 124-127 planned" in gates
        or "Status: active signal-coefficient authority pack; Gates 122-123 complete on `main`, Gate 124 active, Gates 125-127 planned" in gates
        or "Status: active signal-coefficient authority pack; Gates 122-124 complete on `main`, Gate 125 active, Gates 126-127 planned" in gates
        or "Status: active signal-coefficient authority pack; Gates 122-125 complete on `main`, Gate 126 active, Gate 127 planned" in gates
        or "Status: active signal-coefficient authority pack; Gates 122-126 complete on `main`, Gate 127 active" in gates
        or "Status: closed signal-coefficient authority pack on `main`; Gates 122-127 complete, no active gate" in gates
    )
    assert leaves["execution_status"] in {"gate_122_complete_gate_123_active_on_main", "gate_123_complete_gate_124_active_on_main", "gate_124_complete_gate_125_active_on_main", "gate_125_complete_gate_126_active_on_main", "gate_126_complete_gate_127_active_on_main", "signal_coefficient_authority_pack_closed_through_gate_127_on_main"}
    assert leaves["active_gate"] in {"Gate 123", "Gate 124", "Gate 125", "Gate 126", "Gate 127", "none — signal-coefficient authority pack closed through Gate 127 on main"}
    assert leaves["completed_gate_ids"][:1] == ["Gate 122"]
    assert leaves["completed_leaf_ids"][:3] == ["LEAF-G122-001", "LEAF-G122-002", "LEAF-G122-003"]
    assert len(leaves["remaining_leaf_ids"]) in {14, 11, 8, 5, 2, 0}
    assert (
        "Status: active execution log for the signal-coefficient authority pack; Gate 122 complete on `main`, Gate 123 active, Gates 124-127 planned" in execution_log
        or "Status: active execution log for the signal-coefficient authority pack; Gates 122-123 complete on `main`, Gate 124 active, Gates 125-127 planned" in execution_log
        or "Status: active execution log for the signal-coefficient authority pack; Gates 122-124 complete on `main`, Gate 125 active, Gates 126-127 planned" in execution_log
        or "Status: active execution log for the signal-coefficient authority pack; Gates 122-125 complete on `main`, Gate 126 active, Gate 127 planned" in execution_log
        or "Status: active execution log for the signal-coefficient authority pack; Gates 122-126 complete on `main`, Gate 127 active" in execution_log
        or "Status: closed execution log for the signal-coefficient authority pack; Gates 122-127 complete on `main`, no active gate" in execution_log
    )


def test_gate122_receipt_freezes_scope_and_drift_truth() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert "Status: complete on `main`; Gate 123 is now the active gate" in receipt
    assert "tranche-one coefficient scope is frozen tightly enough" in receipt
    assert leaves["inherited_preflight_drift"]["observed_result"] == "20 passed, 6 failed"
    assert "raw_asia_japan_europe_precursor_coefficients" in leaves["tranche_one_authority"]["explicit_exclusions"]
    assert len(leaves["tranche_one_authority"]["mutable_runtime_surfaces"]) == 8
    assert len(leaves["tranche_one_authority"]["temporal_thresholds"]) == 16
    assert len(leaves["tranche_one_authority"]["timing_parameters"]) == 2
