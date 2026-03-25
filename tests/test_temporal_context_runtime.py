"""Gate D tests for temporal desk-window logic."""

from __future__ import annotations

from datetime import datetime

from nvda_desk.config import Settings
from nvda_desk.schemas.cognition import TemporalContextInput
from nvda_desk.services.temporal_context import TemporalContextService


def test_temporal_context_maps_mid_morning_post_expiry_reset_and_carryover() -> None:
    """Gate D should expose explicit desk windows, post-expiry reset, and carryover."""

    service = TemporalContextService(Settings())
    result = service.evaluate(
        TemporalContextInput(
            ts=datetime.fromisoformat("2026-03-30T11:15:00-04:00"),
            next_expiry=datetime.fromisoformat("2026-04-03T16:00:00-04:00"),
            prior_session_return_pct=1.4,
            intraday_move_pct=0.9,
        )
    )
    assert result.session_phase.value == "institutional_repricing"
    assert result.desk_window == "mid_morning"
    assert result.expiry_cycle_state == "post_expiry_reset"
    assert result.carryover_state == "upside_carryover_follow_through"


def test_temporal_context_exposes_expiry_day_and_imminent_event_window() -> None:
    """Gate D should make expiry-day and event veto windows explicit."""

    service = TemporalContextService(Settings())
    result = service.evaluate(
        TemporalContextInput(
            ts=datetime.fromisoformat("2026-03-27T15:20:00-04:00"),
            next_expiry=datetime.fromisoformat("2026-03-27T16:00:00-04:00"),
            next_event_at=datetime.fromisoformat("2026-03-27T15:45:00-04:00"),
            prior_session_return_pct=-0.4,
            intraday_move_pct=0.2,
        )
    )
    assert result.desk_window == "late_session"
    assert result.expiry_cycle_state == "expiry_day"
    assert result.event_proximity_state == "event_imminent"
    assert result.event_window_state == "event_imminent_window"


def test_temporal_context_marks_downside_carryover_reversal() -> None:
    """Gate D prior-session carryover should distinguish reversal from follow-through."""

    service = TemporalContextService(Settings())
    result = service.evaluate(
        TemporalContextInput(
            ts=datetime.fromisoformat("2026-03-24T14:15:00-04:00"),
            next_expiry=datetime.fromisoformat("2026-03-27T16:00:00-04:00"),
            prior_session_return_pct=-2.2,
            intraday_move_pct=1.1,
        )
    )
    assert result.desk_window == "trend_window"
    assert result.recent_path_tag == "prior_session_damage"
    assert result.carryover_state == "downside_carryover_reversal"
