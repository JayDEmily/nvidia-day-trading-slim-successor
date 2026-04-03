from __future__ import annotations

from datetime import datetime

from nvda_desk.domain.session_clock import SessionClockPhase
from nvda_desk.schemas.cognition import (
    ExecutionExpressionOutput,
    GammaState,
    InventoryState,
    LifecycleAction,
    LifecyclePlanOutput,
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


def _options_output(
    *, cluster: str = "pin_reversion_ready", dealer_pressure: str = "dealer_balancing"
) -> OptionsFlowContextOutput:
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
        surface_anchor_state="anchored_to_spot",
        reasons=["options_ready"],
    )


def _posture_output(
    permission: PermissionState = PermissionState.ALLOW,
) -> PostureRiskOutput:
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


def _inventory_state(
    *, existing: float = 12.0, overnight: float = 5.0, open_orders: int = 0
) -> InventoryState:
    return InventoryState(
        existing_inventory_pct=existing,
        fresh_cash_pct=60.0,
        overnight_inventory_pct=overnight,
        open_orders_count=open_orders,
        capital_lockup_pct=5.0,
        cost_basis_gap_pct=0.0,
        thesis_state_input="valid",
        adverse_excursion_pct=0.0,
    )


def _execution_output(
    active: list[str],
    *,
    lifecycle_plan: LifecyclePlanOutput | None = None,
) -> ExecutionExpressionOutput:
    active_setup_variant_ids = ["late_session_pin_reversion"] if active else []
    active_family_ids = ["pin_behaviour"] if active else []
    return ExecutionExpressionOutput(
        active_playbook_ids=active,
        active_setup_variant_ids=active_setup_variant_ids,
        active_family_ids=active_family_ids,
        lead_playbook_id=active[0] if active else None,
        lead_setup_variant_id=(active_setup_variant_ids[0] if active_setup_variant_ids else None),
        lead_family_id=active_family_ids[0] if active_family_ids else None,
        entry_style="pin_fade_scaler",
        playbook_execution_styles={playbook_id: "pin_fade_scaler" for playbook_id in active},
        setup_variant_execution_styles={
            setup_variant_id: "pin_fade_scaler" for setup_variant_id in active_setup_variant_ids
        },
        hedge_required=False,
        inventory_action="hold",
        fresh_capital_action="hold",
        thesis_invalidation_state="x",
        target_fresh_deployable_pct=35.0,
        scaling_plan=[1.0],
        invalidation_reasons=[],
        exit_reasons=[],
        exit_plan=[],
        lifecycle_plan=lifecycle_plan,
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
        inventory=_inventory_state(),
        execution=_execution_output(["pin_reversion"]),
    )

    assert handoff.horizon is CarryHorizon.WEEKEND
    assert handoff.weekend_window is True
    assert CarryAction.ADD_CARRY not in handoff.allowed_actions
    assert handoff.recommended_action_ceiling in {
        CarryAction.HOLD_BASELINE,
        CarryAction.HOLD_SMALL,
    }


def test_carry_handoff_builder_blocks_add_carry_inside_event_carry_window() -> None:
    handoff = CarryHandoffBuilder().build(
        symbol="NVDA",
        evaluation_ts=datetime.fromisoformat("2026-03-24T15:45:00-04:00"),
        temporal=_temporal_output(
            ts="2026-03-24T15:45:00-04:00", event_window_state="event_imminent_window"
        ),
        options_flow=_options_output(cluster="event_suppressed"),
        posture=_posture_output(),
        inventory=_inventory_state(),
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
        inventory=_inventory_state(),
        execution=_execution_output(["pin_reversion"]),
    )

    assert handoff.horizon is CarryHorizon.WEEKEND
    assert handoff.weekend_window is True
    assert handoff.next_session_open_ts is not None
    assert handoff.next_session_open_ts.weekday() == 0
    assert handoff.allowed_actions.count(CarryAction.HOLD_BASELINE) == 1


def test_carry_handoff_builder_consumes_lifecycle_small_overnight_nomination() -> None:
    handoff = CarryHandoffBuilder().build(
        symbol="NVDA",
        evaluation_ts=datetime.fromisoformat("2026-03-24T15:45:00-04:00"),
        temporal=_temporal_output(ts="2026-03-24T15:45:00-04:00"),
        options_flow=_options_output(),
        posture=_posture_output(),
        inventory=_inventory_state(existing=55.0, overnight=0.0),
        execution=_execution_output(
            ["continuation_ladder"],
            lifecycle_plan=LifecyclePlanOutput(
                setup_variant_id="opening_drive_continuation",
                execution_expression_id="continuation_ladder_exec",
                lifecycle_state="carry_nomination_ready",
                next_action=LifecycleAction.HOLD_SMALL_OVERNIGHT,
                carry_candidate=True,
                fired_rules=["late_session_carry_nomination"],
                rationale_codes=["gate_138_test"],
            ),
        ),
    )

    assert handoff.lifecycle_state == "carry_nomination_ready"
    assert handoff.lifecycle_next_action is LifecycleAction.HOLD_SMALL_OVERNIGHT
    assert handoff.lifecycle_action_ceiling is CarryAction.HOLD_SMALL
    assert handoff.allowed_actions == [CarryAction.FLATTEN, CarryAction.HOLD_SMALL]
    assert handoff.lifecycle_carry_candidate is True
    assert "lifecycle_ceiling:hold_small" in handoff.rationale_codes


def test_carry_handoff_builder_respects_lifecycle_flatten_ceiling() -> None:
    handoff = CarryHandoffBuilder().build(
        symbol="NVDA",
        evaluation_ts=datetime.fromisoformat("2026-03-24T15:58:00-04:00"),
        temporal=_temporal_output(ts="2026-03-24T15:58:00-04:00"),
        options_flow=_options_output(),
        posture=_posture_output(),
        inventory=_inventory_state(existing=22.0, overnight=0.0),
        execution=_execution_output(
            ["continuation_ladder"],
            lifecycle_plan=LifecyclePlanOutput(
                setup_variant_id="opening_drive_continuation",
                execution_expression_id="continuation_ladder_exec",
                lifecycle_state="stale_thesis_flatten",
                next_action=LifecycleAction.FLATTEN,
                carry_candidate=False,
                fired_rules=["close_window_stale_thesis"],
                blocked_rules=["carry_blocked_by_incomplete_ladder"],
                rationale_codes=["gate_138_test"],
            ),
        ),
    )

    assert handoff.lifecycle_action_ceiling is CarryAction.FLATTEN
    assert handoff.recommended_action_ceiling is CarryAction.FLATTEN
    assert handoff.allowed_actions == [CarryAction.FLATTEN]
    assert "lifecycle_ceiling:flatten" in handoff.rationale_codes
