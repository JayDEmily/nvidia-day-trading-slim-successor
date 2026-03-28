"""Gate 60 state-policy ontology integrity checks."""

from __future__ import annotations

import json
from pathlib import Path

from nvda_desk.schemas.cognition import RuntimeStateVector
from nvda_desk.schemas.config import StatePolicyAuthorityResponse
from nvda_desk.schemas.state_policy import (
    CanonicalStateVectorField,
    ModifierTransformType,
    MutableRuntimeSurface,
    ProhibitedRuntimeSurface,
    StatePolicyAuthorityPacket,
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
VOCAB_PATH = (
    REPO_ROOT / "docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json"
)


def test_gate60_status_and_closeout_are_recorded() -> None:
    gates_text = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert (
        "## Gate 60 — State-policy vocabulary and coefficient ontology\n\nStatus: complete on `main`"
        in gates_text
    )
    assert "### Gate 60 closeout note" in gates_text

    gate60 = [leaf for leaf in leaves["leaves"] if leaf["gate"] == "Gate 60"]
    assert len(gate60) == 6
    assert all(leaf["status"] == "complete" for leaf in gate60)
    assert all(leaf["id"] in leaves["completed_leaf_ids"] for leaf in gate60)


def test_gate60_docs_freeze_mutable_and_prohibited_surfaces() -> None:
    normative = NORMATIVE.read_text(encoding="utf-8")
    operating_model = OPERATING_MODEL.read_text(encoding="utf-8")

    assert "## State-policy ontology" in normative
    assert "approved modifier transform family is limited to" in normative
    assert "approved mutable runtime surfaces are limited to" in normative
    assert "prohibited runtime variation includes" in normative

    assert "## Gate 60 state-policy authority" in operating_model
    assert "approved modifier read-set is an explicit state vector" in operating_model
    assert "Those fields may inform bounded posture policy" in operating_model


def test_gate60_schema_surface_matches_frozen_ontology() -> None:
    expected_mutable = {
        "entry_gate_score_floor",
        "zone_score_threshold",
        "distance_to_vwap_soft_limit_pct",
        "risk_vix_caution_threshold",
        "risk_vix_hot_threshold",
        "max_risk_per_trade",
        "target_fresh_deployable_pct",
        "hedge_required",
    }
    assert {item.value for item in MutableRuntimeSurface} == expected_mutable

    assert {
        "desk_cognition_grammar_order",
        "stage_owner_assignments",
        "baseline_coefficient_values",
        "calendar_truth",
        "event_identity",
        "raw_market_facts",
        "playbook_registry_membership",
        "review_packet_lineage",
    } == {item.value for item in ProhibitedRuntimeSurface}

    assert {
        "multiplicative_scale",
        "additive_offset",
        "clamp",
        "rank_weight_adjustment",
        "suppression_veto",
    } == {item.value for item in ModifierTransformType}

    model_fields = set(RuntimeStateVector.model_fields)
    required_fields = {
        "desk_window",
        "clock_envelope",
        "carryover_state",
        "expiry_cycle_state",
        "event_proximity_state",
        "event_window_state",
        "volatility_regime",
        "breadth_state",
        "sector_leadership_state",
        "rates_regime_state",
        "fx_stress_state",
        "signal_conflict_state",
        "term_structure_state",
        "skew_state",
        "gamma_state",
        "dealer_pressure_state",
        "options_behavior_cluster",
        "inventory_posture_state",
        "fresh_vs_inventory_state",
        "thesis_state",
        "capital_lockup_state",
        "time_stop_state",
        "permission_state",
    }
    assert required_fields.issubset(model_fields)
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    if successor_pack_position(leaves["active_gate"]) >= 70:
        assert {"day_phase_state", "carry_horizon_state"}.issubset(model_fields)

    authority = StatePolicyAuthorityResponse(
        authority=StatePolicyAuthorityPacket(
            invariants=["desk_cognition_grammar_order"],
            mutable_surfaces=list(MutableRuntimeSurface),
            prohibited_surfaces=list(ProhibitedRuntimeSurface),
            readable_state_fields=list(CanonicalStateVectorField),
            allowed_transform_types=list(ModifierTransformType),
        )
    )
    assert (
        authority.authority.mutable_surfaces[0]
        is MutableRuntimeSurface.ENTRY_GATE_SCORE_FLOOR
    )


def test_gate60_vocabulary_terms_are_generated_and_committed() -> None:
    committed = VOCAB_PATH.read_text(encoding="utf-8")
    generated = build_document().to_json_text()

    assert committed == generated
    vocab = json.loads(committed)
    slugs = {entry["canonical_slug"] for entry in vocab["entries"]}
    assert {
        "state_vector",
        "baseline_coefficient",
        "state_conditioned_modifier",
        "effective_coefficient",
        "prohibited_runtime_variation",
    }.issubset(slugs)
