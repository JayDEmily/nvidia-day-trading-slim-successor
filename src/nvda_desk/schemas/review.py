from __future__ import annotations

from datetime import date, datetime
from enum import StrEnum

from pydantic import BaseModel, Field

from nvda_desk.schemas.events import MarketEventPayload
from nvda_desk.schemas.execution_records import (
    CapitalStateSnapshotPayload,
    DailyPnlReportPayload,
    PositionSnapshotPayload,
)


class ImportedModuleMaturityState(StrEnum):
    """Honest maturity states for imported module review and replay surfaces."""

    CONCEPT_CONTRACT_ONLY = "concept_contract_only"
    IMPLEMENTED_RUNTIME_PROXY = "implemented_runtime_proxy"


class ImportedModuleApprovalState(StrEnum):
    """Explicit non-theatrical approval state for imported modules."""

    NOT_APPROVED = "not_approved"


class ImportedModuleDependencySurface(BaseModel):
    """Review/replay-safe rendering of one imported-module dependency fence."""

    dependency: str = Field(min_length=1)
    status: str = Field(min_length=1)
    note: str = Field(min_length=1)


class ImportedModuleReviewCitation(BaseModel):
    """Review/replay citation for one imported module contract packet."""

    canonical_id: str = Field(min_length=1)
    canonical_slug: str = Field(min_length=1)
    packet_id: str = Field(min_length=1)
    packet_id_v2: str = Field(min_length=1)
    grammar_role: str = Field(min_length=1)
    computation_mode: str = Field(min_length=1)
    maturity_state: ImportedModuleMaturityState
    approval_state: ImportedModuleApprovalState = ImportedModuleApprovalState.NOT_APPROVED
    dependency_fences: list[ImportedModuleDependencySurface] = Field(default_factory=list)
    contract_notes: list[str] = Field(default_factory=list)


class RecordCountSummary(BaseModel):
    signal_event_count: int = Field(ge=0)
    veto_event_count: int = Field(ge=0)
    risk_block_event_count: int = Field(ge=0)
    order_event_count: int = Field(ge=0)
    fill_event_count: int = Field(ge=0)
    position_snapshot_count: int = Field(ge=0)


class ModuleHealthPacket(BaseModel):
    module_id: str = Field(min_length=1)
    evaluation_count: int = Field(ge=0)
    experiment_count: int = Field(ge=0)
    latest_daily_pnl: DailyPnlReportPayload | None = None
    record_counts: RecordCountSummary
    last_signal_at: datetime | None = None
    last_fill_at: datetime | None = None
    open_position_symbols: list[str] = Field(default_factory=list)


class DailyReviewPacket(BaseModel):
    requested_at: datetime
    report_date: date
    trade_count: int = Field(ge=0)
    realized_pnl: float
    unrealized_pnl: float
    account_state: CapitalStateSnapshotPayload
    positions: list[PositionSnapshotPayload]
    module_health: list[ModuleHealthPacket]
    recent_events: list[MarketEventPayload]
