"""Add refresh_tokens table

Revision ID: 9f2b1a8c3d4e
Revises: 85123a23519b
Create Date: 2026-10-18 23:38:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f2b1a8c3d4e'
down_revision: Union[str, Sequence[str], None] = '85123a23519b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'refresh_tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('revoked', sa.Boolean(), nullable=False, default=False),
        sa.ForeignKeyConstraint(['user_id'], ['im.users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        schema='im'
    )
    op.create_index(op.f('ix_im_refresh_tokens_token'), 'refresh_tokens', ['token'], unique=True, schema='im')
    op.create_index(op.f('ix_im_refresh_tokens_user_id'), 'refresh_tokens', ['user_id'], unique=False, schema='im')


def downgrade() -> None:
    op.drop_index(op.f('ix_im_refresh_tokens_user_id'), table_name='refresh_tokens', schema='im')
    op.drop_index(op.f('ix_im_refresh_tokens_token'), table_name='refresh_tokens', schema='im')
    op.drop_table('refresh_tokens', schema='im')

