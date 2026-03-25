from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from nvda_desk.domain.session_clock import SessionClockPhase, SessionClockState


class SessionClockFeaturePayload(BaseModel):
    phase: SessionClockPhase = Field(description="Deterministic v1 session phase")
    market_timezone: str
    ts_market: datetime
    minutes_since_open: int | None = None
    minutes_to_close: int | None = None
    is_pre_market: bool
    is_regular_hours: bool
    is_power_hour: bool
    phase_confidence: float = Field(ge=0.0, le=1.0)

    @classmethod
    def from_state(cls, state: SessionClockState) -> SessionClockFeaturePayload:
        return cls(
            phase=state.phase,
            market_timezone=state.market_timezone,
            ts_market=state.ts_market,
            minutes_since_open=state.minutes_since_open,
            minutes_to_close=state.minutes_to_close,
            is_pre_market=state.is_pre_market,
            is_regular_hours=state.is_regular_hours,
            is_power_hour=state.is_power_hour,
            phase_confidence=state.phase_confidence,
        )
