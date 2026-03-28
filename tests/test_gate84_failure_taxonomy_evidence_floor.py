"""Gate 84 failure-taxonomy deepening checks."""

from __future__ import annotations

from datetime import UTC, datetime
from types import SimpleNamespace
from typing import cast

from nvda_desk.config import Settings
from nvda_desk.schemas.cognition import ReviewExplanationInput
from nvda_desk.schemas.events import (
    DeskEventClass,
    EventMaterialityTier,
    EventQueryWindow,
    EventSemanticPhase,
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
    ReviewEligibilitySurface,
    ReviewFailureClass,
    ReviewResolutionClass,
)
from nvda_desk.schemas.state_policy import (
    CorridorBreachSeverity,
    ReviewChangeBudget,
    ReviewEvidenceBlock,
    ReviewOutcome,
    ReviewSurfaceClass,
)
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.services.review_explanation import ReviewExplanationService
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


def _review_eligibility(
    severity: CorridorBreachSeverity,
) -> ReviewEligibilitySurface:
    return ReviewEligibilitySurface(
        evidence_block=ReviewEvidenceBlock(
            surface_class=ReviewSurfaceClass.POLICY_SURFACE,
            surface_id="gate84_test_surface",
            sample_count=4,
            session_count=1,
            event_slice_count=1,
            regime_slice_count=1,
            coverage_ratio=0.8,
            breach_severity=severity,
            persistence_blocks=1,
            hysteresis_passed=True,
        ),
        trigger_classes=[],
        eligible=True,
        governed_outcome=ReviewOutcome.BOUNDED_ADJUSTMENT_REQUEST,
        change_budget=ReviewChangeBudget.BOUNDED_SINGLE_SURFACE,
    )


def test_gate84_runtime_populates_evidence_floor_for_blocked_trade_path() -> None:
    fixture = supportive_runtime_fixture()
    result = DeskCognitionRuntime(Settings()).run(
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

    assert result.review.failure_taxonomy is not None
    assert (
        result.review.failure_taxonomy.primary_failure_class
        is ReviewFailureClass.POSTURE_POLICY_FAILURE
    )
    assert result.review.failure_taxonomy.resolution is ReviewResolutionClass.BLOCKED_TRADE
    assert result.review.failure_taxonomy.evidence_floor is not None


def test_gate84_failure_taxonomy_reaches_ontology_sizing_and_bad_luck_paths() -> None:
    service = ReviewExplanationService()

    ontology_payload = SimpleNamespace(
        temporal_input=None,
        modifier_runtime_packet=None,
        execution=SimpleNamespace(
            active_playbook_ids=["pb-1"], lead_family_id=None, inventory_action="deploy"
        ),
        eligibility=SimpleNamespace(candidates=["cand-1"], no_trade_reasons=[]),
        posture=SimpleNamespace(permission_state=SimpleNamespace(value="allow")),
    )
    ontology = service._failure_taxonomy(
        cast(ReviewExplanationInput, ontology_payload),
        [],
        _review_eligibility(CorridorBreachSeverity.MATERIAL),
    )
    assert ontology.primary_failure_class is ReviewFailureClass.ONTOLOGY_FAILURE
    assert ontology.evidence_floor is not None

    sizing_payload = SimpleNamespace(
        temporal_input=None,
        modifier_runtime_packet=None,
        execution=SimpleNamespace(
            active_playbook_ids=["pb-1"],
            lead_family_id="lead-1",
            inventory_action="trim",
        ),
        eligibility=SimpleNamespace(candidates=[], no_trade_reasons=[]),
        posture=SimpleNamespace(permission_state=SimpleNamespace(value="allow")),
    )
    sizing = service._failure_taxonomy(
        cast(ReviewExplanationInput, sizing_payload),
        [],
        _review_eligibility(CorridorBreachSeverity.MATERIAL),
    )
    assert sizing.primary_failure_class is ReviewFailureClass.SIZING_FAILURE
    assert sizing.resolution is ReviewResolutionClass.UNRESOLVED

    bad_luck_payload = SimpleNamespace(
        temporal_input=None,
        modifier_runtime_packet=None,
        execution=SimpleNamespace(
            active_playbook_ids=[], lead_family_id=None, inventory_action="hold"
        ),
        eligibility=SimpleNamespace(candidates=[], no_trade_reasons=[]),
        posture=SimpleNamespace(permission_state=SimpleNamespace(value="allow")),
    )
    bad_luck = service._failure_taxonomy(
        cast(ReviewExplanationInput, bad_luck_payload),
        [],
        _review_eligibility(CorridorBreachSeverity.SEVERE),
    )
    assert bad_luck.primary_failure_class is None
    assert bad_luck.resolution is ReviewResolutionClass.BAD_LUCK
