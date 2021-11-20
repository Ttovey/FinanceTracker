"""empty message

Revision ID: 461d45c29c37
Revises: 342320cea269
Create Date: 2021-11-19 13:45:28.954343

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '461d45c29c37'
down_revision = '342320cea269'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('networth', 'date',
               existing_type=sa.DATETIME(),
               nullable=False)
    op.alter_column('networth', 'total',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('networth', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('networth', sa.Column('id', sa.INTEGER(), nullable=False))
    op.alter_column('networth', 'total',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('networth', 'date',
               existing_type=sa.DATETIME(),
               nullable=True)
    # ### end Alembic commands ###
