"""Gate 223 successor-boundary and light-retarget invariants."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_EXECUTION_LOG_v1.md"
MANIFEST = (
    REPO_ROOT
    / "docs/planning/archive_evidence/retained_tests/2026-04-06_successor_retained_test_cleanup/MOVE_MANIFEST_v1.json"
)
GATE210_TEST = REPO_ROOT / "tests/test_gate210_operator_surface_alignment_and_cutover.py"
GATE49_TEST = REPO_ROOT / "tests/test_gate49_temporal_compatibility.py"
SESSION_CLOCK_TEST = REPO_ROOT / "tests/test_session_clock.py"
REPLAY_COMPARE_TEST = REPO_ROOT / "tests/test_replay_compare_runtime.py"
GATE127_TEST = REPO_ROOT / "tests/test_gate127_replay_coefficient_visibility.py"
RESEARCH_EVAL_REPLAY_TEST = REPO_ROOT / "tests/test_research_eval_replay.py"
RESEARCH_REPLAY_TEST = REPO_ROOT / "tests/test_research_replay.py"


def test_gate223_control_surfaces_and_manifest_are_truthful() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    payload = json.loads(LEAVES.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    completed = set(payload["completed_leaf_ids"])

    if "LEAF-G223-004" in completed:
        assert payload["execution_status"] in {
            "gate_223_complete_on_work_branch_gate_224_not_yet_activated",
            "cleanup_pack_closed_no_active_pack_routed",
        }
        assert payload["active_gate"] in {
            "none — Gate 223 complete on work/gate-223-successor-boundary-and-light-retarget-20260406; Gate 224 not yet activated",
            "none",
        }
        assert payload["completed_gate_ids"] in (["Gate 222", "Gate 223"], ["Gate 222", "Gate 223", "Gate 224", "Gate 225"])
        assert payload["pending_gate_ids"] in (["Gate 224", "Gate 225"], [])
        assert (
            "Gate 223 is complete on `work/gate-223-successor-boundary-and-light-retarget-20260406`" in plans
            or "no active pack currently routed; the successor retained-test cleanup execution pack is closed through Gate 225" in plans
        )
        assert "Gate 223 complete on `work/gate-223-successor-boundary-and-light-retarget-20260406`" in execution_log
        assert (
            "Gate 224 remains planned and is not yet activated." in execution_log
            or "cleanup pack closed through Gate 225" in execution_log
        )
        assert (
            "Current active gate: **No active gate under the successor retained-test cleanup execution pack. Gate 223 is complete on `work/gate-223-successor-boundary-and-light-retarget-20260406`; Gate 224 is not yet activated.**" in gate_map
            or "Current active gate: **No active pack currently routed. The successor retained-test cleanup execution pack is closed through Gate 225 on `work/gate-225-retained-test-cleanup-closeout-20260406`.**" in gate_map
        )
    else:
        assert payload["execution_status"] in {
            "gate_223_active_on_work_branch",
            "gate_223_active_leaf_g223_001_complete",
            "gate_223_active_leaf_g223_002_complete",
            "gate_223_active_leaf_g223_003_complete",
        }
        assert payload["active_gate"] == "Gate 223"
        assert payload["completed_gate_ids"] == ["Gate 222"]
        assert payload["pending_gate_ids"] == ["Gate 223", "Gate 224", "Gate 225"]
        assert "successor retained-test cleanup execution pack with Gate 223 active on `work/gate-223-successor-boundary-and-light-retarget-20260406`" in plans
        assert "Current active gate: **Gate 223 active on `work/gate-223-successor-boundary-and-light-retarget-20260406` under the successor retained-test cleanup execution pack.**" in gate_map
        assert "Gate 223 is active on `work/gate-223-successor-boundary-and-light-retarget-20260406`." in execution_log

    decision_ids = {family["decision_id"] for family in manifest["decision_families"]}
    assert "replay_regression__research_shadow_replays" not in decision_ids
    deferred = manifest["deferred_non_archive_actions"]
    assert len(deferred) == 1
    assert deferred[0]["decision_id"] == "replay_regression__research_shadow_replays"
    assert deferred[0]["deferred_to_leaf"] == "LEAF-G223-004"
    assert deferred[0]["planned_action"] == "retire_duplicate"


def test_gate223_retarget_targets_track_leaf_progress() -> None:
    payload = json.loads(LEAVES.read_text(encoding="utf-8"))
    completed = set(payload["completed_leaf_ids"])

    gate210_text = GATE210_TEST.read_text(encoding="utf-8")
    gate49_text = GATE49_TEST.read_text(encoding="utf-8")
    session_clock_text = SESSION_CLOCK_TEST.read_text(encoding="utf-8")
    replay_compare_text = REPLAY_COMPARE_TEST.read_text(encoding="utf-8")
    gate127_text = GATE127_TEST.read_text(encoding="utf-8")

    if "LEAF-G223-001" in completed:
        assert "Successor-local cleanup-pack boundary" in gate210_text
        assert "MOVE_MANIFEST_v1.json" in gate210_text
        assert "2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_LEAVES_v1.json" in gate210_text

    if "LEAF-G223-002" in completed:
        assert "docs/03_DOMAIN_MODEL.md" in gate49_text
        assert "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md" in gate49_text
        assert "Session Clock compatibility wrapper" in session_clock_text
        assert "temporal_state" in session_clock_text

    if "LEAF-G223-003" in completed:
        assert "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md" in replay_compare_text
        assert "Stage-Local Handoff" in replay_compare_text
        assert "successor retained-test cleanup execution pack" in gate127_text
        assert "Gate 223" in gate127_text

    if "LEAF-G223-004" in completed:
        assert not RESEARCH_EVAL_REPLAY_TEST.exists()
        assert not RESEARCH_REPLAY_TEST.exists()
    else:
        assert RESEARCH_EVAL_REPLAY_TEST.exists()
        assert RESEARCH_REPLAY_TEST.exists()
