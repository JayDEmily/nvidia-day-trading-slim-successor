from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.domain.session_clock import SessionClockClassifier
from nvda_desk.schemas.market import (
    DerivedPrecursorField,
    PrecursorContradictionClass,
    PrecursorFreshnessState,
    PrecursorPostureState,
    PrecursorSourceClass,
    PrecursorStitchingAuthorityPacket,
    PrecursorTimestampDiscipline,
    PrecursorVenueSlice,
    PrecursorVenueUniverse,
    RawPrecursorField,
)
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.services.financial_calendar_projection import FinancialCalendarProjectionService
from nvda_desk.services.market_state import MarketStateService
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture

REPO_ROOT = Path(__file__).resolve().parents[1]


def _authority() -> PrecursorStitchingAuthorityPacket:
    return PrecursorStitchingAuthorityPacket(
        venue_order=list(PrecursorVenueUniverse),
        timestamp_disciplines=list(PrecursorTimestampDiscipline),
    )


def _service() -> MarketStateService:
    return MarketStateService(classifier=SessionClockClassifier(Settings()))


def _slice(
    venue: PrecursorVenueUniverse,
    *,
    directional: float,
    pressure: float,
    divergence: float = 0.0,
    warning: float = 0.0,
    freshness: PrecursorFreshnessState = PrecursorFreshnessState.CURRENT,
) -> PrecursorVenueSlice:
    close_hour = {
        PrecursorVenueUniverse.JPX_CASH_INDEX_COMPLEX: 6,
        PrecursorVenueUniverse.HKEX_CASH_INDEX_COMPLEX: 8,
        PrecursorVenueUniverse.MAINLAND_CHINA_CASH_INDEX_COMPLEX: 7,
        PrecursorVenueUniverse.CFFEX_INDEX_FUTURES_COMPLEX: 7,
    }[venue]
    requested = datetime(2026, 3, 23, 14, 0, tzinfo=UTC)
    close_at = requested.replace(hour=close_hour, minute=0)
    source_class = (
        PrecursorSourceClass.INDEX_FUTURES
        if venue is PrecursorVenueUniverse.CFFEX_INDEX_FUTURES_COMPLEX
        else PrecursorSourceClass.CASH_EQUITY_INDEX
    )
    return PrecursorVenueSlice(
        venue=venue,
        source_class=source_class,
        session_close_at=close_at,
        observed_at=close_at.replace(minute=5),
        freshness_state=freshness,
        raw_values={RawPrecursorField.CLOSE_TIMESTAMP: close_at},
        derived_values={
            DerivedPrecursorField.DIRECTIONAL_COMPOSITE_SCORE: directional,
            DerivedPrecursorField.CROSS_VENUE_AGREEMENT_SCORE: 0.8,
            DerivedPrecursorField.FUTURES_CASH_DIVERGENCE_SCORE: divergence,
            DerivedPrecursorField.IMPULSE_PERSISTENCE_SCORE: 0.3,
            DerivedPrecursorField.PRECURSOR_PRESSURE_SCORE: pressure,
            DerivedPrecursorField.CARRY_RISK_WARNING_SCORE: warning,
        },
        lineage_keys=[f"precursor:{venue.value}:1"],
    )


def test_gate117_market_state_aggregates_precursor_economics_into_runtime_packet() -> None:
    service = _service()
    result = service.stitch_precursor_context(
        requested_at=datetime(2026, 3, 23, 14, 0, tzinfo=UTC),
        authority=_authority(),
        slices=[
            _slice(PrecursorVenueUniverse.JPX_CASH_INDEX_COMPLEX, directional=0.4, pressure=0.2),
            _slice(PrecursorVenueUniverse.HKEX_CASH_INDEX_COMPLEX, directional=0.2, pressure=0.1),
            _slice(PrecursorVenueUniverse.CFFEX_INDEX_FUTURES_COMPLEX, directional=0.3, pressure=0.15),
        ],
    )
    packet = service.to_precursor_runtime_packet(result)

    assert packet.raw_fields == [RawPrecursorField.CLOSE_TIMESTAMP]
    assert packet.derived_values[DerivedPrecursorField.DIRECTIONAL_COMPOSITE_SCORE] == 0.3
    assert packet.derived_values[DerivedPrecursorField.PRECURSOR_PRESSURE_SCORE] == 0.15
    assert packet.contradiction_class is PrecursorContradictionClass.NONE
    assert packet.posture_state is PrecursorPostureState.DEGRADED_CONFIDENCE


def test_gate117_calendar_projection_routes_precursor_packet_through_market_state_path() -> None:
    service = FinancialCalendarProjectionService(REPO_ROOT)
    packet = service.project_precursor_runtime_packet(
        requested_at=datetime(2026, 1, 1, 6, 0, tzinfo=UTC)
    )

    assert packet.active_venues == [PrecursorVenueUniverse.CFFEX_INDEX_FUTURES_COMPLEX]
    assert packet.missing_venues == [
        PrecursorVenueUniverse.JPX_CASH_INDEX_COMPLEX,
        PrecursorVenueUniverse.HKEX_CASH_INDEX_COMPLEX,
        PrecursorVenueUniverse.MAINLAND_CHINA_CASH_INDEX_COMPLEX,
    ]
    assert packet.contradiction_class is PrecursorContradictionClass.FUTURES_CASH_DIVERGENCE
    assert packet.posture_state is PrecursorPostureState.STAND_DOWN_PRESSURE
    assert packet.derived_values[DerivedPrecursorField.FUTURES_CASH_DIVERGENCE_SCORE] == 0.8
    assert "futures_cash_divergence_from_calendar_projection" in packet.notes


def test_gate117_supportive_hostile_and_contradictory_precursors_change_runtime_outcomes() -> None:
    service = _service()
    fixture = supportive_runtime_fixture()
    runtime = DeskCognitionRuntime(Settings())

    supportive_packet = service.to_precursor_runtime_packet(
        service.stitch_precursor_context(
            requested_at=datetime(2026, 3, 23, 14, 0, tzinfo=UTC),
            authority=_authority(),
            slices=[
                _slice(PrecursorVenueUniverse.JPX_CASH_INDEX_COMPLEX, directional=0.4, pressure=0.2),
                _slice(PrecursorVenueUniverse.HKEX_CASH_INDEX_COMPLEX, directional=0.3, pressure=0.15),
                _slice(PrecursorVenueUniverse.MAINLAND_CHINA_CASH_INDEX_COMPLEX, directional=0.25, pressure=0.1),
                _slice(PrecursorVenueUniverse.CFFEX_INDEX_FUTURES_COMPLEX, directional=0.35, pressure=0.2),
            ],
        )
    )
    contradictory_packet = service.to_precursor_runtime_packet(
        service.stitch_precursor_context(
            requested_at=datetime(2026, 3, 23, 14, 0, tzinfo=UTC),
            authority=_authority(),
            slices=[
                _slice(PrecursorVenueUniverse.JPX_CASH_INDEX_COMPLEX, directional=0.4, pressure=0.2),
                _slice(PrecursorVenueUniverse.HKEX_CASH_INDEX_COMPLEX, directional=0.3, pressure=0.15),
                _slice(PrecursorVenueUniverse.CFFEX_INDEX_FUTURES_COMPLEX, directional=-0.5, pressure=-0.25),
            ],
        )
    )
    hostile_packet = service.to_precursor_runtime_packet(
        service.stitch_precursor_context(
            requested_at=datetime(2026, 3, 23, 14, 0, tzinfo=UTC),
            authority=_authority(),
            slices=[
                _slice(
                    PrecursorVenueUniverse.CFFEX_INDEX_FUTURES_COMPLEX,
                    directional=0.35,
                    pressure=-0.65,
                    divergence=0.8,
                    warning=0.8,
                ),
            ],
        )
    )

    supportive = runtime.run(
        temporal_input=fixture.temporal_input.model_copy(
            update={"precursor_runtime_packet": supportive_packet}
        ),
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )
    contradictory = runtime.run(
        temporal_input=fixture.temporal_input.model_copy(
            update={"precursor_runtime_packet": contradictory_packet}
        ),
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )
    hostile = runtime.run(
        temporal_input=fixture.temporal_input.model_copy(
            update={"precursor_runtime_packet": hostile_packet}
        ),
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )

    assert supportive.posture.permission_state.value in {"allow", "derisk"}
    assert contradictory.execution.target_fresh_deployable_pct < supportive.execution.target_fresh_deployable_pct
    assert hostile.posture.permission_state.value == "block"
    assert hostile.review.precursor_runtime_binding is not None
    assert hostile.review.precursor_runtime_binding.derived_values[
        DerivedPrecursorField.FUTURES_CASH_DIVERGENCE_SCORE
    ] == 0.8
