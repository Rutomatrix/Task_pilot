"""create teams table

Revision ID: 8b5f88a57e0d
Revises: 1cfb644cec9d
Create Date: 2025-11-11 10:24:23.264978

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b5f88a57e0d'
down_revision: Union[str, Sequence[str], None] = '1cfb644cec9d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'teams',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('Team_ID', sa.String, unique=True, nullable=False),
        sa.Column('Category', sa.String, nullable=False),

        # ⏱️ Timestamps
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('teams')
