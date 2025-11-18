"""create clients table

Revision ID: 1cfb644cec9d
Revises: 
Create Date: 2025-11-10 11:32:02.434604

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1cfb644cec9d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'clients',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('Client_ID', sa.String, unique=True, nullable=False),
        sa.Column('Client_Name', sa.String, nullable=False),
        sa.Column('Description', sa.Text),
        sa.Column('Type', sa.String),
        sa.Column('Status', sa.String),
        sa.Column('Active_Projects', sa.Integer, server_default='0'),

        # ⏱️ Timestamps
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('clients')
