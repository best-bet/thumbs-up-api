"""initial migration

Revision ID: 984145c7e944
Revises: 
Create Date: 2019-03-27 02:09:17.242301

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '984145c7e944'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Items',
    sa.Column('id', sa.Text(), nullable=False),
    sa.Column('project_title', sa.Text(), nullable=False),
    sa.Column('total_num', sa.Integer(), nullable=False),
    sa.Column('next', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Options',
    sa.Column('id', sa.Text(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', src.database.guid.GUID(), nullable=False),
    sa.Column('title', sa.Text(), nullable=False),
    sa.Column('email', sa.Text(), nullable=False),
    sa.Column('phone', sa.Text(), nullable=False),
    sa.Column('sms', sa.Text(), nullable=True),
    sa.Column('verification_code', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Projects')
    op.drop_table('Options')
    op.drop_table('Items')
    # ### end Alembic commands ###
