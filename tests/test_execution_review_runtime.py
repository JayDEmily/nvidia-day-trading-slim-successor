"""Gate D tests for expression/execution and review/explanation layers."""

from __future__ import annotations

from datetime import datetime
from typing import Any, cast

from nvda_desk.config import Settings
from nvda_desk.schemas.cognition import (
    InventoryState,
    MarketRegimeContextInput,
    OptionsFlowContextInput,
    OptionsFlowMicroSnapshot,
    PinProgressionPoint,
    StrikeClusterObservation,
    TemporalContextInput,
    TenorCurvePoint,
)
from nvda_desk.schemas.dmp_v2 import DmpV2ObjectBlock
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime


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
    assert result.execution.active_playbook_ids == ["continuation_ladder", "compression_breakout"]
    assert result.execution.entry_style == "trend_ladder_3_step"
    assert result.execution.playbook_execution_styles["continuation_ladder"] == "trend_ladder_3_step"
    assert result.execution.scaling_plan == [11.0, 16.5, 27.5]
    assert result.execution.thesis_invalidation_state == "trend_structure_broken"
    assert "leadership_lost" in result.execution.invalidation_reasons
    assert "trim_into_extension" in result.execution.exit_reasons


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
    assert any(item.contradiction_id == "regime_signal_conflict" for item in result.review.contradictions)
    assert "module_attribution" in result.review.review_packet
    conflicts = cast(list[str], result.review.review_packet["conflicts"])
    assert "regime_signal_conflict" in conflicts
    packet = cast(dict[str, Any], result.review.review_packet["execution"])
    assert packet["entry_style"] == "stand_aside"



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
    assert len(result.stage_packets_v2) == 7
    assert result.stage_packets[5].payload.model_dump(mode="json") == result.execution.model_dump(mode="json")
    assert result.stage_packets[6].payload.model_dump(mode="json") == result.review.model_dump(mode="json")
    assert isinstance(result.stage_packets_v2[5].blocks[0], DmpV2ObjectBlock)
    assert isinstance(result.stage_packets_v2[6].blocks[0], DmpV2ObjectBlock)
    assert result.stage_packets_v2[5].blocks[0].data == result.execution.model_dump(mode="json")
    assert result.stage_packets_v2[6].blocks[0].data == result.review.model_dump(mode="json")
    assert result.stage_packet_ids["execution"] == result.stage_packets[5].packet_identity.packet_id
    assert result.stage_packet_ids["execution"] == result.stage_packets_v2[5].packet_id
    assert result.stage_packets[6].trace_references.parent_packet_id == result.stage_packets[5].packet_identity.packet_id
    assert result.stage_packets_v2[6].lineage.parent_packet_ids == [result.stage_packets_v2[5].packet_id]
