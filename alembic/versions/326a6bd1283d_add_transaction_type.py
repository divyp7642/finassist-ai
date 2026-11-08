
"""add transaction type

Revision ID: 326a6bd1283d
Revises: 4d9d48d2b15a
Create Date: 2026-10-30 00:31:04.883295
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# Revision identifiers used by Alembic.
revision: str = "326a6bd1283d"

down_revision: Union[str, Sequence[str], None] = (
    "4d9d48d2b15a"
)

branch_labels: Union[str, Sequence[str], None] = None

depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add transaction_type to existing transactions."""

    op.add_column(
        "transactions",
        sa.Column(
            "transaction_type",
            sa.String(length=20),
            nullable=False,
            server_default="expense",
        ),
    )


def downgrade() -> None:
    """Remove transaction_type if migration is reversed."""

    op.drop_column(
        "transactions",
        "transaction_type",
    )
