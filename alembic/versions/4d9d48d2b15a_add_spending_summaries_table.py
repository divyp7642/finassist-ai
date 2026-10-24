
"""add spending summaries table

Revision ID: 4d9d48d2b15a
Revises: 0f9d6a49f734
Create Date: 2026-10-23 19:10:27.143307
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# Revision identifiers used by Alembic
revision: str = "4d9d48d2b15a"

down_revision: Union[str, Sequence[str], None] = (
    "0f9d6a49f734"
)

branch_labels: Union[str, Sequence[str], None] = None

depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the spending summaries table."""

    op.create_table(
        "spending_summaries",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "category",
            sa.String(length=50),
            nullable=False
        ),

        sa.Column(
            "total_amount",
            sa.Numeric(precision=12, scale=2),
            nullable=False
        ),

        sa.Column(
            "transaction_count",
            sa.Integer(),
            nullable=False
        ),

        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"]
        ),

        sa.PrimaryKeyConstraint("id"),

        sa.UniqueConstraint(
            "user_id",
            "category",
            name="uq_spending_summary_user_category"
        )
    )


def downgrade() -> None:
    """Remove the spending summaries table."""

    op.drop_table("spending_summaries")
