from __future__ import annotations

from datetime import UTC, date, datetime
from pathlib import Path

from nvda_desk.schemas.events import DeskEventClass, EventMaterialityTier
from nvda_desk.schemas.market import PrecursorPostureState, PrecursorVenueUniverse
from nvda_desk.schemas.session_clock import CalendarClosureClass, SessionBridgeRule, TradingVenue
from nvda_desk.services.financial_calendar_import import FinancialCalendarImportService
from nvda_desk.services.financial_calendar_projection import FinancialCalendarProjectionService

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_gate91_projects_venue_state_facts_into_desk_calendar_authority() -> None:
    service = FinancialCalendarProjectionService(REPO_ROOT)
    packet = service.project_desk_calendar_authority(session_date=date(2026, 11, 27))

    assert CalendarClosureClass.HALF_DAY in packet.closure_classes
    assert SessionBridgeRule.US_EARLY_CLOSE in packet.bridge_rules
    nasdaq = next(contract for contract in packet.venues if contract.venue is TradingVenue.NASDAQ_US)
    assert CalendarClosureClass.HALF_DAY in nasdaq.closure_classes
    assert SessionBridgeRule.US_EARLY_CLOSE in nasdaq.bridge_rules



def test_gate91_projects_macro_company_and_expiry_records_into_canonical_event_truth() -> None:
    service = FinancialCalendarProjectionService(REPO_ROOT)
    records = service.project_canonical_event_records()
    indexed = {record.event_id: record for record in records}

    cpi = indexed["us-cpi-2025-12"]
    assert cpi.event_class is DeskEventClass.MACRO
    assert cpi.event_subclass == "cpi"
    assert cpi.source_status == "official_confirmed"
    assert cpi.layer_id == "layer_02_us_macro_policy"
    assert "macro_release" in cpi.runtime_tags

    nvda = indexed["corp-nvda-2026-02-25"]
    assert nvda.event_class is DeskEventClass.COMPANY
    assert nvda.event_subclass == "nvda_earnings"
    assert nvda.source_document == "NVIDIA investor relations financial reports / news release"
    assert nvda.entities == ["NVDA"]

    opex = indexed["us-opex-2026-03-20"]
    assert opex.event_class is DeskEventClass.EXPIRY
    assert opex.materiality_tier is EventMaterialityTier.POSTURE_RELEVANT
    assert "expiry_day" in opex.evaluation_tags



def test_gate91_projects_precursor_venue_state_into_runtime_packet() -> None:
    service = FinancialCalendarProjectionService(REPO_ROOT)
    packet = service.project_precursor_runtime_packet(
        requested_at=datetime(2026, 1, 1, 6, 0, tzinfo=UTC)
    )

    assert PrecursorVenueUniverse.JPX_CASH_INDEX_COMPLEX in packet.missing_venues
    assert PrecursorVenueUniverse.HKEX_CASH_INDEX_COMPLEX in packet.missing_venues
    assert PrecursorVenueUniverse.MAINLAND_CHINA_CASH_INDEX_COMPLEX in packet.missing_venues
    assert packet.posture_state is PrecursorPostureState.DEGRADED_CONFIDENCE
    assert any("JPX cash market closed" in note for note in packet.notes)



def test_gate91_live_event_snapshot_retains_projection_fields_needed_by_later_gates() -> None:
    service = FinancialCalendarProjectionService(REPO_ROOT)
    snapshot = service.build_live_event_snapshot(
        requested_at=datetime(2026, 2, 25, 18, 0, tzinfo=UTC),
        symbol="NVDA",
    )

    assert snapshot.next_event is not None
    assert snapshot.next_event.event_id == "corp-nvda-2026-02-25"
    assert snapshot.next_event.event_subclass == "nvda_earnings"
    assert snapshot.next_event.layer_id == "layer_03_nvda_sector_catalysts"
    assert snapshot.next_event.entities == ["NVDA"]
    assert "sector_catalyst" in snapshot.next_event.runtime_tags
    assert snapshot.next_event.import_lineage_key is not None



def test_gate91_thin_crud_sinks_and_import_records_remain_subordinate_and_non_canonical() -> None:
    import_service = FinancialCalendarImportService(REPO_ROOT)
    imported = import_service.import_bundle()
    service = FinancialCalendarProjectionService(REPO_ROOT)
    records = service.project_canonical_event_records()

    raw_import_record = next(record for record in imported.imported_records if record.event_id == "us-cpi-2025-12")
    canonical_record = next(record for record in records if record.event_id == "us-cpi-2025-12")

    assert not hasattr(raw_import_record, "event_class")
    assert canonical_record.event_class is DeskEventClass.MACRO
    assert canonical_record.repo_artifact_path == raw_import_record.repo_artifact_path
    assert canonical_record.import_lineage_key == raw_import_record.import_lineage_key
