"""update_users

Revision ID: c92c7534fde3
Revises: 1a9e838411d2
Create Date: 2025-02-18 19:26:13.367563

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'c92c7534fde3'
down_revision: Union[str, None] = '1a9e838411d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('user_name', sa.String(length=120), nullable=False))
    op.drop_column('users', 'username')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', mysql.VARCHAR(length=120), nullable=False))
    op.drop_column('users', 'user_name')
    # ### end Alembic commands ###
