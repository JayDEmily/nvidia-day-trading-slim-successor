"""Gate 167 serial-conservatism binding-point law checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LEAVES = REPO_ROOT / "docs/planning/2026-04-02_POLICY_TEMPORAL_OBSERVABILITY_SUCCESSOR_LEAVES_v1.json"
RECEIPT = REPO_ROOT / "docs/planning/2026-04-02_GATE167_SERIAL_CONSERVATISM_BINDING_POINT_LAW.md"


def test_gate167_leaves_are_complete() -> None:
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    for leaf_id in ["LEAF-G167-001", "LEAF-G167-002", "LEAF-G167-003", "LEAF-G167-004"]:
        assert leaves["leaves"][leaf_id]["status"] == "complete"


def test_gate167_receipt_freezes_binding_points_without_stealing_risk_lane_authority() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")

    assert "No new governed vocabulary is admitted in Gate 167." in receipt
    assert "posture_hard_block" in receipt
    assert "posture_derisk_local_envelope" in receipt
    assert "modifier_capital_compression" in receipt
    assert "modifier_threshold_tightening" in receipt
    assert "modifier_max_risk_clamp" in receipt
    assert "modifier_required_hedge" in receipt
    assert "modifier_stand_down_or_kill_switch" in receipt
    assert "overlay_risk_derisk_or_block" in receipt
    assert "one primary binder" in receipt
    assert "caution_mechanisms_fired" in receipt
    assert "primary_binding_mechanism" in receipt
    assert "compressed_dimensions" in receipt
    assert "stacked_caution_flags" in receipt
    assert "binding stack, not a score" in receipt
    assert "may **not** decide future independent-risk final cap/veto ownership" in receipt
