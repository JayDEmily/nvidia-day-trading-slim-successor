"""Gate 62 stability metric and corridor integrity checks."""

from __future__ import annotations

import json
from pathlib import Path

from nvda_desk.schemas.cognition import ReviewExplanationOutput
from nvda_desk.schemas.config import StabilityAuthorityResponse
from nvda_desk.schemas.state_policy import (
    BehaviourStabilityState,
    CorridorBounds,
    CorridorBreachSeverity,
    CorridorZone,
    CoverageSliceClass,
    CoverageSliceScore,
    MetricTriggerMode,
    PersistenceHysteresisSpec,
    RuntimeSurfaceClass,
    ScorecardAxis,
    StabilityAuthorityPacket,
    StabilityMetricFamily,
    StabilityMetricObservation,
    SurfaceStabilityScorecard,
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


def test_gate62_status_closeout_and_leaf_progress_are_recorded() -> None:
    gates_text = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert (
        "## Gate 62 — Stability-metric algebra and corridor schema\n\nStatus: complete on `main`"
        in gates_text
    )
    assert "### Gate 62 closeout note" in gates_text
    assert leaves["execution_status"].startswith("gate_") and (
        "_successor_pack_active_from_gate_" in leaves["execution_status"]
        or "_successor_pack_closed_after_gate_" in leaves["execution_status"]
    )
    assert leaves["completed_gate_ids"][:6] == [
        "Gate 59",
        "Gate 60",
        "Gate 61",
        "Gate 62",
        "Gate 63",
        "Gate 64",
    ]
    assert successor_pack_position(leaves["active_gate"]) >= 65

    gate62 = [leaf for leaf in leaves["leaves"] if leaf["gate"] == "Gate 62"]
    assert len(gate62) == 6
    assert all(leaf["status"] == "complete" for leaf in gate62)


def test_gate62_docs_freeze_scorecards_corridors_and_persistence() -> None:
    normative = NORMATIVE.read_text(encoding="utf-8")
    operating_model = OPERATING_MODEL.read_text(encoding="utf-8")
    domain_model = DOMAIN_MODEL.read_text(encoding="utf-8")
    guardrails = GUARDRAILS.read_text(encoding="utf-8")

    assert "## Stability corridor and scorecard law" in normative
    assert (
        "canonical scorecard axes are diagnosis quality, decision quality, economic quality, execution quality, and posture-law fidelity"
        in normative
    )
    assert (
        "every governed stability surface is assessed against a corridor algebra with target, tolerated-drift, and breach zones"
        in normative
    )
    assert "a surface may be `breathing`, `drifting`, or `decaying`" in normative

    assert "## Gate 62 stability authority" in operating_model
    assert (
        "metric families stay explicit: level, slope, acceleration, persistence, dispersion, corridor width, breach frequency, breach severity, and coverage"
        in operating_model
    )
    assert "persistence and hysteresis prevent one noisy block" in operating_model

    assert "### 4c. Stability metric and corridor objects" in domain_model
    assert (
        "**Stability must be judged against frozen scorecards and corridor zones, not one-off outcome snapshots.**"
        in guardrails
    )


def test_gate62_schema_surface_matches_frozen_authority() -> None:
    assert [item.value for item in ScorecardAxis] == [
        "diagnosis_quality",
        "decision_quality",
        "economic_quality",
        "execution_quality",
        "posture_law_fidelity",
    ]
    assert [item.value for item in StabilityMetricFamily] == [
        "level",
        "slope",
        "acceleration",
        "persistence",
        "dispersion",
        "corridor_width",
        "breach_frequency",
        "breach_severity",
        "coverage",
    ]
    assert [item.value for item in MetricTriggerMode] == [
        "descriptive_only",
        "review_trigger",
    ]
    assert [item.value for item in CorridorZone] == [
        "target",
        "tolerated_drift",
        "breach",
    ]
    assert [item.value for item in CorridorBreachSeverity] == [
        "none",
        "drifting",
        "material",
        "severe",
    ]
    assert [item.value for item in BehaviourStabilityState] == [
        "breathing",
        "drifting",
        "decaying",
    ]
    assert [item.value for item in CoverageSliceClass] == [
        "event_class",
        "regime_slice",
        "session_slice",
    ]

    scorecard = SurfaceStabilityScorecard(
        surface_id="entry_gate_score_floor",
        surface_class=RuntimeSurfaceClass.STATE_CONDITIONED_MODIFIER,
        metric_observations=[
            StabilityMetricObservation(
                axis=ScorecardAxis.DECISION_QUALITY,
                metric_family=StabilityMetricFamily.SLOPE,
                trigger_mode=MetricTriggerMode.REVIEW_TRIGGER,
                value=-0.12,
            )
        ],
        corridor=CorridorBounds(
            central_tendency=0.0,
            tolerated_spread=0.1,
            target_low=-0.05,
            target_high=0.05,
            drift_low=-0.1,
            drift_high=0.1,
            breach_low=-0.2,
            breach_high=0.2,
        ),
        breach_severity=CorridorBreachSeverity.DRIFTING,
        behaviour_state=BehaviourStabilityState.DRIFTING,
        persistence=PersistenceHysteresisSpec(
            minimum_blocks=3,
            confirmation_blocks=2,
            recovery_blocks=2,
            cooldown_blocks=1,
        ),
        coverage_slices=[
            CoverageSliceScore(
                slice_class=CoverageSliceClass.EVENT_CLASS,
                slice_label="earnings",
                observation_count=8,
                coverage_ratio=0.75,
            )
        ],
    )
    review = ReviewExplanationOutput(
        summary="stable enough", review_packet={}, stability_scorecards=[scorecard]
    )
    assert review.stability_scorecards[0].behaviour_state is BehaviourStabilityState.DRIFTING

    authority = StabilityAuthorityResponse(
        authority=StabilityAuthorityPacket(
            scorecard_axes=list(ScorecardAxis),
            metric_families=list(StabilityMetricFamily),
            trigger_modes=list(MetricTriggerMode),
            corridor_zones=list(CorridorZone),
            breach_severities=list(CorridorBreachSeverity),
            behaviour_states=list(BehaviourStabilityState),
            coverage_slice_classes=list(CoverageSliceClass),
        )
    )
    assert authority.authority.corridor_zones[-1] is CorridorZone.BREACH


def test_gate62_vocabulary_terms_are_generated_and_committed() -> None:
    committed = VOCAB_PATH.read_text(encoding="utf-8")
    generated = build_document().to_json_text()

    assert committed == generated
    vocab = json.loads(committed)
    slugs = {entry["canonical_slug"] for entry in vocab["entries"]}
    assert {"stability_scorecard", "corridor_zone", "review_evidence_block"}.issubset(slugs)
