from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-untyped]
from pydantic import BaseModel, ConfigDict, Field

ScalarValue = float | int | str | bool


class RuntimeEnvironmentConfig(BaseModel):
    model_config = ConfigDict(extra="ignore")

    mode: str
    timezone: str
    trading_calendar: str
    symbol: str
    peers: list[str] = Field(default_factory=list)


class RuntimePathsConfig(BaseModel):
    model_config = ConfigDict(extra="ignore")

    project_root: str | None = None
    db_path: str | None = None
    signal_score_db_path: str | None = None
    logs_dir: str | None = None
    snapshots_dir: str | None = None
    fixtures_dir: str | None = None
    module_registry_path: str | None = None
    coefficients_registry_path: str | None = None
    strategy_variants_path: str | None = None


class RuntimeSafetyConfig(BaseModel):
    model_config = ConfigDict(extra="ignore")

    block_if_macro_risk_off: bool
    block_if_no_valid_strike: bool
    block_if_missing_options_snapshot: bool
    block_if_missing_vwap_snapshot: bool


class BrokerPrimaryConfig(BaseModel):
    model_config = ConfigDict(extra="ignore")

    enabled: bool = True
    host: str | None = None
    port: int | None = None
    client_id: int | None = None
    account: str | None = None
    market_data_type: str | None = None
    use_snapshot_data: bool | None = None
    reconnect_on_drop: bool | None = None


class BrokerFallbackConfig(BaseModel):
    model_config = ConfigDict(extra="ignore")

    allow_secondary_data_vendor: bool = False
    allow_csv_replay: bool = False


class BrokerConfig(BaseModel):
    model_config = ConfigDict(extra="ignore")

    primary: str
    ibkr: BrokerPrimaryConfig | None = None
    fallbacks: BrokerFallbackConfig | None = None


class RuntimeSettingsDocument(BaseModel):
    model_config = ConfigDict(extra="ignore")

    version: str
    project: str
    profile: str
    environment: RuntimeEnvironmentConfig
    paths: RuntimePathsConfig | None = None
    broker: BrokerConfig | None = None
    safety: RuntimeSafetyConfig


class EvaluationPathsConfig(BaseModel):
    model_config = ConfigDict(extra="ignore")

    runtime_db_path: str
    signal_score_db_path: str
    logs_dir: str
    output_dir: str
    module_registry_path: str | None = None
    coefficients_registry_path: str | None = None
    strategy_variants_path: str | None = None


class EvaluationConfigDocument(BaseModel):
    model_config = ConfigDict(extra="ignore")

    version: str
    project: str
    profile: str
    paths: EvaluationPathsConfig
    notes: list[str] = Field(default_factory=list)


class CoefficientValueSpec(BaseModel):
    model_config = ConfigDict(extra="ignore")

    value: ScalarValue
    test_min: float | int | None = None
    test_max: float | int | None = None
    step: float | int | None = None
    notes: str | None = None


class CoefficientModuleConfig(BaseModel):
    model_config = ConfigDict(extra="ignore")

    module: str
    weight: float = Field(default=1.0, ge=0)
    enabled: bool = True
    coefficients: dict[str, CoefficientValueSpec] = Field(default_factory=dict)


class RuntimeCoefficientGroups(BaseModel):
    model_config = ConfigDict(extra="ignore")

    layer1_signals: dict[str, CoefficientModuleConfig] = Field(default_factory=dict)
    layer2_scoring: dict[str, CoefficientModuleConfig] = Field(default_factory=dict)
    layer3_decision: dict[str, CoefficientModuleConfig] = Field(default_factory=dict)
    layer4_execution: dict[str, CoefficientModuleConfig] = Field(default_factory=dict)


class CoefficientsRegistryDocument(BaseModel):
    model_config = ConfigDict(extra="ignore")

    version: str
    project: str
    notes: list[str] = Field(default_factory=list)
    globals: dict[str, Any] = Field(default_factory=dict)
    runtime: RuntimeCoefficientGroups = Field(default_factory=RuntimeCoefficientGroups)


class VariantEnabledModules(BaseModel):
    model_config = ConfigDict(extra="ignore")

    layer1_signals: list[str] = Field(default_factory=list)
    layer2_scoring: list[str] = Field(default_factory=list)
    layer3_decision: list[str] = Field(default_factory=list)
    layer4_execution: list[str] = Field(default_factory=list)


class VariantOverrides(BaseModel):
    model_config = ConfigDict(extra="ignore")

    weights: dict[str, float] = Field(default_factory=dict)
    coefficients: dict[str, dict[str, ScalarValue]] = Field(default_factory=dict)
    runtime: dict[str, Any] = Field(default_factory=dict)


class StrategyVariantDefinition(BaseModel):
    model_config = ConfigDict(extra="ignore")

    description: str
    enabled_modules: VariantEnabledModules = Field(default_factory=VariantEnabledModules)
    overrides: VariantOverrides = Field(default_factory=VariantOverrides)


class StrategyVariantDefaults(BaseModel):
    model_config = ConfigDict(extra="ignore")

    base_variant: str
    inherit_missing_from: str
    clamp_scores: bool = True
    require_human_review_for_live_use: bool = True


class StrategyVariantsDocument(BaseModel):
    model_config = ConfigDict(extra="ignore")

    version: str
    project: str
    notes: list[str] = Field(default_factory=list)
    defaults: StrategyVariantDefaults
    variants: dict[str, StrategyVariantDefinition] = Field(default_factory=dict)


class ConfigBundle(BaseModel):
    runtime_settings: RuntimeSettingsDocument
    evaluation_config: EvaluationConfigDocument
    coefficients_registry: CoefficientsRegistryDocument
    strategy_variants: StrategyVariantsDocument


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)
    if not isinstance(raw, dict):
        raise TypeError(f"expected mapping at {path}")
    return raw


def load_config_bundle(config_dir: Path) -> ConfigBundle:
    return ConfigBundle(
        runtime_settings=RuntimeSettingsDocument.model_validate(
            _load_yaml(config_dir / "runtime_settings.example.yaml")
        ),
        evaluation_config=EvaluationConfigDocument.model_validate(
            _load_yaml(config_dir / "evaluation_config.example.yaml")
        ),
        coefficients_registry=CoefficientsRegistryDocument.model_validate(
            _load_yaml(config_dir / "coefficients_registry.example.yaml")
        ),
        strategy_variants=StrategyVariantsDocument.model_validate(
            _load_yaml(config_dir / "strategy_variants.example.yaml")
        ),
    )
