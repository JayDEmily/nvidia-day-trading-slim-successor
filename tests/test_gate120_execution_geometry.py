from __future__ import annotations

from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.schemas.cognition import ExecutionExpressionInput
from nvda_desk.schemas.state_policy import ModifierPriorityBand, ModifierRuntimePacket, MutableRuntimeSurface, ResolvedRuntimeSurfaceValue
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.services.execution_expression import ExecutionExpressionService
from nvda_desk.testing.canonical_raw_runtime_harness import CanonicalRawRuntimeHarnessService
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture


def _supportive_result():
    fixture = supportive_runtime_fixture()
    return DeskCognitionRuntime(Settings()).run(
        temporal_input=fixture.temporal_input,
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )


def _canonical_raw_result():
    fixture = supportive_runtime_fixture()
    harness = CanonicalRawRuntimeHarnessService().build_from_path(
        raw_bundle_path=Path("fixtures/real_data/gate_101_canonical_raw_runtime_bundle.json"),
        dataset_id="gate-e-prepared-runtime-dataset",
        regime_input=fixture.regime_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )
    return DeskCognitionRuntime(Settings()).run(
        temporal_input=harness.temporal_input,
        regime_input=harness.regime_input,
        options_flow_input=harness.options_flow_input,
        inventory_state=harness.inventory_state,
        risk_budget_remaining_pct=harness.risk_budget_remaining_pct,
    )


def test_gate120_supportive_runtime_emits_deterministic_execution_geometry() -> None:
    result = _supportive_result()

    assert result.execution.passive_aggressive_bias == "balanced"
    assert result.execution.ladder_spacing_bps == 18.0
    assert result.execution.max_chase_distance_bps == 16.8
    assert result.execution.stop_distance_bps == 45.0
    assert result.execution.take_profit_distance_bps == 90.0
    assert result.execution.per_slice_risk_pct == 0.1167
    assert "event_window_geometry_cautious" in result.execution.geometry_notes
    assert "max_risk_per_trade_cap_applied" in result.execution.geometry_notes


def test_gate120_contextual_stress_tightens_geometry_for_same_candidate() -> None:
    supportive = _supportive_result()
    stressed_options = supportive.options_flow.model_copy(update={"gamma_state": type(supportive.options_flow.gamma_state)("destabilising")})
    stressed_temporal = supportive.temporal.model_copy(update={"event_window_state": "event_imminent_window"})
    payload = ExecutionExpressionInput(
        temporal=stressed_temporal,
        regime=supportive.regime,
        options_flow=stressed_options,
        posture=supportive.posture,
        eligibility=supportive.eligibility,
        modifier_runtime_packet=supportive.execution.modifier_runtime_packet,
    )
    stressed_execution = ExecutionExpressionService().evaluate(payload)

    assert stressed_execution.lead_playbook_id == supportive.execution.lead_playbook_id
    assert stressed_execution.max_chase_distance_bps < supportive.execution.max_chase_distance_bps
    assert stressed_execution.stop_distance_bps > supportive.execution.stop_distance_bps
    assert stressed_execution.hedge_ratio >= supportive.execution.hedge_ratio
    assert "gamma_stress_geometry_tightened" in stressed_execution.geometry_notes


def test_gate120_max_risk_per_trade_caps_per_slice_risk() -> None:
    supportive = _supportive_result()
    packet = ModifierRuntimePacket(
        resolved_surfaces=[
            ResolvedRuntimeSurfaceValue(
                target_surface=MutableRuntimeSurface.MAX_RISK_PER_TRADE,
                owner_stage="execution",
                authority_version="2026-03-31.tranche1",
                baseline_reference="coefficient_authority:2026-03-31.tranche1:max_risk_per_trade",
                baseline_numeric_value=0.35,
                minimum_numeric_value=0.10,
                maximum_numeric_value=0.55,
                effective_numeric_value=0.12,
                winning_precedence_band=ModifierPriorityBand.EVENT_OPTIONS_STRESS,
                source_policy_ids=["test_cap"],
            )
        ]
    )
    payload = ExecutionExpressionInput(
        temporal=supportive.temporal,
        regime=supportive.regime,
        options_flow=supportive.options_flow,
        posture=supportive.posture,
        eligibility=supportive.eligibility,
        modifier_runtime_packet=packet,
    )
    execution = ExecutionExpressionService().evaluate(payload)

    assert execution.per_slice_risk_pct == 0.04
    assert "max_risk_per_trade_cap_applied" in execution.geometry_notes
