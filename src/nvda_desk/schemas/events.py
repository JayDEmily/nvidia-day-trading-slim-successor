from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field

ImpactLevel = Literal["low", "medium", "high"]


class SessionCalendarCreate(BaseModel):
    session_date: date
    venue: str = Field(default="NASDAQ", min_length=1)
    market_open_utc: datetime
    market_close_utc: datetime
    session_label: str = Field(default="regular", min_length=1)
    is_half_day: bool = False


class SessionCalendarPayload(SessionCalendarCreate):
    calendar_id: int


class SessionCalendarListResponse(BaseModel):
    sessions: list[SessionCalendarPayload]


class MarketEventCreate(BaseModel):
    event_ts: datetime
    event_type: str = Field(min_length=1)
    title: str = Field(min_length=1)
    impact_level: ImpactLevel = "medium"
    symbol: str | None = Field(default=None, min_length=1)
    source_document: str = Field(default="manual", min_length=1)
    notes_md: str = ""


class MarketEventPayload(MarketEventCreate):
    event_id: int
    created_at: datetime


class MarketEventListResponse(BaseModel):
    events: list[MarketEventPayload]


class EventProximityResponse(BaseModel):
    requested_at: datetime
    symbol: str | None = None
    event_risk_window_open: bool
    upcoming_events: list[MarketEventPayload]
    recent_events: list[MarketEventPayload]
