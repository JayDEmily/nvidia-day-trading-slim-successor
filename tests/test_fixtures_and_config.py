from __future__ import annotations

from pathlib import Path

from nvda_desk.config_models import load_config_bundle
from nvda_desk.fixtures import load_legacy_option_fixture_rows, load_legacy_vwap_cases


def test_legacy_fixture_loaders_parse_admitted_files() -> None:
    option_rows = load_legacy_option_fixture_rows()
    vwap_cases = load_legacy_vwap_cases()
    assert len(option_rows) == 18
    assert option_rows[0].source_document == "Options Data CSV Output.pdf"
    assert len(vwap_cases) == 2
    assert vwap_cases[0].expected_guardrail_bias == "de_risk_or_block"


def test_config_bundle_loads_example_yaml_files() -> None:
    config_dir = Path(__file__).resolve().parents[1] / "config"
    bundle = load_config_bundle(config_dir)
    assert bundle.runtime_settings.environment.symbol == "NVDA"
    assert bundle.runtime_settings.safety.block_if_macro_risk_off is True
    assert bundle.evaluation_config.paths.output_dir == "./evaluator/outputs"
    assert "baseline" in bundle.strategy_variants.variants
    assert "runtime" in bundle.coefficients_registry.model_dump()
    assert bundle.coefficient_authority.schema_version == "coefficient_authority.v1"
