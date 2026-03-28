from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from typer.testing import CliRunner

from nvda_desk.api.app import app
from nvda_desk.api.deps import (
    get_events_service,
    get_execution_records_service,
    get_overnight_carry_replay_service,
    get_review_packet_service,
)
from nvda_desk.cli import app as cli_app
from nvda_desk.config import Settings
from nvda_desk.db import create_engine_from_url, create_schema, seed_dev_data
from nvda_desk.db.session import create_session_factory
from nvda_desk.domain.session_clock import SessionClockClassifier
from nvda_desk.services.carry_market import OvernightCarryMarketService
from nvda_desk.services.carry_replay import OvernightCarryReplayService
from nvda_desk.services.events import EventsService
from nvda_desk.services.execution_records import ExecutionRecordsService
from nvda_desk.services.market_state import MarketStateService
from nvda_desk.services.review_packets import ReviewPacketService


class Bundle:
    def __init__(self, tmp_path: Path):
        database_url = f"sqlite+pysqlite:///{tmp_path / 'carry_review.db'}"
        create_schema(database_url)
        engine = create_engine_from_url(database_url)
        with Session(engine) as session:
            seed_dev_data(session)
        self.database_url = database_url
        self.session_factory = create_session_factory(database_url)
        classifier = SessionClockClassifier(Settings(database_url=database_url))
        market = MarketStateService(classifier, session_factory=self.session_factory)
        self.events = EventsService(self.session_factory)
        self.execution = ExecutionRecordsService(self.session_factory)
        self.carry_replay = OvernightCarryReplayService(
            self.session_factory,
            OvernightCarryMarketService(self.session_factory, classifier, market),
        )
        self.review = ReviewPacketService(self.session_factory, self.execution, self.events)


def _client(bundle: Bundle) -> Iterator[TestClient]:
    app.dependency_overrides[get_events_service] = lambda: bundle.events
    app.dependency_overrides[get_execution_records_service] = lambda: bundle.execution
    app.dependency_overrides[get_overnight_carry_replay_service] = lambda: bundle.carry_replay
    app.dependency_overrides[get_review_packet_service] = lambda: bundle.review
    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.clear()


runner = CliRunner()


def test_legacy_jsonl_artifacts_parse() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    for rel_path in [
        "backlog/remaining_legacy_source_inventory.jsonl",
        "backlog/legacy_data_fixtures_manifest.jsonl",
        "backlog/legacy_feature_backlog_additions.jsonl",
        "backlog/legacy_module_backlog_additions.jsonl",
    ]:
        path = repo_root / rel_path
        rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
        assert rows


def test_carry_replay_and_review_routes(tmp_path: Path) -> None:
    bundle = Bundle(tmp_path)
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
        carry = client.post(
            "/evals/overnight-carry-evaluator/replay-from-market",
            json={
                "symbol": "NVDA",
                "evaluation_ts": "2026-03-18T17:29:00Z",
                "asia_precursor_composite": 0.35,
                "risk_budget_remaining_pct": 25.0,
                "gross_exposure_pct": 10.0,
                "open_orders_count": 0,
                "baseline_hold_exposure_pct": 10.0,
            },
        )
        health = client.get("/review/module-health/slv-v2-market")
        daily = client.get(
            "/review/daily-packet",
            params={"report_date": "2026-03-18T20:00:00Z", "symbol": "NVDA"},
        )
    assert signal.status_code == 200
    assert order.status_code == 200
    assert pnl.status_code == 200
    assert carry.status_code == 200
    carry_payload = carry.json()
    assert carry_payload["best_path_name"] in {
        "flatten",
        "hold_baseline",
        "follow_recommendation",
    }
    assert carry_payload["event_window_open"] is True
    assert health.status_code == 200
    health_payload = health.json()
    assert health_payload["evaluation_count"] >= 0
    assert health_payload["record_counts"]["signal_event_count"] == 1
    assert daily.status_code == 200
    daily_payload = daily.json()
    assert daily_payload["trade_count"] == 1
    assert len(daily_payload["module_health"]) >= 1
    assert len(daily_payload["recent_events"]) >= 1


def test_cli_wrappers(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    database_url = f"sqlite+pysqlite:///{tmp_path / 'cli.db'}"
    create_schema(database_url)
    engine = create_engine_from_url(database_url)
    with Session(engine) as session:
        seed_dev_data(session)
    monkeypatch.setenv("NVDA_DESK_DATABASE_URL", database_url)
    inventory = runner.invoke(cli_app, ["legacy-source-inventory"])
    fixtures = runner.invoke(cli_app, ["legacy-fixture-summary"])
    carry = runner.invoke(cli_app, ["carry-replay", "--evaluation-ts", "2026-03-18T17:29:00Z"])
    review = runner.invoke(cli_app, ["review-daily-packet", "--report-date", "2026-03-18"])
    assert inventory.exit_code == 0
    assert fixtures.exit_code == 0
    assert carry.exit_code == 0
    assert review.exit_code == 0
    assert "document_count" in inventory.stdout
    assert "fixture_candidate_count" in fixtures.stdout
    assert "best_path_name" in carry.stdout
    assert "module_health" in review.stdout
