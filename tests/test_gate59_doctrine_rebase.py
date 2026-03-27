"""Gate 59 doctrine rebase integrity checks."""

from __future__ import annotations

import json
import re
from pathlib import Path

from tests._successor_pack_helpers import successor_pack_position

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = (
    REPO_ROOT / "docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v6.md"
)
LEAVES = (
    REPO_ROOT
    / "docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v6.json"
)
NORMATIVE = REPO_ROOT / "docs/01_NORMATIVE.md"
OPERATING_MODEL = REPO_ROOT / "docs/02_OPERATING_MODEL.md"
GUARDRAILS = REPO_ROOT / "docs/05_GUARDRAILS.md"
LEGACY_GATES_V45 = (
    REPO_ROOT / "docs/legacy/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v4_5.md"
)
LEGACY_LEAVES_V45 = (
    REPO_ROOT
    / "docs/legacy/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v4_5.json"
)


def _section(text: str, heading: str, next_heading: str) -> str:
    start = text.index(heading)
    end = text.index(next_heading, start)
    return text[start:end]


def test_v6_pair_remains_closed_predecessor_evidence_while_corrective_pair_is_active() -> (
    None
):
    plans = PLANS.read_text()
    gate_map = GATE_MAP.read_text()

    assert (
        "Completed predecessor modification pairs retained as in-repo evidence are:"
        in plans
    )
    assert "2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v6.md" in plans
    assert "2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v6.json" in plans
    assert "The active corrective reconstruction pair from Gate 80 onward is:" in plans
    assert "2026-03-27_REVIEW_RECONSTRUCTION_CORRECTIVE_GATES_v1.md" in plans
    assert "2026-03-27_REVIEW_RECONSTRUCTION_CORRECTIVE_LEAVES_v1.json" in plans
    assert "Gate 59 doctrine rebase complete on `main`" in plans

    assert "closed successor-pack evidence for Gates 59–79" in gate_map
    assert "2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v6.md" in gate_map
    assert "active corrective reconstruction gate surface" in gate_map
    assert (
        "Current active gate: **Gate 81 in the corrective reconstruction pack**."
        in gate_map
    )


def test_v6_gates_doc_is_self_contained_and_governing_inputs_do_not_depend_on_missing_drafts() -> (
    None
):
    gates_text = GATES.read_text()
    governing_inputs = _section(
        gates_text,
        "## Governing inputs",
        "## Historical salvage consulted for Gate 59 closeout",
    )

    assert (
        "2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v4.md" not in governing_inputs
    )
    assert (
        "2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v4.json"
        not in governing_inputs
    )
    assert (
        "2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v4_5.md"
        not in governing_inputs
    )
    assert (
        "2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v4_5.json"
        not in governing_inputs
    )
    assert (
        "2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v5.md" not in governing_inputs
    )
    assert (
        "2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v5.json"
        not in governing_inputs
    )
    assert (
        "No missing `v4` or `v5` draft is a governing dependency of this tranche."
        in gates_text
    )
    assert "Status: complete on `main`" in _section(
        gates_text,
        "## Gate 59 — Doctrine rebase and tranche reset",
        "## Gate 60 — State-policy vocabulary and coefficient ontology",
    )


def test_gate59_doctrine_statements_land_across_normative_operating_and_guardrail_surfaces() -> (
    None
):
    normative = NORMATIVE.read_text()
    operating_model = OPERATING_MODEL.read_text()
    guardrails = GUARDRAILS.read_text()

    assert (
        "stable cognition grammar and only allows bounded, approved change in operating posture"
        in normative
    )
    assert (
        "live paper is the falsification and promotion surface for locked candidates"
        in normative
    )
    assert "review does not imply change" in normative.lower()
    assert (
        "runtime never invents new coefficients or hidden policy in place"
        in normative.lower()
    )

    assert "Historical replay is the research/discovery surface." in operating_model
    assert (
        "Live paper is the falsification/promotion surface for locked candidates"
        in operating_model
    )
    assert "Review may end in `no_change`" in operating_model

    assert (
        "**Stable cognition grammar is preserved unless a deliberate normative change proves otherwise.**"
        in guardrails
    )
    assert (
        "**Live paper is falsification/promotion only, never in-place coefficient discovery.**"
        in guardrails
    )
    assert (
        "**Runtime never invents coefficients or hidden policy in place.**"
        in guardrails
    )


def test_v6_leaves_ledger_marks_gate59_complete_and_gate60_next() -> None:
    leaves = json.loads(LEAVES.read_text())

    assert (
        leaves["governing_plan"]
        == "docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v6.md"
    )
    assert leaves["execution_status"].startswith("gate_") and (
        "_successor_pack_active_from_gate_" in leaves["execution_status"]
        or "_successor_pack_closed_after_gate_" in leaves["execution_status"]
    )
    assert leaves["completed_gate_ids"][:6] == [
        "Gate 59",
        "Gate 60",
        "Gate 61",
        "Gate 62",
        "Gate 63",
        "Gate 64",
    ]
    assert successor_pack_position(leaves["active_gate"]) >= 65
    assert leaves["completed_leaf_ids"][:6] == [
        "LEAF-G59-001",
        "LEAF-G59-002",
        "LEAF-G59-003",
        "LEAF-G59-004",
        "LEAF-G59-005",
        "LEAF-G59-006",
    ]

    gate59 = [leaf for leaf in leaves["leaves"] if leaf["gate"] == "Gate 59"]
    assert len(gate59) == 6
    assert all(leaf["status"] == "complete" for leaf in gate59)
    assert all(leaf["id"] not in leaves["remaining_leaf_ids"] for leaf in gate59)


def test_v6_gate_order_and_leaves_order_are_monotonic() -> None:
    gates_text = GATES.read_text()
    leaves = json.loads(LEAVES.read_text())

    gate_numbers_from_md = [
        int(match)
        for match in re.findall(r"^## Gate (\d+) —", gates_text, flags=re.MULTILINE)
    ]
    assert gate_numbers_from_md == list(range(59, 80))

    gate_numbers_from_leaves = []
    for leaf in leaves["leaves"]:
        gate_no = int(leaf["gate"].split()[1])
        if gate_no not in gate_numbers_from_leaves:
            gate_numbers_from_leaves.append(gate_no)
    assert gate_numbers_from_leaves == list(range(59, 80))


def test_archived_salvage_pair_is_preserved_inside_git_but_not_active() -> None:
    assert LEGACY_GATES_V45.exists()
    assert LEGACY_LEAVES_V45.exists()
    legacy_text = LEGACY_GATES_V45.read_text()
    assert "archived context only; not an active planning authority" in legacy_text
