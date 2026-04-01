"""restore execution-ledger position-instance parity

Revision ID: 20260401_0006
Revises: 20260320_0005
Create Date: 2026-04-01 12:30:00Z
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "20260401_0006"
down_revision = "20260320_0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("order_intent", sa.Column("position_instance_ref", sa.String(length=128), nullable=True))
    op.add_column("order_intent", sa.Column("setup_variant_id", sa.String(length=128), nullable=True))
    op.add_column("order_intent", sa.Column("execution_expression_id", sa.String(length=128), nullable=True))
    op.add_column("order_intent", sa.Column("tradable_expression_family", sa.String(length=64), nullable=True))
    op.add_column("order_intent", sa.Column("lifecycle_state", sa.String(length=64), nullable=True))
    op.add_column("order_intent", sa.Column("lifecycle_action", sa.String(length=32), nullable=True))
    op.add_column("order_intent", sa.Column("current_position_size_pct", sa.Numeric(8, 3), nullable=True))
    op.add_column("order_intent", sa.Column("carry_state_eligible", sa.Boolean(), nullable=True))
    op.add_column("order_intent", sa.Column("hard_flat_required", sa.Boolean(), nullable=True))
    op.create_index(
        "ix_order_intent_position_instance_ref",
        "order_intent",
        ["position_instance_ref"],
        unique=False,
    )
    op.create_index(
        "ix_order_intent_position_instance_created",
        "order_intent",
        ["position_instance_ref", "created_at"],
        unique=False,
    )

    op.create_table(
        "position_instance_snapshot",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("position_instance_ref", sa.String(length=128), nullable=False),
        sa.Column("symbol", sa.String(length=32), nullable=False),
        sa.Column("snapshot_ts", sa.DateTime(timezone=True), nullable=False),
        sa.Column("setup_variant_id", sa.String(length=128), nullable=False),
        sa.Column("execution_expression_id", sa.String(length=128), nullable=False),
        sa.Column("tradable_expression_family", sa.String(length=64), nullable=False),
        sa.Column("lifecycle_state", sa.String(length=64), nullable=False),
        sa.Column("lifecycle_action", sa.String(length=32), nullable=False),
        sa.Column("current_position_size_pct", sa.Numeric(8, 3), nullable=False),
        sa.Column("quantity", sa.Numeric(18, 6), nullable=False),
        sa.Column("average_price", sa.Numeric(18, 6), nullable=False),
        sa.Column("market_price", sa.Numeric(18, 6), nullable=False),
        sa.Column("market_value", sa.Numeric(18, 6), nullable=False),
        sa.Column("unrealized_pnl", sa.Numeric(18, 6), nullable=False),
        sa.Column("carry_state_eligible", sa.Boolean(), nullable=False),
        sa.Column("hard_flat_required", sa.Boolean(), nullable=False),
        sa.Column("source", sa.String(length=32), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_position_instance_snapshot_position_instance_ref",
        "position_instance_snapshot",
        ["position_instance_ref"],
        unique=False,
    )
    op.create_index(
        "ix_position_instance_snapshot_symbol",
        "position_instance_snapshot",
        ["symbol"],
        unique=False,
    )
    op.create_index(
        "ix_position_instance_snapshot_ref_ts",
        "position_instance_snapshot",
        ["position_instance_ref", "snapshot_ts"],
        unique=False,
    )
    op.create_index(
        "ix_position_instance_snapshot_symbol_ts",
        "position_instance_snapshot",
        ["symbol", "snapshot_ts"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_position_instance_snapshot_symbol_ts", table_name="position_instance_snapshot")
    op.drop_index("ix_position_instance_snapshot_ref_ts", table_name="position_instance_snapshot")
    op.drop_index(
        "ix_position_instance_snapshot_symbol",
        table_name="position_instance_snapshot",
    )
    op.drop_index(
        "ix_position_instance_snapshot_position_instance_ref",
        table_name="position_instance_snapshot",
    )
    op.drop_table("position_instance_snapshot")

    op.drop_index("ix_order_intent_position_instance_created", table_name="order_intent")
    op.drop_index("ix_order_intent_position_instance_ref", table_name="order_intent")
    op.drop_column("order_intent", "hard_flat_required")
    op.drop_column("order_intent", "carry_state_eligible")
    op.drop_column("order_intent", "current_position_size_pct")
    op.drop_column("order_intent", "lifecycle_action")
    op.drop_column("order_intent", "lifecycle_state")
    op.drop_column("order_intent", "tradable_expression_family")
    op.drop_column("order_intent", "execution_expression_id")
    op.drop_column("order_intent", "setup_variant_id")
    op.drop_column("order_intent", "position_instance_ref")
