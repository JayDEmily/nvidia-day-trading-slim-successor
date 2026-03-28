"""Gate 64 candidate and adjudication governance integrity checks."""

from __future__ import annotations

import json
from pathlib import Path

from nvda_desk.schemas.cognition import ReviewExplanationOutput
from nvda_desk.schemas.config import CandidateGovernanceAuthorityResponse
from nvda_desk.schemas.review import CandidateGovernanceSurface
from nvda_desk.schemas.state_policy import (
    AdjudicationDisposition,
    CandidateComparisonOutcome,
    CandidateGovernanceAuthorityPacket,
    CandidateLedgerRecord,
    CandidateRole,
    CandidateSetShape,
)
from scripts.build_canonical_vocabulary import build_document

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


def test_gate64_status_closeout_and_leaf_progress_are_recorded() -> None:
    gates_text = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert (
        "## Gate 64 — Candidate, champion, challenger, and adjudication governance\n\nStatus: complete on `main`"
        in gates_text
    )
    assert "### Gate 64 closeout note" in gates_text

    gate64 = [leaf for leaf in leaves["leaves"] if leaf["gate"] == "Gate 64"]
    assert len(gate64) == 5
    assert all(leaf["status"] == "complete" for leaf in gate64)


def test_gate64_docs_freeze_candidate_roles_and_reserved_adjudication() -> None:
    normative = NORMATIVE.read_text(encoding="utf-8")
    operating_model = OPERATING_MODEL.read_text(encoding="utf-8")
    domain_model = DOMAIN_MODEL.read_text(encoding="utf-8")
    guardrails = GUARDRAILS.read_text(encoding="utf-8")

    assert "## Candidate and adjudication law" in normative
    assert (
        "candidate roles are limited to champion, shadow challenger, dormant candidate, and retired candidate"
        in normative
    )
    assert "at least one reserved adjudication span remains untouched" in normative
    assert "research reset rather than another runtime tweak" in normative

    assert "## Gate 64 candidate governance authority" in operating_model
    assert (
        "champion, shadow challenger, dormant candidate, and retired candidate are the only governed role labels"
        in operating_model
    )
    assert (
        "retain champion, promote challenger, demote to dormant, retire candidate, or reset to research"
        in operating_model
    )

    assert "### 4e. Candidate governance and adjudication objects" in domain_model
    assert (
        "**Reserved adjudication spans must stay protected until governed final comparison consumes them.**"
        in guardrails
    )


def test_gate64_schema_surface_exposes_candidate_roles_and_ledger_hooks() -> None:
    assert [item.value for item in CandidateRole] == [
        "champion",
        "shadow_challenger",
        "dormant_candidate",
        "retired_candidate",
    ]
    assert [item.value for item in CandidateComparisonOutcome] == [
        "retain_champion",
        "promote_challenger",
        "demote_to_dormant",
        "retire_candidate",
        "reset_to_research",
    ]
    assert [item.value for item in AdjudicationDisposition] == [
        "reserved_untouched",
        "released_for_final_comparison",
        "consumed_recorded",
    ]

    shape = CandidateSetShape(
        max_candidate_count=4,
        max_shadow_challengers=2,
        allow_dormant_candidates=True,
        allow_retired_candidates=True,
        reserved_adjudication_spans=1,
    )
    ledger = CandidateLedgerRecord(
        candidate_id="candidate_a", role=CandidateRole.CHAMPION
    )
    governance = CandidateGovernanceSurface(
        candidate_shape=shape,
        champion_candidate_id="candidate_a",
        shadow_challenger_ids=["candidate_b"],
        dormant_candidate_ids=["candidate_c"],
        retired_candidate_ids=["candidate_d"],
        comparison_outcome=CandidateComparisonOutcome.RETAIN_CHAMPION,
        adjudication_disposition=AdjudicationDisposition.RESERVED_UNTOUCHED,
    )
    review = ReviewExplanationOutput(
        summary="champion retained", review_packet={}, candidate_governance=governance
    )
    assert review.candidate_governance == governance
    assert ledger.role is CandidateRole.CHAMPION

    authority = CandidateGovernanceAuthorityResponse(
        authority=CandidateGovernanceAuthorityPacket(
            allowed_roles=list(CandidateRole),
            comparison_outcomes=list(CandidateComparisonOutcome),
            adjudication_dispositions=list(AdjudicationDisposition),
            candidate_shape=shape,
        )
    )
    assert authority.authority.candidate_shape.max_candidate_count == 4


def test_gate64_vocabulary_terms_are_generated_and_committed() -> None:
    committed = VOCAB_PATH.read_text(encoding="utf-8")
    generated = build_document().to_json_text()

    assert committed == generated
    vocab = json.loads(committed)
    slugs = {entry["canonical_slug"] for entry in vocab["entries"]}
    assert {"candidate_role", "adjudication_disposition"}.issubset(slugs)
