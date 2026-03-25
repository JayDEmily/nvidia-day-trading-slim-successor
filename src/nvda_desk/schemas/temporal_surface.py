from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from nvda_desk.domain.temporal_state import ClockEnvelope, TemporalState
from nvda_desk.schemas.session_clock import SessionClockFeaturePayload


class TemporalStateFeaturePayload(BaseModel):
    """Canonical outward Step-1 surface for timestamp-driven temporal lookups."""

    phase: str = Field(description="Compatibility phase label projected from temporal state")
    behavioural_phase: str
    clock_envelope: ClockEnvelope
    market_timezone: str
    ts_market: datetime
    minutes_since_open: int | None = None
    minutes_to_close: int | None = None
    is_pre_market: bool
    is_regular_hours: bool
    is_power_hour: bool
    phase_confidence: float = Field(ge=0.0, le=1.0)
    signal_coverage_ratio: float = Field(ge=0.0, le=1.0)
    evidence_tags: list[str] = Field(default_factory=list)
    compatibility_policy: str = Field(default="session_clock_wrapper_retained")

    @classmethod
    def from_state(cls, state: TemporalState) -> TemporalStateFeaturePayload:
        return cls(
            phase=state.phase.value,
            behavioural_phase=state.behavioural_phase.value,
            clock_envelope=state.clock_envelope,
            market_timezone=state.market_timezone,
            ts_market=state.ts_market,
            minutes_since_open=state.minutes_since_open,
            minutes_to_close=state.minutes_to_close,
            is_pre_market=state.is_pre_market,
            is_regular_hours=state.is_regular_hours,
            is_power_hour=state.is_power_hour,
            phase_confidence=state.phase_confidence,
            signal_coverage_ratio=state.signal_coverage_ratio,
            evidence_tags=list(state.evidence_tags),
        )


class SessionClockCompatibilityPayload(SessionClockFeaturePayload):
    """Explicit compatibility wrapper over the canonical temporal-state surface."""

    compatibility_policy: str = Field(default="legacy_wrapper_over_temporal_state")
