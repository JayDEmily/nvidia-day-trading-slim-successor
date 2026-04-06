"""Gate 146 admissibility-versus-candidate-ownership planning checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RECEIPT = REPO_ROOT / "docs/planning/2026-04-01_GATE146_ELIGIBILITY_ADMISSIBILITY_AND_EXECUTION_CANDIDATE_OWNERSHIP.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-01_STAGE_LOCAL_HANDOFF_AND_TERMINAL_RISK_SEAMS_LEAVES_v1.json"
DOMAIN_MODEL = REPO_ROOT / "docs/03_DOMAIN_MODEL.md"
VOCAB_PATH = REPO_ROOT / "docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json"


def test_gate146_receipt_domain_model_and_vocabulary_are_present() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")
    domain_model = DOMAIN_MODEL.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    vocab = json.loads(VOCAB_PATH.read_text(encoding="utf-8"))
    slugs = {entry["canonical_slug"] for entry in vocab["entries"]}

    assert "eligibility_admissibility" in receipt
    assert "execution_candidate_ownership" in receipt
    assert "#### Gate 146 note: eligibility admissibility versus execution candidate ownership" in domain_model
    assert {"eligibility_admissibility", "execution_candidate_ownership"}.issubset(slugs)
    assert leaves["active_gate"] in {"Gate 146", "Gate 147", "Gate 148", "Gate 149", "none — stage-local handoff and terminal-risk seams pack closed through Gate 149 on main"}
