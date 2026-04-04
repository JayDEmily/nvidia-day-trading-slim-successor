"""Helpers for historical planning tests that must tolerate later lawful router states."""

from __future__ import annotations

PHASE3_PLAN_MARKERS = {f"next active gate: `Gate {n}`" for n in range(192, 200)}
PHASE3_GATE_MAP_MARKERS = {
    f"Current active gate: **Gate {n} in the Phase 3 main-target repair programme"
    for n in range(192, 200)
}


def contains_any(text: str, markers: set[str]) -> bool:
    return any(marker in text for marker in markers)
