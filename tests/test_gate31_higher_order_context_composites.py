"""Gate 31 coverage checks for the higher-order context composite tranche."""

from __future__ import annotations

from typing import Any, cast

from nvda_desk.schemas.dmp import DmpGrammarRole
from nvda_desk.schemas.imported_modules.context_scanners import (
    ExecutionContextScoreContractOutput,
    OptionsBehaviourClusterContractOutput,
)
from nvda_desk.schemas.imported_modules.posture_enrichers import (
    CompressionRegimeDetectorContractOutput,
    ObvViFlowConfirmationContractOutput,
)
from tests.contract_chain_fixtures import build_gate_support_bundle

EXPECTED_GATE31_ORDER = [
    "options_behaviour_cluster",
    "execution_context_score",
    "compression_regime_detector",
    "obv_vi_flow_confirmation",
]


def test_gate31_coverage_is_closed_in_frozen_order_with_honest_composite_boundaries() -> None:
    """Gate 31 should close exactly the four planned higher-order composite items."""

    supportive = build_gate_support_bundle()
    outputs = {
        **supportive.scanner_outputs,
        **supportive.enricher_outputs,
    }
    ordered: list[Any] = [outputs[slug] for slug in EXPECTED_GATE31_ORDER]

    assert [output.canonical_slug for output in ordered] == EXPECTED_GATE31_ORDER
    assert [output.canonical_id for output in ordered] == [
        "legacy-module-005",
        "archive-module-021",
        "legacy-module-004",
        "legacy-module-003",
    ]

    options_cluster = cast(
        OptionsBehaviourClusterContractOutput, outputs["options_behaviour_cluster"]
    )
    execution_context = cast(
        ExecutionContextScoreContractOutput, outputs["execution_context_score"]
    )
    compression = cast(
        CompressionRegimeDetectorContractOutput, outputs["compression_regime_detector"]
    )
    obv_confirmation = cast(
        ObvViFlowConfirmationContractOutput, outputs["obv_vi_flow_confirmation"]
    )

    assert options_cluster.grammar_role == DmpGrammarRole.OPTIONS_FLOW_CONTEXT.value
    assert execution_context.grammar_role == DmpGrammarRole.OPTIONS_FLOW_CONTEXT.value
    assert compression.grammar_role == DmpGrammarRole.PLAYBOOK_ELIGIBILITY.value
    assert obv_confirmation.grammar_role == DmpGrammarRole.PLAYBOOK_ELIGIBILITY.value
    assert compression.upstream_contract_slugs == [
        "vol_corridor",
        "execution_context_score",
        "options_behaviour_cluster",
    ]
    assert obv_confirmation.computation_mode.value == "fenced_contract_only"
    assert obv_confirmation.dependency_fences[0].dependency == "market_volume_series"
    assert obv_confirmation.dependency_fences[0].status.value == "fenced_missing_source"


def test_gate31_stressed_context_keeps_composites_descriptive_rather_than_promotional() -> None:
    """Gate 31 should degrade honestly under stress and avoid approval theatre."""

    stressed = build_gate_support_bundle(stressed=True)
    outputs = {
        **stressed.scanner_outputs,
        **stressed.enricher_outputs,
    }
    execution_context = cast(
        ExecutionContextScoreContractOutput, outputs["execution_context_score"]
    )
    compression = cast(
        CompressionRegimeDetectorContractOutput, outputs["compression_regime_detector"]
    )
    obv_confirmation = cast(
        ObvViFlowConfirmationContractOutput, outputs["obv_vi_flow_confirmation"]
    )

    assert execution_context.context_score < 0.6
    assert compression.compression_state in {
        "compression_blocked",
        "compression_watch",
        "compression_absent",
    }
    assert obv_confirmation.confirmation_state == "dependency_fenced"
    assert "market-volume tape" in obv_confirmation.contract_notes[0]
