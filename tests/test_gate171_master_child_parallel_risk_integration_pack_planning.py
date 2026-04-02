"""Gate 171 master/child integration-pack planning checks."""

from __future__ import annotations

import json
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


def test_gate171_pack_is_active_and_routes_to_gate172() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    scope_note = SCOPE_NOTE.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert "2026-04-02_MASTER_CHILD_PARALLEL_RISK_INTEGRATION_GATES_v1.md" in plans
    assert "2026-04-02_MASTER_CHILD_PARALLEL_RISK_INTEGRATION_LEAVES_v1.json" in plans
    assert "2026-04-02_MASTER_CHILD_PARALLEL_RISK_INTEGRATION_EXECUTION_LOG_v1.md" in plans
    assert "2026-04-02_MASTER_CHILD_PARALLEL_RISK_INTEGRATION_DOCUMENT_TOUCH_CHECKLIST_v1.md" in plans
    assert "2026-04-02_MASTER_CHILD_PARALLEL_RISK_INTEGRATION_SCOPE_NOTE_v1.md" in plans
    assert any(f"active gate: Gate {gate} on `work/gate-171-master-child-parallel-risk-integration-pack-20260402`" in plans for gate in (172, 173, 174, 175, 176, 177, 178, 179, 180)) or "closed through Gate 180 on `work/gate-171-master-child-parallel-risk-integration-pack-20260402`" in plans
    assert any(f"Current active gate: **Gate {gate} in the master/child parallel-risk integration pack**." in gate_map for gate in (172, 173, 174, 175, 176, 177, 178, 179, 180)) or "Current active gate: **none — master/child parallel-risk integration pack closed through Gate 180" in gate_map
    assert any(label in gates for label in (
        "Status: active master/child parallel-risk integration pack; Gate 171 complete on `work/gate-171-master-child-parallel-risk-integration-pack-20260402`, Gate 172 active, Gates 173-180 planned",
        "Status: active master/child parallel-risk integration pack; Gates 171-172 complete on `work/gate-171-master-child-parallel-risk-integration-pack-20260402`, Gate 173 active, Gates 174-180 planned",
        "Status: active master/child parallel-risk integration pack; Gates 171-173 complete on `work/gate-171-master-child-parallel-risk-integration-pack-20260402`, Gate 174 active, Gates 175-180 planned",
        "Status: active master/child parallel-risk integration pack; Gates 171-174 complete on `work/gate-171-master-child-parallel-risk-integration-pack-20260402`, Gate 175 active, Gates 176-180 planned",
        "Status: active master/child parallel-risk integration pack; Gates 171-175 complete on `work/gate-171-master-child-parallel-risk-integration-pack-20260402`, Gate 176 active, Gates 177-180 planned",
        "Status: active master/child parallel-risk integration pack; Gates 171-176 complete on `work/gate-171-master-child-parallel-risk-integration-pack-20260402`, Gate 177 active, Gates 178-180 planned",
        "Status: active master/child parallel-risk integration pack; Gates 171-177 complete on `work/gate-171-master-child-parallel-risk-integration-pack-20260402`, Gate 178 active, Gates 179-180 planned",
        "Status: active master/child parallel-risk integration pack; Gates 171-178 complete on `work/gate-171-master-child-parallel-risk-integration-pack-20260402`, Gate 179 active, Gate 180 planned",
        "Status: active master/child parallel-risk integration pack; Gates 171-179 complete on `work/gate-171-master-child-parallel-risk-integration-pack-20260402`, Gate 180 active",
        "Status: closed master/child parallel-risk integration pack through Gate 180 on `work/gate-171-master-child-parallel-risk-integration-pack-20260402`",
    ))
    assert leaves["execution_status"] in {"gate_171_complete_gate_172_active_on_work_branch", "gate_172_complete_gate_173_active_on_work_branch", "gate_173_complete_gate_174_active_on_work_branch", "gate_174_complete_gate_175_active_on_work_branch", "gate_175_complete_gate_176_active_on_work_branch", "gate_176_complete_gate_177_active_on_work_branch", "gate_177_complete_gate_178_active_on_work_branch", "gate_178_complete_gate_179_active_on_work_branch", "gate_179_complete_gate_180_active_on_work_branch", "master_child_parallel_risk_integration_pack_closed_through_gate_180_on_work_branch"}
    assert leaves["active_gate"] in {"Gate 172", "Gate 173", "Gate 174", "Gate 175", "Gate 176", "Gate 177", "Gate 178", "Gate 179", "Gate 180", "none"}
    assert leaves["completed_gate_ids"][0] == "Gate 171"
    assert leaves["completed_leaf_ids"][:4] == [
        "LEAF-G171-001",
        "LEAF-G171-002",
        "LEAF-G171-003",
        "LEAF-G171-004",
    ]
    assert execution_log.startswith("# 2026-04-02_MASTER_CHILD_PARALLEL_RISK_INTEGRATION_EXECUTION_LOG_v1")
    assert any(f"Current planned sequence: active gate: Gate {gate} on `work/gate-171-master-child-parallel-risk-integration-pack-20260402`." in checklist for gate in (172,173,174,175,176,177,178,179,180)) or "closed through Gate 180" in checklist
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
    assert "child is a planning-law/reference-data branch" in scope_note or "planning/reference-data/vocabulary branch" in scope_note
    assert "whole-repo vocabulary/workbook-path hygiene" in scope_note
    assert "unknown / not verified" in scope_note
