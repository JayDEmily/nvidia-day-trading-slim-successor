"""Gate 68 precursor-universe integrity checks."""

from __future__ import annotations

import json
from pathlib import Path

from nvda_desk.schemas.cognition import ReviewExplanationOutput
from nvda_desk.schemas.config import PrecursorUniverseAuthorityResponse
from nvda_desk.schemas.market import (
    DerivedPrecursorField,
    ExcludedPrecursorSource,
    PrecursorSourceClass,
    PrecursorUniverseAuthorityPacket,
    PrecursorVenueContract,
    PrecursorVenueUniverse,
    RawPrecursorField,
    SessionAlignmentExpectation,
)
from nvda_desk.schemas.review import PrecursorGovernanceSurface
from scripts.build_canonical_vocabulary import build_document
from tests._successor_pack_helpers import successor_pack_position

REPO_ROOT = Path(__file__).resolve().parents[1]
GATES = REPO_ROOT / "docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v6.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v6.json"
NORMATIVE = REPO_ROOT / "docs/01_NORMATIVE.md"
OPERATING_MODEL = REPO_ROOT / "docs/02_OPERATING_MODEL.md"
DOMAIN_MODEL = REPO_ROOT / "docs/03_DOMAIN_MODEL.md"
GUARDRAILS = REPO_ROOT / "docs/05_GUARDRAILS.md"
VOCAB_PATH = REPO_ROOT / "docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json"


def test_gate68_status_closeout_and_leaf_progress_are_recorded() -> None:
    gates_text = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert "## Gate 68 — Asia and ex-US precursor market universe\n\nStatus: complete on `main`" in gates_text
    assert "### Gate 68 closeout note" in gates_text
    assert leaves["completed_gate_ids"][:10] == [
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
    ]
    assert successor_pack_position(leaves["active_gate"]) >= 69

    gate68 = [leaf for leaf in leaves["leaves"] if leaf["gate"] == "Gate 68"]
    assert len(gate68) == 5
    assert all(leaf["status"] == "complete" for leaf in gate68)


def test_gate68_docs_freeze_bounded_precursor_scope() -> None:
    normative = NORMATIVE.read_text(encoding="utf-8")
    operating_model = OPERATING_MODEL.read_text(encoding="utf-8")
    domain_model = DOMAIN_MODEL.read_text(encoding="utf-8")
    guardrails = GUARDRAILS.read_text(encoding="utf-8")

    assert "## Precursor-universe law" in normative
    assert "the precursor universe is bounded to JPX cash equity indices, HKEX cash equity indices, Mainland China cash equity indices, and CFFEX index futures" in normative
    assert "Europe, commodities, crypto, and single-stock chatter remain excluded" in normative

    assert "## Gate 68 precursor-universe authority" in operating_model
    assert "only the approved raw and derived precursor fields may flow into later stitching and policy gates" in operating_model

    assert "### 4i. Precursor-universe objects" in domain_model
    assert "**Precursor context must come from the bounded Asia/ex-US universe; no casual source creep.**" in guardrails


def test_gate68_schema_surface_exposes_allowed_fields_and_exclusions() -> None:
    assert [item.value for item in PrecursorVenueUniverse] == [
        "jpx_cash_index_complex",
        "hkex_cash_index_complex",
        "mainland_china_cash_index_complex",
        "cffex_index_futures_complex",
    ]
    assert [item.value for item in PrecursorSourceClass] == ["cash_equity_index", "index_futures"]
    assert [item.value for item in RawPrecursorField] == [
        "session_return_pct",
        "opening_gap_pct",
        "session_range_pct",
        "realised_vol_pct",
        "close_location_in_range",
        "relative_volume_ratio",
        "futures_basis_pct",
        "close_timestamp",
    ]
    assert [item.value for item in DerivedPrecursorField] == [
        "directional_composite_score",
        "cross_venue_agreement_score",
        "futures_cash_divergence_score",
        "impulse_persistence_score",
        "precursor_pressure_score",
        "carry_risk_warning_score",
    ]
    assert [item.value for item in SessionAlignmentExpectation] == [
        "use_last_complete_session",
        "no_partial_session_projection",
        "map_to_next_us_cash_open",
        "weekend_and_holiday_gaps_must_stay_explicit",
    ]
    assert [item.value for item in ExcludedPrecursorSource] == [
        "european_cash_indices",
        "commodities_complex",
        "crypto_24x7",
        "single_stock_chatter",
    ]

    contract = PrecursorVenueContract(
        venue=PrecursorVenueUniverse.CFFEX_INDEX_FUTURES_COMPLEX,
        source_class=PrecursorSourceClass.INDEX_FUTURES,
        allowed_raw_fields=[RawPrecursorField.SESSION_RETURN_PCT, RawPrecursorField.FUTURES_BASIS_PCT],
        allowed_derived_fields=[DerivedPrecursorField.FUTURES_CASH_DIVERGENCE_SCORE, DerivedPrecursorField.CARRY_RISK_WARNING_SCORE],
        session_alignment=[SessionAlignmentExpectation.USE_LAST_COMPLETE_SESSION, SessionAlignmentExpectation.MAP_TO_NEXT_US_CASH_OPEN],
        rationale=["Mainland index futures help explain carry-sensitive precursor pressure before the US open."],
    )
    authority = PrecursorUniverseAuthorityResponse(
        authority=PrecursorUniverseAuthorityPacket(
            venues=[contract],
            raw_fields=list(RawPrecursorField),
            derived_fields=list(DerivedPrecursorField),
            session_alignment_expectations=list(SessionAlignmentExpectation),
            excluded_sources=list(ExcludedPrecursorSource),
        )
    )
    surface = PrecursorGovernanceSurface(
        active_venues=[PrecursorVenueUniverse.JPX_CASH_INDEX_COMPLEX, PrecursorVenueUniverse.HKEX_CASH_INDEX_COMPLEX],
        derived_fields=[DerivedPrecursorField.DIRECTIONAL_COMPOSITE_SCORE, DerivedPrecursorField.CROSS_VENUE_AGREEMENT_SCORE],
        session_alignment=[SessionAlignmentExpectation.USE_LAST_COMPLETE_SESSION],
    )
    review = ReviewExplanationOutput(summary="precursor universe bounded", review_packet={}, precursor_governance=surface)
    assert authority.authority.venues[0].source_class is PrecursorSourceClass.INDEX_FUTURES
    assert review.precursor_governance == surface


def test_gate68_vocabulary_terms_are_generated_and_committed() -> None:
    committed = VOCAB_PATH.read_text(encoding="utf-8")
    generated = build_document().to_json_text()

    assert committed == generated
    vocab = json.loads(committed)
    slugs = {entry["canonical_slug"] for entry in vocab["entries"]}
    assert {"precursor_universe", "event_window_state"}.issubset(slugs)
