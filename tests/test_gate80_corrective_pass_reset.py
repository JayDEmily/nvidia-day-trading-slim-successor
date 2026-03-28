"""Gate 80 corrective-pass reset integrity checks."""

from __future__ import annotations

import json
from pathlib import Path

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

    assert (
        "The active corrective reconstruction pair from Gate 80 onward is:" in plans
        or "The completed corrective reconstruction pair retained as predecessor evidence is:" in plans
    )
    assert "2026-03-27_REVIEW_RECONSTRUCTION_CORRECTIVE_GATES_v1.md" in plans
    assert "2026-03-27_REVIEW_RECONSTRUCTION_CORRECTIVE_LEAVES_v1.json" in plans
    assert "Gate 80 — complete on `main`" in plans
    assert (
        "Gate 81 is next" in plans
        or "Corrective review-reconstruction tranche (Gates 80–87) complete on `main`." in plans
        or "Corrective review-reconstruction tranche (Gates 80–87) is complete on `main` and retained as predecessor evidence." in plans
    )
    assert "2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v6.md" in plans


def test_gate_map_marks_gate80_complete_and_gate81_next() -> None:
    gate_map = GATE_MAP.read_text()

    assert (
        "Current active gate: **Gate 81 in the corrective reconstruction pack**." in gate_map
    ) or (
        "Current active gate: **none — the corrective reconstruction pack is closed through Gate 87 on `main`**."
        in gate_map
    ) or (
        "Current active gate: **Gate 88 in the financial-calendar interstitial pack**."
        in gate_map
    ) or (
        "Current active gate: **Gate 89 in the financial-calendar interstitial pack**."
        in gate_map
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
