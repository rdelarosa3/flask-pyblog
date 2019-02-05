"""empty message

Revision ID: a5f69c0ad9fd
Revises: fa1f8d4c75a3
Create Date: 2019-02-05 02:54:29.767886

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5f69c0ad9fd'
down_revision = 'fa1f8d4c75a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('image_file', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'image_file')
    # ### end Alembic commands ###