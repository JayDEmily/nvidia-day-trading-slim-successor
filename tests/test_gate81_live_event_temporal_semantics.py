from __future__ import annotations

from datetime import UTC, datetime

from nvda_desk.config import Settings
from nvda_desk.schemas.events import (
    DeskEventClass,
    EventConfidenceTier,
    EventFreshnessState,
    EventMaterialityTier,
    EventQueryWindow,
    EventSemanticPhase,
    EventSourceClass,
    EventSourceProvenance,
    LiveEventReference,
    LiveEventSnapshot,
    NormalisedEventRecord,
    SourceConflictDisposition,
    SupportedEventSource,
)
from nvda_desk.schemas.market import (
    DerivedPrecursorField,
    PrecursorContradictionClass,
    PrecursorFallbackDisposition,
    PrecursorPostureState,
    PrecursorRuntimePacket,
    PrecursorVenueUniverse,
)
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.services.event_store import EventStoreService
from nvda_desk.services.temporal_context import TemporalContextService
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture


def _live_event_snapshot() -> LiveEventSnapshot:
    return LiveEventSnapshot(
        requested_at=datetime(2026, 3, 23, 14, 15, tzinfo=UTC),
        symbol="NVDA",
        query_window=EventQueryWindow(lookback_minutes=240, lookahead_minutes=1440),
        next_event=LiveEventReference(
            record_id="evt::1",
            event_id="evt-1",
            event_at=datetime(2026, 3, 23, 15, 30, tzinfo=UTC),
            event_type="macro",
            label="Fed speaker",
            event_class=DeskEventClass.MACRO,
            semantic_phase=EventSemanticPhase.PRICED_RISK,
            materiality_tier=EventMaterialityTier.POSTURE_RELEVANT,
            provenance_count=1,
            lineage_keys=["src:macro:evt-1"],
        ),
        nearby_events=[],
        material_events=[],
        lineage_keys=["src:macro:evt-1"],
    )


def _precursor_packet() -> PrecursorRuntimePacket:
    return PrecursorRuntimePacket(
        requested_at=datetime(2026, 3, 23, 14, 2, tzinfo=UTC),
        stitched_order=[PrecursorVenueUniverse.JPX_CASH_INDEX_COMPLEX],
        active_venues=[PrecursorVenueUniverse.JPX_CASH_INDEX_COMPLEX],
        missing_venues=[PrecursorVenueUniverse.HKEX_CASH_INDEX_COMPLEX],
        derived_fields=[DerivedPrecursorField.DIRECTIONAL_COMPOSITE_SCORE],
        contradiction_class=PrecursorContradictionClass.NONE,
        posture_state=PrecursorPostureState.NORMAL_CONFIDENCE,
        fallback_dispositions=[PrecursorFallbackDisposition.CONTINUE_NORMALLY],
        lineage_keys=["precursor:jpx:1"],
    )


def test_gate81_live_event_reference_preserves_event_class_and_semantic_phase() -> None:
    store = EventStoreService(
        [
            NormalisedEventRecord(
                record_id="evt::1",
                symbol="NVDA",
                event_id="evt-1",
                event_at=datetime(2026, 3, 23, 15, 30, tzinfo=UTC),
                event_type="macro",
                label="Fed speaker",
                event_class=DeskEventClass.MACRO,
                semantic_phase=EventSemanticPhase.PRICED_RISK,
                materiality_tier=EventMaterialityTier.POSTURE_RELEVANT,
                provenance=[
                    EventSourceProvenance(
                        source=SupportedEventSource.MACRO_RELEASE_CALENDAR,
                        source_class=EventSourceClass.MACRO_CALENDAR,
                        source_document="macro_calendar",
                        observed_at=datetime(2026, 3, 23, 10, 0, tzinfo=UTC),
                        freshness_state=EventFreshnessState.CURRENT,
                        confidence_tier=EventConfidenceTier.AUTHORITATIVE,
                        conflict_disposition=SourceConflictDisposition.AUTHORITATIVE_SOURCE_WINS,
                        lineage_key="src:macro:evt-1",
                    )
                ],
                lineage_keys=["src:macro:evt-1"],
            )
        ]
    )
    snapshot = store.build_live_event_snapshot(
        requested_at=datetime(2026, 3, 23, 14, 15, tzinfo=UTC),
        symbol="NVDA",
        query_window=EventQueryWindow(lookback_minutes=240, lookahead_minutes=1440),
    )
    assert snapshot.next_event is not None
    assert snapshot.next_event.event_class is DeskEventClass.MACRO
    assert snapshot.next_event.semantic_phase is EventSemanticPhase.PRICED_RISK


def test_gate81_temporal_context_prefers_live_event_semantic_phase() -> None:
    service = TemporalContextService(Settings())
    fixture = supportive_runtime_fixture().temporal_input.model_copy(
        update={"live_event_snapshot": _live_event_snapshot()}
    )
    output = service.evaluate(fixture)
    assert output.event_proximity_state == "event_live_or_passed"
    assert output.event_window_state == "event_live_window"


def test_gate81_runtime_review_emits_event_window_and_precursor_governance() -> None:
    fixture = supportive_runtime_fixture()
    runtime = DeskCognitionRuntime(Settings())
    result = runtime.run(
        temporal_input=fixture.temporal_input.model_copy(
            update={
                "live_event_snapshot": _live_event_snapshot(),
                "precursor_runtime_packet": _precursor_packet(),
            }
        ),
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )
    assert result.review.event_window_governance is not None
    assert result.review.event_window_governance.event_family == "macro"
    assert (
        result.review.event_window_governance.risk_timing_class.value == "priced_risk"
    )
    assert result.review.precursor_governance is not None
    assert result.review.precursor_governance.active_venues == [
        PrecursorVenueUniverse.JPX_CASH_INDEX_COMPLEX
    ]
