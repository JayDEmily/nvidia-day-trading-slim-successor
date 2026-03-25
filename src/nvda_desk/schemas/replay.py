from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from nvda_desk.domain.session_clock import SessionClockPhase


class ReplayPhaseSummary(BaseModel):
    phase: SessionClockPhase
    bar_count: int = Field(ge=0)
    first_ts: datetime | None = None
    last_ts: datetime | None = None
    open_price: Decimal | None = None
    close_price: Decimal | None = None
    volume_total: int = Field(ge=0)
    return_pct: float | None = None


class ReplaySessionResponse(BaseModel):
    symbol: str
    requested_at: datetime
    start_ts: datetime
    end_ts: datetime
    total_bars: int = Field(ge=0)
    phase_summaries: list[ReplayPhaseSummary]
