from __future__ import annotations

from pathlib import Path

from nvda_desk.schemas.vocabulary import VocabularyCategory, VocabularyDocument
from nvda_desk.services.playbook_registry import PlaybookRegistryService
from scripts.build_canonical_vocabulary import build_document

REPO_ROOT = Path(__file__).resolve().parents[1]
VOCAB_PATH = REPO_ROOT / "docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json"
FEED_PATH = REPO_ROOT / "data/vocabulary/feeder/2026-03-26_GATE55_WORKFLOW_ALIGNMENT_FEED.md"


def test_gate55_canonical_vocabulary_matches_generator_output() -> None:
    assert VOCAB_PATH.read_text(encoding="utf-8") == build_document().to_json_text()


def test_gate55_workflow_terms_have_explicit_canonical_owners() -> None:
    vocab = VocabularyDocument.from_json_path(VOCAB_PATH).entry_index()

    assert vocab["calendar_horizon_gate"].category is VocabularyCategory.WORKFLOW
    assert vocab["calendar_horizon_gate"].stage_owner == "step0_calendar_horizon"
    assert vocab["candidate_family_generation"].stage_owner == "playbook_eligibility"
    assert vocab["carry_handoff"].maps_to_contract == "nvda_desk.schemas.overnight.CloseStateCarryHandoff"
    assert vocab["carry_horizon_branch"].maps_to_contract == "nvda_desk.schemas.overnight.CarryHorizon"
    assert vocab["playbook_family"].maps_to_contract == "nvda_desk.schemas.playbook_registry.PlaybookFamilySpec"
    assert vocab["setup_variant"].maps_to_contract == "nvda_desk.schemas.playbook_registry.SetupVariantSpec"
    assert vocab["execution_expression"].maps_to_contract == "nvda_desk.schemas.playbook_registry.ExecutionTemplateSpec"


def test_gate55_registry_hierarchy_and_workflow_terms_are_all_covered() -> None:
    vocab = VocabularyDocument.from_json_path(VOCAB_PATH).entry_index()
    registry = PlaybookRegistryService().document()

    required_terms = {
        "calendar_horizon_gate",
        "candidate_family_generation",
        "playbook_family",
        "setup_variant",
        "execution_expression",
        "carry_handoff",
        "carry_horizon_branch",
    }
    assert required_terms.issubset(vocab)
    for family in registry.families:
        assert family.family_id in vocab
    for variant in registry.setup_variants:
        assert variant.setup_variant_id in vocab
    for template_id in registry.execution_template_index():
        assert template_id in vocab


def test_gate55_feeder_doc_uses_bounded_reconciliation_decisions() -> None:
    text = FEED_PATH.read_text(encoding="utf-8")

    assert "add_new" in text
    assert "alias_only" in text
    assert "calendar_horizon_gate" in text
    assert "carry_handoff" in text
