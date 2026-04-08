"""Gate 231 coefficient control-plane isolation checks."""
from __future__ import annotations
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / 'PLANS.md'
GATE_MAP = REPO_ROOT / 'docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md'
GATES = REPO_ROOT / 'docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_GATES_v1.md'
LEAVES = REPO_ROOT / 'docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_LEAVES_v1.json'
EXECUTION_LOG = REPO_ROOT / 'docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_EXECUTION_LOG_v1.md'
AUTHORITY_CONFIG = REPO_ROOT / 'config/coefficient_authority.v1.yaml'
MODIFIER_SERVICE = REPO_ROOT / 'src/nvda_desk/services/state_conditioned_modifier.py'
EXECUTION = REPO_ROOT / 'src/nvda_desk/services/execution_expression.py'
RUNTIME = REPO_ROOT / 'src/nvda_desk/services/cognition_runtime.py'
OWNERSHIP_LEDGER = REPO_ROOT / 'docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md'
GATE161 = REPO_ROOT / 'docs/planning/2026-04-02_GATE161_OPPORTUNITY_VS_CAUTION_SHAPING_LAW.md'


def test_gate231_control_surfaces_track_completion_in_later_valid_states() -> None:
    plans = PLANS.read_text(encoding='utf-8')
    gate_map = GATE_MAP.read_text(encoding='utf-8')
    gates = GATES.read_text(encoding='utf-8')
    execution_log = EXECUTION_LOG.read_text(encoding='utf-8')
    payload = json.loads(LEAVES.read_text(encoding='utf-8'))
    assert 'Gate 231' in payload['completed_gate_ids']
    assert all(not leaf_id.startswith('LEAF-G231-') for leaf_id in payload['remaining_leaf_ids'])
    assert '| Gate 231 | complete on `work/gate-231-coefficient-control-plane-isolation-20260408` |' in gate_map
    assert 'Gate 231 captured facts' in gates
    assert '## Gate 231 closeout proof' in execution_log
    assert 'opening-position domain isolation and interface hardening pack' in plans


def test_gate231_source_anchors_match_control_plane_and_shaping_split_claims() -> None:
    config = AUTHORITY_CONFIG.read_text(encoding='utf-8')
    modifier = MODIFIER_SERVICE.read_text(encoding='utf-8')
    execution = EXECUTION.read_text(encoding='utf-8')
    runtime = RUNTIME.read_text(encoding='utf-8')
    ownership = OWNERSHIP_LEDGER.read_text(encoding='utf-8')
    gate161 = GATE161.read_text(encoding='utf-8')
    gates = GATES.read_text(encoding='utf-8')
    assert 'owner_stage: "eligibility"' in config
    assert 'owner_stage: "execution"' in config
    assert 'owner_stage: "posture"' in config
    assert 'owner_stage: "temporal"' in config
    assert 'activation_gate == "Gate 124"' in modifier
    assert 'CoefficientAuthorityDocument.from_yaml_path' in modifier
    assert '_mutable_surface_authority' in modifier
    assert 'ModifierRuntimePacket(' in modifier
    assert 'resolved_surfaces=resolved_surfaces' in modifier
    assert 'effective_lineage=effective_lineage' in modifier
    assert '_operative_surfaces(payload.modifier_runtime_packet)' in execution
    assert 'modifier_runtime_packet = self._modifiers.evaluate(' in runtime
    assert 'posture = self._modifiers.apply_to_posture(posture, modifier_runtime_packet)' in runtime
    assert 'execution = self._modifiers.apply_to_execution(execution, modifier_runtime_packet)' in runtime
    assert 'ModifierRuntimePacket' in ownership
    assert '`ModifierRuntimePacket` outranks `ModifierCompatibilityBridgeSurface`.' in ownership
    assert 'opportunity shaping from caution shaping' in gate161
    assert '`config/coefficient_authority.v1.yaml`' in gates
    assert 'owner-stage law is already explicit' in gates
    assert 'activation-state law is also explicit' in gates
    assert 'ExecutionExpressionService` read operative surfaces from that packet while still authoring the candidate itself' in gates
    assert 'may deform or clamp an already-authored candidate' in gates
