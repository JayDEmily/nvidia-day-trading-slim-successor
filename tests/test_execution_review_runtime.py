"""Gate D tests for expression/execution and review/explanation layers."""

from __future__ import annotations

from datetime import datetime
from typing import Any, cast

from nvda_desk.config import Settings
from nvda_desk.schemas.cognition import (
    ExecutionExpressionInput,
    InventoryState,
    LifecycleAction,
    MarketRegimeContextInput,
    OptionsFlowContextInput,
    OptionsFlowMicroSnapshot,
    PinProgressionPoint,
    PositionContextInput,
    StrikeClusterObservation,
    TemporalContextInput,
    TenorCurvePoint,
    TradableExpressionFamily,
)
from nvda_desk.schemas.dmp_v2 import DmpV2ObjectBlock
from nvda_desk.schemas.overnight import CarryAction
from nvda_desk.services.carry_handoff import CarryHandoffBuilder
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.services.execution_expression import ExecutionExpressionService
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture


def test_desk_cognition_runtime_emits_family_specific_execution_plan() -> None:
    """Gate D should emit ladder variants and invalidation reasons by playbook family."""

    runtime = DeskCognitionRuntime(Settings())
    result = runtime.run(
        temporal_input=TemporalContextInput(
            ts=datetime.fromisoformat("2026-03-23T14:15:00-04:00"),
            next_expiry=datetime.fromisoformat("2026-03-27T16:00:00-04:00"),
            next_event_at=datetime.fromisoformat("2026-03-23T17:00:00-04:00"),
            prior_session_return_pct=1.4,
            intraday_move_pct=0.8,
        ),
        regime_input=MarketRegimeContextInput(
            nvda_return_pct=0.8,
            nq_return_pct=0.5,
            es_return_pct=0.3,
            sox_return_pct=0.9,
            breadth_score=0.67,
            concentration_score=0.41,
            vix_level=18.4,
            vvix_level=84.0,
            us10y=4.22,
            us2y=4.04,
            usdjpy=148.9,
        ),
        options_flow_input=OptionsFlowContextInput(
            spot_price=118.0,
            front_dte=4,
            next_dte=11,
            front_atm_iv=59.0,
            next_atm_iv=60.0,
            put_call_skew=0.18,
            gamma_pressure_score=0.33,
            call_put_imbalance=-0.05,
            oi_concentration=0.44,
            atm_straddle_value=5.9,
            front_realised_vol=60.0,
            next_realised_vol=61.0,
            vix_level=18.4,
            vvix_level=84.0,
            spot_to_pin_distance_pct=1.9,
            vanna_proxy=0.02,
            charm_proxy=0.01,
            repeated_snapshot_sequence=[
                OptionsFlowMicroSnapshot(
                    ts=datetime.fromisoformat("2026-03-23T18:10:00+00:00"),
                    front_atm_iv=59.8,
                    next_atm_iv=60.4,
                    put_call_skew=0.16,
                    gamma_pressure_score=0.36,
                    spot_to_pin_distance_pct=1.9,
                ),
                OptionsFlowMicroSnapshot(
                    ts=datetime.fromisoformat("2026-03-23T18:15:00+00:00"),
                    front_atm_iv=59.0,
                    next_atm_iv=60.0,
                    put_call_skew=0.18,
                    gamma_pressure_score=0.33,
                    spot_to_pin_distance_pct=1.9,
                ),
            ],
            tenor_iv_curve=[
                TenorCurvePoint(tenor_dte=4, atm_iv=59.0),
                TenorCurvePoint(tenor_dte=11, atm_iv=60.0),
                TenorCurvePoint(tenor_dte=25, atm_iv=60.8),
            ],
        ),
        inventory_state=InventoryState(
            existing_inventory_pct=10.0,
            fresh_cash_pct=70.0,
            overnight_inventory_pct=0.0,
            open_orders_count=0,
            capital_lockup_pct=12.0,
            cost_basis_gap_pct=0.5,
            thesis_state_input="valid",
            adverse_excursion_pct=-1.0,
            time_stop_minutes_remaining=180,
        ),
        risk_budget_remaining_pct=68.0,
    )
    assert result.execution.active_playbook_ids == [
        "continuation_ladder",
        "compression_breakout",
    ]
    assert result.execution.entry_style == "trend_ladder_3_step"
    assert (
        result.execution.playbook_execution_styles["continuation_ladder"] == "trend_ladder_3_step"
    )
    assert result.execution.scaling_plan == [11.0, 16.5, 27.5]
    assert result.execution.thesis_invalidation_state == "trend_structure_broken"
    assert "leadership_lost" in result.execution.invalidation_reasons
    assert "trim_into_extension" in result.execution.exit_reasons
    assert result.execution.lifecycle_plan is not None
    assert result.execution.lifecycle_plan.setup_variant_id == "opening_drive_continuation"
    assert result.execution.lifecycle_plan.execution_expression_id == "continuation_ladder_exec"
    assert result.execution.lifecycle_plan.tradable_expression_family is not None
    assert result.execution.lifecycle_plan.tradable_expression_family.value == "single_leg_call_debit"
    assert result.execution.lifecycle_plan.next_action is LifecycleAction.ADD
    assert [action.value for action in result.execution.lifecycle_plan.allowed_actions] == [
        "add",
        "trim",
        "flatten",
        "hold_small_overnight",
        "block_carry",
    ]
    assert "gate_136_additive_lifecycle_scaffold" in result.execution.lifecycle_plan.rationale_codes


def test_desk_cognition_runtime_exposes_pin_reversion_review_packets() -> None:
    """Gate D should promote pin logic into execution and review output."""

    runtime = DeskCognitionRuntime(Settings())
    result = runtime.run(
        temporal_input=TemporalContextInput(
            ts=datetime.fromisoformat("2026-03-23T13:10:00-04:00"),
            next_expiry=datetime.fromisoformat("2026-03-27T16:00:00-04:00"),
            prior_session_return_pct=0.2,
            intraday_move_pct=0.1,
        ),
        regime_input=MarketRegimeContextInput(
            nvda_return_pct=0.2,
            nq_return_pct=0.1,
            es_return_pct=0.1,
            sox_return_pct=0.15,
            breadth_score=0.52,
            concentration_score=0.40,
            vix_level=18.0,
            vvix_level=82.0,
            us10y=4.20,
            us2y=4.05,
            usdjpy=149.0,
        ),
        options_flow_input=OptionsFlowContextInput(
            spot_price=118.0,
            front_dte=4,
            next_dte=11,
            front_atm_iv=58.0,
            next_atm_iv=58.4,
            put_call_skew=0.02,
            gamma_pressure_score=0.22,
            call_put_imbalance=-0.03,
            oi_concentration=0.66,
            atm_straddle_value=5.4,
            vix_level=18.0,
            vvix_level=82.0,
            spot_to_pin_distance_pct=0.2,
            nearby_strike_clusters=[
                StrikeClusterObservation(
                    strike=118.0,
                    side="mixed",
                    open_interest=12000.0,
                    volume=1800.0,
                    distance_to_spot_pct=0.0,
                )
            ],
            repeated_snapshot_sequence=[
                OptionsFlowMicroSnapshot(
                    ts=datetime.fromisoformat("2026-03-23T17:00:00+00:00"),
                    front_atm_iv=57.8,
                    next_atm_iv=58.3,
                    put_call_skew=0.01,
                    gamma_pressure_score=0.24,
                    spot_to_pin_distance_pct=0.6,
                ),
                OptionsFlowMicroSnapshot(
                    ts=datetime.fromisoformat("2026-03-23T17:05:00+00:00"),
                    front_atm_iv=58.0,
                    next_atm_iv=58.4,
                    put_call_skew=0.02,
                    gamma_pressure_score=0.22,
                    spot_to_pin_distance_pct=0.2,
                ),
            ],
            tenor_iv_curve=[
                TenorCurvePoint(tenor_dte=4, atm_iv=58.0),
                TenorCurvePoint(tenor_dte=11, atm_iv=58.4),
                TenorCurvePoint(tenor_dte=25, atm_iv=59.1),
            ],
            pin_progression_sequence=[
                PinProgressionPoint(
                    ts=datetime.fromisoformat("2026-03-23T17:00:00+00:00"),
                    distance_to_pin_pct=0.6,
                ),
                PinProgressionPoint(
                    ts=datetime.fromisoformat("2026-03-23T17:05:00+00:00"),
                    distance_to_pin_pct=0.2,
                ),
            ],
        ),
        inventory_state=InventoryState(
            existing_inventory_pct=22.0,
            fresh_cash_pct=60.0,
            overnight_inventory_pct=5.0,
            open_orders_count=1,
            capital_lockup_pct=20.0,
            cost_basis_gap_pct=-1.5,
            thesis_state_input="valid",
            adverse_excursion_pct=-2.0,
            time_stop_minutes_remaining=75,
        ),
        risk_budget_remaining_pct=50.0,
    )
    assert result.execution.active_playbook_ids == ["pin_reversion"]
    assert result.execution.entry_style == "pin_fade_scaler"
    assert result.execution.inventory_action == "trim"
    assert result.execution.exit_reasons[0] == "exit_on_pin_release"
    assert result.review.review_packet["module_attribution"]
    assert result.review.stage_reason_packets[2].summary == "pin_reversion_ready"


def test_review_packets_expose_conflict_density_and_contradictions() -> None:
    """Gate D review logic should surface conflict density and contradiction packets."""

    runtime = DeskCognitionRuntime(Settings())
    result = runtime.run(
        temporal_input=TemporalContextInput(
            ts=datetime.fromisoformat("2026-03-23T10:10:00-04:00"),
            next_expiry=datetime.fromisoformat("2026-03-27T16:00:00-04:00"),
            next_event_at=datetime.fromisoformat("2026-03-23T10:40:00-04:00"),
            prior_session_return_pct=-1.8,
            intraday_move_pct=-2.6,
        ),
        regime_input=MarketRegimeContextInput(
            nvda_return_pct=2.2,
            nq_return_pct=0.5,
            es_return_pct=0.4,
            sox_return_pct=1.6,
            breadth_score=0.38,
            concentration_score=0.76,
            vix_level=23.0,
            vvix_level=101.0,
            us10y=4.35,
            us2y=4.42,
            usdjpy=146.1,
        ),
        options_flow_input=OptionsFlowContextInput(
            spot_price=112.0,
            front_dte=4,
            next_dte=11,
            front_atm_iv=72.0,
            next_atm_iv=69.5,
            put_call_skew=0.58,
            gamma_pressure_score=0.78,
            call_put_imbalance=0.14,
            oi_concentration=0.58,
            atm_straddle_value=7.6,
            front_realised_vol=55.0,
            next_realised_vol=54.0,
            vix_level=23.0,
            vvix_level=101.0,
            spot_to_pin_distance_pct=0.8,
            repeated_snapshot_sequence=[
                OptionsFlowMicroSnapshot(
                    ts=datetime.fromisoformat("2026-03-23T14:00:00+00:00"),
                    front_atm_iv=70.5,
                    next_atm_iv=69.0,
                    put_call_skew=0.44,
                    gamma_pressure_score=0.65,
                    spot_to_pin_distance_pct=1.1,
                ),
                OptionsFlowMicroSnapshot(
                    ts=datetime.fromisoformat("2026-03-23T14:05:00+00:00"),
                    front_atm_iv=72.0,
                    next_atm_iv=69.5,
                    put_call_skew=0.58,
                    gamma_pressure_score=0.78,
                    spot_to_pin_distance_pct=0.8,
                ),
            ],
        ),
        inventory_state=InventoryState(
            existing_inventory_pct=6.0,
            fresh_cash_pct=75.0,
            overnight_inventory_pct=0.0,
            open_orders_count=0,
            capital_lockup_pct=8.0,
            cost_basis_gap_pct=-0.5,
            thesis_state_input="valid",
            adverse_excursion_pct=-1.0,
            time_stop_minutes_remaining=120,
        ),
        risk_budget_remaining_pct=65.0,
    )
    assert result.review.signal_conflict_density > 0.0
    assert "regime_signal_conflict" in result.review.conflict_tags
    assert any(
        item.contradiction_id == "regime_signal_conflict" for item in result.review.contradictions
    )
    assert "module_attribution" in result.review.review_packet
    conflicts = cast(list[str], result.review.review_packet["conflicts"])
    assert "regime_signal_conflict" in conflicts
    packet = cast(dict[str, Any], result.review.review_packet["execution"])
    assert packet["entry_style"] == "no_trade"


def test_runtime_stage_packets_preserve_execution_payloads_and_order() -> None:
    """Gate 9 should keep the existing typed payloads visible under ordered DMP wrappers."""

    runtime = DeskCognitionRuntime(Settings())
    result = runtime.run(
        temporal_input=TemporalContextInput(
            ts=datetime.fromisoformat("2026-03-23T14:15:00-04:00"),
            next_expiry=datetime.fromisoformat("2026-03-27T16:00:00-04:00"),
            next_event_at=datetime.fromisoformat("2026-03-23T17:00:00-04:00"),
            prior_session_return_pct=1.4,
            intraday_move_pct=0.8,
        ),
        regime_input=MarketRegimeContextInput(
            nvda_return_pct=0.8,
            nq_return_pct=0.5,
            es_return_pct=0.3,
            sox_return_pct=0.9,
            breadth_score=0.67,
            concentration_score=0.41,
            vix_level=18.4,
            vvix_level=84.0,
            us10y=4.22,
            us2y=4.04,
            usdjpy=148.9,
        ),
        options_flow_input=OptionsFlowContextInput(
            spot_price=118.0,
            front_dte=4,
            next_dte=11,
            front_atm_iv=59.0,
            next_atm_iv=60.0,
            put_call_skew=0.18,
            gamma_pressure_score=0.33,
            call_put_imbalance=-0.05,
            oi_concentration=0.44,
            atm_straddle_value=5.9,
            front_realised_vol=60.0,
            next_realised_vol=61.0,
            vix_level=18.4,
            vvix_level=84.0,
            spot_to_pin_distance_pct=1.9,
            vanna_proxy=0.02,
            charm_proxy=0.01,
        ),
        inventory_state=InventoryState(
            existing_inventory_pct=10.0,
            fresh_cash_pct=70.0,
            overnight_inventory_pct=0.0,
            open_orders_count=0,
            capital_lockup_pct=12.0,
            cost_basis_gap_pct=0.5,
            thesis_state_input="valid",
            adverse_excursion_pct=-1.0,
            time_stop_minutes_remaining=180,
        ),
        risk_budget_remaining_pct=68.0,
    )

    assert len(result.stage_packets) == 7
    assert result.stage_packets[5].payload.model_dump(mode="json") == result.execution.model_dump(
        mode="json"
    )
    assert result.stage_packets[6].payload.model_dump(mode="json") == result.review.model_dump(
        mode="json"
    )
    assert isinstance(result.stage_packets[5].blocks[0], DmpV2ObjectBlock)
    assert isinstance(result.stage_packets[6].blocks[0], DmpV2ObjectBlock)
    assert result.stage_packets[5].blocks[0].data == result.execution.model_dump(mode="json")
    assert result.stage_packets[6].blocks[0].data == result.review.model_dump(mode="json")
    execution_payload = result.stage_packets[5].blocks[0].data
    assert isinstance(execution_payload, dict)
    assert execution_payload["lifecycle_plan"]["execution_expression_id"] == "continuation_ladder_exec"
    assert execution_payload["lifecycle_plan"]["tradable_expression_family"] == "single_leg_call_debit"
    assert result.stage_packet_ids["execution"] == result.stage_packets[5].packet_id
    assert result.stage_packets[6].lineage.parent_packet_ids == [result.stage_packets[5].packet_id]

def test_review_packets_render_governed_resolved_surface_lineage() -> None:
    """Gate 125 review output should expose the governed resolved-surface chain directly."""

    fixture = supportive_runtime_fixture()
    result = DeskCognitionRuntime(Settings()).run(
        temporal_input=fixture.temporal_input.model_copy(
            update={
                "ts": datetime.fromisoformat("2026-03-23T15:20:00-04:00"),
                "next_event_at": datetime.fromisoformat("2026-03-24T08:30:00-04:00"),
            }
        ),
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )

    assert result.execution.modifier_runtime_packet is not None
    assert result.review.effective_policy is not None
    assert result.review.review_lineage is not None
    expected = [
        item.model_dump(mode="json") for item in result.execution.modifier_runtime_packet.resolved_surfaces
    ]
    assert [item.model_dump(mode="json") for item in result.review.effective_policy.resolved_surfaces] == expected
    assert [item.model_dump(mode="json") for item in result.review.review_lineage.resolved_surfaces] == expected
    review_effective = cast(dict[str, Any], result.review.review_packet["effective_policy"])
    assert cast(list[dict[str, Any]], review_effective["resolved_surfaces"]) == expected
    target = next(
        item for item in cast(list[dict[str, Any]], review_effective["resolved_surfaces"])
        if item["target_surface"] == "target_fresh_deployable_pct"
    )
    assert target["baseline_numeric_value"] == 55.0
    assert target["winning_precedence_band"] in {
        "phase_carry",
        "event_options_stress",
        "baseline",
    }
    assert any(item["source_policy_ids"] for item in cast(list[dict[str, Any]], review_effective["resolved_surfaces"]))




def _supportive_execution_input_with_position_context(*, current_position_size_pct: float, desk_window: str = "trend_window", event_window_state: str = "clear_window", carry_state_eligible: bool = False, hard_flat_required: bool = False) -> ExecutionExpressionInput:
    fixture = supportive_runtime_fixture()
    runtime_result = DeskCognitionRuntime(Settings()).run(
        temporal_input=fixture.temporal_input,
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )
    temporal = runtime_result.temporal.model_copy(
        update={"desk_window": desk_window, "event_window_state": event_window_state}
    )
    return ExecutionExpressionInput(
        temporal=temporal,
        regime=runtime_result.regime,
        options_flow=runtime_result.options_flow,
        posture=runtime_result.posture,
        eligibility=runtime_result.eligibility,
        modifier_runtime_packet=runtime_result.execution.modifier_runtime_packet,
        position_context=PositionContextInput(
            setup_variant_id="opening_drive_continuation",
            execution_expression_id="continuation_ladder_exec",
            tradable_expression_family=TradableExpressionFamily.SINGLE_LEG_CALL_DEBIT,
            legal_lifecycle_actions=[
                LifecycleAction.ADD,
                LifecycleAction.TRIM,
                LifecycleAction.FLATTEN,
                LifecycleAction.HOLD_SMALL_OVERNIGHT,
                LifecycleAction.BLOCK_CARRY,
            ],
            position_active=current_position_size_pct > 0.0,
            current_position_size_pct=current_position_size_pct,
            carry_state_eligible=carry_state_eligible,
            hard_flat_required=hard_flat_required,
        ),
    )


def test_continuation_lifecycle_flattens_when_breadth_rolls_over() -> None:
    payload = _supportive_execution_input_with_position_context(current_position_size_pct=22.0)
    payload = payload.model_copy(
        update={
            "regime": payload.regime.model_copy(update={"breadth_state": type(payload.regime.breadth_state)("weak")}),
        }
    )

    execution = ExecutionExpressionService().evaluate(payload)

    assert execution.lifecycle_plan is not None
    assert execution.lifecycle_plan.lifecycle_state == "specimen_invalidation_exit"
    assert execution.lifecycle_plan.next_action is LifecycleAction.FLATTEN
    assert "breadth_rollover" in execution.lifecycle_plan.fired_rules
    assert execution.inventory_action == "reduce"
    assert "breadth_rollover" in execution.exit_plan


def test_continuation_lifecycle_flattens_in_late_session_when_ladder_is_incomplete() -> None:
    payload = _supportive_execution_input_with_position_context(
        current_position_size_pct=10.0,
        desk_window="late_session",
        carry_state_eligible=True,
    )

    execution = ExecutionExpressionService().evaluate(payload)

    assert execution.lifecycle_plan is not None
    assert execution.lifecycle_plan.lifecycle_state == "stale_thesis_flatten"
    assert execution.lifecycle_plan.next_action is LifecycleAction.FLATTEN
    assert execution.inventory_action == "reduce"
    assert "close_window_stale_thesis" in execution.lifecycle_plan.fired_rules


def test_continuation_lifecycle_nominates_small_overnight_when_full_and_late() -> None:
    payload = _supportive_execution_input_with_position_context(
        current_position_size_pct=55.0,
        desk_window="late_session",
        carry_state_eligible=True,
    )

    execution = ExecutionExpressionService().evaluate(payload)

    assert execution.lifecycle_plan is not None
    assert execution.lifecycle_plan.lifecycle_state == "carry_nomination_ready"
    assert execution.lifecycle_plan.next_action is LifecycleAction.HOLD_SMALL_OVERNIGHT
    assert execution.lifecycle_plan.carry_candidate is True
    assert execution.inventory_action == "hold"
    assert "late_session_carry_nomination" in execution.exit_plan


def test_continuation_lifecycle_hard_flats_when_explicitly_required() -> None:
    payload = _supportive_execution_input_with_position_context(
        current_position_size_pct=22.0,
        desk_window="late_session",
        carry_state_eligible=True,
        hard_flat_required=True,
    )

    execution = ExecutionExpressionService().evaluate(payload)

    assert execution.lifecycle_plan is not None
    assert execution.lifecycle_plan.lifecycle_state == "hard_flat_required"
    assert execution.lifecycle_plan.next_action is LifecycleAction.FLATTEN
    assert execution.inventory_action == "reduce"
    assert "hard_flat_before_close" in execution.lifecycle_plan.fired_rules


def test_continuation_lifecycle_carry_handoff_stays_on_the_same_chain() -> None:
    payload = _supportive_execution_input_with_position_context(
        current_position_size_pct=55.0,
        desk_window="late_session",
        carry_state_eligible=True,
    )
    execution = ExecutionExpressionService().evaluate(payload)
    handoff = CarryHandoffBuilder().build(
        symbol="NVDA",
        evaluation_ts=datetime.fromisoformat("2026-03-23T15:45:00-04:00"),
        temporal=payload.temporal,
        options_flow=payload.options_flow,
        posture=payload.posture,
        inventory=InventoryState(
            existing_inventory_pct=55.0,
            fresh_cash_pct=15.0,
            overnight_inventory_pct=0.0,
            open_orders_count=0,
            capital_lockup_pct=12.0,
            cost_basis_gap_pct=0.5,
            thesis_state_input="valid",
            adverse_excursion_pct=-1.0,
            time_stop_minutes_remaining=120,
        ),
        execution=execution,
    )

    assert handoff.lifecycle_state == "carry_nomination_ready"
    assert handoff.lifecycle_next_action is LifecycleAction.HOLD_SMALL_OVERNIGHT
    assert handoff.lifecycle_action_ceiling is CarryAction.HOLD_SMALL
    assert handoff.allowed_actions == [CarryAction.FLATTEN, CarryAction.HOLD_SMALL]
    assert handoff.lifecycle_carry_candidate is True
