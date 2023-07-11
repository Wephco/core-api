"""database changes

Revision ID: c0e61c7974ac
Revises: 5d680f667edc
Create Date: 2023-07-11 10:56:50.461197

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0e61c7974ac'
down_revision = '5d680f667edc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'agents', ['name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'agents', type_='unique')
    # ### end Alembic commands ###
