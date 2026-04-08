"""Gate 235 cross-flow harness and pack closeout checks."""
from __future__ import annotations
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / 'PLANS.md'
GATE_MAP = REPO_ROOT / 'docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md'
GATES = REPO_ROOT / 'docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_GATES_v1.md'
LEAVES = REPO_ROOT / 'docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_LEAVES_v1.json'
EXECUTION_LOG = REPO_ROOT / 'docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_EXECUTION_LOG_v1.md'
SCOPE_NOTE = REPO_ROOT / 'docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_SCOPE_NOTE_v1.md'
RAW_HARNESS = REPO_ROOT / 'src/nvda_desk/testing/canonical_raw_runtime_harness.py'
CHAIN = REPO_ROOT / 'src/nvda_desk/services/chain_to_cognition.py'
RUNTIME = REPO_ROOT / 'src/nvda_desk/services/cognition_runtime.py'
DMP = REPO_ROOT / 'src/nvda_desk/schemas/dmp_v2.py'
EXECUTION_RECORDS = REPO_ROOT / 'src/nvda_desk/services/execution_records.py'


def test_gate235_control_surfaces_track_pack_closeout_truthfully() -> None:
    plans = PLANS.read_text(encoding='utf-8')
    gate_map = GATE_MAP.read_text(encoding='utf-8')
    gates = GATES.read_text(encoding='utf-8')
    execution_log = EXECUTION_LOG.read_text(encoding='utf-8')
    scope_note = SCOPE_NOTE.read_text(encoding='utf-8')
    payload = json.loads(LEAVES.read_text(encoding='utf-8'))
    assert payload['active_gate'] == 'none'
    assert payload['remaining_leaf_ids'] == []
    assert payload['pending_gate_ids'] == []
    assert 'Gate 235' in payload['completed_gate_ids']
    assert all(leaf['status'] == 'complete' for leaf in payload['leaves'])
    assert '## Active pack\n\n- none' in plans
    assert 'latest closed pack retained as evidence is the opening-position domain isolation and interface hardening pack closed through Gate 235' in plans
    assert '| Gate 235 | complete on `work/gate-235-cross-flow-harness-and-pack-closeout-20260408` |' in gate_map
    assert 'Current active gate: **No active pack currently routed. The opening-position domain isolation and interface hardening pack is closed through Gate 235' in gate_map
    assert 'Gate 235 captured facts' in gates
    assert '## Gate 235 closeout proof' in execution_log
    assert 'closed Gates 226-235 pack' in scope_note


def test_gate235_source_anchors_match_bounded_route_and_stop_line_claims() -> None:
    raw_harness = RAW_HARNESS.read_text(encoding='utf-8')
    chain = CHAIN.read_text(encoding='utf-8')
    runtime = RUNTIME.read_text(encoding='utf-8')
    dmp = DMP.read_text(encoding='utf-8')
    execution_records = EXECUTION_RECORDS.read_text(encoding='utf-8')
    gates = GATES.read_text(encoding='utf-8')
    scope_note = SCOPE_NOTE.read_text(encoding='utf-8')
    assert 'load_json_bundle' in raw_harness
    assert 'prepare_runtime_dataset' in raw_harness
    assert 'convert_snapshot' in chain
    assert 'self._capital_deployment_authority.evaluate(' in runtime
    assert 'build_dmp_v2_packet_from_payload(' in runtime
    assert 'required_blocks=["object_block"]' in dmp
    assert 'def record_signal(' in execution_records
    assert 'def record_veto(' in execution_records
    assert 'def record_risk_block(' in execution_records
    assert 'def place_paper_order(' in execution_records
    assert 'raw-bundle admission and preparation -> Step 0 route selection -> Step 1 temporal/calendar truth -> serial opportunity ladder through Stage 6 -> preserved opening-position seam -> bounded CDA decision -> DMP stage-packet carriage and packet lineage -> recommendation-receipt attachment seam' in gates
    assert 'no close-position logic, no capital displacement authority, no carry-horizon expansion, and no full arbiter are admitted in this pack' in gates
    assert 'the coefficient plane may shape but not invent candidates' in gates
    assert 'PLANS.md` returns to `## Active pack\n\n- none`' in gates
    assert 'no active pack currently routed' in scope_note
