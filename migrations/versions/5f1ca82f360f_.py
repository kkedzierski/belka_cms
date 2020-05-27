"""empty message

Revision ID: 5f1ca82f360f
Revises: 
Create Date: 2020-05-25 19:24:37.373074

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f1ca82f360f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('website', sa.Column('navbar_font_size', sa.String(length=200), nullable=True))
    op.add_column('website', sa.Column('navbar_font_style', sa.String(length=200), nullable=True))
    op.add_column('website', sa.Column('post_text_font_size', sa.String(length=200), nullable=True))
    op.add_column('website', sa.Column('post_text_font_style', sa.String(length=200), nullable=True))
    op.add_column('website', sa.Column('title_post_font_size', sa.String(length=200), nullable=True))
    op.add_column('website', sa.Column('title_post_font_style', sa.String(length=200), nullable=True))
    op.drop_column('website', 'font_style')
    op.drop_column('website', 'font_size')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('website', sa.Column('font_size', sa.VARCHAR(length=200), nullable=True))
    op.add_column('website', sa.Column('font_style', sa.VARCHAR(length=200), nullable=True))
    op.drop_column('website', 'title_post_font_style')
    op.drop_column('website', 'title_post_font_size')
    op.drop_column('website', 'post_text_font_style')
    op.drop_column('website', 'post_text_font_size')
    op.drop_column('website', 'navbar_font_style')
    op.drop_column('website', 'navbar_font_size')
    # ### end Alembic commands ###