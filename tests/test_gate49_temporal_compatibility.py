from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.domain.session_clock import SessionClockClassifier
from nvda_desk.services.market_state import MarketStateService

REPO_ROOT = Path(__file__).resolve().parents[1]
DOMAIN_MODEL = REPO_ROOT / "docs/03_DOMAIN_MODEL.md"
RUNTIME_LEDGER = (
    REPO_ROOT / "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md"
)


def test_market_state_exposes_temporal_state_and_session_clock_wrapper() -> None:
    """Gate 49 keeps session_clock as a compatibility wrapper under successor doctrine."""

    service = MarketStateService(SessionClockClassifier(Settings()))
    ts = datetime(2026, 3, 18, 13, 35, tzinfo=UTC)

    domain_model = DOMAIN_MODEL.read_text(encoding="utf-8")
    runtime_ledger = RUNTIME_LEDGER.read_text(encoding="utf-8")

    temporal_state = service.get_temporal_state(ts)
    session_clock = service.get_session_clock(ts)

    assert "TemporalContextInput" in domain_model
    assert "TemporalContextOutput" in domain_model
    assert "Session Clock compatibility wrapper" in runtime_ledger
    assert "**Governing authoritative surface:** `TemporalStateFeaturePayload`" in runtime_ledger
    assert "compatibility wrapper retained over `temporal_state`" in runtime_ledger
    assert temporal_state.phase == session_clock.phase.value
    assert temporal_state.compatibility_policy == "session_clock_wrapper_retained"
    assert session_clock.compatibility_policy == "legacy_wrapper_over_temporal_state"
