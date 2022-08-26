"""add user table

Revision ID: 24ebdcab61b0
Revises: 50c37ca59458
Create Date: 2022-08-26 10:45:37.657783

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.sql.expression import null, text 

# revision identifiers, used by Alembic.
revision = '24ebdcab61b0'
down_revision = '50c37ca59458'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', 
                    sa.Column('id', sa.Integer(), nullable = False),
                    sa.Column('email', sa.String(), nullable = False),
                    sa.Column('password', sa.String(), nullable = False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable = False, server_default=text('now()')),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
