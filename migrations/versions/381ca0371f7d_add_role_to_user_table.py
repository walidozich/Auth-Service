"""add role to user table

Revision ID: 381ca0371f7d
Revises: e2566080a925
Create Date: 2025-12-04 23:57:42.085988

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '381ca0371f7d'
down_revision: Union[str, Sequence[str], None] = 'e2566080a925'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

user_role_enum = sa.Enum('ADMIN', 'USER', name='userrole')

def upgrade() -> None:
    """Upgrade schema."""
    user_role_enum.create(op.get_bind())
    op.add_column('users', sa.Column('role', user_role_enum, nullable=False, server_default='USER'))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'role')
    user_role_enum.drop(op.get_bind())
