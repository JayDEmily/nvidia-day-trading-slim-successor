"""Gate 18 tests for shared market-data substrate contracts."""

from __future__ import annotations

from typing import cast

from nvda_desk.config import Settings
from nvda_desk.schemas.dmp import DmpBehaviourClass, DmpGrammarRole
from nvda_desk.schemas.imported_modules.market_substrate import (
    MarketSubstrateContext,
    SpotDataCaptureContractOutput,
    VwapAccumulatorContractOutput,
    VwapRocContractOutput,
)
from nvda_desk.schemas.imported_modules.tranche_a import ContractComputationMode
from nvda_desk.services.imported_modules.market_substrate import MarketSubstrateContractService
from nvda_desk.services.market_regime_context import MarketRegimeContextService
from nvda_desk.services.options_flow_context import OptionsFlowContextService
from nvda_desk.services.temporal_context import TemporalContextService
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture

EXPECTED_GATE18_ORDER = [
    "spot_data_capture",
    "peer_equity_capture",
    "options_data_capture",
    "options_metadata_capture",
    "macro_data_capture",
    "vwap_accumulator",
    "vwap_roc",
]


def _supportive_context() -> MarketSubstrateContext:
    fixture = supportive_runtime_fixture()
    temporal = TemporalContextService(Settings()).evaluate(fixture.temporal_input)
    regime = MarketRegimeContextService().evaluate(fixture.regime_input)
    options_flow = OptionsFlowContextService().evaluate(fixture.options_flow_input)
    return MarketSubstrateContext(
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


def test_market_substrate_contracts_emit_the_frozen_seven_modules_in_order() -> None:
    """Gate 18 should emit the seven shared substrate contracts in gate-map order."""

    emissions = MarketSubstrateContractService().evaluate(_supportive_context())
    assert [emission.output.canonical_slug for emission in emissions] == EXPECTED_GATE18_ORDER
    assert [emission.packet.grammar_role for emission in emissions] == [
        DmpGrammarRole.MARKET_REGIME_CONTEXT,
        DmpGrammarRole.MARKET_REGIME_CONTEXT,
        DmpGrammarRole.OPTIONS_FLOW_CONTEXT,
        DmpGrammarRole.OPTIONS_FLOW_CONTEXT,
        DmpGrammarRole.MARKET_REGIME_CONTEXT,
        DmpGrammarRole.MARKET_REGIME_CONTEXT,
        DmpGrammarRole.MARKET_REGIME_CONTEXT,
    ]
    assert all(emission.packet.behaviour_class is DmpBehaviourClass.MODULE_OUTPUT for emission in emissions)



def test_market_substrate_contracts_keep_proxy_and_fence_boundaries_honest() -> None:
    """Gate 18 should proxy only what the current runtime already knows and fence the rest."""

    emissions = {emission.output.canonical_slug: emission.output for emission in MarketSubstrateContractService().evaluate(_supportive_context())}
    spot = cast(SpotDataCaptureContractOutput, emissions["spot_data_capture"])
    vwap_accumulator = cast(VwapAccumulatorContractOutput, emissions["vwap_accumulator"])
    vwap_roc = cast(VwapRocContractOutput, emissions["vwap_roc"])

    assert spot.computation_mode is ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY
    assert spot.spot_price == 118.0
    assert vwap_accumulator.computation_mode is ContractComputationMode.FENCED_CONTRACT_ONLY
    assert vwap_roc.computation_mode is ContractComputationMode.FENCED_CONTRACT_ONLY
    assert {fence.dependency for fence in vwap_accumulator.dependency_fences if fence.status.value == "fenced_missing_source"} == {"spot_trade_ticks"}
    assert {fence.dependency for fence in vwap_roc.dependency_fences if fence.status.value == "fenced_missing_source"} == {"spot_vwap_10s"}



def test_market_substrate_packets_upgrade_to_v2_without_losing_order_or_schema_names() -> None:
    """Gate 18 should keep the substrate contracts packet-serialisable for later imports."""

    emissions = MarketSubstrateContractService().evaluate(_supportive_context())
    macro = next(emission for emission in emissions if emission.output.canonical_slug == "macro_data_capture")
    options_meta = next(emission for emission in emissions if emission.output.canonical_slug == "options_metadata_capture")

    assert macro.packet.protocol_version == "dmp.v1"
    assert macro.packet_v2.protocol_version == "dmp.v2"
    assert macro.packet_v2.producer.grammar_role == DmpGrammarRole.MARKET_REGIME_CONTEXT.value
    assert options_meta.packet.schema_identifiers.output_model_name == "OptionsMetadataCaptureContractOutput"
    assert options_meta.packet_v2.summary.trader_summary.startswith("options_metadata_capture")
