"""Cleanup-pack install routing invariants for Gate 222 open state."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_GATES_v1.md"
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
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    payload = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert ACTIVE_GATES_DOC in plans
    assert ACTIVE_LEAVES_DOC in plans
    assert ACTIVE_EXECUTION_LOG_DOC in plans
    assert ("successor retained-test cleanup execution pack with Gate 222 active on `main`" in plans) or ("no active pack currently routed" in plans)

    assert "Version:" in gate_map
    assert "Current active gate:" in gate_map
    assert ("Gate 222 active on `main` under the successor retained-test cleanup execution pack." in gate_map) or ("Current active gate: **No active pack currently routed. The successor retained-test cleanup execution pack is closed through Gate 225 on `work/gate-225-retained-test-cleanup-closeout-20260406`.**" in gate_map) or ("Current active gate: **No active pack currently routed. The opening-position domain isolation and interface hardening pack is closed through Gate 235 on `work/gate-235-cross-flow-harness-and-pack-closeout-20260408`.**" in gate_map)
    for gate_id in ("Gate 222", "Gate 223", "Gate 224", "Gate 225"):
        assert f"| {gate_id} |" in gate_map

    assert payload["governing_plan"] == ACTIVE_GATES_DOC
    assert payload["execution_status"] in {"gate_222_active_after_pack_install", "cleanup_pack_closed_no_active_pack_routed"}
    assert payload["active_gate"] in {"Gate 222", "none"}
    assert payload["completed_gate_ids"] in ([], ["Gate 222", "Gate 223", "Gate 224", "Gate 225"])
    assert len(payload["remaining_leaf_ids"]) in {16, 0}
    assert payload["pending_gate_ids"] in (["Gate 222", "Gate 223", "Gate 224", "Gate 225"], [])

    gate_222_leaf = next(leaf for leaf in payload["leaves"] if leaf["id"] == "LEAF-G222-004")
    gate_223_leaf = next(leaf for leaf in payload["leaves"] if leaf["id"] == "LEAF-G223-004")
    assert gate_222_leaf["title"] == "Close Gate 222 as archive-only move gate"
    assert gate_222_leaf["proof_slice"] == [
        "pytest -q tests/test_gate222_archive_and_duplicate_retirement.py tests/test_planning_state_integrity.py"
    ]
    assert gate_223_leaf["title"] == "Retire duplicate replay-shadow tests and close Gate 223"
    assert any(
        "tests/test_replay_compare_runtime.py" in entry
        and "tests/test_gate127_replay_coefficient_visibility.py" in entry
        for entry in gate_223_leaf["proof_slice"]
    )

    assert ("installed and routed on successor `main` with Gate 222 active" in gates) or ("closed successor execution pack through Gate 225" in gates)
    assert "Gate 222: Archive-only move execution" in gates
    assert "`replay_regression__research_shadow_replays`" not in gates.split("### Gate 222: Archive-only move execution", 1)[1].split("### Gate 223:", 1)[0]
    gate_223_section = gates.split("### Gate 223: Successor-boundary rewrite and light retarget execution", 1)[1]
    assert "`replay_regression__research_shadow_replays`" in gate_223_section
    assert "duplicate research-shadow replay tests are retired only after the canonical replay compare guards remain green on the same Gate 223 branch" in gate_223_section

    assert ("Gate 222 active after pack install" in execution_log) or ("cleanup pack closed through Gate 225" in execution_log)
    assert "Gate 222 is the archive-evidence move gate only" in execution_log
    assert "duplicate replay-shadow retirement moves to Gate 223" in execution_log
    assert SOURCE_INTERPRETER in execution_log
