from __future__ import annotations

from pydantic import BaseModel, Field


class CoefficientGroupParameterPayload(BaseModel):
    name: str = Field(min_length=1)
    value: float | int | str | bool
    test_min: float | int | None = None
    test_max: float | int | None = None
    step: float | int | None = None
    notes: str | None = None


class CoefficientGroupPayload(BaseModel):
    key: str = Field(min_length=1)
    layer: str = Field(min_length=1)
    module: str = Field(min_length=1)
    weight: float = Field(ge=0)
    enabled: bool
    parameters: list[CoefficientGroupParameterPayload] = Field(default_factory=list)
    supported_sandbox_overrides: list[str] = Field(default_factory=list)


class CoefficientGroupListResponse(BaseModel):
    groups: list[CoefficientGroupPayload]


class StrategyVariantSummaryPayload(BaseModel):
    name: str = Field(min_length=1)
    description: str
    weight_override_keys: list[str] = Field(default_factory=list)
    coefficient_override_keys: list[str] = Field(default_factory=list)
    supported_sandbox_overrides: list[str] = Field(default_factory=list)


class StrategyVariantListResponse(BaseModel):
    variants: list[StrategyVariantSummaryPayload]


class StrategyVariantPayload(BaseModel):
    name: str = Field(min_length=1)
    description: str
    enabled_module_counts: dict[str, int] = Field(default_factory=dict)
    weight_overrides: dict[str, float] = Field(default_factory=dict)
    coefficient_overrides: dict[str, dict[str, float | int | str | bool]] = Field(default_factory=dict)
    runtime_overrides: dict[str, object] = Field(default_factory=dict)
    supported_sandbox_overrides: list[str] = Field(default_factory=list)
