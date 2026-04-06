"""Cleanup-pack install routing invariants for Gate 222 open state."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_EXECUTION_LOG_v1.md"

ACTIVE_GATES_DOC = "docs/planning/2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_GATES_v1.md"
ACTIVE_LEAVES_DOC = "docs/planning/2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_LEAVES_v1.json"
ACTIVE_EXECUTION_LOG_DOC = "docs/planning/2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_EXECUTION_LOG_v1.md"
SOURCE_INTERPRETER = (
    "/home/jds/dev/nvidia-day-trading/"
    "target_repo_gate201_evidence_inventory_and_provenance_planning_main_fullgit_2026-04-05/"
    ".venv/bin/python"
)


def test_cleanup_pack_is_active_and_gate_222_is_open() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    payload = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert ACTIVE_GATES_DOC in plans
    assert ACTIVE_LEAVES_DOC in plans
    assert ACTIVE_EXECUTION_LOG_DOC in plans
    assert "no active pack currently routed" not in plans
    assert "successor retained-test cleanup execution pack with Gate 222 active on `main`" in plans

    assert "Version: v1.35" in gate_map
    assert "Current active gate:" in gate_map
    assert "Gate 222 active on `main` under the successor retained-test cleanup execution pack." in gate_map
    for gate_id in ("Gate 222", "Gate 223", "Gate 224", "Gate 225"):
        assert f"| {gate_id} |" in gate_map

    assert payload["governing_plan"] == ACTIVE_GATES_DOC
    assert payload["execution_status"] == "gate_222_active_after_pack_install"
    assert payload["active_gate"] == "Gate 222"
    assert payload["completed_gate_ids"] == []
    assert payload["completed_leaf_ids"] == []
    assert len(payload["remaining_leaf_ids"]) == 16
    assert payload["pending_gate_ids"] == ["Gate 222", "Gate 223", "Gate 224", "Gate 225"]

    assert "Gate 222 active after pack install" in execution_log
    assert SOURCE_INTERPRETER in execution_log
    assert "No receipts yet." in execution_log
