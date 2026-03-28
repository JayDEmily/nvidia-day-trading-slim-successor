"""Gate D tests for deterministic options-and-flow classification."""

from __future__ import annotations

from datetime import datetime

from nvda_desk.schemas.cognition import (
    GammaState,
    OptionsFlowContextInput,
    OptionsFlowMicroSnapshot,
    PinProgressionPoint,
    SkewState,
    StrikeClusterObservation,
    TenorCurvePoint,
)
from nvda_desk.services.options_flow_context import OptionsFlowContextService


def test_options_flow_context_detects_negative_gamma_flush_and_vvix_dislocation() -> None:
    """Gate D should convert hostile repeated snapshots into a real flush classifier."""

    service = OptionsFlowContextService()
    result = service.evaluate(
        OptionsFlowContextInput(
            spot_price=111.06,
            front_dte=4,
            next_dte=11,
            front_atm_iv=73.6,
            next_atm_iv=71.4,
            put_call_skew=0.55,
            gamma_pressure_score=0.72,
            call_put_imbalance=0.18,
            oi_concentration=0.61,
            atm_straddle_value=7.43,
            front_realised_vol=59.5,
            next_realised_vol=58.0,
            vix_level=29.0,
            vvix_level=118.0,
            spot_to_pin_distance_pct=0.3,
            vanna_proxy=0.45,
            charm_proxy=0.38,
            repeated_snapshot_sequence=[
                OptionsFlowMicroSnapshot(
                    ts=datetime.fromisoformat("2026-03-23T14:00:00+00:00"),
                    front_atm_iv=71.5,
                    next_atm_iv=70.9,
                    put_call_skew=0.42,
                    gamma_pressure_score=0.60,
                    spot_to_pin_distance_pct=0.6,
                ),
                OptionsFlowMicroSnapshot(
                    ts=datetime.fromisoformat("2026-03-23T14:05:00+00:00"),
                    front_atm_iv=73.6,
                    next_atm_iv=71.4,
                    put_call_skew=0.55,
                    gamma_pressure_score=0.72,
                    spot_to_pin_distance_pct=0.3,
                ),
            ],
        )
    )
    assert result.gamma_state is GammaState.DESTABILISING
    assert result.skew_state is SkewState.DOWNSIDE_HEAVY
    assert result.vix_spread_state == "vvix_dislocation"
    assert result.repeated_snapshot_state == "escalating_pressure"
    assert result.options_behavior_cluster == "event_suppressed"


def test_options_flow_context_extracts_live_pin_cluster_and_pin_progression() -> None:
    """Gate D should turn strike clusters and repeated pin distances into runtime state."""

    service = OptionsFlowContextService()
    result = service.evaluate(
        OptionsFlowContextInput(
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
            vix_level=18.4,
            vvix_level=84.0,
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
                    ts=datetime.fromisoformat("2026-03-23T14:00:00+00:00"),
                    front_atm_iv=57.8,
                    next_atm_iv=58.3,
                    put_call_skew=0.01,
                    gamma_pressure_score=0.24,
                    spot_to_pin_distance_pct=0.6,
                ),
                OptionsFlowMicroSnapshot(
                    ts=datetime.fromisoformat("2026-03-23T14:05:00+00:00"),
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
                    ts=datetime.fromisoformat("2026-03-23T14:00:00+00:00"),
                    distance_to_pin_pct=0.6,
                ),
                PinProgressionPoint(
                    ts=datetime.fromisoformat("2026-03-23T14:05:00+00:00"),
                    distance_to_pin_pct=0.2,
                ),
            ],
        )
    )
    assert result.strike_cluster_state == "live_pin_cluster"
    assert result.dominant_strike == 118.0
    assert result.tenor_curve_state == "contango_curve"
    assert result.pin_progression_state == "pinning_in"
    assert result.options_behavior_cluster == "pin_reversion_ready"


def test_options_flow_context_marks_compression_breakout_and_iv_curve_balance() -> None:
    """Gate D should expose calmer compression state instead of panic logic."""

    service = OptionsFlowContextService()
    result = service.evaluate(
        OptionsFlowContextInput(
            spot_price=118.0,
            front_dte=7,
            next_dte=14,
            front_atm_iv=58.0,
            next_atm_iv=58.5,
            put_call_skew=0.05,
            gamma_pressure_score=0.25,
            call_put_imbalance=-0.04,
            oi_concentration=0.33,
            atm_straddle_value=5.5,
            front_realised_vol=60.0,
            next_realised_vol=61.0,
            vix_level=18.0,
            vvix_level=82.0,
            spot_to_pin_distance_pct=1.8,
            repeated_snapshot_sequence=[
                OptionsFlowMicroSnapshot(
                    ts=datetime.fromisoformat("2026-03-23T14:00:00+00:00"),
                    front_atm_iv=58.8,
                    next_atm_iv=58.9,
                    put_call_skew=0.08,
                    gamma_pressure_score=0.32,
                    spot_to_pin_distance_pct=1.8,
                ),
                OptionsFlowMicroSnapshot(
                    ts=datetime.fromisoformat("2026-03-23T14:05:00+00:00"),
                    front_atm_iv=58.0,
                    next_atm_iv=58.5,
                    put_call_skew=0.05,
                    gamma_pressure_score=0.25,
                    spot_to_pin_distance_pct=1.7,
                ),
            ],
            tenor_iv_curve=[
                TenorCurvePoint(tenor_dte=7, atm_iv=58.0),
                TenorCurvePoint(tenor_dte=14, atm_iv=58.5),
                TenorCurvePoint(tenor_dte=28, atm_iv=59.0),
            ],
        )
    )
    assert result.gamma_state is GammaState.SUPPORTIVE
    assert result.vix_spread_state == "vvix_elevated"
    assert result.iv_rv_curve_state == "iv_curve_balanced"
    assert result.options_behavior_cluster == "compression_breakout_ready"
