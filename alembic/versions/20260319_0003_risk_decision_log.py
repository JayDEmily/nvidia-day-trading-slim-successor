"""add risk decision log table

Revision ID: 20260319_0003
Revises: 20260319_0002
Create Date: 2026-03-19 13:35:00Z
"""

from __future__ import annotations

import sqlalchemy as sa

from alembic import op

revision = "20260319_0003"
down_revision = "20260319_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "risk_decision_log",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("symbol", sa.String(length=32), nullable=False),
        sa.Column("module_id", sa.String(length=128), nullable=False),
        sa.Column("action", sa.String(length=16), nullable=False),
        sa.Column("requested_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("input_json", sa.Text(), nullable=False),
        sa.Column("output_json", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_risk_decision_log_symbol", "risk_decision_log", ["symbol"], unique=False)
    op.create_index(
        "ix_risk_decision_log_module_id", "risk_decision_log", ["module_id"], unique=False
    )
    op.create_index("ix_risk_decision_log_action", "risk_decision_log", ["action"], unique=False)
    op.create_index(
        "ix_risk_decision_log_module_created",
        "risk_decision_log",
        ["module_id", "created_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_risk_decision_log_module_created", table_name="risk_decision_log")
    op.drop_index("ix_risk_decision_log_action", table_name="risk_decision_log")
    op.drop_index("ix_risk_decision_log_module_id", table_name="risk_decision_log")
    op.drop_index("ix_risk_decision_log_symbol", table_name="risk_decision_log")
    op.drop_table("risk_decision_log")
