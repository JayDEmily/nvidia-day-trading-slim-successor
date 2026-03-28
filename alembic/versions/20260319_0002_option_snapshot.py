"""add option snapshot table

Revision ID: 20260319_0002
Revises: 20260318_0001
Create Date: 2026-03-19 12:35:00Z
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "20260319_0002"
down_revision = "20260318_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "option_snapshot",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("instrument_id", sa.Integer(), nullable=False),
        sa.Column("as_of_date", sa.Date(), nullable=False),
        sa.Column("expiry", sa.Date(), nullable=True),
        sa.Column("option_type", sa.String(length=8), nullable=False),
        sa.Column("strike", sa.Numeric(18, 6), nullable=False),
        sa.Column("bid", sa.Numeric(18, 6), nullable=True),
        sa.Column("ask", sa.Numeric(18, 6), nullable=True),
        sa.Column("last", sa.Numeric(18, 6), nullable=True),
        sa.Column("volume", sa.Integer(), nullable=True),
        sa.Column("open_interest", sa.Integer(), nullable=True),
        sa.Column("delta_change", sa.Numeric(18, 6), nullable=True),
        sa.Column("provenance", sa.String(length=64), nullable=False),
        sa.Column("confidence", sa.String(length=32), nullable=False),
        sa.Column("source_document", sa.String(length=255), nullable=False),
        sa.Column("source_pages", sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(["instrument_id"], ["instrument.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "instrument_id",
            "as_of_date",
            "expiry",
            "option_type",
            "strike",
            name="uq_option_snapshot_identity",
        ),
    )
    op.create_index(
        "ix_option_snapshot_surface",
        "option_snapshot",
        ["instrument_id", "as_of_date", "expiry", "option_type", "strike"],
        unique=False,
    )
    op.create_index(
        "ix_option_snapshot_option_type", "option_snapshot", ["option_type"], unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_option_snapshot_option_type", table_name="option_snapshot")
    op.drop_index("ix_option_snapshot_surface", table_name="option_snapshot")
    op.drop_table("option_snapshot")
