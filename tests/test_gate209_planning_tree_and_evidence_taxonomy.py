"""Gate 209 planning-tree and evidence taxonomy checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
README = REPO_ROOT / "README.md"
AGENTS = REPO_ROOT / "AGENTS.md"
PROCESS_LAW = REPO_ROOT / "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_EXECUTION_LOG_v1.md"


def test_gate209_taxonomy_closeout_is_coherent() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    agents = AGENTS.read_text(encoding="utf-8")
    process_law = PROCESS_LAW.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    payload = json.loads(LEAVES.read_text(encoding="utf-8"))
    leaves = {leaf["id"]: leaf for leaf in payload["leaves"]}

    assert "## Planning taxonomy" in plans
    assert "active pack authority" in plans
    assert "latest closed pack retained as evidence" in plans
    assert "latest closed predecessor evidence" in plans
    assert "older historical planning material" in plans
    assert "evidence-input-only material" in plans
    assert ("- next active gate: `Gate 210`" in plans) or ("no active pack currently routed" in plans)
    assert "Historical `next active gate` markers retained for planning-guard continuity" not in plans

    assert "Planning taxonomy stays narrow:" in readme
    assert "the active pack named by `PLANS.md` is the only live planning authority" in readme
    assert "the latest closed pack retained as evidence and the latest closed predecessor evidence are comparison material" in readme
    assert "older closed planning material under `docs/planning/` remains historical" in readme
    assert "closeout notes, contradiction reports, scope notes, salvage matrices, indexes" in readme
    assert "No physical planning-tree reshuffle is required" in readme

    assert "## Planning and evidence taxonomy" in process_law
    assert "active pack authority" in process_law
    assert "latest closed pack retained as evidence" in process_law
    assert "latest closed predecessor evidence" in process_law
    assert "older historical planning material" in process_law
    assert "evidence-input-only material" in process_law
    assert "This taxonomy is semantic before it is physical." in process_law
    assert "Physical planning-tree restructuring is deferred" in process_law
    assert "latest closed predecessor evidence, if that helps immediate predecessor traceability" in process_law
    assert "`AGENTS.md` must point here for detailed workflow law." in process_law

    assert "## Authority order" in agents
    assert "`AGENTS.md` is behavioural authority only." in agents
    assert "`README.md` for human onboarding context only" in agents

    assert (
        "Current active gate: **Gate 210 in the workflow hardening and active-repo reset "
        "foundation pack on `work/gate-209-planning-tree-and-evidence-taxonomy-hardening-20260406`**."
    ) in gate_map or "Current active gate: **No active pack currently routed. The successor retained-test cleanup execution pack is closed through Gate 225 on `work/gate-225-retained-test-cleanup-closeout-20260406`.**" in gate_map
    assert "Gate 208 | complete on `main`" in gate_map
    assert "Gate 209 | complete on `work/gate-209-planning-tree-and-evidence-taxonomy-hardening-20260406`" in gate_map
    assert (
        "Gate 210 | active on `work/gate-209-planning-tree-and-evidence-taxonomy-hardening-20260406`" in gate_map
        or "Gate 210 | complete on `work/gate-210-operator-surface-alignment-and-active-repo-cutover-criteria-20260406`" in gate_map
    )

    assert payload["execution_status"] in {"gate_210_active", "workflow_hardening_and_active_repo_reset_foundation_pack_closed_through_gate_210_on_work_branch"}
    assert payload["active_gate"] in {"Gate 210", "none"}
    assert payload["completed_gate_ids"] in (["Gate 206", "Gate 207", "Gate 208", "Gate 209"], ["Gate 206", "Gate 207", "Gate 208", "Gate 209", "Gate 210"])
    assert set(payload["completed_leaf_ids"]).isdisjoint(set(payload["remaining_leaf_ids"]))
    assert "LEAF-G209-001" in payload["completed_leaf_ids"]
    assert "LEAF-G209-002" in payload["completed_leaf_ids"]
    assert payload["remaining_leaf_ids"] in (["LEAF-G210-001", "LEAF-G210-002"], [])
    assert leaves["LEAF-G209-001"]["status"] == "complete"
    assert leaves["LEAF-G209-002"]["status"] == "complete"
    assert leaves["LEAF-G210-001"]["status"] in {"planned", "complete"}
    assert leaves["LEAF-G210-002"]["status"] in {"planned", "complete"}
    assert leaves["LEAF-G209-001"]["validation_commands"] == [
        "python -m pytest -q tests/test_gate209_planning_tree_and_evidence_taxonomy.py"
    ]
    assert leaves["LEAF-G209-002"]["validation_commands"] == [
        "python -m pytest -q tests/test_gate209_planning_tree_and_evidence_taxonomy.py"
    ]

    assert "Gate 208 merged to main via a non-fast-forward merge commit" in execution_log
    assert (
        "Gate 209 complete on work/gate-209-planning-tree-and-evidence-taxonomy-hardening-20260406" in execution_log
        or "Status: closed execution log for workflow hardening and active-repo reset foundation" in execution_log
    )
    assert (
        "Gate 210 active on work/gate-209-planning-tree-and-evidence-taxonomy-hardening-20260406" in execution_log
        or "The workflow hardening and active-repo reset foundation pack is now closed through Gate 210." in execution_log
    )
    assert "LEAF-G209-001" in execution_log
    assert "LEAF-G209-002" in execution_log
    assert "source .venv/bin/activate && python -m pytest -q tests/test_gate209_planning_tree_and_evidence_taxonomy.py" in execution_log
    assert "physical planning-tree restructuring deferred" in execution_log
