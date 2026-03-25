from __future__ import annotations

from datetime import UTC, date, datetime

from sqlalchemy import asc, desc, select
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, sessionmaker

from nvda_desk.config import Settings
from nvda_desk.db.models import Bar1m, Instrument, OptionSnapshot
from nvda_desk.domain.session_clock import SessionClockClassifier
from nvda_desk.domain.temporal_state import TemporalSignalInput, TemporalStateClassifier
from nvda_desk.schemas.market import Bar1mPayload, IntradayBarsResponse, MarketSnapshotResponse
from nvda_desk.schemas.options import OptionSnapshotPayload, OptionSurfaceResponse, OptionType
from nvda_desk.schemas.session_clock import SessionClockFeaturePayload
from nvda_desk.schemas.temporal_surface import (
    SessionClockCompatibilityPayload,
    TemporalStateFeaturePayload,
)


class MarketStateService:
    def __init__(
        self,
        classifier: SessionClockClassifier,
        session_factory: sessionmaker[Session] | None = None,
        settings: Settings | None = None,
    ):
        self._classifier = classifier
        self._session_factory = session_factory
        self._temporal_classifier = TemporalStateClassifier(settings or Settings())

    def get_session_clock(self, ts: datetime) -> SessionClockFeaturePayload:
        state = self._classifier.classify(ts)
        return SessionClockCompatibilityPayload.from_state(state)

    def get_temporal_state(self, ts: datetime) -> TemporalStateFeaturePayload:
        return TemporalStateFeaturePayload.from_state(self._temporal_classifier.classify(TemporalSignalInput(ts=ts)))

    def get_market_snapshot(self, symbol: str, ts: datetime) -> MarketSnapshotResponse:
        latest_bar = self._get_latest_bar(symbol=symbol, ts=ts)
        return MarketSnapshotResponse(
            symbol=symbol,
            requested_at=ts,
            temporal_state=self.get_temporal_state(ts),
            session_clock=self.get_session_clock(ts),
            latest_bar=latest_bar,
        )

    def get_intraday_bars(self, symbol: str, ts: datetime, limit: int = 30) -> IntradayBarsResponse:
        bars = self._get_intraday_bars(symbol=symbol, ts=ts, limit=limit)
        return IntradayBarsResponse(symbol=symbol, requested_at=ts, bars=bars)

    def get_option_surface(
        self,
        *,
        symbol: str,
        as_of_date: date,
        requested_at: datetime,
        expiry: date | None = None,
        option_type: OptionType | None = None,
    ) -> OptionSurfaceResponse:
        snapshots = self._get_option_surface(
            symbol=symbol,
            as_of_date=as_of_date,
            expiry=expiry,
            option_type=option_type,
        )
        surface_expiry = expiry or (snapshots[0].expiry if snapshots else None)
        return OptionSurfaceResponse(
            symbol=symbol,
            requested_at=requested_at,
            as_of_date=as_of_date,
            expiry=surface_expiry,
            option_type=option_type,
            snapshots=snapshots,
        )

    def _get_latest_bar(self, symbol: str, ts: datetime) -> Bar1mPayload | None:
        bars = self._get_intraday_bars(symbol=symbol, ts=ts, limit=1)
        return bars[0] if bars else None

    def _get_intraday_bars(self, symbol: str, ts: datetime, limit: int) -> list[Bar1mPayload]:
        if self._session_factory is None:
            return []
        try:
            with self._session_factory() as session:
                stmt = (
                    select(Bar1m)
                    .join(Instrument)
                    .where(Instrument.symbol == symbol)
                    .where(Bar1m.ts_utc <= ts)
                    .order_by(desc(Bar1m.ts_utc))
                    .limit(limit)
                )
                rows = list(session.scalars(stmt))
        except OperationalError:
            return []
        rows.reverse()
        return [
            Bar1mPayload(
                ts_utc=row.ts_utc if row.ts_utc.tzinfo is not None else row.ts_utc.replace(tzinfo=UTC),
                open=row.open,
                high=row.high,
                low=row.low,
                close=row.close,
                volume=row.volume,
            )
            for row in rows
        ]

    def _get_option_surface(
        self,
        *,
        symbol: str,
        as_of_date: date,
        expiry: date | None,
        option_type: OptionType | None,
    ) -> list[OptionSnapshotPayload]:
        if self._session_factory is None:
            return []
        try:
            with self._session_factory() as session:
                instrument = session.scalar(select(Instrument).where(Instrument.symbol == symbol))
                if instrument is None:
                    return []
                chosen_expiry = expiry or self._infer_expiry(session, instrument.id, as_of_date)
                if chosen_expiry is None:
                    return []
                stmt = (
                    select(OptionSnapshot)
                    .where(OptionSnapshot.instrument_id == instrument.id)
                    .where(OptionSnapshot.as_of_date == as_of_date)
                    .where(OptionSnapshot.expiry == chosen_expiry)
                )
                if option_type is not None:
                    stmt = stmt.where(OptionSnapshot.option_type == option_type.value)
                rows = list(session.scalars(stmt.order_by(asc(OptionSnapshot.strike))))
        except OperationalError:
            return []
        return [self._to_option_payload(row) for row in rows]

    def _infer_expiry(self, session: Session, instrument_id: int, as_of_date: date) -> date | None:
        stmt = (
            select(OptionSnapshot.expiry)
            .where(OptionSnapshot.instrument_id == instrument_id)
            .where(OptionSnapshot.as_of_date == as_of_date)
            .where(OptionSnapshot.expiry.is_not(None))
            .order_by(asc(OptionSnapshot.expiry))
            .limit(1)
        )
        return session.scalar(stmt)

    def _to_option_payload(self, row: OptionSnapshot) -> OptionSnapshotPayload:
        return OptionSnapshotPayload(
            as_of_date=row.as_of_date,
            expiry=row.expiry,
            option_type=OptionType(row.option_type),
            strike=row.strike,
            bid=row.bid,
            ask=row.ask,
            last=row.last,
            volume=row.volume,
            open_interest=row.open_interest,
            delta_change=row.delta_change,
            provenance=row.provenance,
            confidence=row.confidence,
            source_document=row.source_document,
            source_pages=row.source_pages,
        )
