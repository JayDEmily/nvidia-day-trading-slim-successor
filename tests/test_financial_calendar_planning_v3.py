"""Financial-calendar planning-pack authority checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
AGENTS = REPO_ROOT / "AGENTS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-03-28_FINANCIAL_CALENDAR_INTERSTITIAL_GATES_v3.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-28_FINANCIAL_CALENDAR_INTERSTITIAL_LEAVES_v3.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-03-28_FINANCIAL_CALENDAR_INTERSTITIAL_EXECUTION_LOG_v1.md"


def test_active_planning_surfaces_point_at_the_financial_calendar_pack() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    agents = AGENTS.read_text(encoding="utf-8")

    assert "2026-03-28_FINANCIAL_CALENDAR_INTERSTITIAL_GATES_v3.md" in plans
    assert "2026-03-28_FINANCIAL_CALENDAR_INTERSTITIAL_LEAVES_v3.json" in plans
    assert "2026-03-28_FINANCIAL_CALENDAR_INTERSTITIAL_EXECUTION_LOG_v1.md" in plans
    assert "Gate 88 — planned; next active gate on `main`" in plans

    assert "Current active gate: **Gate 88 in the financial-calendar interstitial pack**." in gate_map
    assert "| Gate 88 | planned; next active gate |" in gate_map
    assert "| Gate 93 | planned |" in gate_map

    assert "2026-03-28_FINANCIAL_CALENDAR_INTERSTITIAL_EXECUTION_LOG_v1.md" in agents


def test_gates_doc_freezes_workflow_transition_and_dmp_constraints() -> None:
    gates = GATES.read_text(encoding="utf-8")

    assert "## Workflow transition and module disposition" in gates
    assert "### Retain as canonical" in gates
    assert "### Retire from authority" in gates
    assert "Retire from authority does **not** mean blind deletion." in gates
    assert "## DMP v2 compatibility constraint" in gates
    assert "must **not** be copied verbatim" in gates
    assert "## Canonical transit rule" in gates
    assert "must **not** be flattened straight into `session_clock`, `next_event_at`, or a lone `event_window_state` label" in gates


def test_leaves_doc_marks_gate88_active_and_freezes_no_flattening_rules() -> None:
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert leaves["governing_plan"] == "docs/planning/2026-03-28_FINANCIAL_CALENDAR_INTERSTITIAL_GATES_v3.md"
    assert leaves["execution_status"] == "gate_88_financial_calendar_pack_active"
    assert leaves["active_gate"] == "Gate 88"
    assert leaves["completed_gate_ids"] == []
    assert leaves["remaining_leaf_ids"][0] == "LEAF-G88-001"
    assert leaves["global_rules"]["retire_from_authority_not_delete"] is True
    assert leaves["global_rules"]["dmp_v2_example_packet_must_not_be_copied_verbatim"] is True
    assert "next_event_at_as_primary_event_system" in leaves["global_rules"]["must_not_flatten_into"]


def test_execution_log_is_active_but_not_claiming_gate88_execution() -> None:
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")

    assert "Status: active execution log for the financial-calendar planning pack" in execution_log
    assert "It does **not** count as a Gate 88 implementation receipt." in execution_log
