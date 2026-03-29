from __future__ import annotations

from nvda_desk.domain.session_clock import SessionClockPhase
from nvda_desk.schemas.cognition import (
    PlaybookEligibilityInput,
    PostureRiskInput,
    ReviewExplanationInput,
    TemporalContextOutput,
)
from nvda_desk.services.market_regime_context import MarketRegimeContextService
from nvda_desk.services.options_flow_context import OptionsFlowContextService
from nvda_desk.services.playbook_eligibility import PlaybookEligibilityService
from nvda_desk.services.posture_risk import PostureRiskService
from nvda_desk.services.review_explanation import ReviewExplanationService
from nvda_desk.services.state_conditioned_modifier import StateConditionedModifierService
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture
from tests.test_gate48_carry_handoff import _execution_output


def _temporal_output(
    *,
    desk_window: str,
    event_window_state: str,
    event_proximity_state: str,
    active_event_family: str,
    event_risk_timing_class: str = "priced_risk",
    event_carry_sensitivity: str = "carry_sensitive",
    event_overlap_class: str = "single_event",
    expiry_cycle_state: str = "next_cycle",
    calendar_closure_classes: list[str] | None = None,
) -> TemporalContextOutput:
    return TemporalContextOutput(
        session_phase=SessionClockPhase.DEALER_UNWIND_CLOSE,
        desk_window=desk_window,
        phase_confidence=0.92,
        clock_envelope="regular_hours",
        behavioural_phase=SessionClockPhase.DEALER_UNWIND_CLOSE,
        signal_coverage_ratio=0.88,
        minutes_since_open=375,
        minutes_to_close=15,
        expiry_days_remaining=3,
        expiry_cycle_state=expiry_cycle_state,
        event_minutes_remaining=30,
        event_proximity_state=event_proximity_state,
        event_window_state=event_window_state,
        event_overlap_class=event_overlap_class,
        event_risk_timing_class=event_risk_timing_class,
        event_carry_sensitivity=event_carry_sensitivity,
        active_event_family=active_event_family,
        calendar_closure_classes=calendar_closure_classes or [],
        session_bridge_rules=[],
        recent_path_tag="balanced_recent_path",
        carryover_state="balanced_carryover",
        reasons=["test_temporal"],
    )



def _upstream_outputs(temporal: TemporalContextOutput):
    fixture = supportive_runtime_fixture()
    regime = MarketRegimeContextService().evaluate(fixture.regime_input)
    options = OptionsFlowContextService().evaluate(fixture.options_flow_input)
    posture = PostureRiskService().evaluate(
        PostureRiskInput(
            temporal=temporal,
            regime=regime,
            options_flow=options,
            inventory=fixture.inventory_state,
            risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
        )
    )
    return fixture, regime, options, posture



def test_gate93_playbook_eligibility_distinguishes_macro_window_and_venue_session_distortion() -> None:
    temporal = _temporal_output(
        desk_window="close",
        event_window_state="event_imminent_window",
        event_proximity_state="event_imminent",
        active_event_family="cpi",
        calendar_closure_classes=["half_day"],
    )
    _, regime, options, posture = _upstream_outputs(temporal)

    eligibility = PlaybookEligibilityService().evaluate(
        PlaybookEligibilityInput(
            temporal=temporal,
            regime=regime,
            options_flow=options,
            posture=posture,
        )
    )

    assert "event_window_veto" in eligibility.no_trade_reasons
    assert "macro_event_window_veto" in eligibility.no_trade_reasons
    assert "venue_session_distortion" in eligibility.no_trade_reasons



def test_gate93_modifier_distinguishes_company_expiry_and_venue_session_policies() -> None:
    temporal = _temporal_output(
        desk_window="late_session",
        event_window_state="event_imminent_window",
        event_proximity_state="event_imminent",
        active_event_family="nvda_earnings",
        expiry_cycle_state="expiry_day",
        calendar_closure_classes=["half_day"],
    )
    fixture, regime, options, posture = _upstream_outputs(temporal)

    packet = StateConditionedModifierService().evaluate(
        temporal_input=fixture.temporal_input,
        temporal=temporal,
        regime=regime,
        options_flow=options,
        posture=posture,
    )

    assert "event_options:company_event_window" in packet.active_policy_ids
    assert "event_options:expiry_distortion" in packet.active_policy_ids
    assert "event_options:venue_session_distortion" in packet.active_policy_ids



def test_gate93_review_explanation_uses_temporal_overlap_and_carry_semantics() -> None:
    temporal = _temporal_output(
        desk_window="late_session",
        event_window_state="event_cooling_off_window",
        event_proximity_state="event_live_or_passed",
        active_event_family="nvda_earnings",
        event_risk_timing_class="cooling_off",
        event_carry_sensitivity="next_session_memory",
        event_overlap_class="overlapping_windows",
    )
    fixture, regime, options, posture = _upstream_outputs(temporal)
    eligibility = PlaybookEligibilityService().evaluate(
        PlaybookEligibilityInput(
            temporal=temporal,
            regime=regime,
            options_flow=options,
            posture=posture,
        )
    )
    modifier = StateConditionedModifierService().evaluate(
        temporal_input=fixture.temporal_input,
        temporal=temporal,
        regime=regime,
        options_flow=options,
        posture=posture,
    )

    review = ReviewExplanationService().evaluate(
        ReviewExplanationInput(
            temporal=temporal,
            regime=regime,
            options_flow=options,
            posture=posture,
            eligibility=eligibility,
            execution=_execution_output(["pin_reversion"]),
            modifier_runtime_packet=modifier,
            temporal_input=fixture.temporal_input,
        )
    )

    assert review.event_window_governance is not None
    assert review.event_window_governance.overlap_class.value == "overlapping_windows"
    assert review.event_window_governance.risk_timing_class.value == "cooling_off"
    assert review.event_window_governance.carry_sensitivity.value == "next_session_memory"
    assert review.event_window_governance.event_family == "nvda_earnings"
