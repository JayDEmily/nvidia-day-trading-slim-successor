"""Gate 22 tests for execution-state, exits, and lifecycle contracts."""

from __future__ import annotations

from typing import cast

from nvda_desk.schemas.dmp import DmpBehaviourClass, DmpGrammarRole
from nvda_desk.schemas.imported_modules.execution_lifecycle import (
    ExecutionLogWriterContractOutput,
    ExecutionTagsContractOutput,
    PositionBookContractOutput,
    TradeLoggerContractOutput,
    TrailingStopContractOutput,
    UnrealizedTrackerContractOutput,
)
from nvda_desk.services.imported_modules.execution_lifecycle import (
    ExecutionLifecycleContractService,
)
from tests.contract_chain_fixtures import build_gate22_context

EXPECTED_GATE22_ORDER = [
    "dynamic_partial_exit_model",
    "take_profit",
    "trailing_stop",
    "unrealized_tracker",
    "position_book",
    "trade_reentry_marker",
    "ladder_continuity_tracker",
    "fill_feedback_router",
    "execution_log_writer",
    "execution_tags",
    "trade_logger",
]


def test_execution_lifecycle_contracts_emit_the_frozen_eleven_modules_in_order() -> None:
    """Gate 22 should emit the execution-lifecycle chain in the frozen gate-map order."""

    emissions = ExecutionLifecycleContractService().evaluate(build_gate22_context())
    assert [emission.output.canonical_slug for emission in emissions] == EXPECTED_GATE22_ORDER
    assert all(emission.packet.grammar_role is DmpGrammarRole.EXPRESSION_EXECUTION for emission in emissions)
    assert all(emission.packet.behaviour_class is DmpBehaviourClass.MODULE_OUTPUT for emission in emissions)


def test_execution_lifecycle_builds_a_preview_position_and_traceable_tags() -> None:
    """Gate 22 should keep lifecycle outputs traceable without claiming live fills."""

    outputs = {
        emission.output.canonical_slug: emission.output
        for emission in ExecutionLifecycleContractService().evaluate(build_gate22_context())
    }
    trailing_stop = cast(TrailingStopContractOutput, outputs["trailing_stop"])
    unrealized_tracker = cast(UnrealizedTrackerContractOutput, outputs["unrealized_tracker"])
    position_book = cast(PositionBookContractOutput, outputs["position_book"])
    execution_log_writer = cast(ExecutionLogWriterContractOutput, outputs["execution_log_writer"])
    execution_tags = cast(ExecutionTagsContractOutput, outputs["execution_tags"])
    trade_logger = cast(TradeLoggerContractOutput, outputs["trade_logger"])

    assert trailing_stop.stop_state == "advisory_trailing_stop_ready"
    assert trailing_stop.trailing_stop_pct == 0.025
    assert unrealized_tracker.tracker_state == "preview_mark_to_market"
    assert position_book.book_state == "preview_position_open"
    assert position_book.live_position_pct == 65.0
    assert execution_log_writer.log_state == "preview_events_logged"
    assert "broker_requests" in execution_log_writer.missing_surfaces
    assert execution_tags.tagging_state == "tagged"
    assert "trend_ladder_3_step" in execution_tags.tags
    assert trade_logger.trade_log_state == "preview_trade_log_ready"
    assert trade_logger.record_count == execution_log_writer.event_count


def test_execution_lifecycle_degrades_to_permission_constrained_state_under_stress() -> None:
    """Gate 22 should keep a truthful constrained state when the stressed fixture blocks entry."""

    outputs = {
        emission.output.canonical_slug: emission.output
        for emission in ExecutionLifecycleContractService().evaluate(build_gate22_context(stressed=True))
    }
    unrealized_tracker = cast(UnrealizedTrackerContractOutput, outputs["unrealized_tracker"])
    execution_tags = cast(ExecutionTagsContractOutput, outputs["execution_tags"])
    trade_logger = cast(TradeLoggerContractOutput, outputs["trade_logger"])

    assert unrealized_tracker.tracker_state == "preview_mark_to_market"
    assert unrealized_tracker.unrealized_pnl_pct == -10.0
    assert "permission_constrained" in execution_tags.tags
    assert trade_logger.trade_log_state == "idle"
    assert trade_logger.last_event_tag == "stand_down"
