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


def test_template_pack_contains_expected_files() -> None:
    assert PACK_DIR.is_dir()
    for path in [README, HOWTO, DOCTRINE, GATE_TEMPLATE, LEAVES_TEMPLATE, WORKED_EXAMPLE]:
        assert path.is_file(), path


def test_readme_and_howto_define_planning_thread_to_coding_thread_flow() -> None:
    readme = README.read_text(encoding="utf-8")
    howto = HOWTO.read_text(encoding="utf-8")

    assert "planning thread" in readme
    assert "coding thread" in readme
    assert "Do **not** fill blanks with guesses." in readme
    assert "vocabulary authority" in readme
    assert "packet/contract authority" in readme

    assert "planning thread" in howto
    assert "coding thread" in howto
    assert "python -m pip install -e .[dev]" in howto
    assert "Do not paper over unknowns with vague wording." in howto
    assert "fresh full-history zip" in howto


def test_doctrine_gate_and_leaves_templates_freeze_workflow_vocabulary_and_contract_checks() -> None:
    doctrine = DOCTRINE.read_text(encoding="utf-8")
    gate_template = GATE_TEMPLATE.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES_TEMPLATE.read_text(encoding="utf-8"))

    assert "Mandatory pre-write scan for every new tranche" in doctrine
    assert "Vocabulary authority" in doctrine
    assert "Packet / contract authority" in doctrine
    assert "Live workflow surfaces" in doctrine
    assert "Do not fill blanks with guesses." in doctrine

    assert "## Intent and workflow anchor" in gate_template
    assert "## Retain / retire-from-authority / amend / add matrix" in gate_template
    assert "## Packet / contract discipline" in gate_template

    assert leaves["global_rules"]["vocabulary_authority_mandatory_before_new_naming"] is True
    assert leaves["global_rules"]["packet_contract_authority_mandatory_when_contracts_change"] is True
    assert leaves["global_rules"]["workflow_trace_mandatory_before_planning_new_behavior"] is True
    assert leaves["global_rules"]["do_not_fill_unknowns_with_guesswork"] is True
    first_leaf = leaves["leaves"][0]
    assert "workflow_intent_assertion" in first_leaf
    assert "vocabulary_terms_checked" in first_leaf
