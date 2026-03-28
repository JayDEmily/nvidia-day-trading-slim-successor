"""Gate 69 phase-of-day and carryover policy integrity checks."""

from __future__ import annotations

import json
from pathlib import Path

from nvda_desk.schemas.cognition import ReviewExplanationOutput, RuntimeStateVector
from nvda_desk.schemas.config import PhaseCarryoverPolicyAuthorityResponse
from nvda_desk.schemas.review import PhaseCarryoverPolicySurface
from nvda_desk.schemas.risk import (
    CarryHorizonState,
    DayPhaseState,
    PhaseBehaviourClass,
    PhaseCarryoverPolicyAuthorityPacket,
    PhaseCarryPolicyRecord,
    PhaseNoActionBias,
)
from nvda_desk.schemas.state_policy import MutableRuntimeSurface
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


def test_gate69_status_closeout_and_leaf_progress_are_recorded() -> None:
    gates_text = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert (
        "## Gate 69 — Phase-of-day and carryover policy matrix\n\nStatus: complete on `main`"
        in gates_text
    )
    assert "### Gate 69 closeout note" in gates_text
    assert leaves["completed_gate_ids"][:11] == [
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
    ]
    assert successor_pack_position(leaves["active_gate"]) >= 70

    gate69 = [leaf for leaf in leaves["leaves"] if leaf["gate"] == "Gate 69"]
    assert len(gate69) == 6
    assert all(leaf["status"] == "complete" for leaf in gate69)


def test_gate69_docs_freeze_phase_carry_and_no_action_law() -> None:
    normative = NORMATIVE.read_text(encoding="utf-8")
    operating_model = OPERATING_MODEL.read_text(encoding="utf-8")
    domain_model = DOMAIN_MODEL.read_text(encoding="utf-8")
    guardrails = GUARDRAILS.read_text(encoding="utf-8")

    assert "## Phase-of-day and carryover policy law" in normative
    assert (
        "approved day-phase states are `opening_disorder`, `opening_resolution`, `trend_window`, `midday_compression`, `late_session`, `close_auction`, and `post_close`"
        in normative
    )
    assert (
        "carry-horizon states are `intraday_only`, `overnight_setup`, `weekend_setup`, and `event_carry_setup`"
        in normative
    )
    assert (
        "midday compression and late-session carry preparation may prefer or require no-action"
        in normative
    )

    assert "## Gate 69 phase-and-carryover policy authority" in operating_model
    assert "the matrix only targets approved mutable runtime surfaces" in operating_model

    assert "### 5a. Phase-and-carryover policy objects" in domain_model
    assert (
        "**Phase/carryover policy may change bounded posture, but it must not force action just because the clock moved.**"
        in guardrails
    )


def test_gate69_schema_surface_extends_state_vector_and_policy_matrix() -> None:
    assert [item.value for item in DayPhaseState] == [
        "opening_disorder",
        "opening_resolution",
        "trend_window",
        "midday_compression",
        "late_session",
        "close_auction",
        "post_close",
    ]
    assert [item.value for item in CarryHorizonState] == [
        "intraday_only",
        "overnight_setup",
        "weekend_setup",
        "event_carry_setup",
    ]
    assert [item.value for item in PhaseBehaviourClass] == [
        "normal_operation",
        "tightened_thresholds",
        "compressed_deployment",
        "carry_preparation",
        "no_action_preferred",
    ]
    assert [item.value for item in PhaseNoActionBias] == [
        "neutral",
        "preferred",
        "required",
    ]

    record = PhaseCarryPolicyRecord(
        day_phase=DayPhaseState.MIDDAY_COMPRESSION,
        carry_horizon=CarryHorizonState.INTRADAY_ONLY,
        behaviour_class=PhaseBehaviourClass.NO_ACTION_PREFERRED,
        no_action_bias=PhaseNoActionBias.PREFERRED,
        mutable_surface_targets=[
            MutableRuntimeSurface.TARGET_FRESH_DEPLOYABLE_PCT,
            MutableRuntimeSurface.ENTRY_GATE_SCORE_FLOOR,
        ],
        notes=["Midday compression prefers waiting over forcing a fresh deployment."],
    )
    authority = PhaseCarryoverPolicyAuthorityResponse(
        authority=PhaseCarryoverPolicyAuthorityPacket(
            day_phases=list(DayPhaseState),
            carry_horizon_states=list(CarryHorizonState),
            behaviour_classes=list(PhaseBehaviourClass),
            no_action_biases=list(PhaseNoActionBias),
            policy_records=[record],
        )
    )
    surface = PhaseCarryoverPolicySurface(
        day_phase_state=DayPhaseState.MIDDAY_COMPRESSION,
        carry_horizon_state=CarryHorizonState.INTRADAY_ONLY,
        behaviour_class=PhaseBehaviourClass.NO_ACTION_PREFERRED,
        no_action_bias=PhaseNoActionBias.PREFERRED,
    )
    review = ReviewExplanationOutput(
        summary="phase policy bounded", review_packet={}, phase_carry_policy=surface
    )

    assert {"day_phase_state", "carry_horizon_state"}.issubset(set(RuntimeStateVector.model_fields))
    assert authority.authority.policy_records[0].no_action_bias is PhaseNoActionBias.PREFERRED
    assert review.phase_carry_policy == surface


def test_gate69_vocabulary_terms_are_generated_and_committed() -> None:
    committed = VOCAB_PATH.read_text(encoding="utf-8")
    generated = build_document().to_json_text()

    assert committed == generated
    vocab = json.loads(committed)
    slugs = {entry["canonical_slug"] for entry in vocab["entries"]}
    assert {"phase_carry_policy", "precursor_universe"}.issubset(slugs)
