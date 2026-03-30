"""Typed runtime contracts for the Desk Cognition Grammar.

Gate C defines the binding schema surface for the desk runtime. These models
make inventory state, repeated options context, playbook actions, review
packets, and runtime-contract metadata explicit so later module imports do not
smuggle in hidden state.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from nvda_desk.domain.session_clock import SessionClockPhase
from nvda_desk.schemas.events import LiveEventSnapshot
from nvda_desk.schemas.market import PrecursorRuntimePacket
from nvda_desk.schemas.review import (
    CandidateGovernanceSurface,
    EconomicContributionPacket,
    EventOptionsStressPolicySurface,
    ImportedModuleReviewCitation,
    ModifierControlLawSurface,
    PhaseCarryoverPolicySurface,
    PrecursorGovernanceSurface,
    PrecursorRuntimeBindingSurface,
    PromotionEvidencePacket,
    ReviewEligibilitySurface,
    ReviewFailurePacket,
    ReviewGovernanceSurface,
    ReviewLineagePacket,
    TemporalEventWindowSurface,
)
from nvda_desk.schemas.risk import CarryHorizonState, DayPhaseState, RiskAction
from nvda_desk.schemas.session_clock import DeskCalendarAuthorityPacket
from nvda_desk.schemas.state_policy import (
    DegradationStep,
    EffectiveCoefficientLineage,
    ModifierRuntimePacket,
    NonActionClass,
    OverrideDisposition,
    SignalConflictClass,
    SurfaceStabilityScorecard,
)


class VolatilityRegime(StrEnum):
    """Bounded volatility-regime labels for desk-context evaluation."""

    CALM = "calm"
    CAUTION = "caution"
    STRESSED = "stressed"


class BreadthState(StrEnum):
    """Breadth-state labels used by regime and posture services."""

    SUPPORTIVE = "supportive"
    MIXED = "mixed"
    WEAK = "weak"


class TermStructureState(StrEnum):
    """Options term-structure states."""

    FRONT_PREMIUM = "front_premium"
    FLAT = "flat"
    BACK_PREMIUM = "back_premium"


class SkewState(StrEnum):
    """Options skew states."""

    DOWNSIDE_HEAVY = "downside_heavy"
    BALANCED = "balanced"
    UPSIDE_CHASE = "upside_chase"


class GammaState(StrEnum):
    """Gamma-pressure states used in options-context analysis."""

    SUPPORTIVE = "supportive"
    NEUTRAL = "neutral"
    DESTABILISING = "destabilising"


class PermissionState(StrEnum):
    """Binding posture/risk permission states."""

    BLOCK = "block"
    DERISK = "derisk"
    ALLOW = "allow"


class PlaybookDecision(StrEnum):
    """Eligibility outcomes for candidate playbooks."""

    ELIGIBLE = "eligible"
    WATCH_ONLY = "watch_only"
    INELIGIBLE = "ineligible"


class PlaybookAction(StrEnum):
    """Explicit per-playbook action surface required by Gate C."""

    ADD = "add"
    HOLD = "hold"
    TRIM = "trim"
    REDUCE = "reduce"
    HEDGE = "hedge"


class BindingStageName(StrEnum):
    """Deterministic names for the seven binding desk-runtime stages."""

    TEMPORAL = "temporal"
    REGIME = "regime"
    OPTIONS_FLOW = "options_flow"
    POSTURE = "posture"
    ELIGIBILITY = "eligibility"
    EXECUTION = "execution"
    REVIEW = "review"


class TemporalContextInput(BaseModel):
    """Inputs required to classify temporal context for a market snapshot."""

    model_config = ConfigDict(extra="forbid")

    ts: datetime
    next_expiry: datetime | None = None
    next_event_at: datetime | None = None
    live_event_snapshot: LiveEventSnapshot | None = None
    precursor_runtime_packet: PrecursorRuntimePacket | None = None
    desk_calendar_authority: DeskCalendarAuthorityPacket | None = None
    prior_session_return_pct: float = 0.0
    intraday_move_pct: float = 0.0
    prior_close_price: float | None = None
    official_open_price: float | None = None
    last_price: float | None = None
    interval_volume_shares: float | None = None
    cumulative_session_volume: float | None = None
    session_vwap: float | None = None
    distance_to_vwap_pct: float | None = None
    vwap_slope_5m_pct: float | None = None
    opening_range_high_5m: float | None = None
    opening_range_low_5m: float | None = None
    opening_range_break_count: int | None = None
    price_realised_vol_5m_pct: float | None = None
    price_realised_vol_15m_pct: float | None = None
    relative_volume_ratio: float | None = None
    rolling_range_5m_pct: float | None = None
    impulse_age_bars: int | None = None


class TemporalContextOutput(BaseModel):
    """Deterministic temporal-context output for downstream layers."""

    model_config = ConfigDict(extra="forbid")

    session_phase: SessionClockPhase
    desk_window: str
    phase_confidence: float
    clock_envelope: str = "closed"
    behavioural_phase: SessionClockPhase | None = None
    signal_coverage_ratio: float = Field(default=0.0, ge=0.0, le=1.0)
    minutes_since_open: int | None = None
    minutes_to_close: int | None = None
    expiry_days_remaining: int | None = None
    expiry_cycle_state: str
    event_minutes_remaining: int | None = None
    event_proximity_state: str
    event_window_state: str
    event_overlap_class: str = "single_event"
    event_risk_timing_class: str = "priced_risk"
    event_carry_sensitivity: str = "intraday_only"
    event_timing_profile: str | None = None
    active_event_family: str | None = None
    calendar_closure_classes: list[str] = Field(default_factory=list)
    session_bridge_rules: list[str] = Field(default_factory=list)
    next_session_open_hint: datetime | None = None
    recent_path_tag: str
    carryover_state: str
    reasons: list[str] = Field(default_factory=list)


class MarketRegimeContextInput(BaseModel):
    """Inputs required to classify market-regime context."""

    model_config = ConfigDict(extra="forbid")

    nvda_return_pct: float
    nq_return_pct: float
    es_return_pct: float
    sox_return_pct: float
    breadth_score: float = Field(ge=0.0, le=1.0)
    concentration_score: float = Field(ge=0.0, le=1.0)
    vix_level: float
    vvix_level: float
    us10y: float
    us2y: float
    usdjpy: float


class MarketRegimeContextOutput(BaseModel):
    """Deterministic market-regime output for downstream layers."""

    model_config = ConfigDict(extra="forbid")

    nvda_vs_nq_residual_pct: float
    nvda_vs_es_residual_pct: float
    beta_leadership_score: float
    volatility_regime: VolatilityRegime
    vol_of_vol_state: str
    breadth_state: BreadthState
    breadth_concentration_state: str
    sector_leadership_state: str
    rates_regime_state: str
    fx_stress_state: str
    signal_conflict_state: str
    curve_10s2s: float
    vix_vvix_spread: float
    cross_asset_pressure_score: float
    reasons: list[str] = Field(default_factory=list)


class StrikeClusterObservation(BaseModel):
    """One nearby strike cluster used to enrich options context."""

    model_config = ConfigDict(extra="forbid")

    strike: float
    side: str
    open_interest: float = Field(ge=0.0)
    volume: float = Field(ge=0.0)
    distance_to_spot_pct: float


class OptionsFlowMicroSnapshot(BaseModel):
    """One repeated intraday options snapshot for state progression."""

    model_config = ConfigDict(extra="forbid")

    ts: datetime
    front_atm_iv: float
    next_atm_iv: float
    put_call_skew: float
    gamma_pressure_score: float
    spot_to_pin_distance_pct: float = 0.0


class TenorCurvePoint(BaseModel):
    """One tenor-point observation for the intraday IV curve."""

    model_config = ConfigDict(extra="forbid")

    tenor_dte: int = Field(ge=0)
    atm_iv: float = Field(ge=0.0)


class PinProgressionPoint(BaseModel):
    """One point tracking distance to a live pin cluster over time."""

    model_config = ConfigDict(extra="forbid")

    ts: datetime
    distance_to_pin_pct: float


class OptionsFlowContextInput(BaseModel):
    """Inputs required to classify options and flow context."""

    model_config = ConfigDict(extra="forbid")

    spot_price: float
    front_dte: int
    next_dte: int
    front_atm_iv: float
    next_atm_iv: float
    put_call_skew: float
    gamma_pressure_score: float
    call_put_imbalance: float
    oi_concentration: float
    atm_straddle_value: float
    front_realised_vol: float = 0.0
    next_realised_vol: float = 0.0
    vix_level: float = 0.0
    vvix_level: float = 0.0
    spot_to_pin_distance_pct: float = 0.0
    call_oi_near_spot: float = 0.0
    put_oi_near_spot: float = 0.0
    front_volume_near_spot: float = 0.0
    next_volume_near_spot: float = 0.0
    vanna_proxy: float = 0.0
    charm_proxy: float = 0.0
    nearby_strike_clusters: list[StrikeClusterObservation] = Field(default_factory=list)
    repeated_snapshot_sequence: list[OptionsFlowMicroSnapshot] = Field(default_factory=list)
    tenor_iv_curve: list[TenorCurvePoint] = Field(default_factory=list)
    pin_progression_sequence: list[PinProgressionPoint] = Field(default_factory=list)


class OptionsFlowContextOutput(BaseModel):
    """Deterministic options-and-flow output for downstream layers."""

    model_config = ConfigDict(extra="forbid")

    term_structure_state: TermStructureState
    skew_state: SkewState
    gamma_state: GammaState
    implied_move_envelope_pct: float
    iv_rv_front_state: str
    iv_rv_next_state: str
    iv_rv_curve_state: str
    pin_risk_state: str
    dealer_pressure_state: str
    vix_spread_state: str
    options_behavior_cluster: str
    flow_tension_score: float
    strike_cluster_state: str
    dominant_strike: float | None = None
    repeated_snapshot_state: str
    skew_evolution_state: str
    tenor_curve_state: str
    pin_progression_state: str
    pin_progression_velocity: float | None = None
    reasons: list[str] = Field(default_factory=list)


class InventoryState(BaseModel):
    """Held exposure, thesis lifecycle, and deployment-control inputs."""

    model_config = ConfigDict(extra="forbid")

    existing_inventory_pct: float = Field(ge=0.0, le=100.0)
    fresh_cash_pct: float = Field(ge=0.0, le=100.0)
    overnight_inventory_pct: float = Field(ge=0.0, le=100.0, default=0.0)
    open_orders_count: int = Field(ge=0, default=0)
    capital_lockup_pct: float = Field(ge=0.0, le=100.0, default=0.0)
    cost_basis_gap_pct: float = 0.0
    thesis_state_input: str = "valid"
    adverse_excursion_pct: float = 0.0
    time_stop_minutes_remaining: int | None = Field(default=None, ge=0)
    thesis_age_minutes: int | None = Field(default=None, ge=0)


class PostureRiskInput(BaseModel):
    """Inputs required for posture and risk permission."""

    model_config = ConfigDict(extra="forbid")

    temporal: TemporalContextOutput
    regime: MarketRegimeContextOutput
    options_flow: OptionsFlowContextOutput
    inventory: InventoryState
    risk_budget_remaining_pct: float = Field(ge=0.0, le=100.0)


class PostureRiskOutput(BaseModel):
    """Binding posture, permission, and deployable-capital output."""

    model_config = ConfigDict(extra="forbid")

    permission_state: PermissionState
    posture_label: str
    inventory_posture_state: str
    fresh_deployable_capital_pct: float
    overnight_deployable_capital_pct: float
    inventory_action_bias: str
    fresh_vs_inventory_state: str
    thesis_state: str
    capital_lockup_state: str
    adverse_excursion_state: str
    time_stop_state: str
    signal_conflict_state: str
    time_stop_minutes_remaining: int | None = None
    thesis_pressure_score: float
    modifier_runtime_packet: ModifierRuntimePacket | None = None
    stand_down_class: NonActionClass | None = None
    conflict_classes: list[SignalConflictClass] = Field(default_factory=list)
    degradation_step: DegradationStep = DegradationStep.NORMAL
    override_disposition: OverrideDisposition = OverrideDisposition.NOT_APPLICABLE
    reasons: list[str] = Field(default_factory=list)


class PlaybookFamilyCandidate(BaseModel):
    """Candidate playbook-family status inside the desk-cognition runtime."""

    model_config = ConfigDict(extra="forbid")

    family_id: str
    decision: PlaybookDecision
    active_setup_variant_ids: list[str] = Field(default_factory=list)
    watch_setup_variant_ids: list[str] = Field(default_factory=list)
    active_playbook_ids: list[str] = Field(default_factory=list)
    watch_playbook_ids: list[str] = Field(default_factory=list)
    reasons: list[str] = Field(default_factory=list)


class SetupVariantCandidate(BaseModel):
    """Candidate setup-variant status inside the desk-cognition runtime."""

    model_config = ConfigDict(extra="forbid")

    setup_variant_id: str
    family_id: str
    execution_expression_id: str | None = None
    horizon: str | None = None
    legacy_playbook_id: str | None = None
    decision: PlaybookDecision
    action_bias: PlaybookAction = PlaybookAction.HOLD
    sizing_fraction: float = Field(default=0.0, ge=0.0, le=1.0)
    hedge_overlay: bool = False
    reasons: list[str] = Field(default_factory=list)


class PlaybookCandidate(BaseModel):
    """Legacy-compatible playbook candidate derived from native setup-variant selection."""

    model_config = ConfigDict(extra="forbid")

    playbook_id: str
    family_id: str | None = None
    setup_variant_id: str | None = None
    execution_expression_id: str | None = None
    horizon: str | None = None
    decision: PlaybookDecision
    action_bias: PlaybookAction = PlaybookAction.HOLD
    sizing_fraction: float = Field(default=0.0, ge=0.0, le=1.0)
    hedge_overlay: bool = False
    reasons: list[str] = Field(default_factory=list)


class CandidateAdjudicationRecord(BaseModel):
    """Deterministic record of how one eligible playbook candidate was ranked."""

    model_config = ConfigDict(extra="forbid")

    playbook_id: str
    family_id: str | None = None
    setup_variant_id: str | None = None
    action_bias: PlaybookAction = PlaybookAction.HOLD
    sizing_fraction: float = Field(default=0.0, ge=0.0, le=1.0)
    score: float
    registry_priority: int = Field(ge=1)
    contradiction_tags: list[str] = Field(default_factory=list)
    reasons: list[str] = Field(default_factory=list)


class PlaybookEligibilityInput(BaseModel):
    """Inputs required to classify playbook eligibility."""

    model_config = ConfigDict(extra="forbid")

    temporal: TemporalContextOutput
    regime: MarketRegimeContextOutput
    options_flow: OptionsFlowContextOutput
    posture: PostureRiskOutput


class PlaybookEligibilityOutput(BaseModel):
    """Eligibility output for the current desk-cognition snapshot."""

    model_config = ConfigDict(extra="forbid")

    family_candidates: list[PlaybookFamilyCandidate] = Field(default_factory=list)
    setup_variant_candidates: list[SetupVariantCandidate] = Field(default_factory=list)
    candidates: list[PlaybookCandidate] = Field(default_factory=list)
    active_family_ids: list[str] = Field(default_factory=list)
    watch_family_ids: list[str] = Field(default_factory=list)
    active_setup_variant_ids: list[str] = Field(default_factory=list)
    watch_setup_variant_ids: list[str] = Field(default_factory=list)
    add_candidates: list[str] = Field(default_factory=list)
    hold_candidates: list[str] = Field(default_factory=list)
    trim_candidates: list[str] = Field(default_factory=list)
    reduce_candidates: list[str] = Field(default_factory=list)
    hedge_candidates: list[str] = Field(default_factory=list)
    probe_candidates: list[str] = Field(default_factory=list)
    watch_only_candidates: list[str] = Field(default_factory=list)
    no_trade_reasons: list[str] = Field(default_factory=list)
    rejected_playbook_reasons: dict[str, list[str]] = Field(default_factory=dict)
    reasons: list[str] = Field(default_factory=list)


class ExecutionExpressionInput(BaseModel):
    """Inputs required to derive deterministic expression and execution."""

    model_config = ConfigDict(extra="forbid")

    temporal: TemporalContextOutput
    regime: MarketRegimeContextOutput
    options_flow: OptionsFlowContextOutput
    posture: PostureRiskOutput
    eligibility: PlaybookEligibilityOutput
    modifier_runtime_packet: ModifierRuntimePacket | None = None


class FinalRiskJoinSurface(BaseModel):
    """Structured record of the final risk authority join after execution synthesis."""

    model_config = ConfigDict(extra="forbid")

    action: RiskAction
    confidence_scalar: float = Field(ge=0.0, le=1.0)
    reasons: list[str] = Field(default_factory=list)
    joined_after_stage: str = "execution_synthesis"
    source_service: str = "risk_gateway"
    lineage_tags: list[str] = Field(default_factory=list)
    execution_effect: str


class ExecutionExpressionOutput(BaseModel):
    """Deterministic execution-expression output."""

    model_config = ConfigDict(extra="forbid")

    active_playbook_ids: list[str] = Field(default_factory=list)
    active_setup_variant_ids: list[str] = Field(default_factory=list)
    active_family_ids: list[str] = Field(default_factory=list)
    pre_final_risk_active_playbook_ids: list[str] = Field(default_factory=list)
    pre_final_risk_lead_playbook_id: str | None = None
    pre_final_risk_entry_style: str | None = None
    lead_playbook_id: str | None = None
    lead_setup_variant_id: str | None = None
    lead_family_id: str | None = None
    adjudication_method: str = "candidate_score_v1"
    contradiction_resolution: str | None = None
    lead_selection_score: float | None = None
    lead_selection_reasons: list[str] = Field(default_factory=list)
    candidate_adjudication: list[CandidateAdjudicationRecord] = Field(default_factory=list)
    entry_style: str
    playbook_execution_styles: dict[str, str] = Field(default_factory=dict)
    setup_variant_execution_styles: dict[str, str] = Field(default_factory=dict)
    entry_gate_score_floor: float = 0.65
    zone_score_threshold: float = 0.50
    distance_to_vwap_soft_limit_pct: float = 1.50
    risk_vix_caution_threshold: float = 24.0
    risk_vix_hot_threshold: float = 32.0
    max_risk_per_trade: float = 0.35
    passive_aggressive_bias: str = "balanced"
    ladder_spacing_bps: float = 0.0
    max_chase_distance_bps: float = 0.0
    stop_distance_bps: float = 0.0
    take_profit_distance_bps: float = 0.0
    hedge_ratio: float = 0.0
    per_slice_risk_pct: float = 0.0
    geometry_notes: list[str] = Field(default_factory=list)
    hedge_required: bool
    inventory_action: str
    fresh_capital_action: str
    thesis_invalidation_state: str
    target_fresh_deployable_pct: float
    scaling_plan: list[float] = Field(default_factory=list)
    invalidation_reasons: list[str] = Field(default_factory=list)
    exit_reasons: list[str] = Field(default_factory=list)
    exit_plan: list[str] = Field(default_factory=list)
    modifier_runtime_packet: ModifierRuntimePacket | None = None
    final_risk_join: FinalRiskJoinSurface | None = None
    reasons: list[str] = Field(default_factory=list)


class RuntimeStateVector(BaseModel):
    """Approved state-vector slice readable by Gate 60 modifier policy."""

    model_config = ConfigDict(extra="forbid")

    desk_window: str
    clock_envelope: str
    day_phase_state: DayPhaseState
    carry_horizon_state: CarryHorizonState
    carryover_state: str
    expiry_cycle_state: str
    event_proximity_state: str
    event_window_state: str
    volatility_regime: VolatilityRegime
    breadth_state: BreadthState
    sector_leadership_state: str
    rates_regime_state: str
    fx_stress_state: str
    signal_conflict_state: str
    term_structure_state: TermStructureState
    skew_state: SkewState
    gamma_state: GammaState
    dealer_pressure_state: str
    options_behavior_cluster: str
    inventory_posture_state: str
    fresh_vs_inventory_state: str
    thesis_state: str
    capital_lockup_state: str
    time_stop_state: str
    permission_state: PermissionState


class EffectivePolicySnapshot(BaseModel):
    """Review-visible snapshot of effective policy surfaces for one decision."""

    model_config = ConfigDict(extra="forbid")

    active_lineage: list[EffectiveCoefficientLineage] = Field(default_factory=list)


class ReviewExplanationInput(BaseModel):
    """Inputs required to reconstruct a deterministic reasoning packet."""

    model_config = ConfigDict(extra="forbid")

    temporal: TemporalContextOutput
    regime: MarketRegimeContextOutput
    options_flow: OptionsFlowContextOutput
    posture: PostureRiskOutput
    eligibility: PlaybookEligibilityOutput
    execution: ExecutionExpressionOutput
    modifier_runtime_packet: ModifierRuntimePacket | None = None
    temporal_input: TemporalContextInput | None = None


class StageReasonPacket(BaseModel):
    """Stage-by-stage reason packet for deterministic review output."""

    model_config = ConfigDict(extra="forbid")

    stage: str
    summary: str
    reasons: list[str] = Field(default_factory=list)


class RejectedPlaybookReason(BaseModel):
    """Explicit rejected-playbook surface required by Gate C review packets."""

    model_config = ConfigDict(extra="forbid")

    playbook_id: str
    decision: PlaybookDecision
    action_bias: PlaybookAction
    reasons: list[str] = Field(default_factory=list)


class ContradictionSurface(BaseModel):
    """One contradiction or tension the review layer must expose."""

    model_config = ConfigDict(extra="forbid")

    contradiction_id: str
    description: str
    implicated_stages: list[str] = Field(default_factory=list)


class PacketLineageSurface(BaseModel):
    """Typed lineage surface for review and replay provenance."""

    model_config = ConfigDict(extra="forbid")

    protocol_version: str = "dmp.v2"
    review_packet_id: str
    decision_packet_id: str
    packet_lineage: list[str] = Field(default_factory=list)
    stage_packet_ids: dict[str, str] = Field(default_factory=dict)


class ReviewExplanationOutput(BaseModel):
    """Structured review and explanation packet for one snapshot."""

    model_config = ConfigDict(extra="forbid")

    summary: str
    conflict_tags: list[str] = Field(default_factory=list)
    signal_conflict_density: float = 0.0
    stage_reason_packets: list[StageReasonPacket] = Field(default_factory=list)
    rejected_playbooks: list[RejectedPlaybookReason] = Field(default_factory=list)
    contradictions: list[ContradictionSurface] = Field(default_factory=list)
    module_attribution: dict[str, float] = Field(default_factory=dict)
    imported_module_citations: list[ImportedModuleReviewCitation] = Field(default_factory=list)
    imported_module_maturity_counts: dict[str, int] = Field(default_factory=dict)
    effective_policy: EffectivePolicySnapshot | None = None
    stability_scorecards: list[SurfaceStabilityScorecard] = Field(default_factory=list)
    review_governance: ReviewGovernanceSurface | None = None
    event_window_governance: TemporalEventWindowSurface | None = None
    precursor_governance: PrecursorGovernanceSurface | None = None
    precursor_runtime_binding: PrecursorRuntimeBindingSurface | None = None
    phase_carry_policy: PhaseCarryoverPolicySurface | None = None
    event_options_stress_policy: EventOptionsStressPolicySurface | None = None
    modifier_control_law: ModifierControlLawSurface | None = None
    review_eligibility: ReviewEligibilitySurface | None = None
    candidate_governance: CandidateGovernanceSurface | None = None
    review_lineage: ReviewLineagePacket | None = None
    failure_taxonomy: ReviewFailurePacket | None = None
    economic_accountability: EconomicContributionPacket | None = None
    promotion_evidence: PromotionEvidencePacket | None = None
    packet_lineage: PacketLineageSurface | None = None
    review_packet: dict[str, object]


class ModuleDocstringContractTemplate(BaseModel):
    """Required docstring sections for imported desk-runtime services."""

    model_config = ConfigDict(extra="forbid")

    template_id: str
    required_sections: list[str] = Field(default_factory=list)


class RuntimeLayerContract(BaseModel):
    """Deterministic contract for one binding Desk Cognition Grammar layer."""

    model_config = ConfigDict(extra="forbid")

    grammar_role: str
    service_path: str
    service_class_name: str
    input_model_name: str
    output_model_name: str
    required_input_fields: list[str] = Field(default_factory=list)
    optional_input_fields: list[str] = Field(default_factory=list)
    required_output_fields: list[str] = Field(default_factory=list)
    optional_output_fields: list[str] = Field(default_factory=list)
    docstring_required: bool = True
    docstring_contract_sections: list[str] = Field(default_factory=list)


class TraceStagePacket(BaseModel):
    """Trace contract for one executed runtime layer."""

    model_config = ConfigDict(extra="forbid")

    grammar_role: str
    service_path: str
    input_model_name: str
    output_model_name: str
    required_input_fields: list[str] = Field(default_factory=list)
    required_output_fields: list[str] = Field(default_factory=list)
    summary: str


ReviewExplanationOutput.model_rebuild()
