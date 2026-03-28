"""DMP v2 schema and migration tests."""

from __future__ import annotations

from datetime import datetime

import pytest
from pydantic import ValidationError

from nvda_desk.domain.session_clock import SessionClockPhase
from nvda_desk.schemas.cognition import TemporalContextOutput
from nvda_desk.schemas.dmp import DmpBehaviourClass, DmpGrammarRole
from nvda_desk.schemas.dmp_v2 import (
    DmpV2ArtifactRefBlock,
    DmpV2ArtifactReference,
    DmpV2Contract,
    DmpV2MetricsBlock,
    DmpV2ObjectBlock,
    DmpV2Packet,
    DmpV2Producer,
    DmpV2SeriesPoint,
    DmpV2SummaryBlock,
    DmpV2TableBlock,
    DmpV2TableColumn,
    DmpV2TimeseriesBlock,
    build_dmp_v2_packet,
    build_dmp_v2_packet_from_payload,
)


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


def test_dmp_v2_packet_serialises_fixed_envelope_and_blocks() -> None:
    """DMP v2 should keep a fixed envelope while allowing typed blocks."""

    packet = build_dmp_v2_packet(
        packet_id="dmp::temporal::001",
        trace_id="trace::session_a",
        run_id="run::session_a::001",
        scenario_id="live_snapshot",
        producer=DmpV2Producer(
            module_id="temporal_context",
            module_version="2.0.0",
            module_instance_id="temporal_context::runtime",
            grammar_role="temporal_context",
            stage_name="temporal_context",
            behaviour_class="stage_output",
            emitted_at=datetime(2026, 3, 24, 9, 31),
        ),
        contract=DmpV2Contract(
            packet_schema_id="dmp.packet@2.0.0",
            payload_contract_id="temporal_context.output@1.0.0",
            compatibility_version="1",
            required_blocks=["object_block", "summary_block"],
            optional_blocks=["metrics_block", "artifact_ref_block"],
        ),
        lineage=None,
        execution_context=None,
        blocks=[
            DmpV2ObjectBlock(
                block_id="payload",
                schema_id="nvda_desk.schemas.cognition.TemporalContextOutput",
                data=_temporal_payload().model_dump(mode="json"),
            ),
            DmpV2MetricsBlock(
                block_id="confidence",
                schema_id="temporal_context.metrics@1.0.0",
                metrics={"phase_confidence": 0.91, "minutes_since_open": 12},
            ),
            DmpV2SummaryBlock(
                block_id="summary_block",
                schema_id="temporal_context.summary@1.0.0",
                data={"trader_summary": "Opening window classified cleanly."},
            ),
            DmpV2ArtifactRefBlock(
                block_id="summary_ref",
                schema_id="temporal_context.summary_ref@1.0.0",
                artifact=DmpV2ArtifactReference(
                    artifact_id="artifact::summary::001",
                    artifact_kind="markdown",
                    media_type="text/markdown",
                    schema_id="temporal_context.summary_ref@1.0.0",
                    checksum="sha256:abc",
                ),
            ),
        ],
        trader_summary="Opening window classified cleanly.",
        extensions={"future_reserved": {"lane": "v2"}},
    )
    restored = DmpV2Packet.model_validate_json(packet.model_dump_json())

    assert restored.protocol_version == "dmp.v2"
    assert restored.producer.grammar_role == "temporal_context"
    assert restored.blocks[0].block_type == "object_block"
    assert restored.summary.trader_summary == "Opening window classified cleanly."
    assert restored.extensions["future_reserved"] == {"lane": "v2"}


def test_dmp_v2_rejects_missing_required_blocks_and_undeclared_kinds() -> None:
    """The declared block contract must govern the packet contents."""

    with pytest.raises(ValidationError):
        build_dmp_v2_packet(
            packet_id="dmp::bad::001",
            trace_id="trace::bad",
            run_id="run::bad",
            scenario_id=None,
            producer=DmpV2Producer(
                module_id="temporal_context",
                module_version="2.0.0",
                module_instance_id="temporal_context::runtime",
                grammar_role="temporal_context",
                stage_name="temporal_context",
                behaviour_class="stage_output",
                emitted_at=datetime(2026, 3, 24, 9, 31),
            ),
            contract=DmpV2Contract(
                packet_schema_id="dmp.packet@2.0.0",
                payload_contract_id="temporal_context.output@1.0.0",
                compatibility_version="1",
                required_blocks=["object_block"],
                optional_blocks=[],
            ),
            lineage=None,
            execution_context=None,
            blocks=[
                DmpV2MetricsBlock(
                    block_id="metrics",
                    schema_id="temporal.metrics@1.0.0",
                    metrics={"phase_confidence": 0.91},
                )
            ],
            trader_summary="No object block present.",
        )


def test_dmp_v2_supports_inline_tables_timeseries_and_artifact_references() -> None:
    """Rich-data blocks should support both inline and externalised payloads."""

    table = DmpV2TableBlock(
        block_id="options_surface_inline",
        schema_id="options.chain.surface@1.0.0",
        table_schema_id="options.chain.surface@1.0.0",
        columns=[
            DmpV2TableColumn(name="expiry", dtype="date"),
            DmpV2TableColumn(name="strike", dtype="float"),
            DmpV2TableColumn(name="call_gamma", dtype="float"),
        ],
        primary_key=["expiry", "strike"],
        row_count=2,
        inline_rows=[
            {"expiry": "2026-03-27", "strike": 118.0, "call_gamma": 0.12},
            {"expiry": "2026-03-27", "strike": 119.0, "call_gamma": 0.09},
        ],
    )
    table_ref = DmpV2TableBlock(
        block_id="options_surface_large",
        schema_id="options.chain.surface@1.0.0",
        table_schema_id="options.chain.surface@1.0.0",
        columns=[
            DmpV2TableColumn(name="expiry", dtype="date"),
            DmpV2TableColumn(name="strike", dtype="float"),
        ],
        primary_key=["expiry", "strike"],
        row_count=5000,
        artifact_ref=DmpV2ArtifactReference(
            artifact_id="artifact::options_chain::20260324T152000Z",
            artifact_kind="parquet_dataset",
            media_type="application/parquet",
            schema_id="options.chain.surface@1.0.0",
            checksum="sha256:def",
            byte_count=8192,
        ),
    )
    timeseries = DmpV2TimeseriesBlock(
        block_id="iv_curve",
        schema_id="options.iv_curve@1.0.0",
        index_name="ts",
        points=[
            DmpV2SeriesPoint(ts="2026-03-24T15:20:00Z", values={"front_atm_iv": 0.59}),
            DmpV2SeriesPoint(ts="2026-03-24T15:21:00Z", values={"front_atm_iv": 0.6}),
        ],
    )

    assert table.inline_rows[0]["strike"] == 118.0
    assert table_ref.artifact_ref is not None
    assert table_ref.artifact_ref.media_type == "application/parquet"
    assert timeseries.points[1].values["front_atm_iv"] == 0.6


def test_build_dmp_v2_packet_from_payload_preserves_identity_context_and_lineage() -> None:
    """Canonical packet building should preserve ids, context, and lineage without a v1 shim."""

    packet = build_dmp_v2_packet_from_payload(
        packet_id="pkt-temporal-001",
        emitted_at=datetime(2026, 3, 24, 9, 31),
        grammar_role=DmpGrammarRole.TEMPORAL_CONTEXT,
        behaviour_class=DmpBehaviourClass.STAGE_OUTPUT,
        payload=_temporal_payload(),
        trader_summary="Opening window classified cleanly.",
        stack_id="stack_live_v1",
        coefficient_set_id="coeff_default_v1",
        dependencies=["temporal_state_v2"],
        input_model_name="TemporalContextInput",
        output_model_name="TemporalContextOutput",
        parent_packet_ids=["pkt-parent-000"],
        dependency_packet_ids=["pkt-parent-000", "pkt-upstream-001"],
        review_trace_id="review-trace::pkt-temporal-001",
        trace_id="trace::session_a",
        run_id="run::session_a::001",
        module_instance_id="temporal_context::runtime",
        registry_version="registry.v2",
        environment_tag="research",
    )

    assert packet.packet_id == "pkt-temporal-001"
    assert packet.execution_context.stack_id == "stack_live_v1"
    assert packet.execution_context.coefficient_set_id == "coeff_default_v1"
    assert packet.lineage.parent_packet_ids == ["pkt-parent-000"]
    assert packet.lineage.dependency_packet_ids == [
        "pkt-parent-000",
        "pkt-upstream-001",
    ]
    assert packet.dependencies == ["temporal_state_v2"]
    assert packet.payload.model_dump(mode="json") == _temporal_payload().model_dump(mode="json")
