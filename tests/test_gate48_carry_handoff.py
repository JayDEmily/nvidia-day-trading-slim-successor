from __future__ import annotations

from datetime import datetime

from nvda_desk.domain.session_clock import SessionClockPhase
from nvda_desk.schemas.cognition import (
    ExecutionExpressionOutput,
    GammaState,
    OptionsFlowContextOutput,
    PermissionState,
    PostureRiskOutput,
    SkewState,
    TemporalContextOutput,
    TermStructureState,
)
from nvda_desk.schemas.overnight import CarryAction, CarryHorizon
from nvda_desk.services.carry_handoff import CarryHandoffBuilder


def _temporal_output(*, ts: str, event_window_state: str = "clear_window") -> TemporalContextOutput:
    return TemporalContextOutput(
        session_phase=SessionClockPhase.DEALER_UNWIND_CLOSE,
        desk_window="close",
        phase_confidence=0.92,
        clock_envelope="regular_hours",
        event_proximity_state="event_clear",
        event_window_state=event_window_state,
        expiry_cycle_state="monthly_expiry_week",
        recent_path_tag="intraday_squeeze",
        carryover_state="neutral",
        minutes_since_open=375,
        minutes_to_close=15,
        signal_coverage_ratio=0.85,
        reasons=["close_state"],
    )


def _options_output(*, cluster: str = "pin_reversion_ready", dealer_pressure: str = "dealer_balancing") -> OptionsFlowContextOutput:
    return OptionsFlowContextOutput(
        term_structure_state=TermStructureState.FLAT,
        skew_state=SkewState.BALANCED,
        gamma_state=GammaState.SUPPORTIVE,
        implied_move_envelope_pct=2.1,
        iv_rv_front_state="front_rich",
        iv_rv_next_state="next_neutral",
        iv_rv_curve_state="front_over_next",
        pin_risk_state="pin_risk_present",
        dealer_pressure_state=dealer_pressure,
        vix_spread_state="normalised",
        options_behavior_cluster=cluster,
        flow_tension_score=0.38,
        strike_cluster_state="live_pin_cluster",
        repeated_snapshot_state="stable",
        skew_evolution_state="stable",
        tenor_curve_state="normal",
        pin_progression_state="pin_stable",
        reasons=["options_ready"],
    )


def _posture_output(permission: PermissionState = PermissionState.ALLOW) -> PostureRiskOutput:
    return PostureRiskOutput(
        permission_state=permission,
        posture_label="test",
        inventory_posture_state="balanced",
        fresh_deployable_capital_pct=40.0,
        overnight_deployable_capital_pct=15.0,
        inventory_action_bias="hold",
        fresh_vs_inventory_state="balanced",
        thesis_state="valid",
        capital_lockup_state="normal",
        adverse_excursion_state="contained",
        time_stop_state="active",
        signal_conflict_state="clear",
        thesis_pressure_score=0.2,
        reasons=["ok"],
    )


def _execution_output(active: list[str]) -> ExecutionExpressionOutput:
    return ExecutionExpressionOutput(
        active_playbook_ids=active,
        entry_style="pin_fade_scaler",
        playbook_execution_styles={playbook_id: "pin_fade_scaler" for playbook_id in active},
        hedge_required=False,
        inventory_action="hold",
        fresh_capital_action="hold",
        thesis_invalidation_state="x",
        target_fresh_deployable_pct=35.0,
        scaling_plan=[1.0],
        invalidation_reasons=[],
        exit_reasons=[],
        exit_plan=[],
        reasons=["ok"],
    )


def test_carry_handoff_builder_treats_friday_close_as_weekend_branch() -> None:
    """Gate 48 should keep weekend carry as a separate branch, not an intraday extension."""

    handoff = CarryHandoffBuilder().build(
        symbol="NVDA",
        evaluation_ts=datetime.fromisoformat("2026-03-27T19:45:00-04:00"),
        temporal=_temporal_output(ts="2026-03-27T19:45:00-04:00"),
        options_flow=_options_output(),
        posture=_posture_output(),
        execution=_execution_output(["pin_reversion"]),
    )

    assert handoff.horizon is CarryHorizon.WEEKEND
    assert handoff.weekend_window is True
    assert CarryAction.ADD_CARRY not in handoff.allowed_actions
    assert handoff.recommended_action_ceiling in {CarryAction.HOLD_BASELINE, CarryAction.HOLD_SMALL}


def test_carry_handoff_builder_blocks_add_carry_inside_event_carry_window() -> None:
    handoff = CarryHandoffBuilder().build(
        symbol="NVDA",
        evaluation_ts=datetime.fromisoformat("2026-03-24T15:45:00-04:00"),
        temporal=_temporal_output(ts="2026-03-24T15:45:00-04:00", event_window_state="event_imminent_window"),
        options_flow=_options_output(cluster="event_suppressed"),
        posture=_posture_output(),
        execution=_execution_output(["term_structure_dislocation"]),
    )

    assert handoff.horizon is CarryHorizon.EVENT_CARRY
    assert handoff.event_carry_window is True
    assert CarryAction.ADD_CARRY not in handoff.allowed_actions


def test_carry_handoff_builder_treats_saturday_morning_as_weekend_branch() -> None:
    handoff = CarryHandoffBuilder().build(
        symbol="NVDA",
        evaluation_ts=datetime.fromisoformat("2026-03-28T08:15:00-04:00"),
        temporal=_temporal_output(ts="2026-03-28T08:15:00-04:00"),
        options_flow=_options_output(),
        posture=_posture_output(),
        execution=_execution_output(["pin_reversion"]),
    )

    assert handoff.horizon is CarryHorizon.WEEKEND
    assert handoff.weekend_window is True
    assert handoff.next_session_open_ts is not None
    assert handoff.next_session_open_ts.weekday() == 0
    assert handoff.allowed_actions.count(CarryAction.HOLD_BASELINE) == 1
