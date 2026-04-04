from __future__ import annotations

from datetime import UTC, date, datetime
from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.domain.session_clock import SessionClockPhase
from nvda_desk.schemas.cognition import TemporalContextInput, TemporalContextOutput
from nvda_desk.schemas.dataset import PreparedRuntimeLineage, PreparedRuntimeSnapshot
from nvda_desk.schemas.events import EventQueryWindow, LiveEventReference, LiveEventSnapshot
from nvda_desk.services.carry_handoff import CarryHandoffBuilder
from nvda_desk.services.chain_to_cognition import ChainToCognitionService
from nvda_desk.services.financial_calendar_projection import FinancialCalendarProjectionService
from nvda_desk.services.temporal_context import TemporalContextService
from tests.test_gate48_carry_handoff import (
    _execution_output,
    _inventory_state,
    _options_output,
    _posture_output,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def _prepared_snapshot() -> PreparedRuntimeSnapshot:
    projection = FinancialCalendarProjectionService(REPO_ROOT)
    authority = projection.project_desk_calendar_authority(session_date=date(2026, 11, 27))
    live_snapshot = projection.build_live_event_snapshot(
        requested_at=datetime(2026, 1, 28, 22, 0, tzinfo=UTC),
        symbol="NVDA",
    )
    return PreparedRuntimeSnapshot(
        ts=datetime.fromisoformat("2026-11-27T12:15:00-05:00"),
        symbol="NVDA",
        aligned_bar_ts=datetime.fromisoformat("2026-11-27T12:15:00-05:00"),
        bar_age_seconds=0,
        spot_price=140.0,
        prior_close_price=138.0,
        session_open_price=139.0,
        intraday_move_pct=0.7,
        prior_session_return_pct=1.2,
        front_expiry=datetime.fromisoformat("2026-11-27T16:00:00-05:00"),
        next_expiry=datetime.fromisoformat("2026-12-04T16:00:00-05:00"),
        front_dte=0,
        next_dte=7,
        front_atm_iv=54.0,
        next_atm_iv=51.0,
        put_call_skew=0.12,
        gamma_pressure_score=0.41,
        call_put_imbalance=0.05,
        oi_concentration=0.42,
        atm_straddle_value=6.2,
        live_event_snapshot=live_snapshot,
        next_event_at=live_snapshot.next_event.event_at if live_snapshot.next_event else None,
        desk_calendar_authority=authority,
        lineage=PreparedRuntimeLineage(
            source_name="test",
            source_type="unit",
            captured_at=datetime(2026, 11, 27, 17, 15, tzinfo=UTC),
            chain_ts=datetime(2026, 11, 27, 17, 15, tzinfo=UTC),
            aligned_bar_ts=datetime(2026, 11, 27, 17, 15, tzinfo=UTC),
            bar_age_seconds=0,
        ),
    )



def test_gate92_chain_to_cognition_carries_desk_calendar_authority() -> None:
    snapshot = _prepared_snapshot()
    converted = ChainToCognitionService().convert_snapshot(snapshot)

    assert converted.temporal_input.desk_calendar_authority is not None
    assert any(venue.venue.value == "nasdaq_us" for venue in converted.temporal_input.desk_calendar_authority.venues)



def test_gate92_temporal_context_uses_desk_calendar_authority_for_half_day_and_next_session_hint() -> None:
    service = TemporalContextService(Settings())
    snapshot = _prepared_snapshot()

    result = service.evaluate(
        TemporalContextInput(
            ts=datetime.fromisoformat("2026-11-27T14:15:00-05:00"),
            next_expiry=snapshot.front_expiry,
            live_event_snapshot=snapshot.live_event_snapshot,
            desk_calendar_authority=snapshot.desk_calendar_authority,
            prior_session_return_pct=snapshot.prior_session_return_pct,
            intraday_move_pct=snapshot.intraday_move_pct,
        )
    )

    assert result.session_phase.value == "closed"
    assert result.desk_window == "closed"
    assert "half_day" in result.calendar_closure_classes
    assert result.next_session_open_hint is not None
    assert result.next_session_open_hint.date().isoformat() == "2026-11-30"



def test_gate92_temporal_context_derives_live_and_cooling_off_event_windows_from_rich_packets() -> None:
    projection = FinancialCalendarProjectionService(REPO_ROOT)
    live_snapshot = projection.build_live_event_snapshot(
        requested_at=datetime(2026, 1, 28, 22, 0, tzinfo=UTC),
        symbol="NVDA",
    )
    service = TemporalContextService(Settings())

    live_result = service.evaluate(
        TemporalContextInput(
            ts=datetime(2026, 1, 28, 22, 0, tzinfo=UTC),
            live_event_snapshot=live_snapshot,
        )
    )
    assert live_result.event_window_state == "event_live_window"
    assert live_result.event_risk_timing_class == "live_release"
    assert live_result.event_carry_sensitivity == "carry_sensitive"
    assert live_result.active_event_family == "mega_cap_ai_earnings"

    cooling_result = service.evaluate(
        TemporalContextInput(
            ts=datetime(2026, 1, 29, 14, 0, tzinfo=UTC),
            live_event_snapshot=projection.build_live_event_snapshot(
                requested_at=datetime(2026, 1, 29, 14, 0, tzinfo=UTC),
                symbol="NVDA",
            ),
        )
    )
    assert cooling_result.event_window_state == "event_cooling_off_window"
    assert cooling_result.event_risk_timing_class == "cooling_off"



def test_gate92_compatibility_next_event_hint_stays_subordinate_to_live_snapshot() -> None:
    service = TemporalContextService(Settings())
    live_snapshot = LiveEventSnapshot(
        requested_at=datetime(2026, 3, 23, 18, 15, tzinfo=UTC),
        symbol="NVDA",
        query_window=EventQueryWindow(lookback_minutes=240, lookahead_minutes=1440),
        next_event=LiveEventReference(
            record_id="evt::1",
            event_id="evt-1",
            event_at=datetime(2026, 3, 23, 19, 30, tzinfo=UTC),
            event_type="cpi",
            label="CPI release",
            event_class=None,
            event_subclass="cpi",
            window_start_at=datetime(2026, 3, 23, 19, 30, tzinfo=UTC),
            window_end_at=datetime(2026, 3, 23, 23, 30, tzinfo=UTC),
        ),
        material_events=[],
    )

    result = service.evaluate(
        TemporalContextInput(
            ts=datetime(2026, 3, 23, 18, 15, tzinfo=UTC),
            next_event_at=datetime(2026, 3, 24, 16, 0, tzinfo=UTC),
            live_event_snapshot=live_snapshot,
        )
    )

    assert result.active_event_family == "cpi"
    assert "compatibility_next_event_at_subordinate_to_live_event_snapshot" in result.reasons
    assert result.event_window_state == "event_imminent_window"



def test_gate92_carry_handoff_prefers_temporal_next_session_open_hint() -> None:
    handoff = CarryHandoffBuilder().build(
        symbol="NVDA",
        evaluation_ts=datetime.fromisoformat("2026-09-06T18:00:00-04:00"),
        temporal=TemporalContextOutput(
            session_phase=SessionClockPhase.CLOSED,
            desk_window="closed",
            phase_confidence=1.0,
            expiry_cycle_state="front_week",
            event_proximity_state="event_live_or_passed",
            event_window_state="event_cooling_off_window",
            event_carry_sensitivity="next_session_memory",
            next_session_open_hint=datetime.fromisoformat("2026-09-08T09:30:00-04:00"),
            calendar_closure_classes=["full_holiday"],
            recent_path_tag="balanced_recent_path",
            carryover_state="balanced_carryover",
            reasons=["test"],
        ),
        options_flow=_options_output(),
        posture=_posture_output(),
        inventory=_inventory_state(existing=10.0, overnight=5.0),
        execution=_execution_output(["pin_reversion"]),
    )

    assert handoff.next_session_open_ts is not None
    assert handoff.next_session_open_ts.date().isoformat() == "2026-09-08"
    assert handoff.event_carry_window is True
    assert any(code.startswith("calendar_closure:") for code in handoff.rationale_codes)
