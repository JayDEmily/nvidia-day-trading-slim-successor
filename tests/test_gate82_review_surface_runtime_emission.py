"""Gate 82 runtime posture-law review surface emission checks."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, cast

from nvda_desk.config import Settings
from nvda_desk.schemas.events import (
    DeskEventClass,
    EventMaterialityTier,
    EventQueryWindow,
    EventSemanticPhase,
    LiveEventReference,
    LiveEventSnapshot,
)
from nvda_desk.schemas.market import (
    DerivedPrecursorField,
    PrecursorContradictionClass,
    PrecursorFallbackDisposition,
    PrecursorPostureState,
    PrecursorRuntimePacket,
    PrecursorVenueUniverse,
)
from nvda_desk.schemas.risk import (
    CarryHorizonState,
    DayPhaseState,
    PhaseBehaviourClass,
    PhaseNoActionBias,
)
from nvda_desk.schemas.state_policy import (
    EventOptionsBehaviourClass,
    EventOptionsStressState,
)
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.services.state_conditioned_modifier import (
    project_carry_horizon_state,
    project_day_phase_state,
    project_event_option_state_labels,
)
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture


def _live_event_snapshot() -> LiveEventSnapshot:
    return LiveEventSnapshot(
        requested_at=datetime(2026, 3, 23, 14, 15, tzinfo=UTC),
        symbol="NVDA",
        query_window=EventQueryWindow(lookback_minutes=240, lookahead_minutes=1440),
        next_event=LiveEventReference(
            record_id="evt::1",
            event_id="evt-1",
            event_at=datetime(2026, 3, 23, 15, 30, tzinfo=UTC),
            event_type="macro",
            label="Fed speaker",
            event_class=DeskEventClass.MACRO,
            semantic_phase=EventSemanticPhase.PRICED_RISK,
            materiality_tier=EventMaterialityTier.POSTURE_RELEVANT,
            provenance_count=1,
            lineage_keys=["src:macro:evt-1"],
        ),
        nearby_events=[],
        material_events=[],
        lineage_keys=["src:macro:evt-1"],
    )


def _precursor_packet() -> PrecursorRuntimePacket:
    return PrecursorRuntimePacket(
        requested_at=datetime(2026, 3, 23, 14, 2, tzinfo=UTC),
        stitched_order=[PrecursorVenueUniverse.JPX_CASH_INDEX_COMPLEX],
        active_venues=[PrecursorVenueUniverse.JPX_CASH_INDEX_COMPLEX],
        missing_venues=[PrecursorVenueUniverse.HKEX_CASH_INDEX_COMPLEX],
        derived_fields=[DerivedPrecursorField.DIRECTIONAL_COMPOSITE_SCORE],
        contradiction_class=PrecursorContradictionClass.NONE,
        posture_state=PrecursorPostureState.NORMAL_CONFIDENCE,
        fallback_dispositions=[PrecursorFallbackDisposition.CONTINUE_NORMALLY],
        lineage_keys=["precursor:jpx:1"],
    )


def test_gate82_runtime_emits_phase_and_event_options_policy_surfaces() -> None:
    fixture = supportive_runtime_fixture()
    result = DeskCognitionRuntime(Settings()).run(
        temporal_input=fixture.temporal_input.model_copy(
            update={
                "live_event_snapshot": _live_event_snapshot(),
                "precursor_runtime_packet": _precursor_packet(),
            }
        ),
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )

    assert result.review.phase_carry_policy is not None
    assert (
        result.review.phase_carry_policy.day_phase_state is DayPhaseState.TREND_WINDOW
    )
    assert (
        result.review.phase_carry_policy.carry_horizon_state
        is CarryHorizonState.INTRADAY_ONLY
    )
    assert (
        result.review.phase_carry_policy.behaviour_class
        is PhaseBehaviourClass.NORMAL_OPERATION
    )
    assert result.review.phase_carry_policy.no_action_bias is PhaseNoActionBias.NEUTRAL

    assert result.review.event_options_stress_policy is not None
    assert (
        result.review.event_options_stress_policy.behaviour_class
        is EventOptionsBehaviourClass.HARD_BLOCK
    )
    assert result.review.event_options_stress_policy.hard_block is True
    assert (
        EventOptionsStressState.EVENT_LIVE
        in result.review.event_options_stress_policy.active_states
    )
    assert result.review.event_options_stress_policy.active_states == [
        EventOptionsStressState.EVENT_LIVE
    ]

    assert result.review.modifier_control_law is not None
    assert result.review.modifier_control_law.triggered_kill_switch is not None
    review_packet = cast(dict[str, Any], result.review.review_packet)
    phase_packet = cast(dict[str, Any], review_packet["phase_carry_policy"])
    event_packet = cast(dict[str, Any], review_packet["event_options_stress_policy"])
    assert phase_packet["carry_horizon_state"] == "intraday_only"
    assert event_packet["hard_block"] is True


def test_gate82_review_surfaces_use_the_same_phase_carry_and_event_state_projectors_as_runtime() -> (
    None
):
    fixture = supportive_runtime_fixture()
    result = DeskCognitionRuntime(Settings()).run(
        temporal_input=fixture.temporal_input.model_copy(
            update={
                "live_event_snapshot": _live_event_snapshot(),
                "precursor_runtime_packet": _precursor_packet(),
            }
        ),
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )

    assert result.review.phase_carry_policy is not None
    assert result.review.event_options_stress_policy is not None
    assert result.review.phase_carry_policy.day_phase_state is project_day_phase_state(
        result.temporal
    )
    assert (
        result.review.phase_carry_policy.carry_horizon_state
        is project_carry_horizon_state(result.temporal)
    )
    projected_labels = project_event_option_state_labels(
        result.temporal, result.options_flow
    )
    assert {
        state.value for state in result.review.event_options_stress_policy.active_states
    } == {
        {
            "event_imminent": EventOptionsStressState.EVENT_IMMINENT.value,
            "event_live": EventOptionsStressState.EVENT_LIVE.value,
            "event_suppressed": EventOptionsStressState.EVENT_SUPPRESSED.value,
            "negative_gamma_stress": EventOptionsStressState.NEGATIVE_GAMMA_STRESS.value,
            "pin_risk": EventOptionsStressState.PIN_RISK.value,
            "expiry_distortion": EventOptionsStressState.EXPIRY_DISTORTION.value,
        }[label]
        for label in projected_labels
    }
