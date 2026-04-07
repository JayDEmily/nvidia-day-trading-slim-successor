"""Gate 219 retained-test inventory and ownership-mapping checks."""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RULES = REPO_ROOT / "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_TEST_INVENTORY_CLASSIFICATION_AND_DECISION_RULES_v1.md"
ARCHIVE_ROOT = REPO_ROOT / "docs/planning/archive_evidence/retained_tests/2026-04-06_successor_retained_test_cleanup/tests"
RETIRED_DUPLICATE_TESTS = {
    "tests/test_research_eval_replay.py",
    "tests/test_research_replay.py",
}
POST_GATE219_TESTS = {
    "tests/test_successor_retained_test_cleanup_pack_routing.py",
    "tests/test_gate220_test_audit_decision_register.py",
    "tests/test_gate221_successor_test_audit_handoff.py",
    "tests/test_gate222_archive_and_duplicate_retirement.py",
    "tests/test_gate223_successor_boundary_and_light_retarget.py",
    "tests/test_gate224_runtime_review_and_contract_retarget.py",
    "tests/test_gate225_retained_test_cleanup_closeout.py",
}

def extract_json_block(document: str, heading: str) -> list[dict[str, object]]:
    pattern = rf"## {re.escape(heading)}\n\n```json\n(.*?)\n```"
    match = re.search(pattern, document, flags=re.DOTALL)
    assert match, heading
    payload = json.loads(match.group(1))
    assert isinstance(payload, list), heading
    return payload


def test_gate219_leaf1_inventory_baseline_covers_retained_tests_once() -> None:
    document = RULES.read_text(encoding="utf-8")
    rows = extract_json_block(document, "Gate 219 canonical retained-test inventory baseline")
    actual_tests = sorted(
        path.relative_to(REPO_ROOT).as_posix() for path in (REPO_ROOT / "tests").glob("test_*.py")
    )

    assert "Gate 219 freezes the retained-test baseline as one row per retained **test family**" in document
    assert "member_tests" in document
    assert len(rows) == 11

    seen_ids: set[str] = set()
    covered_tests: list[str] = []
    total = 0
    for row in rows:
        assert row["test_id"] == row["test_family"]
        assert row["path"] == "tests/"
        assert isinstance(row["historical_gate_lineage"], str) and row["historical_gate_lineage"]
        assert isinstance(row["retained_test_count"], int) and row["retained_test_count"] > 0
        member_tests = row["member_tests"]
        assert isinstance(member_tests, list) and member_tests
        assert len(member_tests) == row["retained_test_count"]
        assert row["test_id"] not in seen_ids
        seen_ids.add(row["test_id"])
        covered_tests.extend(member_tests)
        total += row["retained_test_count"]

    assert len(set(covered_tests)) == len(covered_tests)
    assert total == len(covered_tests)
    for rel in covered_tests:
        original = REPO_ROOT / rel
        archived = ARCHIVE_ROOT / Path(rel).name
        assert original.exists() or archived.exists() or rel in RETIRED_DUPLICATE_TESTS, rel
    assert set(actual_tests) - POST_GATE219_TESTS <= set(covered_tests)


def test_gate219_mapping_rows_remain_frozen_as_the_pre_decision_baseline() -> None:
    document = RULES.read_text(encoding="utf-8")
    inventory_rows = extract_json_block(document, "Gate 219 canonical retained-test inventory baseline")
    mapping_rows = extract_json_block(document, "Gate 219 family doctrine and ownership mapping")

    assert "pending_gate_220_decision" in document
    assert "Gate 219 may use the pre-decision placeholder `pending_gate_220_decision`" in document
    assert "Gate 220 may later split a family row into narrower decision rows" in document

    inventory_by_id = {row["test_id"]: row for row in inventory_rows}
    mapping_by_id = {row["test_id"]: row for row in mapping_rows}

    assert set(inventory_by_id) == set(mapping_by_id)
    assert len(mapping_by_id) == 11

    required_mapping_fields = {
        "bug_surface_class",
        "testing_phase_alignment",
        "authoritative_inputs",
        "runtime_owner_or_planning_owner",
        "downstream_consumer_or_control_surface",
        "current_truth_dependency",
        "status_candidate",
        "decision_outcome",
        "evidence_anchor",
        "disagreement_state",
        "next_action_pack",
        "notes",
    }

    for test_id, row in mapping_by_id.items():
        assert required_mapping_fields <= row.keys(), test_id
        assert row["decision_outcome"] == "pending_gate_220_decision"
        assert row["next_action_pack"] == "Gate 220"
        assert row["disagreement_state"]
        assert isinstance(row["authoritative_inputs"], list) and row["authoritative_inputs"]
        assert isinstance(row["runtime_owner_or_planning_owner"], list) and row["runtime_owner_or_planning_owner"]
        assert isinstance(row["downstream_consumer_or_control_surface"], list) and row["downstream_consumer_or_control_surface"]
        assert isinstance(row["evidence_anchor"], list) and row["evidence_anchor"]
        assert row["current_truth_dependency"]
        assert row["notes"]
        assert inventory_by_id[test_id]["retained_test_count"] == len(inventory_by_id[test_id]["member_tests"])

    assert "successor_required" in mapping_by_id["control_surface_integrity"]["status_candidate"]
    assert "duplicate_candidate" in mapping_by_id["runtime_contract"]["status_candidate"]
    assert "stale_planning_candidate" in mapping_by_id["planning_governance"]["status_candidate"]
    assert "orphan_candidate" in mapping_by_id["migration_or_closeout_guard"]["status_candidate"]
