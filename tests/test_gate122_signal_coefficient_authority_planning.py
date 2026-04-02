"""Gate 122 signal-coefficient authority planning checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_LEAVES_v1.json"
EXECUTION_LOG = (
    REPO_ROOT / "docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_EXECUTION_LOG_v1.md"
)
CHECKLIST = (
    REPO_ROOT
    / "docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_DOCUMENT_TOUCH_CHECKLIST_v1.md"
)

ALLOWED_CURRENT_GATE_MARKERS = {
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
    "Current active gate: **Gate 142 in the stage-local handoff and terminal-risk seams pack**.",
    "Current active gate: **Gate 143 in the stage-local handoff and terminal-risk seams pack**.",
    "Current active gate: **Gate 144 in the stage-local handoff and terminal-risk seams pack**.",
    "Current active gate: **Gate 145 in the stage-local handoff and terminal-risk seams pack**.",
    "Current active gate: **Gate 146 in the stage-local handoff and terminal-risk seams pack**.",
    "Current active gate: **Gate 147 in the stage-local handoff and terminal-risk seams pack**.",
    "Current active gate: **Gate 148 in the stage-local handoff and terminal-risk seams pack**.",
    "Current active gate: **Gate 149 in the stage-local handoff and terminal-risk seams pack**.",
    "Current active gate: **none — stage-local handoff and terminal-risk seams pack closed through Gate 149 on `main`**.",
    "Current active gate: **Gate 151 in the stage-local handoff corrective successor pack**.",
    "Current active gate: **Gate 152 in the stage-local handoff corrective successor pack**.",
    "Current active gate: **Gate 153 in the stage-local handoff corrective successor pack**.",
    "Current active gate: **Gate 154 in the stage-local handoff corrective successor pack**.",
    "Current active gate: **Gate 155 in the stage-local handoff corrective successor pack**.",
    "Current active gate: **Gate 156 in the stage-local handoff corrective successor pack**.",
    "Current active gate: **none — stage-local handoff corrective successor pack closed through Gate 156 on `main`**.",
}


def test_signal_coefficient_authority_pack_is_active() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert (
        "2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_GATES_v1.md" in plans
        or "no active pack currently routed; post-flight repo consistency pack closed through Gate 131 on `main`"
        in plans
        or "stage-local handoff and terminal-risk seams pack closed through Gate 149 on `main`"
        in plans
        or "active gate: Gate 149 reopened on `work/gate-149-reopen-full-suite-closeout-20260402`"
        in plans
        or "2026-04-01_OPENING_DRIVE_CONTINUATION_LIFECYCLE_PILOT_GATES_v1.md" in plans
        or "2026-04-01_EXECUTION_LEDGER_ALEMBIC_PARITY_CORRECTIVE_GATES_v1.md" in plans
        or "2026-04-01_STAGE_LOCAL_HANDOFF_AND_TERMINAL_RISK_SEAMS_GATES_v1.md" in plans
        or "2026-04-02_STAGE_LOCAL_HANDOFF_CORRECTIVE_SUCCESSOR_GATES_v1.md" in plans
    )
    assert (
        "2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_LEAVES_v1.json" in plans
        or "no active pack currently routed; post-flight repo consistency pack closed through Gate 131 on `main`"
        in plans
        or "stage-local handoff and terminal-risk seams pack closed through Gate 149 on `main`"
        in plans
        or "active gate: Gate 149 reopened on `work/gate-149-reopen-full-suite-closeout-20260402`"
        in plans
        or "2026-04-01_OPENING_DRIVE_CONTINUATION_LIFECYCLE_PILOT_LEAVES_v1.json" in plans
        or "2026-04-01_EXECUTION_LEDGER_ALEMBIC_PARITY_CORRECTIVE_LEAVES_v1.json" in plans
        or "2026-04-01_STAGE_LOCAL_HANDOFF_AND_TERMINAL_RISK_SEAMS_LEAVES_v1.json" in plans
    )
    assert (
        "2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_EXECUTION_LOG_v1.md" in plans
        or "no active pack currently routed; post-flight repo consistency pack closed through Gate 131 on `main`"
        in plans
        or "stage-local handoff and terminal-risk seams pack closed through Gate 149 on `main`"
        in plans
        or "active gate: Gate 149 reopened on `work/gate-149-reopen-full-suite-closeout-20260402`"
        in plans
        or "2026-04-01_OPENING_DRIVE_CONTINUATION_LIFECYCLE_PILOT_EXECUTION_LOG_v1.md" in plans
        or "2026-04-01_EXECUTION_LEDGER_ALEMBIC_PARITY_CORRECTIVE_EXECUTION_LOG_v1.md" in plans
        or "2026-04-01_STAGE_LOCAL_HANDOFF_AND_TERMINAL_RISK_SEAMS_EXECUTION_LOG_v1.md" in plans
    )
    assert any(marker in gate_map for marker in ALLOWED_CURRENT_GATE_MARKERS)
    assert (
        "Status: active signal-coefficient authority pack; Gate 122 active, Gates 123-127 planned"
        in gates
        or "Status: active signal-coefficient authority pack; Gate 122 complete on `main`, Gate 123 active, Gates 124-127 planned"
        in gates
        or "Status: active signal-coefficient authority pack; Gates 122-123 complete on `main`, Gate 124 active, Gates 125-127 planned"
        in gates
        or "Status: active signal-coefficient authority pack; Gates 122-124 complete on `main`, Gate 125 active, Gates 126-127 planned"
        in gates
        or "Status: active signal-coefficient authority pack; Gates 122-125 complete on `main`, Gate 126 active, Gate 127 planned"
        in gates
        or "Status: active signal-coefficient authority pack; Gates 122-126 complete on `main`, Gate 127 active"
        in gates
        or "Status: closed signal-coefficient authority pack on `main`; Gates 122-127 complete, no active gate"
        in gates
    )
    assert leaves["execution_status"] in {
        "gate_121_closed_signal_coefficient_authority_pack_active_from_gate_122",
        "gate_122_complete_gate_123_active_on_main",
        "gate_123_complete_gate_124_active_on_main",
        "gate_124_complete_gate_125_active_on_main",
        "gate_125_complete_gate_126_active_on_main",
        "gate_126_complete_gate_127_active_on_main",
        "signal_coefficient_authority_pack_closed_through_gate_127_on_main",
    }
    assert leaves["active_gate"] in {
        "Gate 122",
        "Gate 123",
        "Gate 124",
        "Gate 125",
        "Gate 126",
        "Gate 127",
        "none — signal-coefficient authority pack closed through Gate 127 on main",
        "Gate 128",
        "Gate 129",
        "Gate 130",
        "Gate 131",
        "none — post-flight repo consistency pack closed through Gate 131 on main",
        "Gate 149",
        "none — stage-local handoff and terminal-risk seams pack closed through Gate 149 on main",
    }
    assert len(leaves["remaining_leaf_ids"]) in {17, 14, 11, 8, 5, 2, 0}
    assert execution_log.startswith("# 2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_EXECUTION_LOG_v1")
    assert "Gate 122-127" in checklist or "Gate 122" in checklist


def test_pack_freezes_tranche_one_scope_and_exclusions() -> None:
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert (
        "raw Asia, Japan, Europe, commodity, crypto, or single-stock precursor coefficients"
        in gates
    )
    assert (
        "timing parameters are separated from behavioural thresholds" in gates
        or "timing parameters" in gates
    )
    assert leaves["global_rules"]["workbook_is_research_authority_not_runtime_authority"] is True
    assert (
        leaves["global_rules"]["starter_bounds_must_be_semantically_bounded_not_search_wide"]
        is True
    )
    assert (
        leaves["global_rules"][
            "asia_precursor_proxies_remain_excluded_from_raw_coefficient_authority"
        ]
        is True
    )
