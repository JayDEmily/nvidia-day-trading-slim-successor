"""Gate 35 coverage checks for the execution-orchestration core tranche."""

from __future__ import annotations

from typing import Any, cast

from nvda_desk.schemas.dmp import DmpGrammarRole
from nvda_desk.schemas.imported_modules.execution_lifecycle import (
    ExecutionTagsContractOutput,
)
from nvda_desk.schemas.imported_modules.execution_planning import (
    BrokerAdapterContractOutput,
    EntryPlannerContractOutput,
    OrderSimulatorContractOutput,
    PositionAllocatorContractOutput,
    RunTradingBotContractOutput,
)
from tests.contract_chain_fixtures import build_gate_execution_contract_bundle

EXPECTED_GATE35_ORDER = [
    "entry_planner",
    "position_allocator",
    "order_simulator",
    "broker_adapter",
    "run_trading_bot",
    "execution_tags",
]


def test_gate35_coverage_is_closed_in_frozen_order_with_dry_run_orchestration_honesty() -> (
    None
):
    """Gate 35 should close exactly the six planned execution-orchestration items."""

    supportive = build_gate_execution_contract_bundle()
    outputs = {
        **supportive.planning_outputs,
        "execution_tags": supportive.lifecycle_outputs["execution_tags"],
    }
    ordered: list[Any] = [outputs[slug] for slug in EXPECTED_GATE35_ORDER]

    assert [output.canonical_slug for output in ordered] == EXPECTED_GATE35_ORDER
    assert [output.canonical_id for output in ordered] == [
        "archive-module-027",
        "archive-module-028",
        "archive-module-029",
        "archive-module-054",
        "archive-module-053",
        "archive-module-050",
    ]
    assert all(
        output.grammar_role == DmpGrammarRole.EXPRESSION_EXECUTION.value
        for output in ordered
    )

    entry_planner = cast(EntryPlannerContractOutput, outputs["entry_planner"])
    position_allocator = cast(
        PositionAllocatorContractOutput, outputs["position_allocator"]
    )
    order_simulator = cast(OrderSimulatorContractOutput, outputs["order_simulator"])
    broker_adapter = cast(BrokerAdapterContractOutput, outputs["broker_adapter"])
    run_trading_bot = cast(RunTradingBotContractOutput, outputs["run_trading_bot"])
    execution_tags = cast(ExecutionTagsContractOutput, outputs["execution_tags"])

    assert entry_planner.planner_state == "advisory_plan_ready"
    assert position_allocator.allocation_state == "advisory_allocation_ready"
    assert order_simulator.simulation_state == "advisory_fill_preview_with_vwap_gap"
    assert broker_adapter.routing_state == "fenced_no_broker_bridge"
    assert run_trading_bot.dispatch_state == "dry_run_preview_only"
    assert execution_tags.tagging_state == "tagged"
    assert execution_tags.upstream_contract_slugs == [
        "position_book",
        "fill_feedback_router",
    ]


def test_gate35_stress_keeps_orchestration_core_preview_only() -> None:
    """Gate 35 should stand down honestly under stress without claiming live routing."""

    stressed = build_gate_execution_contract_bundle(stressed=True)
    outputs = {
        **stressed.planning_outputs,
        "execution_tags": stressed.lifecycle_outputs["execution_tags"],
    }

    entry_planner = cast(EntryPlannerContractOutput, outputs["entry_planner"])
    order_simulator = cast(OrderSimulatorContractOutput, outputs["order_simulator"])
    run_trading_bot = cast(RunTradingBotContractOutput, outputs["run_trading_bot"])
    broker_adapter = cast(BrokerAdapterContractOutput, outputs["broker_adapter"])
    execution_tags = cast(ExecutionTagsContractOutput, outputs["execution_tags"])

    assert entry_planner.planner_state == "suppressed_by_gate"
    assert order_simulator.simulation_state == "simulation_suppressed"
    assert run_trading_bot.dispatch_state == "stand_down"
    assert broker_adapter.computation_mode.value == "fenced_contract_only"
    assert "permission_constrained" in execution_tags.tags
