from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field

from nvda_desk.domain.session_clock import SessionClockPhase
from nvda_desk.schemas.module import ModuleClass, ModuleDescriptor


class CarryRecommendation(StrEnum):
    INCREASE = "increase"
    HOLD_SMALL = "hold_small"
    FLATTEN = "flatten"
    BLOCK = "block"


class OvernightCarryEvaluatorInput(BaseModel):
    descriptor: ModuleDescriptor = Field(
        default_factory=lambda: ModuleDescriptor(
            module_id="overnight-carry-v1",
            name="Overnight Carry Evaluator",
            module_class=ModuleClass.SIZING,
            thesis="Advise whether to hold exposure overnight.",
        )
    )
    symbol: str = Field(default="NVDA", min_length=1)
    close_distance_to_vwap_pct: float = Field(ge=-100, le=100)
    close_phase: SessionClockPhase
    realised_vol_pct: float = Field(ge=0, le=1000)
    vix_level: float = Field(ge=0, le=200)
    vvix_level: float = Field(ge=0, le=500)
    asia_precursor_composite: float = Field(ge=-1, le=1)
    risk_budget_remaining_pct: float = Field(ge=0, le=100)
    gross_exposure_pct: float = Field(ge=0, le=100)
    open_orders_count: int = Field(ge=0)


class OvernightCarryEvaluatorOutput(BaseModel):
    carry_recommendation: CarryRecommendation
    overnight_exposure_pct: float = Field(ge=0, le=100)
    keep_orders_active: bool
    rationale_codes: list[str]
    review_required: bool


class CarryDerivedContext(BaseModel):
    evaluation_ts: datetime
    last_bar_ts: datetime
    close_phase: SessionClockPhase
    close_distance_to_vwap_pct: float = Field(ge=-100, le=100)
    realised_vol_pct: float = Field(ge=0, le=1000)
    vix_level: float = Field(ge=0, le=200)
    vvix_level: float = Field(ge=0, le=500)


class OvernightCarryMarketInput(BaseModel):
    descriptor: ModuleDescriptor = Field(
        default_factory=lambda: ModuleDescriptor(
            module_id="overnight-carry-v2-market",
            name="Overnight Carry Evaluator",
            module_class=ModuleClass.SIZING,
            thesis="Advise whether to hold exposure overnight using persisted market state.",
        )
    )
    symbol: str = Field(default="NVDA", min_length=1)
    evaluation_ts: datetime
    asia_precursor_composite: float = Field(ge=-1, le=1)
    risk_budget_remaining_pct: float = Field(ge=0, le=100)
    gross_exposure_pct: float = Field(ge=0, le=100)
    open_orders_count: int = Field(ge=0)


class OvernightCarryMarketOutput(BaseModel):
    carry_recommendation: CarryRecommendation
    overnight_exposure_pct: float = Field(ge=0, le=100)
    keep_orders_active: bool
    rationale_codes: list[str]
    review_required: bool
    derived_context: CarryDerivedContext


class CarryReplayPathSummary(BaseModel):
    path_name: str = Field(min_length=1)
    exposure_pct: float = Field(ge=0, le=100)
    keep_orders_active: bool
    projected_open_price: float = Field(gt=0)
    projected_gap_pct: float
    projected_pnl_pct: float
    rationale_codes: list[str] = Field(default_factory=list)


class OvernightCarryReplayFromMarketInput(BaseModel):
    descriptor: ModuleDescriptor = Field(
        default_factory=lambda: ModuleDescriptor(
            module_id="overnight-carry-v3-replay",
            name="Overnight Carry Replay Comparator",
            module_class=ModuleClass.SIZING,
            thesis="Compare flatten, hold, and carry-guided overnight paths from persisted market state.",
        )
    )
    symbol: str = Field(default="NVDA", min_length=1)
    evaluation_ts: datetime
    asia_precursor_composite: float = Field(ge=-1, le=1)
    risk_budget_remaining_pct: float = Field(ge=0, le=100)
    gross_exposure_pct: float = Field(ge=0, le=100)
    open_orders_count: int = Field(ge=0)
    baseline_hold_exposure_pct: float = Field(default=10.0, ge=0, le=100)


class OvernightCarryReplayFromMarketOutput(BaseModel):
    module_id: str = Field(min_length=1)
    evaluation_ts: datetime
    next_session_open_ts: datetime
    next_session_reference_source: str = Field(min_length=1)
    weekend_window: bool
    event_window_open: bool
    best_path_name: str = Field(min_length=1)
    carry_recommendation: CarryRecommendation
    close_price: float = Field(gt=0)
    next_open_price_reference: float = Field(gt=0)
    path_summaries: list[CarryReplayPathSummary]
