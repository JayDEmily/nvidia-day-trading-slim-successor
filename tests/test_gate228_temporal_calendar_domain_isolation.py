"""Gate 228 temporal/calendar domain isolation checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_EXECUTION_LOG_v1.md"
TEMPORAL = REPO_ROOT / "src/nvda_desk/services/temporal_context.py"
CHAIN = REPO_ROOT / "src/nvda_desk/services/chain_to_cognition.py"
SCHEMAS = REPO_ROOT / "src/nvda_desk/schemas/cognition.py"
GATE175 = REPO_ROOT / "tests/test_gate175_temporal_calendar_multi_clock_runtime.py"
GATE89 = REPO_ROOT / "tests/test_gate89_financial_calendar_crosswalk_and_dmp_lane.py"


def test_gate228_control_surfaces_track_completion_in_later_valid_states() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    payload = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert "Gate 228" in payload["completed_gate_ids"]
    assert all(not leaf_id.startswith("LEAF-G228-") for leaf_id in payload["remaining_leaf_ids"])
    assert "| Gate 228 | complete on `work/gate-228-temporal-calendar-domain-isolation-20260408` |" in gate_map
    assert "Gate 228 captured facts" in gates
    assert "## Gate 228 closeout proof" in execution_log
    assert "opening-position domain isolation and interface hardening pack" in plans


def test_gate228_source_anchors_match_frozen_temporal_calendar_claims() -> None:
    temporal = TEMPORAL.read_text(encoding="utf-8")
    chain = CHAIN.read_text(encoding="utf-8")
    schemas = SCHEMAS.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    gate175 = GATE175.read_text(encoding="utf-8")
    gate89 = GATE89.read_text(encoding="utf-8")

    assert "class TemporalContextService" in temporal
    assert "def evaluate(self, payload: TemporalContextInput) -> TemporalContextOutput:" in temporal
    assert "compatibility_next_event_at_subordinate_to_live_event_snapshot" in temporal
    assert "desk_calendar_authority" in temporal
    assert "class TemporalContextOutput" in schemas
    assert "event_window_state: str" in schemas
    assert "carryover_state: str" in schemas
    assert "TemporalContextInput(" in chain
    assert "packet = result.parallel_risk_lane" in gate175
    assert "paired_runtime_consumers=[\"src/nvda_desk/services/temporal_context.py\"]" in gate89

    assert "the checked-in day-state author remains `TemporalContextService.evaluate(...)`" in gates
    assert "the governing question frozen for this domain is" in gates
    assert "`next_event_at` and `live_event_snapshot`" in gates
    assert "`ChainToCognitionService`, `PreparedRuntimeSnapshot`, `ParallelRiskLanePacket.temporal_surface`" in gates
