from __future__ import annotations

from datetime import UTC, date, datetime
from pathlib import Path

from sqlalchemy.orm import Session

from nvda_desk.config import Settings
from nvda_desk.db import create_engine_from_url, create_schema, seed_dev_data
from nvda_desk.db.models import OptionSnapshot
from nvda_desk.db.session import create_session_factory
from nvda_desk.domain.session_clock import SessionClockClassifier
from nvda_desk.schemas.options import OptionType
from nvda_desk.services.market_state import MarketStateService


def test_gate183_option_snapshot_model_carries_runtime_raw_row_fields() -> None:
    assert hasattr(OptionSnapshot, "iv")
    assert hasattr(OptionSnapshot, "delta")
    assert hasattr(OptionSnapshot, "gamma")


def test_gate183_market_surface_payload_exposes_raw_row_fields_even_when_null(tmp_path: Path) -> None:
    database_url = f"sqlite+pysqlite:///{tmp_path / 'gate183.db'}"
    create_schema(database_url)
    engine = create_engine_from_url(database_url)
    with Session(engine) as session:
        seed_dev_data(session)
    service = MarketStateService(
        SessionClockClassifier(Settings(database_url=database_url)),
        session_factory=create_session_factory(database_url),
    )

    response = service.get_option_surface(
        symbol="NVDA",
        as_of_date=date(2025, 4, 11),
        requested_at=datetime(2025, 4, 11, 15, 0, tzinfo=UTC),
        expiry=date(2025, 4, 11),
        option_type=OptionType.PUT,
    )

    assert response.snapshots
    first = response.snapshots[0]
    dumped = first.model_dump(mode="json")
    assert "iv" in dumped
    assert "delta" in dumped
    assert "gamma" in dumped
