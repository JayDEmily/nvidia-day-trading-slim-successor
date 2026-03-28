"""Gate 21 tests for execution-planning and broker-abstraction contracts."""

from __future__ import annotations

from typing import cast

from nvda_desk.schemas.dmp import DmpBehaviourClass, DmpGrammarRole
from nvda_desk.schemas.imported_modules.execution_planning import (
    BrokerAdapterContractOutput,
    EntryPlannerContractOutput,
    OrderSimulatorContractOutput,
    PositionAllocatorContractOutput,
    RunTradingBotContractOutput,
)
from nvda_desk.services.imported_modules.execution_planning import (
    ExecutionPlanningContractService,
)
from tests.contract_chain_fixtures import build_gate21_context

EXPECTED_GATE21_ORDER = [
    "broker_adapter",
    "entry_planner",
    "position_allocator",
    "order_simulator",
    "run_trading_bot",
]


def test_execution_planning_contracts_emit_the_frozen_five_modules_in_order() -> None:
    """Gate 21 should emit the five execution-planning contracts in gate-map order."""

    emissions = ExecutionPlanningContractService().evaluate(build_gate21_context())
    assert [
        emission.output.canonical_slug for emission in emissions
    ] == EXPECTED_GATE21_ORDER
    assert all(
        emission.packet.grammar_role is DmpGrammarRole.EXPRESSION_EXECUTION
        for emission in emissions
    )
    assert all(
        emission.packet.behaviour_class is DmpBehaviourClass.MODULE_OUTPUT
        for emission in emissions
    )


def test_execution_planning_keeps_broker_boundary_fenced_and_entry_preview_advisory() -> (
    None
):
    """Gate 21 should stop at a dry-run boundary while preserving a usable preview plan."""

    outputs = {
        emission.output.canonical_slug: emission.output
        for emission in ExecutionPlanningContractService().evaluate(
            build_gate21_context()
        )
    }
    broker_adapter = cast(BrokerAdapterContractOutput, outputs["broker_adapter"])
    entry_planner = cast(EntryPlannerContractOutput, outputs["entry_planner"])
    position_allocator = cast(
        PositionAllocatorContractOutput, outputs["position_allocator"]
    )
    order_simulator = cast(OrderSimulatorContractOutput, outputs["order_simulator"])
    run_trading_bot = cast(RunTradingBotContractOutput, outputs["run_trading_bot"])

    assert broker_adapter.routing_state == "fenced_no_broker_bridge"
    assert {fence.dependency for fence in broker_adapter.dependency_fences} == {
        "broker_requests",
        "runtime_translation",
    }
    assert entry_planner.planner_state == "advisory_plan_ready"
    assert entry_planner.planned_playbook == "continuation_ladder"
    assert entry_planner.planned_limit_price is not None
    assert position_allocator.allocation_state == "advisory_allocation_ready"
    assert position_allocator.target_position_pct == 55.0
    assert order_simulator.simulation_state == "advisory_fill_preview_with_vwap_gap"
    assert order_simulator.fill_probability > 0.7
    assert run_trading_bot.dispatch_state == "dry_run_preview_only"
    assert run_trading_bot.run_mode == "dry_run_only"


def test_execution_planning_stands_down_honestly_under_stress() -> None:
    """Gate 21 should degrade to suppression when the stressed fixture blocks entry."""

    outputs = {
        emission.output.canonical_slug: emission.output
        for emission in ExecutionPlanningContractService().evaluate(
            build_gate21_context(stressed=True)
        )
    }
    entry_planner = cast(EntryPlannerContractOutput, outputs["entry_planner"])
    order_simulator = cast(OrderSimulatorContractOutput, outputs["order_simulator"])
    run_trading_bot = cast(RunTradingBotContractOutput, outputs["run_trading_bot"])

    assert entry_planner.planner_state == "suppressed_by_gate"
    assert entry_planner.planned_limit_price is None
    assert order_simulator.simulation_state == "simulation_suppressed"
    assert run_trading_bot.active_dispatches == 0
    assert run_trading_bot.dispatch_state == "stand_down"
