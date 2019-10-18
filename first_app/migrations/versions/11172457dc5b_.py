"""empty message

Revision ID: 11172457dc5b
Revises: 
Create Date: 2019-10-18 19:33:36.818866

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11172457dc5b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('my_model', sa.Column('my_field5', sa.String(length=50), nullable=True))
    op.create_unique_constraint(None, 'my_model', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'my_model', type_='unique')
    op.drop_column('my_model', 'my_field5')
    # ### end Alembic commands ###
