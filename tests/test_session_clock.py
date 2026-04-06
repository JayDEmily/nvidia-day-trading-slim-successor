from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from nvda_desk.config import Settings
from nvda_desk.domain.session_clock import SessionClockClassifier, SessionClockPhase

REPO_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_LEDGER = (
    REPO_ROOT / "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md"
)


@pytest.fixture()
def classifier() -> SessionClockClassifier:
    return SessionClockClassifier(Settings())


def test_pre_market(classifier: SessionClockClassifier) -> None:
    ts = datetime(2026, 3, 18, 12, 0, tzinfo=UTC)  # 08:00 NY (DST)
    state = classifier.classify(ts)
    assert state.phase == SessionClockPhase.PRE_MARKET
    assert state.is_pre_market is True


def test_open_disorder(classifier: SessionClockClassifier) -> None:
    ts = datetime(2026, 3, 18, 13, 35, tzinfo=UTC)  # 09:35 NY
    state = classifier.classify(ts)
    assert state.phase == SessionClockPhase.OPEN_DISORDER
    assert state.minutes_since_open == 5


def test_power_hour(classifier: SessionClockClassifier) -> None:
    ts = datetime(2026, 3, 18, 19, 15, tzinfo=UTC)  # 15:15 NY
    state = classifier.classify(ts)
    assert state.phase == SessionClockPhase.POWER_HOUR
    assert state.is_power_hour is True
    assert state.minutes_to_close == 45


def test_dealer_unwind_close(classifier: SessionClockClassifier) -> None:
    ts = datetime(2026, 3, 18, 19, 45, tzinfo=UTC)  # 15:45 NY
    state = classifier.classify(ts)
    assert state.phase == SessionClockPhase.DEALER_UNWIND_CLOSE


def test_after_hours(classifier: SessionClockClassifier) -> None:
    ts = datetime(2026, 3, 18, 21, 30, tzinfo=UTC)  # 17:30 NY
    state = classifier.classify(ts)
    assert state.phase == SessionClockPhase.AFTER_HOURS


def test_closed(classifier: SessionClockClassifier) -> None:
    ts = datetime(2026, 3, 18, 2, 0, tzinfo=UTC)  # 22:00 previous NY date
    state = classifier.classify(ts)
    assert state.phase == SessionClockPhase.CLOSED


def test_session_clock_wrapper_authority_is_successor_native() -> None:
    runtime_ledger = RUNTIME_LEDGER.read_text(encoding="utf-8")

    assert "### 4.5 Session Clock compatibility wrapper" in runtime_ledger
    assert "compatibility wrapper retained over `temporal_state`" in runtime_ledger
    assert "**Allowed downstream readers:** `/market/session-clock`, compatibility tests, legacy temporal consumers that still require the wrapper shape" in runtime_ledger
    assert "session_clock` must not be described or treated as canonical Step-1 truth" in runtime_ledger
