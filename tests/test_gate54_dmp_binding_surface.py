from __future__ import annotations

from pathlib import Path

from tests.test_gate52_native_playbook_hierarchy import _supportive_runtime_result

REPO_ROOT = Path(__file__).resolve().parents[1]
DMP_V2_SPEC = REPO_ROOT / "docs/planning/2026-03-24_DMP_V2_NORMATIVE_SPEC.md"
GATE54_DECISION = REPO_ROOT / "docs/planning/2026-03-26_DMP_BINDING_SURFACE_DECISION.md"
GATE56_PACK = REPO_ROOT / "docs/planning/2026-03-26_DMP_V2_PROMOTION_GATES_v1.md"


def test_runtime_keeps_v2_as_the_only_live_stage_packet_surface() -> None:
    result = _supportive_runtime_result()

    assert result.stage_packets
    assert all(packet.protocol_version == "dmp.v2" for packet in result.stage_packets)
    assert result.packet_lineage == tuple(packet.packet_id for packet in result.stage_packets)


def test_dmp_docs_state_gate54_as_historical_freeze_and_v2_as_current_target() -> None:
    v2_text = DMP_V2_SPEC.read_text(encoding="utf-8")
    decision_text = GATE54_DECISION.read_text(encoding="utf-8")
    pack_text = GATE56_PACK.read_text(encoding="utf-8")

    assert "canonical live internal message contract" in v2_text
    assert "historical freeze" in decision_text.lower() or "Gate 54" in decision_text
    assert "Gate 57" in pack_text
