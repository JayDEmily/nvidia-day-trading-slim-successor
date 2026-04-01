"""Gate 112 governance-pack closeout checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-03-30_REPO_PROCESS_GOVERNANCE_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-30_REPO_PROCESS_GOVERNANCE_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-03-30_REPO_PROCESS_GOVERNANCE_EXECUTION_LOG_v1.md"
CLOSEOUT = REPO_ROOT / "docs/planning/2026-03-30_GATE112_REPO_PROCESS_GOVERNANCE_CLOSEOUT.md"

ALLOWED_CURRENT_GATE_MARKERS = {
    "Current active gate: **none — repo-process governance pack closed through Gate 112 on `main`**.",
    "Current active gate: **none — execution-authority microtranche closed through Gate 113 on `main`**.",
    "Current active gate: **none — research-mode clarity microtranche closed through Gate 114 on `main`**.",
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

    "Current active gate: **Gate 135 in the opening-drive continuation lifecycle pilot pack**.",
    "Current active gate: **Gate 136 in the opening-drive continuation lifecycle pilot pack**.",
    "Current active gate: **Gate 137 in the opening-drive continuation lifecycle pilot pack**.",
    "Current active gate: **Gate 138 in the opening-drive continuation lifecycle pilot pack**.",
    "Current active gate: **Gate 139 in the opening-drive continuation lifecycle pilot pack**.",
    "Current active gate: **none — opening-drive continuation lifecycle pilot pack closed through Gate 139 on `main`**.",
    "Current active gate: **Gate 140 in the execution-ledger Alembic parity corrective pack**.",
    "Current active gate: **none — execution-ledger Alembic parity corrective pack closed through Gate 140 on `main`**.",
}


def test_governance_pack_is_closed_honestly_across_the_quartet() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")

    assert ("## Active pack\n\n- none" in plans or "2026-03-31_POST_FLIGHT_REPO_CONSISTENCY_GATES_v1.md" in plans or "2026-04-01_OPENING_DRIVE_CONTINUATION_LIFECYCLE_PILOT_GATES_v1.md" in plans or "2026-04-01_EXECUTION_LEDGER_ALEMBIC_PARITY_CORRECTIVE_GATES_v1.md" in plans) or ("2026-03-30_HISTORICAL_EVALUATION_READINESS_GATES_v1.md" in plans)
    assert ("repo-process governance pack closed through Gate 112 on `main`" in plans) or ("2026-03-30_REPO_PROCESS_GOVERNANCE_GATES_v1.md" in plans)
    assert any(marker in gate_map for marker in ALLOWED_CURRENT_GATE_MARKERS)
    assert "| Gate 112 | complete on `main` |" in gate_map
    assert "Status: closed repo-process governance pack on `main`; Gates 107-112 complete, no active gate" in gates
    assert leaves["execution_status"] == "repo_process_governance_pack_closed_through_gate_112_on_main"
    assert leaves["active_gate"] == "none — repo-process governance pack closed through Gate 112 on main"
    assert leaves["completed_gate_ids"] == ["Gate 107", "Gate 108", "Gate 109", "Gate 110", "Gate 111", "Gate 112"]
    assert leaves["remaining_leaf_ids"] == []
    assert "Status: closed execution log for the repo-process governance pack; Gates 107-112 complete on `main`, no active gate" in execution_log


def test_gate112_closeout_doc_freezes_packaging_intent() -> None:
    closeout = CLOSEOUT.read_text(encoding="utf-8")
    assert "Status: Gate 112 complete on `main`; repo-process governance pack closed honestly" in closeout
    assert "The repo-process governance pack is closed through Gate 112 on `main`." in closeout
    assert "nvda_repo_process_governance_pack_closed_gate112_main_2026-03-30.zip" in closeout
