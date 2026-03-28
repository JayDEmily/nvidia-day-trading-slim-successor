"""Temporal-context service for the Desk Cognition Grammar.

This service translates timestamps, expiry proximity, event proximity, and
recent path into deterministic temporal state for downstream layers.
"""

from __future__ import annotations

from datetime import UTC

from nvda_desk.config import Settings
from nvda_desk.domain.session_clock import SessionClockPhase
from nvda_desk.domain.temporal_state import TemporalSignalInput, TemporalStateClassifier
from nvda_desk.schemas.cognition import TemporalContextInput, TemporalContextOutput
from nvda_desk.schemas.events import EventSemanticPhase


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
        desk_window = self._desk_window(clock.behavioural_phase)
        expiry_days_remaining = None
        if payload.next_expiry is not None:
            expiry_days_remaining = max(
                0, (payload.next_expiry.date() - payload.ts.date()).days
            )
        expiry_cycle_state = self._expiry_cycle_state(payload, expiry_days_remaining)
        event_minutes_remaining = None
        event_semantic_phase = None
        live_event_snapshot = payload.live_event_snapshot
        next_live_event = (
            None if live_event_snapshot is None else live_event_snapshot.next_event
        )
        event_anchor = payload.next_event_at
        if next_live_event is not None:
            event_anchor = next_live_event.event_at
            event_semantic_phase = next_live_event.semantic_phase
        if event_anchor is not None:
            event_delta = event_anchor.astimezone(UTC) - payload.ts.astimezone(UTC)
            event_minutes_remaining = int(event_delta.total_seconds() // 60)
        event_proximity_state = self._event_proximity_state(
            event_minutes_remaining, event_semantic_phase
        )
        event_window_state = self._event_window_state(
            event_minutes_remaining, event_semantic_phase
        )
        recent_path_tag = self._recent_path_tag(
            payload.prior_session_return_pct, payload.intraday_move_pct
        )
        carryover_state = self._carryover_state(
            payload.prior_session_return_pct, payload.intraday_move_pct
        )
        reasons = [
            f"clock_envelope:{clock.clock_envelope.value}",
            f"session_phase:{clock.phase.value}",
            f"behavioural_phase:{clock.behavioural_phase.value}",
            f"desk_window:{desk_window}",
            f"signal_coverage_ratio:{clock.signal_coverage_ratio}",
            f"expiry_cycle_state:{expiry_cycle_state}",
            f"event_proximity_state:{event_proximity_state}",
            f"event_window_state:{event_window_state}",
            f"recent_path_tag:{recent_path_tag}",
            f"carryover_state:{carryover_state}",
            *clock.evidence_tags,
        ]
        if expiry_days_remaining is not None:
            reasons.append(f"expiry_days_remaining:{expiry_days_remaining}")
        if event_minutes_remaining is not None:
            reasons.append(f"event_minutes_remaining:{event_minutes_remaining}")
        return TemporalContextOutput(
            session_phase=clock.phase,
            desk_window=desk_window,
            phase_confidence=clock.phase_confidence,
            clock_envelope=clock.clock_envelope.value,
            behavioural_phase=clock.behavioural_phase,
            signal_coverage_ratio=clock.signal_coverage_ratio,
            minutes_since_open=clock.minutes_since_open,
            minutes_to_close=clock.minutes_to_close,
            expiry_days_remaining=expiry_days_remaining,
            expiry_cycle_state=expiry_cycle_state,
            event_minutes_remaining=event_minutes_remaining,
            event_proximity_state=event_proximity_state,
            event_window_state=event_window_state,
            recent_path_tag=recent_path_tag,
            carryover_state=carryover_state,
            reasons=reasons,
        )

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

    def _recent_path_tag(
        self, prior_session_return_pct: float, intraday_move_pct: float
    ) -> str:
        if intraday_move_pct <= -2.0:
            return "intraday_flush"
        if intraday_move_pct >= 2.0:
            return "intraday_squeeze"
        if prior_session_return_pct <= -1.5:
            return "prior_session_damage"
        if prior_session_return_pct >= 1.5:
            return "prior_session_strength"
        return "balanced_recent_path"

    def _carryover_state(
        self, prior_session_return_pct: float, intraday_move_pct: float
    ) -> str:
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
