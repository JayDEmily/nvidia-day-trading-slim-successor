"""Planning-pack checks for the master/child parallel-risk integration pack."""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-02_MASTER_CHILD_PARALLEL_RISK_INTEGRATION_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-02_MASTER_CHILD_PARALLEL_RISK_INTEGRATION_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-02_MASTER_CHILD_PARALLEL_RISK_INTEGRATION_EXECUTION_LOG_v1.md"
CHECKLIST = REPO_ROOT / "docs/planning/2026-04-02_MASTER_CHILD_PARALLEL_RISK_INTEGRATION_DOCUMENT_TOUCH_CHECKLIST_v1.md"
SCOPE_NOTE = REPO_ROOT / "docs/planning/2026-04-02_MASTER_CHILD_PARALLEL_RISK_INTEGRATION_SCOPE_NOTE_v1.md"
RECEIPT = REPO_ROOT / "docs/planning/2026-04-02_GATE171_MASTER_CHILD_PARALLEL_RISK_INTEGRATION_PACK_BOOTSTRAP.md"


def test_gate171_pack_surfaces_remain_coherent_through_closeout() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    scope_note = SCOPE_NOTE.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert "master/child parallel-risk integration pack" in plans
    assert "Current active gate: **Gate 182 in the options-trace integrity repair pack on `main`**." in gate_map
    assert "Status: closed master/child parallel-risk integration pack through Gate 180 on `main`" in gates
    assert leaves["execution_status"] == "master_child_parallel_risk_integration_pack_closed_through_gate_180_on_main"
    assert leaves["active_gate"] == "none"
    assert set(leaves["completed_leaf_ids"]).isdisjoint(leaves["remaining_leaf_ids"])
    assert execution_log.startswith("# 2026-04-02_MASTER_CHILD_PARALLEL_RISK_INTEGRATION_EXECUTION_LOG_v1")
    assert "Current planned sequence: master/child parallel-risk integration pack closed through Gate 180 on `main`." in checklist
    assert "master" in scope_note and "child" in scope_note
    assert "merge child planning/reference-data/vocabulary into master" in scope_note


def test_gate171_future_leaves_are_materially_detailed_and_hygiene_gate_exists() -> None:
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))["leaves"]

    future_gate_ids = {f"Gate {n}" for n in range(172, 181)}
    future_leaves = [leaf for leaf in leaves.values() if leaf["gate"] in future_gate_ids]

    assert future_leaves
    assert any(leaf["gate"] == "Gate 179" for leaf in future_leaves)
    assert any(leaf["gate"] == "Gate 180" for leaf in future_leaves)
    for leaf in future_leaves:
        assert len(leaf["ordered_actions"]) >= 3
        assert len(leaf["forbidden_actions"]) >= 3
        assert leaf["validation_commands"]
        assert leaf["expected_evidence"]
        assert leaf["definition_of_done"]
        assert leaf["packaging_requirement"]


def test_gate171_scope_note_and_receipt_preserve_non_blind_merge_truth() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")
    scope_note = SCOPE_NOTE.read_text(encoding="utf-8")

    assert "repo_gate170_policy_temporal_observability_successor_pack_closed_workbranch_2026-04-02.zip" in receipt
    assert "repo_gate164_parallel_risk_lane_foundation_pack_closed_2026-04-02_slim.zip" in receipt
    assert "PARALLEL_RISK_LANE_PLANNING_HANDOVER_NOTE_2026-04-02.md" in receipt
    assert "no verified `src/` runtime-code deltas" in receipt
    assert "merge planning/reference-data first, then code the lane" in receipt
    assert "Do not blind-apply patches from child into master." in scope_note
    assert re.search(r"planning/reference-data/vocabulary branch|child is a planning-law/reference-data branch", scope_note)
    assert "whole-repo vocabulary/workbook-path hygiene" in scope_note
    assert "unknown / not verified" in scope_note
