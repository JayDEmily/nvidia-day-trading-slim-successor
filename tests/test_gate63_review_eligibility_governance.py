"""Gate 63 review-eligibility governance integrity checks."""

from __future__ import annotations

import json
from pathlib import Path

from nvda_desk.schemas.cognition import ReviewExplanationOutput
from nvda_desk.schemas.config import ReviewEligibilityAuthorityResponse
from nvda_desk.schemas.review import ReviewEligibilitySurface
from nvda_desk.schemas.state_policy import (
    CorridorBreachSeverity,
    ReviewChangeBudget,
    ReviewEligibilityAuthorityPacket,
    ReviewEvidenceBlock,
    ReviewOutcome,
    ReviewSurfaceClass,
    ReviewTriggerClass,
)
from scripts.build_canonical_vocabulary import build_document

REPO_ROOT = Path(__file__).resolve().parents[1]
GATES = REPO_ROOT / "docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v6.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v6.json"
NORMATIVE = REPO_ROOT / "docs/01_NORMATIVE.md"
OPERATING_MODEL = REPO_ROOT / "docs/02_OPERATING_MODEL.md"
DOMAIN_MODEL = REPO_ROOT / "docs/03_DOMAIN_MODEL.md"
GUARDRAILS = REPO_ROOT / "docs/05_GUARDRAILS.md"
VOCAB_PATH = REPO_ROOT / "docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json"


def test_gate63_status_closeout_and_leaf_progress_are_recorded() -> None:
    gates_text = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert "## Gate 63 — Review-eligibility governance\n\nStatus: complete on `main`" in gates_text
    assert "### Gate 63 closeout note" in gates_text

    gate63 = [leaf for leaf in leaves["leaves"] if leaf["gate"] == "Gate 63"]
    assert len(gate63) == 5
    assert all(leaf["status"] == "complete" for leaf in gate63)


def test_gate63_docs_freeze_evidence_floors_and_no_change_review() -> None:
    normative = NORMATIVE.read_text(encoding="utf-8")
    operating_model = OPERATING_MODEL.read_text(encoding="utf-8")
    domain_model = DOMAIN_MODEL.read_text(encoding="utf-8")
    guardrails = GUARDRAILS.read_text(encoding="utf-8")

    assert "## Review-eligibility law" in normative
    assert (
        "review eligibility requires a governed evidence block with explicit minimum floors"
        in normative
    )
    assert "review may conclude `review_not_eligible` or `review_no_change`" in normative
    assert (
        "bounded adjustment request, candidate replacement request, research reset, and missing-module suspicion"
        in normative
    )

    assert "## Gate 63 review-eligibility authority" in operating_model
    assert (
        "review triggers are bounded to corridor breaches, persistence failures, or coverage collapse"
        in operating_model
    )
    assert "every review outcome carries a bounded change budget" in operating_model

    assert "### 4d. Review-eligibility governance objects" in domain_model
    assert (
        "**Review eligibility requires governed evidence floors and may conclude no change.**"
        in guardrails
    )


def test_gate63_schema_surface_exposes_evidence_triggers_and_outcomes() -> None:
    assert [item.value for item in ReviewSurfaceClass] == [
        "coefficient_group",
        "policy_surface",
    ]
    assert [item.value for item in ReviewTriggerClass] == [
        "material_corridor_breach",
        "severe_corridor_breach",
        "persistence_failure",
        "coverage_collapse",
    ]
    assert [item.value for item in ReviewOutcome] == [
        "review_not_eligible",
        "review_no_change",
        "bounded_adjustment_request",
        "candidate_replacement_request",
        "research_reset",
        "missing_module_suspicion",
    ]
    assert [item.value for item in ReviewChangeBudget] == [
        "none",
        "bounded_single_surface",
        "bounded_multi_surface",
        "candidate_swap_only",
        "research_only",
    ]

    evidence = ReviewEvidenceBlock(
        surface_class=ReviewSurfaceClass.COEFFICIENT_GROUP,
        surface_id="entry_gate_group",
        sample_count=24,
        session_count=12,
        event_slice_count=3,
        regime_slice_count=4,
        coverage_ratio=0.78,
        breach_severity=CorridorBreachSeverity.MATERIAL,
        persistence_blocks=3,
        hysteresis_passed=True,
    )
    eligibility = ReviewEligibilitySurface(
        evidence_block=evidence,
        trigger_classes=[
            ReviewTriggerClass.MATERIAL_CORRIDOR_BREACH,
            ReviewTriggerClass.PERSISTENCE_FAILURE,
        ],
        eligible=True,
        governed_outcome=ReviewOutcome.BOUNDED_ADJUSTMENT_REQUEST,
        change_budget=ReviewChangeBudget.BOUNDED_SINGLE_SURFACE,
    )
    review = ReviewExplanationOutput(
        summary="review needed", review_packet={}, review_eligibility=eligibility
    )
    assert review.review_eligibility == eligibility

    authority = ReviewEligibilityAuthorityResponse(
        authority=ReviewEligibilityAuthorityPacket(
            surface_classes=list(ReviewSurfaceClass),
            trigger_classes=list(ReviewTriggerClass),
            outcomes=list(ReviewOutcome),
            change_budgets=list(ReviewChangeBudget),
        )
    )
    assert authority.authority.outcomes[1] is ReviewOutcome.REVIEW_NO_CHANGE


def test_gate63_vocabulary_terms_are_generated_and_committed() -> None:
    committed = VOCAB_PATH.read_text(encoding="utf-8")
    generated = build_document().to_json_text()

    assert committed == generated
    vocab = json.loads(committed)
    slugs = {entry["canonical_slug"] for entry in vocab["entries"]}
    assert {"review_evidence_block", "review_outcome"}.issubset(slugs)
