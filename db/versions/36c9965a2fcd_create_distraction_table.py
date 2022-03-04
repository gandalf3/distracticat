"""create distraction table

Revision ID: 36c9965a2fcd
Revises: 
Create Date: 2022-03-04 02:20:35.785298

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "36c9965a2fcd"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "distraction",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("guild_id", sa.Integer, nullable=False),
        sa.Column("timestamp", sa.Integer),
        sa.Column("description", sa.String),
    )


def downgrade():
    op.drop_table("distraction")
