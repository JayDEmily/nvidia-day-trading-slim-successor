"""Gate 226 opening-position pack bootstrap and routing invariants."""
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
CONTRADICTION_REPORT = REPO_ROOT / 'docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_CONTRADICTION_REPORT_v1.md'
CHECKLIST = REPO_ROOT / 'docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_DOCUMENT_TOUCH_CHECKLIST_v1.md'

def test_gate226_routes_new_pack_and_remains_completed_in_later_valid_states() -> None:
    plans = PLANS.read_text(encoding='utf-8')
    gate_map = GATE_MAP.read_text(encoding='utf-8')
    gates = GATES.read_text(encoding='utf-8')
    execution_log = EXECUTION_LOG.read_text(encoding='utf-8')
    scope_note = SCOPE_NOTE.read_text(encoding='utf-8')
    contradiction_report = CONTRADICTION_REPORT.read_text(encoding='utf-8')
    checklist = CHECKLIST.read_text(encoding='utf-8')
    payload = json.loads(LEAVES.read_text(encoding='utf-8'))
    assert 'docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_GATES_v1.md' in plans
    assert 'docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_LEAVES_v1.json' in plans
    assert 'docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_EXECUTION_LOG_v1.md' in plans
    assert 'opening-position domain isolation and interface hardening pack' in plans
    assert '| Gate 226 | complete on `work/gate-226-pack-bootstrap-and-routing-20260408` |' in gate_map
    assert payload['completed_gate_ids'][0] == 'Gate 226'
    assert 'Gate 226' in payload['completed_gate_ids']
    assert set(payload['completed_leaf_ids']).issuperset({f'LEAF-G226-00{i}' for i in range(1,6)})
    assert all(leaf['status']=='complete' for leaf in payload['leaves'] if leaf['id'].startswith('LEAF-G226-'))
    assert '### Gate 226: Pack bootstrap, contradiction scan, and active-pack routing closeout' in gates
    assert 'Gate 226 closeout proof' in execution_log
    assert 'Gates 226-235' in scope_note or 'closed Gates 226-235 pack' in scope_note
    assert 'Gate 226 completed the normal quartet update' in contradiction_report
    assert 'used in Gate 226 to route the active pack truthfully' in checklist
