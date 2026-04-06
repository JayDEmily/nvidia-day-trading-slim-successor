"""Gate 166 temporal-governance status-ledger checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LEAVES = REPO_ROOT / "docs/planning/2026-04-02_POLICY_TEMPORAL_OBSERVABILITY_SUCCESSOR_LEAVES_v1.json"
RECEIPT = REPO_ROOT / "docs/planning/2026-04-02_GATE166_TEMPORAL_GOVERNANCE_STATUS_LEDGER.md"


def test_gate166_leaves_are_complete() -> None:
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    for leaf_id in ["LEAF-G166-001", "LEAF-G166-002", "LEAF-G166-003", "LEAF-G166-004"]:
        assert leaves["leaves"][leaf_id]["status"] == "complete"


def test_gate166_receipt_freezes_governed_subset_and_remaining_status_classes() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")

    assert "No new governed vocabulary is admitted in Gate 166." in receipt
    assert "open_disorder_relvol_min" in receipt
    assert "anchor_vwap_dist_bps_max" in receipt
    assert "compression_range5_bps_max" in receipt
    assert "trend_vwap_slope_bps_min" in receipt
    assert "power_hour_window_min" in receipt
    assert "unwind_window_min" in receipt
    assert "Temporal_Step1_Framework" in receipt
    assert "Temporal_Bounds_Draft" in receipt
    assert "Bounds_Method" in receipt
    assert "Signal_Coeff_Handoff" in receipt
    assert "governed_live_threshold" in receipt
    assert "fixed_structural_heuristic" in receipt
    assert "deferred_candidate" in receipt
    assert "removal_candidate" in receipt
    assert "coverage_ratio < 0.375" in receipt
    assert "range5_bps >= 80.0" in receipt
    assert "trend_hits >= 4" in receipt
    assert "no live `removal_candidate` values yet" in receipt
    assert "authority:{id}" in receipt
    assert "fixed_heuristic:{id}" in receipt
    assert "deferred_candidate:{id}" in receipt
