from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from nvda_desk.api.app import app
from nvda_desk.api.deps import get_events_service, get_execution_records_service
from nvda_desk.db import create_engine_from_url, create_schema, seed_dev_data
from nvda_desk.db.session import create_session_factory
from nvda_desk.services.events import EventsService
from nvda_desk.services.execution_records import ExecutionRecordsService


@dataclass(frozen=True)
class RecordsBundle:
    events: EventsService
    execution: ExecutionRecordsService


def _build_bundle(tmp_path: Path) -> RecordsBundle:
    database_url = f"sqlite+pysqlite:///{tmp_path / 'second_wave.db'}"
    create_schema(database_url)
    engine = create_engine_from_url(database_url)
    with Session(engine) as session:
        seed_dev_data(session)
    session_factory = create_session_factory(database_url)
    return RecordsBundle(
        events=EventsService(session_factory),
        execution=ExecutionRecordsService(session_factory),
    )


def _client(bundle: RecordsBundle) -> Iterator[TestClient]:
    app.dependency_overrides[get_events_service] = lambda: bundle.events
    app.dependency_overrides[get_execution_records_service] = lambda: bundle.execution
    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.clear()


def test_events_routes_and_proximity(tmp_path: Path) -> None:
    bundle = _build_bundle(tmp_path)
    for client in _client(bundle):
        proximity = client.get(
            "/events/proximity",
            params={"ts": "2026-03-18T15:00:00Z", "symbol": "NVDA"},
        )
        create_event = client.post(
            "/events/market",
            json={
                "symbol": "NVDA",
                "event_ts": "2026-03-18T19:00:00Z",
                "event_type": "analyst_call",
                "impact_level": "low",
                "title": "Analyst call",
                "source_document": "test",
            },
        )
        list_events = client.get("/events/market", params={"symbol": "NVDA"})
        sessions = client.get("/events/calendar")
    assert proximity.status_code == 200
    payload = proximity.json()
    assert payload["event_risk_window_open"] is True
    assert len(payload["upcoming_events"]) == 1
    assert len(payload["recent_events"]) == 1
    assert create_event.status_code == 200
    assert list_events.status_code == 200
    assert any(
        event["title"] == "Analyst call" for event in list_events.json()["events"]
    )
    assert sessions.status_code == 200
    assert len(sessions.json()["sessions"]) >= 2


def test_execution_and_broker_routes(tmp_path: Path) -> None:
    bundle = _build_bundle(tmp_path)
    for client in _client(bundle):
        signal = client.post(
            "/execution/signals",
            json={
                "symbol": "NVDA",
                "module_id": "slv-v2-market",
                "requested_at": "2026-03-18T14:00:00Z",
                "signal_code": "strike_zone_support",
                "direction": "long",
                "score": 0.82,
                "payload": {"strike": 98.0},
            },
        )
        veto = client.post(
            "/execution/vetoes",
            json={
                "symbol": "NVDA",
                "module_id": "slv-v2-market",
                "requested_at": "2026-03-18T14:01:00Z",
                "veto_code": "macro_risk_window",
                "reason": "macro event inside risk window",
            },
        )
        block = client.post(
            "/execution/risk-blocks",
            json={
                "symbol": "NVDA",
                "module_id": "slv-v2-market",
                "requested_at": "2026-03-18T14:02:00Z",
                "reason_codes": ["vvix_hot"],
                "payload": {"vvix": 91.0},
            },
        )
        order = client.post(
            "/broker/orders/paper",
            json={
                "symbol": "NVDA",
                "module_id": "slv-v2-market",
                "requested_at": "2026-03-18T14:03:00Z",
                "side": "buy",
                "quantity": 5,
                "limit_price": 98.0,
                "payload": {"source": "test"},
            },
        )
        signal_list = client.get(
            "/execution/signals", params={"module_id": "slv-v2-market"}
        )
        veto_list = client.get(
            "/execution/vetoes", params={"module_id": "slv-v2-market"}
        )
        block_list = client.get(
            "/execution/risk-blocks", params={"module_id": "slv-v2-market"}
        )
        order_events = client.get("/broker/order-events")
        fill_events = client.get("/broker/fill-events")
        positions = client.get("/broker/positions", params={"symbol": "NVDA"})
        account = client.get("/broker/account-state")
        pnl = client.post(
            "/execution/daily-pnl",
            json={
                "symbol": "NVDA",
                "report_date": "2026-03-18",
                "realized_pnl": 12.5,
                "unrealized_pnl": 7.25,
                "gross_exposure": 490.0,
                "turnover": 490.0,
                "trade_count": 1,
                "notes": ["offline paper fill"],
            },
        )
        pnl_list = client.get("/execution/daily-pnl", params={"symbol": "NVDA"})
    assert signal.status_code == 200
    assert veto.status_code == 200
    assert block.status_code == 200
    assert order.status_code == 200
    order_payload = order.json()
    assert order_payload["status"] == "filled"
    assert order_payload["filled_quantity"] == 5.0
    assert (
        signal_list.status_code == 200 and len(signal_list.json()["signal_events"]) == 1
    )
    assert veto_list.status_code == 200 and len(veto_list.json()["veto_events"]) == 1
    assert (
        block_list.status_code == 200
        and len(block_list.json()["risk_block_events"]) == 1
    )
    assert (
        order_events.status_code == 200
        and len(order_events.json()["order_events"]) == 2
    )
    assert (
        fill_events.status_code == 200 and len(fill_events.json()["fill_events"]) == 1
    )
    assert (
        positions.status_code == 200
        and positions.json()["positions"][0]["quantity"] == 5.0
    )
    assert positions.json()["positions"][0]["market_value"] == 620.0
    assert account.status_code == 200 and account.json()["cash"] == 99510.0
    assert account.json()["gross_exposure"] == 620.0
    assert pnl.status_code == 200
    assert (
        pnl_list.status_code == 200
        and pnl_list.json()["reports"][0]["trade_count"] == 1
    )
