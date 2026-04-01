"""Gate 144 posture split planning and vocabulary checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RECEIPT = REPO_ROOT / "docs/planning/2026-04-01_GATE144_POSTURE_HARD_INVARIANTS_AND_LOCAL_ENVELOPE.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-01_STAGE_LOCAL_HANDOFF_AND_TERMINAL_RISK_SEAMS_LEAVES_v1.json"
DOMAIN_MODEL = REPO_ROOT / "docs/03_DOMAIN_MODEL.md"
VOCAB_PATH = REPO_ROOT / "docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json"


def test_gate144_receipt_domain_model_and_vocabulary_are_present() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")
    domain_model = DOMAIN_MODEL.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    vocab = json.loads(VOCAB_PATH.read_text(encoding="utf-8"))
    slugs = {entry["canonical_slug"] for entry in vocab["entries"]}

    assert "## Admitted governed vocabulary" in receipt
    assert "posture_hard_invariants" in receipt
    assert "posture_local_envelope" in receipt
    assert "posture_downstream_annotations" in receipt
    assert "#### Gate 144 note: posture-owned hard invariants and local envelope" in domain_model
    assert {"posture_hard_invariants", "posture_local_envelope", "posture_downstream_annotations"}.issubset(slugs)
    assert leaves["active_gate"] in {"Gate 145", "Gate 146"}
    assert "Gate 144" in leaves["completed_gate_ids"]
    assert {"LEAF-G144-001", "LEAF-G144-002"}.issubset(set(leaves["completed_leaf_ids"]))
