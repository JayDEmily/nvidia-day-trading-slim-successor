"""Gate 219 retained-test inventory baseline checks."""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RULES = REPO_ROOT / "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_TEST_INVENTORY_CLASSIFICATION_AND_DECISION_RULES_v1.md"


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
