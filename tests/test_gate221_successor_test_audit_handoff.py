"""Gate 221 successor handoff and bounded-proof checks."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
HANDOFF = REPO_ROOT / "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_TEST_AUDIT_PROOF_SLICE_AND_SUCCESSOR_HANDOFF_v1.md"


def test_gate221_leaf1_freezes_bounded_successor_execution_proof_slice() -> None:
    document = HANDOFF.read_text(encoding="utf-8")

    assert "Status: Gate 221 proof-order and successor-handoff surface" in document
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
