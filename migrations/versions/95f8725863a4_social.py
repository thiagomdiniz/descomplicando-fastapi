"""social

Revision ID: 95f8725863a4
Revises: a46a05f95ae4
Create Date: 2024-05-27 05:54:14.254488

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '95f8725863a4'
down_revision: Union[str, None] = 'a46a05f95ae4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('social', 'from_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('social', 'to_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('social', 'to_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('social', 'from_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
