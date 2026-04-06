"""Gate 207 router and doctrine consolidation checks."""

from __future__ import annotations

import json
from pathlib import Path

from ._planning_later_state_helpers import CLEANUP_GATE_MAP_MARKERS, CLEANUP_PLAN_MARKERS, contains_any

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
AGENTS = REPO_ROOT / "AGENTS.md"
PROCESS_LAW = REPO_ROOT / "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_EXECUTION_LOG_v1.md"


def test_gate207_router_and_doctrine_closeout_is_coherent() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    agents = AGENTS.read_text(encoding="utf-8")
    process_law = PROCESS_LAW.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    payload = json.loads(LEAVES.read_text(encoding="utf-8"))
    leaves = {leaf["id"]: leaf for leaf in payload["leaves"]}

    assert "## Active pack" in plans
    assert "## Latest closed pack retained as evidence" in plans
    assert "## Historical router markers retained for planning-guard continuity" not in plans
    assert "Historical `next active gate` markers retained for planning-guard continuity" not in plans
    assert "Historical active-pack markers retained for planning-guard continuity" not in plans
    assert plans.count("## Latest closed predecessor evidence") == 1
    assert (
        "2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_GATES_v1.md" in plans
        or "2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_GATES_v1.md" in plans
    )
    assert contains_any(plans, CLEANUP_PLAN_MARKERS) or "## Active pack\n\n- none" in plans

    assert "## Authority order" in agents
    assert "## Behaviour expectations" in agents
    assert "## Anti-drift behaviour" in agents
    assert "`AGENTS.md` is behavioural authority only." in agents
    assert "`docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`" in agents
    assert "## GitHub-native execution workflow" not in agents
    assert "## Required checks before closing a change" not in agents
    assert "## Anti-drift closeout protocol" not in agents
    assert "Makefile is the single front door" not in agents

    assert "## Execution mode" in process_law
    assert "## Control-surface routing law" in process_law
    assert "## Anti-drift closeout law" in process_law
    assert "one gate at a time" in process_law
    assert "one branch per gate" in process_law
    assert "GitHub branch, commit, and merge history is the primary execution ledger" in process_law
    assert "`AGENTS.md` must point here for detailed workflow law." in process_law

    assert (
        "target-repo admitted-evidence successor gate authority retained as evidence for Gates 200-205" in gate_map
        or "latest closed predecessor gate authority retained as evidence for Gates 200-205" in gate_map
    )
    assert (
        "Current active gate: **Gate 208 in the workflow hardening and active-repo reset foundation pack on `work/gate-207-router-and-doctrine-consolidation-20260406`**." in gate_map
        or contains_any(gate_map, CLEANUP_GATE_MAP_MARKERS)
    )
    assert "Historical prior active-gate markers retained for planning-guard continuity" not in gate_map
    assert "Gate 207 | complete on `work/gate-207-router-and-doctrine-consolidation-20260406`" in gate_map
    assert (
        "Gate 208 | active on `work/gate-207-router-and-doctrine-consolidation-20260406`" in gate_map
        or "| Gate 225 | active on `work/gate-225-retained-test-cleanup-closeout-20260406` |" in gate_map
        or "| Gate 225 | complete on `work/gate-225-retained-test-cleanup-closeout-20260406` |" in gate_map
    )

    assert payload["execution_status"] in {
        "gate_208_active",
        "workflow_hardening_and_active_repo_reset_foundation_pack_closed_through_gate_210_on_work_branch",
    }
    assert payload["active_gate"] in {"Gate 208", "none"}
    assert payload["completed_gate_ids"] in (
        ["Gate 206", "Gate 207"],
        ["Gate 206", "Gate 207", "Gate 208", "Gate 209", "Gate 210"],
    )
    assert set(payload["completed_leaf_ids"]).isdisjoint(set(payload["remaining_leaf_ids"]))
    assert leaves["LEAF-G207-001"]["status"] == "complete"
    assert leaves["LEAF-G207-002"]["status"] == "complete"
    assert leaves["LEAF-G208-001"]["status"] in {"planned", "complete"}
    assert leaves["LEAF-G208-002"]["status"] in {"planned", "complete"}

    assert (
        "Gate 207 complete on work/gate-207-router-and-doctrine-consolidation-20260406, Gate 208 active on work/gate-207-router-and-doctrine-consolidation-20260406" in execution_log
        or "The workflow hardening and active-repo reset foundation pack is now closed through Gate 210." in execution_log
    )
    assert "LEAF-G207-001" in execution_log
    assert "LEAF-G207-002" in execution_log
    assert "source .venv/bin/activate && python -m pytest -q tests/test_gate207_router_and_doctrine_consolidation.py" in execution_log
    assert (
        "Gate 208 is now the current active gate on `work/gate-207-router-and-doctrine-consolidation-20260406`." in execution_log
        or "closed through Gate 210" in execution_log
    )
