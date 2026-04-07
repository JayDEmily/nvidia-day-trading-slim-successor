"""Gate 222 archive-only move invariants."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_ROOT = (
    REPO_ROOT
    / "docs/planning/archive_evidence/retained_tests/2026-04-06_successor_retained_test_cleanup"
)
MANIFEST = ARCHIVE_ROOT / "MOVE_MANIFEST_v1.json"
LEAVES = REPO_ROOT / "docs/planning/2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_EXECUTION_LOG_v1.md"


def _files_for(decision_id: str) -> list[Path]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for family in manifest["decision_families"]:
        if family["decision_id"] == decision_id:
            return [REPO_ROOT / path for path in family["files"]]
    raise AssertionError(f"decision id not found: {decision_id}")


def test_gate222_archive_destination_and_manifest_remain_coherent() -> None:
    payload = json.loads(LEAVES.read_text(encoding="utf-8"))
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    completed = set(payload["completed_leaf_ids"])

    assert ARCHIVE_ROOT.is_dir()
    assert MANIFEST.is_file()
    assert payload["execution_status"] in {
        "gate_222_complete_on_work_branch_gate_223_not_yet_activated",
        "cleanup_pack_closed_no_active_pack_routed",
    }
    assert payload["active_gate"] in {
        "none — Gate 222 complete on work/gate-222-archive-evidence-and-duplicate-retirement-20260406; Gate 223 not yet activated",
        "none",
    }
    assert payload["completed_gate_ids"] in (["Gate 222"], ["Gate 222", "Gate 223", "Gate 224", "Gate 225"])
    assert payload["pending_gate_ids"] in (["Gate 223", "Gate 224", "Gate 225"], [])
    assert "Gate 222 receipts" in execution_log
    assert "Gate 222 complete on `work/gate-222-archive-evidence-and-duplicate-retirement-20260406`" in execution_log
    assert ("Gate 223 remains planned and is not yet activated." in execution_log) or ("cleanup pack closed through Gate 225" in execution_log)
    assert manifest["archive_destination"] == (
        "docs/planning/archive_evidence/retained_tests/2026-04-06_successor_retained_test_cleanup/"
    )
    assert manifest["source_repo_destination_forbidden"] is True

    planning_files = _files_for("planning_governance__closed_source_or_historical_pack_receipts")
    review_files = _files_for("review_or_trace__historical_planning_review_receipts")
    closeout_files = _files_for("migration_or_closeout_guard__historical_closeout_receipts")

    if "LEAF-G222-002" in completed:
        for path in planning_files + review_files:
            archived = ARCHIVE_ROOT / path.relative_to(REPO_ROOT)
            assert archived.is_file()
            assert not path.exists()
    else:
        for path in planning_files + review_files:
            assert path.exists()

    if "LEAF-G222-003" in completed:
        for path in closeout_files:
            archived = ARCHIVE_ROOT / path.relative_to(REPO_ROOT)
            assert archived.is_file()
            assert not path.exists()
    else:
        for path in closeout_files:
            assert path.exists()
