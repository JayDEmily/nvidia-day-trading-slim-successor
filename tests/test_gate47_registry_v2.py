from __future__ import annotations

from nvda_desk.services.playbook_registry import PlaybookRegistryService


def test_registry_v2_exposes_family_variant_and_expression_hierarchy() -> None:
    """Gate 47 should expose explicit family, setup-variant, and expression hierarchy."""

    registry = PlaybookRegistryService()

    assert (
        registry.family_for_playbook("front_expiry_pin_pressure").family_id
        == "pin_behaviour"
    )
    variant = registry.setup_variant_for_playbook("front_expiry_pin_pressure")
    assert variant.setup_variant_id == "front_expiry_pin_build"
    assert variant.execution_expression_id == "front_expiry_pin_pressure_exec"
    assert variant.legacy_playbook_id == "front_expiry_pin_pressure"
    template = registry.template_for_playbook("front_expiry_pin_pressure")
    assert template.template_id == variant.execution_expression_id
