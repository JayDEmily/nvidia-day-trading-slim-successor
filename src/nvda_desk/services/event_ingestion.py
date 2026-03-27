from __future__ import annotations

from collections import defaultdict
from collections.abc import Sequence

from nvda_desk.schemas.events import (
    EventSourceProvenance,
    NormalisedEventRecord,
    RawEventSourceObservation,
    SourceConflictDisposition,
)


class EventIngestionService:
    """Normalise bounded event-source observations into shared event truth.

    Purpose:
        Freeze one provenance-aware event contract before store/query and live
        runtime consumers are wired together.
    Inputs:
        Sequences of `RawEventSourceObservation` instances from supported event
        sources.
    Outputs:
        `NormalisedEventRecord` objects carrying explicit provenance, lineage,
        freshness, confidence, and visible conflict notes.
    Determinism:
        Groups observations by event identity and preserves source disagreement
        explicitly rather than merging it away silently.
    """

    def normalise(self, observations: Sequence[RawEventSourceObservation]) -> list[NormalisedEventRecord]:
        grouped: dict[tuple[str | None, str, str, str], list[RawEventSourceObservation]] = defaultdict(list)
        for observation in observations:
            key = (observation.symbol, observation.event_id, observation.event_type, observation.event_at.isoformat())
            grouped[key].append(observation)

        records: list[NormalisedEventRecord] = []
        for items in grouped.values():
            ordered = sorted(items, key=lambda item: (item.event_at, item.observed_at, item.source.value))
            winner = ordered[0]
            labels = {item.label for item in ordered}
            conflict_notes = []
            if len(labels) > 1:
                conflict_notes.append('label_conflict_visible')
            if any(item.outage_policy is not None for item in ordered):
                conflict_notes.append('source_outage_visible')
            provenance = [
                EventSourceProvenance(
                    source=item.source,
                    source_class=item.source_class,
                    source_document=item.source_document,
                    observed_at=item.observed_at,
                    freshness_state=item.freshness_state,
                    confidence_tier=item.confidence_tier,
                    conflict_disposition=(
                        SourceConflictDisposition.AUTHORITATIVE_SOURCE_WINS
                        if item.confidence_tier.value == 'authoritative'
                        else SourceConflictDisposition.KEEP_CONFLICT_VISIBLE
                    ),
                    outage_policy=item.outage_policy,
                    lineage_key=item.lineage_key,
                    notes=list(item.notes),
                )
                for item in ordered
            ]
            records.append(
                NormalisedEventRecord(
                    record_id=f'evt::{winner.event_id}::{winner.event_at.isoformat()}',
                    symbol=winner.symbol,
                    event_id=winner.event_id,
                    event_at=winner.event_at,
                    event_type=winner.event_type,
                    label=winner.label,
                    event_class=winner.event_class,
                    semantic_phase=winner.semantic_phase,
                    materiality_tier=winner.materiality_tier,
                    provenance=provenance,
                    lineage_keys=[item.lineage_key for item in ordered],
                    conflict_notes=conflict_notes,
                    tags=sorted({item.source_class.value for item in ordered}),
                )
            )
        return sorted(records, key=lambda record: (record.event_at, record.event_id, record.record_id))
