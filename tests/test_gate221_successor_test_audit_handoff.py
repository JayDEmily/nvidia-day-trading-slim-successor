"""Gate 221 successor handoff and bounded-proof checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
HANDOFF = REPO_ROOT / "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_TEST_AUDIT_PROOF_SLICE_AND_SUCCESSOR_HANDOFF_v1.md"
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_EXECUTION_LOG_v1.md"

ACTIVE_BRANCH = "work/gate-221-successor-proof-slice-and-handoff-20260406"
PROOF_COMMAND = (
    "/home/jds/dev/nvidia-day-trading/target_repo_gate201_evidence_inventory_and_provenance_planning_main_fullgit_2026-04-05/"
    ".venv/bin/python -m pytest -q tests/test_gate221_successor_test_audit_handoff.py "
    "tests/test_planning_state_integrity.py"
)


def test_gate221_leaf1_freezes_bounded_successor_execution_proof_slice() -> None:
    document = HANDOFF.read_text(encoding="utf-8")

    assert "Status: closed-pack proof-order, successor execution-queue, and handoff surface" in document
    assert "## Ordered proof slice for the first successor execution pack after bootstrap closeout" in document
    assert "## Broad proof explicitly excluded from the first execution pack" in document
    assert "## Stop conditions that force replanning before or during execution" in document
    assert "## Deterministic next execution-pack boundary" in document
    assert "## Non-source-repo boundary" in document

    assert "pytest -q tests/test_gate221_successor_test_audit_handoff.py tests/test_planning_state_integrity.py" in document
    assert "Execute exactly one grouped execution family from the queued Gate 220 decision register." in document
    assert "Re-run `pytest -q tests/test_gate221_successor_test_audit_handoff.py tests/test_planning_state_integrity.py`" in document

    assert "broad repo-wide `make check` by default" in document
    assert "full runtime pytest across unrelated modules" in document
    assert "executing more than one grouped execution family in the same first post-bootstrap pack" in document

    assert "the chosen execution family cannot be stated without guessing which Gate 220 decision rows it owns" in document
    assert "the work would require source-repo mutation or source-repo rerouting" in document
    assert "the targeted successor-repo proof slice expands into broad blind execution" in document

    assert "The next pack after this bootstrap is the **first successor retained-test execution pack**." in document
    assert "must be created or routed later as a new pack rather than inferred from this bootstrap closeout alone" in document
    assert "must remain inside the successor repo" in document
    assert "treat the source repo as the destination for archive-evidence moves" in document
    assert "claim that any keep / retire / rewrite / move action has already executed" in document


def test_gate221_queue_and_closeout_leave_no_active_pack_routed() -> None:
    document = HANDOFF.read_text(encoding="utf-8")
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    payload = json.loads(LEAVES.read_text(encoding="utf-8"))
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")

    assert "## Grouped successor execution-pack queue from the Gate 220 decision register" in document
    assert "### 1. Archive-evidence move family" in document
    assert "### 2. Successor-boundary rewrite family" in document
    assert "### 3. Duplicate-retirement family" in document
    assert "### 4. Retained keep and retarget family" in document
    assert "`planning_governance__closed_source_or_historical_pack_receipts`" in document
    assert "`review_or_trace__historical_planning_review_receipts`" in document
    assert "`migration_or_closeout_guard__historical_closeout_receipts`" in document
    assert "`migration_or_closeout_guard__successor_cutover_boundary_rule`" in document
    assert "`replay_regression__research_shadow_replays`" in document
    assert "`compatibility_wrapper__preserved_reader_shapes`" in document
    assert "`runtime_contract__current_packet_and_service_contracts`" in document
    assert "## Router-closeout result" in document
    assert "This bootstrap pack closes through Gate 221 with **no active pack currently routed**." in document
    assert "must create or route the appropriate new successor execution pack before any queued family above may execute" in document

    assert "- no active pack currently routed" in plans
    assert (
        "- latest closed pack retained as evidence is the slim active-repo cutover and substantive "
        f"test-audit bootstrap pack closed through Gate 221 on `{ACTIVE_BRANCH}`"
    ) in plans

    assert "Version: v1.34" in gate_map
    assert (
        "Current active gate: **none — the slim active-repo cutover and substantive test-audit "
        f"bootstrap pack is closed through Gate 221 on `{ACTIVE_BRANCH}`, and no active pack is currently routed.**"
    ) in gate_map
    assert f"Gate 221 | complete on `{ACTIVE_BRANCH}`" in gate_map

    assert (
        "Status: closed slim-successor planning pack through Gate 221 on "
        f"`{ACTIVE_BRANCH}`; no active pack is currently routed."
    ) in gates

    assert payload["execution_status"] == "bootstrap_pack_closed_through_gate_221_no_active_pack_routed"
    assert payload["active_gate"] == "none"
    assert payload["completed_gate_ids"] == ["Gate 217", "Gate 218", "Gate 219", "Gate 220", "Gate 221"]
    assert {"LEAF-G221-001", "LEAF-G221-002"} <= set(payload["completed_leaf_ids"])
    assert payload["remaining_leaf_ids"] == []
    assert payload["pending_gate_ids"] == []

    assert (
        "Status: successor execution log for slim active-repo cutover and substantive test-audit "
        f"bootstrap; closed through Gate 221 on `{ACTIVE_BRANCH}`; no active pack is currently routed."
    ) in execution_log
    assert "### LEAF-G221-001" in execution_log
    assert "### LEAF-G221-002" in execution_log
    assert PROOF_COMMAND in execution_log
    assert (
        "repo-local successor environment still unavailable because "
        "/home/jds/dev/nvidia-day-trading-slim-successor/.venv/bin/python does not exist; "
        "Gate 221 proof reused the already-provisioned source-repo interpreter intentionally"
    ) in execution_log
    assert f"Gate 221 is complete on `{ACTIVE_BRANCH}`." in execution_log
    assert "No active pack is currently routed." in execution_log
