"""Add is_admin flag to user table

Revision ID: 9bc4afe1b363
Revises: 26f04848f166
Create Date: 2025-07-29 20:13:25.541504
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '9bc4afe1b363'
down_revision: Union[str, None] = '26f04848f166'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add is_admin column to users.users table."""
    op.add_column(
        'users',
        sa.Column(
            'is_admin',
            sa.Boolean(),
            nullable=False,
            server_default=sa.text('false')
        ),
        schema='users'
    )



def downgrade() -> None:
    """Remove is_admin column from users.users table."""
    op.drop_column('users', 'is_admin', schema='users')
