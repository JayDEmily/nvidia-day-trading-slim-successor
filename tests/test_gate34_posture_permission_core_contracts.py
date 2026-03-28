"""Gate 34 coverage checks for the posture and permission core tranche."""

from __future__ import annotations

from typing import Any, cast

from nvda_desk.schemas.dmp import DmpGrammarRole
from nvda_desk.schemas.imported_modules.tranche_a import (
    ConvictionTierAllocatorContractOutput,
    ModelConfidenceScorerContractOutput,
    SignalConflictDetectorContractOutput,
)
from tests.contract_chain_fixtures import build_gate_support_bundle

EXPECTED_GATE34_ORDER = [
    "signal_conflict_detector",
    "model_confidence_scorer",
    "conviction_tier_allocator",
]


def test_gate34_coverage_is_closed_in_frozen_order_with_non_approved_permission_honesty() -> (
    None
):
    """Gate 34 should close exactly the three posture core contracts."""

    supportive = build_gate_support_bundle()
    outputs = supportive.selector_outputs
    ordered: list[Any] = [outputs[slug] for slug in EXPECTED_GATE34_ORDER]

    assert [output.canonical_slug for output in ordered] == EXPECTED_GATE34_ORDER
    assert [output.canonical_id for output in ordered] == [
        "archive-evaluator-eval02",
        "archive-module-051",
        "archive-module-043",
    ]
    assert all(
        output.grammar_role == DmpGrammarRole.POSTURE_RISK_PERMISSION.value
        for output in ordered
    )

    signal_conflict = cast(
        SignalConflictDetectorContractOutput, outputs["signal_conflict_detector"]
    )
    confidence = cast(
        ModelConfidenceScorerContractOutput, outputs["model_confidence_scorer"]
    )
    conviction = cast(
        ConvictionTierAllocatorContractOutput, outputs["conviction_tier_allocator"]
    )

    assert signal_conflict.conflict_state in {"aligned", "conflicted"}
    assert confidence.confidence_band in {"high", "medium", "low"}
    assert conviction.conviction_tier in {"tier_1", "tier_2", "tier_3"}
    assert "advisory" in conviction.contract_notes[0].lower()


def test_gate34_stress_degrades_confidence_and_conviction_honestly() -> None:
    """Gate 34 should degrade under stress without pretending approval state."""

    stressed = build_gate_support_bundle(stressed=True)
    outputs = stressed.selector_outputs
    confidence = cast(
        ModelConfidenceScorerContractOutput, outputs["model_confidence_scorer"]
    )
    conviction = cast(
        ConvictionTierAllocatorContractOutput, outputs["conviction_tier_allocator"]
    )
    signal_conflict = cast(
        SignalConflictDetectorContractOutput, outputs["signal_conflict_detector"]
    )

    assert confidence.confidence_band in {"medium", "low"}
    assert conviction.conviction_tier in {"tier_2", "tier_3"}
    assert signal_conflict.conflict_score >= 0.0
    assert "Engine score remains fenced" in confidence.contract_notes[0]
