"""Gate 38 coverage checks for the review-ledger and attribution-spine tranche."""

from __future__ import annotations

from typing import Any, cast

from nvda_desk.schemas.dmp import DmpGrammarRole
from nvda_desk.schemas.imported_modules.review_attribution import (
    DailySummaryContractOutput,
    ModuleScoreAttributorContractOutput,
    ModuleTraceAttributionContractOutput,
    ProfitLossLedgerContractOutput,
)
from tests.contract_chain_fixtures import build_gate_execution_contract_bundle

EXPECTED_GATE38_ORDER = [
    "profit_loss_ledger",
    "module_trace_attribution",
    "module_score_attributor",
    "daily_summary",
]


def test_gate38_coverage_is_closed_in_frozen_order_with_preview_review_honesty() -> None:
    """Gate 38 should close exactly the four planned review-spine items."""

    supportive = build_gate_execution_contract_bundle()
    outputs = supportive.review_outputs
    ordered: list[Any] = [outputs[slug] for slug in EXPECTED_GATE38_ORDER]

    assert [output.canonical_slug for output in ordered] == EXPECTED_GATE38_ORDER
    assert [output.canonical_id for output in ordered] == [
        "archive-module-039",
        "archive-module-038",
        "archive-evaluator-eval01",
        "archive-module-041",
    ]
    assert all(output.grammar_role == DmpGrammarRole.REVIEW_EXPLANATION.value for output in ordered)

    profit_loss_ledger = cast(ProfitLossLedgerContractOutput, outputs["profit_loss_ledger"])
    module_trace = cast(ModuleTraceAttributionContractOutput, outputs["module_trace_attribution"])
    module_scores = cast(ModuleScoreAttributorContractOutput, outputs["module_score_attributor"])
    daily_summary = cast(DailySummaryContractOutput, outputs["daily_summary"])

    assert profit_loss_ledger.ledger_state == "preview_pnl_ready"
    assert module_trace.attribution_state == "coherent"
    assert module_scores.score_state == "scored"
    assert daily_summary.day_state == "positive_preview"
    assert module_trace.leading_modules[0] == "engine_score"
    assert module_scores.module_scores["engine_score"] > 0.7


def test_gate38_stress_keeps_review_spine_descriptive_and_not_booked() -> None:
    """Gate 38 should remain descriptive under stress without booked-ledger theatre."""

    stressed = build_gate_execution_contract_bundle(stressed=True)
    outputs = stressed.review_outputs

    profit_loss_ledger = cast(ProfitLossLedgerContractOutput, outputs["profit_loss_ledger"])
    module_trace = cast(ModuleTraceAttributionContractOutput, outputs["module_trace_attribution"])
    daily_summary = cast(DailySummaryContractOutput, outputs["daily_summary"])

    assert profit_loss_ledger.unrealized_pnl_pct < 0.0
    assert (
        profit_loss_ledger.contract_notes[0]
        == "P&L remains a deterministic preview ledger rather than a booked statement."
    )
    assert 0.0 <= module_trace.attribution_confidence <= 1.0
    assert daily_summary.day_state == "negative_preview"
    assert (
        daily_summary.contract_notes[0]
        == "The daily summary is an operator artefact derived only from preview execution state."
    )
