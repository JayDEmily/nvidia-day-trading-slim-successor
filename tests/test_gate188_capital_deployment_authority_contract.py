"""Gate 188 capital-deployment authority contract checks."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from nvda_desk.schemas.cognition import (
    CapitalDeploymentAuthorityAction,
    CapitalDeploymentAuthorityDecision,
    CapitalDeploymentAuthorityInput,
)

REPO_ROOT = Path(__file__).resolve().parents[1]

VOCAB = REPO_ROOT / "docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json"
DOMAIN_MODEL = REPO_ROOT / "docs/03_DOMAIN_MODEL.md"
ARCHITECTURE = REPO_ROOT / "docs/04_TECHNICAL_ARCHITECTURE.md"
RECEIPT = REPO_ROOT / "docs/planning/2026-04-03_GATE188_CAPITAL_DEPLOYMENT_AUTHORITY_CONTRACT.md"

def _entries() -> dict[str, dict[str, object]]:
    payload = json.loads(VOCAB.read_text(encoding="utf-8"))
    return {entry["canonical_slug"]: entry for entry in payload["entries"]}

def test_gate188_vocabulary_admits_bounded_service_and_decision() -> None:
    entries = _entries()
    service = cast(dict[str, Any], entries["capital_deployment_authority_service"])
    decision = cast(dict[str, Any], entries["capital_deployment_authority_decision"])

    assert service["canonical_label"] == "Capital Deployment Authority Service"
    assert service["maps_to_contract"] == (
        "nvda_desk.services.capital_deployment_authority.CapitalDeploymentAuthorityService"
    )
    assert "capital deployment authority" in service["allowed_aliases"]
    assert "not a full arbiter" in service["notes"][0].lower()

    assert decision["canonical_label"] == "Capital Deployment Authority Decision"
    assert decision["maps_to_contract"] == "nvda_desk.schemas.cognition.CapitalDeploymentAuthorityDecision"
    assert "deploy-versus-stand-down" in decision["notes"][0]

def test_gate188_contract_freezes_minimum_inputs_and_outputs() -> None:
    input_fields = CapitalDeploymentAuthorityInput.model_fields
    output_fields = CapitalDeploymentAuthorityDecision.model_fields

    assert CapitalDeploymentAuthorityAction.DEPLOY.value == "deploy"
    assert CapitalDeploymentAuthorityAction.STAND_DOWN.value == "stand_down"

    assert "posture" in input_fields
    assert "eligibility" in input_fields
    assert "execution" in input_fields
    assert "stage_local_handoff" in input_fields
    assert "parallel_risk_lane_packet" in input_fields
    assert "capital_state" in input_fields

    assert output_fields["decision_version"].default == "capital_deployment_authority.v1"
    assert output_fields["service_id"].default == "capital_deployment_authority_service"
    assert "deployment_action" in output_fields
    assert "authorised_deployable_pct" in output_fields
    assert "authorised_notional_usd" in output_fields
    assert "available_buying_power_usd" in output_fields
    assert "terminal_risk_action" in output_fields
    assert "rationale_codes" in output_fields

def test_gate188_docs_and_receipt_freeze_bounded_scope() -> None:
    domain = DOMAIN_MODEL.read_text(encoding="utf-8")
    architecture = ARCHITECTURE.read_text(encoding="utf-8")
    receipt = RECEIPT.read_text(encoding="utf-8")

    assert "CapitalDeploymentAuthorityInput" in domain
    assert "CapitalDeploymentAuthorityDecision" in domain
    assert "does **not** add recommendation memory, close-position logic, or a full portfolio arbiter" in domain
    assert "capital-deployment authority may be evaluated from the already-formed opening candidate plus current capital snapshot" in architecture
    assert "review consumes the bounded capital-deployment authority decision additively" in architecture
    assert "new-opening capital authorisation only" in receipt
    assert "Vocabulary admission landed before code used the term." in receipt
