from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from nvda_desk.api.app import app
from nvda_desk.api.deps import (
    get_module_registry_service,
    get_promotion_service,
)
from nvda_desk.db import create_engine_from_url, create_schema, seed_dev_data
from nvda_desk.db.session import create_session_factory
from nvda_desk.services.module_registry import ModuleRegistryService
from nvda_desk.services.promotion import PromotionService


class RegistryBundle:
    def __init__(self, tmp_path: Path):
        database_url = f"sqlite+pysqlite:///{tmp_path / 'registry_bundle.db'}"
        create_schema(database_url)
        engine = create_engine_from_url(database_url)
        with Session(engine) as session:
            seed_dev_data(session)
        session_factory = create_session_factory(database_url)
        self.registry = ModuleRegistryService(session_factory)
        self.promotion = PromotionService(session_factory)


def _client_with_services(bundle: RegistryBundle) -> Iterator[TestClient]:
    app.dependency_overrides[get_module_registry_service] = lambda: bundle.registry
    app.dependency_overrides[get_promotion_service] = lambda: bundle.promotion
    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.clear()


def test_module_spec_roundtrip(tmp_path: Path) -> None:
    bundle = RegistryBundle(tmp_path)
    for client in _client_with_services(bundle):
        create_response = client.post(
            "/modules/specs",
            json={
                "descriptor": {
                    "module_id": "slv-v1",
                    "name": "Strategic Ladder Validator",
                    "module_class": "signal",
                    "status": "draft",
                    "thesis": "Validate ladder levels against option pressure and session state.",
                },
                "required_inputs": [
                    "spot_price",
                    "distance_to_vwap_pct",
                    "session_phase",
                ],
                "parameters": {"min_fill_plausibility_score": 0.7},
                "notes_md": "Initial formalised draft from legacy extraction.",
                "source_refs": ["legacy/T1DESK_VALUE_CAPTURE.md"],
            },
        )
        list_response = client.get("/modules/specs")
    assert create_response.status_code == 200
    created = create_response.json()
    assert created["descriptor"]["module_id"] == "slv-v1"
    assert created["required_inputs"] == [
        "spot_price",
        "distance_to_vwap_pct",
        "session_phase",
    ]
    assert list_response.status_code == 200
    listed = list_response.json()["specs"]
    assert len(listed) == 1
    assert listed[0]["spec_id"] == created["spec_id"]


def test_promotion_decision_roundtrip(tmp_path: Path) -> None:
    bundle = RegistryBundle(tmp_path)
    for client in _client_with_services(bundle):
        create_response = client.post(
            "/modules/promotions",
            json={
                "module_id": "slv-v1",
                "from_status": "coded",
                "to_status": "backtested",
                "decision_reason": "Passed deterministic evaluator and initial replay checks.",
                "evaluation_ids": [1, 2],
                "evidence_refs": ["docs/planning/SLV_PROMOTION_PLAN.md"],
                "approved_by": "operator",
            },
        )
        list_response = client.get("/modules/promotions", params={"module_id": "slv-v1"})
    assert create_response.status_code == 200
    created = create_response.json()
    assert created["module_id"] == "slv-v1"
    assert created["to_status"] == "backtested"
    assert list_response.status_code == 200
    listed = list_response.json()["decisions"]
    assert len(listed) == 1
    assert listed[0]["decision_id"] == created["decision_id"]
