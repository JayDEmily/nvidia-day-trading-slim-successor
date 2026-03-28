"""Gate 78 runtime integration integrity checks."""

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
from nvda_desk.schemas.review import ReviewFailureClass, ReviewResolutionClass
from nvda_desk.schemas.state_policy import (
    ModifierPriorityBand,
    ModifierRuntimePacket,
    MutableRuntimeSurface,
    ResolvedRuntimeSurfaceValue,
)
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.testing.cognition_fixtures import (
    stressed_runtime_fixture,
    supportive_runtime_fixture,
)
from scripts.build_canonical_vocabulary import build_document
from tests._successor_pack_helpers import successor_pack_position

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


def _tightened_precursor_packet() -> PrecursorRuntimePacket:
    return PrecursorRuntimePacket(
        requested_at=datetime(2026, 3, 23, 19, 20, tzinfo=UTC),
        stitched_order=[
            PrecursorVenueUniverse.CFFEX_INDEX_FUTURES_COMPLEX,
            PrecursorVenueUniverse.JPX_CASH_INDEX_COMPLEX,
        ],
        active_venues=[
            PrecursorVenueUniverse.CFFEX_INDEX_FUTURES_COMPLEX,
            PrecursorVenueUniverse.JPX_CASH_INDEX_COMPLEX,
        ],
        missing_venues=[PrecursorVenueUniverse.HKEX_CASH_INDEX_COMPLEX],
        derived_fields=[DerivedPrecursorField.PRECURSOR_PRESSURE_SCORE],
        contradiction_class=PrecursorContradictionClass.NONE,
        posture_state=PrecursorPostureState.TIGHTENED_POSTURE,
        fallback_dispositions=[PrecursorFallbackDisposition.CONTINUE_NORMALLY],
        lineage_keys=["precursor:cffex:1", "precursor:jpx:1"],
    )


def _unresolved_precursor_packet() -> PrecursorRuntimePacket:
    return PrecursorRuntimePacket(
        requested_at=datetime(2026, 3, 23, 14, 30, tzinfo=UTC),
        stitched_order=[PrecursorVenueUniverse.CFFEX_INDEX_FUTURES_COMPLEX],
        active_venues=[PrecursorVenueUniverse.CFFEX_INDEX_FUTURES_COMPLEX],
        missing_venues=[
            PrecursorVenueUniverse.JPX_CASH_INDEX_COMPLEX,
            PrecursorVenueUniverse.HKEX_CASH_INDEX_COMPLEX,
        ],
        derived_fields=[DerivedPrecursorField.FUTURES_CASH_DIVERGENCE_SCORE],
        contradiction_class=PrecursorContradictionClass.BROAD_CROSS_VENUE_CONFLICT,
        posture_state=PrecursorPostureState.UNRESOLVED_CONTEXT,
        fallback_dispositions=[
            PrecursorFallbackDisposition.REQUIRE_STAND_DOWN_PRESSURE
        ],
        lineage_keys=["precursor:cffex:hard-block"],
    )


def test_gate78_status_closeout_and_leaf_progress_are_recorded() -> None:
    gates_text = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert (
        "## Gate 78 — Runtime integration of state-conditioned modifiers\n\nStatus: complete on `main`"
        in gates_text
    )
    assert "### Gate 78 closeout note" in gates_text
    assert leaves["completed_gate_ids"][:20] == [
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
        "Gate 77",
        "Gate 78",
    ]
    assert successor_pack_position(leaves["active_gate"]) >= 79
    gate78 = [leaf for leaf in leaves["leaves"] if leaf["gate"] == "Gate 78"]
    assert len(gate78) == 5
    assert all(leaf["status"] == "complete" for leaf in gate78)


def test_gate78_docs_freeze_runtime_modifier_integration_law() -> None:
    normative = NORMATIVE.read_text(encoding="utf-8")
    operating_model = OPERATING_MODEL.read_text(encoding="utf-8")
    domain_model = DOMAIN_MODEL.read_text(encoding="utf-8")
    guardrails = GUARDRAILS.read_text(encoding="utf-8")

    assert "## Runtime integration of state-conditioned modifiers" in normative
    assert (
        "runtime must materialise a typed modifier packet before downstream review or replay can talk about effective coefficients honestly"
        in normative
    )
    assert (
        "blocked or stand-down outcomes must be explicit packet fields, not inferred from missing trades"
        in normative
    )

    assert "## Gate 78 runtime modifier integration authority" in operating_model
    assert (
        "`PostureRiskOutput`, `ExecutionExpressionOutput`, and `ReviewExplanationOutput` must all be able to see the same Gate 78 modifier packet"
        in operating_model
    )

    assert "### 5d. Runtime modifier integration objects" in domain_model
    assert (
        "Modifier runtime integration must stay additive, lineaged, and backwards-compatible — no silent rewrites of earlier deterministic consumers."
        in guardrails
    )


def test_gate78_schema_surface_exposes_modifier_runtime_packet() -> None:
    packet = ModifierRuntimePacket(
        active_policy_ids=["phase_carry:late_session:event_carry_setup"],
        resolved_surfaces=[
            ResolvedRuntimeSurfaceValue(
                target_surface=MutableRuntimeSurface.TARGET_FRESH_DEPLOYABLE_PCT,
                baseline_numeric_value=55.0,
                effective_numeric_value=20.625,
                winning_precedence_band=ModifierPriorityBand.PHASE_CARRY,
                source_policy_ids=["phase_carry:late_session:event_carry_setup"],
            )
        ],
    )
    assert (
        packet.resolved_surfaces[0].target_surface
        is MutableRuntimeSurface.TARGET_FRESH_DEPLOYABLE_PCT
    )
    assert packet.resolved_surfaces[0].effective_numeric_value == 20.625


def test_gate78_runtime_applies_deterministic_modifier_caps_and_lineage() -> None:
    fixture = supportive_runtime_fixture()
    runtime = DeskCognitionRuntime(Settings())
    result = runtime.run(
        temporal_input=fixture.temporal_input.model_copy(
            update={
                "ts": datetime.fromisoformat("2026-03-23T15:20:00-04:00"),
                "next_event_at": datetime.fromisoformat("2026-03-24T08:30:00-04:00"),
                "precursor_runtime_packet": _tightened_precursor_packet(),
            }
        ),
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )

    assert result.posture.modifier_runtime_packet is not None
    assert result.posture.permission_state.value == "derisk"
    assert result.execution.target_fresh_deployable_pct == 20.625
    assert result.execution.modifier_runtime_packet is not None
    assert result.review.effective_policy is not None
    assert result.review.review_lineage is not None
    assert (
        "phase_carry:late_session:event_carry_setup"
        in result.review.review_lineage.modifier_policy_ids
    )
    assert (
        MutableRuntimeSurface.TARGET_FRESH_DEPLOYABLE_PCT.value
        in result.review.review_lineage.effective_coefficient_targets
    )
    assert result.review.modifier_control_law is not None
    assert result.review.modifier_control_law.triggered_kill_switch is None


def test_gate78_runtime_exposes_kill_switch_and_blocked_trade_outcomes() -> None:
    fixture = stressed_runtime_fixture()
    runtime = DeskCognitionRuntime(Settings())
    result = runtime.run(
        temporal_input=fixture.temporal_input.model_copy(
            update={
                "next_event_at": fixture.temporal_input.ts,
                "precursor_runtime_packet": _unresolved_precursor_packet(),
            }
        ),
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )

    assert result.posture.permission_state.value == "block"
    assert result.execution.entry_style == "no_trade"
    assert result.review.review_governance is not None
    assert result.review.review_governance.stand_down_class is not None
    assert result.review.modifier_control_law is not None
    assert result.review.modifier_control_law.triggered_kill_switch is not None
    assert result.review.failure_taxonomy is not None
    assert (
        result.review.failure_taxonomy.primary_failure_class
        is ReviewFailureClass.POSTURE_POLICY_FAILURE
    )
    assert (
        result.review.failure_taxonomy.resolution is ReviewResolutionClass.BLOCKED_TRADE
    )
    assert result.review.review_packet["effective_policy"]


def test_gate78_vocabulary_terms_are_generated_and_committed() -> None:
    committed = VOCAB_PATH.read_text(encoding="utf-8")
    generated = build_document().to_json_text()

    assert committed == generated
    vocab = json.loads(committed)
    slugs = {entry["canonical_slug"] for entry in vocab["entries"]}
    assert {"modifier_runtime_packet", "effective_coefficient"}.issubset(slugs)
