"""Gate 47 tests for the checked-in playbook registry v2 surfaces."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from nvda_desk.schemas.cognition import PlaybookAction, PlaybookDecision
from nvda_desk.schemas.playbook_registry import (
    ExecutionTemplateSpec,
    PlaybookDecisionProfile,
    PlaybookRegistryDocument,
)

REGISTRY_PATH = Path("config/playbook_registry.example.yaml")
BACKFILL_FIXTURE_PATH = Path(
    "fixtures/replay/playbook_registry_live_backfill_snapshot.json"
)


def test_playbook_registry_yaml_round_trips_through_typed_document() -> None:
    """Registry YAML should load and serialise deterministically through the v2 typed schemas."""

    document = PlaybookRegistryDocument.from_yaml_path(REGISTRY_PATH)
    restored = PlaybookRegistryDocument.from_yaml_text(document.to_yaml_text())

    assert restored.schema_version == "playbook_registry.v2"
    assert [
        variant.setup_variant_id for variant in restored.ordered_setup_variants()
    ] == [
        "opening_drive_continuation",
        "midday_compression_release",
        "late_session_pin_reversion",
        "negative_gamma_flush_probe",
        "front_expiry_pin_build",
        "front_next_curve_dislocation",
        "skew_relaxation_reversal",
    ]
    assert restored.family_index()["pin_behaviour"].title == "Pin Behaviour"
    assert (
        restored.execution_template_index()["pin_reversion_exec"].entry_style
        == "pin_fade_scaler"
    )


def test_playbook_registry_matches_live_backfill_fixture_exactly() -> None:
    """The checked-in registry snapshot should match the live playbooks, variants, and templates exactly."""

    document = PlaybookRegistryDocument.from_yaml_path(REGISTRY_PATH)
    templates = document.execution_template_index()
    playbooks = {playbook.playbook_id: playbook for playbook in document.playbooks}
    variants = {
        variant.setup_variant_id: variant for variant in document.setup_variants
    }
    fixture = json.loads(BACKFILL_FIXTURE_PATH.read_text())

    assert [
        playbook.playbook_id for playbook in document.ordered_playbooks()
    ] == fixture["ordered_playbooks"]
    assert [
        variant.setup_variant_id for variant in document.ordered_setup_variants()
    ] == fixture["ordered_setup_variants"]
    for playbook_id, expected in fixture["playbook_profiles"].items():
        spec = playbooks[playbook_id]
        assert spec.family_id == expected["family_id"]
        assert spec.setup_variant_id == expected["setup_variant_id"]
        assert spec.horizon.value == expected["horizon"]
        assert spec.eligible.action_bias.value == expected["eligible_action_bias"]
        assert spec.eligible.sizing_fraction == pytest.approx(
            expected["eligible_sizing_fraction"]
        )
        assert spec.watch_only.action_bias.value == expected["watch_action_bias"]
        assert spec.watch_only.hedge_overlay is expected["watch_hedge_overlay"]
        assert spec.execution_template_id == expected["template_id"]

    for variant_id, expected in fixture["setup_variants"].items():
        variant_spec = variants[variant_id]
        assert variant_spec.family_id == expected["family_id"]
        assert (
            variant_spec.execution_expression_id == expected["execution_expression_id"]
        )
        assert variant_spec.horizon.value == expected["horizon"]
        assert variant_spec.legacy_playbook_id == expected["legacy_playbook_id"]

    for template_id, expected in fixture["execution_templates"].items():
        template = templates[template_id]
        assert template.entry_style == expected["entry_style"]
        assert template.scaling_step_factors == expected["scaling_step_factors"]
        assert template.default_inventory_action == expected["default_inventory_action"]
        assert (
            template.default_fresh_capital_action
            == expected["default_fresh_capital_action"]
        )
        assert (
            template.thesis_invalidation_state == expected["thesis_invalidation_state"]
        )
        assert template.exit_reasons == expected["exit_reasons"]


def test_playbook_registry_can_express_probe_style_without_forcing_scaling_to_sum_to_one() -> (
    None
):
    """Registry v2 should still represent the flush probe plan rather than normalising it into a fake ladder."""

    document = PlaybookRegistryDocument.from_yaml_path(REGISTRY_PATH)
    template = document.execution_template_index()["negative_gamma_flush_exec"]

    assert template.scaling_step_factors == [0.10, 0.15]
    assert sum(template.scaling_step_factors) == pytest.approx(0.25)


def test_playbook_registry_rejects_duplicate_priorities_and_negative_scaling_steps() -> (
    None
):
    """Playbook registry schemas should reject ambiguous playbook order and malformed scaling steps."""

    with pytest.raises(ValidationError):
        PlaybookRegistryDocument.model_validate(
            {
                "schema_version": "playbook_registry.v2",
                "registry_version": "broken",
                "execution_templates": [
                    {
                        "template_id": "broken_exec",
                        "entry_style": "bad",
                        "watch_execution_style": "watchlist",
                        "scaling_step_factors": [-0.1],
                        "default_inventory_action": "hold",
                        "default_fresh_capital_action": "hold",
                        "thesis_invalidation_state": "bad",
                        "invalidation_reasons": [],
                        "exit_reasons": [],
                    }
                ],
                "families": [],
                "setup_variants": [],
                "playbooks": [],
            }
        )

    profile = PlaybookDecisionProfile(
        decision=PlaybookDecision.ELIGIBLE,
        action_bias=PlaybookAction.ADD,
        sizing_fraction=0.2,
    )
    with pytest.raises(ValidationError):
        PlaybookRegistryDocument.model_validate(
            {
                "schema_version": "playbook_registry.v2",
                "registry_version": "broken",
                "execution_templates": [
                    ExecutionTemplateSpec(
                        template_id="ok_exec",
                        entry_style="trend_ladder_3_step",
                        scaling_step_factors=[1.0],
                        default_inventory_action="add",
                        default_fresh_capital_action="add",
                        thesis_invalidation_state="trend_structure_broken",
                        invalidation_reasons=["leadership_lost"],
                        exit_reasons=["trim_into_extension"],
                    ).model_dump(mode="json")
                ],
                "families": [
                    {
                        "family_id": "trend_continuation",
                        "title": "Trend Continuation",
                        "thesis": "x",
                    }
                ],
                "setup_variants": [
                    {
                        "setup_variant_id": "v1",
                        "family_id": "trend_continuation",
                        "title": "One",
                        "priority": 1,
                        "execution_expression_id": "ok_exec",
                        "horizon": "intraday",
                    },
                    {
                        "setup_variant_id": "v2",
                        "family_id": "trend_continuation",
                        "title": "Two",
                        "priority": 1,
                        "execution_expression_id": "ok_exec",
                        "horizon": "intraday",
                    },
                ],
                "playbooks": [
                    {
                        "playbook_id": "p1",
                        "title": "One",
                        "rule_id": "one",
                        "execution_template_id": "ok_exec",
                        "execution_expression_id": "ok_exec",
                        "family_id": "trend_continuation",
                        "setup_variant_id": "v1",
                        "horizon": "intraday",
                        "priority": 1,
                        "eligible": profile.model_dump(mode="json"),
                        "watch_only": {
                            "decision": "watch_only",
                            "action_bias": "hold",
                            "sizing_fraction": 0.0,
                            "hedge_overlay": False,
                        },
                        "ineligible": {
                            "decision": "ineligible",
                            "action_bias": "reduce",
                            "sizing_fraction": 0.0,
                            "hedge_overlay": False,
                        },
                    }
                ],
            }
        )
