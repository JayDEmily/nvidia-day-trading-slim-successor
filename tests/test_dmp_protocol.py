"""Gate 8 tests for the internal DMP v1 typed envelope."""

from __future__ import annotations

from datetime import datetime

import pytest
from pydantic import ValidationError

from nvda_desk.domain.session_clock import SessionClockPhase
from nvda_desk.schemas.cognition import TemporalContextOutput
from nvda_desk.schemas.dmp import (
    DmpBehaviourClass,
    DmpGrammarRole,
    DmpPacket,
    DmpPacketIdentity,
    DmpSchemaIdentifiers,
)

TemporalContextPacket = DmpPacket[TemporalContextOutput]


def _temporal_payload() -> TemporalContextOutput:
    return TemporalContextOutput(
        session_phase=SessionClockPhase.OPEN_DISORDER,
        desk_window="open_drive",
        phase_confidence=0.91,
        minutes_since_open=12,
        minutes_to_close=378,
        expiry_cycle_state="weekly_front",
        event_proximity_state="clear",
        event_window_state="none",
        recent_path_tag="trend_up",
        carryover_state="clean",
        reasons=["opening drive intact"],
    )


def _packet() -> TemporalContextPacket:
    return TemporalContextPacket(
        packet_identity=DmpPacketIdentity(
            packet_id="pkt-temporal-001",
            emitted_at=datetime(2026, 3, 24, 9, 31),
        ),
        grammar_role=DmpGrammarRole.TEMPORAL_CONTEXT,
        behaviour_class=DmpBehaviourClass.STAGE_OUTPUT,
        schema_identifiers=DmpSchemaIdentifiers(
            payload_model_name="TemporalContextOutput",
            payload_module_path="nvda_desk.schemas.cognition",
            output_model_name="TemporalContextOutput",
        ),
        stack_id="stack_live_v1",
        coefficient_set_id="coeff_default_v1",
        dependencies=["temporal_state_v1"],
        trader_summary="Opening window classified cleanly.",
        payload=_temporal_payload(),
    )


def test_dmp_packet_serialises_and_restores_typed_payload() -> None:
    """Serialisation should preserve a concrete typed payload model."""

    packet = _packet()
    restored = TemporalContextPacket.model_validate_json(packet.model_dump_json())

    assert restored.protocol_version == "dmp.v1"
    assert isinstance(restored.payload, TemporalContextOutput)
    assert restored.payload.session_phase is SessionClockPhase.OPEN_DISORDER
    assert restored.schema_identifiers.payload_model_name == "TemporalContextOutput"


def test_dmp_packet_requires_metadata_and_forbids_undeclared_extras() -> None:
    """Gate 8 should reject missing required metadata and any undeclared extra fields."""

    with pytest.raises(ValidationError):
        TemporalContextPacket.model_validate(
            {
                "grammar_role": "temporal_context",
                "behaviour_class": "stage_output",
                "schema_identifiers": {
                    "payload_model_name": "TemporalContextOutput",
                    "payload_module_path": "nvda_desk.schemas.cognition",
                },
                "trader_summary": "Missing packet identity should fail.",
                "payload": _temporal_payload().model_dump(mode="json"),
            }
        )

    with pytest.raises(ValidationError):
        TemporalContextPacket.model_validate(
            {
                **_packet().model_dump(mode="json"),
                "unexpected": "nope",
            }
        )

    with pytest.raises(ValidationError):
        TemporalContextPacket.model_validate(
            {
                **_packet().model_dump(mode="json"),
                "payload": {
                    **_temporal_payload().model_dump(mode="json"),
                    "unexpected_nested": "nope",
                },
            }
        )


def test_dmp_packet_keeps_stack_and_coefficient_identity_first_class() -> None:
    """Stack and coefficient identity should live at the envelope top level."""

    packet = _packet()
    dumped = packet.model_dump(mode="json")

    assert dumped["stack_id"] == "stack_live_v1"
    assert dumped["coefficient_set_id"] == "coeff_default_v1"
    assert "stack_id" not in dumped["payload"]
    assert "coefficient_set_id" not in dumped["payload"]
