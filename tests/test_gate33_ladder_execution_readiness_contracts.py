"""Gate 33 coverage checks for the ladder and execution-readiness tranche."""

from __future__ import annotations

from typing import Any, cast

from nvda_desk.schemas.dmp import DmpGrammarRole
from nvda_desk.schemas.imported_modules.ladder_readiness_overlays import (
    LadderReadinessContext,
    VvixLadderShaperContractOutput,
)
from nvda_desk.schemas.imported_modules.market_substrate import (
    MacroDataCaptureContractOutput,
)
from nvda_desk.schemas.imported_modules.posture_enrichers import (
    FillBiasAdjusterContractOutput,
    VolatilitySentimentIndexContractOutput,
)
from nvda_desk.schemas.imported_modules.tranche_a import LadderConstructorContractOutput
from nvda_desk.services.imported_modules.ladder_readiness_overlays import (
    LadderReadinessContractService,
)
from tests.contract_chain_fixtures import build_gate_support_bundle

EXPECTED_GATE33_ORDER = [
    "ladder_constructor",
    "fill_bias_adjuster",
    "vvix_ladder_shaper",
    "volatility_sentiment_index",
]


def _vvix_outputs(*, stressed: bool = False) -> dict[str, object]:
    bundle = build_gate_support_bundle(stressed=stressed)
    emissions = LadderReadinessContractService().evaluate(
        LadderReadinessContext(
            emitted_at=bundle.fixture.temporal_input.ts,
            temporal=bundle.runtime.temporal,
            options_flow=bundle.runtime.options_flow,
            ladder_constructor=cast(
                LadderConstructorContractOutput,
                bundle.selector_outputs["ladder_constructor"],
            ),
            macro_data_capture=cast(
                MacroDataCaptureContractOutput,
                bundle.substrate_outputs["macro_data_capture"],
            ),
            stack_id="core_full_stack",
            coefficient_set_id="full_stack_base",
        )
    )
    return {emission.output.canonical_slug: emission.output for emission in emissions}


def test_gate33_coverage_is_closed_in_frozen_order_with_honest_readiness_overlays() -> None:
    """Gate 33 should close exactly the four ladder/readiness overlays."""

    supportive = build_gate_support_bundle()
    outputs = {
        **supportive.selector_outputs,
        **supportive.enricher_outputs,
        **_vvix_outputs(),
    }
    ordered: list[Any] = [outputs[slug] for slug in EXPECTED_GATE33_ORDER]

    assert [output.canonical_slug for output in ordered] == EXPECTED_GATE33_ORDER
    assert [output.canonical_id for output in ordered] == [
        "archive-module-024",
        "archive-module-026",
        "archive-module-044",
        "legacy-module-002",
    ]

    ladder_constructor = cast(LadderConstructorContractOutput, outputs["ladder_constructor"])
    fill_bias = cast(FillBiasAdjusterContractOutput, outputs["fill_bias_adjuster"])
    vvix_shaper = cast(VvixLadderShaperContractOutput, outputs["vvix_ladder_shaper"])
    volatility_sentiment = cast(
        VolatilitySentimentIndexContractOutput, outputs["volatility_sentiment_index"]
    )

    assert ladder_constructor.grammar_role == DmpGrammarRole.PLAYBOOK_ELIGIBILITY.value
    assert fill_bias.grammar_role == DmpGrammarRole.PLAYBOOK_ELIGIBILITY.value
    assert vvix_shaper.grammar_role == DmpGrammarRole.MARKET_REGIME_CONTEXT.value
    assert volatility_sentiment.grammar_role == DmpGrammarRole.POSTURE_RISK_PERMISSION.value
    assert vvix_shaper.upstream_contract_slugs == [
        "ladder_constructor",
        "macro_data_capture",
    ]
    assert vvix_shaper.dependency_fences[0].dependency == "ladder_constructor"
    assert vvix_shaper.dependency_fences[0].status.value == "satisfied"
    assert vvix_shaper.dependency_fences[1].dependency == "macro_metrics"
    assert vvix_shaper.dependency_fences[1].status.value == "proxied_from_runtime"
    assert len(vvix_shaper.reshaped_ladder) == len(ladder_constructor.ladder_strikes)
    assert vvix_shaper.ladder_width_multiplier > 0.0


def test_gate33_stress_widens_vvix_overlay_without_claiming_live_broker_readiness() -> None:
    """Gate 33 should widen honestly under stress and keep readiness overlays advisory only."""

    outputs = {
        **build_gate_support_bundle(stressed=True).selector_outputs,
        **build_gate_support_bundle(stressed=True).enricher_outputs,
        **_vvix_outputs(stressed=True),
    }
    vvix_shaper = cast(VvixLadderShaperContractOutput, outputs["vvix_ladder_shaper"])
    volatility_sentiment = cast(
        VolatilitySentimentIndexContractOutput, outputs["volatility_sentiment_index"]
    )

    assert vvix_shaper.vvix_regime in {"vvix_elevated", "vvix_spike"}
    assert vvix_shaper.ladder_width_multiplier >= 1.15
    assert volatility_sentiment.sentiment_state in {
        "hostile_volatility_sentiment",
        "mixed_volatility_sentiment",
    }
    assert "No broker route" in vvix_shaper.contract_notes[1]
