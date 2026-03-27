"""Gate 77 review-packet and failure-taxonomy integrity checks."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

from nvda_desk.config import Settings
from nvda_desk.schemas.events import (
    EventMaterialityTier,
    EventQueryWindow,
    LiveEventReference,
    LiveEventSnapshot,
)
from nvda_desk.schemas.market import (
    DerivedPrecursorField,
    PrecursorContradictionClass,
    PrecursorFallbackDisposition,
    PrecursorPostureState,
    PrecursorRuntimePacket,
    PrecursorVenueUniverse,
)
from nvda_desk.schemas.review import (
    EconomicContributionPacket,
    EconomicContributionTag,
    PromotionEvidencePacket,
    ReviewFailureClass,
    ReviewFailurePacket,
    ReviewLineagePacket,
    ReviewResolutionClass,
)
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.services.review_packets import ReviewPacketService
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture
from scripts.build_canonical_vocabulary import build_document

REPO_ROOT = Path(__file__).resolve().parents[1]
GATES = REPO_ROOT / "docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v6.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v6.json"
NORMATIVE = REPO_ROOT / "docs/01_NORMATIVE.md"
OPERATING_MODEL = REPO_ROOT / "docs/02_OPERATING_MODEL.md"
DOMAIN_MODEL = REPO_ROOT / "docs/03_DOMAIN_MODEL.md"
GUARDRAILS = REPO_ROOT / "docs/05_GUARDRAILS.md"
VOCAB_PATH = REPO_ROOT / "docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json"


def _precursor_packet() -> PrecursorRuntimePacket:
    return PrecursorRuntimePacket(
        requested_at=datetime(2026, 3, 23, 14, 2, tzinfo=UTC),
        stitched_order=[PrecursorVenueUniverse.JPX_CASH_INDEX_COMPLEX, PrecursorVenueUniverse.CFFEX_INDEX_FUTURES_COMPLEX],
        active_venues=[PrecursorVenueUniverse.JPX_CASH_INDEX_COMPLEX, PrecursorVenueUniverse.CFFEX_INDEX_FUTURES_COMPLEX],
        missing_venues=[PrecursorVenueUniverse.HKEX_CASH_INDEX_COMPLEX, PrecursorVenueUniverse.MAINLAND_CHINA_CASH_INDEX_COMPLEX],
        derived_fields=[DerivedPrecursorField.DIRECTIONAL_COMPOSITE_SCORE],
        contradiction_class=PrecursorContradictionClass.DIRECTIONAL_SPLIT,
        posture_state=PrecursorPostureState.TIGHTENED_POSTURE,
        fallback_dispositions=[PrecursorFallbackDisposition.CONTINUE_NORMALLY],
        lineage_keys=["precursor:jpx:1", "precursor:cffex:1"],
    )


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
            materiality_tier=EventMaterialityTier.POSTURE_RELEVANT,
            provenance_count=1,
            lineage_keys=["src:ir:evt-1"],
        ),
        nearby_events=[],
        material_events=[],
        lineage_keys=["src:ir:evt-1"],
    )


def test_gate77_status_closeout_and_leaf_progress_are_recorded() -> None:
    gates_text = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert "## Gate 77 — Review packet upgrade and failure taxonomy\n\nStatus: complete on `main`" in gates_text
    assert "### Gate 77 closeout note" in gates_text
    assert leaves["completed_gate_ids"][:19] == [
        "Gate 59", "Gate 60", "Gate 61", "Gate 62", "Gate 63", "Gate 64", "Gate 65", "Gate 66",
        "Gate 67", "Gate 68", "Gate 69", "Gate 70", "Gate 71", "Gate 72", "Gate 73", "Gate 74", "Gate 75", "Gate 76", "Gate 77",
    ]
    assert int(leaves["active_gate"].split()[1]) >= 78
    gate77 = [leaf for leaf in leaves["leaves"] if leaf["gate"] == "Gate 77"]
    assert len(gate77) == 5
    assert all(leaf["status"] == "complete" for leaf in gate77)


def test_gate77_docs_freeze_review_packet_failure_law() -> None:
    normative = NORMATIVE.read_text(encoding="utf-8")
    operating_model = OPERATING_MODEL.read_text(encoding="utf-8")
    domain_model = DOMAIN_MODEL.read_text(encoding="utf-8")
    guardrails = GUARDRAILS.read_text(encoding="utf-8")

    assert "## Review-packet and failure-taxonomy law" in normative
    assert "failure classes are `diagnosis_failure`, `posture_policy_failure`, `eligibility_failure`, `execution_expression_failure`, `sizing_failure`, `data_provenance_failure`, and `ontology_failure`" in normative
    assert "review outputs are `action_taken`, `non_action`, `blocked_trade`, `unknown`, `unresolved`, `bad_luck`, and `ontology_failure`" in normative

    assert "## Gate 77 review-packet and failure-taxonomy authority" in operating_model
    assert "`ReviewExplanationOutput.review_lineage`, `failure_taxonomy`, `economic_accountability`, and `promotion_evidence` are now mandatory typed review surfaces" in operating_model

    assert "### 4o. Review failure-taxonomy objects" in domain_model
    assert "no post hoc story time" in guardrails


def test_gate77_schema_surface_exposes_failure_and_promotion_packets() -> None:
    assert [item.value for item in ReviewFailureClass] == [
        "diagnosis_failure",
        "posture_policy_failure",
        "eligibility_failure",
        "execution_expression_failure",
        "sizing_failure",
        "data_provenance_failure",
        "ontology_failure",
    ]
    assert [item.value for item in ReviewResolutionClass] == [
        "action_taken",
        "non_action",
        "blocked_trade",
        "unknown",
        "unresolved",
        "bad_luck",
        "ontology_failure",
    ]
    assert [item.value for item in EconomicContributionTag] == [
        "value_add",
        "capital_preservation",
        "neutral",
        "value_leak",
        "unknown",
    ]

    lineage = ReviewLineagePacket(
        event_lineage_keys=["src:ir:evt-1"],
        precursor_lineage_keys=["precursor:jpx:1"],
        modifier_policy_ids=[],
        effective_coefficient_targets=[],
        posture_change_reasons=["permission=deploy_small"],
    )
    failure = ReviewFailurePacket(
        primary_failure_class=ReviewFailureClass.DIAGNOSIS_FAILURE,
        resolution=ReviewResolutionClass.UNRESOLVED,
        rationale=["cross_signal_conflict_visible_in_review"],
    )
    contribution = EconomicContributionPacket(diagnosis=EconomicContributionTag.VALUE_LEAK)
    promotion = PromotionEvidencePacket(
        ready_for_candidate_review=False,
        required_sections=["event_lineage_keys", "precursor_lineage_keys"],
        missing_sections=["modifier_policy_ids"],
        notes=["needs more lineage before candidate adjudication"],
    )

    rendered_failure = cast(dict[str, Any], ReviewPacketService.render_failure_taxonomy(failure))
    rendered_promotion = cast(dict[str, Any], ReviewPacketService.render_promotion_evidence(promotion))

    assert rendered_failure["resolution"] == "unresolved"
    assert rendered_promotion["missing_sections"] == ["modifier_policy_ids"]
    assert lineage.event_lineage_keys == ["src:ir:evt-1"]
    assert contribution.diagnosis is EconomicContributionTag.VALUE_LEAK


def test_gate77_runtime_review_packet_carries_lineage_failure_and_promotion_evidence() -> None:
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

    assert result.review.review_lineage is not None
    assert result.review.review_lineage.event_lineage_keys == ["src:ir:evt-1"]
    assert result.review.review_lineage.precursor_lineage_keys == ["precursor:jpx:1", "precursor:cffex:1"]
    assert result.review.failure_taxonomy is not None
    assert result.review.failure_taxonomy.resolution is ReviewResolutionClass.UNRESOLVED
    assert result.review.economic_accountability is not None
    assert result.review.economic_accountability.diagnosis in {EconomicContributionTag.UNKNOWN, EconomicContributionTag.VALUE_LEAK}
    assert result.review.promotion_evidence is not None
    assert result.review.promotion_evidence.ready_for_candidate_review is True
    assert result.review.review_lineage.modifier_policy_ids
    assert result.review.promotion_evidence.missing_sections == []
    review_lineage = cast(dict[str, Any], result.review.review_packet["review_lineage"])
    failure_taxonomy = cast(dict[str, Any], result.review.review_packet["failure_taxonomy"])
    promotion_evidence = cast(dict[str, Any], result.review.review_packet["promotion_evidence"])

    assert review_lineage["event_lineage_keys"] == ["src:ir:evt-1"]
    assert failure_taxonomy["resolution"] == "unresolved"
    assert promotion_evidence["ready_for_candidate_review"] is True


def test_gate77_vocabulary_terms_are_generated_and_committed() -> None:
    committed = VOCAB_PATH.read_text(encoding="utf-8")
    generated = build_document().to_json_text()

    assert committed == generated
    vocab = json.loads(committed)
    slugs = {entry["canonical_slug"] for entry in vocab["entries"]}
    assert {"review_failure_taxonomy", "precursor_runtime_packet"}.issubset(slugs)
