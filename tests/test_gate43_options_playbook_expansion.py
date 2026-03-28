"""Gate 43 tests for options-first playbook expansion."""

from __future__ import annotations

from datetime import datetime

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
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.services.playbook_registry import PlaybookRegistryService


def test_registry_exposes_the_new_options_first_playbooks_in_deterministic_order() -> (
    None
):
    """Gate 43 should extend the registry with the new options-first playbooks."""

    registry = PlaybookRegistryService()

    assert registry.active_playbook_ids() == [
        "continuation_ladder",
        "compression_breakout",
        "pin_reversion",
        "negative_gamma_flush",
        "front_expiry_pin_pressure",
        "term_structure_dislocation",
        "skew_pressure_reversal",
    ]
    assert (
        registry.template_for_playbook("front_expiry_pin_pressure").entry_style
        == "front_pin_scaler"
    )
    assert (
        registry.template_for_playbook("term_structure_dislocation").entry_style
        == "term_dislocation_probe"
    )
    assert (
        registry.template_for_playbook("skew_pressure_reversal").entry_style
        == "skew_reversal_scaler"
    )


def test_runtime_promotes_front_expiry_pin_pressure_without_displacing_legacy_paths() -> (
    None
):
    """Front-expiry pin pressure should qualify only in the focused expiry-window setup."""

    runtime = DeskCognitionRuntime(Settings())
    result = runtime.run(
        temporal_input=TemporalContextInput(
            ts=datetime.fromisoformat("2026-03-20T10:20:00-04:00"),
            next_expiry=datetime.fromisoformat("2026-03-20T16:00:00-04:00"),
            prior_session_return_pct=0.3,
            intraday_move_pct=0.2,
            last_price=111.10,
            official_open_price=110.70,
            interval_volume_shares=2_000_000,
            cumulative_session_volume=8_500_000,
            session_vwap=110.9,
            distance_to_vwap_pct=0.18,
            vwap_slope_5m_pct=0.03,
            opening_range_high_5m=111.1,
            opening_range_low_5m=110.4,
            opening_range_break_count=1,
            price_realised_vol_5m_pct=8.0,
            price_realised_vol_15m_pct=10.0,
            relative_volume_ratio=1.03,
            rolling_range_5m_pct=0.25,
            impulse_age_bars=6,
        ),
        regime_input=MarketRegimeContextInput(
            nvda_return_pct=0.2,
            nq_return_pct=0.15,
            es_return_pct=0.1,
            sox_return_pct=0.2,
            breadth_score=0.54,
            concentration_score=0.46,
            vix_level=19.0,
            vvix_level=78.0,
            us10y=4.15,
            us2y=4.05,
            usdjpy=149.0,
        ),
        options_flow_input=OptionsFlowContextInput(
            spot_price=111.10,
            front_dte=0,
            next_dte=7,
            front_atm_iv=59.5,
            next_atm_iv=55.0,
            put_call_skew=0.06,
            gamma_pressure_score=0.28,
            call_put_imbalance=0.04,
            oi_concentration=0.72,
            atm_straddle_value=6.2,
            front_realised_vol=60.0,
            next_realised_vol=56.0,
            vix_level=19.0,
            vvix_level=78.0,
            spot_to_pin_distance_pct=0.18,
            nearby_strike_clusters=[
                StrikeClusterObservation(
                    strike=111.0,
                    side="mixed",
                    open_interest=18000.0,
                    volume=2600.0,
                    distance_to_spot_pct=0.09,
                )
            ],
            repeated_snapshot_sequence=[
                OptionsFlowMicroSnapshot(
                    ts=datetime.fromisoformat("2026-03-20T13:58:00+00:00"),
                    front_atm_iv=59.2,
                    next_atm_iv=55.1,
                    put_call_skew=0.05,
                    gamma_pressure_score=0.30,
                    spot_to_pin_distance_pct=0.35,
                ),
                OptionsFlowMicroSnapshot(
                    ts=datetime.fromisoformat("2026-03-20T14:05:00+00:00"),
                    front_atm_iv=59.5,
                    next_atm_iv=55.0,
                    put_call_skew=0.06,
                    gamma_pressure_score=0.28,
                    spot_to_pin_distance_pct=0.18,
                ),
            ],
            tenor_iv_curve=[
                TenorCurvePoint(tenor_dte=0, atm_iv=59.5),
                TenorCurvePoint(tenor_dte=7, atm_iv=55.0),
                TenorCurvePoint(tenor_dte=30, atm_iv=48.5),
            ],
            pin_progression_sequence=[
                PinProgressionPoint(
                    ts=datetime.fromisoformat("2026-03-20T13:58:00+00:00"),
                    distance_to_pin_pct=0.35,
                ),
                PinProgressionPoint(
                    ts=datetime.fromisoformat("2026-03-20T14:05:00+00:00"),
                    distance_to_pin_pct=0.18,
                ),
            ],
        ),
        inventory_state=InventoryState(
            existing_inventory_pct=18.0,
            fresh_cash_pct=58.0,
            overnight_inventory_pct=6.0,
            open_orders_count=1,
            capital_lockup_pct=18.0,
            cost_basis_gap_pct=-0.8,
            thesis_state_input="valid",
            adverse_excursion_pct=-1.2,
            time_stop_minutes_remaining=160,
        ),
        risk_budget_remaining_pct=62.0,
    )

    assert result.execution.active_playbook_ids == ["front_expiry_pin_pressure"]
    assert result.execution.entry_style == "front_pin_scaler"
    assert result.execution.inventory_action == "trim"


def test_runtime_promotes_term_structure_dislocation_when_curve_and_iv_rv_diverge() -> (
    None
):
    """Term-structure dislocation should use the new options-first playbook only in a real curve shock."""

    runtime = DeskCognitionRuntime(Settings())
    result = runtime.run(
        temporal_input=TemporalContextInput(
            ts=datetime.fromisoformat("2026-03-24T10:45:00-04:00"),
            next_expiry=datetime.fromisoformat("2026-03-28T16:00:00-04:00"),
            prior_session_return_pct=0.1,
            intraday_move_pct=0.4,
            last_price=176.5,
            official_open_price=174.8,
            interval_volume_shares=2_800_000,
            cumulative_session_volume=12_000_000,
            session_vwap=175.2,
            distance_to_vwap_pct=0.22,
            vwap_slope_5m_pct=0.04,
            opening_range_high_5m=176.8,
            opening_range_low_5m=173.9,
            opening_range_break_count=1,
            price_realised_vol_5m_pct=9.0,
            price_realised_vol_15m_pct=11.0,
            relative_volume_ratio=1.04,
            rolling_range_5m_pct=0.28,
            impulse_age_bars=6,
        ),
        regime_input=MarketRegimeContextInput(
            nvda_return_pct=0.7,
            nq_return_pct=0.3,
            es_return_pct=0.2,
            sox_return_pct=0.6,
            breadth_score=0.58,
            concentration_score=0.49,
            vix_level=20.5,
            vvix_level=72.0,
            us10y=4.22,
            us2y=4.08,
            usdjpy=149.4,
        ),
        options_flow_input=OptionsFlowContextInput(
            spot_price=176.5,
            front_dte=4,
            next_dte=11,
            front_atm_iv=72.0,
            next_atm_iv=66.0,
            put_call_skew=0.18,
            gamma_pressure_score=0.40,
            call_put_imbalance=0.08,
            oi_concentration=0.48,
            atm_straddle_value=11.0,
            front_realised_vol=50.0,
            next_realised_vol=54.0,
            vix_level=20.5,
            vvix_level=72.0,
            spot_to_pin_distance_pct=1.4,
            repeated_snapshot_sequence=[
                OptionsFlowMicroSnapshot(
                    ts=datetime.fromisoformat("2026-03-24T14:38:00+00:00"),
                    front_atm_iv=71.5,
                    next_atm_iv=65.5,
                    put_call_skew=0.16,
                    gamma_pressure_score=0.37,
                    spot_to_pin_distance_pct=1.5,
                ),
                OptionsFlowMicroSnapshot(
                    ts=datetime.fromisoformat("2026-03-24T14:45:00+00:00"),
                    front_atm_iv=72.0,
                    next_atm_iv=66.0,
                    put_call_skew=0.18,
                    gamma_pressure_score=0.40,
                    spot_to_pin_distance_pct=1.4,
                ),
            ],
            tenor_iv_curve=[
                TenorCurvePoint(tenor_dte=4, atm_iv=72.0),
                TenorCurvePoint(tenor_dte=11, atm_iv=66.0),
                TenorCurvePoint(tenor_dte=30, atm_iv=58.0),
            ],
        ),
        inventory_state=InventoryState(
            existing_inventory_pct=8.0,
            fresh_cash_pct=72.0,
            overnight_inventory_pct=0.0,
            open_orders_count=0,
            capital_lockup_pct=10.0,
            cost_basis_gap_pct=0.8,
            thesis_state_input="valid",
            adverse_excursion_pct=-0.6,
            time_stop_minutes_remaining=180,
        ),
        risk_budget_remaining_pct=70.0,
    )

    assert result.execution.active_playbook_ids == ["term_structure_dislocation"]
    assert result.execution.entry_style == "term_dislocation_probe"


def test_runtime_promotes_skew_pressure_reversal_when_dealer_tension_cools_without_a_flush() -> (
    None
):
    """Skew-pressure reversal should stay separate from the full negative-gamma flush playbook."""

    runtime = DeskCognitionRuntime(Settings())
    result = runtime.run(
        temporal_input=TemporalContextInput(
            ts=datetime.fromisoformat("2026-03-24T11:20:00-04:00"),
            next_expiry=datetime.fromisoformat("2026-03-28T16:00:00-04:00"),
            prior_session_return_pct=-0.2,
            intraday_move_pct=-0.4,
            last_price=175.3,
            official_open_price=176.0,
            interval_volume_shares=2_200_000,
            cumulative_session_volume=14_000_000,
            session_vwap=175.8,
            distance_to_vwap_pct=-0.12,
            vwap_slope_5m_pct=-0.01,
            opening_range_high_5m=177.9,
            opening_range_low_5m=173.7,
            opening_range_break_count=1,
            price_realised_vol_5m_pct=11.0,
            price_realised_vol_15m_pct=13.0,
            relative_volume_ratio=1.02,
            rolling_range_5m_pct=0.26,
            impulse_age_bars=12,
        ),
        regime_input=MarketRegimeContextInput(
            nvda_return_pct=-0.4,
            nq_return_pct=-0.1,
            es_return_pct=-0.05,
            sox_return_pct=-0.2,
            breadth_score=0.47,
            concentration_score=0.55,
            vix_level=21.0,
            vvix_level=72.0,
            us10y=4.28,
            us2y=4.12,
            usdjpy=148.7,
        ),
        options_flow_input=OptionsFlowContextInput(
            spot_price=175.3,
            front_dte=4,
            next_dte=11,
            front_atm_iv=68.0,
            next_atm_iv=64.0,
            put_call_skew=0.52,
            gamma_pressure_score=1.38,
            call_put_imbalance=0.15,
            oi_concentration=0.50,
            atm_straddle_value=10.4,
            front_realised_vol=78.0,
            next_realised_vol=76.0,
            vix_level=21.0,
            vvix_level=72.0,
            spot_to_pin_distance_pct=1.95,
            repeated_snapshot_sequence=[
                OptionsFlowMicroSnapshot(
                    ts=datetime.fromisoformat("2026-03-24T15:12:00+00:00"),
                    front_atm_iv=69.0,
                    next_atm_iv=64.5,
                    put_call_skew=0.40,
                    gamma_pressure_score=1.36,
                    spot_to_pin_distance_pct=2.0,
                ),
                OptionsFlowMicroSnapshot(
                    ts=datetime.fromisoformat("2026-03-24T15:20:00+00:00"),
                    front_atm_iv=68.0,
                    next_atm_iv=64.0,
                    put_call_skew=0.52,
                    gamma_pressure_score=1.38,
                    spot_to_pin_distance_pct=1.95,
                ),
            ],
            tenor_iv_curve=[
                TenorCurvePoint(tenor_dte=4, atm_iv=68.0),
                TenorCurvePoint(tenor_dte=11, atm_iv=64.0),
                TenorCurvePoint(tenor_dte=30, atm_iv=61.0),
            ],
            vanna_proxy=0.06,
            charm_proxy=0.06,
        ),
        inventory_state=InventoryState(
            existing_inventory_pct=12.0,
            fresh_cash_pct=66.0,
            overnight_inventory_pct=2.0,
            open_orders_count=1,
            capital_lockup_pct=16.0,
            cost_basis_gap_pct=-1.1,
            thesis_state_input="valid",
            adverse_excursion_pct=-1.4,
            time_stop_minutes_remaining=110,
        ),
        risk_budget_remaining_pct=58.0,
    )

    assert result.execution.active_playbook_ids == ["skew_pressure_reversal"]
    assert result.execution.entry_style == "skew_reversal_scaler"
    assert result.execution.hedge_required is True
