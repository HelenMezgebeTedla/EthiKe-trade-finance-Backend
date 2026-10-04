"""Baseline existing schema

Revision ID: 20aed40b6cd9
Revises: c9dcc79d35a9
Create Date: 2026-10-04 22:18:12.436151

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "20aed40b6cd9"
down_revision: str | Sequence[str] | None = "c9dcc79d35a9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""


def downgrade() -> None:
    """Downgrade schema."""
