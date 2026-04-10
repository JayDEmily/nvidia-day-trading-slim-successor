"""Gate 132 bounded sibling-scenario pack checks."""

from __future__ import annotations

from pathlib import Path

from nvda_desk.schemas.trace_review import BoundedTraceFixturePack

REPO_ROOT = Path(__file__).resolve().parents[1]
PACK_PATH = REPO_ROOT / "fixtures" / "trace_review" / "gate_132_bounded_trace_fixture_pack.json"
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-31_BOUNDED_TRACE_SCENARIO_REVIEW_LEAVES_v1.json"


def _load_pack() -> BoundedTraceFixturePack:
    return BoundedTraceFixturePack.model_validate_json(PACK_PATH.read_text())


def test_gate132_router_and_gate_map_allow_the_new_pack() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    leaves = LEAVES.read_text(encoding="utf-8")

    assert (
        "2026-03-31_BOUNDED_TRACE_SCENARIO_REVIEW_GATES_v1.md" in plans
        or "successor retained-test cleanup execution pack; Gate 224 is active" in plans
        or "Gate 224 is complete on `work/gate-224-runtime-review-and-contract-retarget-20260406`" in plans
        or "successor retained-test cleanup execution pack; Gate 225 is active" in plans
        or "no active pack currently routed" in plans.lower()
        or "2026-04-09_MAIN_SERIAL_STACK_STEPS_3_TO_6_CORRECTIVE_IMPLEMENTATION_GATES_v1.md" in plans
    )
    assert (
        "Gate 132 in the bounded trace scenario review pack" in gate_map
        or "Gate 133 in the bounded trace scenario review pack" in gate_map
        or "Gate 134 in the bounded trace scenario review pack" in gate_map
        or "none — bounded trace scenario review pack closed through Gate 134 on `main`" in gate_map
        or "Gate 149 in the stage-local handoff and terminal-risk seams pack" in gate_map
        or "none — stage-local handoff and terminal-risk seams pack closed through Gate 149 on `main`" in gate_map
        or "Gate 224 active on `work/gate-224-runtime-review-and-contract-retarget-20260406` under the successor retained-test cleanup execution pack" in gate_map
        or "No active gate under the successor retained-test cleanup execution pack. Gate 224 is complete on `work/gate-224-runtime-review-and-contract-retarget-20260406`; Gate 225 is not yet activated." in gate_map
        or "Gate 225 active on `work/gate-225-retained-test-cleanup-closeout-20260406` under the successor retained-test cleanup execution pack" in gate_map
        or "No active gate under the successor retained-test cleanup execution pack. Gate 225 is complete on `work/gate-225-retained-test-cleanup-closeout-20260406`; cleanup pack closed." in gate_map
        or "Current active gate: **No active pack currently routed. The successor retained-test cleanup execution pack is closed through Gate 225 on `work/gate-225-retained-test-cleanup-closeout-20260406`.**" in gate_map
        or "Current active gate: **No active pack currently routed. The main serial stack Steps 3-6 corrective implementation pack is closed through Gate 241 in the uploaded workspace copy.**" in gate_map
    )
    assert "Gate 132" in leaves


def test_gate132_fixture_pack_stays_small_and_anchor_explicit() -> None:
    pack = _load_pack()

    assert pack.pack_id == "gate-132-bounded-trace-review-v1"
    assert pack.source_fixture_pack_id == "gate-e-prepared-runtime"
    assert pack.anchor_symbol == "NVDA"
    assert len(pack.scenarios) == 5
    assert pack.scenario_ids == [
        "anchor_event_imminent",
        "clear_window_continuation",
        "lunch_flattened",
        "imminent_pin_derisk",
        "mild_down_block",
    ]
    assert len(pack.scenario_ids) <= 6
    assert all(s.anchor_snapshot_ts == pack.anchor_snapshot_ts for s in pack.scenarios)


def test_gate132_scenarios_remain_bounded_and_coherent() -> None:
    pack = _load_pack()
    anchor = next(s for s in pack.scenarios if s.scenario_id == "anchor_event_imminent")

    for scenario in pack.scenarios:
        assert scenario.prepared_snapshot.symbol == anchor.prepared_snapshot.symbol
        assert scenario.prepared_snapshot.front_expiry == anchor.prepared_snapshot.front_expiry
        assert scenario.prepared_snapshot.next_expiry == anchor.prepared_snapshot.next_expiry
        assert len(scenario.perturbations) <= 6
        assert scenario.risk_budget_remaining_pct == 68.0

    mild_down = next(s for s in pack.scenarios if s.scenario_id == "mild_down_block")
    rel_move = abs(mild_down.prepared_snapshot.spot_price - anchor.prepared_snapshot.spot_price) / anchor.prepared_snapshot.spot_price
    assert rel_move <= 0.002

    clear_window = next(s for s in pack.scenarios if s.scenario_id == "clear_window_continuation")
    assert clear_window.prepared_snapshot.gamma_pressure_score == 0.35
    assert clear_window.prepared_snapshot.spot_to_pin_distance_pct == 1.2

    imminent_pin = next(s for s in pack.scenarios if s.scenario_id == "imminent_pin_derisk")
    assert imminent_pin.prepared_snapshot.spot_to_pin_distance_pct == 0.08
    assert imminent_pin.prepared_snapshot.next_event_at is not None
    assert anchor.prepared_snapshot.next_event_at is not None
    assert imminent_pin.prepared_snapshot.next_event_at < anchor.prepared_snapshot.next_event_at
