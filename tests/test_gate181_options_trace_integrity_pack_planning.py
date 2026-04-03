"""Planning-pack checks for the options-trace integrity repair pack."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-03_OPTIONS_TRACE_INTEGRITY_REPAIR_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-03_OPTIONS_TRACE_INTEGRITY_REPAIR_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-03_OPTIONS_TRACE_INTEGRITY_REPAIR_EXECUTION_LOG_v1.md"
CHECKLIST = REPO_ROOT / "docs/planning/2026-04-03_OPTIONS_TRACE_INTEGRITY_REPAIR_DOCUMENT_TOUCH_CHECKLIST_v1.md"
SCOPE_NOTE = REPO_ROOT / "docs/planning/2026-04-03_OPTIONS_TRACE_INTEGRITY_REPAIR_SCOPE_NOTE_v1.md"
RECEIPT = REPO_ROOT / "docs/planning/2026-04-03_GATE181_OPTIONS_TRACE_PACK_BOOTSTRAP.md"


def test_gate181_pack_surfaces_are_coherent() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    scope_note = SCOPE_NOTE.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert "docs/planning/2026-04-03_OPTIONS_TRACE_INTEGRITY_REPAIR_GATES_v1.md" in plans
    assert any(marker in gate_map for marker in [
        "Gate 182 in the options-trace integrity repair pack",
        "options-trace integrity repair pack closed through Gate 186 on `main`",
    ])
    assert any(status in gates for status in [
        "Status: active options-trace integrity repair pack from Gate 182 on `main`",
        "Status: closed options-trace integrity repair pack through Gate 186 on `main`",
    ])
    assert leaves["execution_status"] in {
        "gate_181_options_trace_integrity_repair_pack_active_from_gate_182",
        "options_trace_integrity_repair_pack_closed_through_gate_186_on_main",
    }
    assert leaves["active_gate"] in {"Gate 182", "none"}
    assert set(leaves["completed_leaf_ids"]).isdisjoint(leaves["remaining_leaf_ids"])
    assert execution_log.startswith("# 2026-04-03_OPTIONS_TRACE_INTEGRITY_REPAIR_EXECUTION_LOG_v1")
    assert any(state in checklist for state in [
        "options-trace integrity repair pack active from Gate 182 on `main`.",
        "options-trace integrity repair pack closed through Gate 186 on `main`.",
    ])
    assert "F1: IV unit contract inconsistency" in scope_note
    assert "F5: workbook doctrine as raw-runtime replacement. Keep workbook surfaces as evidence input only." in scope_note


def test_gate181_future_gate_structure_preserves_granularity_without_fixed_cardinality() -> None:
    payload = json.loads(LEAVES.read_text(encoding="utf-8"))
    leaves = payload["leaves"]
    counts = {}
    for item in leaves.values():
        counts.setdefault(item["gate"], 0)
        counts[item["gate"]] += 1

    assert counts["Gate 182"] == 5
    assert counts["Gate 183"] == 4
    assert counts["Gate 184"] == 4
    assert counts["Gate 185"] == 5
    assert counts["Gate 186"] == 4
    assert len({counts["Gate 182"], counts["Gate 183"], counts["Gate 184"], counts["Gate 185"], counts["Gate 186"]}) > 1

    future_leaves = [item for item in leaves.values() if item["gate"] in {"Gate 182", "Gate 183", "Gate 184", "Gate 185", "Gate 186"}]
    for item in future_leaves:
        assert len(item["ordered_actions"]) >= 3
        assert len(item["forbidden_actions"]) >= 3
        assert item["validation_commands"]
        assert item["expected_evidence"]
        assert item["definition_of_done"]


def test_gate181_receipt_and_scope_note_preserve_truth_split_and_non_goals() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")
    scope_note = SCOPE_NOTE.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")

    assert "F1 and F4 are confirmed bugs." in receipt
    assert "F2 is a confirmed architectural defect" in receipt
    assert "F3 is a bounded capability gap" in receipt
    assert "it did not edit runtime behaviour under `src/`" in receipt
    assert "Do not treat the findings report as biblical authority." in scope_note
    assert "Do not introduce a second options engine" in scope_note
    assert "F5 is intentionally excluded from execution scope." in checklist
