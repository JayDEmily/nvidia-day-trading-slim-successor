"""Binding state-policy and non-action authority contracts.

Gate 60 freezes what kind of runtime surface is allowed to vary, which state
fields modifiers may read, and which transform family is lawful. Gate 61 then
freezes non-action, conflict, degradation, and override law before later policy
matrices or runtime wiring can rely on informal desk language.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class PolicyStageOwner(StrEnum):
    """Canonical owner stages for state-policy and conflict governance."""

    CALENDAR_HORIZON = "calendar_horizon"
    TEMPORAL = "temporal"
    REGIME = "regime"
    OPTIONS_FLOW = "options_flow"
    POSTURE = "posture"
    ELIGIBILITY = "eligibility"
    EXECUTION = "execution"
    REVIEW = "review"
    EVENT = "event"
    PRECURSOR = "precursor"


class RuntimeSurfaceClass(StrEnum):
    """Lawful ontology for surfaces mentioned by adaptation policy."""

    INVARIANT = "invariant"
    BASELINE_COEFFICIENT = "baseline_coefficient"
    STATE_CONDITIONED_MODIFIER = "state_conditioned_modifier"
    EFFECTIVE_COEFFICIENT = "effective_coefficient"
    REVIEW_ONLY_METRIC = "review_only_metric"
    PROHIBITED_RUNTIME_VARIATION = "prohibited_runtime_variation"


class ModifierTransformType(StrEnum):
    """Bounded transform family approved for state-conditioned modifiers."""

    MULTIPLICATIVE_SCALE = "multiplicative_scale"
    ADDITIVE_OFFSET = "additive_offset"
    CLAMP = "clamp"
    RANK_WEIGHT_ADJUSTMENT = "rank_weight_adjustment"
    SUPPRESSION_VETO = "suppression_veto"


class MutableRuntimeSurface(StrEnum):
    """Runtime surfaces that may lawfully receive approved modifier policy."""

    ENTRY_GATE_SCORE_FLOOR = "entry_gate_score_floor"
    ZONE_SCORE_THRESHOLD = "zone_score_threshold"
    DISTANCE_TO_VWAP_SOFT_LIMIT_PCT = "distance_to_vwap_soft_limit_pct"
    RISK_VIX_CAUTION_THRESHOLD = "risk_vix_caution_threshold"
    RISK_VIX_HOT_THRESHOLD = "risk_vix_hot_threshold"
    MAX_RISK_PER_TRADE = "max_risk_per_trade"
    TARGET_FRESH_DEPLOYABLE_PCT = "target_fresh_deployable_pct"
    HEDGE_REQUIRED = "hedge_required"


class ProhibitedRuntimeSurface(StrEnum):
    """Surfaces that must never vary through runtime state-conditioned policy."""

    DESK_COGNITION_GRAMMAR_ORDER = "desk_cognition_grammar_order"
    STAGE_OWNER_ASSIGNMENTS = "stage_owner_assignments"
    BASELINE_COEFFICIENT_VALUES = "baseline_coefficient_values"
    CALENDAR_TRUTH = "calendar_truth"
    EVENT_IDENTITY = "event_identity"
    RAW_MARKET_FACTS = "raw_market_facts"
    PLAYBOOK_REGISTRY_MEMBERSHIP = "playbook_registry_membership"
    REVIEW_PACKET_LINEAGE = "review_packet_lineage"


class CanonicalStateVectorField(StrEnum):
    """Approved state-vector fields readable by modifier policy."""

    DESK_WINDOW = "desk_window"
    CLOCK_ENVELOPE = "clock_envelope"
    CARRYOVER_STATE = "carryover_state"
    EXPIRY_CYCLE_STATE = "expiry_cycle_state"
    EVENT_PROXIMITY_STATE = "event_proximity_state"
    EVENT_WINDOW_STATE = "event_window_state"
    VOLATILITY_REGIME = "volatility_regime"
    BREADTH_STATE = "breadth_state"
    SECTOR_LEADERSHIP_STATE = "sector_leadership_state"
    RATES_REGIME_STATE = "rates_regime_state"
    FX_STRESS_STATE = "fx_stress_state"
    SIGNAL_CONFLICT_STATE = "signal_conflict_state"
    TERM_STRUCTURE_STATE = "term_structure_state"
    SKEW_STATE = "skew_state"
    GAMMA_STATE = "gamma_state"
    DEALER_PRESSURE_STATE = "dealer_pressure_state"
    OPTIONS_BEHAVIOR_CLUSTER = "options_behavior_cluster"
    INVENTORY_POSTURE_STATE = "inventory_posture_state"
    FRESH_VS_INVENTORY_STATE = "fresh_vs_inventory_state"
    THESIS_STATE = "thesis_state"
    CAPITAL_LOCKUP_STATE = "capital_lockup_state"
    TIME_STOP_STATE = "time_stop_state"
    PERMISSION_STATE = "permission_state"


class StateVectorFieldSpec(BaseModel):
    """One governed state-vector field specification."""

    model_config = ConfigDict(extra="forbid")

    field: CanonicalStateVectorField
    owner_stage: PolicyStageOwner
    source_contract: str = Field(min_length=1)
    posture_triggering: bool = False
    review_visible: bool = True
    notes: list[str] = Field(default_factory=list)


class ModifierPolicySpec(BaseModel):
    """Typed object model for one approved state-conditioned modifier."""

    model_config = ConfigDict(extra="forbid")

    modifier_id: str = Field(min_length=1)
    target_surface: MutableRuntimeSurface
    activation_fields: list[CanonicalStateVectorField] = Field(default_factory=list)
    target_stage_owner: PolicyStageOwner
    transform_type: ModifierTransformType
    cap: float | None = None
    floor: float | None = None
    additive_offset: float | None = None
    multiplicative_scale: float | None = None
    rank_weight_delta: float | None = None
    suppresses_output: bool = False
    precedence_hint: str = ""
    explanation_tags: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class EffectiveCoefficientLineage(BaseModel):
    """Explain how baseline plus approved modifiers yielded one effective surface."""

    model_config = ConfigDict(extra="forbid")

    target_surface: MutableRuntimeSurface
    baseline_reference: str = Field(min_length=1)
    active_modifier_policy_ids: list[str] = Field(default_factory=list)
    explanation_id: str | None = None


class StatePolicyAuthorityPacket(BaseModel):
    """Frozen Gate 60 authority packet for downstream config and review hooks."""

    model_config = ConfigDict(extra="forbid")

    invariants: list[str] = Field(default_factory=list)
    mutable_surfaces: list[MutableRuntimeSurface] = Field(default_factory=list)
    prohibited_surfaces: list[ProhibitedRuntimeSurface] = Field(default_factory=list)
    readable_state_fields: list[CanonicalStateVectorField] = Field(default_factory=list)
    allowed_transform_types: list[ModifierTransformType] = Field(default_factory=list)


class NonActionClass(StrEnum):
    """First-class stand-down classes recognised by runtime and review."""

    DATA_QUALITY_STAND_DOWN = "data_quality_stand_down"
    TEMPORAL_STAND_DOWN = "temporal_stand_down"
    EVENT_RISK_STAND_DOWN = "event_risk_stand_down"
    REGIME_STAND_DOWN = "regime_stand_down"
    OPTIONS_FLOW_STAND_DOWN = "options_flow_stand_down"
    POSTURE_RISK_STAND_DOWN = "posture_risk_stand_down"
    ELIGIBILITY_STAND_DOWN = "eligibility_stand_down"
    EXECUTION_READINESS_STAND_DOWN = "execution_readiness_stand_down"


class SignalConflictClass(StrEnum):
    """Ordered conflict classes from mild divergence to hard veto."""

    OBSERVATION_DIVERGENCE = "observation_divergence"
    CONFIRMATION_CONFLICT = "confirmation_conflict"
    POSTURE_DEGRADATION = "posture_degradation"
    HARD_VETO_CONFLICT = "hard_veto_conflict"


class DegradationStep(StrEnum):
    """Ordered posture degradation ladder used before or at stand-down."""

    NORMAL = "normal"
    CONFIRMATION_TIGHTENED = "confirmation_tightened"
    CONFIDENCE_REDUCED = "confidence_reduced"
    SIZE_REDUCED = "size_reduced"
    WATCH_ONLY = "watch_only"
    STAND_DOWN = "stand_down"
    VETO = "veto"


class OverrideDisposition(StrEnum):
    """Permitted override or annotation posture for deterministic runtime review."""

    NOT_APPLICABLE = "not_applicable"
    AUDIT_ANNOTATION_ONLY = "audit_annotation_only"
    HUMAN_REVIEW_RELEASE_ONLY = "human_review_release_only"
    FORBIDDEN = "forbidden"


class ConflictResolutionPolicy(BaseModel):
    """One governed conflict-resolution rule."""

    model_config = ConfigDict(extra="forbid")

    conflict_class: SignalConflictClass
    primary_owner_stage: PolicyStageOwner
    secondary_owner_stages: list[PolicyStageOwner] = Field(default_factory=list)
    default_degradation_step: DegradationStep
    escalates_to_veto: bool = False
    visibility_required: bool = True
    notes: list[str] = Field(default_factory=list)


class NonActionAuthorityRecord(BaseModel):
    """One governed stand-down rule and its evidence requirement."""

    model_config = ConfigDict(extra="forbid")

    stand_down_class: NonActionClass
    blocking_owner_stage: PolicyStageOwner
    evidence_required: list[str] = Field(default_factory=list)
    review_note_required: bool = True
    notes: list[str] = Field(default_factory=list)


class NonActionAuthorityPacket(BaseModel):
    """Frozen Gate 61 authority packet for non-action and conflict law."""

    model_config = ConfigDict(extra="forbid")

    non_action_classes: list[NonActionClass] = Field(default_factory=list)
    conflict_classes: list[SignalConflictClass] = Field(default_factory=list)
    degradation_steps: list[DegradationStep] = Field(default_factory=list)
    override_dispositions: list[OverrideDisposition] = Field(default_factory=list)
