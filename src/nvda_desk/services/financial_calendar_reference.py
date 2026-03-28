from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime

from nvda_desk.schemas.dmp import DmpBehaviourClass, DmpGrammarRole
from nvda_desk.schemas.dmp_v2 import (
    DmpV2ArtifactRefBlock,
    DmpV2ArtifactReference,
    DmpV2Contract,
    DmpV2ExecutionContext,
    DmpV2Lineage,
    DmpV2ObjectBlock,
    DmpV2Packet,
    DmpV2Producer,
    DmpV2Validation,
    build_dmp_v2_packet,
)
from nvda_desk.schemas.financial_calendar import (
    FinancialCalendarBundleMetadata,
    FinancialCalendarReferenceArtifact,
    default_financial_calendar_crosswalk,
)

FINANCIAL_CALENDAR_PACKET_SCHEMA_ID = "dmp.packet@2.0.0"
FINANCIAL_CALENDAR_PAYLOAD_CONTRACT_ID = (
    "temporal_context.financial_calendar_reference_bundle@1.0.0"
)
FINANCIAL_CALENDAR_STAGE_NAME = "financial_calendar_reference_bundle"
FINANCIAL_CALENDAR_MODULE_ID = "financial_calendar_reference_bundle"


def financial_calendar_crosswalk():
    """Return the frozen Gate 89 crosswalk records."""

    return default_financial_calendar_crosswalk()


def build_financial_calendar_reference_packet(
    *,
    metadata: FinancialCalendarBundleMetadata,
    artifacts: Sequence[FinancialCalendarReferenceArtifact],
    emitted_at: datetime,
    module_version: str = "1.0.0",
    validation: DmpV2Validation | None = None,
) -> DmpV2Packet:
    """Build the repo-native DMP v2 reference-bundle packet for Gate 89/90.

    The packet is intentionally compatible with the current helper layer:
    grammar role stays inside repo enums, behaviour class stays inside repo
    enums, and schema-identifiers compatibility metadata is explicit.
    """

    artifact_refs = [
        DmpV2ArtifactRefBlock(
            block_id=artifact.artifact_id,
            schema_id=artifact.schema_id,
            artifact=DmpV2ArtifactReference(
                artifact_id=artifact.artifact_id,
                artifact_kind=artifact.artifact_kind.value,
                media_type=artifact.media_type,
                schema_id=artifact.schema_id,
                uri=artifact.repo_path,
                checksum=artifact.checksum,
                byte_count=artifact.byte_count,
            ),
        )
        for artifact in artifacts
    ]
    return build_dmp_v2_packet(
        packet_id=f"financial-calendar::{metadata.bundle_id}",
        trace_id=f"trace::financial-calendar::{metadata.bundle_id}",
        run_id=f"run::financial-calendar::{metadata.bundle_id}",
        scenario_id=str(metadata.calendar_year),
        producer=DmpV2Producer(
            module_id=FINANCIAL_CALENDAR_MODULE_ID,
            module_version=module_version,
            module_instance_id=f"{FINANCIAL_CALENDAR_MODULE_ID}::{metadata.calendar_year}",
            grammar_role=DmpGrammarRole.TEMPORAL_CONTEXT.value,
            stage_name=FINANCIAL_CALENDAR_STAGE_NAME,
            behaviour_class=DmpBehaviourClass.REPLAY_ARTEFACT.value,
            emitted_at=emitted_at,
        ),
        contract=DmpV2Contract(
            packet_schema_id=FINANCIAL_CALENDAR_PACKET_SCHEMA_ID,
            payload_contract_id=FINANCIAL_CALENDAR_PAYLOAD_CONTRACT_ID,
            compatibility_version="2",
            required_blocks=["object_block", "artifact_ref_block"],
            optional_blocks=[],
        ),
        lineage=DmpV2Lineage(
            parent_packet_ids=[],
            dependency_packet_ids=[],
            source_artifact_ids=[artifact.artifact_id for artifact in artifacts],
        ),
        execution_context=DmpV2ExecutionContext(
            stack_id=None,
            coefficient_set_id=None,
            registry_version="financial_calendar_reference_bundle@1.0.0",
            environment_tag="repo_checked_in_reference",
        ),
        blocks=[
            DmpV2ObjectBlock(
                block_id="bundle_metadata",
                schema_id="nvda_desk.schemas.financial_calendar.FinancialCalendarBundleMetadata",
                data=metadata.model_dump(mode="json"),
            ),
            *artifact_refs,
        ],
        trader_summary=(
            f"Financial calendar reference bundle for {metadata.calendar_year}; "
            f"{len(metadata.layers)} layers preserved as repo-controlled artefacts."
        ),
        validation=validation or DmpV2Validation(schema_valid=True, validation_errors=[]),
        extensions={
            "schema_identifiers": {
                "payload_model_name": "FinancialCalendarBundleMetadata",
                "payload_module_path": "nvda_desk.schemas.financial_calendar",
                "input_model_name": None,
                "output_model_name": "FinancialCalendarBundleMetadata",
            }
        },
    )
