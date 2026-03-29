"""Financial-calendar planning-pack authority checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
AGENTS = REPO_ROOT / "AGENTS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-03-29_FINANCIAL_CALENDAR_RUNTIME_INTEGRATION_GATES_v2.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-29_FINANCIAL_CALENDAR_RUNTIME_INTEGRATION_LEAVES_v2.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-03-29_FINANCIAL_CALENDAR_RUNTIME_INTEGRATION_EXECUTION_LOG_v2.md"


def test_active_planning_surfaces_point_at_the_runtime_integration_pack() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    agents = AGENTS.read_text(encoding="utf-8")

    assert "2026-03-29_FINANCIAL_CALENDAR_RUNTIME_INTEGRATION_GATES_v2.md" in plans
    assert "2026-03-29_FINANCIAL_CALENDAR_RUNTIME_INTEGRATION_LEAVES_v2.json" in plans
    assert "2026-03-29_FINANCIAL_CALENDAR_RUNTIME_INTEGRATION_EXECUTION_LOG_v2.md" in plans
    assert "Gate 91 — complete on `main`" in plans
    assert "Gate 92 — complete on `main`" in plans

    assert "Current active gate: **Gate 93 in the financial-calendar runtime-integration pack**." in gate_map
    assert "| Gate 91 | complete on `main` |" in gate_map
    assert "| Gate 92 | complete on `main` |" in gate_map
    assert "| Gate 93 | planned; next active gate |" in gate_map

    assert "the active execution log named by repo-root `PLANS.md`" in agents


def test_gates_doc_freezes_projection_transition_and_non_canonical_rules() -> None:
    gates = GATES.read_text(encoding="utf-8")

    assert "## Retain / retire-from-authority / amend / add matrix" in gates
    assert "### Retire from authority (compatibility-only unless later removed)" in gates
    assert "PreparedRuntimeSnapshot.next_event_at" in gates
    assert "SessionCalendarCreate and `MarketEventCreate`" in gates or "SessionCalendarCreate` and `MarketEventCreate" in gates
    assert "Later consumers must not read directly:" in gates
    assert "raw bundle JSON files" in gates
    assert "import-stage records as if they were runtime truth" in gates
    assert "next_event_at` as the sole event system" in gates


def test_leaves_doc_marks_gate92_complete_and_gate93_active() -> None:
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert leaves["governing_plan"] == "docs/planning/2026-03-29_FINANCIAL_CALENDAR_RUNTIME_INTEGRATION_GATES_v2.md"
    assert leaves["execution_status"] == "gate_93_financial_calendar_downstream_alignment_active_after_gate_92"
    assert leaves["active_gate"] == "Gate 93"
    assert leaves["completed_gate_ids"] == ["Gate 88", "Gate 89", "Gate 90", "Gate 91", "Gate 92"]
    assert leaves["completed_leaf_ids"] == [
        "LEAF-G91-001",
        "LEAF-G91-002",
        "LEAF-G91-003",
        "LEAF-G91-004",
        "LEAF-G91-005",
        "LEAF-G91-006",
        "LEAF-G92-001",
        "LEAF-G92-002",
        "LEAF-G92-003",
        "LEAF-G92-004",
        "LEAF-G92-005",
        "LEAF-G92-006",
    ]
    assert leaves["remaining_leaf_ids"][0] == "LEAF-G93-001"
    assert leaves["global_rules"]["raw_bundle_and_import_records_must_not_be_direct_downstream_inputs"] is True
    assert leaves["global_rules"]["compatibility_hints_must_remain_explicitly_non_canonical"] is True


def test_execution_log_contains_gate92_entries_and_gate93_next_status() -> None:
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")

    assert "Status: active execution log for the reviewed financial-calendar runtime-integration tranche; Gates 91-92 complete on `main`, Gate 93 next" in execution_log
    assert "### LEAF-G91-001 — Project venue-state facts into desk-calendar authority surfaces" in execution_log
    assert "### LEAF-G92-006 — Prove bounded temporal outputs preserve the rich meaning required by later consumers" in execution_log
