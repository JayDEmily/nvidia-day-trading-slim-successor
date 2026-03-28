"""Gate 23 tests for review, P&L, attribution, and variant tracking."""

from __future__ import annotations

from typing import cast

from nvda_desk.schemas.dmp import DmpBehaviourClass, DmpGrammarRole
from nvda_desk.schemas.imported_modules.review_attribution import (
    ConfidenceDivergenceLoggerContractOutput,
    DailySummaryContractOutput,
    MacroAlignmentCheckerContractOutput,
    ModuleScoreAttributorContractOutput,
    ProfitLossLedgerContractOutput,
    VariantTraceLoggerContractOutput,
)
from nvda_desk.services.imported_modules.review_attribution import (
    ReviewAttributionContractService,
)
from tests.contract_chain_fixtures import build_gate23_context

EXPECTED_GATE23_ORDER = [
    "profit_loss_ledger",
    "module_trace_attribution",
    "daily_summary",
    "feedback_summary_writer",
    "module_score_attributor",
    "variant_trace_logger",
    "variant_performance_tracker",
    "confidence_divergence_logger",
    "macro_alignment_checker",
]


def test_review_attribution_contracts_emit_the_frozen_nine_modules_in_order() -> None:
    """Gate 23 should emit the review-chain contracts in the frozen gate-map order."""

    emissions = ReviewAttributionContractService().evaluate(build_gate23_context())
    assert [emission.output.canonical_slug for emission in emissions] == EXPECTED_GATE23_ORDER
    assert [emission.packet.grammar_role for emission in emissions[:7]] == [
        DmpGrammarRole.REVIEW_EXPLANATION,
        DmpGrammarRole.REVIEW_EXPLANATION,
        DmpGrammarRole.REVIEW_EXPLANATION,
        DmpGrammarRole.REVIEW_EXPLANATION,
        DmpGrammarRole.REVIEW_EXPLANATION,
        DmpGrammarRole.REVIEW_EXPLANATION,
        DmpGrammarRole.REVIEW_EXPLANATION,
    ]
    assert [emission.packet.grammar_role for emission in emissions[7:]] == [
        DmpGrammarRole.POSTURE_RISK_PERMISSION,
        DmpGrammarRole.POSTURE_RISK_PERMISSION,
    ]
    assert all(
        emission.packet.behaviour_class is DmpBehaviourClass.MODULE_OUTPUT for emission in emissions
    )


def test_review_attribution_builds_preview_pnl_and_variant_trace_surfaces() -> None:
    """Gate 23 should keep review-chain outputs useful without pretending they are booked P&L."""

    outputs = {
        emission.output.canonical_slug: emission.output
        for emission in ReviewAttributionContractService().evaluate(build_gate23_context())
    }
    profit_loss_ledger = cast(ProfitLossLedgerContractOutput, outputs["profit_loss_ledger"])
    daily_summary = cast(DailySummaryContractOutput, outputs["daily_summary"])
    module_score_attributor = cast(
        ModuleScoreAttributorContractOutput, outputs["module_score_attributor"]
    )
    variant_trace_logger = cast(VariantTraceLoggerContractOutput, outputs["variant_trace_logger"])

    assert profit_loss_ledger.ledger_state == "preview_pnl_ready"
    assert profit_loss_ledger.gross_exposure_pct == 65.0
    assert daily_summary.day_state == "positive_preview"
    assert daily_summary.summary_headline == "preview day green and orderly"
    assert module_score_attributor.score_state == "scored"
    assert module_score_attributor.module_scores["engine_score"] > 0.7
    assert variant_trace_logger.trace_state == "variant_traced"
    assert variant_trace_logger.variant_id == "trend_ladder_3_step::trend_window"


def test_review_attribution_marks_macro_and_confidence_stress_honestly() -> None:
    """Gate 23 should expose stressed macro caution and confidence divergence honestly."""

    outputs = {
        emission.output.canonical_slug: emission.output
        for emission in ReviewAttributionContractService().evaluate(
            build_gate23_context(stressed=True)
        )
    }
    profit_loss_ledger = cast(ProfitLossLedgerContractOutput, outputs["profit_loss_ledger"])
    confidence_divergence = cast(
        ConfidenceDivergenceLoggerContractOutput,
        outputs["confidence_divergence_logger"],
    )
    macro_alignment = cast(MacroAlignmentCheckerContractOutput, outputs["macro_alignment_checker"])

    assert profit_loss_ledger.ledger_state == "preview_pnl_ready"
    assert profit_loss_ledger.unrealized_pnl_pct < 0.0
    assert confidence_divergence.divergence_state == "divergent"
    assert confidence_divergence.divergence_score > 0.2
    assert macro_alignment.macro_alignment_state == "cautious"
    assert "macro_hostile" in macro_alignment.macro_flags
