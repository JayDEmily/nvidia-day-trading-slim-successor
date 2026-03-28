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
    assert "Gate 88 — complete on `main`" in plans
    assert "Gate 89 — complete on `main`" in plans
    assert "Gate 90 — complete on `main`" in plans
    assert "Gate 91 — planned; next active gate on `main`" in plans

    assert "Current active gate: **Gate 91 in the financial-calendar interstitial pack**." in gate_map
    assert "| Gate 88 | complete on `main` |" in gate_map
    assert "| Gate 89 | complete on `main` |" in gate_map
    assert "| Gate 90 | complete on `main` |" in gate_map
    assert "| Gate 91 | planned; next active gate |" in gate_map
    assert "| Gate 93 | planned |" in gate_map

    assert "2026-03-28_FINANCIAL_CALENDAR_INTERSTITIAL_EXECUTION_LOG_v1.md" in agents


def test_gates_doc_freezes_workflow_transition_and_dmp_constraints() -> None:
    gates = GATES.read_text(encoding="utf-8")

    assert "## Workflow transition and module disposition" in gates
    assert "### Retain as canonical" in gates
    assert "### Retire from authority" in gates
    assert "SessionClockCompatibilityPayload" in gates
    assert "PreparedRuntimeSnapshot.next_event_at" in gates
    assert "SessionCalendarCreate` and `MarketEventCreate" in gates
    assert "Retire from authority does **not** mean blind deletion." in gates
    assert "state_conditioned_modifier`, `playbook_eligibility`, `carry_handoff`" in gates
    assert "## DMP v2 compatibility constraint" in gates
    assert "must **not** be copied verbatim" in gates
    assert "## Canonical transit rule" in gates
    assert "must **not** be flattened straight into `session_clock`, `next_event_at`, or a lone `event_window_state` label" in gates


def test_leaves_doc_marks_gate88_active_and_freezes_no_flattening_rules() -> None:
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert leaves["governing_plan"] == "docs/planning/2026-03-28_FINANCIAL_CALENDAR_INTERSTITIAL_GATES_v3.md"
    assert leaves["execution_status"] == "gate_91_financial_calendar_canonical_projection_active_after_gate_90"
    assert leaves["active_gate"] == "Gate 91"
    assert leaves["completed_gate_ids"] == ["Gate 88", "Gate 89", "Gate 90"]
    assert leaves["completed_leaf_ids"] == ["LEAF-G88-001", "LEAF-G88-002", "LEAF-G88-003", "LEAF-G88-004", "LEAF-G88-005", "LEAF-G89-001", "LEAF-G89-002", "LEAF-G89-003", "LEAF-G89-004", "LEAF-G90-001", "LEAF-G90-002", "LEAF-G90-003", "LEAF-G90-004"]
    assert leaves["remaining_leaf_ids"][0] == "LEAF-G91-001"
    assert leaves["global_rules"]["retire_from_authority_not_delete"] is True
    assert leaves["global_rules"]["dmp_v2_example_packet_must_not_be_copied_verbatim"] is True
    assert leaves["global_rules"]["no_free_text_event_taxonomy_expansion"] is True
    assert "next_event_at_as_primary_event_system" in leaves["global_rules"]["must_not_flatten_into"]
    assert "carry_handoff" in leaves["global_rules"]["downstream_consumers_must_not_read_raw_bundle_or_import_stage_records"]


def test_execution_log_is_active_but_not_claiming_gate88_execution() -> None:
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")

    assert "Status: active execution log for the financial-calendar planning pack; Gate 88, Gate 89, and Gate 90 complete on `main`, Gate 91 next" in execution_log
    assert "### LEAF-G90-001 — Land the external tranche artefacts under a repo-controlled reference-data path" in execution_log


def test_repo_root_docs_no_longer_claim_a_three_file_quartet_or_unconditional_scope_note() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    agents = AGENTS.read_text(encoding="utf-8")

    assert "The active financial-calendar planning pack from Gate 88 onward is:" in plans
    assert "only if repo-root `PLANS.md` names one" in agents
    assert "active planning control surfaces govern **what work is active now**" in agents


def test_gate88_leaves_are_complete_and_gate89_begins_the_remaining_queue() -> None:
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    gate88 = [leaf for leaf in leaves["leaves"] if leaf["gate"] == "Gate 88"]
    assert len(gate88) == 5
    assert all(leaf["status"] == "complete" for leaf in gate88)
    assert all(leaf["id"] not in leaves["remaining_leaf_ids"] for leaf in gate88)
    gate89 = [leaf for leaf in leaves["leaves"] if leaf["gate"] == "Gate 89"]
    assert len(gate89) == 4
    assert all(leaf["status"] == "complete" for leaf in gate89)
    gate90 = [leaf for leaf in leaves["leaves"] if leaf["gate"] == "Gate 90"]
    assert len(gate90) == 4
    assert all(leaf["status"] == "complete" for leaf in gate90)
    gate91_first = next(leaf for leaf in leaves["leaves"] if leaf["id"] == "LEAF-G91-001")
    assert gate91_first["status"] == "planned; next active leaf"
