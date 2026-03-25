from __future__ import annotations

from pathlib import Path

from nvda_desk.schemas.playbook_registry import PlaybookHorizon
from nvda_desk.schemas.vocabulary import RawDerivedTag, VocabularyCategory, VocabularyDocument, VocabularyEntry
from nvda_desk.services.playbook_registry import PlaybookRegistryService

OUTPUT_PATH = Path("docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json")


def build_document() -> VocabularyDocument:
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
        registry_version="gate50-rebase-2026-03-25",
        notes=[
            "Generated from current live playbook registry and pinned architecture surfaces.",
            "Vocabulary workflow is feeder-process only and must not be treated as blind runtime truth.",
        ],
        entries=entries,
    )


def main() -> None:
    document = build_document()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(document.to_json_text(), encoding="utf-8")


if __name__ == "__main__":
    main()
