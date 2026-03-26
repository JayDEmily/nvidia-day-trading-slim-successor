from __future__ import annotations

from pathlib import Path

from tests.test_gate52_native_playbook_hierarchy import _supportive_runtime_result

REPO_ROOT = Path(__file__).resolve().parents[1]
DMP_V1_SPEC = REPO_ROOT / "docs/planning/2026-03-24_DMP_V1_SPEC.md"
DMP_V2_SPEC = REPO_ROOT / "docs/planning/2026-03-24_DMP_V2_NORMATIVE_SPEC.md"
DMP_DECISION = REPO_ROOT / "docs/planning/2026-03-26_DMP_BINDING_SURFACE_DECISION.md"


def test_runtime_keeps_v1_as_primary_and_v2_as_derived_surface() -> None:
    result = _supportive_runtime_result()

    assert result.stage_packets
    assert result.stage_packets_v2
    assert all(packet.protocol_version == "dmp.v1" for packet in result.stage_packets)
    assert all(packet.protocol_version == "dmp.v2" for packet in result.stage_packets_v2)
    assert [packet.packet_identity.packet_id for packet in result.stage_packets] == [packet.packet_id for packet in result.stage_packets_v2]


def test_services_do_not_directly_build_v2_packets_as_primary_runtime_surface() -> None:
    service_root = REPO_ROOT / "src/nvda_desk/services"
    offenders: list[str] = []
    for path in service_root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        if "build_dmp_v2_packet(" in text:
            offenders.append(str(path.relative_to(REPO_ROOT)))
    assert offenders == []


def test_gate54_docs_state_the_binding_decision_unambiguously() -> None:
    v1_text = DMP_V1_SPEC.read_text(encoding="utf-8")
    v2_text = DMP_V2_SPEC.read_text(encoding="utf-8")
    decision_text = DMP_DECISION.read_text(encoding="utf-8")

    assert "canonical live runtime packet surface" in v1_text
    assert "not the canonical live producer path" in v2_text
    assert "DMP v1 remains the canonical live runtime packet producer surface" in decision_text
    assert "DMP v2 remains an implemented secondary migration/inspection surface" in decision_text
