"""Gate 75 precursor-stitching integrity checks."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.domain.session_clock import SessionClockClassifier
from nvda_desk.schemas.config import PrecursorStitchingAuthorityResponse
from nvda_desk.schemas.market import (
    DerivedPrecursorField,
    PrecursorContradictionClass,
    PrecursorFallbackDisposition,
    PrecursorFreshnessState,
    PrecursorPostureState,
    PrecursorSourceClass,
    PrecursorStitchingAuthorityPacket,
    PrecursorTimestampDiscipline,
    PrecursorVenueSlice,
    PrecursorVenueUniverse,
)
from nvda_desk.services.market_state import MarketStateService
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


def test_gate75_status_closeout_and_leaf_progress_are_recorded() -> None:
    gates_text = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert (
        "## Gate 75 — Precursor stitching, fallback, and contradiction rules\n\nStatus: complete on `main`"
        in gates_text
    )
    assert "### Gate 75 closeout note" in gates_text
    assert leaves["completed_gate_ids"][:17] == [
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
        "Gate 75",
    ]
    assert successor_pack_position(leaves["active_gate"]) >= 76
    gate75 = [leaf for leaf in leaves["leaves"] if leaf["gate"] == "Gate 75"]
    assert len(gate75) == 5
    assert all(leaf["status"] == "complete" for leaf in gate75)


def test_gate75_docs_freeze_precursor_stitching_law() -> None:
    normative = NORMATIVE.read_text(encoding="utf-8")
    operating_model = OPERATING_MODEL.read_text(encoding="utf-8")
    domain_model = DOMAIN_MODEL.read_text(encoding="utf-8")
    guardrails = GUARDRAILS.read_text(encoding="utf-8")

    assert "## Precursor-stitching law" in normative
    assert (
        "precursor venue order is `jpx_cash_index_complex`, `hkex_cash_index_complex`, `mainland_china_cash_index_complex`, then `cffex_index_futures_complex`"
        in normative
    )
    assert (
        "contradiction classes are `none`, `directional_split`, `futures_cash_divergence`, `timestamp_misalignment`, and `broad_cross_venue_conflict`"
        in normative
    )

    assert "## Gate 75 precursor-stitching authority" in operating_model
    assert (
        "`MarketStateService.stitch_precursor_context(...)` is the authoritative pre-runtime assembly path"
        in operating_model
    )

    assert "### 4m. Precursor-stitching objects" in domain_model
    assert "quiet venue reshuffling" in guardrails


def test_gate75_schema_surface_and_service_define_deterministic_stitching() -> None:
    assert [item.value for item in PrecursorTimestampDiscipline] == [
        "last_complete_session_only",
        "venue_local_close_required",
        "request_time_must_not_precede_source_time",
        "no_forward_fill_across_us_decision_window",
    ]
    assert [item.value for item in PrecursorFreshnessState] == [
        "current",
        "degraded",
        "stale",
        "missing",
    ]
    assert [item.value for item in PrecursorFallbackDisposition] == [
        "continue_normally",
        "continue_with_degraded_confidence",
        "continue_without_venue",
        "require_stand_down_pressure",
    ]
    assert [item.value for item in PrecursorContradictionClass] == [
        "none",
        "directional_split",
        "futures_cash_divergence",
        "timestamp_misalignment",
        "broad_cross_venue_conflict",
    ]
    assert [item.value for item in PrecursorPostureState] == [
        "normal_confidence",
        "degraded_confidence",
        "tightened_posture",
        "stand_down_pressure",
        "unresolved_context",
    ]

    authority = PrecursorStitchingAuthorityResponse(
        authority=PrecursorStitchingAuthorityPacket(
            venue_order=[
                PrecursorVenueUniverse.JPX_CASH_INDEX_COMPLEX,
                PrecursorVenueUniverse.HKEX_CASH_INDEX_COMPLEX,
                PrecursorVenueUniverse.MAINLAND_CHINA_CASH_INDEX_COMPLEX,
                PrecursorVenueUniverse.CFFEX_INDEX_FUTURES_COMPLEX,
            ],
            timestamp_disciplines=list(PrecursorTimestampDiscipline),
            freshness_states=list(PrecursorFreshnessState),
            fallback_dispositions=list(PrecursorFallbackDisposition),
            contradiction_classes=list(PrecursorContradictionClass),
            posture_states=list(PrecursorPostureState),
        )
    )
    service = MarketStateService(classifier=SessionClockClassifier(Settings()))
    result = service.stitch_precursor_context(
        requested_at=datetime(2026, 3, 27, 13, 0, tzinfo=UTC),
        authority=authority.authority,
        slices=[
            PrecursorVenueSlice(
                venue=PrecursorVenueUniverse.CFFEX_INDEX_FUTURES_COMPLEX,
                source_class=PrecursorSourceClass.INDEX_FUTURES,
                session_close_at=datetime(2026, 3, 27, 7, 0, tzinfo=UTC),
                observed_at=datetime(2026, 3, 27, 7, 5, tzinfo=UTC),
                freshness_state=PrecursorFreshnessState.CURRENT,
                derived_values={
                    DerivedPrecursorField.DIRECTIONAL_COMPOSITE_SCORE: -0.6,
                    DerivedPrecursorField.FUTURES_CASH_DIVERGENCE_SCORE: 0.1,
                },
                lineage_keys=["precursor:cffex:1"],
            ),
            PrecursorVenueSlice(
                venue=PrecursorVenueUniverse.JPX_CASH_INDEX_COMPLEX,
                source_class=PrecursorSourceClass.CASH_EQUITY_INDEX,
                session_close_at=datetime(2026, 3, 27, 6, 0, tzinfo=UTC),
                observed_at=datetime(2026, 3, 27, 6, 5, tzinfo=UTC),
                freshness_state=PrecursorFreshnessState.DEGRADED,
                derived_values={DerivedPrecursorField.DIRECTIONAL_COMPOSITE_SCORE: 0.5},
                lineage_keys=["precursor:jpx:1"],
            ),
        ],
    )

    assert result.stitched_order == [
        PrecursorVenueUniverse.JPX_CASH_INDEX_COMPLEX,
        PrecursorVenueUniverse.CFFEX_INDEX_FUTURES_COMPLEX,
    ]
    assert result.missing_venues == [
        PrecursorVenueUniverse.HKEX_CASH_INDEX_COMPLEX,
        PrecursorVenueUniverse.MAINLAND_CHINA_CASH_INDEX_COMPLEX,
    ]
    assert result.contradiction_class is PrecursorContradictionClass.DIRECTIONAL_SPLIT
    assert result.posture_state is PrecursorPostureState.TIGHTENED_POSTURE
    assert result.fallback_dispositions[:2] == [
        PrecursorFallbackDisposition.CONTINUE_WITH_DEGRADED_CONFIDENCE,
        PrecursorFallbackDisposition.CONTINUE_NORMALLY,
    ]
    assert result.lineage_keys == ["precursor:cffex:1", "precursor:jpx:1"]


def test_gate75_vocabulary_terms_are_generated_and_committed() -> None:
    committed = VOCAB_PATH.read_text(encoding="utf-8")
    generated = build_document().to_json_text()

    assert committed == generated
    vocab = json.loads(committed)
    slugs = {entry["canonical_slug"] for entry in vocab["entries"]}
    assert {
        "precursor_stitching",
        "precursor_runtime_packet",
        "review_failure_taxonomy",
    }.issubset(slugs)
