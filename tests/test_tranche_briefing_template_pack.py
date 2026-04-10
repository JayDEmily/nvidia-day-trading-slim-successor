"""Reference-pack checks for the tranche briefing template folder."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PACK_DIR = REPO_ROOT / "docs/planning/tranche_briefing_template_pack"
README = PACK_DIR / "README.md"
HOWTO = PACK_DIR / "HOW_TO_USE_THESE_DOCUMENTS.md"

LEGACY_FILES = [
    PACK_DIR / "2026-03-29_GENERIC_TRANCHE_BRIEFING_DOCTRINE_v2.md",
    PACK_DIR / "2026-03-29_GENERIC_GATE_TEMPLATE_v2.md",
    PACK_DIR / "2026-03-29_GENERIC_LEAVES_TEMPLATE_v2.json",
    PACK_DIR / "2026-03-29_WORKED_EXAMPLE_FINANCIAL_CALENDAR_SKELETON_v2.md",
    PACK_DIR / "2026-03-30_GENERIC_EXECUTION_LOG_TEMPLATE_v1.md",
    PACK_DIR / "2026-03-30_GENERIC_DOCUMENT_TOUCH_CHECKLIST_TEMPLATE_v1.md",
]

CURRENT_FILES = [
    PACK_DIR / "2026-04-06_GENERIC_TRANCHE_BRIEFING_DOCTRINE_v3.md",
    PACK_DIR / "2026-04-06_GENERIC_GATE_TEMPLATE_v3.md",
    PACK_DIR / "2026-04-06_GENERIC_LEAVES_TEMPLATE_v3.json",
    PACK_DIR / "2026-04-06_GENERIC_EXECUTION_LOG_TEMPLATE_v2.md",
    PACK_DIR / "2026-04-06_GENERIC_DOCUMENT_TOUCH_CHECKLIST_TEMPLATE_v2.md",
    PACK_DIR / "2026-04-06_WORKED_EXAMPLE_CONTROLLED_CONTINUITY_EXECUTION_PACK_SKELETON_v1.md",
]


def test_template_pack_contains_legacy_and_current_files() -> None:
    assert PACK_DIR.is_dir()
    for path in [README, HOWTO, *LEGACY_FILES, *CURRENT_FILES]:
        assert path.is_file(), path


def test_readme_and_howto_define_default_and_controlled_continuity_flow() -> None:
    readme = README.read_text(encoding="utf-8")
    howto = HOWTO.read_text(encoding="utf-8")

    assert "planning thread" in readme
    assert "coding thread" in readme
    assert "controlled continuity execution pack" in readme
    assert "variable gate and leaf counts" in readme
    assert "Do **not** fill blanks with guesses." in readme
    assert "vocabulary authority" in readme
    assert "packet/contract authority" in readme

    assert "controlled continuity" in howto
    assert "default stop-after-each-gate" in howto
    assert "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md" in howto
    assert "Do not paper over unknowns with vague wording." in howto
    assert "document-touch checklist" in howto
    assert "GitHub branch, commit, and merge history carries the routine execution ledger" in howto
    assert "Create a fresh full-history zip only if the operator explicitly requested" in howto
    assert "pack-install proof" in howto


def test_current_templates_freeze_continuity_and_closed_world_leaf_rules() -> None:
    doctrine = (PACK_DIR / "2026-04-06_GENERIC_TRANCHE_BRIEFING_DOCTRINE_v3.md").read_text(
        encoding="utf-8"
    )
    gate_template = (PACK_DIR / "2026-04-06_GENERIC_GATE_TEMPLATE_v3.md").read_text(
        encoding="utf-8"
    )
    leaves = json.loads(
        (PACK_DIR / "2026-04-06_GENERIC_LEAVES_TEMPLATE_v3.json").read_text(
            encoding="utf-8"
        )
    )
    execution_log_template = (
        PACK_DIR / "2026-04-06_GENERIC_EXECUTION_LOG_TEMPLATE_v2.md"
    ).read_text(encoding="utf-8")
    checklist_template = (
        PACK_DIR / "2026-04-06_GENERIC_DOCUMENT_TOUCH_CHECKLIST_TEMPLATE_v2.md"
    ).read_text(encoding="utf-8")
    repo_law = (REPO_ROOT / "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md").read_text(
        encoding="utf-8"
    )
    active_leaves = json.loads(
        (
            REPO_ROOT
            / "docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_LEAVES_v1.json"
        ).read_text(encoding="utf-8")
    )

    assert "optional controlled continuity packs" in doctrine
    assert "Mandatory pre-write scan for every new tranche" in doctrine
    assert "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md" in doctrine
    assert "GitHub branch, commit, and merge history" in doctrine
    assert "full-history zip was created only if the operator explicitly requested" in doctrine

    assert "## Workflow placement" in gate_template
    assert "## Execution continuity model" in gate_template
    assert "## Document-touch checklist" in gate_template
    assert "## Contradiction scan and state-integrity rules" in gate_template
    assert "exact GitHub branch/commit/merge receipts were recorded for the gate closeout" in gate_template

    assert leaves["global_rules"]["git_history_primary_execution_ledger"] is True
    assert (
        leaves["global_rules"]["zip_required_only_on_explicit_operator_request_or_backup"]
        is True
    )
    assert leaves["global_rules"]["do_not_fill_unknowns_with_guesswork"] is True
    assert leaves["global_rules"]["controlled_continuity_requires_explicit_pack_authorisation"] is True
    assert leaves["global_rules"]["planner_must_define_closed_world_scope"] is True
    assert leaves["continuity_policy"]["mode"] == "per_gate_reverification_default"
    assert leaves["continuity_policy"]["pack_install_receipt_required_before_first_gate"] is True
    assert leaves["continuity_policy"]["merge_to_main_required_before_next_gate"] is True
    assert "pack-install" in execution_log_template
    assert "continuity model after install" in execution_log_template
    assert "Continuity model checked" in checklist_template
    assert "controlled continuity" in checklist_template
    assert (
        "default stop-after-each-gate or controlled continuity model is named explicitly"
        in checklist_template
    )
    assert "## Controlled continuity execution packs" in repo_law
    assert "## Closed-world leaf requirement" in repo_law
    assert active_leaves["global_rules"]["git_history_primary_execution_ledger"] is True
    assert (
        active_leaves["global_rules"]["zip_required_only_on_explicit_operator_request_or_backup"]
        is True
    )
