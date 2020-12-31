"""empty message

Revision ID: be3c5579d26f
Revises: b95dcf100347
Create Date: 2020-12-30 17:29:21.345172

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "be3c5579d26f"
down_revision = "b95dcf100347"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_subscribers_first_name", table_name="subscribers")
    op.drop_index("ix_subscribers_last_name", table_name="subscribers")
    op.drop_column("subscribers", "first_name")
    op.drop_column("subscribers", "last_name")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "subscribers",
        sa.Column(
            "last_name", sa.VARCHAR(length=60), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "subscribers",
        sa.Column(
            "first_name", sa.VARCHAR(length=60), autoincrement=False, nullable=True
        ),
    )
    op.create_index(
        "ix_subscribers_last_name", "subscribers", ["last_name"], unique=False
    )
    op.create_index(
        "ix_subscribers_first_name", "subscribers", ["first_name"], unique=False
    )
    # ### end Alembic commands ###