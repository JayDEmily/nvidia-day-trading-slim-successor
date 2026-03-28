"""Gate C tests for runtime contracts, docstrings, and fixture contracts."""

from __future__ import annotations

from nvda_desk.config import Settings
from nvda_desk.schemas.dmp_v2 import DmpV2ObjectBlock
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.services.cognition_runtime_registry import (
    DeskCognitionRuntimeRegistryService,
)
from nvda_desk.testing.cognition_fixtures import (
    CognitionRuntimeFixture,
    stressed_runtime_fixture,
    supportive_runtime_fixture,
)


def test_runtime_registry_exposes_all_binding_layers_in_order() -> None:
    """The runtime contract registry should expose the seven binding layers in order."""

    service = DeskCognitionRuntimeRegistryService()
    contracts = service.layer_contracts()
    assert [contract.grammar_role for contract in contracts] == [
        "temporal_context",
        "market_regime_context",
        "options_flow_context",
        "posture_risk_permission",
        "playbook_eligibility",
        "expression_execution",
        "review_explanation",
    ]
    assert all(contract.docstring_required for contract in contracts)
    options_contract = next(
        contract
        for contract in contracts
        if contract.grammar_role == "options_flow_context"
    )
    assert "nearby_strike_clusters" in options_contract.optional_input_fields
    assert "repeated_snapshot_state" in options_contract.required_output_fields
    posture_contract = next(
        contract
        for contract in contracts
        if contract.grammar_role == "posture_risk_permission"
    )
    assert "adverse_excursion_state" in posture_contract.required_output_fields
    assert "time_stop_state" in posture_contract.required_output_fields
    playbook_contract = next(
        contract
        for contract in contracts
        if contract.grammar_role == "playbook_eligibility"
    )
    assert "rejected_playbook_reasons" in playbook_contract.required_output_fields
    review_contract = next(
        contract
        for contract in contracts
        if contract.grammar_role == "review_explanation"
    )
    assert "stage_reason_packets" in review_contract.required_output_fields
    assert "rejected_playbooks" in review_contract.required_output_fields


def test_runtime_registry_builds_trace_packets_for_binding_layers() -> None:
    """Trace packet construction should stay deterministic and contract-backed."""

    service = DeskCognitionRuntimeRegistryService()
    packet = service.build_trace_packet(
        grammar_role="options_flow_context", summary="options state ready"
    )
    assert packet.grammar_role == "options_flow_context"
    assert packet.input_model_name == "OptionsFlowContextInput"
    assert packet.output_model_name == "OptionsFlowContextOutput"
    assert "spot_price" in packet.required_input_fields
    assert "repeated_snapshot_state" in packet.required_output_fields
    assert packet.summary == "options state ready"


def test_runtime_registry_enforces_docstring_template() -> None:
    """Gate C should enforce one mandatory runtime-service docstring template."""

    service = DeskCognitionRuntimeRegistryService()
    template = service.docstring_template()
    assert template.required_sections == [
        "Purpose:",
        "Inputs:",
        "Outputs:",
        "Determinism:",
    ]
    service.assert_docstring_contracts()
    service.assert_complete_contract_surface()


def test_cognition_runtime_fixture_contract_is_typed_and_deterministic() -> None:
    """Gate C runtime fixtures should use one typed contract instead of free-form mappings."""

    supportive = supportive_runtime_fixture()
    stressed = stressed_runtime_fixture()
    assert isinstance(supportive, CognitionRuntimeFixture)
    assert isinstance(stressed, CognitionRuntimeFixture)
    assert supportive.fixture_id == "supportive_runtime_fixture"
    assert stressed.inventory_state.time_stop_minutes_remaining == 10
    assert stressed.inventory_state.thesis_state_input == "fragile"


def test_runtime_emits_dmp_packets_in_registry_order_with_typed_payloads() -> None:
    """Gate 9 should packetise all seven binding stages without obscuring their typed outputs."""

    fixture = supportive_runtime_fixture()
    runtime = DeskCognitionRuntime(Settings())
    result = runtime.run(
        temporal_input=fixture.temporal_input,
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )
    contracts = DeskCognitionRuntimeRegistryService().layer_contracts()

    assert [packet.grammar_role.value for packet in result.stage_packets] == [
        contract.grammar_role for contract in contracts
    ]
    assert [
        packet.schema_identifiers.output_model_name for packet in result.stage_packets
    ] == [contract.output_model_name for contract in contracts]
    assert [packet.producer.grammar_role for packet in result.stage_packets] == [
        contract.grammar_role for contract in contracts
    ]
    assert result.packet_lineage == tuple(
        packet.packet_id for packet in result.stage_packets
    )
    assert result.stage_packets[0].payload.model_dump(
        mode="json"
    ) == result.temporal.model_dump(mode="json")
    assert result.stage_packets[-1].payload.model_dump(
        mode="json"
    ) == result.review.model_dump(mode="json")
    assert isinstance(result.stage_packets[0].blocks[0], DmpV2ObjectBlock)
    assert isinstance(result.stage_packets[-1].blocks[0], DmpV2ObjectBlock)
    assert result.stage_packets[0].blocks[0].data == result.temporal.model_dump(
        mode="json"
    )
    assert result.stage_packets[-1].blocks[0].data == result.review.model_dump(
        mode="json"
    )
