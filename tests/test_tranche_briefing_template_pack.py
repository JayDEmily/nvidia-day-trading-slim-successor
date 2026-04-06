"""Reference-pack checks for the tranche briefing template folder."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PACK_DIR = REPO_ROOT / "docs/planning/tranche_briefing_template_pack"
README = PACK_DIR / "README.md"
HOWTO = PACK_DIR / "HOW_TO_USE_THESE_DOCUMENTS.md"
DOCTRINE = PACK_DIR / "2026-03-29_GENERIC_TRANCHE_BRIEFING_DOCTRINE_v2.md"
GATE_TEMPLATE = PACK_DIR / "2026-03-29_GENERIC_GATE_TEMPLATE_v2.md"
LEAVES_TEMPLATE = PACK_DIR / "2026-03-29_GENERIC_LEAVES_TEMPLATE_v2.json"
WORKED_EXAMPLE = PACK_DIR / "2026-03-29_WORKED_EXAMPLE_FINANCIAL_CALENDAR_SKELETON_v2.md"
EXECUTION_LOG_TEMPLATE = PACK_DIR / "2026-03-30_GENERIC_EXECUTION_LOG_TEMPLATE_v1.md"
DOCUMENT_TOUCH_TEMPLATE = PACK_DIR / "2026-03-30_GENERIC_DOCUMENT_TOUCH_CHECKLIST_TEMPLATE_v1.md"


def test_template_pack_contains_expected_files() -> None:
    assert PACK_DIR.is_dir()
    for path in [README, HOWTO, DOCTRINE, GATE_TEMPLATE, LEAVES_TEMPLATE, WORKED_EXAMPLE, EXECUTION_LOG_TEMPLATE, DOCUMENT_TOUCH_TEMPLATE]:
        assert path.is_file(), path


def test_readme_and_howto_define_planning_thread_to_coding_thread_flow() -> None:
    readme = README.read_text(encoding="utf-8")
    howto = HOWTO.read_text(encoding="utf-8")

    assert "planning thread" in readme
    assert "coding thread" in readme
    assert "Do **not** fill blanks with guesses." in readme
    assert "vocabulary authority" in readme
    assert "packet/contract authority" in readme
    assert "document-touch checklist" in readme
    assert "latest closed pack as evidence input only" in readme
    assert "variable gate and leaf counts" in readme
    assert "GitHub branch, commit, and merge history is the default routine execution ledger" in readme
    assert "fresh full-history zip from the exact green repo state" not in readme

    assert "planning thread" in howto
    assert "coding thread" in howto
    assert "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md" in howto
    assert "python -m pip install -e .[dev]" in howto
    assert "Do not paper over unknowns with vague wording." in howto
    assert "document-touch checklist" in howto
    assert "GitHub branch, commit, and merge history carries the routine execution ledger" in howto
    assert "Create a fresh full-history zip only if the operator explicitly requested" in howto
    assert "vocabulary authority named in the active gates master" in howto
    assert "packet/data contract authority named in the active gates master" in howto
    assert "contradiction report" in howto
    assert "git init" not in howto


def test_doctrine_gate_and_leaves_templates_freeze_workflow_vocabulary_contract_and_state_rules() -> None:
    doctrine = DOCTRINE.read_text(encoding="utf-8")
    gate_template = GATE_TEMPLATE.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES_TEMPLATE.read_text(encoding="utf-8"))
    execution_log_template = EXECUTION_LOG_TEMPLATE.read_text(encoding="utf-8")
    checklist_template = DOCUMENT_TOUCH_TEMPLATE.read_text(encoding="utf-8")
    agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    repo_law = (REPO_ROOT / "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md").read_text(
        encoding="utf-8"
    )
    active_leaves = json.loads(
        (
            REPO_ROOT
            / "docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_LEAVES_v1.json"
        ).read_text(encoding="utf-8")
    )

    assert "Mandatory pre-write scan for every new tranche" in doctrine
    assert "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md" in doctrine
    assert "Vocabulary authority" in doctrine
    assert "Packet / contract authority" in doctrine
    assert "Live workflow surfaces" in doctrine
    assert "Document-touch checklist requirement" in doctrine
    assert "Execution-thread reread requirement" in doctrine
    assert "Do not fill blanks with guesses." in doctrine
    assert "state-integrity invariants" in doctrine
    assert "variable" in doctrine
    assert "GitHub branch, commit, and merge history" in doctrine
    assert "fresh full-history zip" not in doctrine

    assert "## Intent and workflow anchor" in gate_template
    assert "## Retain / retire-from-authority / amend / add matrix" in gate_template
    assert "## Packet / contract discipline" in gate_template
    assert "## Document-touch checklist" in gate_template
    assert "## Contradiction scan and state-integrity rules" in gate_template
    assert "Repeat the gate block as many times as needed" in gate_template
    assert "exact GitHub branch/commit receipts were recorded for the gate closeout" in gate_template

    assert leaves["global_rules"]["vocabulary_authority_mandatory_before_new_naming"] is True
    assert leaves["global_rules"]["packet_contract_authority_mandatory_when_contracts_change"] is True
    assert leaves["global_rules"]["workflow_trace_mandatory_before_planning_new_behavior"] is True
    assert leaves["global_rules"]["git_history_primary_execution_ledger"] is True
    assert (
        leaves["global_rules"]["zip_required_only_on_explicit_operator_request_or_backup"]
        is True
    )
    assert "zip_required_before_gate_can_be_called_done" not in leaves["global_rules"]
    assert leaves["global_rules"]["document_touch_checklist_required"] is True
    assert leaves["global_rules"]["do_not_fill_unknowns_with_guesswork"] is True
    assert leaves["global_rules"]["completed_and_remaining_leaf_sets_must_be_disjoint"] is True
    assert leaves["global_rules"]["multi_gate_requests_do_not_waive_per_gate_closeout"] is True
    assert leaves["global_rules"]["gate_and_leaf_counts_are_variable_but_must_preserve_granularity"] is True
    assert leaves["contradiction_scan"]["required_before_new_pack"] is True
    assert leaves["state_invariants"]["active_gate_none_requires_no_remaining_or_pending_ids"] is True
    first_leaf = leaves["leaves"][0]
    assert "workflow_intent_assertion" in first_leaf
    assert "vocabulary_terms_checked" in first_leaf
    assert "document_touch_surfaces" in first_leaf
    assert any("Preserve granularity" in step for step in first_leaf["ordered_actions"])
    assert "GitHub branch, commit, and merge history is the default routine execution ledger" in execution_log_template
    assert "Gate <N> active on `work/<gate-branch-name>`" in execution_log_template
    assert "backup, offline handoff, or sandbox transfer packaging" in checklist_template
    assert (
        "Detailed workflow and tranche law lives in `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`"
        in agents
    )
    assert "GitHub branch, commit, and merge history is the primary execution ledger" in repo_law
    assert active_leaves["global_rules"]["git_history_primary_execution_ledger"] is True
    assert (
        active_leaves["global_rules"]["zip_required_only_on_explicit_operator_request_or_backup"]
        is True
    )
