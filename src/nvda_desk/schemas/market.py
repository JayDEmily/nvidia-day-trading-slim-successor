from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from nvda_desk.schemas.session_clock import SessionClockFeaturePayload


class Bar1mPayload(BaseModel):
    ts_utc: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int


class MarketSnapshotResponse(BaseModel):
    symbol: str
    requested_at: datetime
    session_clock: SessionClockFeaturePayload
    latest_bar: Bar1mPayload | None = None


class IntradayBarsResponse(BaseModel):
    symbol: str
    requested_at: datetime
    bars: list[Bar1mPayload]
