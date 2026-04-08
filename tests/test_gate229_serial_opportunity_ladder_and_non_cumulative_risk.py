"""Gate 229 serial ladder and non-cumulative risk checks."""
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
POSTURE = REPO_ROOT / 'src/nvda_desk/services/posture_risk.py'
ELIGIBILITY = REPO_ROOT / 'src/nvda_desk/services/playbook_eligibility.py'
EXECUTION = REPO_ROOT / 'src/nvda_desk/services/execution_expression.py'
GATE152 = REPO_ROOT / 'docs/planning/2026-04-02_GATE152_STAGE5_STAGE6_AUTHORITY_REPLAN.md'
GATE167 = REPO_ROOT / 'docs/planning/2026-04-02_GATE167_SERIAL_CONSERVATISM_BINDING_POINT_LAW.md'

def test_gate229_control_surfaces_track_completion_in_later_valid_states() -> None:
    plans = PLANS.read_text(encoding='utf-8')
    gate_map = GATE_MAP.read_text(encoding='utf-8')
    gates = GATES.read_text(encoding='utf-8')
    execution_log = EXECUTION_LOG.read_text(encoding='utf-8')
    payload = json.loads(LEAVES.read_text(encoding='utf-8'))
    assert 'Gate 229' in payload['completed_gate_ids']
    assert all(not leaf_id.startswith('LEAF-G229-') for leaf_id in payload['remaining_leaf_ids'])
    assert '| Gate 229 | complete on `work/gate-229-serial-opportunity-ladder-and-non-cumulative-risk-20260408` |' in gate_map
    assert 'Gate 229 captured facts' in gates
    assert '## Gate 229 closeout proof' in execution_log
    assert 'opening-position domain isolation and interface hardening pack' in plans

def test_gate229_source_anchors_match_serial_question_ownership_and_reset_claims() -> None:
    runtime = RUNTIME.read_text(encoding='utf-8')
    posture = POSTURE.read_text(encoding='utf-8')
    eligibility = ELIGIBILITY.read_text(encoding='utf-8')
    execution = EXECUTION.read_text(encoding='utf-8')
    gates = GATES.read_text(encoding='utf-8')
    gate152 = GATE152.read_text(encoding='utf-8')
    gate167 = GATE167.read_text(encoding='utf-8')
    assert 'posture = self._posture.evaluate(' in runtime
    assert 'eligibility = self._eligibility.evaluate(' in runtime
    assert 'execution = self._execution.evaluate(' in runtime
    assert 'class PostureRiskService' in posture
    assert 'PlaybookEligibilityService' in eligibility
    assert 'ExecutionExpressionService' in execution
    assert 'stage6_owns_candidate_ranking_and_lead_selection' in execution
    assert 'Gate 152 is planning-only' in gate152
    assert 'posture_derisk_local_envelope' in gate167
    assert '`PostureRiskService.evaluate(...) -> PlaybookEligibilityService.evaluate(...) -> ExecutionExpressionService.evaluate(...)`' in gates
    assert 'Stage 4 `Posture and Risk Permission`' in gates
    assert 'Stage 5 `Playbook Eligibility`' in gates
    assert 'Stage 6 `Expression and Execution`' in gates
    assert 'must reset after the serial decision' in gates
