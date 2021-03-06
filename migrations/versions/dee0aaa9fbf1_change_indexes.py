"""change indexes

Revision ID: dee0aaa9fbf1
Revises: cf8fc3da099a
Create Date: 2020-12-23 16:23:18.602788

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dee0aaa9fbf1'
down_revision = 'cf8fc3da099a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_book_genre'), 'book', ['genre'], unique=False)
    op.create_index(op.f('ix_book_title'), 'book', ['title'], unique=False)
    op.drop_index('ix_comment_datetime', table_name='comment')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_comment_datetime', 'comment', ['datetime'], unique=False)
    op.drop_index(op.f('ix_book_title'), table_name='book')
    op.drop_index(op.f('ix_book_genre'), table_name='book')
    # ### end Alembic commands ###
