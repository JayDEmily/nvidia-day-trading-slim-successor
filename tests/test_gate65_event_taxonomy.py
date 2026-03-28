"""Gate 65 event-taxonomy integrity checks."""

from __future__ import annotations

import json
from pathlib import Path

from nvda_desk.schemas.events import (
    CompanyEventSubclass,
    DeskEventClass,
    EventMaterialityTier,
    EventSemanticPhase,
    EventTaxonomyAuthorityPacket,
    EventTaxonomyRecord,
    ExpiryEventSubclass,
    MacroEventSubclass,
    PeerEventSubclass,
    PolicyEventSubclass,
    VenueSessionEventSubclass,
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


def test_gate65_status_closeout_and_leaf_progress_are_recorded() -> None:
    gates_text = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert (
        "## Gate 65 — Canonical event taxonomy\n\nStatus: complete on `main`"
        in gates_text
    )
    assert "### Gate 65 closeout note" in gates_text
    assert leaves["completed_gate_ids"][:7] == [
        "Gate 59",
        "Gate 60",
        "Gate 61",
        "Gate 62",
        "Gate 63",
        "Gate 64",
        "Gate 65",
    ]
    assert successor_pack_position(leaves["active_gate"]) >= 66

    gate65 = [leaf for leaf in leaves["leaves"] if leaf["gate"] == "Gate 65"]
    assert len(gate65) == 5
    assert all(leaf["status"] == "complete" for leaf in gate65)


def test_gate65_docs_freeze_bounded_event_identity() -> None:
    normative = NORMATIVE.read_text(encoding="utf-8")
    operating_model = OPERATING_MODEL.read_text(encoding="utf-8")
    domain_model = DOMAIN_MODEL.read_text(encoding="utf-8")
    guardrails = GUARDRAILS.read_text(encoding="utf-8")

    assert "## Event taxonomy law" in normative
    assert (
        "runtime and review may only consume events through the bounded top-level classes"
        in normative
    )
    assert (
        "event identity must separate the event existing, the market pricing it, and the realised reaction"
        in normative
    )

    assert "## Gate 65 event-taxonomy authority" in operating_model
    assert (
        "every event keeps semantic separation between known risk, priced risk, and realised reaction"
        in operating_model
    )

    assert "### 4f. Event taxonomy objects" in domain_model
    assert (
        "**Event identity must stay inside the frozen bounded taxonomy; no free-text event-class drift.**"
        in guardrails
    )


def test_gate65_schema_surface_matches_frozen_authority() -> None:
    assert [item.value for item in DeskEventClass] == [
        "company",
        "peer_company",
        "macro",
        "policy",
        "expiry",
        "venue_session",
    ]
    assert [item.value for item in EventSemanticPhase] == [
        "known_risk",
        "priced_risk",
        "realised_reaction",
    ]
    assert [item.value for item in EventMaterialityTier] == [
        "background",
        "monitor",
        "posture_relevant",
        "desk_critical",
    ]

    record = EventTaxonomyRecord(
        event_class=DeskEventClass.COMPANY,
        subclass=CompanyEventSubclass.NVDA_EARNINGS.value,
        semantic_phase=EventSemanticPhase.KNOWN_RISK,
        materiality_tier=EventMaterialityTier.DESK_CRITICAL,
        notes=["earnings date is known before pricing and realised reaction"],
    )
    authority = EventTaxonomyAuthorityPacket(
        top_level_classes=list(DeskEventClass),
        semantic_phases=list(EventSemanticPhase),
        materiality_tiers=list(EventMaterialityTier),
        company_subclasses=list(CompanyEventSubclass),
        peer_subclasses=list(PeerEventSubclass),
        macro_subclasses=list(MacroEventSubclass),
        policy_subclasses=list(PolicyEventSubclass),
        expiry_subclasses=list(ExpiryEventSubclass),
        venue_session_subclasses=list(VenueSessionEventSubclass),
    )

    assert record.subclass == "nvda_earnings"
    assert (
        authority.policy_subclasses[-1] is PolicyEventSubclass.US_EXPORT_CONTROL_ACTION
    )


def test_gate65_vocabulary_terms_are_present_and_generated() -> None:
    generated = build_document().entry_index()
    committed = json.loads(VOCAB_PATH.read_text(encoding="utf-8"))
    committed_slugs = {entry["canonical_slug"] for entry in committed["entries"]}

    assert "event_taxonomy" in generated
    assert (
        generated["event_taxonomy"].maps_to_contract
        == "nvda_desk.schemas.events.EventTaxonomyAuthorityPacket"
    )
    assert "event_taxonomy" in committed_slugs
