"""Gate 61 non-action, conflict, and discretion integrity checks."""

from __future__ import annotations

import json
from pathlib import Path

from nvda_desk.schemas.cognition import ReviewExplanationOutput
from nvda_desk.schemas.config import NonActionAuthorityResponse
from nvda_desk.schemas.review import ReviewGovernanceSurface
from nvda_desk.schemas.state_policy import (
    DegradationStep,
    NonActionAuthorityPacket,
    NonActionClass,
    OverrideDisposition,
    SignalConflictClass,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
GATES = REPO_ROOT / "docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v6.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v6.json"
NORMATIVE = REPO_ROOT / "docs/01_NORMATIVE.md"
OPERATING_MODEL = REPO_ROOT / "docs/02_OPERATING_MODEL.md"
GUARDRAILS = REPO_ROOT / "docs/05_GUARDRAILS.md"
VOCAB_PATH = REPO_ROOT / "docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json"


def test_gate61_status_closeout_and_leaf_progress_are_recorded() -> None:
    gates_text = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert "## Gate 61 — Non-action, conflict hierarchy, and discretion boundaries\n\nStatus: complete on `main`" in gates_text
    assert "### Gate 61 closeout note" in gates_text
    assert leaves["execution_status"] == "gate_61_complete_on_main_successor_pack_active_from_gate_62"
    assert leaves["completed_gate_ids"] == ["Gate 59", "Gate 60", "Gate 61"]
    assert leaves["active_gate"] == "Gate 62"

    gate61 = [leaf for leaf in leaves["leaves"] if leaf["gate"] == "Gate 61"]
    assert len(gate61) == 5
    assert all(leaf["status"] == "complete" for leaf in gate61)


def test_gate61_docs_forbid_forced_action_and_runtime_discretion() -> None:
    normative = NORMATIVE.read_text(encoding="utf-8")
    operating_model = OPERATING_MODEL.read_text(encoding="utf-8")
    guardrails = GUARDRAILS.read_text(encoding="utf-8")

    assert "## Non-action, conflict, and discretion law" in normative
    assert "non-action is a first-class valid runtime outcome" in normative
    assert "discretionary runtime override is forbidden" in normative

    assert "## Gate 61 non-action and conflict authority" in operating_model
    assert "The deterministic desk is allowed to decide **not** to participate." in operating_model
    assert "stand-down remains first-class" in operating_model

    assert "**No forced-action bias; stand-down is a valid governed outcome.**" in guardrails
    assert "**Discretionary runtime override is forbidden.**" in guardrails


def test_gate61_schema_exposes_review_governance_surface() -> None:
    assert [item.value for item in NonActionClass] == [
        "data_quality_stand_down",
        "temporal_stand_down",
        "event_risk_stand_down",
        "regime_stand_down",
        "options_flow_stand_down",
        "posture_risk_stand_down",
        "eligibility_stand_down",
        "execution_readiness_stand_down",
    ]
    assert [item.value for item in SignalConflictClass] == [
        "observation_divergence",
        "confirmation_conflict",
        "posture_degradation",
        "hard_veto_conflict",
    ]
    assert [item.value for item in DegradationStep] == [
        "normal",
        "confirmation_tightened",
        "confidence_reduced",
        "size_reduced",
        "watch_only",
        "stand_down",
        "veto",
    ]
    assert [item.value for item in OverrideDisposition] == [
        "not_applicable",
        "audit_annotation_only",
        "human_review_release_only",
        "forbidden",
    ]

    governance = ReviewGovernanceSurface(
        stand_down_class=NonActionClass.POSTURE_RISK_STAND_DOWN,
        conflict_classes=[SignalConflictClass.POSTURE_DEGRADATION],
        degradation_step=DegradationStep.SIZE_REDUCED,
        override_disposition=OverrideDisposition.AUDIT_ANNOTATION_ONLY,
        override_audit_notes=["manual note captured"],
    )
    review = ReviewExplanationOutput(summary="held fire", review_packet={}, review_governance=governance)
    assert review.review_governance == governance

    authority = NonActionAuthorityResponse(
        authority=NonActionAuthorityPacket(
            non_action_classes=list(NonActionClass),
            conflict_classes=list(SignalConflictClass),
            degradation_steps=list(DegradationStep),
            override_dispositions=list(OverrideDisposition),
        )
    )
    assert authority.authority.override_dispositions[-1] is OverrideDisposition.FORBIDDEN


def test_gate61_vocabulary_terms_are_present() -> None:
    vocab = json.loads(VOCAB_PATH.read_text(encoding="utf-8"))
    slugs = {entry["canonical_slug"] for entry in vocab["entries"]}
    assert {"stand_down_class", "conflict_class", "degradation_step", "override_disposition"}.issubset(slugs)
