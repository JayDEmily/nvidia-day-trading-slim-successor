"""add raw option row contract fields

Revision ID: 20260403_0007
Revises: 20260401_0006
Create Date: 2026-04-03 14:30:00Z
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "20260403_0007"
down_revision = "20260401_0006"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("option_snapshot", sa.Column("iv", sa.Numeric(18, 6), nullable=True))
    op.add_column("option_snapshot", sa.Column("delta", sa.Numeric(18, 6), nullable=True))
    op.add_column("option_snapshot", sa.Column("gamma", sa.Numeric(18, 6), nullable=True))


def downgrade() -> None:
    op.drop_column("option_snapshot", "gamma")
    op.drop_column("option_snapshot", "delta")
    op.drop_column("option_snapshot", "iv")
