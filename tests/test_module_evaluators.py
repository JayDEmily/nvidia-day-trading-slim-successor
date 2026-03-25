from __future__ import annotations

from nvda_desk.domain.session_clock import SessionClockPhase
from nvda_desk.fixtures import load_legacy_vwap_cases
from nvda_desk.schemas.overnight import OvernightCarryEvaluatorInput
from nvda_desk.schemas.slv import LadderRungInput, StrategicLadderValidatorInput
from nvda_desk.services.module_evaluators import (
    OvernightCarryEvaluatorService,
    StrategicLadderValidatorService,
)


def test_strategic_ladder_validator_adjusts_or_rejects_weak_ladder() -> None:
    service = StrategicLadderValidatorService()
    result = service.evaluate(
        StrategicLadderValidatorInput(
            spot_price=120.0,
            distance_to_vwap_pct=3.1,
            iv_hv_divergence_pct=28.0,
            session_phase=SessionClockPhase.PRE_MARKET,
            rungs=[
                LadderRungInput(
                    price=110.0,
                    size_units=10,
                    strike_pressure_score=0.2,
                    fill_plausibility_score=0.25,
                )
            ],
        )
    )
    assert result.overall_decision.value == "reject"
    assert result.rung_decisions[0].decision.value == "drop"
    assert "iv_hv_divergence_elevated" in result.reasons


def test_strategic_ladder_validator_phase_changes_outcome() -> None:
    service = StrategicLadderValidatorService()
    rung = LadderRungInput(
        price=119.0,
        size_units=10,
        strike_pressure_score=0.8,
        fill_plausibility_score=0.75,
    )
    pre_market = service.evaluate(
        StrategicLadderValidatorInput(
            spot_price=120.0,
            distance_to_vwap_pct=0.4,
            iv_hv_divergence_pct=5.0,
            session_phase=SessionClockPhase.PRE_MARKET,
            rungs=[rung],
        )
    )
    after_hours = service.evaluate(
        StrategicLadderValidatorInput(
            spot_price=120.0,
            distance_to_vwap_pct=0.4,
            iv_hv_divergence_pct=5.0,
            session_phase=SessionClockPhase.AFTER_HOURS,
            rungs=[rung],
        )
    )
    assert pre_market.overall_decision.value == "accept"
    assert after_hours.overall_decision.value in {"adjust", "reject"}


def test_overnight_carry_blocks_hot_risk_state() -> None:
    service = OvernightCarryEvaluatorService()
    result = service.evaluate(
        OvernightCarryEvaluatorInput(
            close_distance_to_vwap_pct=0.8,
            close_phase=SessionClockPhase.DEALER_UNWIND_CLOSE,
            realised_vol_pct=3.2,
            vix_level=34.0,
            vvix_level=118.0,
            asia_precursor_composite=0.4,
            risk_budget_remaining_pct=40.0,
            gross_exposure_pct=20.0,
            open_orders_count=1,
        )
    )
    assert result.carry_recommendation.value == "block"
    assert result.overnight_exposure_pct == 0.0
    assert result.carry_action.value == "block_carry"
    assert result.review_required is True


def test_overnight_carry_matches_admitted_vwap_case_biases() -> None:
    service = OvernightCarryEvaluatorService()
    cases = load_legacy_vwap_cases()
    de_risk_case = cases[0]
    supportive_case = cases[1]
    de_risk_result = service.evaluate(
        OvernightCarryEvaluatorInput(
            close_distance_to_vwap_pct=de_risk_case.close_distance_to_vwap_pct,
            close_phase=SessionClockPhase.DEALER_UNWIND_CLOSE,
            realised_vol_pct=4.5,
            vix_level=de_risk_case.vix_level,
            vvix_level=de_risk_case.vvix_level,
            asia_precursor_composite=de_risk_case.asia_precursor_composite,
            risk_budget_remaining_pct=35.0,
            gross_exposure_pct=20.0,
            open_orders_count=0,
        )
    )
    supportive_result = service.evaluate(
        OvernightCarryEvaluatorInput(
            close_distance_to_vwap_pct=supportive_case.close_distance_to_vwap_pct,
            close_phase=SessionClockPhase.DEALER_UNWIND_CLOSE,
            realised_vol_pct=2.5,
            vix_level=supportive_case.vix_level,
            vvix_level=supportive_case.vvix_level,
            asia_precursor_composite=supportive_case.asia_precursor_composite,
            risk_budget_remaining_pct=35.0,
            gross_exposure_pct=20.0,
            open_orders_count=0,
        )
    )
    assert de_risk_result.carry_recommendation.value in {"block", "flatten"}
    assert de_risk_result.carry_action.value in {"block_carry", "flatten"}
    assert supportive_result.carry_recommendation.value in {"increase", "hold_small"}
    assert supportive_result.carry_action.value in {"add_carry", "hold_small"}
