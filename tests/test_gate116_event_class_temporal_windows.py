from __future__ import annotations

from datetime import UTC, date, datetime
from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.schemas.cognition import TemporalContextInput
from nvda_desk.schemas.events import (
    DeskEventClass,
    EventMaterialityTier,
    EventQueryWindow,
    EventSemanticPhase,
    LiveEventReference,
    LiveEventSnapshot,
)
from nvda_desk.schemas.session_clock import (
    DeskCalendarAuthorityPacket,
    SessionTemplate,
    TradingVenue,
    VenueSessionContract,
    VenueTimezone,
)
from nvda_desk.services.financial_calendar_projection import FinancialCalendarProjectionService
from nvda_desk.services.temporal_context import TemporalContextService

REPO_ROOT = Path(__file__).resolve().parents[1]


def _snapshot(reference: LiveEventReference, *, requested_at: datetime) -> LiveEventSnapshot:
    return LiveEventSnapshot(
        requested_at=requested_at,
        symbol="NVDA",
        query_window=EventQueryWindow(lookback_minutes=240, lookahead_minutes=2880),
        next_event=reference,
        nearby_events=[reference],
        material_events=[reference],
        lineage_keys=["src:test:event"],
    )


def test_gate116_projection_service_populates_future_trading_days() -> None:
    authority = FinancialCalendarProjectionService(REPO_ROOT).project_desk_calendar_authority(
        session_date=date(2026, 11, 27)
    )
    nasdaq = next(contract for contract in authority.venues if contract.venue is TradingVenue.NASDAQ_US)

    assert nasdaq.trading_days[0] == "2026-11-27"
    assert nasdaq.trading_days[1] == "2026-11-30"
    assert len(nasdaq.trading_days) >= 5


def test_gate116_next_session_open_hint_uses_calendar_trading_days() -> None:
    service = TemporalContextService(Settings())
    authority = DeskCalendarAuthorityPacket(
        venues=[
            VenueSessionContract(
                venue=TradingVenue.NASDAQ_US,
                timezone=VenueTimezone.AMERICA_NEW_YORK,
                template=SessionTemplate.US_EQUITY_CONTINUOUS,
                trading_days=["2026-12-24", "2026-12-29"],
            )
        ]
    )

    result = service.evaluate(
        TemporalContextInput(
            ts=datetime.fromisoformat("2026-12-24T15:30:00-05:00"),
            desk_calendar_authority=authority,
        )
    )

    assert result.next_session_open_hint is not None
    assert result.next_session_open_hint.date().isoformat() == "2026-12-29"


def test_gate116_company_events_keep_longer_pre_event_window_than_macro() -> None:
    service = TemporalContextService(Settings())
    requested_at = datetime(2026, 1, 28, 14, 0, tzinfo=UTC)
    company_event = LiveEventReference(
        record_id="evt::company",
        event_id="evt-company",
        event_at=datetime(2026, 1, 29, 0, 0, tzinfo=UTC),
        event_type="earnings",
        label="NVDA earnings",
        event_class=DeskEventClass.COMPANY,
        event_subclass="nvda_earnings",
        semantic_phase=EventSemanticPhase.PRICED_RISK,
        materiality_tier=EventMaterialityTier.DESK_CRITICAL,
    )
    macro_event = LiveEventReference(
        record_id="evt::macro",
        event_id="evt-macro",
        event_at=datetime(2026, 1, 29, 0, 0, tzinfo=UTC),
        event_type="cpi",
        label="CPI",
        event_class=DeskEventClass.MACRO,
        event_subclass="cpi",
        semantic_phase=EventSemanticPhase.PRICED_RISK,
        materiality_tier=EventMaterialityTier.DESK_CRITICAL,
    )

    company_result = service.evaluate(
        TemporalContextInput(
            ts=requested_at,
            live_event_snapshot=_snapshot(company_event, requested_at=requested_at),
        )
    )
    macro_result = service.evaluate(
        TemporalContextInput(
            ts=requested_at,
            live_event_snapshot=_snapshot(macro_event, requested_at=requested_at),
        )
    )

    assert company_result.event_window_state == "same_session_event_window"
    assert company_result.event_timing_profile == "company_like:nvda_earnings"
    assert macro_result.event_window_state == "clear_window"
    assert macro_result.event_timing_profile == "macro_like:cpi"


def test_gate116_company_event_cooling_window_outlasts_macro_release() -> None:
    service = TemporalContextService(Settings())
    requested_at = datetime(2026, 1, 29, 4, 0, tzinfo=UTC)
    company_event = LiveEventReference(
        record_id="evt::company",
        event_id="evt-company",
        event_at=datetime(2026, 1, 28, 20, 0, tzinfo=UTC),
        event_type="earnings",
        label="NVDA earnings",
        event_class=DeskEventClass.COMPANY,
        event_subclass="nvda_earnings",
        semantic_phase=EventSemanticPhase.PRICED_RISK,
        materiality_tier=EventMaterialityTier.DESK_CRITICAL,
        window_start_at=datetime(2026, 1, 28, 20, 0, tzinfo=UTC),
        window_end_at=datetime(2026, 1, 28, 22, 0, tzinfo=UTC),
    )
    macro_event = LiveEventReference(
        record_id="evt::macro",
        event_id="evt-macro",
        event_at=datetime(2026, 1, 28, 20, 0, tzinfo=UTC),
        event_type="cpi",
        label="CPI",
        event_class=DeskEventClass.MACRO,
        event_subclass="cpi",
        semantic_phase=EventSemanticPhase.PRICED_RISK,
        materiality_tier=EventMaterialityTier.DESK_CRITICAL,
        window_start_at=datetime(2026, 1, 28, 20, 0, tzinfo=UTC),
        window_end_at=datetime(2026, 1, 28, 22, 0, tzinfo=UTC),
    )

    company_result = service.evaluate(
        TemporalContextInput(
            ts=requested_at,
            live_event_snapshot=_snapshot(company_event, requested_at=requested_at),
        )
    )
    macro_result = service.evaluate(
        TemporalContextInput(
            ts=requested_at,
            live_event_snapshot=_snapshot(macro_event, requested_at=requested_at),
        )
    )

    assert company_result.event_window_state == "event_cooling_off_window"
    assert macro_result.event_window_state == "event_memory_window"
