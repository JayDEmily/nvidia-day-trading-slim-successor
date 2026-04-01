from __future__ import annotations

from datetime import UTC, datetime
import os
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect

from nvda_desk.db.session import create_session_factory
from nvda_desk.schemas.execution_records import BrokerPaperOrderInput
from nvda_desk.services.execution_records import ExecutionRecordsService

REPO_ROOT = Path(__file__).resolve().parents[1]
ALEMBIC_INI = REPO_ROOT / "alembic.ini"
ALEMBIC_DIR = REPO_ROOT / "alembic"


def _upgrade_head(db_path: Path) -> str:
    database_url = f"sqlite+pysqlite:///{db_path}"
    config = Config(str(ALEMBIC_INI))
    config.set_main_option("script_location", str(ALEMBIC_DIR))
    previous = os.environ.get("NVDA_DESK_DATABASE_URL")
    os.environ["NVDA_DESK_DATABASE_URL"] = database_url
    try:
        command.upgrade(config, "head")
    finally:
        if previous is None:
            os.environ.pop("NVDA_DESK_DATABASE_URL", None)
        else:
            os.environ["NVDA_DESK_DATABASE_URL"] = previous
    return database_url


def test_gate140_alembic_head_matches_bounded_execution_ledger_schema(tmp_path: Path) -> None:
    database_url = _upgrade_head(tmp_path / "gate140_schema.db")
    inspector = inspect(create_engine(database_url))

    assert "position_instance_snapshot" in inspector.get_table_names()

    order_intent_columns = {column["name"] for column in inspector.get_columns("order_intent")}
    assert {
        "position_instance_ref",
        "setup_variant_id",
        "execution_expression_id",
        "tradable_expression_family",
        "lifecycle_state",
        "lifecycle_action",
        "current_position_size_pct",
        "carry_state_eligible",
        "hard_flat_required",
    } <= order_intent_columns

    position_instance_columns = {column["name"] for column in inspector.get_columns("position_instance_snapshot")}
    assert {
        "position_instance_ref",
        "symbol",
        "snapshot_ts",
        "setup_variant_id",
        "execution_expression_id",
        "tradable_expression_family",
        "lifecycle_state",
        "lifecycle_action",
        "current_position_size_pct",
        "quantity",
        "average_price",
        "market_price",
        "market_value",
        "unrealized_pnl",
        "carry_state_eligible",
        "hard_flat_required",
        "source",
    } <= position_instance_columns


def test_gate140_migrated_database_supports_bounded_position_instance_roundtrip(tmp_path: Path) -> None:
    database_url = _upgrade_head(tmp_path / "gate140_runtime.db")
    session_factory = create_session_factory(database_url)
    service = ExecutionRecordsService(session_factory)

    service.place_paper_order(
        BrokerPaperOrderInput(
            symbol="NVDA",
            module_id="slv-v2-market",
            requested_at=datetime(2026, 4, 1, 14, 3, tzinfo=UTC),
            side="buy",
            quantity=5,
            limit_price=98.0,
            position_instance_ref="odi-cont-001",
            setup_variant_id="opening_drive_continuation",
            execution_expression_id="continuation_ladder_exec",
            tradable_expression_family="single_leg_call_debit",
            lifecycle_state="carry_nomination_ready",
            lifecycle_action="hold_small_overnight",
            current_position_size_pct=12.5,
            carry_state_eligible=True,
            hard_flat_required=False,
            payload={"source": "gate140"},
        )
    )

    response = service.list_position_instances(symbol="NVDA")
    assert len(response.position_instances) == 1
    instance = response.position_instances[0]
    assert instance.position_instance_ref == "odi-cont-001"
    assert instance.setup_variant_id == "opening_drive_continuation"
    assert instance.execution_expression_id == "continuation_ladder_exec"
    assert instance.tradable_expression_family == "single_leg_call_debit"
    assert instance.lifecycle_state == "carry_nomination_ready"
    assert instance.lifecycle_action == "hold_small_overnight"
    assert instance.current_position_size_pct == 12.5
    assert instance.carry_state_eligible is True
    assert instance.hard_flat_required is False
    assert instance.quantity == 5.0
