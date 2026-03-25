from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field

from nvda_desk.domain.session_clock import SessionClockPhase


class RiskAction(StrEnum):
    ALLOW = "allow"
    DERISK = "derisk"
    BLOCK = "block"


class RiskPolicyInput(BaseModel):
    symbol: str = Field(default="NVDA", min_length=1)
    module_id: str = Field(min_length=1)
    requested_at: datetime
    session_phase: SessionClockPhase
    vix_level: float = Field(ge=0, le=200)
    vvix_level: float = Field(ge=0, le=500)
    vix_change_pct_15m: float = Field(ge=-1000, le=1000, default=0.0)
    vvix_change_pct_15m: float = Field(ge=-1000, le=1000, default=0.0)
    data_age_seconds: int = Field(ge=0, default=0)
    gross_exposure_pct: float = Field(ge=0, le=100)
    risk_budget_remaining_pct: float = Field(ge=0, le=100)
    open_orders_count: int = Field(ge=0, default=0)
    conflict_tags: list[str] = Field(default_factory=list)
    vix_caution_threshold: float = Field(default=24.0, gt=0, le=200)
    vix_hot_threshold: float = Field(default=32.0, gt=0, le=200)


class RiskDecision(BaseModel):
    action: RiskAction
    reasons: list[str]
    confidence_scalar: float = Field(ge=0, le=1)
    vix_level: float = Field(ge=0, le=200)
    vvix_level: float = Field(ge=0, le=500)
    vix_change_pct_15m: float
    vvix_change_pct_15m: float


class RiskDecisionPayload(BaseModel):
    decision_id: int
    created_at: datetime
    symbol: str
    module_id: str
    requested_at: datetime
    action: RiskAction
    reasons: list[str]
    confidence_scalar: float = Field(ge=0, le=1)
    input_payload: dict[str, object]
    output_payload: dict[str, object]


class RiskDecisionListResponse(BaseModel):
    decisions: list[RiskDecisionPayload]
