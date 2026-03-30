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

    assert "Gate 122 complete and Gate 123 now active" in plans
    assert "Current active gate: **Gate 123 in the signal-coefficient authority pack**." in gate_map
    assert "Status: active signal-coefficient authority pack; Gate 122 complete on `main`, Gate 123 active, Gates 124-127 planned" in gates
    assert leaves["execution_status"] == "gate_122_complete_gate_123_active_on_main"
    assert leaves["active_gate"] == "Gate 123"
    assert leaves["completed_gate_ids"] == ["Gate 122"]
    assert leaves["completed_leaf_ids"] == ["LEAF-G122-001", "LEAF-G122-002", "LEAF-G122-003"]
    assert len(leaves["remaining_leaf_ids"]) == 14
    assert "Status: active execution log for the signal-coefficient authority pack; Gate 122 complete on `main`, Gate 123 active, Gates 124-127 planned" in execution_log


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
