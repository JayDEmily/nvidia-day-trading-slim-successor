"""add second-wave execution and event records

Revision ID: 20260320_0005
Revises: 20260320_0004
Create Date: 2026-03-20 19:35:00Z
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "20260320_0005"
down_revision = "20260320_0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "session_calendar",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("session_date", sa.Date(), nullable=False),
        sa.Column("venue", sa.String(length=32), nullable=False),
        sa.Column("market_open_utc", sa.DateTime(timezone=True), nullable=False),
        sa.Column("market_close_utc", sa.DateTime(timezone=True), nullable=False),
        sa.Column("session_label", sa.String(length=32), nullable=False),
        sa.Column("is_half_day", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("session_date", "venue", name="uq_session_calendar_date_venue"),
    )
    op.create_index("ix_session_calendar_date", "session_calendar", ["session_date"], unique=False)

    op.create_table(
        "market_event",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("symbol", sa.String(length=32), nullable=True),
        sa.Column("event_ts", sa.DateTime(timezone=True), nullable=False),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("impact_level", sa.String(length=16), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("source_document", sa.String(length=255), nullable=False),
        sa.Column("notes_md", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_market_event_symbol", "market_event", ["symbol"], unique=False)
    op.create_index("ix_market_event_ts", "market_event", ["event_ts"], unique=False)
    op.create_index("ix_market_event_event_type", "market_event", ["event_type"], unique=False)
    op.create_index(
        "ix_market_event_symbol_ts", "market_event", ["symbol", "event_ts"], unique=False
    )

    op.create_table(
        "module_signal_event",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("symbol", sa.String(length=32), nullable=False),
        sa.Column("module_id", sa.String(length=128), nullable=False),
        sa.Column("requested_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("signal_code", sa.String(length=128), nullable=False),
        sa.Column("direction", sa.String(length=16), nullable=False),
        sa.Column("score", sa.Numeric(8, 6), nullable=False),
        sa.Column("payload_json", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_module_signal_event_symbol", "module_signal_event", ["symbol"], unique=False
    )
    op.create_index(
        "ix_module_signal_event_module_id", "module_signal_event", ["module_id"], unique=False
    )
    op.create_index(
        "ix_module_signal_event_signal_code", "module_signal_event", ["signal_code"], unique=False
    )
    op.create_index(
        "ix_module_signal_event_module_created",
        "module_signal_event",
        ["module_id", "created_at"],
        unique=False,
    )

    op.create_table(
        "module_veto_event",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("symbol", sa.String(length=32), nullable=False),
        sa.Column("module_id", sa.String(length=128), nullable=False),
        sa.Column("requested_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("veto_code", sa.String(length=128), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("payload_json", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_module_veto_event_symbol", "module_veto_event", ["symbol"], unique=False)
    op.create_index(
        "ix_module_veto_event_module_id", "module_veto_event", ["module_id"], unique=False
    )
    op.create_index(
        "ix_module_veto_event_veto_code", "module_veto_event", ["veto_code"], unique=False
    )
    op.create_index(
        "ix_module_veto_event_module_created",
        "module_veto_event",
        ["module_id", "created_at"],
        unique=False,
    )

    op.create_table(
        "risk_block_event",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("symbol", sa.String(length=32), nullable=False),
        sa.Column("module_id", sa.String(length=128), nullable=False),
        sa.Column("requested_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("linked_risk_decision_id", sa.Integer(), nullable=True),
        sa.Column("reason_codes_json", sa.Text(), nullable=False),
        sa.Column("payload_json", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["linked_risk_decision_id"], ["risk_decision_log.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_risk_block_event_symbol", "risk_block_event", ["symbol"], unique=False)
    op.create_index(
        "ix_risk_block_event_module_id", "risk_block_event", ["module_id"], unique=False
    )
    op.create_index(
        "ix_risk_block_event_module_created",
        "risk_block_event",
        ["module_id", "created_at"],
        unique=False,
    )

    op.create_table(
        "order_intent",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("symbol", sa.String(length=32), nullable=False),
        sa.Column("module_id", sa.String(length=128), nullable=False),
        sa.Column("requested_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("side", sa.String(length=8), nullable=False),
        sa.Column("quantity", sa.Numeric(18, 6), nullable=False),
        sa.Column("order_type", sa.String(length=16), nullable=False),
        sa.Column("limit_price", sa.Numeric(18, 6), nullable=True),
        sa.Column("client_order_ref", sa.String(length=128), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("payload_json", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_order_intent_symbol", "order_intent", ["symbol"], unique=False)
    op.create_index("ix_order_intent_module_id", "order_intent", ["module_id"], unique=False)
    op.create_index("ix_order_intent_side", "order_intent", ["side"], unique=False)
    op.create_index(
        "ix_order_intent_client_order_ref", "order_intent", ["client_order_ref"], unique=True
    )
    op.create_index("ix_order_intent_status", "order_intent", ["status"], unique=False)
    op.create_index(
        "ix_order_intent_module_created", "order_intent", ["module_id", "created_at"], unique=False
    )

    op.create_table(
        "order_event",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("order_intent_id", sa.Integer(), nullable=False),
        sa.Column("event_ts", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("detail", sa.Text(), nullable=False),
        sa.Column("payload_json", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["order_intent_id"], ["order_intent.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_order_event_status", "order_event", ["status"], unique=False)
    op.create_index(
        "ix_order_event_intent_ts", "order_event", ["order_intent_id", "event_ts"], unique=False
    )

    op.create_table(
        "fill_event",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("order_intent_id", sa.Integer(), nullable=False),
        sa.Column("fill_ts", sa.DateTime(timezone=True), nullable=False),
        sa.Column("quantity", sa.Numeric(18, 6), nullable=False),
        sa.Column("fill_price", sa.Numeric(18, 6), nullable=False),
        sa.Column("notional", sa.Numeric(18, 6), nullable=False),
        sa.ForeignKeyConstraint(["order_intent_id"], ["order_intent.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_fill_event_intent_ts", "fill_event", ["order_intent_id", "fill_ts"], unique=False
    )

    op.create_table(
        "position_snapshot",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("symbol", sa.String(length=32), nullable=False),
        sa.Column("snapshot_ts", sa.DateTime(timezone=True), nullable=False),
        sa.Column("quantity", sa.Numeric(18, 6), nullable=False),
        sa.Column("average_price", sa.Numeric(18, 6), nullable=False),
        sa.Column("market_price", sa.Numeric(18, 6), nullable=False),
        sa.Column("market_value", sa.Numeric(18, 6), nullable=False),
        sa.Column("unrealized_pnl", sa.Numeric(18, 6), nullable=False),
        sa.Column("source", sa.String(length=32), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_position_snapshot_symbol", "position_snapshot", ["symbol"], unique=False)
    op.create_index(
        "ix_position_snapshot_symbol_ts",
        "position_snapshot",
        ["symbol", "snapshot_ts"],
        unique=False,
    )

    op.create_table(
        "capital_state_snapshot",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("snapshot_ts", sa.DateTime(timezone=True), nullable=False),
        sa.Column("cash", sa.Numeric(18, 6), nullable=False),
        sa.Column("equity", sa.Numeric(18, 6), nullable=False),
        sa.Column("buying_power", sa.Numeric(18, 6), nullable=False),
        sa.Column("gross_exposure", sa.Numeric(18, 6), nullable=False),
        sa.Column("net_exposure", sa.Numeric(18, 6), nullable=False),
        sa.Column("source", sa.String(length=32), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_capital_state_snapshot_ts", "capital_state_snapshot", ["snapshot_ts"], unique=False
    )

    op.create_table(
        "daily_pnl_report",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("symbol", sa.String(length=32), nullable=False),
        sa.Column("report_date", sa.Date(), nullable=False),
        sa.Column("realized_pnl", sa.Numeric(18, 6), nullable=False),
        sa.Column("unrealized_pnl", sa.Numeric(18, 6), nullable=False),
        sa.Column("gross_exposure", sa.Numeric(18, 6), nullable=False),
        sa.Column("turnover", sa.Numeric(18, 6), nullable=False),
        sa.Column("trade_count", sa.Integer(), nullable=False),
        sa.Column("notes_json", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("symbol", "report_date", name="uq_daily_pnl_report_symbol_date"),
    )
    op.create_index("ix_daily_pnl_report_symbol", "daily_pnl_report", ["symbol"], unique=False)
    op.create_index(
        "ix_daily_pnl_report_report_date", "daily_pnl_report", ["report_date"], unique=False
    )
    op.create_index("ix_daily_pnl_report_date", "daily_pnl_report", ["report_date"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_daily_pnl_report_date", table_name="daily_pnl_report")
    op.drop_index("ix_daily_pnl_report_report_date", table_name="daily_pnl_report")
    op.drop_index("ix_daily_pnl_report_symbol", table_name="daily_pnl_report")
    op.drop_table("daily_pnl_report")

    op.drop_index("ix_capital_state_snapshot_ts", table_name="capital_state_snapshot")
    op.drop_table("capital_state_snapshot")

    op.drop_index("ix_position_snapshot_symbol_ts", table_name="position_snapshot")
    op.drop_index("ix_position_snapshot_symbol", table_name="position_snapshot")
    op.drop_table("position_snapshot")

    op.drop_index("ix_fill_event_intent_ts", table_name="fill_event")
    op.drop_table("fill_event")

    op.drop_index("ix_order_event_intent_ts", table_name="order_event")
    op.drop_index("ix_order_event_status", table_name="order_event")
    op.drop_table("order_event")

    op.drop_index("ix_order_intent_module_created", table_name="order_intent")
    op.drop_index("ix_order_intent_status", table_name="order_intent")
    op.drop_index("ix_order_intent_client_order_ref", table_name="order_intent")
    op.drop_index("ix_order_intent_side", table_name="order_intent")
    op.drop_index("ix_order_intent_module_id", table_name="order_intent")
    op.drop_index("ix_order_intent_symbol", table_name="order_intent")
    op.drop_table("order_intent")

    op.drop_index("ix_risk_block_event_module_created", table_name="risk_block_event")
    op.drop_index("ix_risk_block_event_module_id", table_name="risk_block_event")
    op.drop_index("ix_risk_block_event_symbol", table_name="risk_block_event")
    op.drop_table("risk_block_event")

    op.drop_index("ix_module_veto_event_module_created", table_name="module_veto_event")
    op.drop_index("ix_module_veto_event_veto_code", table_name="module_veto_event")
    op.drop_index("ix_module_veto_event_module_id", table_name="module_veto_event")
    op.drop_index("ix_module_veto_event_symbol", table_name="module_veto_event")
    op.drop_table("module_veto_event")

    op.drop_index("ix_module_signal_event_module_created", table_name="module_signal_event")
    op.drop_index("ix_module_signal_event_signal_code", table_name="module_signal_event")
    op.drop_index("ix_module_signal_event_module_id", table_name="module_signal_event")
    op.drop_index("ix_module_signal_event_symbol", table_name="module_signal_event")
    op.drop_table("module_signal_event")

    op.drop_index("ix_market_event_symbol_ts", table_name="market_event")
    op.drop_index("ix_market_event_event_type", table_name="market_event")
    op.drop_index("ix_market_event_ts", table_name="market_event")
    op.drop_index("ix_market_event_symbol", table_name="market_event")
    op.drop_table("market_event")

    op.drop_index("ix_session_calendar_date", table_name="session_calendar")
    op.drop_table("session_calendar")
