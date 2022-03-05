"""add author and message id columns

Revision ID: 6a2257d1e1b8
Revises: 298e8829acb6
Create Date: 2022-03-04 17:05:00.779861

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a2257d1e1b8'
down_revision = '298e8829acb6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('distraction', sa.Column('author_id', sa.Integer(), nullable=True))
    op.add_column('distraction', sa.Column('message_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('distraction', 'message_id')
    op.drop_column('distraction', 'author_id')
    # ### end Alembic commands ###