"""Gate 13 parity tests for registry-backed playbook loading."""

from __future__ import annotations

from datetime import datetime

from nvda_desk.config import Settings
from nvda_desk.schemas.cognition import (
    InventoryState,
    MarketRegimeContextInput,
    OptionsFlowContextInput,
    OptionsFlowMicroSnapshot,
    PinProgressionPoint,
    TemporalContextInput,
    TenorCurvePoint,
)
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.services.playbook_registry import PlaybookRegistryService


def test_registry_service_exposes_live_playbook_priority_and_templates() -> None:
    """Gate 13 should load playbook order and templates only from the checked-in registry."""

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
        registry.template_for_playbook("continuation_ladder").entry_style
        == "trend_ladder_3_step"
    )
    assert registry.template_for_playbook(
        "negative_gamma_flush"
    ).scaling_step_factors == [0.10, 0.15]


def test_registry_backed_runtime_preserves_supportive_playbook_outputs() -> None:
    """Registry-backed runtime should keep the existing continuation/compression fixture behaviour stable."""

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
            front_realised_vol=60.0,
            next_realised_vol=61.0,
            put_call_skew=0.18,
            gamma_pressure_score=0.33,
            call_put_imbalance=-0.05,
            oi_concentration=0.44,
            atm_straddle_value=5.9,
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
    assert result.execution.playbook_execution_styles == {
        "continuation_ladder": "trend_ladder_3_step",
        "compression_breakout": "compression_release_ladder",
    }
    assert result.execution.scaling_plan == [11.0, 16.5, 27.5]


def test_registry_backed_runtime_preserves_pin_reversion_path() -> None:
    """Registry-backed runtime should keep the pin-reversion execution path unchanged."""

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
            us10y=4.15,
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
    assert result.execution.playbook_execution_styles == {
        "pin_reversion": "pin_fade_scaler"
    }
