from __future__ import annotations

from datetime import UTC, datetime

from nvda_desk.config import Settings
from nvda_desk.domain.session_clock import SessionClockClassifier
from nvda_desk.services.market_state import MarketStateService


def test_market_state_exposes_temporal_state_and_session_clock_wrapper() -> None:
    """Gate 49 should keep session_clock as an explicit wrapper over temporal_state."""

    service = MarketStateService(SessionClockClassifier(Settings()))
    ts = datetime(2026, 3, 18, 13, 35, tzinfo=UTC)

    temporal_state = service.get_temporal_state(ts)
    session_clock = service.get_session_clock(ts)

    assert temporal_state.phase == session_clock.phase.value
    assert temporal_state.compatibility_policy == "session_clock_wrapper_retained"
    assert session_clock.compatibility_policy == "legacy_wrapper_over_temporal_state"
