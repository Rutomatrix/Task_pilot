"""create employees table

Revision ID: 833913e5d09f
Revises: c24ae23479b9
Create Date: 2025-11-14 14:43:53.631460
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY


# revision identifiers, used by Alembic.
revision: str = '833913e5d09f'
down_revision: Union[str, Sequence[str], None] = 'c24ae23479b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'employees',
        sa.Column('id', sa.Integer, primary_key=True, index=True),

        sa.Column('Emp_ID', sa.String, unique=True, nullable=False),
        sa.Column('Team_ID', sa.String),
        sa.Column('Name', sa.String),
        sa.Column('Role', sa.String),

        # ARRAY fields with DB-level empty array default
        sa.Column('Skillset', ARRAY(sa.String), server_default='{}'),
        sa.Column('Current_Tasks', ARRAY(sa.String), server_default='{}'),

        sa.Column('Status', sa.String),
        sa.Column('Comments', sa.Text),
        sa.Column('Email', sa.String, unique=True),

        # ⏱️ Timestamp fields
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )


def downgrade():
    op.drop_table('employees')
