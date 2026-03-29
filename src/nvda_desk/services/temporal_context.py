"""Temporal-context service for the Desk Cognition Grammar.

This service translates timestamps, expiry proximity, event proximity, and
recent path into deterministic temporal state for downstream layers.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from zoneinfo import ZoneInfo

from nvda_desk.config import Settings
from nvda_desk.domain.session_clock import SessionClockPhase
from nvda_desk.domain.temporal_state import TemporalSignalInput, TemporalStateClassifier
from nvda_desk.schemas.cognition import TemporalContextInput, TemporalContextOutput
from nvda_desk.schemas.events import DeskEventClass, EventSemanticPhase, LiveEventReference
from nvda_desk.schemas.session_clock import CalendarClosureClass, SessionBridgeRule
from nvda_desk.schemas.temporal_surface import (
    EventCarrySensitivity,
    EventOverlapClass,
    EventProximityState,
    EventRiskTimingClass,
    EventWindowState,
)


class TemporalContextService:
    """Build deterministic temporal-context outputs from timestamped inputs.

    Purpose:
        Translate timestamps, expiry proximity, and carryover into explicit desk time state.
    Inputs:
        `TemporalContextInput` with the snapshot timestamp and optional expiry/event anchors.
    Outputs:
        `TemporalContextOutput` describing the desk window, event window, expiry cycle,
        recent path, and carryover state.
    Determinism:
        Uses the configured session-clock classifier and fixed threshold logic only.
    """

    def __init__(self, settings: Settings):
        self._classifier = TemporalStateClassifier(settings)
        self._settings = settings
        self._market_tz = ZoneInfo(settings.market_timezone)

    def evaluate(self, payload: TemporalContextInput) -> TemporalContextOutput:
        """Classify temporal context for one market snapshot."""

        clock = self._classifier.classify(
            TemporalSignalInput(
                ts=payload.ts,
                prior_session_return_pct=payload.prior_session_return_pct,
                intraday_move_pct=payload.intraday_move_pct,
                prior_close_price=payload.prior_close_price,
                official_open_price=payload.official_open_price,
                last_price=payload.last_price,
                interval_volume_shares=payload.interval_volume_shares,
                cumulative_session_volume=payload.cumulative_session_volume,
                session_vwap=payload.session_vwap,
                distance_to_vwap_pct=payload.distance_to_vwap_pct,
                vwap_slope_5m_pct=payload.vwap_slope_5m_pct,
                opening_range_high_5m=payload.opening_range_high_5m,
                opening_range_low_5m=payload.opening_range_low_5m,
                opening_range_break_count=payload.opening_range_break_count,
                price_realised_vol_5m_pct=payload.price_realised_vol_5m_pct,
                price_realised_vol_15m_pct=payload.price_realised_vol_15m_pct,
                relative_volume_ratio=payload.relative_volume_ratio,
                rolling_range_5m_pct=payload.rolling_range_5m_pct,
                impulse_age_bars=payload.impulse_age_bars,
            )
        )
        closure_classes = [
            item.value for item in (payload.desk_calendar_authority.closure_classes if payload.desk_calendar_authority is not None else [])
        ]
        bridge_rules = [
            item.value for item in (payload.desk_calendar_authority.bridge_rules if payload.desk_calendar_authority is not None else [])
        ]
        session_phase = clock.phase
        behavioural_phase = clock.behavioural_phase
        desk_window = self._desk_window(clock.behavioural_phase)
        minutes_since_open = clock.minutes_since_open
        minutes_to_close = clock.minutes_to_close
        if payload.desk_calendar_authority is not None:
            session_phase, desk_window, minutes_since_open, minutes_to_close = self._apply_calendar_authority(
                payload=payload,
                phase=session_phase,
                desk_window=desk_window,
                minutes_since_open=minutes_since_open,
                minutes_to_close=minutes_to_close,
            )
        next_session_open_hint = self._next_session_open_hint(payload)
        expiry_days_remaining = None
        if payload.next_expiry is not None:
            expiry_days_remaining = max(0, (payload.next_expiry.date() - payload.ts.date()).days)
        expiry_cycle_state = self._expiry_cycle_state(payload, expiry_days_remaining)
        event_context = self._derive_event_context(payload)
        recent_path_tag = self._recent_path_tag(
            payload.prior_session_return_pct, payload.intraday_move_pct
        )
        carryover_state = self._carryover_state(
            payload.prior_session_return_pct, payload.intraday_move_pct
        )
        reasons = [
            f"clock_envelope:{clock.clock_envelope.value}",
            f"session_phase:{session_phase.value}",
            f"behavioural_phase:{behavioural_phase.value}",
            f"desk_window:{desk_window}",
            f"signal_coverage_ratio:{clock.signal_coverage_ratio}",
            f"expiry_cycle_state:{expiry_cycle_state}",
            f"event_proximity_state:{event_context['event_proximity_state']}",
            f"event_window_state:{event_context['event_window_state']}",
            f"event_overlap_class:{event_context['event_overlap_class']}",
            f"event_risk_timing_class:{event_context['event_risk_timing_class']}",
            f"event_carry_sensitivity:{event_context['event_carry_sensitivity']}",
            f"recent_path_tag:{recent_path_tag}",
            f"carryover_state:{carryover_state}",
            *clock.evidence_tags,
        ]
        if expiry_days_remaining is not None:
            reasons.append(f"expiry_days_remaining:{expiry_days_remaining}")
        if event_context['event_minutes_remaining'] is not None:
            reasons.append(f"event_minutes_remaining:{event_context['event_minutes_remaining']}")
        if closure_classes:
            reasons.append(f"calendar_closure_classes:{','.join(closure_classes)}")
        if bridge_rules:
            reasons.append(f"session_bridge_rules:{','.join(bridge_rules)}")
        if payload.next_event_at is not None and payload.live_event_snapshot is not None:
            reasons.append("compatibility_next_event_at_subordinate_to_live_event_snapshot")
        return TemporalContextOutput(
            session_phase=session_phase,
            desk_window=desk_window,
            phase_confidence=clock.phase_confidence,
            clock_envelope=clock.clock_envelope.value,
            behavioural_phase=behavioural_phase,
            signal_coverage_ratio=clock.signal_coverage_ratio,
            minutes_since_open=minutes_since_open,
            minutes_to_close=minutes_to_close,
            expiry_days_remaining=expiry_days_remaining,
            expiry_cycle_state=expiry_cycle_state,
            event_minutes_remaining=event_context['event_minutes_remaining'],
            event_proximity_state=event_context['event_proximity_state'],
            event_window_state=event_context['event_window_state'],
            event_overlap_class=event_context['event_overlap_class'],
            event_risk_timing_class=event_context['event_risk_timing_class'],
            event_carry_sensitivity=event_context['event_carry_sensitivity'],
            active_event_family=event_context['active_event_family'],
            calendar_closure_classes=closure_classes,
            session_bridge_rules=bridge_rules,
            next_session_open_hint=next_session_open_hint,
            recent_path_tag=recent_path_tag,
            carryover_state=carryover_state,
            reasons=reasons,
        )

    def _apply_calendar_authority(
        self,
        *,
        payload: TemporalContextInput,
        phase: SessionClockPhase,
        desk_window: str,
        minutes_since_open: int | None,
        minutes_to_close: int | None,
    ) -> tuple[SessionClockPhase, str, int | None, int | None]:
        closure_classes = set(payload.desk_calendar_authority.closure_classes)
        bridge_rules = set(payload.desk_calendar_authority.bridge_rules)
        local_ts = payload.ts
        if local_ts.tzinfo is None:
            local_ts = payload.ts.replace(tzinfo=UTC)
        local_ts = local_ts.astimezone(self._market_tz)
        early_close_hour = 13 if CalendarClosureClass.HALF_DAY in closure_classes or CalendarClosureClass.HOLIDAY_EVE_HALF_DAY in closure_classes else self._settings.regular_close_hour
        if CalendarClosureClass.FULL_HOLIDAY in closure_classes:
            return SessionClockPhase.CLOSED, "closed", None, None
        if CalendarClosureClass.HALF_DAY in closure_classes or CalendarClosureClass.HOLIDAY_EVE_HALF_DAY in closure_classes:
            close_dt = local_ts.replace(hour=early_close_hour, minute=0, second=0, microsecond=0)
            open_dt = local_ts.replace(hour=self._settings.regular_open_hour, minute=self._settings.regular_open_minute, second=0, microsecond=0)
            if local_ts >= close_dt:
                return SessionClockPhase.CLOSED, "closed", None, None
            updated_since_open = max(0, int((local_ts - open_dt).total_seconds() // 60))
            updated_to_close = max(0, int((close_dt - local_ts).total_seconds() // 60))
            updated_window = "late_session" if updated_to_close <= 90 else desk_window
            return phase, updated_window, updated_since_open, updated_to_close
        if SessionBridgeRule.US_EARLY_CLOSE in bridge_rules and minutes_to_close is not None:
            return phase, desk_window, minutes_since_open, min(minutes_to_close, 90)
        return phase, desk_window, minutes_since_open, minutes_to_close

    def _next_session_open_hint(self, payload: TemporalContextInput) -> datetime | None:
        if payload.desk_calendar_authority is None:
            return None
        local_ts = payload.ts
        if local_ts.tzinfo is None:
            local_ts = payload.ts.replace(tzinfo=UTC)
        local_ts = local_ts.astimezone(self._market_tz)
        candidate = local_ts.replace(
            hour=self._settings.regular_open_hour,
            minute=self._settings.regular_open_minute,
            second=0,
            microsecond=0,
        )
        closure_classes = set(payload.desk_calendar_authority.closure_classes)
        if (
            CalendarClosureClass.FULL_HOLIDAY not in closure_classes
            and (local_ts < candidate)
        ):
            return candidate
        next_day = local_ts + timedelta(days=1)
        while next_day.weekday() >= 5:
            next_day += timedelta(days=1)
        return next_day.replace(
            hour=self._settings.regular_open_hour,
            minute=self._settings.regular_open_minute,
            second=0,
            microsecond=0,
        )

    def _derive_event_context(self, payload: TemporalContextInput) -> dict[str, str | int | None]:
        live_event_snapshot = payload.live_event_snapshot
        nearby_events = [] if live_event_snapshot is None else live_event_snapshot.material_events
        event_reference = self._primary_event_reference(
            payload.ts,
            None if live_event_snapshot is None else live_event_snapshot.next_event,
            nearby_events,
        )
        if event_reference is None and payload.next_event_at is not None:
            event_minutes_remaining = int(
                (payload.next_event_at.astimezone(UTC) - payload.ts.astimezone(UTC)).total_seconds() // 60
            )
            return {
                'event_minutes_remaining': event_minutes_remaining,
                'event_proximity_state': self._event_proximity_state(event_minutes_remaining, None),
                'event_window_state': self._event_window_state(event_minutes_remaining, None),
                'event_overlap_class': EventOverlapClass.SINGLE_EVENT.value,
                'event_risk_timing_class': EventRiskTimingClass.PRICED_RISK.value,
                'event_carry_sensitivity': EventCarrySensitivity.INTRADAY_ONLY.value,
                'active_event_family': None,
            }
        if event_reference is None:
            return {
                'event_minutes_remaining': None,
                'event_proximity_state': EventProximityState.NO_EVENT_CONTEXT.value,
                'event_window_state': EventWindowState.CLEAR_WINDOW.value,
                'event_overlap_class': EventOverlapClass.SINGLE_EVENT.value,
                'event_risk_timing_class': EventRiskTimingClass.PRICED_RISK.value,
                'event_carry_sensitivity': EventCarrySensitivity.INTRADAY_ONLY.value,
                'active_event_family': None,
            }
        reference = self._event_reference_context(payload.ts, event_reference)
        overlap_class = self._event_overlap_class(payload.ts, nearby_events)
        carry_sensitivity = self._event_carry_sensitivity(event_reference)
        return {
            'event_minutes_remaining': reference['minutes_remaining'],
            'event_proximity_state': reference['proximity_state'],
            'event_window_state': reference['window_state'],
            'event_overlap_class': overlap_class.value,
            'event_risk_timing_class': reference['risk_timing_class'],
            'event_carry_sensitivity': carry_sensitivity.value,
            'active_event_family': event_reference.event_subclass or (event_reference.event_class.value if event_reference.event_class is not None else event_reference.event_type),
        }

    def _primary_event_reference(
        self,
        ts: datetime,
        next_event: LiveEventReference | None,
        nearby_events: list[LiveEventReference],
    ) -> LiveEventReference | None:
        if nearby_events:
            contextualised = [(event, self._event_reference_context(ts, event)) for event in nearby_events]
            active = [
                (event, context)
                for event, context in contextualised
                if context['window_state'] in {
                    EventWindowState.EVENT_LIVE_WINDOW.value,
                    EventWindowState.EVENT_COOLING_OFF_WINDOW.value,
                    EventWindowState.EVENT_MEMORY_WINDOW.value,
                }
            ]
            if active:
                return min(
                    active,
                    key=lambda item: abs(int(item[1]['minutes_remaining'] or 0)),
                )[0]
        if next_event is not None:
            return next_event
        if nearby_events:
            return min(
                nearby_events,
                key=lambda item: abs((item.event_at.astimezone(UTC) - ts.astimezone(UTC)).total_seconds()),
            )
        return None

    def _event_reference_context(
        self, ts: datetime, reference: LiveEventReference
    ) -> dict[str, str | int | None]:
        ts_utc = ts.astimezone(UTC)
        anchor = reference.event_at.astimezone(UTC)
        if reference.window_start_at is None and reference.window_end_at is None:
            minutes_remaining = int((anchor - ts_utc).total_seconds() // 60)
            return {
                'minutes_remaining': minutes_remaining,
                'proximity_state': self._event_proximity_state(minutes_remaining, reference.semantic_phase),
                'window_state': self._event_window_state(minutes_remaining, reference.semantic_phase),
                'risk_timing_class': (
                    EventRiskTimingClass.REALISED_REACTION.value
                    if minutes_remaining <= 0
                    else EventRiskTimingClass.PRICED_RISK.value
                ),
            }
        window_start = (reference.window_start_at or anchor).astimezone(UTC)
        window_end = (reference.window_end_at or anchor).astimezone(UTC)
        minutes_remaining = int((anchor - ts_utc).total_seconds() // 60)
        if window_start <= ts_utc <= window_end:
            risk_timing = EventRiskTimingClass.LIVE_RELEASE
            return {
                'minutes_remaining': minutes_remaining,
                'proximity_state': EventProximityState.EVENT_LIVE_OR_PASSED.value,
                'window_state': EventWindowState.EVENT_LIVE_WINDOW.value,
                'risk_timing_class': risk_timing.value,
            }
        if ts_utc < window_start:
            lead_minutes = int((window_start - ts_utc).total_seconds() // 60)
            if lead_minutes <= 240:
                proximity = EventProximityState.EVENT_IMMINENT
                window_state = EventWindowState.EVENT_IMMINENT_WINDOW
            elif lead_minutes <= 1440:
                proximity = EventProximityState.EVENT_SAME_SESSION
                window_state = EventWindowState.SAME_SESSION_EVENT_WINDOW
            else:
                proximity = EventProximityState.EVENT_SCHEDULED
                window_state = EventWindowState.CLEAR_WINDOW
            risk_timing = EventRiskTimingClass.PRICED_RISK
            return {
                'minutes_remaining': lead_minutes,
                'proximity_state': proximity.value,
                'window_state': window_state.value,
                'risk_timing_class': risk_timing.value,
            }
        minutes_since_end = int((ts_utc - window_end).total_seconds() // 60)
        if minutes_since_end <= 240:
            return {
                'minutes_remaining': -minutes_since_end,
                'proximity_state': EventProximityState.EVENT_LIVE_OR_PASSED.value,
                'window_state': EventWindowState.EVENT_COOLING_OFF_WINDOW.value,
                'risk_timing_class': EventRiskTimingClass.COOLING_OFF.value,
            }
        if minutes_since_end <= 1440:
            return {
                'minutes_remaining': -minutes_since_end,
                'proximity_state': EventProximityState.EVENT_LIVE_OR_PASSED.value,
                'window_state': EventWindowState.EVENT_MEMORY_WINDOW.value,
                'risk_timing_class': EventRiskTimingClass.EVENT_MEMORY.value,
            }
        return {
            'minutes_remaining': -minutes_since_end,
            'proximity_state': EventProximityState.EVENT_LIVE_OR_PASSED.value,
            'window_state': EventWindowState.CLEAR_WINDOW.value,
            'risk_timing_class': EventRiskTimingClass.REALISED_REACTION.value,
        }

    def _event_overlap_class(
        self, ts: datetime, nearby_events: list[LiveEventReference]
    ) -> EventOverlapClass:
        if len(nearby_events) <= 1:
            return EventOverlapClass.SINGLE_EVENT
        active_windows = 0
        ts_utc = ts.astimezone(UTC)
        for event in nearby_events:
            start = (event.window_start_at or event.event_at).astimezone(UTC)
            end = (event.window_end_at or event.event_at).astimezone(UTC)
            if start - timedelta(minutes=240) <= ts_utc <= end + timedelta(minutes=240):
                active_windows += 1
        if active_windows >= 3:
            return EventOverlapClass.HIGHER_PRIORITY_WINDOW_SUPERSEDES
        if active_windows == 2:
            return EventOverlapClass.OVERLAPPING_WINDOWS
        return EventOverlapClass.STACKED_EVENT_CLUSTER

    def _event_carry_sensitivity(self, reference: LiveEventReference) -> EventCarrySensitivity:
        if reference.event_class in {DeskEventClass.MACRO, DeskEventClass.POLICY, DeskEventClass.COMPANY, DeskEventClass.PEER_COMPANY, DeskEventClass.EXPIRY}:
            return EventCarrySensitivity.CARRY_SENSITIVE
        if reference.event_class is DeskEventClass.VENUE_SESSION:
            return EventCarrySensitivity.NEXT_SESSION_MEMORY
        return EventCarrySensitivity.INTRADAY_ONLY

    def _desk_window(self, phase: SessionClockPhase) -> str:
        mapping = {
            SessionClockPhase.PRE_MARKET: "pre_market",
            SessionClockPhase.OPEN_DISORDER: "open_disorder",
            SessionClockPhase.EARLY_ANCHOR: "early_anchor",
            SessionClockPhase.INSTITUTIONAL_REPRICING: "mid_morning",
            SessionClockPhase.MIDDAY_COMPRESSION: "lunch",
            SessionClockPhase.POST_LUNCH_DRIFT: "trend_window",
            SessionClockPhase.POWER_HOUR: "late_session",
            SessionClockPhase.DEALER_UNWIND_CLOSE: "close",
            SessionClockPhase.AFTER_HOURS: "after_hours",
            SessionClockPhase.CLOSED: "closed",
        }
        return mapping[phase]

    def _recent_path_tag(self, prior_session_return_pct: float, intraday_move_pct: float) -> str:
        if intraday_move_pct <= -2.0:
            return "intraday_flush"
        if intraday_move_pct >= 2.0:
            return "intraday_squeeze"
        if prior_session_return_pct <= -1.5:
            return "prior_session_damage"
        if prior_session_return_pct >= 1.5:
            return "prior_session_strength"
        return "balanced_recent_path"

    def _carryover_state(self, prior_session_return_pct: float, intraday_move_pct: float) -> str:
        if prior_session_return_pct <= -1.0 and intraday_move_pct <= -0.75:
            return "downside_carryover_follow_through"
        if prior_session_return_pct >= 1.0 and intraday_move_pct >= 0.75:
            return "upside_carryover_follow_through"
        if prior_session_return_pct <= -1.0 and intraday_move_pct >= 0.5:
            return "downside_carryover_reversal"
        if prior_session_return_pct >= 1.0 and intraday_move_pct <= -0.5:
            return "upside_carryover_fade"
        return "balanced_carryover"

    def _expiry_cycle_state(
        self, payload: TemporalContextInput, expiry_days_remaining: int | None
    ) -> str:
        """Classify expiry-window pressure from days remaining until expiry."""

        if expiry_days_remaining is None:
            return "no_expiry_context"
        if expiry_days_remaining == 0:
            return "expiry_day"
        if payload.ts.weekday() == 0 and 4 <= expiry_days_remaining <= 7:
            return "post_expiry_reset"
        if expiry_days_remaining <= 5:
            return "front_week"
        if expiry_days_remaining <= 14:
            return "next_cycle"
        return "far_cycle"

    def _event_proximity_state(
        self,
        event_minutes_remaining: int | None,
        semantic_phase: EventSemanticPhase | None = None,
    ) -> str:
        """Classify upcoming event proximity for temporal context."""

        if event_minutes_remaining is None:
            return "no_event_context"
        if semantic_phase is EventSemanticPhase.REALISED_REACTION:
            return "event_live_or_passed"
        if event_minutes_remaining <= 0:
            return "event_live_or_passed"
        if semantic_phase is EventSemanticPhase.PRICED_RISK:
            if event_minutes_remaining <= 240:
                return "event_imminent"
            if event_minutes_remaining <= 1440:
                return "event_same_session"
        if event_minutes_remaining <= 60:
            return "event_imminent"
        if event_minutes_remaining <= 240:
            return "event_same_session"
        if event_minutes_remaining <= 1440:
            return "event_same_day"
        return "event_scheduled"

    def _event_window_state(
        self,
        event_minutes_remaining: int | None,
        semantic_phase: EventSemanticPhase | None = None,
    ) -> str:
        """Translate raw event timing into explicit trade-window state."""

        if event_minutes_remaining is None:
            return "clear_window"
        if semantic_phase is EventSemanticPhase.REALISED_REACTION:
            return "event_live_window"
        if event_minutes_remaining <= 0:
            return "event_live_window"
        if semantic_phase is EventSemanticPhase.PRICED_RISK:
            if event_minutes_remaining <= 240:
                return "event_imminent_window"
            if event_minutes_remaining <= 1440:
                return "same_session_event_window"
        if event_minutes_remaining <= 60:
            return "event_imminent_window"
        if event_minutes_remaining <= 240:
            return "same_session_event_window"
        return "clear_window"
