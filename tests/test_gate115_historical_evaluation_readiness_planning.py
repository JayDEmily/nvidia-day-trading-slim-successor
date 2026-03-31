"""Gate 115 historical-evaluation readiness planning checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-03-30_HISTORICAL_EVALUATION_READINESS_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-30_HISTORICAL_EVALUATION_READINESS_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-03-30_HISTORICAL_EVALUATION_READINESS_EXECUTION_LOG_v1.md"
CHECKLIST = REPO_ROOT / "docs/planning/2026-03-30_HISTORICAL_EVALUATION_READINESS_DOCUMENT_TOUCH_CHECKLIST_v1.md"


ALLOWED_CURRENT_GATE_MARKERS = {
    "Current active gate: **Gate 115 in the historical-evaluation readiness pack**.",
    "Current active gate: **Gate 116 in the historical-evaluation readiness pack**.",
    "Current active gate: **Gate 117 in the historical-evaluation readiness pack**.",
    "Current active gate: **Gate 118 in the historical-evaluation readiness pack**.",
    "Current active gate: **Gate 119 in the historical-evaluation readiness pack**.",
    "Current active gate: **Gate 120 in the historical-evaluation readiness pack**.",
    "Current active gate: **Gate 121 in the historical-evaluation readiness pack**.",
    "Current active gate: **none — historical-evaluation readiness pack closed through Gate 121 on `main`**.",
    "Current active gate: **Gate 122 in the signal-coefficient authority pack**.",
    "Current active gate: **Gate 123 in the signal-coefficient authority pack**.",
    "Current active gate: **Gate 124 in the signal-coefficient authority pack**.",
    "Current active gate: **Gate 125 in the signal-coefficient authority pack**.",
    "Current active gate: **Gate 126 in the signal-coefficient authority pack**.",
    "Current active gate: **Gate 127 in the signal-coefficient authority pack**.",
    "Current active gate: **none — signal-coefficient authority pack closed through Gate 127 on `main`**.",
    "Current active gate: **Gate 128 in the post-flight repo consistency pack**.",
    "Current active gate: **Gate 129 in the post-flight repo consistency pack**.",
    "Current active gate: **Gate 130 in the post-flight repo consistency pack**.",
    "Current active gate: **Gate 131 in the post-flight repo consistency pack**.",
    "Current active gate: **none — post-flight repo consistency pack closed through Gate 131 on `main`**.",
}


def test_historical_evaluation_readiness_pack_is_active() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert GATES.exists()
    assert LEAVES.exists()
    assert EXECUTION_LOG.exists()
    assert ("2026-03-30_HISTORICAL_EVALUATION_READINESS_GATES_v1.md" in plans) or ("latest recoverable runtime pack evidence" in plans)
    assert any(f"Gate {gate}" in plans for gate in range(115, 122)) or "closed through Gate 121" in plans
    assert any(marker in gate_map for marker in ALLOWED_CURRENT_GATE_MARKERS)
    assert (
        "Status: active historical-evaluation readiness pack; Gate 115 active, Gates 116-121 planned" in gates
        or "Status: active historical-evaluation readiness pack; Gate 115 complete on `main`, Gate 116 active, Gates 117-121 planned" in gates
        or "Status: active historical-evaluation readiness pack; Gates 115-116 complete on `main`, Gate 117 active, Gates 118-121 planned" in gates
        or "Status: active historical-evaluation readiness pack; Gates 115-117 complete on `main`, Gate 118 active, Gates 119-121 planned" in gates
        or "Status: active historical-evaluation readiness pack; Gates 115-118 complete on `main`, Gate 119 active, Gates 120-121 planned" in gates
        or "Status: active historical-evaluation readiness pack; Gates 115-119 complete on `main`, Gate 120 active, Gate 121 planned" in gates
        or "Status: active historical-evaluation readiness pack; Gates 115-120 complete on `main`, Gate 121 active" in gates
        or "Status: closed historical-evaluation readiness pack on `main`; Gates 115-121 complete, no active gate" in gates
    )
    assert leaves["execution_status"] in {
        "gate_114_closed_historical_evaluation_readiness_pack_active_from_gate_115",
        "gate_115_complete_gate_116_active_on_main",
        "gate_116_complete_gate_117_active_on_main",
        "gate_117_complete_gate_118_active_on_main",
        "gate_118_complete_gate_119_active_on_main",
        "gate_119_complete_gate_120_active_on_main",
        "gate_120_complete_gate_121_active_on_main",
        "historical_evaluation_readiness_pack_closed_through_gate_121_on_main",
    }
    assert leaves["active_gate"] in {
        "Gate 115",
        "Gate 116",
        "Gate 117",
        "Gate 118",
        "Gate 119",
        "Gate 120",
        "Gate 121",
        "none — historical-evaluation readiness pack closed through Gate 121 on main",
    }
    assert len(leaves["remaining_leaf_ids"]) in {45, 38, 32, 25, 19, 12, 6, 0}
    assert execution_log.startswith("# 2026-03-30 Historical Evaluation Readiness Execution Log v1")
    assert "Gate 115-121 pack" in checklist or "Gate 115-121" in checklist


def test_operator_review_ids_are_mapped_and_deferred_ids_stay_out() -> None:
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    for accepted in ("C011", "C013", "C014", "C004", "C006", "C009", "C001"):
        assert accepted in gates
    for deferred in leaves["deferred_operator_review_ids"]:
        assert deferred not in gates
    assert leaves["global_rules"]["gate_order_is_dependency_first_not_brainstorm_order"] is True
