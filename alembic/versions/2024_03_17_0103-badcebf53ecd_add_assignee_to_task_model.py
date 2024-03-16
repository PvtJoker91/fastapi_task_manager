"""Add assignee to task model

Revision ID: badcebf53ecd
Revises: dc800936eb63
Create Date: 2024-03-17 01:03:42.539512

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'badcebf53ecd'
down_revision: Union[str, None] = 'dc800936eb63'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('assignee_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'tasks', 'users', ['assignee_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tasks', type_='foreignkey')
    op.drop_column('tasks', 'assignee_id')
    # ### end Alembic commands ###
