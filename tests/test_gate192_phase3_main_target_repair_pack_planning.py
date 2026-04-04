"""Planning-pack checks for the Phase 3 main-target repair programme."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_EXECUTION_LOG_v1.md"
CHECKLIST = REPO_ROOT / "docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_DOCUMENT_TOUCH_CHECKLIST_v1.md"
SCOPE_NOTE = REPO_ROOT / "docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_SCOPE_NOTE_v1.md"
EVIDENCE_BASELINE = REPO_ROOT / "docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_EVIDENCE_BASELINE_v1.md"
SOURCE_TRUTH = REPO_ROOT / "docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_SOURCE_TRUTH_MATRIX_v1.md"
RECEIPT = REPO_ROOT / "docs/planning/2026-04-04_GATE192_PHASE3_MAIN_TARGET_REPAIR_PACK_BOOTSTRAP.md"


def test_gate192_pack_surfaces_are_coherent() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    scope_note = SCOPE_NOTE.read_text(encoding="utf-8")
    baseline = EVIDENCE_BASELINE.read_text(encoding="utf-8")
    source_truth = SOURCE_TRUTH.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert "docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_GATES_v1.md" in plans
    assert "docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_LEAVES_v1.json" in plans
    assert "docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_EXECUTION_LOG_v1.md" in plans
    assert "docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_DOCUMENT_TOUCH_CHECKLIST_v1.md" in plans
    assert "docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_SCOPE_NOTE_v1.md" in plans
    assert "docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_EVIDENCE_BASELINE_v1.md" in plans
    assert "docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_SOURCE_TRUTH_MATRIX_v1.md" in plans
    assert any(marker in plans for marker in ["- next active gate: `Gate 193`", "- next active gate: `Gate 194`", "- next active gate: `Gate 195`", "- next active gate: `Gate 196`", "- next active gate: `Gate 197`", "- next active gate: `Gate 198`", "- next active gate: `Gate 199`"])

    assert any(marker in gate_map for marker in [
        "Current active gate: **Gate 193 in the Phase 3 main-target repair programme on `work/gate-192-phase3-main-target-repair-pack-20260404`**.",
        "Current active gate: **Gate 194 in the Phase 3 main-target repair programme on `work/gate-193-vocabulary-generator-truth-20260404`**.",
        "Current active gate: **Gate 195 in the Phase 3 main-target repair programme on `work/gate-194-vocabulary-hygiene-reconciliation-20260404`**.",
        "Current active gate: **Gate 196 in the Phase 3 main-target repair programme on `work/gate-195-control-surface-router-gate-map-reconciliation-20260404`**.",
        "Current active gate: **Gate 197 in the Phase 3 main-target repair programme on `work/gate-196-runtime-semantic-drift-reconciliation-20260404`**.",
        "Current active gate: **none — Phase 3 main-target repair programme closed through Gate 199 on `main`**.",
    ])
    assert any(status in gates for status in [
        "Status: active Phase 3 main-target repair planning pack; Gate 192 complete on `work/gate-192-phase3-main-target-repair-pack-20260404`, Gate 193 active, Gates 194-199 planned",
        "Status: active Phase 3 main-target repair planning pack; Gates 192-193 complete on `work/gate-193-vocabulary-generator-truth-20260404`, Gate 194 active, Gates 195-199 planned",
        "Status: active Phase 3 main-target repair planning pack; Gates 192-194 complete on `work/gate-194-vocabulary-hygiene-reconciliation-20260404`, Gate 195 active, Gates 196-199 planned",
        "Status: active Phase 3 main-target repair planning pack; Gates 192-195 complete on `work/gate-195-control-surface-router-gate-map-reconciliation-20260404`, Gate 196 active, Gates 197-199 planned",
        "Status: active Phase 3 main-target repair planning pack; Gates 192-196 complete on `work/gate-196-runtime-semantic-drift-reconciliation-20260404`, Gate 197 active, Gates 198-199 planned",
        "Status: closed Phase 3 main-target repair programme through Gate 199 on `main`",
    ])
    assert leaves["execution_status"] in {
        "gate_192_complete_gate_193_active_on_work_branch",
        "gates_192_193_complete_gate_194_active_on_work_branch",
        "gates_192_194_complete_gate_195_active_on_work_branch",
        "gates_192_195_complete_gate_196_active_on_work_branch",
        "gates_192_196_complete_gate_197_active_on_work_branch",
        "phase3_main_target_repair_programme_closed_through_gate_199_on_main",
    }
    assert leaves["active_gate"] in {"Gate 193", "Gate 194", "Gate 195", "Gate 196", "Gate 197", "Gate 198", "Gate 199", "none"}
    assert set(leaves["completed_leaf_ids"]).isdisjoint(leaves["remaining_leaf_ids"])
    assert execution_log.startswith("# 2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_EXECUTION_LOG_v1")
    assert "Gate 193" in checklist
    assert "scripts/build_canonical_vocabulary.py" in baseline
    assert "scripts/build_canonical_vocabulary.py" in scope_note
    assert "tests treated as evidence rather than authority" in scope_note
    assert "source-truth-first" in source_truth
    assert "CapitalDeploymentAuthorityDecision" in source_truth
    assert "Do not mix runtime-semantic repair with broad static cleanup in the same gate." in scope_note


def test_gate192_future_gate_structure_is_granular_and_keyed() -> None:
    payload = json.loads(LEAVES.read_text(encoding="utf-8"))
    leaves = payload["leaves"]
    assert isinstance(leaves, dict)

    counts: dict[str, int] = {}
    for item in leaves.values():
        counts.setdefault(item["gate"], 0)
        counts[item["gate"]] += 1

    assert counts["Gate 192"] == 4
    assert counts["Gate 193"] == 4
    assert counts["Gate 194"] == 4
    assert counts["Gate 195"] == 5
    assert counts["Gate 196"] == 6
    assert counts["Gate 197"] == 4
    assert counts["Gate 198"] == 4
    assert counts["Gate 199"] == 6
    assert len(set(counts.values())) > 1
    assert payload["global_rules"]["source_truth_precedes_test_truth"] is True

    future_gates = {"Gate 193", "Gate 194", "Gate 195", "Gate 196", "Gate 197", "Gate 198", "Gate 199"}
    future_leaves = [item for item in leaves.values() if item["gate"] in future_gates]
    for item in future_leaves:
        assert len(item["ordered_actions"]) >= 3
        assert len(item["forbidden_actions"]) >= 3
        assert item["validation_commands"]
        assert item["expected_evidence"]
        assert item["definition_of_done"]
        assert item["packaging_requirement"]
        assert item["document_touch_surfaces"]
        assert "docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_SOURCE_TRUTH_MATRIX_v1.md" in item["authority_docs"]

    expected_first_leaves = {
        "Gate 193": "Inspect the vocabulary source-truth seam before trusting downstream tests",
        "Gate 194": "Inspect runtime and vocabulary source truth for residual ambient leakage",
        "Gate 195": "Inspect router and gate-map source truth before trusting closeout tests",
        "Gate 196": "Inspect options-flow source truth before trusting harness expectations",
        "Gate 197": "Inspect the financial-calendar source seam before trusting mypy output",
        "Gate 198": "Inspect helper source truth before trusting strict test failures",
        "Gate 199": "Inspect raw static surfaces before trusting lint output",
    }
    for gate, title in expected_first_leaves.items():
        leaf = next(item for item in leaves.values() if item["gate"] == gate and item["title"] == title)
        assert leaf["repo_surfaces"][0].startswith(("src/", "scripts/", "docs/", "PLANS", "alembic/", "tests/contract_chain_fixtures.py", "tests/_successor_pack_helpers.py"))
        assert not leaf["repo_surfaces"][0].startswith("tests/test_")
        assert "authority" in leaf["objective"].lower() or "source" in leaf["title"].lower()



def test_gate192_receipt_scope_and_execution_log_preserve_planning_truth() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")
    scope_note = SCOPE_NOTE.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")

    assert "it did not edit runtime behaviour under `src/`" in receipt
    assert "Follow-on source-truth hardening pass" in receipt
    assert "it did not start any Phase 3 repair gate" in receipt
    assert "Gate 193 — vocabulary generator and artifact truth reconciliation" in receipt
    assert "side-repo B/C blockers remain outside first-line main-target repair scope" in receipt
    assert "runtime semantics, router/control truth, vocabulary truth, typing seams, helper typing, and static hygiene remain separate" in receipt
    assert 'Do not let vocabulary or router truth drift be “fixed” implicitly by editing downstream tests only.' in scope_note
    assert "Gate 192 complete on `work/gate-192-phase3-main-target-repair-pack-20260404`; Gate 193 active" in execution_log
    assert "Source-truth hardening pass" in execution_log
