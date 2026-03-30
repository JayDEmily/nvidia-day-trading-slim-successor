"""Successor testing-pack planning authority checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
SCOPE_NOTE = REPO_ROOT / "docs/planning/2026-03-30_TESTING_MODULE_SUCCESSOR_SCOPE_NOTE_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-03-30_TESTING_MODULE_SUCCESSOR_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-30_TESTING_MODULE_SUCCESSOR_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-03-30_TESTING_MODULE_SUCCESSOR_EXECUTION_LOG_v1.md"


def test_active_planning_surfaces_point_at_the_successor_testing_pack() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")

    assert "2026-03-30_TESTING_MODULE_SUCCESSOR_GATES_v1.md" in plans
    assert "2026-03-30_TESTING_MODULE_SUCCESSOR_LEAVES_v1.json" in plans
    assert "2026-03-30_TESTING_MODULE_SUCCESSOR_EXECUTION_LOG_v1.md" in plans
    assert "2026-03-30_TESTING_MODULE_SUCCESSOR_SCOPE_NOTE_v1.md" in plans
    assert "Gate 101 — complete on `main` in the successor testing pack" in plans
    assert "Gate 102 — complete on `main` in the successor testing pack" in plans
    assert "Gate 103 — next active gate on `main` in the successor testing pack" in plans
    assert "Gates 104–106 — planned in the successor testing pack; not started on `main`" in plans

    assert "Current active gate: **Gate 103 in the successor testing pack**." in gate_map
    assert "| Gate 101 | complete on `main` |" in gate_map
    assert "| Gate 102 | complete on `main` |" in gate_map
    assert "| Gate 103 | planned; next active gate |" in gate_map
    assert "| Gate 106 | planned |" in gate_map


def test_successor_pack_docs_freeze_remaining_work_honestly() -> None:
    gates = GATES.read_text(encoding="utf-8")
    scope_note = SCOPE_NOTE.read_text(encoding="utf-8")

    assert "Gate 101: Canonical raw-truth bundle admission" in gates
    assert "Gate 106: Successor-pack honest closeout and packaging" in gates
    assert "Gate 101 admitted one canonical raw bundle from existing repo truth" in gates
    assert "Gate 101 admitted one canonical raw bundle from existing repo truth" in scope_note
    assert "Gate 102 proved one full raw -> prepared -> cognition -> review path from the admitted bundle." in scope_note
    assert "do not pretend Gate 104 began" in scope_note


def test_successor_leaves_freeze_gate102_complete_and_gate103_next() -> None:
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert leaves["governing_plan"] == "docs/planning/2026-03-30_TESTING_MODULE_SUCCESSOR_GATES_v1.md"
    assert leaves["execution_status"] == "gate_103_successor_testing_pack_active_on_main"
    assert leaves["active_gate"] == "Gate 103"
    assert leaves["completed_gate_ids"] == ["Gate 101", "Gate 102"]
    assert leaves["completed_leaf_ids"] == ["LEAF-G101-001", "LEAF-G101-002", "LEAF-G102-001", "LEAF-G102-002"]
    assert leaves["remaining_leaf_ids"][:2] == ["LEAF-G103-001", "LEAF-G103-002"]
    assert leaves["global_rules"]["gate_101_raw_truth_is_a_hard_gate"] is True
    assert leaves["global_rules"]["prepared_runtime_coverage_is_not_raw_ingress_coverage"] is True


def test_successor_execution_log_is_open_and_receipt_free() -> None:
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")

    assert "Status: active execution log for the successor testing pack; Gates 101-102 complete on `main`, Gate 103 next" in execution_log
    assert "### LEAF-G101-001" in execution_log
    assert "### LEAF-G102-001" in execution_log
    assert "### Gate 103 receipts" in execution_log
    assert "LEAF-G106-002" in execution_log
