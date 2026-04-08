"""Gate 227 opening-position ingress-boundary isolation checks."""
from __future__ import annotations
import json
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / 'PLANS.md'
GATE_MAP = REPO_ROOT / 'docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md'
GATES = REPO_ROOT / 'docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_GATES_v1.md'
LEAVES = REPO_ROOT / 'docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_LEAVES_v1.json'
EXECUTION_LOG = REPO_ROOT / 'docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_EXECUTION_LOG_v1.md'
RAW_HARNESS = REPO_ROOT / 'src/nvda_desk/testing/canonical_raw_runtime_harness.py'
CHAIN = REPO_ROOT / 'src/nvda_desk/services/chain_to_cognition.py'
CALENDAR_ROUTE = REPO_ROOT / 'docs/planning/2026-03-26_CALENDAR_HORIZON_OWNERSHIP.md'
TEMPORAL_RUNTIME = REPO_ROOT / 'tests/test_temporal_context_runtime.py'

def test_gate227_control_surfaces_track_completion_in_later_valid_states() -> None:
    plans = PLANS.read_text(encoding='utf-8')
    gate_map = GATE_MAP.read_text(encoding='utf-8')
    execution_log = EXECUTION_LOG.read_text(encoding='utf-8')
    payload = json.loads(LEAVES.read_text(encoding='utf-8'))
    assert payload['completed_gate_ids'][:2] == ['Gate 226', 'Gate 227']
    assert all(not leaf_id.startswith('LEAF-G227-') for leaf_id in payload['remaining_leaf_ids'])
    assert 'opening-position domain isolation and interface hardening pack' in plans
    assert '| Gate 227 | complete on `work/gate-227-opening-position-ingress-boundary-isolation-20260408` |' in gate_map
    assert '## Gate 227 closeout proof' in execution_log

def test_gate227_source_anchor_surfaces_match_the_frozen_ingress_claims() -> None:
    raw_harness = RAW_HARNESS.read_text(encoding='utf-8')
    chain = CHAIN.read_text(encoding='utf-8')
    calendar_route = CALENDAR_ROUTE.read_text(encoding='utf-8')
    gates = GATES.read_text(encoding='utf-8')
    temporal_runtime = TEMPORAL_RUNTIME.read_text(encoding='utf-8')
    assert 'load_json_bundle' in raw_harness
    assert 'prepare_runtime_dataset' in raw_harness
    assert 'convert_snapshot' in raw_harness
    assert 'TemporalContextInput(' in chain
    assert 'RealDataCognitionInputs(' in chain
    assert 'Step 0 is an **explicit runtime routing concern**.' in calendar_route
    assert 'TemporalContextService' in temporal_runtime
    assert 'RealDataLoaderService.load_json_bundle(...) -> RealDataLoaderService.prepare_runtime_dataset(...) -> PreparedRuntimeDataset / PreparedRuntimeSnapshot -> ChainToCognitionService.convert_snapshot(...) -> RealDataCognitionInputs' in gates
    assert 'Step 0 remains a runtime orchestration / routing-layer concern' in gates
    assert 'Step 1 begins when `ChainToCognitionService` maps `PreparedRuntimeSnapshot` into `TemporalContextInput`' in gates
    assert 'later domains may not bypass this substrate by re-reading `RealDataBundle` or `PreparedRuntimeDataset` directly' in gates
