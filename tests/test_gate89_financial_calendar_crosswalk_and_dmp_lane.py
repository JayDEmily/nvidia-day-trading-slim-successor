from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from nvda_desk.schemas.dmp import DmpBehaviourClass, DmpGrammarRole
from nvda_desk.schemas.events import (
    CompanyEventSubclass,
    ExpiryEventSubclass,
    MacroEventSubclass,
    PeerEventSubclass,
    PolicyEventSubclass,
    VenueSessionEventSubclass,
)
from nvda_desk.schemas.financial_calendar import (
    DEFAULT_RETAINED_FIELD_MATRIX,
    FinancialCalendarBundleLayerReference,
    FinancialCalendarBundleMetadata,
    FinancialCalendarEventType,
    FinancialCalendarLayerId,
    FinancialCalendarProjectionTarget,
    FinancialCalendarReferenceArtifact,
    FinancialCalendarReferenceArtifactKind,
    FinancialCalendarRepoFit,
)
from nvda_desk.services.financial_calendar_reference import (
    FINANCIAL_CALENDAR_PACKET_SCHEMA_ID,
    FINANCIAL_CALENDAR_PAYLOAD_CONTRACT_ID,
    build_financial_calendar_reference_packet,
    financial_calendar_crosswalk,
)
from scripts.build_canonical_vocabulary import build_document

REPO_ROOT = Path(__file__).resolve().parents[1]
VOCAB_PATH = REPO_ROOT / "docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json"


def _bundle_metadata() -> FinancialCalendarBundleMetadata:
    return FinancialCalendarBundleMetadata(
        bundle_id="nvda_financial_calendar_bundle_v1_2026",
        version="v1",
        calendar_year=2026,
        authority="proposal_for_repo_ingestion",
        design_goal="Smallest scheduled fact set that materially reduces surprise.",
        repo_fit=FinancialCalendarRepoFit(
            intended_root="data/reference/financial_calendar/",
            paired_runtime_consumers=["src/nvda_desk/services/temporal_context.py"],
            paired_schemas=["src/nvda_desk/schemas/events.py", "src/nvda_desk/schemas/dmp_v2.py"],
            import_style="store raw layer artefacts, derive narrow runtime tags from them",
        ),
        layers=[
            FinancialCalendarBundleLayerReference(
                layer_id=FinancialCalendarLayerId.US_MARKET_STRUCTURE,
                title="U.S. market structure",
                file="layers/01_layer_01_us_market_structure_2026.json",
                event_count=38,
            )
        ],
        source_manifest_file="source_manifest.json",
        dmp_v2_binding_files=["DMP_V2_BINDING_PLAN.md"],
        coverage_notes=["Runtime consumes derived tags, not every raw event."],
    )


def test_gate89_crosswalk_covers_frozen_bundle_event_types_without_free_text_taxonomy() -> None:
    crosswalk = financial_calendar_crosswalk()
    covered = {record.bundle_event_type for record in crosswalk}
    assert covered == set(FinancialCalendarEventType)

    allowed_subclasses = {
        *[item.value for item in CompanyEventSubclass],
        *[item.value for item in PeerEventSubclass],
        *[item.value for item in MacroEventSubclass],
        *[item.value for item in PolicyEventSubclass],
        *[item.value for item in ExpiryEventSubclass],
        *[item.value for item in VenueSessionEventSubclass],
    }
    for record in crosswalk:
        if record.event_subclass is not None:
            assert record.event_subclass in allowed_subclasses
        assert FinancialCalendarProjectionTarget.TEMPORAL_CONTEXT in record.projection_targets or record.projection_targets
        assert all(target.value != "session_clock" for target in record.projection_targets)

    earnings_scopes = {
        record.entity_scope.value
        for record in crosswalk
        if record.bundle_event_type is FinancialCalendarEventType.EARNINGS_RELEASE
    }
    assert earnings_scopes == {"nvda_only", "direct_readthrough_mega_cap"}


def test_gate89_retained_field_matrix_keeps_runtime_and_review_provenance_intact() -> None:
    matrix = DEFAULT_RETAINED_FIELD_MATRIX
    import_stage = {field.value for field in matrix.import_stage}
    runtime_review = {field.value for field in matrix.review_runtime_explanation}

    for required in [
        "layer_id",
        "jurisdiction",
        "venues",
        "runtime_tags",
        "evaluation_tags",
        "source_status",
        "repo_artifact_path",
        "import_lineage_key",
    ]:
        assert required in import_stage
    assert {"runtime_tags", "evaluation_tags", "source_document"} <= runtime_review


def test_gate89_repo_native_dmp_lane_stays_compatible_with_current_helper_layer() -> None:
    packet = build_financial_calendar_reference_packet(
        metadata=_bundle_metadata(),
        artifacts=[
            FinancialCalendarReferenceArtifact(
                artifact_id="master",
                artifact_kind=FinancialCalendarReferenceArtifactKind.MASTER_MANIFEST,
                repo_path="data/reference/financial_calendar/financial_calendar_master_2026.json",
                media_type="application/json",
                schema_id="financial_calendar.master_manifest@1.0.0",
            ),
            FinancialCalendarReferenceArtifact(
                artifact_id="layer-01",
                artifact_kind=FinancialCalendarReferenceArtifactKind.LAYER_JSON,
                repo_path="data/reference/financial_calendar/layers/01_layer_01_us_market_structure_2026.json",
                media_type="application/json",
                schema_id="financial_calendar.layer@1.0.0",
            ),
        ],
        emitted_at=datetime(2026, 3, 28, 12, 0, tzinfo=UTC),
    )

    assert packet.grammar_role is DmpGrammarRole.TEMPORAL_CONTEXT
    assert packet.behaviour_class is DmpBehaviourClass.REPLAY_ARTEFACT
    assert packet.contract.packet_schema_id == FINANCIAL_CALENDAR_PACKET_SCHEMA_ID
    assert packet.contract.payload_contract_id == FINANCIAL_CALENDAR_PAYLOAD_CONTRACT_ID
    assert packet.schema_identifiers.payload_model_name == "FinancialCalendarBundleMetadata"
    assert packet.schema_identifiers.payload_module_path == "nvda_desk.schemas.financial_calendar"
    assert packet.payload.bundle_id == "nvda_financial_calendar_bundle_v1_2026"
    assert [block.block_type for block in packet.blocks].count("object_block") == 1
    assert [block.block_type for block in packet.blocks].count("artifact_ref_block") == 2


def test_gate89_vocabulary_terms_are_present_and_generated() -> None:
    generated = build_document().entry_index()
    committed = VOCAB_PATH.read_text(encoding="utf-8")

    assert committed == build_document().to_json_text()
    vocab = json.loads(committed)
    slugs = {entry["canonical_slug"] for entry in vocab["entries"]}
    assert {"financial_calendar_reference_bundle", "financial_calendar_crosswalk", "financial_calendar_import_record"} <= slugs
    assert generated["financial_calendar_reference_bundle"].maps_to_contract == "nvda_desk.schemas.financial_calendar.FinancialCalendarBundleMetadata"
