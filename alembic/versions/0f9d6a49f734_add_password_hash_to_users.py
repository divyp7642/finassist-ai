"""Add password hash to users

Revision ID: 0f9d6a49f734
Revises: 4343773ea0b0
Create Date: 2026-10-15 07:46:15.284221

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0f9d6a49f734'
down_revision: Union[str, Sequence[str], None] = '4343773ea0b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "users",
        sa.Column(
            "password_hash",
            sa.String(length=255),
            nullable=True
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "password_hash")
