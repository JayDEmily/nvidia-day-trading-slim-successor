"""Gate 20 tests for posture and eligibility enricher contracts."""

from __future__ import annotations

from typing import cast

from nvda_desk.config import Settings
from nvda_desk.schemas.cognition import PlaybookEligibilityInput, PostureRiskInput
from nvda_desk.schemas.dmp import DmpBehaviourClass, DmpGrammarRole
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
    ObvViFlowConfirmationContractOutput,
    PostureEnricherContext,
    TailHedgeInjectorContractOutput,
    VolatilitySentimentIndexContractOutput,
)
from nvda_desk.services.imported_modules.context_scanners import ContextScannerContractService
from nvda_desk.services.imported_modules.market_substrate import MarketSubstrateContractService
from nvda_desk.services.imported_modules.posture_enrichers import PostureEnricherContractService
from nvda_desk.services.market_regime_context import MarketRegimeContextService
from nvda_desk.services.options_flow_context import OptionsFlowContextService
from nvda_desk.services.playbook_eligibility import PlaybookEligibilityService
from nvda_desk.services.posture_risk import PostureRiskService
from nvda_desk.services.temporal_context import TemporalContextService
from nvda_desk.testing.cognition_fixtures import (
    stressed_runtime_fixture,
    supportive_runtime_fixture,
)

EXPECTED_GATE20_ORDER = [
    "fill_bias_adjuster",
    "archetype_tagger",
    "compression_regime_detector",
    "obv_vi_flow_confirmation",
    "tail_hedge_injector",
    "volatility_sentiment_index",
]


def _context_from_fixture(*, stressed: bool = False) -> PostureEnricherContext:
    fixture = stressed_runtime_fixture() if stressed else supportive_runtime_fixture()
    temporal = TemporalContextService(Settings()).evaluate(fixture.temporal_input)
    regime = MarketRegimeContextService().evaluate(fixture.regime_input)
    options_flow = OptionsFlowContextService().evaluate(fixture.options_flow_input)
    posture = PostureRiskService().evaluate(
        PostureRiskInput(
            temporal=temporal,
            regime=regime,
            options_flow=options_flow,
            inventory=fixture.inventory_state,
            risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
        )
    )
    eligibility = PlaybookEligibilityService().evaluate(
        PlaybookEligibilityInput(
            temporal=temporal,
            regime=regime,
            options_flow=options_flow,
            posture=posture,
        )
    )
    substrate_outputs = {
        emission.output.canonical_slug: emission.output
        for emission in MarketSubstrateContractService().evaluate(
            MarketSubstrateContext(
                emitted_at=fixture.temporal_input.ts,
                temporal_input=fixture.temporal_input,
                regime_input=fixture.regime_input,
                options_flow_input=fixture.options_flow_input,
                temporal=temporal,
                regime=regime,
                options_flow=options_flow,
                stack_id="core_full_stack",
                coefficient_set_id="full_stack_base",
            )
        )
    }
    scanner_outputs = {
        emission.output.canonical_slug: emission.output
        for emission in ContextScannerContractService().evaluate(
            ContextScannerContext(
                emitted_at=fixture.temporal_input.ts,
                temporal_input=fixture.temporal_input,
                regime_input=fixture.regime_input,
                options_flow_input=fixture.options_flow_input,
                temporal=temporal,
                regime=regime,
                options_flow=options_flow,
                posture=posture,
                eligibility=eligibility,
                spot_data_capture=cast(SpotDataCaptureContractOutput, substrate_outputs["spot_data_capture"]),
                peer_equity_capture=cast(PeerEquityCaptureContractOutput, substrate_outputs["peer_equity_capture"]),
                options_data_capture=cast(OptionsDataCaptureContractOutput, substrate_outputs["options_data_capture"]),
                options_metadata_capture=cast(OptionsMetadataCaptureContractOutput, substrate_outputs["options_metadata_capture"]),
                macro_data_capture=cast(MacroDataCaptureContractOutput, substrate_outputs["macro_data_capture"]),
                vwap_accumulator=cast(VwapAccumulatorContractOutput, substrate_outputs["vwap_accumulator"]),
                vwap_roc=cast(VwapRocContractOutput, substrate_outputs["vwap_roc"]),
                stack_id="core_full_stack",
                coefficient_set_id="full_stack_base",
            )
        )
    }
    return PostureEnricherContext(
        emitted_at=fixture.temporal_input.ts,
        temporal=temporal,
        regime=regime,
        options_flow=options_flow,
        posture=posture,
        eligibility=eligibility,
        macro_signal_score=cast(MacroSignalScoreContractOutput, scanner_outputs["macro_signal_score"]),
        execution_context_score=cast(ExecutionContextScoreContractOutput, scanner_outputs["execution_context_score"]),
        vix_spread_detector=cast(VixSpreadDetectorContractOutput, scanner_outputs["vix_spread_detector"]),
        vol_corridor=cast(VolCorridorContractOutput, scanner_outputs["vol_corridor"]),
        options_behaviour_cluster=cast(OptionsBehaviourClusterContractOutput, scanner_outputs["options_behaviour_cluster"]),
        asia_precursor_context_filter=cast(AsiaPrecursorContextFilterContractOutput, scanner_outputs["asia_precursor_context_filter"]),
        macro_adaptive_weighting_filter=cast(MacroAdaptiveWeightingFilterContractOutput, scanner_outputs["macro_adaptive_weighting_filter"]),
        engine_score=cast(EngineScoreContractOutput, scanner_outputs["engine_score"]),
        stack_id="core_full_stack",
        coefficient_set_id="full_stack_base",
    )


def test_posture_enricher_contracts_emit_the_frozen_six_modules_in_order() -> None:
    """Gate 20 should emit the six enrichers in gate-map order."""

    emissions = PostureEnricherContractService().evaluate(_context_from_fixture())
    assert [emission.output.canonical_slug for emission in emissions] == EXPECTED_GATE20_ORDER
    assert [emission.packet.grammar_role for emission in emissions] == [
        DmpGrammarRole.PLAYBOOK_ELIGIBILITY,
        DmpGrammarRole.PLAYBOOK_ELIGIBILITY,
        DmpGrammarRole.PLAYBOOK_ELIGIBILITY,
        DmpGrammarRole.PLAYBOOK_ELIGIBILITY,
        DmpGrammarRole.POSTURE_RISK_PERMISSION,
        DmpGrammarRole.POSTURE_RISK_PERMISSION,
    ]
    assert all(emission.packet.behaviour_class is DmpBehaviourClass.MODULE_OUTPUT for emission in emissions)


def test_posture_enrichers_keep_fill_bias_and_tail_hedge_advisory_with_explicit_provenance() -> None:
    """Gate 20 should keep the two most execution-adjacent enrichers advisory-only."""

    outputs = {
        emission.output.canonical_slug: emission.output
        for emission in PostureEnricherContractService().evaluate(_context_from_fixture())
    }
    fill_bias = cast(FillBiasAdjusterContractOutput, outputs["fill_bias_adjuster"])
    tail_hedge = cast(TailHedgeInjectorContractOutput, outputs["tail_hedge_injector"])

    assert fill_bias.advisory_only is True
    assert fill_bias.upstream_contract_slugs == [
        "execution_context_score",
        "macro_adaptive_weighting_filter",
        "engine_score",
    ]
    assert fill_bias.fill_bias == "passive_improve"
    assert fill_bias.adjustment_score > 0.7
    assert {fence.dependency for fence in fill_bias.dependency_fences if fence.status.value == "satisfied"} == {
        "context_scanner:execution_context_score",
        "context_scanner:macro_adaptive_weighting_filter",
        "context_scanner:engine_score",
    }

    assert tail_hedge.advisory_only is True
    assert tail_hedge.upstream_contract_slugs == ["macro_signal_score", "vix_spread_detector", "engine_score"]
    assert tail_hedge.hedge_overlay_tag == "no_tail_hedge_needed"
    assert tail_hedge.hedge_ratio == 0.0
    assert {fence.dependency for fence in tail_hedge.dependency_fences if fence.status.value == "satisfied"} == {
        "context_scanner:macro_signal_score",
        "context_scanner:vix_spread_detector",
        "context_scanner:engine_score",
    }


def test_posture_enrichers_reflect_stressed_conditions_and_keep_obv_flow_fenced() -> None:
    """Gate 20 should degrade honestly under stress and fence missing OBV tape dependencies."""

    emissions = PostureEnricherContractService().evaluate(_context_from_fixture(stressed=True))
    outputs = {emission.output.canonical_slug: emission.output for emission in emissions}
    tail_hedge = cast(TailHedgeInjectorContractOutput, outputs["tail_hedge_injector"])
    volatility_sentiment = cast(VolatilitySentimentIndexContractOutput, outputs["volatility_sentiment_index"])
    obv_confirmation = cast(ObvViFlowConfirmationContractOutput, outputs["obv_vi_flow_confirmation"])

    assert tail_hedge.hedge_overlay_tag == "deploy_tail_hedge"
    assert tail_hedge.hedge_ratio == 0.25
    assert volatility_sentiment.sentiment_state == "hostile_volatility_sentiment"
    assert volatility_sentiment.sentiment_index < 0.35
    assert obv_confirmation.confirmation_state == "dependency_fenced"
    assert {fence.dependency for fence in obv_confirmation.dependency_fences if fence.status.value == "fenced_missing_source"} == {
        "market_volume_series",
        "intraday_obv_curve",
    }
    assert emissions[-1].packet.summary.trader_summary.startswith("volatility_sentiment_index")
