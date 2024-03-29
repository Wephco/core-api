"""new_database_changes

Revision ID: 3579407d25f5
Revises: 3f6be6fc58a9
Create Date: 2023-07-20 19:36:30.750403

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3579407d25f5'
down_revision = '3f6be6fc58a9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('consultations', 'service',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.add_column('propertyRequests', sa.Column('preferredService', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('propertyRequests', 'preferredService')
    op.alter_column('consultations', 'service',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
