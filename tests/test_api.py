from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from nvda_desk.api.app import app
from nvda_desk.api.deps import (
    get_market_state_service,
    get_overnight_carry_market_service,
    get_risk_gateway_service,
    get_strategic_ladder_market_service,
    get_strategic_ladder_replay_service,
)
from nvda_desk.config import Settings
from nvda_desk.db import create_engine_from_url, create_schema, seed_dev_data
from nvda_desk.db.session import create_session_factory
from nvda_desk.domain.session_clock import SessionClockClassifier
from nvda_desk.services.carry_market import OvernightCarryMarketService
from nvda_desk.services.market_state import MarketStateService
from nvda_desk.services.risk_gateway import RiskGatewayService
from nvda_desk.services.slv_market import StrategicLadderMarketService
from nvda_desk.services.slv_replay import StrategicLadderReplayService


@dataclass(frozen=True)
class MarketServiceBundle:
    market: MarketStateService
    slv_market: StrategicLadderMarketService
    slv_replay: StrategicLadderReplayService
    carry_market: OvernightCarryMarketService
    risk: RiskGatewayService


def _build_service_bundle(tmp_path: Path) -> MarketServiceBundle:
    database_url = f"sqlite+pysqlite:///{tmp_path / 'test_api.db'}"
    create_schema(database_url)
    engine = create_engine_from_url(database_url)
    with Session(engine) as session:
        seed_dev_data(session)
    settings = Settings(database_url=database_url)
    session_factory = create_session_factory(database_url)
    classifier = SessionClockClassifier(settings)
    market = MarketStateService(classifier, session_factory=session_factory)
    slv_market = StrategicLadderMarketService(session_factory)
    risk = RiskGatewayService(session_factory)
    return MarketServiceBundle(
        market=market,
        slv_market=slv_market,
        slv_replay=StrategicLadderReplayService(session_factory, classifier, market, slv_market, risk),
        carry_market=OvernightCarryMarketService(session_factory, classifier, market),
        risk=risk,
    )


def _client_with_service(bundle: MarketServiceBundle) -> Iterator[TestClient]:
    app.dependency_overrides[get_market_state_service] = lambda: bundle.market
    app.dependency_overrides[get_strategic_ladder_market_service] = lambda: bundle.slv_market
    app.dependency_overrides[get_strategic_ladder_replay_service] = lambda: bundle.slv_replay
    app.dependency_overrides[get_overnight_carry_market_service] = lambda: bundle.carry_market
    app.dependency_overrides[get_risk_gateway_service] = lambda: bundle.risk
    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.clear()


def test_health() -> None:
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_market_session_clock() -> None:
    with TestClient(app) as client:
        response = client.get(
            "/market/session-clock",
            params={"ts": "2026-03-18T13:35:00Z"},
        )
    assert response.status_code == 200
    payload = response.json()
    assert payload["phase"] == "open_disorder"
    assert payload["minutes_since_open"] == 5


def test_config_routes() -> None:
    with TestClient(app) as client:
        runtime_response = client.get("/config/runtime-settings")
        coefficient_response = client.get("/config/coefficients/S06")
        variants_response = client.get("/config/strategy-variants/conservative")
        missing_variant_response = client.get("/config/strategy-variants/does-not-exist")
    assert runtime_response.status_code == 200
    assert runtime_response.json()["environment"]["symbol"] == "NVDA"
    assert coefficient_response.status_code == 200
    assert coefficient_response.json()["key"] == "S06"
    assert variants_response.status_code == 200
    assert variants_response.json()["name"] == "conservative"
    assert missing_variant_response.status_code == 404


def test_market_snapshot_with_seeded_bar(tmp_path: Path) -> None:
    bundle = _build_service_bundle(tmp_path)
    for client in _client_with_service(bundle):
        response = client.get(
            "/market/snapshot",
            params={"symbol": "NVDA", "ts": "2026-03-18T13:40:00Z"},
        )
    assert response.status_code == 200
    payload = response.json()
    assert payload["symbol"] == "NVDA"
    assert payload["session_clock"]["phase"] == "open_disorder"
    assert payload["latest_bar"] is not None
    assert payload["latest_bar"]["ts_utc"] == "2026-03-18T13:40:00Z"


def test_market_intraday_with_seeded_bars(tmp_path: Path) -> None:
    bundle = _build_service_bundle(tmp_path)
    for client in _client_with_service(bundle):
        response = client.get(
            "/market/intraday",
            params={"symbol": "NVDA", "ts": "2026-03-18T13:40:00Z", "limit": 3},
        )
    assert response.status_code == 200
    payload = response.json()
    assert len(payload["bars"]) == 3
    assert payload["bars"][0]["ts_utc"] == "2026-03-18T13:38:00Z"
    assert payload["bars"][2]["ts_utc"] == "2026-03-18T13:40:00Z"


def test_market_option_surface_with_seeded_snapshots(tmp_path: Path) -> None:
    bundle = _build_service_bundle(tmp_path)
    for client in _client_with_service(bundle):
        response = client.get(
            "/market/options-surface",
            params={
                "symbol": "NVDA",
                "as_of_date": "2025-04-11T00:00:00Z",
                "expiry": "2025-04-11T00:00:00Z",
                "option_type": "Put",
            },
        )
    assert response.status_code == 200
    payload = response.json()
    assert payload["symbol"] == "NVDA"
    assert payload["as_of_date"] == "2025-04-11"
    assert payload["expiry"] == "2025-04-11"
    assert payload["option_type"] == "Put"
    assert len(payload["snapshots"]) == 2
    assert payload["snapshots"][0]["strike"] == "97.000000"
    assert payload["snapshots"][1]["strike"] == "98.000000"


def test_strategic_ladder_validator_endpoint() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/modules/strategic-ladder-validator/evaluate",
            json={
                "spot_price": 120.0,
                "distance_to_vwap_pct": 0.4,
                "iv_hv_divergence_pct": 5.0,
                "session_phase": "pre_market",
                "rungs": [
                    {
                        "price": 119.0,
                        "size_units": 10,
                        "strike_pressure_score": 0.8,
                        "fill_plausibility_score": 0.75,
                    }
                ],
            },
        )
    assert response.status_code == 200
    payload = response.json()
    assert payload["overall_decision"] == "accept"


def test_strategic_ladder_validator_from_market_endpoint(tmp_path: Path) -> None:
    bundle = _build_service_bundle(tmp_path)
    for client in _client_with_service(bundle):
        response = client.post(
            "/modules/strategic-ladder-validator/evaluate-from-market",
            json={
                "symbol": "NVDA",
                "as_of_date": "2025-04-11",
                "expiry": "2025-04-11",
                "option_type": "Put",
                "spot_price": 98.0,
                "distance_to_vwap_pct": 0.4,
                "iv_hv_divergence_pct": 8.0,
                "session_phase": "pre_market",
                "rungs": [
                    {"price": 98.0, "size_units": 10},
                    {"price": 94.0, "size_units": 5},
                ],
            },
        )
    assert response.status_code == 200
    payload = response.json()
    assert payload["snapshots_considered"] == 2
    assert payload["overall_decision"] == "adjust"
    assert payload["rung_decisions"][0]["decision"] in {"keep", "adjust"}
    assert payload["rung_decisions"][1]["decision"] in {"adjust", "drop"}
    assert payload["strike_zone_signals"][0]["strike"] == 98.0


def test_strategic_ladder_replay_from_market_endpoint(tmp_path: Path) -> None:
    bundle = _build_service_bundle(tmp_path)
    for client in _client_with_service(bundle):
        response = client.post(
            "/modules/strategic-ladder-validator/replay-from-market",
            json={
                "symbol": "NVDA",
                "as_of_date": "2025-04-11",
                "expiry": "2025-04-11",
                "option_type": "Put",
                "entry_ts": "2026-03-18T13:35:00Z",
                "spot_price": 118.9,
                "distance_to_vwap_pct": 0.4,
                "iv_hv_divergence_pct": 8.0,
                "session_phase": "open_disorder",
                "lookahead_minutes": 20,
                "gross_exposure_pct": 20.0,
                "risk_budget_remaining_pct": 80.0,
                "rungs": [
                    {"price": 118.75, "size_units": 10},
                    {"price": 118.3, "size_units": 5},
                ],
            },
        )
    assert response.status_code == 200
    payload = response.json()
    assert payload["entry_phase"] == "open_disorder"
    assert payload["evaluated_bar_count"] >= 1
    assert payload["supervisory_overlay"]["action"] in {"allow", "derisk"}
    assert len(payload["rung_outcomes"]) == 2


def test_overnight_carry_endpoint() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/modules/overnight-carry-evaluator/evaluate",
            json={
                "close_distance_to_vwap_pct": 0.8,
                "close_phase": "dealer_unwind_close",
                "realised_vol_pct": 2.0,
                "vix_level": 18.0,
                "vvix_level": 90.0,
                "asia_precursor_composite": 0.4,
                "risk_budget_remaining_pct": 30.0,
                "gross_exposure_pct": 10.0,
                "open_orders_count": 0,
            },
        )
    assert response.status_code == 200
    payload = response.json()
    assert payload["carry_recommendation"] == "increase"


def test_overnight_carry_from_market_endpoint(tmp_path: Path) -> None:
    bundle = _build_service_bundle(tmp_path)
    for client in _client_with_service(bundle):
        response = client.post(
            "/modules/overnight-carry-evaluator/evaluate-from-market",
            json={
                "symbol": "NVDA",
                "evaluation_ts": "2026-03-18T17:29:00Z",
                "asia_precursor_composite": 0.35,
                "risk_budget_remaining_pct": 25.0,
                "gross_exposure_pct": 10.0,
                "open_orders_count": 0,
            },
        )
    assert response.status_code == 200
    payload = response.json()
    assert payload["derived_context"]["close_phase"] in {"midday_compression", "post_lunch_drift"}
    assert payload["carry_recommendation"] in {"hold_small", "increase", "flatten", "block"}


def test_risk_gateway_endpoint(tmp_path: Path) -> None:
    bundle = _build_service_bundle(tmp_path)
    for client in _client_with_service(bundle):
        response = client.post(
            "/risk/evaluate",
            json={
                "symbol": "NVDA",
                "module_id": "slv-v3-replay",
                "requested_at": "2026-03-18T13:35:00Z",
                "session_phase": "open_disorder",
                "vix_level": 34.0,
                "vvix_level": 120.0,
                "vix_change_pct_15m": 20.0,
                "vvix_change_pct_15m": 25.0,
                "data_age_seconds": 0,
                "gross_exposure_pct": 20.0,
                "risk_budget_remaining_pct": 50.0,
                "open_orders_count": 0,
                "conflict_tags": [],
            },
        )
        list_response = client.get("/risk/decisions", params={"module_id": "slv-v3-replay"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["action"] == "block"
    assert list_response.status_code == 200
    assert len(list_response.json()["decisions"]) == 1
