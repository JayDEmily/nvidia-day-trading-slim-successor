"""Typed contracts for the co-resident independent parallel risk lane.

These contracts preserve the planning-law distinction that the lane is
co-resident with the serial seven-stage desk grammar without becoming an eighth
stage. The lane may read approved invariants from session start and may add
lawful reads of serial-stage outputs once those outputs exist.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from nvda_desk.domain.session_clock import SessionClockPhase
from nvda_desk.schemas.events import DeskEventClass


class ParallelRiskReadableStage(StrEnum):
    """Bounded serial-stage names the lane may lawfully read."""

    TEMPORAL = "temporal"
    REGIME = "regime"
    OPTIONS_FLOW = "options_flow"
    POSTURE = "posture"
    ELIGIBILITY = "eligibility"
    EXECUTION = "execution"
    REVIEW = "review"


class ParallelRiskStageReadStatus(StrEnum):
    """Availability and use status for one serial-stage read surface."""

    USED = "used"
    AVAILABLE_NOT_USED = "available_not_used"
    NOT_YET_AVAILABLE = "not_yet_available"


class ParallelRiskGovernanceStatus(StrEnum):
    """Governance status carried for one lane surface or source."""

    INVARIANT_DIRECT_READ = "invariant_direct_read"
    GOVERNED_LIVE_THRESHOLD = "governed_live_threshold"
    FIXED_STRUCTURAL_HEURISTIC = "fixed_structural_heuristic"
    COMPATIBILITY_TIMESTAMP = "compatibility_timestamp"
    DEFERRED_NOT_ADMITTED = "deferred_not_admitted"
    LAWFUL_STAGE_OUTPUT = "lawful_stage_output"


class ParallelRiskInvariantSurface(StrEnum):
    """Approved invariant surfaces readable from session start."""

    SERIAL_GRAMMAR_ORDER = "serial_grammar_order"
    STAGE_OWNERSHIP = "stage_ownership"
    DESK_CALENDAR_CONTRACT = "desk_calendar_contract"
    CALENDAR_HORIZON_ROUTING = "calendar_horizon_routing"
    FINANCIAL_CALENDAR_SCHEDULED_FACT_AUTHORITY = "financial_calendar_scheduled_fact_authority"
    EVENT_IDENTITY = "event_identity"
    RAW_MARKET_FACTS = "raw_market_facts"
    RELEASED_COEFFICIENT_AUTHORITY = "released_coefficient_authority"


class ParallelRiskInvariantReadRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    surface: ParallelRiskInvariantSurface
    governance_status: ParallelRiskGovernanceStatus
    used: bool = True
    note: str | None = None


class ParallelRiskStageReadRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    stage: ParallelRiskReadableStage
    status: ParallelRiskStageReadStatus
    note: str | None = None


class ParallelRiskTemporalSurface(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_phase: SessionClockPhase
    behavioural_phase: SessionClockPhase | None = None
    desk_window: str
    clock_envelope: str
    minutes_since_open: int | None = None
    minutes_to_close: int | None = None
    calendar_closure_classes: list[str] = Field(default_factory=list)
    session_bridge_rules: list[str] = Field(default_factory=list)
    next_session_open_hint: datetime | None = None
    event_minutes_remaining: int | None = None
    event_window_state: str
    event_overlap_class: str
    event_risk_timing_class: str
    event_carry_sensitivity: str
    event_timing_profile: str | None = None
    active_event_family: str | None = None
    active_event_class: DeskEventClass | None = None
    expiry_days_remaining: int | None = None
    expiry_cycle_state: str
    session_clock_governance: ParallelRiskGovernanceStatus
    behavioural_phase_governance: ParallelRiskGovernanceStatus
    event_source_governance: ParallelRiskGovernanceStatus
    expiry_source_governance: ParallelRiskGovernanceStatus
    calendar_source_governance: ParallelRiskGovernanceStatus
    lineage_keys: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class ParallelRiskLanePacket(BaseModel):
    model_config = ConfigDict(extra="forbid")

    protocol_version: str = "parallel_risk_lane.v1"
    lane_id: str = "independent_parallel_risk_lane"
    serial_spine_preserved: bool = True
    co_resident_from_session_start: bool = True
    arbiter_active: bool = False
    invariant_reads: list[ParallelRiskInvariantReadRecord] = Field(default_factory=list)
    stage_output_reads: list[ParallelRiskStageReadRecord] = Field(default_factory=list)
    temporal_surface: ParallelRiskTemporalSurface
    notes: list[str] = Field(default_factory=list)
