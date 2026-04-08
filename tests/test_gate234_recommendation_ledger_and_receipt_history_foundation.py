"""Gate 234 recommendation-ledger and receipt-history foundation checks."""
from __future__ import annotations
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / 'PLANS.md'
GATE_MAP = REPO_ROOT / 'docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md'
GATES = REPO_ROOT / 'docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_GATES_v1.md'
LEAVES = REPO_ROOT / 'docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_LEAVES_v1.json'
EXECUTION_LOG = REPO_ROOT / 'docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_EXECUTION_LOG_v1.md'
ARCH = REPO_ROOT / 'docs/04_TECHNICAL_ARCHITECTURE.md'
MODELS = REPO_ROOT / 'src/nvda_desk/db/models.py'
EXECUTION_RECORDS = REPO_ROOT / 'src/nvda_desk/services/execution_records.py'
COGNITION_SCHEMAS = REPO_ROOT / 'src/nvda_desk/schemas/cognition.py'
CALIBRATION_SCHEMAS = REPO_ROOT / 'src/nvda_desk/schemas/calibration.py'
REVIEW = REPO_ROOT / 'src/nvda_desk/services/review_explanation.py'


def test_gate234_control_surfaces_track_completion_in_later_valid_states() -> None:
    plans = PLANS.read_text(encoding='utf-8')
    gate_map = GATE_MAP.read_text(encoding='utf-8')
    gates = GATES.read_text(encoding='utf-8')
    execution_log = EXECUTION_LOG.read_text(encoding='utf-8')
    payload = json.loads(LEAVES.read_text(encoding='utf-8'))
    assert 'Gate 234' in payload['completed_gate_ids']
    assert all(not leaf_id.startswith('LEAF-G234-') for leaf_id in payload['remaining_leaf_ids'])
    assert '| Gate 234 | complete on `work/gate-234-recommendation-ledger-and-receipt-history-foundation-20260408` |' in gate_map
    assert 'Gate 234 captured facts' in gates
    assert '## Gate 234 closeout proof' in execution_log
    assert 'opening-position domain isolation and interface hardening pack' in plans


def test_gate234_source_anchors_match_receipt_schema_linkage_and_non_loop_claims() -> None:
    arch = ARCH.read_text(encoding='utf-8')
    models = MODELS.read_text(encoding='utf-8')
    service = EXECUTION_RECORDS.read_text(encoding='utf-8')
    cognition = COGNITION_SCHEMAS.read_text(encoding='utf-8')
    calibration = CALIBRATION_SCHEMAS.read_text(encoding='utf-8')
    review = REVIEW.read_text(encoding='utf-8')
    gates = GATES.read_text(encoding='utf-8')
    assert '- `module_signal_event`' in arch
    assert '- `module_veto_event`' in arch
    assert '- `risk_block_event`' in arch
    assert '- `order_intent`' in arch
    assert '- `position_instance_snapshot`' in arch
    assert 'class ModuleSignalEvent(Base):' in models
    assert 'class ModuleVetoEvent(Base):' in models
    assert 'class RiskBlockEvent(Base):' in models
    assert 'class OrderIntentRecord(Base):' in models
    assert 'class CapitalStateSnapshot(Base):' in models
    assert 'def record_signal(' in service
    assert 'def record_veto(' in service
    assert 'def record_risk_block(' in service
    assert 'def place_paper_order(' in service
    assert 'review_packet_id: str' in cognition
    assert 'decision_packet_id: str' in cognition
    assert 'stage_packet_ids: dict[str, str] = Field(default_factory=dict)' in cognition
    assert 'review_packet_id: str' in calibration
    assert 'decision_packet_id: str' in calibration
    assert 'review_packet["parallel_risk_lane_summary"]' in review
    assert 'review_packet["capital_deployment_authority"]' in review
    assert 'no first-class per-pass opening-position recommendation ledger table exists yet' in gates
    assert '`ExecutionRecordsService` is the current persistence attachment seam' in gates
    assert 'runtime emits `review_packet_id`, `decision_packet_id`, ordered packet lineage, and `stage_packet_ids`' in gates
    assert 'receipt-history derivatives are frozen here as observational-only Phase 1 surfaces' in gates
