"""creating a post table

Revision ID: 29b084df7212
Revises: 
Create Date: 2022-08-17 02:59:42.789019

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.sql.expression import null, text 


# revision identifiers, used by Alembic.
revision = '29b084df7212'
down_revision = None
branch_labels = None
depends_on = None

#handles changes
def upgrade() -> None:
    op.create_table('posts', 
                    sa.Column('id', sa.Integer(), primary_key = True, nullable = False),
                    sa.Column('title', sa.String(), nullable = False),
                    sa.Column('content', sa.String(), nullable = False),
                    sa.Column('published', sa.Boolean(), server_default= 'TRUE', nullable = False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable = False, server_default=text('now()'))
                    )
    pass
    
#handles deleteing changes 
def downgrade() -> None:
    op.drop_table("posts")
    pass
