"""Gate 219 retained-test inventory and ownership-mapping checks."""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RULES = REPO_ROOT / "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_TEST_INVENTORY_CLASSIFICATION_AND_DECISION_RULES_v1.md"
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_EXECUTION_LOG_v1.md"

ACTIVE_BRANCH = "work/gate-219-retained-test-inventory-and-ownership-mapping-20260406"
PROOF_COMMAND = (
    "/home/jds/dev/nvidia-day-trading/target_repo_gate201_evidence_inventory_and_provenance_planning_main_fullgit_2026-04-05/"
    ".venv/bin/python -m pytest -q tests/test_gate219_test_inventory_classification.py "
    "tests/test_planning_state_integrity.py"
)


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

    assert sorted(covered_tests) == actual_tests
    assert len(set(covered_tests)) == len(actual_tests)
    assert total == len(actual_tests)


def test_gate219_closeout_maps_families_and_routes_gate220() -> None:
    document = RULES.read_text(encoding="utf-8")
    inventory_rows = extract_json_block(document, "Gate 219 canonical retained-test inventory baseline")
    mapping_rows = extract_json_block(document, "Gate 219 family doctrine and ownership mapping")
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    payload = json.loads(LEAVES.read_text(encoding="utf-8"))
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")

    assert "pending_gate_220_decision" in document
    assert "Gate 219 may use the pre-decision placeholder `pending_gate_220_decision`" in document

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

    assert "- next active gate: `Gate 220`" in plans
    assert (
        "- active pack: slim active-repo cutover and substantive test-audit bootstrap pack "
        f"with Gate 219 complete on `{ACTIVE_BRANCH}`; Gate 220 not yet activated"
    ) in plans

    assert "Version: v1.32" in gate_map
    assert (
        "Current active gate: **none — Gate 219 in the slim active-repo cutover and substantive "
        f"test-audit bootstrap pack is complete on `{ACTIVE_BRANCH}`, and Gate 220 is planned but not yet activated.**"
    ) in gate_map
    assert f"Gate 219 | complete on `{ACTIVE_BRANCH}`" in gate_map
    assert "Gate 220 | planned" in gate_map
    assert "Gate 221 | planned" in gate_map

    assert (
        "Status: slim-successor planning pack with Gate 219 complete on "
        f"`{ACTIVE_BRANCH}`; Gates 220-221 planned, Gate 220 not yet activated."
    ) in gates

    assert payload["execution_status"] == "gate_219_complete_on_work_branch_gate_220_not_yet_activated"
    assert (
        payload["active_gate"]
        == "none — Gate 219 complete on work/gate-219-retained-test-inventory-and-ownership-mapping-20260406; Gate 220 not yet activated"
    )
    assert payload["completed_gate_ids"] == ["Gate 217", "Gate 218", "Gate 219"]
    assert {"LEAF-G219-001", "LEAF-G219-002"} <= set(payload["completed_leaf_ids"])
    assert payload["pending_gate_ids"] == ["Gate 220", "Gate 221"]
    assert set(payload["remaining_leaf_ids"]) == {
        "LEAF-G220-001",
        "LEAF-G220-002",
        "LEAF-G221-001",
        "LEAF-G221-002",
    }

    assert (
        "Status: successor execution log for slim active-repo cutover and substantive test-audit "
        f"bootstrap; Gate 219 complete on `{ACTIVE_BRANCH}`, Gates 220-221 planned, Gate 220 not yet activated."
    ) in execution_log
    assert "### LEAF-G219-001" in execution_log
    assert "### LEAF-G219-002" in execution_log
    assert PROOF_COMMAND in execution_log
    assert "repo-local successor environment still unavailable because /home/jds/dev/nvidia-day-trading-slim-successor/.venv/bin/python does not exist" in execution_log
    assert "Gate 219 is complete on `work/gate-219-retained-test-inventory-and-ownership-mapping-20260406`." in execution_log
    assert "Gate 220 remains planned and is not yet activated." in execution_log
