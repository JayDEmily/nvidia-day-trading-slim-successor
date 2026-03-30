from __future__ import annotations

from nvda_desk.config import Settings
from nvda_desk.schemas.state_policy import MutableRuntimeSurface
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture


def test_gate118_all_declared_mutable_surfaces_flow_into_execution_output() -> None:
    fixture = supportive_runtime_fixture()
    runtime = DeskCognitionRuntime(Settings())
    result = runtime.run(
        temporal_input=fixture.temporal_input,
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )

    execution = result.execution
    packet = execution.modifier_runtime_packet
    assert packet is not None

    field_by_surface = {
        MutableRuntimeSurface.ENTRY_GATE_SCORE_FLOOR: execution.entry_gate_score_floor,
        MutableRuntimeSurface.ZONE_SCORE_THRESHOLD: execution.zone_score_threshold,
        MutableRuntimeSurface.DISTANCE_TO_VWAP_SOFT_LIMIT_PCT: execution.distance_to_vwap_soft_limit_pct,
        MutableRuntimeSurface.RISK_VIX_CAUTION_THRESHOLD: execution.risk_vix_caution_threshold,
        MutableRuntimeSurface.RISK_VIX_HOT_THRESHOLD: execution.risk_vix_hot_threshold,
        MutableRuntimeSurface.MAX_RISK_PER_TRADE: execution.max_risk_per_trade,
        MutableRuntimeSurface.TARGET_FRESH_DEPLOYABLE_PCT: execution.target_fresh_deployable_pct,
        MutableRuntimeSurface.HEDGE_REQUIRED: execution.hedge_required,
    }
    assert set(field_by_surface) == set(MutableRuntimeSurface)

    resolved_by_surface = {item.target_surface: item for item in packet.resolved_surfaces}
    for surface, observed in field_by_surface.items():
        resolved = resolved_by_surface[surface]
        if resolved.effective_numeric_value is not None:
            assert observed == resolved.effective_numeric_value
        else:
            assert observed == resolved.effective_boolean_value


def test_gate118_review_packet_exposes_operative_surfaces_for_downstream_consumers() -> None:
    fixture = supportive_runtime_fixture()
    runtime = DeskCognitionRuntime(Settings())
    result = runtime.run(
        temporal_input=fixture.temporal_input,
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )

    execution = result.review.review_packet["execution"]
    assert execution["entry_gate_score_floor"] == result.execution.entry_gate_score_floor
    assert execution["zone_score_threshold"] == result.execution.zone_score_threshold
    assert execution["distance_to_vwap_soft_limit_pct"] == result.execution.distance_to_vwap_soft_limit_pct
    assert execution["risk_vix_caution_threshold"] == result.execution.risk_vix_caution_threshold
    assert execution["risk_vix_hot_threshold"] == result.execution.risk_vix_hot_threshold
    assert execution["max_risk_per_trade"] == result.execution.max_risk_per_trade
