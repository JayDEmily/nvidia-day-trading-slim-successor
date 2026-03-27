"""Gate 71 modifier-control-law integrity checks."""

from __future__ import annotations

import json
from pathlib import Path

from nvda_desk.schemas.cognition import ReviewExplanationOutput
from nvda_desk.schemas.config import ModifierControlLawAuthorityResponse
from nvda_desk.schemas.review import ModifierControlLawSurface
from nvda_desk.schemas.state_policy import (
    CombinationLaw,
    KillSwitchCondition,
    ModifierClampRule,
    ModifierControlLawAuthorityPacket,
    ModifierPriorityBand,
    ModifierVetoRule,
    MutableRuntimeSurface,
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


def test_gate71_status_closeout_and_leaf_progress_are_recorded() -> None:
    gates_text = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert "## Gate 71 — Modifier precedence, caps, vetoes, and kill-switches\n\nStatus: complete on `main`" in gates_text
    assert "### Gate 71 closeout note" in gates_text
    assert leaves["completed_gate_ids"][:13] == [
        "Gate 59", "Gate 60", "Gate 61", "Gate 62", "Gate 63", "Gate 64", "Gate 65",
        "Gate 66", "Gate 67", "Gate 68", "Gate 69", "Gate 70", "Gate 71",
    ]
    assert successor_pack_position(leaves["active_gate"]) >= 72
    gate71 = [leaf for leaf in leaves["leaves"] if leaf["gate"] == "Gate 71"]
    assert len(gate71) == 5
    assert all(leaf["status"] == "complete" for leaf in gate71)


def test_gate71_docs_freeze_precedence_and_kill_switch_law() -> None:
    normative = NORMATIVE.read_text(encoding="utf-8")
    operating_model = OPERATING_MODEL.read_text(encoding="utf-8")
    domain_model = DOMAIN_MODEL.read_text(encoding="utf-8")
    guardrails = GUARDRAILS.read_text(encoding="utf-8")

    assert "## Modifier-control law" in normative
    assert "precedence bands are `kill_switch`, `hard_block`, `event_options_stress`, `phase_carry`, `precursor`, `regime`, and `baseline`" in normative
    assert "lineage must record which precedence band won" in normative

    assert "## Gate 71 modifier-control-law authority" in operating_model
    assert "compatible modifiers combine through bounded algebra and then clamp to approved caps/floors" in operating_model

    assert "### 5c. Modifier-control-law objects" in domain_model
    assert "**When multiple states are active, precedence, vetoes, caps, and kill-switches must follow the frozen control law — no blended judgement soup.**" in guardrails


def test_gate71_schema_surface_exposes_precedence_clamps_and_review_hook() -> None:
    assert [item.value for item in ModifierPriorityBand] == [
        "kill_switch", "hard_block", "event_options_stress", "phase_carry", "precursor", "regime", "baseline",
    ]
    assert [item.value for item in CombinationLaw] == [
        "most_restrictive_wins", "multiply_then_clamp", "additive_offset_then_clamp", "block_overrides_scale",
    ]
    assert [item.value for item in KillSwitchCondition] == [
        "event_live_hard_block",
        "event_suppressed_with_negative_gamma",
        "precursor_contradiction_with_expiry_distortion",
        "data_quality_hard_block",
        "operator_or_broker_hard_block",
    ]

    clamp = ModifierClampRule(
        target_surface=MutableRuntimeSurface.MAX_RISK_PER_TRADE,
        floor=0.1,
        cap=0.5,
        notes=["Combined modifiers may not push max risk per trade outside the frozen corridor."],
    )
    veto = ModifierVetoRule(
        controlling_band=ModifierPriorityBand.HARD_BLOCK,
        suppressed_bands=[ModifierPriorityBand.PHASE_CARRY, ModifierPriorityBand.PRECURSOR, ModifierPriorityBand.BASELINE],
        notes=["A hard block suppresses softer posture modifiers entirely."],
    )
    authority = ModifierControlLawAuthorityResponse(
        authority=ModifierControlLawAuthorityPacket(
            precedence_bands=list(ModifierPriorityBand),
            combination_laws=list(CombinationLaw),
            kill_switch_conditions=list(KillSwitchCondition),
            clamp_rules=[clamp],
            veto_rules=[veto],
            lineage_fields=["winning_precedence_band", "applied_combination_laws", "suppressed_state_labels", "triggered_kill_switch"],
        )
    )
    surface = ModifierControlLawSurface(
        active_precedence_bands=[ModifierPriorityBand.EVENT_OPTIONS_STRESS, ModifierPriorityBand.PHASE_CARRY],
        applied_combination_laws=[CombinationLaw.MOST_RESTRICTIVE_WINS, CombinationLaw.MULTIPLY_THEN_CLAMP],
        suppressed_state_labels=["baseline_opening_bias"],
    )
    review = ReviewExplanationOutput(summary="control law bounded", review_packet={}, modifier_control_law=surface)

    assert authority.authority.veto_rules[0].controlling_band is ModifierPriorityBand.HARD_BLOCK
    assert review.modifier_control_law == surface


def test_gate71_vocabulary_terms_are_generated_and_committed() -> None:
    committed = VOCAB_PATH.read_text(encoding="utf-8")
    generated = build_document().to_json_text()

    assert committed == generated
    vocab = json.loads(committed)
    slugs = {entry["canonical_slug"] for entry in vocab["entries"]}
    assert {"modifier_control_law", "event_options_stress_policy"}.issubset(slugs)
