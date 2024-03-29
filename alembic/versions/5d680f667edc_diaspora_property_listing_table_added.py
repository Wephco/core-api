"""diaspora property listing table added

Revision ID: 5d680f667edc
Revises: 4210d67086fa
Create Date: 2023-07-11 09:09:02.598548

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5d680f667edc'
down_revision = '4210d67086fa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('diasporaPropertyListings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('propertyType', sa.String(), nullable=False),
    sa.Column('propertyImages', postgresql.ARRAY(sa.String()), nullable=False),
    sa.Column('numberOfrooms', sa.Integer(), nullable=True),
    sa.Column('numberOfToilets', sa.Integer(), nullable=True),
    sa.Column('numberOfBathrooms', sa.Integer(), nullable=True),
    sa.Column('numberOfLivingRooms', sa.Integer(), nullable=True),
    sa.Column('numberOfKitchens', sa.Integer(), nullable=True),
    sa.Column('agentId', sa.Integer(), nullable=False),
    sa.Column('createdAt', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['agentId'], ['agents.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('diasporaPropertyListings')
    # ### end Alembic commands ###
