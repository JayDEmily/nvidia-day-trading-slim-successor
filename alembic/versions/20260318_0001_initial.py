"""initial backbone

Revision ID: 20260318_0001
Revises: None
Create Date: 2026-03-18 21:40:00Z
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20260318_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "instrument",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("symbol", sa.String(length=32), nullable=False),
        sa.Column("asset_class", sa.String(length=32), nullable=False),
        sa.Column("venue", sa.String(length=32), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_instrument_symbol", "instrument", ["symbol"], unique=True)

    op.create_table(
        "bar_1m",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("instrument_id", sa.Integer(), nullable=False),
        sa.Column("ts_utc", sa.DateTime(timezone=True), nullable=False),
        sa.Column("open", sa.Numeric(18, 6), nullable=False),
        sa.Column("high", sa.Numeric(18, 6), nullable=False),
        sa.Column("low", sa.Numeric(18, 6), nullable=False),
        sa.Column("close", sa.Numeric(18, 6), nullable=False),
        sa.Column("volume", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["instrument_id"], ["instrument.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("instrument_id", "ts_utc", name="uq_bar_1m_instrument_ts"),
    )
    op.create_index("ix_bar_1m_instrument_ts", "bar_1m", ["instrument_id", "ts_utc"], unique=False)

    op.create_table(
        "research_note",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("symbol", sa.String(length=32), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("thesis", sa.Text(), nullable=False),
        sa.Column("body_md", sa.Text(), nullable=False),
        sa.Column("tags_json", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_research_note_symbol", "research_note", ["symbol"], unique=False)

    op.create_table(
        "evaluation_run",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("symbol", sa.String(length=32), nullable=False),
        sa.Column("module_id", sa.String(length=128), nullable=False),
        sa.Column("module_name", sa.String(length=255), nullable=False),
        sa.Column("module_class", sa.String(length=32), nullable=False),
        sa.Column("verdict", sa.String(length=16), nullable=False),
        sa.Column("score", sa.Numeric(8, 6), nullable=False),
        sa.Column("requested_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("input_json", sa.Text(), nullable=False),
        sa.Column("output_json", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_evaluation_run_module_created", "evaluation_run", ["module_id", "created_at"], unique=False)
    op.create_index("ix_evaluation_run_symbol", "evaluation_run", ["symbol"], unique=False)
    op.create_index("ix_evaluation_run_module_id", "evaluation_run", ["module_id"], unique=False)
    op.create_index("ix_evaluation_run_verdict", "evaluation_run", ["verdict"], unique=False)

    op.create_table(
        "module_spec",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("module_id", sa.String(length=128), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("module_class", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("thesis", sa.Text(), nullable=False),
        sa.Column("required_inputs_json", sa.Text(), nullable=False),
        sa.Column("parameters_json", sa.Text(), nullable=False),
        sa.Column("notes_md", sa.Text(), nullable=False),
        sa.Column("source_refs_json", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_module_spec_module_created", "module_spec", ["module_id", "created_at"], unique=False)
    op.create_index("ix_module_spec_module_id", "module_spec", ["module_id"], unique=False)
    op.create_index("ix_module_spec_status", "module_spec", ["status"], unique=False)

    op.create_table(
        "promotion_decision",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("module_id", sa.String(length=128), nullable=False),
        sa.Column("from_status", sa.String(length=32), nullable=False),
        sa.Column("to_status", sa.String(length=32), nullable=False),
        sa.Column("decision_reason", sa.Text(), nullable=False),
        sa.Column("evaluation_ids_json", sa.Text(), nullable=False),
        sa.Column("evidence_refs_json", sa.Text(), nullable=False),
        sa.Column("approved_by", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_promotion_decision_module_created", "promotion_decision", ["module_id", "created_at"], unique=False)
    op.create_index("ix_promotion_decision_module_id", "promotion_decision", ["module_id"], unique=False)
    op.create_index("ix_promotion_decision_from_status", "promotion_decision", ["from_status"], unique=False)
    op.create_index("ix_promotion_decision_to_status", "promotion_decision", ["to_status"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_promotion_decision_to_status", table_name="promotion_decision")
    op.drop_index("ix_promotion_decision_from_status", table_name="promotion_decision")
    op.drop_index("ix_promotion_decision_module_id", table_name="promotion_decision")
    op.drop_index("ix_promotion_decision_module_created", table_name="promotion_decision")
    op.drop_table("promotion_decision")

    op.drop_index("ix_module_spec_status", table_name="module_spec")
    op.drop_index("ix_module_spec_module_id", table_name="module_spec")
    op.drop_index("ix_module_spec_module_created", table_name="module_spec")
    op.drop_table("module_spec")

    op.drop_index("ix_evaluation_run_verdict", table_name="evaluation_run")
    op.drop_index("ix_evaluation_run_module_id", table_name="evaluation_run")
    op.drop_index("ix_evaluation_run_symbol", table_name="evaluation_run")
    op.drop_index("ix_evaluation_run_module_created", table_name="evaluation_run")
    op.drop_table("evaluation_run")

    op.drop_index("ix_research_note_symbol", table_name="research_note")
    op.drop_table("research_note")

    op.drop_index("ix_bar_1m_instrument_ts", table_name="bar_1m")
    op.drop_table("bar_1m")

    op.drop_index("ix_instrument_symbol", table_name="instrument")
    op.drop_table("instrument")
