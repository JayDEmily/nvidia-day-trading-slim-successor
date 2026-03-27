"""Build the canonical desk vocabulary document.

The generator stays aligned with the pinned runtime registry and the Gate 60/61
state-policy governance vocabulary so the committed JSON cannot drift from the
authoritative builder.
"""

from __future__ import annotations

from pathlib import Path

from nvda_desk.schemas.playbook_registry import PlaybookHorizon
from nvda_desk.schemas.vocabulary import (
    RawDerivedTag,
    VocabularyCategory,
    VocabularyDocument,
    VocabularyEntry,
)
from nvda_desk.services.playbook_registry import PlaybookRegistryService

OUTPUT_PATH = Path("docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json")


def build_document() -> VocabularyDocument:
    """Return the canonical vocabulary document for the current repo state."""

    registry = PlaybookRegistryService()
    document = registry.document()
    entries: list[VocabularyEntry] = [
        VocabularyEntry(
            canonical_slug="temporal_context",
            canonical_label="Temporal Context",
            category=VocabularyCategory.STAGE,
            stage_owner="temporal_context",
            maps_to_contract="nvda_desk.schemas.cognition.TemporalContextOutput",
            allowed_aliases=["step_1", "time_phase_context"],
            notes=["Binding Stage 1 grammar slot."],
        ),
        VocabularyEntry(
            canonical_slug="market_regime_context",
            canonical_label="Market Regime Context",
            category=VocabularyCategory.STAGE,
            stage_owner="market_regime_context",
            maps_to_contract="nvda_desk.schemas.cognition.MarketRegimeContextOutput",
            allowed_aliases=["regime_context"],
        ),
        VocabularyEntry(
            canonical_slug="options_flow_context",
            canonical_label="Options and Flow Context",
            category=VocabularyCategory.STAGE,
            stage_owner="options_flow_context",
            maps_to_contract="nvda_desk.schemas.cognition.OptionsFlowContextOutput",
            allowed_aliases=["options_context", "flow_context"],
        ),
        VocabularyEntry(
            canonical_slug="posture_risk_permission",
            canonical_label="Posture and Risk Permission",
            category=VocabularyCategory.STAGE,
            stage_owner="posture_risk_permission",
            maps_to_contract="nvda_desk.schemas.cognition.PostureRiskOutput",
            allowed_aliases=["posture_risk", "permission_layer"],
        ),
        VocabularyEntry(
            canonical_slug="playbook_eligibility",
            canonical_label="Playbook Eligibility",
            category=VocabularyCategory.STAGE,
            stage_owner="playbook_eligibility",
            maps_to_contract="nvda_desk.schemas.cognition.PlaybookEligibilityOutput",
            allowed_aliases=["selector_layer"],
        ),
        VocabularyEntry(
            canonical_slug="expression_execution",
            canonical_label="Expression and Execution",
            category=VocabularyCategory.STAGE,
            stage_owner="expression_execution",
            maps_to_contract="nvda_desk.schemas.cognition.ExecutionExpressionOutput",
            allowed_aliases=["execution_expression"],
        ),
        VocabularyEntry(
            canonical_slug="review_explanation",
            canonical_label="Review and Explanation",
            category=VocabularyCategory.STAGE,
            stage_owner="review_explanation",
            maps_to_contract="nvda_desk.schemas.cognition.ReviewExplanationOutput",
            allowed_aliases=["review_packet", "reason_packet"],
        ),
        VocabularyEntry(
            canonical_slug="temporal_state",
            canonical_label="Temporal State",
            category=VocabularyCategory.COMPATIBILITY_SURFACE,
            stage_owner="temporal_context",
            maps_to_contract="nvda_desk.schemas.temporal_surface.TemporalStateFeaturePayload",
            allowed_aliases=["step1_temporal_state"],
            disallowed_phrases=["hard_clock_truth"],
        ),
        VocabularyEntry(
            canonical_slug="session_clock",
            canonical_label="Session Clock",
            category=VocabularyCategory.COMPATIBILITY_SURFACE,
            stage_owner="temporal_context",
            maps_to_contract="nvda_desk.schemas.session_clock.SessionClockFeaturePayload",
            allowed_aliases=["session_clock_wrapper"],
            disallowed_phrases=["canonical_step1_truth"],
            notes=["Explicit compatibility wrapper retained over temporal_state."],
        ),
        VocabularyEntry(
            canonical_slug="raw_primitive",
            canonical_label="Raw Primitive",
            category=VocabularyCategory.DATA_CLASSIFICATION,
            stage_owner="research_doctrine",
            raw_or_derived=RawDerivedTag.RAW,
            maps_to_contract="docs/planning/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3.xlsx",
            allowed_aliases=["raw_signal"],
        ),
        VocabularyEntry(
            canonical_slug="derived_feature",
            canonical_label="Derived Feature",
            category=VocabularyCategory.DATA_CLASSIFICATION,
            stage_owner="research_doctrine",
            raw_or_derived=RawDerivedTag.DERIVED,
            maps_to_contract="docs/planning/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3.xlsx",
            allowed_aliases=["derived_state"],
        ),
        VocabularyEntry(
            canonical_slug="vocabulary_workflow",
            canonical_label="Vocabulary Workflow",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="planning_governance",
            maps_to_contract="docs/vocabulary/CONSOLIDATION_WORKFLOW.md",
            allowed_aliases=["consolidation_workflow"],
        ),
        VocabularyEntry(
            canonical_slug="calendar_horizon_gate",
            canonical_label="Calendar Horizon Gate",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="step0_calendar_horizon",
            maps_to_contract="docs/planning/2026-03-26_CALENDAR_HORIZON_OWNERSHIP.md",
            allowed_aliases=["step_0", "horizon_router"],
            notes=["Explicit runtime routing concern that selects intraday vs carry evaluation horizon."],
        ),
        VocabularyEntry(
            canonical_slug="candidate_family_generation",
            canonical_label="Candidate Family Generation",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="playbook_eligibility",
            maps_to_contract="docs/planning/2026-03-26_COGNITIVE_WORKFLOW_IMPLEMENTATION_MAP.md",
            allowed_aliases=["family_generation", "candidate_setup_generation"],
            notes=["Owned by the playbook-selection grammar slot rather than Step 1 or posture."],
        ),
        VocabularyEntry(
            canonical_slug="playbook_family",
            canonical_label="Playbook Family",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="playbook_eligibility",
            maps_to_contract="nvda_desk.schemas.playbook_registry.PlaybookFamilySpec",
            allowed_aliases=["family_layer"],
        ),
        VocabularyEntry(
            canonical_slug="setup_variant",
            canonical_label="Setup Variant",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="playbook_eligibility",
            maps_to_contract="nvda_desk.schemas.playbook_registry.SetupVariantSpec",
            allowed_aliases=["deterministic_setup_variant"],
        ),
        VocabularyEntry(
            canonical_slug="execution_expression",
            canonical_label="Execution Expression",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="expression_execution",
            maps_to_contract="nvda_desk.schemas.playbook_registry.ExecutionTemplateSpec",
            allowed_aliases=["execution_shape"],
        ),
        VocabularyEntry(
            canonical_slug="carry_handoff",
            canonical_label="Carry Handoff",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="carry_horizon",
            maps_to_contract="nvda_desk.schemas.overnight.CloseStateCarryHandoff",
            allowed_aliases=["close_state_handoff"],
            notes=["Typed bridge from intraday close-state into overnight/weekend/event carry evaluation."],
        ),
        VocabularyEntry(
            canonical_slug="carry_horizon_branch",
            canonical_label="Carry Horizon Branch",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="carry_horizon",
            maps_to_contract="nvda_desk.schemas.overnight.CarryHorizon",
            allowed_aliases=["carry_branch"],
            notes=["Separate horizon branch for overnight, weekend, and event carry decisions."],
        ),
        VocabularyEntry(
            canonical_slug="state_vector",
            canonical_label="State Vector",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="review_explanation",
            maps_to_contract="nvda_desk.schemas.cognition.RuntimeStateVector",
            allowed_aliases=["approved_state_vector"],
            notes=["Gate 60 freezes the readable runtime state fields before policy matrices exist."],
        ),
        VocabularyEntry(
            canonical_slug="baseline_coefficient",
            canonical_label="Baseline Coefficient",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="planning_governance",
            maps_to_contract="nvda_desk.schemas.state_policy.RuntimeSurfaceClass",
            allowed_aliases=["release_coefficient"],
            disallowed_phrases=["live_tuning"],
            notes=["May change only through reviewed release, never through runtime self-adjustment."],
        ),
        VocabularyEntry(
            canonical_slug="state_conditioned_modifier",
            canonical_label="State-Conditioned Modifier",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="planning_governance",
            maps_to_contract="nvda_desk.schemas.state_policy.ModifierPolicySpec",
            allowed_aliases=["bounded_modifier"],
            disallowed_phrases=["freeform_override"],
            notes=["Approved runtime policy object that deforms posture without mutating cognition grammar."],
        ),
        VocabularyEntry(
            canonical_slug="effective_coefficient",
            canonical_label="Effective Coefficient",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="review_explanation",
            maps_to_contract="nvda_desk.schemas.state_policy.EffectiveCoefficientLineage",
            allowed_aliases=["effective_policy_surface"],
            notes=["Lawful baseline-plus-modifier result recorded for review lineage."],
        ),
        VocabularyEntry(
            canonical_slug="prohibited_runtime_variation",
            canonical_label="Prohibited Runtime Variation",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="planning_governance",
            maps_to_contract="nvda_desk.schemas.state_policy.ProhibitedRuntimeSurface",
            allowed_aliases=["locked_surface"],
            disallowed_phrases=["runtime_rewrite"],
            notes=["Surfaces such as grammar order, calendar truth, and baseline values remain locked at runtime."],
        ),
        VocabularyEntry(
            canonical_slug="stand_down_class",
            canonical_label="Stand-Down Class",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="review_explanation",
            maps_to_contract="nvda_desk.schemas.state_policy.NonActionClass",
            allowed_aliases=["non_action_class"],
            notes=["Gate 61 makes disciplined non-participation a first-class governed outcome."],
        ),
        VocabularyEntry(
            canonical_slug="conflict_class",
            canonical_label="Conflict Class",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="review_explanation",
            maps_to_contract="nvda_desk.schemas.state_policy.SignalConflictClass",
            allowed_aliases=["signal_conflict_class"],
            notes=["Ordered conflict severity remains visible in review rather than being silently absorbed."],
        ),
        VocabularyEntry(
            canonical_slug="degradation_step",
            canonical_label="Degradation Step",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="posture_risk_permission",
            maps_to_contract="nvda_desk.schemas.state_policy.DegradationStep",
            allowed_aliases=["posture_degradation_step"],
            notes=["Ordered ladder from confirmation tightening through stand-down and veto."],
        ),
        VocabularyEntry(
            canonical_slug="override_disposition",
            canonical_label="Override Disposition",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="review_explanation",
            maps_to_contract="nvda_desk.schemas.state_policy.OverrideDisposition",
            allowed_aliases=["override_status"],
            disallowed_phrases=["trader_feel_override"],
            notes=["Gate 61 forbids smuggled discretionary runtime behaviour and allows only bounded audit/release pathways."],
        ),
        VocabularyEntry(
            canonical_slug="stability_scorecard",
            canonical_label="Stability Scorecard",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="review_explanation",
            maps_to_contract="nvda_desk.schemas.state_policy.SurfaceStabilityScorecard",
            allowed_aliases=["surface_scorecard"],
            notes=["Gate 62 freezes the multi-axis stability surface before review law or candidate comparison."],
        ),
        VocabularyEntry(
            canonical_slug="corridor_zone",
            canonical_label="Corridor Zone",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="review_explanation",
            maps_to_contract="nvda_desk.schemas.state_policy.CorridorZone",
            allowed_aliases=["target_drift_breach_zone"],
            notes=["Target, tolerated-drift, and breach zones remain explicit in governed scorecards."],
        ),
        VocabularyEntry(
            canonical_slug="review_evidence_block",
            canonical_label="Review Evidence Block",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="review_explanation",
            maps_to_contract="nvda_desk.schemas.state_policy.ReviewEvidenceBlock",
            allowed_aliases=["evidence_floor_block"],
            notes=["Gate 63 requires explicit evidence floors before a surface may become review-eligible."],
        ),
        VocabularyEntry(
            canonical_slug="review_outcome",
            canonical_label="Review Outcome",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="review_explanation",
            maps_to_contract="nvda_desk.schemas.state_policy.ReviewOutcome",
            allowed_aliases=["governed_review_outcome"],
            notes=["Includes review_not_eligible and review_no_change as first-class governed results."],
        ),
        VocabularyEntry(
            canonical_slug="candidate_role",
            canonical_label="Candidate Role",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="review_explanation",
            maps_to_contract="nvda_desk.schemas.state_policy.CandidateRole",
            allowed_aliases=["candidate_state_role"],
            notes=["Gate 64 limits candidate roles to champion, shadow challenger, dormant candidate, and retired candidate."],
        ),
        VocabularyEntry(
            canonical_slug="adjudication_disposition",
            canonical_label="Adjudication Disposition",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="review_explanation",
            maps_to_contract="nvda_desk.schemas.state_policy.AdjudicationDisposition",
            allowed_aliases=["reserved_span_state"],
            notes=["The reserved adjudication span stays explicit so live paper cannot quietly exhaust it."],
        ),
        VocabularyEntry(
            canonical_slug="event_taxonomy",
            canonical_label="Event Taxonomy",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="temporal_context",
            maps_to_contract="nvda_desk.schemas.events.EventTaxonomyAuthorityPacket",
            allowed_aliases=["bounded_event_identity"],
            notes=["Gate 65 freezes desk-relevant event classes, subclasses, materiality, and semantic phases."],
        ),
        VocabularyEntry(
            canonical_slug="desk_calendar_contract",
            canonical_label="Desk Calendar Contract",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="temporal_context",
            maps_to_contract="nvda_desk.schemas.session_clock.DeskCalendarAuthorityPacket",
            allowed_aliases=["venue_calendar_authority"],
            notes=["Gate 66 freezes venue/timezone/closure/bridge semantics before runtime plumbing."],
        ),
        VocabularyEntry(
            canonical_slug="event_window_state",
            canonical_label="Event Window State",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="temporal_context",
            maps_to_contract="nvda_desk.schemas.temporal_surface.EventWindowAuthorityPacket",
            allowed_aliases=["event_window_semantics"],
            notes=["Gate 67 freezes event proximity, overlap, cooling-off, and event-memory semantics before later policy gates."],
        ),
    ]
    for horizon in PlaybookHorizon:
        entries.append(
            VocabularyEntry(
                canonical_slug=horizon.value,
                canonical_label=horizon.value.replace("_", " ").title(),
                category=VocabularyCategory.HORIZON,
                stage_owner="playbook_eligibility",
                horizon=horizon.value,
                maps_to_contract="nvda_desk.schemas.playbook_registry.PlaybookHorizon",
                allowed_aliases=[f"carry_{horizon.value}"],
            )
        )
    for family in document.families:
        entries.append(
            VocabularyEntry(
                canonical_slug=family.family_id,
                canonical_label=family.title,
                category=VocabularyCategory.PLAYBOOK_FAMILY,
                stage_owner="playbook_eligibility",
                family=family.family_id,
                maps_to_contract="nvda_desk.schemas.playbook_registry.PlaybookFamilySpec",
                allowed_aliases=[f"family:{family.family_id}"],
                notes=list(family.notes),
            )
        )
    template_index = document.execution_template_index()
    for variant in document.setup_variants:
        template = template_index[variant.execution_expression_id]
        entries.append(
            VocabularyEntry(
                canonical_slug=variant.setup_variant_id,
                canonical_label=variant.title,
                category=VocabularyCategory.SETUP_VARIANT,
                stage_owner="playbook_eligibility",
                family=variant.family_id,
                setup_variant=variant.setup_variant_id,
                execution_expression=variant.execution_expression_id,
                horizon=variant.horizon.value,
                maps_to_contract="nvda_desk.schemas.playbook_registry.SetupVariantSpec",
                allowed_aliases=[f"legacy_playbook:{variant.legacy_playbook_id}"] if variant.legacy_playbook_id else [],
                notes=list(variant.notes),
            )
        )
        entries.append(
            VocabularyEntry(
                canonical_slug=template.template_id,
                canonical_label=template.entry_style.replace("_", " ").title(),
                category=VocabularyCategory.EXECUTION_EXPRESSION,
                stage_owner="expression_execution",
                family=variant.family_id,
                setup_variant=variant.setup_variant_id,
                execution_expression=template.template_id,
                horizon=variant.horizon.value,
                maps_to_contract="nvda_desk.schemas.playbook_registry.ExecutionTemplateSpec",
                allowed_aliases=[template.entry_style],
                notes=[template.thesis_invalidation_state],
            )
        )
    return VocabularyDocument(
        schema_version="desk_vocabulary.v1",
        registry_version="gate64-review-governance-alignment-2026-03-27",
        notes=[
            "Generated from current live playbook registry and pinned architecture surfaces.",
            "Gates 60-64 extend the workflow vocabulary with state-policy, non-action, stability, review-law, and candidate-governance terms.",
            "Vocabulary workflow is feeder-process only and must not be treated as blind runtime truth.",
        ],
        entries=entries,
    )


def main() -> None:
    """Write the generated vocabulary document to the committed JSON path."""

    document = build_document()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(document.to_json_text(), encoding="utf-8")


if __name__ == "__main__":
    main()
