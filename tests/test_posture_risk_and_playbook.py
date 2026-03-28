"""Gate D tests for posture/risk governance and playbook eligibility."""

from __future__ import annotations

from datetime import datetime

from nvda_desk.config import Settings
from nvda_desk.schemas.cognition import (
    InventoryState,
    OptionsFlowContextInput,
    OptionsFlowMicroSnapshot,
    PlaybookAction,
    PlaybookDecision,
    PlaybookEligibilityInput,
    PostureRiskInput,
    TenorCurvePoint,
)
from nvda_desk.services.market_regime_context import MarketRegimeContextService
from nvda_desk.services.options_flow_context import OptionsFlowContextService
from nvda_desk.services.playbook_eligibility import PlaybookEligibilityService
from nvda_desk.services.posture_risk import PostureRiskService
from nvda_desk.services.temporal_context import TemporalContextService
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture


def test_posture_risk_exposes_trapped_inventory_and_conflicted_signals() -> None:
    """Gate D posture logic should make trapped/locked inventory states unavoidable."""

    fixture = supportive_runtime_fixture()
    temporal = TemporalContextService(Settings()).evaluate(fixture.temporal_input)
    regime = MarketRegimeContextService().evaluate(
        fixture.regime_input.model_copy(
            update={
                "breadth_score": 0.38,
                "concentration_score": 0.75,
            }
        )
    )
    options = OptionsFlowContextService().evaluate(
        fixture.options_flow_input.model_copy(
            update={
                "gamma_pressure_score": 0.70,
                "put_call_skew": 0.52,
                "front_realised_vol": 50.0,
                "next_realised_vol": 50.0,
                "vix_level": 24.0,
                "vvix_level": 108.0,
                "repeated_snapshot_sequence": [
                    OptionsFlowMicroSnapshot(
                        ts=datetime.fromisoformat("2026-03-23T18:10:00+00:00"),
                        front_atm_iv=60.0,
                        next_atm_iv=59.0,
                        put_call_skew=0.42,
                        gamma_pressure_score=0.58,
                        spot_to_pin_distance_pct=0.8,
                    ),
                    OptionsFlowMicroSnapshot(
                        ts=datetime.fromisoformat("2026-03-23T18:15:00+00:00"),
                        front_atm_iv=61.5,
                        next_atm_iv=59.8,
                        put_call_skew=0.52,
                        gamma_pressure_score=0.70,
                        spot_to_pin_distance_pct=0.5,
                    ),
                ],
            }
        )
    )
    posture = PostureRiskService().evaluate(
        PostureRiskInput(
            temporal=temporal,
            regime=regime,
            options_flow=options,
            inventory=InventoryState(
                existing_inventory_pct=32.0,
                fresh_cash_pct=12.0,
                overnight_inventory_pct=5.0,
                open_orders_count=1,
                capital_lockup_pct=58.0,
                cost_basis_gap_pct=-7.5,
                thesis_state_input="fragile",
                adverse_excursion_pct=-6.5,
                time_stop_minutes_remaining=12,
            ),
            risk_budget_remaining_pct=40.0,
        )
    )
    assert posture.permission_state.value == "derisk"
    assert posture.inventory_posture_state == "trapped"
    assert posture.fresh_vs_inventory_state == "inventory_locked"
    assert posture.signal_conflict_state == "conflicted_signals"
    assert posture.inventory_action_bias in {"trim", "hedge", "hold"}


def test_playbook_eligibility_surfaces_continuation_and_compression_families() -> None:
    """Gate D should expose explicit continuation and compression playbook families."""

    fixture = supportive_runtime_fixture()
    temporal = TemporalContextService(Settings()).evaluate(fixture.temporal_input)
    regime = MarketRegimeContextService().evaluate(fixture.regime_input)
    options = OptionsFlowContextService().evaluate(
        fixture.options_flow_input.model_copy(
            update={
                "front_atm_iv": 59.0,
                "next_atm_iv": 60.0,
                "front_realised_vol": 60.0,
                "next_realised_vol": 61.0,
                "spot_to_pin_distance_pct": 1.9,
                "vanna_proxy": 0.02,
                "charm_proxy": 0.01,
                "repeated_snapshot_sequence": [
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
                "tenor_iv_curve": [
                    TenorCurvePoint(tenor_dte=4, atm_iv=59.0),
                    TenorCurvePoint(tenor_dte=11, atm_iv=60.0),
                    TenorCurvePoint(tenor_dte=25, atm_iv=60.8),
                ],
            }
        )
    )
    posture = PostureRiskService().evaluate(
        PostureRiskInput(
            temporal=temporal,
            regime=regime,
            options_flow=options,
            inventory=fixture.inventory_state,
            risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
        )
    )
    eligibility = PlaybookEligibilityService().evaluate(
        PlaybookEligibilityInput(
            temporal=temporal,
            regime=regime,
            options_flow=options,
            posture=posture,
        )
    )
    decisions = {
        candidate.playbook_id: candidate.decision
        for candidate in eligibility.candidates
    }
    action_biases = {
        candidate.playbook_id: candidate.action_bias
        for candidate in eligibility.candidates
    }
    assert decisions["continuation_ladder"] is PlaybookDecision.ELIGIBLE
    assert decisions["compression_breakout"] is PlaybookDecision.ELIGIBLE
    assert action_biases["continuation_ladder"] is PlaybookAction.ADD
    assert "continuation_ladder" in eligibility.add_candidates
    assert eligibility.watch_only_candidates == []


def test_playbook_eligibility_distinguishes_probe_only_negative_gamma_flush() -> None:
    """Gate D should separate hostile watch-only flushes from buyable probe-only flushes."""

    temporal = TemporalContextService(Settings()).evaluate(
        supportive_runtime_fixture().temporal_input.model_copy(
            update={
                "ts": datetime.fromisoformat("2026-03-23T10:10:00-04:00"),
                "prior_session_return_pct": -1.8,
                "intraday_move_pct": -2.6,
                "next_event_at": None,
            }
        )
    )
    regime = MarketRegimeContextService().evaluate(
        supportive_runtime_fixture().regime_input.model_copy(
            update={
                "breadth_score": 0.55,
                "concentration_score": 0.48,
                "vix_level": 18.5,
                "vvix_level": 76.0,
            }
        )
    )
    options = OptionsFlowContextService().evaluate(
        OptionsFlowContextInput(
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
            vix_level=18.5,
            vvix_level=76.0,
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
        )
    )
    posture = PostureRiskService().evaluate(
        PostureRiskInput(
            temporal=temporal,
            regime=regime,
            options_flow=options,
            inventory=InventoryState(
                existing_inventory_pct=8.0,
                fresh_cash_pct=70.0,
                overnight_inventory_pct=0.0,
                open_orders_count=0,
                capital_lockup_pct=10.0,
                cost_basis_gap_pct=-1.0,
                thesis_state_input="valid",
                adverse_excursion_pct=-1.5,
                time_stop_minutes_remaining=90,
            ),
            risk_budget_remaining_pct=65.0,
        )
    )
    eligibility = PlaybookEligibilityService().evaluate(
        PlaybookEligibilityInput(
            temporal=temporal,
            regime=regime,
            options_flow=options,
            posture=posture,
        )
    )
    decisions = {
        candidate.playbook_id: candidate.decision
        for candidate in eligibility.candidates
    }
    assert decisions["negative_gamma_flush"] is PlaybookDecision.ELIGIBLE
    assert "negative_gamma_flush" in eligibility.probe_candidates
    assert "negative_gamma_flush" in eligibility.add_candidates


def test_playbook_eligibility_applies_event_window_veto() -> None:
    """Gate D should make event windows explicit no-trade filters."""

    fixture = supportive_runtime_fixture()
    temporal = TemporalContextService(Settings()).evaluate(
        fixture.temporal_input.model_copy(
            update={
                "next_event_at": datetime.fromisoformat("2026-03-23T14:35:00-04:00"),
            }
        )
    )
    regime = MarketRegimeContextService().evaluate(fixture.regime_input)
    options = OptionsFlowContextService().evaluate(
        fixture.options_flow_input.model_copy(
            update={
                "front_realised_vol": 60.0,
                "next_realised_vol": 60.0,
                "vix_level": 23.0,
                "vvix_level": 101.0,
            }
        )
    )
    posture = PostureRiskService().evaluate(
        PostureRiskInput(
            temporal=temporal,
            regime=regime,
            options_flow=options,
            inventory=fixture.inventory_state,
            risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
        )
    )
    eligibility = PlaybookEligibilityService().evaluate(
        PlaybookEligibilityInput(
            temporal=temporal,
            regime=regime,
            options_flow=options,
            posture=posture,
        )
    )
    assert "event_window_veto" in eligibility.no_trade_reasons
    assert all(
        candidate.decision is not PlaybookDecision.ELIGIBLE
        for candidate in eligibility.candidates
    )
