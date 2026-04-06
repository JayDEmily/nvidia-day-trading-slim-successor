"""Gate 86 event-ingestion precedence checks."""

from __future__ import annotations

from datetime import UTC, datetime

from nvda_desk.schemas.events import (
    DeskEventClass,
    EventConfidenceTier,
    EventFreshnessState,
    EventMaterialityTier,
    EventSemanticPhase,
    EventSourceClass,
    RawEventSourceObservation,
    SourceConflictDisposition,
    SourceOutagePolicy,
    SupportedEventSource,
)
from nvda_desk.services.event_ingestion import EventIngestionService


def test_gate86_authoritative_source_wins_with_visible_conflict_and_outage_notes() -> None:
    records = EventIngestionService().normalise(
        [
            RawEventSourceObservation(
                source=SupportedEventSource.ISSUER_INVESTOR_RELATIONS,
                source_class=EventSourceClass.ISSUER_IR,
                symbol="NVDA",
                event_id="evt-earnings",
                event_at=datetime(2026, 3, 23, 20, 0, tzinfo=UTC),
                event_type="earnings",
                label="NVDA earnings",
                event_class=DeskEventClass.COMPANY,
                semantic_phase=EventSemanticPhase.KNOWN_RISK,
                materiality_tier=EventMaterialityTier.DESK_CRITICAL,
                source_document="ir_calendar",
                observed_at=datetime(2026, 3, 22, 10, 0, tzinfo=UTC),
                freshness_state=EventFreshnessState.CURRENT,
                confidence_tier=EventConfidenceTier.AUTHORITATIVE,
                lineage_key="src:ir:evt-earnings",
            ),
            RawEventSourceObservation(
                source=SupportedEventSource.INTERNAL_EVENT_LEDGER,
                source_class=EventSourceClass.INTERNAL_CURATED,
                symbol="NVDA",
                event_id="evt-earnings",
                event_at=datetime(2026, 3, 23, 20, 0, tzinfo=UTC),
                event_type="earnings",
                label="NVDA earnings (desk copy)",
                event_class=DeskEventClass.COMPANY,
                semantic_phase=EventSemanticPhase.KNOWN_RISK,
                materiality_tier=EventMaterialityTier.DESK_CRITICAL,
                source_document="internal_ledger",
                observed_at=datetime(2026, 3, 22, 12, 0, tzinfo=UTC),
                freshness_state=EventFreshnessState.CURRENT,
                confidence_tier=EventConfidenceTier.CORROBORATED,
                lineage_key="src:int:evt-earnings",
                outage_policy=SourceOutagePolicy.USE_LAST_VERIFIED_WITH_FLAG,
            ),
        ]
    )

    assert len(records) == 1
    record = records[0]
    assert record.label == "NVDA earnings"
    assert set(record.conflict_notes) >= {
        "label_conflict_visible",
        "source_outage_visible",
        "source_precedence_applied",
    }
    assert record.provenance[0].source is SupportedEventSource.ISSUER_INVESTOR_RELATIONS
    assert (
        record.provenance[1].conflict_disposition
        is SourceConflictDisposition.AUTHORITATIVE_SOURCE_WINS
    )
