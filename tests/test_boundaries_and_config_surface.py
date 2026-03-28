from __future__ import annotations

import asyncio
from pathlib import Path

from nvda_desk.config_models import load_config_bundle
from nvda_desk.services.config_surface import ConfigSurfaceService
from nvda_desk.services.external_boundaries import (
    InMemoryBrokerAdapter,
    NullOpenAIOrchestrator,
    OpenAIResponseRequest,
    OrderIntent,
)


def test_config_bundle_parses_typed_weights_and_variants() -> None:
    bundle = load_config_bundle(Path(__file__).resolve().parents[1] / "config")
    assert bundle.coefficients_registry.runtime.layer1_signals["S06"].weight == 0.2
    assert (
        bundle.coefficients_registry.runtime.layer1_signals["S08"]
        .coefficients["vwap_proximity_pct"]
        .value
        == 1.5
    )
    assert (
        bundle.strategy_variants.variants["conservative"].overrides.weights["S06"]
        == 0.25
    )
    assert (
        bundle.strategy_variants.variants["conservative"].overrides.coefficients[
            "L3_01"
        ]["score_floor"]
        == 0.72
    )


def test_config_surface_resolves_supported_replay_overrides() -> None:
    service = ConfigSurfaceService(Path(__file__).resolve().parents[1] / "config")
    overrides = service.resolve_replay_overrides(
        strategy_variant_name="conservative",
        coefficient_group_name="S08",
    )
    assert overrides.entry_gate_score_floor == 0.72
    assert overrides.zone_score_threshold == 0.6
    assert overrides.distance_to_vwap_soft_limit_pct == 1.5
    assert overrides.risk_budget_remaining_pct == 50.0


async def _exercise_boundary_stubs() -> tuple[str, str, int]:
    broker = InMemoryBrokerAdapter()
    ref = await broker.place_order(
        OrderIntent(symbol="NVDA", side="buy", quantity=1, limit_price=100.0)
    )
    events = [event async for event in broker.stream_order_events()]
    orchestrator = NullOpenAIOrchestrator()
    artifact = await orchestrator.respond(
        OpenAIResponseRequest(
            prompt="Summarise risk state", tool_names=["risk_gateway"]
        )
    )
    return ref.status, artifact.status, len(events)


def test_external_boundary_stubs_remain_offline() -> None:
    broker_status, orchestrator_status, event_count = asyncio.run(
        _exercise_boundary_stubs()
    )
    assert broker_status == "filled"
    assert orchestrator_status == "unverified_stub"
    assert event_count == 1
