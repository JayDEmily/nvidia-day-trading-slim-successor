"""Gate 105 typed ingress and DB/API seam checks."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sqlalchemy import text

from nvda_desk.api.app import app
from nvda_desk.api.deps import get_config_surface_service
from nvda_desk.config_models import RuntimeSettingsDocument
from nvda_desk.db.session import create_session_factory
from nvda_desk.schemas.dataset import RealDataBundle
from nvda_desk.services.config_surface import ConfigSurfaceLookupError, ConfigSurfaceService

RAW_BUNDLE_PATH = Path("fixtures/real_data/gate_101_canonical_raw_runtime_bundle.json")
GATE105_DOC = Path("docs/planning/2026-03-30_GATE105_INGRESS_DB_API.md")


class _ConfigSurfaceRuntimeStub:
    def __init__(self, payload: RuntimeSettingsDocument) -> None:
        self._payload = payload

    def runtime_settings(self) -> RuntimeSettingsDocument:
        return self._payload


class _ConfigSurfaceMissingGroupStub:
    def get_coefficient_group(self, group_key: str) -> object:
        raise ConfigSurfaceLookupError(f"missing group: {group_key}")



def test_gate105_real_data_bundle_allows_documented_coercion_but_strict_mode_rejects_it() -> None:
    raw = json.loads(RAW_BUNDLE_PATH.read_text(encoding="utf-8"))
    raw["bars"][0]["volume"] = "12345.0"

    coerced = RealDataBundle.model_validate(raw)
    assert coerced.bars[0].volume == 12345.0

    with pytest.raises(ValidationError):
        RealDataBundle.model_validate(raw, strict=True)



def test_gate105_real_data_bundle_rejects_prohibited_ingress_shapes() -> None:
    raw = json.loads(RAW_BUNDLE_PATH.read_text(encoding="utf-8"))
    raw["bars"][0]["rogue_field"] = "nope"

    with pytest.raises(ValidationError):
        RealDataBundle.model_validate(raw)



def test_gate105_sqlalchemy_session_factory_commits_and_rolls_back_cleanly(tmp_path: Path) -> None:
    database_url = f"sqlite+pysqlite:///{tmp_path / 'gate105.db'}"
    session_factory = create_session_factory(database_url)

    with session_factory.begin() as session:
        session.execute(text("create table receipts (id integer primary key, note text not null)"))
        session.execute(text("insert into receipts (note) values ('persisted')"))

    with session_factory() as session:
        count = session.execute(text("select count(*) from receipts")).scalar_one()
        assert count == 1

    with pytest.raises(RuntimeError), session_factory.begin() as session:
        session.execute(text("insert into receipts (note) values ('rolled_back')"))
        raise RuntimeError("force rollback")

    with session_factory() as session:
        notes = session.execute(text("select note from receipts order by id")).scalars().all()
        assert notes == ["persisted"]



def test_gate105_fastapi_dependency_override_allows_bounded_runtime_settings_probe() -> None:
    expected = ConfigSurfaceService(Path("config")).runtime_settings()
    app.dependency_overrides[get_config_surface_service] = lambda: _ConfigSurfaceRuntimeStub(expected)
    try:
        with TestClient(app) as client:
            response = client.get("/config/runtime-settings")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == expected.model_dump(mode="json")



def test_gate105_fastapi_dependency_override_freezes_lookup_error_mapping() -> None:
    app.dependency_overrides[get_config_surface_service] = lambda: _ConfigSurfaceMissingGroupStub()
    try:
        with TestClient(app) as client:
            response = client.get("/config/coefficients/missing-surface")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404
    assert response.json() == {"detail": "missing group: missing-surface"}



def test_gate105_doc_freezes_remaining_scope() -> None:
    doc = GATE105_DOC.read_text(encoding="utf-8")

    assert "Status: Gate 105 complete on `main`; Gate 106 is the next active gate in the successor testing pack" in doc
    assert "typed ingress tests now distinguish accepted coercion from prohibited shapes on the selected runtime bundle surface" in doc
    assert "Gate 106 may begin" in doc
