"""Planning-pack checks for the capital-deployment authority foundation pack."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-03_CAPITAL_DEPLOYMENT_AUTHORITY_FOUNDATION_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-03_CAPITAL_DEPLOYMENT_AUTHORITY_FOUNDATION_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-03_CAPITAL_DEPLOYMENT_AUTHORITY_FOUNDATION_EXECUTION_LOG_v1.md"
CHECKLIST = REPO_ROOT / "docs/planning/2026-04-03_CAPITAL_DEPLOYMENT_AUTHORITY_FOUNDATION_DOCUMENT_TOUCH_CHECKLIST_v1.md"
SCOPE_NOTE = REPO_ROOT / "docs/planning/2026-04-03_CAPITAL_DEPLOYMENT_AUTHORITY_FOUNDATION_SCOPE_NOTE_v1.md"
RECEIPT = REPO_ROOT / "docs/planning/2026-04-03_GATE187_CAPITAL_DEPLOYMENT_AUTHORITY_PACK_BOOTSTRAP.md"


def test_gate187_pack_surfaces_are_coherent() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    scope_note = SCOPE_NOTE.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert "docs/planning/2026-04-03_CAPITAL_DEPLOYMENT_AUTHORITY_FOUNDATION_GATES_v1.md" in plans
    assert any(marker in gate_map for marker in ["Gate 188 in the capital-deployment authority foundation pack", "none — capital-deployment authority foundation pack closed through Gate 191 on `main`"])
    assert any(marker in gates for marker in ["Status: active capital-deployment authority foundation pack from Gate 188", "Status: closed capital-deployment authority foundation pack through Gate 191 on `main`"])
    assert leaves["execution_status"] in {"gate_187_capital_deployment_authority_foundation_pack_active_from_gate_188", "capital_deployment_authority_foundation_pack_closed_through_gate_191_on_main"}
    assert leaves["active_gate"] in {"Gate 188", "none"}
    assert set(leaves["completed_leaf_ids"]).isdisjoint(leaves["remaining_leaf_ids"])
    assert execution_log.startswith("# 2026-04-03_CAPITAL_DEPLOYMENT_AUTHORITY_FOUNDATION_EXECUTION_LOG_v1")
    assert any(marker in checklist for marker in ["capital-deployment authority foundation pack active from Gate 188", "capital-deployment authority foundation pack closed through Gate 191 on `main`"])
    assert "new-opening capital authorisation only" in scope_note
    assert "position-close recommendations" in scope_note


def test_gate187_future_gate_structure_is_bounded() -> None:
    payload = json.loads(LEAVES.read_text(encoding="utf-8"))
    leaves = payload["leaves"]
    counts: dict[str, int] = {}
    for item in leaves.values():
        counts.setdefault(item["gate"], 0)
        counts[item["gate"]] += 1

    assert counts["Gate 188"] == 4
    assert counts["Gate 189"] == 4
    assert counts["Gate 190"] == 4
    assert counts["Gate 191"] == 4

    future_leaves = [item for item in leaves.values() if item["gate"] in {"Gate 188", "Gate 189", "Gate 190", "Gate 191"}]
    for item in future_leaves:
        assert len(item["ordered_actions"]) >= 3
        assert len(item["forbidden_actions"]) >= 3
        assert item["validation_commands"]
        assert item["expected_evidence"]
        assert item["definition_of_done"]


def test_gate187_receipt_and_scope_note_preserve_first_slice_truth() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")
    scope_note = SCOPE_NOTE.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")

    assert "the first slice is **not** a full arbiter" in receipt
    assert "it did not edit runtime behaviour under `src/`" in receipt
    assert "recommendation-memory lookback logic" in scope_note
    assert "Do not let the service become a disguised second posture/risk engine." in scope_note
    assert "a brand-new capital JSON ledger architecture is not required for v1" in checklist
