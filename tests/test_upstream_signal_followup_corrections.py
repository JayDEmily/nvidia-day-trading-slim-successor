"""Targeted follow-up corrections for the upstream signal tranche closeout."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
PROCESS_LAW = REPO_ROOT / "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md"
TESTING = REPO_ROOT / "docs/08_TESTING_AND_PROMOTION.md"


def test_followup_checkpoint_integrity_regime_is_repo_authority() -> None:
    """Checkpoint integrity must live inside repo authority and the execution read stack."""

    testing = TESTING.read_text(encoding="utf-8")
    plans = PLANS.read_text(encoding="utf-8")
    process_law = PROCESS_LAW.read_text(encoding="utf-8")

    assert "## Checkpoint Integrity Gate" in testing
    assert "This rule is forward-only." in testing
    assert "### Runtime checkpoint requirements" in testing
    assert "### Observability requirements" in testing
    assert "### Negative proof requirement" in testing
    assert "### Docstring requirements" in testing
    assert "No test is trusted unless it can prove failure" in testing
    assert "docs/08_TESTING_AND_PROMOTION.md" in plans
    assert "docs/08_TESTING_AND_PROMOTION.md" in process_law
    assert (
        "runtime checkpoints, observable checkpoint truth, negative proof, and structured docstrings are mandatory forward-only."
        in process_law
    )
