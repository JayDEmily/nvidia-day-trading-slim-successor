"""Gate 232 parallel-risk lane clean-room restart checks."""
from __future__ import annotations
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / 'PLANS.md'
GATE_MAP = REPO_ROOT / 'docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md'
GATES = REPO_ROOT / 'docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_GATES_v1.md'
LEAVES = REPO_ROOT / 'docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_LEAVES_v1.json'
EXECUTION_LOG = REPO_ROOT / 'docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_EXECUTION_LOG_v1.md'
NORMATIVE = REPO_ROOT / 'docs/01_NORMATIVE.md'
OWNERSHIP = REPO_ROOT / 'docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md'
RUNTIME = REPO_ROOT / 'src/nvda_desk/services/cognition_runtime.py'
LANE = REPO_ROOT / 'src/nvda_desk/services/parallel_risk_lane.py'
REVIEW = REPO_ROOT / 'src/nvda_desk/services/review_explanation.py'


def test_gate232_control_surfaces_track_completion_in_later_valid_states() -> None:
    plans = PLANS.read_text(encoding='utf-8')
    gate_map = GATE_MAP.read_text(encoding='utf-8')
    gates = GATES.read_text(encoding='utf-8')
    execution_log = EXECUTION_LOG.read_text(encoding='utf-8')
    payload = json.loads(LEAVES.read_text(encoding='utf-8'))
    assert 'Gate 232' in payload['completed_gate_ids']
    assert all(not leaf_id.startswith('LEAF-G232-') for leaf_id in payload['remaining_leaf_ids'])
    assert '| Gate 232 | complete on `work/gate-232-parallel-risk-lane-clean-room-restart-20260408` |' in gate_map
    assert 'Gate 232 captured facts' in gates
    assert '## Gate 232 closeout proof' in execution_log
    assert 'opening-position domain isolation and interface hardening pack' in plans


def test_gate232_source_anchors_match_lane_question_and_anti_duplication_claims() -> None:
    normative = NORMATIVE.read_text(encoding='utf-8')
    ownership = OWNERSHIP.read_text(encoding='utf-8')
    runtime = RUNTIME.read_text(encoding='utf-8')
    lane = LANE.read_text(encoding='utf-8')
    review = REVIEW.read_text(encoding='utf-8')
    gates = GATES.read_text(encoding='utf-8')
    assert 'It is **not** a numbered stage, **not** `1.1`, **not** `step_8`, and **not** a bypass of the serial seven-step desk cognition grammar.' in normative
    assert '- **Canonical label:** Independent Parallel Risk Lane' in ownership
    assert '`nvda_desk.schemas.parallel_risk.ParallelRiskLanePacket`' in ownership
    assert 'parallel_risk_lane = self._parallel_risk_lane.evaluate(' in runtime
    assert 'parallel_risk_lane = self._parallel_risk_lane.enrich_market_translation(' in runtime
    assert 'parallel_risk_lane = self._parallel_risk_lane.enrich_candidate_semantics(' in runtime
    assert 'It does not implement final arbitration, playbook-internal logic, or a second' in lane
    assert 'Do not create distributed caution fog or a silent second owner' in lane
    assert 'review_packet["parallel_risk_lane"]' in review
    assert '`ParallelRiskLaneService.evaluate(...)` immediately after Temporal / Regime / Options-Flow evaluation' in gates
    assert '**not** a numbered serial stage, **not** `1.1`, **not** `step_8`' in gates
    assert '`ParallelRiskLanePacket`' in gates
    assert 'may describe environmental weather, fragility, reshape/wait/hedge-required style consequences' in gates
    assert '`parallel_risk_lane.py`, `cognition_runtime.py`, `posture_risk.py`, `execution_expression.py`, and `review_explanation.py`' in gates
