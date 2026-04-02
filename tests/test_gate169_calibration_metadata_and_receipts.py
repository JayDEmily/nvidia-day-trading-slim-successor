"""Gate 169 calibration metadata and receipt checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LEAVES = REPO_ROOT / "docs/planning/2026-04-02_POLICY_TEMPORAL_OBSERVABILITY_SUCCESSOR_LEAVES_v1.json"
RECEIPT = REPO_ROOT / "docs/planning/2026-04-02_GATE169_CALIBRATION_METADATA_AND_RECEIPTS.md"


def test_gate169_leaves_are_complete() -> None:
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    for leaf_id in ["LEAF-G169-001", "LEAF-G169-002", "LEAF-G169-003", "LEAF-G169-004"]:
        assert leaves["leaves"][leaf_id]["status"] == "complete"


def test_gate169_receipt_freezes_surface_and_policy_metadata_plus_eval_questions() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")

    assert "No new governed vocabulary is admitted in Gate 169." in receipt
    assert "entry_gate_score_floor" in receipt
    assert "zone_score_threshold" in receipt
    assert "risk_vix_hot_threshold" in receipt
    assert "behavioural_purpose" in receipt
    assert "expected_directionality" in receipt
    assert "anti_goal" in receipt
    assert "activation_state" in receipt
    assert "policy_id" in receipt
    assert "over_tightening_signs" in receipt
    assert "redundancy_signs" in receipt
    assert "danger_signs" in receipt
    assert "opportunity_shaping_absence_or_presence" in receipt
    assert "Calibration has not started." in receipt
