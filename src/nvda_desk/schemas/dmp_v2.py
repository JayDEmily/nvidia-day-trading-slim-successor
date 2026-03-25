"""Desk Module Protocol (DMP) v2 typed packet contract.

DMP v2 supersedes the narrow v1 envelope as the long-term canonical internal
message contract. The protocol keeps a fixed top-level envelope while allowing
one or more typed data blocks for heterogeneous module outputs such as compact
objects, scalar metrics, tabular datasets, time series, and external artefact
references.
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from nvda_desk.schemas.dmp import DmpPacket


class DmpV2Producer(BaseModel):
    """Identifies the emitting stage or module."""

    model_config = ConfigDict(extra="forbid")

    module_id: str = Field(min_length=1)
    module_version: str = Field(min_length=1)
    module_instance_id: str = Field(min_length=1)
    grammar_role: str = Field(min_length=1)
    stage_name: str | None = None
    behaviour_class: str = Field(min_length=1)
    emitted_at: datetime


class DmpV2Contract(BaseModel):
    """Declares the packet-level compatibility contract."""

    model_config = ConfigDict(extra="forbid")

    packet_schema_id: str = Field(min_length=1)
    payload_contract_id: str = Field(min_length=1)
    compatibility_version: str = Field(min_length=1)
    required_blocks: list[str] = Field(default_factory=list)
    optional_blocks: list[str] = Field(default_factory=list)


class DmpV2Lineage(BaseModel):
    """Carries packet ancestry, dependencies, and correlation ids."""

    model_config = ConfigDict(extra="forbid")

    parent_packet_ids: list[str] = Field(default_factory=list)
    dependency_packet_ids: list[str] = Field(default_factory=list)
    source_artifact_ids: list[str] = Field(default_factory=list)
    input_fingerprint: str | None = None
    review_trace_id: str | None = None
    replay_trace_id: str | None = None
    decision_trace_id: str | None = None


class DmpV2ExecutionContext(BaseModel):
    """Keeps desk-runtime execution context first-class."""

    model_config = ConfigDict(extra="forbid")

    stack_id: str | None = None
    coefficient_set_id: str | None = None
    playbook_id: str | None = None
    registry_version: str | None = None
    environment_tag: str | None = None


class DmpV2Summary(BaseModel):
    """Bounded human-readable summary surface."""

    model_config = ConfigDict(extra="forbid")

    trader_summary: str = Field(min_length=1)


class DmpV2Validation(BaseModel):
    """Records schema validation state for one packet."""

    model_config = ConfigDict(extra="forbid")

    schema_valid: bool = True
    validation_errors: list[str] = Field(default_factory=list)


class DmpV2ArtifactReference(BaseModel):
    """Typed reference to an externally stored artefact."""

    model_config = ConfigDict(extra="forbid")

    artifact_id: str = Field(min_length=1)
    artifact_kind: str | None = None
    media_type: str = Field(min_length=1)
    schema_id: str = Field(min_length=1)
    uri: str | None = None
    checksum: str | None = None
    byte_count: int | None = Field(default=None, ge=0)


class DmpV2TableColumn(BaseModel):
    """Column descriptor for tabular payload blocks."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    dtype: str = Field(min_length=1)
    unit: str | None = None
    semantic_role: str | None = None


class DmpV2SeriesPoint(BaseModel):
    """One time-series row."""

    model_config = ConfigDict(extra="forbid")

    ts: str = Field(min_length=1)
    values: dict[str, Any] = Field(default_factory=dict)


class _DmpV2BlockBase(BaseModel):
    """Shared block metadata."""

    model_config = ConfigDict(extra="forbid")

    block_type: str
    block_id: str = Field(min_length=1)
    schema_id: str = Field(min_length=1)


class DmpV2ObjectBlock(_DmpV2BlockBase):
    """Carries one compact structured object."""

    block_type: Literal["object_block"] = "object_block"
    data: dict[str, Any] = Field(default_factory=dict)


class DmpV2MetricsBlock(_DmpV2BlockBase):
    """Carries scalar metrics, scores, and flags."""

    block_type: Literal["metrics_block"] = "metrics_block"
    metrics: dict[str, Any] = Field(default_factory=dict)


class DmpV2TableBlock(_DmpV2BlockBase):
    """Carries tabular data inline or by artefact reference."""

    block_type: Literal["table_block"] = "table_block"
    table_schema_id: str = Field(min_length=1)
    columns: list[DmpV2TableColumn] = Field(default_factory=list)
    primary_key: list[str] = Field(default_factory=list)
    partition_keys: list[str] = Field(default_factory=list)
    units: dict[str, str] = Field(default_factory=dict)
    row_count: int = Field(ge=0)
    inline_rows: list[dict[str, Any]] = Field(default_factory=list)
    artifact_ref: DmpV2ArtifactReference | None = None

    @model_validator(mode="after")
    def _validate_storage_mode(self) -> DmpV2TableBlock:
        if not self.inline_rows and self.artifact_ref is None:
            raise ValueError("table_block requires inline_rows or artifact_ref")
        if self.row_count < len(self.inline_rows):
            raise ValueError("row_count cannot be smaller than inline_rows length")
        return self


class DmpV2TimeseriesBlock(_DmpV2BlockBase):
    """Carries an ordered time series."""

    block_type: Literal["timeseries_block"] = "timeseries_block"
    index_name: str = Field(min_length=1)
    points: list[DmpV2SeriesPoint] = Field(default_factory=list)


class DmpV2ArtifactRefBlock(_DmpV2BlockBase):
    """Carries one external artefact reference as the block payload."""

    block_type: Literal["artifact_ref_block"] = "artifact_ref_block"
    artifact: DmpV2ArtifactReference


class DmpV2SummaryBlock(_DmpV2BlockBase):
    """Carries bounded summary text or structured summary metadata."""

    block_type: Literal["summary_block"] = "summary_block"
    data: dict[str, Any] = Field(default_factory=dict)


DmpV2Block = Annotated[
    DmpV2ObjectBlock
    | DmpV2MetricsBlock
    | DmpV2TableBlock
    | DmpV2TimeseriesBlock
    | DmpV2ArtifactRefBlock
    | DmpV2SummaryBlock,
    Field(discriminator="block_type"),
]


class DmpV2Packet(BaseModel):
    """Fixed envelope plus typed blocks for heterogeneous module outputs."""

    model_config = ConfigDict(extra="forbid")

    protocol_version: Literal["dmp.v2"] = "dmp.v2"
    packet_id: str = Field(min_length=1)
    trace_id: str = Field(min_length=1)
    run_id: str = Field(min_length=1)
    scenario_id: str | None = None
    producer: DmpV2Producer
    contract: DmpV2Contract
    lineage: DmpV2Lineage = Field(default_factory=DmpV2Lineage)
    execution_context: DmpV2ExecutionContext = Field(default_factory=DmpV2ExecutionContext)
    blocks: list[DmpV2Block] = Field(default_factory=list, min_length=1)
    summary: DmpV2Summary
    validation: DmpV2Validation = Field(default_factory=DmpV2Validation)
    extensions: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _validate_block_contract(self) -> DmpV2Packet:
        present_block_kinds = [block.block_type for block in self.blocks]
        missing_required = [kind for kind in self.contract.required_blocks if kind not in present_block_kinds]
        if missing_required:
            raise ValueError(f"required block kinds missing: {missing_required}")
        declared = set(self.contract.required_blocks) | set(self.contract.optional_blocks)
        undeclared = [kind for kind in present_block_kinds if kind not in declared]
        if undeclared:
            raise ValueError(f"undeclared block kinds present: {undeclared}")
        return self


def build_dmp_v2_packet(
    *,
    packet_id: str,
    trace_id: str,
    run_id: str,
    scenario_id: str | None,
    producer: DmpV2Producer,
    contract: DmpV2Contract,
    lineage: DmpV2Lineage | None,
    execution_context: DmpV2ExecutionContext | None,
    blocks: list[DmpV2Block],
    trader_summary: str,
    validation: DmpV2Validation | None = None,
    extensions: dict[str, Any] | None = None,
) -> DmpV2Packet:
    """Build one DMP v2 packet from its explicit surfaces."""

    return DmpV2Packet(
        packet_id=packet_id,
        trace_id=trace_id,
        run_id=run_id,
        scenario_id=scenario_id,
        producer=producer,
        contract=contract,
        lineage=lineage or DmpV2Lineage(),
        execution_context=execution_context or DmpV2ExecutionContext(),
        blocks=blocks,
        summary=DmpV2Summary(trader_summary=trader_summary),
        validation=validation or DmpV2Validation(),
        extensions=dict(extensions or {}),
    )


def upgrade_v1_packet_to_v2[PayloadT: BaseModel](
    packet: DmpPacket[PayloadT],
    *,
    trace_id: str,
    run_id: str,
    scenario_id: str | None = None,
    module_version: str = "1.0.0",
    module_instance_id: str | None = None,
    registry_version: str | None = None,
    environment_tag: str | None = None,
) -> DmpV2Packet:
    """Upgrade one DMP v1 packet into the v2 fixed-envelope plus block format."""

    payload = packet.payload
    grammar_role = packet.grammar_role.value
    behaviour_class = packet.behaviour_class.value
    parent_ids = (
        [packet.trace_references.parent_packet_id]
        if packet.trace_references.parent_packet_id is not None
        else []
    )
    return build_dmp_v2_packet(
        packet_id=packet.packet_identity.packet_id,
        trace_id=trace_id,
        run_id=run_id,
        scenario_id=scenario_id,
        producer=DmpV2Producer(
            module_id=grammar_role,
            module_version=module_version,
            module_instance_id=module_instance_id or f"{grammar_role}::default",
            grammar_role=grammar_role,
            stage_name=grammar_role,
            behaviour_class=behaviour_class,
            emitted_at=packet.packet_identity.emitted_at,
        ),
        contract=DmpV2Contract(
            packet_schema_id="dmp.packet@2.0.0",
            payload_contract_id=f"{grammar_role}.output@1.0.0",
            compatibility_version="1",
            required_blocks=["object_block"],
            optional_blocks=["summary_block"],
        ),
        lineage=DmpV2Lineage(
            parent_packet_ids=parent_ids,
            dependency_packet_ids=list(packet.trace_references.upstream_packet_ids),
            source_artifact_ids=[],
            review_trace_id=packet.trace_references.review_trace_id,
            replay_trace_id=packet.trace_references.replay_trace_id,
        ),
        execution_context=DmpV2ExecutionContext(
            stack_id=packet.stack_id,
            coefficient_set_id=packet.coefficient_set_id,
            registry_version=registry_version,
            environment_tag=environment_tag,
        ),
        blocks=[
            DmpV2ObjectBlock(
                block_id="payload",
                schema_id=(
                    f"{packet.schema_identifiers.payload_module_path}."
                    f"{packet.schema_identifiers.output_model_name or payload.__class__.__name__}"
                ),
                data=payload.model_dump(mode="json"),
            )
        ],
        trader_summary=packet.trader_summary,
        extensions={
            "v1_schema_identifiers": packet.schema_identifiers.model_dump(mode="json"),
            "v1_dependencies": list(packet.dependencies),
        },
    )
