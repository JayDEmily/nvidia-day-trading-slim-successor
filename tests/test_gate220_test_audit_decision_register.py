"""Gate 220 test-audit decision-law and register checks."""

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

ACTIVE_BRANCH = "work/gate-220-test-decision-law-and-first-pass-register-20260406"
PROOF_COMMAND = (
    "/home/jds/dev/nvidia-day-trading/target_repo_gate201_evidence_inventory_and_provenance_planning_main_fullgit_2026-04-05/"
    ".venv/bin/python -m pytest -q tests/test_gate220_test_audit_decision_register.py "
    "tests/test_planning_state_integrity.py"
)


def extract_json_block(document: str, heading: str) -> list[dict[str, object]]:
    pattern = rf"## {re.escape(heading)}\n\n```json\n(.*?)\n```"
    match = re.search(pattern, document, flags=re.DOTALL)
    assert match, heading
    payload = json.loads(match.group(1))
    assert isinstance(payload, list), heading
    return payload


def test_gate220_leaf1_decision_law_is_frozen() -> None:
    document = RULES.read_text(encoding="utf-8")

    assert "## Gate 220 governed decision law" in document
    assert "### Allowed outcomes are bounded" in document
    assert "### Allowed disagreement states are bounded" in document
    assert "### Required decision-register memory fields" in document
    assert "### Rejected and deferred readings must remain visible" in document
    assert "### Rejection and deferred-decision preservation" in document
    assert "### Classification is not execution" in document

    for outcome in [
        "`keep_as_is`",
        "`keep_but_retarget_authority`",
        "`rewrite_for_successor_truth`",
        "`move_to_archive_evidence_repo`",
        "`retire_duplicate`",
        "`retire_unproven_or_orphaned`",
        "`defer_requires_new_anchor_or_runtime_change`",
    ]:
        assert outcome in document

    for disagreement_state in [
        "`no_disagreement_recorded`",
        "`resolved_with_memory`",
        "`deferred_pending_new_anchor_or_runtime_change`",
    ]:
        assert disagreement_state in document

    for field_name in [
        "`decision_id`",
        "`source_test_family`",
        "`member_test_count`",
        "`member_tests`",
        "`treatment_tags`",
        "`decision_outcome`",
        "`authoritative_inputs`",
        "`runtime_owner_or_planning_owner`",
        "`downstream_consumer_or_control_surface`",
        "`evidence_anchor`",
        "`disagreement_state`",
        "`rejected_interpretation_ids`",
        "`rejection_or_deferral_reason`",
        "`missing_requirement`",
        "`would_become_valid_if`",
        "`next_action_pack`",
        "`archive_destination`",
        "`classification_not_execution_note`",
        "`notes`",
    ]:
        assert field_name in document

    assert "Gate 220 freezes classification and next action only." in document
    assert "They do not silently delete a test, move a file, or rewrite a runtime or planning surface during this gate." in document


def test_gate220_first_pass_register_covers_retained_tests_and_closes_gate220() -> None:
    document = RULES.read_text(encoding="utf-8")
    inventory_rows = extract_json_block(document, "Gate 219 canonical retained-test inventory baseline")
    decision_rows = extract_json_block(document, "Gate 220 first-pass successor test decision register")
    retained_baseline_tests = sorted(
        member_test for row in inventory_rows for member_test in row["member_tests"]
    )
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    payload = json.loads(LEAVES.read_text(encoding="utf-8"))
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")

    inventory_by_id = {row["test_id"]: row for row in inventory_rows}
    assert len(decision_rows) == 15

    covered_tests: list[str] = []
    decision_ids: set[str] = set()
    for row in decision_rows:
        assert row["decision_id"] not in decision_ids
        decision_ids.add(row["decision_id"])
        assert row["source_test_family"] in inventory_by_id
        assert isinstance(row["member_tests"], list) and row["member_tests"]
        assert row["member_test_count"] == len(row["member_tests"])
        covered_tests.extend(row["member_tests"])
        assert row["decision_outcome"] in {
            "keep_as_is",
            "keep_but_retarget_authority",
            "rewrite_for_successor_truth",
            "move_to_archive_evidence_repo",
            "retire_duplicate",
            "retire_unproven_or_orphaned",
            "defer_requires_new_anchor_or_runtime_change",
        }
        assert row["disagreement_state"] in {
            "no_disagreement_recorded",
            "resolved_with_memory",
            "deferred_pending_new_anchor_or_runtime_change",
        }
        assert row["next_action_pack"] == "Gate 221"
        assert isinstance(row["evidence_anchor"], list) and row["evidence_anchor"]
        assert isinstance(row["treatment_tags"], list) and row["treatment_tags"]
        assert row["classification_not_execution_note"] == (
            "Gate 220 freezes classification and next action only; no test move, deletion, rewrite, "
            "or runtime mutation is executed in this pack."
        )

    assert sorted(covered_tests) == retained_baseline_tests
    assert len(set(covered_tests)) == len(retained_baseline_tests)
    assert any(row["decision_outcome"] == "move_to_archive_evidence_repo" for row in decision_rows)
    assert any(row["decision_outcome"] == "retire_duplicate" for row in decision_rows)
    assert any(row["decision_outcome"] == "rewrite_for_successor_truth" for row in decision_rows)
    assert any("archive_only" in row["treatment_tags"] for row in decision_rows)
    assert any("stale_planning" in row["treatment_tags"] for row in decision_rows)
    assert any("duplicate" in row["treatment_tags"] for row in decision_rows)
    assert any("successor_required" in row["treatment_tags"] for row in decision_rows)

    rewrite_row = next(
        row for row in decision_rows if row["decision_id"] == "migration_or_closeout_guard__successor_cutover_boundary_rule"
    )
    assert rewrite_row["missing_requirement"] == "successor_local_cutover_assertions"
    assert rewrite_row["rejected_interpretation_ids"] == [
        "keep_source_repo_cutover_assertions_verbatim_in_successor_repo"
    ]

    duplicate_row = next(
        row for row in decision_rows if row["decision_id"] == "replay_regression__research_shadow_replays"
    )
    assert duplicate_row["decision_outcome"] == "retire_duplicate"
    assert duplicate_row["rejected_interpretation_ids"] == [
        "keep_research_shadow_replays_as_parallel_runtime_guards"
    ]

    assert "- next active gate: `Gate 221`" in plans
    assert (
        "- active pack: slim active-repo cutover and substantive test-audit bootstrap pack "
        f"with Gate 220 complete on `{ACTIVE_BRANCH}`; Gate 221 not yet activated"
    ) in plans

    assert "Version: v1.33" in gate_map
    assert (
        "Current active gate: **none — Gate 220 in the slim active-repo cutover and substantive "
        f"test-audit bootstrap pack is complete on `{ACTIVE_BRANCH}`, and Gate 221 is planned but not yet activated.**"
    ) in gate_map
    assert f"Gate 220 | complete on `{ACTIVE_BRANCH}`" in gate_map
    assert "Gate 221 | planned" in gate_map

    assert (
        "Status: slim-successor planning pack with Gate 220 complete on "
        f"`{ACTIVE_BRANCH}`; Gate 221 planned, Gate 221 not yet activated."
    ) in gates

    assert payload["execution_status"] == "gate_220_complete_on_work_branch_gate_221_not_yet_activated"
    assert (
        payload["active_gate"]
        == "none — Gate 220 complete on work/gate-220-test-decision-law-and-first-pass-register-20260406; Gate 221 not yet activated"
    )
    assert payload["completed_gate_ids"] == ["Gate 217", "Gate 218", "Gate 219", "Gate 220"]
    assert {"LEAF-G220-001", "LEAF-G220-002"} <= set(payload["completed_leaf_ids"])
    assert payload["pending_gate_ids"] == ["Gate 221"]
    assert set(payload["remaining_leaf_ids"]) == {"LEAF-G221-001", "LEAF-G221-002"}

    assert (
        "Status: successor execution log for slim active-repo cutover and substantive test-audit "
        f"bootstrap; Gate 220 complete on `{ACTIVE_BRANCH}`, Gate 221 planned, Gate 221 not yet activated."
    ) in execution_log
    assert "### LEAF-G220-001" in execution_log
    assert "### LEAF-G220-002" in execution_log
    assert PROOF_COMMAND in execution_log
    assert (
        "repo-local successor environment still unavailable because "
        "/home/jds/dev/nvidia-day-trading-slim-successor/.venv/bin/python does not exist; "
        "Gate 220 proof reused the already-provisioned source-repo interpreter intentionally"
    ) in execution_log
    assert f"Gate 220 is complete on `{ACTIVE_BRANCH}`." in execution_log
    assert "Gate 221 remains planned and is not yet activated." in execution_log
