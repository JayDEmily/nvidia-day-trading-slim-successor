from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from nvda_desk.api.app import app
from nvda_desk.api.deps import (
    get_capital_allocator_service,
    get_evaluation_log_service,
    get_experiment_log_service,
    get_market_state_service,
    get_overnight_carry_market_service,
    get_replay_service,
    get_research_service,
    get_risk_gateway_service,
    get_strategic_ladder_experiment_service,
    get_strategic_ladder_market_service,
    get_strategic_ladder_replay_service,
)
from nvda_desk.config import Settings
from nvda_desk.db import create_engine_from_url, create_schema, seed_dev_data
from nvda_desk.db.session import create_session_factory
from nvda_desk.domain.session_clock import SessionClockClassifier
from nvda_desk.services.capital_allocator import CapitalAllocatorService
from nvda_desk.services.carry_market import OvernightCarryMarketService
from nvda_desk.services.config_surface import ConfigSurfaceService
from nvda_desk.services.evaluation_log import EvaluationLogService
from nvda_desk.services.experiment_log import ExperimentLogService
from nvda_desk.services.market_state import MarketStateService
from nvda_desk.services.replay import ReplayService
from nvda_desk.services.research import ResearchService
from nvda_desk.services.risk_gateway import RiskGatewayService
from nvda_desk.services.slv_experiments import StrategicLadderExperimentService
from nvda_desk.services.slv_market import StrategicLadderMarketService
from nvda_desk.services.slv_replay import StrategicLadderReplayService


class ServiceBundle:
    def __init__(self, tmp_path: Path):
        database_url = f"sqlite+pysqlite:///{tmp_path / 'test_bundle.db'}"
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
        self.market = market
        config_dir = Path(__file__).resolve().parents[1] / "config"
        self.config_surface = ConfigSurfaceService(config_dir)
        self.research = ResearchService(session_factory)
        self.evals = EvaluationLogService(session_factory)
        self.experiments = ExperimentLogService(session_factory)
        self.replay = ReplayService(classifier, session_factory)
        self.slv_market = slv_market
        self.slv_replay = StrategicLadderReplayService(
            session_factory,
            classifier,
            market,
            slv_market,
            risk,
        )
        self.carry_market = OvernightCarryMarketService(session_factory, classifier, market)
        self.risk = risk
        self.slv_experiments = StrategicLadderExperimentService(
            classifier,
            market,
            self.slv_replay,
            self.experiments,
            self.config_surface,
        )
        self.capital_allocator = CapitalAllocatorService(self.experiments, self.config_surface)


def _client_with_services(bundle: ServiceBundle) -> Iterator[TestClient]:
    app.dependency_overrides[get_market_state_service] = lambda: bundle.market
    app.dependency_overrides[get_research_service] = lambda: bundle.research
    app.dependency_overrides[get_evaluation_log_service] = lambda: bundle.evals
    app.dependency_overrides[get_experiment_log_service] = lambda: bundle.experiments
    app.dependency_overrides[get_replay_service] = lambda: bundle.replay
    app.dependency_overrides[get_strategic_ladder_market_service] = lambda: bundle.slv_market
    app.dependency_overrides[get_strategic_ladder_replay_service] = lambda: bundle.slv_replay
    app.dependency_overrides[get_strategic_ladder_experiment_service] = (
        lambda: bundle.slv_experiments
    )
    app.dependency_overrides[get_overnight_carry_market_service] = lambda: bundle.carry_market
    app.dependency_overrides[get_risk_gateway_service] = lambda: bundle.risk
    app.dependency_overrides[get_capital_allocator_service] = lambda: bundle.capital_allocator
    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.clear()


def test_research_note_roundtrip(tmp_path: Path) -> None:
    bundle = ServiceBundle(tmp_path)
    for client in _client_with_services(bundle):
        create_response = client.post(
            "/research/notes",
            json={
                "symbol": "NVDA",
                "title": "Opening ladder thesis",
                "thesis": "Use session clock and options pressure together.",
                "body_md": "Detailed note body.",
                "tags": ["session-clock", "slv"],
            },
        )
        list_response = client.get("/research/notes")
    assert create_response.status_code == 200
    created = create_response.json()
    assert created["title"] == "Opening ladder thesis"
    assert created["tags"] == ["session-clock", "slv"]
    assert list_response.status_code == 200
    listed = list_response.json()["notes"]
    assert len(listed) == 1
    assert listed[0]["note_id"] == created["note_id"]


def test_record_strategic_ladder_eval(tmp_path: Path) -> None:
    bundle = ServiceBundle(tmp_path)
    for client in _client_with_services(bundle):
        response = client.post(
            "/evals/strategic-ladder-validator",
            json={
                "symbol": "NVDA",
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
    assert payload["module_id"] == "slv-v1"
    assert payload["verdict"] == "pass"
    assert payload["output_payload"]["overall_decision"] == "accept"


def test_record_strategic_ladder_market_eval(tmp_path: Path) -> None:
    bundle = ServiceBundle(tmp_path)
    for client in _client_with_services(bundle):
        response = client.post(
            "/evals/strategic-ladder-validator/from-market",
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
    assert payload["module_id"] == "slv-v2-market"
    assert payload["output_payload"]["snapshots_considered"] == 2
    assert payload["verdict"] in {"pass", "review"}
    assert payload["output_payload"]["rung_decisions"][0]["decision"] in {
        "keep",
        "adjust",
    }


def test_record_strategic_ladder_replay_eval(tmp_path: Path) -> None:
    bundle = ServiceBundle(tmp_path)
    for client in _client_with_services(bundle):
        response = client.post(
            "/evals/strategic-ladder-validator/replay-from-market",
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
    assert payload["module_id"] == "slv-v3-replay"
    assert payload["output_payload"]["entry_phase"] == "open_disorder"
    assert payload["output_payload"]["supervisory_overlay"]["action"] in {
        "allow",
        "derisk",
    }
    assert len(payload["output_payload"]["rung_outcomes"]) == 2


def test_replay_session_phases_groups_seeded_bars(tmp_path: Path) -> None:
    bundle = ServiceBundle(tmp_path)
    for client in _client_with_services(bundle):
        response = client.get(
            "/replay/session-phases",
            params={
                "symbol": "NVDA",
                "start_ts": "2026-03-18T13:30:00Z",
                "end_ts": "2026-03-18T17:29:00Z",
            },
        )
    assert response.status_code == 200
    payload = response.json()
    assert payload["total_bars"] == 240
    phases = {item["phase"]: item for item in payload["phase_summaries"]}
    assert phases["open_disorder"]["bar_count"] == 30
    assert phases["early_anchor"]["bar_count"] == 60
    assert phases["institutional_repricing"]["bar_count"] == 60
    assert phases["midday_compression"]["bar_count"] == 90


def test_record_overnight_carry_market_eval(tmp_path: Path) -> None:
    bundle = ServiceBundle(tmp_path)
    for client in _client_with_services(bundle):
        response = client.post(
            "/evals/overnight-carry-evaluator/from-market",
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
    assert payload["module_id"] == "overnight-carry-v2-market"
    assert payload["output_payload"]["derived_context"]["vix_level"] > 0


def test_list_evaluation_runs(tmp_path: Path) -> None:
    bundle = ServiceBundle(tmp_path)
    for client in _client_with_services(bundle):
        create_response = client.post(
            "/evals/strategic-ladder-validator/replay-from-market",
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
        list_response = client.get("/evals/runs", params={"module_id": "slv-v3-replay"})
    assert create_response.status_code == 200
    assert list_response.status_code == 200
    evaluations = list_response.json()["evaluations"]
    assert len(evaluations) == 1
    assert evaluations[0]["module_id"] == "slv-v3-replay"


def test_slv_walk_forward_persists_experiment(tmp_path: Path) -> None:
    bundle = ServiceBundle(tmp_path)
    for client in _client_with_services(bundle):
        response = client.post(
            "/evals/strategic-ladder-validator/walk-forward-from-market",
            json={
                "base_payload": {
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
                "anchor_timestamps": [
                    "2026-03-18T13:35:00Z",
                    "2026-03-18T14:05:00Z",
                    "2026-03-18T15:05:00Z",
                ],
                "config_name": "wf-default",
            },
        )
        experiments = client.get(
            "/evals/experiments",
            params={"module_id": "slv-v3-replay", "experiment_type": "walk_forward"},
        )
    assert response.status_code == 200
    payload = response.json()
    assert payload["evaluation_count"] == 3
    assert payload["experiment_id"] is not None
    assert payload["phase_buckets"]
    assert experiments.status_code == 200
    listed = experiments.json()["experiments"]
    assert len(listed) == 1
    assert listed[0]["config_name"] == "wf-default"
    assert listed[0]["experiment_type"] == "walk_forward"


def test_slv_fragility_persists_failure_modes(tmp_path: Path) -> None:
    bundle = ServiceBundle(tmp_path)
    for client in _client_with_services(bundle):
        response = client.post(
            "/evals/strategic-ladder-validator/fragility-from-market",
            json={
                "base_payload": {
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
                "scenarios": [
                    {"name": "time-delay", "entry_offset_minutes": 5},
                    {"name": "price-shift", "rung_price_shift_pct": 0.5},
                ],
                "config_name": "frag-default",
            },
        )
    assert response.status_code == 200
    payload = response.json()
    assert payload["experiment_id"] is not None
    assert payload["scenario_results"][0]["name"] == "time-delay"
    assert payload["fragility_score"] >= 0.0
    assert isinstance(payload["failure_modes"], list)


def test_slv_batch_ranking_and_allocator(tmp_path: Path) -> None:
    bundle = ServiceBundle(tmp_path)
    for client in _client_with_services(bundle):
        batch_response = client.post(
            "/evals/strategic-ladder-validator/batch-rank-from-market",
            json={
                "base_payload": {
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
                "anchor_timestamps": [
                    "2026-03-18T13:35:00Z",
                    "2026-03-18T14:05:00Z",
                    "2026-03-18T15:05:00Z",
                ],
                "variant_names": ["baseline", "conservative"],
                "variants": [
                    {
                        "name": "vwap-plus",
                        "vwap_offset_pct": 0.5,
                        "coefficient_group_name": "S08",
                    }
                ],
                "batch_name": "batch-1",
            },
        )
        allocation_response = client.post(
            "/allocation/module-regime",
            json={
                "requested_at": "2026-03-18T15:10:00Z",
                "total_capital": 100000,
                "session_phase": "institutional_repricing",
                "vix_level": 19.5,
                "vvix_level": 90.0,
                "strategy_variant_name": "conservative",
                "coefficient_group_name": "S06",
                "candidates": [
                    {
                        "module_id": "slv-v3-replay",
                        "module_name": "Strategic Ladder Replay",
                        "config_key": "S06",
                        "base_weight": 1.0,
                        "min_allocation_pct": 0.0,
                        "max_allocation_pct": 60.0,
                    }
                ],
            },
        )
    assert batch_response.status_code == 200
    batch_payload = batch_response.json()
    assert batch_payload["experiment_id"] is not None
    assert len(batch_payload["ranked_variants"]) == 3
    ranked_names = {item["name"] for item in batch_payload["ranked_variants"]}
    assert {"baseline", "conservative", "vwap-plus"}.issubset(ranked_names)
    assert (
        batch_payload["ranked_variants"][0]["ranking_score"]
        >= batch_payload["ranked_variants"][1]["ranking_score"]
    )
    assert allocation_response.status_code == 200
    allocation_payload = allocation_response.json()
    assert allocation_payload["allocations"][0]["module_id"] == "slv-v3-replay"
    assert allocation_payload["cash_reserve_pct"] >= 0.0
    assert "variant_weight_override_applied" in allocation_payload["allocations"][0]["reasons"]


def test_unknown_strategy_variant_returns_404(tmp_path: Path) -> None:
    bundle = ServiceBundle(tmp_path)
    for client in _client_with_services(bundle):
        response = client.post(
            "/evals/strategic-ladder-validator/batch-rank-from-market",
            json={
                "base_payload": {
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
                "anchor_timestamps": [
                    "2026-03-18T13:35:00Z",
                    "2026-03-18T14:05:00Z",
                    "2026-03-18T15:05:00Z",
                ],
                "variant_names": ["unknown-variant"],
                "batch_name": "bad-batch",
            },
        )
    assert response.status_code == 404
