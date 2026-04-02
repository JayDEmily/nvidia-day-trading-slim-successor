"""Gate 168 review/observability chain strengthening checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LEAVES = REPO_ROOT / "docs/planning/2026-04-02_POLICY_TEMPORAL_OBSERVABILITY_SUCCESSOR_LEAVES_v1.json"
RECEIPT = REPO_ROOT / "docs/planning/2026-04-02_GATE168_REVIEW_OBSERVABILITY_CHAIN_STRENGTHENING.md"


def test_gate168_leaves_are_complete() -> None:
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    for leaf_id in ["LEAF-G168-001", "LEAF-G168-002", "LEAF-G168-003", "LEAF-G168-004"]:
        assert leaves["leaves"][leaf_id]["status"] == "complete"


def test_gate168_receipt_freezes_one_compact_decision_chain_and_dmp_boundary() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")

    assert "No new governed vocabulary is admitted in Gate 168." in receipt
    assert "environment_readout" in receipt
    assert "surface_traces" in receipt
    assert "decision_chain_footer" in receipt
    assert "baseline_value" in receipt
    assert "active_policy_ids" in receipt
    assert "effective_value" in receipt
    assert "clamp_source" in receipt
    assert "primary_consuming_stage" in receipt
    assert "downstream_read_path" in receipt
    assert "trader-trust work, not decorative UI work" in receipt
    assert 'review_packet["decision_chain_view"]' in receipt
    assert "DMP v2 envelope and block taxonomy remain unchanged" in receipt
    assert "unknown / not verified" in receipt
