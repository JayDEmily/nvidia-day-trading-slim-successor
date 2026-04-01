"""Gate 147 overlay-evaluation versus terminal-risk-application planning checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RECEIPT = REPO_ROOT / "docs/planning/2026-04-01_GATE147_OVERLAY_EVALUATION_AND_TERMINAL_RISK_APPLICATION.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-01_STAGE_LOCAL_HANDOFF_AND_TERMINAL_RISK_SEAMS_LEAVES_v1.json"
DOMAIN_MODEL = REPO_ROOT / "docs/03_DOMAIN_MODEL.md"
VOCAB_PATH = REPO_ROOT / "docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json"


def test_gate147_receipt_domain_model_and_vocabulary_are_present() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")
    domain_model = DOMAIN_MODEL.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    vocab = json.loads(VOCAB_PATH.read_text(encoding="utf-8"))
    slugs = {entry["canonical_slug"] for entry in vocab["entries"]}

    assert "overlay_risk_decision" in receipt
    assert "terminal_risk_application" in receipt
    assert "#### Gate 147 note: overlay evaluation versus terminal-risk application" in domain_model
    assert {"overlay_risk_decision", "terminal_risk_application"}.issubset(slugs)
    assert leaves["active_gate"] in {"Gate 147", "Gate 148", "Gate 149"}
