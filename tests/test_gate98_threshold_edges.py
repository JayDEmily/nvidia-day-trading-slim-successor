"""Gate 98 targeted threshold-edge tests."""

from __future__ import annotations

from datetime import timedelta

import pytest

from nvda_desk.config import Settings
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture


@pytest.mark.parametrize(
    ("gamma_pressure_score", "expected_gamma_state"),
    [
        (0.10, "supportive"),
        (0.35, "supportive"),
        (0.50, "neutral"),
        (0.65, "destabilising"),
        (0.95, "destabilising"),
    ],
)
def test_gamma_pressure_edge_cases_are_monotonic_and_bounded(
    gamma_pressure_score: float,
    expected_gamma_state: str,
) -> None:
    fixture = supportive_runtime_fixture()
    runtime = DeskCognitionRuntime(Settings())
    options_flow = fixture.options_flow_input.model_copy(
        update={"gamma_pressure_score": gamma_pressure_score}
    )
    result = runtime.run(
        temporal_input=fixture.temporal_input,
        regime_input=fixture.regime_input,
        options_flow_input=options_flow,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )

    assert result.options_flow.gamma_state == expected_gamma_state

    if gamma_pressure_score < 0.65:
        assert result.execution.target_fresh_deployable_pct == 55.0
        assert result.posture.degradation_step == "normal"
    else:
        assert result.execution.target_fresh_deployable_pct == 30.25
        assert result.posture.degradation_step == "size_reduced"


@pytest.mark.parametrize(
    ("minutes_to_event", "expected_window", "expected_permission", "expected_target"),
    [
        (180, "same_session_event_window", "allow", 55.0),
        (90, "same_session_event_window", "allow", 55.0),
        (30, "event_imminent_window", "derisk", 0.0),
        (10, "event_imminent_window", "derisk", 0.0),
        (-1, "event_live_window", "block", 0.0),
    ],
)
def test_event_window_edge_cases_transition_lawfully(
    minutes_to_event: int,
    expected_window: str,
    expected_permission: str,
    expected_target: float,
) -> None:
    fixture = supportive_runtime_fixture()
    runtime = DeskCognitionRuntime(Settings())
    temporal = fixture.temporal_input.model_copy(
        update={"next_event_at": fixture.temporal_input.ts + timedelta(minutes=minutes_to_event)}
    )
    result = runtime.run(
        temporal_input=temporal,
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )

    assert result.temporal.event_window_state == expected_window
    assert result.posture.permission_state.value == expected_permission
    assert result.execution.target_fresh_deployable_pct == expected_target
    if expected_permission == "block":
        assert result.execution.active_playbook_ids == []
        assert "permission_blocked" in result.eligibility.no_trade_reasons
