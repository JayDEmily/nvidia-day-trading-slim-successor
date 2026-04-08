"""Gate 230 opening-position seam and downstream handoff checks."""
from __future__ import annotations
import json
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / 'PLANS.md'
GATE_MAP = REPO_ROOT / 'docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md'
GATES = REPO_ROOT / 'docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_GATES_v1.md'
LEAVES = REPO_ROOT / 'docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_LEAVES_v1.json'
EXECUTION_LOG = REPO_ROOT / 'docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_EXECUTION_LOG_v1.md'
RUNTIME = REPO_ROOT / 'src/nvda_desk/services/cognition_runtime.py'
RISK_GATEWAY = REPO_ROOT / 'src/nvda_desk/services/risk_gateway.py'
CDA = REPO_ROOT / 'src/nvda_desk/services/capital_deployment_authority.py'
REVIEW = REPO_ROOT / 'src/nvda_desk/services/review_explanation.py'
OWNERSHIP_LEDGER = REPO_ROOT / 'docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md'

def test_gate230_control_surfaces_track_completion_in_later_valid_states() -> None:
    plans = PLANS.read_text(encoding='utf-8')
    gate_map = GATE_MAP.read_text(encoding='utf-8')
    gates = GATES.read_text(encoding='utf-8')
    execution_log = EXECUTION_LOG.read_text(encoding='utf-8')
    payload = json.loads(LEAVES.read_text(encoding='utf-8'))
    assert 'Gate 230' in payload['completed_gate_ids']
    assert all(not leaf_id.startswith('LEAF-G230-') for leaf_id in payload['remaining_leaf_ids'])
    assert '| Gate 230 | complete on `work/gate-230-opening-position-seam-and-downstream-handoff-20260408` |' in gate_map
    assert 'Gate 230 captured facts' in gates
    assert '## Gate 230 closeout proof' in execution_log
    assert 'opening-position domain isolation and interface hardening pack' in plans

def test_gate230_source_anchors_match_seam_ranking_and_bounded_handoff_claims() -> None:
    runtime = RUNTIME.read_text(encoding='utf-8')
    risk_gateway = RISK_GATEWAY.read_text(encoding='utf-8')
    cda = CDA.read_text(encoding='utf-8')
    review = REVIEW.read_text(encoding='utf-8')
    ownership_ledger = OWNERSHIP_LEDGER.read_text(encoding='utf-8')
    gates = GATES.read_text(encoding='utf-8')
    assert 'execution_post_modifier_pre_final_risk' in runtime
    assert 'apply_final_join' in runtime
    assert 'final_risk_join' in risk_gateway
    assert '_NON_DEPLOY_ACTIONS' in cda
    assert 'review_packet' in review
    assert 'StageLocalHandoffSurface' in ownership_ledger
    assert 'nested or duplicated payloads inside `review_packet` must not outrank' in ownership_ledger
    assert '`StageLocalHandoffSurface.execution_post_modifier_pre_final_risk`' in gates
    assert '`RiskGatewayService.apply_final_join(...)`' in gates
    assert '`review_packet` nested copies' in gates
    assert 'bounded downstream fresh-capital authority may read' in gates
    assert '`cognition_runtime.py`, `risk_gateway.py`, `review_explanation.py`, and `capital_deployment_authority.py`' in gates
