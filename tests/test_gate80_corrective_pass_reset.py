"""Gate 80 corrective-pass reset integrity checks."""

from __future__ import annotations

import json
from pathlib import Path

from ._planning_later_state_helpers import CLEANUP_GATE_MAP_MARKERS, CLEANUP_PLAN_MARKERS, contains_any

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
EXECUTION_LOG = (
    REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_EXTENSION_EXECUTION_LOG_v3.md"
)
GATES = REPO_ROOT / "docs/planning/2026-03-27_REVIEW_RECONSTRUCTION_CORRECTIVE_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-27_REVIEW_RECONSTRUCTION_CORRECTIVE_LEAVES_v1.json"
GUARDRAILS = REPO_ROOT / "docs/05_GUARDRAILS.md"


def test_corrective_pair_is_the_active_post_gate79_pointer() -> None:
    plans = PLANS.read_text()
    gate_map = GATE_MAP.read_text()

    assert (
        contains_any(plans, CLEANUP_PLAN_MARKERS)
        or
        "post-flight repo consistency pack active at Gate 128" in plans
        or "post-flight repo consistency pack active at Gate 129" in plans
        or "post-flight repo consistency pack active at Gate 130" in plans
        or "post-flight repo consistency pack active at Gate 131" in plans
        or "no active pack currently routed; post-flight repo consistency pack closed through Gate 131 on `main`" in plans
        or "stage-local handoff and terminal-risk seams pack closed through Gate 149 on `main`" in plans
        or "active gate: Gate 149 reopened on `work/gate-149-reopen-full-suite-closeout-20260402`" in plans
    )
    assert "Gates 59–79 are complete on `main`" in gate_map
    assert "Gates 80–87 are complete on `main`" in gate_map
    assert "2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v6.md" in gate_map


def test_gate_map_marks_gate80_complete_and_gate81_next() -> None:
    gate_map = GATE_MAP.read_text()

    assert (
        contains_any(gate_map, CLEANUP_GATE_MAP_MARKERS)
    ) or (
        "Current active gate: **Gate 81 in the corrective reconstruction pack**." in gate_map
    ) or (
        "Current active gate: **none — the corrective reconstruction pack is closed through Gate 87 on `main`**." in gate_map
    ) or (
        "Current active gate: **Gate 88 in the financial-calendar interstitial pack**." in gate_map
    ) or (
        "Current active gate: **Gate 89 in the financial-calendar interstitial pack**." in gate_map
    ) or (
        "Current active gate: **Gate 128 in the post-flight repo consistency pack**." in gate_map
    ) or (
        "Current active gate: **Gate 129 in the post-flight repo consistency pack**." in gate_map
    ) or (
        "Current active gate: **Gate 130 in the post-flight repo consistency pack**." in gate_map
    ) or (
        "Current active gate: **Gate 131 in the post-flight repo consistency pack**." in gate_map
    ) or (
        "Current active gate: **none — post-flight repo consistency pack closed through Gate 131 on `main`**." in gate_map
    ) or (
        "Current active gate: **Gate 149 in the stage-local handoff and terminal-risk seams pack**." in gate_map
    ) or (
        "Current active gate: **none — stage-local handoff and terminal-risk seams pack closed through Gate 149 on `main`**." in gate_map
    )
    assert "| Gate 80 | complete on `main` |" in gate_map
    assert (
        "| Gate 81 | planned; next active gate |" in gate_map
        or "| Gate 81 | complete on `main` |" in gate_map
    )


def test_corrective_leaves_mark_gate80_complete_and_gate81_next() -> None:
    leaves = json.loads(LEAVES.read_text())

    assert (
        leaves["governing_plan"]
        == "docs/planning/2026-03-27_REVIEW_RECONSTRUCTION_CORRECTIVE_GATES_v1.md"
    )
    assert leaves["execution_status"].startswith("gate_")
    assert leaves["completed_gate_ids"][0] == "Gate 80"
    assert leaves["completed_leaf_ids"][:2] == ["LEAF-G80-001", "LEAF-G80-002"]
    assert leaves["active_gate"] in {"Gate 81", "none"}
    assert "LEAF-G80-001" not in leaves["remaining_leaf_ids"]
    assert "LEAF-G80-002" not in leaves["remaining_leaf_ids"]


def test_gate80_execution_log_and_guardrails_cleanup_are_recorded() -> None:
    execution_log = EXECUTION_LOG.read_text()
    guardrails = GUARDRAILS.read_text()
    gates = GATES.read_text()

    assert "### Gate 80 corrective-pass reset and guidance cleanup" in execution_log
    assert guardrails.count("## Required runtime guardrails") == 1
    assert (
        "Status: Gate 80 complete on `main`; active corrective execution continues at Gate 81"
        in gates
    ) or ("Status: complete on `main`; corrective tranche closed through Gate 87" in gates)
    assert "### Gate 80 closeout note" in gates
