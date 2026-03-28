"""Gate 83 review-governance surface builder checks."""

from __future__ import annotations

from nvda_desk.config import Settings
from nvda_desk.schemas.review import CandidateComparisonContext, PromotionEvidencePacket
from nvda_desk.schemas.state_policy import (
    AdjudicationDisposition,
    CandidateComparisonOutcome,
    CandidateSetShape,
    CorridorBreachSeverity,
    ReviewChangeBudget,
    ReviewOutcome,
    ReviewTriggerClass,
)
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.services.review_explanation import ReviewExplanationService
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture


def test_gate83_runtime_emits_review_eligibility_stability_and_reserved_candidate_governance() -> (
    None
):
    fixture = supportive_runtime_fixture()
    result = DeskCognitionRuntime(Settings()).run(
        temporal_input=fixture.temporal_input,
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )

    assert result.review.review_eligibility is not None
    assert result.review.review_eligibility.eligible is True
    assert (
        result.review.review_eligibility.governed_outcome
        is ReviewOutcome.BOUNDED_ADJUSTMENT_REQUEST
    )
    assert (
        result.review.review_eligibility.change_budget is ReviewChangeBudget.BOUNDED_SINGLE_SURFACE
    )
    assert set(result.review.review_eligibility.trigger_classes) >= {
        ReviewTriggerClass.MATERIAL_CORRIDOR_BREACH,
        ReviewTriggerClass.SEVERE_CORRIDOR_BREACH,
    }

    assert result.review.stability_scorecards
    scorecard = result.review.stability_scorecards[0]
    assert scorecard.breach_severity is CorridorBreachSeverity.SEVERE
    assert scorecard.coverage_slices

    assert result.review.candidate_governance is not None
    assert (
        result.review.candidate_governance.adjudication_disposition
        is AdjudicationDisposition.RESERVED_UNTOUCHED
    )
    assert result.review.candidate_governance.comparison_outcome is None


def test_gate83_candidate_governance_builder_releases_comparison_when_promotion_evidence_is_ready() -> (
    None
):
    surface = ReviewExplanationService()._candidate_governance(
        PromotionEvidencePacket(
            ready_for_candidate_review=True,
            required_sections=[
                "event_lineage_keys",
                "precursor_lineage_keys",
                "modifier_policy_ids",
            ],
            missing_sections=[],
            notes=["gate83_test_ready"],
        ),
        comparison_context=CandidateComparisonContext(
            candidate_shape=CandidateSetShape(
                max_candidate_count=2,
                max_shadow_challengers=1,
                allow_dormant_candidates=True,
                allow_retired_candidates=True,
                reserved_adjudication_spans=1,
            ),
            champion_candidate_id="candidate_a",
            shadow_challenger_ids=["candidate_b"],
            comparison_outcome=CandidateComparisonOutcome.RETAIN_CHAMPION,
            adjudication_disposition=AdjudicationDisposition.RELEASED_FOR_FINAL_COMPARISON,
        ),
    )

    assert surface.adjudication_disposition is AdjudicationDisposition.RELEASED_FOR_FINAL_COMPARISON
    assert surface.comparison_outcome is CandidateComparisonOutcome.RETAIN_CHAMPION
    assert surface.champion_candidate_id == "candidate_a"
    assert surface.shadow_challenger_ids == ["candidate_b"]


def test_gate83_candidate_governance_builder_stays_reserved_without_comparison_context() -> None:
    surface = ReviewExplanationService()._candidate_governance(
        PromotionEvidencePacket(
            ready_for_candidate_review=True,
            required_sections=[
                "event_lineage_keys",
                "precursor_lineage_keys",
                "modifier_policy_ids",
            ],
            missing_sections=[],
            notes=["gate83_ready_but_no_context"],
        )
    )

    assert surface.adjudication_disposition is AdjudicationDisposition.RESERVED_UNTOUCHED
    assert surface.comparison_outcome is None
    assert surface.champion_candidate_id is None
