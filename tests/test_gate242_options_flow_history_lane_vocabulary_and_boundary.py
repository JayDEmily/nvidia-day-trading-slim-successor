from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
VOCAB = REPO_ROOT / 'docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json'
GATES = REPO_ROOT / 'docs/planning/2026-04-09_OPTIONS_AND_FLOW_CONTEXT_HISTORY_LANE_IMPLEMENTATION_GATES_v1.md'
PLANS = REPO_ROOT / 'PLANS.md'
GATE_MAP = REPO_ROOT / 'docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md'


def test_gate242_vocabulary_admits_observational_lane_labels_without_stage_drift() -> None:
    entries = json.loads(VOCAB.read_text(encoding='utf-8'))['entries']
    by_label = {entry['canonical_label']: entry for entry in entries}

    lane = by_label['Options and Flow Context History Lane']
    record = by_label['Options Surface Observation Record']
    store = by_label['Options Surface Observation Store']

    assert lane['stage_owner'] == 'options_flow_context'
    assert 'eighth_stage' in lane['disallowed_phrases']
    assert 'not a desk-cognition stage' in ' '.join(lane['notes'])

    assert record['maps_to_contract'] == 'nvda_desk.schemas.options_flow_history.OptionsFlowHistoryObservationRecord'
    assert 'one lawful raw-source authority only per cycle' in ' '.join(record['notes'])
    assert 'recommendation_receipt' in record['disallowed_phrases']

    assert store['maps_to_contract'] == 'nvda_desk.db.models.OptionsFlowHistoryObservation'
    assert 'Append-only bounded persistence surface' in ' '.join(store['notes'])


def test_gate242_pack_is_no_longer_marked_as_draft_only() -> None:
    gates = GATES.read_text(encoding='utf-8')
    plans = PLANS.read_text(encoding='utf-8')
    gate_map = GATE_MAP.read_text(encoding='utf-8')

    assert 'Status: draft planning pack only' not in gates
    assert 'Status: draft execution log only' not in (REPO_ROOT / 'docs/planning/2026-04-09_OPTIONS_AND_FLOW_CONTEXT_HISTORY_LANE_IMPLEMENTATION_EXECUTION_LOG_v1.md').read_text(encoding='utf-8')
    assert (
        '2026-04-09_OPTIONS_AND_FLOW_CONTEXT_HISTORY_LANE_IMPLEMENTATION_GATES_v1.md' in plans
        or '2026-04-09_OPTIONS_AND_FLOW_CONTEXT_HISTORY_LANE_IMPLEMENTATION_GATES_v1.md' in gate_map
    )
    assert 'recommendation authority' in gates
    assert 'allocator memory' in gates
