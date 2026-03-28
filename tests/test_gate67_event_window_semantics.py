"""Gate 67 temporal event-window integrity checks."""

from __future__ import annotations

import json
from pathlib import Path

from nvda_desk.schemas.cognition import ReviewExplanationOutput
from nvda_desk.schemas.config import EventWindowAuthorityResponse
from nvda_desk.schemas.review import TemporalEventWindowSurface
from nvda_desk.schemas.temporal_surface import (
    EventCarrySensitivity,
    EventOverlapClass,
    EventProximityState,
    EventRiskTimingClass,
    EventWindowAuthorityPacket,
    EventWindowContract,
    EventWindowState,
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


def test_gate67_status_closeout_and_leaf_progress_are_recorded() -> None:
    gates_text = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert (
        "## Gate 67 — Temporal event-window semantics\n\nStatus: complete on `main`" in gates_text
    )
    assert "### Gate 67 closeout note" in gates_text
    assert leaves["completed_gate_ids"][:9] == [
        "Gate 59",
        "Gate 60",
        "Gate 61",
        "Gate 62",
        "Gate 63",
        "Gate 64",
        "Gate 65",
        "Gate 66",
        "Gate 67",
    ]
    assert successor_pack_position(leaves["active_gate"]) >= 68

    gate67 = [leaf for leaf in leaves["leaves"] if leaf["gate"] == "Gate 67"]
    assert len(gate67) == 5
    assert all(leaf["status"] == "complete" for leaf in gate67)


def test_gate67_docs_freeze_event_window_and_overlap_law() -> None:
    normative = NORMATIVE.read_text(encoding="utf-8")
    operating_model = OPERATING_MODEL.read_text(encoding="utf-8")
    domain_model = DOMAIN_MODEL.read_text(encoding="utf-8")
    guardrails = GUARDRAILS.read_text(encoding="utf-8")

    assert "## Temporal event-window law" in normative
    assert (
        "event proximity states are `no_event_context`, `event_scheduled`, `event_same_day`, `event_same_session`, `event_imminent`, and `event_live_or_passed`"
        in normative
    )
    assert (
        "event-window states are `clear_window`, `same_session_event_window`, `event_imminent_window`, `event_live_window`, `event_cooling_off_window`, and `event_memory_window`"
        in normative
    )

    assert "## Gate 67 temporal event-window authority" in operating_model
    assert (
        "overlapping windows must resolve through explicit priority classes rather than informal discretion"
        in operating_model
    )

    assert "### 4h. Temporal event-window objects" in domain_model
    assert (
        "**Event-window semantics must stay typed; `near event` or `probably clear by now` is not lawful runtime language.**"
        in guardrails
    )


def test_gate67_schema_surface_exposes_window_overlap_and_memory_states() -> None:
    assert [item.value for item in EventProximityState] == [
        "no_event_context",
        "event_scheduled",
        "event_same_day",
        "event_same_session",
        "event_imminent",
        "event_live_or_passed",
    ]
    assert [item.value for item in EventWindowState] == [
        "clear_window",
        "same_session_event_window",
        "event_imminent_window",
        "event_live_window",
        "event_cooling_off_window",
        "event_memory_window",
    ]
    assert [item.value for item in EventOverlapClass] == [
        "single_event",
        "stacked_event_cluster",
        "overlapping_windows",
        "higher_priority_window_supersedes",
    ]
    assert [item.value for item in EventRiskTimingClass] == [
        "priced_risk",
        "live_release",
        "realised_reaction",
        "cooling_off",
        "event_memory",
    ]
    assert [item.value for item in EventCarrySensitivity] == [
        "intraday_only",
        "carry_sensitive",
        "next_session_memory",
    ]

    contract = EventWindowContract(
        event_family="nvda_earnings",
        proximity_state=EventProximityState.EVENT_IMMINENT,
        primary_window_state=EventWindowState.EVENT_IMMINENT_WINDOW,
        overlap_class=EventOverlapClass.OVERLAPPING_WINDOWS,
        risk_timing_class=EventRiskTimingClass.PRICED_RISK,
        carry_sensitivity=EventCarrySensitivity.CARRY_SENSITIVE,
        pre_window_minutes=240,
        post_window_minutes=60,
        cooling_off_minutes=30,
        memory_minutes=1440,
    )
    authority = EventWindowAuthorityResponse(
        authority=EventWindowAuthorityPacket(
            proximity_states=list(EventProximityState),
            window_states=list(EventWindowState),
            overlap_classes=list(EventOverlapClass),
            risk_timing_classes=list(EventRiskTimingClass),
            carry_sensitivity_classes=list(EventCarrySensitivity),
            window_contracts=[contract],
        )
    )
    surface = TemporalEventWindowSurface(
        proximity_state=EventProximityState.EVENT_IMMINENT,
        window_state=EventWindowState.EVENT_IMMINENT_WINDOW,
        overlap_class=EventOverlapClass.OVERLAPPING_WINDOWS,
        risk_timing_class=EventRiskTimingClass.PRICED_RISK,
        carry_sensitivity=EventCarrySensitivity.CARRY_SENSITIVE,
        event_family="nvda_earnings",
    )
    review = ReviewExplanationOutput(
        summary="event window bounded",
        review_packet={},
        event_window_governance=surface,
    )
    assert authority.authority.window_contracts[0].memory_minutes == 1440
    assert review.event_window_governance == surface


def test_gate67_vocabulary_terms_are_generated_and_committed() -> None:
    committed = VOCAB_PATH.read_text(encoding="utf-8")
    generated = build_document().to_json_text()

    assert committed == generated
    vocab = json.loads(committed)
    slugs = {entry["canonical_slug"] for entry in vocab["entries"]}
    assert {"event_window_state", "desk_calendar_contract"}.issubset(slugs)
