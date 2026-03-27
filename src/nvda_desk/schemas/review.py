"""Review and daily packet contracts.

The review layer reconstructs deterministic decisions, imported-module lineage,
recent execution records, and the Gate 61 non-action/conflict vocabulary that
later review packets must expose explicitly.
"""

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
from nvda_desk.schemas.market import (
    DerivedPrecursorField,
    PrecursorVenueUniverse,
    SessionAlignmentExpectation,
)
from nvda_desk.schemas.risk import (
    CarryHorizonState,
    DayPhaseState,
    PhaseBehaviourClass,
    PhaseNoActionBias,
)
from nvda_desk.schemas.state_policy import (
    AdjudicationDisposition,
    CandidateComparisonOutcome,
    CandidateSetShape,
    DegradationStep,
    NonActionClass,
    OverrideDisposition,
    ReviewChangeBudget,
    ReviewEvidenceBlock,
    ReviewOutcome,
    ReviewTriggerClass,
    SignalConflictClass,
)
from nvda_desk.schemas.temporal_surface import (
    EventCarrySensitivity,
    EventOverlapClass,
    EventProximityState,
    EventRiskTimingClass,
    EventWindowState,
)


class ImportedModuleMaturityState(StrEnum):
    """Honest maturity states for imported module review and replay surfaces."""

    CONCEPT_CONTRACT_ONLY = "concept_contract_only"
    IMPLEMENTED_RUNTIME_PROXY = "implemented_runtime_proxy"


class ImportedModuleApprovalState(StrEnum):
    """Explicit non-theatrical approval state for imported modules."""

    NOT_APPROVED = "not_approved"


class ImportedModuleDependencySurface(BaseModel):
    """Review-safe rendering of one imported-module dependency fence."""

    dependency: str = Field(min_length=1)
    status: str = Field(min_length=1)
    note: str = Field(min_length=1)


class ImportedModuleReviewCitation(BaseModel):
    """Review/replay citation for one imported module contract packet."""

    canonical_id: str = Field(min_length=1)
    canonical_slug: str = Field(min_length=1)
    packet_id: str = Field(min_length=1)
    grammar_role: str = Field(min_length=1)
    computation_mode: str = Field(min_length=1)
    maturity_state: ImportedModuleMaturityState
    approval_state: ImportedModuleApprovalState = ImportedModuleApprovalState.NOT_APPROVED
    dependency_fences: list[ImportedModuleDependencySurface] = Field(default_factory=list)
    contract_notes: list[str] = Field(default_factory=list)


class RecordCountSummary(BaseModel):
    """Daily record-count summary for the review surface."""

    signal_event_count: int = Field(ge=0)
    veto_event_count: int = Field(ge=0)
    risk_block_event_count: int = Field(ge=0)
    order_event_count: int = Field(ge=0)
    fill_event_count: int = Field(ge=0)
    position_snapshot_count: int = Field(ge=0)


class ModuleHealthPacket(BaseModel):
    """Per-module health packet shown in daily review."""

    module_id: str = Field(min_length=1)
    evaluation_count: int = Field(ge=0)
    experiment_count: int = Field(ge=0)
    latest_daily_pnl: DailyPnlReportPayload | None = None
    record_counts: RecordCountSummary
    last_signal_at: datetime | None = None
    last_fill_at: datetime | None = None
    open_position_symbols: list[str] = Field(default_factory=list)


class DailyReviewPacket(BaseModel):
    """Top-level daily review packet for capital, positions, and events."""

    requested_at: datetime
    report_date: date
    trade_count: int = Field(ge=0)
    realized_pnl: float
    unrealized_pnl: float
    account_state: CapitalStateSnapshotPayload
    positions: list[PositionSnapshotPayload]
    module_health: list[ModuleHealthPacket]
    recent_events: list[MarketEventPayload]


class ReviewGovernanceSurface(BaseModel):
    """Gate 61 review vocabulary for non-action, conflict, and overrides."""

    stand_down_class: NonActionClass | None = None
    conflict_classes: list[SignalConflictClass] = Field(default_factory=list)
    degradation_step: DegradationStep = DegradationStep.NORMAL
    override_disposition: OverrideDisposition = OverrideDisposition.NOT_APPLICABLE
    override_audit_notes: list[str] = Field(default_factory=list)





class TemporalEventWindowSurface(BaseModel):
    """Gate 67 hook exposing bounded event-window semantics to review packets."""

    proximity_state: EventProximityState
    window_state: EventWindowState
    overlap_class: EventOverlapClass = EventOverlapClass.SINGLE_EVENT
    risk_timing_class: EventRiskTimingClass
    carry_sensitivity: EventCarrySensitivity
    event_family: str = Field(min_length=1)




class PrecursorGovernanceSurface(BaseModel):
    """Gate 68 hook exposing bounded precursor-universe selection to review."""

    active_venues: list[PrecursorVenueUniverse] = Field(default_factory=list)
    derived_fields: list[DerivedPrecursorField] = Field(default_factory=list)
    session_alignment: list[SessionAlignmentExpectation] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)




class PhaseCarryoverPolicySurface(BaseModel):
    """Gate 69 hook exposing bounded phase/carry posture meaning to review."""

    day_phase_state: DayPhaseState
    carry_horizon_state: CarryHorizonState
    behaviour_class: PhaseBehaviourClass
    no_action_bias: PhaseNoActionBias = PhaseNoActionBias.NEUTRAL
    notes: list[str] = Field(default_factory=list)


class ReviewEligibilitySurface(BaseModel):
    """Gate 63 hook exposing evidence, triggers, and governed review outcome."""

    evidence_block: ReviewEvidenceBlock
    trigger_classes: list[ReviewTriggerClass] = Field(default_factory=list)
    eligible: bool = False
    governed_outcome: ReviewOutcome = ReviewOutcome.REVIEW_NOT_ELIGIBLE
    change_budget: ReviewChangeBudget = ReviewChangeBudget.NONE


class CandidateGovernanceSurface(BaseModel):
    """Gate 64 hook exposing candidate roles and adjudication state."""

    candidate_shape: CandidateSetShape
    champion_candidate_id: str | None = None
    shadow_challenger_ids: list[str] = Field(default_factory=list)
    dormant_candidate_ids: list[str] = Field(default_factory=list)
    retired_candidate_ids: list[str] = Field(default_factory=list)
    comparison_outcome: CandidateComparisonOutcome | None = None
    adjudication_disposition: AdjudicationDisposition = AdjudicationDisposition.RESERVED_UNTOUCHED
