from __future__ import annotations

from collections.abc import Sequence
from datetime import UTC, datetime, timedelta

from nvda_desk.schemas.events import (
    EventMaterialityTier,
    EventQueryWindow,
    EventStoreQueryResult,
    NormalisedEventRecord,
    ReplayEventConsumerMode,
)


class EventStoreService:
    """Shared event truth service for runtime, review, and replay consumers.

    Purpose:
        Provide one bounded store/query surface over normalised event truth so
        runtime, review, and replay use identical nearby-event semantics.
    Inputs:
        Sequences of `NormalisedEventRecord` objects produced by the Gate 72
        ingestion layer.
    Outputs:
        `EventStoreQueryResult` objects carrying nearby events, material events,
        and lineage maps for the requested consumer mode.
    Determinism:
        Applies stable query windows and explicit materiality filtering without
        hidden source-specific shortcuts.
    """

    def __init__(self, records: Sequence[NormalisedEventRecord]):
        self._records = sorted(records, key=lambda record: (record.event_at, record.record_id))

    def query(
        self,
        *,
        requested_at: datetime,
        symbol: str | None = None,
        query_window: EventQueryWindow | None = None,
        minimum_materiality: EventMaterialityTier = EventMaterialityTier.POSTURE_RELEVANT,
        replay_mode: ReplayEventConsumerMode = ReplayEventConsumerMode.RUNTIME_NEARBY,
    ) -> EventStoreQueryResult:
        window = query_window or EventQueryWindow(lookback_minutes=240, lookahead_minutes=1440)
        lower = self._aware(requested_at) - timedelta(minutes=window.lookback_minutes)
        upper = self._aware(requested_at) + timedelta(minutes=window.lookahead_minutes)
        nearby = [
            record
            for record in self._records
            if lower <= self._aware(record.event_at) <= upper and self._symbol_matches(record.symbol, symbol)
        ]
        material = [record for record in nearby if self._materiality_rank(record.materiality_tier) >= self._materiality_rank(minimum_materiality)]
        lineage_map = {record.record_id: list(record.lineage_keys) for record in nearby}
        return EventStoreQueryResult(
            requested_at=self._aware(requested_at),
            symbol=symbol,
            query_window=window,
            nearby_events=nearby,
            material_events=material,
            lineage_map=lineage_map,
            replay_mode=replay_mode,
        )

    def lineage_for(self, record_id: str) -> list[str]:
        for record in self._records:
            if record.record_id == record_id:
                return list(record.lineage_keys)
        return []

    def _materiality_rank(self, tier: EventMaterialityTier) -> int:
        ordering = {
            EventMaterialityTier.BACKGROUND: 0,
            EventMaterialityTier.MONITOR: 1,
            EventMaterialityTier.POSTURE_RELEVANT: 2,
            EventMaterialityTier.DESK_CRITICAL: 3,
        }
        return ordering[tier]

    def _symbol_matches(self, record_symbol: str | None, requested_symbol: str | None) -> bool:
        return requested_symbol is None or record_symbol in {None, requested_symbol}

    def _aware(self, ts: datetime) -> datetime:
        return ts.astimezone(UTC) if ts.tzinfo is not None else ts.replace(tzinfo=UTC)
