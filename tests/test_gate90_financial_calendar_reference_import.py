from __future__ import annotations

from datetime import UTC, datetime
from typing import cast
from pathlib import Path

from nvda_desk.schemas.dmp import DmpBehaviourClass, DmpGrammarRole
from nvda_desk.schemas.financial_calendar import FinancialCalendarBundleMetadata, FinancialCalendarLayerId
from nvda_desk.services.financial_calendar_import import FinancialCalendarImportService

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_gate90_reference_path_is_checked_in_with_repo_manifest_and_layers() -> None:
    root = REPO_ROOT / "data/reference/financial_calendar"
    assert (root / "repo_manifest.json").exists()
    assert (root / "financial_calendar_master_2026.json").exists()
    assert (root / "source_manifest.json").exists()
    assert (root / "SHA256SUMS.json").exists()
    assert (root / "layers/01_layer_01_us_market_structure_2026.json").exists()
    assert (root / "layers/04_layer_04_asia_precursor_venue_context_2026.json").exists()


def test_gate90_import_service_loads_repo_controlled_bundle_without_runtime_projection() -> None:
    service = FinancialCalendarImportService(REPO_ROOT)
    imported = service.import_bundle()

    assert imported.metadata.bundle_id == "nvda_financial_calendar_bundle_v1_2026"
    assert imported.repo_manifest.import_status == "checked_in_reference_only_not_runtime_active"
    assert len(imported.imported_records) == 179
    assert {record.layer_id for record in imported.imported_records} == set(FinancialCalendarLayerId)

    sample = next(record for record in imported.imported_records if record.event_id == "us-opex-2026-03-20")
    assert sample.repo_artifact_path.endswith("layers/01_layer_01_us_market_structure_2026.json")
    assert sample.import_lineage_key == "financial_calendar::layer_01_us_market_structure::us-opex-2026-03-20"
    assert "monthly_opex" in sample.runtime_tags
    assert "expiry_day" in sample.evaluation_tags
    assert sample.source_status == "official_confirmed"
    assert not hasattr(sample, "event_class")
    assert not hasattr(sample, "semantic_phase")


def test_gate90_reference_packet_uses_repo_controlled_authoritative_artifacts_only() -> None:
    service = FinancialCalendarImportService(REPO_ROOT)
    packet = service.build_reference_packet(emitted_at=datetime(2026, 3, 28, 13, 0, tzinfo=UTC))

    payload = cast(FinancialCalendarBundleMetadata, packet.payload)
    assert packet.grammar_role is DmpGrammarRole.TEMPORAL_CONTEXT
    assert packet.behaviour_class is DmpBehaviourClass.REPLAY_ARTEFACT
    assert payload.repo_fit.intended_root == "data/reference/financial_calendar/"
    assert len(packet.lineage.source_artifact_ids) == 7
    assert {block.block_type for block in packet.blocks} == {"object_block", "artifact_ref_block"}
    artifact_uris = [block.artifact.uri for block in packet.blocks if block.block_type == "artifact_ref_block"]
    assert "data/reference/financial_calendar/dmp_v2_financial_calendar_bundle_example.json" not in artifact_uris
    assert "data/reference/financial_calendar/financial_calendar_master_2026.json" in artifact_uris


def test_gate90_supporting_files_are_retained_under_repo_control_for_review_evidence() -> None:
    service = FinancialCalendarImportService(REPO_ROOT)
    artifacts = service.list_reference_artifacts(include_supporting=True)
    repo_paths = {artifact.repo_path for artifact in artifacts}

    assert "data/reference/financial_calendar/dmp_v2_financial_calendar_bundle_example.json" in repo_paths
    assert "data/reference/financial_calendar/dmp_v2_validation_result.json" in repo_paths
    assert "data/reference/financial_calendar/DMP_V2_BINDING_PLAN.md" in repo_paths
    assert "data/reference/financial_calendar/README.md" in repo_paths
