"""Gate 28 coverage checks for the ingress substrate tranche."""

from __future__ import annotations

from typing import cast

from nvda_desk.config import Settings
from nvda_desk.schemas.cognition import PlaybookEligibilityInput, PostureRiskInput
from nvda_desk.schemas.dmp import DmpGrammarRole
from nvda_desk.schemas.imported_modules.market_substrate import (
    MacroDataCaptureContractOutput,
    MarketSubstrateContext,
    VwapAccumulatorContractOutput,
    VwapRocContractOutput,
)
from nvda_desk.schemas.imported_modules.tranche_a import (
    ContractComputationMode,
    EventFlagCaptureContractOutput,
    RealizedVolatilityEngineContractOutput,
    TrancheAUpstreamContext,
)
from nvda_desk.services.imported_modules.market_substrate import MarketSubstrateContractService
from nvda_desk.services.imported_modules.tranche_a import TrancheAUpstreamContractService
from nvda_desk.services.market_regime_context import MarketRegimeContextService
from nvda_desk.services.options_flow_context import OptionsFlowContextService
from nvda_desk.services.playbook_eligibility import PlaybookEligibilityService
from nvda_desk.services.posture_risk import PostureRiskService
from nvda_desk.services.temporal_context import TemporalContextService
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture

EXPECTED_GATE28_ORDER = [
    "event_flag_capture",
    "spot_data_capture",
    "vwap_accumulator",
    "vwap_roc",
    "peer_equity_capture",
    "macro_data_capture",
    "realized_volatility_engine",
]


def test_gate28_coverage_is_closed_in_frozen_order_with_honest_ingress_fences() -> None:
    """Gate 28 should close exactly the seven planned ingress-substrate items."""

    fixture = supportive_runtime_fixture()
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
    _ = PlaybookEligibilityService().evaluate(
        PlaybookEligibilityInput(
            temporal=temporal,
            regime=regime,
            options_flow=options_flow,
            posture=posture,
        )
    )

    upstream_outputs = {
        emission.output.canonical_slug: emission.output
        for emission in TrancheAUpstreamContractService().evaluate(
            TrancheAUpstreamContext(
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

    outputs = {
        **upstream_outputs,
        **substrate_outputs,
    }
    ordered = [outputs[slug] for slug in EXPECTED_GATE28_ORDER]

    assert [output.canonical_slug for output in ordered] == EXPECTED_GATE28_ORDER
    assert [output.canonical_id for output in ordered] == [
        "archive-module-006",
        "archive-module-001",
        "archive-module-002",
        "archive-module-008",
        "archive-module-007",
        "archive-module-005",
        "archive-module-009",
    ]

    event_flag = cast(EventFlagCaptureContractOutput, outputs["event_flag_capture"])
    vwap_accumulator = cast(VwapAccumulatorContractOutput, outputs["vwap_accumulator"])
    vwap_roc = cast(VwapRocContractOutput, outputs["vwap_roc"])
    macro_data = cast(MacroDataCaptureContractOutput, outputs["macro_data_capture"])
    realized_vol = cast(RealizedVolatilityEngineContractOutput, outputs["realized_volatility_engine"])

    assert event_flag.grammar_role == DmpGrammarRole.TEMPORAL_CONTEXT.value
    assert event_flag.dependency_fences[0].status.value == "proxied_from_runtime"
    assert vwap_accumulator.computation_mode is ContractComputationMode.FENCED_CONTRACT_ONLY
    assert vwap_roc.computation_mode is ContractComputationMode.FENCED_CONTRACT_ONLY
    assert macro_data.computation_mode is ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY
    assert realized_vol.proxy_basis == ["front_realised_vol", "next_realised_vol"]
