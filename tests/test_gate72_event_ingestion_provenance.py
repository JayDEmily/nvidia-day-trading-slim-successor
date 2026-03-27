"""Gate 72 event-ingestion and provenance integrity checks."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from nvda_desk.schemas.config import EventIngestionAuthorityResponse
from nvda_desk.schemas.events import (
    EventConfidenceTier,
    EventFreshnessState,
    EventIngestionAuthorityPacket,
    EventSourceClass,
    EventSourceInventoryRecord,
    RawEventSourceObservation,
    SourceConflictDisposition,
    SourceOutagePolicy,
    SupportedEventSource,
)
from nvda_desk.services.event_ingestion import EventIngestionService
from scripts.build_canonical_vocabulary import build_document

REPO_ROOT = Path(__file__).resolve().parents[1]
GATES = REPO_ROOT / "docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v6.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v6.json"
NORMATIVE = REPO_ROOT / "docs/01_NORMATIVE.md"
OPERATING_MODEL = REPO_ROOT / "docs/02_OPERATING_MODEL.md"
DOMAIN_MODEL = REPO_ROOT / "docs/03_DOMAIN_MODEL.md"
GUARDRAILS = REPO_ROOT / "docs/05_GUARDRAILS.md"
VOCAB_PATH = REPO_ROOT / "docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json"


def test_gate72_status_closeout_and_leaf_progress_are_recorded() -> None:
    gates_text = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert "## Gate 72 — Event-source ingestion and provenance normalisation\n\nStatus: complete on `main`" in gates_text
    assert "### Gate 72 closeout note" in gates_text
    assert leaves["completed_gate_ids"][:14] == [
        "Gate 59", "Gate 60", "Gate 61", "Gate 62", "Gate 63", "Gate 64", "Gate 65", "Gate 66",
        "Gate 67", "Gate 68", "Gate 69", "Gate 70", "Gate 71", "Gate 72",
    ]
    assert int(leaves["active_gate"].split()[1]) >= 73
    gate72 = [leaf for leaf in leaves["leaves"] if leaf["gate"] == "Gate 72"]
    assert len(gate72) == 5
    assert all(leaf["status"] == "complete" for leaf in gate72)


def test_gate72_docs_freeze_provenance_and_outage_law() -> None:
    normative = NORMATIVE.read_text(encoding="utf-8")
    operating_model = OPERATING_MODEL.read_text(encoding="utf-8")
    domain_model = DOMAIN_MODEL.read_text(encoding="utf-8")
    guardrails = GUARDRAILS.read_text(encoding="utf-8")

    assert "## Event-source ingestion and provenance law" in normative
    assert "supported source classes are `exchange_calendar`, `issuer_ir`, `macro_calendar`, `policy_calendar`, `internal_curated`, and `options_expiry_calendar`" in normative
    assert "source outages must remain explicit" in normative

    assert "## Gate 72 event-ingestion and provenance authority" in operating_model
    assert "every normalised event record carries freshness, confidence, lineage, and visible conflict/outage semantics" in operating_model

    assert "### 4j. Event-ingestion and provenance objects" in domain_model
    assert "**Event sources must normalise through the frozen provenance contract; stale, conflicting, or degraded source state must stay visible.**" in guardrails


def test_gate72_schema_surface_and_service_normalise_supported_sources() -> None:
    assert [item.value for item in EventSourceClass] == [
        "exchange_calendar", "issuer_ir", "macro_calendar", "policy_calendar", "internal_curated", "options_expiry_calendar",
    ]
    assert [item.value for item in SupportedEventSource] == [
        "nasdaq_trader", "issuer_investor_relations", "macro_release_calendar", "policy_release_calendar", "internal_event_ledger", "options_expiry_ledger",
    ]
    assert [item.value for item in EventFreshnessState] == ["current", "stale", "deferred"]
    assert [item.value for item in EventConfidenceTier] == ["authoritative", "corroborated", "provisional", "degraded"]
    assert [item.value for item in SourceConflictDisposition] == ["authoritative_source_wins", "latest_corroborated_wins", "keep_conflict_visible"]
    assert [item.value for item in SourceOutagePolicy] == ["use_last_verified_with_flag", "degrade_to_unknown", "drop_source_and_block_unsupported"]

    authority = EventIngestionAuthorityResponse(
        authority=EventIngestionAuthorityPacket(
            source_inventory=[
                EventSourceInventoryRecord(source=SupportedEventSource.NASDAQ_TRADER, source_class=EventSourceClass.EXCHANGE_CALENDAR)
            ],
            source_classes=list(EventSourceClass),
            supported_sources=list(SupportedEventSource),
            freshness_states=list(EventFreshnessState),
            confidence_tiers=list(EventConfidenceTier),
            conflict_dispositions=list(SourceConflictDisposition),
            outage_policies=list(SourceOutagePolicy),
        )
    )
    service = EventIngestionService()
    records = service.normalise([
        RawEventSourceObservation(
            source=SupportedEventSource.NASDAQ_TRADER,
            source_class=EventSourceClass.EXCHANGE_CALENDAR,
            symbol=None,
            event_id="evt-fomc",
            event_at=datetime(2026, 3, 18, 18, 0, tzinfo=UTC),
            event_type="fomc_rate_decision",
            label="FOMC decision",
            source_document="nasdaq_calendar",
            observed_at=datetime(2026, 3, 17, 10, 0, tzinfo=UTC),
            freshness_state=EventFreshnessState.CURRENT,
            confidence_tier=EventConfidenceTier.AUTHORITATIVE,
            lineage_key="src:nasdaq:evt-fomc",
        ),
        RawEventSourceObservation(
            source=SupportedEventSource.INTERNAL_EVENT_LEDGER,
            source_class=EventSourceClass.INTERNAL_CURATED,
            symbol=None,
            event_id="evt-fomc",
            event_at=datetime(2026, 3, 18, 18, 0, tzinfo=UTC),
            event_type="fomc_rate_decision",
            label="FOMC rate decision",
            source_document="internal_ledger",
            observed_at=datetime(2026, 3, 17, 11, 0, tzinfo=UTC),
            freshness_state=EventFreshnessState.CURRENT,
            confidence_tier=EventConfidenceTier.CORROBORATED,
            lineage_key="src:int:evt-fomc",
            outage_policy=SourceOutagePolicy.USE_LAST_VERIFIED_WITH_FLAG,
        ),
    ])

    assert authority.authority.source_inventory[0].source is SupportedEventSource.NASDAQ_TRADER
    assert len(records) == 1
    assert records[0].event_id == "evt-fomc"
    assert len(records[0].provenance) == 2
    assert set(records[0].lineage_keys) == {"src:nasdaq:evt-fomc", "src:int:evt-fomc"}
    assert "label_conflict_visible" in records[0].conflict_notes
    assert "source_outage_visible" in records[0].conflict_notes


def test_gate72_vocabulary_terms_are_generated_and_committed() -> None:
    committed = VOCAB_PATH.read_text(encoding="utf-8")
    generated = build_document().to_json_text()

    assert committed == generated
    vocab = json.loads(committed)
    slugs = {entry["canonical_slug"] for entry in vocab["entries"]}
    assert {"event_provenance_contract", "modifier_control_law"}.issubset(slugs)
