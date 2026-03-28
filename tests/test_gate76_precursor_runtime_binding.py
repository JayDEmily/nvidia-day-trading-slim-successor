"""Gate 76 precursor runtime-binding integrity checks."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.schemas.market import (
    DerivedPrecursorField,
    PrecursorContradictionClass,
    PrecursorFallbackDisposition,
    PrecursorPostureState,
    PrecursorRuntimePacket,
    PrecursorVenueUniverse,
)
from nvda_desk.services.chain_to_cognition import ChainToCognitionService
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.services.real_data_loader import RealDataLoaderService
from nvda_desk.services.review_packets import ReviewPacketService
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture
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
FIXTURE_PACK_PATH = (
    REPO_ROOT / "fixtures" / "real_data" / "gate_e_prepared_runtime_fixture_pack.json"
)


def _precursor_packet() -> PrecursorRuntimePacket:
    return PrecursorRuntimePacket(
        requested_at=datetime(2026, 3, 23, 14, 2, tzinfo=UTC),
        stitched_order=[
            PrecursorVenueUniverse.JPX_CASH_INDEX_COMPLEX,
            PrecursorVenueUniverse.HKEX_CASH_INDEX_COMPLEX,
            PrecursorVenueUniverse.CFFEX_INDEX_FUTURES_COMPLEX,
        ],
        active_venues=[
            PrecursorVenueUniverse.JPX_CASH_INDEX_COMPLEX,
            PrecursorVenueUniverse.HKEX_CASH_INDEX_COMPLEX,
            PrecursorVenueUniverse.CFFEX_INDEX_FUTURES_COMPLEX,
        ],
        missing_venues=[PrecursorVenueUniverse.MAINLAND_CHINA_CASH_INDEX_COMPLEX],
        derived_fields=[
            DerivedPrecursorField.DIRECTIONAL_COMPOSITE_SCORE,
            DerivedPrecursorField.CROSS_VENUE_AGREEMENT_SCORE,
        ],
        contradiction_class=PrecursorContradictionClass.DIRECTIONAL_SPLIT,
        posture_state=PrecursorPostureState.TIGHTENED_POSTURE,
        fallback_dispositions=[
            PrecursorFallbackDisposition.CONTINUE_NORMALLY,
            PrecursorFallbackDisposition.CONTINUE_NORMALLY,
            PrecursorFallbackDisposition.CONTINUE_WITH_DEGRADED_CONFIDENCE,
        ],
        lineage_keys=["precursor:jpx:1", "precursor:hkex:1", "precursor:cffex:1"],
        notes=["active_precursor_packet_for_gate76"],
    )


def test_gate76_status_closeout_and_leaf_progress_are_recorded() -> None:
    gates_text = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert (
        "## Gate 76 — Precursor runtime binding and review exposure\n\nStatus: complete on `main`"
        in gates_text
    )
    assert "### Gate 76 closeout note" in gates_text
    assert leaves["completed_gate_ids"][:18] == [
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
        "Gate 76",
    ]
    assert successor_pack_position(leaves["active_gate"]) >= 77
    gate76 = [leaf for leaf in leaves["leaves"] if leaf["gate"] == "Gate 76"]
    assert len(gate76) == 4
    assert all(leaf["status"] == "complete" for leaf in gate76)


def test_gate76_docs_freeze_precursor_runtime_binding_law() -> None:
    normative = NORMATIVE.read_text(encoding="utf-8")
    operating_model = OPERATING_MODEL.read_text(encoding="utf-8")
    domain_model = DOMAIN_MODEL.read_text(encoding="utf-8")
    guardrails = GUARDRAILS.read_text(encoding="utf-8")

    assert "## Precursor runtime-binding law" in normative
    assert (
        "precursor runtime truth must travel in one additive typed packet shared by runtime ingress and review"
        in normative
    )
    assert (
        "legacy consumers may ignore the richer packet, but they must not rewrite or shadow it"
        in normative
    )

    assert "## Gate 76 precursor runtime-binding authority" in operating_model
    assert (
        "`PreparedRuntimeSnapshot.precursor_runtime_packet` and `TemporalContextInput.precursor_runtime_packet` carry the same typed precursor truth"
        in operating_model
    )

    assert "### 4n. Precursor runtime-binding objects" in domain_model
    assert "no sidecar precursor memory" in guardrails


def test_gate76_precursor_packet_flows_through_chain_to_cognition_and_review() -> None:
    pack = RealDataLoaderService().load_fixture_pack(FIXTURE_PACK_PATH)
    packet = _precursor_packet()
    snapshot = pack.prepared_dataset.snapshots[0].model_copy(
        update={
            "precursor_runtime_packet": packet,
            "lineage": pack.prepared_dataset.snapshots[0].lineage.model_copy(
                update={"precursor_lineage_keys": list(packet.lineage_keys)}
            ),
        }
    )
    converted = ChainToCognitionService().convert_snapshot(snapshot)

    assert converted.temporal_input.precursor_runtime_packet == packet
    assert converted.lineage.precursor_lineage_keys == packet.lineage_keys

    fixture = supportive_runtime_fixture()
    runtime = DeskCognitionRuntime(Settings())
    result = runtime.run(
        temporal_input=fixture.temporal_input.model_copy(
            update={"precursor_runtime_packet": packet}
        ),
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )

    assert result.review.precursor_runtime_binding is not None
    assert result.review.precursor_runtime_binding.active_venues == packet.active_venues
    assert (
        result.review.precursor_runtime_binding.contradiction_class
        is PrecursorContradictionClass.DIRECTIONAL_SPLIT
    )
    assert result.review.review_packet[
        "precursor_runtime_binding"
    ] == ReviewPacketService.render_precursor_runtime_binding(packet)


def test_gate76_vocabulary_terms_are_generated_and_committed() -> None:
    committed = VOCAB_PATH.read_text(encoding="utf-8")
    generated = build_document().to_json_text()

    assert committed == generated
    vocab = json.loads(committed)
    slugs = {entry["canonical_slug"] for entry in vocab["entries"]}
    assert {"precursor_stitching", "precursor_runtime_packet"}.issubset(slugs)
