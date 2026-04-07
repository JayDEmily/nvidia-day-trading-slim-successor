"""Successor-local cleanup-pack boundary checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_EXECUTION_LOG_v1.md"
MANIFEST = (
    REPO_ROOT
    / "docs/planning/archive_evidence/retained_tests/2026-04-06_successor_retained_test_cleanup/MOVE_MANIFEST_v1.json"
)


def test_successor_local_cleanup_pack_boundary_and_archive_truth() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    payload = json.loads(LEAVES.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert "2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_GATES_v1.md" in plans
    assert "2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_LEAVES_v1.json" in plans
    assert "2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_EXECUTION_LOG_v1.md" in plans

    assert payload["completed_gate_ids"] in (["Gate 222"], ["Gate 222", "Gate 223", "Gate 224", "Gate 225"])
    assert payload["pending_gate_ids"] in (["Gate 223", "Gate 224", "Gate 225"], [])

    if payload["active_gate"] == "Gate 223":
        assert "Gate 223 active on `work/gate-223-successor-boundary-and-light-retarget-20260406`" in plans
        assert "Current active gate: **Gate 223 active on `work/gate-223-successor-boundary-and-light-retarget-20260406` under the successor retained-test cleanup execution pack.**" in gate_map
        assert "Gate 223 is active on `work/gate-223-successor-boundary-and-light-retarget-20260406`." in execution_log
    elif payload["active_gate"] == (
        "none — Gate 223 complete on "
        "work/gate-223-successor-boundary-and-light-retarget-20260406; "
        "Gate 224 not yet activated"
    ):
        assert "Gate 223 complete on `work/gate-223-successor-boundary-and-light-retarget-20260406`" in plans
        assert "Gate 224 is not yet activated" in gate_map
        assert "Gate 224 remains planned and is not yet activated." in execution_log
    else:
        assert payload["active_gate"] == "none"
        assert "no active pack currently routed" in plans
        assert "Current active gate: **No active pack currently routed. The successor retained-test cleanup execution pack is closed through Gate 225 on `work/gate-225-retained-test-cleanup-closeout-20260406`.**" in gate_map
        assert "cleanup pack closed through Gate 225" in execution_log

    assert "source_repo_mutation_forbidden" in json.dumps(payload["global_rules"])
    assert "### Gate 223: Successor-boundary rewrite and light retarget execution" in gates
    assert "duplicate research-shadow replay tests are retired only after the canonical replay compare guards remain green on the same Gate 223 branch" in gates

    archive_decision_ids = {family["decision_id"] for family in manifest["decision_families"]}
    assert "replay_regression__research_shadow_replays" not in archive_decision_ids
    deferred = manifest["deferred_non_archive_actions"]
    assert deferred == [
        {
            "decision_id": "replay_regression__research_shadow_replays",
            "deferred_to_leaf": "LEAF-G223-004",
            "planned_action": "retire_duplicate",
            "disagreement_state": "resolved_with_memory",
            "notes": "Gate 222 remained archive-only after pack amendment; duplicate replay-shadow retirement may execute only in Gate 223 after replay-authority retarget proof lands on the same branch.",
            "files": [
                "tests/test_research_eval_replay.py",
                "tests/test_research_replay.py",
            ],
        }
    ]
