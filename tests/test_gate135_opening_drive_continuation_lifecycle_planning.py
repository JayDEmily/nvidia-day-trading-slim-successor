"""Gate 135 opening-drive continuation lifecycle planning checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-01_OPENING_DRIVE_CONTINUATION_LIFECYCLE_PILOT_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-01_OPENING_DRIVE_CONTINUATION_LIFECYCLE_PILOT_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-01_OPENING_DRIVE_CONTINUATION_LIFECYCLE_PILOT_EXECUTION_LOG_v1.md"
CHECKLIST = REPO_ROOT / "docs/planning/2026-04-01_OPENING_DRIVE_CONTINUATION_LIFECYCLE_PILOT_DOCUMENT_TOUCH_CHECKLIST_v1.md"

ALLOWED_CURRENT_GATE_MARKERS = {
    "Current active gate: **Gate 135 in the opening-drive continuation lifecycle pilot pack**.",
    "Current active gate: **Gate 136 in the opening-drive continuation lifecycle pilot pack**.",
    "Current active gate: **Gate 137 in the opening-drive continuation lifecycle pilot pack**.",
    "Current active gate: **Gate 138 in the opening-drive continuation lifecycle pilot pack**.",
    "Current active gate: **Gate 139 in the opening-drive continuation lifecycle pilot pack**.",
    "Current active gate: **none — opening-drive continuation lifecycle pilot pack closed through Gate 139 on `main`**.",
    "Current active gate: **Gate 140 in the execution-ledger Alembic parity corrective pack**.",
    "Current active gate: **none — execution-ledger Alembic parity corrective pack closed through Gate 140 on `main`**.",
}


def test_opening_drive_continuation_lifecycle_pack_is_active() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert ("2026-04-01_OPENING_DRIVE_CONTINUATION_LIFECYCLE_PILOT_GATES_v1.md" in plans) or ("2026-04-01_EXECUTION_LEDGER_ALEMBIC_PARITY_CORRECTIVE_GATES_v1.md" in plans)
    assert ("2026-04-01_OPENING_DRIVE_CONTINUATION_LIFECYCLE_PILOT_LEAVES_v1.json" in plans) or ("2026-04-01_EXECUTION_LEDGER_ALEMBIC_PARITY_CORRECTIVE_LEAVES_v1.json" in plans)
    assert ("2026-04-01_OPENING_DRIVE_CONTINUATION_LIFECYCLE_PILOT_EXECUTION_LOG_v1.md" in plans) or ("2026-04-01_EXECUTION_LEDGER_ALEMBIC_PARITY_CORRECTIVE_EXECUTION_LOG_v1.md" in plans)
    assert ("2026-04-01_OPENING_DRIVE_CONTINUATION_LIFECYCLE_PILOT_DOCUMENT_TOUCH_CHECKLIST_v1.md" in plans) or ("2026-04-01_EXECUTION_LEDGER_ALEMBIC_PARITY_CORRECTIVE_DOCUMENT_TOUCH_CHECKLIST_v1.md" in plans)
    assert any(marker in gate_map for marker in ALLOWED_CURRENT_GATE_MARKERS)
    assert (
        "Status: active opening-drive continuation lifecycle pilot pack; Gate 135 active, Gates 136-139 planned" in gates
        or "Status: active opening-drive continuation lifecycle pilot pack; Gate 135 complete on `main`, Gate 136 active, Gates 137-139 planned" in gates
        or "Status: active opening-drive continuation lifecycle pilot pack; Gates 135-136 complete on `main`, Gate 137 active, Gates 138-139 planned" in gates
        or "Status: active opening-drive continuation lifecycle pilot pack; Gates 135-137 complete on `main`, Gate 138 active, Gate 139 planned" in gates
        or "Status: active opening-drive continuation lifecycle pilot pack; Gates 135-138 complete on `main`, Gate 139 active" in gates
        or "Status: closed opening-drive continuation lifecycle pilot pack on `main`; Gates 135-139 complete, no active gate" in gates
    )
    assert leaves["execution_status"] in {
        "gate_134_closed_opening_drive_continuation_lifecycle_pilot_active_from_gate_135",
        "gate_135_complete_gate_136_active_on_main",
        "gate_136_complete_gate_137_active_on_main",
        "gate_137_complete_gate_138_active_on_main",
        "gate_138_complete_gate_139_active_on_main",
        "opening_drive_continuation_lifecycle_pilot_pack_closed_through_gate_139_on_main",
    }
    assert leaves["active_gate"] in {
        "Gate 135",
        "Gate 136",
        "Gate 137",
        "Gate 138",
        "Gate 139",
        "none — opening-drive continuation lifecycle pilot pack closed through Gate 139 on main",
    }
    assert len(leaves["remaining_leaf_ids"]) in {18, 15, 11, 7, 4, 0}
    assert execution_log.startswith("# 2026-04-01 Opening Drive Continuation Lifecycle Pilot Execution Log v1")
    assert "Gate 135" in checklist
    for leaf in leaves["leaves"]:
        for command in leaf["validation_commands"]:
            assert "PYTHONPATH=" not in command
            assert command.startswith(".venv/bin/python -m pytest -q ")


def test_pack_freezes_specimen_scope_and_packet_discipline() -> None:
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert "opening_drive_continuation" in gates
    assert "continuation_ladder_exec" in gates
    assert "This pack is additive by default." in gates
    assert "## Active vocabulary authority for execution threads" in gates
    assert "## Active packet / data contract authority for execution threads" in gates
    assert "bounded tradable expression family" in gates
    assert leaves["global_rules"]["dmp_v2_execution_stage_envelope_must_remain_stable"] is True
    assert leaves["global_rules"]["continuation_lifecycle_pilot_is_single_setup_variant_only"] is True
    assert leaves["global_rules"]["carry_branch_must_consume_lifecycle_output_not_parallel_hidden_logic"] is True
    assert leaves["global_rules"]["bounded_tradable_expression_family_must_be_frozen_before_lifecycle_behaviour_broadens"] is True
    assert leaves["global_rules"]["leaf_validation_commands_require_repo_local_installed_env"] is True
