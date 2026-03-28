"""Gate 74 live-event-richness integrity checks."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from nvda_desk.schemas.config import LiveEventRichnessAuthorityResponse
from nvda_desk.schemas.events import (
    EventConfidenceTier,
    EventFreshnessState,
    EventMaterialityTier,
    EventQueryWindow,
    EventSourceClass,
    EventSourceProvenance,
    LiveEventRichnessAuthorityPacket,
    NormalisedEventRecord,
    SourceConflictDisposition,
    SupportedEventSource,
)
from nvda_desk.services.event_store import EventStoreService
from scripts.build_canonical_vocabulary import build_document
from tests._successor_pack_helpers import successor_pack_position

REPO_ROOT = Path(__file__).resolve().parents[1]
GATES = (
    REPO_ROOT / "docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v6.md"
)
LEAVES = (
    REPO_ROOT
    / "docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v6.json"
)
NORMATIVE = REPO_ROOT / "docs/01_NORMATIVE.md"
OPERATING_MODEL = REPO_ROOT / "docs/02_OPERATING_MODEL.md"
DOMAIN_MODEL = REPO_ROOT / "docs/03_DOMAIN_MODEL.md"
GUARDRAILS = REPO_ROOT / "docs/05_GUARDRAILS.md"
VOCAB_PATH = (
    REPO_ROOT / "docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json"
)


def test_gate74_status_closeout_and_leaf_progress_are_recorded() -> None:
    gates_text = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert (
        "## Gate 74 — Preserve event richness into live cognition input\n\nStatus: complete on `main`"
        in gates_text
    )
    assert "### Gate 74 closeout note" in gates_text
    assert leaves["completed_gate_ids"][:16] == [
        "Gate 59",
        "Gate 60",
        "Gate 61",
        "Gate 62",
        "Gate 63",
        "Gate 64",
        "Gate 65",
        "Gate 66",
        "Gate 67",
        "Gate 68",
        "Gate 69",
        "Gate 70",
        "Gate 71",
        "Gate 72",
        "Gate 73",
        "Gate 74",
    ]
    assert successor_pack_position(leaves["active_gate"]) >= 75
    gate74 = [leaf for leaf in leaves["leaves"] if leaf["gate"] == "Gate 74"]
    assert len(gate74) == 5
    assert all(leaf["status"] == "complete" for leaf in gate74)


def test_gate74_docs_freeze_live_event_richness_law() -> None:
    normative = NORMATIVE.read_text(encoding="utf-8")
    operating_model = OPERATING_MODEL.read_text(encoding="utf-8")
    domain_model = DOMAIN_MODEL.read_text(encoding="utf-8")
    guardrails = GUARDRAILS.read_text(encoding="utf-8")

    assert "## Live event-richness law" in normative
    assert (
        "preserve event identity, materiality, provenance counts, nearby-event summaries, and lineage keys"
        in normative
    )
    assert (
        "`next_event_at` remains as an explicit backwards-compatible compatibility field"
        in normative
    )

    assert "## Gate 74 live event-richness authority" in operating_model
    assert "`TemporalContextInput.live_event_snapshot`" in operating_model

    assert "### 4l. Live event-richness objects" in domain_model
    assert (
        "`PreparedRuntimeSnapshot.live_event_snapshot` and `TemporalContextInput.live_event_snapshot`"
        in domain_model
    )
    assert (
        "`next_event_at` may remain only as a derived compatibility hint" in guardrails
    )


def test_gate74_schema_surface_and_service_preserve_live_event_truth() -> None:
    authority = LiveEventRichnessAuthorityResponse(
        authority=LiveEventRichnessAuthorityPacket(
            identity_required=True,
            impact_required=True,
            provenance_required=True,
            nearby_summary_required=True,
            lineage_retention_required=True,
            timestamp_backcompat_required=True,
        )
    )
    records = [
        NormalisedEventRecord(
            record_id="evt::1",
            symbol="NVDA",
            event_id="evt-1",
            event_at=datetime(2026, 3, 18, 18, 0, tzinfo=UTC),
            event_type="earnings",
            label="NVDA earnings",
            materiality_tier=EventMaterialityTier.DESK_CRITICAL,
            provenance=[
                EventSourceProvenance(
                    source=SupportedEventSource.ISSUER_INVESTOR_RELATIONS,
                    source_class=EventSourceClass.ISSUER_IR,
                    source_document="ir_calendar",
                    observed_at=datetime(2026, 3, 17, 10, 0, tzinfo=UTC),
                    freshness_state=EventFreshnessState.CURRENT,
                    confidence_tier=EventConfidenceTier.AUTHORITATIVE,
                    conflict_disposition=SourceConflictDisposition.AUTHORITATIVE_SOURCE_WINS,
                    lineage_key="src:ir:evt-1",
                )
            ],
            lineage_keys=["src:ir:evt-1"],
        ),
        NormalisedEventRecord(
            record_id="evt::2",
            symbol=None,
            event_id="evt-2",
            event_at=datetime(2026, 3, 18, 15, 0, tzinfo=UTC),
            event_type="macro",
            label="US CPI",
            materiality_tier=EventMaterialityTier.POSTURE_RELEVANT,
            provenance=[],
            lineage_keys=["src:macro:evt-2"],
        ),
    ]
    service = EventStoreService(records)
    snapshot = service.build_live_event_snapshot(
        requested_at=datetime(2026, 3, 18, 14, 30, tzinfo=UTC),
        symbol="NVDA",
        query_window=EventQueryWindow(lookback_minutes=60, lookahead_minutes=300),
        minimum_materiality=EventMaterialityTier.POSTURE_RELEVANT,
    )

    assert authority.authority.timestamp_backcompat_required is True
    assert snapshot.next_event is not None
    assert snapshot.next_event.event_id == "evt-2"
    assert [event.event_id for event in snapshot.nearby_events] == ["evt-2", "evt-1"]
    assert [event.event_id for event in snapshot.material_events] == ["evt-2", "evt-1"]
    assert snapshot.nearby_events[1].provenance_count == 1
    assert snapshot.lineage_keys == ["src:ir:evt-1", "src:macro:evt-2"]


def test_gate74_vocabulary_terms_are_generated_and_committed() -> None:
    committed = VOCAB_PATH.read_text(encoding="utf-8")
    generated = build_document().to_json_text()

    assert committed == generated
    vocab = json.loads(committed)
    slugs = {entry["canonical_slug"] for entry in vocab["entries"]}
    assert {"shared_event_store", "live_event_richness"}.issubset(slugs)
