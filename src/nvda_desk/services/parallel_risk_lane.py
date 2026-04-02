"""Co-resident independent parallel risk-lane service.

This service materialises the bounded Gate 174-175 runtime surface only:
- lawful invariant reads from session start
- lawful temporal/calendar/event/multi-clock surface after temporal evaluation
- explicit non-arbiter, non-eighth-stage semantics

It does not implement final arbitration, playbook-internal logic, or a second
caution engine.
"""

from __future__ import annotations

from nvda_desk.schemas.cognition import TemporalContextInput, TemporalContextOutput
from nvda_desk.schemas.parallel_risk import (
    ParallelRiskGovernanceStatus,
    ParallelRiskInvariantReadRecord,
    ParallelRiskInvariantSurface,
    ParallelRiskLanePacket,
    ParallelRiskReadableStage,
    ParallelRiskStageReadRecord,
    ParallelRiskStageReadStatus,
    ParallelRiskTemporalSurface,
)


class ParallelRiskLaneService:
    def evaluate(
        self,
        *,
        temporal_input: TemporalContextInput,
        temporal: TemporalContextOutput,
    ) -> ParallelRiskLanePacket:
        event_governance = (
            ParallelRiskGovernanceStatus.INVARIANT_DIRECT_READ
            if temporal_input.live_event_snapshot is not None
            else ParallelRiskGovernanceStatus.COMPATIBILITY_TIMESTAMP
            if temporal_input.next_event_at is not None
            else ParallelRiskGovernanceStatus.DEFERRED_NOT_ADMITTED
        )
        expiry_governance = (
            ParallelRiskGovernanceStatus.COMPATIBILITY_TIMESTAMP
            if temporal_input.next_expiry is not None
            else ParallelRiskGovernanceStatus.DEFERRED_NOT_ADMITTED
        )
        calendar_governance = (
            ParallelRiskGovernanceStatus.INVARIANT_DIRECT_READ
            if temporal_input.desk_calendar_authority is not None
            else ParallelRiskGovernanceStatus.DEFERRED_NOT_ADMITTED
        )
        lineage_keys: list[str] = []
        active_event_class = None
        if temporal_input.live_event_snapshot is not None:
            lineage_keys.extend(temporal_input.live_event_snapshot.lineage_keys)
            next_event = temporal_input.live_event_snapshot.next_event
            active_event_class = None if next_event is None else next_event.event_class
            if next_event is not None:
                lineage_keys.extend(next_event.lineage_keys)
        invariants = [
            ParallelRiskInvariantReadRecord(surface=ParallelRiskInvariantSurface.SERIAL_GRAMMAR_ORDER, governance_status=ParallelRiskGovernanceStatus.INVARIANT_DIRECT_READ, note="seven-stage serial spine remains binding"),
            ParallelRiskInvariantReadRecord(surface=ParallelRiskInvariantSurface.STAGE_OWNERSHIP, governance_status=ParallelRiskGovernanceStatus.INVARIANT_DIRECT_READ, note="parallel lane is co-resident and additive only"),
            ParallelRiskInvariantReadRecord(surface=ParallelRiskInvariantSurface.DESK_CALENDAR_CONTRACT, governance_status=calendar_governance, used=temporal_input.desk_calendar_authority is not None, note="direct read allowed from session start when desk calendar packet is present"),
            ParallelRiskInvariantReadRecord(surface=ParallelRiskInvariantSurface.CALENDAR_HORIZON_ROUTING, governance_status=calendar_governance, used=temporal_input.desk_calendar_authority is not None, note="calendar horizon routing read remains descriptive in Gate 174-175"),
            ParallelRiskInvariantReadRecord(surface=ParallelRiskInvariantSurface.FINANCIAL_CALENDAR_SCHEDULED_FACT_AUTHORITY, governance_status=event_governance, used=temporal_input.live_event_snapshot is not None or temporal_input.next_event_at is not None, note="live event snapshot wins; compatibility timestamp remains subordinate fallback"),
            ParallelRiskInvariantReadRecord(surface=ParallelRiskInvariantSurface.EVENT_IDENTITY, governance_status=event_governance, used=temporal_input.live_event_snapshot is not None or temporal_input.next_event_at is not None, note="event identity is read, not rewritten, by the lane"),
            ParallelRiskInvariantReadRecord(surface=ParallelRiskInvariantSurface.RAW_MARKET_FACTS, governance_status=ParallelRiskGovernanceStatus.INVARIANT_DIRECT_READ, note="raw market facts remain serial-spine facts, not lane inventions"),
            ParallelRiskInvariantReadRecord(surface=ParallelRiskInvariantSurface.RELEASED_COEFFICIENT_AUTHORITY, governance_status=ParallelRiskGovernanceStatus.INVARIANT_DIRECT_READ, used=False, note="baseline authority remains released and immutable; active coefficient reads are deferred in Gate 174-175"),
        ]
        stage_reads = [
            ParallelRiskStageReadRecord(stage=ParallelRiskReadableStage.TEMPORAL, status=ParallelRiskStageReadStatus.USED, note="temporal output is the first lawful stage output the lane may consume"),
            ParallelRiskStageReadRecord(stage=ParallelRiskReadableStage.REGIME, status=ParallelRiskStageReadStatus.NOT_YET_AVAILABLE, note="not read in Gate 174-175"),
            ParallelRiskStageReadRecord(stage=ParallelRiskReadableStage.OPTIONS_FLOW, status=ParallelRiskStageReadStatus.NOT_YET_AVAILABLE, note="not read in Gate 174-175"),
            ParallelRiskStageReadRecord(stage=ParallelRiskReadableStage.POSTURE, status=ParallelRiskStageReadStatus.NOT_YET_AVAILABLE, note="not read in Gate 174-175"),
            ParallelRiskStageReadRecord(stage=ParallelRiskReadableStage.ELIGIBILITY, status=ParallelRiskStageReadStatus.NOT_YET_AVAILABLE, note="not read in Gate 174-175"),
            ParallelRiskStageReadRecord(stage=ParallelRiskReadableStage.EXECUTION, status=ParallelRiskStageReadStatus.NOT_YET_AVAILABLE, note="not read in Gate 174-175"),
            ParallelRiskStageReadRecord(stage=ParallelRiskReadableStage.REVIEW, status=ParallelRiskStageReadStatus.NOT_YET_AVAILABLE, note="review remains downstream of lane creation"),
        ]
        temporal_surface = ParallelRiskTemporalSurface(
            session_phase=temporal.session_phase,
            behavioural_phase=temporal.behavioural_phase,
            desk_window=temporal.desk_window,
            clock_envelope=temporal.clock_envelope,
            minutes_since_open=temporal.minutes_since_open,
            minutes_to_close=temporal.minutes_to_close,
            calendar_closure_classes=list(temporal.calendar_closure_classes),
            session_bridge_rules=list(temporal.session_bridge_rules),
            next_session_open_hint=temporal.next_session_open_hint,
            event_minutes_remaining=temporal.event_minutes_remaining,
            event_window_state=temporal.event_window_state,
            event_overlap_class=temporal.event_overlap_class,
            event_risk_timing_class=temporal.event_risk_timing_class,
            event_carry_sensitivity=temporal.event_carry_sensitivity,
            event_timing_profile=temporal.event_timing_profile,
            active_event_family=temporal.active_event_family,
            active_event_class=active_event_class,
            expiry_days_remaining=temporal.expiry_days_remaining,
            expiry_cycle_state=temporal.expiry_cycle_state,
            session_clock_governance=ParallelRiskGovernanceStatus.FIXED_STRUCTURAL_HEURISTIC,
            behavioural_phase_governance=ParallelRiskGovernanceStatus.GOVERNED_LIVE_THRESHOLD,
            event_source_governance=event_governance,
            expiry_source_governance=expiry_governance,
            calendar_source_governance=calendar_governance,
            lineage_keys=lineage_keys,
            notes=[
                "co_resident_lane_created_after_temporal_stage_only",
                "no_arbiter_behavior_in_gate_174_175",
                "live_event_snapshot_subordinates_next_event_at_when_both_are_present" if temporal_input.live_event_snapshot is not None and temporal_input.next_event_at is not None else "event_source_selection_is_single_surface",
            ],
        )
        return ParallelRiskLanePacket(
            invariant_reads=invariants,
            stage_output_reads=stage_reads,
            temporal_surface=temporal_surface,
            notes=[
                "co_resident_from_session_start",
                "not_step_1_1",
                "not_step_8",
                "not_eighth_stage",
                "descriptive_and_diagnostic_only_in_gate_174_175",
            ],
        )
