
"""add transaction created at

Revision ID: 098c079ff376
Revises: 326a6bd1283d
Create Date: 2026-10-30 15:17:41.611831
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# Revision identifiers used by Alembic.
revision: str = "098c079ff376"
down_revision: Union[str, Sequence[str], None] = "326a6bd1283d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add timestamps without losing existing transactions."""

    # Existing transactions have no recorded creation date.
    # Keep their timestamps NULL rather than inventing dates.
    op.add_column(
        "transactions",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    # New transactions automatically receive the current UTC time
    # from PostgreSQL.
    op.alter_column(
        "transactions",
        "created_at",
        server_default=sa.text("CURRENT_TIMESTAMP"),
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=True,
    )

    # Preserve idx_transactions_user_id.
    # No index changes are required.


def downgrade() -> None:
    """Remove the timestamp column if migration is reversed."""

    op.drop_column(
        "transactions",
        "created_at",
    )
