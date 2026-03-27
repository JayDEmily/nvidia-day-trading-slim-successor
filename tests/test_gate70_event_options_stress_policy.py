"""Gate 70 event and options-stress policy integrity checks."""

from __future__ import annotations

import json
from pathlib import Path

from nvda_desk.schemas.cognition import ReviewExplanationOutput
from nvda_desk.schemas.config import EventOptionsStressAuthorityResponse
from nvda_desk.schemas.review import EventOptionsStressPolicySurface
from nvda_desk.schemas.state_policy import (
    EventOptionsBehaviourClass,
    EventOptionsStressAuthorityPacket,
    EventOptionsStressFamily,
    EventOptionsStressPolicyRecord,
    EventOptionsStressState,
    MutableRuntimeSurface,
    PolicyEffectType,
)
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


def test_gate70_status_closeout_and_leaf_progress_are_recorded() -> None:
    gates_text = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert "## Gate 70 — Event and options-stress policy matrix\n\nStatus: complete on `main`" in gates_text
    assert "### Gate 70 closeout note" in gates_text
    assert leaves["completed_gate_ids"][:12] == [
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
    ]
    assert successor_pack_position(leaves["active_gate"]) >= 71

    gate70 = [leaf for leaf in leaves["leaves"] if leaf["gate"] == "Gate 70"]
    assert len(gate70) == 6
    assert all(leaf["status"] == "complete" for leaf in gate70)


def test_gate70_docs_freeze_event_and_options_stress_law() -> None:
    normative = NORMATIVE.read_text(encoding="utf-8")
    operating_model = OPERATING_MODEL.read_text(encoding="utf-8")
    domain_model = DOMAIN_MODEL.read_text(encoding="utf-8")
    guardrails = GUARDRAILS.read_text(encoding="utf-8")

    assert "## Event/options-stress policy law" in normative
    assert "event/options-stress states are `event_imminent`, `event_live`, `event_suppressed`, `negative_gamma_stress`, `pin_risk`, and `expiry_distortion`" in normative
    assert "the matrix must state what is suppressed, degraded, widened, capped, hedged, or blocked under each state" in normative

    assert "## Gate 70 event/options-stress policy authority" in operating_model
    assert "the matrix covers imminent/live event risk, event suppression, negative gamma stress, pin risk, and expiry distortion" in operating_model

    assert "### 5b. Event/options-stress policy objects" in domain_model
    assert "**Event/options-stress posture must come from the frozen matrix, not improvised event lore or gamma hand-waving.**" in guardrails


def test_gate70_schema_surface_exposes_bounded_matrix_and_review_hook() -> None:
    assert [item.value for item in EventOptionsStressState] == [
        "event_imminent",
        "event_live",
        "event_suppressed",
        "negative_gamma_stress",
        "pin_risk",
        "expiry_distortion",
    ]
    assert [item.value for item in EventOptionsStressFamily] == [
        "company_event",
        "macro_event",
        "policy_event",
        "venue_event",
        "options_geometry",
    ]
    assert [item.value for item in PolicyEffectType] == ["suppress", "degrade", "widen", "cap", "block", "hedge"]
    assert [item.value for item in EventOptionsBehaviourClass] == [
        "tightened_thresholds",
        "hedged_only",
        "size_capped",
        "watch_only",
        "hard_block",
    ]

    record = EventOptionsStressPolicyRecord(
        state=EventOptionsStressState.NEGATIVE_GAMMA_STRESS,
        event_families=[EventOptionsStressFamily.OPTIONS_GEOMETRY],
        mutable_surface_targets=[MutableRuntimeSurface.MAX_RISK_PER_TRADE, MutableRuntimeSurface.HEDGE_REQUIRED],
        effect_types=[PolicyEffectType.CAP, PolicyEffectType.HEDGE],
        behaviour_class=EventOptionsBehaviourClass.HEDGED_ONLY,
        notes=["Negative gamma stress caps fresh risk and requires a hedge overlay."],
    )
    authority = EventOptionsStressAuthorityResponse(
        authority=EventOptionsStressAuthorityPacket(
            states=list(EventOptionsStressState),
            families=list(EventOptionsStressFamily),
            effect_types=list(PolicyEffectType),
            behaviour_classes=list(EventOptionsBehaviourClass),
            policy_records=[record],
        )
    )
    surface = EventOptionsStressPolicySurface(
        active_states=[EventOptionsStressState.EVENT_IMMINENT, EventOptionsStressState.NEGATIVE_GAMMA_STRESS],
        behaviour_class=EventOptionsBehaviourClass.HEDGED_ONLY,
        effect_types=[PolicyEffectType.CAP, PolicyEffectType.HEDGE],
    )
    review = ReviewExplanationOutput(summary="event/options matrix bounded", review_packet={}, event_options_stress_policy=surface)

    assert authority.authority.policy_records[0].behaviour_class is EventOptionsBehaviourClass.HEDGED_ONLY
    assert review.event_options_stress_policy == surface


def test_gate70_vocabulary_terms_are_generated_and_committed() -> None:
    committed = VOCAB_PATH.read_text(encoding="utf-8")
    generated = build_document().to_json_text()

    assert committed == generated
    vocab = json.loads(committed)
    slugs = {entry["canonical_slug"] for entry in vocab["entries"]}
    assert {"event_options_stress_policy", "phase_carry_policy"}.issubset(slugs)
