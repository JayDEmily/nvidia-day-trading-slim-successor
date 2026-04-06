"""Gate 220 test-audit decision-law and register checks."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RULES = REPO_ROOT / "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_TEST_INVENTORY_CLASSIFICATION_AND_DECISION_RULES_v1.md"


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
