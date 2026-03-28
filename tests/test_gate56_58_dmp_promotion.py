from __future__ import annotations

from pathlib import Path

from tests.test_gate52_native_playbook_hierarchy import _supportive_runtime_result

REPO_ROOT = Path(__file__).resolve().parents[1]
DMP_V2_SPEC = REPO_ROOT / "docs/planning/2026-03-24_DMP_V2_NORMATIVE_SPEC.md"
DMP_V1_SPEC = REPO_ROOT / "docs/planning/2026-03-24_DMP_V1_SPEC.md"
PROMOTION_GATES = REPO_ROOT / "docs/planning/2026-03-26_DMP_V2_PROMOTION_GATES_v1.md"


def test_runtime_uses_v2_as_only_live_stage_packet_surface() -> None:
    result = _supportive_runtime_result()

    assert result.stage_packets
    assert all(packet.protocol_version == "dmp.v2" for packet in result.stage_packets)
    assert result.packet_lineage == tuple(
        packet.packet_id for packet in result.stage_packets
    )
    assert result.contract_packets
    assert all(
        packet.protocol_version == "dmp.v2" for packet in result.contract_packets
    )


def test_docs_mark_v2_canonical_and_v1_historical() -> None:
    v2_text = DMP_V2_SPEC.read_text(encoding="utf-8")
    v1_text = DMP_V1_SPEC.read_text(encoding="utf-8")
    promotion_text = PROMOTION_GATES.read_text(encoding="utf-8")

    assert "canonical live internal message contract" in v2_text
    assert "archived historical specification" in v1_text
    assert "executed and closed through Gate 58" in promotion_text
