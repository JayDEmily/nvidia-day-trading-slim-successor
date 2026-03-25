"""Typed contracts for deterministic replay, calibration, and stack comparison.

Gate F makes stack definitions, coefficient application, walk-forward slices,
and deterministic comparison reports explicit runtime artefacts rather than
leaving them implied in tests or ad hoc payloads.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from nvda_desk.schemas.cognition import ReviewExplanationOutput
from nvda_desk.schemas.review import ImportedModuleReviewCitation

EXPECTED_REVIEW_STAGES = [
    "temporal",
    "regime",
    "options_flow",
    "posture",
    "eligibility",
    "execution",
]


class ModuleWeightContract(BaseModel):
    """One explicit module-weight override inside a stack or coefficient set."""

    model_config = ConfigDict(extra="forbid")

    module_id: str
    weight: float
    rationale: str = ""


class SubCoefficientContract(BaseModel):
    """One explicit sub-coefficient override inside a stack or coefficient set."""

    model_config = ConfigDict(extra="forbid")

    coefficient_id: str
    weight: float
    coefficient_family: str = "default"
    rationale: str = ""


class StackDefinition(BaseModel):
    """Explicit runtime stack definition used by replay and comparison."""

    model_config = ConfigDict(extra="forbid")

    stack_id: str
    label: str
    description: str = ""
    enabled_playbooks: list[str] = Field(default_factory=list)
    disabled_playbooks: list[str] = Field(default_factory=list)
    module_weights: dict[str, float] = Field(default_factory=dict)
    sub_coefficients: dict[str, float] = Field(default_factory=dict)
    module_weight_contracts: list[ModuleWeightContract] = Field(default_factory=list)
    sub_coefficient_contracts: list[SubCoefficientContract] = Field(default_factory=list)

    @model_validator(mode="after")
    def populate_explicit_contract_lists(self) -> StackDefinition:
        """Mirror dict overrides into explicit contract lists when omitted."""

        if not self.module_weight_contracts:
            self.module_weight_contracts = [
                ModuleWeightContract(module_id=module_id, weight=weight)
                for module_id, weight in sorted(self.module_weights.items())
            ]
        if not self.sub_coefficient_contracts:
            self.sub_coefficient_contracts = [
                SubCoefficientContract(coefficient_id=coefficient_id, weight=weight)
                for coefficient_id, weight in sorted(self.sub_coefficients.items())
            ]
        return self


class CoefficientSet(BaseModel):
    """Named coefficient overrides to apply on top of a stack definition."""

    model_config = ConfigDict(extra="forbid")

    set_id: str
    stack_id: str
    label: str = ""
    module_weights: dict[str, float] = Field(default_factory=dict)
    sub_coefficients: dict[str, float] = Field(default_factory=dict)
    module_weight_contracts: list[ModuleWeightContract] = Field(default_factory=list)
    sub_coefficient_contracts: list[SubCoefficientContract] = Field(default_factory=list)

    @model_validator(mode="after")
    def populate_explicit_contract_lists(self) -> CoefficientSet:
        """Mirror dict overrides into explicit contract lists when omitted."""

        if not self.module_weight_contracts:
            self.module_weight_contracts = [
                ModuleWeightContract(module_id=module_id, weight=weight)
                for module_id, weight in sorted(self.module_weights.items())
            ]
        if not self.sub_coefficient_contracts:
            self.sub_coefficient_contracts = [
                SubCoefficientContract(coefficient_id=coefficient_id, weight=weight)
                for coefficient_id, weight in sorted(self.sub_coefficients.items())
            ]
        return self


class ScenarioExpectation(BaseModel):
    """Expected veto and playbook outcomes for one deterministic scenario."""

    model_config = ConfigDict(extra="forbid")

    expected_veto: bool = False
    expected_playbooks: list[str] = Field(default_factory=list)
    expected_permission_state: str | None = None
    expected_review_stages: list[str] = Field(default_factory=lambda: list(EXPECTED_REVIEW_STAGES))


class ReplayScenarioRecord(BaseModel):
    """One timestamped scenario row for deterministic comparison runs."""

    model_config = ConfigDict(extra="forbid")

    scenario_id: str
    ts: datetime
    payload: dict[str, object]
    expectation: ScenarioExpectation = Field(default_factory=ScenarioExpectation)


class WalkForwardSliceDefinition(BaseModel):
    """One deterministic walk-forward-ready slice."""

    model_config = ConfigDict(extra="forbid")

    slice_id: str
    label: str
    scenario_ids: list[str] = Field(default_factory=list)


class CoefficientAuditPacket(BaseModel):
    """Concrete record of weights and coefficients applied to one run."""

    model_config = ConfigDict(extra="forbid")

    stack_id: str
    enabled_playbooks: list[str] = Field(default_factory=list)
    disabled_playbooks: list[str] = Field(default_factory=list)
    applied_module_weights: dict[str, float] = Field(default_factory=dict)
    applied_sub_coefficients: dict[str, float] = Field(default_factory=dict)
    scoring_components: dict[str, float] = Field(default_factory=dict)


class ReplayPacketLineage(BaseModel):
    """Typed replay lineage surface bound to one replay run result."""

    model_config = ConfigDict(extra="forbid")

    protocol_version: str = "dmp.v2"
    replay_trace_id: str
    review_packet_id: str
    decision_packet_id: str
    packet_lineage: list[str] = Field(default_factory=list)
    stage_packet_ids: dict[str, str] = Field(default_factory=dict)


class ReplayRunResult(BaseModel):
    """One deterministic replay run result for a coefficient set."""

    model_config = ConfigDict(extra="forbid")

    coefficient_set_id: str
    stack_id: str
    scenario_id: str
    permission_state: str
    active_playbook_ids: list[str] = Field(default_factory=list)
    target_fresh_deployable_pct: float
    replay_score: float
    veto_expected: bool
    veto_observed: bool
    veto_correct: float = Field(ge=0.0, le=1.0)
    contradiction_count: int = 0
    contradiction_rate: float = Field(ge=0.0, le=1.0)
    playbook_precision: float = Field(ge=0.0, le=1.0)
    review_completeness: float = Field(ge=0.0, le=1.0)
    conflict_count: int = 0
    coefficient_audit: CoefficientAuditPacket
    review: ReviewExplanationOutput
    imported_module_citations: list[ImportedModuleReviewCitation] = Field(default_factory=list)
    imported_module_maturity_counts: dict[str, int] = Field(default_factory=dict)
    packet_lineage: ReplayPacketLineage | None = None


class ComparisonMetrics(BaseModel):
    """Stable metrics used to compare deterministic replay runs."""

    model_config = ConfigDict(extra="forbid")

    run_count: int = Field(ge=0)
    veto_rate: float = Field(ge=0.0, le=1.0)
    veto_correctness_rate: float = Field(ge=0.0, le=1.0)
    mean_fresh_deployable_pct: float = Field(ge=0.0)
    mean_replay_score: float = Field(ge=0.0)
    mean_contradiction_rate: float = Field(ge=0.0, le=1.0)
    mean_playbook_precision: float = Field(ge=0.0, le=1.0)
    review_completeness_rate: float = Field(ge=0.0, le=1.0)
    active_playbook_rate: float = Field(ge=0.0, le=1.0)
    mean_active_playbook_count: float = Field(ge=0.0)
    mean_conflict_count: float = Field(ge=0.0)


class StackVersusStackSummary(BaseModel):
    """Stable delta surface for one stack-versus-stack comparison pair."""

    model_config = ConfigDict(extra="forbid")

    left_set_id: str
    right_set_id: str
    left_stack_id: str
    right_stack_id: str
    delta_mean_replay_score: float
    delta_veto_correctness_rate: float
    delta_mean_playbook_precision: float
    delta_mean_fresh_deployable_pct: float


class ComparisonReport(BaseModel):
    """Deterministic comparison report across one or more coefficient sets."""

    model_config = ConfigDict(extra="forbid")

    fixture_pack_id: str | None = None
    scenario_ids: list[str] = Field(default_factory=list)
    reports: dict[str, ComparisonMetrics] = Field(default_factory=dict)
    slice_reports: dict[str, dict[str, ComparisonMetrics]] = Field(default_factory=dict)
    stack_vs_stack_summary: list[StackVersusStackSummary] = Field(default_factory=list)


class ReplayFixturePack(BaseModel):
    """Checked-in deterministic replay regression fixture pack."""

    model_config = ConfigDict(extra="forbid")

    fixture_pack_id: str
    stack_definitions: list[StackDefinition] = Field(default_factory=list)
    coefficient_sets: list[CoefficientSet] = Field(default_factory=list)
    scenarios: list[ReplayScenarioRecord] = Field(default_factory=list)
    walk_forward_slices: list[WalkForwardSliceDefinition] = Field(default_factory=list)
