"""add isDiaspora column to property_listing table

Revision ID: 489d656e5881
Revises: 4210d67086fa
Create Date: 2023-07-03 10:53:59.006561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '489d656e5881'
down_revision = '4210d67086fa'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('propertyListings', sa.Column('isDiaspora', sa.Boolean(), nullable=False))


def downgrade():
    op.drop_column('propertyListings', 'isDiaspora')
