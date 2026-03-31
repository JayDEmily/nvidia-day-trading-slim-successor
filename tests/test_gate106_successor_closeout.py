"""Gate 106 successor-pack closeout checks."""

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
CLOSEOUT_DOC = REPO_ROOT / "docs/planning/2026-03-30_GATE106_SUCCESSOR_CLOSEOUT.md"


def test_gate106_planning_quartet_closes_the_successor_pack_honestly() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    scope_note = SCOPE_NOTE.read_text(encoding="utf-8")

    assert "2026-03-30_TESTING_MODULE_SUCCESSOR_GATES_v1.md" in plans
    assert "2026-03-30_TESTING_MODULE_SUCCESSOR_LEAVES_v1.json" in plans
    assert "Current active gate: **Gate 111 in the repo-process governance pack**." in gate_map or "Current active gate: **Gate 112 in the repo-process governance pack**." in gate_map or "Current active gate: **Gate 115 in the historical-evaluation readiness pack**." in gate_map or "Current active gate: **Gate 116 in the historical-evaluation readiness pack**." in gate_map or "Current active gate: **Gate 117 in the historical-evaluation readiness pack**." in gate_map or "Current active gate: **Gate 118 in the historical-evaluation readiness pack**." in gate_map or "Current active gate: **Gate 119 in the historical-evaluation readiness pack**." in gate_map or "Current active gate: **Gate 120 in the historical-evaluation readiness pack**." in gate_map or "Current active gate: **Gate 121 in the historical-evaluation readiness pack**." in gate_map or "Current active gate: **none — historical-evaluation readiness pack closed through Gate 121 on `main`**." in gate_map or "Current active gate: **Gate 122 in the signal-coefficient authority pack**." in gate_map or "Current active gate: **Gate 123 in the signal-coefficient authority pack**." in gate_map or "Current active gate: **Gate 124 in the signal-coefficient authority pack**." in gate_map or "Current active gate: **Gate 125 in the signal-coefficient authority pack**." in gate_map or "Current active gate: **Gate 126 in the signal-coefficient authority pack**." in gate_map or "Current active gate: **Gate 127 in the signal-coefficient authority pack**." in gate_map or "Current active gate: **none — signal-coefficient authority pack closed through Gate 127 on `main`**." in gate_map or "Current active gate: **Gate 128 in the post-flight repo consistency pack**." in gate_map or "Current active gate: **Gate 129 in the post-flight repo consistency pack**." in gate_map or "Current active gate: **Gate 130 in the post-flight repo consistency pack**." in gate_map or "Current active gate: **Gate 131 in the post-flight repo consistency pack**." in gate_map or "Current active gate: **none — post-flight repo consistency pack closed through Gate 131 on `main`**." in gate_map or "Current active gate: **none — repo-process governance pack closed through Gate 112 on `main`**." in gate_map
    assert "| Gate 106 | complete on `main` |" in gate_map
    assert "Status: closed bounded-scope note retained as evidence for the successor testing pack; Gates 101-106 complete on `main`, no active gate" in scope_note


def test_gate106_leaves_and_execution_log_record_no_remaining_work() -> None:
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")

    assert leaves["execution_status"] == "successor_testing_pack_closed_through_gate_106_on_main"
    assert leaves["active_gate"] == "none — successor testing pack closed through Gate 106 on main"
    assert leaves["completed_gate_ids"] == ["Gate 101", "Gate 102", "Gate 103", "Gate 104", "Gate 105", "Gate 106"]
    assert leaves["remaining_leaf_ids"] == []
    assert all(leaf["status"] == "complete" for leaf in leaves["leaves"])
    assert "Status: closed execution log for the successor testing pack; Gates 101-106 complete on `main`, no active gate" in execution_log
    assert "### LEAF-G106-001" in execution_log
    assert "### LEAF-G106-002" in execution_log


def test_gate106_closeout_doc_freezes_package_intent() -> None:
    closeout = CLOSEOUT_DOC.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")

    assert "Status: Gate 106 complete on `main`; successor testing pack closed honestly" in closeout
    assert "The successor testing pack is closed through Gate 106 on `main`." in closeout
    assert "nvda_repo_successor_testing_pack_closed_gate106_main_2026-03-30.zip" in closeout
    assert "Status: closed successor testing pack on `main`; Gates 101-106 complete, no active gate" in gates
