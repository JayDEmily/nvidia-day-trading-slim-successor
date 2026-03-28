"""Gate 36 coverage checks for the execution-state and ledger-spine tranche."""

from __future__ import annotations

from typing import Any, cast

from nvda_desk.schemas.dmp import DmpGrammarRole
from nvda_desk.schemas.imported_modules.execution_lifecycle import (
    ExecutionLogWriterContractOutput,
    PositionBookContractOutput,
    TradeLoggerContractOutput,
    UnrealizedTrackerContractOutput,
)
from tests.contract_chain_fixtures import build_gate_execution_contract_bundle

EXPECTED_GATE36_ORDER = [
    "execution_log_writer",
    "position_book",
    "trade_logger",
    "unrealized_tracker",
]


def test_gate36_coverage_is_closed_in_frozen_order_with_preview_state_honesty() -> None:
    """Gate 36 should close exactly the four planned execution-state spine items."""

    supportive = build_gate_execution_contract_bundle()
    outputs = supportive.lifecycle_outputs
    ordered: list[Any] = [outputs[slug] for slug in EXPECTED_GATE36_ORDER]

    assert [output.canonical_slug for output in ordered] == EXPECTED_GATE36_ORDER
    assert [output.canonical_id for output in ordered] == [
        "archive-module-030",
        "archive-module-031",
        "archive-module-037",
        "archive-module-032",
    ]
    assert all(
        output.grammar_role == DmpGrammarRole.EXPRESSION_EXECUTION.value
        for output in ordered
    )

    execution_log_writer = cast(
        ExecutionLogWriterContractOutput, outputs["execution_log_writer"]
    )
    position_book = cast(PositionBookContractOutput, outputs["position_book"])
    trade_logger = cast(TradeLoggerContractOutput, outputs["trade_logger"])
    unrealized_tracker = cast(
        UnrealizedTrackerContractOutput, outputs["unrealized_tracker"]
    )

    assert execution_log_writer.log_state == "preview_events_logged"
    assert "broker_requests" in execution_log_writer.missing_surfaces
    assert position_book.book_state == "preview_position_open"
    assert trade_logger.trade_log_state == "preview_trade_log_ready"
    assert trade_logger.record_count == execution_log_writer.event_count
    assert unrealized_tracker.tracker_state == "preview_mark_to_market"


def test_gate36_stress_keeps_state_spine_descriptive_and_unbooked() -> None:
    """Gate 36 should keep the state spine preview-only under stress."""

    stressed = build_gate_execution_contract_bundle(stressed=True)
    outputs = stressed.lifecycle_outputs

    position_book = cast(PositionBookContractOutput, outputs["position_book"])
    trade_logger = cast(TradeLoggerContractOutput, outputs["trade_logger"])
    unrealized_tracker = cast(
        UnrealizedTrackerContractOutput, outputs["unrealized_tracker"]
    )

    assert position_book.book_state in {"preview_position_open", "flat_or_locked"}
    assert trade_logger.trade_log_state == "idle"
    assert trade_logger.last_event_tag == "stand_down"
    assert unrealized_tracker.unrealized_pnl_pct == -10.0
