"""add favourite column to post table

Revision ID: 50c37ca59458
Revises: 29b084df7212
Create Date: 2022-08-17 03:22:43.249773

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50c37ca59458'
down_revision = '29b084df7212'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', 
                  sa.Column('favourites', 
                  sa.Boolean(), server_default= 'TRUE', nullable = False))
    pass

def downgrade() -> None:
    op.drop_column('posts','favourites')
    pass
