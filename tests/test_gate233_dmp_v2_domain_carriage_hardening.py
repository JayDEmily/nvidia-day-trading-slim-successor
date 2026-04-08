"""Gate 233 DMP v2 domain-carriage hardening checks."""
from __future__ import annotations
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / 'PLANS.md'
GATE_MAP = REPO_ROOT / 'docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md'
GATES = REPO_ROOT / 'docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_GATES_v1.md'
LEAVES = REPO_ROOT / 'docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_LEAVES_v1.json'
EXECUTION_LOG = REPO_ROOT / 'docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_EXECUTION_LOG_v1.md'
DMP = REPO_ROOT / 'src/nvda_desk/schemas/dmp_v2.py'
RUNTIME = REPO_ROOT / 'src/nvda_desk/services/cognition_runtime.py'
DMP_TESTS = REPO_ROOT / 'tests/test_dmp_v2_protocol.py'
EXEC_TESTS = REPO_ROOT / 'tests/test_execution_review_runtime.py'


def test_gate233_control_surfaces_track_completion_in_later_valid_states() -> None:
    plans = PLANS.read_text(encoding='utf-8')
    gate_map = GATE_MAP.read_text(encoding='utf-8')
    gates = GATES.read_text(encoding='utf-8')
    execution_log = EXECUTION_LOG.read_text(encoding='utf-8')
    payload = json.loads(LEAVES.read_text(encoding='utf-8'))
    assert 'Gate 233' in payload['completed_gate_ids']
    assert all(not leaf_id.startswith('LEAF-G233-') for leaf_id in payload['remaining_leaf_ids'])
    assert '| Gate 233 | complete on `work/gate-233-dmp-v2-domain-carriage-hardening-20260408` |' in gate_map
    assert 'Gate 233 captured facts' in gates
    assert '## Gate 233 closeout proof' in execution_log
    assert 'opening-position domain isolation and interface hardening pack' in plans


def test_gate233_source_anchors_match_dmp_shell_payload_and_lineage_claims() -> None:
    dmp = DMP.read_text(encoding='utf-8')
    runtime = RUNTIME.read_text(encoding='utf-8')
    dmp_tests = DMP_TESTS.read_text(encoding='utf-8')
    exec_tests = EXEC_TESTS.read_text(encoding='utf-8')
    gates = GATES.read_text(encoding='utf-8')
    assert 'class DmpV2Packet(BaseModel):' in dmp
    assert 'required_blocks=["object_block"]' in dmp
    assert 'data=payload.model_dump(mode="json")' in dmp
    assert 'def build_dmp_v2_packet_from_payload(' in dmp
    assert 'parent_packet_ids=list(parent_packet_ids or [])' in dmp
    assert 'dependency_packet_ids=list(dependency_packet_ids or [])' in dmp
    assert 'build_dmp_v2_packet_from_payload(' in runtime
    assert 'behaviour_class=DmpBehaviourClass.STAGE_OUTPUT' in runtime
    assert 'parent_packet_ids=([upstream_packet_ids[-1]] if upstream_packet_ids else [])' in runtime
    assert 'dependency_packet_ids=list(upstream_packet_ids)' in runtime
    assert 'assert restored.blocks[0].block_type == "object_block"' in dmp_tests
    assert 'assert result.stage_packets[6].lineage.parent_packet_ids == [result.stage_packets[5].packet_id]' in exec_tests
    assert '`DmpV2Packet` carries producer, contract, lineage, execution context, blocks, summary, validation, and extensions' in gates
    assert '`build_dmp_v2_packet_from_payload(...)` is the canonical live builder' in gates
    assert '`DeskCognitionRuntime.run(...)` builds one packet per stage output' in gates
    assert 'the typed model dump inside the `object_block` is the canonical carried payload' in gates
    assert '`dmp_v2.py`, `cognition_runtime.py`, and the execution/review runtime packet consumers' in gates
