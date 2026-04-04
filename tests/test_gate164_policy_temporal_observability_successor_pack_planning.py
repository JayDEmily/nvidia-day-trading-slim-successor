"""Gate 164 policy/temporal/observability successor-pack planning checks."""

from __future__ import annotations

import json
from pathlib import Path

from ._planning_later_state_helpers import (
    PHASE3_GATE_MAP_MARKERS,
    PHASE3_PLAN_MARKERS,
    contains_any,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-02_POLICY_TEMPORAL_OBSERVABILITY_SUCCESSOR_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-02_POLICY_TEMPORAL_OBSERVABILITY_SUCCESSOR_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-02_POLICY_TEMPORAL_OBSERVABILITY_SUCCESSOR_EXECUTION_LOG_v1.md"
CHECKLIST = REPO_ROOT / "docs/planning/2026-04-02_POLICY_TEMPORAL_OBSERVABILITY_SUCCESSOR_DOCUMENT_TOUCH_CHECKLIST_v1.md"
SCOPE_NOTE = REPO_ROOT / "docs/planning/2026-04-02_POLICY_TEMPORAL_OBSERVABILITY_SUCCESSOR_SCOPE_NOTE_v1.md"
RECEIPT = REPO_ROOT / "docs/planning/2026-04-02_GATE164_POLICY_TEMPORAL_OBSERVABILITY_SUCCESSOR_PACK_BOOTSTRAP.md"

ALLOWED_PLAN_MARKERS = {
    "active gate: Gate 165 on `work/gate-164-policy-temporal-observability-pack-20260402`",
    "active gate: Gate 166 on `work/gate-164-policy-temporal-observability-pack-20260402`",
    "active gate: Gate 167 on `work/gate-164-policy-temporal-observability-pack-20260402`",
    "active gate: Gate 168 on `work/gate-164-policy-temporal-observability-pack-20260402`",
    "active gate: Gate 169 on `work/gate-164-policy-temporal-observability-pack-20260402`",
    "active gate: Gate 170 on `work/gate-164-policy-temporal-observability-pack-20260402`",
            "active gate: Gate 172 on `work/gate-171-master-child-parallel-risk-integration-pack-20260402`",
            "no active pack currently routed; master/child parallel-risk integration pack closed through Gate 180 on `work/gate-171-master-child-parallel-risk-integration-pack-20260402`",
    "no active pack currently routed; policy/temporal/observability successor pack closed through Gate 170 on `work/gate-164-policy-temporal-observability-pack-20260402`",
    "no active pack currently routed; policy/temporal/observability successor pack closed through Gate 170 on `main`",
}

ALLOWED_CURRENT_GATE_MARKERS = {
    "Current active gate: **Gate 165 in the policy/temporal/observability successor pack**.",
    "Current active gate: **Gate 166 in the policy/temporal/observability successor pack**.",
    "Current active gate: **Gate 167 in the policy/temporal/observability successor pack**.",
    "Current active gate: **Gate 168 in the policy/temporal/observability successor pack**.",
    "Current active gate: **Gate 169 in the policy/temporal/observability successor pack**.",
    "Current active gate: **Gate 170 in the policy/temporal/observability successor pack**.",
            "Current active gate: **Gate 172 in the master/child parallel-risk integration pack**.",
            "Current active gate: **none — master/child parallel-risk integration pack closed through Gate 180 on `work/gate-171-master-child-parallel-risk-integration-pack-20260402`**.",
    "Current active gate: **none — policy/temporal/observability successor pack closed through Gate 170 on `work/gate-164-policy-temporal-observability-pack-20260402`**.",
    "Current active gate: **none — policy/temporal/observability successor pack closed through Gate 170 on `main`**.",
}

ALLOWED_GATE_STATUS = {
    "Status: active policy/temporal/observability successor pack; Gate 164 complete on `work/gate-164-policy-temporal-observability-pack-20260402`, Gate 165 active, Gates 166-170 planned",
    "Status: active policy/temporal/observability successor pack; Gates 164-165 complete on `work/gate-164-policy-temporal-observability-pack-20260402`, Gate 166 active, Gates 167-170 planned",
    "Status: active policy/temporal/observability successor pack; Gates 164-166 complete on `work/gate-164-policy-temporal-observability-pack-20260402`, Gate 167 active, Gates 168-170 planned",
    "Status: active policy/temporal/observability successor pack; Gates 164-167 complete on `work/gate-164-policy-temporal-observability-pack-20260402`, Gate 168 active, Gates 169-170 planned",
    "Status: active policy/temporal/observability successor pack; Gates 164-168 complete on `work/gate-164-policy-temporal-observability-pack-20260402`, Gate 169 active, Gate 170 planned",
    "Status: active policy/temporal/observability successor pack; Gates 164-169 complete on `work/gate-164-policy-temporal-observability-pack-20260402`, Gate 170 active",
    "Status: closed policy/temporal/observability successor pack through Gate 170 on `work/gate-164-policy-temporal-observability-pack-20260402`",
    "Status: closed policy/temporal/observability successor pack through Gate 170 on `main`",
}


def test_gate164_pack_is_active_and_non_placeholder() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    scope_note = SCOPE_NOTE.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert "2026-04-02_POLICY_TEMPORAL_OBSERVABILITY_SUCCESSOR_GATES_v1.md" in plans
    assert "2026-04-02_POLICY_TEMPORAL_OBSERVABILITY_SUCCESSOR_LEAVES_v1.json" in plans
    assert "2026-04-02_POLICY_TEMPORAL_OBSERVABILITY_SUCCESSOR_EXECUTION_LOG_v1.md" in plans
    assert "2026-04-02_POLICY_TEMPORAL_OBSERVABILITY_SUCCESSOR_DOCUMENT_TOUCH_CHECKLIST_v1.md" in plans
    assert "2026-04-02_POLICY_TEMPORAL_OBSERVABILITY_SUCCESSOR_SCOPE_NOTE_v1.md" in plans
    assert any(marker in plans for marker in ALLOWED_PLAN_MARKERS)
    assert contains_any(gate_map, ALLOWED_CURRENT_GATE_MARKERS | PHASE3_GATE_MAP_MARKERS)
    assert any(marker in gates for marker in ALLOWED_GATE_STATUS)
    assert leaves["execution_status"] in {
        "gate_164_complete_gate_165_active_on_work_branch",
        "gate_165_complete_gate_166_active_on_work_branch",
        "gate_166_complete_gate_167_active_on_work_branch",
        "gate_167_complete_gate_168_active_on_work_branch",
        "gate_168_complete_gate_169_active_on_work_branch",
        "gate_169_complete_gate_170_active_on_work_branch",
        "policy_temporal_observability_successor_pack_closed_through_gate_170_on_work_branch",
        "policy_temporal_observability_successor_pack_closed_through_gate_170_on_main",
    }
    assert leaves["active_gate"] in {"Gate 165", "Gate 166", "Gate 167", "Gate 168", "Gate 169", "Gate 170", "none"}
    assert leaves["completed_gate_ids"] in (
        ["Gate 164"],
        ["Gate 164", "Gate 165"],
        ["Gate 164", "Gate 165", "Gate 166"],
        ["Gate 164", "Gate 165", "Gate 166", "Gate 167"],
        ["Gate 164", "Gate 165", "Gate 166", "Gate 167", "Gate 168"],
        ["Gate 164", "Gate 165", "Gate 166", "Gate 167", "Gate 168", "Gate 169"],
        ["Gate 164", "Gate 165", "Gate 166", "Gate 167", "Gate 168", "Gate 169", "Gate 170"],
    )
    assert leaves["completed_leaf_ids"][:4] == [
        "LEAF-G164-001",
        "LEAF-G164-002",
        "LEAF-G164-003",
        "LEAF-G164-004",
    ]
    assert execution_log.startswith("# 2026-04-02_POLICY_TEMPORAL_OBSERVABILITY_SUCCESSOR_EXECUTION_LOG_v1")
    assert "lean-docs rule" in scope_note
    assert "Gate 164" in checklist


def test_gate164_future_leaves_are_materially_detailed_and_audit_gate_exists() -> None:
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))["leaves"]

    future_gate_ids = {"Gate 165", "Gate 166", "Gate 167", "Gate 168", "Gate 169", "Gate 170"}
    future_leaves = [leaf for leaf in leaves.values() if leaf["gate"] in future_gate_ids]

    assert future_leaves
    assert any(leaf["gate"] == "Gate 170" for leaf in future_leaves)
    for leaf in future_leaves:
        assert len(leaf["ordered_actions"]) >= 3
        assert len(leaf["forbidden_actions"]) >= 3
        assert leaf["validation_commands"]
        assert leaf["expected_evidence"]
        assert leaf["definition_of_done"]
        assert leaf["packaging_requirement"]


def test_gate164_scope_note_and_receipt_preserve_thread_gold_and_boundaries() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")
    scope_note = SCOPE_NOTE.read_text(encoding="utf-8")

    assert "do not write more policy prose than the repo can actually use" in receipt
    assert "independent parallel risk lane" in receipt
    assert "Runtime_Surface_Drivers" in scope_note
    assert "Coeff_Universe_Index" in scope_note
    assert "Derived_Features_Catalog" in scope_note
    assert "DMP v2" in scope_note
    assert "unknown/not verified" in scope_note
