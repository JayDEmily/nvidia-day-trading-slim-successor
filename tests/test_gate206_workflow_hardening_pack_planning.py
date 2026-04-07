"""Gate 206 closeout and Gate 207 routing checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_EXECUTION_LOG_v1.md"

GATE206_LEAVES = {"LEAF-G206-001", "LEAF-G206-002", "LEAF-G206-003"}
GATE207_LEAVES = {"LEAF-G207-001", "LEAF-G207-002"}


def test_gate206_closeout_routes_gate207_coherently() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    payload = json.loads(LEAVES.read_text(encoding="utf-8"))
    leaves = {leaf["id"]: leaf for leaf in payload["leaves"]}
    completed_leaf_ids = set(payload["completed_leaf_ids"])
    remaining_leaf_ids = set(payload["remaining_leaf_ids"])

    assert (REPO_ROOT / "docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_GATES_v1.md").is_file()
    assert (REPO_ROOT / "docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_LEAVES_v1.json").is_file()
    assert (REPO_ROOT / "docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_EXECUTION_LOG_v1.md").is_file()
    assert (
        "- next active gate: `Gate 207`" in plans
        or "no active pack currently routed" in plans
    )

    assert (
        "Current active gate: **Gate 207 in the workflow hardening and active-repo reset "
        "foundation pack on `work/gate-207-router-and-doctrine-consolidation-20260406`**."
    ) in gate_map or "Current active gate: **No active pack currently routed. The successor retained-test cleanup execution pack is closed through Gate 225 on `work/gate-225-retained-test-cleanup-closeout-20260406`.**" in gate_map
    assert "Gate 205 | complete on `main`" in gate_map
    assert "Gate 206 | complete on `main`" in gate_map
    assert (
        "Gate 207 | active on `work/gate-207-router-and-doctrine-consolidation-20260406`" in gate_map
        or "Gate 207 | complete on `work/gate-207-router-and-doctrine-consolidation-20260406`" in gate_map
    )
    assert ("Gate 210 | planned" in gate_map) or ("Gate 210 | complete on `work/gate-210-operator-surface-alignment-and-active-repo-cutover-criteria-20260406`" in gate_map)

    assert payload["governing_plan"] == "docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_GATES_v1.md"
    assert payload["execution_status"] in {"gate_207_active", "workflow_hardening_and_active_repo_reset_foundation_pack_closed_through_gate_210_on_work_branch"}
    assert payload["active_gate"] in {"Gate 207", "none"}
    assert payload["completed_gate_ids"] in (["Gate 206"], ["Gate 206", "Gate 207", "Gate 208", "Gate 209", "Gate 210"])
    assert completed_leaf_ids in (GATE206_LEAVES, GATE206_LEAVES | GATE207_LEAVES | {"LEAF-G208-001", "LEAF-G208-002", "LEAF-G209-001", "LEAF-G209-002", "LEAF-G210-001", "LEAF-G210-002"})
    assert remaining_leaf_ids.isdisjoint(completed_leaf_ids)
    assert remaining_leaf_ids in ({
        "LEAF-G207-001",
        "LEAF-G207-002",
        "LEAF-G208-001",
        "LEAF-G208-002",
        "LEAF-G209-001",
        "LEAF-G209-002",
        "LEAF-G210-001",
        "LEAF-G210-002",
    }, set())
    assert all(leaves[leaf_id]["status"] == "complete" for leaf_id in GATE206_LEAVES)

    assert (
        "Status: active execution log for workflow hardening and active-repo reset foundation; "
        "Gate 206 complete on main, Gate 207 active on "
        "work/gate-207-router-and-doctrine-consolidation-20260406"
    ) in execution_log or ("Status: closed execution log for workflow hardening and active-repo reset foundation" in execution_log)
    assert "2de50ab6456fdecde3bf521594138c6e2d907360" in execution_log
    assert "2f556ed24a6097955a44f5c4b5b4bd7ddb497e97" in execution_log
    assert "7 passed in 0.28s" in execution_log
    assert "non-fast-forward merge commit" in execution_log

    validation_command = (
        "source .venv/bin/activate && python -m pytest -q "
        "tests/test_gate200_target_repo_admitted_evidence_successor_pack_planning.py "
        "tests/test_gate201_target_repo_evidence_governance_planning.py "
        "tests/test_gate202_target_repo_review_governance_planning.py "
        "tests/test_gate203_target_repo_snapshot_and_collection_planning.py "
        "tests/test_gate204_target_repo_dmp_failure_pack_planning.py "
        "tests/test_gate206_workflow_hardening_pack_planning.py"
    )
    assert validation_command in execution_log
