"""added test field

Revision ID: 4088bc4409b5
Revises: f96af15f56af
Create Date: 2021-09-27 12:49:16.748761

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4088bc4409b5"
down_revision = "f96af15f56af"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("subscribers", sa.Column("test_field", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("subscribers", "test_field")
    # ### end Alembic commands ###
