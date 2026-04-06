"""Gate 207 router and doctrine consolidation checks."""

from __future__ import annotations

import json
from pathlib import Path

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
    assert "- next active gate: `Gate 208`" in plans
    assert "Gate 208 active on `work/gate-207-router-and-doctrine-consolidation-20260406`" in plans

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

    assert "target-repo admitted-evidence successor gate authority retained as evidence for Gates 200-205" in gate_map
    assert "Current active gate: **Gate 208 in the workflow hardening and active-repo reset foundation pack on `work/gate-207-router-and-doctrine-consolidation-20260406`**." in gate_map
    assert "Historical prior active-gate markers retained for planning-guard continuity" not in gate_map
    assert "Gate 207 | complete on `work/gate-207-router-and-doctrine-consolidation-20260406`" in gate_map
    assert "Gate 208 | active on `work/gate-207-router-and-doctrine-consolidation-20260406`" in gate_map

    assert payload["execution_status"] == "gate_208_active"
    assert payload["active_gate"] == "Gate 208"
    assert payload["completed_gate_ids"] == ["Gate 206", "Gate 207"]
    assert set(payload["completed_leaf_ids"]).isdisjoint(set(payload["remaining_leaf_ids"]))
    assert leaves["LEAF-G207-001"]["status"] == "complete"
    assert leaves["LEAF-G207-002"]["status"] == "complete"
    assert leaves["LEAF-G208-001"]["status"] == "planned"
    assert leaves["LEAF-G208-002"]["status"] == "planned"

    assert "Gate 207 complete on work/gate-207-router-and-doctrine-consolidation-20260406, Gate 208 active on work/gate-207-router-and-doctrine-consolidation-20260406" in execution_log
    assert "LEAF-G207-001" in execution_log
    assert "LEAF-G207-002" in execution_log
    assert "source .venv/bin/activate && python -m pytest -q tests/test_gate207_router_and_doctrine_consolidation.py" in execution_log
    assert "Gate 208 is now the current active gate on `work/gate-207-router-and-doctrine-consolidation-20260406`." in execution_log
