"""create projects table

Revision ID: 204ad66180ec
Revises: 8b5f88a57e0d
Create Date: 2025-11-11 11:54:51.616680
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY


# revision identifiers, used by Alembic.
revision: str = '204ad66180ec'
down_revision: Union[str, Sequence[str], None] = '8b5f88a57e0d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('Project_ID', sa.String, unique=True, nullable=False),
        sa.Column('Name', sa.String, nullable=False),
        sa.Column('Client_ID', ARRAY(sa.String), server_default='{}'),
        sa.Column('Description', sa.Text),
        sa.Column('Priority', sa.String),
        sa.Column('Deadline', sa.DateTime(timezone=True)),
        sa.Column('Status', sa.String),
        sa.Column('Linked_Inventory', ARRAY(sa.String), server_default='{}'),

        # ⏱️ Timestamps
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('projects')
