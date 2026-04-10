"""add options flow history observation store

Revision ID: 20260409_0008
Revises: 20260403_0007
Create Date: 2026-04-09 18:00:00Z
"""

from __future__ import annotations

import sqlalchemy as sa

from alembic import op

revision = "20260409_0008"
down_revision = "20260403_0007"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "options_flow_history_observation",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("symbol", sa.String(length=32), nullable=False),
        sa.Column("observed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("chain_ts", sa.DateTime(timezone=True), nullable=False),
        sa.Column("front_expiry", sa.Date(), nullable=False),
        sa.Column("next_expiry", sa.Date(), nullable=False),
        sa.Column("partiality_state", sa.String(length=32), nullable=False),
        sa.Column("record_completeness_flag", sa.Boolean(), nullable=False),
        sa.Column("raw_source_authority", sa.String(length=64), nullable=False),
        sa.Column("lineage_json", sa.Text(), nullable=False),
        sa.Column("derived_state_json", sa.Text(), nullable=False),
        sa.Column("front_expiry_rows_json", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("next_expiry_rows_json", sa.Text(), nullable=False, server_default="[]"),
        sa.UniqueConstraint("symbol", "observed_at", name="uq_options_flow_history_observation_identity"),
    )
    op.create_index(
        "ix_options_flow_history_observation_symbol_observed",
        "options_flow_history_observation",
        ["symbol", "observed_at"],
    )
    op.create_index(
        "ix_options_flow_history_observation_symbol_chain",
        "options_flow_history_observation",
        ["symbol", "chain_ts"],
    )


def downgrade() -> None:
    op.drop_index("ix_options_flow_history_observation_symbol_chain", table_name="options_flow_history_observation")
    op.drop_index("ix_options_flow_history_observation_symbol_observed", table_name="options_flow_history_observation")
    op.drop_table("options_flow_history_observation")
