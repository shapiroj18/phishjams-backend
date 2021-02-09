"""added telegram chat id

Revision ID: 140c8f7246ce
Revises: c053ad306e89
Create Date: 2021-02-09 09:45:34.199932

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "140c8f7246ce"
down_revision = "c053ad306e89"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "mjm_alerts", sa.Column("telegram_chat_id", sa.Integer(), nullable=True)
    )
    op.add_column(
        "subscribers", sa.Column("telegram_chat_id", sa.Integer(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("subscribers", "telegram_chat_id")
    op.drop_column("mjm_alerts", "telegram_chat_id")
    # ### end Alembic commands ###
