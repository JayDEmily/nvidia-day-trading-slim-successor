"""Planning-pack checks for the target-repo admitted-evidence successor pack."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_EXECUTION_LOG_v1.md"
CHECKLIST = REPO_ROOT / "docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_DOCUMENT_TOUCH_CHECKLIST_v1.md"
SCOPE_NOTE = REPO_ROOT / "docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_SCOPE_NOTE_v1.md"
CONTRADICTION = REPO_ROOT / "docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_CONTRADICTION_REPORT_v1.md"
SALVAGE = REPO_ROOT / "docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_SALVAGE_MATRIX_v1.md"


def test_gate200_pack_surfaces_are_coherent() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    scope_note = SCOPE_NOTE.read_text(encoding="utf-8")
    contradiction = CONTRADICTION.read_text(encoding="utf-8")
    salvage = SALVAGE.read_text(encoding="utf-8")
    payload = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert "docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_GATES_v1.md" in plans
    assert "docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_LEAVES_v1.json" in plans
    assert "docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_EXECUTION_LOG_v1.md" in plans
    assert "docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_DOCUMENT_TOUCH_CHECKLIST_v1.md" in plans
    assert "docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_SCOPE_NOTE_v1.md" in plans
    assert "docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_CONTRADICTION_REPORT_v1.md" in plans
    assert "docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_SALVAGE_MATRIX_v1.md" in plans
    assert any(marker in plans for marker in ["- next active gate: `Gate 200`", "- next active gate: `Gate 201`", "- next active gate: `Gate 202`", "- next active gate: `Gate 203`"])

    assert any(marker in gate_map for marker in [
        "Current active gate: **Gate 200 in the target-repo admitted-evidence successor planning pack on `work/gate-200-target-repo-admitted-evidence-successor-pack-20260405`**.",
        "Current active gate: **Gate 201 in the target-repo admitted-evidence successor planning pack on `work/gate-200-target-repo-admitted-evidence-successor-pack-20260405`**.",
        "Current active gate: **Gate 201 in the target-repo admitted-evidence successor planning pack on `main`**.",
        "Current active gate: **Gate 202 in the target-repo admitted-evidence successor planning pack on `main`**.",
        "Current active gate: **Gate 203 in the target-repo admitted-evidence successor planning pack on `main`**.",
    ])
    assert "Current active gate: **none — Phase 3 main-target repair programme closed through Gate 199 on `main`**." in gate_map
    assert "Gate 199 | complete on `main`" in gate_map
    assert any(marker in gate_map for marker in ["Gate 200 | active", "Gate 200 | complete"])
    assert any(marker in gate_map for marker in ["Gate 201 | active", "Gate 201 | planned", "Gate 201 | complete"])
    assert any(marker in gate_map for marker in ["Gate 202 | active", "Gate 202 | planned", "Gate 202 | complete"])
    assert any(marker in gate_map for marker in ["Gate 203 | active", "Gate 203 | planned"])
    assert "Gate 205 | planned" in gate_map

    assert any(status in gates for status in [
        "Status: active target-repo admitted-evidence successor planning pack; Gate 200 active",
        "Status: active target-repo admitted-evidence successor planning pack; Gate 200 complete on `work/gate-200-target-repo-admitted-evidence-successor-pack-20260405`, Gate 201 active, Gates 202-205 planned.",
        "Status: active target-repo admitted-evidence successor planning pack; Gates 200-201 complete on `main`, Gate 202 active, Gates 203-205 planned.",
        "Status: active target-repo admitted-evidence successor planning pack; Gates 200-202 complete on `main`, Gate 203 active, Gates 204-205 planned.",
    ])
    assert payload["execution_status"] in {"gate_200_active_on_work_branch", "gate_200_complete_gate_201_active_on_work_branch", "gates_200_201_complete_gate_202_active_on_main", "gates_200_202_complete_gate_203_active_on_main"}
    assert payload["active_gate"] in {"Gate 200", "Gate 201", "Gate 202", "Gate 203"}
    assert payload["completed_gate_ids"] in [[], ["Gate 200"], ["Gate 200", "Gate 201"], ["Gate 200", "Gate 201", "Gate 202"]]
    assert payload["pending_gate_ids"] in [["Gate 200", "Gate 201", "Gate 202", "Gate 203", "Gate 204", "Gate 205"], ["Gate 201", "Gate 202", "Gate 203", "Gate 204", "Gate 205"], ["Gate 202", "Gate 203", "Gate 204", "Gate 205"], ["Gate 203", "Gate 204", "Gate 205"]]
    assert set(payload["completed_leaf_ids"]).isdisjoint(payload["remaining_leaf_ids"])

    assert execution_log.startswith("# 2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_EXECUTION_LOG_v1")
    assert "Starter receipt" in execution_log
    assert any(marker in execution_log for marker in ["Gate 200 remains the active gate", "Gate 200 is complete, and Gate 201 is now the active gate in this pack.", "Gate 202 is now the active gate in this pack.", "Gate 203 is now the active gate in this pack."])
    assert "target-repo admitted-evidence successor planning pack" in checklist
    assert "Gate 212" in contradiction
    assert "evidence only" in salvage
    assert "Gate 212 is not salvageable" in salvage
    assert "may not do" in scope_note
    assert "Gate 212" in scope_note


def test_gate200_future_gate_structure_is_granular() -> None:
    payload = json.loads(LEAVES.read_text(encoding="utf-8"))
    leaves = payload["leaves"]
    assert isinstance(leaves, dict)

    counts: dict[str, int] = {}
    for item in leaves.values():
        counts.setdefault(item["gate"], 0)
        counts[item["gate"]] += 1

    assert counts["Gate 200"] == 4
    assert counts["Gate 201"] == 4
    assert counts["Gate 202"] == 4
    assert counts["Gate 203"] == 3
    assert counts["Gate 204"] == 3
    assert counts["Gate 205"] == 3
    assert len(set(counts.values())) > 1

    assert payload["global_rules"]["source_truth_precedes_test_truth"] is True
    assert payload["global_rules"]["latest_closed_pack_is_evidence_not_template"] is True
    assert payload["global_rules"]["material_control_surface_contradictions_require_contradiction_report"] is True
    assert payload["contradiction_scan"]["current_result"] == "material_conflicts_resolved_into_target_repo_successor_pack"

    for item in leaves.values():
        assert len(item["ordered_actions"]) >= 3
        assert len(item["forbidden_actions"]) >= 3
        assert item["validation_commands"]
        assert item["expected_evidence"]
        assert item["definition_of_done"]
        assert item["packaging_requirement"]
        assert item["document_touch_surfaces"]

    titles = {item["title"] for item in leaves.values()}
    assert "Emit contradiction report and salvage matrix" in titles
    assert "Plan target-snapshot handoff brief and input-bundle contract" in titles
    assert "Identify first DMP packet failure-pack families against repo-native stage links" in titles
