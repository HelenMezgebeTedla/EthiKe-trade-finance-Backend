"""Baseline existing schema

Revision ID: 20aed40b6cd9
Revises: c9dcc79d35a9
Create Date: 2026-10-04 22:18:12.436151

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20aed40b6cd9'
down_revision: Union[str, Sequence[str], None] = 'c9dcc79d35a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
