"""Gate 37 coverage checks for the exit, re-entry, and continuity tranche."""

from __future__ import annotations

from typing import Any, cast

from nvda_desk.schemas.dmp import DmpGrammarRole
from nvda_desk.schemas.imported_modules.execution_lifecycle import (
    DynamicPartialExitModelContractOutput,
    FillFeedbackRouterContractOutput,
    LadderContinuityTrackerContractOutput,
    TakeProfitContractOutput,
    TradeReentryMarkerContractOutput,
    TrailingStopContractOutput,
)
from tests.contract_chain_fixtures import build_gate_execution_contract_bundle

EXPECTED_GATE37_ORDER = [
    "dynamic_partial_exit_model",
    "take_profit",
    "trailing_stop",
    "trade_reentry_marker",
    "fill_feedback_router",
    "ladder_continuity_tracker",
]


def test_gate37_coverage_is_closed_in_frozen_order_with_exit_chain_honesty() -> None:
    """Gate 37 should close exactly the six planned exit and continuity items."""

    supportive = build_gate_execution_contract_bundle()
    outputs = supportive.lifecycle_outputs
    ordered: list[Any] = [outputs[slug] for slug in EXPECTED_GATE37_ORDER]

    assert [output.canonical_slug for output in ordered] == EXPECTED_GATE37_ORDER
    assert [output.canonical_id for output in ordered] == [
        "archive-module-035",
        "archive-module-034",
        "archive-module-033",
        "archive-module-036",
        "archive-module-045",
        "archive-module-047",
    ]
    assert all(
        output.grammar_role == DmpGrammarRole.EXPRESSION_EXECUTION.value
        for output in ordered
    )

    dynamic_partial_exit = cast(
        DynamicPartialExitModelContractOutput, outputs["dynamic_partial_exit_model"]
    )
    take_profit = cast(TakeProfitContractOutput, outputs["take_profit"])
    trailing_stop = cast(TrailingStopContractOutput, outputs["trailing_stop"])
    trade_reentry = cast(
        TradeReentryMarkerContractOutput, outputs["trade_reentry_marker"]
    )
    fill_feedback = cast(
        FillFeedbackRouterContractOutput, outputs["fill_feedback_router"]
    )
    ladder_continuity = cast(
        LadderContinuityTrackerContractOutput, outputs["ladder_continuity_tracker"]
    )

    assert dynamic_partial_exit.model_state == "advisory_partial_exit_ready"
    assert take_profit.take_profit_state == "targets_ready"
    assert trailing_stop.stop_state == "advisory_trailing_stop_ready"
    assert trade_reentry.reentry_state == "position_still_live"
    assert fill_feedback.feedback_route == "feed_back_into_entry_planner"
    assert ladder_continuity.continuity_state == "continuous"
    assert ladder_continuity.ladder_hash is not None


def test_gate37_stress_keeps_exit_chain_preview_only_without_fill_theatre() -> None:
    """Gate 37 should remain dry-run and continuity-aware under stress."""

    stressed = build_gate_execution_contract_bundle(stressed=True)
    outputs = stressed.lifecycle_outputs

    trade_reentry = cast(
        TradeReentryMarkerContractOutput, outputs["trade_reentry_marker"]
    )
    fill_feedback = cast(
        FillFeedbackRouterContractOutput, outputs["fill_feedback_router"]
    )
    ladder_continuity = cast(
        LadderContinuityTrackerContractOutput, outputs["ladder_continuity_tracker"]
    )

    assert trade_reentry.reentry_allowed is False
    assert trade_reentry.reentry_state == "position_still_live"
    assert fill_feedback.feedback_route == "no_feedback_without_simulation"
    assert ladder_continuity.continuity_state == "no_ladder"
    assert 0.0 <= ladder_continuity.continuity_score <= 1.0
    assert "current-session ladder continuity" in ladder_continuity.contract_notes[0]
