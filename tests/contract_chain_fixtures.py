"""Helpers for building deterministic Gate-21 to Gate-23 contract contexts."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import cast

from nvda_desk.config import Settings
from nvda_desk.schemas.imported_modules.context_scanners import (
    AsiaPrecursorContextFilterContractOutput,
    ContextScannerContext,
    EngineScoreContractOutput,
    ExecutionContextScoreContractOutput,
    MacroAdaptiveWeightingFilterContractOutput,
    MacroSignalScoreContractOutput,
    OptionsBehaviourClusterContractOutput,
    VixSpreadDetectorContractOutput,
    VolCorridorContractOutput,
)
from nvda_desk.schemas.imported_modules.execution_lifecycle import (
    ExecutionLifecycleContext,
    ExecutionTagsContractOutput,
    PositionBookContractOutput,
    TradeLoggerContractOutput,
    UnrealizedTrackerContractOutput,
)
from nvda_desk.schemas.imported_modules.execution_planning import (
    BrokerAdapterContractOutput,
    EntryPlannerContractOutput,
    ExecutionPlanningContext,
    OrderSimulatorContractOutput,
    PositionAllocatorContractOutput,
    RunTradingBotContractOutput,
)
from nvda_desk.schemas.imported_modules.market_substrate import (
    MacroDataCaptureContractOutput,
    MarketSubstrateContext,
    OptionsDataCaptureContractOutput,
    OptionsMetadataCaptureContractOutput,
    PeerEquityCaptureContractOutput,
    SpotDataCaptureContractOutput,
    VwapAccumulatorContractOutput,
    VwapRocContractOutput,
)
from nvda_desk.schemas.imported_modules.posture_enrichers import (
    FillBiasAdjusterContractOutput,
    PostureEnricherContext,
)
from nvda_desk.schemas.imported_modules.review_attribution import (
    ReviewAttributionContext,
)
from nvda_desk.schemas.imported_modules.tranche_a import (
    EntryGateContractOutput,
    LadderConstructorContractOutput,
    TrancheASelectorContext,
)
from nvda_desk.services.cognition_runtime import (
    DeskCognitionRuntime,
    DeskCognitionRuntimeResult,
)
from nvda_desk.services.imported_modules.context_scanners import (
    ContextScannerContractService,
)
from nvda_desk.services.imported_modules.execution_lifecycle import (
    ExecutionLifecycleContractService,
)
from nvda_desk.services.imported_modules.execution_planning import (
    ExecutionPlanningContractService,
)
from nvda_desk.services.imported_modules.market_substrate import (
    MarketSubstrateContractService,
)
from nvda_desk.services.imported_modules.posture_enrichers import (
    PostureEnricherContractService,
)
from nvda_desk.services.imported_modules.review_attribution import (
    ReviewAttributionContractService,
)
from nvda_desk.services.imported_modules.tranche_a import (
    TrancheASelectorContractService,
)
from nvda_desk.testing.cognition_fixtures import (
    CognitionRuntimeFixture,
    stressed_runtime_fixture,
    supportive_runtime_fixture,
)


@dataclass(frozen=True)
class GateExecutionContractBundle:
    """Deterministic execution-chain contract outputs for Gates 35 through 39."""

    planning_outputs: Mapping[str, object]
    lifecycle_outputs: Mapping[str, object]
    review_outputs: Mapping[str, object]
    support_outputs: Mapping[str, object]


@dataclass(frozen=True)
class GateSupportBundle:
    fixture: CognitionRuntimeFixture
    runtime: DeskCognitionRuntimeResult
    substrate_outputs: dict[str, object]
    scanner_outputs: dict[str, object]
    enricher_outputs: dict[str, object]
    selector_outputs: dict[str, object]


def _fixture(*, stressed: bool) -> CognitionRuntimeFixture:
    return stressed_runtime_fixture() if stressed else supportive_runtime_fixture()


def _build_support_bundle(*, stressed: bool) -> GateSupportBundle:
    fixture = _fixture(stressed=stressed)
    runtime = DeskCognitionRuntime(Settings()).run(
        temporal_input=fixture.temporal_input,
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
        stack_id="core_full_stack",
        coefficient_set_id="full_stack_base",
    )
    substrate_outputs: dict[str, object] = {
        emission.output.canonical_slug: emission.output
        for emission in MarketSubstrateContractService().evaluate(
            MarketSubstrateContext(
                emitted_at=fixture.temporal_input.ts,
                temporal_input=fixture.temporal_input,
                regime_input=fixture.regime_input,
                options_flow_input=fixture.options_flow_input,
                temporal=runtime.temporal,
                regime=runtime.regime,
                options_flow=runtime.options_flow,
                stack_id="core_full_stack",
                coefficient_set_id="full_stack_base",
            )
        )
    }
    scanner_outputs: dict[str, object] = {
        emission.output.canonical_slug: emission.output
        for emission in ContextScannerContractService().evaluate(
            ContextScannerContext(
                emitted_at=fixture.temporal_input.ts,
                temporal_input=fixture.temporal_input,
                regime_input=fixture.regime_input,
                options_flow_input=fixture.options_flow_input,
                temporal=runtime.temporal,
                regime=runtime.regime,
                options_flow=runtime.options_flow,
                posture=runtime.posture,
                eligibility=runtime.eligibility,
                spot_data_capture=cast(
                    SpotDataCaptureContractOutput,
                    substrate_outputs["spot_data_capture"],
                ),
                peer_equity_capture=cast(
                    PeerEquityCaptureContractOutput,
                    substrate_outputs["peer_equity_capture"],
                ),
                options_data_capture=cast(
                    OptionsDataCaptureContractOutput,
                    substrate_outputs["options_data_capture"],
                ),
                options_metadata_capture=cast(
                    OptionsMetadataCaptureContractOutput,
                    substrate_outputs["options_metadata_capture"],
                ),
                macro_data_capture=cast(
                    MacroDataCaptureContractOutput,
                    substrate_outputs["macro_data_capture"],
                ),
                vwap_accumulator=cast(
                    VwapAccumulatorContractOutput, substrate_outputs["vwap_accumulator"]
                ),
                vwap_roc=cast(VwapRocContractOutput, substrate_outputs["vwap_roc"]),
                stack_id="core_full_stack",
                coefficient_set_id="full_stack_base",
            )
        )
    }
    enricher_outputs: dict[str, object] = {
        emission.output.canonical_slug: emission.output
        for emission in PostureEnricherContractService().evaluate(
            PostureEnricherContext(
                emitted_at=fixture.temporal_input.ts,
                temporal=runtime.temporal,
                regime=runtime.regime,
                options_flow=runtime.options_flow,
                posture=runtime.posture,
                eligibility=runtime.eligibility,
                macro_signal_score=cast(
                    MacroSignalScoreContractOutput,
                    scanner_outputs["macro_signal_score"],
                ),
                execution_context_score=cast(
                    ExecutionContextScoreContractOutput,
                    scanner_outputs["execution_context_score"],
                ),
                vix_spread_detector=cast(
                    VixSpreadDetectorContractOutput,
                    scanner_outputs["vix_spread_detector"],
                ),
                vol_corridor=cast(VolCorridorContractOutput, scanner_outputs["vol_corridor"]),
                options_behaviour_cluster=cast(
                    OptionsBehaviourClusterContractOutput,
                    scanner_outputs["options_behaviour_cluster"],
                ),
                asia_precursor_context_filter=cast(
                    AsiaPrecursorContextFilterContractOutput,
                    scanner_outputs["asia_precursor_context_filter"],
                ),
                macro_adaptive_weighting_filter=cast(
                    MacroAdaptiveWeightingFilterContractOutput,
                    scanner_outputs["macro_adaptive_weighting_filter"],
                ),
                engine_score=cast(EngineScoreContractOutput, scanner_outputs["engine_score"]),
                stack_id="core_full_stack",
                coefficient_set_id="full_stack_base",
            )
        )
    }
    selector_outputs: dict[str, object] = {
        emission.output.canonical_slug: emission.output
        for emission in TrancheASelectorContractService().evaluate(
            TrancheASelectorContext(
                emitted_at=fixture.temporal_input.ts,
                temporal=runtime.temporal,
                regime=runtime.regime,
                options_flow=runtime.options_flow,
                posture=runtime.posture,
                eligibility=runtime.eligibility,
                execution=runtime.execution,
                stack_id="core_full_stack",
                coefficient_set_id="full_stack_base",
            )
        )
    }
    return GateSupportBundle(
        fixture=fixture,
        runtime=runtime,
        substrate_outputs=substrate_outputs,
        scanner_outputs=scanner_outputs,
        enricher_outputs=enricher_outputs,
        selector_outputs=selector_outputs,
    )


def build_gate_support_bundle(*, stressed: bool = False) -> GateSupportBundle:
    """Public helper for deterministic multi-gate support bundles."""

    return _build_support_bundle(stressed=stressed)


def build_gate21_context(*, stressed: bool = False) -> ExecutionPlanningContext:
    """Build a deterministic Gate-21 context from the repo fixtures."""

    bundle = _build_support_bundle(stressed=stressed)
    return ExecutionPlanningContext(
        emitted_at=bundle.fixture.temporal_input.ts,
        temporal=bundle.runtime.temporal,
        regime=bundle.runtime.regime,
        options_flow=bundle.runtime.options_flow,
        posture=bundle.runtime.posture,
        eligibility=bundle.runtime.eligibility,
        execution=bundle.runtime.execution,
        engine_score=cast(EngineScoreContractOutput, bundle.scanner_outputs["engine_score"]),
        entry_gate=cast(EntryGateContractOutput, bundle.selector_outputs["entry_gate"]),
        ladder_constructor=cast(
            LadderConstructorContractOutput,
            bundle.selector_outputs["ladder_constructor"],
        ),
        fill_bias_adjuster=cast(
            FillBiasAdjusterContractOutput,
            bundle.enricher_outputs["fill_bias_adjuster"],
        ),
        spot_data_capture=cast(
            SpotDataCaptureContractOutput, bundle.substrate_outputs["spot_data_capture"]
        ),
        vwap_accumulator=cast(
            VwapAccumulatorContractOutput, bundle.substrate_outputs["vwap_accumulator"]
        ),
        stack_id="core_full_stack",
        coefficient_set_id="full_stack_base",
    )


def build_gate22_context(*, stressed: bool = False) -> ExecutionLifecycleContext:
    """Build a deterministic Gate-22 context from the repo fixtures."""

    bundle = _build_support_bundle(stressed=stressed)
    gate21_context = build_gate21_context(stressed=stressed)
    gate21_outputs = {
        emission.output.canonical_slug: emission.output
        for emission in ExecutionPlanningContractService().evaluate(gate21_context)
    }
    return ExecutionLifecycleContext(
        emitted_at=gate21_context.emitted_at,
        temporal=gate21_context.temporal,
        regime=gate21_context.regime,
        options_flow=gate21_context.options_flow,
        posture=gate21_context.posture,
        eligibility=gate21_context.eligibility,
        execution=gate21_context.execution,
        inventory=bundle.fixture.inventory_state,
        entry_gate=gate21_context.entry_gate,
        spot_data_capture=gate21_context.spot_data_capture,
        broker_adapter=cast(BrokerAdapterContractOutput, gate21_outputs["broker_adapter"]),
        entry_planner=cast(EntryPlannerContractOutput, gate21_outputs["entry_planner"]),
        position_allocator=cast(
            PositionAllocatorContractOutput, gate21_outputs["position_allocator"]
        ),
        order_simulator=cast(OrderSimulatorContractOutput, gate21_outputs["order_simulator"]),
        run_trading_bot=cast(RunTradingBotContractOutput, gate21_outputs["run_trading_bot"]),
        stack_id="core_full_stack",
        coefficient_set_id="full_stack_base",
    )


def build_gate23_context(*, stressed: bool = False) -> ReviewAttributionContext:
    """Build a deterministic Gate-23 context from the repo fixtures."""

    bundle = _build_support_bundle(stressed=stressed)
    gate22_outputs = {
        emission.output.canonical_slug: emission.output
        for emission in ExecutionLifecycleContractService().evaluate(
            build_gate22_context(stressed=stressed)
        )
    }
    return ReviewAttributionContext(
        emitted_at=bundle.fixture.temporal_input.ts,
        temporal=bundle.runtime.temporal,
        regime=bundle.runtime.regime,
        options_flow=bundle.runtime.options_flow,
        posture=bundle.runtime.posture,
        eligibility=bundle.runtime.eligibility,
        execution=bundle.runtime.execution,
        review=bundle.runtime.review,
        engine_score=cast(EngineScoreContractOutput, bundle.scanner_outputs["engine_score"]),
        macro_signal_score=cast(
            MacroSignalScoreContractOutput, bundle.scanner_outputs["macro_signal_score"]
        ),
        unrealized_tracker=cast(
            UnrealizedTrackerContractOutput, gate22_outputs["unrealized_tracker"]
        ),
        position_book=cast(PositionBookContractOutput, gate22_outputs["position_book"]),
        execution_tags=cast(ExecutionTagsContractOutput, gate22_outputs["execution_tags"]),
        trade_logger=cast(TradeLoggerContractOutput, gate22_outputs["trade_logger"]),
        stack_id="core_full_stack",
        coefficient_set_id="full_stack_base",
    )


def build_gate_execution_contract_bundle(*, stressed: bool = False) -> GateExecutionContractBundle:
    """Build the deterministic execution-chain contract outputs used by Gates 35 through 39."""

    support_bundle = _build_support_bundle(stressed=stressed)
    planning_outputs = {
        emission.output.canonical_slug: emission.output
        for emission in ExecutionPlanningContractService().evaluate(
            build_gate21_context(stressed=stressed)
        )
    }
    lifecycle_outputs = {
        emission.output.canonical_slug: emission.output
        for emission in ExecutionLifecycleContractService().evaluate(
            build_gate22_context(stressed=stressed)
        )
    }
    review_outputs = {
        emission.output.canonical_slug: emission.output
        for emission in ReviewAttributionContractService().evaluate(
            build_gate23_context(stressed=stressed)
        )
    }
    support_outputs = {
        **support_bundle.enricher_outputs,
        **support_bundle.selector_outputs,
    }
    return GateExecutionContractBundle(
        planning_outputs=planning_outputs,
        lifecycle_outputs=lifecycle_outputs,
        review_outputs=review_outputs,
        support_outputs=support_outputs,
    )
