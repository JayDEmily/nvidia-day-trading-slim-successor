"""Gate 210 operator-surface alignment and cutover checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
README = REPO_ROOT / "README.md"
MAKEFILE = REPO_ROOT / "Makefile"
AGENTS = REPO_ROOT / "AGENTS.md"
PROCESS_LAW = REPO_ROOT / "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_EXECUTION_LOG_v1.md"
CUTOVER_BRIEF = REPO_ROOT / "docs/planning/2026-04-06_GATE210_SLIM_ACTIVE_REPO_CUTOVER_ENTRY_CRITERIA.md"


def test_gate210_closeout_is_coherent() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    makefile = MAKEFILE.read_text(encoding="utf-8")
    agents = AGENTS.read_text(encoding="utf-8")
    process_law = PROCESS_LAW.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    cutover_brief = CUTOVER_BRIEF.read_text(encoding="utf-8")
    payload = json.loads(LEAVES.read_text(encoding="utf-8"))
    leaves = {leaf["id"]: leaf for leaf in payload["leaves"]}

    assert "## Workflow truth" in readme
    assert "GitHub branch, commit, and merge history is the default execution ledger" in readme
    assert "The planning thread authors packs, reviews scope, and names the leaf-specific proof slice." in readme
    assert "Codex plus local git executes repo mutations, targeted proofs, commits, and pushes." in readme
    assert "Repo-root `PLANS.md` is the live planning router" in readme
    assert "Full-history zip packaging is conditional only: backup, offline transfer, sandbox transfer, or explicit operator request." in readme
    assert "This repo is still the pre-cutover repository." in readme
    assert "Governance and operator-surface gates should default to the targeted proof command named by the active leaf ledger" in readme
    assert "make gate-proof PYTEST_ARGS='tests/test_gate210_operator_surface_alignment_and_cutover.py'" in readme

    assert "help:" in makefile
    assert "test         repo-wide pytest run" in makefile
    assert "test-unit    compatibility alias for the repo-wide pytest run" in makefile
    assert "gate-proof   targeted pytest slice; pass PYTEST_ARGS='tests/test_...'" in makefile
    assert "check        broad proof path: format, lint, typecheck, and repo-wide pytest" in makefile
    assert "gate-proof:" in makefile
    assert "Set PYTEST_ARGS to a targeted pytest path or expression." in makefile
    assert "# Compatibility alias until the repo maintains a true unit-only selection." in makefile

    assert "## Active pack" in plans
    assert "- no active pack currently routed" in plans
    assert "## Latest closed pack retained as evidence" in plans
    assert "2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_GATES_v1.md" in plans
    assert "2026-04-06_GATE210_SLIM_ACTIVE_REPO_CUTOVER_ENTRY_CRITERIA.md" in plans
    assert "workflow hardening and active-repo reset foundation pack closed through Gate 210" in plans
    assert "Gate 210 active" not in plans
    assert "- next active gate: `Gate 210`" not in plans

    assert "`AGENTS.md` is behavioural authority only." in agents
    assert "`README.md` for human onboarding context only" in agents
    assert "GitHub branch, commit, and merge history is the primary execution ledger" in process_law
    assert "Routine zip handoff is deprecated for ordinary execution." in process_law
    assert "Physical planning-tree restructuring is deferred" in process_law

    assert "Version: v1.28" in gate_map
    assert "Current active gate: **none." in gate_map
    assert "no later pack is active yet" in gate_map
    assert "Gate 210 | complete on `work/gate-210-operator-surface-alignment-and-active-repo-cutover-criteria-20260406`" in gate_map
    assert "tests/test_gate210_operator_surface_alignment_and_cutover.py" in gate_map
    assert "Gate 210 | active on `work/gate-209-planning-tree-and-evidence-taxonomy-hardening-20260406`" not in gate_map

    assert "## Purpose" in cutover_brief
    assert "## Already complete upstream" in cutover_brief
    assert "## Entry criteria before any slim-repo cutover starts" in cutover_brief
    assert "## What must be frozen before the cutover" in cutover_brief
    assert "## What the slim active-repo successor should contain" in cutover_brief
    assert "## What stays behind as archive and evidence" in cutover_brief
    assert "## What the first pack in the slim repo is expected to do" in cutover_brief
    assert "## What must not be claimed as already executed" in cutover_brief
    assert "Gate 210 has been merged to `main` and the merge receipt is recorded." in cutover_brief
    assert "Repo-root `PLANS.md` routes no active pack in this source repo." in cutover_brief
    assert "`07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER` substantive work has started" in cutover_brief

    assert payload["execution_status"] == (
        "workflow_hardening_and_active_repo_reset_foundation_pack_closed_through_gate_210_on_work_branch"
    )
    assert payload["active_gate"] == "none"
    assert payload["completed_gate_ids"] == [
        "Gate 206",
        "Gate 207",
        "Gate 208",
        "Gate 209",
        "Gate 210",
    ]
    assert set(payload["completed_leaf_ids"]).isdisjoint(set(payload["remaining_leaf_ids"]))
    assert payload["remaining_leaf_ids"] == []
    assert leaves["LEAF-G210-001"]["status"] == "complete"
    assert leaves["LEAF-G210-002"]["status"] == "complete"
    assert leaves["LEAF-G210-001"]["validation_commands"] == [
        "python -m pytest -q tests/test_gate210_operator_surface_alignment_and_cutover.py"
    ]
    assert leaves["LEAF-G210-002"]["validation_commands"] == [
        "python -m pytest -q tests/test_gate210_operator_surface_alignment_and_cutover.py"
    ]
    assert "docs/planning/2026-04-06_GATE210_SLIM_ACTIVE_REPO_CUTOVER_ENTRY_CRITERIA.md" in leaves["LEAF-G210-002"]["repo_surfaces"]

    assert "Status: closed execution log for workflow hardening and active-repo reset foundation through Gate 210" in execution_log
    assert "## Gate 210 receipts" in execution_log
    assert "LEAF-G210-001" in execution_log
    assert "LEAF-G210-002" in execution_log
    assert "source .venv/bin/activate && python -m pytest -q tests/test_gate210_operator_surface_alignment_and_cutover.py" in execution_log
    assert "No later pack is active, and no slim-repo execution work has started in this branch." in execution_log
