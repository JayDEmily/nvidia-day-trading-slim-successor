"""Desk Module Protocol (DMP) v1 typed envelope.

Gate 8 introduces one internal packet wrapper for desk-runtime stage and module
outputs. The payload remains a concrete typed model from the existing schema
surface; DMP adds deterministic metadata around that payload instead of
flattening it into untyped dictionaries.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from nvda_desk.schemas.calibration import (
    CoefficientAuditPacket,
    CoefficientSet,
    ComparisonReport,
    ReplayRunResult,
    StackDefinition,
)
from nvda_desk.schemas.cognition import (
    ExecutionExpressionOutput,
    MarketRegimeContextOutput,
    OptionsFlowContextOutput,
    PlaybookEligibilityOutput,
    PostureRiskOutput,
    ReviewExplanationOutput,
    TemporalContextOutput,
)
from nvda_desk.schemas.imported_modules.context_scanners import (
    AsiaPrecursorContextFilterContractOutput,
    EngineScoreContractOutput,
    ExecutionContextScoreContractOutput,
    MacroAdaptiveWeightingFilterContractOutput,
    MacroSignalScoreContractOutput,
    OptionsBehaviourClusterContractOutput,
    VixSpreadDetectorContractOutput,
    VolCorridorContractOutput,
)
from nvda_desk.schemas.imported_modules.execution_lifecycle import (
    DynamicPartialExitModelContractOutput,
    ExecutionLogWriterContractOutput,
    ExecutionTagsContractOutput,
    FillFeedbackRouterContractOutput,
    LadderContinuityTrackerContractOutput,
    PositionBookContractOutput,
    TakeProfitContractOutput,
    TradeLoggerContractOutput,
    TradeReentryMarkerContractOutput,
    TrailingStopContractOutput,
    UnrealizedTrackerContractOutput,
)
from nvda_desk.schemas.imported_modules.execution_planning import (
    BrokerAdapterContractOutput,
    EntryPlannerContractOutput,
    OrderSimulatorContractOutput,
    PositionAllocatorContractOutput,
    RunTradingBotContractOutput,
)
from nvda_desk.schemas.imported_modules.ladder_readiness_overlays import (
    VvixLadderShaperContractOutput,
)
from nvda_desk.schemas.imported_modules.market_context_synthesis import (
    RunSignalScanContractOutput,
)
from nvda_desk.schemas.imported_modules.market_substrate import (
    MacroDataCaptureContractOutput,
    OptionsDataCaptureContractOutput,
    OptionsMetadataCaptureContractOutput,
    PeerEquityCaptureContractOutput,
    SpotDataCaptureContractOutput,
    VwapAccumulatorContractOutput,
    VwapRocContractOutput,
)
from nvda_desk.schemas.imported_modules.posture_enrichers import (
    ArchetypeTaggerContractOutput,
    CompressionRegimeDetectorContractOutput,
    FillBiasAdjusterContractOutput,
    ObvViFlowConfirmationContractOutput,
    TailHedgeInjectorContractOutput,
    VolatilitySentimentIndexContractOutput,
)
from nvda_desk.schemas.imported_modules.review_attribution import (
    ConfidenceDivergenceLoggerContractOutput,
    DailySummaryContractOutput,
    FeedbackSummaryWriterContractOutput,
    MacroAlignmentCheckerContractOutput,
    ModuleScoreAttributorContractOutput,
    ModuleTraceAttributionContractOutput,
    ProfitLossLedgerContractOutput,
    VariantPerformanceTrackerContractOutput,
    VariantTraceLoggerContractOutput,
)
from nvda_desk.schemas.imported_modules.tranche_a import (
    ArchetypeMatcherContractOutput,
    ConvictionTierAllocatorContractOutput,
    EntryGateContractOutput,
    EventFlagCaptureContractOutput,
    GammaPressureContractOutput,
    IvVsRvAnalysisContractOutput,
    LadderConstructorContractOutput,
    ModelConfidenceScorerContractOutput,
    PeerDivergenceContractOutput,
    RealizedVolatilityEngineContractOutput,
    SignalConflictDetectorContractOutput,
    SkewInflectionContractOutput,
    VolumeSpikeFilterContractOutput,
)


class DmpGrammarRole(StrEnum):
    """Bounded repo-native grammar roles that DMP may carry in v1."""

    TEMPORAL_CONTEXT = "temporal_context"
    MARKET_REGIME_CONTEXT = "market_regime_context"
    OPTIONS_FLOW_CONTEXT = "options_flow_context"
    POSTURE_RISK_PERMISSION = "posture_risk_permission"
    PLAYBOOK_ELIGIBILITY = "playbook_eligibility"
    EXPRESSION_EXECUTION = "expression_execution"
    REVIEW_EXPLANATION = "review_explanation"
    STACK_DEFINITION = "stack_definition"
    COEFFICIENT_SET = "coefficient_set"
    COEFFICIENT_AUDIT = "coefficient_audit"
    REPLAY_RUN_RESULT = "replay_run_result"
    COMPARISON_REPORT = "comparison_report"


class DmpBehaviourClass(StrEnum):
    """High-level behaviour families allowed in DMP v1."""

    STAGE_OUTPUT = "stage_output"
    MODULE_OUTPUT = "module_output"
    REPLAY_ARTEFACT = "replay_artefact"
    REVIEW_PACKET = "review_packet"


class DmpPacketIdentity(BaseModel):
    """Minimal deterministic identity for one DMP packet."""

    model_config = ConfigDict(extra="forbid")

    packet_id: str = Field(min_length=1)
    emitted_at: datetime


class DmpSchemaIdentifiers(BaseModel):
    """Live schema names attached to one DMP packet."""

    model_config = ConfigDict(extra="forbid")

    payload_model_name: str = Field(min_length=1)
    payload_module_path: str = Field(min_length=1)
    input_model_name: str | None = None
    output_model_name: str | None = None


class DmpTraceReferences(BaseModel):
    """Optional lineage pointers for review and replay attachment later."""

    model_config = ConfigDict(extra="forbid")

    parent_packet_id: str | None = None
    upstream_packet_ids: list[str] = Field(default_factory=list)
    review_trace_id: str | None = None
    replay_trace_id: str | None = None


class DmpPacket[PayloadT: BaseModel](BaseModel):
    """Typed DMP envelope that wraps one repo-native payload model."""

    model_config = ConfigDict(extra="forbid")

    protocol_version: Literal["dmp.v1"] = "dmp.v1"
    packet_identity: DmpPacketIdentity
    grammar_role: DmpGrammarRole
    behaviour_class: DmpBehaviourClass
    schema_identifiers: DmpSchemaIdentifiers
    stack_id: str | None = None
    coefficient_set_id: str | None = None
    dependencies: list[str] = Field(default_factory=list)
    trace_references: DmpTraceReferences = Field(default_factory=DmpTraceReferences)
    trader_summary: str = Field(min_length=1)
    payload: PayloadT


CognitionStagePayload = (
    TemporalContextOutput
    | MarketRegimeContextOutput
    | OptionsFlowContextOutput
    | PostureRiskOutput
    | PlaybookEligibilityOutput
    | ExecutionExpressionOutput
    | ReviewExplanationOutput
)

CalibrationPayload = (
    StackDefinition
    | CoefficientSet
    | CoefficientAuditPacket
    | ReplayRunResult
    | ComparisonReport
)

ImportedModulePayload = (
    EventFlagCaptureContractOutput
    | RealizedVolatilityEngineContractOutput
    | VolumeSpikeFilterContractOutput
    | PeerDivergenceContractOutput
    | GammaPressureContractOutput
    | IvVsRvAnalysisContractOutput
    | SkewInflectionContractOutput
    | SignalConflictDetectorContractOutput
    | ModelConfidenceScorerContractOutput
    | ConvictionTierAllocatorContractOutput
    | EntryGateContractOutput
    | LadderConstructorContractOutput
    | ArchetypeMatcherContractOutput
    | SpotDataCaptureContractOutput
    | PeerEquityCaptureContractOutput
    | OptionsDataCaptureContractOutput
    | OptionsMetadataCaptureContractOutput
    | MacroDataCaptureContractOutput
    | VwapAccumulatorContractOutput
    | VwapRocContractOutput
    | MacroSignalScoreContractOutput
    | ExecutionContextScoreContractOutput
    | VixSpreadDetectorContractOutput
    | VolCorridorContractOutput
    | OptionsBehaviourClusterContractOutput
    | AsiaPrecursorContextFilterContractOutput
    | MacroAdaptiveWeightingFilterContractOutput
    | EngineScoreContractOutput
    | RunSignalScanContractOutput
    | VvixLadderShaperContractOutput
    | FillBiasAdjusterContractOutput
    | ArchetypeTaggerContractOutput
    | CompressionRegimeDetectorContractOutput
    | ObvViFlowConfirmationContractOutput
    | TailHedgeInjectorContractOutput
    | VolatilitySentimentIndexContractOutput
    | BrokerAdapterContractOutput
    | EntryPlannerContractOutput
    | PositionAllocatorContractOutput
    | OrderSimulatorContractOutput
    | RunTradingBotContractOutput
    | DynamicPartialExitModelContractOutput
    | TakeProfitContractOutput
    | TrailingStopContractOutput
    | UnrealizedTrackerContractOutput
    | PositionBookContractOutput
    | TradeReentryMarkerContractOutput
    | LadderContinuityTrackerContractOutput
    | FillFeedbackRouterContractOutput
    | ExecutionLogWriterContractOutput
    | ExecutionTagsContractOutput
    | TradeLoggerContractOutput
    | ProfitLossLedgerContractOutput
    | ModuleTraceAttributionContractOutput
    | DailySummaryContractOutput
    | FeedbackSummaryWriterContractOutput
    | ModuleScoreAttributorContractOutput
    | VariantTraceLoggerContractOutput
    | VariantPerformanceTrackerContractOutput
    | ConfidenceDivergenceLoggerContractOutput
    | MacroAlignmentCheckerContractOutput
)

DeskModulePayload = CognitionStagePayload | CalibrationPayload | ImportedModulePayload

DeskModulePacket = DmpPacket[DeskModulePayload]


def build_dmp_packet(
    *,
    packet_id: str,
    emitted_at: datetime,
    grammar_role: DmpGrammarRole,
    behaviour_class: DmpBehaviourClass,
    payload: DeskModulePayload,
    trader_summary: str,
    stack_id: str | None = None,
    coefficient_set_id: str | None = None,
    dependencies: list[str] | None = None,
    trace_references: DmpTraceReferences | None = None,
    input_model_name: str | None = None,
    output_model_name: str | None = None,
) -> DeskModulePacket:
    """Build one typed DMP packet around an existing repo-native payload model."""

    payload_model = payload.__class__
    return DeskModulePacket(
        packet_identity=DmpPacketIdentity(packet_id=packet_id, emitted_at=emitted_at),
        grammar_role=grammar_role,
        behaviour_class=behaviour_class,
        schema_identifiers=DmpSchemaIdentifiers(
            payload_model_name=payload_model.__name__,
            payload_module_path=payload_model.__module__,
            input_model_name=input_model_name,
            output_model_name=output_model_name or payload_model.__name__,
        ),
        stack_id=stack_id,
        coefficient_set_id=coefficient_set_id,
        dependencies=list(dependencies or []),
        trace_references=trace_references or DmpTraceReferences(),
        trader_summary=trader_summary,
        payload=payload,
    )
