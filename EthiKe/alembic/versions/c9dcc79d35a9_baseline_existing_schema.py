"""Baseline existing schema

Revision ID: c9dcc79d35a9
Revises:
Create Date: 2026-10-04 22:17:36.905503

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "c9dcc79d35a9"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""


def downgrade() -> None:
    """Downgrade schema."""
