"""added mjm table

Revision ID: a305d93c6238
Revises: 7bf20ada100b
Create Date: 2021-01-26 17:44:21.434049

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "a305d93c6238"
down_revision = "7bf20ada100b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "mjm_alerts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("mjm_alerts", sa.Boolean(), nullable=True),
        sa.Column("platform", sa.String(length=60), nullable=True),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.Column(
            "json_response", postgresql.JSON(astext_type=sa.Text()), nullable=True
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_mjm_alerts_timestamp"), "mjm_alerts", ["timestamp"], unique=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_mjm_alerts_timestamp"), table_name="mjm_alerts")
    op.drop_table("mjm_alerts")
    # ### end Alembic commands ###