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


def test_runtime_integration_pack_is_retained_as_closed_predecessor_evidence() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    agents = AGENTS.read_text(encoding="utf-8")

    assert (
        "post-flight repo consistency pack active at Gate 128" in plans
        or "post-flight repo consistency pack active at Gate 129" in plans
        or "post-flight repo consistency pack active at Gate 130" in plans
        or "post-flight repo consistency pack active at Gate 131" in plans
        or "no active pack currently routed; post-flight repo consistency pack closed through Gate 131 on `main`" in plans
    )
    assert "signal-coefficient authority pack closed through Gate 127" in plans

    assert "2026-03-29_FINANCIAL_CALENDAR_RUNTIME_INTEGRATION_GATES_v2.md" in gate_map
    assert "2026-03-29_FINANCIAL_CALENDAR_RUNTIME_INTEGRATION_LEAVES_v2.json" in gate_map
    assert "| Gate 91 | complete on `main` |" in gate_map
    assert "| Gate 92 | complete on `main` |" in gate_map
    assert "| Gate 93 | complete on `main` |" in gate_map
    assert (
        "Current active gate: **Gate 128 in the post-flight repo consistency pack**." in gate_map
        or "Current active gate: **Gate 129 in the post-flight repo consistency pack**." in gate_map
        or "Current active gate: **Gate 130 in the post-flight repo consistency pack**." in gate_map
        or "Current active gate: **Gate 131 in the post-flight repo consistency pack**." in gate_map
        or "Current active gate: **none — post-flight repo consistency pack closed through Gate 131 on `main`**." in gate_map
    )

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


def test_leaves_doc_marks_runtime_integration_pack_closed_through_gate93() -> None:
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert leaves["governing_plan"] == "docs/planning/2026-03-29_FINANCIAL_CALENDAR_RUNTIME_INTEGRATION_GATES_v2.md"
    assert leaves["execution_status"] == "gate_93_financial_calendar_runtime_integration_closed_on_main"
    assert leaves["active_gate"] == "none — runtime-integration pack closed through Gate 93 on main"
    assert leaves["completed_gate_ids"] == ["Gate 88", "Gate 89", "Gate 90", "Gate 91", "Gate 92", "Gate 93"]
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
        "LEAF-G93-001",
        "LEAF-G93-002",
        "LEAF-G93-003",
        "LEAF-G93-004",
        "LEAF-G93-005",
    ]
    assert leaves["remaining_leaf_ids"] == []
    assert leaves["global_rules"]["raw_bundle_and_import_records_must_not_be_direct_downstream_inputs"] is True
    assert leaves["global_rules"]["compatibility_hints_must_remain_explicitly_non_canonical"] is True


def test_execution_log_contains_gate93_entries_and_closed_status() -> None:
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")

    assert "Status: closed execution log for the reviewed financial-calendar runtime-integration tranche; Gates 91-93 complete on `main`, no active gate" in execution_log
    assert "### LEAF-G91-001 — Project venue-state facts into desk-calendar authority surfaces" in execution_log
    assert "### LEAF-G93-005 — Add anti-drift proof that runtime integration cannot be claimed complete while legacy active truth remains" in execution_log
