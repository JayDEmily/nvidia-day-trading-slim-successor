from __future__ import annotations

from datetime import date, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

OrderSide = Literal["buy", "sell"]


class ModuleSignalEventCreate(BaseModel):
    symbol: str = Field(default="NVDA", min_length=1)
    module_id: str = Field(min_length=1)
    requested_at: datetime
    signal_code: str = Field(min_length=1)
    direction: str = Field(default="long", min_length=1)
    score: float = Field(ge=0, le=1)
    payload: dict[str, Any] = Field(default_factory=dict)


class ModuleSignalEventPayload(ModuleSignalEventCreate):
    signal_event_id: int
    created_at: datetime


class ModuleSignalEventListResponse(BaseModel):
    signal_events: list[ModuleSignalEventPayload]


class ModuleVetoEventCreate(BaseModel):
    symbol: str = Field(default="NVDA", min_length=1)
    module_id: str = Field(min_length=1)
    requested_at: datetime
    veto_code: str = Field(min_length=1)
    reason: str = Field(min_length=1)
    payload: dict[str, Any] = Field(default_factory=dict)


class ModuleVetoEventPayload(ModuleVetoEventCreate):
    veto_event_id: int
    created_at: datetime


class ModuleVetoEventListResponse(BaseModel):
    veto_events: list[ModuleVetoEventPayload]


class RiskBlockEventCreate(BaseModel):
    symbol: str = Field(default="NVDA", min_length=1)
    module_id: str = Field(min_length=1)
    requested_at: datetime
    reason_codes: list[str] = Field(default_factory=list)
    linked_risk_decision_id: int | None = None
    payload: dict[str, Any] = Field(default_factory=dict)


class RiskBlockEventPayload(RiskBlockEventCreate):
    risk_block_event_id: int
    created_at: datetime


class RiskBlockEventListResponse(BaseModel):
    risk_block_events: list[RiskBlockEventPayload]


class BrokerPaperOrderInput(BaseModel):
    symbol: str = Field(default="NVDA", min_length=1)
    module_id: str = Field(default="broker-offline", min_length=1)
    requested_at: datetime
    side: OrderSide
    quantity: float = Field(gt=0)
    limit_price: float = Field(gt=0)
    order_type: str = Field(default="limit", min_length=1)
    payload: dict[str, Any] = Field(default_factory=dict)


class BrokerOrderPayload(BaseModel):
    order_intent_id: int
    client_order_ref: str
    status: str
    filled_quantity: float = Field(ge=0)
    average_fill_price: float = Field(gt=0)
    cash_after: float = Field(ge=0)
    equity_after: float = Field(ge=0)
    gross_exposure_after: float = Field(ge=0)


class BrokerOrderEventPayload(BaseModel):
    order_event_id: int
    order_intent_id: int
    created_at: datetime
    event_ts: datetime
    status: str
    detail: str
    payload: dict[str, Any]


class BrokerOrderEventListResponse(BaseModel):
    order_events: list[BrokerOrderEventPayload]


class BrokerFillEventPayload(BaseModel):
    fill_event_id: int
    order_intent_id: int
    created_at: datetime
    fill_ts: datetime
    quantity: float = Field(ge=0)
    fill_price: float = Field(gt=0)
    notional: float = Field(ge=0)


class BrokerFillEventListResponse(BaseModel):
    fill_events: list[BrokerFillEventPayload]


class PositionSnapshotPayload(BaseModel):
    position_snapshot_id: int
    created_at: datetime
    symbol: str
    snapshot_ts: datetime
    quantity: float
    average_price: float = Field(ge=0)
    market_price: float = Field(ge=0)
    market_value: float
    unrealized_pnl: float
    source: str


class PositionSnapshotListResponse(BaseModel):
    positions: list[PositionSnapshotPayload]


class CapitalStateSnapshotPayload(BaseModel):
    capital_state_snapshot_id: int
    created_at: datetime
    snapshot_ts: datetime
    cash: float = Field(ge=0)
    equity: float = Field(ge=0)
    buying_power: float = Field(ge=0)
    gross_exposure: float = Field(ge=0)
    net_exposure: float
    source: str


class DailyPnlReportCreate(BaseModel):
    symbol: str = Field(default="NVDA", min_length=1)
    report_date: date
    realized_pnl: float
    unrealized_pnl: float
    gross_exposure: float = Field(ge=0)
    turnover: float = Field(ge=0)
    trade_count: int = Field(ge=0)
    notes: list[str] = Field(default_factory=list)


class DailyPnlReportPayload(DailyPnlReportCreate):
    daily_pnl_report_id: int
    created_at: datetime


class DailyPnlReportListResponse(BaseModel):
    reports: list[DailyPnlReportPayload]
