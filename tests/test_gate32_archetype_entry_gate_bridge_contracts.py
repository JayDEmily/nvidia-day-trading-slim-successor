"""Gate 32 coverage checks for the archetype and entry-gate bridge tranche."""

from __future__ import annotations

from typing import Any, cast

from nvda_desk.schemas.dmp import DmpGrammarRole
from nvda_desk.schemas.imported_modules.posture_enrichers import (
    ArchetypeTaggerContractOutput,
)
from nvda_desk.schemas.imported_modules.tranche_a import (
    ArchetypeMatcherContractOutput,
    EntryGateContractOutput,
)
from tests.contract_chain_fixtures import build_gate_support_bundle

EXPECTED_GATE32_ORDER = [
    "archetype_matcher",
    "archetype_tagger",
    "entry_gate",
]


def test_gate32_coverage_is_closed_in_frozen_order_with_bridge_dependencies() -> None:
    """Gate 32 should close exactly the three bridge items without new playbook invention."""

    supportive = build_gate_support_bundle()
    outputs = {
        **supportive.enricher_outputs,
        **supportive.selector_outputs,
    }
    ordered: list[Any] = [outputs[slug] for slug in EXPECTED_GATE32_ORDER]

    assert [output.canonical_slug for output in ordered] == EXPECTED_GATE32_ORDER
    assert [output.canonical_id for output in ordered] == [
        "archive-module-020",
        "archive-module-048",
        "archive-module-023",
    ]

    archetype_matcher = cast(
        ArchetypeMatcherContractOutput, outputs["archetype_matcher"]
    )
    archetype_tagger = cast(ArchetypeTaggerContractOutput, outputs["archetype_tagger"])
    entry_gate = cast(EntryGateContractOutput, outputs["entry_gate"])

    assert all(
        output.grammar_role == DmpGrammarRole.PLAYBOOK_ELIGIBILITY.value
        for output in ordered
    )
    assert archetype_matcher.matched_playbook in {
        "continuation_ladder",
        "compression_breakout",
        "pin_reversion",
        "negative_gamma_flush",
        None,
    }
    assert archetype_tagger.upstream_contract_slugs == [
        "engine_score",
        "options_behaviour_cluster",
    ]
    assert entry_gate.dependency_fences[0].dependency == "engine_score"
    assert entry_gate.entry_allowed is False
    assert entry_gate.suppression_tag == "event_window_veto"


def test_gate32_event_window_veto_keeps_entry_gate_honest_without_new_playbooks() -> (
    None
):
    """Gate 32 should cite veto state cleanly under stress and keep archetypes bounded."""

    stressed = build_gate_support_bundle(stressed=True)
    outputs = {
        **stressed.enricher_outputs,
        **stressed.selector_outputs,
    }
    entry_gate = cast(EntryGateContractOutput, outputs["entry_gate"])
    archetype_matcher = cast(
        ArchetypeMatcherContractOutput, outputs["archetype_matcher"]
    )

    assert entry_gate.entry_allowed is False
    assert entry_gate.suppression_tag in {"permission_blocked", "event_window_veto"}
    assert archetype_matcher.matched_playbook in {
        None,
        "negative_gamma_flush",
        "pin_reversion",
        "compression_breakout",
        "continuation_ladder",
    }
    assert "advisory" in entry_gate.contract_notes[0].lower()
