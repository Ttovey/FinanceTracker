"""empty message

Revision ID: 7d004cefd497
Revises: ca62cde621f4
Create Date: 2021-11-01 10:16:17.760497

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d004cefd497'
down_revision = 'ca62cde621f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('asset', sa.Column('quantity', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('asset', 'quantity')
    # ### end Alembic commands ###
