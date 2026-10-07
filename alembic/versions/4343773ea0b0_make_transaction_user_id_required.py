"""make transaction user id required

Revision ID: 4343773ea0b0
Revises: f2ad8cfb6c81
Create Date: 2026-10-06 17:35:54.430370

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4343773ea0b0"
down_revision: Union[str, Sequence[str], None] = "f2ad8cfb6c81"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "transactions",
        "user_id",
        existing_type=sa.Integer(),
        nullable=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "transactions",
        "user_id",
        existing_type=sa.Integer(),
        nullable=True
    )