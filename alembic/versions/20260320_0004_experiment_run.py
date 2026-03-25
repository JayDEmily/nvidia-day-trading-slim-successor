"""add experiment run table

Revision ID: 20260320_0004
Revises: 20260319_0003
Create Date: 2026-03-20 15:05:00Z
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "20260320_0004"
down_revision = "20260319_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "experiment_run",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("symbol", sa.String(length=32), nullable=False),
        sa.Column("module_id", sa.String(length=128), nullable=False),
        sa.Column("experiment_type", sa.String(length=32), nullable=False),
        sa.Column("config_name", sa.String(length=128), nullable=False),
        sa.Column("requested_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ranking_score", sa.Numeric(precision=8, scale=6), nullable=True),
        sa.Column("input_json", sa.Text(), nullable=False),
        sa.Column("output_json", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_experiment_run_symbol", "experiment_run", ["symbol"], unique=False)
    op.create_index("ix_experiment_run_module_id", "experiment_run", ["module_id"], unique=False)
    op.create_index("ix_experiment_run_experiment_type", "experiment_run", ["experiment_type"], unique=False)
    op.create_index(
        "ix_experiment_run_config_name",
        "experiment_run",
        ["config_name"],
        unique=False,
    )
    op.create_index(
        "ix_experiment_run_module_created",
        "experiment_run",
        ["module_id", "created_at"],
        unique=False,
    )
    op.create_index(
        "ix_experiment_run_module_type_created",
        "experiment_run",
        ["module_id", "experiment_type", "created_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_experiment_run_module_type_created", table_name="experiment_run")
    op.drop_index("ix_experiment_run_module_created", table_name="experiment_run")
    op.drop_index("ix_experiment_run_config_name", table_name="experiment_run")
    op.drop_index("ix_experiment_run_experiment_type", table_name="experiment_run")
    op.drop_index("ix_experiment_run_module_id", table_name="experiment_run")
    op.drop_index("ix_experiment_run_symbol", table_name="experiment_run")
    op.drop_table("experiment_run")
