"""empty message

Revision ID: 70848d45a98d
Revises: 
Create Date: 2023-10-18 09:37:54.075344

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70848d45a98d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=2055), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('chat_members',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user', sa.Integer(), nullable=False),
    sa.Column('chat', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender', sa.Integer(), nullable=False),
    sa.Column('chat', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=1024), nullable=False),
    sa.Column('is_read', sa.Boolean(), nullable=False),
    sa.Column('send_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('message')
    op.drop_table('chat_members')
    op.drop_table('chat')
    # ### end Alembic commands ###
