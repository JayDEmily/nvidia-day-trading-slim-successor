"""Gate 39 coverage checks for the remaining review overlays and feedback-chain tranche."""

from __future__ import annotations

from typing import Any, cast

from nvda_desk.schemas.dmp import DmpGrammarRole
from nvda_desk.schemas.imported_modules.posture_enrichers import TailHedgeInjectorContractOutput
from nvda_desk.schemas.imported_modules.review_attribution import (
    ConfidenceDivergenceLoggerContractOutput,
    FeedbackSummaryWriterContractOutput,
    MacroAlignmentCheckerContractOutput,
    VariantPerformanceTrackerContractOutput,
    VariantTraceLoggerContractOutput,
)
from tests.contract_chain_fixtures import build_gate_execution_contract_bundle

EXPECTED_GATE39_ORDER = [
    "variant_trace_logger",
    "variant_performance_tracker",
    "feedback_summary_writer",
    "macro_alignment_checker",
    "confidence_divergence_logger",
    "tail_hedge_injector",
]


def _gate39_outputs(*, stressed: bool = False) -> list[object]:
    bundle = build_gate_execution_contract_bundle(stressed=stressed)
    merged_outputs: dict[str, object] = {
        **bundle.review_outputs,
        **bundle.support_outputs,
    }
    return [merged_outputs[slug] for slug in EXPECTED_GATE39_ORDER]


def test_gate39_coverage_is_closed_in_frozen_order_and_exhausts_remaining_backlog() -> None:
    """Gate 39 should close exactly the six remaining ready-import items in frozen order."""

    ordered: list[Any] = _gate39_outputs()

    assert [output.canonical_slug for output in ordered] == EXPECTED_GATE39_ORDER
    assert [output.canonical_id for output in ordered] == [
        "archive-module-040",
        "archive-evaluator-eval04",
        "archive-evaluator-eval06",
        "archive-evaluator-eval03",
        "archive-evaluator-eval05",
        "archive-module-049",
    ]
    assert [output.grammar_role for output in ordered[:3]] == [
        DmpGrammarRole.REVIEW_EXPLANATION.value,
        DmpGrammarRole.REVIEW_EXPLANATION.value,
        DmpGrammarRole.REVIEW_EXPLANATION.value,
    ]
    assert [output.grammar_role for output in ordered[3:]] == [
        DmpGrammarRole.POSTURE_RISK_PERMISSION.value,
        DmpGrammarRole.POSTURE_RISK_PERMISSION.value,
        DmpGrammarRole.POSTURE_RISK_PERMISSION.value,
    ]

    variant_trace = cast(VariantTraceLoggerContractOutput, ordered[0])
    variant_performance = cast(VariantPerformanceTrackerContractOutput, ordered[1])
    feedback_summary = cast(FeedbackSummaryWriterContractOutput, ordered[2])
    macro_alignment = cast(MacroAlignmentCheckerContractOutput, ordered[3])
    confidence_divergence = cast(ConfidenceDivergenceLoggerContractOutput, ordered[4])
    tail_hedge = cast(TailHedgeInjectorContractOutput, ordered[5])

    assert variant_trace.trace_state == "variant_traced"
    assert variant_performance.tracker_state == "variant_scored"
    assert feedback_summary.summary_state == "feedback_written"
    assert macro_alignment.macro_alignment_state in {"aligned", "cautious"}
    assert confidence_divergence.divergence_state in {"aligned", "divergent"}
    assert tail_hedge.injector_state in {"hedge_clear", "hedge_advised"}
    assert "operator-facing summary" in feedback_summary.contract_notes[0]
    assert "advisory" in tail_hedge.contract_notes[0].lower()


def test_gate39_stress_keeps_feedback_and_hedge_surfaces_advisory_only() -> None:
    """Gate 39 should stay descriptive under stress and avoid live hedge or self-optimising claims."""

    ordered: list[Any] = _gate39_outputs(stressed=True)

    variant_performance = cast(VariantPerformanceTrackerContractOutput, ordered[1])
    feedback_summary = cast(FeedbackSummaryWriterContractOutput, ordered[2])
    macro_alignment = cast(MacroAlignmentCheckerContractOutput, ordered[3])
    confidence_divergence = cast(ConfidenceDivergenceLoggerContractOutput, ordered[4])
    tail_hedge = cast(TailHedgeInjectorContractOutput, ordered[5])

    assert 0.0 <= variant_performance.performance_score <= 1.0
    assert feedback_summary.summary_state == "feedback_written"
    assert macro_alignment.macro_alignment_state == "cautious"
    assert confidence_divergence.divergence_state == "divergent"
    assert tail_hedge.injector_state == "hedge_advised"
    assert tail_hedge.hedge_ratio == 0.25
    assert "live hedge placement" not in " ".join(tail_hedge.contract_notes).lower()
