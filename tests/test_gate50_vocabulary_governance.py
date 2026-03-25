from __future__ import annotations

from pathlib import Path

from nvda_desk.schemas.vocabulary import VocabularyDocument
from nvda_desk.services.playbook_registry import PlaybookRegistryService
from scripts.build_canonical_vocabulary import build_document

VOCAB_PATH = Path("docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json")


def test_canonical_vocabulary_covers_current_registry_hierarchy() -> None:
    """Gate 50 should govern current families, setup variants, expressions, and compatibility labels."""

    vocab = VocabularyDocument.from_json_path(VOCAB_PATH)
    index = vocab.entry_index()
    registry = PlaybookRegistryService()

    for family in registry.document().families:
        assert family.family_id in index
    for variant in registry.document().setup_variants:
        assert variant.setup_variant_id in index
    for template_id in registry.document().execution_template_index():
        assert template_id in index
    assert "temporal_state" in index
    assert index["session_clock"].category.value == "compatibility_surface"


def test_vocabulary_aliases_do_not_reference_stale_canonical_truth() -> None:
    vocab = VocabularyDocument.from_json_path(VOCAB_PATH)
    session_clock = vocab.entry_index()["session_clock"]

    assert "canonical_step1_truth" in session_clock.disallowed_phrases
    assert "session_clock_wrapper" in session_clock.allowed_aliases


def test_canonical_vocabulary_file_matches_generator_output() -> None:
    generated = build_document().to_json_text()
    committed = VOCAB_PATH.read_text(encoding="utf-8")

    assert committed == generated
