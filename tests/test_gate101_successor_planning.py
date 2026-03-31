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


def test_successor_testing_pack_is_retained_as_predecessor_evidence() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")

    assert "2026-03-30_TESTING_MODULE_SUCCESSOR_GATES_v1.md" in plans
    assert "2026-03-30_TESTING_MODULE_SUCCESSOR_LEAVES_v1.json" in plans
    assert "2026-03-30_TESTING_MODULE_SUCCESSOR_EXECUTION_LOG_v1.md" in plans
    assert "2026-03-30_TESTING_MODULE_SUCCESSOR_SCOPE_NOTE_v1.md" in plans

    assert ("Current active gate: **Gate 111 in the repo-process governance pack**." in gate_map) or ("Current active gate: **Gate 112 in the repo-process governance pack**." in gate_map or "Current active gate: **Gate 115 in the historical-evaluation readiness pack**." in gate_map or "Current active gate: **Gate 116 in the historical-evaluation readiness pack**." in gate_map or "Current active gate: **Gate 117 in the historical-evaluation readiness pack**." in gate_map or "Current active gate: **Gate 118 in the historical-evaluation readiness pack**." in gate_map or "Current active gate: **Gate 119 in the historical-evaluation readiness pack**." in gate_map or "Current active gate: **Gate 120 in the historical-evaluation readiness pack**." in gate_map or "Current active gate: **Gate 121 in the historical-evaluation readiness pack**." in gate_map or "Current active gate: **none — historical-evaluation readiness pack closed through Gate 121 on `main`**." in gate_map or "Current active gate: **Gate 122 in the signal-coefficient authority pack**." in gate_map or "Current active gate: **Gate 123 in the signal-coefficient authority pack**." in gate_map or "Current active gate: **Gate 124 in the signal-coefficient authority pack**." in gate_map or "Current active gate: **Gate 125 in the signal-coefficient authority pack**." in gate_map or "Current active gate: **Gate 126 in the signal-coefficient authority pack**." in gate_map or "Current active gate: **Gate 127 in the signal-coefficient authority pack**." in gate_map or "Current active gate: **none — signal-coefficient authority pack closed through Gate 127 on `main`**." in gate_map or "Current active gate: **Gate 128 in the post-flight repo consistency pack**." in gate_map or "Current active gate: **Gate 129 in the post-flight repo consistency pack**." in gate_map or "Current active gate: **Gate 130 in the post-flight repo consistency pack**." in gate_map or "Current active gate: **Gate 131 in the post-flight repo consistency pack**." in gate_map or "Current active gate: **none — post-flight repo consistency pack closed through Gate 131 on `main`**." in gate_map) or ("Current active gate: **none — repo-process governance pack closed through Gate 112 on `main`**." in gate_map) or ("Current active gate: **Gate 115 in the historical-evaluation readiness pack**." in gate_map) or ("Current active gate: **Gate 116 in the historical-evaluation readiness pack**." in gate_map) or ("Current active gate: **Gate 117 in the historical-evaluation readiness pack**." in gate_map) or ("Current active gate: **Gate 118 in the historical-evaluation readiness pack**." in gate_map) or ("Current active gate: **Gate 119 in the historical-evaluation readiness pack**." in gate_map) or ("Current active gate: **Gate 120 in the historical-evaluation readiness pack**." in gate_map) or ("Current active gate: **Gate 121 in the historical-evaluation readiness pack**." in gate_map) or ("Current active gate: **none — historical-evaluation readiness pack closed through Gate 121 on `main`**." in gate_map or "Current active gate: **Gate 122 in the signal-coefficient authority pack**." in gate_map or "Current active gate: **Gate 123 in the signal-coefficient authority pack**." in gate_map or "Current active gate: **Gate 124 in the signal-coefficient authority pack**." in gate_map or "Current active gate: **Gate 125 in the signal-coefficient authority pack**." in gate_map or "Current active gate: **Gate 126 in the signal-coefficient authority pack**." in gate_map or "Current active gate: **Gate 127 in the signal-coefficient authority pack**." in gate_map or "Current active gate: **none — signal-coefficient authority pack closed through Gate 127 on `main`**." in gate_map or "Current active gate: **Gate 128 in the post-flight repo consistency pack**." in gate_map or "Current active gate: **Gate 129 in the post-flight repo consistency pack**." in gate_map or "Current active gate: **Gate 130 in the post-flight repo consistency pack**." in gate_map or "Current active gate: **Gate 131 in the post-flight repo consistency pack**." in gate_map or "Current active gate: **none — post-flight repo consistency pack closed through Gate 131 on `main`**." in gate_map)
    assert "| Gate 101 | complete on `main` |" in gate_map
    assert "| Gate 102 | complete on `main` |" in gate_map
    assert "| Gate 103 | complete on `main` |" in gate_map
    assert "| Gate 104 | complete on `main` |" in gate_map
    assert "| Gate 105 | complete on `main` |" in gate_map
    assert "| Gate 106 | complete on `main` |" in gate_map


def test_successor_pack_docs_freeze_remaining_work_honestly() -> None:
    gates = GATES.read_text(encoding="utf-8")
    scope_note = SCOPE_NOTE.read_text(encoding="utf-8")

    assert "Gate 101: Canonical raw-truth bundle admission" in gates
    assert "Gate 106: Successor-pack honest closeout and packaging" in gates
    assert "Gate 101 admitted one canonical raw bundle from existing repo truth" in gates
    assert "Gate 101 admitted one canonical raw bundle from existing repo truth" in scope_note
    assert "Gate 102 proved one full raw -> prepared -> cognition -> review path from the admitted bundle." in scope_note
    assert "Gate 103 froze bounded parity with the prepared harness and extended runtime-law invariants to the raw path." in scope_note
    assert "Gate 104 added targeted property/stateful testing to the bounded high-risk services." in scope_note
    assert "Gate 105 hardened typed ingress correctness plus repo-native DB/API seams." in scope_note
    assert "Status: closed bounded-scope note retained as evidence for the successor testing pack; Gates 101-106 complete on `main`, no active gate" in scope_note


def test_successor_leaves_freeze_gate106_closeout() -> None:
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert leaves["governing_plan"] == "docs/planning/2026-03-30_TESTING_MODULE_SUCCESSOR_GATES_v1.md"
    assert leaves["execution_status"] == "successor_testing_pack_closed_through_gate_106_on_main"
    assert leaves["active_gate"] == "none — successor testing pack closed through Gate 106 on main"
    assert leaves["completed_gate_ids"] == ["Gate 101", "Gate 102", "Gate 103", "Gate 104", "Gate 105", "Gate 106"]
    assert leaves["completed_leaf_ids"] == ["LEAF-G101-001", "LEAF-G101-002", "LEAF-G102-001", "LEAF-G102-002", "LEAF-G103-001", "LEAF-G103-002", "LEAF-G104-001", "LEAF-G104-002", "LEAF-G105-001", "LEAF-G105-002", "LEAF-G106-001", "LEAF-G106-002"]
    assert leaves["remaining_leaf_ids"] == []
    assert leaves["global_rules"]["gate_101_raw_truth_is_a_hard_gate"] is True
    assert leaves["global_rules"]["prepared_runtime_coverage_is_not_raw_ingress_coverage"] is True


def test_successor_execution_log_is_open_and_receipt_free() -> None:
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")

    assert "Status: closed execution log for the successor testing pack; Gates 101-106 complete on `main`, no active gate" in execution_log
    assert "### LEAF-G101-001" in execution_log
    assert "### LEAF-G102-001" in execution_log
    assert "### LEAF-G103-001" in execution_log
    assert "### LEAF-G104-001" in execution_log
    assert "### LEAF-G105-001" in execution_log
    assert "### LEAF-G106-001" in execution_log
