"""Helpers for historical planning tests that must tolerate later lawful router states."""

from __future__ import annotations

PHASE3_PLAN_MARKERS = {f"next active gate: `Gate {n}`" for n in range(192, 200)}
PHASE3_GATE_MAP_MARKERS = {
    f"Current active gate: **Gate {n} in the Phase 3 main-target repair programme"
    for n in range(192, 200)
}

CLEANUP_PLAN_MARKERS = {
    "2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_GATES_v1.md",
    "active pack is the successor retained-test cleanup execution pack; Gate 222 is active",
    "active pack is the successor retained-test cleanup execution pack; Gate 223 is active",
    "active pack is the successor retained-test cleanup execution pack; Gate 224 is active",
    "active pack is the successor retained-test cleanup execution pack; Gate 225 is active",
    "no active pack currently routed",
}

CLEANUP_GATE_MAP_MARKERS = {
    "Current active gate: **Gate 222 active on",
    "Current active gate: **Gate 223 active on",
    "Current active gate: **Gate 224 active on",
    "Current active gate: **Gate 225 active on",
    "Current active gate: **No active pack currently routed. The successor retained-test cleanup execution pack is closed through Gate 225",
}


def contains_any(text: str, markers: set[str]) -> bool:
    return any(marker in text for marker in markers)
