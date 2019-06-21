"""add_language_in_post

Revision ID: 1eb00d6268af
Revises: e345871e2e89
Create Date: 2019-06-18 13:26:04.180877

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1eb00d6268af'
down_revision = 'e345871e2e89'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('language', sa.String(length=5), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'language')
    # ### end Alembic commands ###
