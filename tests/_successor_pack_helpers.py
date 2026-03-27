from __future__ import annotations

import re


def successor_pack_position(active_gate: str) -> int:
    """Return the next gate number, or closed-after+1 for truthfully closed packs."""

    gate_match = re.search(r"Gate\s+(\d+)", active_gate)
    if gate_match:
        return int(gate_match.group(1))
    closed_match = re.search(r"closed_after_gate_(\d+)", active_gate)
    if closed_match:
        return int(closed_match.group(1)) + 1
    raise ValueError(f"Unrecognised active gate state: {active_gate}")


def successor_pack_closed(active_gate: str) -> bool:
    return "closed_after_gate_" in active_gate
