"""Planning integrity checks for Gate 51+ cognitive-workflow implementation docs."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
GATES = REPO_ROOT / "docs/planning/2026-03-26_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-26_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v1.json"
IMPLEMENTATION_MAP = REPO_ROOT / "docs/planning/2026-03-26_COGNITIVE_WORKFLOW_IMPLEMENTATION_MAP.md"
BOUNDARY_RULES = REPO_ROOT / "docs/planning/2026-03-26_COGNITIVE_WORKFLOW_BOUNDARY_RULES.md"
CALENDAR = REPO_ROOT / "docs/planning/2026-03-26_CALENDAR_HORIZON_OWNERSHIP.md"
GATE52 = REPO_ROOT / "docs/planning/2026-03-26_GATE52_NATIVE_PLAYBOOK_HIERARCHY_IMPLEMENTATION.md"
GATE53 = REPO_ROOT / "docs/planning/2026-03-26_GATE53_CARRY_WEEKEND_EVENT_FORMALISATION.md"
PLANS = REPO_ROOT / "PLANS.md"


def test_gate51_docs_exist_and_gate_pack_marks_gate55_complete() -> None:
    gates_text = GATES.read_text()
    leaves = json.loads(LEAVES.read_text())

    assert (
        "Status: Gates 51–55 complete on `main`; successor pack closed through Gate 55"
        in gates_text
    )
    assert leaves["execution_status"] == "gate_55_complete_on_main_pack_closed"
    assert leaves["completed_gate_ids"] == [
        "Gate 51",
        "Gate 52",
        "Gate 53",
        "Gate 54",
        "Gate 55",
    ]
    assert leaves["active_gate"] == "none_pack_closed_after_gate_55"
    assert leaves["completed_leaf_ids"] == [
        "LEAF-G51-001",
        "LEAF-G51-002",
        "LEAF-G51-003",
        "LEAF-G52-001",
        "LEAF-G52-002",
        "LEAF-G52-003",
        "LEAF-G53-001",
        "LEAF-G53-002",
        "LEAF-G53-003",
        "LEAF-G54-001",
        "LEAF-G54-002",
        "LEAF-G54-003",
        "LEAF-G55-001",
        "LEAF-G55-002",
    ]


def test_gate51_outputs_pin_step0_and_candidate_boundaries() -> None:
    implementation_map = IMPLEMENTATION_MAP.read_text()
    boundary_rules = BOUNDARY_RULES.read_text()
    calendar = CALENDAR.read_text()
    gate52 = GATE52.read_text()
    gate53 = GATE53.read_text()
    gate_map = (REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md").read_text()

    assert (
        "Step 0 calendar/horizon routing is real, but it is not a hidden eighth analysis stage."
        in implementation_map
    )
    assert (
        "Candidate family generation is owned by the **playbook-selection grammar slot**."
        in implementation_map
    )
    assert "Carry-horizon decisioning is owned by the **carry branch**" in implementation_map
    assert "Step 0 is an **explicit runtime routing concern**." in calendar
    assert "Carry begins only at an explicit handoff boundary" in boundary_rules
    assert "family -> setup_variant -> execution_expression" in gate52
    assert "weekend, ordinary overnight, and event carry" in gate53
    assert "Gates 51–55 are complete on `main`" in gate_map
    assert ("Gate 128 is complete on `main`" in gate_map) or ("Gate 129 is active on `main`" in gate_map) or ("Gate 130 is active on `main`" in gate_map) or ("Gates 128-130 are complete on `main`; Gate 131 is active on `main`." in gate_map) or ("Gates 128-131 are complete on `main`." in gate_map)
